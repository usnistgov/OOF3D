// -*- C++ -*-
// $RCSfile: propertyoutput.h,v $
// $Revision: 1.21.18.3 $
// $Author: langer $
// $Date: 2013/11/08 20:45:01 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PROPERTYOUTPUT_H
#define PROPERTYOUTPUT_H

#include <Python.h>

class PropertyOutput;
class PropertyOutputInit;

#include "common/pythonexportable.h"
#include <string>
#include <vector>

class Element;
class FEMesh;
class MasterCoord;
class OutputVal;
class OutputValue;
class Property;


class PropertyOutputInit {
public:
  virtual ~PropertyOutputInit() {}
  virtual OutputVal *operator()(const PropertyOutput*, const FEMesh*,
				const Element*, const MasterCoord&) const = 0;
};

class ScalarPropertyOutputInit : public PropertyOutputInit {
public:
  OutputVal *operator()(const PropertyOutput*, const FEMesh*,
			const Element*, const MasterCoord&) const;
};

class TwoVectorPropertyOutputInit : public PropertyOutputInit {
public:
  OutputVal *operator()(const PropertyOutput*, const FEMesh*,
			const Element*, const MasterCoord&) const;
};

class ThreeVectorPropertyOutputInit : public PropertyOutputInit {
public:
  OutputVal *operator()(const PropertyOutput*, const FEMesh*,
			const Element*, const MasterCoord&) const;
};

class SymmMatrix3PropertyOutputInit : public PropertyOutputInit {
public:
  OutputVal *operator()(const PropertyOutput*, const FEMesh*,
			const Element*, const MasterCoord&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PropertyOutput {
private:
  const std::string name_;
  PyObject* params_;
  const int index_;
public:
  PropertyOutput(const std::string &name, PyObject *params);
  virtual ~PropertyOutput();
  const std::string &name() const { return name_; }
  int index() const { return index_; }
  std::vector<OutputValue> *evaluate(FEMesh*, Element*,
				     const PropertyOutputInit*,
				     const std::vector<MasterCoord*>*);

  // These functions retrieve the values of the Python parameters
  // defined in the PropertyOutputRegistration.  The 'name' argument
  // is the name of the parameter.  It's a char* because that's what
  // Python expects to get.
  double getFloatParam(const char *name) const;
  int getIntParam(const char *name) const;
  const std::string *getStringParam(const char *name) const;
  const std::string *getEnumParam(const char *name) const;
  const std::string *getRegisteredParamName(const char *name) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The bare PropertyOutputRegistration defined here should not be used
// directly.  propertyoutput.spy defines some Python classes derived
// from PropertyOutputRegistration that should be used instead.  Those
// do useful things like create actual Output objects of the correct
// type, and handle the registration's parameters.

class PropertyOutputRegistration {
private:
  const std::string name_;
  const int index_;
  const PropertyOutputInit *initializer_;
  static std::vector<PropertyOutputRegistration*> &allPropertyOutputRegs();
public:
  PropertyOutputRegistration(const std::string &name,
			     const PropertyOutputInit *init);
  const std::string &name() const { return name_; }
  int index() const { return index_; }
  PropertyOutput *instantiate(PyObject *params) const {
    return new PropertyOutput(name(), params);
  }
  const PropertyOutputInit *initializer() const { return initializer_; }

  friend PropertyOutputRegistration *getPropertyOutputReg(const std::string&);
  friend int nPropertyOutputRegistrations();
};

// gcc 4.1.0 by default does not see friend functions declared in classes
PropertyOutputRegistration *getPropertyOutputReg(const std::string&);
int nPropertyOutputRegistrations();

#endif // PROPERTYOUTPUT_H
