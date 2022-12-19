from homie.node import HomieNode
from rfid_reader import RfidReader
from uasyncio import create_task
from door_controller_node import DoorControllerNode
from tag_store import TagStore

class RfidReaderNode(HomieNode):

    def __init__(self, doorController: DoorControllerNode):
        super().__init__(id="RfidReader", name="RfidReader", type="Controller")

        self.tagStore = TagStore()
        self.reader = RfidReader()
        self.doorController = doorController

        create_task(self.loop)


    async def loop(self):
        tag = await self.readTag()
        if (self.tagStore.isValidTag(tag)):
            await self.doorController.unlock()

    async def readTag(self):
        return await self.reader.readTag()


