// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef IDENTIFICATION_SWG
#define IDENTIFICATION_SWG

%module identification

%include "common/typemaps.swg"
%{
#include "common/identification.h"
%}

class IdentifiedObject {
public:
  IdentifiedObject();
  ~IdentifiedObject();
  int objectid();
};

#endif // IDENTIFICATION_SWG

