// -*- C++ -*-
// $RCSfile: dofmap.swg,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2013/11/08 20:43:42 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef DOFMAP_SWG
#define DOFMAP_SWG

%module dofmap
%include "engine/typemaps.swg"
%extern "common/doublevec.swg"
%{
#include "common/doublevec.h"
#include "common/tostring.h"
#include "engine/dofmap.h"
%}

%pragma(python) code="from ooflib.SWIG.common.doublevec import DoubleVecPtr"

class DoFMap {
public:
  DoFMap();
  ~DoFMap();
  %new DoubleVec* extract(DoubleVec&);
  void inject(DoubleVec&, DoubleVec&);
  int range();
  int domain();
  %addmethods {
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

DoFMap compose(DoFMap&, DoFMap&);
DoFMap concat(DoFMap&, DoFMap&);

#endif // DOFMAP_SWG
