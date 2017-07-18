import sys

file0 = open(sys.argv[1], "r")
file1 = open(sys.argv[2], "r")

for line0, line1 in zip(file0, file1):
    if line0[0] == '#':
        continue
    t0, val0 = eval(line0)
    t1, val1 = eval(line1)
    if val1 != 0.0:
        print t0, val0, val1, val0/val1
