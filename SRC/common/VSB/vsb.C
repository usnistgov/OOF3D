// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This file contains the few parts of the VoxelSetBdy machinery that
// aren't templated.

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

// A VoxRot (VoxelRotation) maps axes in the actual configuration to
// axes in the reference configuration and vice versa.  The arguments
// to the constructor are the actual space directions that correspond
// to the +x, +y, and +z directions in the reference space.

VoxRot::VoxRot(VoxelEdgeDirection d0, VoxelEdgeDirection d1,
	       VoxelEdgeDirection d2)
  : actualAxes({d0, d1, d2})
{
  assert(d0.axis != d1.axis && d1.axis != d2.axis && d2.axis != d0.axis);
// #ifdef DEBUG
//   if(d0.axis == d1.axis || d1.axis == d2.axis || d2.axis == d0.axis) {
//     oofcerr << "VoxRot::VoxRot: d0=" << d0 << " d1=" << d1 << " d2=" << d2
// 	    << std::endl;
//     throw ErrProgrammingError("Badly specified voxel rotation!",
// 			      __FILE__, __LINE__);
//   }
// #endif // DEBUG
}

VoxelEdgeDirection VoxRot::toActual(const VoxelEdgeDirection &d) const
{
  if(d.dir == 1)
    return actualAxes[d.axis];
  return actualAxes[d.axis].reverse();
}

VoxelEdgeDirection VoxRot::toReference(const VoxelEdgeDirection &d) const
{
  // d is a direction in the actual space.  Find which of the
  // actualAxes is in the same direction (up to a sign).  TODO: This
  // could be done with a table lookup, but then the VoxRot
  // object would need a lot more data.  Or we could precompute the 24
  // possible rotations and re-use the objects.
  for(int c=0; c<3; c++) {
    if(actualAxes[c].axis == d.axis) {
      // actualAxes[c] is the actual-space direction corresponding to
      // the positive orientation of reference space vector c.  If the
      // actual space direction d is in oppositely oriented, return
      // the negative oriention of the reference space vector.
      return VoxelEdgeDirection(c, d.dir*actualAxes[c].dir);
    }
  }
  assert(0);			// VoxRot::toReference failed!
}

//static const VoxRot noRotation(posX, posY, posZ);

std::ostream &operator<<(std::ostream &os, const VoxRot &rotation) {
  os << "[" << rotation.actualAxes[0] << "," << rotation.actualAxes[1]
     << "," << rotation.actualAxes[2] << "]";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A voxel signature indicates which voxels in the 2x2x2 cube
// surrounding a point are in the voxel category of interest.  It's
// stored in a char, with one bit for each of the eight voxels.  The
// order of the bits in the char is determined by the loops in
// CMicrostructure::voxelSignature.  The innermost loop is over x and
// the outermost is over z.

// Voxel signatures for the single voxels of the 2x2x2 cube are named
// here.  The names say whether the x, y, and z component of the voxel
// position is on the positive side (1) or negative side (0) of the
// cube.  These values can be simply added together to get the
// signature for a multi-voxel group.

// These aren't static because they're swigged and used in the test
// suite.
unsigned char vox000 = 0x01;
unsigned char vox100 = 0x02;
unsigned char vox010 = 0x04;
unsigned char vox110 = 0x08;
unsigned char vox001 = 0x10;
unsigned char vox101 = 0x20;
unsigned char vox011 = 0x40;
unsigned char vox111 = 0x80;

unsigned char voxelALL = 0xff;
unsigned char voxelNONE = 0x00;

std::string &printSig(unsigned char sig) {
  // Store a copy of each signature string, and return a reference to
  // it, because swig does strange things with bare std::string return
  // types.  We need to return a reference to a permanent object.
  static std::map<unsigned char, std::string> sigdict;
  auto s = sigdict.find(sig);
  if(s != sigdict.end())
    return s->second;
  std::vector<std::string> voxels;
  if(sig & vox000) voxels.push_back("vox000");
  if(sig & vox100) voxels.push_back("vox100");
  if(sig & vox010) voxels.push_back("vox010");
  if(sig & vox110) voxels.push_back("vox110");
  if(sig & vox001) voxels.push_back("vox001");
  if(sig & vox101) voxels.push_back("vox101");
  if(sig & vox011) voxels.push_back("vox011");
  if(sig & vox111) voxels.push_back("vox111");
  if(voxels.empty())
    sigdict[sig] = "voxelNONE";
  else if(voxels.size() == 8)
    sigdict[sig] = "voxelALL";
  else if(voxels.size() == 1)
    sigdict[sig] = voxels[0];
  else {
    for(unsigned int i=1; i<voxels.size(); i++)
      voxels[0] += "|" + voxels[i];
    sigdict[sig] = voxels[0];
  }
  return sigdict[sig];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

