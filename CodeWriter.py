__author__ = 'davidberiro'
import Parser



class CodeWriter:

    def __init__(self, filename):
        name = filename + ".asm"
        self.outFile = open(name, 'w')
        self.fileName = ""
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
        self.arithPrefix(True)
        self.outFile.write

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
                self.writeAddress(str(index)) # maybe the index need to be in string - need to chack all 'index'
                self.writeEqual("D", "A")
            else:
                self.writeSeg(segment,index)
                self.writeEqual("A", "D+A")
                self.writeEqual("D", "M")
            self.arithSufix(True)

        elif command == "pop":
            if segment == "static":
                self.writeStatic("A", index)
            else:
                self.writeSeg(segment, index)
                self.writeEqual("D", "D+A")
            self.writeAddress("R13")
            self.writeEqual("M", "D")
            self.arithPrefix(True)
            self.writeEqual("A", "M")
            self.writeEqual("M", "D")

        else:
            return

    def writeSeg(self,segment,index):
        seg = self.buildSeg(segment)
        self.writeAddress(seg)
        if segment == "temp" or "pointer":
            self.writeEqual("D", "A")
        else:
            self.writeEqual("D", "M")
        self.writeAddress(index)

    def writeStatic(self,AorM,index):
        self.writeAddress(self.fileName + "." + index)
        self.outFile.write("\n")
        self.writeEqual("D",AorM)


    def writeEqual(self,arg1,arg2):
        self.outFile.write(arg1 + "=" + arg2)
        self.outFile.write("\n")

    def writeAddress(self,location):
        self.outFile.write("@"+location)
        self.outFile.write("\n")

    def buildSeg(self,seg):
        segment = {
            "this": "THIS",
            "that": "THAT",
            "temp": "R5",
            "pointer": "THIS",
            "local": "LCL",
            "argument": "ARG",
            "constant": ""
        }
        return segment.get(seg, "ERROR")


    def Close(self):
        self.outFile.close()
