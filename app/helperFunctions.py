import os

def pandoc(input):
    return os.popen(f"echo '{input}' |" + \
        f"{os.path.dirname(os.path.realpath(__file__))}" + \
        f"/lib/pandoc/pandoc").read()