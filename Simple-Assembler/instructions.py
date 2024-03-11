import numpy as np
import re

# Define InstructionType enumeration
class InstructionType:
    R_TYPE = 0
    I_TYPE = 1
    S_TYPE = 2
    B_TYPE = 3
    U_TYPE = 4
    J_TYPE = 5

# Define InstructionEncoding class
class InstructionEncoding:
    def __init__(self, type, opcode, funct3, funct7):
        self.type = type
        self.opcode = opcode
        self.funct3 = funct3
        self.funct7 = funct7

# Define instruction map
instruction_map = {
    # R-type
    "add": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [0, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
    "sub": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [0, 0, 0], [0, 1, 0, 0, 0, 0, 0]),
    "sll": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [0, 0, 1], [0, 0, 0, 0, 0, 0, 0]),
    "slt": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [0, 1, 0], [0, 0, 0, 0, 0, 0, 0]),
    "sltu": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [0, 1, 1], [0, 0, 0, 0, 0, 0, 0]),
    "xor": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [1, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
    "srl": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [1, 0, 1], [0, 0, 0, 0, 0, 0, 0]),
    "or": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [1, 1, 0], [0, 0, 0, 0, 0, 0, 0]),
    "and": InstructionEncoding(InstructionType.R_TYPE, [0, 1, 1, 0, 0, 1, 1], [1, 1, 1], [0, 0, 0, 0, 0, 0, 0]),
    # I-type
    "jalr": InstructionEncoding(InstructionType.I_TYPE, [1, 1, 0, 0, 1, 1, 1], [0, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
    "lw": InstructionEncoding(InstructionType.I_TYPE, [0, 0, 0, 0, 0, 1, 1], [0, 1, 0], [0, 0, 0, 0, 0, 0, 0]),
    "addi": InstructionEncoding(InstructionType.I_TYPE, [0, 0, 1, 0, 0, 1, 1], [0, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
    "sltiu": InstructionEncoding(InstructionType.I_TYPE, [0, 0, 1, 0, 0, 1, 1], [0, 1, 1], [0, 0, 0, 0, 0, 0, 0]),
    # S-type
    "sw": InstructionEncoding(InstructionType.S_TYPE, [0, 1, 0, 0, 0, 1, 1], [0, 1, 0], [0, 0, 0, 0, 0, 0, 0]),
    # B-type
    "beq": InstructionEncoding(InstructionType.B_TYPE, [1, 1, 0, 0, 0, 1, 1], [0, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
    "bne": InstructionEncoding(InstructionType.B_TYPE, [1, 1, 0, 0, 0, 1, 1], [0, 0, 1], [0, 0, 0, 0, 0, 0, 0]),
    "blt": InstructionEncoding(InstructionType.B_TYPE, [1, 1, 0, 0, 0, 1, 1], [1, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
    "bge": InstructionEncoding(InstructionType.B_TYPE, [1, 1, 0, 0, 0, 1, 1], [1, 0, 1], [0, 0, 0, 0, 0, 0, 0]),
    "bltu": InstructionEncoding(InstructionType.B_TYPE, [1, 1, 0, 0, 0, 1, 1], [1, 1, 0], [0, 0, 0, 0, 0, 0, 0]),
    "bgeu": InstructionEncoding(InstructionType.B_TYPE, [1, 1, 0, 0, 0, 1, 1], [1, 1, 1], [0, 0, 0, 0, 0, 0, 0]),
    # U-type
    "lui": InstructionEncoding(InstructionType.U_TYPE, [0, 1, 1, 0, 1, 1, 1], [0, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
    "auipc": InstructionEncoding(InstructionType.U_TYPE, [0, 0, 1, 0, 1, 1, 1], [0, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
    # J-type
    "jal": InstructionEncoding(InstructionType.J_TYPE, [1, 1, 0, 1, 1, 1, 1], [0, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
}

# Define RegisterEncoding class
class RegisterEncoding:
    def __init__(self, name, address, saver_status):
        self.name = name
        self.address = address
        self.saver_status = saver_status

# Define register map
register_map = {
    "zero": RegisterEncoding("x0", [0, 0, 0, 0, 0], 2),
    "ra": RegisterEncoding("x1", [0, 0, 0, 0, 1], 0),
    "sp": RegisterEncoding("x2", [0, 0, 0, 1, 0], 1),
    "gp": RegisterEncoding("x3", [0, 0, 0, 1, 1], 2),
    "tp": RegisterEncoding("x4", [0, 0, 1, 0, 0], 2),
    "t0": RegisterEncoding("x5", [0, 0, 1, 0, 1], 0),
    "t1": RegisterEncoding("x6", [0, 0, 1, 1, 0], 0),
    "t2": RegisterEncoding("x7", [0, 0, 1, 1, 1], 0),
    "s0": RegisterEncoding("x8", [0, 1, 0, 0, 0], 1),
    "fp": RegisterEncoding("x8", [0, 1, 0, 0, 0], 1),
    "s1": RegisterEncoding("x9", [0, 1, 0, 0, 1], 1),
    "a0": RegisterEncoding("x10", [0, 1, 0, 1, 0], 0),
    "a1": RegisterEncoding("x11", [0, 1, 0, 1, 1], 0),
    "a2": RegisterEncoding("x12", [0, 1, 1, 0, 0], 0),
    "a3": RegisterEncoding("x13", [0, 1, 1, 0, 1], 0),
    "a4": RegisterEncoding("x14", [0, 1, 1, 1, 0], 0),
    "a5": RegisterEncoding("x15", [0, 1, 1, 1, 1], 0),
    "a6": RegisterEncoding("x16", [1, 0, 0, 0, 0], 0),
    "a7": RegisterEncoding("x17", [1, 0, 0, 0, 1], 0),
    "s2": RegisterEncoding("x18", [1, 0, 0, 1, 0], 0),
    "s3": RegisterEncoding("x19", [1, 0, 0, 1, 1], 0),
    "s4": RegisterEncoding("x20", [1, 0, 1, 0, 0], 0),
    "s5": RegisterEncoding("x21", [1, 0, 1, 0, 1], 0),
    "s6": RegisterEncoding("x22", [1, 0, 1, 1, 0], 0),
    "s7": RegisterEncoding("x23", [1, 0, 1, 1, 1], 0),
    "s8": RegisterEncoding("x24", [1, 1, 0, 0, 0], 0),
    "s9": RegisterEncoding("x25", [1, 1, 0, 0, 1], 0),
    "s10": RegisterEncoding("x26", [1, 1, 0, 1, 0], 0),
    "s11": RegisterEncoding("x27", [1, 1, 0, 1, 1], 0),
    "t3": RegisterEncoding("x28", [1, 1, 1, 0, 0], 0),
    "t4": RegisterEncoding("x29", [1, 1, 1, 0, 1], 0),
    "t5": RegisterEncoding("x30", [1, 1, 1, 1, 0], 0),
    "t6": RegisterEncoding("x31", [1, 1, 1, 1, 1], 0),
}

# Define functions for binary conversion
def int_to_signed_bin_array(a, n):
    value = a & ((1 << n) - 1)
    if value & (1 << (n - 1)):
        value = value - (1 << n)
    return [1 if i == '1' else 0 for i in bin(value & ((1 << n) - 1))[2:].zfill(n)]

def slice_bool_array(bool_array, start_index, end_index):
    return bool_array[start_index:end_index + 1]

# Define tokenizer function
def tokenize(line):
    tokens = line.split()
    real_tokens = []
    for token in tokens:
        sub_tokens = token.split(',')
        for sub_token in sub_tokens:
            real_tokens.append(sub_token)
    return real_tokens

# Define decode function
def decode(tokens):
    instr_type = instruction_map[tokens[0]].type
    decoded = [0] * 32

    if instr_type == InstructionType.R_TYPE:
        decoded[:7] = instruction_map[tokens[0]].funct7
        decoded[7:12] = register_map[tokens[3]].address
        decoded[12:17] = register_map[tokens[2]].address
        decoded[17:20] = instruction_map[tokens[0]].funct3
        decoded[20:25] = register_map[tokens[1]].address
        decoded[25:32] = instruction_map[tokens[0]].opcode

    elif instr_type == InstructionType.I_TYPE:
        if tokens[0] == "lw":
            imm = int_to_signed_bin_array(int(tokens[2]), 12)
        else:
            imm = int_to_signed_bin_array(int(tokens[3]), 12)
        decoded[:12] = imm
        decoded[12:17] = register_map[tokens[3]].address
        decoded[17:20] = instruction_map[tokens[0]].funct3
        decoded[20:25] = register_map[tokens[1]].address
        decoded[25:32] = instruction_map[tokens[0]].opcode

    elif instr_type == InstructionType.S_TYPE:
        imm = int_to_signed_bin_array(int(tokens[2]), 12)
        decoded[:7] = imm[:7]
        decoded[7:12] = register_map[tokens[1]].address
        decoded[12:17] = register_map[tokens[3]].address
        decoded[17:20] = instruction_map[tokens[0]].funct3
        decoded[20:25] = imm[7:]
        decoded[25:32] = instruction_map[tokens[0]].opcode

    elif instr_type == InstructionType.B_TYPE:
        imm = int_to_signed_bin_array(int(tokens[3]), 16)
        decoded[:1] = imm[3:4]
        decoded[1:7] = imm[5:11]
        decoded[7:12] = register_map[tokens[2]].address
        decoded[12:17] = register_map[tokens[1]].address
        decoded[17:20] = instruction_map[tokens[0]].funct3
        decoded[20:25] = imm[11:15]
        decoded[24:25] = imm[4:5]
        decoded[25:32] = instruction_map[tokens[0]].opcode

    elif instr_type == InstructionType.U_TYPE:
        imm = int_to_signed_bin_array(int(tokens[2]), 32)
        decoded[:20] = imm[:20]
        decoded[20:25] = register_map[tokens[1]].address
        decoded[25:32] = instruction_map[tokens[0]].opcode

    elif instr_type == InstructionType.J_TYPE:
        imm = int_to_signed_bin_array(int(tokens[2]), 21)
        decoded[0] = imm[0]
        decoded[1:11] = imm[10:20]
        decoded[11] = imm[9]
        decoded[12:20] = imm[1:9]
        decoded[20:25] = register_map[tokens[1]].address
        decoded[25:32] = instruction_map[tokens[0]].opcode

    return decoded

# Define read_file function
def read_file(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            tokens = tokenize(line)
            decoded = decode(tokens)
            print(''.join(map(str, decoded)))

# Main function
def main():
    read_file("src/instruction/text.txt")

if __name__ == "__main__":
    main()
