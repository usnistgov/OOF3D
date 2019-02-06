// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef VOXELSETBOUNDARY_H
#define VOXELSETBOUNDARY_H

#include <set>
#include <vector>
#include "common/VSB/vsb.h"

#include "common/coord.h"
#include "common/cprism_i.h"

class CMicrostructure;
class COrientedPlane;
class LineSegmentLayer;

class VoxelSetBoundary : public VoxelSetBdy<Coord3D, ICoord3D, int> {
public:
};


// class VoxelSetBoundary {
// private:
//   const unsigned int category;	// for debugging only
//   const CMicrostructure *microstructure;
//   // There's one VSBGraph for each subregion in the CMicrostructure. 
//   std::vector<VSBGraph> graphs;
//   CRectangularPrism *bbox_;
// public:
//   VoxelSetBoundary(const CMicrostructure *ms,
// 		   const std::vector<ICRectangularPrism>&,
// 		   unsigned int cat);
//   ProtoVSBNode *protoVSBNodeFactory(unsigned int, unsigned char,
// 				    const ICoord3D&);
//   void addEdge(const ICoord3D&, const ICoord3D&);
//   void fixTwoFoldNodes(unsigned int s) { graphs[s].fixTwoFoldNodes(); }
//   // void find_boundaries();

//   unsigned int size() const;
//   double volume() const;
//   void findBBox();
//   const CRectangularPrism &bounds() const { return *bbox_; }

//   double clippedVolume(const std::vector<ICRectangularPrism>&,
// 		       const CRectangularPrism&,
// 		       const std::vector<COrientedPlane>&) const;

//   VSBEdgeIterator iterator() const { return VSBEdgeIterator(this); }

//   bool checkEdges() const;
//   bool checkConnectivity() const;
//   void dump(std::ostream &os, const std::vector<ICRectangularPrism>&) const;
//   void dumpLines(const std::string&) const;
//   void saveClippedVSB(const std::vector<COrientedPlane>&,
// 		      const std::string&) const;
//   void drawClippedVSB(const std::vector<COrientedPlane>&,
// 		      LineSegmentLayer*) const;

//   friend class VSBEdgeIterator;
// };

void initializeProtoNodes();

void printHomogRegionStats();
std::string &printSig(unsigned char);

#ifdef DEBUG
void setVerboseVSB(bool);
bool verboseVSB();
#endif // DEBUG

#endif // VOXELSETBOUNDARY_H
