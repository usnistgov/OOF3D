// -*- C++ -*-
// $RCSfile: pixelgroup.h,v $
// $Revision: 1.32.2.17 $
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

#ifndef PIXELGROUP_H
#define PIXELGROUP_H

#include "common/boolarray.h"
#include "common/coord.h"
#include "common/lock.h"
#include "common/pixelattribute.h"
#include <string>
#include <vector>

class BitmapOverlay;
class CMicrostructure;
class CPixelSelection;

// PixelSet is the base class for PixelGroup.  It keep track of the
// pixels, but doesn't manipulate the Microstructure's lists of pixel
// groups or categories.

class PixelSet {
private:
  static int ngroups;
  const int id_;
protected:
  mutable SLock member_lock;
  void weed() const;
  mutable ICoordVector members_;
  mutable bool weeded;
  ICoord geometry;
  CMicrostructure *microstructure;
public:
  PixelSet(const ICoord *geometry, CMicrostructure *microstructure);
  PixelSet(const PixelSet&);
  virtual ~PixelSet();
  int id() const { return id_; }
  void resize(const ICoord *newgeom);
  int len() const;
  bool empty() const;
  PixelSet *clone() const { return new PixelSet(*this); }

  CMicrostructure *getMicrostructure() const { return microstructure; }
  
  void add(CPixelSelection *sel);
  void add(PixelSet *set);
  void addWithoutCheck(CPixelSelection *sel);
  void addWithoutCheck(PixelSet *set);
  virtual void add(const ICoordVector*);
  virtual void addWithoutCheck(const ICoordVector*); // ignore active area
  virtual void add(const ICoord&);
  void remove(CPixelSelection *sel);
  void remove(PixelSet *set);
  void removeWithoutCheck(CPixelSelection *sel);
  void removeWithoutCheck(PixelSet *set);
  virtual void remove(const ICoordVector*);
  virtual void removeWithoutCheck(const ICoordVector*);
  // ICoord pop();			// remove and return one pixel
  virtual void clear();

  virtual void setFromBitmap(const BitmapOverlay&);

  const ICoordVector *members() const;
  void getBounds(ICoord &min, ICoord  &max) const;

  void despeckle(int threshold, BoolArray &selected) const;
  void elkcepsed(int threshold, BoolArray &selected) const;
  void expand(double range, BoolArray &selected) const;
  void shrink(double range, BoolArray &selected) const;
};

class GroupList;
class PixelGroup;
//typedef void (GroupList::*ManipulateGroupList)(PixelGroup*);

class PixelGroup : public PixelSet, public SubAttribute {
private:
  bool meshable_;
public:
  PixelGroup(const std::string &name, const ICoord *geometry,
	     CMicrostructure *microstructure);
  PixelGroup(const std::string &name, const PixelGroup &othergroup);
  virtual ~PixelGroup();
  virtual bool is_meshable() const { return meshable_; }
  void set_meshable(bool);
  virtual void add(const ICoordVector *pixels);
  virtual void addWithoutCheck(const ICoordVector*);
  virtual void add(const ICoord&);
  virtual void remove(const ICoordVector *pixels);
  virtual void clear();
  bool pixelInGroup(const ICoord*);
  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class GroupList : public ListAttribute {
private:
  static const std::string displayname_;
public:
  GroupList() : ListAttribute() {};
  GroupList(const GroupList &g) : ListAttribute(g) {};
  virtual GroupList *clone() const {return new GroupList(*this);};
  virtual bool operator<(const PixelAttribute&) const;  
  virtual const std::string &displayname() const {return displayname_;};
//   static void buildAttributeChangeMap(AttributeVectorMap &avm, ManipulateListAttribute manip, 
// 				      PixelGroup *group, CMicrostructure *microstructure);
};


class GroupListGlobalData : public PixelAttributeGlobalData {
public:
  GroupListGlobalData() : PixelAttributeGlobalData() {};
  virtual ~GroupListGlobalData() {};
  void removeGroup(const std::string &name);
};

std::vector<std::string> *pixelGroupNames(const CMicrostructure*,
					  int cat);

bool pixelGroupQueryPixel(const CMicrostructure&, const ICoord&,
			  const PixelGroup*);
bool pixelGroupQueryCategory(const CMicrostructure&, int, const PixelGroup*);

class PixelGroupAttributeRegistration : public PxlAttributeRegistration {
private:
  static const std::string classname_;
  static const std::string modulename_;
public:
  PixelGroupAttributeRegistration();
  virtual ~PixelGroupAttributeRegistration() {}
  virtual PixelAttribute *createAttribute(const CMicrostructure*) const;
  virtual PixelAttributeGlobalData *createAttributeGlobalData(
				      const CMicrostructure *ms) const;
  virtual const std::string &classname() const { return classname_;}
  virtual const std::string &modulename() const { return modulename_; }
};

#endif // PIXELGROUP_H
