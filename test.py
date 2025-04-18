regs = ["reg" + str(x) for x in range(0,6)]
regs.append("in")
regs.append("out")

commands = []
keywords = ["AND", "EQ", "GEQ", "GRE", "LEQ", "LES", "NAND", "NEQ", "OR", "add", "always", "false", "never", "sub", "submit", "true"]

for i in regs:
    print(i)
    
    
for i in regs:
    for j in regs:
        if (i == j or i == "out"): continue
        else: commands.append(f"{i}_to_{j}")

combined = commands + keywords
print("keywords = {", end = " ")
for index,command in enumerate(combined):
    print(f"{'\n\t' if index%5 == 0 else ''}" + '"' + command + '"', end = ", " if index != len(combined) - 1 else "")
print("\n}")

