// -*- C++ -*-
// $RCSfile: petsc_solverdriver.h,v $
// $Revision: 1.10.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:24 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PETSCSOLVERDRIVER_H
#define PETSCSOLVERDRIVER_H

/*
  Invokes PETSc universe. Universe is created if 
   any solver is called. PETSc Universe must persist
   until the end of OOF sesion. Otherwise, expect a
   segmentation fault. PETSc universe is destroyed
   when OOF exits.
*/
class PETScEnvironment
{
public:
  int argc;
  char** argv;
  PETScEnvironment(std::vector<char*> *argh)
  {
    argc=argh->size();
    argv=new char*[argc];
    // For some reason, the command line argument strings must be the same pointers as the
    // ones in sys.argv (python) or main(argc,char* argv[]) (C).
    // We can't make dummy argv's and expect mpirun to spawn multiple processes.
    // (Might be that the commandline arguments contain the program name)
    for(int i=0;i<argc;i++)
      {
	argv[i]=(*argh)[i];
      }
    //argv[0]=new char[50];
    //argv[1]=new char[50];
    //argv[2]=new char[50];
    //sprintf(argv[0],"oof2");
    //sprintf(argv[1],"-log_summary");
    //sprintf(argv[2],"-ksp_type");
    PetscInitialize(&argc,&argv,PETSC_NULL,PETSC_NULL);
    int size;
    MPI_Comm_size(PETSC_COMM_WORLD,&size);
    std::cerr << "number of processors = " << size << std::endl;
  }
  virtual ~PETScEnvironment()
  {
    PetscFinalize();
    //delete[] argv[0];
    //delete[] argv[1];
    //delete[] argv[2];
    delete[] argv;
  }
};

void InitPETSc(std::vector<char*> *argh);

class SteppingScheme;

class PETScSolverDriverCore
{
  /*
    The base SolverDriverCore class applies a solver 
    to an femesh.
    precompute() creates the different bits, using the FEMesh.
    solve() handles the solver.
    postcompute() places the final solution in the femesh and 
    cleans whatever mess was left behind.
  */

protected:
  LinearSolver * solver;
  CSubProblem * subproblem;

  // This class patterned after solverdriver, but don't know how to use stepping scheme with PETSc yet.
  // Assume it acts like a null scheme for petsc, for now.
  SteppingScheme * sscheme;//stepper uses K and b
  //to solve the Kx=b system
  CSRmatrix * K;
  VECTOR_D *b;
  int nrowsA, ncolsA;

public:
  void set_stepping_scheme(SteppingScheme *smethod) {sscheme = smethod;}

  void clear_memory();

  //CSRmatrix * A;
  //CSRmatrix * C;
  VECTOR_D * x;
  VECTOR_D * rhs;
  VECTOR_D * xp;
  // Petscify the matrices and vectors
  Mat Apetsc_,Cpetsc_;
  Vec xpetsc_,rhspetsc_,xp_petsc_;

  int nrows() {return nrowsA;}
  int ncols() {return ncolsA;}

  PETScSolverDriverCore(SteppingScheme *, LinearSolver *, CSubProblem *);
  PETScSolverDriverCore() : solver(0),
			    subproblem(0),
			    sscheme(0),
			    K(0),
			    b(0),
			    nrowsA(0), 
			    ncolsA(0),
			    //A(0),
			    //C(0),
			    x(0),
			    rhs(0),
			    xp(0)
  {}

  virtual ~PETScSolverDriverCore();

  virtual double residual();
  virtual void precompute(); // create C-objects that will only
			     // persist during iterative process
  virtual bool solve(); // do real work
  virtual void postcompute(); // clean-up the mess
  void set_solver_components (LinearSolver *ls, CSubProblem *subp);

  // The following need not be templates
  template <class MTX, class VEC>
  int InitAsubmatrix(const MTX& mat, const VEC& rowmap, const VEC& colmap, int& nrows, int& ncols);

  template <class MTX, class VEC>
  int InitCsubmatrix(const MTX& mat, const VEC& rowmap, const VEC& colmap, int& nrows, int& ncols);

#ifdef HAVE_MPI
  void precompute_parallel();
  template <class MTX, class VEC>

  int InitAsubmatrix_parallel(const MTX& mat, const VEC& rowmap, const VEC& colmap, int nr, int nc);
#endif
};

#endif // PETSCSOLVERDRIVER_H
