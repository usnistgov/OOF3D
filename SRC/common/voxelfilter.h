// -*- C++ -*-
// $RCSfile: voxelfilter.h,v $
// $Revision: 1.1.2.5 $
// $Author: langer $
// $Date: 2014/12/14 22:49:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef VOXELFILTER_H
#define VOXELFILTER_H

#include <oofconfig.h>
#include "common/lock.h"
#include "common/coord_i.h"
#include "common/pythonexportable.h"

#include <string>
#include <vector>

class CMicrostructure;
class OOFCanvasLayerBase;
class PixelGroup;


// Conditionals used to include voxels in an ImageCanvasLayer display,
// via the vtk-like oofExcludeVoxels filter.

class VoxelFilter : public PythonExportable<VoxelFilter> {
private:
  static std::vector<VoxelFilter*> all_;
  static SLock lock;
protected:
  const CMicrostructure *microstructure;
  OOFCanvasLayerBase *canvaslayer;
public:
  VoxelFilter();
  virtual ~VoxelFilter();
  virtual const std::string &modulename() const;
  virtual bool includeVoxel(const ICoord&) const = 0;
  virtual bool precompute() { return true; }
  virtual void postcompute() {}	
  // Redefine trivial in subclasses that don't actually exclude anything.
  virtual bool trivial() const { return false; }
  virtual void setMicrostructure(const CMicrostructure*);
  virtual void setCanvasLayer(OOFCanvasLayerBase*);
  void setModified();
  friend std::vector<VoxelFilter*> *getVoxelFilters();
};

std::vector<VoxelFilter*> *getVoxelFilters();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class AllVoxels : public VoxelFilter {
public:
  virtual const std::string &classname() const;
  virtual bool includeVoxel(const ICoord&) const { return true; }
  virtual bool trivial() const { return true; }
};

class ActiveVoxels : public VoxelFilter {
public:
  virtual const std::string &classname() const;
  virtual bool includeVoxel(const ICoord&) const;
};

class SelectedVoxels : public VoxelFilter {
public:
  virtual const std::string &classname() const;
  virtual bool includeVoxel(const ICoord&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class BinaryVoxelFilter : public VoxelFilter {
protected:
  VoxelFilter *a, *b;
public:
  BinaryVoxelFilter(VoxelFilter*, VoxelFilter*);
  virtual bool precompute();
  virtual void postcompute();
  virtual void setMicrostructure(const CMicrostructure*);
  virtual void setCanvasLayer(OOFCanvasLayerBase*);
};

class VoxelIntersection : public BinaryVoxelFilter {
public:
  VoxelIntersection(VoxelFilter *a, VoxelFilter *b)
    : BinaryVoxelFilter(a, b)
  {}
  virtual const std::string &classname() const;
  virtual bool includeVoxel(const ICoord&) const;
};

class VoxelUnion : public BinaryVoxelFilter {
public:
  VoxelUnion(VoxelFilter *a, VoxelFilter *b)
    : BinaryVoxelFilter(a, b)
  {}
  virtual const std::string &classname() const;
  virtual bool includeVoxel(const ICoord&) const;
};

class VoxelXor : public BinaryVoxelFilter {
public:
  VoxelXor(VoxelFilter *a, VoxelFilter *b) 
    : BinaryVoxelFilter(a, b)
  {}
  virtual const std::string &classname() const;
  virtual bool includeVoxel(const ICoord&) const;
};

class VoxelNot : public VoxelFilter {
private:
  VoxelFilter *a;
public:
  VoxelNot(VoxelFilter*);
  virtual const std::string &classname() const;
  virtual bool includeVoxel(const ICoord&) const;
  virtual bool precompute();
  virtual void postcompute();
  virtual void setMicrostructure(const CMicrostructure*);
  virtual void setCanvasLayer(OOFCanvasLayerBase*);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class VoxelGroupFilter : public VoxelFilter {
private:
  const std::string groupName;
  PixelGroup *group;
public:
  VoxelGroupFilter(const std::string&);
  virtual const std::string &classname() const;
  virtual bool includeVoxel(const ICoord&) const;
  virtual bool precompute();
};



#endif	// VOXELFILTER_H
