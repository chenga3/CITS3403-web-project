import os
import subprocess

# This could be done with shells scripts, but avoiding them
# as that is not apart of the unit

#solution  = {
#               "questionID": id for the question,
#               "language": (cpp or python),
#               "solution": arr[] (array of lines)
#           }

def makeSolution(language, solution, questionID):

    if language == "cpp":
        solutionFile = open("solution.cpp", "w")
        for i in range(len(solution)):
            solutionFile.write(solution[i])
        solutionFile.close()
        returnedOutput = subprocess.getoutput("g++ solution.cpp")

    elif "language" == "python":
        solutionFile = open("solution.py", "w")
        for i in range(len(solution)):
            solutionFile.write(solution[i])
        solutionFile.close()

    else:
        return 1
        pass

    if returnedOutput == '':
        # Do tests
        pass
    else:
        #return the error
        pass

    return 0

arr = [
        "#include <iostream>\n",
        "using namespace std;\n",
        "int main(void) {\n",
        "   cout << \"Hello World!\\n\";\n",
        "   return 0;\n",
        "}"]

makeSolution("python", arr, 0)
