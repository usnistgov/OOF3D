// -*- C++ -*-
// $RCSfile: activearea.h,v $
// $Revision: 1.8.10.10 $
// $Author: langer $
// $Date: 2014/09/15 15:08:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef ACTIVEAREA_H
#define ACTIVEAREA_H

#include <list>
#include <string>
#include <vector>
#include "common/cpixelselection.h"
#include "common/pixelattribute.h"

class ActiveArea : public CPixelSelection, public SubAttribute {
private:
  bool override_;
public:
  ActiveArea(const ICoord *pxlsize, const Coord *size, CMicrostructure*);
  virtual ~ActiveArea();
  ActiveArea *clone() const { return new ActiveArea(*this); }
  ActiveArea *named_clone(const std::string &name) const;
  bool isActive(const ICoord *pxl) const {
    return override_ || !isSelected(pxl);
  }
  bool isActive(const ICoord &pxl) const {
    return override_ || !isSelected(&pxl);
  }
  void override(bool val) { override_ = val; }
  bool getOverride() const { return override_; }
  void clear();

  void add_pixels(const ICoordVector*);
};

// Pixels in the microstructure can be members of named active areas.
// Note that being a member of an active area means that this pixel is
// *inactive* when the active area in question is current.

class ActiveAreasAttributeRegistration: public PxlAttributeRegistration {
private:
  static const std::string classname_;
  static const std::string modulename_;
public:
  ActiveAreasAttributeRegistration();
  virtual ~ActiveAreasAttributeRegistration() {}
  virtual PixelAttribute* createAttribute(const CMicrostructure*) const;
  virtual const std::string &classname() const { return classname_; }
  virtual const std::string &modulename() const { return modulename_; }
};


class ActiveAreaList : public ListAttribute {
private:
  static const std::string displayname_;
  //static ActiveAreasAttributeRegistration* reg;
public:
  ActiveAreaList() : ListAttribute() {}
  // TODO OPT: Does the copy constructor need to be explicit?  It doesn't
  // do anything special.
  ActiveAreaList(const ActiveAreaList &g) : ListAttribute(g) {}
  virtual ActiveAreaList *clone() const { return new ActiveAreaList(*this); }
  virtual bool operator<(const PixelAttribute&) const;
  virtual const std::string &displayname() const { return displayname_; }
  // These two need access to the "reg" datum.
//   friend class ActiveAreasAttributeRegistration;
//   friend ActiveAreaList *areaListFromPixel(const CMicrostructure*,
// 					   const ICoord*);  
//   static void buildAttributeChangeMap(AttributeVectorMap &avm, ManipulateListAttribute manip, 
// 				      ActiveArea *aa, CMicrostructure *microstructure);

};
  
// Utility function for geting the AAList object from a particular pixel.

ActiveAreaList *areaListFromPixel(const CMicrostructure*, const ICoord*);

#endif // ACTIVEAREA_H
