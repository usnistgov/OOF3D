badlines = [
    "checkpoint named analysis chooser set"
]

import os

dirs = [f for f in os.listdir('.') if os.path.isdir(f)]

for d in dirs:
    filename = os.path.join(d, 'log.py')
    if os.path.exists(filename):
        print filename
        oldfilename = filename + ".save"
        os.rename(filename, oldfilename)
        oldfile = open(oldfilename, "r")
        newfile = open(filename, "w")
        for line in oldfile:
            stripped = line.strip()
            if not (stripped in badlines):
                print >> newfile, line,
