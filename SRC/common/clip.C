// -*- C++ -*-
// $RCSfile: clip.C,v $
// $Revision: 1.1.2.9 $
// $Author: langer $
// $Date: 2013/07/19 20:24:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/clip.h"
#include "common/IO/oofcerr.h"

ClippingPlane::ClippingPlane()
  : normal_(new CUnitVectorDirection(1.0, 0, 0.0)),
    offset_(0),
    enabled_(false),
    flipped_(false)
{}

ClippingPlane::ClippingPlane(CDirection *nrml, double offset)
  : normal_(nrml->clone()),
    offset_(offset),
    enabled_(true),
    flipped_(false)
{}

ClippingPlane::ClippingPlane(const ClippingPlane &other)
  : normal_(other.normal()->clone()),
    offset_(other.offset()),
    enabled_(other.enabled_),
    flipped_(other.flipped_)
{}

const ClippingPlane& ClippingPlane::operator=(const ClippingPlane &other) {
  if(this != &other) {
    normal_ = other.normal()->clone();
    offset_ = other.offset_;
    enabled_ = other.enabled_;
    flipped_ = other.flipped_;
  }
  return *this;
}

bool ClippingPlane::operator==(const ClippingPlane &other) const {
  return (offset_ == other.offset_ && *normal_ == *other.normal_ &&
	  enabled_ == other.enabled_ && flipped_ == other.flipped_);
}

ClippingPlane::~ClippingPlane() {
  delete normal_;
}

bool ClippingPlane::operator!=(const ClippingPlane &other) const {
  return !(*this == other);
}

bool ClippingPlane::operator<(const ClippingPlane &other) const {
  // This is required because a std::set of ClippingPlanes is used in
  // GhostOOFCanvas::set_view.
  if(enabled() && !other.enabled())
    return true;
  if(!enabled() && other.enabled())
    return false;
  if(flipped() && !other.flipped())
    return true;
  if(!flipped() && other.flipped())
    return false;
  return (offset() < other.offset() || 
	  (offset() == other.offset() && *normal() < *other.normal()));
}

std::ostream &operator<<(std::ostream &os, const ClippingPlane &cp) {
  os << "ClippingPlane(normal="<< *cp.normal() << ", offset="
     << cp.offset() << ", enabled=" << cp.enabled() << ")";
  return os;
}
