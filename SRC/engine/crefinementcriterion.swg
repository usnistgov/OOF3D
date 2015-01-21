// -*- C++ -*-
// $RCSfile: crefinementcriterion.swg,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2014/12/14 01:07:46 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CREFINEMENTCRETERION_SWG
#define CREFINEMENTCRETERION_SWG

%module crefine

%include "common/typemaps.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/crefinementcriterion.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonmodifier.h"
#include "engine/cskeletonnode2.h"
#include "engine/homogeneity.h"
%}

%pragma(python) include="engine/crefinementcriterion.spy"

class SegmentChooser {

};

class FromAllSegments : public SegmentChooser {
public:
  FromAllSegments();
};

class FromSelectedSegments : public SegmentChooser {
public:
  FromSelectedSegments();
};

class FromSelectedElements : public SegmentChooser {
public:
  FromSelectedElements();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class RefinementTargets {};

class CheckAllElements : public RefinementTargets {
public:
  CheckAllElements();
};

class CheckSelectedElements : public RefinementTargets {
public:
  CheckSelectedElements();
};

class CheckElementsInGroup : public RefinementTargets {
public:
  CheckElementsInGroup(char*);
};

class CheckHomogeneity : public RefinementTargets {
public:
  CheckHomogeneity(double);
};

class CheckHeterogeneousEdges : public RefinementTargets {
public:
  CheckHeterogeneousEdges(double, SegmentChooser*);
};

class CheckSelectedEdges : public RefinementTargets {
public:
  CheckSelectedEdges();
};

class CheckSegmentsInGroup : public RefinementTargets {
public:
  CheckSegmentsInGroup(char*);
};

class CheckSelectedFaces : public RefinementTargets {
public:
  CheckSelectedFaces();
};

class CheckFacesInGroup: public RefinementTargets {
public:
  CheckFacesInGroup(char*);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class RefinementCriterion {

};

class Unconditionally : public RefinementCriterion {
public:
  Unconditionally();
};

class MinimumVolume : public RefinementCriterion {
public:
  MinimumVolume(double, std::string *enum2string);
};

class MinimumArea : public RefinementCriterion {
public:
  MinimumArea(double, std::string *enum2string);
};

class MinimumLength : public RefinementCriterion {
public:
  MinimumLength(double, std::string *enum2string);
};

%typemap(python, in) std::string *enum2string {}


#endif	// CREFINEMENTCRITERION_SWG
