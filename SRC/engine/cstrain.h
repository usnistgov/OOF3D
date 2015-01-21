// -*- C++ -*-
// $RCSfile: cstrain.h,v $
// $Revision: 1.8.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:39 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#ifndef CSTRAIN_H
#define CSTRAIN_H

class DoubleVec;
class Element;
class FEMesh;
class MasterPosition;
class SmallMatrix;
class SymmMatrix3;

#include "engine/IO/propertyoutput.h"


void findGeometricStrain(const FEMesh*, const Element*,
			 const MasterPosition&, SymmMatrix3*, bool);

void computeDisplacementGradient(const FEMesh*, const Element*,
				 const MasterPosition&, SmallMatrix&);

void computeDisplacement(const FEMesh*, const Element*,
			 const MasterPosition&, DoubleVec&);

class POInitGeometricStrain : public SymmMatrix3PropertyOutputInit {
public:
  virtual OutputVal *operator()(const PropertyOutput*,
				const FEMesh*, const Element*,
				const MasterCoord&) const;
};

#endif // CSTRAIN_H
