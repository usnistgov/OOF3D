// -*- C++ -*-
// $RCSfile: tri3.C,v $
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

#include <oofconfig.h>
#include "engine/masterelement.h"
#include "common/trace.h"
#include "tri3shapefunction.h"
#include <string>
#include <vector>


// Master element for the three node triangle:
//
//       1  (0,1)
//       |\ 			// backslashes
//       | \			// cause 
//       |  \			// spurious
//       |   \			// compiler
//       |    \			// errors
//       |     \		// at the ends of comments
//       2------0
//  (0,0)          (1,0)
//
// Number the nodes this way so that Cartesian coordinates (x,y)
// correspond to area coordinates (x,y,1-x-y).

class Tri3MasterElement : public TriangularMaster {
public:
  Tri3MasterElement() 
    : TriangularMaster("T3_3",
		       "Isoparametric 3 noded triangle with linear interpolation for both fields and positions.", 3, 1)
  {
    shapefunction = new Tri3ShapeFunction(*this);
    mapfunction = shapefunction;

    ProtoNode *pn0 = addProtoNode(masterCoord2D(1, 0));
    pn0->set_mapping();
    pn0->set_func();
    pn0->set_corner();
    pn0->on_edge(0);
    pn0->on_edge(2);

    ProtoNode *pn1 = addProtoNode(masterCoord2D(0, 1));
    pn1->set_mapping();
    pn1->set_func();
    pn1->set_corner();
    pn1->on_edge(0);
    pn1->on_edge(1);

    ProtoNode *pn2 = addProtoNode(masterCoord2D(0,0));
    pn2->set_mapping();
    pn2->set_func();
    pn2->set_corner();
    pn2->on_edge(1);
    pn2->on_edge(2);

    addSCpoint(masterCoord2D(1./3., 1./3.));  // centroid
  }
  virtual ~Tri3MasterElement() {
    delete shapefunction;
  }

  int map_order() const {
    return 1;
  }
  int fun_order() const {
    return 1;
  }

  VTKCellType getCellType() const {
    return VTK_TRIANGLE;
  }
};

// The initialization function makes a single static instance of the
// master element.  It's inside a function so that the initialization
// order can be controlled from Python.  This works around a problem
// related to this initialization on OS X 10.3.

void tri3init() {
  static Tri3MasterElement m;
}

