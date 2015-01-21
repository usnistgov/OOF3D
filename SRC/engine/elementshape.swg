// -*- C++ -*-
// $RCSfile: elementshape.swg,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2014/01/23 20:54:32 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ELEMENTSHAPE_SWG
#define ELEMENTSHAPE_SWG

%include "engine/typemaps.swg"
%pragma(python) include="engine/elementshape.spy"

%{
#include "engine/elementshape.h"
%}

class ElementShape {
public:
  int dimension();
  int nedges();
  int nfaces();
  const string &name();
};

class LinearElementShape : public ElementShape {};

class TriangularElementShape : public ElementShape {};

class QuadrilateralElementShape : public ElementShape {};

class TetrahedralElementShape : public ElementShape {};

void initializeShapes();

StringVec *shapeNames();
ElementShape *getShape(char*);

#endif // ELEMENTSHAPE_SWG
