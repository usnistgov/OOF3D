// -*- C++ -*-
// $RCSfile: equation.C,v $
// $Revision: 1.96.2.7 $
// $Author: langer $
// $Date: 2014/09/17 17:47:56 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#include "common/cleverptr.h"
#include "common/doublevec.h"
#include "common/smallmatrix.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "common/IO/oofcerr.h"
#include "engine/cnonlinearsolver.h"
#include "engine/csubproblem.h"
#include "engine/edge.h"
#include "engine/element.h"
#include "engine/equation.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/fieldeqnlist.h"
#include "engine/flux.h"
#include "engine/fluxnormal.h"
#include "engine/gausspoint.h"
#include "engine/linearizedsystem.h"
#include "engine/material.h"
#include "engine/nodalequation.h"
#include "engine/node.h"
#include "engine/ooferror.h"
#include "engine/property.h"
#include "engine/smallsystem.h"
#include "engine/sparsemat.h"

#include "common/printvec.h"	// for debugging

std::vector<Equation*> &Equation::all() {
  static std::vector<Equation*> all_eqns;
  return all_eqns;
}

Equation *getEquationByIndex(int index) {
  Equation *eqn = Equation::all()[index];
  return eqn;
}

Equation *Equation::getEquation(const std::string &nm) {
  const std::vector<Equation*> &list = all();
  for(std::vector<Equation*>::size_type i=0; i<list.size(); i++) {
    if(list[i]->name() == nm) {
      return list[i];
    }
  }
  throw ErrProgrammingError("Unknown Equation \"" + nm + "\"",
			    __FILE__, __LINE__);
}

FEWrapper<Equation>::AllWrappers
&Equation::FindAllEquationWrappers::operator()() {
    return mesh->equationwrappers;
}

int countEquations() {
  return Equation::all().size();
}



const std::string Equation::modulename_("ooflib.SWIG.engine.equation");


Equation::Equation(const std::string &nm, int d)
  : dim_(d),
    name_(nm),
    index_(all().size())
{
  all().push_back(this);
}


FluxEquation::FluxEquation(const std::string &nm, Flux &flx, int d)
  : Equation(nm, d), fflux(&flx)
{
  fflux->addEquation(this);
}

// position of a given component in the eqn lists in the nodes

int Equation::localindex(const FuncNode &node, const FieldIndex &component)
  const
{
  return node.equationset.offset(this) + component.integer();
}

int Equation::localindex(const FuncNode &node, int component) const {
  return node.equationset.offset(this) + component;
}

NodalEquation *Equation::nodaleqn(const FuncNode &node, int component) const {
  return node.eqnlist[localindex(node, component)];
}

// activate_fluxes() and deactivate_fluxes() are called by
// CSubProblem::activate_equation() and CSubProblem::deactivate_equation().

void FluxEquation::activate_fluxes(CSubProblem *subpr) {
  subpr->activate_flux(*fflux);
}

void FluxEquation::deactivate_fluxes(CSubProblem *subpr) {
  subpr->deactivate_flux(*fflux);
}


bool Equation::is_active(const CSubProblem *subpr) const {
  return subpr->is_active_equation(*this);
}

const std::string &FluxEquation::fluxname() const {
  return fflux->name();
}

const Flux *FluxEquation::flux() const {
  return fflux;
}



SmallSystem *Equation::initializeSystem(const Element *e) {
  return new SmallSystem(dim_, e->ndof());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Equation::make_linear_system is called by
// Material::make_linear_system after the Properties have computed the
// flux matrix for the Flux at the current GaussPoint.
// Equation::make_linear_system has to use the flux matrix to compute
// the GaussPoints contribution to the global stiffness matrix.
#include "engine/masterelement.h"
void
DivergenceEquation::make_linear_system(const CSubProblem *subproblem,
				       const Element *element,
				       const GaussPoint &gpt,
				       const std::vector<int> &dofmap,
				       FluxSysMap &fluxdata,
				       SmallSystem *eqndata,
				       const CNonlinearSolver *nlsolver,
				       LinearizedSystem &linsys) const
{
  double weight = gpt.weight();
  // std::cerr << "DivergenceEquation::make_linear_system: element="
  // 	    << element->get_index() << std::endl;

  bool needResidual = nlsolver->needsResidual();
  bool needJacobian = nlsolver->needsJacobian();

  for (CleverPtr<ElementFuncNodeIterator> mu(element->funcnode_iterator());
       !mu->end(); ++*mu)
  {

    double sf = mu->shapefunction(gpt);
    double dsf[DIM];
    for(int i=0; i<DIM; i++)
      dsf[i] = mu->dshapefunction(i, gpt);

    for (int eqcomp = 0; eqcomp < dim(); ++eqcomp) {
      // Use the un-mapped row.  The matrix will be symmetrized,
      // if possible, afterwards by the subproblem.
      int global_row = nodaleqn( *mu->funcnode(), eqcomp )->ndq_index();

      FluxSysMap::iterator fi = fluxdata.find( fflux );

      if ( fi != fluxdata.end() ) {

	// (*fi).first is a Flux*
	std::vector<int> cmap = (*fi).first->contraction_map( eqcomp );


	// (*fi).second is a SmallSystem*
	if ( !(*fi).second->k_clean ) {
	  const SmallSparseMatrix &k = (*fi).second->kMatrix;

	  for (int ldof = 0; ldof < element->ndof(); ++ldof) {
	    // dofmap is the Element's localDoFmap, which maps local
	    // element dof indices to global ones.
	    int global_col = dofmap[ldof];
	    double sum = 0.0;
	    bool nonzero = false;
	    for(int cc = 0; cc < DIM; ++cc) {
	      if(k.nonzero(cmap[cc], ldof)) {
		nonzero = true;
		// The minus sign here comes from integration by
		// parts, presumably.
		double value = -dsf[cc] * k(cmap[cc], ldof);
		sum += value;
	      }
	    }
	    if(nonzero) {
	      linsys.insertK(global_row, global_col, sum*weight);
	      if(needJacobian)
		linsys.insertJ(global_row, global_col, sum*weight);
	    }
	  }
	} // End of k-matrix loop.

	if ( !(*fi).second->c_clean ) {
	  const SmallSparseMatrix &c = (*fi).second->cMatrix;
	  for (int ldof = 0; ldof < element->ndof(); ++ldof) {
	    int global_col = dofmap[ldof];
	    double sum = 0.0;
	    bool nonzero = false;
	    for(int cc = 0; cc < DIM; ++cc) {
	      if(c.nonzero(cmap[cc], ldof)) {
		nonzero = true;
		double value = -dsf[cc] * c(cmap[cc], ldof);
		sum += value;
	      }
	    }
	    if(nonzero)
	      linsys.insertC(global_row, global_col, sum*weight);
	  }
	} // End of c-matrix loop.


	if ( !(*fi).second->m_clean ) {
	  const SmallSparseMatrix &m = (*fi).second->mMatrix;

	  for (int ldof = 0; ldof < element->ndof(); ++ldof) {
	    int global_col = dofmap[ldof];
	    double sum = 0.0;
	    bool nonzero = false;
	    for (int cc = 0; cc < DIM; ++cc) {
	      if(m.nonzero(cmap[cc], ldof)) {
		sum += -dsf[cc] * m(cmap[cc], ldof);
		nonzero = true;
	      }
	    }
	    if(nonzero)
	      linsys.insertM(global_row, global_col, sum*weight);
	  }
	} // End of m-matrix loop.


	if ( !(*fi).second->flux_clean && needResidual) {
	  const DoubleVec &flux = (*fi).second->fluxVector();
	  double sum = 0.0;
	  bool nonzero = false;
	  for (int cc = 0; cc < DIM; ++cc) {
	    double flx = flux[cmap[cc]];
	    if(flx != 0.0) {
	      nonzero = true;
	      sum += -dsf[cc] * flx;
	    }
	  }
	  if(nonzero)
	    linsys.insert_static_residual(global_row, sum*weight);
	} // End of flux-vector loop.


	if ( !(*fi).second->offset_clean ) {
	  const DoubleVec &offset = (*fi).second->offsetVector();
	  double sum = 0.0;
	  bool nonzero = false;
	  for (int cc = 0; cc < DIM; ++cc) {
	    double off = offset[cmap[cc]];
	    if(off != 0.0) {
	      nonzero = true;
	      sum += -dsf[cc] * off;
	    }
	  }
	  if(nonzero)
	    linsys.insert_body_rhs(global_row, -sum*weight);
	} // End of flux-offset loop.

      } // End if fi != fluxdata.end()


      // Direct equation contributions.

      if ( !eqndata->df_clean && needJacobian ) {
	const SmallSparseMatrix &df = eqndata->dfMatrix;
	for(int ldof = 0; ldof < element->ndof(); ++ldof) {
	  if(df.nonzero(eqcomp, ldof)) {
	    int global_col = dofmap[ldof];
	    double value = sf * df(eqcomp,ldof);
	    linsys.insertJ( global_row, global_col, value*weight );
	  }
	}
      }

      if ( !eqndata->c_clean ) {
	const SmallSparseMatrix &c = eqndata->cMatrix;
	for (int ldof = 0; ldof < element->ndof(); ++ldof) {
	  if(c.nonzero(eqcomp, ldof)) {
	    int global_col = dofmap[ldof];
	    double value = sf * c(eqcomp,ldof);
	    linsys.insertC( global_row, global_col, value*weight );
	  }
	}
      }

      if ( !eqndata->m_clean ) {
	const SmallSparseMatrix &m = eqndata->mMatrix;
	for (int ldof = 0; ldof < element->ndof(); ++ldof) {
	  if(m.nonzero(eqcomp, ldof)) {
	    int global_col = dofmap[ldof];
	    double value = sf * m(eqcomp,ldof);
	    linsys.insertM( global_row, global_col, value*weight );
	  }
	}
      }

      if ( !eqndata->force_clean ) {
	const DoubleVec &force = eqndata->forceVector();
	double f = force[eqcomp];
	if(f != 0.0) {
	  // force contribution
	  double value = sf * f;
	  // add to residual
	  if(needResidual) {
	    linsys.insert_static_residual(global_row, value*weight);
	  }
	  // subtract from rhs
	  linsys.insert_body_rhs(global_row, -value*weight);
	}
      }

      // Finished with direct equation contributions.

    }  // Closes eqcomp loop.

  } // Closes ElementFuncnodeIterator loop.

  // std::cerr << "DivergenceEquation::make_linear_system: residual="
  // 	    << linsys.get_static_residual() << std::endl;

} // end of 'DivergenceEquation::make_linear_system'


void
PlaneFluxEquation::make_linear_system(const CSubProblem *subproblem,
				      const Element *element,
				      const GaussPoint &gpt,
				      const std::vector<int> &dofmap,
				      FluxSysMap &fluxdata,
				      SmallSystem *eqndata,
				      const CNonlinearSolver *nlsolver,
				      LinearizedSystem &linsys) const
{
  double weight = gpt.weight();
  for (CleverPtr<ElementFuncNodeIterator> mu(element->funcnode_iterator()); 
       !mu->end(); ++*mu)
    {
      double sf = mu->shapefunction(gpt);

      for(int eqcomp = 0; eqcomp < dim(); ++eqcomp) {
	int global_row = nodaleqn( *mu->funcnode(), eqcomp )->ndq_index();

	FluxSysMap::iterator fi = fluxdata.find( fflux );

	if ( fi != fluxdata.end() ) {
	  // (*fi).first is a Flux*
	  const std::vector<int> &pmap = (*fi).first->outofplane_map();

	  int fluxcomp = pmap[eqcomp]; // flux component

	  // (*fi).second is a SmallSystem*
	  if ( !(*fi).second->k_clean ) {
	    const SmallSparseMatrix &k = (*fi).second->kMatrix;
	    for(int ldof = 0; ldof < element->ndof(); ++ldof) {
	      // dofmap is the Element's localDoFmap, which maps local
	      // Element dof indices to global ones.
	      if(k.nonzero(fluxcomp, ldof)) {
		int global_col = dofmap[ldof];
		double value = -sf * k( fluxcomp, ldof );
		linsys.insertK( global_row, global_col, value*weight );
		if ( nlsolver->needsJacobian() )
		  linsys.insertJ( global_row, global_col, value*weight );
	      }
	    }
	  }

	  if ( !(*fi).second->c_clean ) {
	    const SmallSparseMatrix &c = (*fi).second->cMatrix;
	    for(int ldof = 0; ldof < element->ndof(); ++ldof) {
	      if(c.nonzero(fluxcomp, ldof)) {
		int global_col = dofmap[ldof];
		double value = -sf * c( fluxcomp, ldof );
		linsys.insertC( global_row, global_col, value*weight );
	      }
	    }
	  }

	  if ( !(*fi).second->m_clean ) {
	    const SmallSparseMatrix &m = (*fi).second->mMatrix;
	    for(int ldof = 0; ldof < element->ndof(); ++ldof) {
	      if(m.nonzero(fluxcomp, ldof)) {
		int global_col = dofmap[ldof];
		double value = sf * m( fluxcomp, ldof );
		linsys.insertM( global_row, global_col, value*weight );
	      }
	    }
	  }

	  if ( !(*fi).second->flux_clean && nlsolver->needsResidual() ) {
	    const DoubleVec &flux = (*fi).second->fluxVector();
	    double f = flux[fluxcomp];
	    if(f != 0.0) {
	      double value = -sf * f;
	      linsys.insert_static_residual(global_row, value*weight);
	    }
	  }

	  if ( !(*fi).second->offset_clean ) {
	    const DoubleVec &offset = (*fi).second->offsetVector();
	    double off = offset[fluxcomp];
	    if(off != 0.0) {
	      double value = -sf * off;
	      // subtract from rhs
	      linsys.insert_body_rhs(global_row, -value*weight);
	    }
	  }

	} // endif fi != fluxdata.end()

      } // end equation component loop
    } // end funcnode loop
  // std::cerr << "PlaneFluxEquation::make_linear_system: residual="
  // 	    << system.get_static_residual() << std::endl;

} // PlaneFluxEquation::make_linear_system



//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


DivergenceEquation::DivergenceEquation(const std::string &name, Flux &flx,
				       int d)
  : FluxEquation(name, flx, d)
{}

const std::string &DivergenceEquation::classname() const {
  static std::string name_("DivergenceEquation");
  return name_;
}


int DivergenceEquation::integration_order(const Element *el) const {
  return el->dshapefun_degree();
}

// Boundary integral for a divergence equation.  Calls back to the
// calling flux to fill the rhs structure, then distributes the
// results, multiplied by the gauss weight, to the nodal equation
// value fields.
#if DIM==2
void DivergenceEquation::boundary_integral(const CSubProblem *subp,
					   LinearizedSystem *ls,
					   const Flux *flux,
					   const BoundaryEdge *ed,
					   const EdgeGaussPoint& egp,
					   const FluxNormal *flxnormal)
  const
{
  DoubleVec J_dot_normal(dim(),0.0);
  for(EdgeNodeIterator edi = ed->node_iterator(); !edi.end(); ++edi) {
    // Call the flux to populate it.
    flux->local_boundary(ed, edi, egp, flxnormal, J_dot_normal);
    // And distribute the values to the boundary rhs vector.
    for(DoubleVec::size_type i=0; i<J_dot_normal.size(); i++) {
      int rownum = nodaleqn(*edi.funcnode(), i)->ndq_index();

      // The invisible + sign here determines the sense of Neumann
      // boundary conditions.  The convention is that the boundary
      // condition specifies the dot product of a flux at the boundary
      // with the outward surface normal.
      ls->insert_force_bndy_rhs(rownum, egp.weight()*J_dot_normal[i]);
    }
  }
}
#else // DIM==3
void DivergenceEquation::boundary_integral(const CSubProblem *subp,
					   LinearizedSystem *ls,
					   const Flux *flux,
					   const Element *el,
					   const GaussPoint &gpt,
					   const FluxNormal *flxnormal)
  const
{
  DoubleVec J_dot_normal(dim(), 0.0);
  for(CleverPtr<ElementFuncNodeIterator> mu(el->funcnode_iterator());
      !mu->end(); ++*mu)
    {
      flux->local_boundary(*mu, gpt, flxnormal, J_dot_normal);
      for(DoubleVec::size_type i=0; i<J_dot_normal.size(); i++) {
	int rownum = nodaleqn(*mu->funcnode(), i)->ndq_index();
	// The invisible + sign here determines the sense of Neumann
	// boundary conditions.  The convention is that the boundary
	// condition specifies the dot product of a flux at the
	// boundary with the outward surface normal.
	ls->insert_force_bndy_rhs(rownum, gpt.weight()*J_dot_normal[i]);
      }
    }
}
#endif // DIM==3

IteratorP DivergenceEquation::iterator() const {
  return fflux->divergence_iterator();
}

IndexP DivergenceEquation::componenttype() const {
  return fflux->divergence_componenttype();
}

IndexP DivergenceEquation::getIndex(const std::string &str) const {
  return fflux->divergence_getIndex(str);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PlaneFluxEquation::PlaneFluxEquation(const std::string &name, Flux &flx, int d)
  : FluxEquation(name, flx, d)
{}

const std::string &PlaneFluxEquation::classname() const {
  static const std::string name_("PlaneFluxEquation");
  return name_;
}

#if DIM==2
void PlaneFluxEquation::boundary_integral(const CSubProblem *m,
					  LinearizedSystem*,
					  const Flux *flux,
					  const BoundaryEdge *ed,
					  const EdgeGaussPoint& egp,
					  const FluxNormal *flxnormal)
  const
{
  return; // stub
}
#else // DIM==3
void PlaneFluxEquation::boundary_integral(const CSubProblem*,
					  LinearizedSystem*,
					  const Flux*,
					  const Element*,
					  const GaussPoint&,
					  const FluxNormal*)
  const
{
  return; // stub
}
#endif

int PlaneFluxEquation::integration_order(const Element *el) const {
  return el->shapefun_degree();
}

IteratorP PlaneFluxEquation::iterator() const {
  return fflux->out_of_plane_iterator();
}

IndexP PlaneFluxEquation::componenttype() const {
  return fflux->componenttype();
}

IndexP PlaneFluxEquation::getIndex(const std::string &str) const {
  return fflux->getOutOfPlaneIndex(str);
  // return fflux->getIndex(str);
}

//////////////

std::ostream &operator<<(std::ostream &os, const Equation &eqn) {
  os << "Equation(" << eqn.name() << ")";
  return os;
}


/////////////////////////////////////////////////////////////////

NaturalEquation::NaturalEquation(const std::string &name, int d)
  : Equation(name, d)
{}


const std::string &NaturalEquation::classname() const {
  static std::string name_("NaturalEquation");
  return name_;
}

void NaturalEquation::make_linear_system(const CSubProblem *subproblem,
					 const Element *element,
					 const GaussPoint &gpt,
					 const std::vector<int> &dofmap,
					 FluxSysMap &fluxdata,
					 SmallSystem *eqndata,
					 const CNonlinearSolver *nlsolver,
					 LinearizedSystem &linsys)
  const {

  // This routine should only be called for gausspoints where it's
  // active.  The flux data is redundant, but removing it probably
  // breaks the API.

  // For each gausspoint in this element where we are active, for
  // each component of the equation, map the collected eqndata to the
  // master stiffness matrix.  The mapping is quite simple.
}

#if DIM==2
void NaturalEquation::boundary_integral(const CSubProblem *subp,
					LinearizedSystem *ls,
					const Flux *flux,
					const BoundaryEdge *ed,
					const EdgeGaussPoint& egp,
					const FluxNormal *flxnormal)
  const
{
  // TODO 3.1: Does this operation even make sense for this class?
}
#else // DIM==3
void NaturalEquation::boundary_integral(const CSubProblem*,
					LinearizedSystem*,
					const Flux*,
					const Element*,
					const GaussPoint&,
					const FluxNormal*)
  const
{
  // TODO 3.1: Does this operation even make sense for this class?
}
#endif // DIM==3

IteratorP NaturalEquation::iterator() const {
  return IteratorP(new ScalarFieldIterator);
}

IndexP NaturalEquation::componenttype() const {
  return IndexP(new ScalarFieldIndex);
}

IndexP NaturalEquation::getIndex(const std::string&str) const {
  return IndexP(new ScalarFieldIndex);
}

int NaturalEquation::integration_order(const Element *el) const {
  return el->shapefun_degree();
}

