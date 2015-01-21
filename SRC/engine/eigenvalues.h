// -*- C++ -*-
// $RCSfile: eigenvalues.h,v $
// $Revision: 1.4.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// simply a class used to store and sort three numbers...

#ifndef EIGENVALUES_H
#define EIGENVALUES_H

#include <iostream>

class EigenValues {
private:
  double max_, mid_, min_;
public:
  EigenValues(double e1, double e2, double e3);
  EigenValues() : max_(0.), mid_(0.), min_(0.) {}
  double max() const { return max_; }
  double mid() const { return mid_; }
  double min() const { return min_; }
  friend std::ostream &operator<<(std::ostream&, const EigenValues&);
};

#endif // EIGENVALUES_H
