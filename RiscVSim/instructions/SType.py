from instructions.instruction import Instruction, registerNames
from instructions.instructionBits import *


class SOperation:
    imm = rs1 = rs2 = None
    op = None

    def __init__(self, imm4_0, rs1, rs2, imm11_5, op):
        self.rs1, self.rs2 = rs1, rs2
        self.imm = (imm11_5 << 5) + imm4_0
        sign = 1 if self.imm < 0 else 0
        self.imm = (self.imm << 19 * sign) + (self.imm * sign)
        self.op = op

    def __repr__(self):
        return self.__class__.__name__ + " %s, %d(%s)" % (registerNames[self.rs2],
                                                          self.imm,
                                                          registerNames[self.rs1])

    def execute(self, **kwargs):
        register = kwargs['register']
        memory = kwargs['memory']
        PC = kwargs['PC']
        memory[register[self.rs1] + self.imm] = self.op(register[self.rs2])
        return PC


class SB(SOperation):

    def __init__(self, imm4_0, rs1, rs2, imm11_5):
        super().__init__(imm4_0, rs1, rs2, imm11_5, lambda x: x & 0xFF)


class SH(SOperation):

    def __init__(self, imm4_0, rs1, rs2, imm11_5):
        super().__init__(imm4_0, rs1, rs2, imm11_5, lambda x: x & 0xFFFF)


class SW(SOperation):

    def __init__(self, imm4_0, rs1, rs2, imm11_5):
        super().__init__(imm4_0, rs1, rs2, imm11_5, lambda x: x)


class SType(Instruction):

    imm4_0 = funct3 = rs1 = rs2 = imm11_5 = None
    operations = {
        0x0: SB,
        0x1: SH,
        0x2: SW
    }

    def __init__(self, instruction):
        super().__init__(instruction)
        self.imm4_0 = getImm4_0(instruction)
        self.funct3 = getFunct3(instruction)
        self.rs1 = getRs1(instruction)
        self.rs2 = getRs2(instruction)
        self.imm11_5 = getImm11_5(instruction)

        self.loadOperation()

    def loadOperation(self):
        operationClass = self.operations[self.funct3]
        self.operation = operationClass(self.imm4_0, self.rs1, self.rs2, self.imm11_5)
