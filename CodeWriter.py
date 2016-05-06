__author__ = 'davidberiro'
import Parser


class CodeWriter:

    def __init__(self, filename):
        # self.parser = Parser(inputFile)
        self.outFile = open("filename", "wb")

    def setFileName(self,fileName):
        self.fileName = fileName

    def writeArithmetic (self,command):
        self

    def WritePushPop (self,command,segment,index):
        self

    def Close(self):
        self.outFile.close()