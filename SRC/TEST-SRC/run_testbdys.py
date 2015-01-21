# -*- python -*-
# $RCSfile: run_testbdys.py,v $
# $Revision: 1.2 $
# $Author: reida $
# $Date: 2001/12/07 20:55:26 $
 

import os, sys, getopt, re, string

tolerance = 0.0
pathprefix = ''

try:
    optlist, args = getopt.getopt(sys.argv[1:],'p:t:')
except getopt.error, message:
    print "Usage: python run_testbdys.py -p <path> -t <tolerance>."

for opt in optlist:
    if opt[0] == '-p':
        pathprefix = opt[1]
        if pathprefix[-1]!='/':
            pathprefix += '/'
    if opt[0] == '-t':
        tolerance = opt[1]

if pathprefix=='':
    print "Usage: python run_testbdys.py -p <path> -t <tolerance>."
    print "Path is the path to the data files.  It is not optional."
    os._exit(4)

# "Runner" shamelessly uses the global value "tolerance".

# New improved version -- "path" is the path to the *data* files,
# and you just run it via the link from the build directory, or
# directly from its own directory.  testbdy.py must be accessible
# from the directory in which you run it.
def runner(bndyargs, filename):
    # excstring = "(cd " + pathprefix + "; " + "python testbdy.py " +\
    #             bndyargs + " )"
    excstring = "python testbdy.py " + bndyargs
    digitsplus = "[-"+string.digits+"]"
    pipe = os.popen(excstring, 'r')
    file = open(pathprefix+filename,'r')
    mismatch = None
    lct = 0
    for linestring in file.readlines():
        lct+=1
        if re.match(digitsplus,linestring[0]):
            # Get next string from the pipe that looks like data.
            pipestring = pipe.readline()
            while not re.match(digitsplus, pipestring[0]):
                pipestring = pipe.readline()
            #
            lineset = string.split(linestring, ' ')
            pipeset = string.split(pipestring, ' ')
            # Compare data entries, howevermany there are.
            for (linevalue, pipevalue) in map(None, lineset, pipeset):
                if abs(float(linevalue)-float(pipevalue)) > tolerance:
                    mismatch = 1
                    print "\nMismatch, line %d in file %s." % (lct, filename)
                    print "   File: " + string.strip(linevalue)
                    print "Program: " + string.strip(pipevalue)
        else:
            # Discard pipe data.
            pipe.readline()

    if mismatch:
        print "Failed on file %s." % filename
    else:
        print "File %s OK." % filename
        
        
runner("-n 3 -u fixed -l fixed", "bdy_3x3_tri_iso_ufix_lfix")
runner("-n 3 -u fixed -l float", "bdy_3x3_tri_iso_ufix_lflo")
runner("-n 3 -u float -l fixed", "bdy_3x3_tri_iso_uflo_lfix")
runner("-n 3 -u flux -l fixed", "bdy_3x3_tri_iso_uflu_lfix")
runner("-n 3 -u fixed -l force", "bdy_3x3_tri_iso_ufix_lfor")

runner("-n 3 -p -u fixed -l fixed", "bdy_3x3_tri_sup_ufix_lfix")
runner("-n 3 -p -u fixed -l float", "bdy_3x3_tri_sup_ufix_lflo")
runner("-n 3 -p -u float -l fixed", "bdy_3x3_tri_sup_uflo_lfix")
runner("-n 3 -p -u flux -l fixed", "bdy_3x3_tri_sup_uflu_lfix")
runner("-n 3 -p -u fixed -l force", "bdy_3x3_tri_sup_ufix_lfor")

runner("-n 3 -b -u fixed -l fixed", "bdy_3x3_tri_sub_ufix_lfix")
runner("-n 3 -b -u fixed -l float", "bdy_3x3_tri_sub_ufix_lflo")
runner("-n 3 -b -u float -l fixed", "bdy_3x3_tri_sub_uflo_lfix")
runner("-n 3 -b -u flux -l fixed", "bdy_3x3_tri_sub_uflu_lfix")
runner("-n 3 -b -u fixed -l force", "bdy_3x3_tri_sub_ufix_lfor")
