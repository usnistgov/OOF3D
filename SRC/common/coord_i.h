// -*- C++ -*-
// $RCSfile: coord_i.h,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2014/12/14 22:49:06 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef COORD_I_H
#define COORD_I_H

#include <oofconfig.h>

// This file contains forward declarations and typedefs from coord.h.
// It can be included instead of that file in most situations, to
// reduce header file dependencies.


// Coord2D and Coord3D are the 2D and 3D coordinate classes.  Both are
// always defined, whatever the value of DIM.  Coord is defined to be
// Coord2D if DIM==2 and Coord3D if DIM==3.  If DIM==2, only Coord2D
// is derived from Position.

#include "engine/ooferror.h"
#include <vector>

class Coord2D;
class Coord3D;
class ICoord2D;
class ICoord3D;
class Position;

#if DIM==2
typedef Coord2D Coord;
typedef ICoord2D ICoord;
#else
typedef Coord3D Coord;
typedef ICoord3D ICoord;
#endif

// TODO 3.1: Why do we define ICoordVector here and ICoordVec in
// typemaps.swg?  They're the same thing. 

typedef std::vector<ICoord> ICoordVector;


#endif // COORD_I_H
