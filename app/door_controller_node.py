from homie.node import HomieNode
from homie.constants import BOOLEAN
from homie.property import HomieProperty
from machine import Pin
from uasyncio import sleep_ms, create_task

class DoorControllerNode(HomieNode):

    DOOR_OPEN_TIME_IN_MS = 500

    def __init__(self):
        super().__init__(id="DoorController", name="DoorController", type="Controller")

        self.contactPin = Pin(5, Pin.IN, Pin.PULL_UP)
        self.contactPin.irq(lambda p: self.contactOpen, Pin.IRQ_FALLING)
        self.contactPin.irq(lambda p: self.contactClose, Pin.IRQ_RISING)
        
        self.openDoorPin = Pin(2, Pin.OUT)

        self.lockStateProperty = HomieProperty(
            id="lockState",
            name="lockState",
            datatype=BOOLEAN,
            settable=False
        )
        self.add_property(self.lockStateProperty)        

        self.unlockProperty = HomieProperty(
            id="unlock",
            name="unlock",
            datatype=BOOLEAN,
            settable=True,
            on_message=lambda t: create_task(self.unlock)
        )
        self.add_property(self.unlockProperty)        

    async def unlock(self):
        self.openDoorPin.on()
        await sleep_ms(self.DOOR_OPEN_TIME_IN_MS)
        self.openDoorPin.off()

    def contactOpen(self, pin: Pin):
        self.lockStateProperty.value = False

    def contactClose(self, pin: Pin):
        self.lockStateProperty.value = True
