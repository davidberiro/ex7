
# __author__ = 'davidberiro'
# import Parser
#
#
#
# class CodeWriter:
#
#     def __init__(self, filename):
#         name = filename + ".asm"
#         self.outFile = open(name, 'w')
#         self.fileName = ""
#         self.outFile.write("@256\n")
#         self.outFile.write("D=A\n")
#         self.outFile.write("@SP\n")
#         self.outFile.write("M=D\n")
#
#     def setFileName(self,fileName):
#         self.fileName = fileName
#
#     def writeArithmetic(self,command):
#         if command == "add":
#             self.arithOper("+")
#         elif command == "sub":
#             self.arithOper("-")
#         elif command == "and":
#             self.arithOper("&")
#         elif command == "or":
#             self.arithOper("|")
#         elif command == "neg":
#             self.arithNegNot("-")
#         elif command == "not":
#             self.arithNegNot("!")
#         elif command == "eq":
#             self.arithJump("JEQ")
#         elif command == "gt":
#             self.arithJump("JGT")
#         elif command == "lt":
#             self.arithJump("JLT")
#
#     def arithJump(self,jump):
#         pass
#
#     def arithOper(self,sign):
#         self.decSP()
#         self.popPushToD(False)
#         self.writeAddress("R13")
#         self.writeEqual("M", "D")
#         self.decSP()
#         self.popPushToD(False)
#         self.writeAddress("R13")
#         temp = "D" + sign + "M"
#         self.writeEqual("D", temp)
#         self.popPushToD(True)
#         self.incSP()
#
#         # self.arithPrefix(True)
#         # self.arithPrefix(True)
#         # self.arithSufix(True)
#
#
#     def arithNegNot(self, sign):
#         self.decSP()
#         self.popToA()
#         temp = sign + "M"
#         self.writeEqual("M", temp)
#         self.incSP()
#         # self.arithPrefix(False)
#         # self.arithSufix(False)
#
#     def incSP(self):
#         self.writeAddress("SP")
#         self.writeEqual("M","M+1")
#
#     def decSP(self):
#         self.writeAddress("SP")
#         self.writeEqual("M", "M-1")
#
#     def popPushToD(self,push):
#         self.writeAddress("SP")
#         self.writeEqual("A", "M")
#         if push:
#             self.writeEqual("M", "D")
#         else:
#             self.writeEqual("D", "M")
#
#     def popToA(self):
#         self.writeAddress("SP")
#         self.writeEqual("A", "M")
#         #self.writeEqual("A", "M")
#
#     # def arithPrefix(self,extand):
#     #     self.writeAddress("SP")
#     #     self.writeEqual("MD", "M-1")
#     #     self.writeEqual("A", "D")
#     #     if extand:
#     #         self.writeEqual("D", "M")
#     #         self.writeAddress("R13")
#     #
#     # def arithSufix(self,extand):
#     #     if extand:
#     #         self.writeAddress("SP")
#     #         self.writeEqual("A", "M")
#     #         self.writeEqual("M", "D")
#     #     self.writeAddress("SP")
#     #     self.writeEqual("M", "M+1")
#
#
#
#     def writePushPop (self,command,segment,index):
#         if command == "push":
#             if segment == "static":
#                 self.writeStatic("M", index)
#             elif segment == "constant":
#                 self.writeAddress(str(index)) # maybe the index need to be in string - need to chack all 'index'
#                 self.writeEqual("D", "A")
#             else:
#                 self.writeSeg(segment,index)
#                 self.writeEqual("A", "D+A")
#                 self.writeEqual("D", "M")
#             self.popPushToD(True)
#             self.incSP()
#             # self.arithSufix(True)
#
#         elif command == "pop":
#             if segment == "static":
#                 self.writeStatic("A", index)
#             else:
#                 self.writeSeg(segment, index)
#                 self.writeEqual("D", "D+A")
#             self.writeAddress("R13")
#             self.writeEqual("M", "D")
#             self.decSP()
#             self.popPushToD(False)
#             self.writeAddress("R13")
#             # self.arithPrefix(True)
#             self.writeEqual("A", "M")
#             self.writeEqual("M", "D")
#
#         else:
#             return
#
#     def writeSeg(self,segment,index):
#         seg = self.buildSeg(segment)
#         self.writeAddress(seg)
#         if segment == "temp" or "pointer":
#             self.writeEqual("D", "A")
#         else:
#             self.writeEqual("D", "M")
#         self.writeAddress(index)
#
#     def writeStatic(self,AorM,index):
#         self.writeAddress(self.fileName + "." + index)
#         self.outFile.write("\n")
#         self.writeEqual("D",AorM)
#
#     def writeEqual(self,arg1,arg2):
#         self.outFile.write(arg1 + "=" + arg2)
#         self.outFile.write("\n")
#
#     def writeAddress(self,location):
#         self.outFile.write("@"+location)
#         self.outFile.write("\n")
#
#     def buildSeg(self,seg):
#         segment = {
#             "this": "THIS",
#             "that": "THAT",
#             "temp": "R5",
#             "pointer": "THIS",
#             "local": "LCL",
#             "argument": "ARG",
#             "constant": ""
#         }
#         return segment.get(seg, "ERROR")
#
#
#     def Close(self):
#         self.outFile.close()

import Parser

Seg = dict(zip(('local', 'argument', 'this', 'that', 'temp', 'pointer'), ('LCL', 'ARG', 'THIS', 'THAT', 5, 3)))
HACK_REGISTER = {"this":"THIS", "that":"THAT", "temp":"R5", "pointer":"THIS", "local":"LCL","argument":"ARG","constant":""}


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



    # def writePushPop (self,command,segment,index):
        # if command == "push":
        #     if segment == "static":
        #         self.writeStatic("M", index)
        #     elif segment == "constant":
        #         self.writeAddress(str(index)) # maybe the index need to be in string - need to chack all 'index'
        #         self.writeEqual("D", "A")
        #     elif segment == "temp":
        #         temp = Seg.get(segment) + int(index)
        #         self.writeAddress(temp)
        #         self.writeEqual("D","M")
        #     elif segment == "pointer":
        #         temp = Seg.get(segment) + int(index)
        #         self.writeAddress(temp)
        #         self.writeEqual("D", "M")
        #     else:
        #         # self.writeSeg(segment,index)
        #         self.writeAddress(Seg.get(segment))
        #         self.writeEqual("D", "M")
        #         self.writeAddress(index)
        #         self.writeEqual("A", "D+A")
        #         self.writeEqual("D", "M")
        #     # self.arithSufix(True)
        #     self.writeAddress("SP")
        #     self.writeEqual("A", "M")
        #     self.writeEqual("M", "D")
        #     self.writeAddress("SP")
        #     self.writeEqual("M", "M+1")
        #
        # elif command == "pop":
        #     if segment == "static":
        #         self.writeStatic("A", index)
        #         self.writeAddress("R13")
        #         self.writeEqual("M", "D")
        #     elif segment == "temp":
        #         temp = Seg.get(segment) + int(index)
        #         self.writeAddress(temp)
        #         self.writeEqual("D", "A")
        #         self.writeAddress("R13")
        #         self.writeEqual("M", "D")
        #     elif segment == "pointer":
        #         temp = Seg.get(segment) + int(index)
        #         self.writeAddress(temp)
        #         self.writeEqual("D", "A")
        #         self.writeAddress("R13")
        #         self.writeEqual("M", "D")
        #     else:
        #         # self.writeSeg(segment, index)
        #         self.writeAddress(Seg.get(segment))
        #         self.writeEqual("D", "M")
        #         self.writeAddress(index)
        #         self.writeEqual("D", "D+A")
        #         self.writeAddress("R13")
        #         self.writeEqual("M", "D")
        #         # self.writeEqual("D", "M")
        #     self.writeAddress("SP")
        #     self.writeEqual("M", "M-1")
        #     self.writeAddress("SP")
        #     self.writeEqual("A", "M")
        #     self.writeEqual("D", "M")
        #     self.writeAddress("R13")
        #     self.writeEqual("A", "M")
        #     self.writeEqual("M", "D")
        #     # self.writeEqual("M", "M+1")
        #     # self.writeEqual("D", "D+A")
        #     # self.arithPrefix(True)
        #     # self.writeEqual("A", "M")
        #     # self.writeEqual("M", "D")
        #
        # else:
        #     return

    def writePushPop(self, command, segment, index):
        if command == "push":
            if segment == "static":
                self.writeAddress(self.fileName + "." + index)
                self.writeEqual("D", "M")
            elif segment == "constant":
                self.writeAddress(str(index))
                self.writeEqual("D", "A")
            else:
                self.writeAddress(HACK_REGISTER[segment])
                if segment == "temp" or segment == "pointer":
                    self.writeEqual("D", "A")
                else:
                    self.writeEqual("D", "M")
                self.writeAddress(index)
                self.writeEqual("A", "D+A")
                self.writeEqual("D", "M")

            self.writeAddress("SP")
            self.writeEqual("A", "M")
            self.writeEqual("M", "D")
            self.writeAddress("SP")
            self.writeEqual("M", "M+1")


        elif command == "pop":
            if segment == "static":
                self.writeAddress(self.fileName + "." + index)
                self.writeEqual("D", "A")
            else:
                self.writeAddress(HACK_REGISTER[segment])
                if segment == "temp" or segment == "pointer":
                    self.writeEqual("D", "A")
                else:
                    self.writeEqual("D", "M")
                self.writeAddress(index)
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
        self.writeAddress(self.fileName + index)
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
