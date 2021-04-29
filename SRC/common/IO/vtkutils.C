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

#if VTK_MAJOR_VERSION >= 9
#define vtkIOExportGL2PS_AUTOINIT 1(vtkIOExportGL2PS)
#define vtkRenderingCore_AUTOINIT 4(vtkInteractionStyle,vtkRenderingFreeType,vtkRenderingOpenGL2,vtkRenderingUI)
#define vtkRenderingOpenGL2_AUTOINIT 1(vtkRenderingGL2PSOpenGL2)
#endif // VTK_MAJOR_VERSION >= 9

#include <vtkAutoInit.h>
#include <vtkVersionMacros.h>
#include <vtkMapper.h>

#include "common/IO/oofcerr.h"
#include "common/IO/vtkutils.h"
#include "common/coord.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

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

// Call this before any other vtk code runs.
// See https://www.vtk.org/Wiki/VTK/Build_System_Migration
// Run-time messages like
//    Error: no override found for 'vtkActor'.
// mean that another module needs to be initialized with
// VTK_MODULE_INIT here.
//
// To find the module, search for the missing name in
// <vtk-build-dir>/lib/cmake/vtk-X.Y/Modules/*.cmake.  It will be
// found in vtkSOMETHING-Headers.cmake.  Then include
// VTK_MODULE_INIT(vtkSOMETHING) below.

void initialize_vtk() {
  static bool initialized = false;
  if(!initialized) {
#ifdef DEBUG
    oofcerr << "Using vtk version " << VTK_VERSION << std::endl;
#endif // DEBUG

#if VTK_MAJOR_VERSION < 9
    VTK_MODULE_INIT(vtkRenderingOpenGL2);
    VTK_MODULE_INIT(vtkRenderingContextOpenGL2);
    VTK_MODULE_INIT(vtkRenderingVolumeOpenGL2);
    VTK_MODULE_INIT(vtkRenderingFreeType);
    VTK_MODULE_INIT(vtkIOExportOpenGL2);
    VTK_MODULE_INIT(vtkRenderingGL2PSOpenGL2);
#endif // VTK_MAJOR_VERSION < 9
    
    vtkMapper::SetResolveCoincidentTopologyToPolygonOffset();
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
// (initialize_X11 had been called from oof.py just before calling
// initialize_vtk.)

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
