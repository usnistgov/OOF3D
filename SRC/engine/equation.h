// -*- C++ -*-
// $RCSfile: equation.h,v $
// $Revision: 1.58.2.2 $
// $Author: langer $
// $Date: 2014/02/24 22:33:39 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// An Equation object is used to identify a set of rows in the global
// stiffness matrix and the rhs.  Each instance of the Equation class
// is a global variable: for example, HeatEqn, ForceBalanceEqn.  The
// instances are created in oof.py.

#include <oofconfig.h>

#ifndef EQUATION_H
#define EQUATION_H

class Equation;

#include "common/identification.h"
#include "common/pythonexportable.h"
#include "engine/fieldeqnlist.h"
#include "engine/indextypes.h"
#include <string>
#include <vector>


class BoundaryEdge;
class CNonlinearSolver;
class CSubProblem;
class Edge;
class EdgeGaussPoint;
class Element;
class ElementFuncNodeIterator;
class Field;
class FieldIndex;
class Flux;
class FluxNormal;
class FluxNormal;
class FuncNode;
class GaussPoint;
class IndexP;
class IteratorP;
class LinearizedSystem;
class Material;
class NodalEquation;
class SmallSystem;
int countEquations();
Equation *getEquationByIndex(int);

typedef std::map<Flux*, SmallSystem*, ltidobject> FluxSysMap;

class Equation : public IdentifiedObject, public PythonExportable<Equation> {
protected:
  int dim_;			// number of components
  std::string name_;
  static const std::string modulename_;
  const unsigned int index_;
public:
  Equation(const std::string &nm, int d);
  virtual ~Equation() {}
  unsigned int index() const { return index_; }
  static Equation *getEquation(const std::string&);

  virtual const std::string &classname() const = 0;
  virtual const std::string &modulename() const { return modulename_; }

  // where a given component lives in the eqn lists in a Node
  int localindex(const FuncNode&, const FieldIndex &component) const;
  int localindex(const FuncNode&, int component) const;
  NodalEquation *nodaleqn(const FuncNode&, int component) const;

  // Equations can return an iterator that iterates over their
  // components, which are the components of the divergence of the
  // host flux, for DivergenceEquations, and out-of-plane components
  // of the flux for PlaneFluxEquation objects.
  virtual IteratorP iterator() const = 0;
  virtual IndexP componenttype() const = 0;
  virtual IndexP getIndex(const std::string&) const = 0;

  static std::vector<Equation*> &all();
  const std::string &name() const { return name_; }

  // const std::string &fluxname() const;
  // const Flux* flux() const;

  int dim() const { return dim_; } // number of components
  int ndof() const { return dim_; }

  virtual void activate_fluxes(CSubProblem*) {};	
  // called when Eqn is activated by CSubProblem
  virtual void deactivate_fluxes(CSubProblem*) {};
  // This is synonymous with CSubProblem::is_active_equation(Equation&):
  bool is_active(const CSubProblem*) const;

  SmallSystem* initializeSystem(const Element*);

  // This is the new one for time-dependene.
  virtual void make_linear_system(const CSubProblem*, const Element*,
				  const GaussPoint&,
				  const std::vector<int>&,
				  FluxSysMap&,
				  SmallSystem*,
				  const CNonlinearSolver*,
				  LinearizedSystem&)
    const {
    return;  // Null for now.  Eventually should be const = 0.
  }

  // Returns the polynomial order of the terms that the equation
  // factors into the stiffness matrix integrand.
  virtual int integration_order(const Element*) const = 0;

#if DIM==2
  virtual void boundary_integral(const CSubProblem*, LinearizedSystem*,
				 const Flux*, 
				 const BoundaryEdge*,
				 const EdgeGaussPoint &, const FluxNormal *)
    const = 0;
#else // DIM==3
  virtual void boundary_integral(const CSubProblem*, LinearizedSystem*,
				 const Flux*, const Element*,
				 const GaussPoint&, const FluxNormal*)
    const = 0;
#endif // DIM==3

  virtual bool allow_boundary_conditions() const = 0;

  // Stuff required by fieldeqnlist.h
  typedef FieldEqnData FEData;	// just use base class from fieldeqnlist.h
  class FindAllEquationWrappers {
  private:
    FEMesh *mesh;
  public:
    FindAllEquationWrappers(FEMesh *mesh) : mesh(mesh) {}
    // Using typedefs to specify the return type of operator()
    // confuses the compiler, so we have to write it out in
    // full. Grrr.
    std::map<const std::vector<FEData>*, FEWrapper<Equation>*,
	     FEvectorCompare<Equation> >
    &operator()();
  };
  typedef FindAllEquationWrappers GetWrappers;
};				// end class Equation


std::ostream &operator<<(std::ostream &os, const Equation&);


class FluxEquation : public Equation {
protected:
  Flux *fflux;
public:
  FluxEquation(const std::string &name, Flux &flx, int d);
  const std::string &fluxname() const;
  const Flux *flux() const;

  void activate_fluxes(CSubProblem*);
  void deactivate_fluxes(CSubProblem*);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// divergence of flux = body force
class DivergenceEquation : public FluxEquation {
public:
  DivergenceEquation(const std::string &name, Flux &flx, int d); 
		
  virtual void make_linear_system(const CSubProblem*, const Element*,
				  const GaussPoint&,
				  const std::vector<int>&,
				  FluxSysMap&,
				  SmallSystem*,
				  const CNonlinearSolver*,
				  LinearizedSystem&) const;
#if DIM==2
  virtual void boundary_integral(const CSubProblem*, LinearizedSystem*,
				 const Flux*, 
				 const BoundaryEdge *, const EdgeGaussPoint&, 
				 const FluxNormal *) const;
#else // DIM==3
  virtual void boundary_integral(const CSubProblem*, LinearizedSystem*,
				 const Flux*, const Element*,
				 const GaussPoint&, const FluxNormal*) const;
#endif // DIM==3
  virtual int integration_order(const Element*) const;

  virtual IteratorP iterator() const;
  virtual IndexP componenttype() const;
  virtual IndexP getIndex(const std::string&) const;

  virtual const std::string &classname() const;
  virtual bool allow_boundary_conditions() const { return true; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PlaneFluxEquation : public FluxEquation {
public:
  PlaneFluxEquation(const std::string &name, Flux &flx, int d);

  virtual void make_linear_system(const CSubProblem*, const Element*,
				  const GaussPoint&,
				  const std::vector<int>&,
				  FluxSysMap&,
				  SmallSystem*,
				  const CNonlinearSolver*,
				  LinearizedSystem&) const;

#if DIM==2
  virtual void boundary_integral(const CSubProblem*, LinearizedSystem*,
				 const Flux*, 
				 const BoundaryEdge*, const EdgeGaussPoint&, 
				 const FluxNormal *)
    const;
#else // DIM==3
  virtual void boundary_integral(const CSubProblem*, LinearizedSystem*,
				 const Flux*, const Element*,
				 const GaussPoint&, const FluxNormal*) const;
#endif // DIM==3
  virtual int integration_order(const Element*) const;

  virtual IteratorP iterator() const;
  virtual IndexP componenttype() const;
  virtual IndexP getIndex(const std::string&) const;

  virtual const std::string &classname() const;
  virtual bool allow_boundary_conditions() const { return false; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


class NaturalEquation : public Equation {
public:
  NaturalEquation(const std::string &name, int d);
   
  virtual void make_linear_system(const CSubProblem*, const Element*,
 				  const GaussPoint&,
				  const std::vector<int>&,
 				  FluxSysMap&,
 				  SmallSystem*,
				  const CNonlinearSolver*,
 				  LinearizedSystem&) const;

#if DIM==2
  virtual void boundary_integral(const CSubProblem*, LinearizedSystem*,
 				 const Flux*, 
 				 const BoundaryEdge*, const EdgeGaussPoint&, 
 				 const FluxNormal *) const;
#else // DIM==3
  virtual void boundary_integral(const CSubProblem*, LinearizedSystem*,
				 const Flux*, const Element*,
				 const GaussPoint&, const FluxNormal*) const;
#endif // DIM==3

  virtual int integration_order(const Element*) const;
  virtual IteratorP iterator() const;
  virtual IndexP componenttype() const;
  virtual IndexP getIndex(const std::string&) const;
  virtual const std::string &classname() const;
  virtual bool allow_boundary_conditions() const { return false; }

};


#endif
