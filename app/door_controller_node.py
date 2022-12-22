from homie.node import HomieNode
from homie.constants import BOOLEAN
from homie.property import HomieProperty
from machine import Pin
from uasyncio import sleep_ms, create_task

class DoorControllerNode(HomieNode):

    DOOR_OPEN_TIME_IN_MS = 1000

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
            on_message=self.onUnlockMessage
        )
        self.add_property(self.unlockProperty)     

    def onUnlockMessage(self, topic, payload, retained):   
        print("message received")  
        unlock = bool(payload)
        if (unlock is True):
            print("unlock!")
            self.unlock()

    async def unlock(self):
        self.unlockProperty.value = True
        self.openDoorPin.on()
        await sleep_ms(self.DOOR_OPEN_TIME_IN_MS)
        self.openDoorPin.off()
        self.unlockProperty.value = False

    def contactOpen(self, pin: Pin):
        self.lockStateProperty.value = False

    def contactClose(self, pin: Pin):
        self.lockStateProperty.value = True
