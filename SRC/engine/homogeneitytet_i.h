// -*- C++ -*-
// $RCSfile: homogeneitytet_i.h,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2015/12/16 16:28:16 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef HOMOGENEITYTET_I_H
#define HOMOGENEITYTET_I_H

#include <oofconfig.h>

#include <vector>
#include <map>

// Classes defined in homogeneitytet.h
class FaceEdgeIntersection;
class FaceFacet;
class FaceFacetEdge;
class HomogeneityTet;

// Other classes used in tyepdefs defined here.
class BarycentricCoord;
class Coord3D;
class PixelPlane;
class TetIntersection;


typedef std::vector<FaceFacet> FaceFacets;

typedef std::map<const Coord3D, BarycentricCoord> BaryCoordCache;
typedef std::vector<const TetIntersection*> TetIntersectionPolygon;
typedef std::map<const PixelPlane*, TetIntersectionPolygon> TetPlaneIsecMap;



#endif // HOMOGENEITYTET_I_H
