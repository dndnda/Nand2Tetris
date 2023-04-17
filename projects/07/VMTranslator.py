import sys
class VMTranslator():
    
    def __init__(self, path):
        self.asmCodes = self.load(path)
        self.outFilePath = path.replace('vm', 'asm')
        self.f = open(path.replace('vm', 'asm'), 'w')
        self.filename = self.f.name.split('\\')[-1].split('.')[0]
        self.segmentMap = {
            "argument": "ARG",
            "local": "LCL",
            "this":"THIS",
            "that":"THAT"
        }
        self.eq = 0
        self.gt = 0
        self.lt = 0
    
    def load(self, path):
        asm = []
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.lstrip().rstrip('\n').rstrip()
                if (line.startswith("//") or len(line)==0):
                    continue
                else:
                    asm.append(line.split(' '))
        return asm
    
    def push(self, vmCode):
        if len(vmCode) != 3:
            print("code pattern wrong! vmCode should contains three seperate code")
            return 
        # write annotation
        push = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.f.write(f"// push {vmCode[1]} {vmCode[2]}\n")
        segment = vmCode[1]
        if segment == "constant":
            self.f.write(f"@{vmCode[2]}\nD=A\n{push}")
        elif segment == "argument":
            self.f.write(f"@ARG\nD=M\n@{vmCode[2]}\nD=D+A\nA=D\nD=M\n{push}")
        elif segment == "local":
            self.f.write(f"@LCL\nD=M\n@{vmCode[2]}\nD=D+A\nA=D\nD=M\n{push}")
        elif segment == "static":
            self.f.write(f"@{self.filename}.{vmCode[2]}\nD=M\n{push}")
        elif segment == "temp":
            self.f.write(f"@5\nD=A\n@{vmCode[2]}\nD=D+A\nA=D\nD=M\n{push}")
        elif segment == "this":
            self.f.write(f"@THIS\nD=M\n@{vmCode[2]}\nD=D+A\nA=D\nD=M\n{push}")
        elif segment == "that":
            self.f.write(f"@THAT\nD=M\n@{vmCode[2]}\nD=D+A\nA=D\nD=M\n{push}")
        elif segment == "pointer":
            if int(vmCode[2]) == 0:
                p = "THIS"
            elif int(vmCode[2]) == 1:
                p = "THAT"
            self.f.write(f"@{p}\nD=M\n{push}")
        self.f.write("\n")

    def pop(self, vmCode):

        self.f.write(f"// pop {vmCode[1]} {vmCode[2]}\n")
        segment = vmCode[1]
        if segment == "constant":
            self.f.write(f"@SP\nM=M-1\n")
        elif segment in {"argument", "local", "this", "that"}:
            self.f.write(f"@{vmCode[2]}\nD=A\n@{self.segmentMap[vmCode[1]]}\nD=D+M\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D\n")
        elif segment == "static":
            self.f.write(f"@SP\nAM=M-1\nD=M\n@{self.filename}.{vmCode[2]}\nM=D\n")
        elif segment == "temp":
            self.f.write(f"@5\nD=A\n@{vmCode[2]}\nD=D+A\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D\n")
        elif segment == "pointer":  
            if int(vmCode[2]) == 0:
                p = "THIS"
            elif int(vmCode[2]) == 1:
                p = "THAT"
            self.f.write(f"@SP\nAM=M-1\nD=M\n@{p}\nM=D\n")
        
        self.f.write("\n")

    def arithmetic(self, vmcode):
        if len(vmcode) > 1:
            print("vmcode should has length 1.")
            return
        
        self.f.write(f"// {vmcode[0]}\n")
        operator = vmcode[0]
        if operator == "add":
            self.f.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n")
        elif operator == "sub":
            self.f.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n")
        elif operator == "neg":
            self.f.write("@SP\nAM=M-1\nM=-M\n@SP\nM=M+1\n")
        elif operator == "and":
            self.f.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n")
        elif operator == "or":
            self.f.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n")
        elif operator == "not":
            self.f.write("@SP\nAM=M-1\nM=!M\n@SP\nM=M+1")
        elif operator == "eq":
            self.f.write(f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@eq_{self.eq}\nD;JNE\n@SP\nA=M-1\nM=-1\n(eq_{self.eq})\n")
            self.eq += 1
        elif operator == "gt":
            self.f.write(f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@gt_{self.gt}\nD;JGT\n@SP\nA=M-1\nM=0\n(gt_{self.gt})\n")
            self.gt += 1
        elif operator == "lt":
            self.f.write(f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@lt_{self.lt}\nD;JLT\n@SP\nA=M-1\nM=0\n(lt_{self.lt})\n")
            self.lt += 1

        self.f.write("\n")

    def translate(self):
        for item in self.asmCodes:
            if len(item) == 1:
                self.arithmetic(item)
            elif item[0] == "pop":
                self.pop(item)
            elif item[0] == "push":
                self.push(item)
        self.f.close()


def main():

    path = sys.argv[1]
    ts = VMTranslator(path)
    ts.translate()


if __name__ == "__main__":
    main()






