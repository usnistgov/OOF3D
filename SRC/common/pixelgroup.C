// -*- C++ -*-
// $RCSfile: pixelgroup.C,v $
// $Revision: 1.41.18.23 $
// $Author: langer $
// $Date: 2014/09/12 19:56:22 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <assert.h>

#include "common/IO/bitoverlay.h"
#include "common/activearea.h"
#include "common/array.h"
#include "common/cmicrostructure.h"
#include "common/pixelattribute.h"
#include "common/pixelgroup.h"
#include "common/cpixelselection.h"
#include "common/switchboard.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "common/IO/oofcerr.h"
#include <algorithm>	

// While it appears that sets may be more convenient than vectors for
// pixel sets, the cost of inserting makes them less efficient.

//----------- 

const std::string
PixelGroupAttributeRegistration::classname_("PixelGroupAttributeRegistration");
const std::string
PixelGroupAttributeRegistration::modulename_("ooflib.SWIG.common.pixelgroup");
const std::string GroupList::displayname_("Groups");


static PixelGroupAttributeRegistration *reg = 0;

PixelGroupAttributeRegistration::PixelGroupAttributeRegistration()
  : PxlAttributeRegistration("PixelGroups")
{
#ifdef DEBUG
  assert( reg==0 );
#endif

  reg = this;
}

// -----------

int PixelSet::ngroups(0);

PixelSet::PixelSet(const ICoord *geometry, CMicrostructure *microstructure)
  : id_(ngroups++),
    weeded(false),
    geometry(*geometry),
    microstructure(microstructure)
{
}
  
PixelGroup::PixelGroup(const std::string &name, const ICoord *geometry,
		       CMicrostructure *microstructure)
  : PixelSet(geometry, microstructure),
    SubAttribute(name),
    meshable_(true)
{
}

PixelSet::PixelSet(const PixelSet &other)
  : id_(ngroups++),
    weeded(false),
    geometry(other.geometry),
    microstructure(other.microstructure)
{
  addWithoutCheck(other.members());
}

PixelGroup::PixelGroup(const std::string &name, const PixelGroup &other)
  : PixelSet(other),
    SubAttribute(name),
    meshable_(other.meshable_)
{
}

PixelSet::~PixelSet() {}

PixelGroup::~PixelGroup() {}

void PixelSet::resize(const ICoord *newgeom) {
  member_lock.acquire();
  if(geometry != *newgeom) {
    geometry = *newgeom;
    // Remove all pixels that don't fit in the new geometry.
    weed();
    int n = len();
    int j = 0;
    for(int i=0; i<n; i++) {	// loop over old set of pixels
      ICoord pxl = members_[i];
      if(pxl[0] < geometry[0] && pxl[1] < geometry[1]
#if DIM == 3
	 && pxl[2] < geometry[2]
#endif // DIM == 3
	 ) 
	{ // accept this pixel
	  if(j < i)
	    members_[j] = members_[i];
	  j++;
	}
    }
    members_.resize(j);
  }
  member_lock.release();
}

void PixelSet::add(CPixelSelection *sel) {
  add(sel->members());
}

void PixelSet::add(PixelSet *set) {
  add(set->members());
}

void PixelSet::addWithoutCheck(CPixelSelection *sel) {
  addWithoutCheck(sel->members());
}

void PixelSet::addWithoutCheck(PixelSet *set) {
  addWithoutCheck(set->members());
}

void PixelSet::add(const ICoordVector *pixels) {
  member_lock.acquire();
  members_.reserve(members_.size() + pixels->size());
  const ActiveArea *aa = microstructure->getActiveArea();
  for(ICoordVector::const_iterator i=pixels->begin(); i!=pixels->end(); i++) {
    if(aa->isActive(&*i)) 
      members_.push_back(*i);
  }
  member_lock.release();
}

void PixelSet::addWithoutCheck(const ICoordVector *pxls) {
  members_.insert(members_.end(), pxls->begin(), pxls->end());
}

void PixelGroup::add(const ICoordVector *pixels) {
  // TODO OPT: should this use the override flag too?
  if(microstructure->getActiveArea()->len() == 0)
    PixelSet::addWithoutCheck(pixels);
  else
    PixelSet::add(pixels);
  AttributeVectorMap avm;
  buildAttributeChangeMap(avm, &GroupList::add, this, reg, microstructure);
  for(ICoordVector::const_iterator i=pixels->begin(); i!=pixels->end(); ++i)
    microstructure->updateAttributeVector(*i, avm);
  microstructure->recategorize();
}

void PixelGroup::addWithoutCheck(const ICoordVector *pixels) {
  PixelSet::addWithoutCheck(pixels);
  AttributeVectorMap avm;
  buildAttributeChangeMap(avm, &GroupList::add, this, reg, microstructure);
  for(ICoordVector::const_iterator i=pixels->begin(); i!=pixels->end(); ++i) 
      microstructure->updateAttributeVector(*i, avm);
  microstructure->recategorize();
}

void PixelSet::add(const ICoord &pixel) {
  if(microstructure->getActiveArea()->isActive(&pixel)) {
    member_lock.acquire();
    members_.push_back(pixel);
    weeded = false;
    member_lock.release();
  }
}

void PixelGroup::add(const ICoord &pixel) {
  PixelSet::add(pixel);
  AttributeVectorMap avm;
  AttributeVectorSet avs;
  PixelAttributeVector *old_pav = microstructure->getAttributeVector(pixel);
  GroupList *old_list = dynamic_cast<GroupList*>((*old_pav)[reg->index()]);
  GroupList *list = new GroupList(*old_list);
  list->add(this);
  PixelAttribute *proper = reg->globalData(microstructure)->sync(list);
  PixelAttributeVector *pav = new PixelAttributeVector(*old_pav);
  (*pav)[reg->index()] = proper;
  microstructure->getMSAttributes().attributeChangeMapEntry(old_pav, pav, avm,
							    avs);
  microstructure->getMSAttributes().addAttributes(avs);
  microstructure->updateAttributeVector(pixel, avm);
  microstructure->recategorize();
}

void PixelSet::getBounds(ICoord &min, ICoord &max) const {
  int min0 = INT_MAX;
  int min1 = INT_MAX;
  int min2 = INT_MAX;
  int max0 = INT_MIN;
  int max1 = INT_MIN;
  int max2 = INT_MIN;
  for(ICoordVector::const_iterator i=members_.begin(); i!=members_.end(); ++i) {
    const ICoord &pxl = *i;
    if(pxl[0] < min0) min0 = pxl[0];
    if(pxl[1] < min1) min1 = pxl[1];
    if(pxl[2] < min2) min2 = pxl[2];
    if(pxl[0] > max0) max0 = pxl[0];
    if(pxl[1] > max1) max1 = pxl[1];
    if(pxl[2] > max2) max2 = pxl[2];
  }
  min = ICoord(min0, min1, min2);
  max = ICoord(max0, max1, max2);
}

void PixelSet::remove(CPixelSelection *sel) {
  remove(sel->members());
}

void PixelSet::remove(PixelSet *set) {
  remove(set->members());
}

void PixelSet::removeWithoutCheck(CPixelSelection *sel) {
  removeWithoutCheck(sel->members());
}

void PixelSet::removeWithoutCheck(PixelSet *set) {
  removeWithoutCheck(set->members());
}

void PixelSet::remove(const ICoordVector *pixels) {
   
  const ActiveArea *aa = microstructure->getActiveArea();

  ICoordVector rejects(*pixels);	// copy, so we can sort
  weed();			// sort and weed the group
  std::sort(rejects.begin(), rejects.end()); // sort pixels to be rejected
  unsigned int g = 0;			// next group member to consider
  unsigned int r = 0;			// next reject to consider
  unsigned int newsize = 0;

  while(g < members_.size() && r < rejects.size()) {
    if(r < rejects.size()-1 && rejects[r]==rejects[r+1]) {
      r++;			// skip duplications in reject list
    }
    else if(members_[g] == rejects[r] && aa->isActive(&rejects[r])) {
      g++;			// skip rejects in member list
    }
    else if(members_[g] < rejects[r]) {
      // retain nonrejected members
      if(g > newsize)
	members_[newsize] = members_[g];
      g++;
      newsize++;
    }
    else {
      // go on to next reject
      r++;
    }
  }
  // Include all remaining group members left after we've examined all
  // the rejects.
  while(g < members_.size()) {
    members_[newsize++] = members_[g++];
  }
  members_.resize(newsize);
}

void PixelSet::removeWithoutCheck(const ICoordVector *pixels) {

  ICoordVector rejects(*pixels);	// copy, so we can sort
  member_lock.acquire();

  weed();			// sort and weed the group
  std::sort(rejects.begin(), rejects.end()); // sort pixels to be rejected
  unsigned int g = 0;			// next group member to consider
  unsigned int r = 0;			// next reject to consider
  unsigned int newsize = 0;

  while(g < members_.size() && r < rejects.size()) {
    if(r < rejects.size()-1 && rejects[r]==rejects[r+1]) {
      r++;			// skip duplications in reject list
    }
    else if(members_[g] == rejects[r]) {
      g++;			// skip rejects in member list
    }
    else if(members_[g] < rejects[r]) {
      // retain nonrejected members
      if(g > newsize)
	members_[newsize] = members_[g];
      g++;
      newsize++;
    }
    else {
      // go on to next reject
      r++;
    }
  }
  // Include all remaining group members left after we've examined all
  // the rejects.
  while(g < members_.size()) {
    members_[newsize++] = members_[g++];
  }
  members_.resize(newsize);
  member_lock.release();
}

void PixelGroup::remove(const ICoordVector *pixels) {
  const ActiveArea *aa = microstructure->getActiveArea();
  if(aa->len() == 0 || aa->getOverride())
    PixelSet::removeWithoutCheck(pixels);
  else
    PixelSet::remove(pixels);
  AttributeVectorMap avm;
  buildAttributeChangeMap(avm, &GroupList::add, this, reg, microstructure);
  for(ICoordVector::const_iterator i=pixels->begin(); i!=pixels->end(); ++i) {
    microstructure->updateAttributeVector(*i, avm);
  }
  microstructure->recategorize();
}

// ICoord PixelSet::pop() {
//   member_lock.acquire();
//   weed();
//   ICoord pxl = members_[members_.size()-1];
//   members_.pop_back();
//   member_lock.release();
//   return pxl;
// }

void PixelSet::clear() {
  member_lock.acquire();
  members_.clear();
  weeded = true;
  member_lock.release();
}

void PixelGroup::clear() {
  // Update grouplists in microstructure
  member_lock.acquire();
  AttributeVectorMap avm;
  buildAttributeChangeMap(avm, &GroupList::remove, this, reg, microstructure);
  for(ICoordVector::const_iterator i=members_.begin(); i!=members_.end(); ++i) {
    microstructure->updateAttributeVector(*i, avm);
  }
  member_lock.release();
  microstructure->recategorize();
  PixelSet::clear();
}

bool PixelGroup::pixelInGroup(const ICoord *where) {
  GroupList *gl = 
    dynamic_cast<GroupList*>(microstructure->getAttribute(*where,
							  reg->index()));
  return gl->contains(this);
}


void PixelSet::setFromBitmap(const BitmapOverlay &bitmap) {
  // This is used to synchronize the Bitmap and the PixelSet that
  // are stored in a CPixelSelection.  It does *not* check the active
  // area, because it's assumed that the Bitmap is already set
  // correctly.
  const ICoord &bitmapsize = bitmap.sizeInPixels();
  int xmin = bitmapsize[0] < geometry[0] ? bitmapsize[0] : geometry[0];
  int ymin = bitmapsize[1] < geometry[1] ? bitmapsize[1] : geometry[1];
#if DIM == 2
  const Array<bool> sub(bitmap.data.subarray(ICoord(0,0), ICoord(xmin, ymin)));
#elif DIM == 3
  int zmin = bitmapsize[2] < geometry[2] ? bitmapsize[2] : geometry[2];
  const Array<bool> sub(bitmap.data.subarray(ICoord(0,0,0), ICoord(xmin, ymin, zmin)));
#endif
  member_lock.acquire();
  for(Array<bool>::const_iterator i=sub.begin(); i!=sub.end(); ++i)
    if(*i)
      members_.push_back(i.coord());
  weeded = false;
  member_lock.release();
}


int PixelSet::len() const {
  member_lock.acquire();
  weed();
  int res = members_.size();
  member_lock.release();
  return res;
}

bool PixelSet::empty() const {
  member_lock.acquire();
  weed();
  bool mt = members_.empty();
  member_lock.release();
  return mt;
}

// Should be called with the member_lock acquired.
void PixelSet::weed() const {
  if(weeded) return;
  if(!members_.empty()) {
    std::sort(members_.begin(), members_.end());
    ICoordVector::iterator newend = std::unique(members_.begin(),
						       members_.end());
    members_.erase(newend, members_.end());
   }
  weeded = true;
}



const ICoordVector *PixelSet::members() const {
  weed();
  return &members_;
}

void PixelGroup::set_meshable(bool deshabille) {
  meshable_ = deshabille;
}

void PixelGroup::print(std::ostream &os) const {
  os << "PixelGroup(" << name();
  if(is_meshable())
    os << ", meshable";
  os << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The CMicrostructure keeps an array of GroupList objects, indicating
// to which groups each pixel belongs.  GroupList is a subclass of
// PixelAttribute, and as such is used to categorize pixels.

bool GroupList::operator<(const PixelAttribute &other) const {
  // Compare two lists of groups, skipping groups that aren't meshable.

  const GroupList &otherlist = dynamic_cast<const GroupList&>(other);
  const std::set<SubAttribute*> &grps = members();
  const std::set<SubAttribute*> &othergrps = otherlist.members();

  std::set<SubAttribute*>::const_iterator i= grps.begin();
  std::set<SubAttribute*>::const_iterator j = othergrps.begin();
  while(true) {
    while(i != grps.end() && !(*i)->is_meshable())
      ++i;
    while(j != othergrps.end() && !(*j)->is_meshable())
      ++j;
    if(i == grps.end()) {
      if(j != othergrps.end()) {
	return true; // grps contains fewer meshable groups than othergrps
      }
      else {
	return false; 		// grouplists are identical.
      }
    }
    if(j == othergrps.end()) {
      return false; // grps contains more meshable groups than othergrps
    }

    if(*i < *j) {
      return true;
    }
    if(*j < *i) {
      return false;
    }
    // grouplists are identical so far
    ++i;
    ++j;
  }
  throw ErrProgrammingError("Impossible condition in GroupList::operator<",
			    __FILE__, __LINE__);
}




PixelAttribute *PixelGroupAttributeRegistration::createAttribute(const CMicrostructure *MS) const {
  GroupList *gl = new GroupList();
  addToGlobalData(MS, gl);
  return gl;
}

PixelAttributeGlobalData *
PixelGroupAttributeRegistration::createAttributeGlobalData(const
							   CMicrostructure *ms)
  const
{
  return new GroupListGlobalData();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// std::vector<std::string> *pixelGroupNames(const CMicrostructure *microstructure,
// 					  const ICoord *where)
// {
//   return ListAttribute::names(microstructure, where, reg);
// }

std::vector<std::string> *pixelGroupNames(const CMicrostructure *microstructure,
					  int cat)
{
  // ListAttribute::names is a static method and returns a new'd
  // std::vector of std::strings.
  return ListAttribute::names(microstructure, cat, reg);
}

// Does the given group contain the given pixel?
bool pixelGroupQueryPixel(const CMicrostructure &microstructure,
			  const ICoord &where, const PixelGroup *group)
{
  GroupList *list =
    dynamic_cast<GroupList*>(microstructure.getAttribute(where, reg->index()));
  return list->contains(group);
}

// Does the given category contain pixels in the given group?
bool pixelGroupQueryCategory(const CMicrostructure &microstructure,
			     int cat, const PixelGroup *group)
{
  ListAttribute *list =
    dynamic_cast<ListAttribute*>(microstructure.getAttributeFromCategory(
							 cat, reg->index()));
  return list->contains(group);
}
