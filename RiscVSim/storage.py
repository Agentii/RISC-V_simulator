
class Memory(list):
    byteSize = 0

    def __init__(self, byteSize):
        super().__init__()
        self.extend([0 for _ in range(8*byteSize)])

    def __getitem__(self, item):
        return super().__getitem__(item//4)

    def __setitem__(self, key, value):
        super().__setitem__(key//4, value)

    def loadInstruction(self, pos):
        return self[pos]

    def storeInstruction(self, pos, instruction):
        self[pos] = instruction


class Register:

    registerNames = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1"] + \
                    ["a" + str(i) for i in range(8)] + \
                    ["s" + str(i) for i in range(2, 12)] + \
                    ["t" + str(i) for i in range(3, 7)]
    register = None

    def __init__(self):
        self.register = dict.fromkeys(range(32), 0)

    def __getitem__(self, item):
        return self.register[item]

    def __setitem__(self, key, value):
        if type(key) is int and 0 <= key < 32:
            if key != 0:
                self.register[key] = value

    def __repr__(self):
        lineSep = "-"*21
        header = "%s\nRegister%sValue\n%s" % (lineSep, " "*8, lineSep)
        content = ""
        for k, v in self.register.items():
            regName = self.registerNames[k] + " (x%d)" % k
            content += "%s%s%s\n" % (regName, " "*(16-len(regName)), hex(v & 0xffffffff))
        return "%s\n%s" % (header, content)
