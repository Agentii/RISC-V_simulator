
class Memory(list):
    byteSize = 0

    def __init__(self, byteSize):
        super().__init__()
        self.extend([0 for _ in range(byteSize)])

    def __getitem__(self, item):
        return self.loadByte(item)

    def __setitem__(self, key, value):
        self.storeByte(key, value)

    def loadByte(self, pos):
        return super().__getitem__(pos) & 0xFF

    def loadHalfword(self, pos):
        return self[pos] + (self[pos+1] << 8)

    def loadWord(self, pos):
        item = super().__getitem__(pos)
        if type(item) == int:
            return self[pos] + (self[pos+1] << 8) + (self[pos+2] << 16) + (self[pos+3] << 24)
        else:
            return item

    def storeByte(self, pos, byte):
        super().__setitem__(pos, byte & 0xFF)

    def storeHalfword(self, pos, halfword):
        for i in range(2):
            self.storeByte(pos+i, halfword >> 8*i)

    def storeWord(self, pos, word):
        for i in range(4):
            if type(word) == int:
                self.storeByte(pos+i, word >> 8*i)
            else:
                super().__setitem__(pos+i, word)


class Register(dict):

    registerNames = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1"] + \
                    ["a" + str(i) for i in range(8)] + \
                    ["s" + str(i) for i in range(2, 12)] + \
                    ["t" + str(i) for i in range(3, 7)]

    def __init__(self):
        super().__init__(dict.fromkeys(range(32), 0))

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if type(key) is int and 0 < key < 32:
            super().__setitem__(key, value)

    def __repr__(self):
        lineSep = "-"*21
        header = "%s\nRegister%sValue\n%s" % (lineSep, " "*8, lineSep)
        content = ""
        for k, v in self.items():
            regName = self.registerNames[k] + " (x%d)" % k
            content += "%s%s%s\n" % (regName, " "*(16-len(regName)), hex(v & 0xffffffff))
        return "%s\n%s" % (header, content)
