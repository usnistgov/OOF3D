// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

%module simpletension2

%{
#include "engine/property/interfaces/surfacetension/simpletension2/simpletension2.h"
%}
%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"

class SimpleTension2 : public Property
{
public:
  SimpleTension2(PyObject *self, char *, double, double, double, double);
};

%pragma(python) include="simpletension2.spy"
