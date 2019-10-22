// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef LATTICESYSTEM_SWG
#define LATTICESYSTEM_SWG

%module latticesystem
%include "common/typemaps.swg"

%{
#include <oofconfig.h>
#include "common/latticesystem.h"
%}
%pragma(python) include="latticesystem.spy"

class LatticeSymmetry {
};


%typemap(python, in) SmallMatrix *ThreeByThreeFloats (SmallMatrix mat) {
  // typemap(python, in) SmallMatrix *ThreeByThreeFloats
  // Convert [[x00, x01, x02],[x10, x11, x12], [x20, x21, x22]] to SmallMatrix
  mat.resize(3, 3);
  for(unsigned int row=0; row<3; row++)  {
    PyObject *pyrow = PyList_GET_ITEM($source, (Py_ssize_t) row);
    for(unsigned int col=0; col<3; col++) {
      PyObject *pyval = PyList_GET_ITEM(pyrow, (Py_ssize_t) col);
      mat(row, col) = PyFloat_AsDouble(pyval);
    }
  }
  $target = &mat;
}

void addLatticeSymmetryMatrix(char*, SmallMatrix *ThreeByThreeFloats);

#endif // LATTICESYSTEM_SWG

