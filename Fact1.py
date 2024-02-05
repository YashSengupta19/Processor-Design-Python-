import math

# Preprocessing

Instruction_Memory = []  # Instruction Memory Format ----> [ Address, Instruction ]
Data_Memory = []  # Data Memory Format ----> [ Address, Data ]

# Register File Format ----> [ Register Number, Register Name, Value Stored in Register ]
Register_File = [["00000", "$zero", 0],
                 ["00001", "$at", 0],
                 ["00010", "$v0", 0],
                 ["00011", "$v1", 0],
                 ["00100", "$a0", 0],
                 ["00101", "$a1", 0],
                 ["00110", "$a2", 0],
                 ["00111", "$a3", 0],
                 ["01000", "$t0", 0],
                 ["01001", "$t1", 0],
                 ["01010", "$t2", 0],
                 ["01011", "$t3", 0],
                 ["01100", "$t4", 0],
                 ["01101", "$t5", 0],
                 ["01110", "$t6", 0],
                 ["01111", "$t7", 0],
                 ["10000", "$s0", 0],
                 ["10001", "$s1", 0],
                 ["10010", "$s2", 0],
                 ["10011", "$s3", 0],
                 ["10100", "$s4", 0],
                 ["10101", "$s5", 0],
                 ["10110", "$s6", 0],
                 ["10111", "$s7", 0],
                 ["11000", "$t8", 0],
                 ["11001", "$t9", 0],
                 ["11010", "$k0", 0],
                 ["11011", "$k1", 0],
                 ["11100", "$gp", 0],
                 ["11101", "$sp", 0],
                 ["11110", "$pf", 0],
                 ["11111", "$ra", 0]]

Machine_Code = '''00100000000011100000000000000000
00100001010011110000000000000000
00100001011110000000000000000000
10001101010011000000000000000000
00100001110011100000000000000001
00100000000011010000000000000001
00010001100000000000000000000110
01110001101011000110100000000010
00100001100011001111111111111111
00010101100000001111111111111101
10101101011011010000000000000000
00100001010010100000000000000100
00100001011010110000000000000100
00100001100011000000000000000001
10101101011011000000000000000000
00010101110010011111111111110011
00100001111010100000000000000000
00100011000010110000000000000000'''

Machine_Code = Machine_Code.split("\n")
# print(len(Machine_Code))
CLOCK = 0


# Used to convert the binary values to decimal
# For Example: Imm field of a particular instruction is in binary
# But to work with it, we need its decimal equivalent

def BinaryToDecimal(imm):
    decimal_value = int(imm,2)
    if decimal_value & 0x8000:
        decimal_value = -((1 << 16) - decimal_value)
    return decimal_value



def BinaryToDecimal(imm):
    decimal_value = int(imm,2)
    if decimal_value & 0x8000:
        decimal_value = -((1 << 16) - decimal_value)
    return decimal_value





# This function is used to access the values stored in a register using its 5 bit register number


def getRegValue(RegNumber):
    global Register_File
    for j in Register_File:
        if j[0] == RegNumber:
            return j[2]


# This function sets the value of the particular register to the given value
# For Example in case of add the value of register rd gets changed.
# This function is used to change the value in the register file


def setRegValue(RegNumber, Value):
    global Register_File
    for j in Register_File:
        if j[0] == RegNumber:
            j[2] = Value


# The two DataMem functions work the same as RegFile functions but for the Data Memory


def getDataMemValue(MemAddress):
    global Data_Memory
    for j in Data_Memory:
        if j[0] == MemAddress:
            return j[1]


def setDataMemValue(MemAddress, Value):
    global Data_Memory
    for j in Data_Memory:
        if j[0] == MemAddress:
            j[1] = Value


def getAddressindex(MemAddress):
    global Instruction_Memory
    for j in Instruction_Memory:
        if j[0] == MemAddress:
            return Instruction_Memory.index(j)


# This is the main function executing the instructions and modifying the currentpointer
# Updating the RegFile, DataMemory, etc


def executeInstruction(Address, Instruction):
    global CLOCK
    global Register_File
    global Data_Memory
    global Instruction_Memory
    CLOCK += 1  # When a particular instruction is executed
    Opcode = Instruction[0:6]
    #print(Opcode)
    # Form cases on the basis of Opcodes
    if Opcode == "000000" or Opcode == "011100":  # R-Format
        #print("IF1")
        # Accessing all the fields of R-Type Instruction
        rs = Instruction[6:11]
        rt = Instruction[11:16]
        rd = Instruction[16:21]
        shamt = Instruction[21:26]
        funct = Instruction[26:]

        # For add
        if funct == "100000":
            x = getRegValue(rs)
            y = getRegValue(rt)
            z = x + y
            setRegValue(rd, z)
            return 1

        # For jr
        elif funct == "001000":
            TargetAddress = getRegValue(rs)
            AddressL = getAddressindex(Address)
            TargetAddressL = getAddressindex(TargetAddress)
            NumberofInstructions = (TargetAddressL - AddressL)
            return NumberofInstructions

        # For sub
        elif funct == "100010":
            a = getRegValue(rs)
            b = getRegValue(rt)
            #print(rs, rt)
            c = a - b
            setRegValue(rd, c)
            return 1

        # For mult
        elif funct == "000010":
            a = getRegValue(rs)
            b = getRegValue(rt)
            #print(rs, rt)
            c = a * b
            setRegValue(rd, c)
            return 1

    else:
        # For jump
        #print("Else1")
        if Opcode == "000010":
            JumpAddress = Instruction[6:32]
            JumpAddress = "0000" + JumpAddress + "00"
            JumpAddress = BinaryToDecimal(JumpAddress)
            JumpAddressL = getAddressindex(JumpAddress)
            AddressL = getAddressindex(Address)
            NumberofInstructions = (JumpAddressL - AddressL)
            return NumberofInstructions

        # For jal
        # jal is the same as j.
        # The only difference is that we have to store PC+4 in ra before returning

        elif Opcode == "000011":
            JumpAddress = Instruction[6:32]
            JumpAddress = "0000" + JumpAddress + "00"
            JumpAddress = BinaryToDecimal(JumpAddress)
            JumpAddressL = getAddressindex(JumpAddress)
            AddressL = getAddressindex(Address)
            NumberofInstructions = (JumpAddressL - AddressL)
            # print(NumberofInstructions)
            setRegValue("11111", Address + 4)  # Here we are storing the address of next instruction in register ra
            return NumberofInstructions

        # For I-type instructions
        else:
            # print("Else")
            # Accessing all the fields of I-Type instruction
            rs = Instruction[6:11]
            rt = Instruction[11:16]
            imm = Instruction[16:32]

            # For load instruction
            if Opcode == "100011":
                imm = "0000000000000000" + imm
                y = BinaryToDecimal(imm)
                x = getRegValue(rs)
                z = x + y
                setRegValue(rt, getDataMemValue(z))
                return 1  # The value 1 we are returning tells how many instructions to jump after this

            # For store instruction
            elif Opcode == "101011":
                imm = "0000000000000000" + imm
                # print(rt)
                x = getRegValue(rs)
                y = BinaryToDecimal(imm)
                # print(x, y)
                setDataMemValue(x + y, getRegValue(rt))
                return 1

            # For addi instruction
            elif Opcode == "001000":
                #print("Addi")
                imm = "0000000000000000" + imm
                y = BinaryToDecimal(imm)
                x = getRegValue(rs)
                #print(rt, x)
                setRegValue(rt, x + y)
                return 1

            # For beq
            elif Opcode == "000100":
                x = getRegValue(rs)
                y = getRegValue(rt)

                # print(rs,rt,"RegNumber")
                # print(x,y,"Reg")

                if x == y:
                    imm = "0000000000000000" + imm
                    JumpAddress = BinaryToDecimal(imm)
                    # print("Address = ", Address)
                    # print("Jump Address = ", JumpAddress)
                    NumberofInstructions = JumpAddress
                    # print("Number of Instructions = ", NumberofInstructions)
                    return NumberofInstructions + 1

                else:
                    return 1

            # for bgtz

            elif Opcode == "000111":
                x = getRegValue(rs)
                y = getRegValue(rt)

                if x > 0:
                    JumpAddress = BinaryToDecimal(imm)
                    # print("Address = ", Address)
                    # print("Jump Address = ", JumpAddress)
                    NumberofInstructions = JumpAddress
                    #print("Number of Instructions = ", NumberofInstructions)
                    return NumberofInstructions + 1 - 43

                else:
                    return 1

            # For bne(incomplete)
            elif Opcode == "000101":
                x = getRegValue(rs)
                y = getRegValue(rt)

                print(rs,rt,"RegNumber")
                print(x,y,"Reg")

                if x != y:
                    imm = imm
                    JumpAddress = BinaryToDecimal(imm)
                    # print("Address = ", Address)
                    # print("Jump Address = ", JumpAddress)
                    NumberofInstructions = JumpAddress
                    print("Number of Instructions = ", NumberofInstructions)
                    return NumberofInstructions

                else:
                    return 1


# print(BinaryToDecimal("1111"))

# First Part of the code we will put the instructions in the instruction memory (hardcoded)

while len(Machine_Code) != 0:
    Starting_Address = int(input("Enter Starting Address of Instruction"))
    N = int(input("Enter Number of instructions"))
    for i in range(N):
        Instruction_Memory.append([Starting_Address, Machine_Code[0]])
        Starting_Address += 4
        del Machine_Code[0]

for i in Instruction_Memory:
    print(i)

# Completing the setup before the main execution
PC = int(input("Enter Starting address"))
Ending_Address = int(input("Enter the ending address of this code"))
pointer = 0  # Keeps track of the instruction to be executed
flag = True

# Setting up the data memory

Starting_AddressIN = int(input("Enter Starting Address of Inputs"))
setRegValue("01010", Starting_AddressIN)
N = int(input("Enter number of Inputs"))
for i in range(N):
    input_temp = int(input("Enter the number"))
    Data_Memory.append([Starting_AddressIN, input_temp])
    Starting_AddressIN += 4

Starting_AddressOUT = int(input("Enter Starting Address of Output)"))
setRegValue("01011", Starting_AddressOUT)
for i in range(N):
    Data_Memory.append([Starting_AddressOUT, 0])
    Starting_AddressOUT += 4
# print(Data_Memory)
# Setting up the register file

setRegValue("01001", N)

# This is where the main execution of the program starts
CLOCK = 0
while flag:
    if Instruction_Memory[pointer][0] == Ending_Address:
        executeInstruction(Instruction_Memory[pointer][0], Instruction_Memory[pointer][1])
        flag = False
    else:
        # print("register values",getRegValue("10100"),getRegValue("10101"),getRegValue("11000"))
        print("Pointer", pointer)
        I_Type = executeInstruction(Instruction_Memory[pointer][0], Instruction_Memory[pointer][
            1])  # The variable I_Type tells which is the next instruction to jump to

        pointer += I_Type

print("Clock", CLOCK)
print(Data_Memory)
