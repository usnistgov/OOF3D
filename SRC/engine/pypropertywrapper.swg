// -*- C++ -*-
// $RCSfile: pypropertywrapper.swg,v $
// $Revision: 1.30.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:43 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PYPROPERTYWRAPPER_SWG
#define PYPROPERTYWRAPPER_SWG

%module pypropertywrapper

%include "engine/typemaps.swg"
%pragma(python) include="pypropertywrapper.spy"
%{
#include "engine/pypropertywrapper.h"
%}

%extern "engine/properties.swg"
%pragma(python) code="from ooflib.SWIG.engine.properties import FluxPropertyPtr"
%pragma(python) code="from ooflib.SWIG.engine.properties import EqnPropertyPtr"

%extern "engine/element.swg"
%pragma(python) code="from ooflib.SWIG.engine.element import ElementDataPtr"

// Not much has to be done here.  The Python functions which are
// called from the C++ side are defined in pypropertywrapper.spy.
// Authors of extensions should derive new classes from PyFluxProperty
// and/or PyEqnProperty.  The derived classes can define the same
// methods, with the same arguments, as the corresponding C++ classes,
// FluxProperty and EqnProperty.  Almost all methods definitions are
// optional, except for integration_order and constant_in_space, which
// are required.  The default C++ base class method will be used if no
// Python method has been provided.

class PyFluxProperty : public FluxProperty {
public:
  PyFluxProperty(PyObject*, PyObject*, char *name);
  ~PyFluxProperty();
};

class PyEqnProperty : public EqnProperty {
public:
  PyEqnProperty(PyObject*, PyObject*, char *name);
  ~PyEqnProperty();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Since PyProperties are spoken to/about from Python, they have
// a simple generic ElementData class with one PyObject* for data.

class PyPropertyElementData : public ElementData {
public:
  PyPropertyElementData(char *name, PyObject *dat);
  // ~PyPropertyElementData();
  PyObject *data();
};

#endif // PYPROPERTYWRAPPER_SWG
