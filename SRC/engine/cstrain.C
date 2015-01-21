// -*- C++ -*-
// $RCSfile: cstrain.C,v $
// $Revision: 1.15.10.4 $
// $Author: fyc $
// $Date: 2014/07/22 21:07:17 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#include "common/doublevec.h"
#include "engine/cstrain.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/mastercoord.h"
#include "engine/symmmatrix.h"


// The following function adds the local geometrical strain at a given
// master position in the given element to the given SymmMatrix3.

void findGeometricStrain(const FEMesh *mesh, const Element *element,
			 const MasterPosition &pos, SymmMatrix3 *strain,
			 bool nonlinear)
{
  SmallMatrix dU(3); // dU(i,j) = du_i/dx_j 
  computeDisplacementGradient(mesh, element, pos, dU);

  // TODO OPT: Earlier versions of this routine had unrolled loops.
  // They could be unrolled again if necessary.
  for(SymTensorIterator ij; !ij.end(); ++ij) {
    int i = ij.row();
    int j = ij.col();
    (*strain)[ij] += 0.5*(dU(i,j) + dU(j,i));
  }

  if(nonlinear) {
    for(SymTensorIterator ij; !ij.end(); ++ij) {
      int i = ij.row();
      int j = ij.col();
      (*strain)[ij] += 
	0.5*(dU(0,i)*dU(0,j) + dU(1,i)*dU(1,j) + dU(2,i)*dU(2,j));
    }
  }
} // end of 'findGeometricStrain'

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO OPT: Create a non-symmetric 3x3 tensor OutputValue class and
// return it from this function, instead of passing in a SmallMatrix.

void computeDisplacementGradient(const FEMesh *mesh, const Element *element,
				 const MasterPosition &pt,
				 SmallMatrix &grad)
{
  // compute the matrix dU(i,j) = d/dx_j (u_i)

  static CompoundField *displacement =
    dynamic_cast<CompoundField*>(Field::getField("Displacement"));

  assert(grad.rows() == 3 && grad.cols() == 3);
  
  for(SpaceIndex j=0; j<DIM; ++j) { // loop over gradient components
    OutputValue oddisp = element->outputFieldDeriv(mesh, *displacement, &j, pt);
    // loop over field components
    for(IteratorP i=displacement->iterator(ALL_INDICES); !i.end(); ++i)
      grad(i.integer(), j) += oddisp[i];
  }

#if DIM==2
  if(!displacement->in_plane(mesh)) {
    Field *oop = displacement->out_of_plane();
    OutputValue oddispz = element->outputField(mesh, *oop, pt);
    for(IteratorP i=oop->iterator(ALL_INDICES); !i.end(); ++i)
      grad(i.integer(), 2) += oddispz[i]; 
  }
#endif // DIM==2
}

void computeDisplacement(const FEMesh *mesh, const Element *element,
			 const MasterPosition &pt,
			 DoubleVec &disp)
{
  static CompoundField *displacement =
    dynamic_cast<CompoundField*>(Field::getField("Displacement"));
  assert(disp.size() == 3);
  OutputValue odisp = element->outputField(mesh, *displacement, pt);
  for(IteratorP i=displacement->iterator(ALL_INDICES); !i.end(); ++i)
    disp[i.integer()] += odisp[i];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Initialize a PropertyOutput with the geometric strain.

OutputVal *POInitGeometricStrain::operator()(const PropertyOutput *po,
					     const FEMesh *mesh,
					     const Element *element,
					     const MasterCoord &pos) const
{
  SymmMatrix3 *strain = new SymmMatrix3();
  // Get the Python parameter that tells which Strain is being
  // computed. It's a RegisteredParameter.
  const std::string *straintype = po->getRegisteredParamName("type");
  if(*straintype == "Geometric" || *straintype == "Elastic") {
    findGeometricStrain(mesh, element, pos, strain, false);
  }
  else if(*straintype == "Nonlinear Geometric") {
    findGeometricStrain(mesh, element, pos, strain, true);
  }
  delete straintype;
  return strain;
};
