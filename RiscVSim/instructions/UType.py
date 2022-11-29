from instructions.instruction import Instruction, registerNames
from instructions.instructionBits import *


class UOperation:
    rd = imm = None
    op = None

    def __init__(self, rd, imm, op):
        self.rd, self.imm = rd, imm
        self.op = op

    def __repr__(self):
        return self.__class__.__name__ + " %s, %d" % (registerNames[self.rd],
                                                      self.imm)

    def execute(self, **kwargs):
        register = kwargs['register']
        PC = kwargs['PC']
        register[self.rd] = self.op(self.imm)
        return PC


class LUI(UOperation):

    def __init__(self, rd, imm):
        super().__init__(rd, imm, lambda x: x << 12)


class AUIPC(UOperation):

    def __init__(self, rd, imm):
        super().__init__(rd, imm, lambda x, PC: PC + (x << 12))

    def execute(self, **kwargs):
        register = kwargs['register']
        PC = kwargs['PC']
        register[self.rd] = self.op(self.imm, PC)
        return PC


class UType(Instruction):

    rd = imm31_12 = None
    operations = {
        0x37: LUI,
        0x17: AUIPC
    }

    def __init__(self, instruction):
        super().__init__(instruction)
        self.rd = getRd(instruction)
        self.imm31_12 = getImm31_12(instruction)
        self.loadOperation()

    def loadOperation(self):
        operationClass = self.operations[self.opcode]
        self.operation = operationClass(self.rd, self.imm31_12)
