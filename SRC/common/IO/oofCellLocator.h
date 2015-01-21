// -*- C++ -*-
// $RCSfile: oofCellLocator.h,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2013/04/17 20:52:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// A slight modification to vtkCellLocator that gives it a slightly
// larger initial bounding box, preventing roundoff error from causing
// line intersections at the boundary of the bounding box to be
// incorrectly ignored.

#ifndef __oofCellLocator_h
#define __oofCellLocator_h

#include <oofconfig.h>

#include <vtkCellLocator.h>

class oofCellLocator : public vtkCellLocator {
 public:
  vtkTypeRevisionMacro(oofCellLocator, vtkCellLocator);
  oofCellLocator() {}
  virtual ~oofCellLocator() {}
  static oofCellLocator *New();
  virtual void BuildLocatorInternal();
};

#endif // __oofCellLocator_h
