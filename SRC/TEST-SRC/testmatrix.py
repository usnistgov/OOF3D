# -*- python -*-
# $RCSfile: testmatrix.py,v $
# $Revision: 1.2.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:42 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

"""
testmatrix.py
Options:
   -M <file>    Matrix
   -b <file>    Right hand side vector
   -t <double>  Tolerance
   -n <int>     Max number of iterations
   -k <int>     Krylov dimension for gmres
   -a <str>     Algorithm (gmres, cg, bicg, bicgstab)
   -p <str>     Preconditioner (none, ilu, ic)
   -h           Print this
"""
from oofcpp import *
import sys, getopt, string

matrixfile = ""
rhsfile = ""
tolerance = 1.e-5
iterations = 1000
krylov = 10

## Wrappers for the actual solver routines.  Arguments are the matrix,
## the rhs, and the preconditioner.  The rhs is replaced with the
## solution on return.  All of the solvers need wrappers with the same
## set of arguments, since the solver will be picked out of a
## dictionary.

def call_gmres(matrix, x, pre):
    return gmres(matrix, x, pre, iterations, tolerance, krylov)

def call_cg(matrix, x, pre):
    return cg(matrix, x, pre, iterations, tolerance)
           
def call_bicg(matrix, x, pre):
    return bicg(matrix, x, pre, iterations, tolerance)

def call_bicgstab(matrix, x, pre):
    return bicgstab(matrix, x, pre, iterations, tolerance)

## The dictionary of solvers.

algorithms = { 'gmres':call_gmres,
               'bicg':call_bicg,
               'bicgstab':call_bicgstab,
               'cg':call_cg}
algorithm = algorithms['gmres']

## The dictionary of preconditioners

preconditioners = { 'none' : Unconditioner,
                    'ilu' : ILU_Preconditioner,
                    'ic' : IC_Preconditioner}
preconditioner = preconditioners['none']


def run():
    getargs()
    if matrixfile and rhsfile:
        n, matrix = readmatrix(matrixfile)
        rhs = readrhs(rhsfile, n)
        x = rhs[:]                      # copy rhs, since solvers overwrite it
        status = algorithm(matrix, x, preconditioner(matrix))
        Ax = matrix*x
        print "x=", x
        resid = Ax - rhs
        print "|Ax-b|=", resid.norm()

def getargs():

    global matrixfile, rhsfile, krylov, iterations, tolerance, algorithm
    global preconditioner
    
    try:
        options, args = getopt.getopt(sys.argv[1:], 'M:b:t:n:k:a:p:h')
    except getopt.error, message:
        sys.stderr.write(message + '\n')
        print __doc__
        sys.exit(1)

 
    for opt in options:
        if opt[0] == '-M':
            try:
                matrixfile = open(opt[1], 'r')
            except IOError:
                print "Can't open file", opt[1], "!"
                sys.exit(1)

        elif opt[0] == '-b':
            try:
                rhsfile = open(opt[1], 'r')
            except IOError:
                print "Can't open file", opt[1], "!"
                sys.exit(1)

        elif opt[0] == '-t':
            tolerance = string.atof(opt[1])

        elif opt[0] == '-n':
            iterations = string.atoi(opt[1])

        elif opt[0] == '-k':
            krylov = string.atoi(opt[1])

        elif opt[0] == '-a':
            try:
                algorithm = algorithms[opt[1]]
            except KeyError:
                print "Unknown algorithm!"
                print "Choices are: ",
                for key in algorithms.keys():
                    print key,
                sys.exit(1)

        elif opt[0] == '-p':
            try:
                preconditioner = preconditioners[opt[1]]
            except KeyError:
                print "Unknown preconditioner!"
                print "Choices are: ",
                for key in preconditioners.keys():
                    print key,
                sys.exit(1)

        elif opt[0] == '-h':
            print __doc__
            sys.exit(0)

## this works like string.atoi or string.atof, as appropriate.
def aton(x):
    if "." in x: return string.atof(x)
    return string.atoi(x)

## Return the fields in the next line that doesn't begin with '%'
def readline(file):
    line = file.readline()
    if line[0] == '%':
        return readline(file)
    return map(aton, string.split(line))

def readmatrix(matfile):
    rows, cols, nnz = readline(matfile)
    matrix = SparseLinkMat(rows, cols)

    nread = 0                           # number of entries read so far
    try:
        while 1:                        # read until EOF
            # Read i, j, m_ij
            i, j, x = readline(matfile)
            nread = nread + 1
    except:
        pass
    print "Read", nread, "matrix entries"
    if nread != nnz:
        print "Warning! Matrix file does not have", nnz, "entries!"
    return rows, matrix.csrmatrix()

def readrhs(rhsfile, n):
    x = Vector(n, 0.0)
    for i in range(n):
        line = rhsfile.readline()
        x[i] = string.atof(line)
    return x

if __name__ == '__main__':
    run()
