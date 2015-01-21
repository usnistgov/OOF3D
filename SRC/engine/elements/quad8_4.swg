// -*- C++ -*-
// $RCSfile: quad8_4.swg,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:27 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef QUAD84_SWIG
#define QUAD84_SWIG

%module quad8_4
%include "engine/typemaps.swg"
%{
  extern void quad8_4init();
%}
void quad8_4init();

%pragma(python) include="quad8_4.spy"

#endif // QUAD8_SWIG
