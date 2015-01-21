// -*- C++ -*-
// $RCSfile: quad8.swg,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:25 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef QUAD8_SWIG
#define QUAD8_SWIG

%module quad8
%include "engine/typemaps.swg"
%{
  extern void quad8init();
%}
void quad8init();

%pragma(python) include="quad8.spy"

#endif // QUAD8_SWIG
