// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#ifndef LARGESTRAINOUTPUT_H
#define LARGESTRAINOUTPUT_H

class Element;
class FEMesh;
class MasterPosition;
class SymmMatrix;
class SymmMatrix3;

#include "engine/IO/propertyoutput.h"

class POInitLargeStrain : public SymmMatrix3PropertyOutputInit {
public:
  virtual OutputVal *operator()(const PropertyOutput*,
				const FEMesh*,
				const Element*,
				const MasterCoord&) const;
};

extern "C" {
  // Arguments of dsyev:
  // jobz, character, 'V' means eigenvectors as well as eigenvalues.
  // uplo, character, 'U' means upper triangle is stored.
  // n, integer, order of A.
  // a, double*, A matrix stored as described by uplo. If evs
  //     are requested, then on output, they are in here.
  // lda, integer, leading dimension of A.
  // w, double, eigenvalues in ascending order.
  // work, double, array of size lwork.
  // lwork, > 3*N-1.
  // info, output, 0 = success.
  void dsyev_(char *jobz, char *uplo, int *n, double *A,
	      int *lda, double *w, double *work, int *lwork, int *info);
};


#endif // LARGESTRAINOUTPUT_H
