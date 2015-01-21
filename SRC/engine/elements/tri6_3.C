// -*- C++ -*-
// $RCSfile: tri6_3.C,v $
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

// Six node triangular element

#include <oofconfig.h>
#include "engine/masterelement.h"
#include "tri3shapefunction.h"
#include "tri6shapefunction.h"

// Master element for the six node triangle.
//
//       2  (0,1)             //
//       |\                   // Believe it or not, all this 
//       | \   	              // stuff out here is just to prevent
//       |  \                 // the compiler from warning about
// edge1 3   1  edge0         // multi-line comments.  It doesn't like
//       |    \               // comment lines ending in a backslash.
//       |     \              //
//       |      \             //
//       4---5---0
//  (0,0)   edge2   (1,0)
//
// //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class Tri_6_3MasterElement : public TriangularMaster {
public:
  Tri_6_3MasterElement()
    : TriangularMaster("T6_3",
		       "Superparametric 6 noded triangle with quadratic interpolation for positions and linear interpolation for fields", 6, 1)
  {
    shapefunction = new Tri3ShapeFunction(*this);
    mapfunction = new Tri6ShapeFunction(*this);

    ProtoNode *pn;
    
    pn = addProtoNode(masterCoord2D(1,0)); // node 0
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(0);
    pn->on_edge(2);

    pn = addProtoNode(masterCoord2D(0.5, 0.5)); // node 1
    pn->set_mapping();
    pn->on_edge(0);

    pn = addProtoNode(masterCoord2D(0, 1)); // node 2
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(0);
    pn->on_edge(1);

    pn = addProtoNode(masterCoord2D(0, 0.5)); // node 3
    pn->set_mapping();
    pn->on_edge(1);

    pn = addProtoNode(masterCoord2D(0,0)); // node 4
    pn->set_mapping();
    pn->set_func();
    pn->set_corner();
    pn->on_edge(1);
    pn->on_edge(2);
    
    pn = addProtoNode(masterCoord2D(0.5, 0)); // node 5
    pn->set_mapping();
    pn->on_edge(2);

    addSCpoint(masterCoord2D(1./3., 1./3.));  // centroid
  }

  virtual ~Tri_6_3MasterElement() {
    delete shapefunction ;
    delete mapfunction;
  }

  int map_order() const {
    return 2;
  }
  int fun_order() const {
    return 1;
  }
  
  VTKCellType getCellType() const {
    return VTK_TRIANGLE;
  }
};

void tri6_3init() {
  static Tri_6_3MasterElement m;
}
