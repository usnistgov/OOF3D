// -*- C++ -*-
// $RCSfile: ilupre.h,v $
// $Revision: 1.2.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef ILUPRE_H
#define ILUPRE_H

#include <vector>
#include "engine/sparsemat.h"
#include "engine/preconditioner.h"

class ILUPreconditionerCore : public PreconditionerBase {
private:
  SparseMat UT, L;
public:
  ILUPreconditionerCore(const SparseMat &A);
  virtual ~ILUPreconditionerCore();
  virtual DoubleVec solve(const DoubleVec &x) const;
  virtual DoubleVec trans_solve(const DoubleVec &x) const;

  SparseMat unfactored() const;
  SparseMat lower() const { return L; }
  SparseMat upper() const { return UT.transpose(); }

  static const std::string classname_;
  virtual const std::string &classname() const { return classname_; }
  static const std::string modulename_;
  virtual const std::string &modulename() const { return modulename_; }
};


#endif
