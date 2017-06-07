// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include "common/IO/oofcerr.h"
#include "common/switchboard.h"
#include "common/tostring.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/masterelement.h"
#include "engine/ooferror.h"
#include "engine/shapefunction.h"
#include <math.h>
#include <iostream>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MasterElementDict &masterElementDict() {
  static MasterElementDict the_dict;
  return the_dict;
}

std::vector<std::string> *getMasterElementNames() {
  std::vector<std::string> *names = new std::vector<std::string>;
  for(MasterElementDict::const_iterator i=masterElementDict().begin();
      i!=masterElementDict().end(); ++i)
    {
      names->push_back((*i).first);
    }
  return names;
}

MasterElement *getMasterElementByName(const std::string &name) {
  MasterElement *el = masterElementDict()[name];
  return el;
}

MasterElement *getMasterElementByShape(const ElementShape *shape,
				       int funorder, int maporder)
{
  for(MasterElementDict::const_iterator i=masterElementDict().begin();
      i!=masterElementDict().end(); ++i)
    {
      MasterElement *mel = (*i).second;
      if(mel->shape() == shape && mel->fun_order() == funorder
	 && mel->map_order() == maporder)
	{
	  return mel;
	}
    }
  throw ErrProgrammingError("No such master element: " + shape->name()
			    + " " + to_string(funorder) + " " +
			    to_string(maporder),
			    __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MasterElement::MasterElement(const std::string &nm, const std::string &desc,
			     const ElementShape *shape,
			     int nn, int nsc)
  : name_(nm), desc_(desc), shape_(shape)
{
  protonodes.reserve(nn);
  sc_points.reserve(nsc);
  edges.reserve(shape_->nedges());
  for(int i=0; i<shape_->nedges(); i++)
    edges.push_back(new MasterEdge);
  masterElementDict()[nm] = this;
  switchboard_notify("new master element");
}

MasterElement::~MasterElement() {
  for(std::vector<const ProtoNode*>::size_type i=0; i<protonodes.size(); i++) {
    delete protonodes[i];
  }
  for(std::vector<const MasterEdge*>::size_type i=0; i<edges.size(); i++) {
    delete edges[i];
  }
}

std::ostream &operator<<(std::ostream &os, const MasterElement &me) {
  os << me.name_;
  return os;
}

int MasterElement::nnodes() const {
  return protonodes.size();
}

int MasterElement::nmapnodes() const {
  return mapnodes.size();
}

int MasterElement::nfuncnodes() const {
  return funcnodes.size();
}

int MasterElement::nexteriorfuncnodes() const {
  return exteriorfuncnodes.size();
}

// Count the number of non-corner nodes on edges that are for mapping only.
int MasterElement::nedgemapnodes_only() const {
  int n = 0;
  for(const ProtoNode *pn : protonodes) {
    if(pn->mapping() && !pn->func() && pn->nedges() == 1)
      n++;
  }
  return n;
}

// Count the number of non-edge nodes on faces that are for mapping only.
int MasterElement::nfacemapnodes_only() const {
  int n = 0;
  for(const ProtoNode *pn : protonodes) {
    if(pn->mapping() && !pn->func() && pn->nedges() == 0 && pn->nfaces() == 1)
      n++;
  }
  return n;
}

// Count the number of interior nodes that are for mapping only
int MasterElement::ninteriormapnodes_only() const {
  int n = 0;
  for(const ProtoNode *pn : protonodes) {
    if(pn->mapping() && !pn->func() && pn->nedges() == 0 && pn->nfaces() == 0)
      n++;
  }
  return n;
}

int MasterElement::nfaces() const {
  return shape_->nfaces();
}

int MasterElement::nedges() const {
  return shape_->nedges();
}

ProtoNode *MasterElement::addProtoNode(const MasterCoord &mc) {
  ProtoNode *pn = new ProtoNode(*this, mc);
  pn->index_ = protonodes.size();
  protonodes.push_back(pn);
  return pn;
}

const ProtoNode *MasterElement::protonode(int n) const {
  return protonodes[n];
}

void MasterElement::addSCpoint(const MasterCoord &mc) {
  sc_points.push_back(mc);
}

void ProtoNode::set_mapping() {	// called to indicate that a P.N. is a map node
  mapping_ = true;
  element.mapnodes.push_back(index_);
}

void ProtoNode::set_func() {
  func_ = true;
  element.funcnodes.push_back(index_);
}

void ProtoNode::set_corner() {
  corner_ = true;
  element.cornernodes.push_back(index_);
}

std::ostream &operator<<(std::ostream &os, const ProtoNode &pn) {
  return os << "ProtoNode" << pn.pos;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The arguments for on_edge and on_face are the vtk indices for the
// tet edges and faces that the ProtoNode is on.

void ProtoNode::on_edge(int edgeno) {
  edgeindex.push_back(edgeno);
  element.edges[edgeno]->addNode(this);
  // Put this node in its MasterElement's exterior lists, if it's not
  // already there.  Checking this way relies on not intermingling
  // on_edge calls for one ProtoNode with calls for another one.
  if(func_)
    if(element.exteriorfuncnodes.empty() ||
       *element.exteriorfuncnodes.rbegin() != index_)
      element.exteriorfuncnodes.push_back(index_);
}

void MasterEdge::addNode(const ProtoNode *pn) {

  // First, keep track of func-ness of nodes, so that func_size()
  // will work.
  if (pn->func()) {
    funcsize_++;
  }

  if(nlist.empty()) {
    nlist.push_back(pn);
    return;
  }
  // Since ProtoNodes on the edges are added to the MasterElement in
  // counterclockwise order, because the indices are assigned as
  // they're added, and because the MasterEdge lists nodes in
  // counterclockwise order, the nodes go into the MasterEdge's list
  // at the end.  The exception to this is when the ProtoNode creation
  // process wraps around.  Then the very first node created belongs
  // at the *end* of the list, and all of the other nodes go just
  // before it.
  const ProtoNode *lastnode = nlist.back();
  if(lastnode->index() == pn->index()-1) {
    nlist.push_back(pn);
  }
  else {
    // insert at the second to last spot
    nlist.insert(--nlist.end(), pn);
  }
  return;
}

const MasterEdge *MasterElement::masteredge(const ElementCornerNodeIterator &n0,
					    const ElementCornerNodeIterator &n1)
  const
{
  const ProtoNode *pn0 = n0.protonode();
  const ProtoNode *pn1 = n1.protonode();
  for(std::vector<MasterEdge*>::size_type i=0; i<edges.size(); i++) {
    std::list<const ProtoNode*> &nlist = edges[i]->nlist;
    if((nlist.front() == pn0 && nlist.back() == pn1)
       || (nlist.front() == pn1 && nlist.back() == pn0)) {
      return edges[i];
    }
  }
  throw ErrUserError("Edge not found in master element");
}

void ProtoNode::on_face(int faceno) {
  faceindex.push_back(faceno);
  element.faces[faceno]->addNode(this);
  // Put this node in its MasterElement's exterior lists, if it's not
  // already there.  Checking this way relies on not intermingling
  // on_face calls for one ProtoNode with calls for another one.

  // TODO: This was commented out.  Why?
  if(func_)
    if(element.exteriorfuncnodes.empty() ||
       *element.exteriorfuncnodes.rbegin() != index_)
      element.exteriorfuncnodes.push_back(index_);
}

void MasterFace::addNode(const ProtoNode *pn) {
  if (pn->func()) {
    funcsize_++;
  }
  nvector.push_back(pn);
  return;
}

const MasterFace *MasterElement3D::masterface(
				      const ElementCornerNodeIterator &n0,
				      const ElementCornerNodeIterator &n1,
				      const ElementCornerNodeIterator &n2)
  const
{
  const ProtoNode *pn0 = n0.protonode();
  const ProtoNode *pn1 = n1.protonode();
  const ProtoNode *pn2 = n2.protonode();

  for(std::vector<MasterFace*>::size_type i=0; i<faces.size(); i++) {
    std::vector<const ProtoNode*> &nvector = faces[i]->nvector;
    // find the first match
    for(std::vector<const ProtoNode*>::size_type j=0; j<nvector.size(); ++j) {
      if(nvector[j] == pn0 &&
	 ((nvector[(j+1)%3] == pn1 && nvector[(j+2)%3] == pn2) ||
	  (nvector[(j+1)%3] == pn2 && nvector[(j+2)%3] == pn1)))
	{
	  return faces[i];
	}
    }
  }
  throw ErrUserError("Face not found in master element");
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int integration_reduction = 0;

int MasterElement::ngauss(int order) const {
  return gptable(order).size();
}

const GaussPtTable &MasterElement::gptable(int i) const {
  if(i >= int(gptable_vec().size()))
    throw ErrResourceShortage(
	  "GaussPtTable: No table for order of integration = " + to_string(i));
  i -= integration_reduction;
  if(i < 0) i = 0;
  return gptable_vec()[i];
}

int MasterElement::ngauss_sets() const {
  return gptable_vec().size();
}

#define max2(a, b) ((a) > (b) ? (a) : (b))
#define max3(a, b, c) ((a) > (b) ? max2((a), (c)) : max2((b), (c)))
#define max4(a, b, c, d) ((a) > (b) ? max3((a), (c), (d)) : max3((b), (c), (d)))

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const GaussPtTable &TriangularMaster::gausspointtable(int deg) const {
  return gptable(deg);
}

const std::vector<GaussPtTable> &TriangularMaster::gptable_vec() const {
  static std::vector<GaussPtTable> table;
  static bool set = 0;
  if(!set) {
    set = 1;

    // Gauss points for a triangle are from "High Degree Efficient
    // Symmetrical Gaussian Quadrature Rules for the Triangle",
    // D.A. Dunavant, International Journal for Numerical Methods in
    // Engineering, vol 21, 1129, (1985).  The weights given there
    // don't include the factor of the area of the triangle, so the
    // weights used here all have an additional factor of 0.5.

     // order = 0, npts = 1
    table.push_back(GaussPtTable(0, 1));
    table[0].addpoint(masterCoord2D(1./3., 1./3.), 0.5);

     // order = 1, npts = 1
    table.push_back(GaussPtTable(1, 1));
    table[1].addpoint(masterCoord2D(1./3., 1./3.), 0.5);

     // order = 2, npts = 3
    table.push_back(GaussPtTable(2, 3));
    table[2].addpoint(masterCoord2D(2./3., 1./6.), 1./6.);
    table[2].addpoint(masterCoord2D(1./6., 2./3.), 1./6.);
    table[2].addpoint(masterCoord2D(1./6., 1./6.), 1./6.);

    // order = 3, npts = 4
    table.push_back(GaussPtTable(3, 4));
    table[3].addpoint(masterCoord2D(1./3., 1./3.), -0.5*0.5625);
    table[3].addpoint(masterCoord2D(0.6, 0.2), 0.5*25./48.);
    table[3].addpoint(masterCoord2D(0.2, 0.6), 0.5*25./48.);
    table[3].addpoint(masterCoord2D(0.2, 0.2), 0.5*25./48.);

    // order = 4, npts = 6
    table.push_back(GaussPtTable(4, 6));
    table[4].addpoint(masterCoord2D(0.108103018168070, 0.445948490915965),
		      0.5*0.223381589678011);
    table[4].addpoint(masterCoord2D(0.445948490915965, 0.108103018168070),
		      0.5*0.223381589678011);
    table[4].addpoint(masterCoord2D(0.445948490915965, 0.445948490915965),
		      0.5*0.223381589678011);
    table[4].addpoint(masterCoord2D(0.816847572980459, 0.091576213509771),
		      0.5*0.109951743655322);
    table[4].addpoint(masterCoord2D(0.091576213509771, 0.816847572980459),
		      0.5*0.109951743655322);
    table[4].addpoint(masterCoord2D(0.091576213509771, 0.091576213509771),
		      0.5*0.109951743655322);
  }
  return table;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const GaussPtTable &QuadrilateralMaster::gausspointtable(int deg) const {
  // 1-D Integration using n gauss points correctly integrates
  // polynomials up to degree 2*n-1.
  int ng = int(ceil(0.5*(deg + 1))); // number of gauss points needed on a side
  return gptable(ng);
}

const std::vector<GaussPtTable> &QuadrilateralMaster::gptable_vec() const {
  static std::vector<GaussPtTable> table;
  static bool set = 0;
  if(!set) {
    set = 1;

    // Use one dimensional integration rules to construct two
    // dimensional rules.

    for(int ord=0; ord<GaussPtTable1::n_orders(); ord++) {

      int npts1 = GaussPtTable1::npts(ord);
      table.push_back(GaussPtTable(ord, npts1*npts1));

      for(GaussPoint1 gx(ord, GaussPoint1::Mmin, GaussPoint1::Mmax);
	  !gx.end(); ++gx)
	for(GaussPoint1 gy(ord, GaussPoint1::Mmin, GaussPoint1::Mmax);
	    !gy.end(); ++gy)
	  table[ord].addpoint(masterCoord2D(gx.mposition(), gy.mposition()),
			      gx.weight()*gy.weight());

    }
  }

  return table;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const GaussPtTable &MasterElement1D::gausspointtable(int deg) const {
  // 1-D Integration using n gauss points correctly integrates
  // polynomials up to degree 2*n-1.
  int ng = int(ceil(0.5*(deg + 1))); // number of gauss points needed
  return gptable(ng);
}

const std::vector<GaussPtTable> &MasterElement1D::gptable_vec() const {
  static std::vector<GaussPtTable> table;
  static bool set = false;
  if(!set) {
    set = true;

    // This routine mostly just copies numbers from one table to
    // another, but the equivalent routines for 2 and 3 dimensional
    // elements do more work.

    for(int ord=0; ord<GaussPtTable1::n_orders(); ord++) {

      int npts1 = GaussPtTable1::npts(ord);
      table.push_back(GaussPtTable(ord, npts1));

      for(GaussPoint1 gx(ord, GaussPoint1::Mmin, GaussPoint1::Mmax);
	  !gx.end(); ++gx)
	table[ord].addpoint(masterCoord1D(gx.mposition()),
			    gx.weight());

    }
  }
  return table;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MasterCoord TriangularMaster::center() const {
  static double third = 1./3.;
  return masterCoord2D(third, third);
}

MasterCoord QuadrilateralMaster::center() const {
  return masterCoord2D(0.,0.);
}

MasterCoord MasterElement1D::center() const {
  return masterCoord1D(0.);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility functions used by MasterElement::build().

template <class TYPE>
TYPE MasterElement::interpolate(const std::vector<TYPE> &cval,
				const MasterCoord &x)
  const
{
  TYPE interpolant;
  for(unsigned int i=0; i<nmapnodes(); i++) {
    interpolant = interpolant + mapfunction->value(i,x)*cval[i];
  }
  return interpolant;
}

static Node *findClosestNode(std::vector<Node*> &nodes, Coord3D pos) {
  double mindist = std::numeric_limits<double>::max();
  Node *closest = nullptr;
  for(Node *node : nodes) {
    double d2 = norm2(node->position() - pos);
    if(d2 < mindist) {
      closest = node;
      mindist = d2;
    }
  }
  assert(closest != nullptr);
  return closest;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// build() creates a real mesh element at the location of the given
// Skeleton element, creating new Nodes if necessary.

Element *MasterElement::build(CSkeletonElement *el,
			      const CSkeleton *skel, FEMesh *femesh,
			      const Material *mat,
			      SkelElNodeMap &edgeNodeMap,
			      SkelElNodeMap &faceNodeMap)
  const
{
  // nodes stores the Nodes that will be passed to the Element
  // constructor.  They correspond 1 to 1 with the vector of
  // ProtoNodes in the MasterElement.
  std::vector<Node*> nodes(nnodes(), nullptr);

  // To compute the positions of new, non-corner Nodes, we need to
  // know the corners of the tet.

  // TODO: If we ever have higher order *skeleton* elements, ie,
  // skeleton elements with curved sides, we'll have to include all of
  // map nodes here, not just the corners.
  std::vector<Coord3D> corners;	// for interpolation of intermediate node pos.
  if(nnodes() > 4) {
    corners.reserve(ncorners());
    for(int i=0; i<ncorners(); i++) {
      corners.push_back(el->getNode(i)->position());
    }
  }

  // The input maps edgeNodeMap and faceNodeMap store the nodes that
  // have been created on the edges and faces of other elements, and
  // that might be reused in this one.  If an edge or face of this
  // element isn't found in the maps, it's added to the maps and the
  // new nodes are stored.  But there may be more than one new node on
  // a face or edge, so we don't add entries to edgeNodeMap or
  // faceNodeMap until we're done (because we're using the existence
  // of entries in the maps to determine if the nodes have to be
  // created).  Instead, new nodes are stored in newEdgeNodes and
  // newFaceNodes, which are merged with edgeNodeMap and faceNodeMap
  // after all nodes have been created.
  SkelElNodeMap newEdgeNodes;
  SkelElNodeMap newFaceNodes;

  // Loop over ProtoNodes and create real ones, if necessary.
  
  for(unsigned int pnidx=0; pnidx<nnodes(); pnidx++) {
    const ProtoNode *pn = protonodes[pnidx];
    // What we do depends on what kind of node this is.
    // TODO: This big if/then could be simpler if we used different
    // subclasses of ProtoNode for corner, edge, face, and interior
    // nodes.
    if(pn->corner()) {
      // Corner nodes have already been created in
      // CSkeleton::populate_femesh().
      // Find out which corner this is:
      for(unsigned int c=0; c<ncorners(); c++) {
	// It is assumed that the calls to ProtoNode::set_corner have
	// been done in the order determined by the vtk ordering of
	// tet corners, so that the corner i of the SkeletonElement
	// corresponds to the i^th corner ProtoNode.
	if(cornernodes[c] == pnidx) {
	  nodes[pnidx] = femesh->getFuncNode(el->getNode(c)->getIndex());
	  break;
	}
      }
    } // end if ProtoNode is at a corner

    else if(pn->nedges() > 0) {
      // ProtoNode is on an edge (but not a corner)
      assert(pn->nedges() == 1);
      // What edge is it on?
      int edgeNo = pn->edgeindex[0];
      Coord3D pos = interpolate(corners, pn->mastercoord());
      // Has the edge been seen before?
      CSkeletonNode *n0 = el->getSegmentNode(edgeNo, 0);
      CSkeletonNode *n1 = el->getSegmentNode(edgeNo, 1);
      CSkeletonMultiNodeKey segkey(n0, n1);
      SkelElNodeMap::iterator it = edgeNodeMap.find(segkey);
      if(it == edgeNodeMap.end()) {
	// The edge hasn't been seen before.  Create a new node.
	Node *newNode = femesh->newFuncNode(pos);
	nodes[pnidx] = newNode;
	// If the edge is already in newEdgeNodes, add the node to it.
	// Otherwise, add the edge to newEdgeNodes and add the node to it.
	SkelElNodeMap::iterator eit = newEdgeNodes.find(segkey);
	if(eit == newEdgeNodes.end()) {
	  newEdgeNodes.emplace(
		       std::make_pair(segkey, std::vector<Node*>(1, newNode)));
	}
	else {
	  eit->second.push_back(newNode);
	}
      }	// end if edge is new.
      else {
	// The edge has already been seen.  Re-use the nodes on it.
	// TODO: Is searching for the closest node too inefficient?
	// The list is probably short.  We can't just look for a node
	// with the exact same position, because round off error in
	// interpolate() may give different results in different
	// elements for the positions of shared nodes.
	nodes[pnidx] = findClosestNode(it->second, pos);
      }	// end if edge has already been seen.
      
    } // end if ProtoNode is on an edge

    else if(pn->nfaces() > 0) {
      // ProtoNode is on a face (but not an edge or corner).
      assert(pn->nedges() == 0 && pn->nfaces() == 1);
      int faceNo = pn->faceindex[0];
      Coord3D pos = interpolate(corners, pn->mastercoord());
      // Has the face been seen before?
      CSkeletonNode *n0 = el->getFaceNode(faceNo, 0);
      CSkeletonNode *n1 = el->getFaceNode(faceNo, 1);
      CSkeletonNode *n2 = el->getFaceNode(faceNo, 2);
      CSkeletonMultiNodeKey facekey(n0, n1, n2);
      SkelElNodeMap::iterator it = faceNodeMap.find(facekey);
      if(it == faceNodeMap.end()) {
	// The face hasn't been seen before.  Create a new node.
	Node *newNode = femesh->newFuncNode(pos);
	nodes[pnidx] = newNode;
	// Add the node to newFaceNodes.
	SkelElNodeMap::iterator fit = newFaceNodes.find(facekey);
	if(fit == newFaceNodes.end()) {
	  newFaceNodes.emplace(
		       std::make_pair(facekey, std::vector<Node*>(1, newNode)));
	}
	else {
	  fit->second.push_back(newNode);
	}
      }	// end if face is new
      else {
	nodes[pnidx] = findClosestNode(it->second, pos);
      }	// end if face has already been seen.

    } // end if ProtoNode is on a face

    else {
      // ProtoNode is interior.  It always needs to be created.
      assert(pn->nedges() == 0 && pn->nfaces() == 0);
      Coord3D pos = interpolate(corners, pn->mastercoord());
      nodes[pnidx] = femesh->newFuncNode(pos);

    } // end if ProtoNode is interior
    
  } // end loop over ProtoNodes

  // Merge the new nodes into edgeNodeMap and faceNodeMap so they can
  // be used by future elements.
  edgeNodeMap.insert(newEdgeNodes.begin(), newEdgeNodes.end());
  faceNodeMap.insert(newFaceNodes.begin(), newFaceNodes.end());

  // Element constructor uses std::move on nodes.
  return new Element(el, *this, nodes, mat);
}

FaceBoundaryElement *MasterElement::buildFaceBoundary(
					      const std::vector<Node*> &nodes)
  const
{
  return new FaceBoundaryElement(*this, nodes);
}

EdgeBoundaryElement *MasterElement::buildEdgeBoundary(
					      const std::vector<Node*> &nodes)
const
{
  return new EdgeBoundaryElement(*this, nodes);
}

ElementLite *MasterElement::buildLite(const std::vector<Coord> *nodes) 
  const
{
  return new ElementLite(*this, nodes);
}

TetrahedralMaster::TetrahedralMaster(const std::string &name,
				     const std::string &desc,
				     int nnodes, int nsc)
  : MasterElement3D(name, desc, getShape("Tetrahedron"), nnodes, nsc) 
{
  faces.reserve(4);
  // MasterEdges are made in the MasterElement constructor.
  // TODO 3.1: MasterFaces should be made in MasterElement3D constructor.
  for(int i=0; i<4; ++i)
    faces.push_back(new MasterFace);
  switchboard_notify("new master element");
}

TetrahedralMaster::~TetrahedralMaster() {
  for(std::vector<const MasterFace*>::size_type i=0; i<faces.size(); i++) {
    delete faces[i];
  }
}

const GaussPtTable &TetrahedralMaster::gausspointtable(int deg) const {
  return gptable(deg);
}

#define sixth 1./6.
#define third 1./3.
#define fourth 0.25
#define c14   0.585410196624969
#define c15   0.138196601125011

const std::vector<GaussPtTable> &TetrahedralMaster::gptable_vec() const {
  static std::vector<GaussPtTable> table;
  static bool set = 0;

  if(!set) {
    set = 1;
     // order = 0, npts = 1
    table.push_back(GaussPtTable(0, 1));
    table[0].addpoint(MasterCoord(fourth, fourth, fourth), sixth);

     // order = 1, npts = 1
    table.push_back(GaussPtTable(1, 1));
    table[1].addpoint(MasterCoord(fourth, fourth, fourth), sixth);

     // order = 2, npts = 4
    table.push_back(GaussPtTable(2, 4));
    table[2].addpoint(MasterCoord(c15, c15, c15), 1./24.);
    table[2].addpoint(MasterCoord(c15, c14, c15), 1./24.);
    table[2].addpoint(MasterCoord(c14, c15, c15), 1./24.);
    table[2].addpoint(MasterCoord(c15, c15, c14), 1./24.);

  }

  return table;
}

MasterCoord TetrahedralMaster::center() const {
  return MasterCoord(fourth, fourth, fourth);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &MasterElement::modulename() const {
  static std::string nm("ooflib.SWIG.engine.masterelement");
  return nm;
}

const std::string &MasterElement1D::classname() const {
  static std::string nm("MasterElement1D");
  return nm;
}

const std::string &TriangularMaster::classname() const {
  static std::string nm("TriangularMaster");
  return nm;
}

const std::string &QuadrilateralMaster::classname() const {
  static std::string nm("QuadrilateralMaster");
  return nm;
}

const std::string &TetrahedralMaster::classname() const {
  static std::string nm("TetrahedralMaster");
  return nm;
}
