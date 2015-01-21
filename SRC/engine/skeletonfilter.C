// -*- C++ -*-
// $RCSfile: skeletonfilter.C,v $
// $Revision: 1.1.2.18 $
// $Author: langer $
// $Date: 2014/12/14 01:07:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "engine/IO/gridsource.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonselectable.h"
#include "engine/material.h"
#include "engine/skeletonfilter.h"

#include <algorithm>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SLock SkeletonFilter::lock;			   // static
std::vector<SkeletonFilter*> SkeletonFilter::all_; // static

const std::string &SkeletonFilter::modulename() const {
  static const std::string name = "ooflib.SWIG.engine.skeletonfilter";
  return name;
}

SkeletonFilter::SkeletonFilter()
  : gridsource(vtkSmartPointer<SkeletonGridSource>())
{
  lock.acquire();
  all_.push_back(this);
  lock.release();
}

SkeletonFilter::~SkeletonFilter() {
  lock.acquire();
  std::vector<SkeletonFilter*>::iterator i = 
    std::find(all_.begin(), all_.end(), this);
  all_.erase(i);
  lock.release();
}

std::vector<SkeletonFilter*> *getSkeletonFilters() {
  return &SkeletonFilter::all_;
}

void SkeletonFilter::mapCellIndex(vtkIdType id, int index) {
  cellIndexMap[id] = index;
}

int SkeletonFilter::getCellIndex(vtkIdType id) const {
  std::map<vtkIdType, int>::const_iterator j = cellIndexMap.find(id);
  if(j != cellIndexMap.end())
    return (*j).second;
  return -1;
}

void SkeletonFilter::setSource(vtkSmartPointer<GridSource> src) {
  gridsource = src;
}

void SkeletonFilter::setModified() {
  if(gridsource.GetPointer() != 0)
    gridsource->Modified();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// bool NodeGroupFilter::acceptable(const CSkeletonSelectable *selectable,
// 				const CSkeletonBase *skeleton)
// const
// {
//   if(selectable->is_in_group(nodegroup)){
//     return true;
//   }else{
//     return false;
//   }
// }
// 
// bool SegmentGroupFilter::acceptable(const CSkeletonSelectable *selectable,
// 				const CSkeletonBase *skeleton)
// const
// {
//   if(selectable->is_in_group(segmentgroup)){
//     return true;
//   }else{
//     return false;
//   }
// }

const std::string &NullFilter::classname() const {
  static const std::string name("NullFilter");
  return name;
}

bool ElementGroupFilter::acceptable(const CSkeletonSelectable *selectable,
				const CSkeletonBase *skeleton)
const
{
  return selectable->is_in_group(elementgroup);
}

const std::string &ElementGroupFilter::classname() const {
  static const std::string name("ElementGroupFilter");
  return name;
}

bool SelectedElementFilter::acceptable(const CSkeletonSelectable *selectable,
				       const CSkeletonBase *skeleton)
  const
{
  return selectable->isSelected();
}
				       
const std::string &SelectedElementFilter::classname() const {
  static const std::string name("SelectedElementFilter");
  return name;
}

bool MaterialFilter::acceptable(const CSkeletonSelectable *selectable,
				const CSkeletonBase *skeleton)
  const
{
  // If any of the elements that use the given selectable has the
  // given material, then the selectable should be drawn.
  ConstCSkeletonElementVector els;
  selectable->getElements(skeleton, els);
  for(ConstCSkeletonElementVector::iterator i=els.begin(); i<els.end(); ++i) {
    const Material *matl = (*i)->material(skeleton);
    if((matl and (matl->name() == materialname || materialname=="<Any>")) ||
       (!matl and materialname == "<None>"))
      {
	return true;
      }
  }
  return false;
}

const std::string &MaterialFilter::classname() const {
  static const std::string name("MaterialFilter");
  return name;
}

bool HomogeneityFilter::acceptable(const CSkeletonSelectable *selectable,
				   const CSkeletonBase *skeleton)
  const
{
  double homog = selectable->homogeneity(skeleton->getMicrostructure());
  // The allowed range is open at the upper end and closed at the
  // lower.  This makes it easy to select all of the inhomogeneous
  // elements, for example.
  return homog >= min && homog < max;
}

const std::string &HomogeneityFilter::classname() const {
  static const std::string name("HomogeneityFilter");
  return name;
}

bool ShapeEnergyFilter::acceptable(const CSkeletonSelectable *selectable,
				   const CSkeletonBase *skeleton)
  const
{
  // If any of the elements that use the given selectable have an
  // acceptable shape energy, then the selectable should be drawn.
  ConstCSkeletonElementVector els;
  selectable->getElements(skeleton, els);
  for(ConstCSkeletonElementVector::iterator i=els.begin(); i<els.end(); ++i) {
    double shapeE = (*i)->energyShape();
    if(shapeE >= min && shapeE <=max) {
      return true;
    }
  }
  return false;
}

const std::string &ShapeEnergyFilter::classname() const {
  static const std::string name("ShapeEnergyFilter");
  return name;
}

bool ElementQualityFilter::acceptable(const CSkeletonSelectable *selectable,
				   const CSkeletonBase *skeleton)
  const
{
  // If any of the elements that use the given selectable have an
  // acceptable E, then the selectable should be drawn.
  ConstCSkeletonElementVector els;
  selectable->getElements(skeleton, els);
  const CMicrostructure *ms = skeleton->getMicrostructure();
  for(ConstCSkeletonElementVector::iterator i=els.begin(); i<els.end(); ++i) {
    double e = (*i)->energyTotal(ms, alpha);
    if(e >= min && e <= max) {
      return true;
    }
  }
  return false;
}

const std::string &ElementQualityFilter::classname() const {
  static const std::string name("ElementQualityFilter");
  return name;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool IntersectionFilter::acceptable(const CSkeletonSelectable *selectable,
				    const CSkeletonBase *skeleton)
  const
{
  return (a->acceptable(selectable, skeleton) &&
	  b->acceptable(selectable, skeleton));
}

void IntersectionFilter::setSource(vtkSmartPointer<GridSource> src) {
  a->setSource(src);
  b->setSource(src);
}

const std::string &IntersectionFilter::classname() const {
  static const std::string name("IntersectionFilter");
  return name;
}

//=\\=//

bool UnionFilter::acceptable(const CSkeletonSelectable *selectable,
			     const CSkeletonBase *skeleton)
  const
{
  return (a->acceptable(selectable, skeleton) ||
	  b->acceptable(selectable, skeleton));
}

void UnionFilter::setSource(vtkSmartPointer<GridSource> src) {
  a->setSource(src);
  b->setSource(src);
}

const std::string &UnionFilter::classname() const {
  static const std::string name("UnionFilter");
  return name;
}

//=\\=//

bool XorFilter::acceptable(const CSkeletonSelectable *selectable,
			   const CSkeletonBase *skeleton)
  const
{
  bool aok = a->acceptable(selectable, skeleton);
  bool bok = b->acceptable(selectable, skeleton);
  return (aok && !bok) || (bok && !aok);
}

void XorFilter::setSource(vtkSmartPointer<GridSource> src) {
  a->setSource(src);
  b->setSource(src);
}

const std::string &XorFilter::classname() const {
  static const std::string name("XorFilter");
  return name;
}

//=\\=//

bool NotFilter::acceptable(const CSkeletonSelectable *selectable,
			   const CSkeletonBase *skeleton)
  const
{
  return !a->acceptable(selectable, skeleton); 
}

void NotFilter::setSource(vtkSmartPointer<GridSource> src) {
  a->setSource(src);
}

const std::string &NotFilter::classname() const {
  static const std::string name("NotFilter");
  return name;
}


