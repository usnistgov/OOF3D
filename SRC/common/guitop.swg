// -*- C++ -*-
// $RCSfile: guitop.swg,v $
// $Revision: 1.1.20.3 $
// $Author: langer $
// $Date: 2014/05/29 13:47:32 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GUITOP_SWG
#define GUITOP_SWG

%module guitop
%include "common/typemaps.swg"
%{
#include <oofconfig.h>
#include "common/guitop.h"
%}
%pragma(python) include="common/guitop.spy"

void setMainLoop(bool);
bool getMainLoop();

#endif // GUITOP
