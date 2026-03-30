from mfrc522 import MFRC522

# refer to https://microcontrollerslab.com/raspberry-pi-pico-rfid-rc522-micropython/ to see associated pin connections

class RFID:
    def __init__(self, spi, sck, miso, mosi, cs, rst, scanned):
        self.reader = MFRC522(spi_id=spi,sck=sck,miso=miso,mosi=mosi,cs=cs,rst=rst)
        self.scanned = scanned # scanned can be later reassigned with another function
        print("RFID Read Ready...")

    def update(self):
        self.reader.init()
        (stat, tag_type) = self.reader.request(self.reader.REQIDL)
        if stat == self.reader.OK:
            (stat, uid) = self.reader.SelectTagSN()
            if stat == self.reader.OK:
                card = int.from_bytes(bytes(uid),"little",False)
                self.scanned(card)
