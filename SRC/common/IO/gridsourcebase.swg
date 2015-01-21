// -*- C++ -*-
// $RCSfile: gridsourcebase.swg,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2013/04/17 15:45:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GRIDSOURCEBASE_SWG
#define GRIDSOURCEBASE_SWG

%module gridsourcebase
%include "common/typemaps.swg"

%{
#include "common/IO/gridsourcebase.h"
%}

class GridSourcePtr {
public:
  ~GridSourcePtr();		// see comment in common/IO/vtkutils.h
  %addmethods {
    void Modified() {
      (*self)->Modified();
    }
  }
};



#endif // GRIDSOURCEBASE_SWG
