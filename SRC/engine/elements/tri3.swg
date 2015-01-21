// -*- C++ -*-
// $RCSfile: tri3.swg,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:29 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef TRI3_SWIG
#define TRI3_SWIG

%module tri3
%include "engine/typemaps.swg"
%{
  extern void tri3init();
%}
void tri3init();

%pragma(python) include="tri3.spy"

#endif // TRI3_SWIG
