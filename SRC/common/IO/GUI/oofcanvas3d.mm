// -*- objc -*-


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// When using the Cocoa instead of X11 the oofcanvas3d code must be
// compiled by ObjectiveC.  This wrapper just gives it the right
// suffix ('.mm', meaning that it's a mix of ObjectiveC and C++).
// When USE_COCOA is defined in setup.py, common/IO/GUI/DIR.py
// includes oofcanvas3d.mm instead of oofcanvas3d.C.

#include "common/IO/GUI/oofcanvas3d.C"
