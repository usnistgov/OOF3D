// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PIXELPLANEFACET_I_H
#define PIXELPLANEFACET_I_H

#include <oofconfig.h>
#include <map>
#include "common/derefcompare.h"

// Classes defined in pixelplanefacet.h
class FacePixelPlane;
class FacePlane;
class FacetEdge;
class HPixelPlane;
class HPlane;
class PixelFacetEdge;
class PixelPlaneFacet;
class PolygonEdge;
class StartFaceIntersectionEdge;
class StopFaceIntersectionEdge;
class TwoFaceIntersectionEdge;

// Classes used here but defined elsewhere
//class Coord2D;
class Plane;
class PixelPlaneIntersection;


typedef std::map<const Plane*, unsigned int, DerefCompare<Plane>> FaceEdgeMap;
typedef std::vector<const PixelPlaneIntersection*> PolyEdgeIntersections;
typedef std::map<const HPixelPlane*, PixelPlaneFacet*,
		 DerefCompare<HPixelPlane>> FacetMap2D;

#endif // PIXELPLANEFACET_I_H
