
__author__ = 'davidberiro'

ARITHMETIC_COMMAND = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
POP = "pop"
PUSH = "push"

C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9


class Parser:



    def __init__(self, inputFileName):
        self.inputFile = open(inputFileName, 'r')
        self.currentLine = None
        self.currentCommand = []
        self.hasNextCommand = False


    def hasMoreCommands(self):
        if self.hasNextCommand:
            return True

        self.currentLine = self.inputFile.readline()

        while self.currentLine:
            self.currentLine = self.currentLine.strip()
            if self.currentLine == "" or self.currentLine.startswith("//"):
                self.currentLine = self.inputFile.readline()
            else:
                self.hasNextCommand = True
                return True

        return False

    def advance(self):
        if self.hasMoreCommands():
            self.currentCommand = self.currentLine.split(' ')
            self.hasNextCommand = False

    def length(self, someList):
        return len(someList)

    def commandType(self):
        if len(self.currentCommand) == 1:
            if self.currentCommand[0] in ARITHMETIC_COMMAND:
                return C_ARITHMETIC
        elif self.currentCommand[0] ==  POP:
            return C_POP
        else:
            return C_PUSH

    def arg1(self):
        if self.currentCommand[0] in ARITHMETIC_COMMAND:
            return self.currentCommand[0]
        else:
            return self.currentCommand[1]

    def arg2(self):
        return self.currentCommand[2]




