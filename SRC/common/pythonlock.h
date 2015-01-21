// -*- C++ -*-
// $RCSfile: pythonlock.h,v $
// $Revision: 1.2 $
// $Author: langer $
// $Date: 2009/05/19 21:34:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PYTHONLOCK_H
#define PYTHONLOCK_H

PyGILState_STATE acquirePyLock();
void releasePyLock(PyGILState_STATE);

#endif // PYTHONLOCK_H
