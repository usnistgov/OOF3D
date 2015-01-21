// -*- C++ -*-
// $RCSfile: boundarycond.C,v $
// $Revision: 1.44.2.7 $
// $Author: langer $
// $Date: 2014/12/14 22:49:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/cleverptr.h"
#include "common/coord.h"
#include "common/printvec.h"
#include "common/trace.h"
#include "common/IO/oofcerr.h"
#include "engine/boundarycond.h"
#include "engine/edge.h"
#include "engine/edgeset.h"
#include "engine/element.h"
#include "engine/equation.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/fluxnormal.h"
#include "engine/gausspoint.h"
#include "engine/linearizedsystem.h"
#include "engine/nodalequation.h"
#include "engine/node.h"
#include "engine/sparsemat.h"
#include "engine/csubproblem.h"
#include <iostream>
#include <stdlib.h>
#include <unistd.h>

class Material;
class Element;



// FloatBCApp is a bit of a special case, it's the C implementation of
// the "apply" function from the Python FloatBC class.  It does the
// leg-work of changing the mapping lists so that they're
// many-to-not-quite-so-many, aggregating DOF's and nodal equations
// correctly.

// This function takes the targets for the map as inputs (named
// new<something>map).  The function is not called for the first dof
// of a floating set.  It changes the maps for the rest of the dofs in
// the set so that they refer to the mapped index of the first dof.

// "initprof" at this point is the value of the first evaluation 
// of the profile function.
void FloatBCApp::editmap(LinearizedSystem *linsys,
			 double val, FuncNode *node,
			 Field *field, int fcomp,
			 Equation *eqn, int eqcomp,
			 int newdofindex, int neweqnindex, int newderivindex,
			 double initprof)
{
  // newdofindex and neweqnindex are indices into the lists of DoFs
  // and NodalEquations used by a Subproblem.

  // Get a global column number for the dof.
  int doflistindex = linsys->getSubproblemDoFIndex(node, field, fcomp);
  // Ditto for the nodal equation's row number. 
  int ndqlistindex = linsys->getSubproblemEqnIndex(node, eqn, eqcomp);

  int derivindex = -1;
  if(newderivindex != -1) {
    derivindex = linsys->getSubproblemDoFIndex(node, field->time_derivative(),
					       fcomp); 
  }

  // LinearizedSystem::applyFloatBC modifies the level 2 maps (see
  // comments in linearizedsystem.h) so that the rows and columns
  // corresponding to the FloatBC's DoFs and equations are summed when
  // submatrices are extracted.
  linsys->applyFloatBC(doflistindex, newdofindex,
		       ndqlistindex, neweqnindex,
		       derivindex, newderivindex);

  profile_data[doflistindex] += val - initprof;
  // std::cerr << "FloatBCApp::editmap: profile_data[" << doflistindex
  // 	    << "] = " << profile_data[doflistindex] << std::endl;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Do the integration to apply a flux boundary conditon.
// The specified condition is in the form of a Python-callable
// object, which appears here as a PyObject*.

// Specified flux might vary in space, so there's a callback.
// What is actually applied is the normal component of the flux,
// which is a force density with the same dimensionality as the
// divergence of the flux. 

#if DIM==2

void NeumannBCApp::integrate(PyObject *wrapper, PyObject *pyfun, 
			     bool normal, double time) {
//   Trace("NeumannBCApp::integrate_");
  // Instance the iterator outside the "for" statement so that the
  // call to total_length is outside the loop.
  EdgeSetIterator bi = bdy->edge_iterator();
  double edgeset_length = bi.total_length();

  for(; !bi.end(); ++bi) {
    
    BoundaryEdge* ed = bi.edge();
    const Element *el = ed->el;

    if(subproblem->contains(el)) {
      int order = el->shapefun_degree();
    
      order+=3; // Add a small offset to the shapefunction order.
      // TODO OPT: Ultimately this should query the profile function for
      // its order somehow, but since the profile function is
      // user-specified, that's a bit tricky.
    
      double traversed_length = bi.traversed_length();
      double edge_length = ed->lab_length();
      for(EdgeGaussPoint egpt=ed->integrator(order); !egpt.end(); ++egpt) {
	double distance = traversed_length + edge_length*egpt.fraction();
	double edgeset_fraction = distance/edgeset_length;
	// Make the contribution to the RHS through the nodalequation.
	// Automatically calls the one with the correct Python
	// call-back wrapper.

	// Make the Python callback at the highest possible level,
	// outside as many loops as possible, because it's expensive.
	FluxNormal *flxnormal = flux->BCCallback(egpt.position(), 
						 time, 
						 egpt.normal(),
						 distance,
						 edgeset_fraction,
						 wrapper,
						 pyfun);
	// egpt.normal() is the normal at this point -- do the
	// rotation, if required.
	if (normal) 
	  flxnormal->transform(egpt.normal());
	// Flux::boundary_integral() calls
	// Equation::boundary_integral() which makes a contribution to
	// the force_bndy_rhs vector in the LinearizedSystem.
	flux->boundary_integral(subproblem, linearsystem, ed, egpt, flxnormal);
	delete flxnormal;
      }
    }
  }
}

#else // DIM==3

void NeumannBCApp::integrate(PyObject *wrapper, PyObject *pyfun, double time)
{
  // wrapper is the flux_locator function in bdycondition.py.
  // pyfun is the profile function.

  // TODO OPT: Why is wrapper passed as an argument to integrate(), and
  // not as a constructor argument?  Is it ever anything other than
  // flux_locator?
  for(CleverPtr<SubDimensionalIterator> fi(bdy->iterator()); !fi->end(); ++*fi)
    {
      Element *face = fi->part();
      if(face->allNodesAreInSubProblem(subproblem)) {
	int order = face->shapefun_degree();
	bool reversed = fi->reversed();
	// TODO OPT: Ultimately this should query the profile function for
	// its order somehow, but since the profile function is
	// user-specified, that's a bit tricky.
	order += 3;
	for(GaussPointIterator igpt=face->integrator(order);!igpt.end();++igpt)
	  {
	    GaussPoint gpt = igpt.gausspoint();
	    Coord normal = findNormal(face, gpt);
	    if(reversed) 
	      normal *= -1;
	    FluxNormal *flxnormal = flux->BCCallback(gpt.position(),
						     time,
						     normal,
						     wrapper,
						     pyfun);
	    flux->boundary_integral(subproblem, linearsystem, face, gpt,
				    flxnormal);
	    delete flxnormal;
	  }
      }
    }
}

#endif // DIM==3


void applyForceBC(CSubProblem *subproblem,
		  LinearizedSystem *ls,
		  Equation *equation, FuncNode *node,
		  int eqcomp, double val)
{
  // Asks the equation for the index corresponding to the current
  // component, then asks the mesh for that component of the
  // boundary_rhs vector, and subtracts val from it.
  int ndqlistindex = equation->nodaleqn(*node, eqcomp)->ndq_index();
  ls->insert_force_bndy_rhs(ndqlistindex, val); 
}

// TODO 3.1: PeriodicFlux boundary conditions.  The normal fluxes
// through two edges are constrained to be equal and opposite through
// the use of a Lagrange multiplier field.
