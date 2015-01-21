// -*- C++ -*-
// $RCSfile: crystalsymmetry.h,v $
// $Revision: 1.2.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:43:20 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CRYSTALSYMMETRY_H
#define CRYSTALSYMMETRY_H

#include <vector>

class SmallMatrix;

// Don't change this enum without also changing crystalsymmetry.spy.
enum AnisoCrystalSymmetry {
  TETRAGONAL,
  HEXAGONAL,
  CUBIC,
  TRIGONAL,
  ORTHORHOMBIC,
  MONOCLINIC,
  TRICLINIC
};

class RotationSet {
private:
  std::vector<const SmallMatrix*> matrices;
  RotationSet(const RotationSet*&); // prohibited
public:
  RotationSet(AnisoCrystalSymmetry);
  ~RotationSet();
  void add(double, double, double,
	   double, double, double,
	   double, double, double);
  const SmallMatrix *operator[](int i) const { return matrices[i]; }
  int size() const { return matrices.size(); }
};

const RotationSet *getEquivalentRotations(AnisoCrystalSymmetry);

#endif // CRYSTALSYMMETRY_H
