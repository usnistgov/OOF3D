// -*- C++ -*-
// $RCSfile: symeig3.h,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// Eigenvalues and eigenvectors of a symmetric 3x3 matrix

#ifndef SYMEIG_H
#define SYMEIG_H

class EigenValues;

template <class MATRIX, class EIGENVECTOR>
void eigensystem(const MATRIX &mat,
		 EIGENVECTOR &eig1, EIGENVECTOR &eig2, EIGENVECTOR &eig3);

template <class MATRIX>
void getEigenvalues(const MATRIX &mat, EigenValues &eig);

#include "symeig3.C"

#endif // SYMEIG_H
