// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

OBSOLETE

#ifndef HOMOGENEITYTET_I_H
#define HOMOGENEITYTET_I_H

#include <oofconfig.h>

#include <vector>
#include <map>
#include <set>
#include "common/derefcompare.h"

// Classes defined in homogeneitytet.h
class EdgePosition;
class FaceEdgeIntersection;
class FaceFacet;
class FaceFacetEdge;
class HomogeneityTet;

// Other classes used in tyepdefs defined here.
class BarycentricCoord;
class Coord3D;
class HPlane;
class PixelPlane;
class TetIntersection;

typedef std::vector<FaceFacet> FaceFacets;
typedef std::map<const Coord3D, BarycentricCoord> BaryCoordCache;
typedef std::vector<const TetIntersection*> TetIntersectionPolygon;
typedef std::map<const PixelPlane*, TetIntersectionPolygon> TetPlaneIsecMap;
typedef std::set<FaceEdgeIntersection*, DerefCompare<FaceEdgeIntersection>> LooseEndSet;

typedef std::multimap<double, FaceEdgeIntersection> LooseEndMap;
typedef std::multimap<std::pair<const HPlane*, const HPlane*>, const HPlane*, DerefPairCompare<HPlane>> CollinearPlaneMap;

typedef std::set<FaceFacetEdge*, DerefCompare<FaceFacetEdge>> FaceFacetEdgeSet;


#endif // HOMOGENEITYTET_I_H
