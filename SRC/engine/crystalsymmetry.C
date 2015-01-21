// -*- C++ -*-
// $RCSfile: crystalsymmetry.C,v $
// $Revision: 1.3.4.3 $
// $Author: langer $
// $Date: 2014/07/08 15:35:22 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "engine/crystalsymmetry.h"
#include "common/smallmatrix.h"
#include <map>
#include <math.h>

typedef std::map<AnisoCrystalSymmetry, RotationSet*> SymDict;

class SymmetryDict {
public:
  SymmetryDict();
  SymDict symdict;
};

static SymmetryDict symmetries;

const RotationSet *getEquivalentRotations(AnisoCrystalSymmetry sym) {
  return symmetries.symdict[sym];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

RotationSet::RotationSet(AnisoCrystalSymmetry sym) {
  SmallMatrix *ident = new SmallMatrix(3);
  (*ident)(0,0) = 1.0;
  (*ident)(1,1) = 1.0;
  (*ident)(2,2) = 1.0;
  matrices.push_back(ident);
  symmetries.symdict[sym] = this;
}

RotationSet::~RotationSet() {
  for(unsigned int i=0; i<matrices.size(); i++)
    delete matrices[i];
}

void RotationSet::add(double r00, double r01, double r02,
		      double r10, double r11, double r12,
		      double r20, double r21, double r22)
{
  SmallMatrix *mat = new SmallMatrix(3);
  (*mat)(0,0) = r00;
  (*mat)(0,1) = r01;
  (*mat)(0,2) = r02;
  (*mat)(1,0) = r10;
  (*mat)(1,1) = r11;
  (*mat)(1,2) = r12;
  (*mat)(2,0) = r20;
  (*mat)(2,1) = r21;
  (*mat)(2,2) = r22;
  matrices.push_back(mat);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SymmetryDict::SymmetryDict() {

  double halfroot3 = 0.5*sqrt(3.0);

  // Matrix elements are copied from Tony Rollett's symmetry.c file.
  // Numbers in comments correspond to numbers in comments in that
  // file.  The identity matrix is added automatically by the
  // RotationSet constructor.

  // ISOTROPIC is not included because all orientations are
  // equivalent.

  RotationSet *rots = new RotationSet(TETRAGONAL);
  rots->add(-1, 0, 0, 0, 1, 0, 0, 0, -1);  // 2
  rots->add(1, 0, 0, 0, -1, 0, 0, 0, -1);  // 3
  rots->add(-1, 0, 0, 0, -1, 0, 0, 0, 1);  // 4
  rots->add(0, 1, 0, -1, 0, 0, 0, 0, 1);	  // 5
  rots->add(0, -1, 0, 1, 0, 0, 0, 0, 1);	  // 6
  rots->add(0, 1, 0, 1, 0, 0, 0, 0, -1);	  // 7
  rots->add(0, -1, 0, -1, 0, 0, 0, 0, -1); // 8

  rots = new RotationSet(HEXAGONAL);
  rots->add(-0.5, halfroot3, 0, -halfroot3, -0.5, 0, 0, 0, 1);  // 2
  rots->add(-0.5, -halfroot3, 0, halfroot3, -0.5, 0, 0, 0, 1);  // 3
  rots->add(0.5, halfroot3, 0, -halfroot3, 0.5, 0, 0, 0, 1);    // 4
  rots->add(-1, 0, 0, 0, -1, 0, 0, 0, 1);		       // 5
  rots->add(0.5, -halfroot3, 0, halfroot3, 0.5, 0, 0, 0, 1);    // 6
  rots->add(-0.5, -halfroot3, 0, -halfroot3, 0.5, 0, 0, 0, -1); // 7
  rots->add(1, 0, 0, 0, -1, 0, 0, 0, -1);		       // 8
  rots->add(-0.5, halfroot3, 0, halfroot3, 0.5, 0, 0, 0, -1);   // 9
  rots->add(0.5, halfroot3, 0, halfroot3, -0.5, 0, 0, 0, -1);   // 10
  rots->add(-1, 0, 0, 0, 1, 0, 0, 0,  -1);		       // 11
  rots->add(0.5, -halfroot3, 0, -halfroot3, -0.5, 0, 0, 0, -1); // 12

  rots = new RotationSet(CUBIC);
  rots->add(0, 0, 1, 1, 0, 0, 0, 1, 0);	  // c 2
  rots->add(0, 1, 0, 0, 0, 1, 1, 0, 0);	  // c 3
  rots->add(0, -1, 0, 0, 0, 1, -1, 0, 0);  // c 4
  rots->add(0, -1, 0, 0, 0, -1, 1, 0, 0);  // c 5
  rots->add(0, 1, 0, 0, 0, -1, -1, 0, 0);  // c 6
  rots->add(0, 0, -1, 1, 0, 0, 0, -1, 0);  // c 7
  rots->add(0, 0, -1, -1, 0, 0, 0, 1, 0);  // c 8
  rots->add(0, 0, 1, -1, 0, 0, 0, -1, 0);  // c 9
  rots->add(-1, 0, 0, 0, 1, 0, 0, 0, -1);  // c 10
  rots->add(-1, 0, 0, 0, -1, 0, 0, 0, 1);  // c 11
  rots->add(1, 0, 0, 0, -1, 0, 0, 0, -1);  // c 12
  rots->add(0, 0, -1, 0, -1, 0, -1, 0, 0); // c 13
  rots->add(0, 0, 1, 0, -1, 0, 1, 0, 0);	  // c 14
  rots->add(0, 0, 1, 0, 1, 0, -1, 0, 0);	  // c 15
  rots->add(0, 0, -1, 0, 1, 0, 1, 0, 0);	  // c 16
  rots->add(-1, 0, 0, 0, 0, -1, 0, -1, 0); // c 17
  rots->add(1, 0, 0, 0, 0, -1, 0, 1, 0);	  // c 18
  rots->add(1, 0, 0, 0, 0, 1, 0, -1, 0);	  // c 19
  rots->add(-1, 0, 0, 0, 0, 1, 0, 1, 0);	  // c 20
  rots->add(0, -1, 0, -1, 0, 0, 0, 0, -1); // c 21
  rots->add(0, 1, 0, -1, 0, 0, 0, 0, 1);	  // c 22
  rots->add(0, 1, 0, 1, 0, 0, 0, 0, -1);	  // c 23
  rots->add(0, -1, 0, 1, 0, 0, 0, 0, 1);	  // c 24

  rots = new RotationSet(TRIGONAL);
  rots->add(-0.5, halfroot3, 0, -halfroot3, -0.5, 0, 0, 0, 1);	// 2
  rots->add(-0.5, -halfroot3, 0, halfroot3, -0.5, 0, 0, 0, 1);	// 3
  rots->add(0.5, halfroot3, 0, halfroot3, -0.5, 0, 0, 0, -1);	// 4
  rots->add(-1, 0, 0, 0, 1, 0, 0, 0, -1);			// 5
  rots->add(0.5, -halfroot3, 0, -halfroot3, -0.5, 0, 0, 0, -1); // 6

  rots = new RotationSet(ORTHORHOMBIC);
  rots->add(-1, 0, 0, 0, 1, 0, 0, 0, -1); // c 2
  rots->add(-1, 0, 0, 0, -1, 0, 0, 0, 1); // c 3
  rots->add(1, 0, 0, 0, -1, 0, 0, 0, -1); // c 4

  // Triclinic has no equivalent orientations.
  rots = new RotationSet(TRICLINIC);

  // Same for monoclinic?
  rots = new RotationSet(MONOCLINIC);


};

