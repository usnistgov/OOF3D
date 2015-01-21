/// -*- C++ -*-
// $RCSfile: smalltensor.h,v $
// $Revision: 1.1.12.2 $
// $Author: langer $
// $Date: 2013/11/08 20:44:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */


#ifndef SMALLTENSOR_H
#define SMALLTENSOR_H


class SmallTensor3{
protected:
  double data[3][3][3];
public:
  double &operator()(int i, int j, int k){ return data[i][j][k]; };
  double operator()(int i, int j, int k) const { return data[i][j][k]; };
};


class SmallTensor4{
protected:
  double data[3][3][3][3];
public:
  double &operator()(int i, int j, int k, int l){ return data[i][j][k][l]; };
  double operator()(int i, int j, int k, int l) const { return data[i][j][k][l]; };
};

#endif
