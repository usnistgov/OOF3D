// -*- C++ -*-
// $RCSfile: rubberband.h,v $
// $Revision: 1.19.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef RUBBERBAND_H
#define RUBBERBAND_H

#include <oofconfig.h>

#include "common/coord.h"
#include <gdk/gdk.h>
#include <libgnomecanvas/libgnomecanvas.h>
#include <gtk/gtk.h>
#include <vector>
#include <iostream>

class OOFCanvas;
class GfxBrushStyle;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class RubberBand {
private:
  void clear();
  bool active_;
protected:
  Coord startpt;
  Coord current;
  GnomeCanvasItem *rubberband;
  GdkBitmap *stipple, *stubble;
  // "draw" is protected so that it can only be called from redraw,
  // and not from outside.  This ensures that the data it uses is up-to-date.
  virtual GnomeCanvasItem *draw(GtkWidget *canvas) = 0;
public:
  RubberBand();
  virtual ~RubberBand();
  virtual void start(const Coord&);
  virtual void redraw(GtkWidget *canvas, const Coord &where);
                                 // undraw, change current pt, redraw
  virtual void stop();
  bool active() const { return active_; }
  virtual void print(std::ostream &os) const = 0; // for debugging
};

std::ostream &operator<<(std::ostream&, const RubberBand&);


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class NoRubberBand : public RubberBand {
protected:
  virtual GnomeCanvasItem *draw(GtkWidget*) { return 0; }
public:
  NoRubberBand() {}
  virtual void start(const Coord&) {}
  virtual void redraw(GtkWidget*, const Coord&) {}
  virtual void print(std::ostream &os) const; // for debugging
};

class RectangleRubberBand : public RubberBand {
private:
  GnomeCanvasPoints *pts;
protected:
  virtual GnomeCanvasItem *draw(GtkWidget *canvas);
public:
  RectangleRubberBand();
  virtual ~RectangleRubberBand();
  virtual void start(const Coord&);
  virtual void print(std::ostream &os) const; // for debugging
};

class CircleRubberBand : public RubberBand {
private:
  GnomeCanvasPoints *pts;
protected:
  virtual GnomeCanvasItem *draw(GtkWidget *canvas);
public:
  CircleRubberBand();
  virtual ~CircleRubberBand();
  virtual void start(const Coord&);
  virtual void print(std::ostream &os) const; // for debugging
};

class EllipseRubberBand : public RubberBand {
protected:
  virtual GnomeCanvasItem *draw(GtkWidget *canvas);
public:
  virtual void print(std::ostream &os) const; // for debugging
};

class SpiderRubberBand : public RubberBand {
private:
  std::vector<GnomeCanvasPoints*> segments;
protected:
  virtual GnomeCanvasItem *draw(GtkWidget *canvas);
public:
  SpiderRubberBand(const std::vector<Coord>*);
  virtual ~SpiderRubberBand();
  virtual void print(std::ostream &os) const; // for debugging
};

class BrushRubberBand : public RubberBand {
private:
  GfxBrushStyle *style;
  GnomeCanvasPoints *trail;
  int npts;
  void cleanup();
protected:
  virtual GnomeCanvasItem *draw(GtkWidget *canvas);
public:
  BrushRubberBand(GfxBrushStyle*);
  virtual void start(const Coord&);
  virtual void stop();
  virtual void print(std::ostream &os) const; // for debugging
};

class LineRubberBand : public RubberBand {
private:
  GnomeCanvasPoints *segment;
protected:
  virtual GnomeCanvasItem *draw(GtkWidget *canvas);
public:
  LineRubberBand();
  virtual ~LineRubberBand();
  virtual void start(const Coord&);
  virtual void print(std::ostream &os) const; // for information
};
  
#endif // RUBBERBAND_H
