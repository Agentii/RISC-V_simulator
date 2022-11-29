
def getOpcode(instruction):
    return instruction & (2 ** 7 - 1)

def getRd(instruction):
    return (instruction >> 7) & (2 ** 5 - 1)

def getFunct3(instruction):
    return (instruction >> 12) & (2 ** 3 - 1)

def getRs1(instruction):
    return (instruction >> 15) & (2 ** 5 - 1)

def getRs2(instruction):
    return (instruction >> 20) & (2 ** 5 - 1)

def getFunct7(instruction):
    return (instruction >> 25) & (2 ** 7 - 1)

def getImm11_0(instruction):
    return instruction >> 20

def getImm4_0(instruction):
    return (instruction >> 7) & (2 ** 5 - 1)

def getImm11_5(instruction):
    return instruction >> 25

def getImm11B(instruction):
    return (instruction >> 7) & (2 ** 1 - 1)

def getImm4_1(instruction):
    return (instruction >> 8) & (2 ** 4 - 1)

def getImm10_5(instruction):
    return (instruction >> 25) & (2 ** 6 - 1)

def getImm12(instruction):
    return instruction >> 31

def getImm31_12(instruction):
    return instruction >> 12

def getImm19_12(instruction):
    return (instruction >> 12) & (2 ** 8 - 1)

def getImm11J(instruction):
    return (instruction >> 20) & (2 ** 1 - 1)

def getImm10_1(instruction):
    return (instruction >> 21) & (2 ** 10 - 1)

def getImm20(instruction):
    return instruction >> 31

def getFunct12(instruction):
    return (instruction >> 20) & (2 ** 12 - 1)
