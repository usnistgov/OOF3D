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
#include "common/printvec.h"
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
  if (pn->func()) {
    funcsize_++;
  }
  nlist.push_back(pn);
  return;
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int integration_reduction = 0;

int MasterElement::ngauss(int order) const {
  return gptable(order).size();
}

const GaussPtTable &MasterElement::gptable(int i) const {
  if(i >= int(gptable_vec().size())) {
    oofcerr << "MasterElement::gptable: i=" << i << " size=" << gptable_vec().size() << std::endl;
    throw ErrResourceShortage(
	  "GaussPtTable: No table for order of integration = "
	  + to_string(i) + " in element " + name());
      ;
  }
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

// Routines for adding symmetrically placed points to Gauss point
// tables for the triangle.  In a symmetric quadrature rule, If a
// point has barycentric coordinates (r,s,t), with r+s+t=1, then any
// permutation of (r,s,t) is also a Gauss point with the same weight.
// The master space reference element is x>=0, y>=0, x+y<=1, and the
// barycentric coords of (x,y) are just (x,y,1-x-y).  Therefore, the
// actual coordinates of a barycentric point (r,s,t) are just (r,s).
// This makes it easy to find the symmetric points.

static void addPoints21(GaussPtTable &tbl, double r, double w) {
  // Barycentric coords are permutations of (r, r, 1-2r)
  double s = 1. - 2.*r;
  tbl.addpoint(masterCoord2D(r, r), w);
  tbl.addpoint(masterCoord2D(r, s), w);
  tbl.addpoint(masterCoord2D(s, r), w);
}

static void addPoints111(GaussPtTable &tbl, double r, double s, double w) {
  // Barycentric coords are permutations of (r, s, 1-r-s)
  double t = 1. - r - s;
  tbl.addpoint(masterCoord2D(r, s), w);
  tbl.addpoint(masterCoord2D(s, r), w);
  tbl.addpoint(masterCoord2D(r, t), w);
  tbl.addpoint(masterCoord2D(t, r), w);
  tbl.addpoint(masterCoord2D(s, t), w);
  tbl.addpoint(masterCoord2D(t, s), w);
}

const GaussPtTable &TriangularMaster::gausspointtable(int deg) const {
  return gptable(deg);
}

const std::vector<GaussPtTable> &TriangularMaster::gptable_vec() const {
  static std::vector<GaussPtTable> table;
  static bool set = 0;
  if(!set) {
    set = 1;

    // Gauss points for a triangle and tetrahedron are from A SET OF
    // SYMMETRIC QUADRATURE RULES ON TRIANGLES AND TETRAHEDRA, Linbo
    // Zhang, Tao Cui and Hui Liu, Journal of Computational
    // Mathematics, Vol.27, No.1, 2009, 89–96.  The numbers were
    // copied out of the source code file src/quad.c from
    // http://lsec.cc.ac.cn/phg/download/phg-0.9.3-20170615.tar.bz2.

    // The weights given there
    // don't include the factor of the area of the triangle, so the
    // weights used here all have an additional factor of 0.5.  It's
    // (mostly) written explicitly for easier comparison to the source
    // text.

    // Previously we had used "High Degree Efficient Symmetrical
    // Gaussian Quadrature Rules for the Triangle", D.A. Dunavant,
    // International Journal for Numerical Methods in Engineering, vol
    // 21, 1129, (1985), but Zhang et al has more values.

     // order = 0, npts = 1
    table.emplace_back(0, 1);
    table.back().addpoint(masterCoord2D(1./3., 1./3.), 0.5);

     // order = 1, npts = 1
    table.emplace_back(1, 1);
    table.back().addpoint(masterCoord2D(1./3., 1./3.), 0.5);

     // order = 2, npts = 3: Zhang QUAD_2D_P2_
    table.emplace_back(2, 3);
    addPoints21(table.back(), 1./6., (1/3.)/2.);

    // order = 3, npts = 6
    table.emplace_back(3, 6);
    addPoints21(table.back(),
		.16288285039589191090016180418490635,
		.28114980244097964825351432270207695/2.);
    addPoints21(table.back(),
		.47791988356756370000000000000000000,
		.05218353089235368507981901063125638/2.);
    
    //* This version (from Dunavant?) has one negative weight but
    //* fewer points.
    // table.push_back(GaussPtTable(3, 4));
    // table[3].addpoint(masterCoord2D(1./3., 1./3.), -0.5*0.5625);
    // table[3].addpoint(masterCoord2D(0.6, 0.2), 0.5*25./48.);
    // table[3].addpoint(masterCoord2D(0.2, 0.6), 0.5*25./48.);
    // table[3].addpoint(masterCoord2D(0.2, 0.2), 0.5*25./48.);

    // order = 4, npts = 6
    table.emplace_back(4, 6);
    addPoints21(table.back(),
		.44594849091596488631832925388305199,
		.22338158967801146569500700843312280/2.);
    addPoints21(table.back(),
		.09157621350977074345957146340220151,
		.10995174365532186763832632490021053/2.);
    
    // order = 5, npts = 7
    table.emplace_back(5, 7);
    addPoints21(table.back(),
		(6. - sqrt(15.))/21,
		(155. - sqrt(15.))/1200./2.);
    addPoints21(table.back(),
		(6 + sqrt(15.))/21,
		(155 + sqrt(15.))/1200./2.);
    table.back().addpoint(masterCoord2D(1./3., 1./3.), 9./40./2.);

    // order = 6, npts = 12
    table.emplace_back(6, 12);
    addPoints21(table.back(),
		.06308901449150222834033160287081916,
		.05084490637020681692093680910686898/2.);
    addPoints21(table.back(),
		.24928674517091042129163855310701908,
		.11678627572637936602528961138557944/2.);
    addPoints111(table.back(),
		 .05314504984481694735324967163139815,
		 .31035245103378440541660773395655215,
		 .08285107561837357519355345642044245/2.);

    // order = 7, npts = 15
    table.emplace_back(7, 15);
    addPoints21(table.back(),
		.02826392415607634022359600691324002,
		.01353386251566556156682309245259393/2.);
    addPoints21(table.back(),
		.47431132326722257527522522793181654,
		.07895125443201098137652145029770332/2.);
    addPoints21(table.back(),
		.24114332584984881025414351267036207,
		.12860792781890607455665553308952344/2.);
    addPoints111(table.back(),
		 .76122274802452380000000000000000000,
		 .04627087779880891064092559391702049,
		 .05612014428337535791666662874675632/2.);
    
    // order = 8, npts = 16
    table.emplace_back(8, 16);
    table.back().addpoint(masterCoord2D(1./3., 1./3.),
			  .14431560767778716825109111048906462/2.);
    addPoints21(table.back(),
		.17056930775176020662229350149146450,
		.10321737053471825028179155029212903/2.);
    addPoints21(table.back(),
		.05054722831703097545842355059659895,
		.03245849762319808031092592834178060/2.);
    addPoints21(table.back(),
		.45929258829272315602881551449416932,
		.09509163426728462479389610438858432/2.);
    addPoints111(table.back(),
		 .26311282963463811342178578628464359,
		 .00839477740995760533721383453929445,
		 .02723031417443499426484469007390892/2.);

  } // end if not set
  return table;
} // end TriangularMaster::gptable_vec

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
  // Linear search, but we don't expect to be searching a large set.
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
      // ProtoNode is on an edge (but not a corner).  The real node
      // was not created in CSkeleton::populate_femesh(), but may have
      // already been created by another call to
      // MasterElement::build().
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

FaceBoundaryElement *MasterElement2D::buildFaceBoundary(
					      const std::vector<Node*> &nodes,
					      const Element *bulkEl)
  const
{
  // nodes contains just the corner nodes of the edge that we're
  // creating.  There may be intermediate nodes if the element is
  // higher order.  They can be obtained from bulkEl, which is a bulk
  // element that has an face containing the given corner nodes.
  return new FaceBoundaryElement(*this,
				 bulkEl->getIntermediateNodes(nodes));
}

EdgeBoundaryElement *MasterElement1D::buildEdgeBoundary(
					      const std::vector<Node*> &nodes,
					      const Element *bulkEl)
const
{
  // nodes contains just the end nodes of the edge that we're
  // creating.  There may be intermediate nodes if the element is
  // higher order.  They can be obtained from bulkEl, which is a bulk
  // element that has an edge between the given end nodes.
  return new EdgeBoundaryElement(*this,
				 bulkEl->getIntermediateNodes(nodes));
}

ElementLite *MasterElement::buildLite(const std::vector<Coord> *nodes) 
  const
{
  return new ElementLite(*this, nodes);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

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

static void addPoints31(GaussPtTable &tbl, double r, double w) {
  // Add gauss points whose position in barycentric coords is a
  // permutation of (r, r, r, 1-3r).  The "31" notation is from Zhang,
  // and means that 3 of the coordinate's components have one value
  // and one has another.  By symmetry, all the points must have the
  // same weight.  Because barycentric coords in the master tet
  // geometry are just (x, y, z, 1-x-y-z), the actual position of a
  // point is given by the first three barycentric components.
  double s = 1. - 3.*r;
  tbl.addpoint(MasterCoord(s, r, r), w);
  tbl.addpoint(MasterCoord(r, s, r), w);
  tbl.addpoint(MasterCoord(r, r, s), w);
  tbl.addpoint(MasterCoord(r, r, r), w);
}

static void addPoints22(GaussPtTable &tbl, double r, double w) {
  // Same as addPoints31, but the barycentric coords are a permutation
  // of (r, r, 0.5-r, 0.5-r).
  double s = 0.5 - r;
  tbl.addpoint(MasterCoord(r, r, s), w);
  tbl.addpoint(MasterCoord(r, s, r), w);
  tbl.addpoint(MasterCoord(s, r, r), w);
  tbl.addpoint(MasterCoord(s, s, r), w);
  tbl.addpoint(MasterCoord(s, r, s), w);
  tbl.addpoint(MasterCoord(r, s, s), w);
}

static void addPoints211(GaussPtTable &tbl, double r, double s, double w) {
  // Barycentric coords are a permutation of (r, r, s, 1-2r-s)
  double t = 1. - 2*r - s;
  tbl.addpoint(MasterCoord(r, r, s), w);
  tbl.addpoint(MasterCoord(r, s, r), w);
  tbl.addpoint(MasterCoord(s, r, r), w);
  
  tbl.addpoint(MasterCoord(r, r, t), w);
  tbl.addpoint(MasterCoord(r, t, r), w);
  tbl.addpoint(MasterCoord(t, r, r), w);

  tbl.addpoint(MasterCoord(r, s, t), w);
  tbl.addpoint(MasterCoord(r, t, s), w);
  tbl.addpoint(MasterCoord(s, r, t), w);
  tbl.addpoint(MasterCoord(s, t, r), w);
  tbl.addpoint(MasterCoord(t, r, s), w);
  tbl.addpoint(MasterCoord(t, s, r), w);
}

const std::vector<GaussPtTable> &TetrahedralMaster::gptable_vec() const {
  static std::vector<GaussPtTable> table;
  static bool set = 0;

  // The weights in each table add up to 1/6, which is the volume of
  // the master space element.

  // Gauss points for a triangle and tetrahedron are from A SET OF
  // SYMMETRIC QUADRATURE RULES ON TRIANGLES AND TETRAHEDRA, Linbo
  // Zhang, Tao Cui and Hui Liu, Journal of Computational
  // Mathematics, Vol.27, No.1, 2009, 89–96.  The numbers were
  // copied out of the source code file src/quad.c from
  // http://lsec.cc.ac.cn/phg/download/phg-0.9.3-20170615.tar.bz2.

  if(!set) {
    set = 1;
     // order = 0, npts = 1
    table.emplace_back(0, 1);
    table.back().addpoint(MasterCoord(0.25, 0.25, 0.25), 1./6.);

     // order = 1, npts = 1
    table.emplace_back(1, 1);
    table.back().addpoint(MasterCoord(0.25, 0.25, 0.25), 1./6.);

    // order = 2, npts = 4
    table.emplace_back(2, 4);
    addPoints31(table.back(), (5. - sqrt(5.))/20., 1./24.);

    // Zienkiewicz and Taylor (5th edition, Vol 1, page 223.  Section
    // 9.10: Numerical integration -- triangular or tetrahdral
    // regions) provide this 5 point rule for order 3, but it includes
    // a negative weight, which most authors object to. 
    // table.emplace_back(3, 5);
    // table.back().addpoint(MasterCoord(0.25, 0.25, 0.25), -4./30.); 
    // table.back().addpoint(MasterCoord(1./6., 1./6., 1./6.), 3./40.);
    // table.back().addpoint(MasterCoord(0.5, 1./6., 1./6.), 3./40.);
    // table.back().addpoint(MasterCoord(1./6., 0.5, 1./6.), 3./40.);
    // table.back().addpoint(MasterCoord(1./6., 1./6., 0.5), 3./40.);

    // order = 3, npts = 8: Zhang, et al QUAD_3D_P3_
    table.emplace_back(3, 8);
    addPoints31(table.back(),
		.32805469671142664733580581998119743,
		.13852796651186214232361769837564129/6.);
    addPoints31(table.back(),
		.10695227393293068277170204157061650,
		.11147203348813785767638230162435871/6.);

    // order = 4, npts = 14:  Zhang QUAD_3D_P4_
    table.emplace_back(4, 14);
    addPoints31(table.back(),
		.09273525031089122628655892066032137,
		.07349304311636194934358694586367885/6.);
    addPoints31(table.back(),
		.31088591926330060975814749494040332,
		.11268792571801585036501492847638892/6.);
    addPoints22(table.back(),
		.04550370412564965000000000000000000,
		.04254602077708146686093208377328816/6.);

    // order = 5, npts = 14: Zhang QUAD_3D_P5_
    table.emplace_back(5, 14);
    addPoints31(table.back(),
		.31088591926330060979734573376345783,
		.11268792571801585079918565233328633/6.);
    addPoints31(table.back(),
		.09273525031089122640232391373703061,
		.07349304311636194954371020548632750/6.);
    addPoints22(table.back(),
		.04550370412564964949188052627933943,
		.04254602077708146643806942812025744/6.);

    // order = 6, npts = 24: Zhang QUAD_3D_P6_
    table.emplace_back(6, 24);
    addPoints31(table.back(),
		.21460287125915202928883921938628499,
		.03992275025816749209969062755747998/6.);
    addPoints31(table.back(),
		.04067395853461135311557944895641006,
		.01007721105532064294801323744593686/6.);
    addPoints31(table.back(),
		.32233789014227551034399447076249213,
		.05535718154365472209515327785372602/6.);
    addPoints211(table.back(),
		 .06366100187501752529923552760572698,
		 .60300566479164914136743113906093969,
		 (27./560.)/6.);

    // order = 7, npts = 35
    table.emplace_back(7, 35);
    table.back().addpoint(MasterCoord(0.25, 0.25, 0.25),
			  .09548528946413084886057843611722638/6.);
    addPoints31(table.back(),
		.31570114977820279942342999959331149,
		.04232958120996702907628617079854674/6.);
    addPoints22(table.back(),
		.05048982259839636876305382298656247,
		.03189692783285757993427482408294246/6.);
    addPoints211(table.back(),
		 .18883383102600104773643110385458576,
		 .57517163758700002348324157702230752,
		 .03720713072833462136961556119148112/6.);
    addPoints211(table.back(),
		 .02126547254148324598883610149981994,
		 .81083024109854856111810537984823239,
		 .00811077082990334156610343349109654/6.);

    // order = 8, npts = 46
    table.emplace_back(8, 46);
    addPoints31(table.back(),
		.03967542307038990126507132953938949,
		.00639714777990232132145142033517302/6.);
    addPoints31(table.back(),
		.31448780069809631378416056269714830,
		.04019044802096617248816115847981783/6.);
    addPoints31(table.back(),
		.10198669306270330000000000000000000,
		.02430797550477032117486910877192260/6.);
    addPoints31(table.back(),
		.18420369694919151227594641734890918,
		.05485889241369744046692412399039144/6.);
    addPoints22(table.back(),
		.06343628775453989240514123870189827,
		.03571961223409918246495096899661762/6.);
    addPoints211(table.back(),
		 .02169016206772800480266248262493018,
		 .71993192203946593588943495335273478,
		 .00718319069785253940945110521980376/6.);
    addPoints211(table.back(),
		 .20448008063679571424133557487274534,
		 .58057719012880922417539817139062041,
		 .01637218194531911754093813975611913/6.);

  } // end if not set
  return table;
} // end TetrahedralMaster::gptable_vec

MasterCoord TetrahedralMaster::center() const {
  return MasterCoord(0.25, 0.25, 0.25);
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void MasterElement::dumpDetails() const {
  oofcerr << "MasterElement::dumpDetails: " << name_ << std::endl;
  for(const ProtoNode *pn : protonodes) {
    OOFcerrIndent indent(4);
    oofcerr << *pn << std::endl;
  }
  OOFcerrIndent indent(2);
  oofcerr << "funcnodes=[";
  std::cerr << funcnodes;
  oofcerr << "]" << std::endl;
  oofcerr << "mapnodes=[";
  std::cerr << mapnodes;
  oofcerr << "]" << std::endl;
  oofcerr << "cornernodes=[";
  std::cerr << cornernodes;
  oofcerr << "]" << std::endl;
  oofcerr << "exteriorfuncnodes=[";
  std::cerr<< exteriorfuncnodes;
  oofcerr << "]" << std::endl;
}
