// -*- C++ -*-
// $RCSfile: identification.h,v $
// $Revision: 1.6.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:51 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef IDENTIFICATION_H
#define IDENTIFICATION_H

// Base class for objects that carry an "objectid()" by which they're
// identified.  By deriving all such objects from a common base class,
// we guarantee that the index will never be duplicated.

class IdentifiedObject {
private:
  static int mastercounter;
protected:
  const int id_;
public:
  IdentifiedObject()
    : id_(mastercounter++)
  {}
  virtual ~IdentifiedObject() {}
  int objectid() const { return id_; }
};

bool operator==(const IdentifiedObject&, const IdentifiedObject&);

// When IdentifiedObjects are used as keys in STL maps and sets, they
// can use this comparator:

struct ltidobject {
  bool operator()(const IdentifiedObject *obj1, const IdentifiedObject *obj2)
    const
  {
    return obj1->objectid() < obj2->objectid();
  }
};

#endif
