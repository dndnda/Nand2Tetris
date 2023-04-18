import sys
import os

class VMTranslator():
    
    def __init__(self, path):
        #self.asmCodes = self.load(path)
        self.muti = False
        if path.endswith('.vm'):
            outFilePath = path.replace('vm', 'asm')
            self.asmCodes = self.load(path)
        else:
            #print("+=+=======>>" + path.split('\\')[-2])
            self.muti = True
            outFilePath = path + path.split('\\')[-2] + ".asm" 
            #print("path: "+ path)
            #print("outFilePath:" + "==========>" + outFilePath)
            files = os.listdir(path)
            tempCode = []
            for file in files:
                if file.endswith('.vm'):
                    tempCode += self.load(os.path.join(path, file))
            self.asmCodes = tempCode

        self.f = open(outFilePath, 'w')
        #self.filename = self.f.name.split('\\')[-1].split('.')[0]
        self.segmentMap = {
            "argument": "ARG",
            "local": "LCL",
            "this":"THIS",
            "that":"THAT"
        }
        self.eq = 0
        self.gt = 0
        self.lt = 0
        self.funcRetunI = dict()
    
    def load(self, path):
        asm = []
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.lstrip().rstrip('\n').rstrip()
                if (line.startswith("//") or len(line)==0):
                    continue
                elif "//" in line:
                    line = line.split("//")[0].rstrip(' ')
                
                asm.append(line.split(' '))
        return asm
    
    def writeInit(self):
        push_D = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        s = "@256\nD=A\n@SP\nM=D\n\n"
        s += "@1\nD=A\n@LCL\nM=D\n@2\nD=A\n@ARG\nM=D\n@3\nD=A\n@THIS\nM=D\n@4\nD=A\n@THAT\nM=D\n"
        s += "@bootstrap\nD=A\n" + push_D
        s += "@LCL\nD=M\n" + push_D
        s += "@ARG\nD=M\n" + push_D
        s += "@THIS\nD=M\n" + push_D
        s += "@THAT\nD=M\n" + push_D
        s += "@5\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@Sys.init\n0;JMP\n(bootstrap)\n"
        self.f.write(s)


    # def bootstrap(self):
    #     self.f.write("// init the stack\n@256\nD=A\n@SP\nM=D\n\n")

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

    def writeLabel(self, vmCode):
        self.f.write(f"// label {vmCode[1]}\n")
        self.f.write(f"({vmCode[1]})\n")
        self.f.write("\n")

    def writeGoto(self, vmCode):
        self.f.write(f"// goto {vmCode[1]}\n")
        self.f.write(f"@{vmCode[1]}\n0;JMP\n")
        self.f.write("\n")

    def writeIf(self, vmCode):
        self.f.write(f"// if-goto {vmCode[1]}\n")
        self.f.write(f"@SP\nAM=M-1\nD=M\n@{vmCode[1]}\nD;JNE\n")
        self.f.write("\n")

    def writeFunction(self, vmCode):
        # functionName = f"{vmCode[1]}"
        # self.filename = vmCode[1].split('.')[0]
        # self.f.write(f"// function {vmCode[1]} {vmCode[2]}\n")
        # self.f.write(f"// Init R13 to n, R14 to i=0\n({functionName})\n@{vmCode[2]}\nD=A\n@R13\nM=D\n@R14\nM=0\n")
        # self.f.write("// condition judge\n")
        # self.f.write(f"({functionName}$condition)\n")
        # self.f.write(f"@R13\nD=M\n@R14\nD=M-D\n@end${functionName}$loop\nD;JGE\n")
        # self.f.write("// Init local vars\n")
        # #self.f.write(f"@R14\nD=M\n@LCL\nA=D+M\nM=0\n@SP\nM=M+1\n@R14\nM=M+1\n")
        # self.f.write(f"@SP\nA=M\nM=0\n@SP\nM=M+1\n@R14\nM=M+1\n@{functionName}$condition\n0;JMP\n(end${functionName}$loop)\n")
        # self.f.write("\n")
        self.filename = vmCode[1].split('.')[0]
        self.f.write(f"// function {vmCode[1]} {vmCode[2]}\n")
        self.f.write(f"({vmCode[1]})")
        n = int(vmCode[2])
        for i in range(n):
            self.f.write("@SP\nA=M\nM=0\n@SP\nM=M+1\n")
        self.f.write("\n")

    def writeCall(self, vmCode):
        
        self.f.write(f"// call {vmCode[1]} {vmCode[2]}\n")
        #self.f.write("// push returAddress\n")
        #self.f.write(f"@{vmCode[1]}$ret.{self.funcRetunI[vmCode[1]]}\nD=M\n@SP\nM=D\n@SP\nM=M+1\n")
        self.f.write(f"@{vmCode[1]}$ret.{self.funcRetunI[vmCode[1]]}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        #self.f.write("// push LCL\n")
        self.f.write("@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        #self.f.write("// push ARG\n")
        self.f.write("@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        #self.f.write("// push THIS\n")
        self.f.write("@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        #self.f.write("// push THAT\n")
        self.f.write("@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        #self.f.write("")
        num = 5 + int(vmCode[2])
        self.f.write(f"@SP\nD=M\n@{num}\nD=D-A\n@ARG\nM=D\n")
        self.f.write(f"@SP\nD=M\n@LCL\nM=D\n")
        self.f.write(f"@{vmCode[1]}\n0;JMP\n({vmCode[1]}$ret.{self.funcRetunI[vmCode[1]]})\n")
        self.f.write('\n')
    
    def writeReturn(self):
        self.f.write("// return\n")

        # R15 -> frame  R13 -> retAddr  R14 -> temp
        s = "@LCL\nD=M\n@R15\nM=D\n@R14\nM=D\n@5\nD=A\n@R14\nA=M-D\nD=M\n@R13\nM=D\n"
        s += "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n"
        s += "@ARG\nD=M+1\n@SP\nM=D\n"
        s += "@R15\nD=M\nD=D-1\nA=D\nD=M\n@THAT\nM=D\n"
        s += "@R15\nD=M\n@2\nD=D-A\nA=D\nD=M\n@THIS\nM=D\n"
        s += "@R15\nD=M\n@3\nD=D-A\nA=D\nD=M\n@ARG\nM=D\n"
        s += "@R15\nD=M\n@4\nD=D-A\nA=D\nD=M\n@LCL\nM=D\n"
        s += "@R13\nA=M\n0;JMP\n"
        s += "\n"
        self.f.write(s)

    
    def translate(self):
        if self.muti:
            self.writeInit()

        for item in self.asmCodes:
            if len(item) == 1 and item[0] != "return":
                self.arithmetic(item)
            elif item[0] == "pop":
                self.pop(item)
            elif item[0] == "push":
                self.push(item)
            elif item[0] == "label":
                self.writeLabel(item)
            elif item[0] == "goto":
                self.writeGoto(item)
            elif item[0] == "if-goto":
                self.writeIf(item)
            elif item[0] == "call":
                if item[1] not in self.funcRetunI:
                    self.funcRetunI[item[1]] = 0
                else:
                    self.funcRetunI[item[1]] += 1

                self.writeCall(item)
            elif item[0] == "function":
                self.writeFunction(item)
            elif item[0] == "return":
                self.writeReturn()
        self.f.close()


def main():

    path = sys.argv[1]
    #print(path)
    ts = VMTranslator(path)
    ts.translate()


if __name__ == "__main__":
    main()






