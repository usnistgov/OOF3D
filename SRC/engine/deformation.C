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
#include "engine/deformation.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/mastercoord.h"
#include "engine/smallmatrix3.h"


// For now, just build a zero matrix.

OutputVal *POInitDeformation::operator()(const PropertyOutput *po,
					 const FEMesh *mesh,
					 const Element *element,
					 const MasterCoord &pos) const
{
  SmallMatrix3 *deformation = new SmallMatrix3();
  // See cstrain.C for the model for this.
  // Switch on the sub-type of the passed-in registered class
  // name by querying on po->getRegisteredParameterName("type"), and
  // populate the deformation in different ways, depending?
  // Or, for deformation, is there only one kind?
  return deformation;
}
