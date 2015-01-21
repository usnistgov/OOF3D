// -*- C++ -*-
// $RCSfile: masterelement.h,v $
// $Revision: 1.32.10.11 $
// $Author: langer $
// $Date: 2014/09/16 02:48:42 $

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
#include "engine/elementshape.h"
#include "engine/gausspoint.h"
#include "engine/mastercoord.h"
#include <iostream>
#include <list>
#include <map>
#include <string>
#include <vector>

#include <vtkCellType.h>

class CSkeletonElement;
class ContourCellSkeleton;
class EdgeBoundaryElement;
class Element;
class ElementBase;
class ElementCornerNodeIterator;
class ElementLite;
class ElementNodeIterator;
class FaceBoundaryElement;
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
#if DIM == 3
  std::vector<int> faceindex;
#endif	// DIM == 3
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
#if DIM==3
  void on_face(int);
#endif

  const MasterCoord &mastercoord() const { return pos; }
  int index() const { return index_; }
  bool mapping() const { return mapping_; }
  bool func() const { return func_; }
  bool corner() const { return corner_; }
  int nedges() const { return edgeindex.size(); } // # of edges this node is on
  int getedge(int i) const { return edgeindex[i]; }
  friend class MasterElement;
  friend std::ostream &operator<<(std::ostream &os, const ProtoNode &pn);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MasterElement : public PythonExportable<MasterElement> {
private:
  std::string name_;		// short name
  std::string desc_;		// long description
  const ElementShape *shape_;
  // int id_;
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
  int nexteriormapnodes_only() const;
  int ninteriormapnodes_only() const;

  virtual MasterCoord center() const = 0;

  // element order info

  virtual int map_order() const = 0;
  virtual int fun_order() const = 0;
  virtual VTKCellType getCellType() const = 0; // vtk cell type

#if DIM == 2
  virtual const std::vector<const MasterCoord*> &perimeter() const = 0;
#endif	// DIM == 2

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
  Element *build(CSkeletonElement *el, const Material *m,
		 const std::vector<Node*> *v) const;
  FaceBoundaryElement *buildFaceBoundary(const std::vector<Node*>*) const;
  EdgeBoundaryElement *buildEdgeBoundary(const std::vector<Node*>*) const;
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

#if DIM == 3
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
#endif	// DIM == 3

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MasterElement1D : public MasterElement {
#if DIM == 2
protected:
  // Only for contouring support in 2D
  virtual int sideno(const MasterCoord&) const { return 0; }
  virtual const MasterCoord *endpoint(int) const { return 0; }
#endif // DIM == 2
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

#if DIM == 2
  // Return the subcells to be used for contouring
  virtual std::vector<ContourCellSkeleton*>* contourcells(int n) const = 0;

  // Return an object used to sort points along the boundary of the
  // element, used in closing contours.
  virtual MasterEndPointComparator bdysorter() const = 0;
  CCurve *perimeterSection(const MasterCoord*, const MasterCoord*) const;
  
  // Is a point on the boundary of the element?
  virtual bool onBoundary(const MasterCoord&) const = 0;
  virtual bool onBoundary2(const MasterCoord&, const MasterCoord&) const = 0;

  // Are two points on the same exterior boundary of the element?
  // Exterior boundaries are those corresponding to node iterators
  // passed in through the third argument of this function.
  virtual bool exterior(const MasterCoord&, const MasterCoord&,
			const std::vector<ElementCornerNodeIterator> &ext)
    const = 0;
protected:
  virtual int sideno(const MasterCoord&) const = 0;
  virtual const MasterCoord *endpoint(int) const = 0;

#endif	// DIM == 2
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

#if DIM == 2
  // Routines used only for contour plotting in 2D.  These don't need
  // to be implemented in 3D, and will probably go away when vtk is
  // used for 2D.
  virtual std::vector<ContourCellSkeleton*>* contourcells(int) const;
  virtual bool onBoundary(const MasterCoord&) const;
  virtual bool onBoundary2(const MasterCoord&, const MasterCoord&) const;
  virtual bool exterior(const MasterCoord&, const MasterCoord&,
			const std::vector<ElementCornerNodeIterator> &ext)
    const;
  virtual const std::vector<const MasterCoord*> &perimeter() const;
  virtual MasterEndPointComparator bdysorter() const;
  static bool endPointComparator(const MasterEndPoint&, const MasterEndPoint&);
  static int sidenumber(const MasterCoord&);
protected:
  virtual int sideno(const MasterCoord &x) const { return sidenumber(x); }
  virtual const MasterCoord *endpoint(int) const;
#endif // DIM == 2

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
#if DIM == 2
  virtual std::vector<ContourCellSkeleton*>* contourcells(int) const;
  virtual bool onBoundary(const MasterCoord&) const;
  virtual bool onBoundary2(const MasterCoord&, const MasterCoord&) const;
  virtual bool exterior(const MasterCoord&, const MasterCoord&,
			const std::vector<ElementCornerNodeIterator> &ext)
    const;
  virtual const std::vector<const MasterCoord*> &perimeter() const;
  virtual MasterEndPointComparator bdysorter() const;
  static bool endPointComparator(const MasterEndPoint&, const MasterEndPoint&);
  static int sidenumber(const MasterCoord&);
protected:
  virtual int sideno(const MasterCoord &x) const { return sidenumber(x); }
  virtual const MasterCoord *endpoint(int) const;
#endif	// DIM == 2
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

#if DIM == 3

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
//   // element order info
  virtual int map_order() const = 0;
  virtual int fun_order() const = 0;
//   virtual const std::vector<const MasterCoord*> &perimeter() const;
//   static bool endPointComparator(const MasterEndPoint&, const MasterEndPoint&);
//   static int sidenumber(const MasterCoord&);
// protected:
//   virtual int sideno(const MasterCoord &x) const { return sidenumber(x); }
//   virtual const MasterCoord *endpoint(int) const;
private:
  virtual const std::vector<GaussPtTable> &gptable_vec() const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#endif	// DIM == 3

extern int integration_reduction;

#endif
