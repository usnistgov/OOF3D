// -*- C++ -*-
// $RCSfile: pixelselectioncouriere.h,v $
// $Revision: 1.5.18.6 $
// $Author: langer $
// $Date: 2014/12/14 22:49:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PIXELSELECTIONCOURIERE_H
#define PIXELSELECTIONCOURIERE_H

#include "common/coord.h"
#include "common/pixelselectioncourier.h"
#include "common/array.h"
#include <vector>

class CMicrostructure;
class CSkeletonElement;
class Material;

// ElementSelection
class ElementSelection : public PixelSelectionCourier {
private:
  // Commented out because the compiler complains about unused private
  // variables.  When this class is completed, this will be
  // uncommented.
  // const CSkeletonElement *element;
  const std::vector<ICoord> *selected;
  std::vector<ICoord>::const_iterator sel_iter;
public:
  ElementSelection(CMicrostructure *ms,
		   const CSkeletonElement *element);
  virtual ~ElementSelection();
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};    

// SegmentSelection
class SegmentSelection : public PixelSelectionCourier {
private:
  const Coord n0, n1;
  const std::vector<ICoord> *selected;
  std::vector<ICoord>::const_iterator sel_iter;
public:
  SegmentSelection(CMicrostructure *ms,
		   const Coord *n0, const Coord *n1);
  virtual ~SegmentSelection();
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

class MaterialSelectionBase : public PixelSelectionCourier {
private:
  Array<PixelAttributeVector*>::const_iterator iter;
  Array<PixelAttributeVector*>::const_iterator iterend;
public:
  MaterialSelectionBase(CMicrostructure*);
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream&) const = 0;
  virtual bool ok(const Material*) const = 0;
};

class MaterialSelection : public MaterialSelectionBase {
private:
  const Material *material;
public:
  MaterialSelection(CMicrostructure*, const Material*);
  virtual bool ok(const Material*) const;
  virtual void print(std::ostream&) const;
};

class AnyMaterialSelection : public MaterialSelectionBase  {
public:
  AnyMaterialSelection(CMicrostructure*);
  virtual bool ok(const Material*) const;
  virtual void print(std::ostream&) const;
};

class NoMaterialSelection : public MaterialSelectionBase {
public:
  NoMaterialSelection(CMicrostructure*);
  virtual bool ok(const Material*) const;
  virtual void print(std::ostream&) const;
};

#endif // PIXELSELECTIONCOURIERE_H
