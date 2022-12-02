from simulator import Simulator

path = r">>path to your binary file (.bin)<<"

if __name__ == "__main__":
    sim = Simulator()
    sim.loadProgram(path)
    # sim.printProgram()  # uncomment to print the program (in binary and encoded to RISC-V operations)
    sim.run()
