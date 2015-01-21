// -*- C++ -*-
// $RCSfile: sincos.h,v $
// $Revision: 1.1.26.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:56 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SINCOS_H
#define SINCOS_H

#include <oofconfig.h>

// Efficient calculation of sin and cos together.

void sincos(double theta, double &sine, double &cosine);

#endif // SINCOS_H
