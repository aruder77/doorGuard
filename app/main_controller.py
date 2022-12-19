from esp_micro.esp_micro_controller import EspMicroController
from doorGuard_device import DoorGuardDevice


class MainController(EspMicroController):
    def __init__(self):
        super().__init__()

    def createHomieDevice(self, settings):
        return DoorGuardDevice(settings)

    def getDeviceName(self):
        return 'doorGuard'

    def getDeviceID(self):
        return 'doorGuard'
