// -*- C++ -*-
// $RCSfile: celectricfield.C,v $
// $Revision: 1.8.10.2 $
// $Author: fyc $
// $Date: 2014/07/22 21:07:11 $

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
#include "engine/celectricfield.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/mastercoord.h"
#include "engine/outputval.h"

void findElectricField(const FEMesh *mesh, const Element *element,
		       const MasterPosition &pos, DoubleVec &efield)
{
  static ScalarField *voltage =
    dynamic_cast<ScalarField*>(Field::getField("Voltage"));;

  for(SpaceIndex j=0; j<DIM; ++j) {
    OutputValue vderiv = element->outputFieldDeriv(mesh, *voltage, &j, pos);
    efield[j] = -vderiv[0];
  }
#if DIM==2
  static Field *voltage_z = voltage->out_of_plane();
  bool inplane = voltage->in_plane(mesh);
  if(!inplane) {
    OutputValue vz = element->outputField(mesh, *voltage_z, pos);
    efield[2] = -vz[0];
  }
#endif // DIM==2
}


