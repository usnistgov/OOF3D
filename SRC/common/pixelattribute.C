// -*- C++ -*-
// $RCSfile: pixelattribute.C,v $
// $Revision: 1.8.18.14 $
// $Author: langer $
// $Date: 2014/09/12 19:56:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/pixelattribute.h"
#include "common/cmicrostructure.h"

std::vector<PxlAttributeRegistration*> &
PxlAttributeRegistration::registrations() { // static & private
  static std::vector<PxlAttributeRegistration*> vec;
  return vec;
}

PxlAttributeRegistration::PxlAttributeRegistration(const std::string &name)
  : name_(name)
{
  index_ = nRegistrations();
  registrations().push_back(this);
}

PixelAttributeGlobalData *PxlAttributeRegistration::createAttributeGlobalData(
						      const CMicrostructure*)
  const 
{
  return new PixelAttributeGlobalData(); 
}

PixelAttributeGlobalData *
PxlAttributeRegistration::globalData(const CMicrostructure *ms) const {
  return ms->getAttributeGlobalData(index_);
}

void PxlAttributeRegistration::addToGlobalData(const CMicrostructure *MS,
					       PixelAttribute *pa) 
    const 
{
  globalData(MS)->sync(pa); 
}

int nAttributes() {
  return PxlAttributeRegistration::nRegistrations();
}

const PxlAttributeRegistration *getRegistration(int i) {
  return PxlAttributeRegistration::getRegistration(i);
}

const PxlAttributeRegistration *PxlAttributeRegistration::getRegistration(int i)
{				// static
  return registrations()[i];
}
						   

std::ostream &operator<<(std::ostream &os, const PixelAttribute &pa) {
  pa.print(os);
  return os;
}

PixelAttributeGlobalData::~PixelAttributeGlobalData() {
  for(AttributeSet::iterator it=attributeValues.begin();
      it!=attributeValues.end(); ++it)
    delete *it;
}


// If the attribute is already in the global data, return that pointer
// and delete this one. If not, add this to the global data. This is 
// required so that there is ONE copy of each attribute.
PixelAttribute *PixelAttributeGlobalData::sync(PixelAttribute *pa) {
  AttributeSet::iterator it = attributeValues.find(pa);
  if(it == attributeValues.end()) {
    attributeValues.insert(pa);
    return pa;
  }
  else {
    delete pa;
    return *it;
  }
}

// The PixelAttribute::operator< only compares "meshable"
// attributes. More details are in the opening comments of
// pixelattribute.h
bool PixelAttributeVector::ltAttributes(const PixelAttributeVector *pavec0,
					const PixelAttributeVector *pavec1)
{
  int n0 = pavec0->size();
  int n1 = pavec1->size();
  int n = n0;
  if(n1 < n0)
    n = n1;
  for(int i=0; i<n; i++) {
    if(*(*pavec0)[i] < *(*pavec1)[i])
      return true;
    if(*(*pavec1)[i] < *(*pavec0)[i])
      return false;
  }
  return n0 < n1;
}

// PixelAttribute::strictLessThan compares all attributes to
// distinguish completely unique attributes.
bool PixelAttributeVector::strictLTAttributes(
				      const PixelAttributeVector *pavec0,
				      const PixelAttributeVector *pavec1)
{
  int n0 = pavec0->size();
  int n1 = pavec1->size();
  int n = n0;
  if(n1 < n0) 
    n = n1;
  for(int i=0; i<n; i++) {
    if((*pavec0)[i]->strictLessThan(*(*pavec1)[i]))
      return true;
    if((*pavec1)[i]->strictLessThan(*(*pavec0)[i]))
      return false;
  }
  return n0 < n1;
}

// pointerLTAttributes compares only the pointer addresses for speed.
bool PixelAttributeVector::pointerLTAttributes(
				       const PixelAttributeVector *pavec0,
				       const PixelAttributeVector *pavec1)
{
  return pavec0 < pavec1;
}

bool PixelAttributeVector::isMapTrivial(const AttributeVectorMap &avm) {
  for(AttributeVectorMap::const_iterator it=avm.begin(); it!=avm.end(); ++it) {
    if((*it).first != (*it).second)
      return false;
  }
  return true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const PixelAttributeVector &pav) {
  os << "[";
  if(pav.size() > 0)
    for(unsigned int i=0; i<pav.size(); i++) {
      if(i > 0)
	os << ", ";
      pav[i]->print(os);
    }
  os << "]";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void ListAttribute::add(SubAttribute *att) {
  data.insert(att);
}

void ListAttribute::remove(SubAttribute *att) {
  std::set<SubAttribute*>::iterator i = data.find(att);
  if(i != data.end())
    data.erase(i);
}

void ListAttribute::remove(const std::string &name) {
  for(std::set<SubAttribute*>::iterator i=data.begin(); i!=data.end(); ++i) {
    if((*i)->name() == name) {
      data.erase(i);
      return;
    }
  }
}

bool ListAttribute::contains(const SubAttribute *att) const {
  std::set<SubAttribute*>::const_iterator i = 
    data.find(const_cast<SubAttribute*>(att));
  return i != data.end();
}

const std::set<SubAttribute*> &ListAttribute::members() const {
  return data;
}

bool ListAttribute::strictLessThan(const PixelAttribute &other) const {
  const ListAttribute &otherlist = dynamic_cast<const ListAttribute&>(other);
  const std::set<SubAttribute*> &att = members();
  const std::set<SubAttribute*> &otheratt = otherlist.members();
  //return att < otheratt;
  std::set<SubAttribute*>::const_iterator i = att.begin();
  std::set<SubAttribute*>::const_iterator j = otheratt.begin();
  for( ; i != att.end() && j != otheratt.end(); ++i, ++j) {
    if((*i)->strictLessThan(**j))
      return true;
    else if((*j)->strictLessThan(**i))
      return false;
  }
  if(i == att.end() && j != otheratt.end())
    return true;
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given a ListAttribute method "manip" and a SubAttribute for it to
// operate on, along with the registration for the attribute, add or
// update entries of the given AttributeVectorMap showing how old
// AttributeVectors change to new AttributeVectors when the operator
// is applied.  Also, update the given Microstructure's list of
// AttributeVectors.

// buildAttributeChangeMap is called by PixelGroup::add and related
// methods, before calling CMicrostructure::updateAttributeVector for
// the affected pixels.  buildAttributeChangeMap will create new
// AttributeVectors that might never be used in the Microstructure,
// but that's ok.  AttributeVectors that aren't used are eliminated
// when MicrostructureAttributes::prune is called.

void buildAttributeChangeMap(AttributeVectorMap &avm,
			     ManipulateListAttribute manip, 
			     SubAttribute *sub,
			     PxlAttributeRegistration *reg, 
			     CMicrostructure *microstructure)
{
  // Create a new AttributeVectorSet that will use all attributes,
  // even non-meshable ones, to distinguish the vectors from one
  // another.
  AttributeVectorSet new_avs(PixelAttributeVector::strictLTAttributes);  
  // Loop over existing AttributeVectors in the Microstructure.
  MicrostructureAttributes &msAttributes = microstructure->getMSAttributes();
  for(AttributeVectorSet::iterator oldAV=msAttributes.begin(); 
      oldAV!=msAttributes.end(); ++oldAV)
    {
      // "reg" is the PxlAttributeRegistration of a ListAttribute.
      // Get the attribute.
      ListAttribute* old_list = 
	dynamic_cast<ListAttribute*>((**oldAV)[reg->index()]);
      // Copy it.
      ListAttribute* new_list = old_list->clone();
      // Modify the copy.
      (new_list->*manip)(sub);
      // The modified copy might be a duplicate of another
      // pre-existing attribute.  Get the original, if there is one,
      // and delete the new one.  If the new one isn't a duplicate,
      // sync() returns it.
      PixelAttribute *proper = reg->globalData(microstructure)->sync(new_list);
      // Create a new PixelAttributeVector that contains the modified copy.
      PixelAttributeVector *pav = new PixelAttributeVector(*(*oldAV));
      (*pav)[reg->index()] = proper;
      // Add an entry to the AttributeVectorMap avm that maps the old
      // AttributeVector to the new one. If the new one is truly new,
      // add it to new_avs as well.
      msAttributes.attributeChangeMapEntry(*oldAV, pav, avm, new_avs);
    }
  // Add the AttributeVectors in new_avs to
  // msAttributes::attributeVectorSet.
  msAttributes.addAttributes(new_avs);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void ListAttribute::print(std::ostream &os) const {
  const std::set<SubAttribute*> &subatts = members();
  if(!subatts.empty()) {
    os << displayname() << "(";
    for(std::set<SubAttribute*>::iterator i = subatts.begin(); i!=subatts.end();
	i++)
      {
	if(i != subatts.begin()) os << ", ";
	os << (*i)->name();
      }
    os << ")";
  }
  else
    os << "[No " << displayname() << "]";
}

std::vector<std::string> *ListAttribute::names() {
  std::vector<std::string> *roster = new std::vector<std::string>;
  roster->reserve(data.size());
  for(std::set<SubAttribute*>::iterator i = data.begin(); i!=data.end(); i++)
    roster->push_back((*i)->name());
  return roster;

}

// static
std::vector<std::string> *ListAttribute::names(
				       const CMicrostructure *microstructure,
				       int cat, PxlAttributeRegistration *reg)
{
  ListAttribute *list = 
    dynamic_cast<ListAttribute*>(microstructure->getAttributeFromCategory(
							  cat, reg->index()));
  return list->names();
}

void SubAttribute::print(std::ostream &os) const {
  os << name() << std::endl;
}

std::ostream &operator<<(std::ostream &os, const SubAttribute &attr) {
  attr.print(os);
  return os;
}
