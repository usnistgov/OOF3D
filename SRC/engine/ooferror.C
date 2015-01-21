// -*- C++ -*-
// $RCSfile: ooferror.C,v $
// $Revision: 1.11.2.1 $
// $Author: langer $
// $Date: 2012/03/13 15:01:13 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/tostring.h"
#include "engine/ooferror.h"
#include <iostream>

const std::string ErrNoSuchField::pythonequiv() const {
  return "ErrNoSuchField(\"" + field + "\")";
}

const std::string ErrDuplicateField::pythonequiv() const {
  return "ErrDuplicateField('" + field + "','"
    + newtype + "','" + oldtype + "')";
}

ErrNoSuchProperty::ErrNoSuchProperty(const std::string &mat,
				     const std::string &prop)
  : ErrUserErrorBase<ErrNoSuchProperty>(
         "Material \"" + mat + "\" has no property of type \"" + prop + "\"."),
    material(mat),
    propname(prop)
{} 

const std::string ErrNoSuchProperty::pythonequiv() const {
  return "ErrNoSuchProperty('" + material + "', '" + propname + "')";
}


ErrConvergenceFailure::ErrConvergenceFailure(const std::string &op, int n)
  : ErrUserErrorBase<ErrConvergenceFailure>(
	    op + " failed to converge in " + to_string(n) + " steps"),
      operation(op), nsteps(n)
{}

const std::string ErrConvergenceFailure::pythonequiv() const {
  return "ErrConvergenceFailure('" + operation + "'," + to_string(nsteps)+")";
}

ErrTimeStepTooSmall::ErrTimeStepTooSmall(double timestep)
  : ErrUserErrorBase<ErrTimeStepTooSmall>(
		     "Timestep " + to_string(timestep) + " is too small."
					  ),
    timestep(timestep)
{}

const std::string ErrTimeStepTooSmall::pythonequiv() const {
  return "ErrTimeStepTooSmall(" + to_string(timestep) + ")";
}

ErrBadMaterial::ErrBadMaterial(const std::string &name)
  : ErrUserErrorBase<ErrBadMaterial>(
		     "Material \"" + name + "\" is badly formed."),
    name(name)
{}
