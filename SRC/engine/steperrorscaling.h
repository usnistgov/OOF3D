// -*- C++ -*-
// $RCSfile: steperrorscaling.h,v $
// $Revision: 1.3.4.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:52 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef STEPERRORSCALING_H
#define STEPERRORSCALING_H

class DoubleVec;

class StepErrorScaling {
public:
  virtual ~StepErrorScaling() {}
  virtual bool globalscaling() const = 0;
  virtual double operator()(double deltat, 
			    DoubleVec &start,
			    DoubleVec &end1,
			    DoubleVec &end2) const = 0;
};

class RelativeErrorScaling : public StepErrorScaling {
public:
  virtual bool globalscaling() const { return false; }
  virtual double operator()(double deltat,
			    DoubleVec &start,
			    DoubleVec &end1,
			    DoubleVec &end2) const;
};

class AbsoluteErrorScaling : public StepErrorScaling {
public:
  virtual bool globalscaling() const { return false; }
  virtual double operator()(double deltat,
			    DoubleVec &start,
			    DoubleVec &end1,
			    DoubleVec &end2) const;
};

class XOverErrorScaling : public StepErrorScaling {
public:
  virtual bool globalscaling() const { return true; }
  virtual double operator()(double deltat,
			    DoubleVec &start,
			    DoubleVec &end1,
			    DoubleVec &end2) const;
};

class GlobalErrorScaling : public StepErrorScaling {
public:
  virtual bool globalscaling() const { return true; }
  virtual double operator()(double deltat,
			    DoubleVec &start,
			    DoubleVec &end1,
			    DoubleVec &end2) const;
};

#endif // STEPERRORSCALING_H
