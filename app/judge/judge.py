import subprocess
import os
import sys
path = os.path.dirname(os.path.realpath(__file__))


class Question:
    def __init__(self, id, language, code, time):
        self.id = id
        self.language = language # cpp or py
        self.code = code
        self.time = time
        self.testCases = []
    def __repr__(self):
        return f"ID:{self.id}, language:{self.language}"

class testCase:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

def writeQuestion(question):
    if question.language == 'cpp':
        file = open("solution.cpp", "w")
    elif question.language == 'py':
        file = open("solution.py", "w")
    else:
        return 1

    file.write(question.code)
    file.close()
    return 0



def compileCode(question):
    # Compile CPP to Binary
    if question.language == 'cpp':
        output = subprocess.run(['g++', '-o','solution', 'solution.cpp'],
                                capture_output=True)
        if output.returncode == 0:
            return 0
        else:
            return output.stderr

    # CoMpIlE pYtHoN
    if question.language == 'py':
        return 0

    # not a reconized file type
    else:
        return 1



def testSolution(question):
    if question.testCases == None:
        return 1

    results = {}
    i = 0
    for test in question.testCases:
        if question.language == 'cpp':
            output = subprocess.Popen([f"{path}/../lib/time -f %e -o runtime ./solution"],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        universal_newlines=True,
                                        bufsize=0)
            for line in test.inputs:
                output.stdin.write(f"{line}\n")

        if question.language == 'py':
            output = subprocess.Popen([f"{path}/../lib/time -f %e -o runtime python3 solution.py"],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        universal_newlines=True,
                                        bufsize=0)

            for line in test.inputs:
                output.stdin.write(f"{line}\n")

        stdout, stderr = output.communicate()
        if stderr != '':
            results[i] = stderr
        else:
            o = stdout.strip().split("\n")
            try:

                for j in range(0,len(test.outputs)):
                    if o[j] == test.outputs[j]:
                        file = open("runtime","r")
                        time = file.readline()
                        results[f"{i}"] = f"Completed in {time}".strip()
                        file.close()
                    else:
                        results[f"{i}"] = "Incorrect output"
            except:
                results[f"{i}"] = "Failed"
        i+=1
    return results

def cleanUp():
    subprocess.run(['rm solution*'], shell=True)
    subprocess.run(['rm runtime'], shell=True)


def judge(question):
    os.chdir(path)
    writeQuestion(question)
    temp = compileCode(question)
    if temp != 0:
        return {'error': str(temp, "utf-8")}
    return testSolution(question)




