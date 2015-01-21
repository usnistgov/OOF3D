// -*- C++ -*-
// $RCSfile: cskeletonelement.swg,v $
// $Revision: 1.1.2.21 $
// $Author: langer $
// $Date: 2014/12/14 01:07:48 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONELEMENT_SWG
#define CSKELETONELEMENT_SWG

%module cskeletonelement

%include "common/typemaps.swg"
%extern "engine/cskeletonselectable.swg"
%extern "common/cmicrostructure.swg"
%extern "engine/cskeletonnode2.swg"
%extern "engine/material.swg"
%{
#include <oofconfig.h>
#include "common/IO/oofcerr.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonselectable_i.h"
#include "engine/material.h"
%}

%pragma(python) include="engine/cskeletonelement.spy"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonMultiNodeSelectablePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonSelectablePtr"
%pragma(python) code="from ooflib.SWIG.common.cmicrostructure import CMicrostructurePtr"

class LineIntersectionPoint {
public:
  ~LineIntersectionPoint();
  Coord position();
  %new LineIntersectionPoint *next(CSkeletonBase*);
  bool done();
  CSkeletonElement *getElement();
  void addTraversedElement(CSkeletonElement*);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeletonElement : public CSkeletonMultiNodeSelectable {
public:
  int getIndex();
  int getMeshIndex();
  bool interior(Coord *Point);
  double volume();
  double volumeInVoxelUnits(CMicrostructure*);
  double volumeInFractionalUnits(CMicrostructure*);
  bool illegal();
  bool suspect();
  double homogeneity(CMicrostructure*);
  int dominantPixel(CMicrostructure*); 
  double energyShape();
  Material *material(CSkeletonBase*);
  int getNumberOfNodes();
  int getNumberOfSegments();
  // getSegmentNode can't be swigged, because importing cskeletonnode2
  // here causes an import loop.  cskeletonnode2 imports
  // cskeletonelement.
  //  CSkeletonNode *getSegmentNode(int, int);

  %new LineIntersectionPoint *startLinearXSection(CSkeletonBase*,
					Coord *Point, Coord *Point);

  const string& get_function() { return generating_function; }
  %addmethods {
    int uiIdentifier() {
      return self->getIndex();
    }
  }
  void dumpFaceInfo(CSkeletonBase*); // debugging
};

long get_globalElementCount();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// In C++, CSkeletonElementIterator is a typemap.  These methods must be
// added here so that it can be used in PySkeletonElementIterator, which
// acts like a real Python iterator.

class CSkeletonElementIterator {
public:
  %addmethods {
    CSkeletonElement *dereference() {
      return **self;
    }
    void increment() {
      ++*self;
    }
    bool notEqual(CSkeletonElementIterator *other) {
      return *self != *other;
    }
  }
};

void dumpElements();

#endif	// CSKELETONELEMENT_SWG


