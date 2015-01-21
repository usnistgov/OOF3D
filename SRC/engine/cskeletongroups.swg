// -*- C++ -*-
// $RCSfile: cskeletongroups.swg,v $
// $Revision: 1.1.2.6 $
// $Author: langer $
// $Date: 2013/05/16 18:57:32 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONGROUPS_SWG
#define CSKELETONGROUPS_SWG

%module cskeletongroups

%include "engine/typemaps.swg"
%{
#include <oofconfig.h>
#include "common/tostring.h"
#include "engine/cskeletongroups.h"
%}

%pragma(python) include="engine/cskeletongroups.spy"

class CGroupTrackerBase {
public:
  CSkeletonSelectableSet* get_group(char*);
};

class CGroupTracker : public CGroupTrackerBase { 
public:
  CGroupTracker() {};
  void add_group(char*);
  void clear_group(char*);
  void remove_group(char*);
  void rename_group(char*, char*);
  void add(char*, CSkeletonSelectable*);
  void remove(char*, CSkeletonSelectable*);
  int get_group_size(char*);
  CGroupTracker* sheriff();
  %addmethods {
    %new string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

class CDeputyGroupTracker : public CGroupTrackerBase {
public:
  CDeputyGroupTracker(CGroupTrackerBase*);
};

#endif




