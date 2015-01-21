// -*- C++ -*-
// $RCSfile: element.h,v $
// $Revision: 1.64.2.22 $
// $Author: langer $
// $Date: 2014/09/16 02:48:40 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ELEMENT_H
#define ELEMENT_H

class Element;
class MasterElement;

#include "common/coord.h"
#include "common/doublevec.h"
#include "common/pythonexportable.h"
#include "engine/gausspoint.h"
#include "engine/indextypes.h"
#include "engine/shapefunction.h"
#include <string>
#include <vector>

#if DIM==3
#include <vtkCellType.h>
#include <vtkSmartPointer.h>
#include <vtkIdList.h>
#endif // DIM==3

class BoundaryEdge;
class BoundaryFace;
class CNonlinearSolver;
class CSkeletonBase;
class CSkeletonElement;
class CSubProblem;
class Edge;
class EdgeSet;
class ElementCornerNodeIterator;
class ElementCornerNodePositionIterator;
class ElementFuncNodeIterator;
class ElementFuncNodePositionIterator;
class ElementMapNodeIterator;
class ElementMapNodePositionIterator;
class ElementNodeIterator;
class ElementNodePositionIterator;
class ElementReg;
class FEMesh;
class Face;
class Field;
class Flux;
class FuncNode;
class GridSource;
class LinearizedSystem;
class MasterElement;
class MasterPosition;
class Material;
class Node;
class OutputValue;
class SimpleCellLayer;

#if DIM==3
class MasterElement3D;
#endif // DIM==3

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Base class for storage into the element.  Subclasses should 
// add fields for the actual data they want to store.

class ElementData : public PythonExportable<ElementData> {
private:
  const std::string name_;
public:
  ElementData(const std::string &nm);
  virtual ~ElementData() {}
  virtual const std::string &classname() const = 0;
  virtual const std::string &modulename() const = 0;
  const std::string &name() const { return name_; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ElementBase is the base class for Element, real full-featured
// finite elements, and for ElementLite, which are used for plotting
// cross sections and other temporary uses.

class ElementBase : public PythonExportable<ElementBase> {
private:
  ElementBase(const ElementBase&);	      // prohibited
  ElementBase &operator=(const ElementBase&); // prohibited
protected:
  const MasterElement &master;

public:
  ElementBase(const MasterElement&);
  virtual ~ElementBase() {}
  virtual const std::string &modulename() const;
  const MasterElement &masterelement() const { return master; }
  int dimension() const;
  int nnodes() const;
  int nmapnodes() const;
  int nfuncnodes() const;
  int ncorners() const;
  int nexteriorfuncnodes() const; // exterior to the element, not the mesh.

  int nedges() const;

  virtual Coord position(int node) const = 0;

  // The node_positerator methods are like the node_iterator methods
  // in the Element class, except that they only return the positions
  // of the nodes, not the nodes themselves.  This allows them to work
  // with ElementLites, which don't have real Node objects.
  ElementNodePositionIterator *node_positerator() const;
  ElementMapNodePositionIterator *mapnode_positerator() const;
  ElementFuncNodePositionIterator *funcnode_positerator() const;
  ElementCornerNodePositionIterator *cornernode_positerator() const;

  int shapefun_degree() const;
  int dshapefun_degree() const;
  int mapfun_degree() const;

  // det_jacobian times d(master coord)/d(real coord)
  // includes the factor of |J| for efficiency... don't compute it too often
  double Jdmasterdx(SpaceIndex, SpaceIndex, const GaussPoint&) const;
  double Jdmasterdx(SpaceIndex, SpaceIndex, const MasterCoord&) const;
  double Jdmasterdx(SpaceIndex, SpaceIndex, const Coord&) const; // slow

  // Jacobian of the transformation from master to real coordinates
  virtual double jacobian(SpaceIndex, SpaceIndex, const GaussPoint&) const;
  virtual double jacobian(SpaceIndex, SpaceIndex, const MasterCoord&) const;

  virtual double det_jacobian(const GaussPoint &g) const;
  virtual double det_jacobian(const MasterCoord &mc) const;

  MasterCoord to_master(const Coord&) const; // slow!
  Coord from_master(const MasterPosition&) const;
  // swig requires versions that take pointers instead of references
  MasterCoord to_master(const Coord *c) const { return to_master(*c); }
  Coord from_master(const MasterPosition *m) const { return from_master(*m); }
  MasterCoord center() const;
  double span() const; // Volume, area, or length, depending on dimension.

  // function to return a bunch of gausspoints, for doing integration
  // in Python.  This is probably temporary.
  std::vector<GaussPoint*>* integration_points(int order) const;

  GaussPointIterator integrator(int order) const;
  // int ngauss(int order);	// number of gauss points used at this order

#if DIM==3
  VTKCellType getCellType() const;
#endif // DIM==3

  virtual const std::string *repr() const = 0; // id string for Python

  friend class ElementMapNodePositionIterator;
  friend class ElementFuncNodePositionIterator;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ElementLite knows about master elements, shape functions, and
// mapping from master space to real space.  It uses Coords instead of
// Nodes, and therefore doesn't know anything about degrees of freedom
// or equations.  It also doesn't assume the existence of a Skeleton
// or FEMesh.  It's used in cases in which it's necessary to use the
// finite element machinery to to integrals over regions which don't
// necessarily correspond to actual elements in the Mesh.

class ElementLite : public ElementBase {
private:
  std::vector<Coord> coords;
public:
  ElementLite(const MasterElement&, const std::vector<Coord>*);
  const std::string &classname() const;
  virtual Coord position(int) const;
  virtual const std::string *repr() const; // id string for Python
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class Element : public ElementBase {
private: 
  // Set of pointers to data objects.
  mutable std::vector<ElementData*> el_data;

  Element(const Element&);	      // prohibited
  Element &operator=(const Element&); // prohibited

protected: // Nodelist needs to be visible to interface elements.
  const std::vector<Node*> nodelist;

private:
  const Material *matl;
  int index_;
#if DIM==2
  std::vector<ElementCornerNodeIterator> *exterior_edges;
#endif // DIM==2

  // Elements have to know the SkeletonElements that created them, so
  // that when the SkeletonElement's material changes, the Element can
  // find out about it.  Since a SkeletonElement can create many
  // Elements, it's more efficient to store the SkeletonElement in the
  // Element than vice versa.
  CSkeletonElement * cskeleton_element;

  // // The edgeset allows elements to own the edges, which are created
  // // and manipulated in connection with boundary conditions.  A
  // // typical element will have an empty edgeset.  Elements with
  // // nontrivial boundaries will allocate enough space for all possible
  // // edges at the time that the first edge is requested through a call
  // // to getBndyEdge.  Space is allocated in "add_b_edge".
  // std::vector<BoundaryEdge*> edgeset;
  // std::vector<BoundaryFace*> faceset;
  

  friend class ElementNodeIterator;
  friend class ElementMapNodeIterator;
  friend class ElementFuncNodeIterator;

public:
  Element(CSkeletonElement *el, const MasterElement&, const std::vector<Node*>*,
	  const Material*);
  virtual ~Element();

  virtual const std::string &classname() const;

  CSkeletonElement * get_skeleton_element() const { return cskeleton_element; }
  const std::vector<Node*> & get_nodelist() const { return nodelist; }

  // getSegmentNode() is used only in ElementPtr.intersectPlane() in
  // element.spy.  It only needs to be defined for 3D elements.  TODO 3.1:
  // Fix the class hierarchy so this doesn't have to be here.
  Node *getSegmentNode(const FEMesh*, int segno, int nodeno) const;

  virtual const std::string *repr() const; // id string for Python

  const Material *material() const { return matl; }
  // Tell the Element that the Material may have changed.
  void refreshMaterial(const CSkeletonBase*);
  
  // Are all nodes of this element in the given subproblem?  This is
  // different from asking whether or not the element is in the
  // subproblem, since subproblem definitions may not apply to
  // interface elements.  This method is only used on interface
  // elements.
  bool allNodesAreInSubProblem(const CSubProblem*) const;

  int ndof() const;
  std::vector<int> localDoFmap() const;
  void localDoFs(const FEMesh*, DoubleVec&) const;

  // Compute this element's contribution to the global stiffness
  // matrix at the given time.  Redefined in InterfaceElement, to do
  // each "side" separately.
  void make_linear_system(const CSubProblem*, double time,
			  const CNonlinearSolver*,
			  LinearizedSystem &) const;

  // Post-equilibrium processing.
  void post_process(CSubProblem *) const;

  void set_index(int);
  const int &get_index() const;


  // Access to Nodes and ShapeFunctions is done through the
  // ElementNodeIterator classes.  Accessing ShapeFunctions via the
  // iterators ensures that the proper shape function will be selected
  // for non-isoparametric elements, where one node may be associated
  // with more than one shapefunction, the correct choice being
  // determined by whether the node is being used in its role as a
  // mapping node or an interpolation (func) node.
  ElementNodeIterator node_iterator() const;
  ElementMapNodeIterator mapnode_iterator() const;
  virtual ElementFuncNodeIterator* funcnode_iterator() const;
  ElementCornerNodeIterator cornernode_iterator() const;

  virtual Coord position(int) const;

  // Superconvergent patch recovery
  int nSCpoints() const;
  const MasterCoord &getMasterSCpoint(int i) const;

  // Functions for manipulating the element's data sets.  TODO OPT: As a
  // practical matter, in the actual property classes, you don't know
  // who else has put data into the element, so you end up retrieving
  // and deleting the data by name, rather than position.  This is
  // inefficient for a vector, but it's what we want to do, therefore
  // the ElementData* vector should be changed to a name-indexed map,
  // to preserve this API but increase the efficiency of the
  // name-based searches.  OR, the Property classes can remember the
  // index of their data, which is reasonable if all elements have the
  // same data sets.

  int appendData(ElementData *x) const;
  void setDataByName(ElementData *x) const;
  void setData(int i, ElementData *x) const;
  ElementData *getData(int i) const;
  int getIndexByName(const std::string &name) const;
  ElementData *getDataByName(const std::string &name) const;
  // Deletion functions remove the pointer from the array, but do NOT
  // delete the pointed-to object -- that's the caller's
  // responsibility.
  void delDataByName(const std::string &name) const;
  void delData(int i) const;
  void clearData() const; // Clears the whole structure.  Do not use.

  //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

  OutputValue outputField(const FEMesh*, const Field&, const MasterPosition&)
    const;

  std::vector<OutputValue> *outputFields(const FEMesh*, const Field&,
					 const std::vector<MasterCoord*>*)
    const;

  std::vector<OutputValue> *outputFields(const FEMesh*, const Field&,
					 const std::vector<MasterCoord>&)
    const;

  std::vector<OutputValue> *outputFieldDerivs(const FEMesh*, const Field&,
					      SpaceIndex*,
					      const std::vector<MasterCoord*>*)
    const;
  
  OutputValue outputFieldDeriv(const FEMesh*, const Field &, SpaceIndex *,
			       const MasterPosition &) const;

  // OutputValue outputFlux(const FEMesh*, const Flux&, const MasterPosition&)
  //   const;

  std::vector<OutputValue> *outputFluxes(const FEMesh*, const Flux &flux,
					 const std::vector<MasterCoord*>*)
    const;

  //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

//   // Wrappers for Material::begin_element and Material::end_element,
//   // to be called when doing material dependent computations outside
//   // of the make_stiffness machinery.
//   void begin_material_computation(FEMesh*) const;
//   void end_material_computation(FEMesh*) const;

#if DIM==2
  // Identify the edge between the two given nodes as an exterior edge.
  void set_exterior(const Node&, const Node&);

  // Are two master coordinates on the same exterior edge?  An
  // exterior edge is a geometrical boundary of the system (as opposed
  // to a boundary where boundary conditions apply).
  bool exterior(const MasterCoord &, const MasterCoord&) const;
  void dump_exterior() const; // debugging
#endif  // DIM==2

  //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

  // BoundaryEdge machinery, for boundary conditions.

  // // Retrieve an edge from the edgelist if present, or create
  // // it if not.  This is the "universal" exterior interface that
  // // other programs should use. 
  // BoundaryEdge *getBndyEdge(const FuncNode*, const FuncNode*);


  // void add_b_edge(BoundaryEdge*);
  // BoundaryEdge *find_b_edge(const FuncNode*, const FuncNode*) const;

  // // Create a BoundaryEdge object joining the given nodes.  This
  // // function is implemented by the concrete element class,
  // // because it can depend on node-ordering and spatial 
  // // configuration information which isn't known until that level.
  // BoundaryEdge *newBndyEdge(const FuncNode*, const FuncNode*) const;

// #if DIM==3
//   // Similiar to the above but for faces
//   BoundaryFace *getBndyFace(const FuncNode*, const FuncNode*, const FuncNode*);
//   void add_b_face(BoundaryFace*);
//   BoundaryFace *find_b_face(const FuncNode*, const FuncNode*, const FuncNode*)
//     const;
//   BoundaryFace *newBndyFace(const FuncNode*, const FuncNode*, const FuncNode*)
//     const;
// #endif	// DIM==3

  //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

  // A routine which returns Edge objects corresponding to all of the
  // edges of the element -- used to draw the element.
#if DIM==2
  std::vector<Edge*> *perimeter() const;
#endif	// DIM==2
#if DIM==3
  vtkSmartPointer<vtkIdList> getPointIds() const;
  void drawGridCell(vtkSmartPointer<GridSource>, SimpleCellLayer*) const;
#endif	// DIM==3



  friend std::ostream &operator<<(std::ostream&, const Element&);

  Node* getCornerNode(int i) const;
  void setMaterial(const Material* pMat){matl=pMat;}

  //These definitions won't be (shouldn't be) used.
  virtual const std::string &name() const {
    static const std::string _ename = "Element";
    return _ename; 
  }
  virtual std::vector<std::string>* namelist() const { return 0; }
};  // end class Element

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FaceBoundaryElement: public Element {
protected:
  // neighboring bulk elements
  const Element *front_;
  const Element *back_;
public:
  FaceBoundaryElement(const MasterElement&, const std::vector<Node*>*);
  const std::string &classname() const;
  void setFrontBulk(const Element *el) { front_ = el; }
  const Element *getFrontBulk() const;
  void setBackBulk(const Element *el) { back_ = el; }
  const Element *getBackBulk() const;
};

class EdgeBoundaryElement: public Element {
public:
  EdgeBoundaryElement(const MasterElement&, const std::vector<Node*>*);
  const std::string &classname() const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef INTERFACEELEMENTS

// InterfaceElements have split nodes, and add storage in the subclass
// for a second list of nodes -- by arbitrary convention, these extra
// nodes are the "left side" nodes, and the ones stored in the base
// class are the "right side" nodes.  The iterators and some node
// access functions use the left-right nomenclature.  The constructor
// guarantees that these are assigned correctly.

// TODO MER: This has to be redone^H^H^H^H^H^HDdeleted for 3D, where
// these are face elements.

enum Sidedness { LEFT, RIGHT }; // Used for the internal element state.

class InterfaceElement: public Element
{
private:
  const std::vector<Node*> nodelist2;  // Right-side nodes.
  bool left_nodes_in_interface_order;
  bool right_nodes_in_interface_order;
  // cskeleton_element2 is commented out because it's not used yet.
  // When the interface elements are fully implemented, presumably it
  // will be used.
  //CSkeletonElement * cskeleton_element2;
  int _segmentordernumber;
  std::vector<std::string> _interfacenames;
  mutable Sidedness current_side;  
public:
  virtual const std::string &name() const; //retrieve the last name in the list
  virtual std::vector<std::string>* namelist() const;
  const std::vector<Node*> & get_leftnodelist() const { return nodelist;}
  const std::vector<Node*> & get_rightnodelist() const { return nodelist2;}
  InterfaceElement(CSkeletonElement *leftskelel, CSkeletonElement *rightskelel,
		   int segmentordernumber,
		   const MasterElement&,
		   const std::vector<Node*>*, const std::vector<Node*>*,
		   bool leftnodes_inorder, bool rightnodes_inorder,
		   const Material*,
		   const std::vector<std::string>* interfacenames);
  virtual ~InterfaceElement();
  bool isSubProblemInterfaceElement(const CSubProblem*) const;

  virtual void make_linear_system(const CSubProblem* const,
				  double time,
				  const CNonlinearSolver *nlsolver,
				  LinearizedSystem &system) const;
  // Tell the Element that the Material may have changed.
  //  void refreshInterfaceMaterial(const CSkeletonBase*);

  // Tell the Element that the name of one of the boundaries that it's
  // on has changed.
  void rename(const std::string& oldname, const std::string& newname);

  // "Span" is a pair of nodes, the start and end, in interface order.
  // It's used by some properties to compute the element normal.
  std::vector<const Node*> get_left_span() const;
  std::vector<const Node*> get_right_span() const;

  Sidedness side() const { return current_side; }

  virtual ElementFuncNodeIterator* funcnode_iterator() const;

  virtual double jacobian(SpaceIndex i, 
			  SpaceIndex j, const GaussPoint &g) const;
  virtual double jacobian(SpaceIndex i,
			  SpaceIndex j, const MasterCoord &mc) const;

  // virtual double det_jacobian(const GaussPoint &) const;
  // virtual double det_jacobian(const MasterCoord &) const;

  friend std::ostream &operator<<(std::ostream&, const InterfaceElement&);
};  // end class InterfaceElement

#endif // INTERFACEELEMENTS

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CoordElementData : public ElementData {
private:
  const Coord coord_;
  static std::string class_;
  static std::string module_;
public:
  CoordElementData(const std::string &nm, 
		   const Coord c) : ElementData(nm),coord_(c) 
  {}
  virtual ~CoordElementData() {}
  virtual const std::string &classname() const { return class_; }
  virtual const std::string &modulename() const { return module_; }
  const Coord &coord() const { return coord_; }
};

#if DIM==3
Coord findNormal(const ElementBase*, const MasterPosition&);
std::vector<OutputValue> *findNormals(const ElementBase*,
				      const std::vector<MasterCoord*>*);
#endif // DIM==3

#endif	// ELEMENT_H
