// -*- C++ -*-
// $RCSfile: shapefunctioncache.h,v $
// $Revision: 1.4.18.2 $
// $Author: langer $
// $Date: 2014/01/05 03:20:04 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Store the values of the derivatives of a shapefunction and the
// determinant of the jacobian at gauss points. This differs from the
// precomputed values stored in the ShapeFunctionTable class, because
// those values only depend on the master element geometry. These
// values depend on the real space geometry.  We don't want to
// precompute and store the shapefunctions for each element
// individually, because that would take too much memory. But we don't
// want to recompute shape functions when computing all the different
// Properties of a single element.

#ifndef SHAPEFUNCTIONCACHE_H
#define SHAPEFUNCTIONCACHE_H

class ElementBase;
class GaussPoint;
#include "engine/indextypes.h"

#include <vector>

class ShapeFunctionCache {
private:
  ShapeFunctionCache(int, int);
  ~ShapeFunctionCache();
  
  // has a value been stored?    
  bool query_dsf(const ElementBase*, ShapeFunctionIndex, SpaceIndex,
		 const GaussPoint&, double&) const;
  bool query_jac(const ElementBase*, const GaussPoint&, double&) const;
  
  // store a value
  void store_dsf(const ElementBase*, ShapeFunctionIndex, SpaceIndex,
		 const GaussPoint&, double);
  void store_jac(const ElementBase*, const GaussPoint&, double);
  
  class SFCValue {
  public:
    SFCValue() : computed(0), value(-1234) {}
    bool computed;		// has this been computed already?
    double value;		// its value, if it's been computed.
  };
  std::vector<SFCValue> *det_jac; // determinant of jacobian at gauss points
  std::vector<std::vector<std::vector<SFCValue> > > *df; // derivs at gauss pts
  void reset(const ElementBase*);
  bool current(const ElementBase*) const;
  const ElementBase *cached_element; // element for which this was last computed

  friend class ShapeFunction;
};

#endif
