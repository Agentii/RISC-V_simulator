
instructionTypes = {
    0x33: "R-type",
    0x13: "I-type",
    0x3:  "I-type",
    0x23: "S-type",
    0x63: "B-type",
    0x37: "U-type",
    0x17: "U-type",
    0x6F: "J-type",
    0x67: "J-type",
    0x73: "Environment"
}

registerNames = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1"] + \
                ["a" + str(i) for i in range(8)] + \
                ["s" + str(i) for i in range(2, 12)] + \
                ["t" + str(i) for i in range(3, 7)]


class Instruction(int):

    instruction = None
    opcode = None
    operation = None

    def __init__(self, instruction):
        self.instruction = instruction
        self.opcode = instruction & (2**7 - 1)

    def getOperation(self):
        return self.operation

    def getOpcode(self):
        return self.opcode

    def __repr__(self):
        return str(format(self.instruction, ' 033b'))  # change to '032b' if using 2's complement
