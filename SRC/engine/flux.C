// -*- C++ -*-
// $RCSfile: flux.C,v $
// $Revision: 1.73.2.12 $
// $Author: langer $
// $Date: 2014/12/14 22:49:19 $


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
#include "common/coord.h"
#include "common/pythonlock.h"
#include "common/smallmatrix.h"
#include "common/trace.h"
#include "common/vectormath.h"
#include "engine/csubproblem.h"
#include "engine/edge.h"
#include "engine/element.h"
#include "engine/equation.h"
#include "engine/femesh.h"
#include "engine/flux.h"
#include "engine/fluxnormal.h"
#include "engine/indextypes.h"
#include "engine/material.h"
#include "engine/nodalequation.h"
#include "engine/ooferror.h"
#include "engine/outputval.h"
#include "engine/smallsystem.h"
#include "engine/symmmatrix.h"

const std::string Flux::modulename_("ooflib.SWIG.engine.flux");

std::vector<Flux*> &Flux::allfluxes() {
  static std::vector<Flux*> all_fluxes;
  return all_fluxes;
}

Flux *getFluxByIndex(int index) {
  return Flux::allfluxes()[index];
}

int countFluxes() {
  return Flux::allfluxes().size();
}

Flux *Flux::getFlux(const std::string &name) {
  const std::vector<Flux*> &list = allfluxes();
  for(std::vector<Flux*>::size_type i=0; i<list.size(); i++) {
    if(list[i]->name() == name) {
      return list[i];
    }
  }
  throw ErrProgrammingError("Unknown Flux \"" + name + "\"",
			    __FILE__, __LINE__);
}

Flux::Flux(const std::string &nm, int d, int dvdim)
  : name_(nm),
    dim(d),
    divdim(dvdim)
{
  index_ = allfluxes().size();
  allfluxes().push_back(this);
}

bool operator==(const Flux &fluxa, const Flux &fluxb) {
  return fluxa.index_ == fluxb.index_;
}

bool operator!=(const Flux &fluxa, const Flux &fluxb) {
  return fluxa.index_ != fluxb.index_;
}

std::ostream &operator<<(std::ostream &os, const Flux &flux) {
  os << "Flux(" << flux.name() << ")";
  return os;
}

void Flux::addEquation(Equation *eqn) {
  // Add eqn to the list of equations in which this flux appears, but
  // first make sure that it's not already in the list.
  for(std::vector<Equation*>::size_type i=0; i<eqnlist.size(); i++) {
    if(eqnlist[i] == eqn) return;
  }
  eqnlist.push_back(eqn);
}

SmallSystem *Flux::initializeSystem(const Element *el) const {
  return new SmallSystem(dim, el->ndof());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &VectorFlux::classname() const {
  static std::string name_("VectorFlux");
  return name_;
}

const std::string &SymmetricTensorFlux::classname() const {
  static std::string name_("SymmetricTensorFlux");
  return name_;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO MER: Get rid of planarity arg in 3D.
IteratorP VectorFlux::iterator(Planarity planarity) const {
  int maxdim = 3;
  int mindim = 0;
#if DIM==2
  if(planarity == IN_PLANE) maxdim = 2;
  if(planarity == OUT_OF_PLANE) mindim = 2;
#endif	// DIM==2
  return IteratorP(new VectorFieldIterator(mindim, maxdim));
}

IteratorP VectorFlux::divergence_iterator() const {
  return IteratorP(new ScalarFieldIterator);
}

IteratorP VectorFlux::out_of_plane_iterator() const {
  return IteratorP(new OutOfPlaneVectorFieldIterator());
}

IndexP VectorFlux::componenttype() const {
  return IndexP(new VectorFieldIndex);
}

IndexP VectorFlux::getIndex(const std::string &str) const {
  return IndexP(new VectorFieldIndex(str[0] - 'x'));
}

IndexP VectorFlux::getOutOfPlaneIndex(const std::string &str) const {
  return IndexP(new OutOfPlaneVectorFieldIndex(str[0] - 'x'));
}

IndexP VectorFlux::divergence_componenttype() const {
  return IndexP(new ScalarFieldIndex);
}

IndexP VectorFlux::divergence_getIndex(const std::string&) const {
  return IndexP(new ScalarFieldIndex);
}

IteratorP SymmetricTensorFlux::iterator(Planarity planarity) const {
#if DIM==2
  if(planarity == IN_PLANE)
    return IteratorP(new SymTensorInPlaneIterator);
  if(planarity == OUT_OF_PLANE)
    return IteratorP(new SymTensorOutOfPlaneIterator);
#endif	// DIM==2
  return IteratorP(new SymTensorIterator);
}

IteratorP SymmetricTensorFlux::divergence_iterator() const
{
  return IteratorP(new VectorFieldIterator(0, DIM));
}

IteratorP SymmetricTensorFlux::out_of_plane_iterator() const {
  return IteratorP(new OutOfPlaneSymTensorIterator());
}

IndexP SymmetricTensorFlux::componenttype() const {
  return IndexP(new SymTensorIndex);
}

IndexP SymmetricTensorFlux::getIndex(const std::string &str) const {
  return IndexP(new SymTensorIndex(SymTensorIndex::str2voigt(str)));
}

IndexP SymmetricTensorFlux::getOutOfPlaneIndex(const std::string &str) const {
  return IndexP(new OutOfPlaneSymTensorIndex(SymTensorIndex::str2voigt(str)));
}

IndexP SymmetricTensorFlux::divergence_componenttype() const {
  return IndexP(new VectorFieldIndex);
}

IndexP SymmetricTensorFlux::divergence_getIndex(const std::string &str) const {
  return IndexP(new VectorFieldIndex(str[0] - 'x'));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

DoubleVec *Flux::evaluate(const FEMesh *mesh,
			  const Element *el,
			  const MasterPosition &pos) const
{
  DoubleVec *result = new DoubleVec(dim, 0.0);
  if (el->material()!=NULL) {

    if (!el->material()->self_consistent())
      throw ErrBadMaterial(el->material()->name());

    SmallSystem *fluxdata = initializeSystem(el);
    el->material()->find_fluxdata(mesh, el, this, pos, fluxdata);
    *result = fluxdata->fluxVector(); // copy!
    
    delete fluxdata;
  }
  return result;
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int Flux::eqn_integration_order(const CSubProblem *subp, const Element *el)
  const
{
  int order = 0;
  for(std::vector<Equation*>::size_type i=0; i<eqnlist.size(); ++i) {
    Equation *eqn = eqnlist[i];
    if(subp->is_active_equation(*eqn)) {
      int ord = eqn->integration_order(el);
      if(ord > order)
	order = ord;
    }
  }
  return order;
}

// Flux boundary condition uses the same mechanism as the stiffness
// matrix, only it makes its contribution to the boundary right-hand-side,
// rather than to the global stiffness matrix.
#if DIM==2
void Flux::boundary_integral(const CSubProblem *subp, LinearizedSystem *ls,
			     const BoundaryEdge *ed,
			     const EdgeGaussPoint &egp,
			     const FluxNormal *flxnormal)
  const 
{
  for(std::vector<Equation*>::size_type i=0; i<eqnlist.size(); i++) {
    Equation *eq = eqnlist[i];
    if(subp->is_active_equation(*eq)) {
      eq->boundary_integral(subp, ls, this, ed, egp, flxnormal);
    }
  }
}

#else // DIM==3
void Flux::boundary_integral(const CSubProblem *subp, LinearizedSystem *ls,
			 const Element *el, const GaussPoint &gpt,
			 const FluxNormal *flxnormal)
  const
{
  for(std::vector<Equation*>::const_iterator eqi=eqnlist.begin();
      eqi!=eqnlist.end(); ++eqi) 
    {
      Equation *eq = *eqi;
      if(subp->is_active_equation(*eq)) {
	eq->boundary_integral(subp, ls, this, el, gpt, flxnormal);
      }
    }
}
#endif // DIM==3

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// Contraction maps are used by the Divergence equation to map between
// equation components and flux components.  Since they're only really
// geometry-dependent, they can be precomputed at flux-construction
// time.  The same voigt stuff is already coded into the
// SymTensorIndex object, and in principle it could be re-used instead
// of re-created here, so that if voigt order ever changes, we only
// have to do change it in one place.
std::vector< std::vector<int> >
SymmetricTensorFlux::build_contraction_map()  {

  // This just constructs and returns the voigt index matrix:
  //   0 5 4
  //   5 1 3
  //   4 3 2

  std::vector<int> res0(3,0);
  // This 0 ----------^ is the equation component
  res0[0]=0;  // sigma_00
  res0[1]=5;  // sigma_10
  res0[2]=4;  // sigma_20

  std::vector<int> res1(3,0);
  // This 1 ----------^ is the equation component
  res1[0]=5;  // sigma_01
  res1[1]=1;  // sigma_11
  res1[2]=3;  // sigma_21

  std::vector<int> res2(3,0);
  res2[0]=4;  // sigma_02
  res2[1]=3;  // sigma_12
  res2[2]=2;  // sigma_22

  std::vector< std::vector<int> > res(3);
  res[0]=res0;
  res[1]=res1;
  res[2]=res2;

  return res;
}

std::vector< std::vector<int> > SymmetricTensorFlux::contraction_map_ = \
  SymmetricTensorFlux::build_contraction_map();

std::vector<int> SymmetricTensorFlux::contraction_map(int eqcomp) const {
  return SymmetricTensorFlux::contraction_map_[eqcomp];
}



// This outofplane_map presents the z-column of the tensor in
// Voigt-index order, which means that sigma_zz is first and sigma_xz
// is last.  This appears backwards, but because the rest of the code
// assumes Voigt order, it's the right thing to do here.  This
// ordering makes the conjugacy code's assumption of Voigt ordering
// correct, and allows it to symmetrize the resulting matrix
// correctly.
std::vector<int> SymmetricTensorFlux::build_outofplane_map()  {
  std::vector<int> res(3,0); //
  res[0]=2;  // sigma_22
  res[1]=3;  // sigma_12
  res[2]=4;  // sigma_02
  return res;
}

std::vector<int> SymmetricTensorFlux::outofplane_map_ = \
  SymmetricTensorFlux::build_outofplane_map();

const std::vector<int> &SymmetricTensorFlux::outofplane_map() const {
  return SymmetricTensorFlux::outofplane_map_;
}



std::vector<int> VectorFlux::build_contraction_map() {
 std::vector<int> res(3,0);
  res[0]=0; res[1]=1; res[2]=2;
  return res;
}

std::vector<int> VectorFlux::contraction_map_ = \
  VectorFlux::build_contraction_map();

std::vector<int> VectorFlux::contraction_map(int comp) const {
  return VectorFlux::contraction_map_; // Discard argument.
}



std::vector<int> VectorFlux::build_outofplane_map() {
  std::vector<int> res(1,0); //
  res[0]=2;  // Trivial map, z component.
  return res;
}

std::vector<int> VectorFlux::outofplane_map_ = \
  VectorFlux::build_outofplane_map();

const std::vector<int> &VectorFlux::outofplane_map() const {
  return VectorFlux::outofplane_map_;
}



// Local_boundary function is the analogue of the local_stiffness
// function, except that it's much simpler.  The core assumption here
// is that the components of the equation will match up with
// components of the flux normal in the obvious way, so that the sizes
// will match and the assignment will be straightforward.
#if DIM==2
void SymmetricTensorFlux::local_boundary(const BoundaryEdge *ed,
					 EdgeNodeIterator& edi,
					 const EdgeGaussPoint &egp,
					 const FluxNormal *flxnormal,
					 DoubleVec& rhs) 
  const
{

  const SymTensorFluxNormal *flxn =
    dynamic_cast<const SymTensorFluxNormal*>(flxnormal);
  // Check size of rhs -- has to be 2 for this flux.
  int rhssize = rhs.size();
  if (rhssize == SYMTEN_DIV_DIM) {
    if (flxn->size() == rhssize) { // Simple case, do the obvious.
      double sfvalue = edi.shapefunction(egp);
      rhs[0] = sfvalue * flxn->val[0];
      rhs[1] = sfvalue * flxn->val[1];
    }
  }
}
#else // DIM==3
void SymmetricTensorFlux::local_boundary(const ElementFuncNodeIterator& efni,
					 const GaussPoint &gpt,
					 const FluxNormal *flxnormal,
					 DoubleVec& rhs)
  const
{
  const SymTensorFluxNormal *flxn =
    dynamic_cast<const SymTensorFluxNormal*>(flxnormal);
  // Check size of rhs -- has to be 2 for this flux.
  int rhssize = rhs.size();
  assert(rhssize == SYMTEN_DIV_DIM);
  assert(rhssize == flxn->size());
  double sfvalue = efni.shapefunction(gpt);
  rhs[0] = sfvalue * flxn->val[0];
  rhs[1] = sfvalue * flxn->val[1];
  rhs[2] = sfvalue * flxn->val[2];
  // oofcerr << "SymmetricTensorFlux::local_boundary: rhs = "
  // 	  << rhs[0] << " " << rhs[1] << " " << rhs[2] << std::endl;
}
#endif // DIM==3


// Evaluate the dot product of the flux with the normal at
// the indicated edge gauss point.
#if DIM==2
OutputVal *SymmetricTensorFlux::contract(const FEMesh *mesh,
					 const Element *elmt,
					 const EdgeGaussPoint &egpt)
  const
 {
   OutputValue value = output( mesh, elmt, egpt );
   const SymmMatrix3 &valueRef =
     dynamic_cast<const SymmMatrix3&>(value.valueRef());
   Coord normal2 = egpt.normal();
   // Pretend the normal is a 3-vector so that we can dot it with the flux.
   DoubleVec normal3(3, 0.0);
   normal3[0] = normal2[0];
   normal3[1] = normal2[1];
   // Take the dot product.
   DoubleVec resultvec(valueRef*normal3);
   // Convert the result into an OutputVal, dropping the z-component.
   VectorOutputVal *result = new VectorOutputVal(2);
   (*result)[0] = resultvec[0];
   (*result)[1] = resultvec[1];
   return result;
//   DoubleVec *value = evaluate(mesh, elmt, egpt);
//   // voigt order, 00, 11, 22, 12, 02, 01
//   DoubleVec *result = new DoubleVec(divdim, 0.0);
//   Coord normal = egpt.normal();
//   (*result)[0] = (*value)[0]*normal[0] + (*value)[5]*normal[1];
//   (*result)[1] = (*value)[5]*normal[0] + (*value)[1]*normal[1];
//   delete value;  // deleting new'd DoubleVec from "evaluate".
//   return result;
}
#else  // DIM==3
OutputVal *SymmetricTensorFlux::contract(const FEMesh *mesh,
					 const Element *elmt,
					 const GaussPoint &gpt)
  const
{
  OutputValue value = output(mesh, elmt, gpt);
  const SymmMatrix3 &valueRef =
    dynamic_cast<const SymmMatrix3&>(value.valueRef());
  Coord normal = findNormal(elmt, gpt);
  Coord resultVec(valueRef*normal); // dot product
  VectorOutputVal *result = new VectorOutputVal(3);
  (*result)[0] = resultVec[0];
  (*result)[1] = resultVec[1];
  (*result)[2] = resultVec[2];
  return result;
}
#endif // DIM==3

#if DIM==2
FluxNormal *SymmetricTensorFlux::BCCallback(const Coord &pos,
					    double time,
					    const Coord &nrm,
					    const double distance,
					    const double fraction,
					    PyObject *wrapper,
					    const PyObject *pyfunction)
  const {

  PyObject *args;
  PyObject *result;
  Coord cres;

  PyGILState_STATE pystate = acquirePyLock();
  // Call the wrapper function, which is flux_locator, in bdycondition.py.
  args = Py_BuildValue((char*) "(Oddddddd)", pyfunction, pos[0], pos[1], time,
		       nrm[0], nrm[1], distance, fraction);
  result = PyEval_CallObject(wrapper, args);
  Py_DECREF(args);
  if(result) {
    if(PyTuple_Check(result)) {
      if(PyTuple_Size(result) == (Py_ssize_t) 2) {
	cres[0] = PyFloat_AsDouble(PyTuple_GetItem(result, (Py_ssize_t) 0));
	cres[1] = PyFloat_AsDouble(PyTuple_GetItem(result, (Py_ssize_t) 1));
      }
      else {
	// Only one "release" per possible control-flow path.
	releasePyLock(pystate);
	throw
	  ErrSetupError(
		       "SymmetricTensorFlux::BCCallback: Wrong size of tuple.");
      }
    }
    else {
      releasePyLock(pystate);
      throw ErrSetupError("SymmetricTensorFlux::BCCallback: Expected a tuple.");
    }
  }
  else {			// !result.  PyEval_CallObject failed.
    releasePyLock(pystate);
    pythonErrorRelay();
  }
  releasePyLock(pystate);
  Py_XDECREF(result);
  return new SymTensorFluxNormal(cres[0],cres[1]);
}
#else // DIM==3
FluxNormal *SymmetricTensorFlux::BCCallback(const Coord &pos,
					    double time,
					    const Coord &nrm,
					    PyObject *wrapper,
					    const PyObject *pyfunction)
  const {

  PyObject *args;
  PyObject *result;
  Coord cres;

  PyGILState_STATE pystate = acquirePyLock();
  args = Py_BuildValue((char*) "(Oddddddd)", pyfunction,
		       pos[0], pos[1], pos[2],
		       time,
		       nrm[0], nrm[1], nrm[2]);
  // Call the wrapper function, which is flux_locator, in bdycondition.py.
  result = PyEval_CallObject(wrapper, args);
  Py_DECREF(args);
  if(result) {
    if(PyTuple_Check(result)) {
      if(PyTuple_Size(result) == (Py_ssize_t) 3) {
	cres[0] = PyFloat_AsDouble(PyTuple_GetItem(result, (Py_ssize_t) 0));
	cres[1] = PyFloat_AsDouble(PyTuple_GetItem(result, (Py_ssize_t) 1));
	cres[2] = PyFloat_AsDouble(PyTuple_GetItem(result, (Py_ssize_t) 2));
      }
      else {
	// Only one "release" per possible control-flow path.
	releasePyLock(pystate);
	throw
	  ErrSetupError(
		       "SymmetricTensorFlux::BCCallback: Wrong size of tuple.");
      }
    }
    else {
      releasePyLock(pystate);
      throw ErrSetupError("SymmetricTensorFlux::BCCallback: Expected a tuple.");
    }
  }
  else {			// !result.  PyEval_CallObject failed.
    releasePyLock(pystate);
    pythonErrorRelay();
  }
  releasePyLock(pystate);
  Py_XDECREF(result);
  return new SymTensorFluxNormal(cres);
}
#endif // DIM==3

OutputValue Flux::output(const FEMesh *mesh, const Element *el,
			 const MasterPosition &pos) const
{
  // std::cerr << "Flux::output: pos=" << pos << " el=" << *el << std::endl;
  DoubleVec *fluxvals = evaluate( mesh, el, pos );
  OutputValue ov = newOutputValue();
  for(IteratorP it = iterator(ALL_INDICES); !it.end(); ++it) {
    ov[it] = (*fluxvals)[it.integer()];
  }
  delete fluxvals;
  return ov;
}

OutputValue SymmetricTensorFlux::newOutputValue() const {
  return OutputValue(new SymmMatrix3());
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

OutputValue VectorFlux::newOutputValue() const {
  return OutputValue(new VectorOutputVal(ndof()));
}


// The VectorFlux boundary condition calls the correct wrapper
// for its callback, and assumes the components match up
// trivially, in the absence of indications otherwise from
// the equation.
#if DIM==2
void VectorFlux::local_boundary(const BoundaryEdge *ed,
				EdgeNodeIterator& edi,
				const EdgeGaussPoint &egp,
				const FluxNormal *flxnormal,
				DoubleVec& rhs)
  const 
{
  const VectorFluxNormal *flxn =
    dynamic_cast<const VectorFluxNormal*>(flxnormal);
  int rhssize = rhs.size();
  if (rhssize == VEC_DIV_DIM) {
    if (flxn->size() == rhssize) {
      rhs[0] = edi.shapefunction(egp) * flxn->value();
    }
  }
}
#else // DIM==3
void VectorFlux::local_boundary(const ElementFuncNodeIterator& efni,
				const GaussPoint &gpt,
				const FluxNormal *flxnormal,
				DoubleVec& rhs)
  const
{
  const VectorFluxNormal *flxn =
    dynamic_cast<const VectorFluxNormal*>(flxnormal);
  int rhssize = rhs.size();
  assert(rhssize == VEC_DIV_DIM);
  assert(rhssize == flxn->size());
  rhs[0] = efni.shapefunction(gpt) * flxn->value();
}
#endif // DIM==3


// Evalute the dot product of the flux with the normal at the
// indicated gauss point.
#if DIM==2
OutputVal *VectorFlux::contract(const FEMesh *mesh,
				const Element *elmt,
				const EdgeGaussPoint &egpt)
  const
{
  OutputValue value = output( mesh, elmt, egpt );
  const VectorOutputVal &valueRef =
    dynamic_cast<const VectorOutputVal&>(value.valueRef());
  Coord normal = egpt.normal();
  DoubleVec normalvec(3);
  normalvec[0] = normal[0];
  normalvec[1] = normal[1];
  normalvec[2] = 0.0;
  return new ScalarOutputVal(valueRef.dot(normalvec));
//   DoubleVec *value = evaluate(mesh, elmt, egpt);
//   Coord normal = egpt.normal();
//   DoubleVec *result = new DoubleVec(divdim, 0.0);
//   (*result)[0] = (*value)[0]*normal[0] + (*value)[1]*normal[1];
//   return result;
}
#else  // DIM==3
OutputVal *VectorFlux::contract(const FEMesh *mesh,
				const Element *elmt,
				const GaussPoint &gpt)
  const
{
  // TODO: Why doesn't this return an OutputValue?
  OutputValue value = output(mesh, elmt, gpt);
  const VectorOutputVal &valueRef =
    dynamic_cast<const VectorOutputVal&>(value.valueRef());
  Coord normal = findNormal(elmt, gpt);
  return new ScalarOutputVal(valueRef.dot(normal));
}
#endif // DIM==3


#if DIM==2
FluxNormal *VectorFlux::BCCallback(const Coord &pos,
				   double time,
				   const Coord &nrm,
				   const double distance,
				   const double fraction,
				   PyObject *wrapper,
				   const PyObject *pyfunction)
  const 
{
  PyObject *args;
  PyObject *result;
  double dres = 0.0;

  PyGILState_STATE pystate = acquirePyLock();
  args = Py_BuildValue((char*) "(Oddddddd)",pyfunction, pos[0], pos[1], time,
		       nrm[0], nrm[1], distance, fraction);
  // Call the wrapper function, which is flux_locator, in bdycondition.py.
  result = PyEval_CallObject(wrapper, args);
  Py_DECREF(args);

  if(result) {
    if(PyTuple_Check(result)) {
      if(PyTuple_Size(result)==1) {
	dres = PyFloat_AsDouble(PyTuple_GET_ITEM(result, (Py_ssize_t) 0));
      }
      else {
	// Only one "release" per possible control-flow path.
	releasePyLock(pystate);
	throw
	  ErrSetupError("VectorFlux::BCCallback: Wrong size of tuple.");
      }
    }
    else {
      releasePyLock(pystate);
      throw ErrSetupError("VectorFlux::BCCallback: Expected a tuple.");
    }
  }

  Py_XDECREF(result);
  releasePyLock(pystate);

  return new VectorFluxNormal(dres);
}
#else // DIM==3
FluxNormal *VectorFlux::BCCallback(const Coord &pos,
				   double time,
				   const Coord &nrm,
				   PyObject *wrapper,
				   const PyObject *pyfunction)
  const 
{
  PyObject *args;
  PyObject *result;
  double dres = 0.0;

  PyGILState_STATE pystate = acquirePyLock();
  args = Py_BuildValue((char*) "(Oddddddd)", 
		       pyfunction,
		       pos[0], pos[1], pos[2],
		       time,
		       nrm[0], nrm[1], nrm[2]);
  // Call the wrapper function, which is flux_locator, in bdycondition.py.
  result = PyEval_CallObject(wrapper, args);
  Py_DECREF(args);

  if(result) {
    if(PyTuple_Check(result)) {
      if(PyTuple_Size(result)==1) {
	dres = PyFloat_AsDouble(PyTuple_GET_ITEM(result, (Py_ssize_t) 0));
      }
      else {
	// Only one "release" per possible control-flow path.
	releasePyLock(pystate);
	throw
	  ErrSetupError("VectorFlux::BCCallback: Wrong size of tuple.");
      }
    }
    else {
      releasePyLock(pystate);
      throw ErrSetupError("VectorFlux::BCCallback: Expected a tuple.");
    }
  }

  Py_XDECREF(result);
  releasePyLock(pystate);

  return new VectorFluxNormal(dres);
}
#endif	// DIM==3
