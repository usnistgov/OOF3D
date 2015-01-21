// -*- C++ -*-
// $RCSfile: damping.swg,v $
// $Revision: 1.2.16.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:27 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef DAMPING_SWG
#define DAMPING_SWG

%module damping

%{
#include "engine/property/damping/damping.h"
%}

%include "engine/typemaps.swg"
%include "engine/propertyhdr.swg"

class IsotropicDampingProp : public Property {
public:
  IsotropicDampingProp(PyObject*, char*, double);
};

%pragma(python) include="damping.spy"

#endif // DAMPING_SWG
