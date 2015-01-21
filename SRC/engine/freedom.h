// -*- C++ -*-
// $RCSfile: freedom.h,v $
// $Revision: 1.12.6.2 $
// $Author: langer $
// $Date: 2013/11/08 20:44:25 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */


class DegreeOfFreedom;

#ifndef FREEDOM_H
#define FREEDOM_H

#include <iostream>

class FEMesh;

class DegreeOfFreedom {
private:
  DegreeOfFreedom(const DegreeOfFreedom&);
public:				// should be private, but swig complains
  DegreeOfFreedom(int);
  ~DegreeOfFreedom() {}
  friend class FEMesh;		// only a FEMesh can create or destroy a DoF
protected:
  int index_;
public:
  int dofindex() const { return index_;}
  double value(const FEMesh *mesh) const;
  double &value(FEMesh *mesh) const;
  void setValue(const FEMesh *mesh, double newValue);
};

struct DoFCompare {
  bool operator()(const DegreeOfFreedom *a, const DegreeOfFreedom *b) const {
    return a->dofindex() < b->dofindex();
  }
};

std::ostream &operator<<(std::ostream &os, const DegreeOfFreedom &dof);

#endif
