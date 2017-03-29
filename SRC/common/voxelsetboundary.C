// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/oofcerr.h"
#include "common/geometry.h"
#include "common/voxelsetboundary.h"
#include "common/cmicrostructure.h"
#include "common/printvec.h"

// TODO: Testing!  Use pixel selection methods to generate 512 test
// cases, using all 2x2x2 voxel configurations inside a border of
// entirely selected or entirely unselected voxels.  Generate the VSBs
// and check that the computed volume (from the VSB) of selected and
// unselected voxels is correct.  Then generate Skeletons and check
// the total volume of each element as well as the volume of each
// category.

#define swap(x, y) { auto temp = x; x = y; y = temp; }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelEdgeDirection::VoxelEdgeDirection(unsigned int ax, int d)
  : axis(ax),
    dir(d)
{
  assert(axis >=0 && axis <= 2);
  assert(dir == 1 || dir == -1);
}

VoxelEdgeDirection::VoxelEdgeDirection(const Coord3D &vec) {
  // This constructor uses Coord3D instead of ICoord3D because its
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

VoxelEdgeDirection VoxelEdgeDirection::reverse() const {
  return VoxelEdgeDirection(axis, -dir);
}

// Which of the two given ICoord3Ds has the larger component in this
// direction?  Return 1 if i0 is greater, -1 if i1 is greater, and 0
// if they're the same.

int VoxelEdgeDirection::compare(const ICoord3D &i0, const ICoord3D &i1) const {
  int d = (i0[axis] - i1[axis]) * dir;
  return d == 0 ? 0 : (d > 0 ? 1 : -1);
}

static const VoxelEdgeDirection posX(0, 1);
static const VoxelEdgeDirection negX(0, -1);
static const VoxelEdgeDirection posY(1, 1);
static const VoxelEdgeDirection negY(1, -1);
static const VoxelEdgeDirection posZ(2, 1);
static const VoxelEdgeDirection negZ(2, -1);

static VoxelEdgeList allDirs({posX, negX, posY, negY, posZ, negZ});

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

static unsigned char voxelALL = 0xff;
static unsigned char voxelNONE = 0x00;

static ICoord3D singleVoxelOffset(unsigned char voxel) {
  // There must be a more elegant way of doing this, but this is
  // probably more efficient.
  if(voxel == vox000)
    return ICoord3D(-1, -1, -1);
  if(voxel == vox100)
    return ICoord3D(1, -1, -1);
  if(voxel == vox010)
    return ICoord3D(-1, 1, -1);
  if(voxel == vox110)
    return ICoord3D(1, 1, -1);
  if(voxel == vox001)
    return ICoord3D(-1, -1, 1);
  if(voxel == vox101)
    return ICoord3D(1, -1, 1);
  if(voxel == vox011)
    return ICoord3D(-1, 1, 1);
  if(voxel == vox111)
    return ICoord3D(1, 1, 1);
  throw ErrProgrammingError("Unexpected argument to singleVoxelOffset!",
			    __FILE__, __LINE__);
}

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

// A VoxRot (VoxelRotation) maps axes in the actual configuration to
// axes in the reference configuration and vice versa.  The arguments
// to the constructor are the actual space directions that correspond
// to the +x, +y, and +z directions in the reference space.

VoxRot::VoxRot(VoxelEdgeDirection d0, VoxelEdgeDirection d1,
	       VoxelEdgeDirection d2)
  : actualAxes({d0, d1, d2})
{
#ifdef DEBUG
  if(d0.axis == d1.axis || d1.axis == d2.axis || d2.axis == d0.axis) {
    oofcerr << "VoxRot::VoxRot: d0=" << d0 << " d1=" << d1 << " d2=" << d2
	    << std::endl;
    throw ErrProgrammingError("Badly specified voxel rotation!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
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
  throw ErrProgrammingError("VoxRot::toReference failed!",
			    __FILE__, __LINE__);
}

static const VoxRot noRotation(posX, posY, posZ);

std::ostream &operator<<(std::ostream &os, const VoxRot &rotation) {
  os << "[" << rotation.actualAxes[0] << "," << rotation.actualAxes[1]
     << "," << rotation.actualAxes[2] << "]";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ProtoVSBNode::ProtoVSBNode(const VoxRot &rot)
  : rotation(rot)
{}

VoxelEdgeDirection ProtoVSBNode::getReferenceDir(const ProtoVSBNode *that)
  const
{
  // Return the direction from this node to that node
  return rotation.toReference(
		      VoxelEdgeDirection(that->position() - position()));
}

// Given two voxels, decide if they're in canonical order or not. The
// answer is arbitrary, but must be the same for the other
// ProtoVSBNode that shares the two voxels.  The voxels are specified
// by the single voxel signatures, which define where they are
// relative to the center of the current ProtoVSBNode in its reference
// orientation.  The comparison is made using the *actual*
// orientation, so that it can be compared to a different
// ProtoVSBNode's view of the same two voxels.

bool ProtoVSBNode::voxelOrder(unsigned char sig0, unsigned char sig1) const {
  // Get the positions of the voxels relative to the center of the
  // 2x2x2 cube.
  assert(sig0 != sig1);
  ICoord3D v0 = singleVoxelOffset(sig0);
  ICoord3D v1 = singleVoxelOffset(sig1);
  // Find out which reference direction is the actual space x direction.
  VoxelEdgeDirection xdir = rotation.toReference(posX);
  int cmp = xdir.compare(v0, v1);
  if(cmp != 0)
    return cmp > 0;
  
  // The x components are the same.  Use y instead.
  VoxelEdgeDirection ydir = rotation.toReference(posY);
  cmp = ydir.compare(v0, v1);
  if(cmp != 0)
    return cmp > 0;

  // Use z.
  VoxelEdgeDirection zdir = rotation.toReference(posZ);
  cmp = zdir.compare(v0, v1);
  assert(cmp != 0);
  return cmp > 0;
}

#ifdef DEBUG
void ProtoVSBNode::checkDir(const VoxelEdgeDirection &dir) const {
  for(VoxelEdgeDirection allowed : connectDirs()) {
    if(allowed == dir)
      return;
  }
  oofcerr << "ProtoVSBNode::checkDir: this=" << *this
	  << " dir=" << dir << std::endl;
  oofcerr << "ProtoVSBNode::checkDir: connectDirs=";
  std::cerr << connectDirs();
  oofcerr << std::endl;
  throw ErrProgrammingError("ProtoVSBNode::checkDir failed!",
			    __FILE__, __LINE__);
}

std::ostream &operator<<(std::ostream &os, const ProtoVSBNode &pnode) {
  pnode.print(os);
  return os;
}

#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void SingleNode::makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D &here) {
  // oofcerr << "SingleNode::makeVSBNodes: here=" << here << std::endl;
  vsbNode = new VSBNode(here);
  vsb->addNode(vsbNode);
}

const Coord3D &SingleNode::position() const {
  assert(vsbNode != nullptr);
  return vsbNode->position;
}

void ProtoVSBNode::connectDoubleBack(const ProtoVSBNode*, VSBNode*, VSBNode*,
				     VSBNode*&, VSBNode*&)
{
  throw ErrProgrammingError("connectDoubleBack called illegally!",
			    __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const Coord3D &DoubleNode::position() const {
  assert(vsbNode0 != nullptr);
  return vsbNode0->position;
}

const Coord3D &TripleNode::position() const {
  assert(vsbNode0 != nullptr);
  return vsbNode0->position;
}

const Coord3D &MultiNode::position() const {
  assert(vsbNodes[0] != nullptr);
  return vsbNodes[0]->position;
}

void DoubleNode::makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D &here) {
  vsbNode0 = new VSBNode(here);
  vsbNode1 = new VSBNode(here);
  vsb->addNode(vsbNode0);
  vsb->addNode(vsbNode1);
}

void TripleNode::makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D  &here) {
  vsbNode0 = new VSBNode(here);
  vsbNode1 = new VSBNode(here);
  vsbNode2 = new VSBNode(here);
  vsb->addNode(vsbNode0);
  vsb->addNode(vsbNode1);
  vsb->addNode(vsbNode2);
}

void MultiNode::makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D  &here) {
  for(unsigned int i=0; i<vsbNodes.size(); i++) {
    vsbNodes[i] = new VSBNode(here);
    vsb->addNode(vsbNodes[i]);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// For a node at the corner of a single voxel, the reference
// configuration in the 2x2x2 cube has the voxel in the +x, +y, +z
// corner (vox111) and the neighbors in the +x, +y, +z directions.

class SingleVoxel : public SingleNode {
public:
  SingleVoxel(const VoxRot &rot)
    : SingleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new SingleVoxel(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNode);
    // The neighbors are in the +x, +y, and +z directions, so
    // inserting them in the neighbor list in that order puts them
    // CW when viewed from outside (from the -x, -y, -z side).
    vsbNode->setNeighbor(dir.axis, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    vsbNode->setNeighbor(dir.axis, othernode);
    return vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SingleVoxel(" << printSig(signature) << ", " << rotation
       << ")";
  }
#endif // DEBUG
};
 
//--------

// Seven voxels are just like one, except the "outside" is on the
// other side.  The only difference between SevenVoxels and
// SingleVoxel is that we need to ensure that the order of the +xyz
// axes is CCW, so the args to ensureClockwise are in a different
// order.

class SevenVoxels : public SingleNode {
public:
  SevenVoxels(const VoxRot &rot)
    : SingleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new SevenVoxels(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNode);
    // The neighbors are in the +x, +y, and +z directions, but
    // inserting them in the neighbor list in otherproto order would puts
    // them CCW when viewed from outside (from the +x, +y, +z side).
    // They're supposed to be CW, so switch 0 and 2.
    vsbNode->setNeighbor(2-dir.axis, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    vsbNode->setNeighbor(2-dir.axis, othernode);
    return vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SevenVoxels(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG

};

//--------

// Two voxels that share an edge.

class TwoVoxelsByEdge : public DoubleNode {
public:
  TwoVoxelsByEdge(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new TwoVoxelsByEdge(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    // The reference configuration is vox000 + vox110.  There are
    // edges in the posX, negX, posY, negY, and negZ directions.
    static const VoxelEdgeList v({posX, negX, posY, negY, negZ});
    return v;
  }

  /*
                 posZ  ^        ^  posY
                       |       /
                       |      /
                       |      
                            +--------+        The edges coming in to the 
                           /        /|        central vertex (X) are labeled 
                         0/        / |        with their neighbor indices.
                     1   /  1     /  |
    negX <---  ---------X--------+   +   --> posX
              /        /|        |  /
             /       0/ |2       | /
            /        /  |        |/ vox110
           +--------+   +--------+
           |        |  / 
           |        | /  
    vox000 |        |/   |
           +--------+    |
                         V negZ
                         
   */

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // The edges of vox000 connect to vsbNode0 and the edges of
    // vox110 to vsbNode1.  vox000's edges are negY, negX, negZ, in
    // that order (CW as viewed from outside (from +x+y+z).
    // Similarly, vox110's edges are posY, posX, negZ.
// #ifdef DEBUG
//     oofcerr << "TwoVoxelsByEdge::connect: position=" << position()
// 	    << " dir=" << dir << std::endl;
//     oofcerr << "TwoVoxelsByEdge::connect:  this=" << *this
// 	    << " node0=" << vsbNode0->getIndex()
// 	    << " node1=" << vsbNode1->getIndex()
// 	    << std::endl;
//     oofcerr << "TwoVoxelsByEdge::connect: other=" << *otherproto << std::endl;
// #endif // DEBUG
    
    if(dir == negX || dir == negY) {
      // Connect to vox000's edges, using vsbNode0.
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
// #ifdef DEBUG
//       oofcerr << "TwoVoxelsByEdge::connect: connecting VSBNodes "
// 	      << vsbNode0->getIndex() << " and " << othernode->getIndex()
// 	      << std::endl;
// #endif // DEBUG
      // Since dir.axis is 0 or 1, 1-dir.axis gives us the order we want.
      vsbNode0->setNeighbor(1-dir.axis, othernode); 
    }
    else if(dir == posX || dir == posY) {
      // Connect to vox110's edges, using vsbNode1.
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
// #ifdef DEBUG
//       oofcerr << "TwoVoxelsByEdge::connect: connecting VSBNodes "
// 	      << vsbNode1->getIndex() << " and " << othernode->getIndex()
// 	      << std::endl;
// #endif // DEBUG
      vsbNode1->setNeighbor(1-dir.axis, othernode);
    }
    else {
      // Both vsbNode0 and vsbNode1 connect in the negZ direction
      // along a doubled edge.  We need to ensure that the two split
      // nodes at the far end of the edge are connected to the
      // corresponding split nodes here.  If we think of the split
      // nodes as being separated slightly, we need to connect two
      // nodes that are separated in the same direction.

      // voxelOrder takes two voxels (assumed to be neighbors) and
      // returns a geometrically deduced bool.  If the voxels at the
      // other end of a doubled edge have the same relative position,
      // then voxelOrder will return the same bool for them.  When
      // connecting to split nodes, passing the nodes to
      // connectDoubleBack in the order in which voxelOrder is true
      // will guarantee that the connection is done correctly.
      assert(dir == negZ);
      bool ordered = voxelOrder(vox000, vox110);
      VSBNode *othernode0, *othernode1;
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
// #ifdef DEBUG
//       oofcerr << "TwoVoxelsByEdge::connect, calling connectDoubleBack,"
// 	<< " ordered=" << ordered << std::endl;
// #endif // DEBUG
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
// #ifdef DEBUG
//       oofcerr << "TwoVoxelsByEdge::connect: connecting node0="
// 	      << node0->getIndex() << " and othernode0="
// 	      << othernode0->getIndex() << std::endl;
//       oofcerr << "TwoVoxelsByEdge::connect: connecting node1="
// 	      << node1->getIndex() << " and othernode1="
// 	      << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
// #ifdef DEBUG
//     oofcerr << "TwoVoxelsByEdge::connectBack: position=" << position()
// 	   << " dir=" << dir << std::endl;
//     oofcerr << "TwoVoxelsByEdge::connectBack:  this=" << *this << std::endl;
//     oofcerr << "TwoVoxelsByEdge::connectBack: other=" << *otherproto
// 	    << std::endl;
// #endif // DEBUG
    if(dir == negX || dir == negY) {
      vsbNode0->setNeighbor(1-dir.axis, othernode);
// #ifdef DEBUG
//       oofcerr << "TwoVoxelsByEdge::connectBack: connecting "
// 	      << vsbNode0->getIndex() << " to " << othernode->getIndex()
// 	      << std::endl;
// #endif // DEBUG
      return vsbNode0;
    }
    if(dir == posX || dir == posY) {
      vsbNode1->setNeighbor(1-dir.axis, othernode);
// #ifdef DEBUG
//       oofcerr << "TwoVoxelsByEdge::connectBack: connecting "
// 	      << vsbNode1->getIndex() << " to " << othernode->getIndex()
// 	      << std::endl;
// #endif // DEBUG
      return vsbNode1;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in TwoVoxelsByEdge::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = voxelOrder(vox000, vox110);
    node0 = ordered ? vsbNode0 : vsbNode1;
    node1 = ordered ? vsbNode1 : vsbNode0;
// #ifdef DEBUG
//     oofcerr << "TwoVoxelsByEdge::connectDoubleBack: position=" << position()
// 	    << std::endl;
//     oofcerr << "TwoVoxelsByEdge::connectDoubleBack:  this=" << *this
// 	    << std::endl;
//     oofcerr << "TwoVoxelsByEdge::connectDoubleBack: other=" << *otherproto
// 	    << std::endl;
//     oofcerr << "TwoVoxelsByEdge::connectDoubleBack: node0=" << node0->getIndex()
// 	    << " othernode0=" << othernode0->getIndex() << std::endl;
//     oofcerr << "TwoVoxelsByEdge::connectDoubleBack: node1=" << node1->getIndex()
// 	    << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
    node0->setNeighbor(2, othernode0);
    node1->setNeighbor(2, othernode1);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "TwoVoxelsByEdge(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};  // end class TwoVoxelsByEdge

//-------------

// Two voxels that touch at a corner.

class TwoVoxelsByCorner : public DoubleNode {
public:
  TwoVoxelsByCorner(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new TwoVoxelsByCorner(rotation);}

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }
  
  virtual void connect(ProtoVSBNode *otherproto) {
    // TwoVoxelsByCorner is easier than TwoVoxelsByEdge, because there
    // aren't two connections going out in the same direction.  We can
    // simply say that the edges on vox000 connect to vsbNode0, and
    // the edges on vox111 connect to vsbNode1.  There's no
    // consistency to maintain at the other end of a doubled edge.
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir.dir == -1) {		// negX, negY, or negZ
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      // The edges around vox000 in CW order when viewed from +x+y+z
      // are negZ, negY, negX. 
      vsbNode0->setNeighbor(2-dir.axis, othernode);
    }
    else {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      // The edges around vox111 in CW order when viewed from -x-y-z
      // are posX, posY, pozY.
      vsbNode1->setNeighbor(dir.axis, othernode);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir.dir == -1) {
      vsbNode0->setNeighbor(2-dir.axis, othernode);
      return vsbNode0;
    }
    vsbNode1->setNeighbor(dir.axis, othernode);
    return vsbNode1;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "TwoVoxelsByCorner(" << printSig(signature) << ", " << rotation
       << ")";
  }
#endif // DEBUG
};	// end class TwoVoxelsByCorner
  
//--------

// SixVoxelsByEdge is the inverse of TwoVoxelsByEdge

class SixVoxelsByEdge : public DoubleNode {
public:
  SixVoxelsByEdge(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new SixVoxelsByEdge(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    // The reference configuration is vox000 + vox110.  There are
    // edges in the posX, negX, posY, negY, and negZ directions.
    static const VoxelEdgeList v({posX, negX, posY, negY, negZ});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // See comments in TwoVoxelsByEdge.  This is identical, except
    // that the order of the neighbors in the VSBNodes is reversed by
    // using dir.axis instead of 1-dir.axis in the X and Y calls to
    // setNeighbor.
    if(dir == negX || dir == negY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(dir.axis, othernode); 
    }
    else if(dir == posX || dir == posY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(dir.axis, othernode);
    }
    else {
      assert(dir == negZ);
      bool ordered = voxelOrder(vox000, vox110);
      VSBNode *othernode0, *othernode1;
      VSBNode *node0 = ordered? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered? vsbNode1 : vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX || dir == negY) {
      vsbNode0->setNeighbor(dir.axis, othernode);
      return vsbNode0;
    }
    else if(dir == posX || dir == posY) {
      vsbNode1->setNeighbor(dir.axis, othernode);
      return vsbNode1;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in SixVoxelsByEdge::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = voxelOrder(vox000, vox110);
    node0 = ordered ? vsbNode0 : vsbNode1;
    node1 = ordered ? vsbNode1 : vsbNode0;
    node0->setNeighbor(2, othernode0);
    node1->setNeighbor(2, othernode1);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SixVoxelsByEdge(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};  // end class SixVoxelsByEdge

//--------

// SixVoxelsByCorner is the inverse of TwoVoxelsByCorner

class SixVoxelsByCorner : public DoubleNode {
public:
  SixVoxelsByCorner(const VoxRot &rot)
    : DoubleNode(rot)
  {}
  virtual ProtoVSBNode *clone() const { return new SixVoxelsByCorner(rotation);}

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    // SixVoxelsByCorner is easier than SixVoxelsByEdge, because there
    // aren't two connections going out in the same direction.  We can
    // simply say that the edges on vox000 connect to vsbNode0, and
    // the edges on vox111 connect to vsbNode1.  There's no
    // consistency to maintain at the other end of a doubled edge.
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir.dir == -1) {		// negX, negY, or negZ
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      // The edges around vox000 in CW order when viewed from -x-y-z
      // are negX, negY, negZ. 
      vsbNode0->setNeighbor(dir.axis, othernode);
    }
    else {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      // The edges around vox111 in CW order when viewed from +x+y+z
      // are posZ, posY, pozX.
      vsbNode1->setNeighbor(2-dir.axis, othernode);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir.dir == -1) {
      vsbNode0->setNeighbor(dir.axis, othernode);
      return vsbNode0;
    }
    vsbNode1->setNeighbor(2-dir.axis, othernode);
    return vsbNode1;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SixVoxelsByCorner(" << printSig(signature) << ", " << rotation
       << ")";
  }
#endif // DEBUG
};
  
//----------

// Three voxels in an L configuration.  The node does not need to be
// split.  The reference configuration is vox000, vox100,
// vox010, with edges posX, posY, negZ in that order.

class ThreeVoxL : public SingleNode {
public:
  ThreeVoxL(const VoxRot &rot)
    : SingleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new ThreeVoxL(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negZ, posX, posY});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNode);
    vsbNode->setNeighbor(dir.axis, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    vsbNode->setNeighbor(dir.axis, othernode);
    return vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeVoxL(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

// ----------

// FiveVoxL is the inverse of ThreeVoxL.  The connections are
// the same, but the order is reversed.

class FiveVoxL : public SingleNode {
public:
  FiveVoxL(const VoxRot &rot)
    : SingleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new FiveVoxL(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negZ, posX, posY});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNode);
    vsbNode->setNeighbor(2-dir.axis, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    vsbNode->setNeighbor(2-dir.axis, othernode);
    return vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveVoxL(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

//---------

// ThreeTwoOne is three voxels, two stacked face to face and a third
// connected to one of the other two along an edge.  There are 24
// orientations.  The reference configuration contains voxels 000,
// 111, and 110.

class ThreeTwoOne : public DoubleNode {
public:
  ThreeTwoOne(const VoxRot &rot)
    : DoubleNode(rot)
  {}
  
  virtual ProtoVSBNode *clone() const { return new ThreeTwoOne(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negY, negX, negZ, posZ});
    return v;
  }

  void makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D &here) {
    vsbNode0 = new VSBNode(here);
    vsbNode1 = new VSBNode(here);
    vsb->addNode(vsbNode0);
    vsb->twoFoldNode(vsbNode1);
    // Don't add vsbNode1 to the graph! It's not a real node.
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // See comments in TwoVoxelsByEdge.  This is similar, but the
    // edges on vox110 are different, and its VSBNode will only be
    // connected to two edges, so we have to tell the VSB about it.
    // VSBNode0 is the 3-fold node, with edges on vox000 in the negX,
    // negY, and negZ directions.  VSBNode1 is the 2-fold node, on
    // vox110 and vox111, with edges negZ and posZ.
    
    if(dir == negX || dir == negY) {
      // Connecting to the edges on vox000
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(1-dir.axis, othernode);
    }
    else if(dir==posZ) {
      // Connecting to the edges on vox110
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else {
      // The double edge coming in on negZ.  To ensure compatibility
      // with the other ends of edge, use voxelOrder to determine the
      // order of the input and output args to connectDoubleBack.
      assert(dir == negZ);
      bool ordered = voxelOrder(vox000, vox110);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode1->setNeighbor(1, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX || dir == negY) {
      vsbNode0->setNeighbor(1-dir.axis, othernode);
      return vsbNode0;
    }
    if(dir == posZ) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in ThreeTwoOne::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = voxelOrder(vox000, vox110);
    if(ordered) {
      node0 = vsbNode0;
      node1 = vsbNode1;
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode1->setNeighbor(1, othernode1);
    }
    else {
      node0 = vsbNode1;
      node1 = vsbNode0;
      vsbNode0->setNeighbor(2, othernode1);
      vsbNode1->setNeighbor(1, othernode0);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeTwoOne(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end class ThreeTwoOne

//---------

// FiveTwoOne is the inverse of ThreeTwoOne

class FiveTwoOne : public DoubleNode {
public:
  FiveTwoOne(const VoxRot &rot)
    : DoubleNode(rot)
  {}
  
  virtual ProtoVSBNode *clone() const { return new FiveTwoOne(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negY, negX, negZ, posZ});
    return v;
  }

  void makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D &here) {
    vsbNode0 = new VSBNode(here);
    vsbNode1 = new VSBNode(here);
    vsb->addNode(vsbNode0);
    // Don't add vsbNode1 to the graph! It's not a real node.
    vsb->twoFoldNode(vsbNode1);
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // See comments in TwoVoxelsByEdge.  This is similar, but the
    // edges on vox110 are different, and its VSBNode will only be
    // connected to two edges, so we have to tell the VSB about it.
    // We always make VSBNode1 be the 2-fold node, so the logic is a
    // bit different from TwoVoxelsByEdge.
    
    if(dir == negX || dir == negY) {
      // Connecting to the edges on vox000
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(dir.axis, othernode);
    }
    else if(dir==posZ) {
      // Connecting to the edges on vox110
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else {
      // The double edge coming in on negZ.
      assert(dir == negZ);
      bool ordered = voxelOrder(vox000, vox110);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode1->setNeighbor(1, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX || dir == negY) {
      vsbNode0->setNeighbor(dir.axis, othernode);
      return vsbNode0;
    }
    if(dir == posZ) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in FiveTwoOne::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = voxelOrder(vox000, vox110);
    if(ordered) {
      node0 = vsbNode0;
      node1 = vsbNode1;
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode1->setNeighbor(1, othernode1);
    }
    else {
      node0 = vsbNode1;
      node1 = vsbNode0;
      vsbNode0->setNeighbor(2, othernode1);
      vsbNode1->setNeighbor(1, othernode0);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveTwoOne(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end class FiveTwoOne

//--------

// Three voxels that each share an edge with both of the others.  

class ThreeVoxByEdges : public TripleNode {
public:
  ThreeVoxByEdges(const VoxRot &rot)
    : TripleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new ThreeVoxByEdges(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // The reference configuration is vox110 + vox011 + vox101.
    // There are doubled edges in the +x, +y, and +z directions and
    // single edges in the -x, -y, and -z directions.  We use vsbNode0
    // for the edges of vox110, vsbNode1 for 101, and vsbNode2 for
    // 011.
    if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode2);
      vsbNode2->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      // Two edges between vox110 (VSBNode0) and vox101 (VSBNode1)
      bool ordered = voxelOrder(vox110, vox101);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // The edges on vsbNode0 (vox110) are (negZ, posY, posX),
      // CW.  This is posX, so it goes in slot 2.
      vsbNode0->setNeighbor(2, othernode0);
      // The edges on vsbNode1 (vox101) are (negY, posX, posZ),
      // CW.  This is posX, so it goes in slot 1.
      vsbNode1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      // Two edges between vox110 (VSBNode0) and vox011 (VSBNode2)
      bool ordered = voxelOrder(vox110, vox011);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode2;
      VSBNode *node1 = ordered ? vsbNode2 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negZ, posY, posX).
      vsbNode0->setNeighbor(1, othernode0);
      // Edges are (negX, posZ, posY)
      vsbNode2->setNeighbor(2, othernode1);
    }
    else if(dir == posZ) {
      // Two edges between vox101 (VSBNode1) and vox011 (VSBNode2)
      bool ordered = voxelOrder(vox101, vox011);
      VSBNode *node0 = ordered ? vsbNode1 : vsbNode2;
      VSBNode *node1 = ordered ? vsbNode2 : vsbNode1;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negY, posX, posZ)
      vsbNode1->setNeighbor(2, othernode0);
      // Edges are (negX, posZ, posY)
      vsbNode2->setNeighbor(1, othernode1);
    }
  } // end connect()

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX) {
      vsbNode2->setNeighbor(0, othernode);
      return vsbNode2;
    }
    if(dir == negY) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(0, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in ThreeVoxByEdges::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = voxelOrder(vox110, vox101);
      node0 = vsbNode0;
      node1 = vsbNode1;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      bool ordered = voxelOrder(vox110, vox011);
      node0 = vsbNode0;
      node1 = vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode0->setNeighbor(1, othernode0);
      vsbNode2->setNeighbor(2, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = voxelOrder(vox101, vox011);
      node0 = vsbNode1;
      node1 = vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode1->setNeighbor(2, othernode0);
      vsbNode2->setNeighbor(1, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeVoxByEdges(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end class ThreeVoxByEdges

//-----------

// FiveVoxByEdges is the inverse of ThreeVoxByEdges

class FiveVoxByEdges : public TripleNode {
public:
  FiveVoxByEdges(const VoxRot &rot)
    : TripleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new FiveVoxByEdges(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // The reference configuration is ~(vox110|vox011|vox101).
    // There are doubled edges in the +x, +y, and +z directions and
    // single edges in the -x, -y, and -z directions.  We use vsbNode0
    // for the edges of vox110, vsbNode1 for 101, and vsbNode2 for
    // 011.
    if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode2);
      vsbNode2->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      // Two edges between vox110 (VSBNode0) and vox101 (VSBNode1)
      bool ordered = voxelOrder(vox110, vox101);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // The edges on vsbNode0 (vox110) are (negZ, posX, posY),
      // CW.  This is posX, so it goes in slot 1.
      vsbNode0->setNeighbor(1, othernode0);
      // The edges on vsbNode1 (vox101) are (negY, posX, posZ),
      // CW.  This is posX, so it goes in slot 2.
      vsbNode1->setNeighbor(2, othernode1);
    }
    else if(dir == posY) {
      // Two edges between vox110 (VSBNode0) and vox011 (VSBNode2)
      bool ordered = voxelOrder(vox110, vox011);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode2;
      VSBNode *node1 = ordered ? vsbNode2 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negZ, posX, posY).
      vsbNode0->setNeighbor(2, othernode0);
      // Edges are (negX, posY, posZ)
      vsbNode2->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      // Two edges between vox101 (VSBNode1) and vox011 (VSBNode2)
      bool ordered = voxelOrder(vox101, vox011);
      VSBNode *node0 = ordered ? vsbNode1 : vsbNode2;
      VSBNode *node1 = ordered ? vsbNode2 : vsbNode1;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges on VSBNode1 are (negY, posZ, posX)
      vsbNode1->setNeighbor(1, othernode0);
      // Edges on VSBNode2 are (negX, posY, posZ)
      vsbNode2->setNeighbor(2, othernode1);
    }
  } // end connect()

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX) {
      vsbNode2->setNeighbor(0, othernode);
      return vsbNode2;
    }
    if(dir == negY) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(0, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in FiveVoxByEdges::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = voxelOrder(vox110, vox101);
      node0 = vsbNode0;
      node1 = vsbNode1;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode0->setNeighbor(1, othernode0);
      vsbNode1->setNeighbor(2, othernode1);
    }
    else if(dir == posY) {
      bool ordered = voxelOrder(vox110, vox011);
      node0 = vsbNode0;
      node1 = vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode2->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = voxelOrder(vox101, vox011);
      node0 = vsbNode1;
      node1 = vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode1->setNeighbor(1, othernode0);
      vsbNode2->setNeighbor(2, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveVoxByEdges(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end FiveVoxByEdges

//--------------

// Four voxels in the shape of two perpendicular stacks of two voxels.
// This configuration is chiral and requires an additional node to be
// created, although there are no multiply connected edges.

class ChiralR : public DoubleNode {
public:
  ChiralR(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new ChiralR(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, negX, posZ, negZ});
    return v;
  }

  virtual void makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D &here) {
    DoubleNode::makeVSBNodes(vsb, here);
    vsbNode0->setNeighbor(0, vsbNode1);
    vsbNode1->setNeighbor(0, vsbNode0);
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // Connect posX and negZ to VSBNode0, and negX and posZ to VSBNode1.
    // The two VSBNodes are already connected by a dummy edge, in makeVSBNodes.
    // VSBNode0's CW edges are [dummy], negZ, posX.
    // VSBNode1's CW edges are [dummy], negX, posZ.
    // The order of the edges is the reverse of the order in ChiralL.
    if(dir == posX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(2, othernode);
    }
    else if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(1, othernode);
    }
    else if(dir == posZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(2, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(1, othernode);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == posX) {
      vsbNode0->setNeighbor(2, othernode);
      return vsbNode0;
    }
    if(dir == negX) {
      vsbNode1->setNeighbor(1, othernode);
      return vsbNode1;
    }
    if(dir == posZ) {
      vsbNode1->setNeighbor(2, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(1, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError("Unexpected direction in ChiralR::connectBack!",
			      __FILE__, __LINE__);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ChiralR(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

//--------------

// The mirror image of ChiralR is ChiralL

class ChiralL : public DoubleNode {
public:
  ChiralL(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new ChiralL(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, negX, posZ, negZ});
    return v;
  }

  virtual void makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D &here) {
    DoubleNode::makeVSBNodes(vsb, here);
    vsbNode0->setNeighbor(0, vsbNode1);
    vsbNode1->setNeighbor(0, vsbNode0);
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // Connect posX and negZ to VSBNode0, and negX and posZ to VSBNode1.
    // The two VSBNodes are already connected by a dummy edge, in makeVSBNodes.
    // VSBNode0's CW edges are [dummy], posX, negZ.
    // VSBNode1's CW edges are [dummy], posZ, negX.
    // The order of the edges is the reverse of the order in ChiralR.
    if(dir == posX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(1, othernode);
    }
    else if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(2, othernode);
    }
    else if(dir == posZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(1, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(2, othernode);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == posX) {
      vsbNode0->setNeighbor(1, othernode);
      return vsbNode0;
    }
    if(dir == negX) {
      vsbNode1->setNeighbor(2, othernode);
      return vsbNode1;
    }
    if(dir == posZ) {
      vsbNode1->setNeighbor(1, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(2, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError("Unexpected direction in ChiralL::connectBack!",
			      __FILE__, __LINE__);
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ChiralL(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

//------------

// The Pyramid is 4 voxels stacked in a sort of skewed pyramid.  It
// contains one central voxel and the voxels on each of its faces.  An
// infinitesimal hexagonal face is inserted in the corner to convert
// the 6-fold vertex into 6 3-fold vertices.

class Pyramid : public MultiNode {
public:
  Pyramid(const VoxRot &rot)
    : MultiNode(6, rot)
  {}

  virtual ProtoVSBNode *clone() const { return new Pyramid(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void makeVSBNodes(VoxelSetBoundary *vsb, const ICoord3D &here) {
    MultiNode::makeVSBNodes(vsb, here);
    for(unsigned int i=0; i<6; i++) {
      // Neighbor 1 is the previous node in the hexagonal face.
      vsbNodes[i]->setNeighbor(1, vsbNodes[(i+5)%6]);
      // Neighbor 2 is the next node in the hexagonal face.
      vsbNodes[i]->setNeighbor(2, vsbNodes[(i+1)%6]);
    }
  }

  // hexDirIndex maps the directions to the nodes of the hexagon.  The
  // edge in direction dir intersects the hexagon at
  // vsbNodes[hexDirIndex(dir)].
  unsigned int hexDirIndex(const VoxelEdgeDirection &dir) const {
    if(dir == posX)
      return 0;
    if(dir == negZ)
      return 1;
    if(dir == posY)
      return 2;
    if(dir == negX)
      return 3;
    if(dir == posZ)
      return 4;
    assert(dir == negY);
    return 5;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    unsigned int i = hexDirIndex(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNodes[i]);
    vsbNodes[i]->setNeighbor(0, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    unsigned int i = hexDirIndex(dir);
    vsbNodes[i]->setNeighbor(0, othernode);
    return vsbNodes[i];
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "Pyramid(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

//----------

// Four voxels arranged in a checkerboard pattern, each sharing an
// edge with all of the others.  Each edge becomes a split edge, and
// there's one VSBNode for the inside corner of each voxel.

class CheckerBoard : public MultiNode {
public:
  CheckerBoard(const VoxRot &rot)
    : MultiNode(4, rot)
  {}

  ProtoVSBNode *clone() const { return new CheckerBoard(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    // The reference configuration is vox100 + vox010 + vox001 +
    // vox111.  Use VSBnodes[0] for vox100, 1 for vox010, 2 for
    // vox001, and 3 for vox111.  The assignment of neighbor indices
    // for the VSBNodes is arbitrary but consistent (and gets them all
    // CW, hopefully!)
// #ifdef DEBUG
//     oofcerr << "CheckerBoard::connect:  this=" << *this << std::endl;
//     oofcerr << "CheckerBoard::connect: other=" << *otherproto << std::endl;
//     OOFcerrIndent indent(2);
// #endif // DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
// #ifdef DEBUG
//     oofcerr << "CheckerBoard::connect: dir=" << dir << std::endl;
// #endif // DEBUG
    if(dir == posX) {
      // The posX edge is between voxels 100 and 111, so it connects
      // to vsbNodes 0 and 3.
      bool ordered = voxelOrder(vox100, vox111);
      VSBNode *node0 = ordered ? vsbNodes[0] : vsbNodes[3];
      VSBNode *node1 = ordered ? vsbNodes[3] : vsbNodes[0];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connect: othernode0=" << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[0]->setNeighbor(0, othernode0);
      vsbNodes[3]->setNeighbor(2, othernode1);
    }
    else if(dir == negX) {
      // negX is between voxels 001 and 010, connecting to vsbNodes 2
      // and 1.
      bool ordered = voxelOrder(vox001, vox010);
      VSBNode *node0 = ordered ? vsbNodes[2] : vsbNodes[1];
      VSBNode *node1 = ordered ? vsbNodes[1] : vsbNodes[2];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connect: othernode0=" << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[2]->setNeighbor(1, othernode0);
      vsbNodes[1]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      // posY is between voxels 010 and 111, connecting to vsbNodes 1
      // and 3.
      bool ordered = voxelOrder(vox010, vox111);
      VSBNode *node0 = ordered ? vsbNodes[1] : vsbNodes[3];
      VSBNode *node1 = ordered ? vsbNodes[3] : vsbNodes[1];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connect: othernode0=" << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[1]->setNeighbor(1, othernode0);
      vsbNodes[3]->setNeighbor(0, othernode1);
    }
    else if(dir == negY) {
      // negY is between voxels 001 and 100, connecting to vsbNodes 2
      // and 0.
      bool ordered = voxelOrder(vox001, vox100);
      VSBNode *node0 = ordered ? vsbNodes[2] : vsbNodes[0];
      VSBNode *node1 = ordered ? vsbNodes[0] : vsbNodes[2];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connect: othernode0=" << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[2]->setNeighbor(2, othernode0);
      vsbNodes[0]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      // posZ is between voxels 001 and 111, connecting to vsbNodes 2
      // and 3.
      bool ordered = voxelOrder(vox001, vox111);
      VSBNode *node0 = ordered ? vsbNodes[2] : vsbNodes[3];
      VSBNode *node1 = ordered ? vsbNodes[3] : vsbNodes[2];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connect: othernode0=" << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[2]->setNeighbor(0, othernode0);
      vsbNodes[3]->setNeighbor(1, othernode1);
    }
    else if(dir == negZ) {
      // negZ is between voxels 100 and 010, connecting to vsbNodes 0
      // and 1.
      bool ordered = voxelOrder(vox100, vox010);
      VSBNode *node0 = ordered ? vsbNodes[0] : vsbNodes[1];
      VSBNode *node1 = ordered ? vsbNodes[1] : vsbNodes[0];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connect: ordered=" << ordered
// 	      << " othernode0=" << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[0]->setNeighbor(2, othernode0);
      vsbNodes[1]->setNeighbor(2, othernode1);
    }
  } // end CheckerBoard::connect

  virtual VSBNode *connectBack(const ProtoVSBNode*, VSBNode*) {
    throw ErrProgrammingError("CheckerBoard::connectBack should not be called!",
			      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
// #ifdef DEBUG
//     oofcerr << "CheckerBoard::connectDoubleBack:  this=" << *this << std::endl;
//     oofcerr << "CheckerBoard::connectDoubleBack: other=" << *otherproto
// 	    << std::endl;
//     oofcerr << "CheckerBoard::connectDoubleBack: dir=" << dir << std::endl;
//     oofcerr << "CheckerBoard::connectDoubleBack: othernode0=" << othernode0
// 	    << " othernode1=" << othernode1 << std::endl;
//     OOFcerrIndent indent(2);
// #endif // DEBUG
    // See comments in CheckerBoard::connect.
    if(dir == posX) {
      bool ordered = voxelOrder(vox100, vox111);
      node0 = vsbNodes[0];
      node1 = vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connectDoubleBack: othernode0="
// 	      << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[0]->setNeighbor(0, othernode0);
      vsbNodes[3]->setNeighbor(2, othernode1);
    }
    else if(dir == negX) {
      bool ordered = voxelOrder(vox001, vox010);
      node0 = vsbNodes[2];
      node1 = vsbNodes[1];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connectDoubleBack: othernode0="
// 	      << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[2]->setNeighbor(1, othernode0);
      vsbNodes[1]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      bool ordered = voxelOrder(vox010, vox111);
      node0 = vsbNodes[1];
      node1 = vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connectDoubleBack: othernode0="
// 	      << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[1]->setNeighbor(1, othernode0);
      vsbNodes[3]->setNeighbor(0, othernode1);
    }
    else if(dir == negY) {
      bool ordered = voxelOrder(vox001, vox100);
      node0 = vsbNodes[2];
      node1 = vsbNodes[0];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connectDoubleBack: othernode0="
// 	      << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[2]->setNeighbor(2, othernode0);
      vsbNodes[0]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = voxelOrder(vox001, vox111);
      node0 = vsbNodes[2];
      node1 = vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connectDoubleBack: othernode0="
// 	      << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[2]->setNeighbor(0, othernode0);
      vsbNodes[3]->setNeighbor(1, othernode1);
    }
    else if(dir == negZ) {
      bool ordered = voxelOrder(vox100, vox010);
      node0 = vsbNodes[0];
      node1 = vsbNodes[1];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
// #ifdef DEBUG
//       oofcerr << "CheckerBoard::connectDoubleBack: othernode0="
// 	      << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() << std::endl;
// #endif // DEBUG
      vsbNodes[0]->setNeighbor(2, othernode0);
      vsbNodes[1]->setNeighbor(2, othernode1);
    }
// #ifdef DEBUG
//     oofcerr << "CheckerBoard::connectDoubleBack: node0=" << node0
// 	    << " node1=" << node1 << std::endl;
//     oofcerr << "CheckerBoard::connectDoubleBack: done" << std::endl;
// #endif // DEBUG
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "CheckerBoard(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end class CheckerBoard

//-------------

// FourThreeOne is three voxels in an L with one more voxel out of the
// plane of the L and over the gap.

class FourThreeOne : public DoubleNode {
public:
  FourThreeOne(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new FourThreeOne(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ, negZ});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    // The reference configuration is three voxels in the Z=0 plane,
    // vox000, vox100 and vox010, just like ThreeVoxL, plus one voxel
    // at vox111.  The three in the L are connected to vsbNode0 and
    // the single voxel is connected to vsbNode1.  The edges in the
    // posX and posY directions are doubled.

    // Neighbor indexing for the edges of the single voxel at vox111
    // is posZ, posX, posY.  For the inside corner of the L it's negZ,
    // posX, posY.
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == posZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      bool ordered = voxelOrder(vox100, vox111);
      VSBNode *othernode0, *othernode1;
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
// #ifdef DEBUG
//       oofcerr << "FourThreeOne::connect: dir=posX, ordered=" << ordered
// 	      << " node0=" << node0->getIndex()
// 	      << " node1=" << node1->getIndex() << std::endl;
// #endif // DEBUG
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      // Conveniently the posX and posY neighbor indexing is the same
      // for both nodes.
      node0->setNeighbor(1, othernode0);
      node1->setNeighbor(1, othernode1);
    }
    else {
      assert(dir == posY);
      bool ordered = voxelOrder(vox010, vox111);
      VSBNode *othernode0, *othernode1;
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
// #ifdef DEBUG
//       oofcerr << "FourThreeOne::connect: dir=posY, ordered=" << ordered
// 	      << " node0=" << node0->getIndex()
// 	      << " node1=" << node1->getIndex() << std::endl;
// #endif // DEBUG
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posZ) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(0, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in FourThreeOne::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
// #ifdef DEBUG
//     oofcerr << "FourThreeOne::connectDoubleBack: this=" << *this << std::endl;
// #endif // DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = voxelOrder(vox100, vox111);
      node0 = ordered ? vsbNode0 : vsbNode1;
      node1 = ordered ? vsbNode1 : vsbNode0;
// #ifdef DEBUG
//       oofcerr << "FourThreeOne::connectDoubleBack: dir=posX, ordered="
// 	      << ordered
// 	      << " othernode0=" << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() 
// 	      << " node0=" << node0->getIndex()
// 	      << " node1=" << node1->getIndex() << std::endl;
// #endif // DEBUG
      node0->setNeighbor(1, othernode0);
      node1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      bool ordered = voxelOrder(vox010, vox111);
      node0 = ordered ? vsbNode0 : vsbNode1;
      node1 = ordered ? vsbNode1 : vsbNode0;
// #ifdef DEBUG
//       oofcerr << "FourThreeOne::connectDoubleBack: dir=posY, ordered="
// 	      << ordered
// 	      << " othernode0=" << othernode0->getIndex()
// 	      << " othernode1=" << othernode1->getIndex() 
// 	      << " node0=" << node0->getIndex()
// 	      << " node1=" << node1->getIndex() << std::endl;
// #endif // DEBUG
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
    else {
      oofcerr << "FourThreeOne::connectDoubleBack: position="
	      << position() << " other position=" << otherproto->position()
	      << " rotation=" << rotation
	      << " dir=" << dir << std::endl;
      throw ErrProgrammingError(
	      "Unexpected direction in FourThreeOne::connectDoubleBack!",
	      __FILE__, __LINE__);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FourThreeOne(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};	// end class FourThreeOne

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static std::vector<const ProtoVSBNode*> protoNodeTable(256, nullptr);

static void pn(unsigned char signature, const ProtoVSBNode *protoNode) {
#ifdef DEBUG
  if(protoNode != nullptr)
    protoNode->setSignature(signature);
  if(protoNodeTable[signature] != nullptr) {
    oofcerr << "Duplicate signature! " << signature << " "
	    << printSig(signature) << std::endl;
    throw ErrProgrammingError("Duplicate ProtoVSBNode signature!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  protoNodeTable[signature] = protoNode;
}

void initializeProtoNodes() {
  // Create an instance of each ProtoVSBNode class in each orientation
  // and store it in a table indexed by the voxel signature for that
  // configuration.  The table is used to create the ProtoVSBNodes
  // when a CMicrostructure is computing voxel set boundaries.

  // First, the configurations that *don't* define a vertex.
  // Including these explicitly just helps us to be sure that we
  // covered all the cases.
  
  // The trivial cases:
  pn(voxelNONE, nullptr); // no voxels
  pn(voxelALL, nullptr); // all 8 voxels

  // Two adjacent voxels sharing a face (the butterstick
  // configurations) don't define a vertex.  There are 12
  // possibilities:
  pn(vox000|vox001, nullptr);
  pn(vox010|vox011, nullptr);
  pn(vox100|vox101, nullptr);
  pn(vox110|vox111, nullptr);
  pn(vox000|vox010, nullptr);
  pn(vox001|vox011, nullptr);
  pn(vox100|vox110, nullptr);
  pn(vox101|vox111, nullptr);
  pn(vox000|vox100, nullptr);
  pn(vox001|vox101, nullptr);
  pn(vox010|vox110, nullptr);
  pn(vox011|vox111, nullptr);
  // Ditto for the 12 inverse buttersticks (two holes sharing a face).
  pn(~(vox000|vox001), nullptr);
  pn(~(vox010|vox011), nullptr);
  pn(~(vox100|vox101), nullptr);
  pn(~(vox110|vox111), nullptr);
  pn(~(vox000|vox010), nullptr);
  pn(~(vox001|vox011), nullptr);
  pn(~(vox100|vox110), nullptr);
  pn(~(vox101|vox111), nullptr);
  pn(~(vox000|vox100), nullptr);
  pn(~(vox001|vox101), nullptr);
  pn(~(vox010|vox110), nullptr);
  pn(~(vox011|vox111), nullptr);

  // Four voxels in one plane don't define a vertex.  There are 6
  // configurations:
  pn(vox000|vox001|vox010|vox011, nullptr); // x=0
  pn(vox100|vox101|vox110|vox111, nullptr); // x=1
  pn(vox000|vox100|vox001|vox101, nullptr); // y=0
  pn(vox010|vox110|vox011|vox111, nullptr); // y=1
  pn(vox000|vox010|vox100|vox110, nullptr); // z=0
  pn(vox001|vox011|vox101|vox111, nullptr); // z=1
  
  // Two parallel offset stacks of two voxels don't define a vertex.
  pn(vox000|vox001|vox110|vox111, nullptr);
  pn(vox100|vox101|vox010|vox011, nullptr);
  pn(vox000|vox100|vox011|vox111, nullptr);
  pn(vox001|vox101|vox010|vox110, nullptr);
  pn(vox001|vox011|vox100|vox110, nullptr);
  pn(vox000|vox010|vox101|vox111, nullptr);

  // Now the real cases:
  pn(vox111, new SingleVoxel(VoxRot(posX, posY, posZ)));
  pn(vox101, new SingleVoxel(VoxRot(negY, posX, posZ)));
  pn(vox001, new SingleVoxel(VoxRot(negX, negY, posZ)));
  pn(vox011, new SingleVoxel(VoxRot(posY, negX, posZ)));
  pn(vox000, new SingleVoxel(VoxRot(negY, negX, negZ)));
  pn(vox010, new SingleVoxel(VoxRot(negX, posY, negZ)));
  pn(vox110, new SingleVoxel(VoxRot(posY, posX, negZ)));
  pn(vox100, new SingleVoxel(VoxRot(posX, negY, negZ)));

  pn(~vox111, new SevenVoxels(VoxRot(posX, posY, posZ)));
  pn(~vox101, new SevenVoxels(VoxRot(negY, posX, posZ)));
  pn(~vox001, new SevenVoxels(VoxRot(negX, negY, posZ)));
  pn(~vox011, new SevenVoxels(VoxRot(posY, negX, posZ)));
  pn(~vox000, new SevenVoxels(VoxRot(negY, negX, negZ)));
  pn(~vox010, new SevenVoxels(VoxRot(negX, posY, negZ)));
  pn(~vox110, new SevenVoxels(VoxRot(posY, posX, negZ)));
  pn(~vox100, new SevenVoxels(VoxRot(posX, negY, negZ)));

  pn(vox000|vox110, new TwoVoxelsByEdge(VoxRot(posX, posY, posZ)));
  pn(vox010|vox100, new TwoVoxelsByEdge(VoxRot(posY, negX, posZ)));
  pn(vox001|vox111, new TwoVoxelsByEdge(VoxRot(negY, negX, negZ)));
  pn(vox101|vox011, new TwoVoxelsByEdge(VoxRot(posX, negY, negZ)));
  pn(vox100|vox111, new TwoVoxelsByEdge(VoxRot(posZ, posY, negX)));
  pn(vox101|vox110, new TwoVoxelsByEdge(VoxRot(posY, negZ, negX)));
  pn(vox000|vox011, new TwoVoxelsByEdge(VoxRot(negY, negZ, posX)));
  pn(vox001|vox010, new TwoVoxelsByEdge(VoxRot(negZ, posY, posX)));
  pn(vox010|vox111, new TwoVoxelsByEdge(VoxRot(posX, posZ, negY)));
  pn(vox110|vox011, new TwoVoxelsByEdge(VoxRot(negZ, posX, negY)));
  pn(vox000|vox101, new TwoVoxelsByEdge(VoxRot(negZ, negX, posY)));
  pn(vox001|vox100, new TwoVoxelsByEdge(VoxRot(negX, posZ, posY)));

  pn(~(vox000|vox110), new SixVoxelsByEdge(VoxRot(posX, posY, posZ)));
  pn(~(vox010|vox100), new SixVoxelsByEdge(VoxRot(posY, negX, posZ)));
  pn(~(vox001|vox111), new SixVoxelsByEdge(VoxRot(negY, negX, negZ)));
  pn(~(vox101|vox011), new SixVoxelsByEdge(VoxRot(posX, negY, negZ)));
  pn(~(vox100|vox111), new SixVoxelsByEdge(VoxRot(posZ, posY, negX)));
  pn(~(vox101|vox110), new SixVoxelsByEdge(VoxRot(posY, negZ, negX)));
  pn(~(vox000|vox011), new SixVoxelsByEdge(VoxRot(negY, negZ, posX)));
  pn(~(vox001|vox010), new SixVoxelsByEdge(VoxRot(negZ, posY, posX)));
  pn(~(vox010|vox111), new SixVoxelsByEdge(VoxRot(posX, posZ, negY)));
  pn(~(vox110|vox011), new SixVoxelsByEdge(VoxRot(negZ, posX, negY)));
  pn(~(vox000|vox101), new SixVoxelsByEdge(VoxRot(negZ, negX, posY)));
  pn(~(vox001|vox100), new SixVoxelsByEdge(VoxRot(negX, posZ, posY)));

  // pn(~(vox000|vox110), new SixVoxelsByEdge(VoxRot(posX, posY, posZ)));
  // pn(~(vox010|vox100), new SixVoxelsByEdge(VoxRot(posY, negX, posZ)));
  // pn(~(vox001|vox111), new SixVoxelsByEdge(VoxRot(negY, negX, negZ)));//
  // pn(~(vox011|vox101), new SixVoxelsByEdge(VoxRot(posY, posX, negZ)));
  // pn(~(vox000|vox011), new SixVoxelsByEdge(VoxRot(negZ, posY, posX)));
  // pn(~(vox001|vox010), new SixVoxelsByEdge(VoxRot(posZ, negY, posX)));
  // pn(~(vox100|vox111), new SixVoxelsByEdge(VoxRot(posZ, posY, negX)));
  // pn(~(vox110|vox101), new SixVoxelsByEdge(VoxRot(negY, posZ, negX)));
  // pn(~(vox000|vox101), new SixVoxelsByEdge(VoxRot(negZ, negX, posY)));
  // pn(~(vox100|vox001), new SixVoxelsByEdge(VoxRot(negX, posZ, posY)));
  // pn(~(vox010|vox111), new SixVoxelsByEdge(VoxRot(posX, posZ, negY)));
  // pn(~(vox110|vox011), new SixVoxelsByEdge(VoxRot(posZ, negX, negY)));

  pn(vox000|vox111, new TwoVoxelsByCorner(VoxRot(posX, posY, posZ)));
  pn(vox100|vox011, new TwoVoxelsByCorner(VoxRot(posY, negX, posZ)));
  pn(vox110|vox001, new TwoVoxelsByCorner(VoxRot(negX, negY, posZ)));
  pn(vox010|vox101, new TwoVoxelsByCorner(VoxRot(negY, posX, posZ)));

  pn(~(vox000|vox111), new SixVoxelsByCorner(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox011), new SixVoxelsByCorner(VoxRot(posY, negX, posZ)));
  pn(~(vox110|vox001), new SixVoxelsByCorner(VoxRot(negX, negY, posZ)));
  pn(~(vox010|vox101), new SixVoxelsByCorner(VoxRot(negY, posX, posZ)));

  // Three voxels in the Z=0 plane
  pn(vox000|vox100|vox010, new ThreeVoxL(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox110, new ThreeVoxL(VoxRot(posY, negX, posZ)));
  pn(vox100|vox110|vox010, new ThreeVoxL(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110, new ThreeVoxL(VoxRot(negY, posX, posZ)));
  // Three voxels in the Z=1 plane
  pn(vox001|vox101|vox011, new ThreeVoxL(VoxRot(posY, posX, negZ)));
  pn(vox111|vox011|vox001, new ThreeVoxL(VoxRot(posX, negY, negZ)));
  pn(vox101|vox111|vox011, new ThreeVoxL(VoxRot(negY, negX, negZ)));
  pn(vox101|vox111|vox001, new ThreeVoxL(VoxRot(negX, posY, negZ)));
  // Three voxels in the X=0 plane
  pn(vox000|vox010|vox001, new ThreeVoxL(VoxRot(posY, posZ, posX)));
  pn(vox000|vox001|vox011, new ThreeVoxL(VoxRot(negZ, posY, posX)));
  pn(vox001|vox011|vox010, new ThreeVoxL(VoxRot(negY, negZ, posX)));
  pn(vox000|vox010|vox011, new ThreeVoxL(VoxRot(posZ, negY, posX)));
  // Three voxels in the X=1 plane
  pn(vox100|vox101|vox110, new ThreeVoxL(VoxRot(posZ, posY, negX)));
  pn(vox111|vox101|vox100, new ThreeVoxL(VoxRot(posY, negZ, negX)));
  pn(vox101|vox111|vox110, new ThreeVoxL(VoxRot(negZ, negY, negX)));
  pn(vox111|vox110|vox100, new ThreeVoxL(VoxRot(negY, posZ, negX)));
  // Three voxels in the Y=0 plane
  pn(vox000|vox100|vox001, new ThreeVoxL(VoxRot(posZ, posX, posY)));
  pn(vox000|vox001|vox101, new ThreeVoxL(VoxRot(posX, negZ, posY)));
  pn(vox001|vox101|vox100, new ThreeVoxL(VoxRot(negZ, negX, posY)));
  pn(vox000|vox100|vox101, new ThreeVoxL(VoxRot(negX, posZ, posY)));
  // Three voxels in the Y=1 plane
  pn(vox110|vox010|vox011, new ThreeVoxL(VoxRot(posX, posZ, negY)));
  pn(vox111|vox011|vox010, new ThreeVoxL(VoxRot(negZ, posX, negY)));
  pn(vox111|vox011|vox110, new ThreeVoxL(VoxRot(negX, negZ, negY)));
  pn(vox110|vox010|vox111, new ThreeVoxL(VoxRot(posZ, negX, negY)));

  pn(~(vox100|vox101|vox110), new FiveVoxL(VoxRot(posZ, posY, negX)));
  pn(~(vox111|vox101|vox100), new FiveVoxL(VoxRot(posY, negZ, negX)));
  pn(~(vox101|vox111|vox110), new FiveVoxL(VoxRot(negZ, negY, negX)));
  pn(~(vox111|vox110|vox100), new FiveVoxL(VoxRot(negY, posZ, negX)));
  pn(~(vox000|vox010|vox001), new FiveVoxL(VoxRot(posY, posZ, posX)));
  pn(~(vox000|vox001|vox011), new FiveVoxL(VoxRot(negZ, posY, posX)));
  pn(~(vox001|vox011|vox010), new FiveVoxL(VoxRot(negY, negZ, posX)));
  pn(~(vox000|vox010|vox011), new FiveVoxL(VoxRot(posZ, negY, posX)));
  pn(~(vox110|vox010|vox011), new FiveVoxL(VoxRot(posX, posZ, negY)));
  pn(~(vox111|vox011|vox010), new FiveVoxL(VoxRot(negZ, posX, negY)));
  pn(~(vox111|vox011|vox110), new FiveVoxL(VoxRot(negX, negZ, negY)));
  pn(~(vox110|vox010|vox111), new FiveVoxL(VoxRot(posZ, negX, negY)));
  pn(~(vox000|vox100|vox001), new FiveVoxL(VoxRot(posZ, posX, posY)));
  pn(~(vox000|vox001|vox101), new FiveVoxL(VoxRot(posX, negZ, posY)));
  pn(~(vox001|vox101|vox100), new FiveVoxL(VoxRot(negZ, negX, posY)));
  pn(~(vox000|vox100|vox101), new FiveVoxL(VoxRot(negX, posZ, posY)));
  pn(~(vox001|vox101|vox011), new FiveVoxL(VoxRot(posY, posX, negZ)));
  pn(~(vox111|vox011|vox001), new FiveVoxL(VoxRot(posX, negY, negZ)));
  pn(~(vox101|vox111|vox011), new FiveVoxL(VoxRot(negY, negX, negZ)));
  pn(~(vox101|vox111|vox001), new FiveVoxL(VoxRot(negX, posY, negZ)));
  pn(~(vox000|vox100|vox010), new FiveVoxL(VoxRot(posX, posY, posZ)));
  pn(~(vox000|vox100|vox110), new FiveVoxL(VoxRot(posY, negX, posZ)));
  pn(~(vox100|vox110|vox010), new FiveVoxL(VoxRot(negX, negY, posZ)));
  pn(~(vox000|vox010|vox110), new FiveVoxL(VoxRot(negY, posX, posZ)));

  // Double stack in the z direction, single voxel in the z=0 plane
  pn(vox000|vox110|vox111, new ThreeTwoOne(VoxRot(posX, posY, posZ)));
  pn(vox100|vox010|vox011, new ThreeTwoOne(VoxRot(posY, negX, posZ)));
  pn(vox000|vox110|vox001, new ThreeTwoOne(VoxRot(negX, negY, posZ)));
  pn(vox100|vox010|vox101, new ThreeTwoOne(VoxRot(negY, posX, posZ)));
  // Double stack in the z direction, single voxel in the z=1 plane
  pn(vox001|vox110|vox111, new ThreeTwoOne(VoxRot(posY, posX, negZ)));
  pn(vox010|vox011|vox101, new ThreeTwoOne(VoxRot(negX, posY, negZ)));
  pn(vox000|vox001|vox111, new ThreeTwoOne(VoxRot(negY, negX, negZ)));
  pn(vox100|vox101|vox011, new ThreeTwoOne(VoxRot(posX, negY, negZ)));
  // Double stack in the x direction, single voxel in the x=1 plane
  pn(vox000|vox100|vox111, new ThreeTwoOne(VoxRot(negZ, negY, negX)));
  pn(vox001|vox110|vox101, new ThreeTwoOne(VoxRot(negY, posZ, negX)));
  pn(vox100|vox011|vox111, new ThreeTwoOne(VoxRot(posZ, posY, negX)));
  pn(vox101|vox110|vox010, new ThreeTwoOne(VoxRot(posY, negZ, negX)));
  // Double stack in the x direction, single voxel in the x=0 plane
  pn(vox000|vox100|vox011, new ThreeTwoOne(VoxRot(negY, negZ, posX)));
  pn(vox010|vox001|vox101, new ThreeTwoOne(VoxRot(posZ, negY, posX)));
  pn(vox000|vox011|vox111, new ThreeTwoOne(VoxRot(posY, posZ, posX)));
  pn(vox001|vox010|vox110, new ThreeTwoOne(VoxRot(negZ, posY, posX)));
  // Double stack in the y direction, single voxel in the x=0 plane
  pn(vox000|vox010|vox101, new ThreeTwoOne(VoxRot(negZ, negX, posY)));
  pn(vox001|vox100|vox110, new ThreeTwoOne(VoxRot(posX, negZ, posY)));
  pn(vox000|vox101|vox111, new ThreeTwoOne(VoxRot(posZ, posX, posY)));
  pn(vox100|vox001|vox011, new ThreeTwoOne(VoxRot(negX, posZ, posY)));
  // Double stack in the y direction, single voxel in the x=1 plane
  pn(vox000|vox010|vox111, new ThreeTwoOne(VoxRot(negX, negZ, negY)));
  pn(vox110|vox001|vox011, new ThreeTwoOne(VoxRot(posZ, negX, negY)));
  pn(vox010|vox101|vox111, new ThreeTwoOne(VoxRot(posX, posZ, negY)));
  pn(vox100|vox110|vox011, new ThreeTwoOne(VoxRot(negZ, posX, negY)));

  // Double stack in the z direction, single hole in the z=0 plane
  pn(~(vox000|vox110|vox111), new FiveTwoOne(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox010|vox011), new FiveTwoOne(VoxRot(posY, negX, posZ)));
  pn(~(vox000|vox110|vox001), new FiveTwoOne(VoxRot(negX, negY, posZ)));
  pn(~(vox100|vox010|vox101), new FiveTwoOne(VoxRot(negY, posX, posZ)));
  // Double stack in the z direction, single hole in the z=1 plane
  pn(~(vox001|vox110|vox111), new FiveTwoOne(VoxRot(posY, posX, negZ)));
  pn(~(vox010|vox011|vox101), new FiveTwoOne(VoxRot(negX, posY, negZ)));
  pn(~(vox000|vox001|vox111), new FiveTwoOne(VoxRot(negY, negX, negZ)));
  pn(~(vox100|vox101|vox011), new FiveTwoOne(VoxRot(posX, negY, negZ)));
  // Double stack in the x direction, single hole in the x=1 plane
  pn(~(vox000|vox100|vox111), new FiveTwoOne(VoxRot(negZ, negY, negX)));
  pn(~(vox001|vox110|vox101), new FiveTwoOne(VoxRot(negY, posZ, negX)));
  pn(~(vox100|vox011|vox111), new FiveTwoOne(VoxRot(posZ, posY, negX)));
  pn(~(vox101|vox110|vox010), new FiveTwoOne(VoxRot(posY, negZ, negX)));
  // Double stack in the x direction, single hole in the x=0 plane
  pn(~(vox000|vox100|vox011), new FiveTwoOne(VoxRot(negY, negZ, posX)));
  pn(~(vox010|vox001|vox101), new FiveTwoOne(VoxRot(posZ, negY, posX)));
  pn(~(vox000|vox011|vox111), new FiveTwoOne(VoxRot(posY, posZ, posX)));
  pn(~(vox001|vox010|vox110), new FiveTwoOne(VoxRot(negZ, posY, posX)));
  // Double stack in the y direction, single hole in the x=0 plane
  pn(~(vox000|vox010|vox101), new FiveTwoOne(VoxRot(negZ, negX, posY)));
  pn(~(vox001|vox100|vox110), new FiveTwoOne(VoxRot(posX, negZ, posY)));
  pn(~(vox000|vox101|vox111), new FiveTwoOne(VoxRot(posZ, posX, posY)));
  pn(~(vox100|vox001|vox011), new FiveTwoOne(VoxRot(negX, posZ, posY)));
  // Double stack in the y direction, single hole in the x=1 plane
  pn(~(vox000|vox010|vox111), new FiveTwoOne(VoxRot(negX, negZ, negY)));
  pn(~(vox110|vox001|vox011), new FiveTwoOne(VoxRot(posZ, negX, negY)));
  pn(~(vox010|vox101|vox111), new FiveTwoOne(VoxRot(posX, posZ, negY)));
  pn(~(vox100|vox110|vox011), new FiveTwoOne(VoxRot(negZ, posX, negY)));

  pn(vox110|vox011|vox101, new ThreeVoxByEdges(VoxRot(posX, posY, posZ)));
  pn(vox100|vox001|vox111, new ThreeVoxByEdges(VoxRot(negY, posX, posZ)));
  pn(vox000|vox101|vox011, new ThreeVoxByEdges(VoxRot(negX, negY, posZ)));
  pn(vox010|vox001|vox111, new ThreeVoxByEdges(VoxRot(posY, negX, posZ)));

  pn(vox111|vox100|vox010, new ThreeVoxByEdges(VoxRot(posY, posX, negZ)));
  pn(vox000|vox110|vox101, new ThreeVoxByEdges(VoxRot(posX, negY, negZ)));
  pn(vox100|vox010|vox001, new ThreeVoxByEdges(VoxRot(negY, negX, negZ)));
  pn(vox000|vox011|vox110, new ThreeVoxByEdges(VoxRot(negX, posY, negZ)));

  pn(~(vox110|vox011|vox101), new FiveVoxByEdges(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox001|vox111), new FiveVoxByEdges(VoxRot(negY, posX, posZ)));
  pn(~(vox000|vox101|vox011), new FiveVoxByEdges(VoxRot(negX, negY, posZ)));
  pn(~(vox010|vox001|vox111), new FiveVoxByEdges(VoxRot(posY, negX, posZ)));

  pn(~(vox111|vox100|vox010), new FiveVoxByEdges(VoxRot(posY, posX, negZ)));
  pn(~(vox000|vox110|vox101), new FiveVoxByEdges(VoxRot(posX, negY, negZ)));
  pn(~(vox100|vox010|vox001), new FiveVoxByEdges(VoxRot(negY, negX, negZ)));
  pn(~(vox000|vox011|vox110), new FiveVoxByEdges(VoxRot(negX, posY, negZ)));

  pn(vox000|vox100|vox010|vox011, new ChiralR(VoxRot(posX, posY, posZ)));
  pn(vox000|vox010|vox110|vox111, new ChiralR(VoxRot(negY, posX, posZ)));
  pn(vox100|vox010|vox110|vox101, new ChiralR(VoxRot(negX, negY, posZ)));
  pn(vox000|vox001|vox100|vox110, new ChiralR(VoxRot(posY, negX, posZ)));

  pn(vox000|vox001|vox011|vox111, new ChiralR(VoxRot(negZ, posY, posX)));
  pn(vox101|vox111|vox011|vox010, new ChiralR(VoxRot(negZ, posX, negY)));
  pn(vox001|vox101|vox111|vox110, new ChiralR(VoxRot(negZ, negY, negX)));
  pn(vox001|vox011|vox100|vox101, new ChiralR(VoxRot(negZ, negX, posY)));

  pn(vox000|vox010|vox001|vox101, new ChiralR(VoxRot(posX, negZ, posY)));
  pn(vox001|vox011|vox010|vox110, new ChiralR(VoxRot(negY, negZ, posX)));
  pn(vox100|vox110|vox111|vox011, new ChiralR(VoxRot(negX, negZ, negY)));
  pn(vox000|vox100|vox101|vox111, new ChiralR(VoxRot(posY, negZ, negX)));

  pn(vox000|vox001|vox010|vox110, new ChiralL(VoxRot(posX, posY, posZ)));
  pn(vox100|vox110|vox010|vox011, new ChiralL(VoxRot(negY, posX, posZ)));
  pn(vox000|vox100|vox110|vox111, new ChiralL(VoxRot(negX, negY, posZ)));
  pn(vox000|vox100|vox101|vox010, new ChiralL(VoxRot(posY, negX, posZ)));

  pn(vox101|vox001|vox011|vox010, new ChiralL(VoxRot(negZ, posY, posX)));
  pn(vox001|vox011|vox111|vox110, new ChiralL(VoxRot(negZ, posX, negY)));
  pn(vox100|vox101|vox111|vox011, new ChiralL(VoxRot(negZ, negY, negX)));
  pn(vox000|vox001|vox101|vox111, new ChiralL(VoxRot(negZ, negX, posY)));

  pn(vox000|vox100|vox001|vox011, new ChiralL(VoxRot(posX, negZ, posY)));
  pn(vox000|vox010|vox011|vox111, new ChiralL(VoxRot(negY, negZ, posX)));
  pn(vox101|vox111|vox110|vox010, new ChiralL(VoxRot(negX, negZ, negY)));
  pn(vox001|vox101|vox100|vox110, new ChiralL(VoxRot(posY, negZ, negX)));

  pn(vox000|vox001|vox010|vox100, new Pyramid(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox101|vox110, new Pyramid(VoxRot(posY, negX, posZ)));
  pn(vox111|vox110|vox010|vox100, new Pyramid(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110|vox011, new Pyramid(VoxRot(negY, posX, posZ)));

  pn(vox111|vox110|vox101|vox011, new Pyramid(VoxRot(negY, negX, negZ)));
  pn(vox001|vox011|vox111|vox010, new Pyramid(VoxRot(posX, negY, negZ)));
  pn(vox000|vox001|vox011|vox101, new Pyramid(VoxRot(posY, posX, negZ)));
  pn(vox001|vox101|vox111|vox100, new Pyramid(VoxRot(negX, posY, negZ)));

  pn(vox100|vox010|vox001|vox111, new CheckerBoard(VoxRot(posX, posY, posZ)));
  pn(vox000|vox110|vox101|vox011, new CheckerBoard(VoxRot(posY, negX, posZ)));

  pn(vox000|vox010|vox100|vox111, new FourThreeOne(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox110|vox011, new FourThreeOne(VoxRot(posY, negX, posZ)));
  pn(vox100|vox010|vox110|vox001, new FourThreeOne(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110|vox101, new FourThreeOne(VoxRot(negY, posX, posZ)));

  pn(vox000|vox001|vox011|vox110, new FourThreeOne(VoxRot(negZ, posY, posX)));
  pn(vox100|vox010|vox011|vox111, new FourThreeOne(VoxRot(negZ, posX, negY)));
  pn(vox000|vox110|vox111|vox101, new FourThreeOne(VoxRot(negZ, negY, negX)));
  pn(vox100|vox101|vox001|vox010, new FourThreeOne(VoxRot(negZ, negX, posY)));

  pn(vox010|vox011|vox101|vox110, new FourThreeOne(VoxRot(posX, posZ, negY)));
  pn(vox100|vox110|vox111|vox001, new FourThreeOne(VoxRot(negY, posZ, negX)));
  pn(vox000|vox100|vox101|vox011, new FourThreeOne(VoxRot(negX, posZ, posY)));
  pn(vox000|vox010|vox001|vox111, new FourThreeOne(VoxRot(posY, posZ, posX)));

  pn(vox000|vox001|vox101|vox110, new FourThreeOne(VoxRot(posX, negZ, posY)));
  pn(vox001|vox011|vox010|vox100, new FourThreeOne(VoxRot(negY, negZ, posX)));
  pn(vox000|vox011|vox111|vox110, new FourThreeOne(VoxRot(negX, negZ, negY)));
  pn(vox010|vox100|vox101|vox111, new FourThreeOne(VoxRot(posY, negZ, negX)));

  pn(vox100|vox110|vox101|vox011, new FourThreeOne(VoxRot(posZ, posY, negX)));
  pn(vox000|vox001|vox100|vox111, new FourThreeOne(VoxRot(posZ, posX, posY)));
  pn(vox000|vox010|vox011|vox101, new FourThreeOne(VoxRot(posZ, negY, posX)));
  pn(vox001|vox111|vox110|vox010, new FourThreeOne(VoxRot(posZ, negX, negY)));

  pn(vox001|vox011|vox111|vox100, new FourThreeOne(VoxRot(posX, negY, negZ)));
  pn(vox000|vox101|vox011|vox111, new FourThreeOne(VoxRot(negY, negX, negZ)));
  pn(vox010|vox001|vox101|vox111, new FourThreeOne(VoxRot(negX, posY, negZ)));
  pn(vox110|vox001|vox101|vox011, new FourThreeOne(VoxRot(posY, posX, negZ)));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// #ifdef DEBUG
// static std::set<VSBNode*> allNodes;
// #endif // DEBUG

VSBNode::VSBNode(const Coord3D &p)
    : trimmed(false), neighbors(3, nullptr), position(p)
{
// #ifdef DEBUG
//   allNodes.insert(this);
// #endif // DEBUG
}

VSBNode::VSBNode(const ICoord3D &p)
  : trimmed(false), neighbors(3, nullptr), position(p.coord())
{
// #ifdef DEBUG
//   allNodes.insert(this);
// #endif // DEBUG
}

VSBNode::~VSBNode() {
// #ifdef DEBUG
//   allNodes.erase(this);
// #endif // DEBUG
}

void VSBNode::setNeighbor(unsigned int i, VSBNode *nbr) {
  assert(neighbors[i] == nullptr);
  neighbors[i] = nbr;
// #ifdef DEBUG
//   if(allNodes.count(nbr) != 1) {
//     oofcerr << "VSBNode::setNeighbor: bad neighbor! nbr=" << nbr << std::endl;
//     oofcerr << "VSBNode::setNeighbor: this->index=" << index
// 	    << " position=" << position << std::endl;
//     throw ErrProgrammingError("Neighbor is not a node!", __FILE__, __LINE__);
//   }
// #endif // DEBUG
}

void VSBNode::replaceNeighbor(VSBNode *oldnode, VSBNode *newnode) {
// #ifdef DEBUG
//   if(allNodes.count(newnode) != 1) {
//     oofcerr << "VSBNode::replaceNeighbor: bad neighbor! newnode="
// 	    << newnode << std::endl;
//     oofcerr << "VSBNode::replaceNeighbor: this->index=" << index
// 	    << " position=" << position << std::endl;
//     throw ErrProgrammingError("Neighbor is not a node!", __FILE__, __LINE__);
//   }
// #endif // DEBUG
  for(unsigned int i=0; i<3; i++) {
    if(neighbors[i] == oldnode) {
      neighbors[i] = newnode;
      return;
    }
  }
  throw ErrProgrammingError("VSBNode::replaceNeighbor failed!",
			    __FILE__, __LINE__);
}

unsigned int VSBNode::neighborIndex(const VSBNode *nbr) const {
  for(unsigned int i=0; i<3; i++)
    if(neighbors[i] == nbr)
      return i;
  throw ErrProgrammingError("VSBNode::neighborIndex failed!",
			    __FILE__, __LINE__);
}

// nextCWNeighbor returns the neighbor of this node that follows the
// given node CW in the neighbor list.  This is where the CW storage
// ordering of the neighbors is important.

const VSBNode *VSBNode::nextCWNeighbor(const VSBNode *nbr) const {
  if(neighbors[0] == nbr)
    return neighbors[1];
  if(neighbors[1] == nbr)
    return neighbors[2];
  assert(neighbors[2] == nbr);
  return neighbors[0];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VSBGraph::~VSBGraph() {
  for(VSBNode *node : vertices)
    delete node;
  vertices.clear();
}

void VSBGraph::addNode(VSBNode *node) {
  node->index = vertices.size();
  vertices.push_back(node);
// #ifdef DEBUG
//   oofcerr << "VSBGraph::addNode: " << node->index << " " << node->position
// 	  << std::endl;
// #endif // DEBUG
}

// bool VSBGraph::verify() const {
//   bool ok = true;
//   for(const VSBNode *vertex : vertices) {
//     ok = ok && vertex->checkNeighborCount();
//   }
//   return ok;
// }

Coord3D VSBGraph::center() const {
  Coord ctr;
  for(VSBNode *vertex : vertices)
    ctr += vertex->position;
  return ctr/vertices.size();
}

double VSBGraph::volume() const {
  // Based on r3d_reduce.  Compute the volume of the polyhedron by
  // splitting each face into triangles, and computing the volume of
  // the each tet formed by a triangle and the center of the
  // polyhedron.

// #ifdef DEBUG
//   oofcerr << "VSBGraph::volume: size=" << size() << std::endl;
// #endif // DEBUG
  
  // emarks indicates which edges have been used.
  Coord3D cntr = center();
  double vol = 0.0;
  std::vector<std::vector<bool>> emarks(vertices.size(), {false, false, false});
  // Find an unused edge.
  for(unsigned int vstart=0; vstart<vertices.size(); vstart++) {
    for(unsigned int pstart=0; pstart<3; pstart++) {
      if(!emarks[vstart][pstart]) {
	// Found an unused edge.  Follow the sequence of neighbors
	// around a facet, using the starting point and a segment of
	// the perimeter to define a triangular portion of the facet.
	const VSBNode *startNode = vertices[vstart];
	Coord3D startPt = startNode->position;
// #ifdef DEBUG
// 	oofcerr << "VSBGraph::volume: new face, startPt=" << startPt
// 		<< std::endl;
// #endif // DEBUG
	// cur and prev are the endpoints of a segment of the
	// perimeter.  Their initial values *don't* contribute to the
	// area, because prev==startPt.
	const VSBNode *prev = startNode;
	const VSBNode *cur = startNode->getNeighbor(pstart);
	emarks[vstart][pstart] = true;
	bool done = false;
	do {
	  // Go to next pair
	  const VSBNode *next = cur->nextCWNeighbor(prev);
	  prev = cur;
	  cur = next;
	  emarks[prev->index][prev->neighborIndex(cur)] = true;
	  if(cur == startNode) {
	    done = true;
	  }
	  else {
	    double dv = dot(
		    cross(prev->position-startPt, cur->position-startPt),
		    startPt-cntr);
	    vol += dv;
// #ifdef DEBUG
// 	    OOFcerrIndent indent(2);
// 	    oofcerr << "VSBGraph::volume: adding tet "
// 		    << prev->position << " " << cur->position << " "
// 		    << startPt << " " << cntr << " dv=" << dv/6. << std::endl;
// #endif // DEBUG
	  }
	} while(!done);
	
      }
    } // end loop over pstart
  } // end loop over vstart

  return vol/6.;
}

bool VSBGraph::checkEdges() const {
  bool result = true;
  for(const VSBNode *vertex : vertices) {
    for(unsigned int n=0; n<3; n++) {
      VSBNode *nbr = vertex->getNeighbor(n);
      if(nbr == nullptr) {
	oofcerr << "VSBGraph::checkEdges: missing neighbor " << n
		<< " for vertex " << vertex->index << " " << vertex->position
		<< std::endl;
	result = false;
      }
      else {
	bool ok = false;
	for(unsigned int i=0; i<3; i++) {
	  if(nbr->getNeighbor(i) == vertex) {
	    ok = true;
	    break;
	  }
	}
	if(!ok) {
	  result = false;
	  oofcerr << "VSBGraph::checkEdges: node "
		  << nbr->index << " " << nbr->position
		  << " is a neighbor of node " << vertex->index
		  << " " << vertex->position << " but not vice versa."
		  << std::endl;
	}
      }
    }
  }
  oofcerr << "VSBGraph::checkEdges: ok!" << std::endl;
  return result;
}

// Write out the graph structure
void VSBGraph::dump(std::ostream &os) const {
  for(const VSBNode *vertex: vertices)
    os << "Vertex " << vertex << " " << vertex->index << std::endl;
  for(const VSBNode *vertex : vertices) {
    os << "Vertex " << vertex->index << " " << vertex->position << std::endl;
    os << "  ";
    for(VSBNode *nbr : vertex->neighbors) {
      os << nbr << " ";
      // if(nbr)
      // 	os << "(" << nbr << ", " << nbr->index << ")  ";
      // else
      // 	os << "(0x0)  ";
    }
    os << std::endl;
  }
}

// Write out the edges in a plottable form
void VSBGraph::dumpLines(std::ostream &os) const {
  for(const VSBNode *vertex : vertices) {
    for(VSBNode *nbr : vertex->neighbors) {
      if(nbr && vertex->index < nbr->index)
	os << vertex->position << ", " << nbr->position << " # "
	   << vertex->index << " " << nbr->index << std::endl;
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VSBEdgeIterator::VSBEdgeIterator(const VSBGraph *gr)
  : graph(gr),
    ihere(0),
    inbr(0),
    finished(false)
{}

const VSBNode *VSBEdgeIterator::node0() const {
  return graph->getNode(ihere);
}

const VSBNode *VSBEdgeIterator::node1() const {
  return graph->getNode(ihere)->getNeighbor(inbr);
}

void VSBEdgeIterator::next() {
  if(inbr < 2) {
    inbr++;
    return;
  }
  // nbr == 2
  inbr = 0;
  ihere++;
  if(ihere == graph->size()) {
    finished = true;
    return;
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelSetBoundary::~VoxelSetBoundary() {
  delete bounds;
}

// protoVSBNodeFactory converts a signature (2x2x2 set of bools stored
// as a char) to a type of ProtoVSBNode and a VoxRot.  To do
// that, it clones the ProtoVSBNode that's in the protoNodeTable for
// that signature.

ProtoVSBNode *VoxelSetBoundary::protoVSBNodeFactory(unsigned char signature,
						    const ICoord3D &here)
{
// #ifdef DEBUG
//   oofcerr << "VoxelSetBoundary::protoVSBNodeFactory: signature="
// 	  << int(signature) << " " << printSig(signature) << std::endl;
//   oofcerr << "VoxelSetBoundary::protoVSBNodeFactory: protoNode="
// 	  << protoNodeTable[signature] << std::endl;
// #endif // DEBUG
  const ProtoVSBNode *prototype = protoNodeTable[signature];
  if(prototype == nullptr)
    return nullptr;
  ProtoVSBNode *protoNode = prototype->clone();
#ifdef DEBUG
  protoNode->setSignature(signature);
#endif // DEBUG
// #ifdef DEBUG
//   oofcerr << "VoxelSetBoundary::protoVSBNodeFactory: signature="
// 	  << printSig(signature) << " here=" << here
// 	  << " protoNode=" << *protoNode << std::endl;
// #endif // DEBUG
  protoNode->makeVSBNodes(this, here);
// #ifdef DEBUG
//   oofcerr << "VoxelSetBoundary::protoVSBNodeFactory: done" << std::endl;
// #endif // DEBUG
  return protoNode;
}

void VoxelSetBoundary::twoFoldNode(VSBNode *node) {
  twoFoldNodes.insert(node);
}

void VoxelSetBoundary::fixTwoFoldNodes() {
  for(VSBNode *node : twoFoldNodes) {
    VSBNode *n0 = node->neighbors[0];
    VSBNode *n1 = node->neighbors[1];
    n0->replaceNeighbor(node, n1);
    n1->replaceNeighbor(node, n0);
    delete node;
  }
  twoFoldNodes.clear();
}

double VoxelSetBoundary::volume() const {
  return graph.volume() * microstructure->volumeOfVoxels();    
}

bool VoxelSetBoundary::checkEdges() const {
  return graph.checkEdges();
}
