// -*- C++ -*-
// $RCSfile: progressGUI.h,v $
// $Revision: 1.1.20.2 $
// $Author: langer $
// $Date: 2013/01/28 16:58:10 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PROGRESSGUI_H
#define PROGRESSGUI_H

// When the swigged python module is loaded, it calls this function,
// which sets up the hook that disconnects GUI progress bars when
// Progress objects are destroyed or finished.

void initialize();

#endif // PROGRESSGUI_H
