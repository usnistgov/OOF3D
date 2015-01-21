// -*- C++ -*-
// $RCSfile: material.C,v $
// $Revision: 1.147.4.41 $
// $Author: langer $
// $Date: 2014/11/24 21:44:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#include "common/IO/oofcerr.h"
#include "common/activearea.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/pixelattribute.h"
#include "common/printvec.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "engine/IO/propertyoutput.h"
#include "engine/cnonlinearsolver.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/equation.h"
#include "engine/equation.h"
#include "engine/femesh.h"
#include "engine/flux.h"
#include "engine/linearizedsystem.h"
#include "engine/mastercoord.h"
#include "engine/material.h"
#include "engine/ooferror.h"
#include "engine/property/color/color.h"
#include "engine/smallsystem.h"

#include <assert.h>
#include <iostream>
#include <vector>
#include <map>

#include <vtkImageMapToColors.h>


//Interface branch
Material::Material(const std::string &nm,
		   const std::string &materialtype)
  : name_(nm),
    type_(materialtype),
    fluxprop(Flux::allfluxes().size()),
    outputprop(nPropertyOutputRegistrations()),
    self_consistent_(true)
{
  // oofcerr << "Material::ctor: " << this << std::endl;
  // Ensure that keys exist in the maps for all the fluxes and
  // equations.  This may not be strictly necessary, since std::maps
  // will create pairs as required by the operator[] function, but it
  // seems wise.

  for(std::vector<Flux*>::const_iterator fi = Flux::allfluxes().begin();
      fi!=Flux::allfluxes().end(); ++fi)
    fluxpropmap[*fi] = FluxPropList();
  for(std::vector<Equation*>::const_iterator ei = Equation::all().begin();
      ei!=Equation::all().end(); ++ei)
    eqnpropmap[*ei] = std::vector<EqnProperty*>();
}

Material::~Material() {
  // oofcerr << "Material::dtor: " << this << std::endl;
}

const TimeStamp &Material::getTimeStamp() const {
  return timestamp;
}

std::ostream &operator<<(std::ostream &os, const Material &mat) {
  os << "Material('" << mat.name();
  for(std::vector<Property*>::size_type i=0; i<mat.property.size(); i++)
    os << ", " << *mat.property[i];
  os << "')";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// Special local class for keeping track of which *types* of
// properties are present in the material.  There can only be one
// property of each type in a well-formed material.

class MaterialPropertyRegistration {
private:
  const std::string tag;
  Property *property;
  MaterialPropertyRegistration(Property *p, const std::string &str)
    : tag(str), property(p)
  {}
  friend class MaterialPropertyRegistry;
};

// Register a property under the name "tag"
void MaterialPropertyRegistry::registr(Property *prop, const std::string &tag) {
  if(fetch(tag)) {		// Can't have two Properties with the same name
    throw ErrRedundantProperty(tag);
  }
  reg.push_back(new MaterialPropertyRegistration(prop, tag));
}

// Find the property registered with the name "tag"
Property *MaterialPropertyRegistry::fetch(const std::string &tag) const {
  for(std::vector<MaterialPropertyRegistration*>::size_type i=0; i<reg.size();
      i++)
    {
      if(reg[i]->tag == tag) {
	return reg[i]->property;
      }
    }
  return 0;
}

MaterialPropertyRegistry::~MaterialPropertyRegistry() {
  clear();
}

void MaterialPropertyRegistry::clear() {
  for(std::vector<MaterialPropertyRegistration*>::size_type i=0; i<reg.size();
      i++)
    delete reg[i];
  reg.clear();
}

#ifdef DEBUG
void MaterialPropertyRegistry::dump(std::ostream &os) const {
  for(std::vector<MaterialPropertyRegistration*>::size_type i=0; i<reg.size();
      i++)
    {
      os << reg[i]->property->name()
	 << " (" << reg[i]->property->classname() << ") "
	 << reg[i]->tag << std::endl;
    }
}
#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


Property *Material::getProperty(int i) const {
  return property[i];
}


void Material::add1Property(Property *prop) {
  property.push_back(prop);
  ++timestamp;
}

void Material::remove1Property(Property *prop) {
  for(std::vector<Property*>::iterator p=property.begin(); p<property.end();
      ++p)
    {
      if(*p == prop) {
	property.erase(p);
	++timestamp;
	return;
      }
    }
  throw ErrNoSuchProperty(name(), prop->name());
}

void Material::registerPropertyType(Property *p, const std::string &nm) {
  // Called by Property::bookkeeping().
  registry.registr(p, nm);
}

// Return the property whose type is given by the string.
Property *Material::fetchProperty(const std::string &nm) const {
  Property *prop = registry.fetch(nm);
  if(!prop) {
    throw ErrNoSuchProperty(name(), nm);
  }
  return prop;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


void Material::clear_fluxproplist() {
  for(std::vector<FluxPropList>::size_type i=0; i< fluxprop.size(); i++)
    fluxprop[i].clear();
  for(FluxPropMap::iterator fpi=fluxpropmap.begin(); fpi!=fluxpropmap.end();
      ++fpi)
    {
      (*fpi).second.clear();
    }
}

void Material::clear_eqnproplist() {
  for(EqnPropMap::iterator epi=eqnpropmap.begin(); epi!=eqnpropmap.end(); ++epi)
    {
      (*epi).second.clear();
    }
}

void Material::clear_xref() {
  clear_fluxproplist();
  clear_eqnproplist();
  clear_outputprop();
  registry.clear();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Material::registerFlux(Property *prop, const Flux *flux) {
  // This property contributes to this flux.  Called by
  // Property::bookkeeping().
  FluxProperty *p = dynamic_cast<FluxProperty*>(prop);
  fluxprop[flux->index()].push_back(p);
  fluxpropmap[flux].push_back(p);
}

void Material::registerEqn(Property *prop, const Equation *eqn) {
  // This property contributes directly to this equation.  Called by
  // Property::bookkeeping.
  eqnpropmap[eqn].push_back(dynamic_cast<EqnProperty*>(prop));
}

// Routine to query whether or not this material has properties which
// contribute to the indicated flux -- this is true if the
// corresponding fluxprop entry has nonzero length.
bool Material::contributes_to_flux(const Flux *flux) const {
  if (!fluxprop[flux->index()].empty()) {
    return true;
  }
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Material::registerOutput(Property *prop, const std::string &outputname) {
  // The given Property, which is present in this material,
  // contributes to the given PropertyOutput.
  PropertyOutputRegistration *poreg = getPropertyOutputReg(outputname);
  if(!poreg)
    throw ErrProgrammingError("PropertyOutputRegistration " + outputname
			      + " not found!", __FILE__, __LINE__);
  outputprop[poreg->index()].push_back(prop);
}

void Material::clear_outputprop() {
  for(std::vector<std::vector<Property*> >::size_type i=0; i<outputprop.size();
      i++)
    outputprop[i].clear();
};

const std::vector<Property*> &
Material::outputProperties(const PropertyOutput *pout) const {
  return outputprop[pout->index()];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Element start/end.  Since each element has a unique material,
// these can only be called once per element.  The reason they're
// here is because the Material is the one with the handy-dandy
// list of properties.
void Material::begin_element(const CSubProblem *subproblem, const Element *el)
  const
{
  for(std::vector<Property*>::size_type i=0;i<property.size();i++) {
    if(subproblem->currently_active_prop(property[i])) {
      property[i]->begin_element(subproblem, el);
    }
  }
}

void Material::end_element(const CSubProblem *subproblem, const Element *el)
  const
{
  for(std::vector<Property*>::size_type i=0;i<property.size();i++) {
    if(subproblem->currently_active_prop(property[i])) {
      property[i]->end_element(subproblem, el);
    }
  }
}

void Material::cprecompute(CSubProblem *subproblem) {

  // Build the lists of fluxes and equations which have contributions
  // from active fields.  A flux is active if an active property
  // contributes to it, and a property is active if every field it
  // depends on is defined.  An equation is active if it's being
  // solved.
  subproblem->clear_active_fluxes(this);
  std::vector<Flux*> &active_fluxes = subproblem->active_fluxes(this);
  subproblem->clear_active_equations(this);
  std::vector<Equation*> &active_eqns = subproblem->active_equations(this);
  std::vector<Flux*> &flxs = Flux::allfluxes();
  for(std::vector<Flux*>::iterator fi = flxs.begin(); fi!=flxs.end();++fi) {
    if (subproblem->is_active_flux(*(*fi)))
      active_fluxes.push_back(*fi);
  }

  std::vector<Equation*> &eqns = Equation::all();
  for(std::vector<Equation*>::iterator ei = eqns.begin(); ei!=eqns.end();++ei) {
    if (subproblem->is_active_equation(*(*ei)))
      active_eqns.push_back(*ei);
  }
}

int Material::integrationOrder(const CSubProblem *subproblem,
			       const Element *element)
  const
{
  int maxorder = 0;
  const std::vector<Equation*> &active_eqns =
    subproblem->active_equations(this);
  const std::vector<Flux*> &active_fluxes = subproblem->active_fluxes(this);

  for(std::vector<Flux*>::const_iterator fluxi = active_fluxes.begin();
      fluxi != active_fluxes.end(); ++fluxi)
    {
      FluxPropMap::const_iterator stupid = fluxpropmap.find(*fluxi);
      const FluxPropList &flux_prop_list = (*stupid).second;
      const Flux *flux = (*stupid).first;

      // Loop over active FluxEquations that use this flux.
      for(std::vector<Equation*>::const_iterator eqn=flux->getEqnList().begin();
	  eqn!=flux->getEqnList().end(); ++eqn)
	{

	  for(FluxPropList::const_iterator property = flux_prop_list.begin();
	      property != flux_prop_list.end(); ++property)
	    {
	      int order = (*property)->integration_order(subproblem, element) +
		(*eqn)->integration_order(element);
	      if(order > maxorder)
		maxorder = order;
	    }
	}
    }
  
  for(std::vector<Equation*>::const_iterator eqn=active_eqns.begin();
      eqn != active_eqns.end(); ++eqn)
    {
      EqnPropMap::const_iterator stupid = eqnpropmap.find(*eqn);
      const EqnPropList &proplist = (*stupid).second;
      for(std::vector<EqnProperty*>::const_iterator property=proplist.begin();
	  property != proplist.end(); ++property)
	{
	  int order = (*property)->integration_order(subproblem, element) +
	    (*eqn)->integration_order(element);
	  if(order > maxorder)
	    maxorder = order;
	}
	  
    }
  return maxorder;
} // Material::integrationOrder

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Post-processing is initially very simple -- just call each
// member property's post_process routine....
void Material::post_process(CSubProblem *subproblem, const Element *el) const {
  for(std::vector<Property*>::size_type i=0; i<property.size(); i++) {
    property[i]->post_process(subproblem, el);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=
//=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=

// Make_linear_system, already inside the gausspoint loop.
// Called from Element::make_linear_system.
void Material::make_linear_system(const CSubProblem *subproblem,
				  const Element *el,
				  const GaussPointIterator &gpt,
				  const std::vector<int> &dofmap,
				  double time,
				  const CNonlinearSolver *nlsolver,
				  LinearizedSystem &linearized_system)
  const
{
  // By the time we are called, we are promised that cross_reference
  // has been run, and that the material is in a consistent state.
  GaussPoint pt = gpt.gausspoint(); // current gauss pt from gauss pt iterator
  FEMesh *mesh = subproblem->mesh;

  FluxSysMap fluxdata;

  const std::vector<Flux*> &active_fluxes = subproblem->active_fluxes(this);

  for (std::vector<Flux*>::const_iterator fluxi = active_fluxes.begin();
       fluxi != active_fluxes.end(); ++fluxi)
    {
      // "SmallSystem" is a set of 3 matrices and a vector.
      SmallSystem *flux_small_sys = (*fluxi)->initializeSystem( el );
      SmallSystem *property_flux_info = (*fluxi)->initializeSystem( el );
	  
      // Use "at", because everything is const. Actually, don't use it,
      // because it's not standard.  Use "find" instead.
      FluxPropMap::const_iterator stupid = fluxpropmap.find(*fluxi);
      const FluxPropList &flux_prop_list = (*stupid).second;

      // Compute the flux info for each property associated with current flux.
      // There should only be FluxProperties in the list.
      for (FluxPropList::const_iterator property = flux_prop_list.begin();
           property != flux_prop_list.end(); ++property)
	{
	  // if the property is active in the current subproblem,
	  // calculate its contributions to the active flux
	  if(subproblem->currently_active_prop(*property)) {
	    (*property)->begin_point( mesh, el, (*fluxi), pt );
	    (*property)->make_flux_contributions(mesh, el, *fluxi, pt, time,
						 nlsolver, property_flux_info);
	    (*property)->end_point( mesh, el, (*fluxi), pt );
	    
	    // add the flux contributions of the property to the flux
	    // small system
	    *flux_small_sys += *property_flux_info;
	    property_flux_info->reset();
	  } // End of if (property active in subproblem)
	  
      } // End of active flux property list loop.

      fluxdata[*fluxi] = flux_small_sys;
      delete property_flux_info;
    } // End of active flux loop.

  // Now, for each equation, build the direct contributions
  // in the equation lists.

  // TODO OPT: For point-wise constraint equations, "activity" might be
  // true at some gausspoints and false at others.  We are already
  // inside the gausspoint loop, so for us here it's just true or
  // false, but the question is not answered by the active_eqns
  // iterator.  It may make sense to iterate over these separately,
  // but the constraint handling *property* is still in the material,
  // so we still have to do this in this routine somewhere.

  const std::vector<Equation*> &active_eqns = 
    subproblem->active_equations(this);

  for(std::vector<Equation*>::const_iterator eqn = active_eqns.begin();
      eqn != active_eqns.end();  ++eqn)
  {
    SmallSystem *eqndata = (*eqn)->initializeSystem( el );
    SmallSystem *property_eqn_info = (*eqn)->initializeSystem(el);

    EqnPropMap::const_iterator stupid = eqnpropmap.find(*eqn);
    const EqnPropList &eqn_prop_list = (*stupid).second;

    // TODO 3.1: MAYBE In principle, there could be another begin_point
    // hook here to call the property with the appropriate equation.
    // If such a thing turns out to be needed, follow the begin_point
    // pattern for fluxes.
    for(std::vector<EqnProperty*>::const_iterator property=eqn_prop_list.begin();
	property != eqn_prop_list.end(); ++property)
      {
	if(subproblem->currently_active_prop(*property)) {
	  (*property)->make_equation_contributions(mesh, el, *eqn, pt, time,
						   nlsolver, property_eqn_info);

	  // add the eqn contributions of the property to the eqn
	  // small system
	  *eqndata += *property_eqn_info;
	  property_eqn_info->reset();
	}
      } // End of property loop.
    
    // Finally, we use the computed fluxdata and eqndata to make
    // the contributions to the global vectors and matrices.
    // Here dofmap is the Element's localDoFmap, which maps local
    // element dof indices to global ones.
    (*eqn)->make_linear_system( subproblem, el, pt, dofmap,
			        fluxdata, eqndata,
				nlsolver, linearized_system );
    delete eqndata;
    delete property_eqn_info;
  } // End of equation loop.

  // Clean up fluxdata map.
  for (FluxSysMap::iterator fi = fluxdata.begin(); fi != fluxdata.end(); ++fi) {
    delete (*fi).second;
    (*fi).second = 0;
  }
  // fluxdata object goes out of scope and is destroyed.
} // End of 'Material::make_linear_system'


// find_fluxdata is called by Flux::evaluate when computing a flux
// value. It's not used directly for matrix construction.

void Material::find_fluxdata(const FEMesh *mesh, const Element *el,
			     const Flux *flux, const MasterPosition &mpos,
			     SmallSystem *fluxdata) const {
  FluxPropMap::const_iterator stupid = fluxpropmap.find(flux);
  const FluxPropList &fpl = (*stupid).second;
  double time = mesh->getCurrentTime();
  
  for(FluxPropList::const_iterator fp=fpl.begin(); fp!=fpl.end(); ++fp) {
    (*fp)->begin_point(mesh, el, flux, mpos);
    // Instead of checking fields, we rely on the field-evaluation
    // exception, because field activities are not necessarily set
    // correctly except during linearized-system construction.
    try {
      (*fp)->flux_value(mesh, el, flux, mpos, time, fluxdata);
    }
    catch (ErrNoSuchField &exc) {
    }
    (*fp)->end_point(mesh, el, flux, mpos);
  }
}

//=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=

// Returns a FluxPropList for a given Flux.

FluxPropList Material::get_flux_props(const Flux *fluks) const
{
  return fluxprop[fluks->index()];
}

#ifdef DEBUG
void Material::dump(std::ostream &os) const {
  os << "Material " << name() << ":" << std::endl;
  registry.dump(os);
}

#endif // DEBUG

//=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=

// Materials are assigned to Microstructure pixels with a
// PixelAttribute class.  See common/pixelattribute.h for details.

const std::string
MaterialAttributeRegistration::classname_("MaterialAttributeRegistration");
const std::string
MaterialAttributeRegistration::modulename_("ooflib.SWIG.engine.material");

// reg is initialized by the MaterialAttributeRegistration
// constructor, which is invoked from material.spy when the module is
// imported.
static MaterialAttributeRegistration *reg = 0;

class MaterialAttributeGlobalData : public PixelAttributeGlobalData {
public:
  const CMicrostructure *microstructure;

  MaterialAttributeGlobalData(const CMicrostructure *ms)
    : PixelAttributeGlobalData(),
      microstructure(ms)
  {}

  std::vector<const Material*> *getMaterials() const {
    std::vector<const Material*> *mvec = new std::vector<const Material*>;
    for(AttributeSet::iterator it = attributeValues.begin();
	it != attributeValues.end(); ++it)
      {
	MaterialAttribute *m = dynamic_cast<MaterialAttribute*>(*it);
	if(m->get() != 0) {
	  // oofcerr << "MaterialAttributeGlobalData:getMaterials: mat="
	  // 	  << m->get() << std::endl;
	  mvec->push_back(m->get());
	}
      }
    return mvec;
  }

  const Material *getMaterial(const std::string &name) const {
    for(AttributeSet::iterator it=attributeValues.begin();
	it != attributeValues.end(); ++it)
      {
	MaterialAttribute *m = dynamic_cast<MaterialAttribute*>(*it);
	const Material *mat = m->get();
	if(mat && mat->name() == name)
	  return mat;
      }
    return 0;
  }
  
  void removeMaterial(const Material *mat) {
    // Remove the attribute for the given material.  There can be at
    // most one such attribute.
    for(AttributeSet::iterator it=attributeValues.begin();
	it != attributeValues.end(); ++it)
      {
	MaterialAttribute *m = dynamic_cast<MaterialAttribute*>(*it);
	if(m->get() == mat) {
	  attributeValues.erase(it);
	  delete *it;
	  return;
	}
      }
  }

  TimeStamp getTimeStamp() const {
    TimeStamp latest = timeZero;
    const MicrostructureAttributes &attributes =
      microstructure->getMSAttributes();
    attributes.prune();
    for(AttributeVectorSet::const_iterator it = attributes.begin();
	it != attributes.end(); ++it)
      {
	MaterialAttribute *ma =
	  dynamic_cast<MaterialAttribute*>((**it)[reg->index()]);
	if(ma->get() != 0) {
	  const TimeStamp &ts = ma->get()->getTimeStamp();
	  if(ts > latest)
	    latest = ts;
	}
      }
    return latest;
  }

  vtkSmartPointer<vtkLookupTable> getMaterialColorLookupTable(
					      const CColor &noColor,
					      const CColor &noMaterial)
  {
    vtkSmartPointer<vtkLookupTable> lut = 
      vtkSmartPointer<vtkLookupTable>::New();
    lut->SetNumberOfColors(microstructure->nCategories());
    for(int i=0; i<microstructure->nCategories(); ++i) {
      const Material *mat = getMaterialFromCategory(microstructure, i);
      if(mat) {
	try {	
	  Property *cprop = mat->fetchProperty("Color");
	  ColorProp *colorprop = dynamic_cast<ColorProp*>(cprop);
	  const CColor &cc = colorprop->color();
	  lut->SetTableValue(i, cc.getRed(), cc.getGreen(), cc.getBlue(),
			     cc.getAlpha());
	}
	catch(ErrNoSuchProperty &exc) {
	  lut->SetTableValue(i, noColor.getRed(), noColor.getGreen(),
			     noColor.getBlue(), noColor.getAlpha());
	}
      }	// end if(mat)
      else {
	lut->SetTableValue(i, noMaterial.getRed(), noMaterial.getGreen(),
			   noMaterial.getBlue(), noMaterial.getAlpha());
      }
    }
    return lut;
  }
};  // end class MaterialAttributeGlobalData

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MaterialAttributeRegistration::MaterialAttributeRegistration()
  : PxlAttributeRegistration("Material")
{
  reg = this;
}

PixelAttributeGlobalData *
MaterialAttributeRegistration::createAttributeGlobalData(const
							 CMicrostructure *ms)
  const
{
  return new MaterialAttributeGlobalData(ms);
}


PixelAttribute *
MaterialAttributeRegistration::createAttribute(const
					       CMicrostructure *ms) const {
  // Stored in the calling microstructure's attribute map,
  // destroyed along with the microstructure.
  MaterialAttribute *ma =  new MaterialAttribute();
  addToGlobalData(ms, ma);
  return ma;
}

void MaterialAttribute::set(const Material *m) {
  material = m;
}


// Find all the MaterialAttributes in the given microstructure which
// refer to this material, and clear them.  If the attribute change
// map is nontrivial, iterate over all of of the MaterialAttributes
// and check them individually.

bool Material::cleanAttributes(CMicrostructure *ms) const {
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg->globalData(ms));
  MaterialAttribute *matAtt = new MaterialAttribute();
  PixelAttribute *proper = gd->sync(matAtt);
  AttributeVectorMap avm;
  ms->buildAttributeChangeMap(proper, reg->index(), avm);
  if(!PixelAttributeVector::isMapTrivial(avm)) {
    Array<PixelAttributeVector*> &attVec = ms->getAttributeVectors();
    for(Array<PixelAttributeVector*>::iterator j=attVec.begin();
	j!=attVec.end(); ++j) 
      {
	ms->updateAttributeVector(j.coord(), avm);
      }
    ms->recategorize();
  }
  // removeMaterial() must be called even if the material isn't
  // actually used in any pixels, in order to keep the global and
  // local data in sync.
  gd->removeMaterial(this);
  return true;
}


bool MaterialAttribute::operator<(const PixelAttribute &other) const {
  const MaterialAttribute &othermat =
    dynamic_cast<const MaterialAttribute&>(other);
  if(material != 0 && othermat.material != 0)
    return material->name() < othermat.material->name();
  if(material == 0 && othermat.material != 0)
    return true;
  return false;
}

void MaterialAttribute::print(std::ostream &os) const {
  if(material)
    os << "Material(" << material->name() << ")";
  else
    os << "[No Material]";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


void updateHelper(CMicrostructure *ms, AttributeVectorMap &avm,
		  const ICoordVector *pxls) 
{
  const ActiveArea *activearea = ms->getActiveArea();
  if(!PixelAttributeVector::isMapTrivial(avm)) {
    if(activearea->len() == 0) {
      for(ICoordVector::const_iterator i=pxls->begin(); i!=pxls->end(); ++i) {
	ms->updateAttributeVector(*i, avm);
      }
    }
    else {
      for(ICoordVector::const_iterator i=pxls->begin(); i!=pxls->end(); ++i) {
	if(activearea->isActive(*i)) {
	  ms->updateAttributeVector(*i, avm);
	}
      }
    }
    ms->recategorize();
  }
}

void updateHelper(CMicrostructure *ms, AttributeVectorMap &avm) {
  const ActiveArea *activearea = ms->getActiveArea();
  Array<PixelAttributeVector*> &attVec = ms->getAttributeVectors(); 
  if(!PixelAttributeVector::isMapTrivial(avm)) {
    if(activearea->len() == 0) {
      for(Array<PixelAttributeVector*>::iterator j = attVec.begin();
	  j != attVec.end(); ++j)  
	{
	  ms->updateAttributeVector(j.coord(), avm);
	}
    }
    else {
      for(Array<PixelAttributeVector*>::iterator j = attVec.begin();
	  j != attVec.end(); ++j)  
	{
	  if(activearea->isActive(j.coord())) {
	    ms->updateAttributeVector(j.coord(), avm);
	  }
	}
    }
    ms->recategorize();
  }
}

void Material::assignToPixels(CMicrostructure *ms,
			      const ICoordVector *pxls) const
{
#ifdef DEBUG
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg->globalData(ms));
  assert(gd!=0);
#endif
  MaterialAttribute *matAtt = new MaterialAttribute(this);
  PixelAttribute *proper = reg->globalData(ms)->sync(matAtt);
  AttributeVectorMap avm;
  ms->buildAttributeChangeMap(proper, reg->index(), avm);
  updateHelper(ms, avm, pxls);
}

void Material::assignToPixelGroup(CMicrostructure *ms,
				  const PixelSet *pixset) const
{
  // Assign material to the pixels in the given group.
  assignToPixels(ms, pixset->members());
}

void Material::assignToAllPixels(CMicrostructure *ms) const {
#ifdef DEBUG
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg->globalData(ms));
  assert(gd!=0);
#endif
  MaterialAttribute *matAtt = new MaterialAttribute(this);
  PixelAttribute *proper = reg->globalData(ms)->sync(matAtt);
  AttributeVectorMap avm;
  ms->buildAttributeChangeMap(proper, reg->index(), avm);
  updateHelper(ms, avm);
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void removeMaterialFromPixels(CMicrostructure *ms,
			      const ICoordVector &pxls)
{
#ifdef DEBUG
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg-> globalData(ms));
  assert(gd!=0);
#endif
  MaterialAttribute *matAtt = new MaterialAttribute();
  PixelAttribute *proper = reg->globalData(ms)->sync(matAtt);
  AttributeVectorMap avm;
  ms->buildAttributeChangeMap(proper, reg->index(), avm);
  updateHelper(ms, avm, &pxls);
}

void removeMaterialFromPixels(CMicrostructure *ms,
				const PixelSet *pixset)
{
  removeMaterialFromPixels(ms, *pixset->members());
}

void removeAllMaterials(CMicrostructure *ms) {
#ifdef DEBUG
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg-> globalData(ms));
  assert(gd!=0);
#endif
  MaterialAttribute *matAtt = new MaterialAttribute();
  PixelAttribute *proper = reg->globalData(ms)->sync(matAtt);
  AttributeVectorMap avm;
  ms->buildAttributeChangeMap(proper, reg->index(), avm);
  updateHelper(ms, avm);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

TimeStamp getMaterialTimeStamp(const CMicrostructure *ms) {
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg->globalData(ms));
#ifdef DEBUG
  assert(gd!=0);
#endif
  return gd->getTimeStamp();
}

const Material *getMaterialFromCategory(const CMicrostructure *ms,
					int category)
{
  MaterialAttribute *m = dynamic_cast<MaterialAttribute*>
    (ms->getAttributeFromCategory(category, reg->index()));
  return m->get();
}

const Material *getMaterialFromPoint(const CMicrostructure *ms,
				     const ICoord *where)
{
  MaterialAttribute * matAtt = dynamic_cast<MaterialAttribute*>
    (ms->getAttribute(*where, reg->index()));
#ifdef DEBUG
  assert(matAtt!=0);
#endif
  return matAtt->get();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MaterialImage::MaterialImage(CMicrostructure *ms,
			     const CColor *noMaterial,
			     const CColor *noColor)
  : microstructure(ms),
    noMaterial(*noMaterial),
    noColor(*noColor)
{
  
  sizeInPixels_ = microstructure->sizeInPixels();
  size_ = microstructure->size();

  vtkSmartPointer<vtkImageData> mImage = vtkSmartPointer<vtkImageData>::New();
  mImage->SetDimensions(sizeInPixels_);
  mImage->SetScalarTypeToUnsignedChar();
  mImage->SetNumberOfScalarComponents(1);
  mImage->AllocateScalars();

  Coord pixelSize = microstructure->sizeOfPixels();
  mImage->SetSpacing(pixelSize);

  Array<PixelAttributeVector*> &attVec = microstructure->getAttributeVectors();

  for(Array<PixelAttributeVector*>::iterator i=attVec.begin(); i!=attVec.end();
      ++i)
    {
      // SetScalarComponentFromFloat (or Double) is slow
      unsigned char* ptr = (unsigned char*) mImage->GetScalarPointer(
				   i.coord()[0], i.coord()[1], i.coord()[2]);
      *ptr = microstructure->category(i.coord());
    }

  mImage->Update();

  vtkSmartPointer<vtkLookupTable> lut = 
    getMaterialColorLookupTable(microstructure, noColor, noMaterial);
  vtkSmartPointer<vtkImageMapToColors> map =
    vtkSmartPointer<vtkImageMapToColors>::New();
  map->SetLookupTable(lut);
  map->SetOutputFormatToRGBA();
  map->SetInputConnection(mImage->GetProducerPort());
  image = map->GetOutput();
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Return a list of all Materials used in a Microstructure.

std::vector<const Material*> * getMaterials(const CMicrostructure *ms)
{
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg-> globalData(ms));
#ifdef DEBUG
  assert(gd!=0);
#endif
  return gd->getMaterials();
}

const Material *getMaterial(const CMicrostructure *ms, const std::string &name) 
{
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg->globalData(ms));
  return gd->getMaterial(name);
}

vtkSmartPointer<vtkLookupTable> getMaterialColorLookupTable(
					    const CMicrostructure *ms, 
					    const CColor *noColor, 
					    const CColor *noMaterial) 
{
  MaterialAttributeGlobalData *gd =
    dynamic_cast<MaterialAttributeGlobalData*>(reg-> globalData(ms));
#ifdef DEBUG
  assert(gd!=0);
#endif
  return gd->getMaterialColorLookupTable(*noColor, *noMaterial);
}


