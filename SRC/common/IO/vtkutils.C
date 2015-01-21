// -*- C++ -*-
// $RCSfile: vtkutils.C,v $
// $Revision: 1.1.2.10 $
// $Author: langer $
// $Date: 2014/12/14 22:49:10 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <limits>
#include "common/IO/vtkutils.h"
#include "common/coord.h"

// Copy a std::vector of doubles into a new vtkDoubleArray, and return
// a vtkSmartPointer to the array.

vtkSmartPointer<vtkDoubleArray> fillDataArray(const std::vector<double> *x) {
  vtkSmartPointer<vtkDoubleArray> array =
    vtkSmartPointer<vtkDoubleArray>::New();
  array->Allocate(x->size());
  for(unsigned int i=0; i<x->size(); i++)
    array->InsertNextValue((*x)[i]);
  return array;
}

void getDataArrayRange(vtkSmartPointer<vtkDataArray> data, double *minmax) {
  data->GetRange(minmax);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Coord cell2coord(vtkSmartPointer<vtkCell> cell) {
  vtkSmartPointer<vtkPoints> pts = cell->GetPoints();
  double xmin = std::numeric_limits<double>::max();
  double ymin = xmin;
  double zmin = xmin;
  for(int i=0; i<pts->GetNumberOfPoints(); i++) {
    double x[3];
    pts->GetPoint(i, x);
    if(x[0] < xmin) xmin = x[0];
    if(x[1] < ymin) ymin = x[1];
    if(x[2] < zmin) zmin = x[2];
  }
  return Coord(xmin, ymin, zmin);
}

