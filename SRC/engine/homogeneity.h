// -*- C++ -*-
// $RCSfile: homogeneity.h,v $
// $Revision: 1.1.2.1 $
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

#ifndef HOMOGENEITY_H
#define HOMOGENEITY_H

#include <oofconfig.h>

#define UNKNOWN_CATEGORY -1

class HomogeneityData {
private:
  double homogeneity;
  int dominantpixel;
  double homog_energy;
  // // This is the "clone" constructor.
  // HomogeneityData(double hom, int cat, double nrg) 
  //   : homogeneity(hom), dominantpixel(cat), homog_energy(nrg)
  // {}
public:
  HomogeneityData(double hom, int cat)
    : homogeneity(hom), dominantpixel(cat), homog_energy(1.0-hom)
  {}
  HomogeneityData()
    : homogeneity(0), dominantpixel(UNKNOWN_CATEGORY), homog_energy(0)
  {}
  double get_homogeneity() const { return homogeneity; }
  int get_dominantpixel() const { return dominantpixel; }
  double get_energy() const { return homog_energy; }
  // HomogeneityData clone() const { 
  //   return HomogeneityData(*this);
  //   // return HomogeneityData(this->homogeneity, this->dominantpixel,
  //   // 			   this->homog_energy); 
  // }
};


#endif // HOMOGENEITY_H
