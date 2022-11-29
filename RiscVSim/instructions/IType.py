from instructions.instruction import Instruction, registerNames
from instructions.instructionBits import *
import operator

class IOperation:
    rd = rs1 = imm = None
    op = None

    def __init__(self, rd, rs1, imm, op):
        self.rd, self.rs1, self.imm = rd, rs1, imm
        self.op = op

    def __repr__(self):
        return self.__class__.__name__ + " %s, %s, %d" % (registerNames[self.rd],
                                                          registerNames[self.rs1],
                                                          self.imm)

    def execute(self, **kwargs):
        register = kwargs['register']
        PC = kwargs['PC']
        register[self.rd] = self.op(register[self.rs1], self.imm)
        return PC

    def executeLoad(self, register, memory):
        register[self.rd] = self.op(memory[register[self.rs1] + self.imm])


class ADDI(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, operator.__add__)


class SLTI(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, operator.__lt__)


class SLTIU(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, lambda x, y: (x & 0xffffffff) < (y & 0xffffffff))


class XORI(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, operator.__xor__)


class ORI(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, operator.__or__)


class ANDI(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, operator.__and__)


class SLLI(IOperation):

    def __init__(self, rd, rs1, shamt):
        super().__init__(rd, rs1, shamt, lambda x, y: (x << y) & ((1 << x.bit_length()) - 1))


class SRLI(IOperation):

    def __init__(self, rd, rs1, shamt):
        super().__init__(rd, rs1, shamt, lambda x, y: (x % (1 << 32)) >> y)


class SRAI(IOperation):

    def __init__(self, rd, rs1, shamt):
        super().__init__(rd, rs1, shamt, operator.__rshift__)


class LB(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, lambda x: x & 0xF)

    def execute(self, **kwargs):
        self.executeLoad(kwargs['register'], kwargs['memory'])
        PC = kwargs['PC']
        return PC


class LH(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, lambda x: x & 0xFF)

    def execute(self, **kwargs):
        self.executeLoad(kwargs['register'], kwargs['memory'])
        PC = kwargs['PC']
        return PC


class LW(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, lambda x: x)

    def execute(self, **kwargs):
        self.executeLoad(kwargs['register'], kwargs['memory'])
        PC = kwargs['PC']
        return PC


class LBU(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, lambda x: (x & 0xffffffff) & 0xF)

    def execute(self, **kwargs):
        self.executeLoad(kwargs['register'], kwargs['memory'])
        PC = kwargs['PC']
        return PC


class LHU(IOperation):

    def __init__(self, rd, rs1, imm):
        super().__init__(rd, rs1, imm, lambda x: (x & 0xffffffff) & 0xFF)

    def execute(self, **kwargs):
        self.executeLoad(kwargs['register'], kwargs['memory'])
        PC = kwargs['PC']
        return PC


class IType(Instruction):

    rd = funct3 = rs1 = imm11_0 = None
    operations = {
        0x13: {
            0x0: ADDI,
            0x2: SLTI,
            0x3: SLTIU,
            0x4: XORI,
            0x6: ORI,
            0x7: ANDI,
            0x1: {
                0x0: SLLI
            },
            0x5: {
                0x0: SRLI,
                0x20: SRAI
            }
        },
        0x3: {
            0x0: LB,
            0x1: LH,
            0x2: LW,
            0x4: LBU,
            0x5: LHU
        }
    }

    def __init__(self, instruction):
        super().__init__(instruction)
        self.rd = getRd(instruction)
        self.funct3 = getFunct3(instruction)
        self.rs1 = getRs1(instruction)
        self.imm11_0 = getImm11_0(instruction)

        self.loadOperation()

    def loadOperation(self):
        operationClass = self.operations[self.opcode][self.funct3]
        if self.opcode == 0x13 and (self.funct3 == 0x1 or self.funct3 == 0x5):
            shamt = self.imm11_0 & (2 ** 5 - 1)
            imm11_5 = self.imm11_0 >> 5
            self.operation = operationClass[imm11_5](self.rd, self.rs1, shamt)
        else:
            self.operation = operationClass(self.rd, self.rs1, self.imm11_0)
