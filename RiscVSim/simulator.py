from fileparser import Parser
from storage import *

class PC(int):
    def __init__(self):
        self.__new__(int, 0)


class Simulator:

    program = None
    parser = None
    register = None
    memory = None
    PC = PC()

    def __init__(self):
        self.parser = Parser()
        self.register = Register()
        self.memory = Memory(1_048_576*20)  # 1*20 MB (times 20 because of an error when loading immediates)

    def loadProgram(self, filePath):
        self.parser.parseFile(filePath)
        self.program = self.parser.getProgram()
        for instruction in self.program:
            self.memory.storeWord(self.PC, instruction)
            self.PC += 4
        self.PC = 0

    def printProgram(self):
        binTitle = "Binary instructions"
        encTitle = "Encoded instructions"
        header = binTitle + " "*(32-len(binTitle)) + "\t" + encTitle
        lineSep = "-"*len(header)
        print(lineSep + "\n" + header + "\n" + lineSep)
        for instr in self.program:
            if type(instr) == int:
                continue
            print(str(instr) + "\t" + str(instr.getOperation()))
        print("\n")

    def run(self):
        while True:
            instr = self.memory.loadWord(self.PC)
            if type(instr) == int:
                print(self.register)
                break
            self.PC = instr.getOperation().execute(register=self.register, memory=self.memory, PC=self.PC)
            self.PC += 4
