// -*- C++ -*-
// $RCSfile: ooferror.h,v $
// $Revision: 1.10.4.4 $
// $Author: langer $
// $Date: 2014/07/22 21:02:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef ENGINE_OOFERROR_H
#define ENGINE_OOFERROR_H

#include "common/ooferror.h"

class ErrNoSuchField : public ErrUserErrorBase<ErrNoSuchField> {
private:
  const std::string field;
public:
  ErrNoSuchField(const std::string &field)
    : ErrUserErrorBase<ErrNoSuchField>("No such field: " + field),
      field(field)
  {}
  virtual ~ErrNoSuchField() {}
  virtual const std::string pythonequiv() const;

};

class ErrDuplicateField : public ErrUserErrorBase<ErrDuplicateField> {
private:
  const std::string field;
  const std::string oldtype;
  const std::string newtype;
public:
  ErrDuplicateField(const std::string &field,
		    const std::string &newtype,
		    const std::string &oldtype)
    : ErrUserErrorBase<ErrDuplicateField>("New field " + field + " of type " + newtype + " conflicts with old field of type " + oldtype),
      field(field),
      oldtype(oldtype),
      newtype(newtype)
  {}
  virtual ~ErrDuplicateField() {}
  virtual const std::string pythonequiv() const;

};

// Trying to get a property that a Material doesn't have.

class ErrNoSuchProperty : public ErrUserErrorBase<ErrNoSuchProperty> {
private:
  const std::string material;
public:
  ErrNoSuchProperty(const std::string &mat, const std::string &prop);
  const std::string propname;
  virtual const std::string pythonequiv() const;
};

class ErrPropertyMissing : public ErrUserErrorBase<ErrPropertyMissing> {
private:
  const std::string material;
  const std::string propname;
  const std::string missingprop;
public:
  ErrPropertyMissing(const std::string &mat, const std::string &prop,
		     const std::string &miss)
    : ErrUserErrorBase<ErrPropertyMissing>(
		    "Property \"" + prop + "\" in Material \"" + mat +
		    "\" requires a Property of class \"" + miss + "\""),
    material(mat),
    propname(prop),
    missingprop(miss)
  {}
  virtual const std::string pythonequiv() const {
    return "ErrPropertyMissing('"
      + material + "','" + propname + "','" + missingprop + "')";
  }
};

class ErrRedundantProperty : public ErrUserErrorBase<ErrRedundantProperty> {
private:
  std::string tag;
public:
  ErrRedundantProperty(const std::string &t)
    :  ErrUserErrorBase<ErrRedundantProperty>(""), tag(t)
  {}
  const std::string &get_tag() { return tag; }
  virtual const std::string pythonequiv() const {
    return "ErrRedundantProperty('" + tag + "')";
  }
};

class ErrBadMaterial : public ErrUserErrorBase<ErrBadMaterial> {
private:
  const std::string name;
public:
  ErrBadMaterial(const std::string &name);
  virtual const std::string pythonequiv() const {
    return "ErrBadMaterial('" + name + "')";
  }
  const std::string &materialName() const { return name; }
};

class ErrConvergenceFailure : public ErrUserErrorBase<ErrConvergenceFailure> {
private:
  const std::string operation;
  const int nsteps;
public:
  ErrConvergenceFailure(const std::string &op, int n);   
  virtual const std::string pythonequiv() const;
};

class ErrInstabilityError : public ErrUserErrorBase<ErrInstabilityError> {
public:
  ErrInstabilityError(const std::string &m)
    : ErrUserErrorBase<ErrInstabilityError>(m) 
  {}
  virtual const std::string pythonequiv() const {
    return "ErrInstabilityError('" + msg + "')";
  }
};

class ErrTimeStepTooSmall : public ErrUserErrorBase<ErrTimeStepTooSmall> {
private:
  double timestep;
public:
  ErrTimeStepTooSmall(double timestep);
  virtual const std::string pythonequiv() const;
};

class ErrInvalidDestination: public ErrUserErrorBase<ErrInvalidDestination> {
public:
  ErrInvalidDestination() :
    ErrUserErrorBase<ErrInvalidDestination>("")
  {}
  virtual const std::string pythonequiv() const {
    return "ErrInvalidDestination()";
  }
};

// class ErrSearchFailure : public ErrErrorBase<ErrSearchFailure> {
// public:
//   virtual const std::string pythonequiv() const {
//     return "ErrSearchFailure";
//   }
//   virtual const std::string *summary() const {
//     return new std::string("Internal search error");
//   }
// };


#endif // ENGINE_OOFERROR_H
