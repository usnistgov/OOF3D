// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/cmicrostructure.h"
#include "engine/homogeneity.h"

HomogeneityData::HomogeneityData(double hom, int cat)
  : homogeneity(hom),
    dominantpixel(cat),
    homog_energy(1.0-hom)
{}

HomogeneityData::HomogeneityData()
  : homogeneity(0),
    dominantpixel(UNKNOWN_CATEGORY),
    homog_energy(0)
{}
