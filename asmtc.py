from string import ascii_letters  

prog_name = "storage_cracker_copy"
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
	"NAND", "NEQ", "always", "true", "false",
	"never"
]

def get_registers(command):
    ret_regs = [-1, -1]
    regs = command.split("_to_")
    for index,value in enumerate(regs):
        if (value == "in"): ret_regs[index] = 6
        elif (value == "out"): ret_regs[index] = 7
        else: ret_regs[index] = value[len(value) - 1]
    return ret_regs[0], ret_regs[1]

registers = [0, 0, 0, 0, 0, 0, 0, 0] # Registers 0-5, input, output
labels_consts = {}
jump_addresses = []

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
            if (len(prog_line) != 0): program.append(prog_line)
        else:
            prog_line = line.strip()
            program.append(prog_line)

# Get the address list for the program
print(program)
address = 0
for line in program:
    args = line.split(" ")
    keyword = args[0]
    if (keyword == "const"): # Const 
        # Check if all arguments exist and are correct
        try:
            arg1 = args[1]
            arg2 = args[2]
        except:
            exit("Error, invalid argument(s) for const")
            
        if (arg1[0] not in ascii_letters): exit("Invalid const name, must start with a letter")
        elif (not args[2].isdigit()): exit("Invalid const value, must be a number")
        elif (arg1 in keywords): exit("Const name cannot be a keyword")
        else: labels_consts[arg1] = arg2
    
    elif (keyword == "label"):
        try: arg1 = args[1]
        except: exit("Error, invalid argument(s) for const")
        
        if (arg1[0] not in ascii_letters): exit("Invalid const name, must start with a letter")
        elif (arg1 in keywords): exit("Loop name cannot be a keyword")
        else: labels_consts[arg1] = address + 1
    
    elif ("_to_" in keyword): # Copy command
        from_reg, to_reg = get_registers(keyword)
        registers[to_reg] = registers[from_reg]