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
};

void tet10_4init() {
  static Tet10MasterElement m;
}
