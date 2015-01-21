// -*- C++ -*-
// $RCSfile: tri6_3.swg,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:31 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef TRI6_3_SWIG
#define TRI6_3_SWIG

%module tri6_3
%include "engine/typemaps.swg"
%{
  extern void tri6_3init();
%}
void tri6_3init();

%pragma(python) include="tri6_3.spy"

#endif // TRI6_3_SWIG
