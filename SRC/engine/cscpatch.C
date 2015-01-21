// -*- C++ -*-
// $RCSfile: cscpatch.C,v $
// $Revision: 1.18.10.4 $
// $Author: langer $
// $Date: 2014/12/14 22:49:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <iostream>
#include "common/doublevec.h"
#include "common/printvec.h"
#include "common/vectormath.h"
#include "common/coord.h"
#include "engine/cscpatch.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/femesh.h"
#include "engine/flux.h"
#include "engine/node.h"
#include "engine/ooferror.h"
#include "engine/outputval.h"


// CSCPatches are created in CSubProblem::add_scpatch().  There's one
// CSCPatch for each assembly_node.

// CSCPatch constructor.
CSCPatch::CSCPatch(CSubProblem *subp, const int order, const Material *mat,
		   const std::vector<int> *elems,
		   const std::vector<int> *nds,
		   const int qualified)
  : subproblem(subp),
    femesh_order_(order),
    material_(mat),
    qualified_(qualified),
    Amtx((unsigned) 0)
{
  // adding elements
  for(std::vector<int>::size_type i=0; i<elems->size(); i++)
    elements.push_back(subproblem->mesh->getElement((*elems)[i]));
  // adding nodes
  for(std::vector<int>::size_type i=0; i<nds->size(); i++)
    nodes.push_back(subproblem->mesh->getNode((*nds)[i]));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// // CSCPatch Copy constructor.
// CSCPatch::CSCPatch(const CSCPatch &other)
//   : subproblem(other.subproblem),
//     femesh_order_(other.femesh_order_),
//     material_(other.material_),
//     qualified_(other.qualified_)
// {
//   std::cerr << "CSCPatch copy constructor!" << std::endl;
//   // adding elements
//   for(std::vector<Element*>::size_type i=0; i<other.elements.size(); i++)
//     elements.push_back(other.elements[i]);
//   // adding nodes
//   for(std::vector<Node*>::size_type i=0; i<other.nodes.size(); i++)
//     nodes.push_back(other.nodes[i]);
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// CSCPatch destructor
CSCPatch::~CSCPatch()
{
  // deleting new'd SmallMatrix's of "coefficients".
  for(std::vector<SmallMatrix*>::size_type i=0; i<coefficients.size(); i++)
    delete coefficients[i];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::vector<int> *CSCPatch::get_elements() const {
  std::vector<int> *elems = new std::vector<int>;
  for(std::vector<Element*>::size_type i=0; i<elements.size(); i++)
    elems->push_back(elements[i]->get_index());
  return elems;
}


std::vector<int> *CSCPatch::get_nodes() const {
  std::vector<int> *nds = new std::vector<int>;
  for(std::vector<Node*>::size_type i=0; i<nodes.size(); i++)
    nds->push_back(nodes[i]->index());
  return nds;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Basis functions
double CSCPatch::basis(int i, const Coord &pos)
{
  // As cubic element types available in OOF2, these basis functions
  // have to be expanded.
  double x = pos[0];
  double y = pos[1];
  if (i==0)
    return 1.;
  if (i==1)
    return x;
  if (i==2)
    return y;
  if (i==3)
    return x*y;
  if (i==4)
    return x*x;
  if (i==5)
    return y*y;
  if (i==6)
    return x*x*y;
  if (i==7)
    return x*y*y;
  if (i==8)
    return x*x*y*y;
  if (i==9)
    return x*x*x;
  if (i==10)
    return y*y*y;
  if (i==11)
    return x*x*x*y;
  if (i==12)
    return x*y*y*y;
  if (i==13)
    return x*x*x*y*y;
  if (i==14)
    return x*x*y*y*y;
  if (i==15)
    return x*x*x*y*y*y;
  throw ErrBadIndex(i, __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int CSCPatch::nsamples()
{
  int nsamples = 0;
  for(std::vector<Element*>::size_type i=0; i<elements.size(); i++)
    nsamples += elements[i]->nSCpoints();
  return nsamples;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int CSCPatch::get_size()  // setting the size of Amtx.
{
  int ns = nsamples();
  if(femesh_order_ == 1) {  // available size: 3, 4, 6, 9, 16
    if(ns < 4)
      return 3;
    else if(ns < 6)
      return 4;
    else if(ns < 9)
      return 6;
    else if(ns < 16)
      return 9;
    else
      return 16;
  }
  else {  // available size: 6, 9, 16
    if(ns < 9)
      return 6;
    else if(ns < 16)
      return 9;
    else
      return 16;
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSCPatch::recover_fluxes(const std::vector<Flux*>& allfluxes)
{
  // RCL: What this does is it gets a least squares fit of P.a to
  // the fluxes at the superconvergent (or high accuracy) sampling points
  // 'a' is a vector of unknown parameters in the expansion P.a where P
  // is a polynomial basis

  // Equation to solve:
  // Amtx . a = b
  // Amtx = sum (pT^p)
  // b = sum (pT . flux)
  // This needs to be solved for each component of the flux.
  // Oh wait ... it's not.
  // With B = [b0, b1, ... bn], it could be done in one shot.
  std::vector<SmallMatrix*> stored_pT;
  std::vector<MasterCoord> stored_mscp; // stored SC points (MasterCoord)
  std::vector<int> elmap;  // matching element(vector indices) map

  int size_ = get_size();  // determine the size of Amtx
  Amtx.resize(size_, size_);
  Amtx.clear();  // initialize with 0s.
  
  // evaluating "Amtx", which will be constant for all flux components.
  for(std::vector<Element*>::size_type i=0; i<elements.size(); i++) {
    for(int j=0; j<elements[i]->nSCpoints(); j++) {
      const MasterCoord &master = elements[i]->getMasterSCpoint(j);
      const Coord position = elements[i]->from_master(master);
      stored_mscp.push_back(master);
      elmap.push_back(i);
      // eval & store Amtx, pT.
      eval_Amtx(size_, position, stored_pT);
    }
  }

  // iterating over all fluxes.
  for(std::vector<Flux*>::size_type i=0; i<allfluxes.size(); i++) {
    solve(size_, allfluxes[i], elmap, stored_mscp, stored_pT);
    // time to actually recover fluxes  
    for(std::vector<Node*>::size_type j=0; j<nodes.size(); j++) {
      recover_this_flux(size_, nodes[j], i, allfluxes[i]);
    }
  }

  // deleting new'd SmallMatrix's of "stored_pT"
  for(std::vector<SmallMatrix*>::size_type i=0; i<stored_pT.size(); i++)
    delete stored_pT[i];

}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSCPatch::eval_Amtx(const int &size_, const Coord &pos,
			 std::vector<SmallMatrix*> &stored_pT)
{
  SmallMatrix *pT = new SmallMatrix(size_, 1);
  SmallMatrix p(1, size_);
  for(int i=0; i<size_; i++) {
    (*pT)(i,0) = basis(i, pos);
    p(0,i) = basis(i, pos);
  }
  Amtx += (*pT)*p;
  stored_pT.push_back(pT);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO 3.1: Amtx is badly conditioned, and so the solutions can vary
// widely from machine to machine.  This means that ZZ AMR (as
// implemented here) is unreliable.  The
// Adaptive_SubProblem_Refinement test in TEST/mesh_modify_test.py is
// commented out, because it gives different results on an Intel Mac,
// and two different Linux boxes.  If the commented-out debugging
// lines in CSCPatch::solve are uncommented, you'll see that the Amtx
// and rhs (input Bmtx) are the same, but the solutions (output Bmtx)
// are different.

void CSCPatch::solve(const int &size_, const Flux *fluks,
		     std::vector<int> &elmap,
		     std::vector<MasterCoord> &stored_mscp,
		     std::vector<SmallMatrix*> &stored_pT)
{
  // evaluating flux and store.
  std::vector<DoubleVec*> stored_flux;
  for(std::vector<MasterCoord>::size_type i=0; i<stored_mscp.size(); i++) {
    //TODO OPT: Should fluks->evaluate accept a subproblem instead of a
    //mesh object for its first argument?
    stored_flux.push_back(fluks->evaluate(subproblem->mesh, elements[elmap[i]],
					  stored_mscp[i]));
  }
  SmallMatrix Amtx_copy(Amtx);  // Amtx is damaged when solving.
  // B = [b0, b1, ..., bn] -- n: Flux->ndof(), basically a collection of b's.
  SmallMatrix *Bmtx = new SmallMatrix(size_, fluks->ndof());
  Bmtx->clear();
  // Filling Bmtx with numbers.
  for(int n=0; n<fluks->ndof(); n++) {
    for(std::vector<SmallMatrix*>::size_type i=0; i<stored_pT.size(); i++) {
      SmallMatrix *ptv = stored_pT[i];
      double component = (*(stored_flux[i]))[n];
      for(int j=0; j<size_; j++)
	(*Bmtx)(j,n) += (*ptv)(j,0) * component;
    }
  }
//   std::cerr << "CSCPatch::solve: Amtx=" << Amtx << std::endl;
//   std::cerr << "CSCPatch::solve input Bmtx=" << *Bmtx << std::endl;
  Amtx_copy.solve(*Bmtx);  // passed-in "Bmtx" is the solution.
//   std::cerr << "CSCPatch::solve output Bmtx=" << *Bmtx << std::endl;
  coefficients.push_back(Bmtx);  // stores the solution

  // deleting new'd DoubleVecs of "stored_flux"
  for(std::vector<DoubleVec*>::size_type i=0; i<stored_flux.size(); i++)
    delete stored_flux[i];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSCPatch::recover_this_flux(const int &size_, const Node *nd,
				 const int &coef_index, const Flux *fluks)
{
  // values of the recovered flux
  DoubleVec *fvalues = new DoubleVec(fluks->ndof(), 0.0);
  const Coord pos = nd->position();
  SmallMatrix *bmtx = coefficients[coef_index];
  for(int i=0; i<fluks->ndof(); i++)
    for (int j=0; j<size_; j++)
      (*fvalues)[i] += basis(j, pos) * (*bmtx)(j, i);
  subproblem->add_this_flux(material_, fluks, nd, fvalues);
}
