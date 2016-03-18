// -*- C++ -*-
// $RCSfile: coincidences.h,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2015/08/03 20:46:04 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef COINCIDENCES_H
#define COINCIDENCES_H

#include <oofconfig.h>

#include "tetintersection.h"

void resolveTwoFoldCoincidence(
	       unsigned int, unsigned int,
	       const std::pair<CoordIsec::iterator, CoordIsec::iterator> &,
	       const std::vector<Coord3D>&,
	       std::vector<ElEdgeMap>&,
	       BaryCoordMap&,
	       PixelPlaneFacet*,
	       const PixelPlane&,
	       unsigned int,
	       const std::vector<const PixelPlane*>&,
	       BaryCoordCache&
#ifdef DEBUG
	       , bool verbose
#endif // DEBUG
			       );
	       
void resolveThreeFoldCoincidence(
	       const std::pair<CoordIsec::iterator, CoordIsec::iterator> &,
	       const std::vector<Coord3D>&,
	       std::vector<ElEdgeMap>&,
	       BaryCoordMap&,
	       PixelPlaneFacet*,
	       const PixelPlane&,
	       unsigned int,
	       const std::vector<const PixelPlane*>&,
	       BaryCoordCache&
#ifdef DEBUG
	       , bool verbose
#endif // DEBUG
			       );

void resolveMultipleCoincidence(
		const std::pair<CoordIsec::iterator, CoordIsec::iterator>&,
		const std::vector<Coord3D> &epts,
		unsigned int,
		unsigned int,
		std::vector<ElEdgeMap>&,
		BaryCoordMap&,
		PixelPlaneFacet*,
		const PixelPlane&,
		unsigned int,
		const std::vector<const PixelPlane*>&,
		BaryCoordCache&
#ifdef DEBUG
		, bool verbose
#endif // DEBUG
				);

// void resolveFourFoldCoincidence(
// 	       const std::pair<CoordIsec::iterator, CoordIsec::iterator> &,
// 	       const std::vector<Coord3D>&,
// 	       std::vector<ElEdgeMap>&,
// 	       BaryCoordMap&,
// 	       PixelPlaneFacet*,
// 	       const PixelPlane&,
// 	       unsigned int,
// 	       const std::vector<const PixelPlane*>&,
// 	       BaryCoordCache&
// #ifdef DEBUG
// 	       , bool verbose
// #endif // DEBUG
// 			       );

// void resolveFiveFoldCoincidence(
// 	       const std::pair<CoordIsec::iterator, CoordIsec::iterator> &,
// 	       const std::vector<Coord3D>&,
// 	       std::vector<ElEdgeMap>&,
// 	       BaryCoordMap&,
// 	       PixelPlaneFacet*,
// 	       const PixelPlane&,
// 	       unsigned int,
// 	       const std::vector<const PixelPlane*>&,
// 	       BaryCoordCache&
// #ifdef DEBUG
// 	       , bool verbose
// #endif // DEBUG
// 			       );

#endif // COINCIDENCES_H
