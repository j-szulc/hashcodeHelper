from coconut_shell import *

# {path: numOfThreads
inputs = {"test.txt": 1}

# command to execute worker
worker = "python3 worker.py"

# {inputPath: (solution, solutionScore)}
results = {key: (None,0) for key in inputs}

# Custom Unicode characters from the Private Use section

# Separates solution from solutionScore
smallSeparator = '\uE069'

# Separates solution+smallSeparator+solutionScore from each other
bigSeparator = '\uE420'

def supervise(inputPath):
    with open(inputPath,"r") as file:
        readingSolution = True
        currentSolution = []
        currentScore = None
        for line in sh(worker)(file.readlines()):
            if line == smallSeparator:
                    assert readingSolution
                    readingSolution = False
            elif line == bigSeparator:
                    assert not readingSolution
                    if currentScore > results[inputPath][1]:
                        results[inputPath]=(currentSolution,currentScore)
                    readingSolution = True
                    currentSolution = []
                    currentScore = None
            else:
                assert smallSeparator not in line
                assert bigSeparator not in line
                if readingSolution:
                    currentSolution.append(line)
                else:
                    currentScore = int(line)

supervise("test.txt")
print(results)