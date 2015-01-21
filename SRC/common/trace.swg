// -*- C++ -*-
// $RCSfile: trace.swg,v $
// $Revision: 1.6.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef TRACE_SWG
#define TRACE_SWG
%include "common/typemaps.swg"

%{
#include "common/trace.h"
%}

%inline void trace_enable() {
  Trace_t::enable();
}

%inline void trace_disable() {
  Trace_t::disable();
}

#endif // TRACE_SWG
