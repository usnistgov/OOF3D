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

#ifndef GLSTRAIN_H
#define GLSTRAIN_H

class Element;
class FEMesh;
class MasterPosition;
class SymmMatrix;
class SymmMatrix3;

#include "engine/IO/propertyoutput.h"

class POInitGLStrain : public SymmMatrix3PropertyOutputInit {
public:
  virtual OutputVal *operator()(const PropertyOutput*,
				const FEMesh*,
				const Element*,
				const MasterCoord&) const;
};

#endif // GLSTRAIN_H
