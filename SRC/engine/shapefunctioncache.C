// -*- C++ -*-
// $RCSfile: shapefunctioncache.C,v $
// $Revision: 1.10.10.2 $
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

#include <oofconfig.h>
#include "gausspoint.h"
#include "shapefunctioncache.h"

#include <iostream>

ShapeFunctionCache::ShapeFunctionCache(int ngauss, int nsf)
  : det_jac(new std::vector<SFCValue>(ngauss)),
    df(new std::vector<std::vector<std::vector<SFCValue> > >
       (ngauss,
	std::vector<std::vector<SFCValue> >(nsf,
					     std::vector<SFCValue>(DIM)))),
    cached_element(0)
{}

ShapeFunctionCache::~ShapeFunctionCache() {
  delete det_jac;
  delete df;
}

// is the cache usable?
bool ShapeFunctionCache::current(const ElementBase *el) const {
  return cached_element == el;
}

void ShapeFunctionCache::reset(const ElementBase *el) {
  if(!current(el)) {
    for(std::vector<SFCValue>::size_type i=0; i<det_jac->size(); i++)
      (*det_jac)[i].computed = 0;
    // To be completely pedantic, the "unsigned int"s in the following
    // lines should all be "std::vector<something>::size_type", but
    // the "something" is a mess.  Since the pedanticism is simply to
    // suppress compiler warning messages, using "unsigned int" is
    // almost certainly safe.
    for(unsigned int i=0; i<df->size(); i++)
      for(unsigned int j=0; j<(*df)[i].size(); j++)
	for(unsigned int k=0; k<(*df)[i][j].size(); k++)
	  (*df)[i][j][k].computed = 0;
  }
  cached_element = el;
}

bool ShapeFunctionCache::query_dsf(const ElementBase *el, ShapeFunctionIndex i,
				   SpaceIndex j, const GaussPoint &g,
				   double &value) const
{
  if(!current(el)) return 0; // cached element is different
  SFCValue &v = (*df)[g.index()][i][j];
  
  if(v.computed) {
    value = v.value;
    return 1;
  }
  return 0;
}

bool ShapeFunctionCache::query_jac(const ElementBase *el, const GaussPoint &g,
				   double &value) const
{
  if(!current(el)) return 0;
  SFCValue &v = (*det_jac)[g.index()];
  if(v.computed) {
    value = v.value;
    return 1;
  }
  return 0;
}

void ShapeFunctionCache::store_dsf(const ElementBase *el, ShapeFunctionIndex i,
				   SpaceIndex j, const GaussPoint &g,
				   double value)
{
  reset(el);
  
  SFCValue &v = (*df)[g.index()][i][j];
  v.value = value;
  v.computed = 1;
}

void ShapeFunctionCache::store_jac(const ElementBase *el, const GaussPoint &g,
				   double value)
{
  reset(el);
  SFCValue &v = (*det_jac)[g.index()];
  v.value = value;
  v.computed = 1;
}

