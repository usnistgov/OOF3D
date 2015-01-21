// -*- C++ -*-
// $RCSfile: planarity.h,v $
// $Revision: 1.3.18.3 $
// $Author: langer $
// $Date: 2014/09/17 21:26:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PLANARITY_H
#define PLANARITY_H

// TODO 3.1: Don't define IN_PLANE or OUT_OF_PLANE in 3D?

// Vector and Tensor iterators can have the following types:
enum Planarity {IN_PLANE,	// loops over only x and y components
		OUT_OF_PLANE,	// loops over only z components
		ALL_INDICES};	// loops over all components

#endif // PLANARITY_H
