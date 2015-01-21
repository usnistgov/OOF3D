// -*- C++ -*-
// $RCSfile: clip.h,v $
// $Revision: 1.1.2.5 $
// $Author: langer $
// $Date: 2012/12/05 20:31:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CLIP_H
#define CLIP_H

#include <oofconfig.h>

#include "common/direction.h"
#include <vector>

class ClippingPlane {
private:
  CDirection *normal_;
  double offset_;
  bool enabled_;
  bool flipped_;
public:
  ClippingPlane();
  ClippingPlane(CDirection *nrml, double offset);
  ClippingPlane(const ClippingPlane&);
  const ClippingPlane &operator=(const ClippingPlane&);
  bool operator==(const ClippingPlane&) const;
  bool operator!=(const ClippingPlane&) const;
  bool operator<(const ClippingPlane&) const;
  ~ClippingPlane();
  const CDirection *normal() const { return normal_; }
  CDirection *normal() { return normal_; }
  double offset() const { return offset_; }
  bool enabled() const { return enabled_; }
  void enable() { enabled_ = true; }
  void disable() { enabled_ = false; }
  bool flipped() const { return flipped_; }
  void flip() { flipped_ = true; }
  void unflip() { flipped_ = false; }
};

std::ostream &operator<<(std::ostream&, const ClippingPlane&);

typedef std::vector<ClippingPlane> ClippingPlaneList;

#endif // CLIP_H
