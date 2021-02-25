from coconut_shell import *
import sys
import threading

# {path: numOfThreads
inputs = {"test.txt": 1}

# command to execute worker
worker = "python3 worker.py"

# {inputPath: (solution, solutionScore)}
results = {key: (None,0) for key in inputs}
mutex = threading.Lock()

# Custom Unicode characters from the Private Use section
# Separates messages
separator = '\uE069'

class Msg:
    def __init__(self,type,data):
        self.type = type
        self.data = data
    def __str__(self):
        return "TYPE: {}\nDATA:\n{}".format(self.type,"\n".join(self.data))

def getMessage(src=input):
    line = separator
    while line == separator:
        line = src()
    result = []
    while line != separator:
        result.append(line)
        line = src()
    return Msg(result[0], result[1:])

def sendMessage(msgType, msgData=[], dst=print):
    dst(separator)
    dst(msgType)
    for line in msgData:
        dst(line)
    dst(separator)

def requestInput():
    sendMessage("REQUEST_INPUT")

def shouldSubmit(score):
    sendMessage("REPORT",[score])
    msg = getMessage()
    result = score > int(msg.data[0])
    return result

def startSubmit():
    print(separator)
    print("SUBMIT")

def endSubmit():
    print(separator)

def supervise(inputPath):
    w = None
    init = threading.Lock()
    init.acquire()
    end = threading.Lock()
    end.acquire()
    def helper():
        init.acquire()
        try:
            while True:
                m = getMessage(lambda: next(w))
                print(m)
                if m.type == "REQUEST_INPUT":
                    yield from sh("cat {}".format(inputPath))
                elif m.type == "REPORT":
                    res = []
                    mutex.acquire()
                    sendMessage("RES_SHOULD_SUBMIT",[str(results[inputPath][1])],dst=res.append)
                    mutex.release()
                    yield from res
                elif m.type == "SUBMIT":
                    score = m.data[0]
                    rest = m.data[1:]
                    mutex.acquire()
                    if int(score) > results[inputPath][1]:
                        results[inputPath] = (rest,score)
                    mutex.release()
        except StopIteration:
            pass
        end.release()
    w = sh(worker)(helper())
    init.release()
    w.wait()
    end.acquire()

def test():
    print(sh(worker)([str(3),separator,"RES_SHOULD_SUBMIT",str(3),separator]).read())

from time import sleep
if __name__ == "__main__":
    supervise("test.txt")
    supervise("test.txt")
    #test()
