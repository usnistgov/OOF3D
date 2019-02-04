// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Classes for computing the intersection of a set of voxels with a
// convex polyhedron.  Derived from the OOF3D code, but independent of
// it.

// Template arguments:
//  COORD: a class representing a 3D coordinate with float components
//         double COORD::operator[](int) const
//         double & COORD:operator[](int)

#ifndef VSB_H
#define VSB_H

#include <set>
#include <vector>

class ProtoVSBNode;
class VoxelSetBoundary;
class VSBGraph;
class VSBNode;

#include "cprism.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Predefined voxel signatures for the 8 individual voxels.
extern unsigned char vox000, vox100, vox010, vox110,
  vox001, vox101, vox011, vox111;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


class VoxelEdgeDirection {
public:
  VoxelEdgeDirection(unsigned int a, int d);

  template <class COORD>
  VoxelEdgeDirection(const COORD &vec) {
    // This constructor uses COORD instead of ICOORD because its
    // caller gets positions out of VSBNodes, and those positions can be
    // nonintegers.  When this is used, however, we expect the values to
    // be integers.
    assert((vec[0] != 0 && vec[1] == 0 && vec[2] == 0) ||
	   (vec[0] == 0 && vec[1] != 0 && vec[2] == 0) ||
	   (vec[0] == 0 && vec[1] == 0 && vec[2] != 0));
    for(unsigned int c=0; c<3; c++) {
      if(vec[c] != 0) {
	axis = c;
	dir = (vec[c] > 0 ? 1 : -1);
	return;
      }
    }
  }

  unsigned int axis;		// 0, 1, or 2
  int dir;			// 1 or -1
  VoxelEdgeDirection reverse() const;
  bool operator==(const VoxelEdgeDirection &other) const {
    return axis == other.axis && dir == other.dir;
  }
  
  // Compare the positions of two points in this direction.  Return 1
  // if the first point is past the second point, -1 if it's the other
  // way around, and 0 if they're at the same position.
  template <class ICOORD>
  int compare(const ICOORD &i0, const ICOORD &i1) const {
    int d = (i0[axis] - i1[axis]) * dir;
    return d == 0 ? 0 : (d > 0 ? 1 : -1);
  }

};

extern const VoxelEdgeDirection posX, negX, posY, negY, posZ, negZ;

typedef std::vector<VoxelEdgeDirection> VoxelEdgeList;
extern const VoxelEdgeList allDirs;

std::ostream &operator<<(std::ostream&, const VoxelEdgeDirection&);

#endif // VSB_H
