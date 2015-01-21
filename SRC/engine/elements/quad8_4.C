// -*- C++ -*-
// $RCSfile: quad8_4.C,v $
// $Revision: 1.4.6.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Eight node quadrilateral element

// This file is currently not loaded.  See comments in quad8_4.spy,
// and commented-out lines in DIR.py and initialize.py.

#include <oofconfig.h>
#include "engine/masterelement.h"
#include "quad4shapefunction.h"
#include "quad8shapefunction.h"


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


class Quad_8_4MasterElement : public QuadrilateralMaster {
public:
  Quad_8_4MasterElement()
    : QuadrilateralMaster("Q8_4", 
			  "Superparametric 8 noded quadrilateral with quadratic interpolation for positions and bilinear interpolation for fields", 8, 1)
  {
    shapefunction = new Quad4ShapeFunction(*this);
    mapfunction = new Quad8ShapeFunction(*this);

    ProtoNode *pn;
    
    // 0
    pn = addProtoNode(MasterCoord(-1, -1));
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(0);
    pn->on_edge(3);

    // 1
    pn = addProtoNode(MasterCoord(0, -1));
    pn->set_mapping();
    pn->on_edge(0);

    // 2
    pn = addProtoNode(MasterCoord(1, -1));
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(0);
    pn->on_edge(1);

    // 3
    pn = addProtoNode(MasterCoord(1, 0));
    pn->set_mapping();
    pn->on_edge(1);

    // 4
    pn = addProtoNode(MasterCoord(1, 1));
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(1);
    pn->on_edge(2);
    
    // 5
    pn = addProtoNode(MasterCoord(0, 1));
    pn->set_mapping();
    pn->on_edge(2);

    // 6
    pn = addProtoNode(MasterCoord(-1, 1));
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(2);
    pn->on_edge(3);

    // 7
    pn = addProtoNode(MasterCoord(-1, 0));
    pn->set_mapping();
    pn->on_edge(3);

    addSCpoint(MasterCoord(0., 0.));
  }
  virtual ~Quad_8_4MasterElement() {
    delete shapefunction;
    delete mapfunction;
  }

  int map_order() const {
    return 2;
  }
  int fun_order() const {
    return 1;
  }

};

void quad8_4init() {
  static Quad_8_4MasterElement m;
}

