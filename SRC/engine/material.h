// -*- C++ -*-
// $RCSfile: material.h,v $
// $Revision: 1.60.8.18 $
// $Author: langer $
// $Date: 2014/12/14 22:49:20 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef MATERIAL_H
#define MATERIAL_H

#include "common/ccolor.h"
#include "common/coord_i.h"
#include "common/identification.h"
#include "common/imagebase.h"
#include "common/pixelattribute.h"
#include "common/timestamp.h"
#include "engine/gausspoint.h"
#include <iostream>
#include <string>
#include <vector>
#include <map>

#if DIM==3
#include <vtkLookupTable.h>
#include <vtkSmartPointer.h>
#endif	// DIM==3

class CColor;
class CNonlinearSolver;
class CSubProblem;
class CMicrostructure;
class Element;
class EqnProperty;
class FEMesh;
class Field;
class Flux;
class FluxProperty;
class Equation;
class LinearizedSystem;
class MasterPosition;
class PixelSet;
class Property;
class PropertyOutput;
class SmallSystem;
class StringImage;

//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//

// MaterialPropertyRegistration associates a Property and a tag, such
// as "Elasticity".  A Material can have at most one Property
// associated with any given tag.  The definition is in material.C.

class MaterialPropertyRegistration;

// MaterialPropertyRegistry handles the MaterialPropertyRegistration
// objects for a Material.

class MaterialPropertyRegistry {
private:
  std::vector<MaterialPropertyRegistration*> reg;
public:
  ~MaterialPropertyRegistry();

  // Register a property under the name "tag"
  void registr(Property *prop, const std::string &tag);
  // Find the property registered with the name "tag"
  Property *fetch(const std::string &tag) const;

  void clear();
#ifdef DEBUG
  void dump(std::ostream&) const;
#endif // DEBUG
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// class for listing the Properties that contribute to a Flux

class FluxPropList : public std::vector<FluxProperty*> {
public:
  // A Flux is active for this material if any of the Properties that
  // contribute to it are active.  A Property is active if all of the
  // Fields it uses are defined.
  bool active(const CSubProblem*) const;
};


// Similar class for properties that contribute to an Equation.

typedef std::vector<EqnProperty*> EqnPropList;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class Material : public IdentifiedObject {
private:
  std::string name_;

  std::string type_;//bulk or interface

  // all Properties of this Material
  std::vector<Property*> property;

  // list of all Properties that contribute to a Flux
  std::vector<FluxPropList> fluxprop;
  typedef std::map<const Flux*, FluxPropList, ltidobject> FluxPropMap;
  FluxPropMap fluxpropmap;

  // list of all Properties that contribute directoy to an equation.
  std::vector<EqnPropList> eqnprop;
  typedef std::map<const Equation*, EqnPropList, ltidobject> EqnPropMap;
  EqnPropMap eqnpropmap;

  // // Lists of active fluxes and equations for the current subproblem.
  // std::vector<Flux*> active_fluxes;
  // std::vector<Equation*> active_eqns;
  // list of all Properties that contribute to a PropertyOutput
  std::vector<std::vector<Property*> > outputprop;
  void clear_fluxproplist();
  void clear_eqnproplist();
  void clear_outputprop();

  TimeStamp timestamp;
  bool self_consistent_;

  Material(const Material&);	// forbidden
public:
  Material();
  Material(const std::string&, const std::string&);
  ~Material();

  const std::string &type(){ return type_; }

  const std::string &name() const { return name_; }

  void rename(std::string newname) { name_ = newname; }

  bool self_consistent() const { return self_consistent_; }
  void set_consistency(bool state) { self_consistent_ = state; }

  // Properties

  MaterialPropertyRegistry registry; // facilitates interproperty communication
  void registerPropertyType(Property *p, const std::string &name);
  void registerFlux(Property *p, const Flux *flux);
  void registerEqn(Property *p, const Equation *eqn);
  bool contributes_to_flux(const Flux *flux) const;
  // fetchProperty uses the property category to retrieve the property
  Property *fetchProperty(const std::string &name) const;
  Property *getProperty(int i) const;
  int nProperties() const { return property.size(); }
  
  void add1Property(Property*);
  void remove1Property(Property*);
  void clear_xref();
  void cprecompute(CSubProblem*); // only precomputes computable properties
  void begin_element(const CSubProblem*, const Element*)
    const;
  void end_element(const CSubProblem*, const Element*) const;

  // PropertyOutputs
  void registerOutput(Property*, const std::string&);
  const std::vector<Property*> &outputProperties(const PropertyOutput*) const;

  bool cleanAttributes(CMicrostructure*) const;

  const TimeStamp &getTimeStamp() const;

  void make_linear_system(const CSubProblem*,
			  const Element*,
			  const GaussPointIterator&,
			  const std::vector<int>&,
			  double time,
			  const CNonlinearSolver*,
			  LinearizedSystem&) const;
  void find_fluxdata(const FEMesh*, const Element*, const Flux*,
		     const MasterPosition&, SmallSystem*) const;

  void post_process(CSubProblem*, const Element*) const;

  int integrationOrder(const CSubProblem*, const Element*) const;

  void assignToPixels(CMicrostructure*, const ICoordVector*) const;
  void assignToPixelGroup(CMicrostructure*, const PixelSet*) const;
  void assignToAllPixels(CMicrostructure*) const;
  // Returns a FluxPropList for a given Flux.
  FluxPropList get_flux_props(const Flux*) const;

  friend std::ostream &operator<<(std::ostream &, const Material&);

#ifdef DEBUG
  void dump(std::ostream&) const;
#endif // DEBUG
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Classes and functions for handling the assignment of Materials to
// pixels in a Microstructure.

class MaterialAttribute : public PixelAttribute {
private:
  const Material *material;
public:
  MaterialAttribute() : PixelAttribute(), material(0) {}
  MaterialAttribute(const Material *m) : PixelAttribute(), material(m) {}
  void set(const Material *m);
  const Material *get() const { return material; }
  virtual bool operator<(const PixelAttribute&) const;
  virtual bool strictLessThan(const PixelAttribute& x) const {
    return operator<(x);
  }
  virtual void print(std::ostream&) const;
};

class MaterialAttributeRegistration : public PxlAttributeRegistration {
private:
  static const std::string classname_;
  static const std::string modulename_;
public:
  MaterialAttributeRegistration();
  virtual ~MaterialAttributeRegistration() {}
  virtual PixelAttribute *createAttribute(const CMicrostructure*) const;
  virtual PixelAttributeGlobalData*
     createAttributeGlobalData(const CMicrostructure*) const;
  
  virtual const std::string &classname() const { return classname_; }
  virtual const std::string &modulename() const { return modulename_; }
};

const Material *getMaterialFromCategory(const CMicrostructure*, int category);
const Material *getMaterialFromPoint(const CMicrostructure*, const ICoord*);
const Material *getMaterial(const CMicrostructure*, const std::string&);
std::vector<const Material*> *getMaterials(const CMicrostructure*);
void removeMaterialFromPixels(CMicrostructure*, const PixelSet*);
void removeMaterialFromPixels(CMicrostructure*, const ICoordVector&);
void removeAllMaterials(CMicrostructure*);
TimeStamp getMaterialTimeStamp(const CMicrostructure*);
vtkSmartPointer<vtkLookupTable> getMaterialColorLookupTable(
				    const CMicrostructure*, 
				    const CColor *noColor,
				    const CColor *noMaterial);

class MaterialImage : public ImageBase {
private:
  CMicrostructure *microstructure;
  const CColor noMaterial;
  const CColor noColor;
public:
  MaterialImage(CMicrostructure*, const CColor*, const CColor*);
  virtual ~MaterialImage() {}
};

#endif
