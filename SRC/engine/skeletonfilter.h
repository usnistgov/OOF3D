// -*- C++ -*-
// $RCSfile: skeletonfilter.h,v $
// $Revision: 1.1.2.16 $
// $Author: langer $
// $Date: 2014/11/25 22:08:31 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SKELETONFILTER_H
#define SKELETONFILTER_H

#include <oofconfig.h>
#include "common/lock.h"
#include "common/pythonexportable.h"

#include <string>
#include <map>
#include <vector>
#include <vtkType.h>

class CSkeletonBase;
class CSkeletonSelectable;
class GridSource;

class SkeletonFilter : public PythonExportable<SkeletonFilter> {
private:
  std::map<vtkIdType, int> cellIndexMap;
  static std::vector<SkeletonFilter*> all_;
  static SLock lock;
protected:
  vtkSmartPointer<GridSource> gridsource;
public:
  SkeletonFilter();
  virtual ~SkeletonFilter();
  virtual const std::string &modulename() const;
  virtual void precompute(const CSkeletonBase*) {}
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*) 
    const = 0;
  virtual void postcompute() {}
  virtual void mapCellIndex(vtkIdType id, int index);
  virtual int getCellIndex(vtkIdType id) const;
  virtual void resetMap() { cellIndexMap.clear(); }
  virtual void setSource(vtkSmartPointer<GridSource>);
  void setModified();
  friend std::vector<SkeletonFilter*> *getSkeletonFilters();
};

std::vector<SkeletonFilter*> *getSkeletonFilters();

class NullFilter: public SkeletonFilter {
public:
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const {
    return true;
  }
  // The NullFilter doesn't need a map.
  virtual const std::string &classname() const;
  virtual void mapCellIndex(vtkIdType, int) {}
  virtual int getCellIndex(vtkIdType id) const { return id; }
  virtual void resetMap() {}
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class IntersectionFilter: public SkeletonFilter {
private:
  SkeletonFilter *a, *b;
public:
  IntersectionFilter(SkeletonFilter *a, SkeletonFilter *b)
    : a(a), b(b)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
  virtual void precompute(const CSkeletonBase *skel) {
    a->precompute(skel); b->precompute(skel);
  }
  virtual void postcompute() { a->postcompute(); b->postcompute(); }
  virtual void setSource(vtkSmartPointer<GridSource>);
};

class UnionFilter: public SkeletonFilter {
private:
  SkeletonFilter *a, *b;
public:
  UnionFilter(SkeletonFilter *a, SkeletonFilter *b)
    : a(a), b(b)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
  virtual void precompute(const CSkeletonBase *skel) { 
    a->precompute(skel); b->precompute(skel); 
  }
  virtual void postcompute() { a->postcompute(); b->postcompute(); }
  virtual void setSource(vtkSmartPointer<GridSource>);
};

class XorFilter: public SkeletonFilter {
private:
  SkeletonFilter *a, *b;
public:
  XorFilter(SkeletonFilter *a, SkeletonFilter *b)
    : a(a), b(b)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
  virtual void precompute(const CSkeletonBase *skel) {
    a->precompute(skel); b->precompute(skel); 
  }
  virtual void postcompute() { a->postcompute(); b->postcompute(); }
  virtual void setSource(vtkSmartPointer<GridSource>);
};

class NotFilter: public SkeletonFilter {
private:
  SkeletonFilter *a;
public:
  NotFilter(SkeletonFilter *a)
    : a(a)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*) 
    const;
  virtual void precompute(const CSkeletonBase *skel) { a->precompute(skel); }
  virtual void postcompute() { a->postcompute(); }
  virtual void setSource(vtkSmartPointer<GridSource>);
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

//TODO 3.1: This is more complicated than i thought. We need to think
//it through. What it even means to filter a skeleton by Segments or
//by Nodes since we would likely prefere to not have floating
//segments, nodes for many reasons. Another note is that we need to
//check the display and try to find if there are already some tags per
//kind of selectable to display or is it only for element displays
//only.

// class NodeGroupFilter : public SkeletonFilter {
// private:
//   const std::string nodegroup;
// public:
//   NodeGroupFilter(const std::string &name)
//   :nodegroup(name)
//   {}
//   virtual bool acceptable(const CSkeletonSelectable* selectable, const CSkeletonBase* base)
//     const;
// };
// 
// class SegmentGroupFilter : public SkeletonFilter {
// private:
//   const std::string segmentgroup;
// public:
//   SegmentGroupFilter(const std::string &name)
//   :segmentgroup(name)
//   {}
//   virtual bool acceptable(const CSkeletonSelectable* selectable, const CSkeletonBase* base)
//     const;
// };

class ElementGroupFilter : public SkeletonFilter {
private:
  const std::string elementgroup;
public:
  ElementGroupFilter(const std::string &name)
  :elementgroup(name)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
};

class SelectedElementFilter : public SkeletonFilter {
public:
  SelectedElementFilter() {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
};

class MaterialFilter: public SkeletonFilter {
 private:
  const std::string materialname;
 public:
  MaterialFilter(const std::string &name)
    : materialname(name)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
};

class HomogeneityFilter : public SkeletonFilter {
private:
  const double min, max;
public:
  HomogeneityFilter(double min, double max)
    : min(min), max(max)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
};

class ShapeEnergyFilter : public SkeletonFilter {
private:
  const double min, max;
public:
  ShapeEnergyFilter(double min, double max)
    : min(min), max(max)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
};

class ElementQualityFilter : public SkeletonFilter {
private:
  const double alpha;
  const double min, max;
public:
  ElementQualityFilter(double alpha, double min, double max)
    : alpha(alpha), min(min), max(max)
  {}
  virtual const std::string &classname() const;
  virtual bool acceptable(const CSkeletonSelectable*, const CSkeletonBase*)
    const;
};

// TODO 3.1: Add volume of interest filters: spheres, cubes, plus whatever
// is convenient given existing vtk filters. 


#endif // SKELETONFILTER_H
