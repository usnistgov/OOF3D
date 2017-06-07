// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MASTERELEMENT_H
#define MASTERELEMENT_H

class MasterElement;
class MasterEdge;
class MasterFace;

#include <oofconfig.h>

#include "common/coord.h"
#include "common/pythonexportable.h"
#include "engine/cskeleton2_i.h"
#include "engine/elementshape.h"
#include "engine/gausspoint.h"
#include "engine/mastercoord.h"
#include <iostream>
#include <list>
#include <map>
#include <string>
#include <vector>

#include <vtkCellType.h>

class CSkeleton;
class CSkeletonElement;
class ContourCellSkeleton;
class EdgeBoundaryElement;
class Element;
class ElementBase;
class ElementCornerNodeIterator;
class ElementLite;
class ElementNodeIterator;
class FaceBoundaryElement;
class FEMesh;
//class InterfaceElement;
class Material;
class Node;

// Each Element type has a corresponding MasterElement type.  Only one
// instance of each MasterElement type is created.  The MasterElement
// will need to be constructed *before* the ShapeFunction, because the
// ShapeFunction needs to know the Gauss points so that it can
// precompute its values there.

// The instances of each MasterElement type are stored in a
// MasterElementDict, from which they can be retrieved by name.

typedef std::map<std::string, MasterElement*> MasterElementDict;

std::vector<std::string> *getMasterElementNames();
MasterElement *getMasterElementByName(const std::string&);
MasterElement *getMasterElementByShape(const ElementShape*, int, int);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// MasterElements don't have real Nodes, they just have ProtoNodes.

class ProtoNode {
private:
  const MasterCoord pos;
  MasterElement &element;
  int index_;			// local to a masterelement
  std::vector<int> edgeindex;	// Zero length indicates an interior node.
  std::vector<int> faceindex;
  bool mapping_;
  bool func_;
  bool corner_;
  // only called by MasterElement::addProtoNode
  ProtoNode(MasterElement &el, const MasterCoord &ps)
    : pos(ps),
      element(el),
      mapping_(false),
      func_(false),
      corner_(false)
  {}
public:
  void set_mapping();
  void set_func();
  void set_corner();
  void on_edge(int);
  void on_face(int);

  const MasterCoord &mastercoord() const { return pos; }
  int index() const { return index_; }
  bool mapping() const { return mapping_; }
  bool func() const { return func_; }
  bool corner() const { return corner_; }
  int nedges() const { return edgeindex.size(); } // # of edges this node is on
  int getedge(int i) const { return edgeindex[i]; }
  int nfaces() const { return faceindex.size(); }
  friend class MasterElement;
  friend std::ostream &operator<<(std::ostream &os, const ProtoNode &pn);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MasterElement : public PythonExportable<MasterElement> {
private:
  std::string name_;		// short name
  std::string desc_;		// long description
  const ElementShape *shape_;
public:
  MasterElement(const std::string &nm, const std::string &desc,
		const ElementShape *shape, int nnodes, int nsc);
  virtual ~MasterElement();
  virtual const std::string &modulename() const;
  const std::string &name() const { return name_; }
  const std::string &description() const { return desc_; }
  // int id() const { return id_; }

  // get a ProtoNode by number
  const ProtoNode *protonode(int) const;
  const MasterEdge *masteredge(const ElementCornerNodeIterator&,
			       const ElementCornerNodeIterator&) const;
  int dimension() const { return shape_->dimension(); }
  const ElementShape *shape() const { return shape_; }
  int nnodes() const;
  int nfuncnodes() const;
  int nmapnodes() const;
  int nfaces() const;
  int nedges() const;
  // We used to define nsides(), which was equal to nedges(), but that
  // only makes sense in 2D.
  int ncorners() const { return cornernodes.size(); }
  int nexteriorfuncnodes() const;
  int ninteriorfuncnodes() const { return nfuncnodes() - nexteriorfuncnodes(); }
  int nfacemapnodes_only() const;
  int nedgemapnodes_only() const;
  int ninteriormapnodes_only() const;

  virtual MasterCoord center() const = 0;

  // element order info

  virtual int map_order() const = 0;
  virtual int fun_order() const = 0;
  virtual VTKCellType getCellType() const = 0; // vtk cell type

  // Return a table of gauss points suitable for integration of
  // polynomials of a given degree.  The order of integration (number
  // of gauss points) depends on the subclass.
  virtual const GaussPtTable &gausspointtable(int deg) const = 0;

  // Return a table of gauss points for a given integration order.
  const GaussPtTable &gptable(int) const;

  // Number of orders of integration available.
  // This is defined in the TriangularMaster and QuadrilateralMaster classes.
  int ngauss_sets() const;

  // Number of Gauss points used at given integration order.
  int ngauss(int order) const;

  // Create a real Element
  Element *build(CSkeletonElement *el, const CSkeleton *skel, FEMesh *mesh,
		 const Material *m,
		 SkelElNodeMap &edgeNodeMap, SkelElNodeMap &faceNodeMap) const;
  FaceBoundaryElement *buildFaceBoundary(const std::vector<Node*>&) const;
  EdgeBoundaryElement *buildEdgeBoundary(const std::vector<Node*>&) const;
  ElementLite *buildLite(const std::vector<Coord>*) const;

  //Interface branch
  // Create a real InterfaceElement
  // TODO 3.1: Create 3D implementation.  Commented out temporarily.
  // InterfaceElement *buildInterfaceElement(
  // 			  PyObject *skelel, PyObject *skelel2,
  // 			  int segmentordernumber,
  // 			  Material *m,
  // 			  const std::vector<Node*> *v,
  // 			  const std::vector<Node*> *v2,
  // 			  bool leftnodesinorder,
  // 			  bool rightnodesinorder,
  // 			  const std::vector<std::string> *interfacenames)
  //   const;

  // ***********************

  // Superconvergent patch recovery
  int nSCpoints() const { return sc_points.size(); }
  const MasterCoord &getSCpoint(int i) const { return sc_points[i]; }

  template <class TYPE>
  TYPE interpolate(const std::vector<TYPE>&, const MasterCoord&) const;

  // ***********************

protected:
  ShapeFunction *shapefunction;	// set in derived class constructor
  ShapeFunction *mapfunction;	// ditto

  // The MasterElement derived classes must create their ProtoNodes by
  // calling MasterElement::addProtoNode().  They must start at a
  // corner and proceed counterclockwise around the boundary of the
  // element.  The interior nodes, if any, must come last.  Not
  // following this rule will confuse the skeleton when it's
  // constructing real elements, and the correspondence between
  // ProtoNodes in the MasterElement and Nodes in the Element will be
  // lost.
  ProtoNode *addProtoNode(const MasterCoord&);
  std::vector<const ProtoNode*> protonodes;
  std::vector<int> funcnodes;	// indices into protonode list
  std::vector<int> mapnodes;	// ditto
  std::vector<int> cornernodes;	// ditto ditto
  std::vector<int> exteriorfuncnodes; // ditto ditto ditto
  std::vector<MasterEdge*> edges;
  std::vector<MasterFace*> faces;

  // Superconvergent patch recovery
  void addSCpoint(const MasterCoord&);
  std::vector<MasterCoord> sc_points;

  const std::vector<const MasterCoord*> *findPerimeter() const;
  
  
  // Return a vector of tables of gauss points for all integration orders.
  virtual const std::vector<GaussPtTable> &gptable_vec() const = 0;

  friend class ElementBase;
  // friend class InterfaceElement;
  // friend class ElementNodeIterator;
  friend class ElementCornerNodePositionIterator;
  friend class ElementExteriorNodePositionIterator;
  friend class ElementFuncNodePositionIterator;
  friend class ElementMapNodePositionIterator;
  friend class ShapeFunction;
  friend class ProtoNode;
  friend std::ostream& operator<<(std::ostream&, const MasterElement&);

};  // end class MasterElement

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MasterElement3D : public MasterElement {
public:
  MasterElement3D(const std::string &name, const std::string &desc,
		  const ElementShape *shape,
		  int nnodes, int nsc)
    : MasterElement(name, desc, shape, nnodes, nsc)
  {}
  // TODO 3.1: If we have things other than tets, we may need a four arg
  // version of this.
  const MasterFace *masterface(const ElementCornerNodeIterator&,
			       const ElementCornerNodeIterator&,
			       const ElementCornerNodeIterator&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MasterElement1D : public MasterElement {
public:
  MasterElement1D(const std::string &name, const std::string &desc,
	     int nnodes, int nsc)
    : MasterElement(name, desc, getShape("Line"), nnodes, nsc)
  {}
  virtual ~MasterElement1D() {}
  virtual const GaussPtTable &gausspointtable(int deg) const;
  virtual MasterCoord center() const;
  virtual const std::string &classname() const;
  // element order info
  virtual int map_order() const = 0;
  virtual int fun_order() const = 0;
private:
  virtual const std::vector<GaussPtTable> &gptable_vec() const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MasterElement2D : public MasterElement {
public:
  MasterElement2D(const std::string &name, const std::string &desc, 
		  const ElementShape *shape, int nnodes, int nsc)
    : MasterElement(name, desc, shape, nnodes, nsc) {}
  virtual ~MasterElement2D() {}
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class TriangularMaster : public MasterElement2D {
public:
  TriangularMaster(const std::string &name, const std::string &desc,
		   int nnodes, int nsc)
    : MasterElement2D(name, desc, getShape("Triangle"), nnodes, nsc)
  {}
  virtual ~TriangularMaster() {}
  virtual const std::string &classname() const;
  virtual const GaussPtTable &gausspointtable(int deg) const;
  virtual MasterCoord center() const;
  // element order info
  virtual int map_order() const = 0;
  virtual int fun_order() const = 0;
private:
  virtual const std::vector<GaussPtTable> &gptable_vec() const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class QuadrilateralMaster : public MasterElement2D {
public:
  QuadrilateralMaster(const std::string &name, const std::string &desc,
		      int nnodes, int nsc)
    : MasterElement2D(name, desc, getShape("Quadrilateral"), nnodes, nsc)
  {}
  virtual ~QuadrilateralMaster() {}
  virtual const std::string &classname() const;
  virtual const GaussPtTable &gausspointtable(int deg) const;
  virtual MasterCoord center() const;
  // element order info
  virtual int map_order() const = 0;
  virtual int fun_order() const = 0;
private:
  virtual const std::vector<GaussPtTable> &gptable_vec() const;
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MasterEdge {
private:
  // linked list of nodes on this edge, in order of increasing index,
  // therefore going counterclockwise around the element
  std::list<const ProtoNode*> nlist;
  int funcsize_;
public:
  MasterEdge() : funcsize_(0) {}
  void addNode(const ProtoNode*);
  int size() const { return nlist.size(); }
  int func_size() const { return funcsize_; }
  friend class MasterElement;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MasterFace {
private:
  // vector used for the face so that we can use operator []
  std::vector<const ProtoNode*> nvector;
  int funcsize_;
public:
  MasterFace() : funcsize_(0) {}
  void addNode(const ProtoNode*);
  int size() const { return nvector.size(); }
  int func_size() const { return funcsize_; }
  friend class MasterElement3D;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class TetrahedralMaster : public MasterElement3D {
public:
  TetrahedralMaster(const std::string &name, const std::string &desc,
		    int nnodes, int nsc);
  virtual ~TetrahedralMaster();
  virtual const std::string &classname() const;
  virtual const GaussPtTable &gausspointtable(int deg) const;
  virtual MasterCoord center() const;
  int ncorners() {return 4;}
  virtual int map_order() const = 0;
  virtual int fun_order() const = 0;
private:
  virtual const std::vector<GaussPtTable> &gptable_vec() const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

extern int integration_reduction;

#endif
