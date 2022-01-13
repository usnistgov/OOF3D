// -*- C++ -*-

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
#include "common/cleverptr.h"
#include "engine/largestrainoutput.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/mastercoord.h"
#include "engine/symmmatrix3.h"
#include "engine/smallmatrix3.h"

OutputVal *POInitLargeStrain::operator()(const PropertyOutput *po,
				      const FEMesh *mesh,
				      const Element *element,
				      const MasterCoord &pos) const
{
  SmallMatrix3 *deformation = new SmallMatrix3();
  std::cerr << "POInitLargeStrain::operator()" << std::endl;
  std::cerr << *deformation << std::endl;
  // See cstrain.C for the model for this.
  // Switch on the sub-type of the passed-in registered class
  // name by querying on po->getRegisteredParameterName("type"), and
  // populate the deformation in different ways, depending?
  // Or, for deformation, is there only one kind?

  
  ThreeVectorField *displacement = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));

  for (CleverPtr<ElementFuncNodeIterator> efi(element->funcnode_iterator());
       !(efi->end()); ++(*efi)) {
    OutputValue dval = displacement->newOutputValue();
    // Reference-state derivatives.
    double dshapedx = efi->dshapefunction(0,pos);
    double dshapedy = efi->dshapefunction(1,pos);
    double dshapedz = efi->dshapefunction(2,pos);
    
    // Vector value of the displacement at the node.
    dval += displacement->output(mesh, *efi);
    
    for (IteratorP ip = displacement->iterator(ALL_INDICES);
	 !ip.end(); ++ip) {
      int idx = ip.integer();
      // std::cerr << "Displacement component " << ip << " is " << dval[ip] << std::endl;
      (*deformation)(idx,0) += dval[ip]*dshapedx;
      (*deformation)(idx,1) += dval[ip]*dshapedy;
      (*deformation)(idx,2) += dval[ip]*dshapedz;
    }
  }

  (*deformation)(0,0) += 1.0;
  (*deformation)(1,1) += 1.0;
  (*deformation)(2,2) += 1.0;

  SymmMatrix3 *cmatrix = new SymmMatrix3();
  for(int i=0;i<3;++i)
    for(int j=0;j<=i;++j)
      for(int k=0;k<3;++k)
	(*cmatrix)(i,j) += (*deformation)(k,i)*(*deformation)(k,j);

  // Get the output type, and compute the relevant quantity.
  
  const std::string *outputtype = po->getRegisteredParamName("type");
  if (*outputtype=="Green Lagrange Strain") {
    SymmMatrix3 *glstrain = new SymmMatrix3();
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j) {
	(*glstrain)(i,j) = 0.5*( (*cmatrix)(i,j) - (i==j ? 1.0 : 0.0));
      }
    delete cmatrix;
    return glstrain;
  } 
  else {
    if (*outputtype=="Logarithmic Strain") {
      return cmatrix; // Place-holder, actually compute logarithm.
    }
    else {
      std::cerr << "Unknown large strain type." << std::endl;
    }
    
  } // Bottom of switching on types.
}


