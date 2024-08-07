class TagStore:
    VALID_TAGS_FILE = "tags.dat"

    def __init__(self):
        self.tags = {}
        self.read_tags()

    def isValidTag(self, tag):
        return tag in self.tags

    def read_tags(self):
        lines = []
        try:
            with open(self.VALID_TAGS_FILE) as f:
                lines = f.readlines()
        except OSError:
            pass
        for line in lines:
            uuid, name = line.strip("\n").split(";")
            self.tags[uuid.strip()] = name.strip()

    def write_tags(self):
        with open(self.VALID_TAGS_FILE, "w") as f:
            f.write(self.getTags())

    def addTag(self, tag, name):
        self.tags[tag] = name
        self.write_tags()

    def removeTag(self, tag):
        del self.tags[tag]
        self.write_tags()

    def setTags(self, tags):
        for line in tags.splitlines():
            uuid, name = line.strip().split(";")
            self.tags[uuid.strip()] = name.strip()
        self.write_tags()

    def getTags(self):
        lines = []
        for uuid, name in self.tags.items():
            lines.append("%s;%s\n" % (uuid, name))
        return ''.join(lines)

