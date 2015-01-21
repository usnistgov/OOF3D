// -*- C++ -*-
// $RCSfile: largestrain.h,v $
// $Revision: 1.6.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:33 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef CLARGESTRAINELASTICITY_H
#define CLARGESTRAINELASTICITY_H

#include "engine/property/elasticity/elasticity.h"
#include "engine/property/elasticity/cijkl.h"
#include "common/pythonexportable.h"
#include <string>

class OrientationPropBase;


class CLargeStrainElasticity : public Elasticity
{
public:
  CLargeStrainElasticity(PyObject *registry, const std::string &name);
  virtual ~CLargeStrainElasticity() {}
  virtual void flux_matrix(const FEMesh *mesh,
			   const Element *element,
			   const ElementFuncNodeIterator &nu,
			   const Flux *flux,
			   const MasterPosition &x,
			   double time,
			   SmallSystem *fluxmtx) const;
  virtual void geometricStrain(const FEMesh*, const Element*, 
			       const MasterPosition&, SymmMatrix3*) const;
  virtual bool is_symmetric_K(const CSubProblem*) const;
};

class CIsoLargeStrainElasticity
  : public CLargeStrainElasticity, virtual public PythonNative<Property>
{
private:
  Cijkl c_ijkl;
public:
  CIsoLargeStrainElasticity(PyObject *registry, PyObject *self,
			    const std::string &name, const Cijkl &c);
  virtual ~CIsoLargeStrainElasticity() {}
  virtual const Cijkl cijkl(const FEMesh*, const Element*,
			    const MasterPosition&) const
  {
    return c_ijkl;
  }
};

class CAnisoLargeStrainElasticity
  : public CLargeStrainElasticity, virtual public PythonNative<Property>
{
private:
  const OrientationPropBase *orientation;
  virtual void precompute(FEMesh*);
  virtual void cross_reference(Material*);
  Cijkl crystal_cijkl_;
  Cijkl lab_cijkl;
public:
  CAnisoLargeStrainElasticity(PyObject *registry, PyObject *self,
			      const std::string &nm, const Cijkl &c);
  virtual ~CAnisoLargeStrainElasticity() {}
  virtual const Cijkl cijkl(const FEMesh*, const Element*,
			    const MasterPosition&) const;
  virtual const Cijkl &crystal_cijkl() const;
};

#endif	// CLARGESTRAINELASTICITY_H
