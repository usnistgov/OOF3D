// -*- C++ -*-
// $RCSfile: propertyoutput.swg,v $
// $Revision: 1.15.10.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:02 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PROPERTYOUTPUT_SWG
#define PROPERTYOUTPUT_SWG

%module propertyoutput

%include "engine/typemaps.swg"
%extern "engine/properties.swg"
%{
#include "engine/IO/propertyoutput.h"
%}

%pragma(python) include="engine/IO/propertyoutput.spy"

// PropertyOutput initializers

class PropertyOutputInit {};

class ScalarPropertyOutputInit : public PropertyOutputInit {
public:
  ScalarPropertyOutputInit();
};

class TwoVectorPropertyOutputInit : public PropertyOutputInit {
public:
  TwoVectorPropertyOutputInit();
};

class ThreeVectorPropertyOutputInit : public PropertyOutputInit {
public:
  ThreeVectorPropertyOutputInit();
};

class SymmMatrix3PropertyOutputInit : public PropertyOutputInit {
public:
  SymmMatrix3PropertyOutputInit();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PropertyOutput {
public:
  ~PropertyOutput();
  const string &name();
  %new OutputValueVec *evaluate(FEMesh*, Element*, PropertyOutputInit*,
				MasterCoordVec*);
  double getFloatParam(char*);
  int getIntParam(char*);
  %new const string *getStringParam(char*);
  %new const string *getEnumParam(char*);
  %new const string *getRegisteredParamName(char*);
};

class PropertyOutputRegistration {
public:
  PropertyOutputRegistration(char*, PropertyOutputInit*);
  ~PropertyOutputRegistration();
  const string &name();
  const PropertyOutputInit *initializer();
  %new PropertyOutput *instantiate(PyObject*);
};


#endif	// PROPERTYOUTPUT_SWG
