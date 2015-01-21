// -*- C++ -*-
// $RCSfile: material.swg,v $
// $Revision: 1.48.2.13 $
// $Author: langer $
// $Date: 2013/11/08 20:44:29 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MATERIAL_SWG
#define MATERIAL_SWG

%module material
%include "engine/typemaps.swg"
%{
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/material.h"
#include "engine/property.h"
#include "common/pixelgroup.h"
#include "common/ccolor.h"
#include "common/vtkColorLUT.h"
  typedef const std::string MaterialType;
%}

%pragma(python) include="engine/material.spy"
%extern "common/pixelattribute.swg"
%pragma(python) code="from ooflib.SWIG.common.pixelattribute import PxlAttributeRegistrationPtr"
%extern "common/timestamp.swg"
%pragma(python) code="from ooflib.SWIG.common.timestamp import TimeStampPtr;"
%extern "engine/femesh.swg"
%extern "common/imagebase.swg"
%pragma(python) code="from ooflib.SWIG.common.imagebase import ImageBasePtr"


%typemap(python, out) Property* {
  $target = $source->pythonObject();
  if(!$target)
    return 0;
}

// Convert a std::string& to a MaterialType Enum
%typemap(python, out) MaterialType {
  // typemap(python, out) MaterialType*
  static PyObject *MaterialTypeEnum = 0;
  if(!MaterialTypeEnum) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.material");
    MaterialTypeEnum = PyObject_GetAttrString(module, "MaterialType");
    Py_XDECREF(module);
    if(!MaterialTypeEnum) return 0;
    Py_XINCREF(MaterialTypeEnum);
  }
  PyObject *arglist = Py_BuildValue("(s)", $source->c_str());
  $target = PyEval_CallObject(MaterialTypeEnum, arglist);
  Py_XDECREF(arglist);
}

class CMicrostructure;
class LinearizedSystem;
class PixelSet;
class Property;

class Material {
public:
  Material(char *name, char* materialtype);
  ~Material();
  const string &name();
  void rename(char *newname);

  MaterialType type();

  void add1Property(Property *newprop);
  void remove1Property(Property *oldprop);
  Property *fetchProperty(char *name);
  Property *getProperty(int);
  int nProperties();

  void registerPropertyType(Property *p, char* name);
  void registerFlux(Property*, Flux*);
  void registerEqn(Property*, Equation*);
  void registerOutput(Property*, char*);

  void clear_xref();
  bool self_consistent();
  void set_consistency(bool);
  void cprecompute(CSubProblem*);
  void begin_element(CSubProblem*, Element*);
  void end_element(CSubProblem*, Element*);
  bool contributes_to_flux(Flux*);

  bool cleanAttributes(CMicrostructure*);

  void assignToPixels(CMicrostructure*, ICoordVec *iPointList);
  void assignToPixelGroup(CMicrostructure*, PixelSet*);
  void assignToAllPixels(CMicrostructure*);
};

class MaterialAttributeRegistration : public PxlAttributeRegistration {
public:
  MaterialAttributeRegistration();
};

%new MaterialVec *getMaterials(CMicrostructure*);
Material *getMaterialFromCategory(CMicrostructure*, int);
Material *getMaterialFromPoint(CMicrostructure*, ICoord *iPoint);
void removeMaterialFromPixels(CMicrostructure*, PixelSet*);
void removeAllMaterials(CMicrostructure*);
TimeStamp getMaterialTimeStamp(CMicrostructure*);
vtkLookupTablePtr getMaterialColorLookupTable(CMicrostructure*, CColor*,
					      CColor*);

class MaterialImage : public ImageBase {
public:
  MaterialImage(CMicrostructure*, CColor*, CColor*);
  //void fillstringimage(StringImage*);
  vtkImageData* getVTKImageData() const;
};

%typemap(python,out) Property*;

#endif // MATERIAL_SWG
