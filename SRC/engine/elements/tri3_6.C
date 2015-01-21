// -*- C++ -*-
// $RCSfile: tri3_6.C,v $
// $Revision: 1.3.18.1 $
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

// Six node triangular element

#include <oofconfig.h>
#include "engine/masterelement.h"
#include "tri3shapefunction.h"
#include "tri6shapefunction.h"

// Master element for the six node triangle.
//
//       2  (0,1)
//       |\ 					   	// backslash
//       | \						// terminated
//       |  \						// comments
//       3   1						// generate
//       |    \						// spurious
//       |     \					// compiler
//       |      \					// warnings
//       4---5---0
//  (0,0)           (1,0)
//

class Tri6MasterElement : public TriangularMaster {
public:
  Tri6MasterElement()
    : TriangularMaster("T3_6",
		       "Subparametric 6 noded triangle with linear interpolation for positions and quadratic interpolation for fields", 6, 3)
  {
    shapefunction = new Tri6ShapeFunction(*this);
    mapfunction = new Tri3ShapeFunction(*this);

    ProtoNode *pn;

    pn = addProtoNode(masterCoord2D(1, 0)); // map node 0, func node 0
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(0);
    pn->on_edge(2);

    pn = addProtoNode(masterCoord2D(0.5, 0.5)); // func node 1
    pn->set_func();
    pn->on_edge(0);

    pn = addProtoNode(masterCoord2D(0, 1)); // map node 1, func node 2
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(0);
    pn->on_edge(1);

    pn = addProtoNode(masterCoord2D(0, 0.5)); // func node 3
    pn->set_func();
    pn->on_edge(1);

    pn = addProtoNode(masterCoord2D(0,0)); // map node 2, func node 4
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(1);
    pn->on_edge(2);
    
    pn = addProtoNode(masterCoord2D(0.5, 0)); // func node 5
    pn->set_func();
    pn->on_edge(2);

    addSCpoint(masterCoord2D(0.5, 0.));
    addSCpoint(masterCoord2D(0.5, 0.5));
    addSCpoint(masterCoord2D(0., 0.5));
  }

  virtual ~Tri6MasterElement() {
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
    return VTK_QUADRATIC_TRIANGLE;
  }
};

void tri3_6init() {
  static Tri6MasterElement m;
}
