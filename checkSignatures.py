# This checks the voxel signatures in voxelsetboundary.C and looks for
# duplicates.

file = open("SRC/common/voxelsetboundary.C", "r")

def sort(sig):
    voxels = sorted(sig.split("|"))
    return "|".join(voxels)

sigs = {}
count = 0
dups = 0

for i, line in enumerate(file):
    line = line.strip()
    if line.startswith("pn("):
        comma = line.find(",")
        sig = line[3:comma]
        if sig.startswith("~("):
            sig = "~(" + sort(sig[2:-1]) + ")"
        else:
            sig = sort(sig)
        # print i+1, sig
        if sig in sigs:
            print "Duplicate signature", sig, "at lines", sigs[sig], "and", i+1
            dups += 1
        else:
            sigs[sig] = i+1
        count += 1

print "Read", count, "signatures.  Found", dups, "duplicates."
