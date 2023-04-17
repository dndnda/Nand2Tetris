import sys

# class Assembler():
#     def __init__(self):
#         self.symbolTable = {
#             "R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,
#             "R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,
#             "SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"SCREEN":16384,"KBD":24576
#         }
#         self.avalibleAddress = 16

#     def load(self, path):
#         pureCode = list()
#         with open(path, encoding='utf-8') as f:
#             lines = f.readlines()
#             for line in lines:
#                 tmp = line.rstrip('\n').replace(' ', '')
#                 if (not tmp.startswith('//')) and len(tmp) != 0:
#                     tmp = tmp.split("//")[0]
#                     pureCode.append(tmp)
#         self.instructionList = pureCode

#     def firstPass(self):
#         instructions = self.instructionList
#         newInstruc = []
#         row = 0
#         for instruction in instructions:
#             if instruction.startswith('('):
#                 self.symbolTable[instruction[1:-1]] = row
#             else:
#                 row += 1
#                 newInstruc.append(instruction)
#         self.instructionList = newInstruc

#     def secondPass(self):
#         instructions = self.instructionList
#         newInstruc = []
#         for instruction in instructions:
#             symbol = instruction[1:]
#             if instruction.startswith('@') and not symbol.isnumeric():
#                 if symbol not in self.symbolTable:
#                     self.symbolTable[symbol] = self.avalibleAddress
#                     self.avalibleAddress += 1
#                 newInstruc.append("@" + str(self.symbolTable[symbol]))
#             else:
#                 newInstruc.append(instruction)
#         self.instructionList = newInstruc


class Parser():

    def __init__(self, path):
        pureCode = list()
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                tmp = line.rstrip('\n').replace(' ', '')
                if (not tmp.startswith('//')) and len(tmp) != 0:
                    tmp = tmp.split("//")[0]
                    pureCode.append(tmp)
        self.instructionList = pureCode
        self.nextIndex = 0
        self.correntInstru = ""
        self.constant = {
            "A":"A_INSTRUCTION",
            "C":"C_INSTRUCTION",
            "L":"L_INSTRUCTION"
        }

    def hasMoreLines(self):
        return self.nextIndex < len(self.instructionList)
    def advance(self):
        self.correntInstru = self.instructionList[self.nextIndex]
        self.nextIndex += 1

    def instructionType(self):
        if self.correntInstru.startswith('@'):
            return self.constant["A"]
        if self.correntInstru.startswith('(') and self.correntInstru.endswith(')'):
            return self.constant["L"]
        else:
            return self.constant["C"]
    def symbol(self):
        if self.correntInstru.startswith('@'):
            return self.correntInstru[1:]
        elif self.correntInstru.startswith('(') and self.correntInstru.endswith(')'):
            return self.correntInstru[1:-1]
        
    def dest(self):
        if not '=' in self.correntInstru:
            return None
        tmp = self.correntInstru.split('=')
        return tmp[0]
        
    def comp(self):
        if '=' in self.correntInstru:
            return self.correntInstru.split('=')[1].split(';')[0]
        else:
            return self.correntInstru.split(';')[0]
    def jump(self):
        if not ';' in self.correntInstru:
            return None
        return self.correntInstru.split(';')[-1]

class Code():
    def __init__(self) -> None:
        pass
    @classmethod
    def dest(cls, s):
        if s is None:
            return "000"
        elif s == "M":
            return "001"
        elif s == "D":
            return "010"
        elif s == "DM" or s == "MD":
            return "011"
        elif s == "A":
            return "100"
        elif s == "AM" or s == "MA":
            return "101"
        elif s == "AD" or s == "DA":
            return "110"
        elif s == "ADM" or s == "AMD" or s == "DAM" or s == "DMA" or s == "MDA" or s == "MAD":
            return "111"
        
    @classmethod
    def comp(cls, s):
        if s == "0":
            return "0101010"
        elif s == "1":
            return "0111111"
        elif s == "-1":
            return "0111010"
        elif s == "D":
            return "0001100"
        elif s == "A" or s == "M":
            if s == "A":
                return "0110000"
            else:
                return "1110000"
        elif s == "!D":
            return "0001101"
        elif s == "!A" or s == "!M":
            if s == "!A":
                return "0110001"
            else:
                return "1110001"
        elif s == "-D":
            return "0001111"
        elif s == "-A" or s == "-M":
            if s == "-A":
                return "0110011"
            else:
                return "1110011"
        elif s == "D+1":
            return "0011111"
        elif s == "A+1" or s == "M+1":
            if s == "A+1":
                return "0110111"
            else:
                return "1110111"
        elif s == "D-1":
            return "0001110"
        elif s == "A-1" or s == "M-1":
            if s == "A-1":
                return "0110010"
            else:
                return "1110010"
        elif s == "D+A":
            return "0000010"
        elif s == "D+M":
            return "1000010"
        elif s == "D-A":
            return "0010011"
        elif s == "D-M":
            return "1010011"
        elif s == "A-D":
            return "0000111"
        elif s == "M-D":
            return "1000111"
        elif s == "D&A":
            return "0000000"
        elif s == "D&M":
            return "1000000"
        elif s == "D|A":
            return "0010101"
        elif s == "D|M":
            return "1010101"
        
    @classmethod
    def jump(cls, s):
        if s is None:
            return "000"
        elif s == "JGT":
            return "001"
        elif s == "JEQ":
            return "010"
        elif s == "JGE":
            return "011"
        elif s == "JLT":
            return "100"
        elif s == "JNE":
            return "101"
        elif s == "JLE":
            return "110"
        elif s == "JMP":
            return "111"

class Assembler():
    
    def __init__(self, path):
        self.filename = path.split('\\', -1)[-1].split('.')[0]
        self.paser = Parser(path)
        self.avalibleAddress = 16
        self.symbolTable = SymbolTable()
    
    def firstPass(self):
        row = 0
        paser = self.paser
        while paser.hasMoreLines():
            paser.advance()
            type = paser.instructionType()
            if type == paser.constant["L"]:
                sym = paser.symbol()
                self.symbolTable.addEntry(sym, row)
            else:
                row += 1
        self.paser.nextIndex = 0
    
    def decode(self):
        self.firstPass()

        paser = self.paser
        outFile = self.filename + ".hack"
        row = 0
        with open(outFile, 'w') as f:
            while paser.hasMoreLines():
                paser.advance()
                type = paser.instructionType()
                #print(type)
                if type == paser.constant["A"]:
                    row += 1
                    symbol = paser.symbol()
                    if not symbol.isnumeric() and not self.symbolTable.contains(symbol):
                        self.symbolTable.addEntry(symbol, self.avalibleAddress)
                        self.avalibleAddress += 1
                    if symbol.isnumeric():
                        f.write(f'{int(symbol):016b}')
                        f.write('\n')
                    else:
                        #print(self.symbolTable.getAddress(symbol))
                        f.write(f'{int(self.symbolTable.getAddress(symbol)):016b}')
                        f.write('\n')
                elif type == paser.constant["L"]:
                    symbol = paser.symbol()
                    self.symbolTable.addEntry(symbol, row)
                elif type == paser.constant["C"]:
                    row += 1
                    dest = paser.dest()
                    #print(dest, len(dest))
                    comp = paser.comp()
                    jump = paser.jump()
                    f.write("111" + Code.comp(comp) +  Code.dest(dest) + Code.jump(jump))
                    f.write('\n')
            

class SymbolTable():
    def __init__(self):
        self.symbolTable = {
            "R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,
            "R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,
            "SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"SCREEN":16384,"KBD":24576
        }
        
    def addEntry(self, symbol, address):
        self.symbolTable[symbol] = int(address)
    def contains(self, symbol):
        return symbol in self.symbolTable
    def getAddress(self, symbol):
        return self.symbolTable[symbol]

                    







def main():
    path = sys.argv[1]
    ass = Assembler(path)
    ass.decode()

    

    
    # with open('demo.hack', 'w') as f:
    #     for line in pureCode:
    #         line += '\n'
    #         f.write(line)


if __name__ == "__main__":
    main()
