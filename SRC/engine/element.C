// -*- C++ -*-
// $RCSfile: element.C,v $
// $Revision: 1.91.2.32 $
// $Author: langer $
// $Date: 2014/12/14 01:07:52 $

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
#include "common/IO/oofcerr.h"
#include "common/cleverptr.h"
#include "common/doublevec.h"
#include "common/ooferror.h"
#include "common/printvec.h"
#include "common/pythonlock.h"
#include "common/swiglib.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "engine/IO/gridsource.h"
#include "engine/cnonlinearsolver.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/csubproblem.h"
#include "engine/edge.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
//#include "engine/face.h"
#include "engine/femesh.h"
#include "engine/flux.h"
#include "engine/linearizedsystem.h"
#include "engine/masterelement.h"
#include "engine/material.h"
#include "engine/nodalequation.h"
#include "engine/node.h"
#include "engine/ooferror.h"
#include "engine/outputval.h"
#include "engine/shapefunction.h"
#include <string>
#include <vector>

#if DIM==3
#include <vtkMath.h>
#endif	// DIM==3

// ElementData constructors.
ElementData::ElementData(const std::string &nm)
  : name_(nm)
{}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementBase::ElementBase(const MasterElement &me)
  : master(me)
{}

const std::string &ElementBase::modulename() const {
  static const std::string name("ooflib.SWIG.engine.element");
  return name;
}

int ElementBase::dimension() const {
  return master.dimension();
}

int ElementBase::nedges() const {
  return master.nedges();
}

int ElementBase::nnodes() const { 
  return master.nnodes(); 
}

int ElementBase::nmapnodes() const { 
  return master.nmapnodes(); 
}

int ElementBase::nfuncnodes() const {
  return master.nfuncnodes(); 
}

int ElementBase::ncorners() const { 
  return master.ncorners(); 
}

int ElementBase::nexteriorfuncnodes() const {
  return master.nexteriorfuncnodes(); 
}

double ElementBase::det_jacobian(const GaussPoint &g) const {
  return master.mapfunction->det_jacobian(this, g);
}

double ElementBase::det_jacobian(const MasterCoord &mc) const {
  return master.mapfunction->det_jacobian(this, mc);
}

int ElementBase::shapefun_degree() const {
  return master.shapefunction->degree();
}

int ElementBase::dshapefun_degree() const {
  return master.shapefunction->deriv_degree();
}

int ElementBase::mapfun_degree() const {
  return master.mapfunction->degree();
}

double ElementBase::Jdmasterdx(SpaceIndex i, SpaceIndex j, const GaussPoint &g)
  const
{

#if DIM==2
  //         | J11  -J01 |
  //  J^-1 = |           | / |J|
  //         |-J10   J00 |

  double sum = 0;
  if(i == j) {
    int ii = 1 - i;
    for(ElementNodePositionIterator ni=mapnode_positerator(); !ni.end(); ++ni) {
      sum += (ni.position())[ii] * ni.masterderiv(ii, g);
    }
  }
  else {			// i != j
    for(ElementNodePositionIterator ni=mapnode_positerator(); !ni.end(); ++ni)
      sum -= (ni.position())[i] * ni.masterderiv(j, g);
  }
  return sum;

#elif DIM==3
  // Typing out a closed form in code is messy for 3d.  TODO 3.1: 3D it
  // might be worth it to type it out eventually as this is
  // inefficient
  double m[DIM][DIM], inverse[DIM][DIM];
  int ii, jj;
  for(ii=0; ii<DIM; ++ii) {
    for(jj=0; jj<DIM; ++jj) {
      m[ii][jj] = jacobian(ii,jj,g);
    }
  }
  double dj = vtkMath::Determinant3x3(m);
  vtkMath::Invert3x3(m,inverse);
  return dj*inverse[i][j];
#endif	// DIM==3
}

double ElementBase::Jdmasterdx(SpaceIndex i, SpaceIndex j,
			       const MasterCoord &mc)
  const
{
#if DIM==2
  double sum = 0;
  if(i == j) {
    int ii = 1 - i;
    for(ElementNodePositionIterator ni=mapnode_positerator(); !ni.end(); ++ni)
      sum += (ni.position())[ii] * ni.masterderiv(ii, mc);
  }
  else {			// i != j
    for(ElementNodePositionIterator ni=mapnode_positerator(); !ni.end(); ++ni)
      sum -= (ni.position())[i] * ni.masterderiv(j, mc);
  }
  return sum;

#elif DIM==3
  double m[DIM][DIM], inverse[DIM][DIM];
  int ii, jj;
  for(ii=0; ii<DIM; ++ii) {
    for(jj=0; jj<DIM; ++jj) {
      m[ii][jj] = jacobian(ii,jj,mc);
    }
  }
  double dj = vtkMath::Determinant3x3(m);
  vtkMath::Invert3x3(m,inverse);
  return dj*inverse[i][j];
#endif	// DIM==3
}


double ElementBase::Jdmasterdx(SpaceIndex i, SpaceIndex j, const Coord &coord)
  const
{
  return Jdmasterdx(i, j, to_master(coord));
}


// conversion between real coordinates and master element coordinates

Coord ElementBase::from_master(const MasterPosition &mc) const {
  Coord p;			// initialized to (0,0) or (0,0,0)
  for(CleverPtr<ElementMapNodePositionIterator> n(mapnode_positerator()); 
      !n->end(); ++*n)
    {
      p += n->shapefunction(mc) * n->position();
    }
  return p;
}

static const double tolerancesq = 1.e-10; // should be settable by user
static const int maxiter = 100;	// should also be settable by user

MasterCoord ElementBase::to_master(const Coord &x) const {
  // Use Newton's method to solve from_master(xi) - x = 0 for xi.
  // xi -> xi + J^-1 * (x - from_master(xi))
  MasterCoord xi;		// initialized to (0,0) or (0,0,0)
  Coord dx = x - from_master(xi);
  int iter = 0;
  do {				// Newton iteration
    double jac[DIM][DIM]; // use simple matrix repr. for 2x2
    for(SpaceIndex i=0; i<DIM; ++i)
      for(SpaceIndex j=0; j<DIM; ++j)
	jac[i][j] = jacobian(i, j, xi);

#if DIM==2
    double dj = jac[0][0]*jac[1][1] - jac[0][1]*jac[1][0];
    dj = 1./dj;
    // xi --> xi + J^-1*(x - from_master(xi))
    xi(0) += ( jac[1][1]*dx[0] - jac[0][1]*dx[1])*dj;
    xi(1) += (-jac[1][0]*dx[0] + jac[0][0]*dx[1])*dj;
#elif DIM==3
    double invjac[DIM][DIM];
    vtkMath::Invert3x3(jac,invjac);
    // xi --> xi + J^-1*(x - from_master(xi))
    xi[0] += ( invjac[0][0]*dx[0] + invjac[0][1]*dx[1] + invjac[0][2]*dx[2] );
    xi[1] += ( invjac[1][0]*dx[0] + invjac[1][1]*dx[1] + invjac[1][2]*dx[2] );
    xi[2] += ( invjac[2][0]*dx[0] + invjac[2][1]*dx[1] + invjac[2][2]*dx[2] );
#endif // DIM==3
    dx = x - from_master(xi);	// reevaluate rhs
  } while((norm2(dx) > tolerancesq) && (++iter < maxiter));
  return xi;
}


// J(i,j) = d(real_coord i)/d(master_coord j)

double ElementBase::jacobian(SpaceIndex i, SpaceIndex j, const GaussPoint &g)
  const
{
  double jac = 0.0;
  for(CleverPtr<ElementMapNodePositionIterator> ni(mapnode_positerator()); 
      !ni->end(); ++*ni)
    {
      jac += (ni->position())[i] * ni->masterderiv(j, g);
    }
  return jac;
}

double ElementBase::jacobian(SpaceIndex i, SpaceIndex j, const MasterCoord &mc)
  const
{
  double jac = 0.0;
  for(CleverPtr<ElementMapNodePositionIterator> ni(mapnode_positerator()); 
      !ni->end(); ++*ni)
    {
      jac += (ni->position())[i] * ni->masterderiv(j, mc);
    }
  return jac;
}

// Generic area calculation, done by integrating 1.  TODO OPT: It may be
// better to do a dimension-dependent calculation.

double ElementBase::span() const {
  double a = 0.0;
  for(GaussPointIterator gpt = integrator(0); !gpt.end(); ++gpt) {
    a += gpt.gausspoint().weight();
  }
  return a;
}

MasterCoord ElementBase::center() const {
  return master.center();
}

std::vector<GaussPoint*>* ElementBase::integration_points(int order) const {
  std::vector<GaussPoint*>* r = new std::vector<GaussPoint*>;
  for(GaussPointIterator g = integrator(order); !g.end(); ++g) {
    r->push_back(g.gausspointptr());
  }
  return r;
}

GaussPointIterator ElementBase::integrator(int order) const {
  return GaussPointIterator(this, (order < 0 ? 0 : order));
}

VTKCellType ElementBase::getCellType() const { 
  return master.getCellType(); 
}

ElementNodePositionIterator *ElementBase::node_positerator() const {
  return new ElementNodePositionIterator(*this);
}

ElementMapNodePositionIterator *ElementBase::mapnode_positerator() const {
  return new ElementMapNodePositionIterator(*this);
}

ElementFuncNodePositionIterator *ElementBase::funcnode_positerator() const {
  return new ElementFuncNodePositionIterator(*this);
}

ElementCornerNodePositionIterator *ElementBase::cornernode_positerator() const {
  return new ElementCornerNodePositionIterator(*this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementLite::ElementLite(const MasterElement &me,
			 const std::vector<Coord> *pts)
  : ElementBase(me),
    coords(*pts)
{}

const std::string &ElementLite::classname() const {
  static const std::string cname("ElementLite");
  return cname;
}

Coord ElementLite::position(int i) const {
  return coords[i];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Element::Element(CSkeletonElement *el, const MasterElement &me,
		 const std::vector<Node*> *nl, const Material *mat)
  : ElementBase(me),
    nodelist(*nl),
    matl(mat),
#if DIM==2
    exterior_edges(0),
#endif // DIM==2
    cskeleton_element(el)
{
  //  Trace("Element::Element " + me.name());
  //  int nn = me.nnodes();
  //  for(int i=0; i<nn; i++) {
  //    nodelist[i] = (*nl)[i];
  //  }
}

Element::~Element() {
  // for(unsigned int i=0; i<edgeset.size(); i++)
  //   delete edgeset[i];
  // for(unsigned int i=0; i<faceset.size(); i++)
  //   delete faceset[i];

#if DIM==2
  delete exterior_edges;
#endif // DIM=2
}

const std::string &Element::classname() const {
  static const std::string cname("Element");
  return cname;
}

const std::string *Element::repr() const {
  std::string *rep =  new std::string(master.name());
  for(int i=0; i<nnodes(); i++)
    *rep += " " + to_string(*nodelist[i]);
  return rep;
}

const std::string *ElementLite::repr() const {
  std::string *rep = new std::string(master.name());
  for(int i=0; i<nnodes(); i++) {
    *rep += " " + to_string(coords[i]);
  }
  return rep;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Element::set_index(int i) {
  index_=i;
}

const int &Element::get_index() const {
  return index_;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// refreshMaterial() is called when Materials have been reassigned in a
// Microstructure after the FEMesh has been created.  The Elements
// need to ask their SkeletonElements for the new Material.

void Element::refreshMaterial(const CSkeletonBase *skeleton) {
  if(cskeleton_element)
    matl = cskeleton_element->material(skeleton);
  else
    matl = 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Actually construct the linear system object.  Called from
// CSubProblem::make_linear_system.

void Element::make_linear_system(const CSubProblem *const subproblem,
				 double time,
				 const CNonlinearSolver *nlsolver,
				 LinearizedSystem &system)
  const
{
  std::vector<int> dofmap = localDoFmap();
  const Material *mat = material();
  if(mat) {
    mat->begin_element(subproblem, this);
    // TODO OPT: iorder could be precomputed or cached, but do some
    // careful profiling before changing anything.  Preliminary tests
    // indicate that the time spent computing iorder is negligible.
    int iorder = mat->integrationOrder(subproblem, this);

    // TODO OPT: MAYBE Use different integration orders for different
    // equations and properties.  That might make precomputations
    // difficult.
    for(GaussPointIterator gpt = integrator(iorder);
	!gpt.end();++gpt) {
      mat->make_linear_system( subproblem, this, gpt, dofmap, time,
			       nlsolver, system );
    }    
    mat->end_element(subproblem, this);
  }
}


// Post-processing, which is after equilibration.
void Element::post_process(CSubProblem *subproblem) const {
  const Material *mat = material();
  if(mat) {
    mat->post_process(subproblem, this);
  }
}

// void Element::begin_material_computation(FEMesh *mesh) const {
//   const Material *mat = material();
//   if(mat)
//     mat->begin_element(mesh, this);
// }

// void Element::end_material_computation(FEMesh *mesh) const {
//   const Material *mat = material();
//   if(mat)
//     mat->end_element(mesh, this);
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int Element::appendData(ElementData *x) const {
  el_data.push_back(x);
  return el_data.size() - 1;
}

void Element::setData(int i, ElementData *x) const {
  el_data[i] = x;
}

ElementData *Element::getData(int i) const {
  return el_data[i];
}

// This call does retrieval-by-name, and so should be used
// as infrequently as can be managed.

ElementData *Element::getDataByName(const std::string &name) const {
  int i=getIndexByName(name);
  if (i >= 0)
    return getData(i);
  else
    return 0;
}

// Overwrites the data indexed under the indicated name, appends
// it, whichever.

void Element::setDataByName(ElementData *x) const {
  int i=getIndexByName(x->name());
  if (i>=0)
    // NB Does this overwrite have implications for reference counts
    // of the referred-to Python data?
    setData(i,x);
  else
    appendData(x);
}

// Retrieval by name should be done infrequently, to avoid the search.

int Element::getIndexByName(const std::string &searchname) const {
  for(std::vector<ElementData*>::size_type i=0; i<el_data.size(); i++) {
    if (el_data[i]->name() == searchname) {
      return i;
    }
  }
  // Not found -- this is permissible, return something.
  return -1;
}

// Deletion functions do not remove the pointed-to object, they just
// remove the ElementData* from the element object's local array.

void Element::delData(int i) const {
  std::vector<ElementData*>::iterator it = el_data.begin();
  it += i;
  el_data.erase(it);
}

void Element::delDataByName(const std::string &name) const {
  std::vector<ElementData*>::iterator it = el_data.begin();
  int i=getIndexByName(name);
  it += i;
  el_data.erase(it);
}

void Element::clearData() const {
  el_data.clear();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementNodeIterator Element::node_iterator() const {
  return ElementNodeIterator(*this);
}

ElementMapNodeIterator Element::mapnode_iterator() const {
  return ElementMapNodeIterator(*this);
}

// This returns a pointer, so that the caller can get either an
// ElementFuncNodeIterator or an InterfaceElementFuncNodeIterator with
// appropriate sidedness, according to context.

ElementFuncNodeIterator *Element::funcnode_iterator() const {
  return new ElementFuncNodeIterator(*this);
}

ElementCornerNodeIterator Element::cornernode_iterator() const {
  return ElementCornerNodeIterator(*this);
}

Coord Element::position(int i) const {
  return nodelist[i]->position();
}

Node *Element::getSegmentNode(const FEMesh *femesh, int segidx, int nodeidx)
  const
{
  CSkeletonNode *skelnode = get_skeleton_element()->getSegmentNode(segidx,
								   nodeidx);
  // Skeleton and FEMesh node indices agree for corner nodes, since
  // corner nodes are always func nodes.
  Node *node = femesh->getNode(skelnode->getIndex());
  assert(node->position() == skelnode->position());
  return node;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==3

// findNormal is only used for 2D Elements in 3D.  It's not defined as
// an Element method because 2D and 3D elements aren't different
// classes.  TODO 3.1: Perhaps that means that the class structure is
// wrong.

// TODO 3.1: Displaced normal?  This version just uses the initial
// positions of the nodes.

Coord findNormal(const ElementBase *elem, const MasterPosition &position) {
  assert(elem->masterelement().dimension() == 2);
  // The normal to a 2D vector at the given position is found by
  // mapping the 2D master space x and y unit vectors to physical
  // space at the given position, and taking their cross product
  // there.
  MasterCoord mc = position.mastercoord();
  // Physical space components of the master space x vector (not normalized)
  double j00 = elem->jacobian(0, 0, mc);
  double j10 = elem->jacobian(1, 0, mc);
  double j20 = elem->jacobian(2, 0, mc);
  // Physical space components of the master space y vector (not normalized)
  double j01 = elem->jacobian(0, 1, mc);
  double j11 = elem->jacobian(1, 1, mc);
  double j21 = elem->jacobian(2, 1, mc);
  // Cross product of the x and y vectors
  Coord norm(j10*j21 - j20*j11,
	     j20*j01 - j00*j21,
	     j00*j11 - j10*j01);
  // normalize it.
  double len2 = norm2(norm);
  return norm/sqrt(len2);
}

std::vector<OutputValue> *findNormals(const ElementBase *elem, 
				      const std::vector<MasterCoord*> *coords)
{
  std::vector<OutputValue> *results = new std::vector<OutputValue>;
  results->reserve(coords->size());
  for(std::vector<MasterCoord*>::size_type i=0; i<coords->size(); i++) {
    Coord normal = findNormal(elem, *(*coords)[i]);
    results->push_back(OutputValue(new VectorOutputVal(normal)));
  }
  return results;
}
#endif // DIM==3

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Superconvergent patch recovery
int Element::nSCpoints() const {
  return master.nSCpoints();
}

const MasterCoord &Element::getMasterSCpoint(int i) const {
  return master.getSCpoint(i);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


OutputValue Element::outputField(const FEMesh *mesh, const Field &field,
				 const MasterPosition &pos)
  const
{
  OutputValue val = field.newOutputValue();
  for(CleverPtr<ElementFuncNodeIterator> node(funcnode_iterator()); 
      !node->end(); ++*node)
    {
      double sfvalue = node->shapefunction(pos);
      val += sfvalue*field.output(mesh, *node);
    }
  return val;
}

std::vector<OutputValue> *
Element::outputFields(const FEMesh *mesh, const Field &field,
		      const std::vector<MasterCoord*> *coords) const
{
  std::vector<OutputValue> *results = new std::vector<OutputValue>;
  results->reserve(coords->size());
  for(std::vector<MasterCoord*>::size_type i=0; i<coords->size(); i++) {
    OutputValue val = field.newOutputValue();
    for(CleverPtr<ElementFuncNodeIterator> node(funcnode_iterator()); 
	!node->end(); ++*node) 
      {
	double sfvalue = node->shapefunction(*(*coords)[i]);
	// Field::output returns an appropriate type of 0 if the Field
	// isn't defined on the Node.
	val += sfvalue*field.output(mesh, *node);
      }
    results->push_back(val);
  }
  return results;
}

// std::vector<OutputValue> *
// Element::outputFieldsAnyway(const CSubProblem *mesh, const Field &field,
// 			    const std::vector<MasterCoord*> *coords) const
// {
//   // Return zero if the field isn't defined.  Don't throw an exception.
//   if(mesh->is_defined_field(field))
//     return outputFields(mesh, field, coords);
//   // Field isn't defined.
//   std::vector<OutputValue> *results = new std::vector<OutputValue>;
//   results->reserve(coords->size());
//   for(std::vector<MasterCoord*>::size_type i=0; i<coords->size(); i++) {
//     results->push_back(field.newOutputValue());
//   }
//   return results;
// }

// This version takes a vector of MasterCoords, not MasterCoord*s, and
// is used by Edge::outputFields.
std::vector<OutputValue> *
Element::outputFields(const FEMesh *mesh, const Field &field,
		      const std::vector<MasterCoord> &coords) const
{
  std::vector<OutputValue> *results = new std::vector<OutputValue>;
  results->reserve(coords.size());
  for(std::vector<MasterCoord>::size_type i=0; i<coords.size(); i++) {
    OutputValue val = field.newOutputValue();
    for(CleverPtr<ElementFuncNodeIterator> node(funcnode_iterator());
	!node->end(); ++*node)
      {
	double sfvalue = node->shapefunction(coords[i]);
	// Field::output returns an appropriate type of 0 if the Field
	// isn't defined on the Node.
	val += sfvalue*field.output(mesh, *node);
      }
    results->push_back(val);
  }
  return results;
}

// std::vector<OutputValue> *
// Element::outputFieldsAnyway(const CSubProblem *mesh, const Field &field,
// 		      const std::vector<MasterCoord> &coords) const
// {
//   if(mesh->is_defined_field(field))
//     return outputFields(mesh, field, coords);
//   std::vector<OutputValue> *results = new std::vector<OutputValue>;
//   results->reserve(coords.size());
//   for(std::vector<MasterCoord>::size_type i=0; i<coords.size(); i++) {
//     results->push_back(field.newOutputValue());
//   }
//   return results;
// }

std::vector<OutputValue> *
Element::outputFieldDerivs(const FEMesh *mesh, const Field &field,
			   SpaceIndex *deriv_component,
			   const std::vector<MasterCoord*> *coords) const
{
  std::vector<OutputValue> *results = new std::vector<OutputValue>;
  results->reserve(coords->size());
  for(std::vector<MasterCoord*>::size_type i=0; i<coords->size(); i++) {
    OutputValue val = field.newOutputValue();
    for(CleverPtr<ElementFuncNodeIterator> node(funcnode_iterator());
	!node->end(); ++*node) 
      {
	double dsfvalue = node->dshapefunction(*deriv_component, *(*coords)[i]);
	val += dsfvalue*field.output(mesh, *node);
      }
    results->push_back(val);
  }
  return results;
}

OutputValue Element::outputFieldDeriv(const FEMesh *mesh, const Field &field,
				      SpaceIndex *deriv_component,
				      const MasterPosition &pos) const
{
  OutputValue val = field.newOutputValue();
  for(CleverPtr<ElementFuncNodeIterator> node(funcnode_iterator());
      !node->end(); ++*node)
    {
      double dsfvalue = node->dshapefunction(*deriv_component, pos);
      val += dsfvalue*field.output(mesh, *node);
    }
  return val;
}

// OutputValue Element::outputFlux(const FEMesh *mesh, const Flux &flux,
// 				const MasterPosition &pos) const
// {
//   return flux.output( mesh, this, pos );
// }

std::vector<OutputValue> *
Element::outputFluxes(const FEMesh *mesh, const Flux &flux,
		      const std::vector<MasterCoord*> *coords) const
{
  std::vector<OutputValue> *results = new std::vector<OutputValue>;
  results->reserve(coords->size());
  for(std::vector<MasterCoord*>::size_type i=0; i<coords->size(); i++)
    results->push_back( flux.output( mesh, this, *(*coords)[i] ) );
  return results;
}

// Create a vector mapping the canonical order of the Element's
// degrees of freedom to the DOF's actual indices.  Almost identical
// code to the routine below.
std::vector<int> Element::localDoFmap() const {
  std::vector<int> dofmap(ndof(),-1);
  for(std::vector<Field*>::size_type fi=0; fi< Field::all().size(); fi++) {
    Field &field = *Field::all()[fi];
    // Field components.
    for(IteratorP fcomp=field.iterator(ALL_INDICES); !fcomp.end(); ++fcomp) {
      // Nodes
      for(CleverPtr<ElementFuncNodeIterator> node(funcnode_iterator());
	  !node->end(); ++*node)
	{
	  if(node->hasField(field)) {
	    DegreeOfFreedom *dof = field(*node, fcomp.integer());
	    dofmap[node->localindex(field, fcomp)] = dof->dofindex();
	  }
	}
    }
  }
  return dofmap;
}

// Fill in a vector of the values of the Element's degrees of freedom,
// in canonical order.  The list is assumed to already be the correct
// size. 

void Element::localDoFs(const FEMesh *mesh, DoubleVec &doflist) const
{
  for(std::vector<Field*>::size_type fi=0; fi<Field::all().size(); fi++) {
    Field &field = *Field::all()[fi];
    // loop over field components
    for(IteratorP fcomp=field.iterator(ALL_INDICES); !fcomp.end(); ++fcomp) {
      // loop over nodes
      for(CleverPtr<ElementFuncNodeIterator> node(funcnode_iterator());
	  !node->end(); ++*node)
	{
	  if(node->hasField(field)) {
	    DegreeOfFreedom *dof = field(*node, fcomp.integer());
// 	    std::cerr << "Element::localDoFs: "
// 		      << field << "[" << fcomp.integer() << "] "
// 		      << node.node()->position() << " "
// 		      << node.localindex(field, fcomp) << std::endl;
	    doflist[node->localindex(field, fcomp)] = dof->value(mesh);
	  }
	}
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// // The main edge function.

// BoundaryEdge *Element::newBndyEdge(const FuncNode *n0, const FuncNode *n1)
//   const
// {
//   assert(0);  // This is obsolete.
// //   Trace("Element::newBndyEdge " + to_string(*n0) + " " + to_string(*n1));
//   // find ElementCornerNodeIterators for each FuncNode
//   ElementCornerNodeIterator alpha = cornernode_iterator();
//   // It may not be sufficient to compare pointers to Nodes, since the
//   // Nodes can have different derived types.  Use
//   // operator==(Node&,Node&) and operator!=(Node&,Node&) instead.
//   while((*alpha.node() != *n0) && !alpha.end()) {
//     ++alpha;
//   }
//   if(alpha.end()) {
//     throw ErrUserError("Element::newBndyEdge: Nodes not corners of element");
//   }
// #if DIM == 2
//   bool forward;
//   ElementCornerNodeIterator beta = alpha + 1;
//   if(*beta.node() == *n1) {
//     // second node is in front of first
//     forward = true;
//   }
//   else {			// second node isn't in front
//     beta = alpha + (ncorners() - 1);
//     if(*beta.node() != *n1) {
//       // it's not behind either
//       throw ErrUserError("Element::newBndyEdge: Inconsistent node set");
//     }
//     forward = false;		// it was behind
//   }
// #elif DIM == 3
//   ElementCornerNodeIterator beta = cornernode_iterator();
//   while((*beta.node() != *n1) && !beta.end()) {
//     ++beta;
//   }
//   if(beta.end()) {
//     throw ErrUserError("Element::newBndyEdge: Nodes not corners of element");
//   }
// #endif

//   // find out which edge of the masterelement contains alpha and beta
//   const MasterEdge *medge = masterelement().masteredge(alpha, beta);

//   // put the endpoints and all intermediate FuncNodes in the BoundaryEdge
//   BoundaryEdge *ed = new BoundaryEdge(this, medge->func_size());
//   ed->add_node(alpha.funcnode_iterator());
// #if DIM==2 // TODO 3.1: 3D will have to add edge nodes another way for 3D when we do quadratic elements
//   int increment;
//   if(forward)
//     increment = 1;
//   else
//     increment = nexteriorfuncnodes() - 1;

//   ElementExteriorNodeIterator middle = alpha.exteriornode_iterator()+increment;
//   while(*middle.node() != *beta.node()) {
//     ed->add_node(middle);
//     middle += increment;
//   }
// #endif
//   ed->add_node(beta.funcnode_iterator());

//   return ed;
// } // end Element::newBndyEdge

// BoundaryEdge *Element::getBndyEdge(const FuncNode *n0, const FuncNode *n1) {

//   assert(0);  // This is obsolete.

//   BoundaryEdge *ed;

// //   Trace("Element::getBndyEdge " + to_string(*n0) + " " + to_string(*n1));
//   // find_edge will correctly detect nullness of the edgelist.
//   if( (ed=find_b_edge(n0,n1))==0 ) {
//     ed=newBndyEdge(n0,n1);
//     if(ed!=0) {
//       add_b_edge(ed);
//       return ed;
//     }
//     else
//       throw ErrUserError("Element::getBndyEdge: Unable to make edge.");
//     // Probable cause is that the input nodes are not adjacent
//     // corners in the derived element type.
//   }
//   return ed; // Otherwise return the non-null result from find_edge.
// }

// BoundaryEdge *Element::find_b_edge(const FuncNode *n0, const FuncNode *n1)
//   const
// {
//   assert(0);  // This is obsolete.
//   for(unsigned int i=0; i<edgeset.size(); i++) {
//     if(edgeset[i]->edge_match(n0, n1))
//       return edgeset[i];
//   }
//   return 0;
// }

// void Element::add_b_edge(BoundaryEdge *ed_in) {
//   assert(0);  // This is obsolete.
//   // The edge list is not allocated unless needed, and it needs to be
//   // 2x the number of geometric edges, because edges are directed.
//   if(edgeset.empty())
//     edgeset.reserve(2*master.nedges());
//   edgeset.push_back(ed_in);
// }

// #if DIM==3

// BoundaryFace *Element::newBndyFace(const FuncNode *n0, const FuncNode *n1,
// 				   const FuncNode *n2)
//   const
// {
// //   Trace("Element::newBndyFace " + to_string(*n0) + " " + to_string(*n1));
//   // find ElementCornerNodeIterators for each FuncNode
//   ElementCornerNodeIterator alpha = cornernode_iterator();
//   // It may not be sufficient to compare pointers to Nodes, since the
//   // Nodes can have different derived types.  Use
//   // operator==(Node&,Node&) and operator!=(Node&,Node&) instead.
//   while((*alpha.node() != *n0) && !alpha.end()) {
//     ++alpha;
//   }
//   if(alpha.end()) {
//     throw ErrUserError("Element::newBndyFace: Nodes not corners of element");
//   }
//   //bool forward;

//   ElementCornerNodeIterator beta = cornernode_iterator();
//   while((*beta.node() != *n1) && !beta.end()) {
//     ++beta;
//   }
//   if(beta.end()) {
//     throw ErrUserError("Element::newBndyFace: Nodes not corners of element");
//   }

//   ElementCornerNodeIterator gamma = cornernode_iterator();
//   while((*gamma.node() != *n2) && !gamma.end()) {
//     ++gamma;
//   }
//   if(gamma.end()) {
//     throw ErrUserError("Element::newBndyFace: Nodes not corners of element");
//   }

//   // find out which face of the masterelement contains alpha and beta and gamma
//   const MasterFace *mface = masterelement3D().masterface(alpha, beta, gamma);

//   // put the endpoints and all intermediate FuncNodes in the BoundaryFace
//   BoundaryFace *ed = new BoundaryFace(this, mface->func_size());
//   ed->add_node(alpha.funcnode_iterator());
//   ed->add_node(beta.funcnode_iterator());
//   ed->add_node(gamma.funcnode_iterator());

//   return ed;
// } // end Element::newBndyFace

// BoundaryFace *Element::getBndyFace(const FuncNode *n0, const FuncNode *n1,
// 				   const FuncNode *n2)
// {
//   BoundaryFace *fc;

// //   Trace("Element::getBndyFace " + to_string(*n0) + " " + to_string(*n1));
//   // find_face will correctly detect nullness of the facelist.
//   if( (fc = find_b_face(n0,n1,n2)) == 0 ) {
//     fc = newBndyFace(n0,n1,n2);
//     if(fc!=0) {
//       add_b_face(fc);
//       return fc;
//     }
//     else
//       throw ErrUserError("Element::getBndyFace: Unable to make face.");
//     // Probable cause is that the input nodes are not adjacent
//     // corners in the derived element type.
//   }
//   return fc; // Otherwise return the non-null result from find_face.
// }

// BoundaryFace *Element::find_b_face(const FuncNode *n0, const FuncNode *n1,
// 				   const FuncNode *n2) 
//   const
// {
//   for(unsigned int i=0; i<faceset.size(); i++) {
//     if(faceset[i]->face_match(n0, n1, n2))
//       return faceset[i];
//   }
//   return 0;
// }

// void Element::add_b_face(BoundaryFace *fc_in) {
//   if(faceset.empty())
//     faceset.reserve(2*master.nfaces());
//   faceset.push_back(fc_in);
// }

// #endif // DIM==3

#if DIM==2
std::vector<Edge*> *Element::perimeter() const {
  std::vector<Edge*> *brim = new std::vector<Edge*>(master.nedges());
  for(ElementCornerNodeIterator it=cornernode_iterator(); !it.end(); ++it) {
    (*brim)[it.index()] = new Edge(this,
				   it.mastercoord(), (it+1).mastercoord());
  }
  return brim;
}
#endif

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int Element::ndof() const {
  int n = 0;
  for(CleverPtr<ElementFuncNodeIterator> ni(funcnode_iterator());
      !ni->end(); ++*ni) {
    // int dn = ni.funcnode()->ndof();
    // std::cerr << "DOFs: " << dn << std::endl;
    n += ni->funcnode()->ndof();
  }

  return n;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==2
bool Element::exterior(const MasterCoord &a, const MasterCoord &b) const {
  // Are points a and b on the same exterior edge?
  if(!exterior_edges)
    return 0;
  // Let the master do the actual computation, so as to avoid roundoff errors.
  return master.exterior(a, b, *exterior_edges);
}

void Element::set_exterior(const Node &n0, const Node &n1) {
  if(!exterior_edges)
    exterior_edges = new std::vector<ElementCornerNodeIterator>;
  // find which edge these nodes are on.
  for(ElementCornerNodeIterator it=cornernode_iterator(); !it.end(); ++it) {
    const Node *node0 = it.node();
    const Node *node1 = (it+1).node();
    if((node0==&n0 && node1==&n1) || (node1==&n0 && node0==&n1)) {
      exterior_edges->push_back(it);
//       cerr << "Element::set_exterior it=" << it << endl;
//       cerr << "    n0=" << n0 <<     "    n1=" << n1 << endl;
//       cerr << " node0=" << *node0 << " node1=" << *node1 << endl;
      return;
    }
  }
}

void Element::dump_exterior() const {  // debugging
  if(!exterior_edges) return;
  std::cerr << "Element::dump_exterior " << *this << std::endl;
  for(std::vector<ElementCornerNodeIterator>::size_type i=0;
      i<exterior_edges->size(); i++)
    std::cerr << "   " << (*exterior_edges)[i] << std::endl;
}
#endif	// DIM==2

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==3

vtkSmartPointer<vtkIdList> Element::getPointIds() const {
  return get_skeleton_element()->getPointIds();
}

void Element::drawGridCell(vtkSmartPointer<GridSource> src, 
			   SimpleCellLayer *layer)
  const
{
  MeshGridSource *msrc = MeshGridSource::SafeDownCast(src);
  const FEMesh *mesh = msrc->Getmesh();
  double enhancement = msrc->GetEnhancement();
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  int n = nfuncnodes();
  points->Allocate(n, n);
  vtkSmartPointer<vtkIdList> ids = vtkSmartPointer<vtkIdList>::New();
  for(CleverPtr<ElementFuncNodeIterator> it(funcnode_iterator());
      !it->end(); ++*it)
    {
    int nidx = points->InsertNextPoint(
       it->funcnode()->displaced_position(mesh, enhancement).xpointer());
    ids->InsertNextId(nidx);
  }
  layer->newGrid(points, 1);
  layer->addCell(getCellType(), ids);
}

#endif	// DIM==3

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const Element &el) {
  os << el.master.name();
  for(ElementCornerNodeIterator it=el.cornernode_iterator(); !it.end(); ++it)
    os << " " << it.node()->position();
  return os;
}

Node* Element::getCornerNode(int i) const
{
  ElementCornerNodeIterator nit = cornernode_iterator();
  return (nit+i).node();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FaceBoundaryElement::FaceBoundaryElement(const MasterElement &me,
					 const std::vector<Node*> *nl)
  : Element(0, me, nl, 0),
    front_(0), back_(0)
{}

const std::string &FaceBoundaryElement::classname() const {
  static const std::string cname("FaceBoundaryElement");
  return cname;
}

const Element *FaceBoundaryElement::getBackBulk() const {
  return (back_ ? back_ : front_);
}

const Element *FaceBoundaryElement::getFrontBulk() const {
  return (front_ ? front_ : back_);
}

EdgeBoundaryElement::EdgeBoundaryElement(const MasterElement &me,
					 const std::vector<Node*> *nl)
  : Element(0, me, nl, 0)
{}

const std::string &EdgeBoundaryElement::classname() const {
  static const std::string cname("EdgeBoundaryElement");
  return cname;
}

bool Element::allNodesAreInSubProblem(const CSubProblem *subp) const {
  // Are all the nodes of this element in the given subproblem?  This
  // is only used for subdimensional elements at interfaces.  Bulk
  // elements must satisfy CSubProblem::contains().  TODO 3.1: This may
  // have to be done differently for elements with split nodes.
  for(ElementNodeIterator n=node_iterator(); !n.end(); ++n) {
    if(!subp->containsNode(n.node()))
       return false;
  }
  return true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef INTERFACELEMENTS

// TODO 3.1: InterfaceElement shouldn't be needed, since 1D and 2D
// elements in OOF3D are actual Elements.  The 1D and 2D elements
// might need some code from the old InterfaceElement class in order
// to implement split nodes, so the class hasn't actually been
// deleted.  It hasn't been updated for 3D, though.

InterfaceElement::InterfaceElement(CSkeletonElement *leftskelel, 
				   CSkeletonElement *rightskelel,
				   int segmentordernumber,
				   const MasterElement &me,
				   const std::vector<Node*> *nlleft, 
				   const std::vector<Node*> *nlright,
				   bool left_inorder,
				   bool right_inorder,
				   const Material *mat,
				   const std::vector<std::string>* 
				   pInterfacenames)
  : Element(leftskelel,me,nlleft,mat),
    nodelist2(*nlright), 
    left_nodes_in_interface_order(left_inorder),
    right_nodes_in_interface_order(right_inorder),
	  // cskeleton_element2(rightskelel),  // not yet used...
    _segmentordernumber(segmentordernumber),
    _interfacenames(*pInterfacenames),
    current_side(LEFT)
{
  abort();
}

InterfaceElement::~InterfaceElement()
{
}


const std::string &InterfaceElement::name() const
{
  //An InterfaceElement is associated with at least one interface or
  //boundary.
  // assert(_interfacenames.empty())
  return _interfacenames.back();
}

std::vector<std::string>* InterfaceElement::namelist() const
{
  std::vector<std::string> *ptmp = 
    new std::vector<std::string>(_interfacenames.size());
  //(*ptmp).insert(_interfacenames.begin(),_interfacenames.end());
  (*ptmp).assign(_interfacenames.begin(),_interfacenames.end());
  return ptmp;
}

// //Called by FEMesh::refreshInterfaceMaterials, which is called by
// //mesh.py->refreshMaterials
// void InterfaceElement::refreshInterfaceMaterial(const CSkeletonBase *skeleton)
// {
//   // TODO 3.1: Do we need a separate refreshInterfaceMaterial() method?
//   // This might need to do more work than refreshMaterial() does.
//   refreshMaterial(skeleton);
// }

bool InterfaceElement::isSubProblemInterfaceElement(
					    const CSubProblem* pSubProblem)
  const
{
  //TODO 3.1: Allow the edgement with split-nodes to be
  //located at subproblem or mesh boundaries
//   for(std::vector<Node*>::size_type i=0;
//       i<nnodes();i++)
  for(int i=0;i<nnodes();i++)
    {
      if(!pSubProblem->containsNode(get_nodelist()[i]))
	{
	  return false;
	}
    }
  for(std::vector<Node*>::size_type i=0;
      i<nodelist2.size();i++)
    {
      if(!pSubProblem->containsNode(nodelist2[i]))
	{
	  return false;
	}
    }
  return true;
}

void InterfaceElement::rename(const std::string& oldname, 
			      const std::string& newname)
{
  //TODO 3.1: Try find() and vector::assign(iter_begin,iter_end)
  for(std::vector<std::string>::size_type i=0;i<_interfacenames.size();i++) {
    if(_interfacenames[i]==oldname) {
      _interfacenames[i]=newname;
      return;
    }
  }
}

// Span retrieval functions.  Return the first and last node on the
// indicated side, in interface order.  If the nodes are not split,
// these two functions will have the same return value.

std::vector<const Node*> InterfaceElement::get_left_span() const {
  std::vector<const Node*> span = std::vector<const Node*>(2);
  if(left_nodes_in_interface_order) {
    span[0] = nodelist.front();
    span[1] = nodelist.back();
  }
  else {
    span[0] = nodelist.back();
    span[1] = nodelist.front();
  }
  return span;
}

std::vector<const Node*> InterfaceElement::get_right_span() const {
  std::vector<const Node*> span = std::vector<const Node*>(2);
 if(right_nodes_in_interface_order) {
    span[0] = nodelist2.front();
    span[1] = nodelist2.back();
  }
  else {
    span[0] = nodelist2.back();
    span[1] = nodelist2.front();
  } 
  return span;
}


ElementFuncNodeIterator *InterfaceElement::funcnode_iterator() const 
{
  return new InterfaceElementFuncNodeIterator(*this);
}


std::ostream &operator<<(std::ostream &os, const InterfaceElement &ed)
{
  os << ed.masterelement().name();
  os << " [";
  for(ElementNodeIterator it=ed.node_iterator(); !it.end(); ++it)
    os << " " << it.node()->position();
  os << " ], [";
  for(std::vector<Node*>::size_type i=0;i<ed.get_rightnodelist().size();i++)
    os << " " << ed.get_rightnodelist()[i]->position();
  os << " ], " << ed._segmentordernumber << ", " << ed.name();
  return os;
}

// The InterfaceElement's make_linear_system does two passes, one
// for the left side and one for the right side.  Sidedness is
// manifested in the behavior of the funcnode iterator.  Do this only
// if you have a material -- otherwise, your nodes are not split.

void InterfaceElement::make_linear_system(const CSubProblem *const subproblem,
					  double time,
					  const CNonlinearSolver *nlsolver,
					  LinearizedSystem &system) const
{
  std::vector<int> dofmap = localDoFmap();
  const Material *mat = material();
  
  if(mat) {
    // std::cerr << "Inside InterfaceElement::make_linear_system with a material." << std::endl;
    mat->begin_element(subproblem,this);
    int iorder = mat->integrationOrder(subproblem,this);

    current_side = LEFT;
    // std::cerr << "InterfaceElement::make_linear_system, left-side gp loop." << std::endl;
    for(GaussPointIterator gpt = integrator(iorder);
	!gpt.end();++gpt) {
      mat->make_linear_system( subproblem, this, gpt, dofmap, time,
			       nlsolver, system );
    }    

    current_side = RIGHT;
    // std::cerr << "InterfaceElement::make_linear_system, right-side gp loop." << std::endl;
    for(GaussPointIterator gpt = integrator(iorder);
	!gpt.end();++gpt) {
      mat->make_linear_system( subproblem, this, gpt, dofmap, time,
			       nlsolver, system );
    }
   
    current_side = LEFT;  // Return stateful objects to their initial state..

    mat->end_element(subproblem,this);
  }
}
					  
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The InterfaceElement jacobian is sort of brutally hacked -- we have
// a 2x2 matrix to work with, but we only need one, because we have
// (x,y) coords as a function of a single master-space variable.  So,
// just use the first column.  Also, we over-ride the determinant
// function, and use it to compute the magnitude, but we don't rename
// it, which is rather sleazy.  TODO MER: De-sleaze this.  

double InterfaceElement::jacobian(SpaceIndex i, 
				  SpaceIndex j, const GaussPoint &g) const
{
  double jac = 0.0;
  // TODO MER: This has to handle face elements in 3D, where j will be 0
  // or 1.  Is it possible to ensure that this routine will never be
  // called with the wrong j, so that we can eliminate the "if"?
  if (j==0) {
    for(ElementMapNodeIterator ni=mapnode_iterator(); !ni.end(); ++ni) { 
      jac += (ni.node()->position())[i]*ni.masterderiv(j,g);
    }
  }
  return jac;
}

double InterfaceElement::jacobian(SpaceIndex i, 
				  SpaceIndex j, const MasterCoord &mc)
  const
{
  double jac = 0.0;
  if (j==0) { 
    for(ElementMapNodeIterator ni=mapnode_iterator(); !ni.end(); ++ni) 
      jac += (ni.node()->position())[i]*ni.masterderiv(j,mc);
  }
  return jac;
}

// double InterfaceElement::det_jacobian(const GaussPoint &g) const {
//   double j00 = this->jacobian(0,0,g);
//   double j10 = this->jacobian(1,0,g);
//   return sqrt(j00*j00+j10*j10);
// }

// double InterfaceElement::det_jacobian(const MasterCoord &mc) const {
//   double j00 = this->jacobian(0,0,mc);
//   double j10 = this->jacobian(1,0,mc);
//   return sqrt(j00*j00+j10*j10);
// }


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


#endif // INTERFACEELEMENTS

//////////////////////////////////////////////////////////////////////////

std::string CoordElementData::class_("CoordElementData");
std::string CoordElementData::module_("ooflib.SWIG.engine.element");
