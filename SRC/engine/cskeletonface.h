// -*- C++ -*-
// $RCSfile: cskeletonface.h,v $
// $Revision: 1.1.2.47 $
// $Author: langer $
// $Date: 2014/12/14 22:49:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CSKELETONFACE_H
#define CSKELETONFACE_H

#include "common/coord_i.h"
#include "engine/cskeletonselectable.h"

#include <vtkPoints.h>
#include <vtkSmartPointer.h>
#include <vtkTriangle.h>

class CSkeletonNode;

class CSkeletonFace : public CSkeletonMultiNodeSelectable {
private:
  int nelements;
  static const std::string modulename_;
  static const std::string classname_;

  static long globalFaceCount;

public:
  CSkeletonFace(CSkeletonNodeVector *ns); 
  virtual ~CSkeletonFace();

  virtual const std::string &modulename() const { return modulename_; }
  virtual const std::string &classname() const { return classname_; }

  virtual CSkeletonFace *new_child(int idx, vtkSmartPointer<vtkPoints> pts);
  
  virtual VTKCellType  getCellType() const { return VTK_TRIANGLE; }
  virtual vtkSmartPointer<vtkCell> getEmptyVtkCell() const;

  virtual double homogeneity(const CMicrostructure*) const;

  double area() const;		// always non-negative!
  double areaInVoxelUnits(const CMicrostructure *MS) const;
  double areaInFractionalUnits(const CMicrostructure *MS) const;
  void increment_nelements();
  void decrement_nelements();
  virtual int nElements() const { return nelements; }
  Coord normal() const;
  virtual void getElements(const CSkeletonBase *skel,
			   ConstCSkeletonElementVector&) const;
  virtual void getElements(const CSkeletonBase *skel, CSkeletonElementVector&);
  const CSkeletonElement *getElement(const CSkeletonBase*, int) const;
  
  CSkeletonNode *get_other_node(const CSkeletonSegment *s) const;
  const CSkeletonElement *get_other_element(const CSkeletonBase*,
					    const CSkeletonElement*) const;

  bool contains(const Coord&) const;
  virtual void print(std::ostream&) const;

  friend long get_globalFaceCount();
};

long get_globalFaceCount();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class OrientedCSkeletonFace {
private:
  static long globalOrientedFaceCount;
  OrientedCSkeletonFace(const OrientedCSkeletonFace&);
protected:
  CSkeletonFace *face;
  int direction;

public:
  OrientedCSkeletonFace(CSkeletonFace *f, int d=1);
  ~OrientedCSkeletonFace();

  void set_direction(const CSkeletonNode *n0, const CSkeletonNode *n1, 
		     const CSkeletonNode *n2);
  VTKCellType getCellType() const { return VTK_TRIANGLE; }
  CSkeletonFace *get_face() const { return face; }
  int nnodes() const { return face->nnodes(); }

  Coord get_direction_vector() const;
  int get_direction() const { return direction; }
  void reverse() { direction *= -1; }
  CSkeletonNode *getNode(int i) const;
  double get_offset() const;

  vtkSmartPointer<vtkIdList> getPointIds() const;

  friend bool operator==(const OrientedCSkeletonFace &f1,
			 const OrientedCSkeletonFace &f2);
  friend bool operator!=(const OrientedCSkeletonFace &f1,
			 const OrientedCSkeletonFace &f2);
  friend bool operator<(const OrientedCSkeletonFace &f1,
			const OrientedCSkeletonFace &f2);

  void print(std::ostream &os) const { face->print(os); }

  // sort by multinode key for definitive comparison
  static bool ltKey(const OrientedCSkeletonFace *f1,
		    const OrientedCSkeletonFace *f2);

  friend long get_globalOrientedFaceCount();
};

long get_globalOrientedFaceCount();

std::ostream& operator<<(std::ostream&, const OrientedCSkeletonFace&);

// functors used by sorting algorithm for containers of pointers
struct OrientedFaceLTUid {
  bool operator()(const OrientedCSkeletonFace *f1,
		  const OrientedCSkeletonFace *f2) 
    const 
  {
    return *f1 < *f2;
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility class that packages an oriented set of faces.  Analogous to
// SegmentSequence in cskeletonsegment.h.

class OrientedSurface {
private:
  bool closed_;
public:
  OrientedSurface();
  ~OrientedSurface();
  OrientedCSkeletonFaceSet faces;

  void insert(OrientedCSkeletonFace *f) { faces.insert(f); }
  void insert(const OrientedCSkeletonFaceSet::iterator &start,
	      const OrientedCSkeletonFaceSet::iterator &end) 
  {
    faces.insert(start, end);
  }
  void remove(CSkeletonFace*);
  void clear();
  void reverse();
  unsigned int size() const { return faces.size(); }
  bool empty() const { return faces.empty(); }
  void setClosed(bool c) { closed_ = c; }
  bool closed() const { return closed_; }
  Coord normal() const;
  double volume() const;
  OrientedCSkeletonFaceSet::const_iterator begin() const;
  OrientedCSkeletonFaceSet::const_iterator end() const;
private:
  OrientedSurface(const OrientedSurface&); // not implemented
  OrientedSurface &operator=(const OrientedSurface&); // not implemented
};

OrientedSurface *orientFaces(const CSkeletonBase*, 
			     const CSkeletonFaceVector*,
			     OrientedCSkeletonFace*);
bool augmentSurface(const CSkeletonBase*,
		    CSkeletonSegmentSet&, SegFaceMap&, SegFaceListMap&,
		    OrientedSurface*);

#endif	// CSKELETONFACE_H



