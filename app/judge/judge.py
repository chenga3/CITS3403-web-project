import os
import subprocess

# This could be done with shells scripts, but avoiding them
# as that is not apart of the unit

#solution  = {
#               "questionID": id for the question,
#               "language": (cpp or python),
#               "solution": arr[] (array of lines)
#           }

def testSolution(language, solution, questionID):

    returnedOutput = ""

    if language == "cpp":
        solutionFile = open("solution/solution.cpp", "w")
        for i in range(len(solution)):
            solutionFile.write(solution[i])
        solutionFile.close()
        returnedOutput = subprocess.getoutput("g++ solution/solution.cpp")
    elif language == "python":
        solutionFile = open("solution/solution.py", "w")
        for i in range(len(solution)):
            solutionFile.write(solution[i])
        solutionFile.close()
    else:
        return 1
        pass

    if returnedOutput == '':
        # need to get cases and number of cases from db
        # write inputs to input file
        # check the outputs against the expected values
        testCases = 1
        for i in range(testCases):
            #do tests
    else:
        #return the error
        print(returnedOutput)
        pass

    return 0


arr = [
        "#include <iostream>\n",
        "using namespace std;\n",
        "int main(void) {\n",
        "   cout << \"Hello World!\\n\";\n",
        "   return 0;\n",
        "}"]

testSolution("cpp", arr, 0)
