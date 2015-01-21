// -*- C++ -*-
// $RCSfile: progressGUI.swg,v $
// $Revision: 1.1.20.2 $
// $Author: langer $
// $Date: 2013/01/28 16:58:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PROGRESSGUI_SWG
#define PROGRESSGUI_SWG

%module progressGUI
%include "common/typemaps.swg"

%{
#include "common/IO/GUI/progressGUI.h"
%}
%pragma(python) include="common/IO/GUI/progressGUI.spy"

void initialize();

#endif // PROGRESSGUI_SWG
