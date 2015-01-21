// -*- C++ -*-
// $RCSfile: freedom.C,v $
// $Revision: 1.15.6.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:25 $

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
#include "common/tostring.h"
#include "engine/femesh.h"
#include "engine/freedom.h"
#include <string>

DegreeOfFreedom::DegreeOfFreedom(int ind)
  : index_(ind)
{
}

// Making DegreeOfFreedom::value inline in freedom.h causes horrible
// #include loops.

double DegreeOfFreedom::value(const FEMesh *mesh) const {
  return (*mesh->dofvalues)[index_];
}

double &DegreeOfFreedom::value(FEMesh *mesh) const {
  return (*mesh->dofvalues)[index_];
}

void DegreeOfFreedom::setValue(const FEMesh *mesh, double newValue)
{
  (*mesh->dofvalues)[index_] = newValue;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const DegreeOfFreedom &dof) {
  return os << "[" << dof.dofindex() << "]";
}
