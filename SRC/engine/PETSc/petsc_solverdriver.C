// -*- C++ -*-
// $RCSfile: petsc_solverdriver.C,v $
// $Revision: 1.15.18.1 $
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

#include <oofconfig.h>
#include "engine/csrmatrix.h"
#include "engine/csubproblem.h"
#include "engine/matvec.h"
#include "engine/solver.h"
extern "C"
{
#include "petscksp.h"
}
#include "petsc_solverdriver.h"
#include "engine/steppingscheme.h"

// This function preferably called at around the start of oof2 initialization.
// Need to pass to it the command line arguments (perhaps from python).
void InitPETSc(std::vector<char*> *argh)
{
  //If mesh is solved with PETSc, keep the environment until closing session
  static PETScEnvironment petsc_environment(argh);
}

PETScSolverDriverCore::~PETScSolverDriverCore()
{
}

PETScSolverDriverCore::PETScSolverDriverCore(SteppingScheme *stepsch,
				   LinearSolver *solver, CSubProblem *subp)
  : solver(solver),
    subproblem(subp),
    sscheme(stepsch),
    K(0),
    b(0),
    nrowsA(0), 
    ncolsA(0),
    //A(0),
    //C(0),
    x(0),
    rhs(0),
    xp(0)
{
}

void PETScSolverDriverCore::set_solver_components(LinearSolver *ls, CSubProblem *subp)
{
  solver = ls;
  subproblem = subp;
}

double PETScSolverDriverCore::residual()
{
  return solver->get_residual();
}

void PETScSolverDriverCore::precompute()
{
#ifdef HAVE_MPI

  precompute_parallel();

#else
  // At this point the solver and the preconditioner are already selected
  // at the UI and passed as arguments into the solver
  RWLock * rwlock = subproblem->mesh->get_rwlock();
  rwlock->read_acquire(); //acquire read lock

  try
    {

      // Wrap some timing code around
      struct timeval tp;
      double t1,t2;
      int rtn=gettimeofday(&tp,NULL);
      t1=(double)tp.tv_sec+(1.e-6)*tp.tv_usec;

      int nrows,ncolsA,ncolsC;

      PetscPrintf(PETSC_COMM_WORLD,"The A submatrix in petsc:\n");
      // Transfer A submatrix to petsc (Apetsc_). Check that it is square
      if(InitAsubmatrix((subproblem->linearsystem).get_stiffness(),
			subproblem->indepeqnmap,subproblem->freedofmap,nrows,ncolsA)!=0)
	throw ErrSetupError("Stiffness matrix (A) is not square! nrows="
			    + to_string(nrows) + ", ncols="
			    + to_string(ncolsA));

      this->nrowsA=nrows;
      this->ncolsA=ncolsA;

      PetscPrintf(PETSC_COMM_WORLD,"The C submatrix in petsc:\n");
      // Transfer C submatrix to Cpetsc_
      // A and C should have the same nrows
      InitCsubmatrix((subproblem->linearsystem).get_stiffness(),
		     subproblem->indepeqnmap,subproblem->fixeddofmap,nrows,ncolsC);

      // Do the usual thing and fetch the x,rhs,and xp vectors, then copy these to petsc.
      // The dof is private to femesh so a more direct copy is not possible for now.
      if (!x)
	{
	  x = new VECTOR_D (ncolsA, 0.0);
	}
      x->clear();
      subproblem->get_unknowns(*x, subproblem->freedofmap);

      if (!rhs)
	{
	  rhs = new VECTOR_D (ncolsA, 0.0);
	}
      rhs->clear();
      subproblem->get_rhs(*rhs, subproblem->indepeqnmap);

      if (!xp)
	{
	  xp = new VECTOR_D (ncolsC, 0.0);
	}
      xp->clear();
      subproblem->get_unknowns(*xp, subproblem->fixeddofmap);

      // Now create petsc vectors...
      VecCreate(PETSC_COMM_WORLD,&xpetsc_);
      VecSetSizes(xpetsc_,PETSC_DECIDE,ncolsA);
      VecSetFromOptions(xpetsc_);
      VecDuplicate(xpetsc_,&rhspetsc_);

      VecCreate(PETSC_COMM_WORLD,&xp_petsc_);
      VecSetSizes(xp_petsc_,PETSC_DECIDE,ncolsC);
      VecSetFromOptions(xp_petsc_);

      // ...and copy the fetched vectors to petsc
      PetscScalar S;
      for(int i=0; i<ncolsA; i++)
	{
	  S=(*x)(i);
	  VecSetValues(xpetsc_,1,&i,&S,INSERT_VALUES);
	}
      VecAssemblyBegin(xpetsc_);
      //Anything you want to do in the mean time? Put it here.
      VecAssemblyEnd(xpetsc_);

      // Take a peek
      //VecView(xpetsc_,PETSC_VIEWER_STDOUT_WORLD);

      for(int i=0; i<ncolsA; i++)
	{
	  S=(*rhs)(i);
	  VecSetValues(rhspetsc_,1,&i,&S,INSERT_VALUES);
	}
      VecAssemblyBegin(rhspetsc_);
      //Anything you want to do in the mean time? Put it here.
      VecAssemblyEnd(rhspetsc_);

      // Take a peek
      //VecView(rhspetsc_,PETSC_VIEWER_STDOUT_WORLD);

      for(int i=0; i<ncolsC; i++)
	{
	  S=-(*xp)(i);
	  VecSetValues(xp_petsc_,1,&i,&S,INSERT_VALUES);
	}
      VecAssemblyBegin(xp_petsc_);
      //Anything you want to do in the mean time? Put it here.
      VecAssemblyEnd(xp_petsc_);

      // Take a peek
      //VecView(xp_petsc_,PETSC_VIEWER_STDOUT_WORLD);

      // Get the equivalent of *rhs -= (*C) * (*xp);
      MatMultAdd(Cpetsc_,xp_petsc_,rhspetsc_,rhspetsc_);

      // Take a peek
      //VecView(rhspetsc_,PETSC_VIEWER_STDOUT_WORLD);

      rtn=gettimeofday(&tp,NULL);
      t2=(double)tp.tv_sec+(1.e-6)*tp.tv_usec;
      PetscPrintf(PETSC_COMM_WORLD,"Timing petsc solverdriver precompute: %lf\n",(t2-t1));

    } //end of try block
  catch(...) //guarantee that lock will be released if ANY exception is raised
    {
      rwlock->read_release(); 
      throw;
    }

  rwlock->read_release();

#if 0
  //stepper interactions
  sscheme->precompute(subproblem, A, rhs, x);//these lines should be outside the locked area

  // Get the K matrix and b vector of the linear system, and store it.
  // We don't actually own these matrices, but they're stored as
  // object attributes so they're common to precompute, solve, and
  // postcompute.
  K = sscheme->get_K(subproblem, A);
  b = sscheme->get_b(subproblem, A, rhs);
#endif

#endif
}

//#include <sys/time.h>

bool PETScSolverDriverCore::solve()
{
  solver->set_blocking(subproblem);

  // petsc solver precompute does nothing, and there is no CSRmatrix member anymore
  //solver->precompute(*K);

  // Wrap some timing code around solve
  struct timeval tp;
  double t1,t2;
  int rtn=gettimeofday(&tp,NULL);
  t1=(double)tp.tv_sec+(1.e-6)*tp.tv_usec;

  bool status = solver->solve(Apetsc_, rhspetsc_, xpetsc_);

  rtn=gettimeofday(&tp,NULL);
  t2=(double)tp.tv_sec+(1.e-6)*tp.tv_usec;
  PetscPrintf(PETSC_COMM_WORLD,"Timing petsc solver solve: %lf\n",(t2-t1));

  solver->postcompute(); // Call possibly-null post-compute hook.

  return status;
}

void PETScSolverDriverCore::postcompute()
{
  RWLock * rwlock = subproblem->mesh->get_rwlock();
  rwlock->write_acquire();

  try
    {
#ifdef HAVE_MPI

      int dim=subproblem->m_combinedmatrixdim;
      Vec xlocalpetsc;
      VecCreateSeq(PETSC_COMM_SELF,dim,&xlocalpetsc);
      IS is,islocal;
      ISCreateStride(PETSC_COMM_WORLD,dim,0,1,&is);
      ISCreateStride(PETSC_COMM_SELF,dim,0,1,&islocal);
      VecScatter ctx;
      VecScatterCreate(xpetsc_,is,xlocalpetsc,islocal,&ctx);
      VecScatterBegin(xpetsc_,xlocalpetsc,INSERT_VALUES,SCATTER_FORWARD,ctx);
      VecScatterEnd(xpetsc_,xlocalpetsc,INSERT_VALUES,SCATTER_FORWARD,ctx);
      VecScatterDestroy(ctx);
      ISDestroy(is);
      ISDestroy(islocal);

      //PetscScalar* temp_array;
      double* temp_array;
      VecGetArray(xlocalpetsc, &temp_array);

      subproblem->NodalPositionSolution(temp_array);

      VecRestoreArray(xlocalpetsc,&temp_array);
      VecDestroy(xlocalpetsc);

#else

      // Copy possibly-distributed vector into a sequential (local) vector, to get all the components
      Vec xlocalpetsc;
      VecCreateSeq(PETSC_COMM_SELF,ncolsA,&xlocalpetsc);
      IS is,islocal;
      ISCreateStride(PETSC_COMM_WORLD,ncolsA,0,1,&is);
      ISCreateStride(PETSC_COMM_SELF,ncolsA,0,1,&islocal);
      VecScatter ctx;
      VecScatterCreate(xpetsc_,is,xlocalpetsc,islocal,&ctx);
      VecScatterBegin(xpetsc_,xlocalpetsc,INSERT_VALUES,SCATTER_FORWARD,ctx);
      VecScatterEnd(xpetsc_,xlocalpetsc,INSERT_VALUES,SCATTER_FORWARD,ctx);
      VecScatterDestroy(ctx);
      ISDestroy(is);
      ISDestroy(islocal);

      //VecView(xpetsc_,PETSC_VIEWER_STDOUT_WORLD);

      // Have to copy the PETSc vectors into VECTOR_D for OOF2
      PetscScalar* temp_array;
      VecGetArray(xlocalpetsc, &temp_array);
      for(int i = 0; i<ncolsA; i++)
	{
	  (*x)(i)=double(temp_array[i]);
	  //PetscPrintf(PETSC_COMM_WORLD,"xpetsc solution %d: %lf\n",i,(*x)(i));
	}
      VecRestoreArray(xlocalpetsc,&temp_array);
      VecDestroy(xlocalpetsc);

      subproblem->set_unknowns(*x, subproblem->freedofmap);
#endif

     // In the old days, when nodal equations had values, the values
     // of the dependent equations were computed here.  There's no
     // actual need to do this, but here's how it was done:
     // CSRmatrix Cp = femesh->Cpmatrix();
     // CSRmatrix B = femesh->Bmatrix();
     // femesh->set_rhs(Cp * (*x) + B * (*xp), femesh->depeqnmap);

      sscheme->set_x(x); //stepping scheme creates a copy of solution
    }
  catch(...)
    {
      rwlock->write_release();
    }
  rwlock->write_release();
  sscheme->postcompute(subproblem);
}

void PETScSolverDriverCore::clear_memory()
{
  // Destroy petsc matrices and vectors here
#ifdef HAVE_MPI
  MatDestroy(Apetsc_);
  //MatDestroy(Cpetsc_);

  VecDestroy(xpetsc_);
  VecDestroy(rhspetsc_);
  //VecDestroy(xp_petsc_);
#else
  MatDestroy(Apetsc_);
  MatDestroy(Cpetsc_);

  VecDestroy(xpetsc_);
  VecDestroy(rhspetsc_);
  VecDestroy(xp_petsc_);
#endif

  delete x;
  delete rhs;
  delete xp;

  sscheme->clean_up();
  K=0;
  b=0;
}


#if 0
// Extract submatrix from the large stiffness matrix that contains A,C,C',B.
// This code patterned/taken after comprow_double.h.
// Spawned two versions. The one for the A submatrix checks for squareness.
template <class MTX, class VEC>
int PETScSolverDriverCore::InitAsubmatrix(const MTX& mat,
					  const VEC& rowmap, const VEC& colmap,
					  int &nrows, int &ncols)
{
  // Count how many rows and columns are in the target matrix
  int nr = 0;
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > nr) nr = rowmap[i];
    }
  nr++;
  nrows=nr;

  int nc = 0;
  for(typename VEC::size_type i=0; i<colmap.size(); i++)
    {
      if(colmap[i] > nc) nc = colmap[i];
    }
  nc++;
  ncols=nc;

  // Invert the rowmap to find out which rows of the source matrix
  // contribute to each row of the target.
  std::vector<std::list<int> > invrowmap(nr);
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > -1)
	{
	  invrowmap[rowmap[i]].push_front(i);
	}
    }

  //int nz = 0;			// non-zeros found so far

  if(nr!=nc)//check for squareness
    return -1;

  PetscScalar S;
  int Istart,Iend;
  MatCreate(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,nr,nc,&Apetsc_);
  MatSetFromOptions(Apetsc_);
  MatGetOwnershipRange(Apetsc_,&Istart,&Iend);
  PetscPrintf(PETSC_COMM_WORLD,"maxnnz = %d, Istart = %d, Iend = %d\n",maxnnz,Istart,Iend);

  // loop over rows of the target matrix
  //  plus follow the petsc ownership range
  for(int i=Istart; i<Iend; i++)
    {
      // make a list of which columns appear in this row
      std::list<CSRRowEntry> cols;	// doubly linked list
      // loop over source rows that contribute to this target row
      for(std::list<int>::const_iterator isrc=invrowmap[i].begin();
	  isrc != invrowmap[i].end(); ++isrc)
	{
	  // loop over entries in source row
	  int srcrow = *isrc;
	  for(typename MTX::const_iterator ij=mat.begin(srcrow);
	      ij < mat.end(srcrow); ++ij)
	    {
	      int j = colmap[ij.col()];
	      if(j >= 0) {	// is this column being used?
		// has this column already been found?
		bool found = false;
		for(std::list<CSRRowEntry>::iterator tj=cols.begin();
		    tj != cols.end() && !found; ++tj)
		  {
		    int targetcol = (*tj).col();
		    if(j == targetcol) {
		      (*tj) += *ij; // add to preexisting entry
		      found = true;
		    }
		    else if(j < targetcol) {
		      cols.insert(tj, CSRRowEntry(j, *ij)); // insert before tj
		      found = true;
		    }
		  } // end loop over target columns
		if(!found) {
		  cols.push_back(CSRRowEntry(j, *ij));	// insert at end
		}
	      } // this source column is used
	    } // loop over entries in source row
	}	// loop over source rows that contribute to this target row

      // copy data into target matrix
      //nz += cols.size();
      //rowptr_[i+1] = nz;		// beginning of next row
      for(std::list<CSRRowEntry>::const_iterator tj=cols.begin();
	  tj != cols.end(); ++tj)
	{
	  //val_.push_back((*tj).val());
	  //colind_.push_back((*tj).col());
	  int j=(*tj).col();
	  S=(*tj).val();
	  MatSetValues(Apetsc_,1,&i,1,&j,&S,INSERT_VALUES);
	}

    } // end i-loop over target rows
  //nz_=nz;

  MatAssemblyBegin(Apetsc_,MAT_FINAL_ASSEMBLY);
  //Anything you want to do in the mean time? Put it here.
  MatAssemblyEnd(Apetsc_,MAT_FINAL_ASSEMBLY);

  // Take just a little peek before continuing
  //MatView(Apetsc_,PETSC_VIEWER_STDOUT_WORLD);

  return 0;
}

template <class MTX, class VEC>
int PETScSolverDriverCore::InitCsubmatrix(const MTX& mat,
					  const VEC& rowmap, const VEC& colmap,
					  int &nrows, int &ncols)
{
  // Count how many rows and columns are in the target matrix
  int nr = 0;
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > nr) nr = rowmap[i];
    }
  nr++;
  nrows=nr;

  int nc = 0;
  for(typename VEC::size_type i=0; i<colmap.size(); i++)
    {
      if(colmap[i] > nc) nc = colmap[i];
    }
  nc++;
  ncols=nc;

  // Invert the rowmap to find out which rows of the source matrix
  // contribute to each row of the target.
  std::vector<std::list<int> > invrowmap(nr);
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > -1)
	{
	  invrowmap[rowmap[i]].push_front(i);
	}
    }

  //int nz = 0;			// non-zeros found so far

  PetscScalar S;
  int Istart,Iend;
  MatCreate(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,nr,nc,&Cpetsc_);
  MatSetFromOptions(Cpetsc_);
  MatGetOwnershipRange(Cpetsc_,&Istart,&Iend);
  PetscPrintf(PETSC_COMM_WORLD,"maxnnz = %d, Istart = %d, Iend = %d\n",maxnnz,Istart,Iend);

  // loop over rows of the target matrix
  //  plus follow the petsc ownership range
  for(int i=Istart; i<Iend; i++)
    {
      // make a list of which columns appear in this row
      std::list<CSRRowEntry> cols;	// doubly linked list
      // loop over source rows that contribute to this target row
      for(std::list<int>::const_iterator isrc=invrowmap[i].begin();
	  isrc != invrowmap[i].end(); ++isrc)
	{
	  // loop over entries in source row
	  int srcrow = *isrc;
	  for(typename MTX::const_iterator ij=mat.begin(srcrow);
	      ij < mat.end(srcrow); ++ij)
	    {
	      int j = colmap[ij.col()];
	      if(j >= 0) {	// is this column being used?
		// has this column already been found?
		bool found = false;
		for(std::list<CSRRowEntry>::iterator tj=cols.begin();
		    tj != cols.end() && !found; ++tj)
		  {
		    int targetcol = (*tj).col();
		    if(j == targetcol) {
		      (*tj) += *ij; // add to preexisting entry
		      found = true;
		    }
		    else if(j < targetcol) {
		      cols.insert(tj, CSRRowEntry(j, *ij)); // insert before tj
		      found = true;
		    }
		  } // end loop over target columns
		if(!found) {
		  cols.push_back(CSRRowEntry(j, *ij));	// insert at end
		}
	      } // this source column is used
	    } // loop over entries in source row
	}	// loop over source rows that contribute to this target row

      // copy data into target matrix
      //nz += cols.size();
      //rowptr_[i+1] = nz;		// beginning of next row
      for(std::list<CSRRowEntry>::const_iterator tj=cols.begin();
	  tj != cols.end(); ++tj)
	{
	  //val_.push_back((*tj).val());
	  //colind_.push_back((*tj).col());
	  int j=(*tj).col();
	  S=(*tj).val();
	  MatSetValues(Cpetsc_,1,&i,1,&j,&S,INSERT_VALUES);
	}

    } // end i-loop over target rows
  //nz_=nz;

  MatAssemblyBegin(Cpetsc_,MAT_FINAL_ASSEMBLY);
  //Anything you want to do in the mean time? Put it here.
  MatAssemblyEnd(Cpetsc_,MAT_FINAL_ASSEMBLY);

  // Take just a little peek before continuing
  //MatView(Cpetsc_,PETSC_VIEWER_STDOUT_WORLD);

  return 0;
}

#else

// Do preallocation of petsc matrices

// Extract submatrix from the large stiffness matrix that contains A,C,C',B.
// This code patterned/taken after comprow_double.h.
// Spawned two versions. The one for the A submatrix checks for squareness.
template <class MTX, class VEC>
int PETScSolverDriverCore::InitAsubmatrix(const MTX& mat,
					  const VEC& rowmap, const VEC& colmap,
					  int &nrows, int &ncols)
{
  // Count how many rows and columns are in the target matrix
  int nr = 0;
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > nr) nr = rowmap[i];
    }
  nr++;
  nrows=nr;

  int nc = 0;
  for(typename VEC::size_type i=0; i<colmap.size(); i++)
    {
      if(colmap[i] > nc) nc = colmap[i];
    }
  nc++;
  ncols=nc;

  // Invert the rowmap to find out which rows of the source matrix
  // contribute to each row of the target.
  std::vector<std::list<int> > invrowmap(nr);
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > -1)
	{
	  invrowmap[rowmap[i]].push_front(i);
	}
    }

  //int nz = 0;			// non-zeros found so far

  if(nr!=nc)//check for squareness
    return -1;

  unsigned int maxnnz=0;

  // First determine the maximum nnz (number of nonzeros in a row) to be passed to MatCreateMPIAIJ

  // loop over rows of the target matrix
  for(int i=0; i<nr; i++)
    {
      // make a list of which columns appear in this row
      std::list<CSRRowEntry> cols;	// doubly linked list
      // loop over source rows that contribute to this target row
      for(std::list<int>::const_iterator isrc=invrowmap[i].begin();
	  isrc != invrowmap[i].end(); ++isrc)
	{
	  // loop over entries in source row
	  int srcrow = *isrc;
	  for(typename MTX::const_iterator ij=mat.begin(srcrow);
	      ij < mat.end(srcrow); ++ij)
	    {
	      int j = colmap[ij.col()];
	      if(j >= 0) {	// is this column being used?
		// has this column already been found?
		bool found = false;
		for(std::list<CSRRowEntry>::iterator tj=cols.begin();
		    tj != cols.end() && !found; ++tj)
		  {
		    int targetcol = (*tj).col();
		    if(j == targetcol) {
		      (*tj) += *ij; // add to preexisting entry
		      found = true;
		    }
		    else if(j < targetcol) {
		      cols.insert(tj, CSRRowEntry(j, *ij)); // insert before tj
		      found = true;
		    }
		  } // end loop over target columns
		if(!found) {
		  cols.push_back(CSRRowEntry(j, *ij));	// insert at end
		}
	      } // this source column is used
	    } // loop over entries in source row
	}	// loop over source rows that contribute to this target row

      if(maxnnz<cols.size())
	maxnnz=cols.size();

    } // end i-loop over target rows

  PetscScalar S;
  int Istart,Iend;
#if 0
  MatCreate(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,nr,nc,&Apetsc_);
#else
  MatCreateMPIAIJ(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,nr,nc,
		  maxnnz,PETSC_NULL,maxnnz,PETSC_NULL,&Apetsc_);
#endif
  MatSetFromOptions(Apetsc_);
  MatGetOwnershipRange(Apetsc_,&Istart,&Iend);
  PetscPrintf(PETSC_COMM_WORLD,"maxnnz = %d, Istart = %d, Iend = %d\n",maxnnz,Istart,Iend);

  // Now set the petsc matrix values

  // loop over rows of the target matrix
  //  plus follow the petsc ownership range
  for(int i=Istart; i<Iend; i++)
  //for(int i=0; i<nr; i++)
    {
      // make a list of which columns appear in this row
      std::list<CSRRowEntry> cols;	// doubly linked list
      // loop over source rows that contribute to this target row
      for(std::list<int>::const_iterator isrc=invrowmap[i].begin();
	  isrc != invrowmap[i].end(); ++isrc)
	{
	  // loop over entries in source row
	  int srcrow = *isrc;
	  for(typename MTX::const_iterator ij=mat.begin(srcrow);
	      ij < mat.end(srcrow); ++ij)
	    {
	      int j = colmap[ij.col()];
	      if(j >= 0) {	// is this column being used?
		// has this column already been found?
		bool found = false;
		for(std::list<CSRRowEntry>::iterator tj=cols.begin();
		    tj != cols.end() && !found; ++tj)
		  {
		    int targetcol = (*tj).col();
		    if(j == targetcol) {
		      (*tj) += *ij; // add to preexisting entry
		      found = true;
		    }
		    else if(j < targetcol) {
		      cols.insert(tj, CSRRowEntry(j, *ij)); // insert before tj
		      found = true;
		    }
		  } // end loop over target columns
		if(!found) {
		  cols.push_back(CSRRowEntry(j, *ij));	// insert at end
		}
	      } // this source column is used
	    } // loop over entries in source row
	}	// loop over source rows that contribute to this target row

      // copy data into target matrix
      for(std::list<CSRRowEntry>::const_iterator tj=cols.begin();
	  tj != cols.end(); ++tj)
	{
	  int j=(*tj).col();
	  S=(*tj).val();
	  MatSetValues(Apetsc_,1,&i,1,&j,&S,INSERT_VALUES);
	}

    } // end i-loop over target rows

  MatAssemblyBegin(Apetsc_,MAT_FINAL_ASSEMBLY);
  //Anything you want to do in the mean time? Put it here.
  MatAssemblyEnd(Apetsc_,MAT_FINAL_ASSEMBLY);

  // Take just a little peek before continuing
  //MatView(Apetsc_,PETSC_VIEWER_STDOUT_WORLD);

  return 0;
}

template <class MTX, class VEC>
int PETScSolverDriverCore::InitCsubmatrix(const MTX& mat,
					  const VEC& rowmap, const VEC& colmap,
					  int &nrows, int &ncols)
{
  // Count how many rows and columns are in the target matrix
  int nr = 0;
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > nr) nr = rowmap[i];
    }
  nr++;
  nrows=nr;

  int nc = 0;
  for(typename VEC::size_type i=0; i<colmap.size(); i++)
    {
      if(colmap[i] > nc) nc = colmap[i];
    }
  nc++;
  ncols=nc;

  // Invert the rowmap to find out which rows of the source matrix
  // contribute to each row of the target.
  std::vector<std::list<int> > invrowmap(nr);
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > -1)
	{
	  invrowmap[rowmap[i]].push_front(i);
	}
    }

  //int nz = 0;			// non-zeros found so far

  unsigned int maxnnz=0;

  // First determine the maximum nnz (number of nonzeros in a row) to be passed to MatCreateMPIAIJ

  // loop over rows of the target matrix
  for(int i=0; i<nr; i++)
    {
      // make a list of which columns appear in this row
      std::list<CSRRowEntry> cols;	// doubly linked list
      // loop over source rows that contribute to this target row
      for(std::list<int>::const_iterator isrc=invrowmap[i].begin();
	  isrc != invrowmap[i].end(); ++isrc)
	{
	  // loop over entries in source row
	  int srcrow = *isrc;
	  for(typename MTX::const_iterator ij=mat.begin(srcrow);
	      ij < mat.end(srcrow); ++ij)
	    {
	      int j = colmap[ij.col()];
	      if(j >= 0) {	// is this column being used?
		// has this column already been found?
		bool found = false;
		for(std::list<CSRRowEntry>::iterator tj=cols.begin();
		    tj != cols.end() && !found; ++tj)
		  {
		    int targetcol = (*tj).col();
		    if(j == targetcol) {
		      (*tj) += *ij; // add to preexisting entry
		      found = true;
		    }
		    else if(j < targetcol) {
		      cols.insert(tj, CSRRowEntry(j, *ij)); // insert before tj
		      found = true;
		    }
		  } // end loop over target columns
		if(!found) {
		  cols.push_back(CSRRowEntry(j, *ij));	// insert at end
		}
	      } // this source column is used
	    } // loop over entries in source row
	}	// loop over source rows that contribute to this target row

      if(maxnnz<cols.size())
	maxnnz=cols.size();

    } // end i-loop over target rows

  PetscScalar S;
  int Istart,Iend;
  MatCreateMPIAIJ(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,nr,nc,
		  maxnnz,PETSC_NULL,maxnnz,PETSC_NULL,&Cpetsc_);
  MatSetFromOptions(Cpetsc_);
  MatGetOwnershipRange(Cpetsc_,&Istart,&Iend);
  PetscPrintf(PETSC_COMM_WORLD,"maxnnz = %d, Istart = %d, Iend = %d\n",maxnnz,Istart,Iend);

  // Now set the petsc matrix values

  // loop over rows of the target matrix
  //  plus follow the petsc ownership range
  for(int i=Istart; i<Iend; i++)
  //for(int i=0; i<nr; i++)
    {
      // make a list of which columns appear in this row
      std::list<CSRRowEntry> cols;	// doubly linked list
      // loop over source rows that contribute to this target row
      for(std::list<int>::const_iterator isrc=invrowmap[i].begin();
	  isrc != invrowmap[i].end(); ++isrc)
	{
	  // loop over entries in source row
	  int srcrow = *isrc;
	  for(typename MTX::const_iterator ij=mat.begin(srcrow);
	      ij < mat.end(srcrow); ++ij)
	    {
	      int j = colmap[ij.col()];
	      if(j >= 0) {	// is this column being used?
		// has this column already been found?
		bool found = false;
		for(std::list<CSRRowEntry>::iterator tj=cols.begin();
		    tj != cols.end() && !found; ++tj)
		  {
		    int targetcol = (*tj).col();
		    if(j == targetcol) {
		      (*tj) += *ij; // add to preexisting entry
		      found = true;
		    }
		    else if(j < targetcol) {
		      cols.insert(tj, CSRRowEntry(j, *ij)); // insert before tj
		      found = true;
		    }
		  } // end loop over target columns
		if(!found) {
		  cols.push_back(CSRRowEntry(j, *ij));	// insert at end
		}
	      } // this source column is used
	    } // loop over entries in source row
	}	// loop over source rows that contribute to this target row

      // copy data into target matrix
      for(std::list<CSRRowEntry>::const_iterator tj=cols.begin();
	  tj != cols.end(); ++tj)
	{
	  int j=(*tj).col();
	  S=(*tj).val();
	  MatSetValues(Cpetsc_,1,&i,1,&j,&S,INSERT_VALUES);
	}

    } // end i-loop over target rows

  MatAssemblyBegin(Cpetsc_,MAT_FINAL_ASSEMBLY);
  //Anything you want to do in the mean time? Put it here.
  MatAssemblyEnd(Cpetsc_,MAT_FINAL_ASSEMBLY);

  // Take just a little peek before continuing
  //MatView(Cpetsc_,PETSC_VIEWER_STDOUT_WORLD);

  return 0;
}

#endif


//
// for real parallel stuff
//

#ifdef HAVE_MPI

template <class MTX, class VEC>
int PETScSolverDriverCore::InitAsubmatrix_parallel(const MTX& mat,
						   const VEC& rowmap, const VEC& colmap,
						   int nr, int nc)
{
  // Invert the rowmap to find out which rows of the source matrix
  // contribute to each row of the target.
  std::vector<std::list<int> > invrowmap(nr);
  for(typename VEC::size_type i=0; i<rowmap.size(); i++)
    {
      if(rowmap[i] > -1)
	{
	  invrowmap[rowmap[i]].push_front(i);
	}
    }

  unsigned int maxnnz=0;

  // First determine the maximum nnz (number of nonzeros in a row) to be passed to MatCreateMPIAIJ

  // loop over rows of the target matrix
  for(int i=0; i<nr; i++)
    {
      // make a list of which columns appear in this row
      std::list<CSRRowEntry> cols;	// doubly linked list
      // loop over source rows that contribute to this target row
      for(std::list<int>::const_iterator isrc=invrowmap[i].begin();
	  isrc != invrowmap[i].end(); ++isrc)
	{
	  // loop over entries in source row
	  int srcrow = *isrc;
	  for(typename MTX::const_iterator ij=mat.begin(srcrow);
	      ij < mat.end(srcrow); ++ij)
	    {
	      int j = colmap[ij.col()];
	      if(j >= 0) {	// is this column being used?
		// has this column already been found?
		bool found = false;
		for(std::list<CSRRowEntry>::iterator tj=cols.begin();
		    tj != cols.end() && !found; ++tj)
		  {
		    int targetcol = (*tj).col();
		    if(j == targetcol) {
		      (*tj) += *ij; // add to preexisting entry
		      found = true;
		    }
		    else if(j < targetcol) {
		      cols.insert(tj, CSRRowEntry(j, *ij)); // insert before tj
		      found = true;
		    }
		  } // end loop over target columns
		if(!found) {
		  cols.push_back(CSRRowEntry(j, *ij));	// insert at end
		}
	      } // this source column is used
	    } // loop over entries in source row
	}	// loop over source rows that contribute to this target row

      if(maxnnz<cols.size())
	maxnnz=cols.size();

    } // end i-loop over target rows

  PetscScalar S;
  int Istart,Iend;
#if 0
  MatCreate(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,nr,nc,&Apetsc_);
#else
  MatCreateMPIAIJ(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,nr,nc,
		  maxnnz,PETSC_NULL,maxnnz,PETSC_NULL,&Apetsc_);
#endif
  MatSetFromOptions(Apetsc_);
  MatGetOwnershipRange(Apetsc_,&Istart,&Iend);
  PetscPrintf(PETSC_COMM_WORLD,"maxnnz = %d, Istart = %d, Iend = %d\n",maxnnz,Istart,Iend);

  // Now set the petsc matrix values

  // loop over rows of the target matrix
  for(int i=0; i<nr; i++)
    {
      // make a list of which columns appear in this row
      std::list<CSRRowEntry> cols;	// doubly linked list
      // loop over source rows that contribute to this target row
      for(std::list<int>::const_iterator isrc=invrowmap[i].begin();
	  isrc != invrowmap[i].end(); ++isrc)
	{
	  // loop over entries in source row
	  int srcrow = *isrc;
	  for(typename MTX::const_iterator ij=mat.begin(srcrow);
	      ij < mat.end(srcrow); ++ij)
	    {
	      int j = colmap[ij.col()];
	      if(j >= 0) {	// is this column being used?
		// has this column already been found?
		bool found = false;
		for(std::list<CSRRowEntry>::iterator tj=cols.begin();
		    tj != cols.end() && !found; ++tj)
		  {
		    int targetcol = (*tj).col();
		    if(j == targetcol) {
		      (*tj) += *ij; // add to preexisting entry
		      found = true;
		    }
		    else if(j < targetcol) {
		      cols.insert(tj, CSRRowEntry(j, *ij)); // insert before tj
		      found = true;
		    }
		  } // end loop over target columns
		if(!found) {
		  cols.push_back(CSRRowEntry(j, *ij));	// insert at end
		}
	      } // this source column is used
	    } // loop over entries in source row
	}	// loop over source rows that contribute to this target row

      // copy data into target matrix
      for(std::list<CSRRowEntry>::const_iterator tj=cols.begin();
	  tj != cols.end(); ++tj)
	{
	  int j=(*tj).col();
	  S=(*tj).val();
	  MatSetValues(Apetsc_,1,&i,1,&j,&S,ADD_VALUES);
	}

    } // end i-loop over target rows

  MatAssemblyBegin(Apetsc_,MAT_FINAL_ASSEMBLY);
  //Anything you want to do in the mean time? Put it here.
  MatAssemblyEnd(Apetsc_,MAT_FINAL_ASSEMBLY);

  // Take just a little peek before continuing
  //MatView(Apetsc_,PETSC_VIEWER_STDOUT_WORLD);

  return 0;
}

void PETScSolverDriverCore::precompute_parallel()
{
  RWLock * rwlock = subproblem->mesh->get_rwlock();
  rwlock->read_acquire(); //acquire read lock

#if 1
  //This one does not create a CSRmatrix for A

  CSRmatrix * C=0;

  try
    {
      int n, m;

      n=0;
      for(std::vector<int>::size_type i=0; i<subproblem->indepeqnmap.size();i++)
	{
	  if(n<subproblem->indepeqnmap[i])
	    n=subproblem->indepeqnmap[i];
	}
      n++;

      C = new CSRmatrix (subproblem->Cmatrix());
      m = C->ncols();

      if (!x)
	{
	  x = new VECTOR_D (n, 0.0);
	}
      x->clear();
      subproblem->get_unknowns(*x, subproblem->freedofmap);

      if (!rhs)
	{
	  rhs = new VECTOR_D (n, 0.0);
	}
      rhs->clear();
      subproblem->get_rhs(*rhs, subproblem->indepeqnmap);

      if (!xp)
	{
	  xp = new VECTOR_D (m, 0.0);
	}
      xp->clear();
      subproblem->get_unknowns(*xp, subproblem->fixeddofmap);
      *rhs -= (*C) * (*xp);

      int dim=subproblem->m_combinedmatrixdim;

      //Report the stiffness matrix dim by filling nrowsA and ncolsA
      this->nrowsA=dim;
      this->ncolsA=dim;

      InitAsubmatrix_parallel((subproblem->linearsystem).get_stiffness(),
			      subproblem->m_precombined_indepeqnmap,
			      subproblem->m_precombined_freedofmap,
			      dim,dim);

      //Map the rhs vector onto the rows of the parallel stiffness matrix
      VecCreate(PETSC_COMM_WORLD,&xpetsc_);
      VecSetSizes(xpetsc_,PETSC_DECIDE,dim);
      VecSetFromOptions(xpetsc_);
      VecDuplicate(xpetsc_,&rhspetsc_);

      PetscScalar S;
      for(std::vector<int>::size_type j=0;j<subproblem->freedofmap.size();j++)
	{
	  int icol=subproblem->freedofmap[j];
	  int icolg=subproblem->m_precombined_freedofmap[j];
	  if(icol!=-1)
	    {
	      if(icolg==-1)
		{
		  std::cerr << "*********** TROUBLE rhs mapping *************************\n";
		}
	      else
		{
		  S=(*rhs)(icol);
		  VecSetValues(rhspetsc_,1,&icolg,&S,ADD_VALUES);
		}
	    }
	}

      VecAssemblyBegin(rhspetsc_);
      //Anything you want to do in the mean time? Put it here.
      VecAssemblyEnd(rhspetsc_);

      // Take just a little peek before continuing
      MatView(Apetsc_,PETSC_VIEWER_STDOUT_WORLD);

      // Take a peek
      VecView(rhspetsc_,PETSC_VIEWER_STDOUT_WORLD);

      if(C)
	delete C;

    } //end of try block
  catch(...) //guarantee that lock will be released if ANY exception is raised
    {
      if(C)
	delete C;

      //std::cerr << "releasing the lock in catch" << std::endl;
      rwlock->read_release(); 
      throw;
    }

#endif
#if 0
  CSRmatrix * A;// A and C are temporary
  CSRmatrix * C;

  try
    {
      int n, m;
      A = new CSRmatrix (subproblem->Amatrix());

      nrowsA = n = A->nrows();

      ncolsA = A->ncols();
      if(n != A->ncols())
	throw ErrSetupError("Local stiffness matrix is not square! nrows="
			    + to_string(n) + ", ncols="
			    + to_string(A->ncols()));

      C = new CSRmatrix (subproblem->Cmatrix());
      m = C->ncols();

      if (!x)
	{
	  x = new VECTOR_D (n, 0.0);
	}
      x->clear();
      subproblem->get_unknowns(*x, subproblem->freedofmap);

      if (!rhs)
	{
	  rhs = new VECTOR_D (n, 0.0);
	}
      rhs->clear();
      subproblem->get_rhs(*rhs, subproblem->indepeqnmap);

      if (!xp)
	{
	  xp = new VECTOR_D (m, 0.0);
	}
      xp->clear();
      subproblem->get_unknowns(*xp, subproblem->fixeddofmap);
      *rhs -= (*C) * (*xp);

      //
      // Test parallel stiffness matrix construction
      // Do the obvious thing, then optimize later
      //
      int dim=subproblem->m_combinedmatrixdim;

      //Map the rhs vector onto the rows of the parallel stiffness matrix
      VecCreate(PETSC_COMM_WORLD,&xpetsc_);
      VecSetSizes(xpetsc_,PETSC_DECIDE,dim);
      VecSetFromOptions(xpetsc_);
      VecDuplicate(xpetsc_,&rhspetsc_);

      PetscScalar S;

      int Istart,Iend;
      int maxnnz=9;//femesh->m_precombined_eqnsize;//Make a better estimate later
      //Now create the global stiffness matrix
      MatCreateMPIAIJ(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,dim,dim,
		      maxnnz,PETSC_NULL,maxnnz,PETSC_NULL,&Apetsc_);
      MatSetFromOptions(Apetsc_);
      MatGetOwnershipRange(Apetsc_,&Istart,&Iend);
      PetscPrintf(PETSC_COMM_WORLD,"maxnnz = %d, Istart = %d, Iend = %d\n",maxnnz,Istart,Iend);

      //Make a brute-force mapping and copy
      const CSRmatrix Aref=*A;
      for(std::vector<int>::size_type j=0;j<subproblem->freedofmap.size();j++)
	{
	  int icol=subproblem->freedofmap[j];
	  int icolg=subproblem->m_precombined_freedofmap[j];
	  if(icol!=-1)
	    {
	      if(icolg==-1)
		{
		  std::cerr << "*********** TROUBLE rhs mapping *************************\n";
		}
	      else
		{
		  S=(*rhs)(icol);
		  VecSetValues(rhspetsc_,1,&icolg,&S,ADD_VALUES);

		  // This job is done by InitAsubmatrix_parallel
		  for(std::vector<int>::size_type i=0;i<subproblem->indepeqnmap.size();i++)
		    {
		      int irow=subproblem->indepeqnmap[i];
		      if(irow != -1)
			{
			  int irowg=subproblem->m_precombined_indepeqnmap[i];
			  if(irowg == -1)
			    {
			      std::cerr << "*********** TROUBLE matrix mapping **************************\n";
			    }
			  else
			    {
			      //std::cerr << "A(" << irow << "," << icol << ")=" << Aref(irow,icol) << " " << " goes to " << "(" << irowg << "," << icolg << ")\n";
			      S=Aref(irow,icol);
			      // Map local stiffness matrix elements to the global/combined stiffness matrix
			      MatSetValues(Apetsc_,1,&irowg,1,&icolg,&S,ADD_VALUES);
			    }
			}
		    }

		}
	    }
	}

      MatAssemblyBegin(Apetsc_,MAT_FINAL_ASSEMBLY);
      //Anything you want to do in the mean time? Put it here.
      MatAssemblyEnd(Apetsc_,MAT_FINAL_ASSEMBLY);

      VecAssemblyBegin(rhspetsc_);
      //Anything you want to do in the mean time? Put it here.
      VecAssemblyEnd(rhspetsc_);

      // Take just a little peek before continuing
      MatView(Apetsc_,PETSC_VIEWER_STDOUT_WORLD);

      // Take a peek
      VecView(rhspetsc_,PETSC_VIEWER_STDOUT_WORLD);

      delete A;
      delete C;

    } //end of try block
  catch(...) //guarantee that lock will be released if ANY exception is raised
    {
      delete A;
      delete C;

      //std::cerr << "releasing the lock in catch" << std::endl;
      rwlock->read_release(); 
      throw;
    }

#endif

  //std::cerr << "releasing the lock while exiting the function " << std::endl;
  rwlock->read_release();
}
#endif
