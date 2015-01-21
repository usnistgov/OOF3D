// -*- C++ -*-
// $RCSfile: pixelattribute_i.h,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2014/12/14 01:07:42 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This file contains forward declarations and typedefs from
// pixelattribute.h.  It can be included instead of that file in most
// situations, to reduce header file dependencies.

#ifndef PIXELATTRIBUTE_I_H
#define PIXELATTRIBUTE_I_H

#include <oofconfig.h>

#include <map>
#include <set>
#include <vector>

class PixelAttribute;
class PixelAttributeVector;
class PixelAttributeGlobalData;

// We want the AttributeVectorMap to always use the default (pointer)
// comparison function for speed.
typedef std::map<PixelAttributeVector*, PixelAttributeVector*>
AttributeVectorMap;

typedef std::set<PixelAttribute*, bool (*)(const PixelAttribute*,
					   const PixelAttribute*)> AttributeSet;
typedef bool (*LTAttributeVector)(const PixelAttributeVector*,
				  const PixelAttributeVector*);
typedef std::set<PixelAttributeVector*, LTAttributeVector> AttributeVectorSet;
typedef std::vector<PixelAttributeVector*> AttributeVectorVec;

typedef std::map<PixelAttributeVector*, unsigned int, LTAttributeVector>
AttributeVectorCategoryMap;


#endif // PIXELATTRIBUTE_I_H
