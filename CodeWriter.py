__author__ = 'davidberiro'
import Parser



class CodeWriter:

    def __init__(self, filename):
        name = filename + ".asm"
        self.outFile = open(name, 'w')

    def setFileName(self,fileName):
        self.fileName = fileName

    def writeArithmetic (self,command):
        pass

    def writePushPop (self,command,segment,index):
        if command == "push":
            if segment == "static":
                self.writeStatic("M", index)
            elif segment == "constant":
                self.writeAddress(index) # maybe the index need to be in string - need to chack all 'index'
                self.writeEqual("D", "A")
            else:
                self.writeSeg(segment,index)
                self.writeEqual("A", "D+A")
                self.writeEqual("D", "M")
            self.writeAddress("SP")
            self.writeEqual("A","M")
            self.writeEqual("M", "D")
            self.writeAddress("SP")
            self.writeEqual("M", "M+1")

        elif command == "pop":
            if segment == "static":
                self.writeStatic("A", index)
            else:
                self.writeSeg(segment, index)
                self.writeEqual("D", "D+A")
            self.writeAddress("R13")
            self.writeEqual("M", "D")
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