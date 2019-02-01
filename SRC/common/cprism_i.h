// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This file exists so that when we separate the voxelsetboundary code
// from the rest of OOF3D for distribution, we don't need to be
// redefining CRectangularPrism and ICRectangularPrism everywhere.
// The voxelsetboundary files will use CRectPrism<COORD> and everyone
// else will use CRectangularPrism.

#ifndef CPRISM_I_H
#define CPRISM_I_H

#include <oofconfig.h>

// TODO: Is there a way to do this without actually including cprism.h
// here?  It would be nice to only have to include it in .C files, not
// .h files.  This file is included in other .h files.

#include "common/coord.h"
#include "common/cprism.h"
typedef CRectPrism<Coord3D> CRectangularPrism;
typedef ICRectPrism<ICoord3D> ICRectangularPrism;

template class CRectPrism<Coord3D>;
template class ICRectPrism<ICoord3D>;

#endif // CPRISM_I_H
