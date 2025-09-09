# MicroPython MQTT simple client
# Source: micropython-lib (MIT License)

import usocket as socket
import ustruct as struct
from ubinascii import hexlify

class MQTTException(Exception):
    pass

class MQTTClient:

    def __init__(self, client_id, server, port=0, user=None, password=None,
                 keepalive=0, ssl=False, ssl_params={}):
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.server = server
        self.port = port
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.sock = None
        self.cb = None
        self.pid = 0
        self.rcv_pids = {}

    def _send_str(self, s):
        self.sock.write(struct.pack("!H", len(s)))
        self.sock.write(s)

    def _recv_len(self):
        n = 0
        sh = 0
        while 1:
            b = self.sock.read(1)[0]
            n |= (b & 0x7f) << sh
            if not b & 0x80:
                return n
            sh += 7

    def set_callback(self, f):
        self.cb = f

    def connect(self, clean_session=True):
        addr = socket.getaddrinfo(self.server, self.port)[0][-1]
        self.sock = socket.socket()
        self.sock.connect(addr)
        if self.ssl:
            import ussl
            self.sock = ussl.wrap_socket(self.sock, **self.ssl_params)

        premsg = bytearray(b"\x10\0\0\0\0\0")
        msg = bytearray(b"\x04MQTT\x04\x02\0\0")
        sz = 10 + 2 + len(self.client_id)
        msg[6] = clean_session << 1
        if self.user is not None:
            sz += 2 + len(self.user) + 2 + len(self.pswd)
            msg[6] |= 0xC0
        if self.keepalive:
            msg[7] |= self.keepalive >> 8
            msg[8] |= self.keepalive & 0xFF
        i = 1
        while sz > 0x7f:
            premsg[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        premsg[i] = sz
        self.sock.write(premsg, i+1)
        self.sock.write(msg)
        self._send_str(self.client_id)
        if self.user is not None:
            self._send_str(self.user)
            self._send_str(self.pswd)
        resp = self.sock.read(4)
        if resp[0] != 0x20 or resp[1] != 0x02:
            raise MQTTException("CONNACK error")
        if resp[3] != 0:
            raise MQTTException(resp[3])
        return resp[2] & 1

    def disconnect(self):
        self.sock.write(b"\xe0\0")
        self.sock.close()

    def ping(self):
        self.sock.write(b"\xc0\0")

    def publish(self, topic, msg, retain=False, qos=0):
        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= qos << 1 | retain
        sz = 2 + len(topic) + len(msg)
        if qos > 0:
            sz += 2
        i = 1
        while sz > 0x7f:
            pkt[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        pkt[i] = sz
        self.sock.write(pkt, i+1)
        self._send_str(topic)
        if qos > 0:
            self.pid += 1
            pid = self.pid
            struct.pack_into("!H", pkt, 0, pid)
            self.sock.write(pkt, 2)
        self.sock.write(msg)
        if qos == 1:
            while 1:
                op = self.wait_msg()
                if op == 0x40:
                    sz = self.sock.read(1)
                    rcv_pid = struct.unpack("!H", self.sock.read(2))[0]
                    if pid == rcv_pid:
                        return
        elif qos == 2:
            raise NotImplementedError()

    def subscribe(self, topic, qos=0):
        pkt = bytearray(b"\x82\0\0\0")
        sz = 2 + 2 + len(topic) + 1
        i = 1
        while sz > 0x7f:
            pkt[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        pkt[i] = sz
        self.sock.write(pkt, i+1)
        self.pid += 1
        pid = self.pid
        struct.pack_into("!H", pkt, 0, pid)
        self.sock.write(pkt, 2)
        self._send_str(topic)
        self.sock.write(bytes([qos]))
        while 1:
            op = self.wait_msg()
            if op == 0x90:
                resp = self.sock.read(4)
                if resp[1] != pid:
                    continue
                if resp[3] == 0x80:
                    raise MQTTException("SUBACK failed")
                return

    def wait_msg(self):
        res = self.sock.read(1)
        if res is None:
            return None
        if res == b"":
            raise OSError(-1)
        if res == b"\xd0":
            self.sock.read(1)
            return None
        if res == b"\x40":
            self.sock.read(3)
            return 0x40
        if res[0] & 0xf0 != 0x30:
            return res[0]
        sz = self._recv_len()
        topic_len = struct.unpack("!H", self.sock.read(2))[0]
        topic = self.sock.read(topic_len)
        sz -= topic_len + 2
        if res[0] & 6:
            pid = struct.unpack("!H", self.sock.read(2))[0]
            sz -= 2
        msg = self.sock.read(sz)
        if self.cb:
            self.cb(topic, msg)
        return res[0]

    def check_msg(self):
        self.sock.setblocking(False)
        try:
            return self.wait_msg()
        except OSError:
            pass
        finally:
            self.sock.setblocking(True)
