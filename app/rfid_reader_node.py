from homie.node import HomieNode
from homie.constants import STRING
from homie.property import HomieProperty
from rfid_reader import RfidReader
from uasyncio import create_task, sleep_ms
from door_controller_node import DoorControllerNode
from tag_store import TagStore

class RfidReaderNode(HomieNode):

    def __init__(self, doorController: DoorControllerNode, tagStore: TagStore):
        super().__init__(id="RfidReader", name="RfidReader", type="Controller")

        self.lastValidTagProperty = HomieProperty(
            id="lastValidTag",
            name="lastValidTag",
            datatype=STRING,
            settable=False,
            pub_on_upd=True
        )
        self.add_property(self.lastValidTagProperty)              

        self.lastInvalidTagProperty = HomieProperty(
            id="lastInvalidTag",
            name="lastInvalidTag",
            datatype=STRING,
            settable=False,
            pub_on_upd=True
        )
        self.add_property(self.lastInvalidTagProperty)              

        self.tagStore = tagStore
        self.reader = RfidReader()
        self.doorController = doorController

        create_task(self.loop())


    async def loop(self):
        while True:
            tag = await self.readTag()
            if (self.tagStore.isValidTag(tag)):
                self.lastValidTagProperty.value = tag
                await self.doorController.unlock()
            else:
                self.lastInvalidTagProperty.value = tag
            await sleep_ms(500)

    async def readTag(self):
        return await self.reader.readTag()


