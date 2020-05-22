import sys


class CPU:

    def __init__(self):
        self.ram = [0b00000000] * 256
        self.reg = [0b00000000] * 8
        self.pc = 0
        self.L = False
        self.G = False
        self.E = False

    def load(self, program):
        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def run(self):

        LDI = 0b10000010
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        PRN = 0b01000111
        HLT = 0b00000001

        halted = False

        while not halted:
            instruction = self.ram[self.pc]

            if instruction == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]

                self.reg[reg_num] = value

                self.pc += 3

            elif instruction == PRN:
                reg_num = self.ram[self.pc + 1]
                print("PRINT ", self.reg[reg_num])
                self.pc += 2

            elif instruction == CMP:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                comp_a = self.reg[reg_a]
                comp_b = self.reg[reg_b]

                if comp_a < comp_b:
                    self.L = True
                elif comp_a > comp_b:
                    self.G = True

                if comp_a == comp_b:
                    self.E = True
                else:
                    self.E = False

                self.pc += 3

            elif instruction == JMP:
                reg_num = self.ram[self.pc + 1]
                self.pc = self.reg[reg_num]

            elif instruction == JEQ:
                if self.E == True:
                    reg_num = self.ram[self.pc + 1]
                    self.pc = self.reg[reg_num]
                else:
                    self.pc += 2

            elif instruction == JNE:
                if self.E == False:
                    reg_num = self.ram[self.pc + 1]
                    self.pc = self.reg[reg_num]
                else:
                    self.pc += 2

            elif instruction == HLT:
                halted = True


cpu = CPU()

file = open("sctest.ls8", "r")
program = []
for instruction in file:
    byte = instruction.split()[0]
    if byte != '#':
        byte = int(byte, base=2)
        program.append(byte)

cpu.load(program)

cpu.run()
