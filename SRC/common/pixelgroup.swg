// -*- C++ -*-
// $RCSfile: pixelgroup.swg,v $
// $Revision: 1.27.10.16 $
// $Author: langer $
// $Date: 2014/09/27 22:33:55 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PIXELGROUP_SWG
#define PIXELGROUP_SWG

%module pixelgroup
%include "common/typemaps.swg"

%{
#include "common/pixelgroup.h"
#include "common/cmicrostructure.h"
#include "common/ooferror.h"
%}
%pragma(python) include="pixelgroup.spy"
%extern "common/cmicrostructure.swg"
%extern "common/pixelattribute.swg"

%pragma(python) code="from ooflib.SWIG.common.pixelattribute import PxlAttributeRegistrationPtr"

%typemap(python, argout) ICoord &ICoordOut {
   // typemap(python, argout) ICoord &ICoordOut
   // Convert the ICoord to an iPoint and return it.  If $target
   // already exists, make sure that it's a list and append the iPoint
   // to it.
   static PyObject *iPointClass = 0;
   if(!iPointClass) {
     PyObject *module = PyImport_ImportModule("ooflib.common.primitives");
     iPointClass = PyObject_GetAttrString(module, "iPoint");
     if(!iPointClass) return 0;
     Py_XDECREF(module);
   }
#ifndef DIM_3
   PyObject *xyargs = Py_BuildValue("ii", (*$source)[0], (*$source)[1]);
#else
   PyObject *xyargs = Py_BuildValue("iii", (*$source)[0], (*$source)[1],
				    (*$source)[2]);
#endif // DIM_3
   PyObject *ipt = PyObject_CallObject(iPointClass, xyargs);
   Py_XDECREF(xyargs);
   if(!$target) {
     $target = ipt;
   }
   else if($target == Py_None) {
     Py_DECREF(Py_None);
     $target = ipt;
   }
   else {
     if(!PyList_Check($target)) {
       PyObject *other = $target;
       $target = PyList_New((Py_ssize_t) 0);
       PyList_Append($target, other);
       Py_XDECREF(other);
     }
     PyList_Append($target, ipt);
     Py_XDECREF(ipt);
   }
}

%typemap(python, ignore) ICoord &ICoordOut (ICoord tmp) {
  // typemap(python, ignore) ICoord &ICoordOut
  $target = &tmp;
}

class PixelSet {
public:
  ~PixelSet();
  int id();
  void resize(ICoord *iPoint);
  void add(CPixelSelection *sel);
  void addWithoutCheck(PixelSet *set);
  void remove(CPixelSelection *sel);
  void getBounds(ICoord &ICoordOut, ICoord &ICoordOut);

  %new PixelSet *clone();
  void clear();
  // TODO 3.1: members() is used only by PixelGroup._pixels_from_group
  // in analysisdomain.py.  That should use a more efficient method
  // that doesn't entail copying a long list of ICoords.  It could do
  // something like what the FEMeshContainerProxy classes in
  // femesh.spy do for iterating over Mesh components.  See the similar
  // TODO in cpixelselection.swg.
  ICoordVec *members();
  %addmethods {
    int __len__() {
      return self->len();
    }
    void addGroup(PixelGroup *g) {
      self->add(g);
    }
  }
};

class PixelGroup : public PixelSet {
public:
  PixelGroup(char *name, ICoord *iPoint, CMicrostructure *microstructure);
  ~PixelGroup();
  void rename(char*);
  bool is_meshable();
  void set_meshable(bool);
  const string &name();
  bool pixelInGroup(const ICoord *iPoint);
  %addmethods {
    void addPixels(const ICoordVec *iPointList) {
      self->add(iPointList);
    }
  }
};

%new StringVec *pixelGroupNames(CMicrostructure*, int cat);

class PixelGroupAttributeRegistration : public PxlAttributeRegistration {
public:
  PixelGroupAttributeRegistration();
  ~PixelGroupAttributeRegistration();
};

#endif // PIXELGROUP_SWG
