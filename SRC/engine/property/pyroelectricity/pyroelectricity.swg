// -*- C++ -*-
// $RCSfile: pyroelectricity.swg,v $
// $Revision: 1.3.18.3 $
// $Author: langer $
// $Date: 2013/11/08 20:46:02 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef PYROELECTRICITY_SWG
#define PYROELECTRICITY_SWG

%module pyroelectricity

%{
#include "engine/property/pyroelectricity/pyroelectricity.h"
%}

%include "engine/typemaps.swg"
%include "engine/propertyhdr.swg"



class PyroElectricity : public Property {
public:
  PyroElectricity(PyObject *reg, char *name,
		  double px, double py, double pz, double t0,
		  std::string *enum2string);
};

%pragma(python) include="pyroelectricity.spy"

#endif	// PYROELECTRICITY_SWG
