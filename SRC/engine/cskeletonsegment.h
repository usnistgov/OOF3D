// -*- C++ -*-
// $RCSfile: cskeletonsegment.h,v $
// $Revision: 1.1.2.43 $
// $Author: langer $
// $Date: 2014/12/14 22:49:15 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CSKELETONSEGMENT_H
#define CSKELETONSEGMENT_H

#include "common/coord_i.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonselectable.h"
#include <vtkLine.h>
#include <vtkPoints.h>
#include <vtkSmartPointer.h>


class CSkeletonSegment : public CSkeletonMultiNodeSelectable {
private: 
  int nelements;
  static const std::string modulename_;
  static const std::string classname_;

public:
  CSkeletonSegment(CSkeletonNodeVector *ns);
  virtual ~CSkeletonSegment();

  virtual const std::string &modulename() const { return modulename_; }
  virtual const std::string &classname() const { return classname_; }

  virtual CSkeletonSegment *new_child(int idx, vtkSmartPointer<vtkPoints> pts);

  double length() const;
  double lengthInVoxelUnits(const CMicrostructure *MS) const;
  double lengthInFractionalUnits(const CMicrostructure *MS) const;
  virtual double homogeneity(const CMicrostructure *MS) const;
  int dominantPixel(const CMicrostructure*) const;
  void increment_nelements();
  void decrement_nelements();
  int num_elements() const { return nelements; }
  virtual void getElements(const CSkeletonBase*, ConstCSkeletonElementVector&)
    const;
  virtual void getElements(const CSkeletonBase*, CSkeletonElementVector&);
  const CSkeletonElement *getElement(const CSkeletonBase*, int) const;
  virtual int nElements() const { return nelements; }

  virtual vtkSmartPointer<vtkCell> getEmptyVtkCell() const;
  virtual VTKCellType getCellType() const { return VTK_LINE; }

  CSkeletonNode *get_other_node(const CSkeletonNode *n) {
    return (n == (*nodes)[0] ? (*nodes)[1] : (*nodes)[0] );
  }

  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class OrientedCSkeletonSegment {
protected:
  CSkeletonSegment *segment;
  int direction;

public:
  OrientedCSkeletonSegment(CSkeletonSegment *s, int d=1)
    : segment(s), direction(d)
  {}
  ~OrientedCSkeletonSegment() {}

  void set_direction(const CSkeletonNode *n0, const CSkeletonNode *n1);
  void set_direction(const CSkeletonNode*);
  void reverse() { direction *= -1; }
  VTKCellType getCellType() const {return VTK_LINE;}
  CSkeletonSegment *get_segment() const { return segment; }
  Coord get_direction_vector();
  vtkSmartPointer<vtkIdList> getPointIds() const;

  CSkeletonNode *getNode(int i) const {
    return (direction == 1 ?
	    segment->getNode(i) : segment->getNode(1-i));
  }
  //void edgesFromSegs(CSkeletonSelectable

  // TODO MER: Get rid of this, replace it with sequenceSegments, below.
  static bool segSequence(const CSkeletonSelectableList *seglist,
  			  CSkeletonNode *start,  
  			  CSkeletonSegmentVector &sequenced_segs,
  			  CSkeletonNodeVector &sequenced_nodes);

  friend bool operator==(const OrientedCSkeletonSegment &s1,
			 const OrientedCSkeletonSegment &s2)
  {
    return (s1.getNode(0)->getIndex() == s2.getNode(0)->getIndex() && 
	    s1.getNode(1)->getIndex() == s2.getNode(1)->getIndex());
  }  
  friend bool operator!=(const OrientedCSkeletonSegment &s1,
			 const OrientedCSkeletonSegment &s2) {
    return !(s1.getNode(0)->getIndex() == s2.getNode(0)->getIndex() && 
	     s1.getNode(1)->getIndex() == s2.getNode(1)->getIndex());
  }

  friend std::ostream &operator<<(std::ostream&, 
				  const OrientedCSkeletonSegment&);
};

typedef std::vector<OrientedCSkeletonSegment*> OrientedCSkeletonSegmentVector;
typedef std::set<OrientedCSkeletonSegment*> OrientedCSkeletonSegmentSet;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility class that packages the outputs from sequenceSegments.
// This class is opaque in python, so there's little overhead in
// passing it back and forth between languages.

class SegmentSequence {
public:
  ~SegmentSequence();
  OrientedCSkeletonSegmentVector segments;
  bool closed() const;
  void reverse();
  Coord span() const;		// last point - first point
  OrientedCSkeletonSegmentVector::const_iterator begin() const;
  OrientedCSkeletonSegmentVector::const_iterator end() const; 
  double projectedArea(const std::string &projection) const;
};

SegmentSequence *sequenceSegments(const CSkeletonSegmentVector *segments,
				  CSkeletonNode *startNode);		 

typedef std::map<CSkeletonNode*, CSkeletonSegmentList> AdjacencyMap;
AdjacencyMap findAdjacency(const CSkeletonSegmentVector*);

#endif	// CSKELETONSEGMENT_H



