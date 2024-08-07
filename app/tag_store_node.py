from homie.node import HomieNode
from homie.constants import STRING
from homie.property import HomieProperty
from rfid_reader import RfidReader
from uasyncio import create_task, sleep_ms
from door_controller_node import DoorControllerNode
from tag_store import TagStore


class TagStoreNode(HomieNode):

    def __init__(self, tagStore: TagStore):
        super().__init__(id="TagStore", name="TagStore", type="Controller")

        self.addTagProperty = HomieProperty(
            id="addTag",
            name="addTag",
            datatype=STRING,
            settable=True,
            pub_on_upd=False,
            on_message=self.onAddTagMessage
        )
        self.add_property(self.addTagProperty)

        self.removeTagProperty = HomieProperty(
            id="removeTag",
            name="removeTag",
            datatype=STRING,
            settable=True,
            pub_on_upd=False,
            on_message=self.onRemoveTagMessage
        )
        self.add_property(self.removeTagProperty)

        self.tagsProperty = HomieProperty(
            id="tags",
            name="tags",
            datatype=STRING,
            settable=True,
            pub_on_upd=True,
            default=tagStore.getTags(),
            on_message=self.onSetTags
        )
        self.add_property(self.tagsProperty)

        self.tagStore = tagStore

    def onAddTagMessage(self, topic, payload, retained):
        tag, name = payload.split(";")
        if len(tag.strip()) == 10:
            self.tagStore.addTag(tag, name)
        self.tagsProperty.value = self.tagStore.getTags()

    def onRemoveTagMessage(self, topic, payload, retained):
        tag, name = payload.split(";")
        if len(tag.strip()) == 10:
            self.tagStore.removeTag(tag)
        self.tagsProperty.value = self.tagStore.getTags()

    def onSetTags(self, topic, payload, retained):
        self.tagStore.setTags(payload)
        self.tagsProperty.value = self.tagStore.getTags()
