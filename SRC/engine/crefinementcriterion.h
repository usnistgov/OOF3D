// -*- C++ -*-
// $RCSfile: crefinementcriterion.h,v $
// $Revision: 1.1.2.4 $
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

#include <oofconfig.h>

#ifndef CREFINEMENTCRETERION_H
#define CREFINEMENTCRETERION_H

#include "engine/cskeletonselectable_i.h"
#include "engine/cskeletonmodifier.h"

// For now, in the 3D code, there is no RefinementDegree object and no
// ruleset object as only bisection is implemented and we only have
// tetrahedra.  See refine.py for the old refinement degree code.

 class RefinementCriterion;
 typedef std::pair<CSkeletonMultiNodeKey, short> SegmentMarkDatum;
 typedef std::map<CSkeletonMultiNodeKey, short> SegmentMarks;

 // A RefinementSignature is a vector of pairs of ints.  The first int
 // in the pair is an element segment index.  The second is the
 // refinement degree.  The vector is sorted in segment index order.
 typedef std::pair<short, short> RefinementSignaturePair;
 typedef std::vector<RefinementSignaturePair> RefinementSignature;

 //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Segment choosers are helper classes for refinement targets that
// target segments rather than elements.  They specify the set of
// segments from which the choice is made.

class SegmentChooser {
protected:
  CSkeletonSegmentVector *segs;
public:
  SegmentChooser() {segs = new CSkeletonSegmentVector;};
  virtual ~SegmentChooser() {delete segs;};
  virtual CSkeletonSegmentVector *getSegments(CSkeletonBase *skeleton) = 0;
};

class FromAllSegments : public SegmentChooser {
public:
  FromAllSegments() {};
  virtual ~FromAllSegments() {};
  virtual CSkeletonSegmentVector *getSegments(CSkeletonBase *skeleton);
};

class FromSelectedSegments : public SegmentChooser {
public:
  FromSelectedSegments() {};
  virtual ~FromSelectedSegments() {};
  virtual CSkeletonSegmentVector *getSegments(CSkeletonBase *skeleton);
};

class FromSelectedElements : public SegmentChooser {
public:
  FromSelectedElements() {};
  virtual ~FromSelectedElements() {};
  virtual CSkeletonSegmentVector *getSegments(CSkeletonBase *skeleton);
};

 /******************************************************

		      TARGETS

 *******************************************************/

 class RefinementTargets {
 protected:
   SegmentMarks segmentMarks;
 public:
   RefinementTargets() {}
   virtual ~RefinementTargets() {}
   virtual void createSegmentMarks(CSkeletonBase *skeleton,
				   RefinementCriterion *criterion, short d) = 0;
   void markSegment(CSkeletonSegment *segment, short d);
   void markElement(CSkeletonElement *element, short d);
   void mark(CSkeletonNode *n1, CSkeletonNode *n2, short d);
   void signature(const CSkeletonElement *element, RefinementSignature *sig)
     const;
 };

 class CheckAllElements : public RefinementTargets {
 public:
   CheckAllElements() {}
   ~CheckAllElements() {}
   virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
 };

 class CheckSelectedElements : public RefinementTargets {
 public:
   CheckSelectedElements() {}
   ~CheckSelectedElements() {}
   virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
 };

 class CheckElementsInGroup : public RefinementTargets{
 private:
   const std::string group;
 public:
   CheckElementsInGroup(const std::string &g) : group(g) {}
   ~CheckElementsInGroup() {}
   virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
 };

 class CheckHomogeneity : public RefinementTargets{
 private:
   double threshold;
 public:
   CheckHomogeneity(double th) : RefinementTargets() {threshold = th;};
   ~CheckHomogeneity() {};
   virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
 };

class CheckHeterogeneousEdges : public RefinementTargets {
private:
  double threshold;
  SegmentChooser *chooser;
public:
  CheckHeterogeneousEdges(double t, SegmentChooser *choozer) 
    : threshold(t), chooser(choozer)
  {}
  virtual ~CheckHeterogeneousEdges() {delete chooser;};
  virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
};

class CheckSelectedEdges : public RefinementTargets {
public:
  CheckSelectedEdges() {}
  virtual ~CheckSelectedEdges() {}
  virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
};

class CheckSegmentsInGroup : public RefinementTargets {
private:
  const std::string group;
public:
  CheckSegmentsInGroup(const std::string &g) : group(g) {}
  ~CheckSegmentsInGroup() {}
  virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
};

class CheckSelectedFaces : public RefinementTargets {
public:
  CheckSelectedFaces() {}
  virtual ~CheckSelectedFaces() {}
  virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
};

class CheckFacesInGroup: public RefinementTargets {
private:
  const std::string group;
public:
  CheckFacesInGroup(const std::string &g) : group(g) {}
  ~CheckFacesInGroup() {}
  virtual void createSegmentMarks(CSkeletonBase*, RefinementCriterion*, short);
};


/******************************************************

                      CRITERION

*******************************************************/

class RefinementCriterion {
public:
  RefinementCriterion() {};
  virtual ~RefinementCriterion() {};
  virtual bool isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable) const 
  = 0;
};

class Unconditionally : public RefinementCriterion {
public:
  Unconditionally() : RefinementCriterion() {}
  ~Unconditionally() {}
  virtual bool isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable) const
  {
    return true;
  }
};

class MinimumVolume : public RefinementCriterion {
private:
  double threshold;
  std::string units;
public:
  MinimumVolume(double t, std::string *u) : RefinementCriterion(), threshold(t), units(*u) {};
  MinimumVolume(double t) : RefinementCriterion(), threshold(t) {}
  ~MinimumVolume() {}
  virtual bool isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable) const;
};

class MinimumArea : public RefinementCriterion {
private:
  double threshold;
  std::string units;
public:
  MinimumArea(double t, std::string *u) : RefinementCriterion(), threshold(t), units(*u) {};
  MinimumArea(double t) : RefinementCriterion(), threshold(t) {}
  ~MinimumArea() {}
  virtual bool isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable) const;
};

class MinimumLength : public RefinementCriterion {
private:
  double threshold;
  std::string units;
public:
  MinimumLength(double t, std::string *u) : RefinementCriterion(), threshold(t), units(*u) {};
  MinimumLength(double t) : RefinementCriterion(), threshold(t) {}
  ~MinimumLength() {}
  virtual bool isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable) const;
};

#endif	// CREFINEMENTCRETERION_H

