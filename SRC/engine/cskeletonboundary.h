// -*- C++ -*-
// $RCSfile: cskeletonboundary.h,v $
// $Revision: 1.1.2.32 $
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

#include <oofconfig.h>

#ifndef CSKELETONBOUNDARY_H
#define CSKELETONBOUNDARY_H

#include <string>
#include "common/pythonexportable.h"
// #include "engine/cskeletonnode2.h"
#include "engine/cskeletonsegment.h"
// #include "engine/cskeletonface.h"
#include "engine/cskeletonselectable_i.h"

class CSkeleton;


class CSkeletonBoundary;
typedef std::map<std::string, CSkeletonBoundary*> CSkeletonBoundaryMap;

class CSkeletonPointBoundary;
typedef std::map<std::string, CSkeletonPointBoundary*> CSkeletonPointBoundaryMap;

class CSkeletonEdgeBoundary;
typedef std::map<std::string, CSkeletonEdgeBoundary*> CSkeletonEdgeBoundaryMap;

class CSkeletonFaceBoundary;
typedef std::map<std::string, CSkeletonFaceBoundary*> CSkeletonFaceBoundaryMap;


class CSkeletonBoundary : public PythonExportable<CSkeletonBoundary> {
protected:
  std::string name_;
  static const std::string modulename_;

 public:
  CSkeletonBoundary(const std::string &n);
  virtual ~CSkeletonBoundary();
  virtual const std::string &modulename() const { return modulename_; }
  const std::string &get_name() { return name_; }
  void rename(const std::string &newname) { name_=newname; }
  virtual int size() const = 0;
  virtual bool empty() const = 0;
  virtual void remove() = 0;
  virtual bool exterior() { return false; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeletonPointBoundary : public CSkeletonBoundary {
protected:
  CSkeletonNodeSet nodes;
  static const std::string classname_;

public:
  CSkeletonPointBoundary(const std::string &n) : CSkeletonBoundary(n) {}
  virtual ~CSkeletonPointBoundary() {}
  virtual int size() const { return nodes.size(); }
  virtual bool empty() const { return nodes.empty(); }
  void addNode(CSkeletonNode *n) { nodes.insert(n); }
  void appendNodes(const CSkeletonNodeVector*);
  void removeNodes(const CSkeletonNodeVector*);
  void remove() { nodes.clear(); }
  bool hasNode(const CSkeletonNode*) const;
  const CSkeletonNodeSet *getNodes() const { return &nodes; }
  CSkeletonPointBoundary *map(CSkeleton *new_skeleton, SkeletonMapDir direction,
			      bool exterior);

  virtual const std::string &classname() const { return classname_; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ExteriorCSkeletonPointBoundary : public CSkeletonPointBoundary {
protected:
  static const std::string classname_;
public:
  ExteriorCSkeletonPointBoundary(const std::string &n)
    : CSkeletonPointBoundary(n) {}
  virtual ~ExteriorCSkeletonPointBoundary() {}
  virtual bool exterior() { return true; }
  virtual const std::string &classname() const { return classname_; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeletonEdgeBoundary : public CSkeletonBoundary {
protected:
  OrientedCSkeletonSegmentVector oriented_segments;
  static const std::string classname_;

public:
  CSkeletonEdgeBoundary(const std::string &n) : CSkeletonBoundary(n) {}
  virtual ~CSkeletonEdgeBoundary();
  virtual int size() const { return oriented_segments.size(); }
  virtual bool empty() const { return oriented_segments.empty(); }
  void addOrientedSegment(OrientedCSkeletonSegment *s) {
    oriented_segments.push_back(s);
  }
  void remove() { oriented_segments.clear(); } 
  bool try_appendSegs(const CSkeletonSegmentVector*) const;
  void appendSegs(const CSkeletonSegmentVector*);
  void appendSegs(const OrientedCSkeletonSegmentVector&);
  bool try_removeSegs(const CSkeletonSegmentVector*) const;
  void removeSegs(const CSkeletonSegmentVector*);
  void reverse();
  double length() const;
  bool hasSegment(const CSkeletonSegment*) const;

  // TODO 3.1: Why does getSegments() return OrientedCSegments?  This is
  // inconsistent.  I've added getOrientedSegments() below, which is
  // the same as getSegments.  Check that all getSegments() calls have
  // been changed to getOrientedSegments(), then rename
  // getUnorientedSegments() to getSegments().  [There are methods
  // named 'getSegments" in other classes too.  Be careful!]
  const OrientedCSkeletonSegmentVector *getSegments() const;
  const OrientedCSkeletonSegmentVector *getOrientedSegments() const;
  CSkeletonSegmentVector *getUnorientedSegments() const;

  CSkeletonNodeVector *getNodes() const; // for tests

  CSkeletonEdgeBoundary *map(CSkeleton *new_skeleton, SkeletonMapDir direction,
			     bool exterior);

  static bool getOrientedSegs(OrientedCSkeletonSegment*,
			      CSkeletonSelectableList*, 
			      SkeletonMapDir, OrientedCSkeletonSegmentVector&);

  virtual const std::string &classname() const { return classname_; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ExteriorCSkeletonEdgeBoundary : public CSkeletonEdgeBoundary {
protected:
  static const std::string classname_;

public:
  ExteriorCSkeletonEdgeBoundary(const std::string &n)
    : CSkeletonEdgeBoundary(n) {}
  virtual ~ExteriorCSkeletonEdgeBoundary() {}
  //addEdge() checks if edge is exterior
  virtual bool exterior() { return true; }

  virtual const std::string &classname() const { return classname_; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeletonFaceBoundary : public CSkeletonBoundary {
protected:
  // The OrientedSurface may be created before the boundary, so it's a
  // pointer.  The boundary takes over ownership of it.
  OrientedSurface *oriented_faces;
  //  OrientedCSkeletonFaceSet oriented_faces;
  static const std::string classname_;

public:
  CSkeletonFaceBoundary(const std::string &n);
  virtual ~CSkeletonFaceBoundary();
  void setSurface(OrientedSurface *surface);
  virtual int size() const;
  virtual bool empty() const;
  void addOrientedFace(OrientedCSkeletonFace *s);
  void remove();
  void reverse();
  bool try_appendFaces(const CSkeletonBase*, const CSkeletonFaceVector*) const;
  void appendFaces(const OrientedCSkeletonFaceSet&);
  void appendFaces(const CSkeletonBase*, const CSkeletonFaceVector*);
  bool try_removeFaces(const CSkeletonBase*, const CSkeletonFaceVector*) const;
  void removeFaces(const CSkeletonBase*, const CSkeletonFaceVector*);
  // TODO 3.1: Fix the names here.  getFaces should return the unoriented
  // faces, and there should be a getOrientedFaces method.
  const OrientedCSkeletonFaceSet *getFaces() const;
  CSkeletonFaceVector *getUnorientedFaces() const;
  double area() const;
  CSkeletonFaceBoundary *map(CSkeleton *new_skeleton, SkeletonMapDir direction,
			     bool exterior);
  bool hasFace(const CSkeletonFace*) const;

  virtual const std::string &classname() const { return classname_; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ExteriorCSkeletonFaceBoundary : public CSkeletonFaceBoundary {
protected:
  static const std::string classname_;

public:
  ExteriorCSkeletonFaceBoundary(const std::string &n) 
    : CSkeletonFaceBoundary(n)
  {}
  virtual ~ExteriorCSkeletonFaceBoundary() {}
  //addFace() checks if face is exterior
  virtual bool exterior() { return true; }

  virtual const std::string &classname() const { return classname_; }
};

#endif

