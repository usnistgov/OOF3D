// -*- C++ -*-
// $RCSfile: angle2color.C,v $
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

#include <oofconfig.h>

// Methods for converting COrientations to colors, for display
// purposes.  Although the space of colors and the space of
// orientations are both three dimensional, they have different
// topologies, so there's no obviously best way of converting from one
// to the other.

#include "common/ccolor.h"
#include "engine/angle2color.h"
#include "common/corientation.h"
#include <math.h>

CColor Bunge2RGB::operator()(const COrientation &angle) const {
  COrientBunge bunge = angle.bunge();
  double bunge1 = bunge.phi1()/(2.*M_PI) + 0.5;
  double bunge2 = bunge.theta()/M_PI;
  double bunge3 = bunge.phi2()/(2.*M_PI) + 0.5;
  return CColor(bunge1, bunge2, bunge3);
}

CColor Euler2RGB::operator()(const COrientation &angle) const {
  COrientABG abg = angle.abg();
  return CColor(abg.alpha()/M_PI,
		abg.beta()/(2.*M_PI) + 0.5,
		abg.gamma()/(2.*M_PI) + 0.5);
}

CColor Euler2HSV::operator()(const COrientation &angle) const {
  COrientABG abg = angle.abg();
  // alpha is (0, pi). hue is (0, 360)
  double hue = abg.alpha()*360./M_PI;
  // saturation is (0,1).  beta is (-pi, pi)
  double saturation = abg.beta()/(2.*M_PI)+ 0.5;
  // value is (0, 1).  gamma is (-pi, pi)
  double value = abg.gamma()/(2.*M_PI) + 0.5;
  CHSVColor hsv(hue, saturation, value);
  return CColor(hsv.getRed(), hsv.getGreen(), hsv.getBlue());
}

CColor Axis2HSV::operator()(const COrientation &angle) const {
  COrientAxis axis = angle.axis();
  double psi = axis.angle();
  double x = axis.x();
  double y = axis.y();
  double z = axis.z();
  double r2 = x*x + y*y + z*z;
  double r = sqrt(r2);
  double costheta = z/r;
  double phi = atan2(y, x);
  // saturation is (0,1),  psi is (-pi, pi).
  double sat = (psi + M_PI)/(2*M_PI);
  // phi is (-pi, pi), hue is (0, 360).
  double hue = (phi + M_PI)*180./M_PI;
  // costheta is (-1, 1), value is (0, 1).
  double val = 0.5*(costheta + 1.);
  CHSVColor hsv(hue, sat, val);
  return CColor(hsv.getRed(), hsv.getGreen(), hsv.getBlue());
}
