import sys
class VMTranslator():
    
    def __init__(self, path):
        self.asmCodes = self.load(path)
        self.outFilePath = path.replace('vm', 'asm')
        self.f = open(path.replace('vm', 'asm'), 'w')
        self.filename = self.f.name.split('\\')[-1].split('.')[0]
        # self.segmentMap = {
        #     "argument": "ARG",
        #     "local": "LCL",
            
        # }
    
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
        self.f.write(f"// push {vmCode[1]} {vmCode[2]}\n")
        segment = vmCode[1]
        if segment == "constant":
            self.f.write(f"@SP\nA=M\nM={vmCode[2]}\n@SP\nM=M+1\n")
        elif segment == "argument":
            self.f.write(f"@ARG\nD=M\n@{vmCode[2]}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == "local":
            self.f.write(f"@LCL\nD=M\n@{vmCode[2]}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == "static":
            self.write(f"")

    def pop(self, vmCode):
        pass

    def arithmetic(self, vmcode):
        if len(vmcode) > 1:
            print("vmcode should has length 1.")
            return
        operator = vmcode[0]
        


    def closeF(self):
        self.f.close()

def main():

    path = sys.argv[1]
    ts = VMTranslator(path)
    ts.push(ts.asmCodes[0])
    ts.push(ts.asmCodes[1])
    print(ts.filename)
    ts.closeF()


if __name__ == "__main__":
    main()






