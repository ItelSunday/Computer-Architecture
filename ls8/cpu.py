"""CPU functionality."""

import sys
print(sys.argv)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Memory to hold 256 bytes of memory
        self.ram = [00000000] * 256
        # registers
        self.reg = [0] * 8
        # initialize pc to increment
        self.pc = 0
        
    def ram_read(self, MAR):
        #accept the address to read and return the value
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        #accepts a value to write and the adrress to write it to
        #MDR = Memory Data Register | MAR = Memory Address Register
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    num = line.split('#', 1)[0]
                    if num.strip() == '':
                        continue
                    self.ram[address] = int(num, 2)
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)
            


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        
        # ir = self.reg[self.pc]
        
        # #stores operands a and b which can be 1 or 2 bytes ahead of instruction byte or non existent
        # operand_a = self.ram_read(self.pc+1)
        # operand_b = self.ram_read(self.pc+2)

        running = True

        while running:
            # if ir > LDI:
            #hold a copy of the currently executing 8-bit instruction
            ir = self.ram[self.pc]

            #stores operands a and b which can be 1 or 2 bytes ahead of instruction byte, or nonexistent
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

             # mask and shift to determiner number of operands
            num_operands  = (ir & 0b11000000) >> 6

            #TODO it has two operands
            if ir == LDI:
                # LDI opcode, site value at specified spot in register
                self.reg[operand_a] = operand_b
                #TODO has one operand
            elif ir == PRN:
                print(self.reg[operand_a])
            elif ir == HLT:
                #HLT opcode, stop the loop
                print('code halting ...')
                running = False
                break
            self.pc += num_operands + 1