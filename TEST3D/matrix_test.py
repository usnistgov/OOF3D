# -*- python -*-
# $RCSfile: matrix_test.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:46 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


import unittest, os

from UTILS import file_utils
fp_file_compare = file_utils.fp_file_compare
reference_file = file_utils.reference_file

# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
file_utils.generate = False

datadir = 'matrix_data'

def loadMatrix(filename, fortran=False, symmetric=False):
    phile = file(reference_file(datadir, filename), 'r')
    matrix = sparsemat.SparseMat(0,0)
    for line in phile:
        try:
            istr, jstr, valstr = line.split()
            i = int(istr)
            j = int(jstr)
            val = float(valstr)
        except:
            # Ignore lines that don't make sense.  They're
            # probably comments or blank lines.
            pass
        else:
            if not fortran:
                matrix.insert(i, j, val)
                if symmetric and i != j:
                    matrix.insert(j, i, val)
            else:
                matrix.insert(i-1, j-1, val)
                if symmetric and i != j:
                    matrix.insert(j-1, i-1, val)
    matrix.consolidate()
    return matrix

def saveMatrix(matrix, filename):
    phile = open(filename, 'w')
    for i,j,val in matrix:
        print >> phile, i, j, "%16.9e"%val
    phile.close()

import sets
def fillMatrix(matrix):
    # Convert a sparse matrix to a full one.  For testing only, not
    # for general use.
    for row in range(matrix.nrows()):
        cols = sets.Set(range(matrix.ncols()))
        for i,j,x in matrix.row(row):
            cols.remove(j)
        for col in cols:
            matrix.insert(row, col, 0.0)
        

def loadVector(filename):
    vector = doublevec.DoubleVec(0) # will be resized by load()
    vector.load(reference_file(datadir, filename))
    return vector

class Matrix_Ops(unittest.TestCase):
    def setUp(self):
        global ooferror
        global sparsemat
        from ooflib.SWIG.common import ooferror
        from ooflib.SWIG.engine import sparsemat
    def readwrite(self, infile, compfile):
        matrix = loadMatrix(infile)
        saveMatrix(matrix, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, compfile),
                                     1.e-8))
        file_utils.remove('matrix.out')
    def countRow(self, matrix, rowno):
        count = 0
        for i,j,v in matrix.row(rowno):
            print >> sys.stderr, i, j, v
            count += 1
        return count

    def Read(self):     # Tests IO and iteration over matrix elements.
        # Read a matrix with no repeated indices
        self.readwrite('matrix1', 'matrix1.out')
        # Read the same matrix, but with data given in a
        # different order.
        self.readwrite('matrix1a', 'matrix1.out')
        # Read a matrix with repeated indices
        self.readwrite('matrixMulti', 'matrixMulti.out')
        # Read a matrix with an empty first row
        self.readwrite('lowertriunit', 'lowertriunit.out')
    def RowIter(self):
        matrix = loadMatrix('rowcountmat')
        self.assertEqual(self.countRow(matrix, 0), 2)
        self.assertEqual(self.countRow(matrix, 1), 0)
        self.assertEqual(self.countRow(matrix, 2), 2)
        self.assertEqual(self.countRow(matrix, 3), 0)
        self.assertEqual(self.countRow(matrix, 4), 4)
        self.assertRaises(ooferror.ErrProgrammingError,
                          self.countRow, matrix, 5)
        
    def Add(self):
        matrix1 = loadMatrix('matrix1')
        matrix2 = loadMatrix('matrix2')
        sum = matrix1 + matrix2
        saveMatrix(sum, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'sum.mat'),
                                     1.e-8))
        diff = matrix1 - matrix2
        saveMatrix(diff, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'diff.mat'),
                                     1.e-8))
        file_utils.remove('matrix.out')
    def Add_In_Place(self):
        matrix1 = loadMatrix('matrix1')
        matrix2 = loadMatrix('matrix2')
        m = matrix1.clone()
        self.assert_(matrix1.nnonzeros() == m.nnonzeros())
        m.add(1.0, matrix2)
        saveMatrix(m, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'sum.mat'),
                                     1.e-8))
        # matrix2 should not have changed.
        saveMatrix(matrix2, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'matrix2.out'),
                                     1.e-8))
        # matrix1 should not have changed either
        saveMatrix(matrix1, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'matrix1.out'),
                                     1.e-8))
        m = matrix1.clone()
        m += matrix2
        saveMatrix(m, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'sum.mat'),
                                     1.e-8))
        saveMatrix(matrix2, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'matrix2.out'),
                                     1.e-8))
        m = matrix1.clone()
        m.add(-1.0, matrix2)
        saveMatrix(m, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'diff.mat'),
                                     1.e-8))
        m = matrix1.clone()
        m -= matrix2
        saveMatrix(m, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'diff.mat'),
                                     1.e-8))
        file_utils.remove('matrix.out')
    def Scalar_Multiply(self):
        matrix = loadMatrix('matrix1')
        prod = matrix*2.0
        saveMatrix(prod, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                     os.path.join(datadir, 'prod.out'),
                     1.e-8))
        prod = 2.0*matrix
        saveMatrix(prod, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                     os.path.join(datadir, 'prod.out'),
                     1.e-8))
        prod = matrix/0.5
        saveMatrix(prod, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                     os.path.join(datadir, 'prod.out'),
                     1.e-8))
        matrix2 = matrix.clone()
        matrix2 *= 2.0
        saveMatrix(matrix2, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                     os.path.join(datadir, 'prod.out'),
                     1.e-8))
        matrix2 = matrix.clone()
        matrix2 /= 0.5
        saveMatrix(matrix2, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'prod.out'),
                                     1.e-8))
        file_utils.remove('matrix.out')

    def Matrix_Multiply(self):
        ident = loadMatrix('identity')
        matrix1 = loadMatrix('matrix1')
        matrix2 = loadMatrix('matrix2')
        prod = ident*matrix1
        saveMatrix(prod, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'prod1.out'),
                                     1.e-8))
        prod = matrix1*ident
        saveMatrix(prod, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'prod1.out'),
                                     1.e-8))
        prod = matrix1*matrix2
        saveMatrix(prod, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'prod2.out'),
                                     1.e-8))
        prod = matrix2*matrix1
        saveMatrix(prod, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'prod3.out'),
                                     1.e-8))
        file_utils.remove('matrix.out')
        

class Vector_Ops(unittest.TestCase):
    def setUp(self):
        global ooferror
        global doublevec
        from ooflib.SWIG.common import ooferror
        from ooflib.SWIG.common import doublevec
        
    def VectorIO(self):
        vector = loadVector('vector0')
        vector.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vector0.out'),
                                     1.e-8))
        file_utils.remove('vector.out')

    def Add(self):
        vector0 = loadVector('vector0')
        vector1 = loadVector('vector1')
        self.assertEqual(vector0.size(), 4)
        self.assertEqual(vector1.size(), 4)
        sum = vector0 + vector1
        sum.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecsum.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec.axpy(2.0, vector1)
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecsum2.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec += vector1
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecsum.out'),
                                     1.e-8))
        diff = vector0 - vector1
        diff.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecdiff.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec -= vector1
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecdiff.out'),
                                     1e-08))
        file_utils.remove('vector.out')
        
    def Multiply(self):
        vector0 = loadVector('vector0')
        vector1 = loadVector('vector1')
        vec = 2*vector0
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        vec = vector0*2.0
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        vec = vector0/0.5
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec *= 2.0
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec /= 0.5
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        dot = vector0 * vector1
        self.assertEqual(dot, 20.0)
        dot = vector0.dot(vector1)
        self.assertEqual(dot, 20.0)
        file_utils.remove('vector.out')
            
class Matrix_Vector_Ops(unittest.TestCase):
    def setUp(self):
        global doublevec
        global sparsemat
        from ooflib.SWIG.common import doublevec
        from ooflib.SWIG.engine import sparsemat
    def Multiply(self):
        matrix = loadMatrix('matrix1')
        vector = loadVector('vector0')
        vec = matrix*vector
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'matvec.out'),
                                     1.e-8))
        vec = vector*matrix
        vec.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'matvec2.out'),
                                     1.e-8))
        file_utils.remove('vector.out')
    def Solve(self):
        result = doublevec.DoubleVec(4)

        # Lower triangular matrix with implicit unit diagonal.
        lower = loadMatrix('lowertriunit')

        rhs = loadVector('rhs0')
        lower.solve_lower_triangle_unitd(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve0.out'),
                                     1.e-8))

        rhs = loadVector('rhs1')
        lower.solve_lower_triangle_unitd(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve1.out'),
                                     1.e-8))

        # Upper triangular matrix with explicit diagonal entries.
        upper = loadMatrix('uppertri')

        rhs = loadVector('rhs0')
        upper.solve_upper_triangle(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve2.out'),
                                     1.e-8))
        resid = upper*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        upper.solve_upper_triangle(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve3.out'),
                                     1.e-8))
        resid = upper*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        # Transpose of upper triangular matrix with explicit diagonal entries.
        rhs = loadVector('rhs0')
        upper.solve_upper_triangle_trans(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve4.out'),
                                     1.e-8))
        resid = upper.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        upper.solve_upper_triangle_trans(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve5.out'),
                                     1.e-8))
        resid = upper.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        # Transpose of lower triangular matrix with explicit diagonal
        # entries.
        lower = loadMatrix('lowertri')

        rhs = loadVector('rhs0')
        lower.solve_lower_triangle_trans(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve6.out'),
                                     1.e-8))
        resid = lower.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        lower.solve_lower_triangle_trans(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve7.out'),
                                     1.e-8))
        resid = lower.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        # Lower triangular matrix with explicit unit diagonal entries.
        rhs = loadVector('rhs0')
        lower.solve_lower_triangle(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve8.out'),
                                     1.e-8))
        resid = lower*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        lower.solve_lower_triangle(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve9.out'),
                                     1.e-8))
        resid = lower*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        # Transpose of lower triangular matrix with implicit unit
        # diagonal.
        lower = loadMatrix('lowertriunit')

        lowerunit = lower.clone()
        for i in range(lowerunit.nrows()):
            lowerunit.insert(i, i, 1.0)

        rhs = loadVector('rhs0')
        lower.solve_lower_triangle_trans_unitd(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve10.out'),
                                     1.e-8))
        resid = lowerunit.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        lower.solve_lower_triangle_trans_unitd(rhs, result)
        result.save('vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve11.out'),
                                     1.e-8))
        resid = lowerunit.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        file_utils.remove('vector.out')
        

class Matrix_Factorization(unittest.TestCase):
    def setUp(self):
        global sparsemat
        global preconditioner
        global doublevec
        from ooflib.SWIG.common import doublevec
        from ooflib.SWIG.engine import sparsemat
        from ooflib.SWIG.engine import preconditioner
    def LU(self):
        # Test the ILU code on dense matrices.
        # A full identity matrix
        matrix = loadMatrix('identity-full')
        pcwrap = preconditioner.ILUPreconditioner()
        pc = pcwrap.create_preconditioner(matrix)
        unfact = pc.unfactored()
        saveMatrix(unfact, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'identity-full'),
                                     1.e-8))

        # Non-trivial test: a dense asymmetric matrix.
        matrix = loadMatrix('dense-asym-mat')
        pcwrap = preconditioner.ILUPreconditioner()
        pc = pcwrap.create_preconditioner(matrix)
        unfact = pc.unfactored()
        saveMatrix(unfact, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'ilu_unfactored'),
                                     1.e-8))
        # Check the preconditioner solutions...
        for vecname in ('rhs2.1', 'rhs2.2', 'rhs2.3'):
            vec = loadVector(vecname)
            result = pc.solve(vec)
            result.save('vector.out')
            self.assert_(fp_file_compare('vector.out',
                                         os.path.join(datadir,
                                                      vecname+'_ilu.out'),
                                         1.e-8))

        # A big(ger) dense matrix
        matrix = loadMatrix('big.mat')
        pcwrap = preconditioner.ILUPreconditioner()
        pc = pcwrap.create_preconditioner(matrix)
        unfact = pc.unfactored()
        saveMatrix(unfact, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'big.mat'),
                                     1.e-8))
        saveMatrix(pc.lower(), 'matrix.out')
        l_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'big_lower.out'),
                               1.e-8)
        saveMatrix(pc.upper(), 'matrix.out')
        u_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'big_upper.out'),
                               1.e-8)
        self.assert_(l_ok and u_ok)

        file_utils.remove('matrix.out')
        file_utils.remove('vector.out')

    def ILU(self):
        # Actual incomplete factorizations of sparse matrices.

        # A sparse identity matrix
        print >> sys.stderr,  "identity"
        matrix = loadMatrix('identity')
        pcwrap = preconditioner.ILUPreconditioner()
        pc = pcwrap.create_preconditioner(matrix)
        unfact = pc.unfactored()
        saveMatrix(unfact, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'identity'),
                                     1.e-8))
        # A sparse diagonal non-identity matrix.
        print >> sys.stderr,  "diag"
        matrix = loadMatrix('diag')
        pc = pcwrap.create_preconditioner(matrix)
        unfact = pc.unfactored()
        saveMatrix(unfact, 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'diag'),
                                     1.e-8))

        # Non-trivial tests.  The reference files were checked against
        # SparseLib++'s ILU routine.

        # A 4x4 sparse matrix.
        print >> sys.stderr,  "matrix1"
        matrix = loadMatrix('matrix1')
        pc = pcwrap.create_preconditioner(matrix)
        saveMatrix(pc.lower(), 'matrix.out')
        l_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'matrix1_lower.out'),
                               1.e-8)
        saveMatrix(pc.upper(), 'matrix.out')
        u_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'matrix1_upper.out'),
                               1.e-8)
        self.assert_(l_ok and u_ok)

        # A 10x10 sparse matrix with 62 entries.
        print >> sys.stderr,  "sparse10x10.mat"
        matrix = loadMatrix('sparse10x10.mat')
        pc = pcwrap.create_preconditioner(matrix)
        saveMatrix(pc.lower(), 'matrix.out')
        l_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'sparse10_lower.out'),
                               1.e-8)
        saveMatrix(pc.upper(), 'matrix.out')
        u_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'sparse10_upper.out'),
                               1.e-8)
        self.assert_(l_ok and u_ok)
        unfact = pc.unfactored()
        saveMatrix(unfact, 'matrix.out')
        # Check that the factoring *isn't* exact.
        self.assert_(
            not fp_file_compare('matrix.out',
                                os.path.join(datadir, 'sparse10x10.mat'),
                                1.e-8, quiet=True))
        
        # A 50x50 sparse matrix with 157 entries.
        print >> sys.stderr,  "bigsparse2.mat"
        matrix = loadMatrix('bigsparse2.mat')
        pc = pcwrap.create_preconditioner(matrix)
        saveMatrix(pc.lower(), 'matrix.out')
        l_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'bigsparse2_lower.out'),
                               1.e-8)
        saveMatrix(pc.upper(), 'matrix.out')
        u_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'bigsparse2_upper.out'),
                               1.e-8)
        self.assert_(l_ok and u_ok)

        # A 50x50 sparse matrix with 297 entries.
        print >> sys.stderr,  "bigsparse.mat"
        matrix = loadMatrix('bigsparse.mat')
        pc = pcwrap.create_preconditioner(matrix)
        saveMatrix(pc.lower(), 'matrix.out')
        l_ok = fp_file_compare('matrix.out',
                                  os.path.join(datadir, 'bigsparse_lower.out'),
                                  1.e-8)
        saveMatrix(pc.upper(), 'matrix.out')
        u_ok = fp_file_compare('matrix.out',
                               os.path.join(datadir, 'bigsparse_upper.out'),
                               1.e-8)
        self.assert_(l_ok and u_ok)

        file_utils.remove('matrix.out')

    def Cholesky(self):
        # Cholesky decomposition of dense symmetric positive definite matrices.
        matrix = loadMatrix('identity-full')
        pcwrap = preconditioner.ICPreconditioner()
        pc = pcwrap.create_preconditioner(matrix)
        saveMatrix(pc.unfactored(), 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'identity-full'),
                                     1.e-8))

        matrix = loadMatrix('small_sym_dense.mat')
        pc = pcwrap.create_preconditioner(matrix)
        saveMatrix(pc.unfactored(), 'matrix.out')
        self.assert_(fp_file_compare(
                'matrix.out', os.path.join(datadir, 'small_sym_dense.mat'),
                1.e-8))
        # Check preconditioner solutions
        for vecname in ('rhs0', 'rhs1'):
            vec = loadVector(vecname)
            result = pc.solve(vec)
            result.save('vector.out')
            self.assert_(fp_file_compare('vector.out',
                                         os.path.join(datadir,
                                                      vecname+'_ic.out'),
                                         1.e-8))
            resid = matrix*result - vec
            self.assertAlmostEqual(resid.norm(), 0.0, 8)

        matrix = loadMatrix('small_sym_dense2.mat')
        pc = pcwrap.create_preconditioner(matrix)
        saveMatrix(pc.unfactored(), 'matrix.out')
        self.assert_(fp_file_compare(
                'matrix.out', os.path.join(datadir, 'small_sym_dense2.mat'),
                1.e-8))
        for vecname in ('rhs2.1', 'rhs2.2', 'rhs2.3'):
            vec = loadVector(vecname)
            result = pc.solve(vec)
            result.save('vector.out')
            self.assert_(fp_file_compare('vector.out',
                                         os.path.join(datadir,
                                                      vecname+'_ic.out'),
                                         1.e-8))
            resid = matrix*result - vec
            self.assertAlmostEqual(resid.norm(), 0.0, 8)
            
        saveMatrix(pc.upper(), 'matrix.out')
        self.assert_(fp_file_compare(
                'matrix.out', os.path.join(datadir,
                                           'small_sym_dense2_lower.out'),
                1.e-8))

        # Hilbert matrix, which is notoriously badly conditioned.
        size = 12               # test fails for size > 12!
        matrix = sparsemat.SparseMat(size, size)
        for i in range(size):
            for j in range(size):
                matrix.insert(i, j, 1./(i+j+1.0))
        matrix.consolidate()
        norm = 1.0/matrix.norm()
        pc = pcwrap.create_preconditioner(matrix)
        resid = pc.unfactored() - matrix
        for i,j,x in resid:
            self.assertAlmostEqual(x*norm, 0.0, 8)

        # Large Matrix market matrices
        for mtxname in ('bcsstk01.mtx', 'bcsstk07.mtx'):
            print >> sys.stderr,  mtxname
            matrix = loadMatrix(mtxname, fortran=True, symmetric=True)
            fillMatrix(matrix)
            matrix.consolidate()
            pc = pcwrap.create_preconditioner(matrix)
            unf = pc.unfactored()
            resid = matrix - unf
            resid.consolidate()
            norm = 1./matrix.norm()
            for i,j,x in resid:
                self.assertAlmostEqual(x*norm, 0.0, 8)
        
        file_utils.remove('matrix.out')
        file_utils.remove('vector.out')

    def IC(self):               # Incomplete Cholesky decomposition
        matrix = loadMatrix('identity')
        pcwrap = preconditioner.ICPreconditioner()
        pc = pcwrap.create_preconditioner(matrix)
        saveMatrix(pc.unfactored(), 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'identity'),
                                     1.e-8))

        ## NOTE: The reference matrices were generated by this
        ## program, not SparseLib++, because the SparseLib++ IC
        ## preconditioner seems to be broken...

        matrix = loadMatrix('small_sym_sparse2.mat')
        pc = pcwrap.create_preconditioner(matrix)
        # Save the *upper* triangle, even though the lower one is more
        # natural for the ICPreconditioner class. The reference file
        # generated by SparseLib++ contains the upper triangle.
        saveMatrix(pc.upper(), 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir,
                                                  'small_sym_upper2.out'),
                                     1.e-8))

        matrix = loadMatrix('small_sym_sparse.mat')
        pc = pcwrap.create_preconditioner(matrix)
        # Save the *upper* triangle, even though the lower one is more
        # natural for the ICPreconditioner class. The reference file
        # generated by SparseLib++ contains the upper triangle.
        saveMatrix(pc.upper(), 'matrix.out')
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir,
                                                  'small_sym_upper.out'),
                                     1.e-8))

        # Big matrices from Matrix Market. 'bcsstk07' has been
        # removed. It can't be factored, apparently due to a pathology
        # of the matrix or the algorithm.  It passes the complete
        # Cholesky test.
        for mtxname in ('s1rmq4m1', 'bcsstk01',):
            print >> sys.stderr,  mtxname+'.mtx'
            matrix = loadMatrix(mtxname+'.mtx', fortran=True, symmetric=True)
            pc = pcwrap.create_preconditioner(matrix)
            self.assert_(pc.upper().unique_indices())
            saveMatrix(pc.upper(), 'matrix.out')
            self.assert_(fp_file_compare(
                    'matrix.out', os.path.join(datadir,
                                               mtxname+'_upper.out'),
                    1.e-8))
        file_utils.remove('matrix.out')


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
        
basic_set = [
    Matrix_Ops("Read"),
    Matrix_Ops("RowIter"),
    Vector_Ops("VectorIO")
    ]
math_set = [
    Matrix_Ops("Add"),
    Matrix_Ops("Add_In_Place"),
    Matrix_Ops("Scalar_Multiply"),
    Matrix_Ops("Matrix_Multiply"),
    Vector_Ops("Add"),
    Vector_Ops("Multiply"),
    Matrix_Vector_Ops("Multiply"),
    Matrix_Vector_Ops("Solve"),
    Matrix_Factorization("LU"),
    Matrix_Factorization("ILU"),
    Matrix_Factorization("Cholesky"),
    Matrix_Factorization("IC"),
    ]

test_set = basic_set + math_set
