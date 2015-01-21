// -*- C++ -*-
// $RCSfile: cmicrostructure.C,v $
// $Revision: 1.83.2.54 $
// $Author: langer $
// $Date: 2014/12/12 19:38:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <algorithm>
#include <assert.h>
#include <iomanip>
#include <map>
#include <math.h>		// for sqrt()
#include <stdlib.h>		// for abs()
#include <vector>

#include "common/IO/oofcerr.h"
#include "common/activearea.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/cpixelselection.h"
#include "common/geometry.h"
#include "common/lock.h"
#include "common/pixelattribute.h"
#include "common/pixelgroup.h"
#include "common/pixelsetboundary.h"
#include "common/printvec.h"

#include <iostream>

// TODO OPT: Many locks in this file are commented out.  Why?  Should they
// be removed, or reinstated?

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

long CMicrostructure::globalMicrostructureCount = 0; // used for code testing
static SLock globalMicrostructureCountLock;

long get_globalMicrostructureCount() {
  return CMicrostructure::globalMicrostructureCount;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// attributeVectorSet uses strictLTAttributes to determine strict
// uniqueness and deterministic order (including attributes that are
// not "meshable" such as ActiveVolume (Area). attrVecToCategoryMap
// uses the pointerLTAttributes for speed.

MicrostructureAttributes::MicrostructureAttributes(const CMicrostructure *ms) 
  : MS(ms),
    attributeGlobalData(nAttributes()),
    attributeVectorSet(PixelAttributeVector::strictLTAttributes),
    attrVecToCategoryMap(PixelAttributeVector::pointerLTAttributes) 
{
  PixelAttributeVector *emptyAttributeVector = new PixelAttributeVector;
  for(std::vector<PixelAttributeGlobalData*>::size_type i=0;
      i<attributeGlobalData.size(); ++i)
    {
      const PxlAttributeRegistration *pareg =
	PxlAttributeRegistration::getRegistration(i);
      attributeGlobalData[i] = pareg->createAttributeGlobalData(MS);
      emptyAttributeVector->push_back(pareg->createAttribute(MS));
      if(pareg->name() == "PixelGroups")
	pixelgroup_index = i;
    }
  attributeVectorSet.insert(emptyAttributeVector);
}

MicrostructureAttributes::~MicrostructureAttributes() {
  for(std::vector<PixelAttributeGlobalData*>::size_type i=0;
      i<attributeGlobalData.size(); ++i) 
    {
      delete attributeGlobalData[i];
    }
  for(AttributeVectorSet::iterator it=attributeVectorSet.begin();
      it!=attributeVectorSet.end(); ++it)
    {
      delete *it;
    }
}


void MicrostructureAttributes::prune() const {
  // SAFER pruning. Create a temporary copy of the attributeVectorSet,
  // and rebuild the class member with only attributes that have a
  // non-zero number of voxels.
  AttributeVectorSet temp(PixelAttributeVector::strictLTAttributes);
  temp.insert(attributeVectorSet.begin(), attributeVectorSet.end());
  attributeVectorSet.clear();
  for(AttributeVectorSet::iterator i = temp.begin(); 
      i!= temp.end(); ++i) {
    if((*i)->getNumberOfVoxels() != 0)
      attributeVectorSet.insert(*i);
  }
}

// Populate the attrVecToCategoryMap by looping over the
// PixelAttributeVectors in attributeVectorSet and assigning an
// integer category to each PAV.  PAVs that differ only in
// non-meshable attributes will have the same category number, but
// will have their own entries in attrVecToCategoryMap.  This allows
// faster lookup later.

void MicrostructureAttributes::categorize() {
  // Remove AttributeVectors that aren't used, but might have been
  // created by buildAttributeChangeMap.
  prune();
  // Create a temporary AttributeVectorCategoryMap using
  // PixelAttributeVector::ltAttributes, which is expensive, for
  // finding the categories.  Attribute vectors that are strictly
  // unique but the same for meshable attributes will only have one
  // representative entry in temp. However, in the
  // attrVecToCategoryMap object, we need distinct entries in order to
  // use the pointer comparison, which is faster.
  AttributeVectorCategoryMap temp(PixelAttributeVector::ltAttributes);
  attrVecToCategoryMap.clear();
  attrVecVec.clear();
  ncategories_ = 0;
  
  // // Copy the set to a temporary vector and sort it with
  // // strictLTAttributes so that the category numbers are assigned in a
  // // reproducible way. This is helpful for debugging.
  // std::vector<PixelAttributeVector*> sortedAttributes;
  // sortedAttributes.insert(sortedAttributes.begin(),
  // 			  attributeVectorSet.begin(),
  // 			  attributeVectorSet.end());
  // std::sort(sortedAttributes.begin(), sortedAttributes.end(),
  // 	    PixelAttributeVector::strictLTAttributes);
  // for(std::vector<PixelAttributeVector*>::iterator i=sortedAttributes.begin();
  //      i != sortedAttributes.end(); ++i)

  for(AttributeVectorSet::iterator i=attributeVectorSet.begin(); 
      i!=attributeVectorSet.end(); ++i)
    {
      AttributeVectorCategoryMap::iterator pav = temp.find(*i);
      if(pav == temp.end()) {
	temp[*i] = ncategories_;
	attrVecToCategoryMap[*i] = ncategories_;
	attrVecVec.push_back(*i);
	++ncategories_;
      }
      else {
	attrVecToCategoryMap[*i] = (*pav).second;
      }
    }
}

void MicrostructureAttributes::categorizeRO(AttributeVectorCategoryMap &avcm) {
  prune();
  avcm.clear();
  AttributeVectorCategoryMap::iterator pav;
  for(AttributeVectorSet::iterator i = attributeVectorSet.begin();
      i != attributeVectorSet.end(); ++i) {
    pav = avcm.find(*i);
    if(pav == avcm.end()) {
      int cat = avcm.size();
      avcm[*i] = cat;
    }
  }
}


PixelAttribute *MicrostructureAttributes::getAttributeFromCategory(
					   unsigned int cat, int index)
  const
{
  if(cat < attrVecVec.size())
    return (*attrVecVec[cat])[index];
  throw ErrProgrammingError("Could not find attribute for category",
   			    __FILE__, __LINE__);
}


PixelAttributeGlobalData *
MicrostructureAttributes::getAttributeGlobalData(int attributeID) const {
  return attributeGlobalData[attributeID];
}

// Given an old PixelAttributeVector and a new one that will replace
// it, see if the new one is really new (ie, not already present in
// the Microstructure).  Update an AttributeVectorMap, which maps the
// old PAV to its replacement (which is either the given new PAV or a
// pre-existing equivalent).  If the new PAV is truly new, add it to
// new_avs as well, so that it can later be added to the
// Microstructure's list of PAVs.

// This has a structure similar to PixelAttributeGlobalData::sync, and
// could be called "sync" instead.  The difference is that
// PixelAttributeGlobalData::sync operates on PixelAttributes, but
// this operates on vectors of them.

void MicrostructureAttributes::attributeChangeMapEntry(
					       PixelAttributeVector *old_pav,
					       PixelAttributeVector *new_pav, 
					       AttributeVectorMap &avm,
					       AttributeVectorSet &new_avs) 
{
  // Look for new_pav in the old set of attribute vectors.
  AttributeVectorSet::iterator j = attributeVectorSet.find(new_pav);
  //oofcerr << "num new_avs " << new_avs.size() << std::endl;
  if(j == attributeVectorSet.end()) {
    // new_pav isn't in attributeVectorSet.  Is it in new_avs?
    AttributeVectorSet::iterator k = new_avs.find(new_pav);
    //oofcerr << "new_pav not in new_avs? " << (k==new_avs.end()) << std::endl;
    // if(k!=new_avs.end())
    //   oofcerr << "found new_pav in new_avs " << (*k) << std::endl;
    if(k==new_avs.end()) {
      // new_pav isn't in new_avs either.  Put it in new_avs and map
      // old_pav to new_pav.
      new_avs.insert(new_pav);
      avm[old_pav] = new_pav;
      // oofcerr << "new pav " << old_pav << " " << new_pav << " "
      // 	      << new_avs.size() << std::endl;
    }
    else {
      // new_pav is a duplicate of one already in new_avs.  Delete
      // new_pav, and change the map so that it points to the
      // pre-existing version.
      delete new_pav;
      avm[old_pav] = (*k);
    }
  }
  else {			// j != attributeVectorSet.end()
    // new_pav is a duplicate of one already in attributeVectorSet.
    // Delete it, and change avm so that it points to the pre-existing
    // version.
    delete new_pav;
    avm[old_pav] = (*j);
    // oofcerr << "fnd pav " << old_pav << " " << (*j) << std::endl;
  }
}

void MicrostructureAttributes::buildAttributeChangeMap(
				       PixelAttribute *pa, 
				       int index, AttributeVectorMap &avm) 
{
  AttributeVectorSet new_avs(PixelAttributeVector::strictLTAttributes);
  for(AttributeVectorSet::iterator i = attributeVectorSet.begin(); 
      i != attributeVectorSet.end(); ++i) 
    {
      PixelAttributeVector *pav = new PixelAttributeVector(*(*i));
      (*pav)[index] = pa;
      attributeChangeMapEntry(*i, pav, avm, new_avs);
    }
  attributeVectorSet.insert(new_avs.begin(), new_avs.end());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CMicrostructure::CMicrostructure(const std::string &name,
				 const ICoord *isz, const Coord *sz) 
  : pxlsize_(*isz),
    size_(*sz),
    attributeVectors(*isz, (PixelAttributeVector*)0),
    attributes(this),
    categorymap(*isz, 0),
    categorized(false),
    ncategories(0),
    name_(name)
{
  globalMicrostructureCountLock.acquire();
  ++globalMicrostructureCount;
  globalMicrostructureCountLock.release();
#if DIM == 2
  delta_ = Coord((*sz)[0]/(*isz)[0], (*sz)[1]/(*isz)[1]);
#elif DIM == 3
  delta_ = Coord((*sz)[0]/(*isz)[0], (*sz)[1]/(*isz)[1], (*sz)[2]/(*isz)[2]);
#endif

  // At this point, the attributes main storage object will only have
  // one entry, which is an empty PixelAttributeVector
  PixelAttributeVector *empty = *(attributes.begin());
  for(Array<PixelAttributeVector*>::iterator j=attributeVectors.begin();
      j!=attributeVectors.end(); ++j) 
    {
      attributeVectors[j] = empty;
      empty->incrementVoxelCount();
    }
}

CMicrostructure::~CMicrostructure() {
  destroy();
  globalMicrostructureCountLock.acquire();
  --globalMicrostructureCount;
  globalMicrostructureCountLock.release();
}


// This routine, and the constructor, could lock the
// groups_attributes_lock for writing, but it's probably not required.
void CMicrostructure::destroy() {
  for(std::list<PixelGroup*>::iterator i=pixelgroups.begin();
      i!=pixelgroups.end(); i++) 
    {
      delete *i;
    }
  pixelgroups.resize(0);
}

PixelAttributeGlobalData *CMicrostructure::getAttributeGlobalData(int which)
  const 
{
  return attributes.getAttributeGlobalData(which);
}


// Replace the AttributeVector* at position "where" with the one that
// it's mapped to via the given AttributeVectorMap, and adjust the
// voxel counts in the old and new AttributeVectors.

void CMicrostructure::updateAttributeVector(const ICoord &where,
					    AttributeVectorMap &avm) const
{
  PixelAttributeVector *old_vec = attributeVectors[where];
  PixelAttributeVector *new_vec = avm[old_vec];
  attributeVectors[where] = new_vec;
  if(!old_vec || !new_vec) 
    throw ErrProgrammingError("CMicrostructure: Null Attribute Vector",
			      __FILE__, __LINE__);
  old_vec->decrementVoxelCount();
  new_vec->incrementVoxelCount();
}


PixelAttribute *CMicrostructure::getAttribute(const ICoord &where, int index)
  const
{ 
  return (*attributeVectors[where])[index]; 
}

TimeStamp &CMicrostructure::getTimeStamp() {
  return timestamp;
}

const TimeStamp &CMicrostructure::getTimeStamp() const {
  return timestamp;
}

int CMicrostructure::nGroups() const {
  // groups_attributes_lock.read_acquire();
  int res = pixelgroups.size();
  // groups_attributes_lock.read_release();
  return res;
}

// Convert a Coord in the physical space to pixel coordinates (without
// rounding to the nearest integer).
Coord CMicrostructure::physical2Pixel(const Coord &pt) const {
#if DIM == 2
  return Coord(pt[0]/delta_[0], pt[1]/delta_[1]);
#elif DIM == 3
  return Coord(pt[0]/delta_[0], pt[1]/delta_[1], pt[2]/delta_[2]);
#endif
}

// Return the physical space coordinates of the lower-left corner of a
// pixel.
Coord CMicrostructure::pixel2Physical(const ICoord &pxl) const {
#if DIM == 2
  return Coord(pxl[0]*delta_[0], pxl[1]*delta_[1]);
#elif DIM == 3
  return Coord(pxl[0]*delta_[0], pxl[1]*delta_[1], pxl[2]*delta_[2]);
#endif
}

// Return the physical space coordinates of a given non-integer
// coordinate in pixel space.
Coord CMicrostructure::pixel2Physical(const Coord &pt) const {
#if DIM == 2
  return Coord(pt[0]*delta_[0], pt[1]*delta_[1]);
#elif DIM == 3
  return Coord(pt[0]*delta_[0], pt[1]*delta_[1], pt[2]*delta_[2]);
#endif
}

// Return the coordinates of the pixel that contains the given point.
ICoord CMicrostructure::pixelFromPoint(const Coord &pt) const {
  Coord p = physical2Pixel(pt);
  int xx = (int) floor(p[0]);
  int yy = (int) floor(p[1]);
  if(xx >= pxlsize_[0])
    --xx;
  if(yy >= pxlsize_[1])
    --yy;
#if DIM == 2
  return ICoord(xx, yy);
#elif DIM == 3
  int zz = (int) floor(p[2]);
  if(zz >= pxlsize_[2])
    --zz;
  return ICoord(xx, yy, zz);
#endif
}

bool CMicrostructure::contains(const ICoord &ip) const {
#if DIM==2
  return ((ip[0]>=0 && ip[0]<pxlsize_[0]) && (ip[1]>=0 && ip[1]<pxlsize_[1]));
#elif DIM==3
  return ((ip[0]>=0 && ip[0]<pxlsize_[0]) && (ip[1]>=0 && ip[1]<pxlsize_[1])
	  && (ip[2]>=0 && ip[2]<pxlsize_[2]));
#endif	// DIM==3
}

bool CMicrostructure::isSelected(const ICoord *x) const {
  return pixelSelection->isSelected(x); 
}

PixelGroup *CMicrostructure::findGroup(const std::string &name) const {
  // Get an existing group.  Don't create one if it doesn't already exist.
  // groups_attributes_lock.read_acquire();
  PixelGroup *res = 0;
  for(std::list<PixelGroup*>::const_iterator i=pixelgroups.begin();
      i!=pixelgroups.end(); i++) 
    {
      if((*i)->name() == name) {
	res = (*i);
	break;
      }
    }
  // groups_attributes_lock.read_release();
  return res;
}


PixelGroup *CMicrostructure::getGroup(const std::string &name,
				      bool *newness)
{
  // Get an existing group, or create one if necessary.  Set the "newness"
  // pointer according to whether or not a new group is created.
  *newness = false;
  // findGroup independently handles the groups_attributes_lock.
  PixelGroup *grp = findGroup(name);
  if(grp) 
    return grp;
  // groups_attributes_lock.write_acquire();
  PixelGroup *newgrp = new PixelGroup(name, &pxlsize_, this);
  pixelgroups.push_back(newgrp);
  ++timestamp;
  *newness = true;
  // groups_attributes_lock.write_release();
  return newgrp;
}

void CMicrostructure::removeGroup(const std::string &name) {
  // category_lock.acquire();
  // groups_attributes_lock.read_acquire();
  //attributes.removeGroup(name);
  PixelGroup *g = findGroup(name);
  g->clear();
  pixelgroups.remove(g);
  // groups_attributes_lock.read_release();
  // category_lock.release();
}

std::vector<std::string> *CMicrostructure::groupNames() const {
  std::vector<std::string> *roster = new std::vector<std::string>;
  // groups_attributes_lock.read_acquire();
  for(std::list<PixelGroup*>::const_iterator i=pixelgroups.begin(); 
      i!=pixelgroups.end(); i++) 
    {
      roster->push_back((*i)->name());
    }
  // groups_attributes_lock.read_release();
  return roster;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool CMicrostructure::isActive(const Coord &point) const {
  return activearea->isActive(pixelFromPoint(point));
}

bool CMicrostructure::isActive(const ICoord &pxl) const {
  return activearea->isActive(pxl);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// This function should only be run with the category_lock acquired.
// It is the caller's responsibility to do this -- all callers are
// within the CMicrostructure class, because this function (and the
// lock) is private.
void CMicrostructure::categorize() const {

  // groups_attributes_lock.read_acquire();
  attributes.categorize();
  categoryBdys.clear();  // PixelSetBoundary has no default constructor.

#if DIM==3
  // the polydata we return is done in the pixel coordinate system so
  // that we can use some integer math in calculating the homogeneity
  ICoord dirs[3];
  dirs[0]=ICoord(-1,0,0);
  dirs[1]=ICoord(0,-1,0);
  dirs[2]=ICoord(0,0,-1);
#endif	// DIM==3
  ncategories = attributes.ncategories();
  for(int i=0; i < ncategories; ++i) {
#if DIM==2
    PixelSetBoundary psb(this);
    categoryBdys.push_back(psb);
#elif DIM==3
    VoxelSetBoundary vsb;
    // TODO OPT: VoxelSetBoundary objects are fairly large. Do we
    // really want to be copying them into categoryBdys?
    categoryBdys.push_back(vsb);
#endif	// DIM==3
  }

  // loop over pixels in the microstructure
  for(Array<int>::iterator i=categorymap.begin(); i!=categorymap.end(); ++i) {
    const ICoord &where = i.coord();
    // attributeVectors is an Array<PixelAttributeVector*>
    categorymap[i] = attributes.getCategory(attributeVectors[where]);

#if DIM==2
    categoryBdys[ (*cat).second ].add_pixel(where);
#elif DIM==3
    // Insert bottom, left, and back faces into polydata.
    for(int j=0; j<3; j++) {
      if(categorymap.contains(where+dirs[j])) {
	unsigned int vxlcat0 = categorymap[where];
	unsigned int vxlcat1 = categorymap[where+dirs[j]];
	if(vxlcat0 != vxlcat1) {
#ifdef DEBUG
	  assert(vxlcat0 < categoryBdys.size());
	  assert(vxlcat1 < categoryBdys.size());
#endif	// DEBUG
	  categoryBdys[ vxlcat0 ].add_face(where, j, -1);
	  categoryBdys[ vxlcat1 ].add_face(where, j, 1);
	} // end if vxlcat0 != vxlcat1
      } // end if(categorymap.contains....
    } // end loop over directions
#endif	// DIM==3
  }  // end loop over category map

  // Find the boundaries.
#if DIM==2
  for(std::vector<PixelSetBoundary>::iterator i = categoryBdys.begin();
      i!=categoryBdys.end(); ++i ) {
    (*i).find_boundary();
  }
#endif	// DIM==2

 categorized = true;
 // groups_attributes_lock.read_release();
} // end CMicrostructure::categorize

int CMicrostructure::nCategories() const {
  // oofcerr << "Acquire, nCategories." << std::endl;
  // category_lock.acquire();
  if(!categorized)
    categorize();
  int res = ncategories;
  // category_lock.release();
  // oofcerr << "Release." << std::endl;
  return res;
}

int CMicrostructure::category(const ICoord *where) const {
  // oofcerr << "Acquire, category1" << std::endl;
  // category_lock.acquire();
  if(!categorized)
    categorize();
  int cat = categorymap[*where];
  // category_lock.release();
  // oofcerr << "Release." << std::endl;
  return cat;
}

int CMicrostructure::category(const ICoord &where) const {
  // oofcerr << "Acquire, category2" << std::endl;
  // category_lock.acquire();
  if(!categorized)
    categorize();
  int res = categorymap[where];
  // category_lock.release();
  // oofcerr << "Release." << std::endl;
  return res;
}

// Special version for finding the category of the pixel under an
// arbitrary point.
int CMicrostructure::category(const Coord *where) const {
  // oofcerr << "Acquire, category3." << std::endl;
  // category_lock.acquire();
  if(!categorized) 
    categorize();
  int res = categorymap[pixelFromPoint(*where)];
  // category_lock.release();
  // oofcerr << "Release." << std::endl;
  return res;
}

// Special version for finding the category of the pixel under an
// arbitrary point.
int CMicrostructure::category(const Coord &where) const {
  // oofcerr << "Acquire, category3." << std::endl;
  // category_lock.acquire();
  if(!categorized) 
    categorize();
  int res = categorymap[pixelFromPoint(where)];
  // category_lock.release();
  // oofcerr << "Release." << std::endl;
  return res;
}

const Array<int> *CMicrostructure::getCategoryMap() const {
  // oofcerr << "Acquire, getCategoryMap." << std::endl;
  // category_lock.acquire();
  if(!categorized)
    categorize();
  // category_lock.release();
  // oofcerr << "Released, getCategoryMap." << std::endl;
  return &categorymap;
}

// getCategoryMapRO() is a combination of getCategoryMap() and
// categorize().  It doesn't compute category boundaries, and it is
// strictly const -- it doesn't even change any mutable data in the
// CMicrostructure.  It uses strictLessThan_Attributes instead of
// operator< when comparing PixelAttributes.  It's used when writing a
// Microstructure to a file.


const Array<int> *CMicrostructure::getCategoryMapRO() const {
  // groups_attributes_lock.read_acquire();
#if DIM == 2
  Array<int> *localmap = new Array<int>(pxlsize_[0], pxlsize_[1]);
#elif DIM == 3
  Array<int> *localmap = new Array<int>(pxlsize_[0], pxlsize_[1], pxlsize_[2]);
#endif
  AttributeVectorCategoryMap avcm(PixelAttributeVector::pointerLTAttributes);
  attributes.categorizeRO(avcm);

  for(Array<int>::iterator i=localmap->begin(); i!=localmap->end(); ++i) {
    const ICoord &where = i.coord();
    (*localmap)[where] = avcm[attributeVectors[where]];
   }
  // groups_attributes_lock.read_release();
  return localmap;
}

void CMicrostructure::recategorize() {
  // oofcerr << "Acquire, recategorize." << std::endl;
  // category_lock.acquire();
  attributes.prune();
  categorized = false;
  ++timestamp;
  // category_lock.release();
  // oofcerr << "Release." << std::endl;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Geometry routines for identifying pixels in the microstructure that
// are under segments and elements. 

bool swapEndPoints(const ICoord &ip0, const ICoord &ip1, const Coord &diff) {
  ICoord id = ip1 - ip0;
  // TODO MERGE: fill in the 2D part and use it.
#if DIM==3
  // swap endpoints if they are not in the right order.  Making a huge
  // if condition so we don't have to repeat these few lines of code
  // 6 times.
  if( ( id[2] == 0 &&
	// z-plane with bigger x-range
	(( fabs(diff[0]) >= fabs(diff[1]) && ip0[0] > ip1[0] ) || 
	 // z-plane with bigger y-range
	 ( fabs(diff[1]) > fabs(diff[0]) && ip0[1] > ip1[1] )) ) 
      ||
      ( id[1] == 0 &&
	// y-plane with bigger z-range
	(( fabs(diff[2]) >= fabs(diff[0]) && ip0[2] > ip1[2] ) || 
	 // y-plane with bigger x-range
	 ( fabs(diff[0]) > fabs(diff[2]) && ip0[0] > ip1[0] )) )
      || 
      ( id[0] == 0 &&
	// x-plane with bigger z-range
	(( fabs(diff[2]) >= fabs(diff[1]) && ip0[2] > ip1[2] ) || 
	 // x-plane with bigger y-range
	 ( fabs(diff[1]) > fabs(diff[2]) && ip0[1] > ip1[1] )) )
      ) 
    return true;
  return false;
#endif	// DIM==3
}

// Return a list (vector) of pixels underlying a segment.  It's the
// responsibility of the caller to delete the vector.
std::vector<ICoord> *CMicrostructure::segmentPixels(const Coord &c0,
						    const Coord &c1,
						    bool &vertical_horizontal,
						    bool &swap,
						    bool verbose)
  const
{
  // Coordinates of endpoints in pixel space (real).
  Coord p0(physical2Pixel(c0));
  Coord p1(physical2Pixel(c1));
  // if(verbose) {
  //   oofcerr << "CMicrostructure::segmentPixels: c0=" << c0 << " c1=" << c1
  // 	    << std::endl
  // 	    << "                                 p0=" << p0 << " p1=" << p1
  // 	    << std::endl;
  // }

  // Coordinates of pixels containing the endpoints (integer).  Note
  // that we *don't* use CMicrostructure::pixelFromPoint() here,
  // because we have to treat the pixel boundary cases differently.
#if DIM==2
  ICoord ip0((int) floor(p0[0]), (int) floor(p0[1]));
  ICoord ip1((int) floor(p1[0]), (int) floor(p1[1]));
#elif DIM==3
  ICoord ip0((int) floor(p0[0]), (int) floor(p0[1]), (int) floor(p0[2]));
  ICoord ip1((int) floor(p1[0]), (int) floor(p1[1]), (int) floor(p1[2]));
  // if(verbose)
  //   oofcerr << "CMicrostructure::segmentPixels: ip0=" << ip0 << " ip1=" << ip1
  // 	    << std::endl;
#endif

  // If an endpoint lies exactly on a pixel boundary, then the correct
  // choice for the pixel "containing" the endpoint depends on which
  // direction the segment is going.  The rule is that some part of
  // the segment must lie within the selected pixel. 
  for(int i=0; i<DIM; ++i) {
    if(ip0[i] == p0[i] && ip1[i] < ip0[i])
      ip0[i] -= 1;
    if(ip1[i] == p1[i] && ip0[i] < ip1[i])
      ip1[i] -= 1;
  }

  // Round off error may have put a point out of bounds.  Fix it.
  for(int i=0; i<DIM; ++i) {
    if(ip0[i] == pxlsize_[i]) ip0[i] -= 1;
    if(ip1[i] == pxlsize_[i]) ip1[i] -= 1;
    if(ip0[i] < 0) ip0[i] = 0;
    if(ip1[i] < 0) ip1[i] = 0;
  }
  // if(verbose)
  //   oofcerr << "CMicrostructure::segmentPixels: bounds check ip0=" << ip0 
  // 	    << " ip1=" << ip1
  // 	    << std::endl;

  // For vertical and horizontal segments that exactly lie along the
  // pixel boundaries, we need to pick the correct row or column of
  // pixels.  For instance,
  //
  //  |    element B  |
  //  |xxxxxxxxxxxxxxx|
  //  b---------------a   segment a-b lies on the pixel boundary
  //  |ooooooooooooooo|
  //  |    element A  |
  //
  //  From element A's point of view, pixels along the segment a-b
  //  should be "ooooo", whereas from element B's p.o.v, corresponding
  //  pixels should be "xxxxx".
  //  Code below will deal with this adjustment.


  vertical_horizontal=false;
#if DIM==2
  // This assumes we are traversing an element in counter clockwise
  // order, which we can only do in 2D.  Here, we are trying to get
  // the pixels that lie on the inside of the element.  We'll have to
  // use different conditions in 3D to figure out which side is the
  // inside. 
  // Horizontal
  if ((p0[1] == p1[1] && p0[1] == ip0[1]) && p0[0] > p1[0]) {
    if(ip0[1] >= 1) ip0[1] -= 1;
    if(ip1[1] >= 1) ip1[1] -= 1;
    vertical_horizontal=true;
  }
  // Vertical 
  if ((p0[0] == p1[0] && p0[0] == ip0[0]) && p0[1] < p1[1]) {
    if(ip0[0] >= 1) ip0[0] -= 1;
    if(ip1[0] >= 1) ip1[0] -= 1;
    vertical_horizontal=true;
  }
#elif DIM==3 
  //TODO 3.1: Figure out how what conditions to use to get the inside.
  // We need to pass in information about which direction to perturb
  // in.  This needs to be chosen carefully, using element data such
  // that this direction is not along a plane.
//   // Horizontal
//   if ((p0[1] == p1[1] && p0[1] == ip0[1])) {
//     vertical_horizontal=true;
//   }
//   // Vertical 
//   if ((p0[0] == p1[0] && p0[0] == ip0[0])) {
//     vertical_horizontal=true;
//   }
//   // The other Horizontal
//   if ((p0[2] == p1(2) && p0[2] == ip0[2])) {
//     vertical_horizontal=true;
//   }
#endif

  // For vertical and horizontal segments on skeleton(microstructure)
  // edges, all that matters is that the chosen pixels aren't outside
  // the microstructure.  After the preceding check, the only way that
  // an end pixel can be outside is if the segment lies along the top
  // right, or front edges.
  for(int i=0; i<DIM; ++i) {
    int max = pxlsize_[i];
    if(ip0[i] == max && ip1[i] == max) {
      ip0[i] = max - 1;
      ip1[i] = max - 1;
    }
  }
  // if(verbose)
  //   oofcerr << "CMicrostructure::segmentPixels: after bdy check, ip0="
  // 	    << ip0 << " ip1=" << ip1 << std::endl;


  ICoord id = ip1 - ip0;	// distance between pixel endpoints
  Coord diff = p1 - p0;
  //if(print) oofcerr << "id, diff " << id << " " << diff << std::endl;

#if DIM==2
  if(id[0] == 0 && id[1] == 0) { // segment is entirely within one pixel
    return new std::vector<ICoord>(1, ip0);
  }
  
  if(id[0] == 0) {	
    // Segment is contained within a single column of pixels.
    int npix = abs(id[1]) + 1;
    std::vector<ICoord> *pixels = new std::vector<ICoord>(npix);
    int x = ip0[0];
    int y0 = (ip0[1] < ip1[1]) ? ip0[1] : ip1[1];
    for(int i=0; i<npix; i++)
      (*pixels)[i] = ICoord(x, y0+i);
    return pixels;
  }
  
  if(id[1] == 0) {	
    // Segment is contained within a single row of pixels.
    int npix = abs(id[0]) + 1;
    std::vector<ICoord> *pixels = new std::vector<ICoord>(npix);
    int y = ip0[1];
    int x0 = (ip0[0] < ip1[0]) ? ip0[0] : ip1[0];
    for(int i=0; i<npix; i++)
      (*pixels)[i] = ICoord(x0+i, y);
    return pixels;
  }

  // segment is diagonal
  if(abs(id[0]) >= abs(id[1])) {
    // x range is bigger than y range, so loop over x.
    // Make sure that p0 is to the left of p1.
    if(ip0[0] > ip1[0]) {
      ICoord itemp(ip1);
      ip1 = ip0;
      ip0 = itemp;
      Coord temp(p1);
      p1 = p0;
      p0 = temp;
    }
    std::vector<ICoord> *pixels = new std::vector<ICoord>;
    pixels->reserve(2*abs(id[0])); // biggest possible size
    double x0 = p0[0];
    double y0 = p0[1];
    double slope = (p1[1] - y0)/(p1[0] - x0);
    pixels->push_back(ip0);
    // Iterate over columns of pixels.  Compute the y intercepts at
    // the boundaries between the columns (ie, integer values of x).
    // Whenever the integer part of the y intercept changes, we need
    // to include an extra pixel (at the new y value) in the previous
    // column.
    int lasty = ip0[1];	// previous integer part of y intercept
    for(int x=ip0[0]+1; x<=ip1[0]; ++x) {
      int y = int(floor(y0 + slope*(x-x0)));
      if(y >=0 && y < pxlsize_[1]) {
	if(y != lasty) {
	  pixels->push_back(ICoord(x-1, y));
	}
	pixels->push_back(ICoord(x,y));
      }
      lasty = y;
    }
    // The last pixel may not have been included yet, if there's one
    // more y intercept change to come, so make sure it's included.
    if(pixels->back() != ip1)
      pixels->push_back(ip1);
    return pixels;
  } // abs(id(0)) >= abs(id(1))
  
  // abs(id(1)) > abs(id(0))
  // y range is bigger than x range, so loop over y.
  if(ip0[1] > ip1[1]) {
    ICoord itemp(ip1);
    ip1 = ip0;
    ip0 = itemp;
    Coord temp(p1);
    p1 = p0;
    p0 = temp;
  }
  std::vector<ICoord> *pixels = new std::vector<ICoord>;
  pixels->reserve(2*abs(id(1)));
  double x0 = p0[0];
  double y0 = p0[1];
  double slope = (p1[0] - x0)/(p1[1] - y0); // dx/dy
  pixels->push_back(ip0);
  int lastx = ip0[0];
  // iterate over rows of pixels
  for(int y=ip0[1]+1; y<=ip1[1]; ++y) {
    int x = int(floor(x0 + slope*(y-y0)));
    if(x >= 0 && x < maxx) {
      if(x != lastx)
	pixels->push_back(ICoord(x, y-1));
      pixels->push_back(ICoord(x,y));
    }
    lastx = x;
  }
  if(pixels->back() != ip1)
    pixels->push_back(ip1);
  return pixels;

#elif DIM==3

  if(id[0] == 0 && id[1] == 0 && id[2] == 0) {
    // segment is entirely within one pixel
    return new std::vector<ICoord>(1, ip0);
  }

  swap = swapEndPoints(ip0, ip1, diff);
  if(swap) {
    ICoord itemp(ip1);
    ip1 = ip0;
    ip0 = itemp;
    Coord temp(p1);
    p1 = p0;
    p0 = temp;
  }
  // if(verbose)
  //   oofcerr << "CMicrostructure::segmentPixels: after swap: ip0="
  // 	    << ip0 << " ip1=" << ip1 << std::endl;

  ICoord start, increment;
  int npix = 0;
  bool line = false, plane = false;
  int i = -1, j = -1, k = -1;
  if(id[0] == 0 && id[2] == 0) {	
    // Segment is contained within a single y-column of pixels.
    i = 1;
    j = 2;
    k = 0;
    line = true;
  }

  if(id[1] == 0 && id[2] == 0) {	
    // Segment is contained within a single x-row of pixels.
    i = 0;
    j = 1;
    k = 2;
    line = true;
  }

  if(id[0] == 0 && id[1] == 0) {	
    // Segment is contained within a single z-column of pixels.
    i = 2;
    j = 0;
    k = 1;
    line = true;
  }
  // if(verbose)
  //   oofcerr << "CMicrostructure::segmentPixels: line=" << line << std::endl;
  if(line) {
    npix = abs(id[i]) + 1;
    start[i] = (ip0[i] < ip1[i]) ? ip0[i] : ip1[i];
    start[j] = ip0[j];
    start[k] = ip0[k];
    increment[i] = 1;
    increment[j] = increment[k] = 0;
    std::vector<ICoord> *pixels = new std::vector<ICoord>(npix);
    for(int i=0; i<npix; i++) 
      (*pixels)[i] = start+increment*i;
    return pixels;
  }

  double slope = 0;
  int x = 0, y = 0, z = 0, lasty = 0;
  double x0 = 0, y0 = 0;

  if(id[2] == 0) {
    // segment is in a z-plane
    k = 2;
    z = ip0[2];
    // if(verbose)
    //   oofcerr << "CMicrostructure::segmentPixels: diff=" << diff << std::endl;
    if(fabs(diff[0]) >= fabs(diff[1])) {
      // loop over x
      // if(verbose)
      // 	oofcerr << "CMicrostructure::segmentPixels: looping over x"
      // 		<< std::endl;
      i = 0;
      j = 1;
    }
    else {
      // if(verbose)
      // 	oofcerr << "CMicrostructure::segmentPixels: looping over y"
      // 		<< std::endl;
      i = 1;
      j = 0;
    }
    plane = true;
  }
  if(id[1] == 0) {
    // segment is in a y-plane
    k = 1;
    z = ip0[1];
    if(fabs(diff[2]) >= fabs(diff[0])) {
      // loop over z
      i = 2;
      j = 0;
    }
    else {
      i = 0;
      j = 2;
    }
    plane = true;
  }
  if(id[0] == 0) {
    // segment is in an x-plane
    k = 0;
    z = ip0[0];
    if(fabs(diff[2]) >= fabs(diff[1])) {
      // loop over z
      i = 2;
      j = 1;
    }
    else {
      i = 1;
      j = 2;
    }
    plane = true;
  }
  // if(verbose)
  //   oofcerr << "CMicrostructure::segmentPixels: plane=" << plane
  // 	    << " i=" << i << " j=" << j << " k=" << k
  // 	    << std::endl;
  // for simplicity, i and x indicate the coordinate we are looping
  // over, j and y indicate the other varying coord, and k and z refer
  // to the fixed coord.
  if(plane) {
    x0 = p0[i];
    y0 = p0[j];
    slope = (p1[j] - y0)/(p1[i] - x0); 
    std::vector<ICoord> *pixels = new std::vector<ICoord>;
    pixels->reserve(2*abs(id[i])); // biggest possible size
    pixels->push_back(ip0);
    // if(verbose)
    //   oofcerr << "CMicrostructure::segmentPixels: startpt=" << pixels->back()
    // 	      << std::endl;
    // Iterate over columns of pixels.  Compute the y intercepts at
    // the boundaries between the columns (ie, integer values of x).
    // Whenever the integer part of the y intercept changes, we need
    // to include an extra pixel (at the new y value) in the previous
    // column.
    lasty = ip0[j];	// previous integer part of y intercept
    // if(verbose)
    //   oofcerr << "CMicrostructure::segmentPixels: x range = "
    // 	      << ip0[i]+1 << " " << ip1[i] << std::endl;
    for(int x = ip0[i]+1; x <= ip1[i]; ++x) {
      int y = int(floor(y0 + slope*(x-x0)));
      if(y >= 0 && y < pxlsize_[j]) {
	if(y != lasty) {
	  ICoord vox1;
	  vox1[i] = x-1;
	  vox1[j] = y;
	  vox1[k] = z;
	  pixels->push_back(vox1);
	  // if(verbose)
	  //   oofcerr << "CMicrostructure::segmentPixels: added extra " 
	  // 	    << pixels->back() << std::endl;
	}
	ICoord vox2;
	vox2[i] = x;
	vox2[j] = y;
	vox2[k] = z;
	pixels->push_back(vox2);
	// if(verbose)
	//   oofcerr << "CMicrostructure::segmentPixels: added " << pixels->back()
	// 	  << std::endl;
      }
      lasty = y;
    }    
    // The last pixel may not have been included yet, if there's one
    // more y intercept change to come, so make sure it's included.
    if(pixels->back() != ip1) {
      pixels->push_back(ip1);
      // if(verbose)
      // 	oofcerr << "CMicrostructure::segmentPixels: added final "
      // 		<< pixels->back() << std::endl;
    }
    // if(verbose)
    //   oofcerr << "CMicrostructure::segmentPixels: done" << std::endl;
    return pixels;
  }

  // if we haven't returned by now, then the segment varies in all 3
  // coords. First find which coordinate has the largest range.
  double max = 0;
  for(int c = 0; c < 3; ++c) {
    if(fabs(diff[c]) > max || abs(id[c]) > max ||
       (abs(id[c]) == max && fabs(diff[c]) > fabs(diff[i])) ) 
      {
	max = (fabs(diff[c]) > abs(id[c]) ? fabs(diff[c]) : abs(id[c]));
	i = c;
	if(fabs(diff[ (c+1) % 3]) > fabs(diff[ (c+2) % 3])) {
	  j = (c+1) % 3;
	  k = (c+2) % 3;
	}
	else {
	  j = (c+2) % 3;
	  k = (c+1) % 3;
	}
      }
  }
  // Now swap the coords if necessary.
  if(ip0[i] > ip1[i]) {
    ICoord itemp(ip1);
    ip1 = ip0;
    ip0 = itemp;
    Coord temp(p1);
    p1 = p0;
    p0 = temp;
    swap = true;
  }

  x0 = p0[i];
  y0 = p0[j];
  double z0 = p0[k];
  slope = (p1[j] - y0)/(p1[i] - x0);  
  double slopez = (p1[k] - z0)/(p1[i] - x0);
  std::vector<ICoord> *pixels = new std::vector<ICoord>;
  pixels->reserve(2*abs(id[i])); // biggest possible size
  pixels->push_back(ip0);
  // Iterate over columns of pixels.  Compute the y intercepts at the
  // boundaries between the columns (ie, integer values of x).
  // Whenever the integer part of the y or z intercept changes, we
  // need to include an extra pixel (at the new y, or z, or both
  // values) in the previous column.
  lasty = ip0[j];	// previous integer part of y intercept
  int lastz = ip0[k];
  for(x = ip0[i]+1; x <= ip1[i]; ++x) {
    y = int(floor(y0 + slope*(x-x0)));
    z = int(floor(z0 + slopez*(x-x0)));
    if(y >= 0 && y < pxlsize_[j]) {
      // TODO 3.1: there could be two missing pixels here...
      if(y != lasty && z != lastz) {
	ICoord vox;
	int nexty = lasty + (slope > 0 ? 1 : -1);
	int nextz = lastz + (slopez > 0 ? 1 : -1);
	double y1 = int(floor(y0 + slope/slopez * (nextz + (slopez > 0 ? 0 : 1) - z0)));
	double z1 = int(floor(z0 + slopez/slope * (nexty + (slope > 0 ? 0 : 1) - y0))); 
	vox[i] = x-1;
	if(y1 == lasty) {
	  vox[j] = y1;
	  vox[k] = nextz;
	}
	else if(z1 == lastz) {
	  vox[j] = nexty;
	  vox[k] = z1;
	}
	else { // the segment intersects a corner
	  vox[j] = nexty;
	  vox[k] = lastz;
	}
	pixels->push_back(vox);
      }
      if(y != lasty || z != lastz) {
	ICoord vox1;
	vox1[i] = x-1;
	vox1[j] = y;
	vox1[k] = z;
	pixels->push_back(vox1);
      }
      ICoord vox2;
      vox2[i] = x;
      vox2[j] = y;
      vox2[k] = z;
      pixels->push_back(vox2);
    }
    lasty = y;
    lastz = z;
  }    
  // The last pixel may not have been included yet, and there may be
  // one more pixel in between, so make sure they're included.
  if(pixels->back() != ip1) {
    // double check that the second to last pixel is contiguous
    if(ip1[j] != lasty && ip1[k] != lastz) {
      ICoord vox;
      int nexty = y + (slope > 0 ? 1 : -1);
      int nextz = z + (slopez > 0 ? 1 : -1);
      y = int(floor(y0 + slope/slopez * (nextz + (slopez > 0 ? 0 : 1) - z0)));
      z = int(floor(z0 + slopez/slope * (nexty + (slope > 0 ? 0 : 1) - y0))); 
      vox[i] = x-1;
      if(y == lasty) {
	vox[j] = y;
	vox[k] = nextz;
      }
      else if(z == lastz) {
	vox[j] = nexty;
	vox[k] = z;
      }
      else { // the segment intersects a corner
	vox[j] = nexty;
	vox[k] = lastz;
      }
      pixels->push_back(vox);
    }
    pixels->push_back(ip1);
  }
  return pixels;

#endif	// DIM==3

} // end CMicrostructure::segmentPixels

// TODO 3.1: Code for marking the pixels under segments and triangles
// hasn't been updated for 3D.  The 2D code won't compile with the 3D
// Coord and ICoord classes.

#if DIM==2

static const ICoord east(1, 0);
static const ICoord west(-1, 0);
static const ICoord north(0, 1);
static const ICoord south(0, -1);
static const ICoord northeast(1, 1);
static const ICoord northwest(-1, 1);
static const ICoord southeast(1, -1);
static const ICoord southwest(-1, -1);

MarkInfo::MarkInfo(const ICoord &size)
  : markedpixels(size, false),
    markedregion(markedpixels.subarray(ICoord::origin, markedpixels.size()))
{
  // Initial setting of markedregion will be overwritten... why is it done?
}


// Set the bounds of the marking region and clear it.  The
// markedpixels array is an array of booleans, used as an intermediate
// result when marking complicated things like elements.

MarkInfo *CMicrostructure::beginMarking(const CRectangle &bbox) const {
  MarkInfo *mm = new MarkInfo(sizeInPixels());
  ICoord p0 = pixelFromPoint(bbox.lowerleft());
  ICoord p1 = pixelFromPoint(bbox.upperright()) + northeast;
  if(p1[0] >= pxlsize_[0]) p1[0] = pxlsize_[0];
  if(p1[1] >= pxlsize_[1]) p1[1] = pxlsize_[1];
  mm->markedregion = mm->markedpixels.subarray(p0, p1);
  mm->markedregion.clear(false);
  return mm;
}

// Return a set containing all the marked pixels.  It's the
// responsibility of the caller to delete the vector.

ICoordVector *CMicrostructure::markedPixels(MarkInfo *mm) const {
  return mm->markedregion.pixels(true); // returns new'd vector
}

// Mark the pixels underlying a segment.

void CMicrostructure::markSegment(MarkInfo *mm, 
				  const Coord &c0, const Coord &c1) const
{
  bool dummy1, dummy2;
  const std::vector<ICoord> *pixels = segmentPixels(c0, c1, dummy1, dummy2, false);
//   oofcerr << "CMicrostructure::markSegment: c0=" <<  c0 << " c1=" << c1 << std::endl;
  for(std::vector<ICoord>::const_iterator pxl=pixels->begin();
      pxl<pixels->end(); ++pxl)
    {
//       oofcerr << "CMicrostructure::markSegment: pxl=" << *pxl << std::endl;
      mm->markedregion.set(*pxl);
    }
//   oofcerr << "CMicrostructure:markSegment: deleting pixels" << std::endl;
  delete pixels;
//   oofcerr << "CMicrostructure::markSegment: done" << std::endl;
}


// Mark the pixels under a triangle by marking the pixels under its
// edges, then using a burn algorithm to mark the ones inside.

void CMicrostructure::markTriangle(MarkInfo *mm, const Coord &c0,
				   const Coord &c1, const Coord &c2)
  const
{
  markSegment(mm, c0, c1);
  markSegment(mm, c1, c2);
  markSegment(mm, c2, c0);
  // Find an unmarked point at which to start the burn algorithm.  For
  // small or narrow triangles, the center point may lie within a
  // pixel's distance of the edge and be already marked.
  ICoord start = pixelFromPoint(1./3.*(c0 + c1 + c2));
  if(mm->markedregion[start]) {
    // Center is already marked.  Unmarked pixels, if any, will lie
    // near the triangle's shortest edge.  Look for an unmarked pixel
    // by starting at the midpoint of the shortest edge and moving
    // towards the center of the triangle.  This code is really ugly
    // since it hardly seems worthwhile to put c0,c1,c2 in an array
    // and iterate over them.
    int shortest = 0;
    double shortlen = norm2(c1 - c2);
    double dd = norm2(c2 - c0);
    if(dd < shortlen) {
      shortlen = dd;
      shortest = 1;
    }
    dd = norm2(c0 - c1);
    if(dd < shortlen) {
      shortest = 2;
    }
    Coord mid;			// midpoint of shortest side
    Coord r;			// unit vector from center of short
				// side toward the opposite corner.
    switch (shortest) {
    case 0:
      mid = 0.5*(c1 + c2);
      r = c0 - mid;
      break;
    case 1:
      mid = 0.5*(c2 + c0);
      r = c1 - mid;
      break;
    case 2:
      mid = 0.5*(c0 + c1);
      r = c2 - mid;
      break;
    }
    double normr = sqrt(norm2(r));
    double maxdist = normr/3.0;	// no point in moving beyond center
    r = (1./normr)*r;		// unit vector
    double d = 1.0;
    bool ok = false;		// found a starting point yet?
    while(d < maxdist && !ok) {
      start = pixelFromPoint(mid + d*r);
      if(!mm->markedregion[start])
	ok = true;
      d += 1.0;
    }
    if(!ok) return;		// all interior pixels must already be marked
  }
  // Burn algorithm.  If a site is unmarked, the mark_site routine
  // marks it and puts it on the activesites list.  The main loop
  // (here) removes sites from the list and calls mark_site on their
  // neighbors.  Since the edges of the triangle are already marked,
  // they don't become active, and the burn won't spread beyond the
  // edges.
  std::vector<ICoord> activesites; // sites whose neighbors need to be checked
  mm->mark_site(activesites, start); // come on baby, light my fire
  while(!activesites.empty()) {
    const ICoord here = activesites.back();
    activesites.pop_back();
    mm->mark_site(activesites, here + east);
    mm->mark_site(activesites, here + west);
    mm->mark_site(activesites, here + north);
    mm->mark_site(activesites, here + south);
    mm->mark_site(activesites, here + northeast);
    mm->mark_site(activesites, here + northwest);
    mm->mark_site(activesites, here + southeast);
    mm->mark_site(activesites, here + southwest);
  }
}      // end markTriangle

void MarkInfo::mark_site(std::vector<ICoord> &activesites,
			     const ICoord &here)
{
  if(markedregion.contains(here) && !markedregion[here]) {
    markedregion.set(here);
    activesites.push_back(here);
  }
}

void CMicrostructure::endMarking(MarkInfo *mm) const {
  delete mm;
}

#endif // DIM==2

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Returns Point instead of bool via the cskel_OutPoint typemap.
// bool CMicrostructure::transitionPointWithPoints(const Coord *c0,
// 						const Coord *c1,
// 						Coord *point) const
// {
//   TransitionPointIterator tpIterator(this, *c0, *c1);
//   return transitionPointClosest(*c0, *c1, tpIterator, point); 
// }


// // Find the closest transition point in the segment that ranges
// // from c0 to c1.  The TransitionPointIterator stores the vector of pixels.
// bool CMicrostructure::transitionPointClosest(const Coord &c0, const Coord &c1, 
// 					     TransitionPointIterator &tpIterator,
// 					     Coord *result) const
// {

//   std::vector<Coord> *transitions = new std::vector<Coord>;
//   bool found = false;
//   for(tpIterator.begin(); !tpIterator.end(); ++tpIterator) {
//     found = true;
//     transitions->push_back( pixel2Physical(tpIterator.current()) );
//   }

//   // Now, we need to sort them out to find the closest
//   int tsize = transitions->size();
//   if( found && tsize>0){ 
//     if(tsize == 1)
//       *result = Coord((*transitions)[0]);
//     else {
//       double min, dist;
//       int theone = 0;
//       min = norm2((*transitions)[0] - c0);
//       for(int i=1; i<tsize; i++) {
// 	dist = norm2((*transitions)[i] - c0);
// 	if(dist < min) {
// 	  min = dist;
// 	  theone = i;
// 	}
//       }
//       *result = Coord((*transitions)[theone]);
//     }
//   }
//   delete transitions;
  
//   return found;
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the point on the line joining c0 and c1 at which the pixel
// category changes, and return it in result.  The return value is
// true if there's exactly one transition point.

bool CMicrostructure::transitionPoint(const Coord &c0, const Coord &c1,
				      Coord *result, bool verbose) const
{

  bool found1 = false;
  for(TransitionPointIterator tpIterator(this, c0, c1, verbose); 
      !tpIterator.end(); ++tpIterator) {
    *result = pixel2Physical(tpIterator.current());
    if(found1) {   // found too many transitions
      return false;
    }
    else
      found1 = true;
  }
  return found1;

}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double CMicrostructure::edgeHomogeneity(const Coord &c0, const Coord &c1) 
  const
{
  // oofcerr << "CMicrostructure::edgeHomogeneity" << std::endl;
  // oofcerr << c0 << " " << c1 << std::endl;

  TransitionPointIterator tpIterator(this, c0, c1, false); 
  // Check to see if all of the pixels have the same category.  If
  // they do, the homogeneity is 1.0.  It's *important* to do this
  // check, because without it roundoff error can give a result that
  // is less than 1.0.  
  if(tpIterator.end())
    return 1.0;

  std::vector<double> lengths(nCategories(), 0.0);
  Coord prevpt = tpIterator.first();
  Coord finalpt = tpIterator.last();
  for( ; !tpIterator.end(); ++tpIterator) {
    lengths[tpIterator.getPrevcat()] += sqrt(norm2(tpIterator.current() -
						   prevpt));
    // oofcerr << tpIterator.current() << " " << prevpt << std::endl;
    // oofcerr << tpIterator.getPrevcat() << " "
    // 	    << sqrt(norm2(tpIterator.current() - prevpt)) << " "
    // 	    << lengths[tpIterator.getPrevcat()] << std::endl;
    prevpt = tpIterator.current();
  }
  lengths[tpIterator.getPrevcat()] += sqrt(norm2(finalpt - prevpt));
  // oofcerr << finalpt << " " << prevpt << std::endl;
  // oofcerr << tpIterator.getPrevcat() << " " << sqrt(norm2(finalpt - prevpt))
  // 	  << " " << lengths[tpIterator.getPrevcat()]  << std::endl;

  double max = 0.0;
  for(std::vector<double>::size_type i=0; i<lengths.size(); i++) {
    if(max < lengths[i])
      max = lengths[i];
  }

  double normdelta = tpIterator.getNormDelta();
  // oofcerr << max << " " << normdelta << std::endl;
#ifdef DEBUG
  // Use a tolerance to avoid triggering the error in cases of round off error.
  if( (max/normdelta) > (1+1e-14) )
    throw ErrProgrammingError("edge homogeneity greater than 1",
			      __FILE__, __LINE__);
#endif
  return max/normdelta;
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// For SnapRefine.

// Modified edgeHomogeneity function that returns the dominant pixel
// category.  The homogeneity value and dominant pixel category may
// depend on the order of the coordinate parameters i.e. swig'ed
// edgeHomogeneityCat(c0,c1) not always equal to
// edgeHomogeneity(c1,c0) because segmentPixels is sensitive to the
// direction c0->c1 (see the comments and implementation of
// segmentPixels).
double CMicrostructure::edgeHomogeneityCat(const Coord &c0, const Coord &c1,
					   int *cat)
  const
{
  TransitionPointIterator tpIterator(this, c0, c1, false); 
  // Check to see if all of the pixels have the same category.  If
  // they do, the homogeneity is 1.0.  It's *important* to do this
  // check, because without it roundoff error can give a result that
  // is less than 1.0.  
  if(tpIterator.end()) {
    *cat = tpIterator.getPrevcat();
    return 1.0;
  }

  std::vector<double> lengths(nCategories(), 0.0);
  Coord prevpt = tpIterator.first();
  Coord finalpt = tpIterator.last();
  for( ; !tpIterator.end(); ++tpIterator) {
    lengths[tpIterator.getPrevcat()] += sqrt(norm2(tpIterator.current() -
						   prevpt));
    prevpt = tpIterator.current();
  }
  lengths[tpIterator.getPrevcat()] += sqrt(norm2(finalpt - prevpt));

  double max = 0.0;
  for(std::vector<double>::size_type i=0; i<lengths.size(); i++) {
    if(max < lengths[i]) {
      *cat = i;
      max = lengths[i];
    }
  }

  double normdelta = tpIterator.getNormDelta();
  return max/normdelta;
}


//This version of transitionPointWithPoints looks at the pixels on both
//sides of the directed line segment c0-c1 if the segment is vertical
//or horizontal and lies at a pixel boundary.
// bool
// CMicrostructure::transitionPointWithPoints_unbiased(const Coord *c0,
// 						    const Coord *c1,
// 						    Coord *point) const
// {
//   Coord cleft,cright;
//   bool bleft, bright, bverticalhorizontal;
  
//   const std::vector<ICoord> *pixels = segmentPixels(*c0, *c1, bverticalhorizontal);
//   TransitionPointIterator tpIterator1(this, *c0, *c1, pixels);
//   bleft = transitionPointClosest(*c0, *c1, tpIterator1, &cleft);  
//   if(bverticalhorizontal)
//     {
//       const std::vector<ICoord> *pixelsright = segmentPixels(*c1, *c0, bverticalhorizontal);
//       TransitionPointIterator tpIterator2(this, *c0, *c1, pixelsright);
//       bright = transitionPointClosest(*c0, *c1, tpIterator2, &cright);
//     }
//   else
//     {
//       bright=false;
//     }
//   if(bleft && bright) {	     //Pick the one closest to the endpoint c0
//     if(norm2(*c0-cleft)<norm2(*c0-cright)) {
//       *point=cleft;
//     }
//     else {
//       *point=cright;
//     }
//     return true;
//   }
//   else if(bright) {
//     *point=cright;
//     return true;
//   }
//   else {
//     //This may be garbage
//     *point=cleft;
//     return bleft;
//   }
// }

TransitionPointIterator::TransitionPointIterator(
			const CMicrostructure *microstructure,
			const Coord &c0, const Coord &c1, bool verbose) 
{
  MS = microstructure;
  bool dummy, swap;
  // segment pixels can reorder c0 and c1. We need to make sure p0 and
  // p1 are consistent.
  if(verbose)
    oofcerr << "TransitionPointIterator::ctor: c0=" << c0 << " c1=" << c1
	    << std::endl;
  pixels = MS->segmentPixels(c0, c1, dummy, swap, verbose);
  if(verbose)
    std::cerr << "TransitionPointIterator::ctor: pixels=" << *pixels
	      << std::endl;
#ifdef DEBUG
  // make sure the pixels are contiguous
  std::vector<ICoord>::const_iterator prev = pixels->begin();
  std::vector<ICoord>::const_iterator it = prev;
  // ICoord i1(1,0,0);
  // ICoord i2(-1,0,0);
  // ICoord i3(0,1,0);
  // ICoord i4(0,-1,0);
  // ICoord i5(0,0,1);
  // ICoord i6(0,0,-1);
  bool bad = false;
  for(++it; it!=pixels->end() && !bad; ++it, ++prev) {
    const ICoord diff((*it) - (*prev));
    bad = (norm2(*it - *prev) != 1);
  }
  if(bad) {
    oofcerr << "TransitionPointIterator::ctor: coords: " << c0 << " " << c1
	      << std::endl;
    std::cerr << "TransitionPointIterator::ctor: pixels: " << *pixels
	      << std::endl;
    throw ErrProgrammingError("CMicrostructure: invalid pixel difference",
			      __FILE__, __LINE__);
  }
#endif	// DEBUG

  if(swap) {
    p0 = MS->physical2Pixel(c1);
    p1 = MS->physical2Pixel(c0);
  }
  else {
    p0 = MS->physical2Pixel(c0);
    p1 = MS->physical2Pixel(c1);
  }
  begin();
}

// TransitionPointIterator::TransitionPointIterator(
// 			const CMicrostructure *microstructure,
// 			const Coord &c0, const Coord &c1, 
// 			const std::vector<ICoord> *pxls) 
// {
//   MS = microstructure;
//   pixels = pxls;
//   p0 = MS->physical2Pixel(c0);
//   p1 = MS->physical2Pixel(c1);
//   begin();
// }

void TransitionPointIterator::begin()
{
  pixel = pixels->begin();
  cat = MS->category(*pixel);
  prevcat = cat;
  prevpixel = *pixel;
  ++pixel;
  currentTransPoint = Coord();
  delta = p1-p0;
  if(!infiniteSlope()) { // delta[0] != 0
    x0 = p0[0];
    y0 = p0[1];
    slope = delta[1]/delta[0];
    invslope = 1./slope;
#if DIM==3
    z0 = p0[2];
    slopez = delta[2]/delta[0];
    invslopez = 1./slopez;
#endif
  }
#if DIM==3
  else if (delta[1]!=0 && delta[2]!=0) {
    // delta[0] == 0, so treat y as the independent variable (?)
    y0 = p0[1];
    z0 = p0[2];
    slope = delta[2]/delta[1];
    invslope = 1./slope;
  }
#endif
  found = false;
  // find the first transition point, if there is one
  this->operator++();
}

void TransitionPointIterator::operator++() {
  localfound = false;
  prevcat = cat;
  for( ; pixel<pixels->end() && !localfound; ++pixel) {
    cat = MS->category(*pixel);
    if(cat != prevcat) {
      localfound = true;
      found = true;
      if(infiniteSlope()) {	// delta[0] == 0
#if DIM == 2
	currentTransPoint = Coord(p0[0], (*pixel)(1));
#elif DIM == 3
	if (delta[1] == 0)
	  currentTransPoint = Coord(p0[0], p0[1], (*pixel)[2]);
	else if (delta[2] == 0)
	  currentTransPoint = Coord(p0[0], (*pixel)[1], p0[2]);
	else {
	  diff = *pixel - prevpixel;
	  if(diff[1] == -1) { // moving down, take bottom edge of last point
	    y = prevpixel[1];
	    z = z0 + (y-y0)*slope;
	  }
	  else if(diff[1] == 1) { // moving up, take top edge of last point
	    y = prevpixel[1] + 1.0;
	    z = z0 + (y-y0)*slope;
	  }
	  else if(diff[2] == 1) { // moving back, take back edge of last point
	    z = prevpixel[2] + 1.0;
	    y = y0 + (z-z0)*invslope;
	  }
	  else if(diff[2] == -1) { // moving left, take left edge of last point
	    z = prevpixel[2];
	    y = y0 + (z-z0)*invslope;
	  }
	  currentTransPoint = Coord(p0[0], y, z);
	}
#endif
	//oofcerr << "C " << currentTransPoint << std::endl;
      }	
      else {   // !infiniteSlope(), delta[0] != 0
	diff = *pixel - prevpixel;
	if(diff[0] == 1) {	// moving right, take right edge of last point
	  x = prevpixel[0] + 1.0;
	  y = y0 + (x-x0)*slope;
#if DIM == 3
	  z = z0 + (x-x0)*slopez;
#endif
	}
	else if(diff[0] == -1) { // moving left, take left edge of last point
	  x = prevpixel[0];
	  y = y0 + (x-x0)*slope;
#if DIM == 3
	  z = z0 + (x-x0)*slopez;
#endif
	}
	else if(diff[1] == -1) { // moving down, take bottom edge of last point
	  y = prevpixel[1];
	  x = x0 + (y-y0)*invslope;
#if DIM == 3
	  z = z0 + (x-x0)*slopez;
#endif
	}
	else if(diff[1] == 1) {	 // moving up, take top edge of last point
	  y = prevpixel[1] + 1.0;
	  x = x0 + (y-y0)*invslope;
#if DIM == 3
	  z = z0 + (x-x0)*slopez;
#endif
	}
#if DIM == 2
	currentTransPoint = Coord(x,y);
#elif DIM == 3
	else if(diff[2] == 1) {  // moving back, take back edge of last point
	  z = prevpixel[2] + 1.0;
	  x = x0 + (z-z0)*invslopez;
	  y = y0 + (x-x0)*slope;
	}
	else if(diff[2] == -1){	// moving forwards, take front edge of last pt
	  z = prevpixel[2];
	  x = x0 + (z-z0)*invslopez;
	  y = y0 + (x-x0)*slope;
	}
	else {
	  oofcerr << "TransitionPointIterator::operator++: p0=" << p0
		  << " p1=" << p1 << " pixel=" << *pixel
		  << " prevpixel=" << prevpixel << " diff=" << diff
		  << std::endl;
	  std::cerr << "TransitionPointIterator::operator++: pixels= "
		  << *pixels << std::endl;
	  throw ErrProgrammingError("CMicrostructure: invalid pixel difference",
				    __FILE__, __LINE__);
	}
	currentTransPoint = Coord(x,y,z);
#endif
      }	// end if infiniteSlope()
    }
    prevpixel = *pixel;
  }
} // end TransitionPointIterator::operator++

Coord TransitionPointIterator::first() {
  return p0;
}	
      
Coord TransitionPointIterator::last() {
  return p1;
}  


