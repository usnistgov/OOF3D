// -*- C++ -*-
// $RCSfile: vtkColorLUT.h,v $
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

#include <oofconfig.h>

// Wrappers for vtkLookupTable methods, so that we can use them from Python.

#include <vtkSmartPointer.h>
#include <vtkLookupTable.h>

#ifndef VTKCOLORLUT_H
#define VTKCOLORLUT_H

vtkSmartPointer<vtkLookupTable> New();

void SetNumberOfColors(vtkSmartPointer<vtkLookupTable>, int);

void SetTableValue(vtkSmartPointer<vtkLookupTable>, int,
		   double, double, double, double);

// typedef used by swig.
typedef vtkSmartPointer<vtkLookupTable> vtkLookupTablePtr;

#endif
