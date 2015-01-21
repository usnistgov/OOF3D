// -*- C++ -*-
// $RCSfile: elasticity.swg,v $
// $Revision: 1.11.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:29 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ELASTICITY_SWG
#define ELASTICITY_SWG

%module elasticity

%{
#include "engine/property/elasticity/elasticity.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%extern "engine/property/elasticity/cijkl.swg"
%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.cijkl import CijklPtr"

class Elasticity : public Property {
public:
  Cijkl cijkl(const FEMesh*, const Element*, const MasterPosition&);
};

#endif // ELASTICITY_SWG
