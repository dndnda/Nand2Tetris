lines = []
with open("StackArithmetic\SimpleAdd\SimpleAdd.vm") as f:
    print(f.name)
    s = f.readlines()
    for line in s:
        line = line.lstrip().rstrip('\n')
        if (line.startswith("//") or len(line)==0):
            continue
        else:
            temp = line.split(' ')
            lines.append(temp)
            #print(temp)

print(lines)

