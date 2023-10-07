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
        lines = []
        for uuid, name in self.tags.items():
            lines.append("%s;%s\n" % (uuid, name))
        with open(self.VALID_TAGS_FILE, "w") as f:
            f.write(''.join(lines))        