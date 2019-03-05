// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// This file is included by VSB/vsb.h and should not be loaded
// elsewhere.  The code here has been separated out just because the
// file was too large, and not because this code is independent of
// that.

// See comments in VSB/vsb.h.  This file contains the ProtoVSBNode
// subclasses discussed there.

#ifndef VSB_PROTONODES_H
#define VSB_PROTONODES_H

// Intermediate ProtoVSBNode classes.  SingleNode is a ProtoVSBNode
// that isn't split into multiple VSBNodes.  DoubleNode is split into
// two VSBNodes.  TripleNode is split into three.  MultiNode is split
// into more than three.

template <class COORD, class ICOORD>
class SingleNode : public ProtoVSBNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
protected:
  Node *vsbNode;
public:
  SingleNode(const VoxRot &rot)
    : ProtoVSBNode<COORD, ICOORD>(rot),
      vsbNode(nullptr)
  {}
  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    vsbNode = new Node(here);
    graph->addNode(vsbNode);
  }
  virtual const COORD &position() const {
    assert(vsbNode != nullptr);
    return vsbNode->position;
  }
};

template <class COORD, class ICOORD>
class DoubleNode : public ProtoVSBNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
protected:
  Node *vsbNode0, *vsbNode1;
public:
  DoubleNode(const VoxRot &rot)
    : ProtoVSBNode<COORD, ICOORD>(rot),
      vsbNode0(nullptr), vsbNode1(nullptr)
  {}
  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    vsbNode0 = new Node(here);
    vsbNode1 = new Node(here);
    graph->addNode(vsbNode0);
    graph->addNode(vsbNode1);
  }
  virtual const COORD &position() const {
    assert(vsbNode0 != nullptr);
    return vsbNode0->position;
  }
};

template <class COORD, class ICOORD>
class TripleNode : public ProtoVSBNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
protected:
  Node *vsbNode0, *vsbNode1, *vsbNode2;
public:
  TripleNode(const VoxRot &rot)
    : ProtoVSBNode<COORD, ICOORD>(rot),
      vsbNode0(nullptr), vsbNode1(nullptr), vsbNode2(nullptr)
  {}
  virtual void makeVSBNodes(VSBGraph<COORD, ICOORD> *graph,
			    const ICOORD &here)
  {
    vsbNode0 = new Node(here);
    vsbNode1 = new Node(here);
    vsbNode2 = new Node(here);
    graph->addNode(vsbNode0);
    graph->addNode(vsbNode1);
    graph->addNode(vsbNode2);
  }
  virtual const COORD &position() const {
    assert(vsbNode0 != nullptr);
    return vsbNode0->position;
  }
};

template <class COORD, class ICOORD>
class MultiNode : public ProtoVSBNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  // For more than three, give up on writing them out explicitly;
protected:
  std::vector<Node*> vsbNodes;
public:
  MultiNode(unsigned int n, const VoxRot &rot)
    : ProtoVSBNode<COORD, ICOORD>(rot),
      vsbNodes(n, nullptr)
  {}
  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    for(unsigned int i=0; i<vsbNodes.size(); i++) {
      vsbNodes[i] = new Node(here);
      graph->addNode(vsbNodes[i]);
    }
  }
  virtual const COORD &position() const {
    assert(vsbNodes[0] != nullptr);
    return vsbNodes[0]->position;
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Concrete subclasses of ProtoVSBNode


// For a node at the corner of a single voxel, the reference
// configuration in the 2x2x2 cube has the voxel in the +x, +y, +z
// corner (vox111) and the neighbors in the +x, +y, +z directions.

template <class COORD, class ICOORD>
class SingleVoxel : public SingleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  SingleVoxel(const VoxRot &rot)
    : SingleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new SingleVoxel<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNode);
    // The neighbors are in the +x, +y, and +z directions, so
    // inserting them in the neighbor list in that order puts them
    // CW when viewed from outside (from the -x, -y, -z side).
    this->vsbNode->setNeighbor(dir.axis, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    this->vsbNode->setNeighbor(dir.axis, othernode);
    return this->vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SingleVoxel(" << printSig(this->signature) << ", " << this->rotation
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

template <class COORD, class ICOORD>
class SevenVoxels : public SingleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  SevenVoxels(const VoxRot &rot)
    : SingleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new SevenVoxels<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNode);
    // The neighbors are in the +x, +y, and +z directions, but
    // inserting them in the neighbor list in otherproto order would puts
    // them CCW when viewed from outside (from the +x, +y, +z side).
    // They're supposed to be CW, so switch 0 and 2.
    this->vsbNode->setNeighbor(2-dir.axis, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    this->vsbNode->setNeighbor(2-dir.axis, othernode);
    return this->vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SevenVoxels(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};

//--------

// Two voxels that share an edge.

template <class COORD, class ICOORD>
class TwoVoxelsByEdge : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  TwoVoxelsByEdge(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new TwoVoxelsByEdge<COORD, ICOORD>(this->rotation);
  }

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

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // The edges of vox000 connect to vsbNode0 and the edges of
    // vox110 to vsbNode1.  vox000's edges are negY, negX, negZ, in
    // that order (CW as viewed from outside (from +x+y+z).
    // Similarly, vox110's edges are posY, posX, negZ.
    if(dir == negX || dir == negY) {
      // Connect to vox000's edges, using vsbNode0.
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      // Since dir.axis is 0 or 1, 1-dir.axis gives us the order we want.
      this->vsbNode0->setNeighbor(1-dir.axis, othernode); 
    }
    else if(dir == posX || dir == posY) {
      // Connect to vox110's edges, using vsbNode1.
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(1-dir.axis, othernode);
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
      bool ordered = this->voxelOrder(vox000, vox110);
      Node *othernode0, *othernode1;
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX || dir == negY) {
      this->vsbNode0->setNeighbor(1-dir.axis, othernode);
      return this->vsbNode0;
    }
    assert(dir == posX || dir == posY);
    this->vsbNode1->setNeighbor(1-dir.axis, othernode);
    return this->vsbNode1;
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = this->voxelOrder(vox000, vox110);
    node0 = ordered ? this->vsbNode0 : this->vsbNode1;
    node1 = ordered ? this->vsbNode1 : this->vsbNode0;
    node0->setNeighbor(2, othernode0);
    node1->setNeighbor(2, othernode1);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "TwoVoxelsByEdge(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};  // end class TwoVoxelsByEdge

//-------------

// Two voxels that touch at a corner.

template <class COORD, class ICOORD>
class TwoVoxelsByCorner : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  TwoVoxelsByCorner(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new TwoVoxelsByCorner<COORD, ICOORD>(this->rotation);}

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }
  
  virtual void connect(ProtoNode *otherproto) {
    // TwoVoxelsByCorner is easier than TwoVoxelsByEdge, because there
    // aren't two connections going out in the same direction.  We can
    // simply say that the edges on vox000 connect to vsbNode0, and
    // the edges on vox111 connect to vsbNode1.  There's no
    // consistency to maintain at the other end of a doubled edge.
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir.dir == -1) {		// negX, negY, or negZ
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      // The edges around vox000 in CW order when viewed from +x+y+z
      // are negZ, negY, negX. 
      this->vsbNode0->setNeighbor(2-dir.axis, othernode);
    }
    else {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      // The edges around vox111 in CW order when viewed from -x-y-z
      // are posX, posY, pozY.
      this->vsbNode1->setNeighbor(dir.axis, othernode);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir.dir == -1) {
      this->vsbNode0->setNeighbor(2-dir.axis, othernode);
      return this->vsbNode0;
    }
    this->vsbNode1->setNeighbor(dir.axis, othernode);
    return this->vsbNode1;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "TwoVoxelsByCorner(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};	// end class TwoVoxelsByCorner

//--------

// SixVoxelsByEdge is the inverse of TwoVoxelsByEdge

template <class COORD, class ICOORD>
class SixVoxelsByEdge : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  SixVoxelsByEdge(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new SixVoxelsByEdge<COORD, ICOORD>(this->rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    // The reference configuration all voxels *except* vox000 and
    // vox110.  There are edges in the posX, negX, posY, negY, and
    // negZ directions.
    static const VoxelEdgeList v({posX, negX, posY, negY, negZ});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // The edges on vox100 connect to vsbNode0 and the edges on vox010
    // connect to vsbNode1.  Edges on vox100 are posX, negY, negZ.
    // Edges on vox010 are negX, posY, negZ.
    if(dir == posX || dir == negY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(dir.axis, othernode); 
    }
    else if(dir == negX || dir == posY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(dir.axis, othernode);
    }
    else {
      assert(dir == negZ);
      bool ordered = this->voxelOrder(vox100, vox010);
      Node *othernode0, *othernode1;
      Node *node0 = ordered? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered? this->vsbNode1 : this->vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == posX || dir == negY) {
      this->vsbNode0->setNeighbor(dir.axis, othernode);
      return this->vsbNode0;
    }
    assert(dir == negX || dir == posY);
    this->vsbNode1->setNeighbor(dir.axis, othernode);
    return this->vsbNode1;
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = this->voxelOrder(vox100, vox010);
    node0 = ordered ? this->vsbNode0 : this->vsbNode1;
    node1 = ordered ? this->vsbNode1 : this->vsbNode0;
    node0->setNeighbor(2, othernode0);
    node1->setNeighbor(2, othernode1);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SixVoxelsByEdge(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};  // end class SixVoxelsByEdge

//--------

// SixVoxelsByCorner is the inverse of TwoVoxelsByCorner

template <class COORD, class ICOORD>
class SixVoxelsByCorner : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  SixVoxelsByCorner(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}
  virtual ProtoNode *clone() const {
    return new SixVoxelsByCorner<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoNode *otherproto) {
    // SixVoxelsByCorner is easier than SixVoxelsByEdge, because there
    // aren't two connections going out in the same direction.  We can
    // simply say that the edges on vox000 (which is a hole) connect
    // to vsbNode0, and the edges on vox111 (also a hole) connect to
    // vsbNode1.  There's no consistency to maintain at the other end
    // of a doubled edge.
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir.dir == -1) {		// negX, negY, or negZ
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      // The edges around vox000 in CW order when viewed from -x-y-z
      // are negX, negY, negZ. 
      this->vsbNode0->setNeighbor(dir.axis, othernode);
    }
    else {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      // The edges around vox111 in CW order when viewed from +x+y+z
      // are posZ, posY, pozX.
      this->vsbNode1->setNeighbor(2-dir.axis, othernode);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir.dir == -1) {
      this->vsbNode0->setNeighbor(dir.axis, othernode);
      return this->vsbNode0;
    }
    this->vsbNode1->setNeighbor(2-dir.axis, othernode);
    return this->vsbNode1;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SixVoxelsByCorner(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end SixVoxelsByCorner

//----------

// Three voxels in an L configuration.  The node does not need to be
// split.  The reference configuration is vox000, vox100,
// vox010, with edges posX, posY, negZ in that order.

template <class COORD, class ICOORD>
class ThreeVoxL : public SingleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ThreeVoxL(const VoxRot &rot)
    : SingleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new ThreeVoxL<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negZ, posX, posY});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNode);
    this->vsbNode->setNeighbor(dir.axis, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    this->vsbNode->setNeighbor(dir.axis, othernode);
    return this->vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeVoxL(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end ThreeVoxL

// ----------

// FiveVoxL is the inverse of ThreeVoxL.  The connections are
// the same, but the order is reversed.

template <class COORD, class ICOORD>
class FiveVoxL : public SingleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  FiveVoxL(const VoxRot &rot)
    : SingleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new FiveVoxL<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negZ, posX, posY});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNode);
    this->vsbNode->setNeighbor(2-dir.axis, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    this->vsbNode->setNeighbor(2-dir.axis, othernode);
    return this->vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveVoxL(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end FiveVoxL

//---------

// ThreeTwoOne is three voxels, two stacked face to face and a third
// connected to one of the other two along an edge.  There are 24
// orientations.  The reference configuration contains voxels 000,
// 111, and 110.

template <class COORD, class ICOORD>
class ThreeTwoOne : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ThreeTwoOne(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}
  
  virtual ProtoNode *clone() const {
    return new ThreeTwoOne<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negY, negX, negZ, posZ});
    return v;
  }

  void makeVSBNodes(Graph *graph, const ICOORD &here) {
    this->vsbNode0 = new Node(here);
    this->vsbNode1 = new Node(here);
    graph->addNode(this->vsbNode0);
    graph->twoFoldNode(this->vsbNode1);
    // Don't add vsbNode1 to the graph! It's not a real node.
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // See comments in TwoVoxelsByEdge.  This is similar, but the
    // edges on vox110 are different, and its VSBNode will only be
    // connected to two edges, so we have to tell the VSB about it.
    // VSBNode0 is the 3-fold node, with edges on vox000 in the negX,
    // negY, and negZ directions.  VSBNode1 is the 2-fold node, on
    // vox110 and vox111, with edges negZ and posZ.
    
    if(dir == negX || dir == negY) {
      // Connecting to the edges on vox000
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(1-dir.axis, othernode);
    }
    else if(dir==posZ) {
      // Connecting to the edges on vox110
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(0, othernode);
    }
    else {
      // The double edge coming in on negZ.  To ensure compatibility
      // with the other ends of edge, use voxelOrder to determine the
      // order of the input and output args to connectDoubleBack.
      assert(dir == negZ);
      bool ordered = this->voxelOrder(vox000, vox110);
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNode0->setNeighbor(2, othernode0);
      this->vsbNode1->setNeighbor(1, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX || dir == negY) {
      this->vsbNode0->setNeighbor(1-dir.axis, othernode);
      return this->vsbNode0;
    }
    assert(dir == posZ);
    this->vsbNode1->setNeighbor(0, othernode);
    return this->vsbNode1;
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = this->voxelOrder(vox000, vox110);
    if(ordered) {
      node0 = this->vsbNode0;
      node1 = this->vsbNode1;
      this->vsbNode0->setNeighbor(2, othernode0);
      this->vsbNode1->setNeighbor(1, othernode1);
    }
    else {
      node0 = this->vsbNode1;
      node1 = this->vsbNode0;
      this->vsbNode0->setNeighbor(2, othernode1);
      this->vsbNode1->setNeighbor(1, othernode0);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeTwoOne(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end class ThreeTwoOne

//---------

// FiveTwoOne is the inverse of ThreeTwoOne.  The reference
// configuration contains all voxels except vox000, vox111, and
// vox110.  That means that vox100 and vox010 touch along an edge.
// The case is treated completely differently from ThreeTwoOne,
// because it's not possible to resolve the doubled edge in a unique
// way.  So here we add an extra (third) node and avoid a doubled
// edge.  It's not possible to resolve ThreeTwoOne in this way because
// it would lead to an insufficiently connected graph.

template <class COORD, class ICOORD>
class FiveTwoOne : public TripleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  FiveTwoOne(const VoxRot &rot)
    : TripleNode<COORD, ICOORD>(rot)
  {
  }
  
  virtual ProtoNode *clone() const {
    return new FiveTwoOne<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negY, negX, negZ, posZ});
    return v;
  }

  void makeVSBNodes(Graph *graph, const ICOORD &here) {
    TripleNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    this->vsbNode0->setNeighbor(2, this->vsbNode2);
    this->vsbNode1->setNeighbor(1, this->vsbNode2);
    this->vsbNode2->setNeighbor(2, this->vsbNode0);
    this->vsbNode2->setNeighbor(1, this->vsbNode1);
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // vsbNode0 connects the negY, negZ edges of vox100 and vsbNode1
    // connects the negX, negZ edges of vox010.  Both also connect to
    // vsbNode2, which connects the posZ edge as well.
    
    if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir==posZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode2);
      this->vsbNode2->setNeighbor(0, othernode);
    }
    else {
      // The double edge coming in on negZ.
      assert(dir == negZ);
      bool ordered = this->voxelOrder(vox100, vox010);
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNode0->setNeighbor(1, othernode0);
      this->vsbNode1->setNeighbor(2, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX) {
      this->vsbNode1->setNeighbor(0, othernode);
      return this->vsbNode1;
    }
    if(dir == negY) {
      this->vsbNode0->setNeighbor(0, othernode);
      return this->vsbNode0;
    }
    assert(dir == posZ);
    this->vsbNode2->setNeighbor(0, othernode);
    return this->vsbNode2;
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = this->voxelOrder(vox100, vox010);
    if(ordered) {
      node0 = this->vsbNode0;
      node1 = this->vsbNode1;
      this->vsbNode0->setNeighbor(1, othernode0);
      this->vsbNode1->setNeighbor(2, othernode1);
    }
    else {
      node0 = this->vsbNode1;
      node1 = this->vsbNode0;
      this->vsbNode0->setNeighbor(1, othernode1);
      this->vsbNode1->setNeighbor(2, othernode0);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveTwoOne(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};				// end class FiveTwoOne

//--------

// Three voxels that each share an edge with both of the others.  

template <class COORD, class ICOORD>
class ThreeVoxByEdges : public TripleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ThreeVoxByEdges(const VoxRot &rot)
    : TripleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new ThreeVoxByEdges<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // The reference configuration is vox110 + vox011 + vox101.
    // There are doubled edges in the +x, +y, and +z directions and
    // single edges in the -x, -y, and -z directions.  We use vsbNode0
    // for the edges of vox110, vsbNode1 for 101, and vsbNode2 for
    // 011.
    if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode2);
      this->vsbNode2->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      // Two edges between vox110 (vsbNode0) and vox101 (vsbNode1)
      bool ordered = this->voxelOrder(vox110, vox101);
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // The edges on vsbNode0 (vox110) are (negZ, posY, posX),
      // CW.  This is posX, so it goes in slot 2.
      this->vsbNode0->setNeighbor(2, othernode0);
      // The edges on vsbNode1 (vox101) are (negY, posX, posZ),
      // CW.  This is posX, so it goes in slot 1.
      this->vsbNode1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      // Two edges between vox110 (vsbNode0) and vox011 (vsbNode2)
      bool ordered = this->voxelOrder(vox110, vox011);
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode2;
      Node *node1 = ordered ? this->vsbNode2 : this->vsbNode0;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negZ, posY, posX).
      this->vsbNode0->setNeighbor(1, othernode0);
      // Edges are (negX, posZ, posY)
      this->vsbNode2->setNeighbor(2, othernode1);
    }
    else if(dir == posZ) {
      // Two edges between vox101 (vsbNode1) and vox011 (vsbNode2)
      bool ordered = this->voxelOrder(vox101, vox011);
      Node *node0 = ordered ? this->vsbNode1 : this->vsbNode2;
      Node *node1 = ordered ? this->vsbNode2 : this->vsbNode1;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negY, posX, posZ)
      this->vsbNode1->setNeighbor(2, othernode0);
      // Edges are (negX, posZ, posY)
      this->vsbNode2->setNeighbor(1, othernode1);
    }
  } // end connect()

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX) {
      this->vsbNode2->setNeighbor(0, othernode);
      return this->vsbNode2;
    }
    if(dir == negY) {
      this->vsbNode1->setNeighbor(0, othernode);
      return this->vsbNode1;
    }
    assert(dir == negZ);
    this->vsbNode0->setNeighbor(0, othernode);
    return this->vsbNode0;
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = this->voxelOrder(vox110, vox101);
      node0 = this->vsbNode0;
      node1 = this->vsbNode1;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNode0->setNeighbor(2, othernode0);
      this->vsbNode1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      bool ordered = this->voxelOrder(vox110, vox011);
      node0 = this->vsbNode0;
      node1 = this->vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNode0->setNeighbor(1, othernode0);
      this->vsbNode2->setNeighbor(2, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = this->voxelOrder(vox101, vox011);
      node0 = this->vsbNode1;
      node1 = this->vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNode1->setNeighbor(2, othernode0);
      this->vsbNode2->setNeighbor(1, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeVoxByEdges(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};				// end class ThreeVoxByEdges

//-----------

// FiveVoxByEdges is the inverse of ThreeVoxByEdges, but has to be
// treated more like Pyramid with an extra voxel.  The reference
// configuration is all voxels except vox110, vox011, and vox101.

template <class COORD, class ICOORD>
class FiveVoxByEdges : public MultiNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  FiveVoxByEdges(const VoxRot &rot)
    : MultiNode<COORD, ICOORD>(7, rot)
  {}

  virtual ProtoNode *clone() const {
    return new FiveVoxByEdges<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    MultiNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    for(unsigned int i=0; i<6; i++) {
      // Same as Pyramid::makeVSBNodes()
      this->vsbNodes[i]->setNeighbor(2, this->vsbNodes[(i+5)%6]);
      this->vsbNodes[i]->setNeighbor(1, this->vsbNodes[(i+1)%6]);
    }
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // The reference configuration is ~(vox110|vox011|vox101).  There
    // are doubled edges in the +x, +y, and +z directions and single
    // edges in the -x, -y, and -z directions.  Nodes vsbNodes[0]
    // through vsbNodes[5] form an infinitesimal hexagon at the
    // junction of voxels 100, 001, and 010.  vsbNodes[6] links the
    // edges of vox111, which are coincident the the +x, +y, and +z
    // edges of the other voxels.
    if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNodes[3]);
      this->vsbNodes[3]->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNodes[1]);
      this->vsbNodes[1]->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNodes[5]);
      this->vsbNodes[5]->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      // Two edges between vox100 and vox111
      bool ordered = this->voxelOrder(vox100, vox111);
      Node *node0 = ordered ? this->vsbNodes[0] : this->vsbNodes[6];
      Node *node1 = ordered ? this->vsbNodes[6] : this->vsbNodes[0];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[0]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      // Two edges between vox010 and vox111
      bool ordered = this->voxelOrder(vox010, vox111);
      Node *node0 = ordered ? this->vsbNodes[4] : this->vsbNodes[6];
      Node *node1 = ordered ? this->vsbNodes[6] : this->vsbNodes[4];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[4]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      // Two edges between vox001 and vox111
      bool ordered = this->voxelOrder(vox001, vox111);
      Node *node0 = ordered ? this->vsbNodes[2] : this->vsbNodes[6];
      Node *node1 = ordered ? this->vsbNodes[6] : this->vsbNodes[2];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[2]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(2, othernode1);
    }
  } // end connect()

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX) {
      this->vsbNodes[3]->setNeighbor(0, othernode);
      return this->vsbNodes[3];
    }
    if(dir == negY) {
      this->vsbNodes[1]->setNeighbor(0, othernode);
      return this->vsbNodes[1];
    }
    assert(dir == negZ);
    this->vsbNodes[5]->setNeighbor(0, othernode);
    return this->vsbNodes[5];
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = this->voxelOrder(vox100, vox111);
      node0 = this->vsbNodes[0];
      node1 = this->vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[0]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      bool ordered = this->voxelOrder(vox010, vox111);
      node0 = this->vsbNodes[4];
      node1 = this->vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[4]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = this->voxelOrder(vox001, vox111);
      node0 = this->vsbNodes[2];
      node1 = this->vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[2]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(2, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveVoxByEdges(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};				// end FiveVoxByEdges

//--------------

// Four voxels in the shape of two perpendicular stacks of two voxels.
// This configuration is chiral and requires an additional node to be
// created, although there are no multiply connected edges.

template <class COORD, class ICOORD>
class ChiralR : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ChiralR(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new ChiralR<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, negX, posZ, negZ});
    return v;
  }

  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    DoubleNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    this->vsbNode0->setNeighbor(0, this->vsbNode1);
    this->vsbNode1->setNeighbor(0, this->vsbNode0);
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // Connect posX and negZ to vsbNode0, and negX and posZ to vsbNode1.
    // The two VSBNodes are already connected by a dummy edge, in makeVSBNodes.
    // vsbNode0's CW edges are [dummy], negZ, posX.
    // vsbNode1's CW edges are [dummy], negX, posZ.
    // The order of the edges is the reverse of the order in ChiralL.
    if(dir == posX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(2, othernode);
    }
    else if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(1, othernode);
    }
    else if(dir == posZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(2, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(1, othernode);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == posX) {
      this->vsbNode0->setNeighbor(2, othernode);
      return this->vsbNode0;
    }
    if(dir == negX) {
      this->vsbNode1->setNeighbor(1, othernode);
      return this->vsbNode1;
    }
    if(dir == posZ) {
      this->vsbNode1->setNeighbor(2, othernode);
      return this->vsbNode1;
    }
    assert(dir == negZ);
    this->vsbNode0->setNeighbor(1, othernode);
    return this->vsbNode0;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ChiralR(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end ChiralR

//--------------

// The mirror image of ChiralR is ChiralL

template <class COORD, class ICOORD>
class ChiralL : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ChiralL(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new ChiralL<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, negX, posZ, negZ});
    return v;
  }

  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    DoubleNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    this->vsbNode0->setNeighbor(0, this->vsbNode1);
    this->vsbNode1->setNeighbor(0, this->vsbNode0);
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // Connect posX and negZ to vsbNode0, and negX and posZ to vsbNode1.
    // The two VSBNodes are already connected by a dummy edge, in makeVSBNodes.
    // vsbNode0's CW edges are [dummy], posX, negZ.
    // vsbNode1's CW edges are [dummy], posZ, negX.
    // The order of the edges is the reverse of the order in ChiralR.
    if(dir == posX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(1, othernode);
    }
    else if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(2, othernode);
    }
    else if(dir == posZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(1, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(2, othernode);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == posX) {
      this->vsbNode0->setNeighbor(1, othernode);
      return this->vsbNode0;
    }
    if(dir == negX) {
      this->vsbNode1->setNeighbor(2, othernode);
      return this->vsbNode1;
    }
    if(dir == posZ) {
      this->vsbNode1->setNeighbor(1, othernode);
      return this->vsbNode1;
    }
    assert(dir == negZ);
    this->vsbNode0->setNeighbor(2, othernode);
    return this->vsbNode0;
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ChiralL(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end ChiralL

//------------

// The Pyramid is 4 voxels stacked in a sort of skewed pyramid.  It
// contains one central voxel and the voxels on each of its faces.  An
// infinitesimal hexagonal face is inserted in the corner to convert
// the 6-fold vertex into 6 3-fold vertices.

template <class COORD, class ICOORD>
class Pyramid : public MultiNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  Pyramid(const VoxRot &rot)
    : MultiNode<COORD, ICOORD>(6, rot)
  {}

  virtual ProtoNode *clone() const {
    return new Pyramid<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    MultiNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    for(unsigned int i=0; i<6; i++) {
      // Neighbor 1 is the previous node in the hexagonal face.
      this->vsbNodes[i]->setNeighbor(1, this->vsbNodes[(i+5)%6]);
      // Neighbor 2 is the next node in the hexagonal face.
      this->vsbNodes[i]->setNeighbor(2, this->vsbNodes[(i+1)%6]);
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

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    unsigned int i = hexDirIndex(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNodes[i]);
    this->vsbNodes[i]->setNeighbor(0, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    unsigned int i = hexDirIndex(dir);
    this->vsbNodes[i]->setNeighbor(0, othernode);
    return this->vsbNodes[i];
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "Pyramid(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end Pyramid

//----------

// Four voxels arranged in a checkerboard pattern, each sharing an
// edge with all of the others.  Each edge becomes a split edge, and
// there's one VSBNode for the inside corner of each voxel.

template <class COORD, class ICOORD>
class CheckerBoard : public MultiNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  CheckerBoard(const VoxRot &rot)
    : MultiNode<COORD, ICOORD>(4, rot)
  {}

  ProtoNode *clone() const {
    return new CheckerBoard<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoNode *otherproto) {
    // The reference configuration is vox100 + vox010 + vox001 +
    // vox111.  Use VSBnodes[0] for vox100, 1 for vox010, 2 for
    // vox001, and 3 for vox111.  The assignment of neighbor indices
    // for the VSBNodes is arbitrary but consistent (and gets them all
    // CW, hopefully!)
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posX) {
      // The posX edge is between voxels 100 and 111, so it connects
      // to vsbNodes 0 and 3.
      bool ordered = this->voxelOrder(vox100, vox111);
      Node *node0 = ordered ? this->vsbNodes[0] : this->vsbNodes[3];
      Node *node1 = ordered ? this->vsbNodes[3] : this->vsbNodes[0];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[0]->setNeighbor(0, othernode0);
      this->vsbNodes[3]->setNeighbor(2, othernode1);
    }
    else if(dir == negX) {
      // negX is between voxels 001 and 010, connecting to vsbNodes 2
      // and 1.
      bool ordered = this->voxelOrder(vox001, vox010);
      Node *node0 = ordered ? this->vsbNodes[2] : this->vsbNodes[1];
      Node *node1 = ordered ? this->vsbNodes[1] : this->vsbNodes[2];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[2]->setNeighbor(1, othernode0);
      this->vsbNodes[1]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      // posY is between voxels 010 and 111, connecting to vsbNodes 1
      // and 3.
      bool ordered = this->voxelOrder(vox010, vox111);
      Node *node0 = ordered ? this->vsbNodes[1] : this->vsbNodes[3];
      Node *node1 = ordered ? this->vsbNodes[3] : this->vsbNodes[1];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[1]->setNeighbor(1, othernode0);
      this->vsbNodes[3]->setNeighbor(0, othernode1);
    }
    else if(dir == negY) {
      // negY is between voxels 001 and 100, connecting to vsbNodes 2
      // and 0.
      bool ordered = this->voxelOrder(vox001, vox100);
      Node *node0 = ordered ? this->vsbNodes[2] : this->vsbNodes[0];
      Node *node1 = ordered ? this->vsbNodes[0] : this->vsbNodes[2];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[2]->setNeighbor(2, othernode0);
      this->vsbNodes[0]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      // posZ is between voxels 001 and 111, connecting to vsbNodes 2
      // and 3.
      bool ordered = this->voxelOrder(vox001, vox111);
      Node *node0 = ordered ? this->vsbNodes[2] : this->vsbNodes[3];
      Node *node1 = ordered ? this->vsbNodes[3] : this->vsbNodes[2];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[2]->setNeighbor(0, othernode0);
      this->vsbNodes[3]->setNeighbor(1, othernode1);
    }
    else if(dir == negZ) {
      // negZ is between voxels 100 and 010, connecting to vsbNodes 0
      // and 1.
      bool ordered = this->voxelOrder(vox100, vox010);
      Node *node0 = ordered ? this->vsbNodes[0] : this->vsbNodes[1];
      Node *node1 = ordered ? this->vsbNodes[1] : this->vsbNodes[0];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[0]->setNeighbor(2, othernode0);
      this->vsbNodes[1]->setNeighbor(2, othernode1);
    }
  } // end CheckerBoard::connect

  virtual Node *connectBack(const ProtoNode*, Node*) {
    assert(false);  // CheckerBoard::connectBack should not be called!
    return nullptr; // not reached
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    // See comments in CheckerBoard::connect.
    if(dir == posX) {
      bool ordered = this->voxelOrder(vox100, vox111);
      node0 = this->vsbNodes[0];
      node1 = this->vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[0]->setNeighbor(0, othernode0);
      this->vsbNodes[3]->setNeighbor(2, othernode1);
    }
    else if(dir == negX) {
      bool ordered = this->voxelOrder(vox001, vox010);
      node0 = this->vsbNodes[2];
      node1 = this->vsbNodes[1];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[2]->setNeighbor(1, othernode0);
      this->vsbNodes[1]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      bool ordered = this->voxelOrder(vox010, vox111);
      node0 = this->vsbNodes[1];
      node1 = this->vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[1]->setNeighbor(1, othernode0);
      this->vsbNodes[3]->setNeighbor(0, othernode1);
    }
    else if(dir == negY) {
      bool ordered = this->voxelOrder(vox001, vox100);
      node0 = this->vsbNodes[2];
      node1 = this->vsbNodes[0];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[2]->setNeighbor(2, othernode0);
      this->vsbNodes[0]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = this->voxelOrder(vox001, vox111);
      node0 = this->vsbNodes[2];
      node1 = this->vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[2]->setNeighbor(0, othernode0);
      this->vsbNodes[3]->setNeighbor(1, othernode1);
    }
    else if(dir == negZ) {
      bool ordered = this->voxelOrder(vox100, vox010);
      node0 = this->vsbNodes[0];
      node1 = this->vsbNodes[1];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[0]->setNeighbor(2, othernode0);
      this->vsbNodes[1]->setNeighbor(2, othernode1);
    }
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "CheckerBoard(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end CheckerBoard

//-------------

// FourThreeOne is three voxels in an L with one more voxel out of the
// plane of the L and over the gap.

template <class COORD, class ICOORD>
class FourThreeOne : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  FourThreeOne(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new FourThreeOne<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ, negZ});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    // The reference configuration is three voxels in the Z=0 plane,
    // vox000, vox100 and vox010, just like ThreeVoxL, plus one voxel
    // at vox111.  The three in the L are connected to vsbNode0 and
    // the single voxel is connected to vsbNode1.  The edges in the
    // posX and posY directions are doubled.

    // Neighbor indexing for the edges of the single voxel at vox111
    // is posZ, posX, posY.  For the inside corner of the L it's negZ,
    // posX, posY.
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == posZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      bool ordered = this->voxelOrder(vox100, vox111);
      Node *othernode0, *othernode1;
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      // Conveniently the posX and posY neighbor indexing is the same
      // for both nodes.
      node0->setNeighbor(1, othernode0);
      node1->setNeighbor(1, othernode1);
    }
    else {
      assert(dir == posY);
      bool ordered = this->voxelOrder(vox010, vox111);
      Node *othernode0, *othernode1;
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto,
			       Node *othernode)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posZ) {
      this->vsbNode1->setNeighbor(0, othernode);
      return this->vsbNode1;
    }
    assert(dir == negZ);
    this->vsbNode0->setNeighbor(0, othernode);
    return this->vsbNode0;
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = this->voxelOrder(vox100, vox111);
      node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      node0->setNeighbor(1, othernode0);
      node1->setNeighbor(1, othernode1);
    }
    else {
      assert(dir == posY);
      bool ordered = this->voxelOrder(vox010, vox111);
      node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FourThreeOne(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};	// end FourThreeOne

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Build the table of ProtoNode classes

template <class COORD, class ICOORD>
std::vector<ProtoVSBNode<COORD, ICOORD>*> &getProtoNodeTable() {
  static std::vector<ProtoVSBNode<COORD, ICOORD>*> table(256, nullptr);
  return table;
}

template <class COORD, class ICOORD>
ProtoVSBNode<COORD, ICOORD> *fetchProtoNode(unsigned char signature) {
  return getProtoNodeTable<COORD, ICOORD>()[signature];
}


template <class COORD, class ICOORD>
void pn(unsigned char signature, ProtoVSBNode<COORD, ICOORD> *protoNode)
{
  assert(protoNode != nullptr);
#ifdef DEBUG
  protoNode->setSignature(signature);
  if(getProtoNodeTable<COORD, ICOORD>()[signature] != nullptr) {
    std::cerr << "Duplicate signature! " << signature << " "
	    << printSig(signature) << std::endl;
    assert(false);
  }
#endif // DEBUG
  getProtoNodeTable<COORD, ICOORD>()[signature] = protoNode;
}

// This version is for voxel configurations that don't create a
// vertex.  The template arguments have to be given explicitly when
// this is used.
template <class COORD, class ICOORD>
void pn(unsigned char signature) {
  getProtoNodeTable<COORD, ICOORD>()[signature] = nullptr;
}

// This function must be called before anything else.
template <class COORD, class ICOORD>
void initializeProtoNodes() {
  // Create an instance of each ProtoVSBNode class in each orientation
  // and store it in a table indexed by the voxel signature for that
  // configuration.  The table is used to create the ProtoVSBNodes
  // when a CMicrostructure is computing voxel set boundaries.

  static bool done = false;
  if(done)
    return;
  done = true;

  // First, the configurations that *don't* define a vertex.
  // Including these explicitly just helps us to be sure that we
  // covered all the cases.
  
  // The trivial cases:
  pn<COORD, ICOORD>(voxelNONE); // no voxels
  pn<COORD, ICOORD>(voxelALL); // all 8 voxels

  // Two adjacent voxels sharing a face (the butterstick
  // configurations) don't define a vertex.  There are 12
  // possibilities:
  pn<COORD, ICOORD>(vox000|vox001);
  pn<COORD, ICOORD>(vox010|vox011);
  pn<COORD, ICOORD>(vox100|vox101);
  pn<COORD, ICOORD>(vox110|vox111);
  pn<COORD, ICOORD>(vox000|vox010);
  pn<COORD, ICOORD>(vox001|vox011);
  pn<COORD, ICOORD>(vox100|vox110);
  pn<COORD, ICOORD>(vox101|vox111);
  pn<COORD, ICOORD>(vox000|vox100);
  pn<COORD, ICOORD>(vox001|vox101);
  pn<COORD, ICOORD>(vox010|vox110);
  pn<COORD, ICOORD>(vox011|vox111);
  // Ditto for the 12 inverse buttersticks (two holes sharing a face).
  pn<COORD, ICOORD>(~(vox000|vox001));
  pn<COORD, ICOORD>(~(vox010|vox011));
  pn<COORD, ICOORD>(~(vox100|vox101));
  pn<COORD, ICOORD>(~(vox110|vox111));
  pn<COORD, ICOORD>(~(vox000|vox010));
  pn<COORD, ICOORD>(~(vox001|vox011));
  pn<COORD, ICOORD>(~(vox100|vox110));
  pn<COORD, ICOORD>(~(vox101|vox111));
  pn<COORD, ICOORD>(~(vox000|vox100));
  pn<COORD, ICOORD>(~(vox001|vox101));
  pn<COORD, ICOORD>(~(vox010|vox110));
  pn<COORD, ICOORD>(~(vox011|vox111));

  // Four voxels in one plane don't define a vertex.  There are 6
  // configurations:
  pn<COORD, ICOORD>(vox000|vox001|vox010|vox011); // x=0
  pn<COORD, ICOORD>(vox100|vox101|vox110|vox111); // x=1
  pn<COORD, ICOORD>(vox000|vox100|vox001|vox101); // y=0
  pn<COORD, ICOORD>(vox010|vox110|vox011|vox111); // y=1
  pn<COORD, ICOORD>(vox000|vox010|vox100|vox110); // z=0
  pn<COORD, ICOORD>(vox001|vox011|vox101|vox111); // z=1
  
  // Two parallel offset stacks of two voxels don't define a vertex.
  pn<COORD, ICOORD>(vox000|vox001|vox110|vox111);
  pn<COORD, ICOORD>(vox100|vox101|vox010|vox011);
  pn<COORD, ICOORD>(vox000|vox100|vox011|vox111);
  pn<COORD, ICOORD>(vox001|vox101|vox010|vox110);
  pn<COORD, ICOORD>(vox001|vox011|vox100|vox110);
  pn<COORD, ICOORD>(vox000|vox010|vox101|vox111);

  // Now the real cases:
  pn(vox111, new SingleVoxel<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox101, new SingleVoxel<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(vox001, new SingleVoxel<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox011, new SingleVoxel<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox000, new SingleVoxel<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox010, new SingleVoxel<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(vox110, new SingleVoxel<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox100, new SingleVoxel<COORD, ICOORD>(VoxRot(posX, negY, negZ)));

  pn(~vox111, new SevenVoxels<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~vox101, new SevenVoxels<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(~vox001, new SevenVoxels<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~vox011, new SevenVoxels<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~vox000, new SevenVoxels<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~vox010, new SevenVoxels<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(~vox110, new SevenVoxels<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(~vox100, new SevenVoxels<COORD, ICOORD>(VoxRot(posX, negY, negZ)));

  pn(vox000|vox110, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox010|vox100, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox001|vox111, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox101|vox011, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox100|vox111, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(vox101|vox110, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  pn(vox000|vox011, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox001|vox010, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox010|vox111, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(vox110|vox011, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox000|vox101, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(vox001|vox100, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negX, posZ, posY)));

  pn(~(vox000|vox110), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox010|vox100), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~(vox001|vox111), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~(vox101|vox011), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(~(vox100|vox111), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(~(vox101|vox110), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  pn(~(vox000|vox011), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(~(vox001|vox010), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(~(vox010|vox111), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(~(vox110|vox011), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(~(vox000|vox101), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(~(vox001|vox100), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negX, posZ, posY)));

  pn(vox000|vox111, new TwoVoxelsByCorner<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox100|vox011, new TwoVoxelsByCorner<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox110|vox001, new TwoVoxelsByCorner<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox010|vox101, new TwoVoxelsByCorner<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  pn(~(vox000|vox111), new SixVoxelsByCorner<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox011), new SixVoxelsByCorner<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~(vox110|vox001), new SixVoxelsByCorner<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~(vox010|vox101), new SixVoxelsByCorner<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  // Three voxels in the Z=0 plane
  pn(vox000|vox100|vox010, new ThreeVoxL<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox100|vox110|vox010, new ThreeVoxL<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  // Three voxels in the Z=1 plane
  pn(vox001|vox101|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox111|vox011|vox001, new ThreeVoxL<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox101|vox111|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox101|vox111|vox001, new ThreeVoxL<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  // Three voxels in the X=0 plane
  pn(vox000|vox010|vox001, new ThreeVoxL<COORD, ICOORD>(VoxRot(posY, posZ, posX)));
  pn(vox000|vox001|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox001|vox011|vox010, new ThreeVoxL<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox000|vox010|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  // Three voxels in the X=1 plane
  pn(vox100|vox101|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(vox111|vox101|vox100, new ThreeVoxL<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  pn(vox101|vox111|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox111|vox110|vox100, new ThreeVoxL<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  // Three voxels in the Y=0 plane
  pn(vox000|vox100|vox001, new ThreeVoxL<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(vox000|vox001|vox101, new ThreeVoxL<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox001|vox101|vox100, new ThreeVoxL<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(vox000|vox100|vox101, new ThreeVoxL<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  // Three voxels in the Y=1 plane
  pn(vox110|vox010|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(vox111|vox011|vox010, new ThreeVoxL<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox111|vox011|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox110|vox010|vox111, new ThreeVoxL<COORD, ICOORD>(VoxRot(posZ, negX, negY)));

  pn(~(vox100|vox101|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(~(vox111|vox101|vox100), new FiveVoxL<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  pn(~(vox101|vox111|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(~(vox111|vox110|vox100), new FiveVoxL<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  pn(~(vox000|vox010|vox001), new FiveVoxL<COORD, ICOORD>(VoxRot(posY, posZ, posX)));
  pn(~(vox000|vox001|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(~(vox001|vox011|vox010), new FiveVoxL<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(~(vox000|vox010|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  pn(~(vox110|vox010|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(~(vox111|vox011|vox010), new FiveVoxL<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(~(vox111|vox011|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(~(vox110|vox010|vox111), new FiveVoxL<COORD, ICOORD>(VoxRot(posZ, negX, negY)));
  pn(~(vox000|vox100|vox001), new FiveVoxL<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(~(vox000|vox001|vox101), new FiveVoxL<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(~(vox001|vox101|vox100), new FiveVoxL<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(~(vox000|vox100|vox101), new FiveVoxL<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  pn(~(vox001|vox101|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(~(vox111|vox011|vox001), new FiveVoxL<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(~(vox101|vox111|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~(vox101|vox111|vox001), new FiveVoxL<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(~(vox000|vox100|vox010), new FiveVoxL<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox000|vox100|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~(vox100|vox110|vox010), new FiveVoxL<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~(vox000|vox010|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  // Double stack in the z direction, single voxel in the z=0 plane
  pn(vox000|vox110|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox100|vox010|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox000|vox110|vox001, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox100|vox010|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  // Double stack in the z direction, single voxel in the z=1 plane
  pn(vox001|vox110|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox010|vox011|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(vox000|vox001|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox100|vox101|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  // Double stack in the x direction, single voxel in the x=1 plane
  pn(vox000|vox100|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox001|vox110|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  pn(vox100|vox011|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(vox101|vox110|vox010, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  // Double stack in the x direction, single voxel in the x=0 plane
  pn(vox000|vox100|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox010|vox001|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  pn(vox000|vox011|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posY, posZ, posX)));
  pn(vox001|vox010|vox110, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  // Double stack in the y direction, single voxel in the x=0 plane
  pn(vox000|vox010|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(vox001|vox100|vox110, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox000|vox101|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(vox100|vox001|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  // Double stack in the y direction, single voxel in the x=1 plane
  pn(vox000|vox010|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox110|vox001|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posZ, negX, negY)));
  pn(vox010|vox101|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(vox100|vox110|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negZ, posX, negY)));

  // Double stack in the z direction, single hole in the z=0 plane
  pn(~(vox000|vox110|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox010|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~(vox000|vox110|vox001), new FiveTwoOne<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~(vox100|vox010|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  // Double stack in the z direction, single hole in the z=1 plane
  pn(~(vox001|vox110|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(~(vox010|vox011|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(~(vox000|vox001|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~(vox100|vox101|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  // Double stack in the x direction, single hole in the x=1 plane
  pn(~(vox000|vox100|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(~(vox001|vox110|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  pn(~(vox100|vox011|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(~(vox101|vox110|vox010), new FiveTwoOne<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  // Double stack in the x direction, single hole in the x=0 plane
  pn(~(vox000|vox100|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(~(vox010|vox001|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  pn(~(vox000|vox011|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posY, posZ, posX)));
  pn(~(vox001|vox010|vox110), new FiveTwoOne<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  // Double stack in the y direction, single hole in the x=0 plane
  pn(~(vox000|vox010|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(~(vox001|vox100|vox110), new FiveTwoOne<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(~(vox000|vox101|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(~(vox100|vox001|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  // Double stack in the y direction, single hole in the x=1 plane
  pn(~(vox000|vox010|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(~(vox110|vox001|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(posZ, negX, negY)));
  pn(~(vox010|vox101|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(~(vox100|vox110|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(negZ, posX, negY)));

  pn(vox110|vox011|vox101, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox100|vox001|vox111, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(vox000|vox101|vox011, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox010|vox001|vox111, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(vox111|vox100|vox010, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox000|vox110|vox101, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox100|vox010|vox001, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox000|vox011|vox110, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(negX, posY, negZ)));

  pn(~(vox110|vox011|vox101), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox001|vox111), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(~(vox000|vox101|vox011), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~(vox010|vox001|vox111), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(~(vox111|vox100|vox010), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(~(vox000|vox110|vox101), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(~(vox100|vox010|vox001), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~(vox000|vox011|vox110), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(negX, posY, negZ)));

  pn(vox000|vox100|vox010|vox011, new ChiralR<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox010|vox110|vox111, new ChiralR<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(vox100|vox010|vox110|vox101, new ChiralR<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox001|vox100|vox110, new ChiralR<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(vox000|vox001|vox011|vox111, new ChiralR<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox101|vox111|vox011|vox010, new ChiralR<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox001|vox101|vox111|vox110, new ChiralR<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox001|vox011|vox100|vox101, new ChiralR<COORD, ICOORD>(VoxRot(negZ, negX, posY)));

  pn(vox000|vox010|vox001|vox101, new ChiralR<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox001|vox011|vox010|vox110, new ChiralR<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox100|vox110|vox111|vox011, new ChiralR<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox000|vox100|vox101|vox111, new ChiralR<COORD, ICOORD>(VoxRot(posY, negZ, negX)));

  pn(vox000|vox001|vox010|vox110, new ChiralL<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox100|vox110|vox010|vox011, new ChiralL<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(vox000|vox100|vox110|vox111, new ChiralL<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox100|vox101|vox010, new ChiralL<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(vox101|vox001|vox011|vox010, new ChiralL<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox001|vox011|vox111|vox110, new ChiralL<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox100|vox101|vox111|vox011, new ChiralL<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox000|vox001|vox101|vox111, new ChiralL<COORD, ICOORD>(VoxRot(negZ, negX, posY)));

  pn(vox000|vox100|vox001|vox011, new ChiralL<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox000|vox010|vox011|vox111, new ChiralL<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox101|vox111|vox110|vox010, new ChiralL<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox001|vox101|vox100|vox110, new ChiralL<COORD, ICOORD>(VoxRot(posY, negZ, negX)));

  pn(vox000|vox001|vox010|vox100, new Pyramid<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox101|vox110, new Pyramid<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox111|vox110|vox010|vox100, new Pyramid<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110|vox011, new Pyramid<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  pn(vox111|vox110|vox101|vox011, new Pyramid<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox001|vox011|vox111|vox010, new Pyramid<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox000|vox001|vox011|vox101, new Pyramid<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox001|vox101|vox111|vox100, new Pyramid<COORD, ICOORD>(VoxRot(negX, posY, negZ)));

  pn(vox100|vox010|vox001|vox111, new CheckerBoard<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox110|vox101|vox011, new CheckerBoard<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(vox000|vox010|vox100|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox110|vox011, new FourThreeOne<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox100|vox010|vox110|vox001, new FourThreeOne<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110|vox101, new FourThreeOne<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  pn(vox000|vox001|vox011|vox110, new FourThreeOne<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox100|vox010|vox011|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox000|vox110|vox111|vox101, new FourThreeOne<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox100|vox101|vox001|vox010, new FourThreeOne<COORD, ICOORD>(VoxRot(negZ, negX, posY)));

  pn(vox010|vox011|vox101|vox110, new FourThreeOne<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(vox100|vox110|vox111|vox001, new FourThreeOne<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  pn(vox000|vox100|vox101|vox011, new FourThreeOne<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  pn(vox000|vox010|vox001|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(posY, posZ, posX)));

  pn(vox000|vox001|vox101|vox110, new FourThreeOne<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox001|vox011|vox010|vox100, new FourThreeOne<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox000|vox011|vox111|vox110, new FourThreeOne<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox010|vox100|vox101|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(posY, negZ, negX)));

  pn(vox100|vox110|vox101|vox011, new FourThreeOne<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(vox000|vox001|vox100|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(vox000|vox010|vox011|vox101, new FourThreeOne<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  pn(vox001|vox111|vox110|vox010, new FourThreeOne<COORD, ICOORD>(VoxRot(posZ, negX, negY)));

  pn(vox001|vox011|vox111|vox100, new FourThreeOne<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox000|vox101|vox011|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox010|vox001|vox101|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(vox110|vox001|vox101|vox011, new FourThreeOne<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
} // end initializeProtoNodes()

#endif // VSB_PROTONODES_H
