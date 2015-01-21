// -*- C++ -*-
// $RCSfile: simpletension.C,v $
// $Revision: 1.3.10.2 $
// $Author: fyc $
// $Date: 2014/07/29 21:22:28 $

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
#include "common/doublevec.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/field.h"
#include "engine/linearizedsystem.h"
#include "engine/material.h"
#include "engine/node.h"
#include "engine/smallsystem.h"
#include "simpletension.h"

SimpleTension::SimpleTension(PyObject *reg, const std::string &nm,
			     double gamma_left, double gamma_right)
  : EqnProperty(nm,reg), _gamma_left(gamma_left), _gamma_right(gamma_right)
{
  delta_r = Coord(0,0);
}

int SimpleTension::integration_order(const CSubProblem*, 
				     const Element *el) const
{
  return 0;
}

// InterfaceElements can have split nodes.  The InterfaceElement class
// provides a get_nodelist2 function, which works similarly to the
// Element's get_nodelist() function.  TODO OPT: These should be
// iterators, almost certainly.


void SimpleTension::begin_element(const CSubProblem *pSubp, 
				  const Element *pElem) {
  
  FuncNode *n0,*nn;
  int nnodes = pElem->nnodes();
  // This is a bit strange, but non-edgements don't really have a
  // notion of a "first" or "last" node, so the generic tools don't
  // support it very well.
  int i=0;
  for(CleverPtr<ElementFuncNodeIterator> efi(pElem->funcnode_iterator());
      !efi->end(); ++*efi ) {
    if(i==0) { n0=efi->funcnode(); }
    if(i==(nnodes-1)) { nn=efi->funcnode(); }
    ++i;
  }
  delta_r = nn->position()-n0->position();
}

void SimpleTension::end_element(const CSubProblem* pSubp, const Element* pElem)
{}

void SimpleTension::cross_reference(Material* pMat)
{
  return;
}

void SimpleTension::post_process(CSubProblem* pSubp, 
				 const Element *pElem) const
{
}


void SimpleTension::force_value(const FEMesh *mesh, 
				const Element *element,
				const Equation *eqn, 
				const MasterPosition &pt,
				double time, SmallSystem *eqndata) const {

  int nnodes = element->nnodes();

  std::vector<Coord> u(nnodes);
  std::vector<double> dphi(nnodes);

  // TODO 3.1: Set disp in precompute().
  TwoVectorField *disp = 
    dynamic_cast<TwoVectorField*>(Field::getField("Displacement"));
  
  // Extract the displacement-field values at the nodes, and do the
  // shape-function derivative evaluations.

  // TODO MER: The non-point-dependent part of this (i.e. the "u" vector)
  // should be assembled in the begin_element routine, not here.

  int ndi=0;
  for(CleverPtr<ElementFuncNodeIterator> efi(element->funcnode_iterator());
      !efi->end(); ++*efi) {
    u[ndi].x = ((*disp)(efi->funcnode(),0))->value(mesh);
    u[ndi].y = ((*disp)(efi->funcnode(),1))->value(mesh);
    dphi[ndi] = efi->masterderiv(0,pt);
    ++ndi;
  }
  
  Coord dstrn(delta_r);
  for(int i=0;i<nnodes;++i) {
    dstrn.x += u[i].x*dphi[i];
    dstrn.y += u[i].y*dphi[i];
  }
  
  double normalization= 1.0/sqrt(dot(dstrn,dstrn));

}


void SimpleTension::force_deriv_matrix(const FEMesh *mesh, 
				       const Element *element,
				       const Equation *eqn, 
				       const ElementFuncNodeIterator&,
				       const MasterPosition &pt,
				       double time, 
				       SmallSystem *eqndata) const {
  std::cerr << "Force deriv called." << std::endl;
}
