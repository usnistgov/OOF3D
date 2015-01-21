// -*- C++ -*-
// $RCSfile: crationalizers.swg,v $
// $Revision: 1.1.4.5 $
// $Author: langer $
// $Date: 2011/10/21 21:11:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CRATIONALIZERS_SWG
#define CRATIONALIZERS_SWG

%module crefine

%include "engine/typemaps.swg"
%extern "engine/cskeletonmodifier.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/crationalizers.h"
#include "engine/cskeletonmodifier.h"
#include "engine/cskeleton2.h"
%}

%pragma(python) include="engine/crationalizers.spy"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkeletonModifierPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeleton2 import CSkeletonPtr"

class Rationalizer {
public:
  // Function pointers in swig are tricky and likely to change with
  // swig versions.  Since we only have two cases, we just add methods
  // which use the right function pointer from within C++, instead of
  // swigging the rationalize() method directly.
  %addmethods {
     void findAndRationalize(CSkeleton *skel, CSkelModTargets *targets,
			     CSkelModCriterion *criterion) 
     {
       self->rationalize(skel, targets, criterion, &Rationalizer::findAndFix);
     }

     void rationalizeAll(CSkeleton *skel, CSkelModTargets *targets,
			 CSkelModCriterion *criterion) 
     {
       self->rationalize(skel, targets, criterion, &Rationalizer::fixAll);
     }
   }
  // void findAndFix(CSkeleton*, CSkeletonElement*);
  // void fixAll(CSkeleton*, CSkeletonElement*);
  int get_num_rationalized();
};

class RemoveBadTetrahedra : public Rationalizer {
public:
  RemoveBadTetrahedra(double acute_angle, double obtuse_angle);
};

#endif
