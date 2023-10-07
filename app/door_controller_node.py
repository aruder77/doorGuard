from homie.node import HomieNode
from homie.constants import BOOLEAN
from homie.property import HomieProperty
from machine import Pin, PWM
from uasyncio import sleep_ms, create_task, ThreadSafeFlag


class DoorControllerNode(HomieNode):
    DOOR_OPEN_TIME_IN_MS = 1000

    def __init__(self):
        super().__init__(id="DoorController", name="DoorController", type="Controller")

        self.contactPin = Pin(5, Pin.IN, Pin.PULL_UP)
        self.reedPin = Pin(26, Pin.IN, Pin.PULL_UP)
        self.pipPadPin = Pin(27, Pin.IN, Pin.PULL_UP)
        self.openDoorPin = Pin(2, Pin.OUT)
        self.buzzerPin = Pin(3, Pin.OUT)

        self.buzzerPwm = PWM(self.buzzerPin)
        self.buzzerPwm.freq(4000)

        self.unlockFlag = ThreadSafeFlag()

        self.lockStateProperty = HomieProperty(
            id="lockState",
            name="lockState",
            datatype=BOOLEAN,
            settable=False,
            pub_on_upd=False,
            default="true"
        )
        self.add_property(self.lockStateProperty)

        self.pinPadStateProperty = HomieProperty(
            id="pipPadContact",
            name="pinPadContact",
            datatype=BOOLEAN,
            settable=False,
            pub_on_upd=False,
            default="false"
        )
        self.add_property(self.pinPadStateProperty)

        self.reedStateProperty = HomieProperty(
            id="reedState",
            name="reedState",
            datatype=BOOLEAN,
            settable=False,
            pub_on_upd=False,
            default="false"
        )
        self.add_property(self.reedStateProperty)

        self.unlockProperty = HomieProperty(
            id="unlock",
            name="unlock",
            datatype=BOOLEAN,
            settable=True,
            default="false",
            on_message=self.onUnlockMessage,
            pub_on_upd=False,
            retained=False
        )
        self.add_property(self.unlockProperty)

        self.buzzerProperty = HomieProperty(
            id="buzzer",
            name="buzzer",
            datatype=BOOLEAN,
            settable=True,
            default="false",
            on_message=self.onBuzzerMessage,
            pub_on_upd=False,
            retained=False
        )
        self.add_property(self.buzzerProperty)

        create_task(self.unlockLoop())
        create_task(self.lockStateLoop())

    async def unlockLoop(self):
        while True:
            print("scanning for tag...")
            await self.unlockFlag.wait()
            await create_task(self.unlock())
            await sleep_ms(self.DOOR_OPEN_TIME_IN_MS)

    def onUnlockMessage(self, topic, payload, retained):
        self.unlockFlag.set()

    def onBuzzerMessage(self, topic, payload, retained):
        if payload == "true":
            self.buzzerPwm.duty_u16(32000)
        else:
            self.buzzerPwm.deinit()

    async def unlock(self):
        self.unlockProperty.value = "true"
        self.openDoorPin.on()
        await sleep_ms(self.DOOR_OPEN_TIME_IN_MS)
        self.openDoorPin.off()
        self.unlockProperty.value = "false"

    async def lockStateLoop(self):
        while True:
            if self.contactPin.value() == 1:
                self.lockStateProperty.value = "false"
            else:
                self.lockStateProperty.value = "true"

            if self.reedPin.value() == 1:
                self.reedStateProperty.value = "true"
            else:
                self.reedStateProperty.value = "false"

            if self.pipPadPin.value() == 1:
                self.pinPadStateProperty.value = "true"
            else:
                self.pinPadStateProperty.value = "false"

            await sleep_ms(100)
