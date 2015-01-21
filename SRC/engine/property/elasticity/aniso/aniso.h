// -*- C++ -*-
// $RCSfile: aniso.h,v $
// $Revision: 1.17.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:29 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ANISOELASTICITY_H
#define ANISOELASTICITY_H

#include "engine/property/elasticity/elasticity.h"
#include "engine/property/elasticity/cijkl.h"
#include "common/pythonexportable.h"
#include <string>

class OrientationPropBase;

// Because CAnisoElasticity is a PythonExportable class that is
// subclassed in Python, it must be derived from PythonNative.

class CAnisoElasticity
  : public Elasticity, virtual public PythonNative<Property>
{
public:
  CAnisoElasticity(PyObject *registry, PyObject *self, 
		  const std::string &nm, const Cijkl &c)
    :   PythonNative<Property>(self),
	Elasticity(nm, registry),
	orientation(0),
	crystal_cijkl_(c)
  {}
  virtual ~CAnisoElasticity() {}
  virtual const Cijkl cijkl(const FEMesh*, const Element*,
			    const MasterPosition&) const;
  virtual const Cijkl &crystal_cijkl() const;
private:
  const OrientationPropBase *orientation;
  virtual void precompute(FEMesh*);
  virtual void cross_reference(Material*);
  Cijkl crystal_cijkl_;
  Cijkl lab_cijkl;
};


#endif // ANISOELASTICITY_H
