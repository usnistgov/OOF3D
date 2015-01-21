// -*- C++ -*-
// $RCSfile: cskeletonselectable_i.h,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2014/12/14 01:07:51 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This file contains forward declarations and typedefs from
// cskeletonselectable.h.  It can be included instead of that file in
// most situations, to reduce header file dependencies.

#ifndef CSKELETONSELECTABLE_I_H
#define CSKELETONSELECTABLE_I_H

#include <oofconfig.h>

#include <list>
#include <map>
#include <set>
#include <vector>

class CDeputySelectionTracker;
class CSelectionTracker;
class CSelectionTrackerBase;
class CSkeletonSelectable;

class CGroupTrackerBase;

typedef unsigned long uidtype;


typedef std::vector<CSelectionTrackerBase*> CSelectionTrackerVector;
typedef std::vector<CGroupTrackerBase*> CGroupTrackerVector;
// for the parents and children, lists are more efficient than vectors
// because we need to be able to remove items from arbitrary
// positions.  TODO 3.1: consider changing this type.  Finding whether
// something is in a list is inefficient, and adding unique items is
// inefficient. A map has all the qualities we need. (Maybe a std::set?)
typedef std::list<CSkeletonSelectable*> CSkeletonSelectableList;

// Various useful typedefs for derived classes of
// CSkeletonSelectable. The different classes interact with each other
// containing these types, so it is useful to define them here.
//  TODO MER: Really? Move the Node-, Element-, Face-, and Segment-
// specific typedefs to the appropriate files.

typedef std::vector<uidtype> UidVector;

class CSkeletonNode;
typedef std::vector< CSkeletonNode* > CSkeletonNodeVector;
typedef CSkeletonNodeVector::const_iterator CSkeletonNodeIterator;
typedef std::list< CSkeletonNode* > CSkeletonNodeList;

class CSkeletonMultiNodeKey;
class CSkeletonMultiNodeSelectable;

class CSkeletonSegment;
typedef std::vector<CSkeletonSegment*> CSkeletonSegmentVector;
typedef std::map<CSkeletonMultiNodeKey, CSkeletonSegment*> CSkeletonSegmentMap;
typedef CSkeletonSegmentMap::const_iterator CSkeletonSegmentIterator;
typedef std::list<CSkeletonSegment*> CSkeletonSegmentList;

class CSkeletonFace;
typedef std::vector<CSkeletonFace*> CSkeletonFaceVector;
typedef std::map<CSkeletonMultiNodeKey, CSkeletonFace*> CSkeletonFaceMap;
typedef CSkeletonFaceMap::const_iterator CSkeletonFaceIterator;

class CSkeletonElement;
typedef std::vector<CSkeletonElement*> CSkeletonElementVector;
typedef CSkeletonElementVector::const_iterator CSkeletonElementIterator;
typedef std::vector<const CSkeletonElement*> ConstCSkeletonElementVector;

// functor used by sorting algorithm for containers of pointers
struct CSkeletonSelectableLTUid {
  bool operator()(const CSkeletonSelectable*, const CSkeletonSelectable*) const;
};


typedef std::set<CSkeletonSelectable*, CSkeletonSelectableLTUid> CSkeletonSelectableSet;
typedef std::set<CSkeletonNode*, CSkeletonSelectableLTUid> CSkeletonNodeSet;
typedef std::set<CSkeletonSegment*, CSkeletonSelectableLTUid> CSkeletonSegmentSet;
typedef std::set<CSkeletonFace*, CSkeletonSelectableLTUid> CSkeletonFaceSet;
typedef std::set<CSkeletonElement*, CSkeletonSelectableLTUid> CSkeletonElementSet;
typedef std::set<const CSkeletonElement*, CSkeletonSelectableLTUid> ConstCSkeletonElementSet;

// vectors of pairs are used for substitutions in ProvisionalChanges
typedef std::pair<CSkeletonSelectable*, CSkeletonSelectable*> CSkeletonSelectablePair;

struct CSkeletonSelectablePairLTUid {
  bool operator()(const CSkeletonSelectablePair &a,
		  const CSkeletonSelectablePair &b) const;
};
    
typedef std::set<CSkeletonSelectablePair, CSkeletonSelectablePairLTUid> CSkeletonSelectablePairSet;

class OrientedCSkeletonFace;
class OrientedSurface;
struct OrientedFaceLTUid;

typedef std::set<OrientedCSkeletonFace*, OrientedFaceLTUid>
    OrientedCSkeletonFaceSet;

typedef std::vector<OrientedCSkeletonFace*> OrientedCSkeletonFaceVector;

typedef std::list<CSkeletonFace*> CSkeletonFaceList;
typedef std::map<CSkeletonSegment*, CSkeletonFaceList> SegFaceListMap;
typedef std::map<CSkeletonSegment*, OrientedCSkeletonFace*> SegFaceMap;


// TODO 3.1: Use const std::string* here.  Copies of strings could use a
// lot of memory.  Even better would be for GroupNameSets to be shared
// between CSkeletonSelectable objects.
typedef std::set<std::string> GroupNameSet;

// TODO 3.1: These aren't best names. Which is down?  Toward the parent or
// toward the child?  (MAP_UP is toward the parent.  Perhaps the name
// should be MAP_TO_PARENT.)
enum SkeletonMapDir {MAP_DOWN=0, MAP_UP=1};


#endif // CSKELETONSELECTABLE_I_H
