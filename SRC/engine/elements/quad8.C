// -*- C++ -*-
// $RCSfile: quad8.C,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/01/18 04:42:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Eight node isoparametric quadrilateral element

#include <oofconfig.h>
#include "engine/masterelement.h"
#include "quad8shapefunction.h"
#include <math.h>


//                      (0, 1)
//  (-1, 1)  6------------5-----------4  (1, 1)
//           |                        |
//           |                        |
//           |                        |
//           |                        |
//  (-1, 0)  7                        3  (1, 0)
//           |                        |
//           |                        |
//           |                        |
//           |                        |
//  (-1,-1)  0------------1-----------2  (1,-1)
//                      (0,-1)        


class Quad_8_8MasterElement : public QuadrilateralMaster {
public:
  Quad_8_8MasterElement()
    : QuadrilateralMaster("Q8_8",
			  "Isoparametric 8 noded quadrilateral with quadratic interpolation for both positions and fields", 8, 4)
  {
    shapefunction = new Quad8ShapeFunction(*this);
    mapfunction = shapefunction;

    ProtoNode *pn;
    
    // 0
    pn = addProtoNode(masterCoord2D(-1, -1));
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(0);
    pn->on_edge(3);

    // 1
    pn = addProtoNode(masterCoord2D(0, -1));
    pn->set_mapping();
    pn->set_func();
    pn->on_edge(0);

    // 2
    pn = addProtoNode(masterCoord2D(1, -1));
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(0);
    pn->on_edge(1);

    // 3
    pn = addProtoNode(masterCoord2D(1, 0));
    pn->set_mapping();
    pn->set_func();
    pn->on_edge(1);

    // 4
    pn = addProtoNode(masterCoord2D(1, 1));
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(1);
    pn->on_edge(2);
    
    // 5
    pn = addProtoNode(masterCoord2D(0, 1));
    pn->set_mapping();
    pn->set_func();
    pn->on_edge(2);

    // 6
    pn = addProtoNode(masterCoord2D(-1, 1));
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(2);
    pn->on_edge(3);

    // 7
    pn = addProtoNode(masterCoord2D(-1, 0));
    pn->set_mapping();
    pn->set_func();
    pn->on_edge(3);

    addSCpoint(masterCoord2D(-1./sqrt(3.), -1./sqrt(3.)));
    addSCpoint(masterCoord2D( 1./sqrt(3.), -1./sqrt(3.)));
    addSCpoint(masterCoord2D( 1./sqrt(3.),  1./sqrt(3.)));
    addSCpoint(masterCoord2D(-1./sqrt(3.),  1./sqrt(3.)));
  }
  virtual ~Quad_8_8MasterElement() {
    delete mapfunction;
  }

  int map_order() const {
    return 2;
  }
  int fun_order() const {
    return 2;
  }

  VTKCellType getCellType() const {
    return VTK_QUADRATIC_QUAD;
  }

};

void quad8init() {
  static Quad_8_8MasterElement m;
}

