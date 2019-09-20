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
        #initial where the start of stack points to in memory, store in r7
        self.sp = 0xF4
        self.reg[7] = self.ram[self.sp]

        # initialize pc to increment
        self.pc = 0
        
        #initialize branch table with all opcodes and the function call
        self.branch_table = {}
        self.branch_table[0b10000010] = self.handle_ldi
        self.branch_table[0b01000111] = self.handle_prn
        self.branch_table[0b00000001] = self.handle_hlt
        self.branch_table[0b01000101] = self.handle_push
        self.branch_table[0b01000110] = self.handle_pop

        
        
    def ram_read(self, MAR):
        #accept the address to read and return the value
        return self.ram[MAR]
    def ram_write(self, MDR, MAR):
        #accept a value to write, and the adrress to write it to
        #MDR = memory data register, MAR = memory address register
        self.ram[MAR] = MDR
    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) != 2:
            print(f'usage: {sys.argv[0]} [file]')
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    #find first part of instruction
                    number = line.split('#')[0]
                    #replace all \n with empty space
                    number = number.replace('\n', '')
                    #remove any empty space 
                    number = number.strip()
                    #forgot about the bland lines, convert binary to int and store in ram
                    if number is not '':
                        number = int(number, 2)
                        # add to the memory
                        self.ram[address] = number
                        address += 1
        
        except FileNotFoundError:
            print(f'{sys.argv[0]}: File not found')
            sys.exit(2)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
@@ -74,46 +80,58 @@
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == DIV:
            if not self.reg[reg_b]:
                print('Error,can not divide by 0')
                sys.exit()
            self.reg[reg_a] /= self.reg[reg_b]
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
    def handle_ldi(self, operand_a, operand_b):
        #LDI opcode, store vlaue at register
        self.reg[operand_a] = operand_b
    def handle_prn(self, operand_a):
        print(self.reg[operand_a])
    def handle_hlt(self):
        print('code halting...')
        sys.exit()

    def handle_push(self, operand_a):
        #decrement then store in the stack
        self.sp -= 1
        r_value = self.reg[operand_a]
        self.ram[self.sp] = r_value

    def handle_pop(self, operand_a):
        #store value in stack indicated by pointer, store in register at given reg index given by operand
        value = self.ram[self.sp]
        self.reg[operand_a] = value
        self.sp += 1

    def run(self):
        """Run the CPU."""

        while True:
            #hold a copy of the currently executing 8-bit instruction
            ir = self.ram[self.pc]
            #stores operands a and b which can be 1 or 2 bytes ahead of instruction byte, or nonexistent
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            # mask and shift to determiner number of operands
            num_operands  = (ir & 0b11000000) >> 6
            alu_handle = (ir & 0b00100000) >> 5
            if alu_handle:
                self.alu(ir, operand_a, operand_b)
            elif num_operands == 2:
                self.branch_table[ir](operand_a, operand_b)
            elif num_operands == 1:
                self.branch_table[ir](operand_a)
            elif num_operands == 0:
                self.branch_table[ir]()
            else:
                self.handle_hlt()
            self.pc += num_operands + 1