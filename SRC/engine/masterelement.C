// -*- C++ -*-
// $RCSfile: masterelement.C,v $
// $Revision: 1.41.6.14 $
// $Author: langer $
// $Date: 2014/11/05 16:54:25 $

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
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/masterelement.h"
#include "engine/ooferror.h"
#include "engine/shapefunction.h"
#include <math.h>
#include <iostream>

#if DIM == 2
#include "engine/IO/contour.h"
#include "engine/contourcell.h"
#endif // DIM == 2

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

// Count the number of exterior nodes that are for mapping only.
int MasterElement::nexteriormapnodes_only() const {
  int n = 0;
  for(std::vector<const ProtoNode*>::const_iterator pn=protonodes.begin();
      pn<protonodes.end(); ++pn)
    {
      if((*pn)->mapping() && ! (*pn)->func() && (*pn)->nedges() > 0)
	n++;
    }
  return n;
}
// Count the number of interior nodes that are for mapping only
int MasterElement::ninteriormapnodes_only() const {
  int n = 0;
  for(std::vector<const ProtoNode*>::const_iterator pn=protonodes.begin();
      pn<protonodes.end(); ++pn)
    {
      if((*pn)->mapping() && !(*pn)->func() && (*pn)->nedges() == 0)
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

#if DIM == 3

void ProtoNode::on_face(int faceno) {
  faceindex.push_back(faceno);
  element.faces[faceno]->addNode(this);
  // Put this node in its MasterElement's exterior lists, if it's not
  // already there.  Checking this way relies on not intermingling
  // on_face calls for one ProtoNode with calls for another one.
//   if(func_)
//     if(element.exteriorfuncnodes.empty() ||
//        *element.exteriorfuncnodes.rbegin() != index_)
//       element.exteriorfuncnodes.push_back(index_);
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
#endif	// DIM == 3

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

#if DIM == 2

// The MasterElement2D::contourcells functions return a vector of
// pointers to ContourCellSkeletons.  This vector is passed out to
// Python via a swig typemap (in masterelement.swg) and its elements
// are cached and wrapped in masterelement.spy.  The wrapping
// transfers the ownership to Python, so we don't have to worry about
// deleting the ContourCellSkeleton pointers that we've allocated
// here.

std::vector<ContourCellSkeleton*>*
TriangularMaster::contourcells(int n) const {
  // Divide a triangular master element up into n^2 triangles, like
  // this:
  //
  //  even n     odd n
  //
  //   |\         |\               	// backslashes
  //   | \        | \       		// terminating
  //   ----       ----       y1		// comments
  //   | /|\      | /|\      		// generate
  //   |/ | \     |/ | \      		// spurious
  //   ------     ------     y		// compiler
  //              |\ | /|\		// warnings
  //              | \|/ | \		//
  //              ---------
  //	             x  x1

  std::vector<ContourCellSkeleton*>* cells =
    new std::vector<ContourCellSkeleton*>(n*n);
  double dx = 1.0/n;
  int k = 0;			// counts cells

  for(int j=0; j<n; j++) {	// loop over rows
    bool leanleft = (j + n) % 2;
    double y = j*dx;
    double y1 = (j+1)*dx;
    if(j == n-1) y1 = 1.0;	// avoid roundoff
    for(int i=0; i<n-j-1; i++) { // loop over columns, not including the last
      double x = i*dx;
      double x1 = (i+1)*dx;
      ContourCellSkeleton &cell1 = *((*cells)[k++] = new ContourCellSkeleton);
      ContourCellSkeleton &cell2 = *((*cells)[k++] = new ContourCellSkeleton);
      ContourCellCoord ll(x, y, i, j);
      ContourCellCoord lr(x1, y, i+1, j);
      ContourCellCoord ur(x1, y1, i+1, j+1);
      ContourCellCoord ul(x, y1, i, j+1);
      if(leanleft) {
	// lower left triangle of a pair
	cell1[0] = ll;
	cell1[1] = lr;
	cell1[2] = ul;
	// upper right triangle of a pair
	cell2[0] = lr;
	cell2[1] = ur;
	cell2[2] = ul;
      }
      else {
	// upper left triangle of a pair
	cell1[0] = ll;
	cell1[1] = ur;
	cell1[2] = ul;
	// lower right triangle of a pair
	cell2[0] = ll;
	cell2[1] = lr;
	cell2[2] = ur;
      }
      leanleft = !leanleft;
    }
    // final triangle in the row
    ContourCellSkeleton &cell = *((*cells)[k++] = new ContourCellSkeleton);
    // See comment in TriangularMaster::exterior(), below, before
    // changing the next two lines!
    double x = 1.0 - y1;
    double x1 = 1.0 - y;
    cell[0] = ContourCellCoord(x, y, n-j-1, j);
    cell[1] = ContourCellCoord(x1, y, n-j, j);
    cell[2] = ContourCellCoord(x, y1, n-j-1, j+1);
  }
  return cells;
}

std::vector<ContourCellSkeleton*>*
QuadrilateralMaster::contourcells(int n) const
{

  std::vector<ContourCellSkeleton*>* cells =
    new std::vector<ContourCellSkeleton*>(2*n*n);
  double dx = 2.0/n;
  int k = 0;			// counts cells
  for(int j=0; j<n; j++) {
    bool leanleft = j%2 == 0;
    double y = j*dx - 1.0;
    double y1 = (j+1)*dx - 1.0;
    if(j == n-1) y1 = 1.0;	// avoid roundoff
    for(int i=0; i<n; i++) {
      double x = i*dx - 1.0;
      double x1 = (i+1)*dx - 1.0;
      if(i == n-1) x1 = 1.0;	// avoid roundoff
      ContourCellSkeleton &cell1 = *((*cells)[k++] = new ContourCellSkeleton);
      ContourCellSkeleton &cell2 = *((*cells)[k++] = new ContourCellSkeleton);
      ContourCellCoord ll(x, y, i, j);
      ContourCellCoord lr(x1, y, i+1, j);
      ContourCellCoord ur(x1, y1, i+1, j+1);
      ContourCellCoord ul(x, y1, i, j+1);
      if(leanleft) {
	cell1[0] = ll;
	cell1[1] = lr;
	cell1[2] = ul;
	cell2[0] = lr;
	cell2[1] = ur;
	cell2[2] = ul;
      }
      else {
	cell1[0] = ll;
	cell1[1] = ur;
	cell1[2] = ul;
	cell2[0] = ll;
	cell2[1] = lr;
	cell2[2] = ur;
      }
      leanleft ^= 1;
    }
  }
  return cells;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Is a point on the boundary of the MasterElement?

bool TriangularMaster::onBoundary(const MasterCoord &pt) const {
  return (pt(0) == 0.0 || pt(1) == 0.0 || pt(0) + pt(1) == 1.0);
}

bool QuadrilateralMaster::onBoundary(const MasterCoord &pt) const {
  return (pt(0) == -1.0 || pt(1) == -1.0 || pt(0) == 1.0 || pt(1) == 1.0);
}

// Are two points on the *same* boundary of the MasterElement?

bool TriangularMaster::onBoundary2(const MasterCoord &pt0,
                                   const MasterCoord &pt1)
  const
{
  return
    (pt0(0) == 0.0 && pt1(0) == 0.0) ||
    (pt0(1) == 0.0 && pt1(1) == 0.0) ||
    (pt0(0) + pt0(1) == 1.0 && pt1(0) + pt1(1) == 1.0);
}

bool QuadrilateralMaster::onBoundary2(const MasterCoord &pt0,
                                      const MasterCoord &pt1)
  const
{
  return
    (pt0(0) == -1.0 && pt1(0) == -1.0) ||
    (pt0(1) == -1.0 && pt1(1) == -1.0) ||
    (pt0(0) == 1.0 && pt1(0) == 1.0) ||
    (pt0(1) == 1.0 && pt1(1) == 1.0);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Are the two given MasterCoords on the same exterior edge of the
// master element?  An 'exterior' edge, as far as this routine cares,
// is one that begins at a corner listed in the given list of
// ElementCornerNodeIterators.  In the real world, exterior edges are
// those that form geometrical boundaries of the system.  They don't
// necessarily have anything to do with the boundary conditions, but
// are important for creating contour plots.

bool TriangularMaster::exterior(
			const MasterCoord &a, const MasterCoord &b,
			const std::vector<ElementCornerNodeIterator> &ext)
  const
{
  if(onBoundary(a) && onBoundary(b)) {
    for(std::vector<ElementCornerNodeIterator>::size_type i=0; i<ext.size();i++)
      {
	const MasterCoord &bdystart = ext[i].mastercoord();
	double x0 = bdystart(0);
	double y0 = bdystart(1);
	// We could presumably compute whether or not points a and b
	// were on an edge in some general way, but it's probably faster
	// and more accurate to take advantage of what we know of the
	// master element geometry, and just make a few simple
	// comparisons.
	if(x0 == 0.0) {
	  if(y0 == 0.0) {		// bottom edge, y=0
	    if(a(1)==0.0 && b(1)==0.0) {
	      return 1;
	    }
	  }
	  else if(y0 == 1.0) {	// left edge, x=0
	    if(a(0)==0.0 && b(0)==0.0) {
	      return 1;
	    }
	  }
	}
	else if(x0 == 1.0) {	// upper right edge, x+y=1
	  // Here we worry about roundoff error making it look like a
	  // point isn't quite on an edge.  But points a and b are
	  // really the corners of ContourCellSkeletons, so we just
	  // have to make sure that the comparison here is compatible
	  // with the computation there.
	  if(a(0)==1.0-a(1) && b(0)==1.0-b(1)) {
	    return 1;
	  }
	}
      }
  }
  return 0;
}

bool QuadrilateralMaster::exterior(const MasterCoord &a, const MasterCoord &b,
				   const std::vector<ElementCornerNodeIterator> &ext)
  const
{
  if(onBoundary(a) && onBoundary(b)) {
    for(std::vector<ElementCornerNodeIterator>::size_type i=0; i<ext.size();i++)
      {
	const MasterCoord &bdystart = ext[i].mastercoord();
	double x0 = bdystart(0);
	double y0 = bdystart(1);
	if(x0 == -1.0 && y0 == -1.0) { // bottom edge, y=-1
	  if(a(1) == -1.0 && b(1) == -1.0) {
	    return 1;
	  }
	}
	else if(x0 == 1.0 && y0 == -1.0) { // right edge, x=1
	  if(a(0) == 1.0 &&  b(0) == 1.0) {
	    return 1;
	  }
	}
	else if(x0 == 1.0 && y0 == 1.0) {	// top edge, y=1
	  if(a(1) == 1.0 && b(1) == 1.0) {
	    return 1;
	  }
	}
	else if(x0 == -1.0 && y0 == 1.0) { // left edge, x=-1
	  if(a(0) == -1.0 && b(0) == -1.0) {
	    return 1;
	  }
	}
      }
  }
  return 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::vector<const MasterCoord*> &TriangularMaster::perimeter() const {
  static const std::vector<const MasterCoord*> *p = 0;
  if(!p)
    p = findPerimeter();
  return *p;
}

const std::vector<const MasterCoord*> &QuadrilateralMaster::perimeter() const {
  static const std::vector<const MasterCoord*> *p = 0;
  if(!p)
    p = findPerimeter();
  return *p;
}

const std::vector<const MasterCoord*> &MasterElement1D::perimeter() const {
  static const std::vector<const MasterCoord*> *p = 0;
  if(!p)
    p = findPerimeter();
  return *p;
}

const std::vector<const MasterCoord*> *MasterElement::findPerimeter() const {
  std::vector<const MasterCoord*> *p = new std::vector<const MasterCoord*>;
  for(int i=0; i<nnodes(); i++) {
    const ProtoNode *pn = protonodes[i];
    if(pn->corner())
      p->push_back(&pn->mastercoord());
  }
  return p;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Contour plotting support functions.  It's quite possible that these
// can be rewritten in terms of generic MasterElement functions.  It
// would be good to do so, because these functions assume a particular
// geometry of the MasterElements.  The geometry assumed here must be
// consistent with the geometry laid out in the MasterElement subclass
// constructors.

CCurve *MasterElement::perimeterSection(const MasterCoord *a,
					const MasterCoord *b) const
{
  CCurve *curve = new CCurve;
  int sidea = sideno(*a);
  int sideb = sideno(*b);
  curve->push_back(a);
  int n = nedges();
  if(sidea != sideb) {
    for(int i=sidea; i!= sideb; i=(i+1)%n) {
      // See the "Memory Allocation Note" in contour.C.
      curve->push_back(endpoint(i));
    }
  }
  curve->push_back(b);
  return curve;
}

// -----------

int TriangularMaster::sidenumber(const MasterCoord &a) {
  // Given a MasterCoord on the edge of a triangular MasterElement,
  // return an integer indicating which side of the element it's on.
  // Sides include their endpoints but not their startpoints, going
  // counterclockwise.
  //
  //  |\          * (ending a comment with '\' generates a compiler warning!)
  // 0| \2
  //  |  \        *
  //  ----
  //    1
  if(a(0) == 0.0 && a(1) != 1.0) return 0;
  if(a(1) == 0.0) return 1;
  return 2;
}

const MasterCoord *TriangularMaster::endpoint(int side_number) const {
  // This returns the counterclockwise end of the side.  See the
  // "Memory Allocation Note" in contour.C for why this function
  // returns a pointer to static data.
  static const MasterCoord z00(0.0, 0.0);
  static const MasterCoord z10(1.0, 0.0);
  static const MasterCoord z01(0.0, 1.0);
  switch(side_number) {
  case 0:
    return &z00;
  case 1:
    return &z10;
  case 2:
    return &z01;
  }
  return 0;			// not reached
}

bool TriangularMaster::endPointComparator(const MasterEndPoint &a,
					const MasterEndPoint &b) // static
{
  int sidea = sidenumber(*a.mc);
  int sideb = sidenumber(*b.mc);
  if(sidea != sideb)
    return sidea < sideb;
  // both points on the same side
  switch(sidea) {
  case 0:
    if(a(1) > b(1)) return true;
    if(a(1) < b(1)) return false;
    break;
  case 1:
    if(a(0) < b(0)) return true;
    if(a(0) > b(0)) return false;
    break;
  case 2:
    if(a(0) > b(0)) return true;
    if(a(0) < b(0)) return false;
  }
  // both points coincide
  if(!a.start && b.start) return true;
  return false;
}

MasterEndPointComparator TriangularMaster::bdysorter() const {
  return TriangularMaster::endPointComparator;
}

// ----------

int QuadrilateralMaster::sidenumber(const MasterCoord &a) {
  //
  //   __3__
  //   |   |
  //  0|   |2
  //   -----
  //     1

  if(a(0) == -1.0 && a(1) != 1.0) return 0;
  if(a(1) == -1.0) return 1;
  if(a(0) == 1.0) return 2;
  return 3;
}

const MasterCoord *QuadrilateralMaster::endpoint(int side_number) const {
  // This returns the counterclockwise end of the side.  See the
  // "Memory Allocation Note" in contour.C for why this function
  // returns a pointer to static data.
  static const MasterCoord sw(-1.0, -1.0);
  static const MasterCoord se( 1.0, -1.0);
  static const MasterCoord ne( 1.0,  1.0);
  static const MasterCoord nw(-1.0,  1.0);
  switch(side_number) {
  case 0:
    return &sw;
  case 1:
    return &se;
  case 2:
    return &ne;
  case 3:
    return &nw;
  }
  return 0;			// not reached
}

bool QuadrilateralMaster::endPointComparator(const MasterEndPoint &a,
					     const MasterEndPoint &b) // static
{
  int sidea = sidenumber(*a.mc);
  int sideb = sidenumber(*b.mc);
  if(sidea != sideb)
    return sidea < sideb;
  switch(sidea) {
  case 0:
    if(a(1) > b(1)) return true;
    if(a(1) < b(1)) return false;
    break;
  case 1:
    if(a(0) < b(0)) return true;
    if(a(0) > b(0)) return false;
    break;
  case 2:
    if(a(1) < b(1)) return true;
    if(a(1) > b(1)) return false;
    break;
  case 3:
    if(a(0) > b(0)) return true;
    if(a(0) < b(0)) return false;
  };
  if(!a.start && b.start) return true;
  return false;
}

MasterEndPointComparator QuadrilateralMaster::bdysorter() const {
  return QuadrilateralMaster::endPointComparator;
}

// -------

// // Dealing with Edge elements the same way is sort of dumb, since
// // contouring is never done on edge elements.  But the class heirarchy
// // requires it at the moment.
// // TODO 3.1: Fix that.
// static bool edgeMasterEndPointComparator(const MasterEndPoint &a,
// 					 const MasterEndPoint &b)
// {
//   if(a(0) < b(0)) return true;
//   if(a(0) > b(0)) return false;
//   if(a(1) < b(1)) return true;
//   return false;
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Edgement *MasterElement::buildInterfaceElement(
// 		       PyObject *leftskelel, PyObject *rightskelel,
// 		       int segmentordernumber,
// 		       Material *m,
// 		       const std::vector<Node*> *leftnodes,
// 		       const std::vector<Node*> *rightnodes,
// 		       bool leftnodesinorder, bool rightnodesinorder,
// 		       const std::vector<std::string> *pInterfacenames)
//   const
// {
//   return new InterfaceElement(leftskelel, rightskelel,
// 			      segmentordernumber,
// 			      *this,
// 			      leftnodes, rightnodes,
// 			      leftnodesinorder, rightnodesinorder,
// 			      m, pInterfacenames);
// }

#endif	// DIM == 2

Element *MasterElement::build(CSkeletonElement *el, const Material *m,
			      const std::vector<Node*> *nodes)
  const
{
  return new Element(el, *this, nodes, m);
}

FaceBoundaryElement *MasterElement::buildFaceBoundary(
					      const std::vector<Node*> *nodes)
  const
{
  return new FaceBoundaryElement(*this, nodes);
}

EdgeBoundaryElement *MasterElement::buildEdgeBoundary(
					      const std::vector<Node*> *nodes)
const
{
  return new EdgeBoundaryElement(*this, nodes);
}

ElementLite *MasterElement::buildLite(const std::vector<Coord> *nodes) 
  const
{
  return new ElementLite(*this, nodes);
}

#if DIM == 3

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

#endif	// DIM == 3


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

#if DIM == 3
const std::string &TetrahedralMaster::classname() const {
  static std::string nm("TetrahedralMaster");
  return nm;
}
#endif // DIM == 3
