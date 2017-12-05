// -*- C++ -*-

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
#include "common/IO/oofcerr.h"
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#include <vtkAutoInit.h>
#include <vtkVersionMacros.h>

// Call this before any other vtk code runs.
// See https://www.vtk.org/Wiki/VTK/Build_System_Migration
// Run-time messages like
//    Error: no override found for 'vtkActor'.
// mean that another module needs to be initialized here.


void initialize_vtk() {
  static bool initialized = false;
  if(!initialized) {
#ifdef DEBUG
    oofcerr << "Using vtk version " << VTK_VERSION << std::endl;
#endif // DEBUG
    VTK_MODULE_INIT(vtkRenderingOpenGL2);
    VTK_MODULE_INIT(vtkRenderingContextOpenGL2);
    VTK_MODULE_INIT(vtkRenderingVolumeOpenGL2);
    VTK_MODULE_INIT(vtkRenderingFreeType);


    // A comment on vtk-users led me to the VTK
    // Utilities/Maintenance/WhatModules.py script, which supposedly
    // scans your code and determines what modules it needs.
    // According to the script, we need the following.  But it doesn't
    // say if they should be imported via VTK_MODULE_INIT, or what.
    // Apparently this is incorrect, because it just leads to a Symbol
    // not found error for __Z32vtkCommonCore_AutoInit_Constructv,
    // although libvtkCommonCore is linked.
    
    // VTK_MODULE_INIT(vtkCommonCore);
    // VTK_MODULE_INIT(vtkCommonDataModel);
    // VTK_MODULE_INIT(vtkCommonExecutionModel);
    // VTK_MODULE_INIT(vtkCommonTransforms);
    // VTK_MODULE_INIT(vtkFiltersCore);
    // VTK_MODULE_INIT(vtkFiltersExtraction);
    // VTK_MODULE_INIT(vtkFiltersGeneral);
    // VTK_MODULE_INIT(vtkFiltersGeometry);
    // VTK_MODULE_INIT(vtkFiltersModeling);
    // VTK_MODULE_INIT(vtkFiltersSources);
    // VTK_MODULE_INIT(vtkIOExport);
    // VTK_MODULE_INIT(vtkIOImage);
    // VTK_MODULE_INIT(vtkIOXML);
    // VTK_MODULE_INIT(vtkImagingColor);
    // VTK_MODULE_INIT(vtkImagingCore);
    // VTK_MODULE_INIT(vtkImagingGeneral);
    // VTK_MODULE_INIT(vtkImagingMath);
    // VTK_MODULE_INIT(vtkRenderingAnnotation);
    // VTK_MODULE_INIT(vtkRenderingCore);
    // VTK_MODULE_INIT(vtkRenderingOpenGL);
    // VTK_MODULE_INIT(vtkWrappingPythonCore);
    // VTK_MODULE_INIT(vtktiff);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Some X11 errors indicated that we needed to call XInitThreads.
// That doesn't seem to be the case.  This code was inserted to see if
// calling XInitThreads would fix the problem.  It doesn't do anything
// unless USE_XINITTHREADS is defined (which it isn't).  The code is
// here so that if the problem recurs, searching for XInitThreads will
// find this comment.

// Using vtk8, and NOT calling XInitThreads here, all is ok whether or
// not --sync is used on the command line.  Calling XInitThreads here
// makes the program crash as soon as it enters the gtk main loop.

// Using vtk7, calling XInitThreads is ok if --sync is NOT used.
// --sync makes the program crash in the main loop.  Not calling
// XinitThreads is ok with or without --sync.

// vtk  --sync  XinitThreads  crash
//   7     no      yes          none
//   7     yes     yes          main loop
//   7     yes     no           main loop
//   7     no      no           none

//   8     no      yes          main loop
//   8     yes     yes          main loop
//   8     yes     no           none
//   8     no      no           none

#ifdef USE_XINITTHREADS
#include <X11/Xlib.h>

void initialize_X11() {
  // TODO: This doesn't really belong in this file.
  static bool initialized = false;
  if(!initialized) {
    initialized = true;

    XInitThreads();
  }

}

#else  // not USE_XINITTHREADS

void initialize_X11() {}

#endif // not USE_XINITTHREADS
