import os
import subprocess

def pandoc(input):
    output = subprocess.Popen([f"{os.path.dirname(os.path.realpath(__file__))}"+\
                                 "/lib/pandoc/pandoc"],
                                
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        shell=True,
                                        universal_newlines=True,
                                        bufsize=0)
    stdout, stderr = output.communicate(input=input)
    return stdout.strip()

    # return os.popen(f"echo '{input}' |" + \
    #     f"{os.path.dirname(os.path.realpath(__file__))}" + \
    #     f"/lib/pandoc/pandoc").read(
