# RISC-V Simulator in Python


### About
This repository contains a Python Simulator for the RV32I Base Instruction 
Set (Excluding the instructions: `fence`, `fence.i`, `ebreak`, `csrrw`, 
`csrrs`, `csrrc`, `csrrwi`, `csrrsi`, `csrrci`)


### How it works
1. The simulator's parser reads a binary file containing the instructions
of a RISC-V program and parses the instructions into an object-oriented 
format.


2. The encoded instructions translates the RISC-V operations to Python
operations, which can be run by the simulator.


3. The simulator generates an empty 1 MB memory, 32x32 bit register and
initialises a program counter (PC) before loading the encoded program
into memory.


4. The simulator runs the program by reading and executing an instruction 
from its memory, using the PC as a pointer.


5. The program terminates when the simulator reads the last instruction from 
memory, or when it reads an `ecall` instruction, thus printing the 32 registers
in the console.

   
### Usage
- *The program runs from `main.py`.*


- To run the program, add the path to your binary file to the **path** variable in 
`main.py`.
- Then, start the program by running `main.py`.
