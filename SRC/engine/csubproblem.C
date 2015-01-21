// -*- C++ -*-
// $RCSfile: csubproblem.C,v $
// $Revision: 1.65.2.18 $
// $Author: fyc $
// $Date: 2015/01/07 15:53:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include <map>
#include <utility>		// for std::pair
#include <vector>

#include "common/cleverptr.h"
#include "common/coord.h"
#include "common/lock.h"
#include "common/printvec.h"	// debugging
#include "common/progress.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "common/IO/oofcerr.h"
#include "common/vectormath.h"
#include "engine/cconjugate.h"
#include "engine/cnonlinearsolver.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/flux.h"
#include "engine/linearizedsystem.h"
#include "engine/material.h"
#include "engine/meshiterator.h"
#include "engine/nodalequation.h"
#include "engine/node.h"
#include "engine/ooferror.h"
#include "engine/property.h"
//AMR subproblem
#include "engine/cscpatch.h"
#include "engine/nodalfluxes.h"
#include "engine/nodalscpatches.h"


typedef std::pair<FuncNode::FieldSet, FuncNode::EquationSet> FEPair;
// std::pair has an operator< defined in terms of its template args'
// operator<, and FieldSet and EquationSet have operator<, so
// LocalMapDict doesn't need an explicitly assigned comparison
// operator template arg.
typedef std::map<FEPair, std::vector<int> > LocalMapDict;

long CSubProblem::globalCSubProblemCount = 0;
SLock globalCSubProblemCountLock;

CSubProblem::CSubProblem()
  : rwlock(0),
    mesh(0),
    precomputeRequired(true),
    n_active_eqn(0),
    n_active_field(0),
    staticStepper_(true)
{
  globalCSubProblemCountLock.acquire();
  ++globalCSubProblemCount;
  globalCSubProblemCountLock.release();
}

CSubProblem::~CSubProblem() {
  // delete cached lists of active fluxes and equations
  for(ActiveFluxMap::iterator it = active_flux_map.begin();
      it!=active_flux_map.end(); ++it)
      delete it->second;
  for(ActiveEqnMap::iterator it = active_equation_map.begin();
      it!=active_equation_map.end(); ++it)
      delete it->second;

  //AMR subproblem
  std::map<const int, NodalSCPatches*>::iterator piter;
  for(piter=scpatches.begin(); piter!=scpatches.end(); piter++)
    delete piter->second;

  std::map<const int, NodalFluxes*>::iterator fiter;
  for(fiter=recovered_fluxes.begin(); fiter!=recovered_fluxes.end(); fiter++)
    delete fiter->second;

  globalCSubProblemCountLock.acquire();
  --globalCSubProblemCount;
  globalCSubProblemCountLock.release();
}

void CSubProblem::set_mesh(FEMesh *msh) {
  mesh = msh;
}

void CSubProblem::set_nnodes(int n) {
  nNodes_ = n;
}

long get_globalCSubProblemCount() {
  return CSubProblem::globalCSubProblemCount;
}

CMicrostructure *CSubProblem::get_microstructure() const {
  return mesh->get_microstructure();
}

void CSubProblem::setStaticStepper(bool x) { 
  staticStepper_ = x; 
}

int CSubProblem::nelements() const {
  return element_iterator().size();
}

int CSubProblem::nnodes() const {
  return node_iterator().size();
}

int CSubProblem::nfuncnodes() const {
  return funcnode_iterator().size();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSubProblem::EquationData::EquationData()
  : active(0)
{}

void CSubProblem::activate_equation(Equation &eqn) {
  // Trace("CSubProblem::activate_equation " + eqn.name());
  int index = eqn.index();
  // Make sure that there's an EquationData entry for this Equation
  if(index >= int(eqndata.size())) {
    eqndata.resize(index+1);
  }
  if(!eqndata[index].active) {
    eqndata[index].active = true; // Mark the Equation as active
    ++n_active_eqn; // Total number of active NodalEquations at each Node.

    // Create NodalEquations for this Equation in each Node.  This
    // also updates the Nodes' EquationSets.
    for(FuncNodeIterator ni=funcnode_iterator(); !ni.end(); ++ni) {
      ni.node()->addEquation(mesh, eqn);
    }
    // Activate fluxes required for this Equation
    eqn.activate_fluxes(this);
  }
}

void CSubProblem::deactivate_equation(Equation &eqn) {
  if(is_active_equation(eqn)) {
    int index = eqn.index();
    eqndata[index].active = false;
    for(FuncNodeIterator ni=funcnode_iterator(); !ni.end(); ++ni) {
      ni.node()->removeEquation(mesh, eqn);
    }
    // perform garbage collection on the nodaleqn list
    mesh->clean_nodaleqn();
    --n_active_eqn;
    eqn.deactivate_fluxes(this);
  }
}

// TODO 3.1: PLASTICITY How is is_active_equation used?  Should it examine
// each Node's EquationSet, or just check the CSubProblem's
// EquationData.active?  This may need a closer look when we get
// automatically activated auxiliary equations, esp. in
// Flux::make_stiffness and related functions.  Most other invocations
// of is_active_equation are used to determine what equations the user
// has explicitly activated.

// is_active_equation is used by Material::precompute when building
// the Material's active_eqns list, which is used in
// Material::make_linear_system.  There's a TODO 3.1 in that routine about
// the insufficiency of this list in the presence of point-wise
// constraint equations.

bool CSubProblem::is_active_equation(const Equation &eqn) const {
  std::vector<EquationData>::size_type index = eqn.index();
  return (index < eqndata.size()) && eqndata[index].active;
}

int CSubProblem::n_active_eqns() const {
  return n_active_eqn;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Flux bookkeeping.

// activate_flux is called indirectly by activate_equation, which is
// called by menu commands.  If a flux is active, then the
// corresponding divergence equation is being solved.

void CSubProblem::activate_flux(const Flux &flux) {
  std::vector<int>::size_type index = flux.index();
  if(index >= active_flux.size()) {
    active_flux.resize(index+1, 0);
  }
  ++active_flux[index];
}

void CSubProblem::deactivate_flux(const Flux &flux) {
  std::vector<int>::size_type index = flux.index();
  if(index < active_flux.size()) {
    if(active_flux[index] > 0)
      --active_flux[index];
  }
}

bool CSubProblem::is_active_flux(const Flux &flux) const {
  std::vector<int>::size_type index = flux.index();
  if(index < active_flux.size()) {
    return active_flux[index] > 0;
  }
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Field stuff

// activate, etc, for Fields have to be routed through Field virtual
// functions, because they have to know if the Field is a
// CompoundField or not.  The routines that do the real work are
// CSubProblem::do_activate, etc.

CSubProblem::FieldData::FieldData()
  : active(0),
    defined(0)
{}

bool CSubProblem::define_field(const Field &field) {
  if(!is_defined_field(field)) {
    field.define(this);
    return true;
  }
  return false;
}

void CSubProblem::undefine_field(const Field &field) {
  field.undefine(this);
}

void CSubProblem::activate_field(const Field &field) {
  field.activate(this);
}

void CSubProblem::deactivate_field(const Field &field) {
  field.deactivate(this);
}

void CSubProblem::do_define_field(const Field &field) {
  requirePrecompute();
  std::vector<FieldData>::size_type index = field.index();
  if(fielddata.size() <= index) {
    fielddata.resize(index+1);
  }
  FieldData &fdata = fielddata[index];
  if(!fdata.defined) {
    fdata.defined = true;
    mesh->reserveMoreDoFs(nfuncnodes()*field.ndof());
    for(FuncNodeIterator ni=funcnode_iterator(); !ni.end(); ++ni) {
//       oofcerr << "CSubProblem::do_define_field: adding " << field
// 		<< " at node " << *ni.node() << std::endl;
      ni.node()->addField(mesh, field);
    }
  }
}

void CSubProblem::do_undefine_field(const Field &field) {
  requirePrecompute();
  if(is_defined_field(field)) {
    if(is_active_field(field)) {
      deactivate_field(field);
    }
    std::vector<FieldData>::size_type index = field.index();
    if(index < fielddata.size()) {
      fielddata[index].defined = false;
      for(FuncNodeIterator ni=funcnode_iterator(); !ni.end(); ++ni) {
	ni.node()->removeField(mesh, field);
      }
      mesh->clean_doflist();
    }
  }
}

// Function to copy a field from another CSubProblem.  The other
// CSubProblem must have the same geometry, i.e. the same-indexed
// funcnodes must be in the same location, and the field must be
// defined.  Called by meshmenu.copyMesh.

void CSubProblem::acquire_field_data(Field &field, const CSubProblem *other) {
  for(FuncNodeIterator i=funcnode_iterator(); !i.end(); ++i) {
    for(int d=0; d<field.ndof(); ++d) {
      if(i.node()->hasField(field)) {
	field(i.node(), d)->value(mesh) =
	  field(other->mesh->getFuncNode(i.count()), d)->value(other->mesh);
      }
    }
  }
}

bool CSubProblem::is_defined_field(const Field &field) const {
  return (field.index() < fielddata.size())
    && fielddata[field.index()].defined;
}

void CSubProblem::do_activate_field(const Field &field) {
  if(!is_active_field(field)) {
    n_active_field++;
    FieldData &fdata = fielddata[field.index()];
    fdata.active = true;
  }
}

void CSubProblem::do_deactivate_field(const Field &field) {
  if(is_active_field(field)) {
    n_active_field--;
    fielddata[field.index()].active = false;
  }
}

bool CSubProblem::is_active_field(const Field &field) const {
  return (field.index() < fielddata.size()) && fielddata[field.index()].active;
}

int CSubProblem::n_active_fields() const {
  return n_active_field;
}

#if DIM==2
bool CSubProblem::in_plane(const Field &field) const {
  return mesh->in_plane(field);
//   return (field.index() < fielddata.size())
//     && fielddata[field.index()].in_plane;
}
#endif // DIM==2

// Call the given function on each Field defined in the SubProblem.
// The arguments to the function are the Field, its time derivative
// Field, and a bool indicating whether or not the time derivative is
// actually defined.

void CSubProblem::fieldLooper(
		      void (*fn)(void *, const Field&, const Field&, bool),
		      void *data)
const
{
  const std::vector<CompoundField*> *fields = all_compound_fields();
  for(unsigned int f=0; f<fields->size(); ++f) {
    CompoundField *field = (*fields)[f];
    if(is_defined_field(*field)) {
      Field *tdfield = field->time_derivative();
      bool tddefined = is_defined_field(*tdfield);
      (*fn)(data, *field, *tdfield, tddefined);
#if DIM==2
      Field *zfield = field->out_of_plane();
      Field *tdzfield = field->out_of_plane_time_derivative();
      (*fn)(data, *zfield, *tdzfield, tddefined);
#endif	// DIM==2
    }
  }
  delete fields;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Return a list of all the defined compound fields.  Compound fields
// are the ones that correspond directly to physical fields.

std::vector<CompoundField*>* CSubProblem::all_compound_fields() const {
  std::vector<CompoundField*>* flist = new std::vector<CompoundField*>;
  std::vector<CompoundField*> &allfields = CompoundField::allcompoundfields();
  flist->reserve(fielddata.size());
  for(std::vector<CompoundField*>::size_type i=0; i<allfields.size(); i++) {
    // TODO 3.1: PLASTICITY This only picks up explicitly defined Fields.
    // Should it look at Node::fieldset instead?  Should there be
    // another function that retrieves implicit Fields that may not be
    // in CSubProblem::fielddata?
    if(is_defined_field(*allfields[i]))
      flist->push_back(allfields[i]);
  }
  return flist;
}

int CSubProblem::ndof() const {
  std::vector<CompoundField*> *fields = all_compound_fields();
  int ncomponents = 0;
  for(std::vector<CompoundField*>::const_iterator f=fields->begin();
      f<fields->end(); ++f)
    {
      const CompoundField &field = *(*f);
      ncomponents += 
	field.ndof()
	+ field.time_derivative()->ndof()
#if DIM==2
	+ field.out_of_plane()->ndof()
	+ field.out_of_plane_time_derivative()->ndof()
#endif // DIM==2
	;
    }
  delete fields;
  return ncomponents*nNodes_;
}

// Likewise for Equation objects.
std::vector<Equation*>* CSubProblem::all_equations() const {
  std::vector<Equation*> *eqlist = new std::vector<Equation*>;
  std::vector<Equation*> &alleqns = Equation::all();
  eqlist->reserve(eqndata.size());
  for(std::vector<Equation*>::size_type i=0; i<alleqns.size(); i++) {
    if(is_active_equation(*alleqns[i]))
      eqlist->push_back(alleqns[i]);
  }
  return eqlist;
}

int CSubProblem::neqn() const {
  std::vector<Equation*> *eqns = all_equations();
  int n = 0;
  for(std::vector<Equation*>::const_iterator e=eqns->begin(); e<eqns->end(); ++e)
    {
      n += (*e)->dim();
    }
  return n*nNodes_;
}

std::vector<Flux*>* CSubProblem::all_fluxes() const {
  std::vector<Flux*> *fluxlist = new std::vector<Flux*>;
  std::vector<Flux*> &allfluxen = Flux::allfluxes();
  for(std::vector<Flux*>::size_type i=0; i<allfluxen.size(); i++) {
    if(is_active_flux(*allfluxen[i]))
      fluxlist->push_back(allfluxen[i]);
  }
  return fluxlist;
}

std::vector<Flux*> CSubProblem::allFluxes() const {  // non-swigged version.
  std::vector<Flux*> fluxlist;
  std::vector<Flux*> &allfluxen = Flux::allfluxes();
  for(std::vector<Flux*>::size_type i=0; i<allfluxen.size(); i++) {
    if(is_active_flux(*allfluxen[i]))
      fluxlist.push_back(allfluxen[i]);
  }
  return fluxlist;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::vector<Flux*> &CSubProblem::active_fluxes(const Material *matl) {
  ActiveFluxMap::iterator it = active_flux_map.find(matl);
  if(it == active_flux_map.end()) {
    std::vector<Flux*> *vec = new std::vector<Flux*>();
    active_flux_map[matl] = vec;
    return *vec;
  }
  return *it->second;
}

const std::vector<Flux*> &CSubProblem::active_fluxes(const Material *matl)
  const
{
  ActiveFluxMap::const_iterator it = active_flux_map.find(matl);
  if(it == active_flux_map.end()) {
    throw ErrProgrammingError("Didn't find flux map for material!",
			      __FILE__, __LINE__);
  }
  return *it->second;
}

std::vector<Equation*> &CSubProblem::active_equations(const Material *matl) {
  ActiveEqnMap::iterator it = active_equation_map.find(matl);
  if(it == active_equation_map.end()) {
    std::vector<Equation*> *vec = new std::vector<Equation*>();
    active_equation_map[matl] = vec;
    return *vec;
  }
  return *it->second;
}

const std::vector<Equation*> &
CSubProblem::active_equations(const Material *matl)
  const
{
  ActiveEqnMap::const_iterator it = active_equation_map.find(matl);
  if(it == active_equation_map.end()) {
    throw ErrProgrammingError("Didn't find equation map for material!",
			      __FILE__, __LINE__);
  }
  return *it->second;
}

void CSubProblem::clear_active_fluxes(const Material *matl) {
  ActiveFluxMap::iterator it = active_flux_map.find(matl);
  if(it != active_flux_map.end()) {
    delete it->second;
    active_flux_map.erase(it);
  }
}

void CSubProblem::clear_active_equations(const Material *matl) {
  ActiveEqnMap::iterator it = active_equation_map.find(matl);
  if(it != active_equation_map.end()) {
    delete it->second;
    active_equation_map.erase(it);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Construct mesh2subpDoFMap, mesh2subpEqnMap, and dof2Deriv, which
// are the parts of the LinearizedSystem mapping machinery that really
// belong to the Subproblem.

void CSubProblem::mapFields() {
  int n = mesh->ndof();
  mesh2subpDoFMap.reset(n);
  mesh2subpEqnMap.reset(n);
  fieldLooper(&CSubProblem::mapField, this);
}

void CSubProblem::mapField(void *data,
			   const Field &field, const Field &tdfield,
			   bool tddefined)
{
  ((CSubProblem*) data)->mapField_(field, tdfield, tddefined);
}

void CSubProblem::mapField_(const Field &field, const Field &tdfield,
			    bool tddefined)
{
  for(FuncNodeIterator nd=funcnode_iterator(); !nd.end(); ++nd) {
    FuncNode *node = nd.node();
    for(int i=0; i<field.ndof(); i++) { // loop over field components
      int dofindex = field(node, i)->dofindex(); // global index
      int eqnindex = global_dof2eqn_map[dofindex];
      int mappedDoFIndx = mesh2subpDoFMap.add(dofindex);
      if(eqnindex != -1)	// eqn is inactive if eqnindex == -1
	mesh2subpEqnMap.add(eqnindex);
      if(tddefined) {
	int tdindx = mesh2subpDoFMap.add(tdfield(node, i)->dofindex());
	dof2Deriv[mappedDoFIndx] = tdindx;
      }
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Caches of often-used property-dependent flags.  The cache is
// constructed by Material.precompute (defined in material.spy).
// Since the cache reconstructed before each Material is used in a
// computation, it's unnecessary to invalidate the cache when
// Materials or Properties change.

// A property is active if it's computable and is used in an active
// Flux or Equation.

void CSubProblem::cache_active_prop(const Property *prop, bool active) {
  propActivity[prop] = active;
}

bool CSubProblem::currently_active_prop(const Property *prop) const {
  PropertyFlagCache::const_iterator which = propActivity.find(prop);
  if(which != propActivity.end())
    return (*which).second;
  return false;
}

// TODO OPT: find_computable_prop and currently_computable_prop
// weren't being used, so they've been commented out.  Find out if
// caching the computability is really worth the effort.

// void CSubProblem::find_computable_prop(const Property *prop) {
//   propComputability[prop] = prop->is_computable(this);
// }

// bool CSubProblem::currently_computable_prop(const Property *prop) const {
//   PropertyFlagCache::const_iterator which = propComputability.find(prop);
//   if(which != propComputability.end())
//     return (*which).second;
//   return false;
// }

void CSubProblem::cache_nonlinearity_prop(const Property *prop, bool nonlin) {
  propNonlinearity[prop] = nonlin;
}

bool CSubProblem::currently_nonlinear_prop(const Property *prop) const {
  PropertyFlagCache::const_iterator which = propNonlinearity.find(prop);
  if(which != propNonlinearity.end())
    return (*which).second;
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int CSubProblem::getDerivIndex(int dofindex) const {
  // Return the subproblem derivative index corresponding to a
  // subproblem DoF index, or -1 if there is no defined derivative.
  DoFMap::TranslationMap::const_iterator i = dof2Deriv.find(dofindex);
  if(i == dof2Deriv.end())
    return -1;
  return (*i).second;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSubProblem::set_slaveDoF(int dofindex) {
  slaveDoFs.insert(dofindex);
}

void CSubProblem::clear_slaveDoFs() {
  slaveDoFs.clear();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool CSubProblem::set_meshdofs(const DoubleVec *dofs) const {
  return mesh->set_dofvalues(*dofs, mesh2subpDoFMap, get_slaveDoFs());
}

DoubleVec *CSubProblem::get_meshdofs() const {
  int n = mesh2subpDoFMap.range();
  DoubleVec *dofs = new DoubleVec(n, 0.0);
  mesh->get_dofvalues(*dofs, mesh2subpDoFMap);
  return dofs;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

LinearizedSystem *CSubProblem::new_linear_system(double time) {
  // Make sure that indices in the master equation list and dof list
  // in the mesh are contiguous.
  mesh->housekeeping();

  LinearizedSystem *linearsystem = new LinearizedSystem(this, time);

  return linearsystem;
}

void CSubProblem::make_linear_system(LinearizedSystem *linearsystem,
				     const CNonlinearSolver *nlsolver)
  const
{
  double time = linearsystem->time();

  DefiniteProgress *progress =
    dynamic_cast<DefiniteProgress*>(getProgress("Building linear system",
						DEFINITE));

  // TODO 3.1: TDEP The first thing we want to do for each element is
  // determine the integration order, so we know how many gausspoints
  // there are, and then signal to all the elements, so they can
  // re-interpolate their pointwise fields, if any.

  // Order of integration is implicit in the element gausspoints,
  // which have been set (along with any gpdofs) by the mesh.
  for(ElementIterator ei=element_iterator(); !ei.end() && !progress->stopped();
      ++ei)
    {
      ei.element()->make_linear_system( this, time, nlsolver, *linearsystem );
      progress->setFraction( float(ei.count()+1)/float(ei.size()) );
      progress->setMessage(to_string(ei.count()+1) + "/" + to_string(ei.size())
			   + " elements"
			   );
    }

  //Interface branch
  //TODO 3.1: Write an InterfaceElementIterator for the subproblem.
  unsigned int n = mesh->edgement.size();
  for(std::vector<Element*>::size_type i=0; i<n && !progress->stopped(); i++) {
    if(mesh->edgement[i]->allNodesAreInSubProblem(this)) {
      mesh->edgement[i]->make_linear_system( this, time, nlsolver, 
					     *linearsystem );
    }
    progress->setFraction(double(i+1)/n);
    progress->setMessage(to_string(i+1) + "/" + to_string(n) + " edges");
  }
  progress->finish();
  if(progress->stopped()) {
    throw ErrInterrupted();
  }

  linearsystem->consolidate();

  // oofcerr << "CSubProblem::make_linear_system exiting." << std::endl;
  // linearsystem->dumpAll("junk.out",time,"MLS exit");
} // end of 'CSubProblem::make_linear_system'

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Preliminary -- no housekeeping, just run the element's
// post-equilibration loop.
void CSubProblem::post_process() {
  DefiniteProgress *progress =
    dynamic_cast<DefiniteProgress*>(getProgress("Postprocessing", DEFINITE));
  for(ElementIterator ei=element_iterator(); !ei.end(); ++ei) {
    ei.element()->post_process(this);
    progress->setFraction(float(ei.count()+1)/float(ei.size()));
    progress->setMessage(to_string(ei.count()+1) + "/" + to_string(ei.size())
			 + " elements");
  }

  //Interface branch
  //TODO 3.1: Write an InterfaceElementIterator for the subproblem.
  unsigned int n = mesh->edgement.size();
  for(std::vector<Element*>::size_type i=0; i<n; i++) {
    if(mesh->edgement[i]->allNodesAreInSubProblem(this))
	  mesh->edgement[i]->post_process(this);
    progress->setFraction(double(i+1)/n);
    progress->setMessage(to_string(i+1) + "/" + to_string(n) + " edges");
  }
  progress->finish();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Routines for symmetrizing the matrix (or trying to), using
// conjugacy data.

// Utility function used by getLocalMap_.

void mapLocalNonConjField(const Field &field, std::vector<int> &lmap,
			  int &lowestrow, FuncNode::FieldSet &fieldset)
{
  for(IteratorP fieldcomp = field.iterator(ALL_INDICES); !fieldcomp.end();
      ++fieldcomp)
    {
      if(lowestrow == -1 || lowestrow >= (int) lmap.size())
	throw ErrSetupError("Too many degrees of freedom! Not enough equations?");
      int dof_indx = fieldset.offset(&field) + fieldcomp.integer();
      lmap[lowestrow] = dof_indx;
      while(lmap[lowestrow] == -1 and lowestrow < (int) lmap.size())
	++lowestrow;
    }
}

// See if a local conjugacy map has already been constructed for the
// given fieldset and nodeset, and construct a new one if necessary.
// (In this context, "local" means "local to a Node".)  The local map
// is a vector of ints.  For the i^th equation in a FuncNode's list of
// NodalEquations, localmap[i] is the index of the conjugate degree of
// freedom in the Node's list of DegreeOfFreedoms.  If there is no
// conjugate degree of freedom, localmap[i] is -1.

struct FieldCompare {
  bool operator()(const Field *f1, const Field *f2) const {
    return f1->name() < f2->name();
  }
};

static std::vector<int> &getLocalMap_(FuncNode::FieldSet &fieldset,
				      FuncNode::EquationSet &eqnset,
				      LocalMapDict &localmaps,
				      CSubProblem *subproblem,
				      const std::vector<CConjugatePair*> &pairs)
{
  FEPair key(fieldset, eqnset);
  LocalMapDict::iterator i = localmaps.find(key);
  if(i == localmaps.end()) {
    // create a new map
    std::vector<int> lmap(eqnset.dimsum(), -1);
    std::set<const Field*, FieldCompare> usedfields;
    for(std::vector<CConjugatePair*>::const_iterator p=pairs.begin();
	p < pairs.end(); ++p)
      {
	const Field &field = *(*p)->get_field();
	const Equation &eqn = *(*p)->get_equation();
	if(subproblem->is_active_field(field) &&
	   subproblem->is_active_equation(eqn))
	  {
	    const FieldIndex &equationcomp = *(*p)->get_equation_component();
	    const FieldIndex &fieldcomp = *(*p)->get_field_component();
	    int eqn_indx = eqnset.offset(&eqn) + equationcomp.integer();
	    int dof_indx = fieldset.offset(&field) + fieldcomp.integer();
	    lmap[eqn_indx] = dof_indx;
	    usedfields.insert(&field);
	  }
      }
    // Check that all active Fields and Equations have been
    // included. If a Field has no conjugacy data, it still has to be
    // mapped.
    // First, find the lowest available row number.
    int lowestrow = -1;
    for(unsigned int j=0; j<lmap.size(); j++) {
      if(lmap[j] == -1) {
	lowestrow = j;
	break;
      }
    }
    // If lowestrow == -1 here, then all equation slots have been
    // filled, which is ok if there are no unmapped Fields.  We don't
    // know that yet.

    const std::vector<CompoundField*> *fields =
      subproblem->all_compound_fields();
    for(unsigned int f=0; f<fields->size(); ++f) {
      CompoundField &field = *(*fields)[f];
      if(subproblem->is_active_field(field)) {
	std::set<const Field*>::iterator look = usedfields.find(&field);
	if(look == usedfields.end()) {
	  mapLocalNonConjField(field, lmap, lowestrow, fieldset);
#if DIM==2
	  Field *oop = field.out_of_plane();
	  if(subproblem->is_active_field(*oop)) {
	    // Check if oop is in usedfields?
	    mapLocalNonConjField(*oop, lmap, lowestrow, fieldset);
	  }
#endif
	}
      }	// end if field is active
    } // end loop over fields
    delete fields;

    localmaps.insert(LocalMapDict::value_type(key, lmap)); // copies lmap

    return localmaps[key];	// returns reference to copy in localmaps
  } // found existing map
  else {
    return (*i).second;		// reuse an existing map
  }
}

void CSubProblem::set_equation_mapping(
			  const std::vector<CConjugatePair*> *conjugacylist)
{
  // Build a mapping array such that, given a global dof index i, it
  // returns the global nodal equation index of the conjugate
  // equation, if there is one, or the nodal equation index of some
  // other (unique) equation, if there is no conjugate.  Using this
  // map to set the order of the rows of the K, C, and M matrices will
  // make those matrices symmetric, if possible.

  // Make sure that indices in the master equation list and dof list
  // in the mesh are contiguous.
  mesh->housekeeping();

  global_dof2eqn_map.clear();
  global_dof2eqn_map.resize(mesh->dof.size(), -1);

  LocalMapDict localmaps;
  for(FuncNodeIterator iter=funcnode_iterator(); !iter.end(); ++iter) {
    FuncNode *node = iter.node();

    std::vector<NodalEquation*> &eqnlist = node->eqnlist;
    // Get the localmap, which indicates the conjugacy relations
    // between nodal equations and degrees of freedom in the Node.
    // Localmap's domain is nodal equations, and its range is nodal
    // DOFs.
    std::vector<int> &localmap = getLocalMap_(node->fieldset,
					      node->equationset,
					      localmaps, this, *conjugacylist);
    for(std::vector<NodalEquation*>::size_type i=0; i<eqnlist.size(); ++i) {
      // Only do stuff if this mapping makes sense.
      if (localmap[i]!=-1) {
	NodalEquation* neq = eqnlist[i];
	int row = neq->ndq_index(); // Index in master stiffness mtx
	int whichdof = localmap[i];
	DegreeOfFreedom *dof = (node->doflist)[whichdof];
	int col = dof->dofindex();  // Also in master stiffness mtx

	global_dof2eqn_map[col] = row;
      }
    } // end loop over nodal equations
  } // end loop over nodes
} // set_equation_mapping

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Return a list of all the Materials used by this subproblem.  This
// generic function is inefficient, and is re-implemented in
// subproblem subclasses.

MaterialSet *CSubProblem::getMaterials() const {
  MaterialSet *mset = new MaterialSet;
  for(ElementIterator ei=element_iterator(); !ei.end(); ++ei) {
    const Material *matl = ei.element()->material();
    if(matl) {
      mset->insert(matl);
    }
  }

  // Make sure to include surface materials in interfaces.
  unsigned int ne = mesh->edgement.size();
  for(std::vector<Element*>::size_type i=0; i<ne; ++i) { 
    if(mesh->edgement[i]->allNodesAreInSubProblem(this)) {
      const Material *matl = mesh->edgement[i]->material();
      if(matl) {
	mset->insert(matl);
      }
    }
  }
  return mset;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// dump_dof and dump_eqn are commented out because they require const
// iterators, which I'm too lazy to write just now.

// void CSubProblem::dump_dof() const {
//   for(FuncNodeIterator i=funcnode_iterator(); !i.end(); ++i) {
//     const FuncNode &node = *i.node();
//     std::cout << "node = " << node << std::endl;
//     for(std::vector<Field*>::size_type f=0; f<Field::all().size(); f++) {
//       const Field &field = *Field::all()[f];
//       if(field.is_defined(this)) {
// 	for(int j=0; j<field.ndof(); j++) {
// 	  std::cout << "\t" << field.name() << "[" << j << "] dof="
// 	       << *field(node, j) << std::endl;
// 	}
//       }
//     }
//     for(std::vector<Equation*>::size_type e=0;e<Equation::all().size();e++){
//       const Equation &eqn = *Equation::all()[e];
//       if(eqn.is_active(this)) {
// 	for(int j=0; j<eqn.dim(); j++) {
// 	  std::cout << "\t" << eqn.name() << "[" << j << "] nodaleqn="
// 	       << *eqn.nodaleqn(node, j) << std::endl;
// 	}
//       }
//     }
//   }
// }


// void CSubProblem::dump_eqn() const {
//   for(FuncNodeIterator i=funcnode_iterator(); !i.end(); ++i) {
//     const FuncNode &node = *i.node();
//     std::cout << "node = " << node << std::endl;
//     for(std::vector<Equation*>::size_type e=0;e<Equation::all().size();e++){
//       const Equation &eqn = *Equation::all()[e];
//       if(eqn.is_active(this)) {
// 	for(int j=0; j<eqn.dim(); j++) {
// 	  std::cout << "\t" << eqn.name() << "[" << j << "] nodaleqn="
// 	       << *eqn.nodaleqn(node, j) << std::endl;
// 	}
//       }
//     }
//   }
// }

void CSubProblem::requirePrecompute() {
  precomputeLock.acquire();
  precomputeRequired = true;
  precomputeLock.release();
}


//////////////////////////////////////////////////////////////////////////

#ifdef HAVE_MPI

#include "common/mpitools.h"

// This should be called after set_equation_mapping and mapdofeqs.
// A note that might be useful and cleared up my own (RCL?) confusion:
// When an equation (neq=mesh->nodaleqn[i]) is made dependent in
// bdycondition.py, it is the object
// mesh->nodaleqn[global_equation_map[neq->ndq_index()]] that is made
// dependent, even though it is neq and not the above that originally
// corresponded to the equation. It comes out alright though, because
// when tagging a row (say j) of the local matrix as dependent, it
// suffices to check mesh->nodaleqn[j].
void CSubProblem::set_parallel_mapping()
{
  ResetSharesData();

  // Using global_equation_map, give CNodeShareInfo the information about where
  // in the local stiffness matrix the equation/row can be found.
  for(EqnNodeMap::iterator it=mesh->m_eqnnodemap.begin();
      it!=mesh->m_eqnnodemap.end();it++)
    {
      NodalEquation* pne=it->first;
      FuncNode* pfn=it->second;
      //Get sharing information for FuncNode
      CNodeShareInfo* pns=mesh->m_nodesharemap[pfn];
      //Get index of NodalEqn in FuncNode->eqnlist
      int localindex=(find(pfn->eqnlist.begin(),pfn->eqnlist.end(),pne)-
      		      pfn->eqnlist.begin());
      pns->localeqnindexlist.push_back(localindex);
      pns->symmatrixeqnindexlist.push_back(global_equation_map[pne->ndq_index()]);
      // (global_equation_map[pne->ndq_index()] is the row number in the stiffness matrix.
      // We shall put this row later into its right place in the combined linear system.
    }
  // Give CNodeShareInfo the information about where in the local
  // stiffness matrix the dof/column can be found
  for(DoFNodeMap::iterator it=mesh->m_dofnodemap.begin();
      it!=mesh->m_dofnodemap.end();it++)
    {
      DegreeOfFreedom* pdof=it->first;
      //FuncNode associated with this DoF
      FuncNode* pfn=it->second;
      //Get sharing information for FuncNode
      CNodeShareInfo* pns=mesh->m_nodesharemap[pfn];
      //Get index of DoF in FuncNode->doflist
      int localindex=(find(pfn->doflist.begin(),pfn->doflist.end(),pdof)-
      		      pfn->doflist.begin());
      pns->localdofindexlist.push_back(localindex);
      //Get index of DoF in the mesh->dof vector
      int mtxindex=(find(mesh->dof.begin(),mesh->dof.end(),pdof)-mesh->dof.begin());
      pns->symmatrixdofindexlist.push_back(mtxindex);
    }
  //RCL testing
  if(Rank()==-1)
    {
      for(NodeShareMap::iterator it=mesh->m_nodesharemap.begin();
	  it!=mesh->m_nodesharemap.end();it++)
	{
	  CNodeShareInfo* pns=it->second;
	  oofcerr << "****** Inherited index ****** " << pns->inheritedindex << std::endl;
	  for(std::vector<int>::size_type i=0;i<pns->localeqnindexlist.size();i++)
	    {
	      oofcerr << "NodalEqn " << pns->localeqnindexlist[i] << "," <<
		pns->symmatrixeqnindexlist[i] << std::endl;
	    }
	  for(std::vector<int>::size_type i=0;i<pns->localdofindexlist.size();i++)
	    {
	      oofcerr << "DoF " << pns->localdofindexlist[i] << "," <<
		pns->symmatrixdofindexlist[i] << std::endl;
	    }
	}
    }

  // This process may own a node but
  // is not associated with an element that is being solved (e.g. the node is at the boundary
  // of a subproblem, and this boundary (zero area) belongs to this process). Have to pass ownership
  // of the node to the next process that can solve for it (i.e. contains an element of the
  // subproblem). (This loop got added after the subproblems were introduced)
  int procSize=Size(),localrank=Rank();
  for(int i=0;i<procSize;i++)// Pass the ownership of nodes to successively higher ranks
    {
      std::vector<int> sbuf;
      // Collect the index of nodes that are not part of the subproblem
      for(NodeShareMap::iterator it=mesh->m_nodesharemap.begin();
	  it!=mesh->m_nodesharemap.end();it++)
	{
	  CNodeShareInfo* pns=it->second;
	  if(pns->owns && !(pns->hasElement))
	    {
	      pns->owns=false;
	      // If everything is consistent, nextrank must be a valid process number (!=-1)
	      std::cout << pns->nextrank << "*** next rank index ***" <<pns-> nextindex << std::endl;
	      sbuf.push_back(pns->nextrank);
	      sbuf.push_back(pns->nextindex);
	    }
	}
      // Gather the sizes to determine the maximum message size from each process
      std::vector<int>* psbufsizelist=_Allgather_Int(sbuf.size());

      std::vector<int>::size_type maxsbufsize=sbuf.size();
      for(std::vector<int>::iterator it=psbufsizelist->begin();it!=psbufsizelist->end();it++)
	{
	  if(maxsbufsize<(std::vector<int>::size_type)*it)
	    maxsbufsize=*it;
	}
      //First element of sbuf must exist, so that _Allgather_IntVec won't crash the program
      if(sbuf.empty())
	sbuf.push_back(-1);
      std::vector<int>* psbufall=_Allgather_IntVec(&sbuf,maxsbufsize);
      if(localrank==0)
	{
	  delete psbufsizelist;
	  delete psbufall;
	  continue;
	}
      for(std::vector<int>::size_type k=0;k<psbufall->size();k+=maxsbufsize)
	{
	  int iproc=k/maxsbufsize;
	  for(std::vector<int>::size_type l=0;l<(*psbufsizelist)[iproc];l+=2)
	    {
	      if(localrank==(*psbufall)[k+l])
		{
		  if(mesh->m_indexnodemap.find((*psbufall)[k+l+1])!=mesh->m_indexnodemap.end())
		    {
		      CNodeShareInfo* pns=
			mesh->m_nodesharemap[mesh->m_indexnodemap[(*psbufall)[k+l+1]]];
		      pns->owns=true;
		    }
		  else
		    {
		      //The alternative should not happen
		      oofcerr << "remote index not found!" << std::endl;
		    }
		}
	    }
	}
      delete psbufsizelist;
      delete psbufall;
    }

  //Use information in the vectors indepeqnmap and freedofmap to determine where
  //the rows and columns (DoFs and NodalEqns) should go.
  //If the process owns the node (ergo the DoF and NodalEqn), and if the DoF is free (not fixed),
  //or if the NodalEqn is independent (and active), then the locations should be taken from
  // indepeqnmap or freedofmap.
  //Otherwise, this information should come from the other processes (later).
  m_precombined_indepeqnmap.resize(indepeqnmap.size(),0);
  for(NodeShareMap::iterator it=mesh->m_nodesharemap.begin();
      it!=mesh->m_nodesharemap.end();it++)
    {
      CNodeShareInfo* pns=it->second;
      if(pns->owns==false)
	{
	  for(std::vector<int>::iterator it2=pns->symmatrixeqnindexlist.begin();
	      it2!=pns->symmatrixeqnindexlist.end();it2++)
	    {
	      m_precombined_indepeqnmap[*it2]=-1;//mark as not owned
	    }
	}
    }
  int nrc=0;
  for(std::vector<int>::size_type i=0;i<indepeqnmap.size();i++)
    {
      if(m_precombined_indepeqnmap[i]==0 && indepeqnmap[i]!=-1)
	{
	  m_precombined_indepeqnmap[i]=nrc++;
	}
      else
	{
	  m_precombined_indepeqnmap[i]=-1;//make sure to mark as inactive or not owned
	}
    }
  m_precombined_eqnsize=nrc;

  m_precombined_freedofmap.resize(freedofmap.size(),0);
  for(NodeShareMap::iterator it=mesh->m_nodesharemap.begin();
      it!=mesh->m_nodesharemap.end();it++)
    {
      CNodeShareInfo* pns=it->second;
      if(pns->owns==false)
	{
	  for(std::vector<int>::iterator it2=pns->symmatrixdofindexlist.begin();
	      it2!=pns->symmatrixdofindexlist.end();it2++)
	    {
	      m_precombined_freedofmap[*it2]=-1;//mark as not owned
	    }
	}
    }
  nrc=0;
  for(std::vector<int>::size_type i=0;i<freedofmap.size();i++)
    {
      if(m_precombined_freedofmap[i]==0 && freedofmap[i]!=-1)
	{
	  m_precombined_freedofmap[i]=nrc++;
	}
      else
	{
	  m_precombined_freedofmap[i]=-1;//make sure to mark as fixed or not owned
	}
    }
  m_precombined_dofsize=nrc;

  //ASSERT(m_precombined_dofsize==m_precombined_eqnsize)
  //oofcerr << "m_precombined_eqnsize,dofsize " << m_precombined_eqnsize << " *** =?= *** " <<
  //  m_precombined_dofsize << std::endl;
  //oofcerr << "indepeqnmap,freedofmap sizes " << indepeqnmap.size() << " *** =?= *** " <<
  //  freedofmap.size() << std::endl;

  //Gather all the DoF sizes
  //std::vector<int> *_Allgather_Int(int);//Caller responsible for deletion of return value!
  //Ship and collect
  std::vector<int>* pdofsizelist=_Allgather_Int(m_precombined_dofsize);
  //ASSERT(pdofsizelist->size()==Size()) //Size() from mpitools.h
  if(Rank()==-1)
    {
      for(std::vector<int>::size_type i=0;i<pdofsizelist->size();i++)
	{
	  oofcerr << "***** dofsize ******* " << i << ":" << (*pdofsizelist)[i] << std::endl;
	}
    }

  //Gather the DoF and NodalEqn information owned by each process
  std::vector<int> sbuf;
  for(NodeShareMap::iterator it=mesh->m_nodesharemap.begin();
      it!=mesh->m_nodesharemap.end();it++)
    {
      CNodeShareInfo* pns=it->second;
      if(pns->owns==true)
	{
	  //Move through each process that share the node (but don't own it)
	  //(There usually is only one other process that shares this node)
	  for(std::vector<int>::size_type i=0;i<pns->remoteproclist.size();i++)
	    {
	      std::vector<int>::size_type localdofsize=pns->localdofindexlist.size(),
		localeqnsize=pns->localeqnindexlist.size();

	      //We pack and ship the following:
	      // [remoteproc,remoteindex,#localdofs,#localeqns,
	      //                         localdofindex1,precombineddofindex1,...,
	      //                         localeqnindex1,precombinedeqnindex1,...]
	      //Store the "headers"
	      sbuf.push_back(pns->remoteproclist[i]);
	      sbuf.push_back(pns->remoteindexlist[i]);
	      // Store the dof indices local to the node. It should be
	      // the same for every node, because the fields and
	      // equations are added the same way to each node.
	      std::vector<int> sbufdof;
	      for(std::vector<int>::size_type j=0;j<localdofsize;j++)
		{
		  // Since the node owns it, the map should not return
		  // a -1 when indexed with symmatrixdofindexlist
		  int precomindex=m_precombined_freedofmap[pns->symmatrixdofindexlist[j]];
		  //if(Rank()==0)
		  //  oofcerr << "dof precomindex " << precomindex << "\n";
		  if(precomindex>-1)
		    {
		      sbufdof.push_back(pns->localdofindexlist[j]);
		      sbufdof.push_back(precomindex);
		    }
		}

	      // Store the eqn indices local to the node. It should be
	      // the same for every node, because the fields and
	      // equations are added the same way to each node.
	      // (using CNodeShareInfo::doflist and
	      // CNodeShareInfo::eqnlist)
	      std::vector<int> sbufeqn;
	      for(std::vector<int>::size_type j=0;j<localeqnsize;j++)
		{
		  int precomindex=m_precombined_indepeqnmap[pns->symmatrixeqnindexlist[j]];
		  //if(Rank()==0)
		  //  oofcerr << "eqn precomindex " << precomindex << "\n";
		  if(precomindex>-1)
		    {
		      sbufeqn.push_back(pns->localeqnindexlist[j]);
		      sbufeqn.push_back(precomindex);
		    }
		}

	      sbuf.push_back(sbufdof.size()/2);
	      sbuf.push_back(sbufeqn.size()/2);
	      for(std::vector<int>::iterator it2=sbufdof.begin();it2!=sbufdof.end();it2++)
		{
		  sbuf.push_back(*it2);
		}
	      for(std::vector<int>::iterator it2=sbufeqn.begin();it2!=sbufeqn.end();it2++)
		{
		  sbuf.push_back(*it2);
		}
	    }
	}
    }

  //Ship and collect
  //First gather the maximum size of sbuf among the processes, then use this in _Allgather_IntVec
  // TODO: MPI(?) Explore variable lengths for the buffer size coming from each process ("AllgatherV")
  std::vector<int>* psbufsizelist=_Allgather_Int(sbuf.size());
  std::vector<int>::size_type maxsbufsize=sbuf.size();
  for(std::vector<int>::iterator it=psbufsizelist->begin();it!=psbufsizelist->end();it++)
    {
      if(maxsbufsize<(std::vector<int>::size_type)*it)
	maxsbufsize=*it;
    }

  //First element of sbuf must exist, so that _Allgather_IntVec won't
  //crash the program
  if(sbuf.empty())
    sbuf.push_back(-1);
  std::vector<int>* psbufall=_Allgather_IntVec(&sbuf,maxsbufsize);
  //RCL testing, check what's being gathered
  if(Rank()==-1)
    {
      for(std::vector<int>::size_type i=0;i<psbufall->size();i+=maxsbufsize)
	{
	  int iproc=i/maxsbufsize;
	  oofcerr << "\n**** From Proc " << iproc << ", sbufsize=" << (*psbufsizelist)[iproc] <<
	    ", maxsbufsize=" << maxsbufsize << " ****\n";
	  for(std::vector<int>::size_type j=0;j<(*psbufsizelist)[iproc];j++)
	    {
	      oofcerr << (*psbufall)[i+j] << ",";
	    }
	}
    }

  //Unite! Construct mapping for combined stiffness matrix!

  //Check freedofmap and m_precombined_freedofmap before the shift
  if(Rank()==-1)
    {
      for(std::vector<int>::size_type i=0;i<freedofmap.size();i++)
	{
	  oofcerr << "**** freedofmap, m_precombined : " << freedofmap[i] << ", " <<
	    m_precombined_freedofmap[i] << "\n";
	}
      for(std::vector<int>::size_type i=0;i<indepeqnmap.size();i++)
	{
	  oofcerr << "**** indepeqnmap, m_precombined : " << indepeqnmap[i] << ", " <<
	    m_precombined_indepeqnmap[i] << "\n";
	}
    }

  //First calculate offsets for the rows and columns of the local stiffness matrix
  int rowoffset, columnoffset;
  //int localrank=Rank();
  //ASSERT(localrank<pdofsizelist->size())
  rowoffset=0;
  for(std::vector<int>::size_type i=0;i<(std::vector<int>::size_type)localrank;i++)
    {
      rowoffset+=(*pdofsizelist)[i];
    }
  columnoffset=rowoffset;
  //Add all the dofsizes gathered to get the dimension of the global/combined stiffness matrix
  m_combinedmatrixdim=rowoffset;
  for(std::vector<int>::size_type i=(std::vector<int>::size_type)localrank;
      i<pdofsizelist->size();i++)
    {
      m_combinedmatrixdim+=(*pdofsizelist)[i];
    }
  //Shift the indices in m_precombined_freedofmap and m_precombined_indepeqnmap
  for(std::vector<int>::size_type i=0;i<m_precombined_freedofmap.size();i++)
    {
      if(m_precombined_freedofmap[i]!=-1)
	m_precombined_freedofmap[i]+=columnoffset;
    }
  for(std::vector<int>::size_type i=0;i<m_precombined_indepeqnmap.size();i++)
    {
      if(m_precombined_indepeqnmap[i]!=-1)
	m_precombined_indepeqnmap[i]+=rowoffset;
    }

  //Now get the information gathered for the sharing of the DoFs and NodalEqns
  // to shift the indices of the local non-owned rows and columns
  //Note: If the value of indepeqnmap[i] (freedofmap[i]) is non-zero, then
  // m_precombined_indepeqnmap (m_precombined_freedofmap[i]) must also be non-zero.
  rowoffset=0;
  columnoffset=0;
  for(std::vector<int>::size_type i=0;i<psbufall->size();i+=maxsbufsize)
    {
      int iproc=i/maxsbufsize;
      std::vector<int>::size_type realbufsize=(*psbufsizelist)[iproc],
	inc=i;
      if(iproc!=localrank)//No need to check data sent by the same process
	{
	  while(realbufsize>(inc-i))
	    {
	      int data1=(*psbufall)[inc],
		data2;
	      std::vector<int>::size_type tmpdofsize=(*psbufall)[inc+2],
		tmpeqnsize=(*psbufall)[inc+3];
	      if(data1==localrank)
		{
		  //remote index relative to iproc, but local index relative to localrank
		  data1=(*psbufall)[inc+1];
		  CNodeShareInfo* pns=mesh->m_nodesharemap[mesh->m_indexnodemap[data1]];
		  //Go over the localdofindices and the remote dof indices they are mapped to
		  //tmpdofsize=(*psbufall)[inc+2];
		  if(pns->hasElement)
		    {
		      for(std::vector<int>::size_type j=0;j<tmpdofsize;j++)
			{
			  data1=(*psbufall)[inc+4+2*j];
			  data2=(*psbufall)[inc+4+2*j+1];
			  //We expect these find()'s to be successful (i.e. not .end())
			  int localindex=(find(pns->localdofindexlist.begin(),pns->localdofindexlist.end(),data1)-
					  pns->localdofindexlist.begin());
			  //symmatrixdofindexlist[localindex] gives the local target column
			  //when the local stiffness matrix is populated.
			  m_precombined_freedofmap[pns->symmatrixdofindexlist[localindex]]=data2+columnoffset;
			}
		      std::vector<int>::size_type eqnbegin=inc+4+2*tmpdofsize;
		      //tmpeqnsize=(*psbufall)[inc+3];
		      for(std::vector<int>::size_type j=0;j<tmpeqnsize;j++)
			{
			  data1=(*psbufall)[eqnbegin+2*j];
			  data2=(*psbufall)[eqnbegin+2*j+1];
			  //We expect these find()'s to be successful (i.e. not .end())
			  int localindex=(find(pns->localeqnindexlist.begin(),pns->localeqnindexlist.end(),data1)-
					  pns->localeqnindexlist.begin());
			  //symmatrixeqnindexlist[localindex] gives the local target row
			  //when the local stiffness matrix is populated.
			  m_precombined_indepeqnmap[pns->symmatrixeqnindexlist[localindex]]=data2+rowoffset;
			}
		    }
		}
	      inc+=4+2*(tmpdofsize+tmpeqnsize);
	    }
	}
      rowoffset+=(*pdofsizelist)[iproc];
      columnoffset=rowoffset;
    }

  //Check freedofmap and m_precombined_freedofmap after the shift
  if(Rank()==-1)
    {
      for(std::vector<int>::size_type i=0;i<freedofmap.size();i++)
	{
	  oofcerr << "**** freedofmap, m_precombined : " << freedofmap[i] << ", " <<
	    m_precombined_freedofmap[i] << "\n";
	}
      for(std::vector<int>::size_type i=0;i<indepeqnmap.size();i++)
	{
	  oofcerr << "**** indepeqnmap, m_precombined : " << indepeqnmap[i] << ", " <<
	    m_precombined_indepeqnmap[i] << "\n";
	}
    }

  //cleanup
  sbuf.clear();
  psbufsizelist->clear();
  delete psbufsizelist;
  psbufall->clear();
  delete psbufall;
  pdofsizelist->clear();
  delete pdofsizelist;
} // end set_parallel_mapping

void CSubProblem::NodalPositionSolution(double* temp_array)
{
  //Display (X,Y:NodalValues) at the terminal
  //For testing, and can be called only after
  //set_precombined_equation_mapping and solve
  for(FuncNodeIterator ni=funcnode_iterator(); !ni.end(); ++ni)
    //for(FuncNodeIterator ni(this); !ni.end(); ++ni)
    {
      FuncNode* pfn=ni.node();
      oofcerr << "(x,y:nodalvalues)=(" << pfn->position() << ":";
      //Search dof for the index of the dofs in FuncNode->doflist
      for(std::vector<DegreeOfFreedom*>::iterator it=pfn->doflist.begin();
	  it!=pfn->doflist.end();it++)
	{
	  int index=(find(mesh->dof.begin(),mesh->dof.end(),*it) - 
		     mesh->dof.begin());
	  if(m_precombined_freedofmap[index]!=-1)
	    oofcerr << temp_array[m_precombined_freedofmap[index]] << ",";
	}
      oofcerr << ")\n";
    }

  // Do work like that of FEMesh::set_unknowns()
  for(std::vector<DegreeOfFreedom*>::size_type i=0; i<mesh->dof.size(); i++)
    {
      if(m_precombined_freedofmap[i] != -1)
	{
	  mesh->dof[i]->value(mesh) = temp_array[m_precombined_freedofmap[i]];
	}
    }
} // end CSubProblem::NodalPositionSolution

void CSubProblem::ResetSharesData()
{
  //Note: m_precombined_indepeqnmap.resize(...,0) does not reset the elements
  // that have previously been allocated so have to do an explicit clear.
  m_precombined_indepeqnmap.clear();
  m_precombined_freedofmap.clear();
  for(NodeShareMap::iterator it=mesh->m_nodesharemap.begin();
      it!=mesh->m_nodesharemap.end();it++)
    {
      CNodeShareInfo* pns=it->second;
      pns->localdofindexlist.clear();
      pns->localeqnindexlist.clear();
      pns->symmatrixdofindexlist.clear();
      pns->symmatrixeqnindexlist.clear();

      //Reinitialize the owns flag
      if(pns->_owns0)
	pns->owns=true;
      else
	pns->owns=false;

      // Is the node part of an element contained in a subproblem of the current process?
      FuncNode* pfn=it->first;
      if(containsNode(pfn))
	{
	  mesh->m_nodesharemap[pfn]->hasElement=true;
	}
      else
	{
	  mesh->m_nodesharemap[pfn]->hasElement=false;
	}
    }
}

int CSubProblem::GatherNumNodes()
{
  // Get the number of nodes for this subproblem
  // Must be "owned" by the current process.
  int nOwned=0;
  for(FuncNodeIterator ni=funcnode_iterator(); !ni.end(); ++ni)
    {
      FuncNode* pfn=ni.node();
      if(pfn->isShared())
	{
	  if(mesh->m_nodesharemap[pfn]->_owns0)
	    nOwned++;
	}
      else
	{
	  nOwned++;
	}
    }

  // collect from all processes
  int nnodes=0;
  std::vector<int>* pnnodes=_Allgather_Int(nOwned);
  for(std::vector<int>::size_type i=0;i<pnnodes->size();i++)
    {
      nnodes+=(*pnnodes)[i];
    }
  delete pnnodes;
  return nnodes;
}

#endif // HAVE_MPI

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ZZ error estimation stuff. Translocated from femesh.C
// TODO 3.1 This should be encapsulated elsewhere, so that different
// error estimators can be used.

// initializing "scpatches"
void CSubProblem::init_scpatches(const std::vector<int> *snodes) {
  // snodes is a list of mesh node indices, in order of the
  // corresponding skeleton node indices.  scpatches is a std::map,
  // mapping ints to NodalSCPatches*.
  for(std::vector<int>::size_type i=0; i<snodes->size(); i++)
    scpatches[(*snodes)[i]] = new NodalSCPatches();
}

// create/add a new CSCPatch pointer
void CSubProblem::add_scpatch(const int assembly_node, const Material *mat,
			      const int order,
			      const std::vector<int> *elems,
			      const std::vector<int> *nodes,
			      const int qualified)
{
  // make sure to delete new'd CSCPatch's at FEMesh's destruction.
  CSCPatch *patch = new CSCPatch(this, order, mat, elems, nodes, qualified);
  scpatches[assembly_node]->add_patch(patch);
}

// get elements and nodes from the patch
std::vector<int> *CSubProblem::get_elements_from_patch(const int assembly_node,
						       const Material *mat)
{
  return scpatches[assembly_node]->get_elements_from_patch(mat);
}

std::vector<int> *CSubProblem::get_nodes_from_patch(const int assembly_node,
						    const Material *mat)
{
  return scpatches[assembly_node]->get_nodes_from_patch(mat);
}

// initialize "recovered_fluxes"
void CSubProblem::init_nodalfluxes() {
  for(FuncNodeIterator i=funcnode_iterator(); !i.end(); ++i)
    recovered_fluxes[i.node()->index()] = new NodalFluxes();
}

// recover fluxes
void CSubProblem::recover_fluxes() {
  std::map<const int, NodalSCPatches*>::iterator iter;
  std::vector<Flux*> allfluxes = allFluxes();
  for(iter=scpatches.begin(); iter!=scpatches.end(); iter++)
    (iter->second)->recover_fluxes(allfluxes);
}

// add a recovered flux to the map
void CSubProblem::add_this_flux(const Material *mat, const Flux *fluks,
				const Node *nd, DoubleVec *fvalues)
{
  recovered_fluxes[nd->index()]->add_flux_value(mat, fluks, fvalues);
}

// compute a recovered flux at MasterCoord
DoubleVec *CSubProblem::get_recovered_flux(const Flux *fluks,
					   const Element *elem,
					   const MasterCoord &mc)
{
  int dim = fluks->ndof();
  DoubleVec *result = new DoubleVec(dim, 0.0);
  for(int i=0; i<dim; i++) {
    // interpolating the value
    for(CleverPtr<ElementFuncNodeIterator>node(elem->funcnode_iterator());
	!node->end(); ++*node)
      {
	double temp = recovered_fluxes[(node->node())->index()]->
	  get_flux_component(elem->material(), fluks, i);
	(*result)[i] += node->shapefunction(mc)*temp;
      }
  }
  return result;
}

// compute all the recovered fluxes at Coord -- swigged one
void CSubProblem::report_recovered_fluxes(const Element *elem,
					  const Coord *point) {
  std::vector<Flux*> fluxes = allFluxes();
  for (std::vector<Flux*>::size_type i=0; i<fluxes.size(); i++) {
    oofcerr << fluxes[i]->name() << std::endl;
    int dim = fluxes[i]->ndof();
    for(int j=0; j<dim; j++) {
      double j_th_component = 0.0;
      for(CleverPtr<ElementFuncNodeIterator> node(elem->funcnode_iterator());
	  !node->end(); ++*node)
	{
	  double comp = recovered_fluxes[(node->node())->index()]
	    ->get_flux_component(elem->material(), fluxes[i], j);
	  j_th_component += node->shapefunction(elem->to_master(*point))*comp;
	}
      oofcerr << j_th_component << std::endl;
    }
    oofcerr << "==========================" << std::endl;
  }
}


double CSubProblem::zz_L2_estimate(const Element *elem, const Flux *fluks) {
  // What to compute:
  // Integral_e[(flux_ex-flux_fe)^T (flux_ex-flux_fe)]^(1/2)
  // flux_ex -> recovered flux
  //
  // Things to consider to determine integration order
  // Linear mesh: recovered stress field is linear, so the order
  // is 2 -- 2x2 gauss point needed.
  // Quadratic mesh: recovered stress field is quadratic, thus the order
  // should be 4 -- 3x3 gauss points needed.

  int order = 2*elem->shapefun_degree();
  int dim = fluks->ndof();
  double error = 0.0;
  double refer = 0.0;
  for(GaussPointIterator gpt = elem->integrator(order); !gpt.end(); ++gpt) {
    MasterCoord mc = gpt.gausspoint().mastercoord();
    double wt = gpt.gausspoint().weight();
    zz_L2_estimate_sub(elem, fluks, dim, error, refer, mc, wt);
  }
  if (refer == 0.0)
    return 0.0;
  return sqrt(error/refer);
}


// TODO 3.1: Remove dim arg.
void CSubProblem::zz_L2_estimate_sub(const Element *elem, const Flux *fluks,
				     const int &dim, double &error,
				     double &refer,
				     const MasterCoord &mc, const double &wt)
{
  // flux(diff) vectors
  DoubleVec *recovered = get_recovered_flux(fluks, elem, mc);
  DoubleVec *feflux = fluks->evaluate( this->mesh, elem, mc );
  DoubleVec diff = *recovered - *feflux;
  error += (diff*diff) * wt;
  refer += ((*recovered)*(*recovered)) * wt;
  delete recovered;
  delete feflux;
}

DoubleVec *CSubProblem::zz_L2_weights(const Flux *fluks,
				      const double &bottom,
				      const double &top)
{
  DoubleVec *weights = new DoubleVec;
  DoubleVec values;

  int dim = fluks->ndof();
  bool first = true;
  int order=0;			// initialized to suppress compiler warnings
  double min=0, max=0;		// will be reinitialized below
  for(ElementIterator i=element_iterator(); !i.end(); ++i) {
    Element *elem = i.element();
    if(first)
      order = 2*elem->shapefun_degree();
    double value = 0.0;
    for(GaussPointIterator gpt = elem->integrator(order); !gpt.end(); ++gpt) {
      MasterCoord mc = gpt.gausspoint().mastercoord();
      double wt = gpt.gausspoint().weight();
      zz_L2_weights_sub(elem, fluks, dim, value, mc, wt);
    }
    values.push_back(value);
    if(first) {
      min = value;
      max = value;
      first = false;
    }
    else {
      if(value < min)
	min = value;
      if(value > max)
	max = value;
    }
  }

//   int order = 2*mesh->element[0]->shapefun_degree();
//   int dim = fluks->ndof();

//   Element *elem = element[0];
//   double value = 0.0;
//   for(GaussPointIterator gpt = elem->integrator(order); !gpt.end(); ++gpt) {
//     MasterCoord mc = gpt.gausspoint().mastercoord();
//     double wt = gpt.gausspoint().weight();
//     zz_L2_weights_sub(elem, fluks, dim, value, mc, wt);
//   }
//   values.push_back(value);
//   double min = value;
//   double max = value;

//   for(int i=1; i<mesh->nelements(); i++) {
//     Element *elem = mesh->element[i];
//     value = 0.0;
//     for(GaussPointIterator gpt = elem->integrator(order); !gpt.end(); ++gpt) {
//       MasterCoord mc = gpt.gausspoint().mastercoord();
//       double wt = gpt.gausspoint().weight();
//       zz_L2_weights_sub(elem, fluks, dim, value, mc, wt);
//     }
//     values.push_back(value);
//     if(value < min)
//       min = value;
//     if(value > max)
//       max = value;
//   }

  double upper = min + (max-min)*top;
  double lower = min + (max-min)*bottom;
  double diff = upper - lower;
  double sum = upper + lower;
  for(DoubleVec::size_type i=0; i<values.size(); i++)
    weights->push_back(0.5*erf(M_E*(2*values[i]-sum)/diff)+0.5);
  return weights;
}

// TODO 3.1: Remove dim arg.
void CSubProblem::zz_L2_weights_sub(const Element *elem, const Flux *fluks,
				    const int &dim, double &value,
				    const MasterCoord &mc, const double &wt)
{
  // flux vector
  DoubleVec *feflux = fluks->evaluate( this->mesh, elem, mc );
  value += ((*feflux)*(*feflux))*wt;
  delete feflux;
}
