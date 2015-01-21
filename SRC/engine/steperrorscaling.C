// -*- C++ -*-
// $RCSfile: steperrorscaling.C,v $
// $Revision: 1.4.4.1 $
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

#include "common/doublevec.h"
#include "common/printvec.h"
#include "engine/steperrorscaling.h"
#include <math.h>

double RelativeErrorScaling::operator()(double deltat,
					DoubleVec &ystart,
					DoubleVec &yend0,
					DoubleVec &yend1) const
{
  double errmax = 0.0;
  for(unsigned int i=0; i<yend0.size(); i++) {
    double err = yend1[i] - yend0[i];
    if(yend0[i] != 0.0)
      err /= yend0[i];
    else if (yend1[i] != 0.0)
      err /= yend1[i];
    err = fabs(err);
    if(errmax < err)
      errmax = err;
  }
  return errmax;
}

double AbsoluteErrorScaling::operator()(double deltat,
					DoubleVec &ystart,
					DoubleVec &yend0,
					DoubleVec &yend1) const
{
  double errmax = 0.0;
  for(unsigned int i=0; i<yend0.size(); i++) {
    double err = fabs(yend1[i] - yend0[i]);
    if(errmax < err)
      errmax = err;
  }
  return errmax;
}

double XOverErrorScaling::operator()(double deltat,
				     DoubleVec &ystart,
				     DoubleVec &yend0,
				     DoubleVec &yend1) const 
{
  // Error is scaled by |y| + |dt dy/dt|, which gives relative errors,
  // except near zero crossings. 
  double errmax = 0.0;
  for(unsigned int i=0; i<yend0.size(); i++) {
    double err = fabs(yend1[i] - yend0[i]);
    double scal = fabs(yend1[i]) + fabs(yend1[i] - ystart[i]);
    // If scal is zero, then y==0 and dy/dt==0, so err=0 too.
    if(scal != 0.0) {
      err /= scal;
      if(errmax < err)
	errmax = err;
    }
  }
  return errmax;
};

double GlobalErrorScaling::operator()(double deltat,
				      DoubleVec &ystart,
				      DoubleVec &yend0,
				      DoubleVec &yend1) const
{
  // Error is scaled by |dt dy/dt|.
  double errmax = 0.0;
  for(unsigned int i=0; i<yend0.size(); i++) {
    double err = fabs(yend1[i] - yend0[i]);
    double scal = fabs(yend1[i] - ystart[i]);
    if(scal == 0.0)
      scal = fabs(yend0[i] - ystart[i]);
    if(scal != 0.0) {
      err /= scal;
      if(errmax < err)
	errmax = err;
    }
    // If ystart[i] == yend0[i] == yend1[i], just ignore this point.
    // There's no apparent error.
  }
  return errmax;
} 
