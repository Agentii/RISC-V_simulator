from fileparser import Parser
from storage import *

class PC(int):
    def __init__(self):
        self.__new__(int, 0)

    def incrementBy(self, val):
        self.__new__(int, self + val)

class Simulator:

    program = None
    parser = None
    register = None
    memory = None
    PC = PC()

    def __init__(self):
        self.parser = Parser()
        self.register = Register()
        self.memory = Memory(1_048_576)  # 1 MB

    def loadProgram(self, filePath):
        self.parser.parseFile(filePath)
        self.program = self.parser.getProgram()
        for instruction in self.program:
            self.memory.storeInstruction(self.PC, instruction)
            self.PC += 4
        self.PC = 0

    def printProgram(self):
        binTitle = "Binary instructions"
        encTitle = "Encoded instructions"
        header = binTitle + " "*(32-len(binTitle)) + "\t" + encTitle
        lineSep = "-"*len(header)
        print(lineSep + "\n" + header + "\n" + lineSep)
        for instr in self.program:
            print(str(instr) + "\t" + str(instr.getOperation()))

    def run(self):
        while True:
            instr = self.memory.loadInstruction(self.PC)
            if instr == 0:
                break
            self.PC = instr.getOperation().execute(register=self.register, memory=self.memory, PC=self.PC)
            self.PC += 4
