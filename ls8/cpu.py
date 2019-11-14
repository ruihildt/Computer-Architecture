"""CPU functionality."""

import sys

# Add instructions
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # program counter
        self.pc = 0
        # flag
        self.fl = 0
        # registers
        self.reg = [0] * 8
        self.reg[6] = 0xF4
        # memory
        self.ram = [0] * 256
        self.running = True

    def load(self, filename):
        """Load a program into memory."""
        address = 0

        with open(filename) as f:
            for line in f:
                comment_split = line.split("#")
                num = comment_split[0].strip()

                if len(num) == 0:
                    continue


                instruction = int(num, 2)
                self.ram[address] = instruction

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]

        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            # FETCH instruction from ram
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # LDI instruction
            if IR == LDI:
                instruction_size = 3
                # Add the value to the register
                self.reg[operand_a] = operand_b

            # PRN instruction
            elif IR == PRN:
                instruction_size = 2
                print(self.reg[operand_a])

            # HLT instruction
            elif IR == HLT:
                self.running = False

            elif IR == MUL:
                instruction_size = 3

                self.alu(MUL, operand_a, operand_b)

            else:
                print(f'Unknown command "{IR}" provided')

            self.pc += instruction_size