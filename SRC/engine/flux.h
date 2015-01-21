// -*- C++ -*-
// $RCSfile: flux.h,v $
// $Revision: 1.48.4.6 $
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

#ifndef FLUX_H
#define FLUX_H

class Flux;

#include "common/coord_i.h"
#include "common/identification.h"
#include "common/pythonexportable.h"
#include "engine/fieldindex.h"
#include <vector>
#include <string>
#include <Python.h>

class BoundaryEdge;
class CSubProblem;
class CSubProblem;
class EdgeGaussPoint;
class EdgeNodeIterator;
class Element;
class ElementFuncNodeIterator;
class Equation;
class FEMesh;
class Field;
class FieldIndex;
class FluxNormal;
class GaussPoint;
class IteratorP;
class LinearizedSystem;
class MasterPosition;
class OutputVal;
class OutputValue;
class SmallMatrix;
class SmallSystem;


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class Flux : public IdentifiedObject, public PythonExportable<Flux> {
private:
  static const std::string modulename_;
  const std::string name_;
  int index_;
protected:
  // Eqnlist made protected so that the boundary_integral methods of
  // the derived classes can see it.
  std::vector<Equation*> eqnlist;

  int dim;			// number of components
  int divdim;			// number of components in divergence
public:
  Flux(const std::string &name, int dimension, int divdim);
  virtual ~Flux() {}
  static std::vector<Flux*> &allfluxes();
  static Flux *getFlux(const std::string &name);
  int index() const { return index_; }
  virtual const std::string &classname() const = 0;
  virtual const std::string &modulename() const { return modulename_; }

  int ndof() const { return dim; }
  virtual int divergence_dim() const { return divdim; }
  const std::vector<Equation*> &getEqnList() const { return eqnlist; }

  void addEquation(Equation*);	// this flux appears in this equation

  const std::string &name() const { return name_; }


  virtual IteratorP iterator(Planarity) const = 0;
  virtual IteratorP divergence_iterator() const = 0;
  virtual IteratorP out_of_plane_iterator() const = 0;
  virtual IndexP componenttype() const = 0;
  virtual IndexP getIndex(const std::string&) const = 0;
  virtual IndexP getOutOfPlaneIndex(const std::string&) const = 0;
  virtual IndexP divergence_componenttype() const = 0;
  virtual IndexP divergence_getIndex(const std::string&) const = 0;

  // Create a SmallSystem object for use while accumulating the
  // components of the local stiffness matrix, flux offsets, and right
  // hand side.  This returns a 'new'd object.
  SmallSystem *initializeSystem(const Element*) const;

#if DIM==2
  virtual OutputVal *contract(const FEMesh*, const Element*,
			      const EdgeGaussPoint&) const = 0;
#else  // DIM==3
  virtual OutputVal *contract(const FEMesh*, const Element*,
			      const GaussPoint&) const = 0;
#endif // DIM==3

  DoubleVec *evaluate(const FEMesh*, const Element*, const MasterPosition&)
    const;

  OutputValue output(const FEMesh*, const Element*, const MasterPosition&)
    const;
  virtual OutputValue newOutputValue() const = 0;

  int eqn_integration_order(const CSubProblem*, const Element*) const;

  virtual std::vector<int> contraction_map(int) const = 0;
  virtual const std::vector<int> &outofplane_map() const = 0;

#if DIM==2
  void boundary_integral(const CSubProblem*, LinearizedSystem*,
			 const BoundaryEdge*, const EdgeGaussPoint&,
			 const FluxNormal *) const;
  // local_boundary computes the integrand for the boundary integrals
  // in the divergence equation.
  virtual void local_boundary(const BoundaryEdge*, EdgeNodeIterator&,
			      const EdgeGaussPoint&, const FluxNormal *,
			      DoubleVec&) const = 0;
  virtual FluxNormal *BCCallback(const Coord&,
				 double,
				 const Coord&,
				 const double, const double,
				 PyObject *, const PyObject *)
    const = 0;
#else // DIM==3
  void boundary_integral(const CSubProblem*, LinearizedSystem*,
			 const Element*, const GaussPoint&,
			 const FluxNormal*) const;
  // local_boundary computes the integrand for the boundary integrals
  // in the divergence equation.
  virtual void local_boundary(const ElementFuncNodeIterator&,
			      const GaussPoint&, const FluxNormal *,
			      DoubleVec&) const = 0;
  virtual FluxNormal *BCCallback(const Coord&,
				 double,
				 const Coord&,
				 PyObject *, const PyObject *)
    const = 0;
#endif // DIM==3



  friend bool operator==(const Flux&, const Flux&);
  friend bool operator!=(const Flux&, const Flux&);
};

std::ostream &operator<<(std::ostream&, const Flux&);

// // for std::pair
// inline bool operator<(const Flux &a, const Flux &b) {
//   return a.name()!=b.name();
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#define VEC_FLUX_DIM 3
#define VEC_DIV_DIM 1	// dimension of the divergence

class VectorFlux : public Flux {
private:
  static std::vector<int> contraction_map_;
  static std::vector<int> outofplane_map_;
public:
  static std::vector<int> build_contraction_map();
  static std::vector<int> build_outofplane_map();
  VectorFlux(const std::string &name)
    : Flux(name, VEC_FLUX_DIM, VEC_DIV_DIM)
  {}

  virtual ~VectorFlux() {}
  virtual const std::string &classname() const;

  virtual std::vector<int> contraction_map(int) const;
  virtual const std::vector<int> &outofplane_map() const;

#if DIM==2
  virtual void local_boundary(const BoundaryEdge*, EdgeNodeIterator&,
			      const EdgeGaussPoint&,
			      const FluxNormal *,
			      DoubleVec&) const;
  virtual FluxNormal *BCCallback(const Coord&,
				 double,
				 const Coord&,
				 const double, const double,
				 PyObject *, const PyObject *)
    const;
#else // DIM==3
  virtual void local_boundary(const ElementFuncNodeIterator&,
			      const GaussPoint&, const FluxNormal *,
			      DoubleVec&) const;
  virtual FluxNormal *BCCallback(const Coord&,
				 double,
				 const Coord&,
				 PyObject *, const PyObject *)
    const;
#endif // DIM==3

  virtual IteratorP iterator(Planarity) const;
  virtual IteratorP divergence_iterator() const;
  virtual IteratorP out_of_plane_iterator() const;
  virtual IndexP componenttype() const;
  virtual IndexP getIndex(const std::string&) const;
  virtual IndexP getOutOfPlaneIndex(const std::string&) const;
  virtual IndexP divergence_componenttype() const;
  virtual IndexP divergence_getIndex(const std::string&) const;

#if DIM==2
  virtual OutputVal *contract(const FEMesh*, const Element*,
			      const EdgeGaussPoint&) const;
#else // DIM==3
  virtual OutputVal *contract(const FEMesh*, const Element*,
			      const GaussPoint&) const;
#endif // DIM==3
  virtual OutputValue newOutputValue() const;

};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#define SYMTEN_FLUX_DIM 6	// independent components of a 3x3 symm. matrix
#define SYMTEN_DIV_DIM DIM // dimension of the divergence

// The divergence f_z = d_i sigma_iz is *two* dimensional when
// DIM is 2, even though the flux sigma is always 3x3 tensor.  If
// the flux is in-plane, then f_z = 0 since sigma_iz = 0.  If the flux
// isn't in-plane, then f_z can be solved for after sigma_iz is found,
// but it can't be specified as part of the problem.

class SymmetricTensorFlux : public Flux {
private:
  static std::vector< std::vector<int> > contraction_map_;
  static std::vector<int> outofplane_map_;
public:
  static std::vector< std::vector<int> > build_contraction_map();
  static std::vector<int> build_outofplane_map();
  SymmetricTensorFlux(const std::string &name)
    : Flux(name, SYMTEN_FLUX_DIM, SYMTEN_DIV_DIM)
  {}
  virtual ~SymmetricTensorFlux() {}
  virtual const std::string &classname() const;

  virtual std::vector<int> contraction_map(int) const;
  virtual const std::vector<int> &outofplane_map() const;
#if DIM==2
  virtual void local_boundary(const BoundaryEdge*, EdgeNodeIterator&,
			      const EdgeGaussPoint&,
			      const FluxNormal *,
			      DoubleVec&) const;
  virtual FluxNormal *BCCallback(const Coord&,
				 double,
				 const Coord&,
				 const double, const double,
				 PyObject *, const PyObject *)
    const;
#else // DIM==3
  virtual void local_boundary(const ElementFuncNodeIterator&,
			      const GaussPoint&, const FluxNormal*,
			      DoubleVec&) const;
  virtual FluxNormal *BCCallback(const Coord&,
				 double,
				 const Coord&,
				 PyObject *, const PyObject *)
    const;
#endif // DIM==3

#if DIM==2
  virtual OutputVal *contract(const FEMesh*, const Element*,
			      const EdgeGaussPoint&) const;
#else // DIM==3
  virtual OutputVal *contract(const FEMesh*, const Element*,
			      const GaussPoint&) const;
#endif // DIM==3

  virtual OutputValue newOutputValue() const;

  virtual IteratorP iterator(Planarity) const;
  virtual IteratorP divergence_iterator() const;
  virtual IteratorP out_of_plane_iterator() const;
  virtual IndexP componenttype() const;
  virtual IndexP getIndex(const std::string&) const;
  virtual IndexP getOutOfPlaneIndex(const std::string&) const;
  virtual IndexP divergence_componenttype() const;
  virtual IndexP divergence_getIndex(const std::string&) const;

  // Ideally, all arguments here would be const, but the first
  // PyObject* gets passed to PyEval_CallObject, which itself does
  // not have const arguments.
};


// Utilities used by the Python interface
Flux *getFluxByIndex(int);
int countFluxes();

#endif // FLUX_H
