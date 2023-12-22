import sys
import subprocess
from scripts.extract import extract 
from scripts.generate import generate

if len(sys.argv) > 0:
    arg = sys.argv[1]
    if arg == "extract":
        extract()
    elif arg == "generate":
        generate()
    else:
        print("Invalid argument.")
else:
    print("No argument provided.")
    subprocess.run("notify_phone && notify_phone", shell=True)
