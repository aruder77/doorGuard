from homie.device import HomieDevice, await_ready_state
from utime import time
from door_controller_node import DoorControllerNode
from rfid_reader_node import RfidReaderNode


class DoorGuardDevice(HomieDevice):

    def __init__(self, settings):
        super().__init__(settings)

        self.doorControllerNode = DoorControllerNode()
        self.rfidReaderNode = RfidReaderNode(self.doorControllerNode)

        self.add_node(self.doorControllerNode)
        self.add_node(self.rfidReaderNode)

        # DoorControllerNode
        # - doorState
        # - opener
        # RfidReaderNode
        # - accessLog
        # - lastValidTag
        # - lastInvalidTag
        # - readTag()
        # TagStore
        # - isTagValid()
        # - addTag()
        # - removeTag()
        # DoorGuardController
        # - mode: add, remove, access
        # - main loop
        # - calls readerNode.readTag()
        # - switch mode:
        #   - access:
        #     - if store.isValid() -> doorController.open()
        #   - add:
        #     - store.addTag()
        #   - remove:
        #     - store.removeTag()
    



