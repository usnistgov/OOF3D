// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef VTKUTILS_SWG
#define VTKUTILS_SWG

%module vtkutils
%include "common/typemaps.swg"
%extern "common/direction.swg"

%{
#include "common/IO/vtkutils.h"
#include "common/direction.h"
#include <vtkDataArray.h>
#include <vtkVersion.h>
%}

%typemap(python, argout) double *outDoublePair {
  // typemap(python, argout) double *outDoublePair
  $target = PyList_New((Py_ssize_t) 2);
  PyList_SET_ITEM($target, (Py_ssize_t) 0, PyFloat_FromDouble($source[0]));
  PyList_SET_ITEM($target, (Py_ssize_t) 1, PyFloat_FromDouble($source[1]));
}

%typemap(python, ignore) double *outDoublePair (double dpair[2]) {
  // typemap(python, ignore) double *outDoublePair
  $target = dpair;
}

void initialize_vtk();		// Call before any other vtk code
void initialize_X11();

%inline %{
int vtkMajorVersion() { return VTK_MAJOR_VERSION; }
int vtkMinorVersion() { return VTK_MINOR_VERSION; }
int vtkBuildVersion() { return VTK_BUILD_VERSION; }
%}

class vtkDoubleArrayPtr {
public:
  ~vtkDoubleArrayPtr();
  %addmethods {
    int size() {
      return (*self)->GetNumberOfTuples();
    }
  }
};

class vtkDataArrayPtr {
public:
  ~vtkDataArrayPtr();
  %addmethods {
    int size() {
      return (*self)->GetNumberOfTuples();
    }
  }
};

void getDataArrayRange(vtkDataArrayPtr, double *outDoublePair);

class vtkIntArrayPtr {
public:
  ~vtkIntArrayPtr();
  %addmethods {
    int size() {
      return (*self)->GetNumberOfTuples();
    }
  }
};

class vtkUnstructuredGridPtr {
public:
  ~vtkUnstructuredGridPtr();
};

class vtkPointsPtr {
public:
  ~vtkPointsPtr();
};

class vtkIdListPtr {
public:
  ~vtkIdListPtr();
public:
  %addmethods {
    int size() { return (*self)->GetNumberOfIds(); }
    int __getitem__(int i) { return (*self)->GetId(i); }
  }
};

class vtkCellPtr {
public:
  ~vtkCellPtr();
  %addmethods {
    bool null() {
      return self->GetPointer() == 0;
    }
  }
};

class vtkPlanePtr {
public:
  ~vtkPlanePtr();
};

class vtkActorPtr {
public:
  ~vtkActorPtr();
  %addmethods {
    bool equals(vtkActorPtr actor) {
      return (*self) == actor;
    }
  }
};

class vtkActorCollectionPtr {
public:
  ~vtkActorCollectionPtr();
  %addmethods {
    bool hasActor(vtkActorPtr actor) {
      return (*self)->IsItemPresent(actor) != 0;
    }
  }
};

%new vtkDoubleArrayPtr fillDataArray(const DoubleList*);
Coord cell2coord(vtkCellPtr);

#endif // VTKUTILS_SWG

