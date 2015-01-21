// -*- C++ -*-
// $RCSfile: materialset.h,v $
// $Revision: 1.2.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:44:30 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef MATERIALSET_H
#define MATERIALSET_H

class Material;

#include <set>

struct MaterialCompare {
  bool operator()(const Material *m1, const Material *m2) const;
};

typedef std::set<const Material*, MaterialCompare> MaterialSet;

#endif // MATERIALSET_H
