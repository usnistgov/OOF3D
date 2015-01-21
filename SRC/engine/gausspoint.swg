// -*- C++ -*-
// $RCSfile: gausspoint.swg,v $
// $Revision: 1.4.18.2 $
// $Author: langer $
// $Date: 2014/01/23 20:54:32 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GAUSSPOINT_SWG
#define GAUSSPOINT_SWG

%module gausspoint
%{
#include "engine/gausspoint.h"
%}

%pragma(python) code="from ooflib.SWIG.engine.mastercoord import MasterPositionPtr"
%pragma(python) code="from ooflib.SWIG.engine.mastercoord import MasterCoordPtr"
%pragma(python) code="from ooflib.SWIG.common.coord import PositionPtr"

%include "engine/typemaps.swg"
%extern "engine/mastercoord.swg"
%extern "common/coord.swg"

class GaussPoint : public Position, public MasterPosition {
public:
  double weight();
  MasterCoord mastercoord();
  ~GaussPoint();
  Coord coord();
};

#endif // GAUSSPOINT_SWG
