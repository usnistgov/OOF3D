// -*- C++ -*-
// $RCSfile: vtkColorLUT.C,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2014/11/24 21:44:47 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/vtkColorLUT.h"
#include "common/IO/oofcerr.h"

vtkSmartPointer<vtkLookupTable> New() {
  return vtkSmartPointer<vtkLookupTable>::New();
}

void SetNumberOfColors(vtkSmartPointer<vtkLookupTable> lut, int n) {
  lut->SetNumberOfColors(n);
}

void SetTableValue(vtkSmartPointer<vtkLookupTable> lut, int n,
		   double r, double g, double b, double a) {
  lut->SetTableValue(n, r, g, b, a);
}
