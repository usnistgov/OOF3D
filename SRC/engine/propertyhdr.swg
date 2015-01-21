// -*- C++ -*-
// $RCSfile: propertyhdr.swg,v $
// $Revision: 1.7.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:42 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PROPERTYHDR_SWG
#define PROPERTYHDR_SWG
%include "engine/typemaps.swg"

// This file should be %include'd in all .swg files for properties
// derived directly from the Property base class.

// If we didn't have a complicated directory and module/package
// structure, we could simply use '%import "engine/properties.swg"'
// here.  But that inserts the line "from properties import *" in the
// swig-generated .py files in the property subdirectories, which is
// not what we want.  For one thing, it imports too much.  For
// another, it doesn't get the correct path to the properties.py file.
// So we use the less powerful '%extern' construction, and explicitly
// add the code to import the name we need for the Property base
// class.

%pragma(python) code="from ooflib.SWIG.engine.properties import PropertyPtr"
%extern "engine/properties.swg"

#endif // PROPERTYHDR_SWG
