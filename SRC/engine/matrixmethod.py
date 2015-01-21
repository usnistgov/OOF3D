# -*- python -*-
# $RCSfile: matrixmethod.py,v $
# $Revision: 1.6.4.3 $
# $Author: fyc $
# $Date: 2014/07/28 22:14:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.engine import cmatrixmethods
from ooflib.SWIG.engine import ooferror2
from ooflib.SWIG.engine import preconditioner
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

import math

# Methods for solving SparseMat matrix equations.  Subclasses need to
# have a (Python) 'solveMatrix' method which takes four non-self arguments:
#   a SparseMat matrix
#   a DoubleVec rhs
#   a DoubleVec solution
# and returns a tuple containing the number of iterations taken and
# the final residual.

## TODO OPT: MAYBE Cache the preconditioners in the LinearizedSystem
## so they can be re-used if the matrix hasn't changed.

class MatrixMethod(registeredclass.RegisteredClass):
    registry = []
    def shortrepr(self):
        return self.__class__.__name__
    def solve(self, matrix, rhs, solution):
        return self.solveMatrix(matrix, rhs, solution)
    tip="Ways to solve a matrix equation."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/matrixmethod.xml')
            

class PreconditionedMatrixMethod(MatrixMethod):
    def shortrepr(self):
        return "%s(%s)" % (self.__class__.__name__, 
                           self.preconditioner.shortrepr())

class SymmetricMatrixMethodParam(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        super(SymmetricMatrixMethodParam, self).__init__(
            name, MatrixMethod, value=value, default=default, tip=tip,
            auxData=auxData)

class AsymmetricMatrixMethodParam(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        super(AsymmetricMatrixMethodParam, self).__init__(
            name, MatrixMethod, value=value, default=default, tip=tip,
            auxData=auxData)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

_check_symmetry = False #debug.debug()

## The routines in cmatrixmethods return the number of iterations and
## the residual. 

class ConjugateGradient(PreconditionedMatrixMethod):
    def __init__(self, preconditioner, tolerance, max_iterations):
        self.preconditioner = preconditioner
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    def solveMatrix(self, matrix, rhs, solution):
        if _check_symmetry:
            import sys
            if (matrix.nrows()!=matrix.ncols() or
                not matrix.is_symmetric(1.e-12)): # can be very slow
                raise ooferror2.ErrPyProgrammingError(
                    "%dx%d CG matrix is not symmetric!" %
                    (matrix.nrows(), matrix.ncols()))
#         debug.fmsg("matrix=\n%s" % matrix)
#         debug.fmsg("rhs=", rhs)
        pc = self.preconditioner.create_preconditioner(matrix)
        return cmatrixmethods.solveCG(
            matrix, rhs, pc,
            self.max_iterations, self.tolerance, solution)

registeredclass.Registration(
    "CG",
    MatrixMethod,
    ConjugateGradient,
    ordering=1,
    symmetricOnly=True,
    params=[
        parameter.RegisteredParameter(
            "preconditioner",
            preconditioner.PreconditionerPtr,
            tip="Black magic for making the matrix more easily solvable."),
        parameter.FloatParameter(
            "tolerance", 1.e-13,
            tip="Largest acceptable relative error in the matrix solution."),
        parameter.IntParameter(
            "max_iterations", 1000,
            tip="Maximum number of iterations to perform.")],
    tip="Conjugate Gradient method for iteratively solving symmetric matrices.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/cg.xml')
    )

def check_symmetry(menuitem, state):
    global _check_symmetry
    _check_symmetry = state

mainmenu.debugmenu.addItem(
    oofmenu.CheckOOFMenuItem(
        'Check_CG_symmetry',
        debug.debug(),
        callback=check_symmetry,
        help='Verify matrix symmetry before using Conjugate Gradient.',
        discussion="<para>For debugging.  Slow.</para>"))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class BiConjugateGradient(PreconditionedMatrixMethod):
    def __init__(self, preconditioner, tolerance, max_iterations):
        self.preconditioner = preconditioner
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    def solveMatrix(self, matrix, rhs, solution):
        pc = self.preconditioner.create_preconditioner(matrix)
        return cmatrixmethods.solveBiCG(
            matrix, rhs, pc,
            self.max_iterations, self.tolerance, solution)

registeredclass.Registration(
    "BiCG",
    MatrixMethod,
    BiConjugateGradient,
    ordering=2,
    symmetricOnly=False,
    params=[
        parameter.RegisteredParameter(
            "preconditioner",
            preconditioner.PreconditionerPtr,
            tip="Black magic for making the matrix more easily solvable."),
        parameter.FloatParameter(
            "tolerance", 1.e-13,
            tip="Largest acceptable relative error in the matrix solution."),
        parameter.IntParameter(
            "max_iterations", 1000,
            tip="Maximum number of iterations to perform.")],
    tip="Bi-conjugate gradient method for iteratively solving non-symmetric matrices.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/bicg.xml')
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class StabilizedBiConjugateGradient(PreconditionedMatrixMethod):
    def __init__(self, preconditioner, tolerance, max_iterations):
        self.preconditioner = preconditioner
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    def solveMatrix(self, matrix, rhs, solution):
        pc = self.preconditioner.create_preconditioner(matrix)
        return cmatrixmethods.solveBiCGStab(
            matrix, rhs, pc,
            self.max_iterations, self.tolerance, solution)

registeredclass.Registration(
    "BiCGStab",
    MatrixMethod,
    StabilizedBiConjugateGradient,
    ordering=2.1,
    symmetricOnly=False,
    params=[
        parameter.RegisteredParameter(
            "preconditioner",
            preconditioner.PreconditionerPtr,
            tip="Black magic for making the matrix more easily solvable."),
        parameter.FloatParameter(
            "tolerance", 1.e-13,
            tip="Largest acceptable relative error in the matrix solution."),
        parameter.IntParameter(
            "max_iterations", 1000,
            tip="Maximum number of iterations to perform.")],
    tip="Stabilized bi-conjugate gradient method for iteratively solving non-symmetric matrices.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/bicgstab.xml')
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class GeneralizedMinResidual(PreconditionedMatrixMethod):
    def __init__(self, preconditioner, tolerance, max_iterations,
                 krylov_dimension):
        self.preconditioner = preconditioner
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.krylov_dimension = krylov_dimension
    def solveMatrix(self, matrix, rhs, solution):
        pc = self.preconditioner.create_preconditioner(matrix)
        return cmatrixmethods.solveGMRes(
            matrix, rhs, pc,
            self.max_iterations, self.krylov_dimension, self.tolerance,
            solution)

registeredclass.Registration(
    "GMRES",
    MatrixMethod,
    GeneralizedMinResidual,
    ordering=3,
    symmetricOnly=False,
    params=[
        parameter.RegisteredParameter(
            "preconditioner",
            preconditioner.PreconditionerPtr,
            tip="Black magic for making the matrix more easily solvable."),
        parameter.FloatParameter(
            "tolerance", 1.e-13,
            tip="Largest acceptable relative error in the matrix solution."),
        parameter.IntParameter(
            "max_iterations", 1000,
            tip="Maximum number of iterations to perform."),
        parameter.IntParameter(
            "krylov_dimension", 100,
            tip="Making the Krylov dimension bigger will improve convergence but use more memory.")],
    tip="Generalized Minimal Residual method for iteratively solving non-symmetric matrices.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/gmres.xml')
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class DirectMatrixSolver(MatrixMethod):
    def solveMatrix(self, matrix, rhs, solution):
        cmatrixmethods.solveDirect(matrix, rhs, solution)
        return (1, 0)

registeredclass.Registration(
    "Direct",
    MatrixMethod,
    DirectMatrixSolver,
    ordering=400,
    symmetricOnly=False,
    tip="A non-iterative non-sparse matrix solver using LU decomposition.  Uses a lot of memory.  Not recommended if the finite element mesh is large.",
    discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/reg/directmatrix.xml"))

## TODO 3.1: Add a PETSc method?

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# BasicMatrixMethod is used when setting solver parameters in Basic
# mode.  It only requires the user to choose between Iterative and
# Direct.

class BasicMatrixMethod(registeredclass.RegisteredClass):
    registry = []
    tip="Simple methods for solving matrix equations."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/basicmatrix.xml')

class BasicDirect(BasicMatrixMethod):
    def shortrepr(self):
        return "Direct"
    def resolve_symmetric(self, existingSolver):
        if isinstance(existingSolver, DirectMatrixSolver):
            return existingSolver
        return DirectMatrixSolver()
    def resolve_asymmetric(self, existingSolver):
        if isinstance(existingSolver, DirectMatrixSolver):
            return existingSolver
        return DirectMatrixSolver()


class BasicIterative(BasicMatrixMethod):
    def __init__(self, tolerance, max_iterations):
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    def resolve_symmetric(self, existingSolver):
        if (isinstance(existingSolver, ConjugateGradient) and
            existingSolver.tolerance == self.tolerance and
            existingSolver.max_iterations == self.max_iterations and
            isinstance(existingSolver.preconditioner,
                       preconditioner.ILUPreconditioner)):
            return existingSolver
        return ConjugateGradient(
            preconditioner=preconditioner.ILUPreconditioner(),
            tolerance=self.tolerance,
            max_iterations=self.max_iterations)
    def resolve_asymmetric(self, subproblemcontext, existingSolver):
        krylov_guess = 30;    # Guess the krylov dimension for GMRES. 
        if (isinstance(existingSolver, GeneralizedMinResidual) and
            existingSolver.tolerance == self.tolerance and
            existingSolver.max_iterations == self.max_iterations and
            existingSolver.krylov_dimension == krylov_guess and
            isinstance(existingSolver.preconditioner,
                       preconditioner.ILUPreconditioner)):
            return existingSolver
        return GeneralizedMinResidual(
            preconditioner=preconditioner.ILUPreconditioner(),
            tolerance=self.tolerance,
            max_iterations=self.max_iterations,
            krylov_dimension=krylov_guess)
    def shortrepr(self):
        return "Iterative"

registeredclass.Registration(
    'Iterative',
    BasicMatrixMethod,
    BasicIterative,
    ordering=0,
    params=[
        parameter.FloatParameter(
            "tolerance", 1.e-13,
            tip="Largest acceptable relative error in the matrix solution."),
        parameter.IntParameter(
            "max_iterations", 1000,
            tip="Maximum number of iterations to perform.")],
    tip='Solve matrix equations approximately and iteratively, without using exta memory.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/basiciterative.xml')
    )

registeredclass.Registration(
    'Direct',
    BasicMatrixMethod,
    BasicDirect,
    ordering=1,
    tip='Solve matrix equations with a direct method.  Not recommended for large problems.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/basicdirect.xml'))
                
