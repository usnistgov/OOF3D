// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// A simple 3D array class used by vsb.h.

// The template arguments are DATA, ICOORD, and IPRISM.

// DATA is the type of data stored in the array.  The class must have
// a null constructor.

// ICOORD is an integer 3D coordinate class with
//   ICOORD(int, int, int)                   constructor
//   ICOORD ICOORD::operator[](int)          component access
//   const ICOORD& ICOORD::operator[](int)   component access
//   bool operator==(const ICOORD&, const ICOORD&)
//   bool operator!=(const ICOORD&, const ICOORD&)
//   ICOORD operator-(const ICOORD&, const ICOORD&)


// IPRISM is a rectangular prism that provides
//   IPRISM(ICOORD, ICOORD)  constructor, given any two opposite corners
//   ICOORD IPRISM::lowerleftback() returns the corner with the minimum
//            values of x, y, and z.
//   ICOORD IPRISM::upperrightfront() returns the corner with the maximum
//            values of x, y, and z.
//   ICOORD size() const;  number of elements in each direction

// The range of the array indices is given by the IPRISM argument to
// the constructor.  They do not have to start at (0, 0, 0).  If the
// prism is defined by the ICOORDs p0 and p1, where p0[i] < p1[i] for
// i in (0,1,2), then an ICOORD x is a valid index into the array if
// p0[i] <= x[i] < p1[i] for i in (0,1,2).  In other words, it's just
// what you should expect.

// The array defines iterator and const_iterator classes, which act
// like the usual stl iterators, and are returned by the array's
// begin() and end() methods.  Dereferencing an iterator returns the
// array element at that location.  An iterator's coord() method
// returns its current location as an ICOORD.  Using an iterator to
// loop over an array loops over x fastest and z slowest.

// The data in the array is stored in a single block of memory at
// &data[ICOORD(0,0,0)]. 

#ifndef ARRAY3D_H
#define ARRAY3D_H

#include <iostream>

template<class DATA, class ICOORD, class IPRISM> class Array3D;

template<class DATA, class ICOORD, class IPRISM>
class Array3DIter {
public:
  typedef Array3D<DATA, ICOORD, IPRISM> ArrayType;
  ArrayType *array;
  ICOORD location;
  Array3DIter(ArrayType *ra)
    : array(ra),
      location(ra->origin_)
  {}
  Array3DIter(ArrayType *ra, ICOORD &loc)
    : array(ra),
      location(loc)
  {}
  void operator++() {
    location[0]++;
    if(location[0] == array->ultima_[0]) {
      location[0] = array->origin_[0];
      location[1]++;
      if(location[1] == array->ultima_[1]) {
	location[1] = array->origin_[1];
	location[2]++;
      }
    }
  }
  DATA &operator*() {
    return (*array)[location];
  }
  const ICOORD &coord() const {
    return location;
  }
  friend bool operator==(const Array3DIter<DATA, ICOORD, IPRISM> &a,
			 const Array3DIter<DATA, ICOORD, IPRISM> &b)
  {
    return a.location == b.location;
  }
  friend bool operator!=(const Array3DIter<DATA, ICOORD, IPRISM> &a,
			 const Array3DIter<DATA, ICOORD, IPRISM> &b)
  {
    return a.location != b.location;
  }
};

template<class DATA, class ICOORD, class IPRISM>
class Array3DConstIter {
public:
  typedef Array3D<DATA, ICOORD, IPRISM> ArrayType;
  const ArrayType *array;
  ICOORD location;
  Array3DConstIter(const ArrayType *ra)
    : array(ra),
      location(ra->origin_)
  {}
  Array3DConstIter(const ArrayType *ra, ICOORD &loc)
    : array(ra),
      location(loc)
  {}
  void operator++() {
    location[0]++;
    if(location[0] == array->ultima_[0]) {
      location[0] = array->origin_[0];
      location[1]++;
      if(location[1] == array->ultima_[1]) {
	location[1] = array->origin_[1];
	location[2]++;
      }
    }
  }
  const DATA &operator*() const {
    return (*array)[location];
  }
  const ICOORD &coord() const {
    return location;
  }
  friend bool operator==(const Array3DConstIter<DATA, ICOORD, IPRISM> &a,
			 const Array3DConstIter<DATA, ICOORD, IPRISM> &b)
  {
    return a.location == b.location;
  }
  friend bool operator!=(const Array3DConstIter<DATA, ICOORD, IPRISM> &a,
			 const Array3DConstIter<DATA, ICOORD, IPRISM> &b)
  {
    return a.location != b.location;
  }
};

template<class DATA, class ICOORD, class IPRISM>
std::ostream &operator<<(std::ostream &os,
			 const Array3DIter<DATA,ICOORD,IPRISM> &iter) {
  return os << "Array3DIter(" << iter.location << ")";
}

template<class DATA, class ICOORD, class IPRISM>
std::ostream &operator<<(std::ostream &os,
			 const Array3DConstIter<DATA,ICOORD,IPRISM> &iter) {
  return os << "Array3DConstIter(" << iter.location << ")";
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template<class DATA, class ICOORD, class IPRISM>
class Array3D {
public:
  typedef Array3DIter<DATA, ICOORD, IPRISM> iterator;
  typedef Array3DConstIter<DATA, ICOORD, IPRISM> const_iterator;
private:
  IPRISM bounds;
  DATA ***data;
  ICOORD origin_;		// lower left back
  ICOORD ultima_;		// upper right front

  // Cached end-iterators.
  iterator fin;
  const_iterator cfin;

  void allocate() {
    ICOORD sz = bounds.size();
    if(sz[2] > 0) {
      data = new DATA**[sz[2]];
      //memset((void*) data, 0, sz[2]*sizeof(DATA**));
      for(int i=0; i<sz[2]; i++) {
	data[i] = new DATA*[sz[1]];
	//memset((void*) data[i], 0, sz[1]*sizeof(DATA*));
      }
      data[0][0] = new DATA[sz[0]*sz[1]*sz[2]];
      int offset = 0;
      for(int z=0; z<sz[2]; z++) {
	for(int y=0; y<sz[1]; y++) {
	  data[z][y] = data[0][0] + offset;
	  offset += sz[0];
	}
      }
    }
    else
      data = nullptr;
  } // end allocate

  void free() {
    ICOORD sz = bounds.size();
    if(data) {
      if(sz[2] > 0)
	delete [] data[0][0];
      for(int i=0; i<sz[2]; i++)
	delete [] data[i];
      delete [] data;
    }
  }

  void findfin() {
    fin = Array3DIter<DATA, ICOORD, IPRISM>(this);
    fin.location = ICOORD(origin_[0], origin_[1], ultima_[2]);
    cfin = Array3DConstIter<DATA, ICOORD, IPRISM>(this);
    cfin.location = fin.location;
  }

public:
  
  Array3D(const IPRISM &bnds)
    : bounds(bnds),
      origin_(bnds.lowerleftback()),
      ultima_(bnds.upperrightfront()),
      fin(this, ultima_),
      cfin(this, ultima_)
  {
    findfin();
    allocate();
  }

  Array3D(const IPRISM &bnds, const DATA &val)
    : bounds(bnds),
      origin_(bnds.lowerleftback()),
      ultima_(bnds.upperrightfront()),
      fin(this, ultima_),
      cfin(this, ultima_)
  {
    findfin();
    allocate();
    for(auto i=begin(); i!=end(); ++i) {
      ICOORD x = i.coord() - origin_;
      data[x[2]][x[1]][x[0]] = val;
    }
  }
  
  ~Array3D() {
    free();
  }

  // Copy constructor is expensive
  Array3D(const Array3D<DATA, ICOORD, IPRISM> &other)
    : bounds(other.bounds),
      origin_(other.origin_),
      ultima_(other.ultima_),
      fin(this, ultima_),
      cfin(this, ultima_)
  {
    allocate();
    ICOORD sz = bounds.size();
    memcpy((void*) &data[0][0][0], (void*) &other.data[0][0][0],
	   sz[0]*sz[1]*sz[2]*sizeof(DATA));
  }

  // Move construcutor is cheap
  Array3D(const Array3D<DATA, ICOORD, IPRISM> &&other)
    : bounds(std::move(other.bounds)),
      data(std::move(other.data)),
      origin_(other.origin_),
      ultima_(other.ultima_),
      fin(this, ultima_),
      cfin(this, ultima_)
  {
    other.data = nullptr;
  }

  ICOORD size() const { return bounds.size(); }

  const DATA &operator[](const ICOORD &x) const {
    ICOORD p = x - origin_;
    return data[p[2]][p[1]][p[0]];
  }

  DATA &operator[](const ICOORD &x) {
    ICOORD p = x - origin_;
    return data[p[2]][p[1]][p[0]];
  }

  iterator begin() {
    return Array3DIter<DATA, ICOORD, IPRISM>(this);
  }

  const_iterator begin() const {
    return Array3DConstIter<DATA, ICOORD, IPRISM>(this);
  }

  const iterator &end() {
    return fin;
  }

  const const_iterator &end() const {
    return cfin;
  }

  friend class Array3DIter<DATA, ICOORD, IPRISM>;
  friend class Array3DConstIter<DATA, ICOORD, IPRISM>;
};


#endif // ARRAY3D_H
