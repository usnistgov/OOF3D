// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PLANEINTERSECTION_I_H
#define PLANEINTERSECTION_I_H

#include <oofconfig.h>
#include <set>
#include "common/derefcompare.h"

// Classes defined in planeintersection.h

class MultiCornerIntersection;
class MultiFaceIntersection;
class MultiVSBIntersection;
class PixelPlaneIntersection;
class PixelPlaneIntersectionNR;
class PlaneIntersection;
class RedundantIntersection;
class SimpleIntersection;
class TetEdgeIntersection;
class TetIntersection;
class TetNodeIntersection;
class TripleFaceIntersection;
class TriplePixelPlaneIntersection;

// Classes used here but defined elsewhere
class FacePlane;
class HPixelPlane;
class FacePixelPlane;

enum Interiority {INTERIOR, EXTERIOR, MIXED};

// CrossingType indicates whether a voxel set boundary edge enters or
// exits the tet polygon at a given PlaneIntersection.

enum CrossingType {NONCROSSING, ENTRY, EXIT};


// TODO: Using std::less instead of DerefCompare should be faster, but
// it means that the order of the planes in FacePlaneSet and
// PixelPlaneSet depends on pointer ordering, not plane ordering, and
// is therefore not 100% repeatable and is hard to debug.  After
// debugging, see if std::less is faster.

typedef std::set<const FacePlane*, DerefCompare<FacePlane>> FacePlaneSet;
typedef std::set<const HPixelPlane*, DerefCompare<HPixelPlane>> PixelPlaneSet;
typedef std::set<const FacePixelPlane*, DerefCompare<FacePixelPlane>> FacePixelPlaneSet;


#endif // PLANEINTERSECTION_I_H
