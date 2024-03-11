class Opcode:
    def __init__(self, name, type, bits):
        self.name = name
        self.type = type
        self.bits = bits

class Immediate:
    def __init__(self, number, bits):
        self.number = number
        self.bits = bits

class Label:
    def __init__(self, name, isPresent):
        self.name = name
        self.isPresent = isPresent

class Instruction:
    def __init__(self, opcode, registers, label, immediates, position, funct3, funct7, elementCount):
        self.opcode = opcode
        self.registers = registers
        self.label = label
        self.immediates = immediates
        self.position = position
        self.funct3 = funct3
        self.funct7 = funct7
        self.elementCount = elementCount

class InputFile:
    def __init__(self, instructions, size):
        self.instructions = instructions
        self.size = size

def readFile(RELATIVE_FILE_PATH):
    with open(RELATIVE_FILE_PATH, 'r') as file:
        return file.read()

def assignInstruction(ASSEMBLY_CODE):
    # Split the assembly code into lines
    lines = ASSEMBLY_CODE.split('\n')

    # Initialize a list to store instructions
    instructions = []

    # Iterate over each line in the assembly code
    for line in lines:
        # Ignore empty lines and comments
        if line.strip() == '' or line.strip().startswith('//'):
            continue

        # Split the line into tokens
        tokens = line.strip().split()

        # Extract opcode, registers, label, immediates, position, funct3, funct7, elementCount
        opcode_name = tokens[0]
        opcode_type = InstructionType.R_TYPE  # For example, assuming all are R_TYPE for now
        opcode_bits = []  # You need to define how to extract opcode bits based on opcode_name
        opcode = Opcode(opcode_name, opcode_type, opcode_bits)

        # Example: You need to extract registers, label, immediates, position, funct3, funct7, elementCount similarly

        # Create an Instruction object and append it to the list of instructions
        instruction = Instruction(opcode, None, None, None, None, None, None, None)  # Replace None with extracted values
        instructions.append(instruction)

    # Create an InputFile object containing the list of instructions and return it
    input_file = InputFile(instructions, len(instructions))
    return input_file

def writeFile(INPUT):
    pass  # Add code to write instructions to a file if needed

# Define InstructionType enumeration
class InstructionType:
    R_TYPE,
    I_TYPE,
    S_TYPE,
    B_TYPE,
    U_TYPE,
    J_TYPE,
    COMMENT

# Now, you can use these functions to read the file, assign instructions, and write instructions to a file if needed
def main():
    ASSEMBLY_CODE = readFile("path/to/your/assembly/file.txt")
    input_file = assignInstruction(ASSEMBLY_CODE)
    writeFile(input_file)

if __name__ == "__main__":
    main()
