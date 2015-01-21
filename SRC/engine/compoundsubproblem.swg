// -*- C++ -*-
// $RCSfile: compoundsubproblem.swg,v $
// $Revision: 1.5.10.3 $
// $Author: fyc $
// $Date: 2014/04/18 20:00:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef COMPOUNDSUBPROBLEM_SWG
#define COMPOUNDSUBPROBLEM_SWG

%module compoundsubproblem

%include "engine/typemaps.swg"
%extern "engine/csubproblem.swg"
%pragma(python) include="engine/compoundsubproblem.spy"
%pragma(python) code="from ooflib.SWIG.engine.csubproblem import CSubProblemPtr"
%pragma(python) code="from ooflib.SWIG.common.lock import LockPtr"

%{
#include "engine/compoundsubproblem.h"
%}

class CIntersectionSubProblem: public CSubProblem {
public:
  bool consistency;
  CIntersectionSubProblem(CSubProblem*, CSubProblem*);
  ~CIntersectionSubProblem();
  // precomputeLock and precomputeRequired have to be listed here,
  // even though they're swigged in the base class, because swig seems
  // to have a bug.  If data members are swigged in multiple
  // subclasses, when the base class is in another file, then the
  // PyMethodDef list in the swig-generated C++ files lists the wrong
  // class for the set and get methods.
  Lock precomputeLock;
  bool precomputeRequired;
  
  void updateDependencyA(CSubProblem*);
  void updateDependencyB(CSubProblem*);
};

class CUnionSubProblem: public CSubProblem {
public:
  bool consistency;
  CUnionSubProblem(CSubProblem*, CSubProblem*);
  ~CUnionSubProblem();
  Lock precomputeLock;
  bool precomputeRequired;
  
  void updateDependencyA(CSubProblem*);
  void updateDependencyB(CSubProblem*);
};

class CXorSubProblem: public CSubProblem {
public:
  bool consistency;
  CXorSubProblem(CSubProblem*, CSubProblem*);
  ~CXorSubProblem();
  Lock precomputeLock;
  bool precomputeRequired;
  
  void updateDependencyA(CSubProblem*);
  void updateDependencyB(CSubProblem*);
};

class CComplementSubProblem: public CSubProblem {
public:
  bool consistency;
  CComplementSubProblem(CSubProblem*);
  ~CComplementSubProblem();
  Lock precomputeLock;
  bool precomputeRequired;
  
  void updateDependency(CSubProblem*);
  //void redefine(CSubProblem *comp);
};

#endif // COMPOUNDSUBPROBLEM_SWG
