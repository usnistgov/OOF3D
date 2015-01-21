// -*- C++ -*-
// $RCSfile: elementshape.h,v $
// $Revision: 1.1.2.2 $
// $Author: fyc $
// $Date: 2014/07/29 21:21:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ELEMENTSHAPE_H
#define ELEMENTSHAPE_H

// Classes describing the shapes of master elements.  The number of
// nodes is *not* part of the shape.  The name passed to the
// ElementShape constructor is the argument to be used in getShape(),
// which returns the singleton instance of each ElementShape subclass.
// The singletons are created by initialize(), which is called when
// the python module is imported.

#include <oofconfig.h>
#include "common/pythonexportable.h"
#include <vector>

class ElementShape : public PythonExportable<ElementShape> {
 private:
  const std::string name_;
 public:
  ElementShape(const std::string&);
  virtual ~ElementShape() {}
  const std::string &modulename() const;
  virtual const std::string &classname() const = 0;

  const std::string &name() const { return name_; }
  virtual int dimension() const = 0;
  virtual int nedges() const = 0;
  virtual int nfaces() const = 0;
  virtual int ncorners() const = 0;
};

class LinearElementShape : public ElementShape {
 public:
  LinearElementShape();
  const std::string &classname() const;
  virtual int dimension() const { return 1; }

  virtual int nedges() const { 
    // TODO MER: I'm not sure that this is correct...  In 2D, the linear
    // element is used as an interface and therefore should be treated
    // as two separate coincident edges.  In 3D, it's not used as an
    // interface, and should be a single edge.
#if DIM==2
    return 2;
#else
    return 1;
#endif
  }
  virtual int nfaces() const { return 0; }
  virtual int ncorners() const { return 2; }
};

class TriangularElementShape : public ElementShape {
 public:
  TriangularElementShape();
  const std::string &classname() const;
  virtual int dimension() const { return 2; }
  virtual int nedges() const { return 3; }
  virtual int nfaces() const { 
    // See comment in LinearElementShape::nedges().
#if DIM==2
    return 0;
#else
    return 2;
#endif
  }
  virtual int ncorners() const { return 3; }
};

class QuadrilateralElementShape : public ElementShape {
 public:
  QuadrilateralElementShape();
  const std::string &classname() const;
  virtual int dimension() const { return 2; }
  virtual int nedges() const { return 4; }
  virtual int nfaces() const {
    // See comment in LinearElementShape::nedges().
#if DIM==2
    return 0;
#else
    return 2;
#endif
  }
  virtual int ncorners() const { return 4; }
};

#if DIM == 3
class TetrahedralElementShape : public ElementShape {
 public:
  TetrahedralElementShape();
  const std::string &classname() const;
  virtual int dimension() const { return 3; }
  virtual int nedges() const { return 6; }
  virtual int nfaces() const { return 4; }
  virtual int ncorners() const { return 4; }
};
#endif // DIM == 3

ElementShape *getShape(const std::string&);
void initializeShapes();
std::vector<std::string> *shapeNames(); // *Not* a new vector!


#endif // ELEMENTSHAPE_H
