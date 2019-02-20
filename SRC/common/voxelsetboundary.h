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

#include "common/coord.h"
#include "common/VSB/cprism.h"
#include "common/VSB/cplane.h"

typedef ICRectPrism<ICoord3D> VoxelBin;
typedef std::vector<VoxelBin> BinList;

class CMicrostructure;
class LineSegmentLayer;


// TODO: Why isn't VoxelSetBoundary derived from VoxelSetBdy instead
// of containing a pointer to one?

class VoxelSetBoundary {
private:
  const CMicrostructure *microstructure;
  VoxelSetBdy<Coord3D, ICoord3D, int> *vsb;
public:
  VoxelSetBoundary(const CMicrostructure *ms, const BinList &bins, int cat);
  ~VoxelSetBoundary();
  unsigned int size() const { return vsb->size(); }
  double clippedVolume(const CRectPrism<Coord3D> &bbox,
		       const std::vector<VSBPlane<Coord3D>> &planes) const;
  bool checkEdges() const;
  void dump(std::ostream &os) const;
  void dumpLines(const std::string&) const;
  void saveClippedVSB(const std::vector<VSBPlane<Coord3D>>&,
 		      const std::string&) const;
  void drawClippedVSB(const std::vector<VSBPlane<Coord3D>>&,
 		      LineSegmentLayer*) const;
  VoxelSetBdy<Coord3D, ICoord3D, int>::EdgeIterator iterator() const;
};


void initializeVSB();

void printHomogRegionStats();
std::string &printSig(unsigned char);

#endif // VOXELSETBOUNDARY_H
