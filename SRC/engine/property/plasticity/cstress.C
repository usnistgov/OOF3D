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
#include "engine/property/plasticity/cstress.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/mastercoord.h"
#include "engine/symmmatrix3.h"
#include "engine/smallmatrix3.h"

OutputVal *POInitCauchyStress::operator()(const PropertyOutput *po,
					  const FEMesh *mesh,
					  const Element *element,
					  const MasterCoord &pos) const
{
  SymmMatrix3 *cstress = new SymmMatrix3();
  std::cerr << "POInitCauchyStress::operator()" << std::endl;
  // Get the element's plastic data object and retrieve the
  // stuff we want from it.

  // For evaluation points which are not themselves gausspoints,
  // figure out how we want to interpolate.
  
  return cstress;
  
}
