// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef HTETDEBUG_SWG
#define HTETDEBUG_SWG

%module htetdebug

%include "common/typemaps.swg"

%pragma(python) include="engine/htetdebug.spy"

%{
#include "engine/cskeletonelement.h"
#include "engine/homogeneitytet.h"
%}

void setVerboseElement(unsigned int);
void setVerboseAllElements();
void setVerboseFace(unsigned int);
void setVerbosePlane(unsigned int dir, int offset, int side);
void setVerboseCategory(unsigned int);

#endif // HTETDEBUG_SWG
