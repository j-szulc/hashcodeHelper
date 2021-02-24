from coconut_shell import *
import sys

# {path: numOfThreads
inputs = {"test.txt": 1}

# command to execute worker
worker = "python3 worker.py"

# {inputPath: (solution, solutionScore)}
results = {key: (None,0) for key in inputs}

# Custom Unicode characters from the Private Use section
# Separates messages
separator = '\uE069'

class Msg:
    def __init__(self,type,data):
        self.type = type
        self.data = data

def getMessage(src=input):
    line = separator
    while line == separator:
        line = src()
    result = []
    while line != separator:
        result.append(line)
        line = src()
    return Msg(result[0], result[1:])

def sendMessage(msgType, msgData):
    print(separator)
    print(msgType)
    for line in msgData:
        print(line)
    print(separator)

def requestInput():
    sendMessage("REQUEST_INPUT",[])

def shouldSubmit(score):
    sendMessage("SHOULD_SUBMIT",[score])
    msg = getMessage()
    return score > int(msg.data[0])

def startSubmit():
    print(separator)
    print("SUBMIT")

def endSubmit():
    print(separator)

#def supervise(inputPath):


print(sh(worker)([str(3),separator,"RES_SHOULD_SUBMIT",str(3),separator]).read())