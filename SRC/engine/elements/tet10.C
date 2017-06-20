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
#include "engine/masterelement.h"
#include "tet10shapefunction.h"
#include "tet4shapefunction.h"
#include "common/trace.h"

// TODO: Move tet topology definitions out of CSkeletonElement and
// don't include cskeletonelement.h here.
#include "engine/cskeletonelement.h"

#include <vtkCellType.h>


// Master element for the ten node tetrahedron.

class Tet10MasterElement : public TetrahedralMaster {
public:
  Tet10MasterElement()
    : TetrahedralMaster("TET4_10",
			"Subparametric 10 noded tetrahedron with linear interpolation for positions and quadratic interpolation for fields.", 10, 1)
  {
    shapefunction = new Tet10ShapeFunction(*this);
    mapfunction = new Tet4ShapeFunction(*this);

    // Node ordering for the corners has to be compatible with the
    // ordering used by vtk, which is what the Skeleton element uses.
    // Getting it wrong will produce elements with negative volumes.

    ProtoNode *pn0 = addProtoNode(MasterCoord(0.0, 0.0, 0.0));
    pn0->set_mapping();
    pn0->set_func();
    pn0->set_corner();
    pn0->on_edge(0);
    pn0->on_edge(2);
    pn0->on_edge(3);
    pn0->on_face(0);
    pn0->on_face(2);
    pn0->on_face(3);

    ProtoNode *pn1 = addProtoNode(MasterCoord(0.0, 1.0, 0.0));
    pn1->set_mapping();
    pn1->set_func();
    pn1->set_corner();
    pn1->on_edge(0);
    pn1->on_edge(1);
    pn1->on_edge(4);
    pn1->on_face(0);
    pn1->on_face(1);
    pn1->on_face(3);

    ProtoNode *pn2 = addProtoNode(MasterCoord(0.0, 0.0, 1.0));
    pn2->set_mapping();
    pn2->set_func();
    pn2->set_corner();
    pn2->on_edge(3);
    pn2->on_edge(4);
    pn2->on_edge(5);
    pn2->on_face(0);
    pn2->on_face(1);
    pn2->on_face(2);

    ProtoNode *pn3 = addProtoNode(MasterCoord(1.0, 0.0, 0.0));
    pn3->set_mapping();
    pn3->set_func();
    pn3->set_corner();
    pn3->on_edge(1);
    pn3->on_edge(2);
    pn3->on_edge(5);
    pn3->on_face(1);
    pn3->on_face(2);
    pn3->on_face(3);

    // Nodes on edges

    ProtoNode *pn4 = addProtoNode(MasterCoord(0.0, 0.5, 0.0));
    pn4->set_func();
    pn4->on_edge(0);
    pn4->on_face(0);
    pn4->on_face(3);

    ProtoNode *pn5 = addProtoNode(MasterCoord(0.0, 0.0, 0.5));
    pn5->set_func();
    pn5->on_edge(2);
    pn5->on_face(2);
    pn5->on_face(3);

    ProtoNode *pn6 = addProtoNode(MasterCoord(0.5, 0.0, 0.0));
    pn6->set_func();
    pn6->on_edge(3);
    pn6->on_face(0);
    pn6->on_face(2);

    ProtoNode *pn7 = addProtoNode(MasterCoord(0.0, 0.5, 0.5));
    pn7->set_func();
    pn7->on_edge(1);
    pn7->on_face(1);
    pn7->on_face(3);

    ProtoNode *pn8 = addProtoNode(MasterCoord(0.5, 0.0, 0.5));
    pn8->set_func();
    pn8->on_edge(5);
    pn8->on_face(1);
    pn8->on_face(2);

    ProtoNode *pn9 = addProtoNode(MasterCoord(0.5, 0.5, 0.0));
    pn9->set_func();
    pn9->on_edge(4);
    pn9->on_face(0);
    pn9->on_face(1);

    // There should presumably be more than on superconvergent point,
    // but we haven't implemented superconvergent patch recovery in 3D
    // yet anyway.  This point is probably incorrect.
    addSCpoint(MasterCoord(1./4, 1./4, 1./4));
  }

  virtual ~Tet10MasterElement() {
    delete shapefunction;
    delete mapfunction;
  }

  int map_order() const {
    return 1;
  }

  int fun_order() const {
    return 2;
  }

  VTKCellType getCellType() const {
    return VTK_TETRA;
  }

  // getIntermediateEdgeNodes returns the nodes for a 1D element that
  // coincides with the edge of this element spanning the given corner
  // nodes. The nodes are specified by their indices in this element's
  // protonodes list.  The result is in the order expected by the 1D
  // element's constructor.

  NodeIndexVec getIntermediateEdgeNodes(const NodeIndexVec &crnrs) const {
    assert(crnrs.size() == 2);
    assert(crnrs[0] != crnrs[1]);
    unsigned int edgeNo = CSkeletonElement::nodeNodeEdge[crnrs[0]][crnrs[1]];
    NodeIndexVec result;
    if(edgeNo == 0)
      result = {0, 4, 1};
    else if(edgeNo == 1)
      result = {1, 7, 2};
    else if(edgeNo == 2)
      result = {0, 5, 2};
    else if(edgeNo == 3)
      result = {0, 6, 3};
    else if(edgeNo == 4)
      result = {1, 9, 3};
    else if(edgeNo == 5)
      result = {2, 8, 3};
    else 
      throw ErrProgrammingError("Bad edge number!", __FILE__, __LINE__);
    if(result.front() != crnrs.front()) {
      assert(result.front() == crnrs.back() && result.back() == crnrs.front());
      std::reverse(result.begin(), result.end());
    }
    return result;
  }
  
  // getIntermediateFaceeNodes returns the nodes for a 2D element that
  // coincides with the face of this element spanning the given corner
  // nodes. The nodes are specified by their indices in this element's
  // protonodes list.  The result is in the order expected by the 2D
  // element's constructor.

  NodeIndexVec getIntermediateFaceNodes(const NodeIndexVec &crnrs) const {
    assert(crnrs.size() == 3);
    assert(crnrs[0]!=crnrs[1] && crnrs[1]!=crnrs[2] && crnrs[2]!=crnrs[0]);
    // The face can be identified easily by the corner that's *not* in
    // the given list.
    int missingNode = 6 - crnrs[0] - crnrs[1] - crnrs[2];
    NodeIndexVec nodes;
    if(missingNode == 0) {
      nodes = {1, 7, 2, 8, 3, 9};
    }
    else if(missingNode == 1) {
      nodes = {0, 6, 3, 8, 2, 5};
    }
    else if(missingNode == 2) {
      nodes = {0, 4, 1, 9, 3, 6};
    }
    else if(missingNode == 3) {
      nodes = {0, 5, 2, 7, 1, 4};
    }
    else
      throw ErrProgrammingError("Bad face number!", __FILE__, __LINE__);

    // The lists of node indices created above contain the nodes of
    // the desired face going in order around the face, but they might
    // not go around the face in the right direction or start at the
    // right node.  They need to start at crnrs[0] and then go to
    // crnrs[1], with one intervening node.
    
    // See if the result needs to be permuted.
    // Find the position in nodes of the first and second entries in crnrs.
    auto i0 = std::find(nodes.begin(), nodes.end(), crnrs[0]);
    auto i1 = std::find(nodes.begin(), nodes.end(), crnrs[1]);
    assert(i0 < nodes.end() && i1 < nodes.end() && i0 != i1);
    // If crnrs[0] and crnrs[1] are already the first and third
    // entries in nodes, no permutation is needed.
    if(i0 == nodes.begin() && i1 == i0+2)
      return nodes;
    // If crnrs[1] is 2 spots after crnrs[0], or if it's 4 spots
    // earlier (the list wraps around) then the list is in the right
    // direction but starts at the wrong place.  Use a cyclic
    // permutation.
    if((i0 < i1 && i1 == i0 + 2) || (i0 > i1 && i0 == i1 + 4)) {
      NodeIndexVec result(i0, nodes.end());	      // i0 to end
      result.insert(result.end(), nodes.begin(), i0); // beginning to i0-1
      return result;
    }
    // If crnrs[1] is 4 spots after crnrs[0], or if it's 2 spots
    // earlier (the list wraps around) then the list is in the wrong
    // direction and maybe also starts at the wrong place.  Use a
    // cyclic permutation of the reversed list.
    if((i0 < i1 && i1 == i0 + 4) || (i0 > i1 && i0 == i1 + 2)) {
      // r0 iterates backwards starting at i0.
      auto r0=std::reverse_iterator<NodeIndexVec::iterator>(i0)-1;
      // Include entries from i0 to the beginning (ie rend).
      NodeIndexVec result(r0, nodes.rend());
      // Include from the end (ie rbegin) to i0+1
      result.insert(result.end(), nodes.rbegin(), r0);
      return result;
    }
    throw ErrProgrammingError("Unexpected node ordering!",
				__FILE__, __LINE__);
  }

  
};				// end class Tet10MasterElement

void tet10_4init() {
  static Tet10MasterElement m;
}
