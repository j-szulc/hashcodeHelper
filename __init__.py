from coconut_shell import *
import sys
import os
import signal
import atexit
import threading
import pickle
import time

# {path: numOfThreads
inputs = {"c_many_ingredients.in": 8}

# command to execute worker
worker = "/home/james/.local/share/virtualenvs/hashcodeHelper-D1Ml_3Lv/bin/python smartWorker.py"

# {inputPath: (solution, solutionScore)}
results = {key: (None,0) for key in inputs}
resultPath = "results.json"
mutex = threading.Lock()

# Automatically load existing backup if exists
autoLoad = False

# Custom Unicode characters from the Private Use section
# Separates messages
separator = '\uE069'

ends = []

debug = False

autoBackup = True

backupDebug = False

# in seconds
backupInterval = 10

def save():
    mutex.acquire()
    try:
        pickle.dump(results, open(resultPath, "wb"))
    finally:
        mutex.release()


def load():
    mutex.acquire()
    try:
        global results
        results = pickle.load(open(resultPath, "rb"))
    except:
        pass
    finally:
        mutex.release()

def loopedBackup():
    while True:
        time.sleep(backupInterval)
        save()
        if backupDebug:
            print("Backup successful!",file=sys.stderr)

class Msg:
    def __init__(self,type,data):
        self.type = type
        self.data = data
    def __str__(self):
        return "TYPE: {}\nDATA:\n{}".format(self.type,"\n".join(self.data))

def getMessage(src=input):
    if debug:
        oldSrc = src
        def debugSrc():
            line = oldSrc()
            print(line,file=sys.stderr)
            return line
        src = debugSrc
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

def startSubmit(score):
    print(separator)
    print("SUBMIT")
    print(score)

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
                #print(m)
                if m.type == "REQUEST_INPUT":
                    yield from sh("cat {}".format(inputPath))
                elif m.type == "REPORT":
                    res = []
                    mutex.acquire()
                    sendMessage("RES_SHOULD_SUBMIT",[str(results[inputPath][1])],dst=res.append)
                    mutex.release()
                    yield from res
                elif m.type == "SUBMIT":
                    score = int(m.data[0])
                    rest = m.data[1:]
                    mutex.acquire()
                    old = results[inputPath][1]
                    if score > old:
                        msg = "New result for {}!: {} -> {}".format(inputPath,old,score)
                        if old != 0:
                            msg += " : improved by {}%".format(100*((score/old)-1))
                        print(msg)
                        results[inputPath] = (rest,score)
                    mutex.release()
        except StopIteration:
            pass
        w.wait()
        end.release()
    w = sh(worker)(helper())
    init.release()
    return end

def scores():
    return [result[1] for result in results.values()]

def wait():
    for lock in ends:
        lock.acquire()

from time import sleep
if __name__ == "__main__":
    if autoLoad:
        try:
            load()
        except:
            pass
    if autoBackup:
        fork(loopedBackup,daemon=True)
    os.setpgrp()  # create new process group, become its leader
    for (path, nOfCores) in inputs.items():
        for i in range(nOfCores):
            ends.append(supervise(path))
    atexit.register(lambda: os.killpg(0, signal.SIGKILL))  # kill all processes in my group


    #test()
