// -*- C++ -*-
// $RCSfile: angle2color.h,v $
// $Revision: 1.3.24.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:05 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ANGLE2COLOR_H
#define ANGLE2COLOR_H

#include <oofconfig.h>

class CColor;
class COrientation;

class Angle2Color {
public:
  virtual ~Angle2Color() {}
  virtual Angle2Color *clone() const = 0;
  virtual CColor operator()(const COrientation&) const = 0;
};

template <class TYPE>
class Angle2ColorTemplate : public Angle2Color {
public:
  virtual ~Angle2ColorTemplate() {}
  virtual Angle2Color *clone() const {
    return new TYPE(*dynamic_cast<const TYPE*>(this)); 
  }
};

class Bunge2RGB : public Angle2ColorTemplate<Bunge2RGB> {
public:
  virtual CColor operator()(const COrientation&) const;
};

class Euler2RGB : public Angle2ColorTemplate<Euler2RGB> {
public:
  virtual CColor operator()(const COrientation&) const;
};

class Euler2HSV : public Angle2ColorTemplate<Euler2HSV> {
public:
  virtual CColor operator()(const COrientation&) const;
};

class Axis2HSV : public Angle2ColorTemplate<Axis2HSV> {
public:
  virtual CColor operator()(const COrientation&) const;
};

#endif // ANGLE2COLOR_H
