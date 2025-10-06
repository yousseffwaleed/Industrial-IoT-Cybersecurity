from pirc522 import RFID
import time

rdr = RFID()  # uses pigpio daemon (pigpiod)
print("Hold a tag near the reader (Ctrl+C to exit)")
try:
    while True:
        rdr.wait_for_tag()
        (err, tag_type) = rdr.request()
        if not err:
            (err, uid) = rdr.anticoll()
            if not err:
                print("UID:", uid)
                if rdr.select_tag(uid) == 0:
                    # Example: read data block 8
                    (err, data) = rdr.read(8)
                    if not err:
                        print("Block 8:", data)
                rdr.stop_crypto()
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    rdr.cleanup()
