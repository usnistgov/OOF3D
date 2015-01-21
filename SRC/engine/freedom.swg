// -*- C++ -*-
// $RCSfile: freedom.swg,v $
// $Revision: 1.10.6.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:25 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef FREEDOM_SWG
#define FREEDOM_SWG

%include "engine/typemaps.swg"
%extern "engine/femesh.swg"

%{
#include "engine/freedom.h"
%}

class DegreeOfFreedom {
public:
  double value(FEMesh*);
  int dofindex();

  %addmethods {
    void increment(FEMesh *mesh, double x) {
      self->value(mesh) += x;
    }
  }
};

#endif // FREEDOM_SWG
