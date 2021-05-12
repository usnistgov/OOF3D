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

// Module initiation in VTK 9.

// Since we're not using cmake to build OOF3D, we have to do some
// things by hand.

// (1) Use FindNeededModules.py (in Utilities/Maintenance in the VTK
// source) to find which VTK modules need to be included.  % python

// FindNeededModules.py -j path/to/modules.json -s path/to/OOF3D

// path/to/modules.json is in the VTK9 *build* directory.
// path/to/OOF3D is a directory containing OOF3D source.  VTK expects
// C++ files to have a .cxx suffix, so I copied the .C and .h files to
// FLAT, appended .cxx to the .C file names, and ran FindNeededModules
// on FLAT.

// Grepping for all of the VTK include statements, putting htem in a
// file, and running FindNeededModules on *that* gave a different
// result.

// (2) The output from FindNeededModules looks like
// find_package(VTK
//  COMPONENTS
//      CommonCore
//      CommonDataModel
//      [etc]
//  )
// Put the modules listed there into a CMakeLists.txt file:
//   project(vtktest C CXX)
//   [ The find_package lines ]
//   add_library(foo dummy.cxx)
//   # I don't know if this is needed or how to find which libraries to include
//   target_link_libraries(foo vtkCommonCore-9.0 [others libraries])
//   vtk_module_autoinit(TARGETS foo
//     MODULES
//       VTK::CommonCore
//       VTK::CommonDataModel
//       [same modules as in find_package, but with VTK:: prepended]
//    )

// (3) Create dummy.cxx in the same directory as CMakeLists.txt.  I
// just wrote hello world.  I don't know if it has to actually use
// vtk.  Adding a few lines of trivial vtk calls didn't change the
// results.

// (4) Create a build directory in the directory.  cd to it and run
// "cmake ..".

// (5) There should be a subdirectory called CMakeFiles containing a
// file called vtkModuleAutoInit_[somesortofhash].h.  This contains a
// bunch of #defines.  Include the #defines in this file, followed by
// #include <vtkAutoInit.h>.

// (6) For each of the #defines from FindNeededModules, add the
// corresponding library to the list in set_clib_flags in
// SRC/common/DIR.py.  Some of the #define don't have a corresponding
// library.

// (7) Run the program. If there are "undefined symbol" messages, use
// nm to find the symbols in the vtk libraries and add the libraries
// to the list in DIR.py.

// (8) Hope that that all worked.


// #defines found by grepping all "#include <vtk*>" lines from all
// OOF3D files, putting them in vtkincludes.h, and running
// FindNeededModules on that.
#define vtkIOExport_AUTOINIT 1(vtkIOExportPDF)
#define vtkIOExportGL2PS_AUTOINIT 1(vtkIOExportGL2PS)
#define vtkRenderingContext2D_AUTOINIT 1(vtkRenderingContextOpenGL2)
#define vtkRenderingCore_AUTOINIT 4(vtkInteractionStyle,vtkRenderingFreeType,vtkRenderingOpenGL2,vtkRenderingUI)
#define vtkRenderingOpenGL2_AUTOINIT 1(vtkRenderingGL2PSOpenGL2)
#define vtkRenderingVolume_AUTOINIT 1(vtkRenderingVolumeOpenGL2)

// #defines found by copying all OOF3D .C and .h files to FLAT,
// renaming FLAT/*.C to FLAT/*.cxx, and running FindNeededModules.py
// on FLAT.

// #define vtkIOExportGL2PS_AUTOINIT 1(vtkIOExportGL2PS)
// #define vtkRenderingCore_AUTOINIT 4(vtkInteractionStyle,vtkRenderingFreeType,vtkRenderingOpenGL2,vtkRenderingUI)
// #define vtkRenderingOpenGL2_AUTOINIT 1(vtkRenderingGL2PSOpenGL2)



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
