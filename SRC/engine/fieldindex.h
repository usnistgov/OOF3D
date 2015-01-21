// -*- C++ -*-
// $RCSfile: fieldindex.h,v $
// $Revision: 1.20.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:44:24 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef FIELDINDEX_H
#define FIELDINDEX_H

#include <iostream>
#include <string>
#include <vector>
#include "engine/indextypes.h"
#include "engine/planarity.h"


// Classes for referring to the components of a field, flux, or
// equation.  Having different types all derived from a common base
// class allows the same code to handle scalars, vectors, and tensors.
// The base class is called 'FieldIndex' because it's commonly used to
// choose the components of a Field, and because
// 'FieldFluxEquationOrOtherIndexableObjectIndex' is too long.

class FieldIterator;
class OutputValue;

class FieldIndex {
public:
  FieldIndex() {}
  virtual ~FieldIndex() { }
  virtual FieldIndex *cloneIndex() const = 0; // create a copy
  // The possible values of the index must be ordered in some
  // (possibly arbitrary) way, so that, for example, the corresponding
  // degrees of freedom of a Field at a Node can be listed in order.
  // FieldIndex::integer() returns the rank of the index in this
  // arbitrary ordering.  For example, the VectorFieldIndex just
  // returns the value of the index, and the SymTensorIndex returns
  // the index's Voigt representation.
  virtual int integer() const = 0;
  // in_plane() is false if the index represents an out-of-plane
  // component of a field.
  virtual bool in_plane() const = 0;
  // Set the value of the index by passing in a vector of ints.
  // Inefficient, but general.
  virtual void set(const std::vector<int>*) = 0;
  // Return the value of the index as a vector of ints.  The vector
  // needs to be deleted by the caller.
  virtual std::vector<int>* components() const = 0;

  virtual void print(std::ostream &os) const = 0;
  virtual const std::string &shortstring() const = 0;
};

std::ostream &operator<<(std::ostream &os, const FieldIndex &fi);

// operator== should only be used in contexts where it's clear that
// the two FieldIndices have the same subclass.

bool operator==(const FieldIndex&, const FieldIndex&);

// The ScalarFieldIndex has no value, which is not to say that it is
// worthless.  It just doesn't do anything.

class ScalarFieldIndex : virtual public FieldIndex {
public:
  ScalarFieldIndex() {}
  virtual ~ScalarFieldIndex() {}
  virtual FieldIndex *cloneIndex() const {
    return new ScalarFieldIndex;
  }
  virtual int integer() const { return 0; }
  virtual bool in_plane() const { return true; }
  virtual void set(const std::vector<int>*) {}
  virtual std::vector<int> *components() const;	// returns a zero-length vector
  virtual void print(std::ostream&) const;
  virtual const std::string &shortstring() const;
};


// The VectorFieldIndex stores a single int.

class VectorFieldIndex : virtual public FieldIndex {
protected:
  int index_;
public:
  VectorFieldIndex() : index_(0) {}
  VectorFieldIndex(SpaceIndex i) : index_(i) {}
  VectorFieldIndex(const VectorFieldIndex &o) : index_(o.index_) {}
  virtual ~VectorFieldIndex() {}
  virtual FieldIndex *cloneIndex() const { return new VectorFieldIndex(*this); }
  virtual int integer() const { return index_; }
  virtual bool in_plane() const { return index_ < 2; }
  virtual void set(const std::vector<int>*);
  void set(int);
  virtual std::vector<int> *components() const;
  virtual void print(std::ostream&) const;
  virtual const std::string &shortstring() const;
};

// The OutOfPlaneVectorFieldIndex is a VectorFieldIndex that only
// represents the out-of-plane part of the vector field.  The only
// substantial difference is in the integer function, which says that
// the 2 (z) component is the first component.

class OutOfPlaneVectorFieldIndex : public VectorFieldIndex {
public:
  OutOfPlaneVectorFieldIndex() : VectorFieldIndex(2) {}
  OutOfPlaneVectorFieldIndex(SpaceIndex i) : VectorFieldIndex(i) {}
  virtual int integer() const { return index_ - 2; }
  virtual FieldIndex *cloneIndex() const {
    return new OutOfPlaneVectorFieldIndex(*this);
  }
};


// The SymTensorIndex stores the Voigt representation of the ij index
// of a 3x3 symmetric tensor.  i and j can be retrieved with the row()
// and col() functions.

//  i j  Voigt
//  0 0  0
//  1 0  5
//  1 1  1
//  2 0  4
//  2 1  3
//  2 2  2

class SymTensorIndex : virtual public FieldIndex {
protected:
  int v;			// voigt index
public:
  SymTensorIndex() : v(0) {}
  SymTensorIndex(SpaceIndex i) : v(i) {}
  SymTensorIndex(SpaceIndex i, SpaceIndex j) : v(i==j? int(i) : int(6-i-j)) {}
  SymTensorIndex(const SymTensorIndex &o) : v(o.v) {}
  virtual ~SymTensorIndex() {}
  virtual FieldIndex *cloneIndex() const { return new SymTensorIndex(*this); }
  virtual int integer() const { return v; }
  int row() const;		// i
  int col() const;		// j
  bool diagonal() const { return v < 3; }
  virtual bool in_plane() const { return v < 2 || v == 5; }
  virtual void set(const std::vector<int>*);
  virtual std::vector<int> *components() const;	// returns new vector
  virtual void print(std::ostream&) const;
  static int ij2voigt(int i, int j) { return ( i==j ? i : 6-i-j ); }
  // The argument str in str2voigt must be "pq" where p and q are in
  // ('x', 'y', 'z')
  static int str2voigt(const std::string &str) {
    return ij2voigt(str[0]-'x', str[1]-'x');
  }
  virtual const std::string &shortstring() const;
};

// See comment above wrt OutOfPlaneVectorFieldIndex.

class OutOfPlaneSymTensorIndex : public SymTensorIndex {
public:
  OutOfPlaneSymTensorIndex() : SymTensorIndex(2) {}
  OutOfPlaneSymTensorIndex(SpaceIndex i) : SymTensorIndex(i) {}
  OutOfPlaneSymTensorIndex(SpaceIndex i, SpaceIndex j) : SymTensorIndex(i,j) {}
  virtual FieldIndex *cloneIndex() const {
    return new OutOfPlaneSymTensorIndex(*this);
  }
  virtual int integer() const { return v - 2; }
};


// Wrapper class so that Fluxes and Fields can return an appropriate
// type of FieldIndex, other classes don't have to worry about
// deallocating it, and the virtual functions still work.

class IndexP {
protected:
  FieldIndex *fieldindex;
public:
  IndexP(FieldIndex *i) : fieldindex(i) {}
  IndexP(const IndexP &o) : fieldindex(o.fieldindex->cloneIndex()) {}
  virtual ~IndexP() { delete fieldindex; }
  int integer() const { return fieldindex->integer(); }
  bool in_plane() const { return fieldindex->in_plane(); }
  operator const FieldIndex&() const { return *fieldindex; }
  IndexP cloneIndex() const {
    return IndexP(fieldindex->cloneIndex());
  }
  void set(const std::vector<int> *comps) { fieldindex->set(comps); }
  std::vector<int> *components() const { // returns new vector
    return fieldindex->components();
  }
  const std::string &shortstring() const {
    return fieldindex->shortstring();
  }
};

std::ostream &operator<<(std::ostream &, const IndexP&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A FieldIterator is a FieldIndex that can be incremented, so it can
// loop over all possible values of the index.  The reason that we
// need separate FieldIterator and FieldIndex classes is that the
// Iterators can have different flavors for iterating over subsets of
// the possible Index values.  In particular, there are in-plane and
// out-of-plane iterators whose constructors take a Planarity
// argument.  We don't always know the planarity in circumstances
// where we need an Index, but we have to know it when we need an
// Iterator.

// Both FieldIndex and FieldIterator need clone() functions, but they
// return different types so they must have different names (since
// FieldIterator is derived from FieldIndex).  A happy side effect is
// that it's possible to call FieldIterator::cloneIndex() to get an
// independent FieldIndex object containing the current state of the
// FieldIterator.


class FieldIterator : virtual public FieldIndex {
public:
  FieldIterator() {}
  virtual ~FieldIterator() {}
  virtual void operator++() = 0; // go to next FieldIndex value
  virtual bool end() const = 0;	// are we there yet?
  virtual void reset() = 0;
  virtual FieldIterator *cloneIterator() const = 0;
};

class ScalarFieldIterator : public ScalarFieldIndex, public FieldIterator
{
private:
  bool done;
public:
  ScalarFieldIterator() : done(false) {}
  ScalarFieldIterator(const ScalarFieldIterator &o) : done(o.done) {}
  virtual ~ScalarFieldIterator() {}
  virtual void operator++() { done = true; }
  virtual bool end() const { return done; }
  virtual void reset() { done = false; }
  virtual FieldIterator *cloneIterator() const {
    return new ScalarFieldIterator(*this);
  }
};

class VectorFieldIterator : public VectorFieldIndex, public FieldIterator
{
private:
  int max;
  int start;
public:
  VectorFieldIterator() : max(3), start(0) {}
  VectorFieldIterator(int i, int dim=3)
    : VectorFieldIndex(i), max(dim), start(i)
  {}
  VectorFieldIterator(const VectorFieldIterator &o)
    :  VectorFieldIndex(o), max(o.max), start(o.start)
  {}
  virtual ~VectorFieldIterator() {}
  virtual void operator++() { index_++; }
  virtual bool end() const { return index_ >= max; }
  virtual void reset() { index_ = start; }
  virtual FieldIterator *cloneIterator() const {
    return new VectorFieldIterator(*this);
  }
};

class OutOfPlaneVectorFieldIterator
  : public OutOfPlaneVectorFieldIndex, public FieldIterator
{
private:
  int max;
public:
  OutOfPlaneVectorFieldIterator() : max(3) {}
  virtual ~OutOfPlaneVectorFieldIterator() {}
  virtual void operator++() { index_++; }
  virtual bool end() const { return index_ >= max; }
  virtual void reset() { index_ = 0; }
  virtual FieldIterator *cloneIterator() const {
    return new OutOfPlaneVectorFieldIterator(*this);
  }
};


class SymTensorIterator : public SymTensorIndex, public FieldIterator {
public:
  SymTensorIterator() {}
  SymTensorIterator(SpaceIndex i) : SymTensorIndex(i) {}
  SymTensorIterator(SpaceIndex i, SpaceIndex j) : SymTensorIndex(i, j) {}
  virtual ~SymTensorIterator() {}
  virtual void operator++() { v++; }
  virtual bool end() const { return v > 5; }
  virtual void reset() { v = 0; }
  virtual FieldIterator *cloneIterator() const {
    return new SymTensorIterator(*this);
  }
};


class SymTensorInPlaneIterator : public SymTensorIterator {
public:
  SymTensorInPlaneIterator() {}
  SymTensorInPlaneIterator(int i) : SymTensorIterator(i) {}
  virtual ~SymTensorInPlaneIterator() {}
  virtual void operator++() { v++; if(v == 2) v = 5; }
  virtual FieldIterator *cloneIterator() const {
    return new SymTensorInPlaneIterator(*this);
  }
//   virtual int len() const { return 3; }
};

// The SymTensorOutOfPlaneIterator loops over the out-of-plane
// components of a SymTensorIndex.  This is different than looping
// over all the components of an OutOfPlaneSymTensorIndex, because the
// integer() functions return different values.  That is, this
// iterator loops over zz, yz, and xz, giving them integer values 2,
// 3, and 4.
class SymTensorOutOfPlaneIterator : public SymTensorIterator {
public:
  SymTensorOutOfPlaneIterator() : SymTensorIterator(2) {}
  SymTensorOutOfPlaneIterator(int i) : SymTensorIterator(i) {}
  virtual ~SymTensorOutOfPlaneIterator() {}
  virtual void operator++() { v++; }
  bool end() const { return v > 4; }
  virtual FieldIterator *cloneIterator() const {
    return new SymTensorOutOfPlaneIterator(*this);
  }
};

// The OutOfPlaneSymTensorIterator loops over all the components of a
// OutOfPlaneSymTensorIndex: zz, yz, xz, with integer values 0, 1, 2.
class OutOfPlaneSymTensorIterator
  : public OutOfPlaneSymTensorIndex, public FieldIterator
{
public:
  virtual ~OutOfPlaneSymTensorIterator() {}
  virtual void operator++() { v++; }
  virtual bool end() const { return v > 4; }
  virtual void reset() { v = 0; }
  virtual FieldIterator *cloneIterator() const {
    return new OutOfPlaneSymTensorIterator(*this);
  }
};

// Wrapper class so that Fluxes and Fields can return an appropriate
// type of iterator, other classes don't have to worry about
// deallocating it, and the virtual functions still work.

class IteratorP : public IndexP {
private:
  // IndexP already stores a pointer to the underlying FieldIndex,
  // which is a base class of the underlying FieldIterator.  So
  // there's no need to store it again -- just cast it to the derived
  // class when it's needed.  Whoops -- that's too slow! Store it instead.
  FieldIterator *fi_;
  FieldIterator *fielditerator() {  return fi_; }
  const FieldIterator *fielditerator() const { return fi_; }
public:
  IteratorP(FieldIterator *i)
    : IndexP(i),
      fi_(dynamic_cast<FieldIterator*>(i))
  {}
  // The copy constructor needs to create a copy of the underlying
  // FieldIterator object.  If we naively used the IndexP copy
  // constructor, we'll get only the FieldIndex part of the
  // FieldIterator.
  IteratorP(const IteratorP &o)
    : IndexP(o.fi_->cloneIterator())
  {
    fi_ = dynamic_cast<FieldIterator*>(fieldindex);
  }
  virtual ~IteratorP() {}
  operator const FieldIndex*() const { return fieldindex; }
  operator const FieldIterator*() const { return fi_; }
  inline void operator++() { fi_->operator++(); }
  inline bool end() const { return fi_->end(); }
  inline void reset() { fi_->reset(); }
  IteratorP cloneIterator() const {
    return IteratorP(fi_->cloneIterator());
  }
};

IteratorP *getSymTensorIterator(Planarity);
OutputValue *newSymTensorOutputValue();

#endif // FIELDINDEX_H
