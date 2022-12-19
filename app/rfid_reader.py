from uasyncio import sleep_ms
from machine import I2C, Pin

class RfidReader: 

    def __init__(self):
        self.i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100_000)

        # detect Nano Leser 9 and read firmware and hardware version
        firmwareVersion = int.from_bytes(self.i2c.readfrom_mem(0x0C, 0xA0, 1), "big")
        if (firmwareVersion > 0 and firmwareVersion < 256):
            hardwareVersion = int.from_bytes(self.i2c.readfrom_mem(0x0C, 0xA2, 1), "big")
            if (hardwareVersion > 0 and hardwareVersion < 256):
                print("Nano Leser 9 detected!")
                print("Hardware version: %d" % hardwareVersion)
                print("Firmware version: %d" % firmwareVersion)

    async def readTag(self):
        while True: 
            # initiate tag reading
            self.i2c.readfrom_mem(0x0C, 0xA6, 1)

            # read tag ID length
            tagUUIDLen = int.from_bytes(self.i2c.readfrom_mem(0x0C, 0xBF, 1), "big")
            while tagUUIDLen == 0xFF and not tagUUIDLen == 0x00:
                await sleep_ms(2)
                tagUUIDLen = int.from_bytes(self.i2c.readfrom_mem(0x0C, 0xBF, 1), "big")

            # read tag ID
            if tagUUIDLen != 0:
                print("Tag detected! Length: %d" % tagUUIDLen)

                uuid=[]
                for i in range(tagUUIDLen):
                    uuid.append(int.from_bytes(self.i2c.readfrom_mem(0x0C, 0xB0 + i, 1), "big"))
                
                tagID = ''.join("%02x" % x for x in uuid)
                print("detected tag: " + tagID)
                return tagID

            await sleep_ms(500)
    
