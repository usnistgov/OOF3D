// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This file contains two template classes CRectPrism<COORD> and
// ICRectPrism<COORD>, which define rectangular prisms.  The template
// argument COORD is a coordinate class, which must be based on
// doubles for CRectPrism and ints for ICRectPrism.

#ifndef CPRISM_H
#define CPRISM_H

#include <iostream>
#include <limits>
#include <vector>

#define min_(a,b) ((a) < (b)? (a) : (b))
#define max_(a,b) ((a) > (b)? (a) : (b))

// CRectangularPrism_ is a base class for CRectPrism and ICRectPrism.

template <class VTYPE, class CTYPE>
class CRectangularPrism_  {
protected:
  CTYPE uprightfront;
  CTYPE lowleftback;
  CTYPE size_;
public:
  CRectangularPrism_() {
    // The null constructor creates an "uninitialized" prism, with its
    // min and max reversed.  When it swallows its first point or
    // prism it will contain only that point or prism.
    uprightfront = CTYPE(-std::numeric_limits<VTYPE>::max(),
			 -std::numeric_limits<VTYPE>::max(),
			 -std::numeric_limits<VTYPE>::max());
    lowleftback = CTYPE(std::numeric_limits<VTYPE>::max(),
			std::numeric_limits<VTYPE>::max(),
			std::numeric_limits<VTYPE>::max());
  }
  CRectangularPrism_(const CTYPE &a, const CTYPE &b) {
    uprightfront = a;
    lowleftback = a;
    swallow(b);
  }
  CRectangularPrism_(const std::vector<CTYPE> &vec) {
    // construct the bounding box of the points in vec
    assert(vec.size() > 0);
    uprightfront = vec[0];
    lowleftback = vec[0];
    for(unsigned int i=1; i<vec.size(); i++)
      swallow(vec[i]);
  }

  virtual ~CRectangularPrism_() {}

  // Define lowerleft and upperright for compatibility with 2D code.
  // Perhaps a more general name should be found for both versions.
  inline const CTYPE &lowerleft() const { return lowleftback; }
  inline const CTYPE &upperright() const { return uprightfront; }
  inline const CTYPE &lowerleftback() const { return lowleftback; }
  inline const CTYPE &upperrightfront() const { return uprightfront; }
  inline const CTYPE center() const { return 0.5*(lowleftback+uprightfront); }
  template <class CTYPE2>
  void swallow(const CTYPE2 &pt) {
    if(uprightfront[0] < pt[0]) uprightfront[0] = pt[0];
    if(uprightfront[1] < pt[1]) uprightfront[1] = pt[1];
    if(uprightfront[2] < pt[2]) uprightfront[2] = pt[2];
    if(lowleftback[0] > pt[0]) lowleftback[0] = pt[0];
    if(lowleftback[1] > pt[1]) lowleftback[1] = pt[1];
    if(lowleftback[2] > pt[2]) lowleftback[2] = pt[2];
    size_ = uprightfront - lowleftback;
  }
  template <class VTYPE2, class CTYPE2>
  void swallowPrism(const CRectangularPrism_<VTYPE2, CTYPE2> &other) {
    swallow(other.upperrightfront());
    swallow(other.lowerleftback());
  }
  inline VTYPE xmin() const { return lowleftback[0]; }
  inline VTYPE xmax() const { return uprightfront[0]; }
  inline VTYPE ymin() const { return lowleftback[1]; }
  inline VTYPE ymax() const { return uprightfront[1]; }
  inline VTYPE zmin() const { return lowleftback[2]; }
  inline VTYPE zmax() const { return uprightfront[2]; }
  double min(int dir) const { return lowleftback[dir]; }
  double max(int dir) const { return uprightfront[dir]; }
  inline VTYPE height() const { return uprightfront[1] - lowleftback[1]; }
  inline VTYPE width() const { return uprightfront[0] - lowleftback[0]; }
  inline VTYPE depth() const { return uprightfront[2] - lowleftback[2]; }
  inline virtual VTYPE volume() const { return width()*height()*depth(); }
  inline const CTYPE &size() const { return size_; }
  bool contains(const CTYPE &point) const {
    if(point[0] < xmin() || point[0] >= xmax()) return false;
    if(point[1] < ymin() || point[1] >= ymax()) return false;
    if(point[2] < zmin() || point[2] >= zmax()) return false;
    return true;
  }
  template <class VTYPE2, class CTYPE2>
  bool intersects(const CRectangularPrism_<VTYPE2, CTYPE2> &other) const {
    if(uprightfront[0] < other.lowleftback[0]) return false;
    if(uprightfront[1] < other.lowleftback[1]) return false;
    if(uprightfront[2] < other.lowleftback[2]) return false;
    if(lowleftback[0] > other.uprightfront[0]) return false;
    if(lowleftback[1] > other.uprightfront[1]) return false;
    if(lowleftback[2] > other.uprightfront[2]) return false;
    return true;
  }
  template <class VTYPE2, class CTYPE2>
  bool intersects_open(const CRectangularPrism_<VTYPE2, CTYPE2> &other) const {
    if(uprightfront[0] <= other.lowleftback[0]) return false;
    if(uprightfront[1] <= other.lowleftback[1]) return false;
    if(uprightfront[2] <= other.lowleftback[2]) return false;
    if(lowleftback[0] >= other.uprightfront[0]) return false;
    if(lowleftback[1] >= other.uprightfront[1]) return false;
    if(lowleftback[2] >= other.uprightfront[2]) return false;
    return true;
  }
  virtual int ncorners() const { return 8; }
  virtual CTYPE operator[](int i) const {
    switch(i) {
    case 0:
      return lowleftback;
    case 1:
      return CTYPE(uprightfront[0], lowleftback[1], lowleftback[2]);
    case 2:
      return CTYPE(uprightfront[0], uprightfront[1], lowleftback[2]);
    case 3:
      return CTYPE(lowleftback[0], uprightfront[1], lowleftback[2]);
		case 4:
      return uprightfront;
    case 5:
      return CTYPE(lowleftback[0], uprightfront[1], uprightfront[2]);
    case 6:
      return CTYPE(lowleftback[0], lowleftback[1], uprightfront[2]);
    case 7:
      return CTYPE(uprightfront[0], lowleftback[1], uprightfront[2]);
    };
    throw ErrBadIndex(i, __FILE__, __LINE__);
  }
  // 
  void restrict(const CRectangularPrism_<VTYPE, CTYPE> &limits) {
    if(limits.xmin() > lowleftback[0])
      lowleftback[0] = min_(uprightfront[0], limits.xmin());
    if(limits.xmax() < uprightfront[0])
      uprightfront[0] = max_(lowleftback[0], limits.xmax());
    if(limits.ymin() > lowleftback[1])
      lowleftback[1] = min_(uprightfront[1], limits.ymin());
    if(limits.ymax() < uprightfront[1])
      uprightfront[1] = max_(lowleftback[1], limits.ymax());
    if(limits.zmin() > lowleftback[2])
      lowleftback[2] = min_(uprightfront[2], limits.zmin());
    if(limits.zmax() < uprightfront[2])
      uprightfront[2] = max_(lowleftback[2], limits.zmax());
    size_ = uprightfront - lowleftback;
  }

  template <class VTYPE2, class CTYPE2> friend class CRectangularPrism_;
};				// end CRectangularPrism_

// double and int subclasses

template <class COORD>
class CRectPrism: public CRectangularPrism_<double, COORD> {
public:
  CRectPrism() {}
  CRectPrism(const COORD &a, const COORD &b)
    : CRectangularPrism_<double, COORD>(a,b)
  {}
  CRectPrism(const std::vector<COORD> &v)
    : CRectangularPrism_<double, COORD>(v)
  {}
  CRectPrism(const COORD *a, const COORD *b)
    : CRectangularPrism_<double, COORD>(*a, *b)
  {}
  friend std::ostream& operator<<(std::ostream &os,
				  const CRectPrism<COORD> &rect)
  {
    os << "CRectangularPrism(" << rect.lowleftback << ", "
       << rect.uprightfront << ")";
    return os;
  }
  void expand(double howmuch)  {
    double mid = 0.5*(this->lowleftback[0] + this->uprightfront[0]);
    double size = 0.5*(this->uprightfront[0] - this->lowleftback[0])
      * (1 + howmuch);
    this->lowleftback[0] = mid - size;
    this->uprightfront[0] = mid + size;
    mid = 0.5*(this->lowleftback[1] + this->uprightfront[1]);
    size = 0.5*(this->uprightfront[1] - this->lowleftback[1])*(1 + howmuch);
    this->lowleftback[1] = mid - size;
    this->uprightfront[1] = mid + size;
    mid = 0.5*(this->lowleftback[2] + this->uprightfront[2]);
    size = 0.5*(this->uprightfront[2] - this->lowleftback[2])*(1 + howmuch);
    this->lowleftback[2] = mid - size;
    this->uprightfront[2] = mid + size;
    this->size_ = this->uprightfront - this->lowleftback;
  }
};

template <class COORD>
class ICRectPrism : public CRectangularPrism_<int, COORD> {
public:
  ICRectPrism() {}
  ICRectPrism(const COORD &a, const COORD &b)
    : CRectangularPrism_<int, COORD>(a,b)
  {}
  friend std::ostream& operator<<(std::ostream &os,
				  const ICRectPrism<COORD> &rect)
  {
    os << "ICRectangularPrism(" << rect.lowleftback << ", "
       << rect.uprightfront << ")";
    return os;
  }
};

#undef min_
#undef max_

#endif // CPRISM_H
