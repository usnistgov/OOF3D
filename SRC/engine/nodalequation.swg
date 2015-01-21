// -*- C++ -*-
// $RCSfile: nodalequation.swg,v $
// $Revision: 1.10.6.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:35 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef NODALEQUATION_SWG
#define NODALEQUATION_SWG

%module nodalequation
%include "engine/typemaps.swg"

%{
#include "engine/nodalequation.h"
%}

class NodalEquation {
public:
  int ndq_index();
};

#endif // NODALEQUATION_SWG
