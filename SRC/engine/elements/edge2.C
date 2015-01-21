// -*- C++ -*-
// $RCSfile: edge2.C,v $
// $Revision: 1.2.16.1 $
// $Author: langer $
// $Date: 2014/01/18 04:41:58 $

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
#include "edge2shapefunction.h"
#include "common/trace.h"

// Master element for the 2-noded edge element:
//
//     0----------------------1
//  (-1,0)                  (1,0)
// Here, the y-component of master-coord is totally trivial.


class Edge2MasterElement : public MasterElement1D{
public:
  Edge2MasterElement()
  //Interface branch
    : MasterElement1D("D2_2","Isoparametric 2-noded edge element", 2, 0)
      //    : MasterElement1D("Isoparametric 2-noded edge element", 2)
  {
    shapefunction = new Edge2ShapeFunction(*this);
    mapfunction = shapefunction;

    ProtoNode *pn0 = addProtoNode(masterCoord1D(-1.));
    pn0->set_mapping();
    pn0->set_func();
    // not sure about these two ...
    pn0->set_corner();
    pn0->on_edge(0);

    ProtoNode *pn1 = addProtoNode(masterCoord1D(1.));
    pn1->set_mapping();
    pn1->set_func();
    // not sure about these two ...
    pn1->set_corner();
    pn1->on_edge(0);
  }
  virtual ~Edge2MasterElement(){
    delete shapefunction;
  }

  int map_order() const {
    return 1;
  }
  int fun_order() const {
    return 1;
  }

  VTKCellType getCellType() const {
    return VTK_LINE;
  }

};

static Edge2MasterElement m;
