// -*- C++ -*-
// $RCSfile: cfiddlenodesbaseParallel.swg,v $
// $Revision: 1.4.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:18 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CFIDDLENODESBASEPARALLEL_SWG
#define CFIDDLENODESBASEPARALLEL_SWG

%module cfiddlenodesbaseParallel
%pragma(python) include="cfiddlenodesbaseParallel.spy"

%include "common/typemaps.swg"

// in  CFNMoveDataVec*  [CFiddleNodesMoveData] -> std::vector<CFiddleNodesMoveData*>*
%{
#include "engine/cfiddlenodesbaseParallel.h"
#include <vector>
  typedef std::vector<CFiddleNodesMoveData*> CFNMoveDataVec;
%}

%typemap(python, in) CFNMoveDataVec* (CFNMoveDataVec cfnv) {
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "Error in CFNMoveDataVec* typemap.  Python list required.");
    return NULL;
  }
  CFNMoveDataVec::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
						  Py_ssize_t,
						  CFNMoveDataVec::size_type);
  cfnv.resize(sz);
  for(CFNMoveDataVec::size_type i=0; i<sz; i++) {
    CFiddleNodesMoveData *cfn;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**)&cfn, "_CFiddleNodeMoveData_p");
    cfnv[i] = cfn;
  }
  $target = &cfnv;
}

class CFiddleNodesMoveData {
public:
  CFiddleNodesMoveData(int, int, double, double);
  int master;
  int index;
  double x;
  double y;
};

void tuneFiddle();
CFiddleNodesMoveData create_movedata(int, int, double, double);
void _Send_MoveData(CFNMoveDataVec*, IntVec*, int);
void _Isend_MoveData(CFNMoveDataVec*, IntVec*, int);
CFiddleNodesMoveData _Recv_MoveData(int, int);

#endif // CFIDDLENODEBASEPARALLEL_SWG
