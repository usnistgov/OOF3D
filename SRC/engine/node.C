// -*- C++ -*-
// $RCSfile: node.C,v $
// $Revision: 1.41.6.11 $
// $Author: langer $
// $Date: 2014/09/17 17:47:59 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/IO/canvaslayers.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "engine/IO/gridsource.h"
#include "engine/element.h"
#include "engine/equation.h"
#include "engine/femesh.h"
#include "engine/nodalequation.h"
#include "engine/node.h"

#include <vtkSmartPointer.h>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Names needed for PythonExportable base class
const std::string Node::modulename_("ooflib.SWIG.engine.node");
const std::string Node::classname_("Node");
const std::string FuncNode::classname_("FuncNode");

Node::Node(int n, const Coord &p)
  : pos(p),
    index_(n)
{}

FuncNode::FuncNode(FEMesh *mesh, int n, const Coord &p)
  : Node(n, p), PointData(mesh)
{
  // No space is allocated for dofs or nodaleqns here.  It's all done
  // by addField and addEquation.  That means that we're assuming that
  // the FEMesh construction process creates all of the nodes *before*
  // defining any fields or activating any equations.  

  // addField and addEquation are in the PointData class, of which
  // nodes are a subclass.
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Node comparison operator -- the node integer index 
// is the one true arbiter of node equality.

bool operator==(const Node &n1, const Node &n2)
{
  return n1.index() == n2.index();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Node::drawGridCell(vtkSmartPointer<GridSource> src,
			SimpleCellLayer *layer)
const
{
  MeshGridSource *msrc = MeshGridSource::SafeDownCast(src);
  const FEMesh *mesh = msrc->Getmesh();
  double enhancement = msrc->GetEnhancement();
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  points->Allocate(1, 1);
  vtkSmartPointer<vtkIdList> ids = vtkSmartPointer<vtkIdList>::New();
  //double x[3];
  //displaced_position(mesh, enhancement).writePointer(x);
  int idx = points->InsertNextPoint(displaced_position(mesh, enhancement).xpointer());
  ids->InsertNextId(idx);
  layer->newGrid(points, 1);
  layer->addCell(VTK_VERTEX, ids);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Coord FuncNode::displaced_position(const FEMesh *mesh, double enhancement) const
{
#if DIM==2
  static TwoVectorField *displcmnt = 0;
  if(!displcmnt)
    displcmnt = dynamic_cast<TwoVectorField*>(Field::getField("Displacement"));
#elif DIM==3
  static ThreeVectorField *displcmnt = 0;
  if(!displcmnt)
    displcmnt = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
#endif
  if(hasField(*displcmnt)) {
    double dx = (*displcmnt)(this, 0)->value(mesh) * enhancement;
    double dy = (*displcmnt)(this, 1)->value(mesh) * enhancement;
#if DIM==2
    return pos + Coord(dx, dy);
#elif DIM==3
    double dz = (*displcmnt)(this, 2)->value(mesh) * enhancement;
    return pos + Coord(dx, dy, dz);
#endif
  }
  return pos;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const Node &node) {
  os << "[" << node.index() << "] " << node.pos;
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::vector<std::string> *Node::fieldNames() const {
  return new std::vector<std::string>;
}

std::vector<std::string> *FuncNode::fieldNames() const {
  std::vector<std::string> *names = new std::vector<std::string>;
  for(int i=0; i<countCompoundFields(); i++) {
    // TODO OPT: There has to be a better way to do this. 
    CompoundField *field = getCompoundFieldByIndex(i);
    if(hasField(*field)) {
      names->push_back(field->name());
    }
  }
  return names;
}
