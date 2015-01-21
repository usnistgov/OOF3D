// -*- C++ -*-
// $RCSfile: cmicrostructure.h,v $
// $Revision: 1.51.8.36 $
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

#ifndef CMICROSTRUCTURE_H
#define CMICROSTRUCTURE_H

class CMicrostructure;

#include "common/array.h"
#include "common/boolarray.h"
#include "common/coord.h"
#include "common/lock.h"
#include "common/pixelattribute_i.h"
#include "common/timestamp.h"

#include <list>
#include <vector>

class ActiveArea;
class CPixelSelection;
class CSegment;
class CRectangle;
class PixelGroup;

#if DIM==2
class PixelSetBoundary;
#else
class VoxelSetBoundary;
#endif

// Some operations, such as finding the pixels under an element,
// require marking pixels in the microstructure.  Neither the
// microstructure nor the pixels can keep track of which pixels are
// marked, because there might be concurrent marking threads.  So the
// mark information is kept in a separate MarkInfo object.
class MarkInfo {
private:
  friend class CMicrostructure;
  MarkInfo(const ICoord &size);
  BoolArray markedpixels;
  BoolArray markedregion;	// active subarray of markedpixels
  void mark_site(std::vector<ICoord>&, const ICoord&);
  friend std::ostream &operator<<(std::ostream &os, const MarkInfo &mi) {
    os << mi.markedregion; 
    return os;
  }
};


class TransitionPointIterator {
private:
  const CMicrostructure *MS;
  const std::vector<ICoord> *pixels;
  std::vector<ICoord>::const_iterator pixel;
  Coord p0, p1, delta, currentTransPoint;
  ICoord diff, prevpixel;
  int cat, prevcat;
  double slope, invslope, x0, y0, x, y;
#if DIM==3
  double slopez, invslopez, z0, z;
#endif
  bool found, localfound;

public:
  TransitionPointIterator(const CMicrostructure*, const Coord&, const Coord&,
			  bool verbose); 
  // TransitionPointIterator(const CMicrostructure*, const Coord&, const Coord&,
  // 			  const std::vector<ICoord> *); 
  ~TransitionPointIterator() { delete pixels; } 
  void begin(); 
  bool infiniteSlope() { return (delta[0]==0); }
  void operator++();
  Coord current() { return currentTransPoint; }
  bool end() { return (pixel>=pixels->end() && localfound==false); }
  bool isfound() { return found; }
  int numPixels() { return pixels->size(); }
  int getPrevcat() { return prevcat; }
  // The first and last points of the segment.
  Coord first();
  Coord last();
  double getNormDelta() { return sqrt(norm2(delta)); }

};

// This class holds containers for the set of PixelAttributeVectors
// found in its microstructure and manages mapping those attribute
// vectors to categories as well as managing the pixel groups.  Each
// CMicrostructure contains a MicrostructureAttributes object.

class MicrostructureAttributes {
private:
  const CMicrostructure *MS;
  std::vector<PixelAttributeGlobalData*> attributeGlobalData;
  mutable AttributeVectorSet attributeVectorSet;
  mutable AttributeVectorCategoryMap attrVecToCategoryMap;
  mutable AttributeVectorVec attrVecVec;
  int pixelgroup_index;
  int ncategories_;
public:
  MicrostructureAttributes(const CMicrostructure *ms);
  ~MicrostructureAttributes();
  PixelAttributeGlobalData *getAttributeGlobalData(int attributeID) const;
  PixelAttribute* getAttributeFromCategory(unsigned int cat, int index) const;
  AttributeVectorSet::iterator begin() { return attributeVectorSet.begin(); }
  AttributeVectorSet::iterator end() { return attributeVectorSet.end(); }
  AttributeVectorSet::const_iterator begin() const {
    return attributeVectorSet.begin();
  }
  AttributeVectorSet::const_iterator end() const {
    return attributeVectorSet.end();
  }
  void addAttributes(AttributeVectorSet &new_avs) { 
    attributeVectorSet.insert(new_avs.begin(), new_avs.end()); 
  }
  void attributeChangeMapEntry(PixelAttributeVector*, PixelAttributeVector*,
			       AttributeVectorMap&, AttributeVectorSet&);
  void buildAttributeChangeMap(PixelAttribute *pa, int index,
			       AttributeVectorMap &avm);
  void prune() const;
  void categorize();
  void categorizeRO(AttributeVectorCategoryMap &avcm);
  int ncategories() { return ncategories_; }
  unsigned int getCategory(PixelAttributeVector *pav) {
    return attrVecToCategoryMap[pav];
  }
};


class CMicrostructure {
private:
  ICoord pxlsize_;		// size of microstructure in pixels
  Coord size_;			// physical size of whole microstructure
  Coord delta_;			// physical size of a pixel
  TimeStamp timestamp;

  static long globalMicrostructureCount; // for testing

  // List of pixel groups defined on this microstructure.
  std::list<PixelGroup*> pixelgroups;
  CPixelSelection *pixelSelection;

  // The array of pointers to pixel attribute vectors, assoicated with
  // each pixel.
  mutable Array<PixelAttributeVector*> attributeVectors;
  mutable MicrostructureAttributes attributes;

  // categorymap caches the pixel categories assigned by categorize().
  // It's mutable because CMicrostructure::category() is
  // logically const, but it caches the categories in the categorymap.
  mutable Array<int> categorymap;

  // List of the boundaries of the categories.
#if DIM==2
  mutable std::vector<PixelSetBoundary> categoryBdys;
#elif DIM==3
  mutable std::vector<VoxelSetBoundary> categoryBdys;
#endif

  mutable bool categorized;
  mutable int ncategories;
  void categorize() const;

  // Lock to protect the sometimes-lengthy categorization process, and
  // functions which query the data it produces.  This lock protects
  // the categoryBdys, categorized, ncategories, categorymap, and
  // defunctgroups members, and should be invoked by any
  // CMicrostructure function that modifies them, including those that
  // might do so indirectly by potentially calling categorize().
  // Categorize itself does not acquire this lock, but all of its
  // callers must.
  mutable SLock category_lock;

  // // Second lock, to protect data shared between the categorize()
  // // function and other group and attribute modifying functions --
  // // categorize reads these data, but others can write them.
  // // Specifically, this protects the attributeMap and pixelgroups
  // // data members.
  // mutable SRWLock groups_attributes_lock;
  
  ActiveArea *activearea;	

  std::string name_;
public:
  CMicrostructure(const std::string &name,
		  const ICoord *pxlsize, const Coord *size);
  ~CMicrostructure();
  const std::string &name() const { return name_; }
  void rename(const std::string &name) { name_ = name; }
  void destroy();
  const Coord &size() const { return size_; }
  const ICoord &sizeInPixels() const { return pxlsize_; }
  const Coord &sizeOfPixels() const { return delta_; }
#if DIM==2
  double areaOfPixels() const { return delta_[0]*delta_[1]; }
#elif DIM==3
  double volumeOfPixels() const { return delta_[0]*delta_[1]*delta_[2]; }
  double volume() const { return size_.x[0]*size_.x[1]*size_.x[2]; }
#endif
  Coord physical2Pixel(const Coord&) const; // real space to pixel coords
  Coord pixel2Physical(const ICoord&) const;
  Coord pixel2Physical(const Coord&) const;
  ICoord pixelFromPoint(const Coord&) const; // pixel containing the given point
  bool contains(const ICoord&) const;
  TimeStamp &getTimeStamp();
  const TimeStamp &getTimeStamp() const;

  void setCurrentActiveArea(ActiveArea *aa) { activearea = aa; }
  const ActiveArea *getActiveArea() const { return activearea; }
  bool isActive(const Coord& point) const;
  bool isActive(const ICoord &pxl) const;

  void setPixelSelection(CPixelSelection *pxlsl) { pixelSelection = pxlsl; }
  bool isSelected(const ICoord*) const;

  int nGroups() const;
  PixelGroup *getGroup(const std::string &name, bool *newness);
  PixelGroup *findGroup(const std::string &name) const;
  void removeGroup(const std::string &name);
  std::vector<std::string> *groupNames() const;

  Array<PixelAttributeVector*>& getAttributeVectors() {
    return attributeVectors; 
  }
  const Array<PixelAttributeVector*>& getConstAttributeVectors() const {
    return attributeVectors;
  }
  MicrostructureAttributes &getMSAttributes() { return attributes; }
  const MicrostructureAttributes &getMSAttributes() const {return attributes; }
  PixelAttribute* getAttribute(const ICoord &where, int index) const;
  PixelAttribute* getAttributeFromCategory(int cat, int index) const {
    return attributes.getAttributeFromCategory(cat,index); 
  }
  PixelAttributeVector *getAttributeVector(const ICoord &where) const {
    return attributeVectors[where]; 
  }
  PixelAttributeGlobalData *getAttributeGlobalData(int attributeID) const;
  void buildAttributeChangeMap(PixelAttribute *pa, int index,
			       AttributeVectorMap &avm)
  {
    attributes.buildAttributeChangeMap(pa, index, avm); 
  }
  void updateAttributeVector(const ICoord &where, AttributeVectorMap &avm)
    const;
  const Array<int> *getCategoryMap() const; // changes mutable private data
  const Array<int> *getCategoryMapRO() const; // changes no data

  int nCategories() const;
  // Three different versions of this for convenience in calling it...
  int category(const ICoord *where) const;
  int category(const ICoord &where) const;
  int category(const Coord *where) const; // Arbitrary physical-coord point.
  int category(const Coord &where) const; // Arbitrary physical-coord point.
  void recategorize();
  
  bool is_categorized() const { return categorized; }

#if DIM==2
  const std::vector<PixelSetBoundary> &getCategoryBdys() const {
    return categoryBdys;
  }
#elif DIM==3
  const std::vector<VoxelSetBoundary> &getCategoryBdys() const {
    return categoryBdys;
  }
#endif

  std::vector<ICoord> *segmentPixels(const Coord&, const Coord&, bool&, bool&,
				     bool verbose)
  const;
  
#if DIM==2
  MarkInfo *beginMarking(const CRectangle&) const; // sets active subarray of markedpixels
  void markSegment(MarkInfo*, const Coord&, const Coord&) const;
  void markTriangle(MarkInfo*, const Coord&, const Coord&, const Coord&) const;
  ICoordVector *markedPixels(MarkInfo*) const;
  void endMarking(MarkInfo*) const;
#endif // DIM==2

  // bool transitionPointClosest(const Coord&, const Coord&, 
  // 			      TransitionPointIterator&, Coord *result) const;
  bool transitionPoint(const Coord&, const Coord&, Coord *result, bool) const;
  double edgeHomogeneity(const Coord&, const Coord&) const;

  double edgeHomogeneityCat(const Coord&, const Coord&, int* cat) const;

  friend long get_globalMicrostructureCount();
};

long get_globalMicrostructureCount();

#endif // CMICROSTRUCTURE_H
