// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// dielectric permittivity property

#ifndef PERMITTIVITY_H
#define PERMITTIVITY_H


#include "engine/property.h"
#include "engine/symmmatrix.h"
#include "common/pythonexportable.h"
#include "engine/smallsystem.h"
#include <string>

class CSubProblem;
class Element;
class Equation;
class ElementNodeIterator;
class Material;
class OrientationPropBase;
class OutputVal;
class PropertyOutput;
class ScalarField;
class VectorFlux;

class DielectricPermittivity : public FluxProperty {
public:
  DielectricPermittivity(PyObject *registry, const std::string &name);
  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*,
			   const MasterPosition&,
			   double time,
			   SmallSystem*) const;

  virtual void cross_reference(Material*) = 0;
  virtual void output(FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*);
  virtual const SymmMatrix3 permittivityTensor(const FEMesh *mesh,
						const Element *element,
						const MasterPosition&x)
    const = 0;
  virtual int integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return true; }
protected:
  SymmMatrix3 permittivitytensor_;
  ScalarField *voltage;
  VectorFlux *total_polarization;
};

class IsoDielectricPermittivity : public DielectricPermittivity {
public:
  IsoDielectricPermittivity(PyObject *registry,
		      const std::string &name, double epsilon);
  virtual void cross_reference(Material*) {}
  virtual void precompute(FEMesh*);
  virtual const SymmMatrix3 permittivityTensor(const FEMesh *mesh,
					       const Element *element,
					       const MasterPosition&x) const
  {
    return permittivitytensor_;
  }
  virtual void output(FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*);
private:
  double epsilon_;
};

class AnisoDielectricPermittivity : public DielectricPermittivity {
public:
  AnisoDielectricPermittivity(PyObject *registry,
			    const std::string &name,
			    SymmMatrix3 *epsilon);
  virtual void cross_reference(Material*); // finds Orientation
  virtual void precompute(FEMesh*);
  virtual const SymmMatrix3 permittivityTensor(const FEMesh *mesh,
					       const Element *element,
					       const MasterPosition &x) const;
  virtual void output(FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*);
private:
  SymmMatrix3 epsilon_;
  OrientationPropBase *orientation;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// distributed charge density

class ChargeDensity : public EqnProperty {
private:
  double q_;
  VectorFlux *total_polarization;
public:
  ChargeDensity(PyObject *registry, const std::string &name, double qd);
  double rho() { return q_; }
  virtual int integration_order(const CSubProblem*, const Element*) const;
  virtual void force_value(const FEMesh*, const Element*,
			   const Equation*, const MasterPosition&,
			   double time, SmallSystem *) const;
  virtual bool constant_in_space() const { return true; }
  virtual void output(FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*);
};

#endif	// PERMITTIVITY_H
