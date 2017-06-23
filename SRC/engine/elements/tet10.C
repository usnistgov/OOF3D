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
#include <algorithm>

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
    // ordering used by vtk.  See Chapter 5, Figure 5-4, in the VTK
    // book.

    std::vector<ProtoNode*> cpn(4, nullptr); // corner protonodes

    cpn[0] = addProtoNode(MasterCoord(0.0, 0.0, 0.0));
    cpn[0]->set_mapping();
    cpn[0]->set_func();
    cpn[0]->set_corner();
    cpn[0]->on_edge(0);
    cpn[0]->on_edge(2);
    cpn[0]->on_edge(3);
    cpn[0]->on_face(0);
    cpn[0]->on_face(2);
    cpn[0]->on_face(3);

    cpn[1] = addProtoNode(MasterCoord(0.0, 1.0, 0.0));
    cpn[1]->set_mapping();
    cpn[1]->set_func();
    cpn[1]->set_corner();
    cpn[1]->on_edge(0);
    cpn[1]->on_edge(1);
    cpn[1]->on_edge(4);
    cpn[1]->on_face(0);
    cpn[1]->on_face(1);
    cpn[1]->on_face(3);

    cpn[2] = addProtoNode(MasterCoord(0.0, 0.0, 1.0));
    cpn[2]->set_mapping();
    cpn[2]->set_func();
    cpn[2]->set_corner();
    cpn[2]->on_edge(3);
    cpn[2]->on_edge(4);
    cpn[2]->on_edge(5);
    cpn[2]->on_face(0);
    cpn[2]->on_face(1);
    cpn[2]->on_face(2);

    cpn[3] = addProtoNode(MasterCoord(1.0, 0.0, 0.0));
    cpn[3]->set_mapping();
    cpn[3]->set_func();
    cpn[3]->set_corner();
    cpn[3]->on_edge(1);
    cpn[3]->on_edge(2);
    cpn[3]->on_edge(5);
    cpn[3]->on_face(1);
    cpn[3]->on_face(2);
    cpn[3]->on_face(3);

    // Nodes on edges.  VTK kindly numbers them in order of edge
    // numbers.  The ProtoNode index is the 4 plus the edge number.
    for(unsigned int edge=0; edge<6; edge++) {
      unsigned int c0 = CSkeletonElement::edgeNodes[edge][0];
      unsigned int c1 = CSkeletonElement::edgeNodes[edge][1];
      ProtoNode *pn = addProtoNode(0.5*(cpn[c0]->mastercoord() +
					cpn[c1]->mastercoord()));
      pn->set_func();
      pn->on_edge(edge);
      pn->on_face(CSkeletonElement::edgeFaces[edge][0]);
      pn->on_face(CSkeletonElement::edgeFaces[edge][1]);
    }

    // There should presumably be more than one superconvergent point,
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
    return VTK_QUADRATIC_TETRA;
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
    unsigned int midPt = edgeNo + 4;
    // NodeIndexVec result(3);
    // result[0] = crnrs[0];
    // result[1] = midPt;
    // result[2] = crnrs[1];
    // return result;
    return NodeIndexVec({crnrs[0], midPt, crnrs[1]});
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
      nodes = {1, 5, 2, 9, 3, 8};
    }
    else if(missingNode == 1) {
      nodes = {0, 7, 3, 9, 2, 6};
    }
    else if(missingNode == 2) {
      nodes = {0, 4, 1, 8, 3, 7};
    }
    else if(missingNode == 3) {
      nodes = {0, 6, 2, 5, 1, 4};
    }
    else
      throw ErrProgrammingError("Bad face number!", __FILE__, __LINE__);

    // The lists of node indices created above contain the nodes of
    // the desired face going in order around the face, but possibly
    // in the wrong direction or starting at the wrong node.  It needs
    // to start at crnrs[0] and then go to crnrs[1], with one
    // intervening node.
    
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
