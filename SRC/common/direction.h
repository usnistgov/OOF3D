// -*- C++ -*-
// $RCSfile: direction.h,v $
// $Revision: 1.2.2.10 $
// $Author: langer $
// $Date: 2014/12/14 22:49:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef DIRECTION_H
#define DIRECTION_H

// A Direction is a direction in 3D space, even in 2D OOF2. It is
// *not* an Orientation.

#include "common/coord.h"
#include "common/pythonexportable.h"

class CAngleDirection;
class CUnitVectorDirection;

#include "common/doublevec.h"

class COrientation;
class SmallMatrix;

class CDirection : public PythonExportable<CDirection> {
public:
  CDirection();
  virtual ~CDirection();
  virtual const std::string &classname() const = 0;
  virtual const std::string &modulename() const;
  // Conversion
  virtual CUnitVectorDirection unitVector() const = 0;
  virtual CAngleDirection angles() const = 0;
  // Matrix multiplication (for rotation).
  virtual CUnitVectorDirection matmult(const SmallMatrix&) const = 0;
  // Components
  virtual double theta() const = 0;
  virtual double phi() const = 0;
  virtual double dot(const Coord*) const = 0;
  virtual CDirection *clone() const = 0;
  virtual Coord *coord() const = 0;
  // Identification (used in the ClippingPlane UI)
  virtual std::string *identifier() const = 0;
  
  bool operator==(const CDirection&) const;
  bool operator<(const CDirection&) const;
};

std::ostream &operator<<(std::ostream&, const CDirection&);

// bool operator==(const CDirection&, const CDirection&);
// bool operator<(const CDirection&, const CDirection&);

class CUnitVectorDirection : public CDirection {
private:
  DoubleVec vec;
public:
  CUnitVectorDirection(double x, double y, double z);
  CUnitVectorDirection(const DoubleVec*);
  CUnitVectorDirection(const Coord*);
  virtual const std::string &classname() const;
  virtual CUnitVectorDirection unitVector() const { return *this; }
  virtual CAngleDirection angles() const;
  virtual CUnitVectorDirection matmult(const SmallMatrix&) const;
  virtual double theta() const;
  virtual double phi() const;
  virtual double dot(const Coord*) const;
  double x() const { return vec[0]; }
  double y() const { return vec[1]; }
  double z() const { return vec[2]; }
  const double *pointer() const { return &vec[0]; }
  virtual CUnitVectorDirection *clone() const {
    return new CUnitVectorDirection(*this); 
  }
  virtual Coord *coord() const;
  virtual std::string *identifier() const;
  bool operator==(const CUnitVectorDirection&) const;
  bool operator<(const CUnitVectorDirection&) const;
};

class CAngleDirection : public CDirection {
private:
  double theta_, phi_;
public:
  CAngleDirection(double, double);
  virtual const std::string &classname() const;
  virtual CUnitVectorDirection unitVector() const;
  virtual CAngleDirection angles() const { return *this; }
  virtual CUnitVectorDirection matmult(const SmallMatrix&) const;
  virtual double theta() const { return theta_; }
  virtual double phi() const { return phi_; }
  virtual double dot(const Coord*) const;
  virtual CAngleDirection *clone() const {
    return new CAngleDirection(*this);
  }
  virtual Coord *coord() const;
  virtual std::string *identifier() const;
  bool operator==(const CAngleDirection&) const;
};

class CDirectionX : public CDirection {
public:
  CDirectionX() {}
  virtual const std::string &classname() const;
  virtual CUnitVectorDirection unitVector() const;
  virtual CAngleDirection angles() const;
  virtual CUnitVectorDirection matmult(const SmallMatrix&) const;
  virtual double theta() const { return M_PI/2.; }
  virtual double phi() const { return 0.0; }
  virtual double dot(const Coord*) const;
  virtual CDirectionX *clone() const {
    return new CDirectionX();
  }
  virtual Coord *coord() const;
  virtual std::string *identifier() const;
};

class CDirectionY : public CDirection {
public:
  CDirectionY() {}
  virtual const std::string &classname() const;
  virtual CUnitVectorDirection unitVector() const;
  virtual CAngleDirection angles() const;
  virtual CUnitVectorDirection matmult(const SmallMatrix&) const;
  virtual double theta() const { return M_PI/2.; }
  virtual double phi() const { return M_PI/2.; }
  virtual double dot(const Coord*) const;
  virtual CDirectionY *clone() const {
    return new CDirectionY();
  }
  virtual Coord *coord() const;
  virtual std::string *identifier() const;
};

class CDirectionZ : public CDirection {
public:
  CDirectionZ() {}
  virtual const std::string &classname() const;
  virtual CUnitVectorDirection unitVector() const;
  virtual CAngleDirection angles() const;
  virtual CUnitVectorDirection matmult(const SmallMatrix&) const;
  virtual double theta() const { return 0.0; }
  virtual double phi() const { return 0.0; }
  virtual double dot(const Coord*) const;
  virtual CDirectionZ *clone() const {
    return new CDirectionZ();
  }
  virtual Coord *coord() const;
  virtual std::string *identifier() const;
};

CUnitVectorDirection operator*(const SmallMatrix&, const CDirection&);

#endif // DIRECTION_H
