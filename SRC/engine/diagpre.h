// -*- C++ -*-
// $RCSfile: diagpre.h,v $
// $Revision: 1.2.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:41 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>



#ifndef DIAGPRE_H
#define DIAGPRE_H

class SparseMat;
#include <vector>
#include "engine/preconditioner.h"

// DiagPreconditionerCore is the heart of the Jacobi preconditioner.
// Sorry about the confusion of names.

class DiagPreconditionerCore : public PreconditionerBase {

 private:
  DoubleVec diag_;

 public:
  DiagPreconditionerCore (const SparseMat &);
  virtual ~DiagPreconditionerCore (void) { };
  DoubleVec solve (const DoubleVec &x) const;
  DoubleVec trans_solve (const DoubleVec &x) const;
  
  const double &diag(int i) const { return diag_[i]; }
  double &diag(int i) { return diag_[i]; }

  static const std::string classname_;
  virtual const std::string &classname() const { return classname_; }
  static const std::string modulename_;
  virtual const std::string &modulename() const { return modulename_; }
};

#endif  // DIAGPRE_H
