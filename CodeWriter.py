

import Parser

Seg = dict(zip(('local','argument','this','that','temp','pointer'),('LCL','ARG','THIS','THAT',5,3)))

class CodeWriter:

    def __init__(self, filename):
        name = filename + ".asm"
        self.outFile = open(name, 'w')
        self.fileName = ""
        self.labelnumber = 0
        self.outFile.write("@256\n")
        self.outFile.write("D=A\n")
        self.outFile.write("@SP\n")
        self.outFile.write("M=D\n")



    def setFileName(self,fileName):
        self.fileName = fileName

    def writeArithmetic(self,command):
        if command == "add":
            self.arithOper("+")
        elif command == "sub":
            self.arithOper("-")
        elif command == "and":
            self.arithOper("&")
        elif command == "or":
            self.arithOper("|")
        elif command == "neg":
            self.arithNegNot("-")
        elif command == "not":
            self.arithNegNot("!")
        elif command == "eq":
            self.arithJump("JEQ")
        elif command == "gt":
            self.arithJump("JGT")
        elif command == "lt":
            self.arithJump("JLT")

    def arithJump(self,jump):
        self.arithOper("-")
        self.outFile.write("@SP\n")
        self.outFile.write("M=M-1\n")
        self.outFile.write("A=M\n")
        self.outFile.write("D=M\n")
        self.outFile.write("@TRUE" + str(self.labelnumber) + "\n")
        self.outFile.write("D;" + jump + "\n")
        self.outFile.write("@SP\n")
        self.outFile.write("A=M\n")
        self.outFile.write("M=0\n")
        self.outFile.write("@SKIP" + str(self.labelnumber) + "\n")
        self.outFile.write("0;JMP\n")
        self.outFile.write("(TRUE" + str(self.labelnumber) + ")\n")
        self.outFile.write("@SP\n")
        self.outFile.write("A=M\n")
        self.outFile.write("M=-1\n")
        self.outFile.write("(SKIP" + str(self.labelnumber) + ")\n")
        self.arithSufix(False)
        self.labelnumber = self.labelnumber + 1

    def arithNegNot(self,sign):
        self.arithPrefix(False)
        temp = sign + "M"
        self.writeEqual("M",temp)
        self.arithSufix(False)

    def arithOper(self,sign):
        self.arithPrefix(True)
        self.writeEqual("M", "D")
        self.arithPrefix(True)
        temp = "D" + sign + "M"
        self.writeEqual("D", temp)
        self.arithSufix(True)


    def arithPrefix(self,extand):
        self.writeAddress("SP")
        self.writeEqual("MD", "M-1")
        self.writeEqual("A", "D")
        if extand:
            self.writeEqual("D", "M")
            self.writeAddress("R13")

    def arithSufix(self,extand):
        if extand:
            self.writeAddress("SP")
            self.writeEqual("A", "M")
            self.writeEqual("M", "D")
        self.writeAddress("SP")
        self.writeEqual("M", "M+1")



    def writePushPop (self,command,segment,index):
        if command == "push":
            if segment == "static":
                self.writeStatic("M", index)
            elif segment == "constant":
                self.writeAddress(str(index))
                self.writeEqual("D", "A")
            elif segment in ("temp","pointer"):
                self.outFile.write("@%d\n" %(Seg.get(segment) + int(index)))
                self.outFile.write("D=M\n")
            elif segment == "static":
                self.outFile.write("@" + self.fileName + str(index) + "\n")
                self.outFile.write("D=M\n")
            else:
                symbol = Seg.get(segment)
                self.outFile.write("@%s\n" %symbol)
                self.outFile.write("D=M\n")
                self.outFile.write("@%s\n" %index)
                self.outFile.write("A=D+A\n")
                self.outFile.write("D=M\n")
            self.writeAddress("SP")
            self.writeEqual("A", "M")
            self.writeEqual("M", "D")
            self.writeAddress("SP")
            self.writeEqual("M", "M+1")

        elif command == "pop":
            if segment == "static":
                self.outFile.write("@" + self.fileName + str(index) + "\n")
                self.outFile.write("D=A\n")
                self.outFile.write("@R13\n")
                self.outFile.write("M=D\n")
            elif segment in ("temp", "pointer"):
                self.outFile.write("@%d\n" %(Seg.get(segment) + int(index)))
                self.outFile.write("D=A\n")
                self.outFile.write("@R13\n")
                self.outFile.write("M=D\n")
            else:
                symbol = Seg.get(segment)
                self.writeAddress(index)
                self.outFile.write("D=A\n")
                self.writeAddress(symbol)
                self.outFile.write("A=M\n")
                self.outFile.write("D=D+A\n")
                self.outFile.write("@R13\n")
                self.outFile.write("M=D\n")

            self.writeAddress("SP")
            self.writeEqual("M", "M-1")
            self.writeAddress("SP")
            self.writeEqual("A", "M")
            self.writeEqual("D", "M")
            self.writeAddress("R13")
            self.writeEqual("A", "M")
            self.writeEqual("M", "D")


        else:
            return

    def writeStatic(self,AorM,index):
        self.writeAddress(self.fileName + index)
        self.writeEqual("D",AorM)


    def writeEqual(self,arg1,arg2):
        self.outFile.write(arg1 + "=" + arg2)
        self.outFile.write("\n")

    def writeAddress(self,location):
        self.outFile.write("@"+location)
        self.outFile.write("\n")


    def Close(self):
        self.outFile.close()
