// -*- C++ -*-
// $RCSfile: corientation.swg,v $
// $Revision: 1.1.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:42:58 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CORIENTATION_SWG
#define CORIENTATION_SWG

%module corientation
%include "common/typemaps.swg"

%{
#include "common/corientation.h"
%}

%pragma(python) include="corientation.spy"

class COrientation {
public:
  ~COrientation();
  COrientABG abg();
  COrientBunge bunge();
  COrientQuaternion quaternion();
  COrientX X();
  COrientXYZ XYZ();
  COrientAxis axis();
  COrientRodrigues rodrigues();

  %addmethods {
    bool __eq__(COrientation *other) {
      return self->abg() == other->abg();
    }
    bool __ne__(COrientation *other) {
      return self->abg() != other->abg();
    }
  }
};

class COrientABG : public COrientation {
public:
  COrientABG(double, double, double);
  ~COrientABG();
  double alpha();
  double beta();
  double gamma();
  %addmethods {
    COrientABG __neg__() {
      return -(*self);
    }
  }
};

class COrientBunge : public COrientation {
public:
  COrientBunge(double, double, double);
  ~COrientBunge();
  double phi1();
  double theta();
  double phi2();
};

class COrientQuaternion : public COrientation {
public:
  COrientQuaternion(double, double, double, double);
  ~COrientQuaternion();
  double e0() const;
  double e1() const;
  double e2() const;
  double e3() const;
};

class COrientX : public COrientation {
public:
  COrientX(double, double, double);
  ~COrientX();
  double phi();
  double theta();
  double psi();
};

class COrientXYZ : public COrientation {
public:
  COrientXYZ(double, double, double);
  ~COrientXYZ();
  double phi();
  double theta();
  double psi();
};

class COrientAxis : public COrientation {
public:
  COrientAxis(double, double, double, double);
  ~COrientAxis();
  double angle();
  double x();
  double y();
  double z();
};

class COrientRodrigues : public COrientation {
public:
  COrientRodrigues(double, double, double);
  ~COrientRodrigues();
  double r1();
  double r2();
  double r3();
};


#endif	// CORIENTATION_SWG
