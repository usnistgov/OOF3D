// -*- C++ -*-
// $RCSfile: elementshape.C,v $
// $Revision: 1.1.2.4 $
// $Author: fyc $
// $Date: 2014/02/18 16:38:15 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/oofcerr.h"
#include "engine/elementshape.h"
#include "engine/ooferror.h"
#include <algorithm>
#include <map>
#include <vector>
#include <algorithm>

typedef std::map<const std::string, ElementShape*> ElementShapeMap;

static ElementShapeMap &shapes() {
  static ElementShapeMap _shapes;
  return _shapes;
}

static std::vector<std::string> &names() {
  static std::vector<std::string> _names;
  return _names;
}

static bool sorted = true;


ElementShape::ElementShape(const std::string &name)
  : name_(name)
{
  // Check that this shape hasn't already been created.
  ElementShapeMap::const_iterator i = shapes().find(name_);
  if(i != shapes().end()) {
    // Because this is called during startup, the error handling
    // machinery may not be in place, and a direct message is helpful.
    oofcerr << "ElementShape::ctor: attempting to redefine shape "
	    << name_ << std::endl;
    throw ErrProgrammingError("Shape " + name_ + " has already been created.",
			      __FILE__, __LINE__);
  }
  shapes()[name_] = this;
  names().push_back(name_);
  sorted = false;
}

const std::string &ElementShape::modulename() const {
  static std::string nm = "ooflib.SWIG.engine.elementshape";
  return nm;
}

// The names given to the shapes here are the ones that will appear in
// the GUI for the element categories.

LinearElementShape::LinearElementShape()
  : ElementShape("Line")
{}

const std::string &LinearElementShape::classname() const {
  static const std::string name("LinearElementShape");
  return name;
}

TriangularElementShape::TriangularElementShape()
  : ElementShape("Triangle")
{}

const std::string &TriangularElementShape::classname() const {
  static const std::string name("TriangularElementShape");
  return name;
}

QuadrilateralElementShape::QuadrilateralElementShape()
  : ElementShape("Quadrilateral")
{}

const std::string &QuadrilateralElementShape::classname() const {
  static const std::string name("QuadrilateralElementShape");
  return name;
}

#if DIM == 3
TetrahedralElementShape::TetrahedralElementShape()
  : ElementShape("Tetrahedron")
{}

const std::string &TetrahedralElementShape::classname() const {
  static const std::string name("TetrahedralElementShape");
  return name;
}
#endif // DIM == 3


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static bool initialized = false;

void initializeShapes() {
  // This should only be called once.
  if(initialized)
    return;
  new LinearElementShape();
  new TriangularElementShape();
  new QuadrilateralElementShape();
#if DIM == 3
  new TetrahedralElementShape();
#endif // DIM == 3
  initialized = true;
}

class ShapeSorter {
public:
  bool operator()(const std::string &one, const std::string &two) const {
    const ElementShape *thing1 = getShape(one);
    const ElementShape *thing2 = getShape(two);
    // Return true if one is less than two.
    // Larger dimension comes first.
    if(thing1->dimension() > thing2->dimension()) return true;
    if(thing1->dimension() < thing2->dimension()) return false;
    // More corners first.
    if(thing1->ncorners() > thing2->ncorners()) return true;
    if(thing1->ncorners() < thing2->ncorners()) return false;
    // This is actually enough...
    return false;
  }
};

// shapeNames() returns the names of the shapes in a logical order for
// organizing them in the GUI.

std::vector<std::string> *shapeNames() {
  if(!sorted) {
    ShapeSorter sorter;
    std::sort(names().begin(), names().end(), sorter);
    sorted = true;
  }
  return &names();
}

// Get the singleton instance of the given shape.
ElementShape *getShape(const std::string &name) {
  initializeShapes();
  ElementShapeMap::const_iterator i = shapes().find(name);
  if(i == shapes().end()) {
    throw ErrProgrammingError("No such shape: " + name, __FILE__, __LINE__);
  }
  return (*i).second;
}

