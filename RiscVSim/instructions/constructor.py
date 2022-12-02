from instructions.RType import RType
from instructions.IType import IType
from instructions.SType import SType
from instructions.BType import BType
from instructions.UType import UType
from instructions.JType import JType
from instructions.EnvType import Environment
from instructions.instructionBits import getOpcode
from instructions.instruction import instructionTypes

def createInstruction(instructionCode):
    opcode = getOpcode(instructionCode)
    if opcode not in instructionTypes.keys():
        return instructionCode
    instructionType = instructionTypes[opcode]
    instruction = None
    if instructionType == "R-type":
        instruction = RType(instructionCode)

    elif instructionType == "I-type":
        instruction = IType(instructionCode)

    elif instructionType == "S-type":
        instruction = SType(instructionCode)

    elif instructionType == "B-type":
        instruction = BType(instructionCode)

    elif instructionType == "U-type":
        instruction = UType(instructionCode)

    elif instructionType == "J-type":
        instruction = JType(instructionCode)

    elif instructionType == "Environment":
        instruction = Environment(instructionCode)

    return instruction
