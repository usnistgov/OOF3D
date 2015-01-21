// -*- C++ -*-
// $RCSfile: quad4.C,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/01/18 04:41:59 $

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
#include "quad4shapefunction.h"
#include "common/trace.h"


// Master element for the four node quadrilateral:
//
//  (-1,1)   3--------------------2  (1,1)
//           |                    | 
//           |                    |
//           |                    |
//           |                    |
//           |                    |
//           |                    |
//           |                    |
//  (-1,-1)  0--------------------1  (1,-1)


class Quad4MasterElement : public QuadrilateralMaster {
public:
  Quad4MasterElement()
    : QuadrilateralMaster("Q4_4",
			  "Isoparametric 4 noded quadrilateral with bilinear interpolation for both positions and fields", 4, 1)
  {
    shapefunction = new Quad4ShapeFunction(*this);
    mapfunction = shapefunction;

    ProtoNode *pn0 = addProtoNode(masterCoord2D(-1.0, -1.0));
    pn0->set_mapping();
    pn0->set_func();
    pn0->set_corner();
    pn0->on_edge(0);
    pn0->on_edge(3);

    ProtoNode *pn1 = addProtoNode(masterCoord2D(1.0, -1.0));
    pn1->set_mapping();
    pn1->set_func();
    pn1->set_corner();
    pn1->on_edge(0);
    pn1->on_edge(1);

    ProtoNode *pn2 = addProtoNode(masterCoord2D(1.0, 1.0));
    pn2->set_mapping();
    pn2->set_func();
    pn2->set_corner();
    pn2->on_edge(1);
    pn2->on_edge(2);
    
    ProtoNode *pn3 = addProtoNode(masterCoord2D(-1.0, 1.0));
    pn3->set_mapping();
    pn3->set_func();
    pn3->set_corner();
    pn3->on_edge(2);
    pn3->on_edge(3);

    addSCpoint(masterCoord2D(0., 0.));
  }
  virtual ~Quad4MasterElement() {
    delete shapefunction;   
  }

  int map_order() const {
    return 1;
  }
  int fun_order() const {
    return 1;
  }

  VTKCellType getCellType() const {
    return VTK_QUAD;
  }

};

void quad4init() {
  static Quad4MasterElement m;
}

