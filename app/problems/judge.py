import subprocess
import os
import sys
path = os.path.dirname(os.path.realpath(__file__))

# Class to store question
class Question:
    def __init__(self, id, language, code, time):
        self.id = id
        self.language = language # cpp or py
        self.code = code
        self.time = time
        self.testCases = []

# Class to store test case
class testCase:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

# Write question to file 
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


# Compile the code into a binary
def compileCode(question):
    # Compile CPP to Binary
    result = {"pass":"yes", "error": ""}
    if question.language == 'cpp':
        output = subprocess.run(['g++', '-o','solution', 'solution.cpp'],
                                capture_output=True)
        if output.returncode == 0:
            return result
        else:
            result["pass"] = "no"
            result["error"] = str(output.stderr,"utf-8")
            return result

    # CoMpIlE pYtHoN
    if question.language == 'py':
        return result


# test the code against the test cases from the 
# database
def testSolution(question):
    # break if no test cases
    if question.testCases == None:
        return 1

    # initialise results
    results = {"pass": "yes"}
    i = 0

    # Loop through all the test cases
    for test in question.testCases:
        # run the code
        if question.language == 'cpp':
            output = subprocess.Popen([f"{path}/../lib/time -f %e -o runtime ./solution"],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        universal_newlines=True,
                                        bufsize=0)
            # pipe in stdin
            for line in test.inputs:
                output.stdin.write(f"{line}\n")

        # run the code
        if question.language == 'py':
            output = subprocess.Popen([f"{path}/../lib/time -f %e -o runtime python3 solution.py"],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        universal_newlines=True,
                                        bufsize=0)
            # pipe in stdin
            for line in test.inputs:
                output.stdin.write(f"{line}\n")

        # get stdout
        stdout, stderr = output.communicate()
        # check stderr
        if stderr != '':
            results["pass"] = "no"
        else:
            o = stdout.strip().split("\n")
            file = open("runtime","r")
            time = file.readline()
            file.close()
            # Check runtime
            if float(time) > question.time:
                results[f"{i}"] = "Failed: Did not finish in time :("
                results["pass"] = "no"
                continue
            # added runtime to the result if successfull
            try:
                for j in range(0,len(test.outputs)):
                    if o[j] == test.outputs[j]:
                        results[f"{i}"] = f"Passed: Completed in {time}".strip()
                    else:
                        results[f"{i}"] = "Failed: Incorrect output"
                        results["pass"] = "no"
                        break
            except:
                results[f"{i}"] = "Failed"
        i+=1

    return results

# Delete files
def cleanUp():
    try:
        subprocess.run(['rm solution*'], shell=True)
        subprocess.run(['rm runtime'], shell=True)
    except:
        pass


# judge main function
def judge(question):
    os.chdir(path)
    writeQuestion(question)
    temp = compileCode(question)
    if temp["pass"] != "yes":
        return temp
    output = testSolution(question)
    return output




