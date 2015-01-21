// -*- C++ -*-
// $RCSfile: steperrorscaling.swg,v $
// $Revision: 1.3.4.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef STEPERRORSCALING_SWG
#define STEPERRORSCALING_SWG

%module steperrorscaling

%include "engine/typemaps.swg"
%pragma(python) include="steperrorscaling.spy"
%{
#include "common/doublevec.h"
#include "engine/steperrorscaling.h"
%}

class StepErrorScaling {
public:
  bool globalscaling();
  %addmethods {
    double __call__(double deltat, DoubleVec &start,
		    DoubleVec &end0, DoubleVec &end1)
    {
      return (*self)(deltat, start, end0, end1);
    }
  }
};

class RelativeErrorScaling : public StepErrorScaling {
public:
  RelativeErrorScaling();
};

class AbsoluteErrorScaling : public StepErrorScaling {
public:
  AbsoluteErrorScaling();
};

class XOverErrorScaling : public StepErrorScaling {
public:
  XOverErrorScaling();
};

class GlobalErrorScaling : public StepErrorScaling {
public:
  GlobalErrorScaling();
};

#endif // STEPERRORSCALING_SWG
