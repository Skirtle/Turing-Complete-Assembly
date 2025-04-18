from sys import platform
from string import ascii_letters  
from subprocess import check_output


whoami = check_output(["whoami"]).decode().strip()
if ("linux" in platform):
    hostname = check_output("hostname").decode().strip()
    username = f"{whoami}@{hostname}"
elif ("win" in platform):
    split_name = whoami.split("\\")
    username = f"{split_name[1]}@{split_name[0]}"
else:
    username = "guest"

prog_name = "multiply"
input_file = f"./Programs/{prog_name}.asmtc"

keywords = [
        "reg0_to_reg1", "reg0_to_reg2", "reg0_to_reg3", "reg0_to_reg4", "reg0_to_reg5",
        "reg0_to_in", "reg0_to_out", "reg1_to_reg0", "reg1_to_reg2", "reg1_to_reg3",
        "reg1_to_reg4", "reg1_to_reg5", "reg1_to_in", "reg1_to_out", "reg2_to_reg0",
        "reg2_to_reg1", "reg2_to_reg3", "reg2_to_reg4", "reg2_to_reg5", "reg2_to_in",
        "reg2_to_out", "reg3_to_reg0", "reg3_to_reg1", "reg3_to_reg2", "reg3_to_reg4",
        "reg3_to_reg5", "reg3_to_in", "reg3_to_out", "reg4_to_reg0", "reg4_to_reg1",
        "reg4_to_reg2", "reg4_to_reg3", "reg4_to_reg5", "reg4_to_in", "reg4_to_out",
        "reg5_to_reg0", "reg5_to_reg1", "reg5_to_reg2", "reg5_to_reg3", "reg5_to_reg4",
        "reg5_to_in", "reg5_to_out", "in_to_reg0", "in_to_reg1", "in_to_reg2",
        "in_to_reg3", "in_to_reg4", "in_to_reg5", "in_to_out", "AND",
        "EQ", "GEQ", "GRE", "LEQ", "LES",
        "NAND", "NEQ", "OR", "add", "always",
        "false", "never", "sub", "submit", "true",
        "NOR", "XOR", "XNOR"
]
compute_keywords = [
	"AND", "NAND", "OR", "NOR", "XOR", "XNOR", "add", "sub"
]
cond_keywords = [
	"EQ", "GEQ", "GRE", "LEQ", "LES",
	"NEQ", "always", "true", "false",
	"never"
]


registers = [0, 0, 0, 0, 0, 0, 0, 0] # Registers 0-5, input, output
labels_consts = {}

def get_registers(command):
    ret_regs = [-1, -1]
    regs = command.split("_to_")
    for index,value in enumerate(regs):
        if (value == "in"): ret_regs[index] = 6
        elif (value == "out"): ret_regs[index] = 7
        else: ret_regs[index] = value[len(value) - 1]
    return int(ret_regs[0]), int(ret_regs[1])

def compute(command, val1, val2):
    if (command == "AND"): return val1 & val2
    elif (command == "NAND"): return ~(val1 & val2)
    elif (command == "OR"): return val1 | val2
    elif (command == "NOR"): return ~(val1 | val2)
    elif (command == "XOR"): return val1 ^ val2
    elif (command == "XNOR"): return ~(val1 ^ val2)
    elif (command == "add"): return val1 + val2
    elif (command == "sub"): return val1 - val2
    else: exit("Weird ass error lmao")
    
def condition(command, val) -> bool:
    if (command == "EQ"): return val == 0
    elif (command == "GEQ"): return val >= 0
    elif (command == "GRE"): return val > 0
    elif (command == "LEQ"): return val <= 0
    elif (command == "LES"): return val < 0
    elif (command == "NEQ"): return val != 0
    elif (command == "always" or command == "true"): return True
    elif (command == "false" or command == "never"): return False
    else: exit("Weird ass error but for cond")

def execute(line, pc) -> int:
    global labels_consts, registers
    # Label and const evaluations
    if (line in labels_consts): 
        registers[0] = labels_consts[line]
        return pc + 1
    elif ("_to_" in line):
        # Copy registers
        from_reg, to_reg = get_registers(line)
        
        # Input and output
        if (from_reg == 6): registers[6] = int(input(f"{username}$ "))
        registers[to_reg] = registers[from_reg]
        if (to_reg == 7): print(registers[7])
        return pc + 1
    elif (line in compute_keywords):
        # Compute keywords
        registers[3] = compute(line, registers[1], registers[2])
        return pc + 1
    elif (line in cond_keywords):
        # Condition keywords
        cond = condition(line, registers[3])
        return registers[0] if cond else pc + 1
    elif (line.isdigit()):
        registers[0] = int(line)
        return pc + 1
    else:
        exit(f"Unknown variable \"{line}\"")


# Grab program file and find what we need
with open(input_file, "r") as file:
    address = 0
    full_program = []
    program = []
    prog_line = ""
    
    for line in file:
        # Start stripping lines
        if (len(line) == 0 or line == "\n"): continue
        line = line.strip()
        
        full_program.append(line) # Includes comments
        
        # Find the # and remove it, plus everything after it
        comment_index = line.find("#")
        if (comment_index != -1):
            prog_line = line[:comment_index]
            if (len(prog_line) != 0): program.append(prog_line.strip())
        else:
            prog_line = line.strip()
            program.append(prog_line)

# Get the address list for the program
# print(program)
address = 0
functional_program = []
for line in program:
    args = line.split(" ")
    keyword = args[0]
    if (keyword == "const"): # Const 
        # Check if all arguments exist and are correct
        try:
            arg1 = args[1]
            arg2 = int(args[2])
        except:
            exit("Error, invalid argument(s) for const")
            
        if (arg1[0] not in ascii_letters): exit("Invalid const name, must start with a letter")
        elif (not args[2].isdigit()): exit("Invalid const value, must be a number")
        elif (arg1 in keywords): exit("Const name cannot be a keyword")
        elif (arg1 in labels_consts): exit("Const name already used")
        else: labels_consts[arg1] = int(arg2)
    
    elif (keyword == "label"):
        try: arg1 = args[1]
        except: exit("Error, invalid argument(s) for const")
        
        if (arg1[0] not in ascii_letters): exit("Invalid label name, must start with a letter")
        elif (arg1 in keywords): exit("Label name cannot be a keyword")
        elif (arg1 in labels_consts): exit("Label name already used")
        else: labels_consts[arg1] = address  
    
    else:
        functional_program.append(line)
        address += 1


pc = 0
while (True):
    if (pc >= len(functional_program)): break
    pc = execute(functional_program[pc], pc)
    # print(registers)

print(registers)