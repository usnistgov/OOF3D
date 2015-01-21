// -*- C++ -*-
// $RCSfile: oofcanvas.h,v $
// $Revision: 1.59.18.3 $
// $Author: langer $
// $Date: 2014/10/17 21:48:04 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


// TODO: There is apparently some kind of bug in the canvas
// code, which results in the appearance of some "garbage" (random)
// screen pixels in the image layer, which however only appear in GUI
// testing.  This is likely to be a drawing/timing issue, and might go
// away with future revisions of the canvas.  To reproduce the
// anomaly, just run the 00015_tutorial_skeleton test, and watch for
// the junk at the bottom of the image when the graphics window comes
// up.  Experiments with a truncated version of the test show that
// zooming out and then in is sufficient to make the junk pixels go
// away.  Also, they don't appear on the Mac, and they don't appear in
// anti-aliased mode, which suggests that the junk is not corrupted
// image data.

#include <oofconfig.h>

#ifndef OOFCANVAS_H
#define OOFCANVAS_H

class OOFCanvas;
class OOFCanvasLayer;

#include "common/coord.h"
#include "common/IO/GUI/rubberband.h"
#include <gtk/gtk.h>
#include <libgnomecanvas/libgnomecanvas.h>
#include <vector>

class AbstractImage;
class CRectangle;

class OOFCanvas {
private:
  static bool initialized;
  bool isnew;
  bool empty;
  bool mousedown;
  Coord last_mouse;
  Coord mousedown_point;
  double affineflip[6];
  PyObject *mouse_callback;
  PyObject *config_callback;
  guint mouse_handler_id, config_handler_id;
  RubberBand *rubberband;
  OOFCanvasLayer *underlayer;
  RubberBand *make_rubberband(const Coord&);
protected:
  GtkWidget *canvas;
  double pixels_per_unit;	// zoom factor
  GnomeCanvasGroup *root;
  std::vector<OOFCanvasLayer*> layers;
  OOFCanvasLayer *current_layer;
  guint lineWidth;
  guint32 lineColor, fillColor; // , bgColor;
  double margin;
public:
  OOFCanvas(bool antialias);
  ~OOFCanvas();
  PyObject *widget();
  PyObject *rootitem();

  bool is_empty() const { return empty; }

  // Zoom routines.
  double get_pixels_per_unit() const { return pixels_per_unit; }
  void set_pixels_per_unit(double);
  void zoom(double);		// scale by the given factor
  void zoomAbout(double, const Coord*); // ... while keeping a point fixed
  void underlay();		// recompute the background rectangle

  PyObject *get_hadjustment() const;
  PyObject *get_vadjustment() const;
  ICoord get_allocation() const;

  // Size of canvas in pixels
  int get_width_in_pixels() const;
  int get_height_in_pixels() const;

  // This calls the GnomeCanvas's "set_scroll_region", which restricts
  // the allowed scrolling area to the passed-in rectangle.  It has
  // the side-effect of repositioning the offsets so that as much of
  // the passed-in rectangle as possible is visible.  It has no effect
  // on what portion of the canvas is drawable.
  void set_scrollregion(const CRectangle&);
  CRectangle get_scrollregion() const;
  // These functions set and return the current scroll position.
  ICoord get_scroll_offsets() const;
  void set_scroll_offsets(const ICoord*);

  // Utility functions for canvas coordinate transformations.
  Coord world_coord(int, int) const; // convert window to world coordinates
  Coord world_coord(const Coord&) const;
  Coord window_coord(const Coord *Point) const;	// and back

  // The limits of what's actually been drawn so far.
  CRectangle get_bounds() const;

  OOFCanvasLayer *newLayer();
  void deleteLayer(OOFCanvasLayer*);

  void clear();
  void show();

  void set_lineWidth(unsigned int);
  void set_lineColor(guint32*);
  void set_fillColor(guint32*, unsigned char);
  void set_underlay_params(const std::vector<gushort>*, double);
  void set_bgColor_local(const std::vector<gushort>*);
  void set_bgColor(const std::vector<gushort>*);
  void set_margin(double f);
  void set_margin_local(double f);

  void draw_dot(const Coord *dot);
  void draw_triangle(const Coord *triangle, double angle);
  void draw_segment(const GnomeCanvasPoints *segment);
  void draw_segments(const std::vector<GnomeCanvasPoints*>*);
  void draw_curve(const GnomeCanvasPoints *curve);
  void draw_polygon(const GnomeCanvasPoints *polygon);
  void fill_polygon(const GnomeCanvasPoints *polygon);
  void draw_circle(const Coord&, double);
  void fill_circle(const Coord&, double);
  void draw_image(const AbstractImage*, const Coord*, const Coord*);
  void draw_alpha_image(const AbstractImage*, const Coord*, const Coord*);
												//unsigned char);

  void set_rubberband(RubberBand*);

  // Separate callbacks for mouse events and resize events.
  void set_mouse_callback(PyObject*);
  void set_configure_callback(PyObject *);

  // Callback functions
  static void gtk_destroy(GtkWidget*, gpointer);
  void destroy();
  static gint mouse_event(GnomeCanvasItem*, GdkEvent*, gpointer);
  void mouse_eventCB(GnomeCanvasItem*, GdkEvent*);
  static gint configure_event(GnomeCanvas*, GtkAllocation*, gpointer);
  void configure_eventCB(GtkAllocation*);

  friend class OOFCanvasLayer;
  friend class RubberBand;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class OOFCanvasLayer {
protected:
  GnomeCanvasItem *grp, *subgrp;
  OOFCanvas *canvas;
public:
  OOFCanvasLayer(OOFCanvas*);
  ~OOFCanvasLayer();
  GnomeCanvasGroup *group() const;
  void raise_layer(int);
  void raise_to_top();
  void lower_layer(int);
  void show();
  void hide();
  void move(double, double);
  void clear();
  void make_current();
  void destroy();
};

#endif
