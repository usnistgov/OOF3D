# -*- python -*-

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
# file_utils.generate = True

datadir = 'matrix_data'

def loadMatrix(filename, fortran=False, symmetric=False):
    matrix = sparsemat.SparseMat(0, 0)
    f = reference_file(datadir, filename)
    matrix.load(f)
    return matrix

def saveMatrix(matrix, filename):
    matrix.save(filename)

def loadVector(filename):
    vector = doublevec.DoubleVec(0)
    f = reference_file(datadir, filename)
    vector.load(f)
    return vector

def saveVector(vector, filename):
    vector.save(filename)

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

    def MatrixIO(self):
        # Read a matrix with no repeated indices
        self.readwrite('matrix1', 'matrix1.out')

        # Read the same matrix, but with data given in a
        # different order.
        self.readwrite('matrix1a', 'matrix1.out')

        # Read a matrix with an empty first row
        self.readwrite('lowertriunit', 'lowertriunit.out')

        # Empty matrix
        self.readwrite('empty.mtx', 'empty.mtx')

    def Basics(self):
        mat = sparsemat.SparseMat(1000, 1000) 
        self.assert_(mat.nrows() == 1000)
        self.assert_(mat.ncols() == 1000)
        self.assert_(mat.nnonzeros() == 0)
        self.assert_(mat.empty())

        mat.insert(5, 10, 0.5)
        mat.insert(600, 20, 0.6)
        mat.insert(800, 800, 0.8)
        self.assert_(not mat.empty())
        self.assert_(mat.nnonzeros() == 3)
        self.assert_(not mat.is_symmetric(1e-10))
        
        mat.insert(10, 5, 0.5)
        mat.insert(20, 600, 0.6)
        self.assert_(mat.is_symmetric(1e-10))

        mat.resize(900, 900)
        self.assert_(mat.nnonzeros() == 0)

    def Transpose(self):
        matrix1 = loadMatrix('matrix1')
        mat = matrix1.transpose()
        saveMatrix(mat, "matrix.out")
        self.assert_(fp_file_compare('matrix.out',
                                     os.path.join(datadir, 'transpose.mtx'),
                                     1.e-8))
        file_utils.remove('matrix.out')
        
    def Add(self):
        matrix1 = loadMatrix('matrix1')
        matrix2 = loadMatrix('matrix2')
        s = matrix1 + matrix2
        saveMatrix(s, 'matrix.out')
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
        vector = loadVector("vector0")
        saveVector(vector, "vector.out")
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vector0.out'),
                                     1.e-8))
        file_utils.remove('vector.out')

    def Basics(self):
        vec = doublevec.DoubleVec(10)
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vec_zero'),
                                     1.e-8))

        vec = doublevec.DoubleVec(10, 0.5)
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vec_init'),
                                     1.e-8))
        
        vec.unit()
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vec_unit'),
                                     1.e-8))

        self.assert_(vec.size() == 10)

        vec.resize(5)
        self.assert_(vec.size() == 5)
        file_utils.remove('vector.out')

    def Add(self):
        vector0 = loadVector('vector0')
        vector1 = loadVector('vector1')
        self.assertEqual(vector0.size(), 4)
        self.assertEqual(vector1.size(), 4)
        sum = vector0 + vector1
        saveVector(sum, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecsum.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec.axpy(2.0, vector1)
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecsum2.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec += vector1
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecsum.out'),
                                     1.e-8))
        diff = vector0 - vector1
        saveVector(diff, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecdiff.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec -= vector1
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecdiff.out'),
                                     1e-08))
        file_utils.remove('vector.out')
        
    def Multiply(self):
        vector0 = loadVector('vector0')
        vector1 = loadVector('vector1')
        vec = 2*vector0
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        vec = vector0*2.0
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        vec = vector0/0.5
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec *= 2.0
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'vecprod.out'),
                                     1.e-8))
        vec = vector0.clone()
        vec /= 0.5
        saveVector(vec, 'vector.out')
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
        saveVector(vec, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'matvec.out'),
                                     1.e-8))
        vec = vector*matrix
        saveVector(vec, 'vector.out')
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
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve0.out'),
                                     1.e-8))

        rhs = loadVector('rhs1')
        lower.solve_lower_triangle_unitd(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve1.out'),
                                     1.e-8))

        # Upper triangular matrix with explicit diagonal entries.
        upper = loadMatrix('uppertri')
        rhs = loadVector('rhs0')
        upper.solve_upper_triangle(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve2.out'),
                                     1.e-8))
        resid = upper*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        upper.solve_upper_triangle(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve3.out'),
                                     1.e-8))
        resid = upper*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        # Transpose of upper triangular matrix with explicit diagonal entries.
        rhs = loadVector('rhs0')
        upper.solve_upper_triangle_trans(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve4.out'),
                                     1.e-8))
        resid = upper.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        upper.solve_upper_triangle_trans(rhs, result)
        saveVector(result, 'vector.out')
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
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve6.out'),
                                     1.e-8))
        resid = lower.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        lower.solve_lower_triangle_trans(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve7.out'),
                                     1.e-8))
        resid = lower.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        # Lower triangular matrix with explicit unit diagonal entries.
        rhs = loadVector('rhs0')
        lower.solve_lower_triangle(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve8.out'),
                                     1.e-8))
        resid = lower*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        lower.solve_lower_triangle(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve9.out'),
                                     1.e-8))
        resid = lower*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        # Transpose of lower triangular matrix with implicit unit
        # diagonal.
        lower = loadMatrix('lowertriunit')
        lowerunit = lower.unit_lower();
        rhs = loadVector('rhs0')
        lower.solve_lower_triangle_trans_unitd(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve10.out'),
                                     1.e-8))
        resid = lowerunit.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        rhs = loadVector('rhs1')
        lower.solve_lower_triangle_trans_unitd(rhs, result)
        saveVector(result, 'vector.out')
        self.assert_(fp_file_compare('vector.out',
                                     os.path.join(datadir, 'solve11.out'),
                                     1.e-8))
        resid = lowerunit.transpose()*result - rhs
        self.assertAlmostEqual(resid.norm(), 0.0, 8)

        file_utils.remove('vector.out')

basic_set = [
    Matrix_Ops("MatrixIO"),
    Matrix_Ops("Basics"),
    Vector_Ops("VectorIO"),
    Vector_Ops("Basics"),
]
math_set = [
    Matrix_Ops("Add"),
    Matrix_Ops("Add_In_Place"),
    Matrix_Ops("Scalar_Multiply"),
    Matrix_Ops("Matrix_Multiply"),
    Matrix_Ops("Transpose"),
    Vector_Ops("Add"),
    Vector_Ops("Multiply"),
    Matrix_Vector_Ops("Multiply"),
    Matrix_Vector_Ops("Solve"),
]

test_set = basic_set + math_set
