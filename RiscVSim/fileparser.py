
from struct import unpack
from instructions.instructionBits import getOpcode
from instructions.instruction import instructionTypes
from instructions.constructor import createInstruction

class Parser:

    program = None

    def parseFile(self, filePath):
        with open(filePath, mode='rb') as file:
            file = file.read()
        instructionCodeList = map(int, unpack("i" * (len(file) // 4), file))
        self._generateProgram(instructionCodeList)

    def _generateProgram(self, instructionCodeList):
        self.program = Program()
        for instrCode in instructionCodeList:
            opcode = getOpcode(instrCode)
            if opcode not in instructionTypes.keys():
                continue
            instruction = createInstruction(instrCode)
            self.program.addInstruction(instruction)

    def getProgram(self):
        return self.program


class Program(list):

    def __init__(self):
        super().__init__()

    def addInstruction(self, instruction):
        self.append(instruction)
