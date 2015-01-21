// -*- C++ -*-
// $RCSfile: pixelgroupsubproblem.C,v $
// $Revision: 1.6.10.2 $
// $Author: langer $
// $Date: 2014/12/14 01:07:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/cmicrostructure.h"
#include "common/pixelgroup.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/pixelgroupsubproblem.h"
#include <iostream>

CPixelGroupSubProblem::CPixelGroupSubProblem(const std::string &groupname)
  : PredicateSubProblem<PixelGroupSubProblemPredicate>
    (PixelGroupSubProblemPredicate(groupname))
{
//   std::cerr << "** Creating CPixelGroupSubProblem " << groupname << " " << this
// 	    << std::endl;
}

CPixelGroupSubProblem::~CPixelGroupSubProblem() {
//   std::cerr << "** Destroying CPixelGroupSubProblem ** " << this << std::endl;
}

PixelGroupSubProblemPredicate::PixelGroupSubProblemPredicate(
			const std::string &groupname)
  : groupname(groupname),
    pixelgroup(0)
{}

bool PixelGroupSubProblemPredicate::operator()(const FEMesh *mesh,
					       const Element *element) const
{
  const CMicrostructure *microstructure = mesh->get_microstructure();
  if(pixelgroup == 0) {
    pixelgroup = microstructure->findGroup(groupname);
  }
  int dompxl = element->get_skeleton_element()->dominantPixel(microstructure);
  // Are pixels in category dompxl in the given pixelgroup?
  return pixelGroupQueryCategory(*microstructure, dompxl, pixelgroup);
}

std::ostream &operator<<(std::ostream &os,
			 const PixelGroupSubProblemPredicate &p)
{
  return os << "PixelGroupSubProblemPredicate('" << p.groupname << "')";
}
