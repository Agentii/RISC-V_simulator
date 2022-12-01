from instructions.instruction import Instruction, registerNames
from instructions.instructionBits import *
from instructions.IType import IOperation

class JOperation:
    rd = imm = None
    op = None

    def __init__(self, rd, imm19_12, imm11, imm10_1, imm20, op):
        self.rd = rd
        self.imm = (imm20 << 20) + (imm19_12 << 12) + (imm11 << 11) + (imm10_1 << 1)
        self.op = op

    def __repr__(self):
        return self.__class__.__name__ + " %s, %d" % (registerNames[self.rd],
                                                      self.imm)

    def execute(self, **kwargs):
        register = kwargs['register']
        PC = kwargs['PC']
        register[self.rd] = PC + 4
        PC += self.imm - 4
        return PC


class JAL(JOperation):

    def __init__(self, rd, imm19_12, imm11, imm10_1, imm20):
        super().__init__(rd, imm19_12, imm11, imm10_1, imm20, lambda x: x)


class JALR(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, lambda x: x)

    def execute(self, **kwargs):
        register = kwargs['register']
        PC = kwargs['PC']
        register[self.rd] = PC + 4
        PC = ((register[self.rs1] + self.imm) >> 1 << 1) - 4
        return PC

class JType(Instruction):
    rd = None
    imm19_12 = imm11 = imm10_1 = imm20 = None  # JAL
    funct3 = rs1 = imm11_0 = None  # JALR
    operations = {
        0x6F: JAL,
        0x67: JALR
    }

    def __init__(self, instruction):
        super().__init__(instruction)
        self.rd = getRd(instruction)
        self.imm19_12 = getImm19_12(instruction)
        self.imm11 = getImm11J(instruction)
        self.imm10_1 = getImm10_1(instruction)
        self.imm20 = getImm20(instruction)
        self.funct3 = getFunct3(instruction)
        self.rs1 = getRs1(instruction)
        self.imm11_0 = getImm11_0(instruction)

        self.loadOperation()

    def loadOperation(self):
        operationClass = self.operations[self.opcode]
        if self.opcode == 0x67:
            self.operation = operationClass(self.rd, self.rs1, self.imm11_0)
        else:
            self.operation = operationClass(self.rd, self.imm19_12, self.imm11, self.imm10_1, self.imm20)
