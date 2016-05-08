__author__ = 'davidberiro'

import os
from Parser import *
from CodeWriter import *
import sys

files = []
directory = argv[1]
os.chdir(directory)

if directory.endwith(".vm"):
    outputname = directory.split("/")[-1][:-3]
    os.chdir("..")
else:
    outputname = directory.split("/")[-1]


for f in os.listdir("."):
    if f.endwith(".vm"):
        files.append(f)

codewriter = CodeWriter(outputname)

for file in files:
    parser = parser(file)
    codewriter.setFileName(file[:-3])

    while parser.hasMoreCommands():
        parser.advance()
        command = parser.commandType()

        if command == parser.C_ARITHMETIC:
            codewriter.writeArithmetic(parser.arg1())
        elif command == parser.C_POP or command == parser.C_PUSH:
            if command == parser.C_POP:
                com = "pop"
            else:
                com = "push"
            segment = parser.arg1()
            index = parser.arg2()
            codewriter.writePushPop(com, segment, index)

codewriter.close()








