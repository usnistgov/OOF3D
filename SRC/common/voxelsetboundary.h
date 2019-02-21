// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// OOF3D-specific wrapper for the generic voxel set boundary code in
// VSB/vsb.h.

#include <oofconfig.h>

#ifndef VOXELSETBOUNDARY_H
#define VOXELSETBOUNDARY_H

#include <set>
#include <vector>
#include "common/VSB/vsb.h"

#include "common/array.h"
#include "common/coord.h"
#include "common/VSB/cprism.h"
#include "common/VSB/cplane.h"

typedef ICRectPrism<ICoord3D> VoxelBin;
typedef std::vector<VoxelBin> BinList;

class CMicrostructure;
class LineSegmentLayer;


class VoxelSetBoundary : public VoxelSetBdy<Coord3D, ICoord3D, Array<int>, int>
{
private:
  const CMicrostructure *microstructure;
public:
  VoxelSetBoundary(const CMicrostructure *ms, const BinList &bins, int cat);
  void dumpLines(const std::string&) const;
  void saveClippedVSB(const std::vector<VSBPlane<Coord3D>>&,
 		      const std::string&) const;
  void drawClippedVSB(const std::vector<VSBPlane<Coord3D>>&,
 		      LineSegmentLayer*) const;
};


void initializeVSB();

void printHomogRegionStats();
std::string &printSig(unsigned char);

#endif // VOXELSETBOUNDARY_H
