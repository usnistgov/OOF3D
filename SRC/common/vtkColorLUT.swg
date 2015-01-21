// -*- C++ -*-
// $RCSfile: vtkColorLUT.swg,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2014/11/24 21:44:48 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef VTKCOLORLUT_SWG
#define VTKCOLORLUT_SWG

%module vtkColorLUT
%include "common/typemaps.swg"

%{
#include "common/vtkColorLUT.h"
#include "common/IO/vtkutils.h"
%}

class vtkLookupTablePtr {
public:
  //vtkLookupTablePtr(const vtkLookupTablePtr&);
  ~vtkLookupTablePtr();
};

vtkLookupTablePtr New();

void SetNumberOfColors(vtkLookupTablePtr lut, int n);

void SetTableValue(vtkLookupTablePtr lut, int n,
		   double r, double g, double b, double a);

#endif	// VTKCOLORLUT_H
