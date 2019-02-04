// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "vsb.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelEdgeDirection::VoxelEdgeDirection(unsigned int ax, int d)
  : axis(ax),
    dir(d)
{
  assert(axis >=0 && axis <= 2);
  assert(dir == 1 || dir == -1);
}


VoxelEdgeDirection VoxelEdgeDirection::reverse() const {
  return VoxelEdgeDirection(axis, -dir);
}

// Which of the two given ICoord3Ds has the larger component in this
// direction?  Return 1 if i0 is greater, -1 if i1 is greater, and 0
// if they're the same.


const VoxelEdgeDirection posX(0, 1);
const VoxelEdgeDirection negX(0, -1);
const VoxelEdgeDirection posY(1, 1);
const VoxelEdgeDirection negY(1, -1);
const VoxelEdgeDirection posZ(2, 1);
const VoxelEdgeDirection negZ(2, -1);

const VoxelEdgeList allDirs({posX, negX, posY, negY, posZ, negZ});

std::ostream &operator<<(std::ostream &os, const VoxelEdgeDirection &dir) {
  if(dir == posX)
    os << "posX";
  else if(dir == posY)
    os << "posY";
  else if(dir == posZ)
    os << "posZ";
  else if(dir == negX)
    os << "negX";
  else if(dir == negY)
    os << "negY";
  else if(dir == negZ)
    os << "negZ";
  else
    os << "VoxelEdgeDirection(" << dir.axis << "," << dir.dir << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//




