// -*- C++ -*-
// $RCSfile: rubberband3d.h,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2012/03/22 21:08:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef RUBBERBAND3D_H
#define RUBBERBAND3D_H

#include <oofconfig.h>

#include "common/coord.h"
#include <iostream>
#include <vector>
#include <vtkActor.h>
#include <vtkDataSetMapper.h>
#include <vtkPoints.h>
#include <vtkPolyData.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>

class OOFCanvas3D;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class RubberBand {
private:
  void clear(vtkRenderer *renderer);
  bool active_;
protected:
  Coord startpt;
  Coord current;
  vtkSmartPointer<vtkActor> rubberband;
  vtkSmartPointer<vtkDataSetMapper> mapper;
  //GdkBitmap *stipple, *stubble;
  // "draw" is protected so that it can only be called from redraw,
  // and not from outside.  This ensures that the data it uses is up-to-date.
  virtual void draw() = 0;
public:
  RubberBand();
  virtual ~RubberBand() {}
  virtual void start(const Coord&);
  virtual void redraw(vtkRenderer *renderer, const Coord &where);
                                 // undraw, change current pt, redraw
  virtual void stop(vtkRenderer *renderer);
  bool active() const { return active_; }
  //virtual void print(std::ostream &os) const = 0; // for debugging
};

//std::ostream &operator<<(std::ostream&, const RubberBand&);


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class NoRubberBand : public RubberBand {
protected:
  virtual void draw() {};
public:
  NoRubberBand() {};
  virtual void start(const Coord&) {};
  virtual void redraw(vtkRenderer *renderer, const Coord&) {};
  //virtual void print(std::ostream &os) const; // for debugging
};


class SpiderRubberBand : public RubberBand {
private:
  vtkSmartPointer<vtkPoints> points;
  vtkSmartPointer<vtkPolyData> poly;
protected:
  virtual void draw();
public:
  SpiderRubberBand(const std::vector<Coord>*);
  virtual ~SpiderRubberBand();
  //virtual void print(std::ostream &os) const; // for debugging
};

  
#endif // RUBBERBAND_H
