from instructions.instruction import Instruction, registerNames
from instructions.instructionBits import *
import operator

class ROperation:
    rd = rs1 = rs2 = None
    op = None

    def __init__(self, rd, rs1, rs2, op):
        self.rd, self.rs1, self.rs2 = rd, rs1, rs2
        self.op = op

    def __repr__(self):
        return self.__class__.__name__ + " %s, %s, %s" % (registerNames[self.rd],
                                                          registerNames[self.rs1],
                                                          registerNames[self.rs2])

    def execute(self, **kwargs):
        register = kwargs['register']
        PC = kwargs['PC']
        register[self.rd] = self.op(register[self.rs1], register[self.rs2])
        return PC


class ADD(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, operator.__add__)


class SUB(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, operator.__sub__)


class SLL(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, lambda x, y: (x << y) & ((1 << x.bit_length()) - 1))


class SLT(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, operator.__lt__)


class SLTU(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, lambda x, y: (x & 0xffffffff) < (y & 0xffffffff))


class XOR(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, operator.__xor__)


class SRL(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, lambda x, y: (x % (1 << 32)) >> y)


class SRA(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, operator.__rshift__)


class OR(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, operator.__or__)


class AND(ROperation):

    def __init__(self, rd, rs1, rs2):
        super().__init__(rd, rs1, rs2, operator.__and__)


class RType(Instruction):

    rd = funct3 = rs1 = rs2 = funct7 = None
    operations = {
        0x0: {
            0x0: ADD,
            0x1: SLL,
            0x2: SLT,
            0x3: SLTU,
            0x4: XOR,
            0x5: SRL,
            0x6: OR,
            0x7: AND
        },
        0x20: {
            0x0: SUB,
            0x5: SRA
        }
    }

    def __init__(self, instruction):
        super().__init__(instruction)
        self.rd = getRd(instruction)
        self.funct3 = getFunct3(instruction)
        self.rs1 = getRs1(instruction)
        self.rs2 = getRs2(instruction)
        self.funct7 = getFunct7(instruction)

        self.loadOperation()

    def loadOperation(self):
        operationClass = self.operations[self.funct7][self.funct3]
        self.operation = operationClass(self.rd, self.rs1, self.rs2)
