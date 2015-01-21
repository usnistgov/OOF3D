// -*- C++ -*-
// $RCSfile: fixillegal.swg,v $
// $Revision: 1.1.2.4 $
// $Author: langer $
// $Date: 2014/12/14 01:07:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CFIXILLEGAL_SWG
#define CFIXILLEGAL_SWG

%module fixillegal

%include "common/typemaps.swg"
%extern "engine/cskeletonmodifier.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/fixillegal.h"
#include "engine/cskeletonmodifier.h"
#include "engine/cskeleton2.h"
#include "engine/homogeneity.h"
%}

%pragma(python) include="engine/fixillegal.spy"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkeletonModifierPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeleton2 import CSkeletonBasePtr"

class FixIllegal : public CSkeletonModifier {
public:
  FixIllegal();
  int getNGuilty();
  int getNDone();
};


#endif



