__author__ = 'davidberiro'

import os
from Parser import *
from CodeWriter import *
import sys

files = []
directory = sys.argv[1]
if directory.endswith(".vm"):
    outputname = directory.split("/")[-1][:-3]
    length = -(len(outputname) + 4)
    directory = directory[:length]


else:
    outputname = directory.split("/")[-1]

os.chdir(directory)

for f in os.listdir("."):
    if f.endswith(".vm"):
        files.append(f)

codewriter = CodeWriter(outputname)

for file in files:
    print (file)
    parser = Parser.Parser(file)
    codewriter.setFileName(file[:-3])

    while parser.hasMoreCommands():
        parser.advance()
        command = parser.commandType()

        if command == Parser.C_ARITHMETIC:
            codewriter.writeArithmetic(parser.arg1())
        elif command == Parser.C_POP or command == Parser.C_PUSH:
            if command == Parser.C_POP:
                com = "pop"
            else:
                com = "push"
            segment = parser.arg1()
            index = parser.arg2()
            print ("command: " + com + ", segment: " + segment + ", index: " + str(index))
            codewriter.writePushPop(com, segment, index)

codewriter.Close()








