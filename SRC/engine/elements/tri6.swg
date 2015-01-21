// -*- C++ -*-
// $RCSfile: tri6.swg,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:30 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef TRI6_SWIG
#define TRI6_SWIG

%module tri6
%include "engine/typemaps.swg"
%{
  extern void tri6init();
%}
void tri6init();

%pragma(python) include="tri6.spy"

#endif // TRI6_SWIG
