// -*- C++ -*-
// $RCSfile: edgeset.h,v $
// $Revision: 1.15.4.7 $
// $Author: langer $
// $Date: 2014/11/05 16:54:24 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef EDGESET_H
#define EDGESET_H

class EdgeSet;
class EdgeSetIterator;
class FaceSet;
class FaceSetIterator;
class SubDimensionalIterator;
class SubDimensionalSet;

#include "common/doublevec.h"
#include "engine/edge.h"
//#include "femesh.h"
#include <vector>
#include <set>

class Element;
class FEMesh;
class FuncNode;

// The SubDimensionalSet subclasses, EdgeSet and FaceSet, have all of
// the information about the geometry of an EdgeBoundary or
// FaceBoundary.  For integration, they provide gausspoints, weights,
// and the direction of the normal vector.  They also provide a
// guaranteed-unique way of getting out the FuncNodes of which it is
// composed.

class SubDimensionalSet {
protected:
  FEMesh *mesh;
  std::vector<Element*> parts;	// edges or faces
  std::vector<bool> directions;
public:
  SubDimensionalSet(FEMesh*);
  virtual ~SubDimensionalSet() {}
  int size() const { return parts.size(); }
  bool empty() const { return parts.empty(); }
  void add(Element*, bool);
  virtual SubDimensionalIterator *iterator() const = 0;
  friend class SubDimensionalIterator;
};

class SubDimensionalIterator {
protected:
  const SubDimensionalSet *bdy;	// EdgeSet or FaceSet being iterated over
  unsigned int index_;
public:
  SubDimensionalIterator(const SubDimensionalSet*);
  Element *part() const { return bdy->parts[index_]; }
  bool reversed() const { return bdy->directions[index_]; }
  void operator++() { index_++; }
  bool end() const { return index_ == bdy->parts.size(); }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class EdgeNodeDistance;


class EdgeSet : public SubDimensionalSet {
public:
  EdgeSet(FEMesh *m) : SubDimensionalSet(m) {}
  virtual ~EdgeSet() {}

  std::vector<const EdgeNodeDistance*> *ndlist();
  virtual SubDimensionalIterator *iterator() const;

  friend class EdgeSetIterator;
};

class EdgeSetIterator : public SubDimensionalIterator {
private:
  DoubleVec cumulength_;
  double length;
public:
  EdgeSetIterator(const EdgeSet *es);
  Element* edge() const { return part(); }
  double traversed_length() const { return cumulength_[index_]; }
  double total_length() const { return length; };
};

std::ostream &operator<<(std::ostream&, const EdgeSetIterator&);


// Progress along an EdgeNode is measured not only by nodes, but also
// by cumulative and fractional distance along the edge, as well as
// node index.  These data are encapsulated in this object for
// convenience.
class EdgeNodeDistance {
public:
  const FuncNode *node;
  int index;
  double distance;
  double fraction;
  EdgeNodeDistance(const FuncNode *fn, int i, double d, double f) :
    node(fn), index(i), distance(d), fraction(f) {}
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==3

class FaceSet : public SubDimensionalSet {
public:
  FaceSet(FEMesh *mesh) : SubDimensionalSet(mesh) {}
  virtual ~FaceSet() {}

  // FaceSetIterator face_iterator() const;
  void addFace(Element*, bool);
  std::set<Node*> *getNodes() const;
  virtual SubDimensionalIterator *iterator() const;
  friend class FaceSetIterator;
};

class FaceSetIterator : public SubDimensionalIterator {
public:
  FaceSetIterator(const FaceSet *fs) : SubDimensionalIterator(fs) {}
  Element *face() const { return part(); }
};

#endif // DIM==3

#endif	// EDGESET_H

