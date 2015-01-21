# -*- python -*-
# $RCSfile: randommatrix.py,v $
# $Revision: 1.3.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

"""
Generate a random matrix and vector, suitable for
testing the matrix solver in testmatrix.py.
Matrix and rhs go to M.<suffix> and b.<suffix>.
Mathematica code for the same matrix and rhs go to M.<suffix>.ma
The arguments are:
  -n <size>   system size
  -s <x>      sparseness (0 = empty matrix, 1 = full matrix)
  -S          Symmetric matrix
  -T          Tridiagonal matrix
  -r <seed>   Random seed (integer)
  -F <suffix> Output file suffix
  -h          Print this
"""

import oofpath
from oofcpp import *
import sys, getopt, string, whrandom

size = 3
sparseness = 1.0
mmaformat = 0
symmetric = 0
tridiagonal = 0
suffix = ".xxx"

def getargs():
    global size, sparseness, symmetric, tridiagonal, suffix
    try:
        options, args = getopt.getopt(sys.argv[1:], 'n:s:STr:F:h')
    except getopt.error, message:
        sys.stderr.write(message + '\n')
        print __doc__
        sys.exit(1)
    for opt in options:
        if opt[0] == '-n':
            size = string.atoi(opt[1])
        elif opt[0] == '-s':
            sparseness = string.atof(opt[1])
        elif opt[0] == '-r':
            seed = string.atoi(opt[1])
            whrandom.seed(seed, 0, 1)
        elif opt[0] == '-S':
            symmetric = 1
        elif opt[0] == '-T':
            tridiagonal = 1
        elif opt[0] == '-F':
            suffix = "." + opt[1]
        elif opt[0] == '-h':
            print __doc__
            sys.exit(0)


def make_mtx():
    mat = SparseLinkMat(size, size)
    if tridiagonal:
        for i in range(size):
            mat[i,i] = 4*whrandom.random()
        if symmetric:
            for i in range(0, size-1):
                mat[i,i+1] = whrandom.random() - 0.5
                mat[i+1,i] = mat[i,i+1]
        else:
            for i in range(1, size-1):
                mat[i,i-1] = whrandom.random() - 0.5
                mat[i,i+1] = whrandom.random() - 0.5
            mat[0,1] = whrandom.random() - 0.5
            mat[size-1,size-2] = whrandom.random() - 0.5
    else:
        for i in range(size):
            if symmetric:
                jval = range(i, size)
            else:
                jval = range(0, size)
                for j in jval:
                    if whrandom.random() <= sparseness:
                        mat[i,j] = whrandom.random()
                        if symmetric:
                            mat[j,i] = mat[i,j]
    return mat

def print_mtx(mat):
    print size, size
    print mat.csrmatrix()

def print_mtx_mma(mat):
    print "A = {"
    for i in range(size):
        print "{",
        for j in range(size):
            print mat[i,j],
            if j < size-1:
                print ", ",
        print "}",                  # end of row
        if i < size-1:
            print ",",
        print ""                    # end of output line
    print "};"
    
def make_rhs():
    rhs = range(size)
    for i in range(size):
        rhs[i] = whrandom.random()
    return rhs

def print_rhs(rhs):
    for i in rhs:
        print i

def print_rhs_mma(rhs):
    print "b = {",
    for i in rhs[:size-1]:
        print i,", "
    print rhs[size-1], "};"

if __name__ == '__main__':
    getargs()
    mat = make_mtx()
    rhs = make_rhs()
    sys.stdout = open('M'+suffix, 'w')
    print_mtx(mat)
    sys.stdout.close()
    sys.stdout = open('b'+suffix, 'w')
    print_rhs(rhs)
    sys.stdout.close()
    sys.stdout = open('M'+suffix+'.ma', 'w')
    print_mtx_mma(mat)
    print_rhs_mma(rhs)
    print "x = LinearSolve[A,b]; x"
    print "r = A.x - b; Sqrt[r.r]"
