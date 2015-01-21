// -*- C++ -*-
// $RCSfile: crystalsymmetry.swg,v $
// $Revision: 1.2.4.3 $
// $Author: langer $
// $Date: 2014/06/27 20:30:33 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CRYSTALSYMMETRY_SWG
#define CRYSTALSYMMETRY_SWG

%module crystalsymmetry

%pragma(python) include="engine/crystalsymmetry.spy"
%{
#include "engine/crystalsymmetry.h"
%}


// $source is a Python AnisoCrystalSymmetry instance.
// AnisoCrystalSymmetry is an Enum subclass defined in
// crystalsymmetry.spy.

%typemap(python, in) AnisoCrystalSymmetry* (AnisoCrystalSymmetry sym) {
  // typemap(python, in) AnisoCrystalSymmetry*
  std::string name = PyString_AsString(
	       PyObject_CallMethod($source, (char *) "string", NULL));
  if(name == "Tetragonal")
    sym = TETRAGONAL;
  if(name == "Hexagonal")
    sym = HEXAGONAL;
  if(name == "Cubic")
    sym = CUBIC;
  if(name == "Trigonal")
    sym = TRIGONAL;
  if(name == "Orthorhombic")
    sym = ORTHORHOMBIC;
  if(name == "Monoclinic")
    sym = MONOCLINIC;
  if(name == "Triclinic")
    sym = TRICLINIC;
  $target = &sym;
};

#endif // CRYSTALSYMMETRY_SWG
