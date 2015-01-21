// -*- C++ -*-
// $RCSfile: cskeletonselectable.swg,v $
// $Revision: 1.1.4.38 $
// $Author: langer $
// $Date: 2014/10/01 21:28:33 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONSELECTABLE_SWG
#define CSKELETONSELECTABLE_SWG

%module cskeletonselectable

%include "engine/typemaps.swg"
%extern "common/IO/canvaslayers.swg"
%extern "engine/cskeletonnode2.swg"
%{
#include <oofconfig.h>
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonselectable.h"
#include "common/IO/canvaslayers.h"
#include "common/IO/vtkutils.h"
%}

%pragma(python) include="engine/cskeletonselectable.spy"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkIdListPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkCellPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"

// Convert a std::set* of std::strings to a list of Python strings
%typemap(python, out) GroupNameSet* {
   // typemap(python, out) GroupNameSet*
   GroupNameSet::size_type sz = $source->size();
   assert((int) sz >= PY_SSIZE_T_MIN && (int) sz <= PY_SSIZE_T_MAX);
   $target = PyList_New((Py_ssize_t) sz);
   int ii = 0;
   for(GroupNameSet::const_iterator i=$source->begin(); i!=$source->end(); ++i){
     PyObject *str = PyString_FromString((*i).c_str());
     PyList_SET_ITEM($target, (Py_ssize_t) ii++, str); // Steals reference.
   }
}

%typemap(python, out) CSkeletonSelectable* {
   // typemap(python, out) CSkeletonSelectable*
   $target = $source->pythonObject();
}

enum SkeletonMapDir {MAP_DOWN, MAP_UP};

class CSkeletonSelectable {
public:
  int getUid();
  bool isSelected();
  void local_select();
  void local_deselect();
  void select(CSelectionTrackerVector *cvector,
	      CSelectionTrackerVector *pvector);
  void deselect(CSelectionTrackerVector *cvector,
		CSelectionTrackerVector *pvector);
  void add_to_group(char *group, CGroupTrackerVector *cvector,
		    CGroupTrackerVector *pvector);
  void remove_from_group(char* group, CGroupTrackerVector *cvector,
			 CGroupTrackerVector *pvector);
  void add_group_to_local(char* group);
  void remove_group_from_local(char* group);
  GroupNameSet *groupNames();
  bool is_in_group(char *group);

  CSkeletonSelectable *last_parent();
  CSkeletonSelectable *last_child();

  VTKCellType getCellType();
  bool active(CSkeletonBase *);
  vtkCellPtr getVtkCell();
  vtkIdListPtr getPointIds();

  %addmethods {
    int __hash__() {
      return self->getUid();
    }
    %new Coord *center() {
      Coord *x = new Coord();
      *x = self->center();
      return x;
    }
    bool __eq__(const CSkeletonSelectable *other) {
      return *self == *other;
    }
  }
};

int peekUID();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeletonMultiNodeSelectable : public CSkeletonSelectable {
public:
  CSkeletonNodeVector *getNodes();
  int nnodes();
  int getNodeIndexIntoList(CSkeletonNode *);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CAbstractTracker {};

class CSelectionTrackerBase : public CAbstractTracker {
public:
  ~CSelectionTrackerBase();
  CSelectionTracker* sheriff();
  CSkeletonSelectableSet* get();
  void clear();
  void clearskeleton();
  int size();
  bool empty();
  void write();
};

class CSelectionTracker : public CSelectionTrackerBase {
 public:
  CSelectionTracker();
  %new CSelectionTracker* clone();
  void implied_select(CSelectionTrackerBase *other);
  void add(CSkeletonSelectable *s);
};

class CDeputySelectionTracker : public CSelectionTrackerBase {
public:
  CDeputySelectionTracker(CSelectionTrackerBase*);
};

long getTrackerCount();		// for testing, used by memcheck

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void rebuildLayerCells(CSkeletonBase*, SimpleCellLayer*,
		       CAbstractTracker*);

#endif
