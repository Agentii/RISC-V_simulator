from instructions.instruction import Instruction, registerNames
from instructions.instructionBits import *
import operator

class BOperation:
    rs1 = rs2 = imm = None
    op = None

    def __init__(self, imm11, imm4_1, rs1, rs2, imm10_5, imm12, op):
        self.rs1, self.rs2 = rs1, rs2
        self.imm = (imm12 << 12) + (imm11 << 11) + (imm10_5 << 5) + (imm4_1 << 1)
        self.op = op

    def __repr__(self):
        return self.__class__.__name__ + " %s, %s, %d" % (registerNames[self.rs1],
                                                          registerNames[self.rs2],
                                                          self.imm)

    def execute(self, **kwargs):
        register = kwargs['register']
        PC = kwargs['PC']
        if self.op(register[self.rs1], register[self.rs2]):
            PC += self.imm - 4
        return PC


class BEQ(BOperation):

    def __init__(self, imm11, imm4_1, rs1, rs2, imm10_5, imm12):
        super().__init__(imm11, imm4_1, rs1, rs2, imm10_5, imm12, operator.__eq__)


class BNE(BOperation):

    def __init__(self, imm11, imm4_1, rs1, rs2, imm10_5, imm12):
        super().__init__(imm11, imm4_1, rs1, rs2, imm10_5, imm12, operator.__ne__)


class BLT(BOperation):

    def __init__(self, imm11, imm4_1, rs1, rs2, imm10_5, imm12):
        super().__init__(imm11, imm4_1, rs1, rs2, imm10_5, imm12, operator.__lt__)


class BGE(BOperation):

    def __init__(self, imm11, imm4_1, rs1, rs2, imm10_5, imm12):
        super().__init__(imm11, imm4_1, rs1, rs2, imm10_5, imm12, operator.__ge__)


class BLTU(BOperation):

    def __init__(self, imm11, imm4_1, rs1, rs2, imm10_5, imm12):
        super().__init__(imm11, imm4_1, rs1, rs2, imm10_5, imm12, lambda x, y: (x & 0xffffffff) < (y & 0xffffffff))


class BGEU(BOperation):

    def __init__(self, imm11, imm4_1, rs1, rs2, imm10_5, imm12):
        super().__init__(imm11, imm4_1, rs1, rs2, imm10_5, imm12, lambda x, y: (x & 0xffffffff) >= (y & 0xffffffff))


class BType(Instruction):

    imm11 = imm4_1 = funct3 = rs1 = rs2 = imm10_5 = imm12 = None
    operations = {
        0x0: BEQ,
        0x1: BNE,
        0x4: BLT,
        0x5: BGE,
        0x6: BLTU,
        0x7: BGEU
    }

    def __init__(self, instruction):
        super().__init__(instruction)
        self.imm11 = getImm11B(instruction)
        self.imm4_1 = getImm4_1(instruction)
        self.funct3 = getFunct3(instruction)
        self.rs1 = getRs1(instruction)
        self.rs2 = getRs2(instruction)
        self.imm10_5 = getImm10_5(instruction)
        self.imm12 = getImm12(instruction)

        self.loadOperation()

    def loadOperation(self):
        operationClass = self.operations[self.funct3]
        self.operation = operationClass(self.imm11, self.imm4_1, self.rs1, self.rs2, self.imm10_5, self.imm12)
