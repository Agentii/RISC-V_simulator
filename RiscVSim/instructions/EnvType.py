from instructions.instruction import Instruction
from instructions.instructionBits import *


class EnvOperation:
    rd = funct3 = rs1 = funct12 = None
    op = None

    def __init__(self, rd, funct3, rs1, funct12, op):
        self.rd, self.funct3, self.rs1, self.funct12 = rd, funct3, rs1, funct12
        self.op = op

    def __repr__(self):
        return self.__class__.__name__

    def execute(self, **kwargs):  # Not needed for current ISA
        pass


class ECALL(EnvOperation):

    def __init__(self, rd, funct3, rs1, funct12):
        super().__init__(rd, funct3, rs1, funct12, print)

    def execute(self, **kwargs):
        register = kwargs['register']
        PC = kwargs['PC']
        self.op(register)
        return PC


class Environment(Instruction):

    rd = funct3 = rs1 = funct12 = None
    operations = {
        0x0: {
            0x0: ECALL
        }
    }

    def __init__(self, instruction):
        super().__init__(instruction)
        self.rd = getRd(instruction)
        self.funct3 = getFunct3(instruction)
        self.rs1 = getRs1(instruction)
        self.funct12 = getFunct12(instruction)
        getOpcode(instruction)

        self.loadOperation()

    def loadOperation(self):
        operationClass = self.operations[self.funct3][self.funct12]
        self.operation = operationClass(self.rd, self.funct3, self.rs1, self.funct12)
