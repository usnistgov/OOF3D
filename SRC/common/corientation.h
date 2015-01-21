// -*- C++ -*-
// $RCSfile: corientation.h,v $
// $Revision: 1.1.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:42:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CORIENTATION_H
#define CORIENTATION_H

class COrientation;
class COrientABG;
class COrientBunge;
class COrientQuaternion;
class COrientX;
class COrientXYZ;
class COrientAxis;
class COrientRodrigues;

#include <vector>
#include <string>
#include <iostream>

class SmallMatrix;

class COrientation {
private:
  mutable SmallMatrix *cachedrot;
public:
  COrientation();
  COrientation(const COrientation&);
  virtual ~COrientation();

  // As used by the Cijkl's "transform" method, these matrices
  // yield lab-frame vectors when right-multiplied by crystal-frame vectors.
  virtual SmallMatrix *rotation_() const = 0; // returns new'd pointer
  const SmallMatrix &rotation() const;

  // Any orientation can be transformed into another one via the
  // rotation matrix.  These are virtual functions so that subclass
  // objects can override the trivial conversion into their own type.
  virtual COrientABG abg() const;
  virtual COrientBunge bunge() const;
  virtual COrientQuaternion quaternion() const;
  virtual COrientX X() const;
  virtual COrientXYZ XYZ() const;
  virtual COrientAxis axis() const;
  virtual COrientRodrigues rodrigues() const;

  virtual void print(std::ostream&) const = 0;
};

class COrientABG : public COrientation {
private:
  double alpha_, beta_, gamma_;
public:
  COrientABG(double alpha, double beta, double gamma)
    : alpha_(alpha), beta_(beta), gamma_(gamma)
  {}
  COrientABG(const SmallMatrix&);
  // Default constructor is needed so that an array of these can be created.
  COrientABG() : alpha_(0.0), beta_(0.0), gamma_(0.0) {}
  virtual SmallMatrix *rotation_() const;
  virtual COrientABG abg() const { return *this; }
  // COrientABG has special status among the COrientation subclasses,
  // because it's the default representation.  It needs some extra
  // methods because of that.
  COrientABG operator-() const {
    return COrientABG(-alpha_, -gamma_, -beta_);
  }
  double alpha() const { return alpha_; }
  double beta() const { return beta_; }
  double gamma() const { return gamma_; }
  bool operator==(const COrientABG&) const;
  bool operator!=(const COrientABG&) const;
  virtual void print(std::ostream&) const;
};

class COrientBunge : public COrientation {
private:
  double phi1_, theta_, phi2_;
public:
  COrientBunge(double phi1, double theta, double phi2)
    : phi1_(phi1), theta_(theta), phi2_(phi2)
  {}
  COrientBunge(const SmallMatrix&);
  virtual SmallMatrix *rotation_() const;
  virtual COrientBunge bunge() const { return *this; }
  double phi1() const { return phi1_; }
  double theta() const { return theta_; }
  double phi2() const { return phi2_; }
  virtual void print(std::ostream&) const;
};

class COrientQuaternion : public COrientation {
private:
  double e0_, e1_, e2_, e3_;
public:
  COrientQuaternion(double e0, double e1, double e2, double e3);
  COrientQuaternion(const SmallMatrix&);
  virtual SmallMatrix *rotation_() const;
  virtual COrientQuaternion quaternion() const { return *this; }
  double e0() const { return e0_; }
  double e1() const { return e1_; }
  double e2() const { return e2_; }
  double e3() const { return e3_; }
  virtual void print(std::ostream&) const;
};

// Goldstein's "X" convention.  This may have some other more
// descriptive name, but I don't know what it is.  Rotations are z,x,z.

class COrientX : public COrientation {
private:
  double phi_, theta_, psi_;
public:
  COrientX(double phi, double theta, double psi)
    : phi_(phi), theta_(theta), psi_(psi)
  {}
  COrientX(const SmallMatrix&);
  virtual SmallMatrix *rotation_() const;
  virtual COrientX x() const { return *this; }
  double phi() const { return phi_; }
  double theta() const { return theta_; }
  double psi() const { return psi_; }
  virtual void print(std::ostream&) const;
};

// The "aerodynamic" XYZ convention, with each rotation about a
// different principal axis.  Again the name is from Goldstein.

class COrientXYZ : public COrientation {
private:
  double phi_, theta_, psi_;
public:
  COrientXYZ(double phi, double theta, double psi)
    : phi_(phi), theta_(theta), psi_(psi)
  {}
  COrientXYZ(const SmallMatrix&);
  virtual SmallMatrix *rotation_() const;
  virtual COrientXYZ xyz() const { return *this; }
  double phi() const { return phi_; }
  double theta() const { return theta_; }
  double psi() const { return psi_; }
  virtual void print(std::ostream&) const;
};

class COrientAxis : public COrientation {
private:
  double angle_, x_, y_, z_;
public:
  COrientAxis(double angle, double x, double y, double z)
    : angle_(angle), x_(x), y_(y), z_(z)
  {}
  COrientAxis(const SmallMatrix&);
  virtual SmallMatrix *rotation_() const;
  virtual COrientAxis axis() const { return *this; }
  double angle() const { return angle_; }
  double x() const { return x_; }
  double y() const { return y_; }
  double z() const { return z_; }
  virtual void print(std::ostream&) const;
};

// Rodrigues vector. Another way of describing crystal orientations.
// This form is quite popular in the texture community; it is
// particularly useful to describe fiber-texture and poling in
// ferroelectrics. --REG

class COrientRodrigues : public COrientation {
private:
  double r1_, r2_, r3_;
public:
  COrientRodrigues(double r1, double r2, double r3)
    : r1_(r1), r2_(r2), r3_(r3)
  {}
  COrientRodrigues(const SmallMatrix&);
  virtual SmallMatrix *rotation_() const;
  virtual COrientRodrigues rodrigues() const { return *this; }
  double r1() const { return r1_; }
  double r2() const { return r2_; }
  double r3() const { return r3_; }
  virtual void print(std::ostream&) const;
};

std::ostream &operator<<(std::ostream&, const COrientation&);

#endif // CORIENTATION_H
