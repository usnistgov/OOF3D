// -*- C++ -*-
// $RCSfile: array.h,v $
// $Revision: 1.32.10.10 $
// $Author: langer $
// $Date: 2014/05/29 13:47:28 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Template for a two dimensional array.  Indexing is done either with
// ICoords or an STL-style iterator.  The template argument is the
// type of the array element.

// Constructors:
//	Array<TYPE>::Array(int width, int height);
//	Array<TYPE>::Array(ICoord &size);	size(0)=width, size(1)=height
//      Array<TYPE>::Array(ICoord &size, const TYPE &val);
//      Array<TYPE>::Array(const ICRectangle&); [ICRectangularPrism in 3D]
//      Array<TYPE>::Array(const ICoord&, ArrayData<TYPE>*);

// STL-style Iterators:
// To loop over an array, there is a typedef
//	Array<TYPE>::iterator
// and functions
//	Array<TYPE>::iterator Array<TYPE>::begin();
//	Array<TYPE>::iterator Array<TYPE>::end();
// Use them like this:
//	Array<TYPE> array(size);
//	for(Array<TYPE>::iterator i=array.begin(); i!= array.end(); ++i) {
//	   array[i] = whatever;
//	   *i = whatever;    // *i is the same as array[i]
//      }
// If you need to know the actual position of the iterator, use
//	const ICoord &Array<TYPE>::iterator::coord();
// There are corresponding const_iterator versions of the iterators
// for looping over const arrays.

// To loop over only part of an array, first construct a subarray by
// calling
//	Array<TYPE> Array<TYPE>::subarray(const ICoord&, const ICoord&);
// and use the subarray's begin() and end() iterators.  The ICoord
// arguments are two diagonally opposite corners of the subarray.  The
// right and top edges of the subarray are NOT included in the
// iteration.  That means that
//	ICoord size;
//	Array<TYPE> a = array(size);
//	Array<TYPE> b = a.subarray(ICoord(0,0), size);
// makes a and b effectively identical.
// Subarrays *share* their data with the original array.  They are not
// completely independent objects.  The shared data is reference
// counted, however, so it's safe to destroy an array before
// destroying its subarrays.

// Non-STL style access:
// Array<TYPE>::operator[](ICoord &index)

// The ICoord argument must fall within the array bounds.  If the
// array was created like this:
//	Array<TYPE> array(ICoord(w, h));
// then
//	0 <= index(0) < w
//	0 <= index(1) < h
// If the array is a subarray,
//	Array<TYPE> array=otherarray.subarray(ICoord(lft,btm), ICoord(rgt,top))
// then
// 	lft <= index(0) < rgt
//	btm <= index(1) < top
// assuming that lft <= rgt and btm <= top.

// The copy constructor does not make a new independent array, it
// makes a copy that shares its data with the original. To make a
// real, independent copy, use
//	Array<TYPE>::clone().

// Utility functions:
//	ICoord Array<TYPE>::size()
//	int Array<TYPE>::width()
//	int Array<TYPE>::height()
//	bool Array<TYPE>::contains(ICoord&)
//	void Array<TYPE>::resize(ICoord&)   -- Don't use on subarrays!
//      void Array<TYPE>::clear(const TYPE &t) -- Sets all entries to t
// The first three functions, acting on a subarray, return the actual
// size, not the magnitude of the largest possible index.  That is, for
//	Array<TYPE> array=otherarray.subarray(ICoord(1,1), ICoord(5,5));
// we get
// 	array.size() == ICoord(4,4)


#ifndef ARRAY_H
#define ARRAY_H

#include <oofconfig.h>
#include "coord.h"		// for ICoord
#include "geometry.h"		// for ICRectangle
#include <iostream>
#include <string.h>		// for memcpy
#include <assert.h>

template <class TYPE> class Array;
template <class TYPE> class ArrayIterator;
template <class TYPE> class ConstArrayIterator;

// ArrayData is a reference counted storage for the Array contents.
// The reference counting is used NOT to prevent or delay copying when
// creating a new array, but rather to create subarrays that share
// data with the main array.  When changing data values, the Array
// does not make sure that it's the only referer to the ArrayData (ie,
// there is NO copy-on-write semantics).

template <class TYPE>
class ArrayData {
private:
  friend class Array<TYPE>;	// our only friend in the whole wide world
#if DIM == 2
  TYPE **data;
#elif DIM == 3
  TYPE ***data;
#endif
  ArrayData(const ICoord &size)
    : refcount(0), size(size)
  {
    allocate();
  }
  ArrayData(const ArrayData<TYPE> &other)
    : refcount(1), size(other.size)
  {
    allocate();
    copy(other);
  }
  ~ArrayData() {
    free();
  }
  void allocate() {
    int i;

#if DIM == 2
    data = new TYPE*[size[1]];
    if(!data) {
      std::cerr << "ArrayData: Failed to allocate array of " << size[1]
		<< " pointers!" << std::endl;
      exit(1);			// should throw an exception 
    }
		
    // Size can be 0x0, in which case dereferencing "data" is not allowed.
    if (size[1]>0) {
      data[0] = new TYPE[size[0]*size[1]];
      if(!data[0]) {
	std::cerr << "ArrayData: Failed to allocate array of " << size 
		  << " objects of size " << sizeof(TYPE) << "!" << std::endl;
	exit(1);			// should throw an exception here.
      }
    }
		
		// set the pointers to point to the right part of the 1D array.
    for(i=1; i<size[1]; i++) 
      data[i] = data[i-1] + size[0];
    
#elif DIM == 3
    int j;
    data = new TYPE**[size[2]];
    if(!data) {
      std::cerr << "ArrayData: Failed to allocate array of " << size[2]
		<< " double pointers!" << std::endl;
      exit(1);			// should throw an exception 
    }
    
    for(i=0; i<size[2]; i++){
      data[i] = new TYPE*[size[1]];
      if(!data) {
	std::cerr << "ArrayData: Failed to allocate array of " << size[1]
		  << " pointers!" << std::endl;
	exit(1);			// should throw an exception 
      }
    }
    
    // Size can be 0x0x0, in which case dereferencing "data" is not allowed.
    if (size[2]>0) {
      data[0][0] = new TYPE[size[0]*size[1]*size[2]];
      if(!data[0][0]) {
	std::cerr << "ArrayData: Failed to allocate array of " << size 
		  << " objects of size " << sizeof(TYPE) << "!" << std::endl;
	exit(1);			// should throw an exception here.
      }
    }

    // set the pointers to point to the right part of the 1D array.
    //data[0] = &(data[0][0]);
    
    for(j=1; j<size[1]; j++) {
      data[0][j] = data[0][j-1] + size[0];
    }
    for(i=1; i<size[2]; i++){
      data[i][0] = data[i-1][size[1]-1] + size[0];
      for(j=1; j<size[1]; j++) {
	data[i][j] = data[i][j-1] + size[0];
      }
    }

#endif // DIM==3
  } // allocate
  void resize(const ICoord &newsize) { // destroys contents
    if(newsize == size) return;
    free();			// have to do this *before* setting size!
    size = newsize;
    allocate();
  }
  void free() {
    if(data) {
#if DIM==2
      if (size[1]>0)
	delete [] data[0];
#elif DIM==3
      if (size[2]>0)
	delete [] data[0][0];
      for(int i=0; i<size[2]; i++)
	delete [] data[i];
#endif
      delete [] data;
    }
  }
public:		       // these have to be available to Array subclasses
  int refcount;
  ICoord size;
  void copy(const ArrayData<TYPE> &other) {
#if DIM == 2
    if (size[1]>0) 
      (void) memcpy(data[0], other.data[0], size[0]*size[1]*sizeof(TYPE));
#elif DIM == 3
    if (size[2]>0 && size[1]>0) 
      (void) memcpy(data[0][0], other.data[0][0],
		    size[0]*size[1]*size[2]*sizeof(TYPE));
#endif
  }
  void clear(const TYPE &t) {
#if DIM == 2
    int n = size[0]*size[1];
    if (n>0) {
      TYPE *d = data[0];
      for(int i=0; i<n; i++)
	d[i] = t;
    }
#elif DIM == 3
    int n = size[0]*size[1]*size[2];
    if (n>0) {
      TYPE *d = data[0][0];
      for(int i=0; i<n; i++)
	d[i] = t;
    }

#endif
  }
  TYPE &get(const ICoord &z) {
#if DIM == 2
    return data[z[1]][z[0]];
#elif DIM == 3
    return data[z[2]][z[1]][z[0]];
#endif
  }
  const TYPE &get(const ICoord &z) const {
#if DIM == 2
    return data[z[1]][z[0]];
#elif DIM == 3
    return data[z[2]][z[1]][z[0]];
#endif
  }
};

template <class TYPE>
class Array {
protected:
  ArrayData<TYPE> *dataptr;
#if DIM == 2
  ICRectangle bounds_;
#elif DIM == 3
  ICRectangularPrism bounds_;
#endif
  void allocate() {
    // Allocate space for the full array, even if this is a subarray.
    // This should probably never be called for subarrays.
#ifdef DEBUG
    ICoord c(bounds_.upperright());
    assert(c[0] > 0 && c[1] > 0 && c[2] > 0);
#endif // DEBUG
    dataptr = new ArrayData<TYPE>(bounds_.upperright());
    ++dataptr->refcount;
    findfin();
  }

  void free() {
    if(dataptr && --dataptr->refcount == 0) {
      delete dataptr;
      dataptr = 0;
    }
  }
public:
#if DIM == 2
  Array(int w, int h)
    : dataptr(0), bounds_(ICoord(0,0), ICoord(w,h)) 
  {
    allocate(); 
  }
  Array(const ICoord &size, const TYPE &x0)
     : dataptr(0), bounds_(ICoord(0,0), size)
  {
    allocate();
    clear(x0);
  }
  Array(const ICoord &size, ArrayData<TYPE> *dataptr)
    : dataptr(dataptr), bounds_(ICoord(0,0), size)
  {
    if(!dataptr)
      allocate();
  }
  Array(const ICRectangle &bounds)
    : dataptr(0), bounds_(bounds) 
  {
    allocate();
  }
#elif DIM == 3
  Array(int w, int h, int d)
    : dataptr(0), bounds_(ICoord(0,0,0), ICoord(w,h,d))
  { 
    allocate(); 
  }
  Array(const ICoord &size, const TYPE &x0) 
     : dataptr(0), bounds_(ICoord(0,0,0), size)
  {
    allocate();
    clear(x0); 
  }
  Array(const ICoord &size, ArrayData<TYPE> *dataptr)
    : dataptr(dataptr), bounds_(ICoord(0,0,0), size)
  {
    if(!dataptr)
      allocate();
  }
  Array(const ICRectangularPrism &bounds)
    : dataptr(0), bounds_(bounds) 
  {
    allocate();
  }
#endif	// DIM == 3

  // The copy constructor does not make an independent copy-- it makes
  // a new Array that shares data with the original.  This is the
  // right thing to do when passing a subarray to a function, but the
  // wrong thing to do if you really want to make a copy.  To make an
  // independent copy, use the clone() method.
  Array(const Array &other)
    : dataptr(other.dataptr),
      bounds_(other.bounds_),
      fin(other.fin),
      cfin(other.cfin)
  {
    ++dataptr->refcount;
  }

  // Make a true (deep) copy.
  Array<TYPE> clone() const {
    Array<TYPE> bozo(bounds_);
    bozo.dataptr->copy(*dataptr);
    return bozo;
  }

  void resize(const ICoord &sz) {
    if(sz == size()) return;
#if DIM == 2
    bounds_ = ICRectangle(ICoord(0,0), sz);
#elif DIM == 3
    bounds_ = ICRectangularPrism(ICoord(0,0,0), sz);
#endif
    free();
    allocate();
  }

  virtual ~Array() { free(); }

  inline const ICoord &size() const { return bounds_.size(); }
  inline int width() const { return bounds_.width(); }
  inline int height() const { return bounds_.height(); }
  inline bool contains(const ICoord &point) const {
    return bounds_.contains(point); 
  }
#if DIM == 2
  inline const ICRectangle &bounds() const { return bounds_; }
  inline int lastdim() const { return height(); }
#elif DIM == 3
  inline int depth() const { return bounds_.depth(); }
  inline int lastdim() const { return depth(); }
  inline const ICRectangularPrism &bounds() const { return bounds_; }
#endif

  Array &operator=(const Array &other) {
    // Don't try to use this to overwrite a subarray within another
    // array!  There probably should be a check that prevents this
    // from happening.
    if(this != &other) {
      free();
      bounds_ = other.bounds_;
      dataptr = other.dataptr;
      ++dataptr->refcount;
      findfin();
    }
    return *this;
  }
  
  virtual void clear(const TYPE& t) {
    for(iterator i=begin(); i!=end(); ++i)
      *i = t;
  }
  
  inline TYPE &operator[](const ICoord &z) {
#ifdef DEBUG
    assert(z[0] < bounds_.xmax());
    assert(z[1] < bounds_.ymax());
    assert(z[0] >= bounds_.xmin());
    assert(z[1] >= bounds_.ymin());
#if DIM == 3
    assert(z[2] < bounds_.zmax());
    assert(z[2] >= bounds_.zmin());
#endif
#endif	
    return dataptr->get(z);
  }
  inline const TYPE &operator[](const ICoord &z) const {
#ifdef DEBUG
    assert(z[0] < bounds_.xmax());
    assert(z[1] < bounds_.ymax());
    assert(z[0] >= bounds_.xmin());
    assert(z[1] >= bounds_.ymin());
#if DIM == 3
    assert(z[2] < bounds_.zmax());
    assert(z[2] >= bounds_.zmin());
#endif
#endif	
    return dataptr->get(z);
  }

  TYPE **ptrptr() { return dataptr->data; } // caveat emptor
 
  typedef ArrayIterator<TYPE> iterator;
  typedef ConstArrayIterator<TYPE> const_iterator;

  iterator begin() {
    return ArrayIterator<TYPE>(*this);
  }

  const_iterator begin() const {
    return ConstArrayIterator<TYPE>(*this);
  }

protected:
  // fin and cfin are cached end() iterators, so that they're not
  // recomputed each time a for loop checks its end condition.
  iterator fin;
  const_iterator cfin;
  void findfin() {
    fin = ArrayIterator<TYPE>(*this);
#if DIM == 2
    fin.location = ICoord(bounds_.xmin(), bounds_.ymax());
#elif DIM == 3
    fin.location = ICoord(bounds_.xmin(), bounds_.ymin(), bounds_.zmax());
#endif
    cfin = ConstArrayIterator<TYPE>(*this);
    cfin.location = fin.location;
  }

public:

  // end() returns an iterator that points to the point just after the
  // last point in the iteration order.

  iterator end() {  
    return fin;
  }

  const_iterator end() const {
    return cfin;
  }

  inline TYPE &operator[](const ArrayIterator<TYPE> &iter) {
    return (*this)[iter.location];
  }

  inline const TYPE &operator[](const ConstArrayIterator<TYPE> &iter) const {
    return (*this)[iter.location];
  }

  Array<TYPE> subarray(const ICoord &crnr0, const ICoord &crnr1) {
    Array<TYPE> newarray(dataptr->size, dataptr);
    ++dataptr->refcount;
#if DIM == 2
    newarray.bounds_ = ICRectangle(crnr0, crnr1);
#elif DIM == 3
    newarray.bounds_ = ICRectangularPrism(crnr0, crnr1);
#endif
    newarray.bounds_.restrict(bounds());
    newarray.findfin();
    return newarray;
  }

  const Array<TYPE> subarray(const ICoord &crnr0, const ICoord &crnr1) const {
    Array<TYPE> newarray(dataptr->size, dataptr);
    ++dataptr->refcount;
#if DIM == 2
    newarray.bounds_ = ICRectangle(crnr0, crnr1);
#elif DIM == 3
    newarray.bounds_ = ICRectangularPrism(crnr0, crnr1);
#endif
    newarray.bounds_.restrict(bounds());
    newarray.findfin();
    return newarray;
  }

  friend class ArrayIterator<TYPE>;
  friend class ConstArrayIterator<TYPE>;
  friend std::ostream &operator<<(std::ostream &os, const Array<TYPE> &arr) {
    for(typename Array<TYPE>::const_iterator i=arr.begin(); i!=arr.end(); ++i)
      os << i.coord() << " " << *i << std::endl;
    return os;
  }
};


template <class TYPE>
class ArrayIterator {
private:
  ICoord location;		// current point
  Array<TYPE> *array;		
public:
  ArrayIterator(Array<TYPE> &array)
    : location(array.bounds_.lowerleft()),
      array(&array) {}

  ArrayIterator() : array(0) {}

  void operator++() {
    location[0]++;
    if(location[0] == array->bounds_.xmax()) {
      location[0] = array->bounds_.xmin();
      location[1]++;
#if DIM == 3
      if(location[1] == array->bounds_.ymax()) {
	location[1] = array->bounds_.ymin();
	location[2]++;
      }
#endif
    }
  }

  void reset() {
    location[0] = array->bounds_.xmin();
    location[1] = array->bounds_.ymin();
#if DIM == 3
    location[2] = array->bounds_.zmin();
#endif
  }

  bool done() const {
#if DIM == 2
    if (location[0] == array->bounds_.xmax()-1 && 
	location[1] == array->bounds_.ymax()-1)
      return true;
#elif DIM == 3
    if (location[0] == array->bounds_.xmax()-1 && 
	location[1] == array->bounds_.ymax()-1 && 
	location[2] == array->bounds_.zmax()-1)
      return true;
#endif
    return false;
  }

  inline TYPE &operator*() {
    return (*array)[location];
  }
  inline const ICoord &coord() const { return location; }
  friend
  bool operator==(const ArrayIterator<TYPE> &a, const ArrayIterator<TYPE> &b)
  {
    return a.location == b.location;
  }
  friend
  bool operator!=(const ArrayIterator<TYPE> &a, const ArrayIterator<TYPE> &b)
  {
    return a.location != b.location;
  }
  friend class Array<TYPE>;
  friend std::ostream &operator<<(std::ostream &os,
				  const ArrayIterator<TYPE>& iter)
  {
    return os << iter.location;
  }
};

template <class TYPE>
class ConstArrayIterator {
private:
  ICoord location;		// current point
  const Array<TYPE> *array;
public:
  ConstArrayIterator(const Array<TYPE> &array)
    : location(array.bounds_.lowerleft()), 
      array(&array)
  {}
  ConstArrayIterator() : array(0) {}
  void operator++() {
    location[0]++;
    if(location[0] == array->bounds_.xmax()) {
      location[0] = array->bounds_.xmin();
      location[1]++;
#if DIM == 3
			if(location[1] == array->bounds_.ymax()) {
				location[1] = array->bounds_.ymin();
				location[2]++;
			}
#endif
    }
  }
  inline const TYPE &operator*() {
    return (*array)[location];
  }
  inline const ICoord &coord() const { return location; }

  bool done() const {
#if DIM == 2
    if (location[0] == array->bounds_.xmax()-1 && 
	location[1] == array->bounds_.ymax()-1)
      return true;
#elif DIM == 3
    if (location[0] == array->bounds_.xmax()-1 && 
	location[1] == array->bounds_.ymax()-1 && 
	location[2] == array->bounds_.zmax()-1)
      return true;
#endif
    return false;
  }

  friend
  bool operator==(const ConstArrayIterator<TYPE> &a,
		  const ConstArrayIterator<TYPE> &b)
  {
    return a.location == b.location;
  }
  friend
  bool operator!=(const ConstArrayIterator<TYPE> &a,
		  const ConstArrayIterator<TYPE> &b)
  {
    return !(a.location == b.location);
  }
  friend class Array<TYPE>;
  friend std::ostream &operator<<(std::ostream &os,
				  const ConstArrayIterator<TYPE>& iter)
  {
    return os << iter.location;
  }
};


#endif
