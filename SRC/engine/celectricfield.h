// -*- C++ -*-
// $RCSfile: celectricfield.h,v $
// $Revision: 1.5.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CELECTRICFIELD_H
#define CELECTRICFIELD_H

class Element;
class FEMesh;
class MasterPosition;

#include "common/doublevec.h"
#include "engine/IO/propertyoutput.h"

void findElectricField(const FEMesh*, const Element*,
		       const MasterPosition &, DoubleVec &);



#endif // CELECTRICFIELD_H
