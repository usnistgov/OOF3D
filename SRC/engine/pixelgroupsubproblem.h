// -*- C++ -*-
// $RCSfile: pixelgroupsubproblem.h,v $
// $Revision: 1.7.10.1 $
// $Author: langer $
// $Date: 2013/08/23 21:45:51 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PXLGROUPSUBPROBLEM_H
#define PXLGROUPSUBPROBLEM_H

#include "engine/predicatesubproblem.h"
#include <string>

class PixelGroup;

class PixelGroupSubProblemPredicate {
private:
  const std::string groupname;
  mutable PixelGroup *pixelgroup;
public:
  PixelGroupSubProblemPredicate(const std::string&);
  bool operator()(const FEMesh*, const Element *element) const;
  friend std::ostream &operator<<(std::ostream&,
				  const PixelGroupSubProblemPredicate&);
};

class CPixelGroupSubProblem:
  public PredicateSubProblem<PixelGroupSubProblemPredicate> {
public:
  CPixelGroupSubProblem(const std::string &groupname);
  virtual ~CPixelGroupSubProblem();
};
#endif // PXLGROUPSUBPROBLEM_H
