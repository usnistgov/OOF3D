// -*- C++ -*-
// $RCSfile: testsolver.C,v $
// $Revision: 1.2.142.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:43 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// File to demonstrate what appears to be a pathology of the GMRES 
// solver -- certain matrices seem to give it a lot of trouble.

#include "common/config.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unistd.h>
using namespace std;

#define MAIN
#include "sparselink.h"
#include "SparseLib++/gmres.h"
#include "SparseLib++/cg.h"
#include "SparseLib++/bicg.h"
#include "SparseLib++/bicgstab.h"
#include "SparseLib++/ilupre_double.h"
#include "SparseLib++/comprow_double.h"
#include "SparseLib++/mvmd.h"
#include "preconditioner.h"
#include "engine/matvec.h"


SparseLinkMatrix<double> matrix_populate(std::ifstream *f) {
  std::vector<int> row,col;
  std::vector<double> z;
  int rtemp,ctemp,rowsize=0,colsize=0;
  double ztemp;
  
  // Scan the data so we know the size before we build the mtx.
  while( (*f) >> rtemp >> ctemp >> ztemp ) {
    row.push_back(rtemp);
    col.push_back(ctemp);
    z.push_back(ztemp);
    rowsize = (rtemp > rowsize ? rtemp : rowsize);
    colsize = (ctemp > colsize ? ctemp : colsize);
  } 
  
  if(rowsize!=colsize) {
    std::cerr << "Matrix is not square.  Carrying on regardless." << std::endl;
  }

  SparseLinkMatrix<double> A(rowsize+1,colsize+1);

  for(int i=0; i<z.size(); ++i) {
    A(row[i],col[i])=z[i];
  }
  return A;
}

void rhs_populate(VECTOR_D &rhs, std::ifstream *f) {
  int itemp;
  double ztemp;
  
  while( (*f) >> itemp >> ztemp ) {
    if(itemp < rhs.size() )
      rhs[itemp] = ztemp;
    else
      std::cerr << "Out of bounds value in rhs, ignored." << std::endl;
  }
}

int main(int argc, char *argv[]) {

  extern int optind;
  extern char *optarg;
  string mname,rname;
  int c;

  enum {SOLV_GMRES, SOLV_CG, SOLV_BiCG, SOLV_BiCGSTAB} solver;

  // Defaults for settable parameters.
  bool precondition=0;
  int krylov_dim=10;
  double tol = 1.0e-5;
  int maxiters=1000;
  solver = SOLV_GMRES;
  std::ifstream *mtxfile=0,*rhsfile=0;
  

  bool mtxfilearg = 0;
  bool rhsfilearg = 0;
  while((c=getopt(argc,argv,"f:r:gcbst:i:p"))!=-1) {
    switch((char)c) {
    case 'f':
      mname = optarg;
      mtxfile = new ifstream(optarg);
      mtxfilearg = 1;
      break;
    case 'r':
      rname = optarg;
      rhsfile = new ifstream(optarg);
      rhsfilearg = 1;
      break;
    case 'i':
      maxiters = atoi(optarg);
      break;
    case 't':
      tol = atof(optarg);
      break;
    case 'g':
      solver = SOLV_GMRES;
      break;
    case 'c':
      solver = SOLV_CG;
      break;
    case 'b':
      solver = SOLV_BiCG;
      break;
    case 's':
      solver = SOLV_BiCGSTAB;
      break;
    case 'p':
      precondition = 1;
      break;
    default:
      break;
    }
  }

  if(!mtxfilearg) {
    std::cerr << std::endl << "Usage: " << std::endl;
    std::cerr << "testsolver -f <mtxfile> <-r rhsfile> <-[g|c|b|s]> " <<
      "<-i iterations> <-t tol> <-p>" << std::endl;
    std::cerr << "Mtxfile argument is mandatory.  Default rhs is trivial."
	      << std::endl << std::endl;
    _exit(4);
  }
  if(!(*mtxfile)) {
    std::cerr << "Matrix file " << mname <<   
      " not found, unable to proceed." << std::endl;
    _exit(2);
  }
  
  SparseLinkMatrix<double> Amat = matrix_populate(mtxfile);
  VECTOR_D rhs(Amat.ncols(),0.0);
  VECTOR_D x(Amat.nrows(),0.0);

  if(rhsfilearg) {
    if(*rhsfile) {
      rhs_populate(rhs, rhsfile);
    }
    else {
      std::cerr << "Right-hand side file " << rname << "not found, aborting." 
		<< std::endl;
      _exit(4);
    }
  }

  CompRow_Mat_double A(Amat);

  // Preconditioner constructers don't allow you to create a variable
  // of the appropriate type and assign as required -- easier to
  // create both preconditioners, and then just use whichever one is
  // appropriate.  Unconditioner is required because you have to pass
  // in *something* for 3rd argument of the SparseLib++ solvers.
  Unconditioner precon0(A);
  CompRow_ILUPreconditioner_double precon1(A);
  
  bool failure = 0;
  MATRIX_D H(krylov_dim+1, krylov_dim);

  switch(solver) {
  case SOLV_GMRES:
    if(precondition) {
      std::cerr << "Running GMRES, preconditioned." << std::endl;
      failure = GMRES(A, x, rhs, precon1, H, krylov_dim, maxiters, tol);
    } 
    else {
      std::cerr << "Running GMRES, unpreconditioned." << std::endl;
      failure = GMRES(A, x, rhs, precon0, H, krylov_dim, maxiters, tol);
    }
    break;
  case SOLV_CG:
    if(precondition) {
      std::cerr << "Running CG, preconditioned." << std::endl;
      failure = CG(A, x, rhs, precon1, maxiters, tol);
    }
    else {
      std::cerr << "Running CG, unpreconditioned." << std::endl;
      failure = CG(A, x, rhs, precon0, maxiters, tol);
    }
    break;
  case SOLV_BiCG:
    if(precondition) {
      std::cerr << "Running BiCG, preconditioned." << std::endl;
      failure = BiCG(A, x, rhs, precon1, maxiters, tol);
    }
    else {
      std::cerr << "Running BiCG, unpreconditioned." << std::endl;
      failure = BiCG(A, x, rhs, precon0, maxiters, tol);
    }
    break;
  case SOLV_BiCGSTAB:
    if(precondition) {
      std::cerr << "Running BiCGSTAB, preconditioned." << std::endl;
      failure = BiCGSTAB(A, x, rhs, precon1, maxiters, tol);
    }
    else {
      std::cerr << "Running BiCGSTAB, unpreconditioned." << std::endl;
      failure = BiCGSTAB(A, x, rhs, precon0, maxiters, tol);
    }
    break;
  }

  if(failure) 
    std::cerr << "Solution failed to converge." << std::endl;
  else
    std::cerr << "Solution converged." << std::endl;

  std::cerr << "Iterations: " << maxiters << std::endl;
  std::cerr << "Nominal residual: " << tol << std::endl;
  std::cerr << std::endl << "Solution:" << std::endl;
  for(int i=0;i<x.size();++i) {
    std::cerr << i << " : " << x[i] << std::endl;
  }

  // For extra-super-paranoia, rebuild matrix from Amat.
  CompRow_Mat_double newA(Amat);
  VECTOR_D check_rhs = newA*x;

  std::cerr << "Residuals: " << std::endl;
  double residual=0.0, rms=0.0;
  for(int i=0;i<check_rhs.size(); ++i) {
    residual = check_rhs[i]-rhs[i];
    std::cerr << i << " : " << residual << std::endl;
    rms+=residual*residual;
  }
  rms=sqrt(rms/check_rhs.size());
  std::cerr << "RMS residual: " << rms << std::endl;

}
