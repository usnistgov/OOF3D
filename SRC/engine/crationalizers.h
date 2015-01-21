// -*- C++ -*-
// $RCSfile: crationalizers.h,v $
// $Revision: 1.1.4.12 $
// $Author: langer $
// $Date: 2014/12/14 01:07:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CRATIONALIZERS_H
#define CRATIONALIZERS_H

#include "engine/cskeletonmodifier.h"
#include "engine/cskeletonselectable_i.h"

// Subclasses of Rationalizer must have a function "findAndFix" which
// takes a skeleton and an element as arguments and returns a list of
// ProvisionalChanges objects indicating what can be done.
// ProvisionalChanges is defined in cskeleton2.h. (Skeleton.mergeNode()
// returns one.)  They must also have a "fixAll" function that does the
// same thing, but doesn't bother checking the elements first.

// When using AutomaticRationalization, the Rationalizers are called in
// the order of their Registrations.  Therefore the Rationalizers that
// need to be called last (eg RemoveBadTriangle) need to have large
// 'ordering's.

/******************************************************

                   RATIONALIZERS

*******************************************************/
class Rationalizer;
typedef ProvisionalChangesVector* (Rationalizer::*FixerFunction)(
					 CSkeleton*, CSkeletonElement*) const;

class Rationalizer {
private:
  int num_rationalized;
public:
  Rationalizer();
  virtual ~Rationalizer();
  void rationalize(CSkeleton *skel, CSkelModTargets *targets,
		   CSkelModCriterion *criterion, FixerFunction fixer);
  virtual ProvisionalChangesVector* findAndFix(CSkeleton*, CSkeletonElement*)
    const = 0;
  virtual ProvisionalChangesVector* fixAll(CSkeleton*, CSkeletonElement*)
    const = 0;
  int get_num_rationalized() const { return num_rationalized; }
};

class RemoveBadTetrahedra : public Rationalizer {
private:
  double acute;
  double obtuse;
  double small_solid;
  double large_solid;

  // These are cleared and recalculated for each element.  As class
  // members they don't have to be passed around.
  /// TODO 3.1: Don't do that.  It's not thread safe and it screws up
  /// constness, unless the objects are mutable.  Wrap the angles up
  /// in a struct and pass around a pointer to the struct.
  mutable std::vector< std::pair<short, short> > obtuse_angles;
  mutable std::vector< std::pair<short, short> > acute_angles;
  mutable std::vector<short> small_solid_angles;
  mutable std::vector<short> large_solid_angles;
  mutable std::vector<short> large_dihedral_angles;
  mutable std::vector<short> small_dihedral_angles;
  void findAngles(const CSkeletonElement*, bool) const;

public:
  RemoveBadTetrahedra(double acute_angle, double obtuse_angle);
  virtual ~RemoveBadTetrahedra() {}
  // TODO 3.1: The arguments to findAndFix() and fixAll() should
  // probably be const.
  virtual ProvisionalChangesVector* findAndFix(CSkeleton*, CSkeletonElement*)
    const;
  virtual ProvisionalChangesVector* fixAll(CSkeleton*, CSkeletonElement*) 
    const;
  ProvisionalChangesVector* fix(CSkeleton*, CSkeletonElement*) const;
};

#endif
