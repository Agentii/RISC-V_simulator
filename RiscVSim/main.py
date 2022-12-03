from simulator import Simulator
import sys

path = r">>path to your binary file (.bin)<<"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    sim = Simulator()
    sim.loadProgram(path)
    # sim.printProgram()  # uncomment to print the program (in binary and encoded to RISC-V operations)
    sim.run()
