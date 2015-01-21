// -*- C++ -*-
// $RCSfile: oofcanvas.C,v $
// $Revision: 1.125.2.2 $
// $Author: langer $
// $Date: 2014/08/01 19:53:06 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// TODO MERGE: The stringimage files have been removed, but routines
// in this file still use StringImage.  StringImage won't be necessary
// when 2D uses vtk.

#include "common/IO/GUI/canvasdot.h"
#include "common/IO/GUI/canvastriangle.h"
#include "common/IO/GUI/oofcanvas.h"
#include "common/IO/GUI/rubberband.h"
#include "common/abstractimage.h"
#include "common/geometry.h"
#include "common/ooferror.h"
#include "common/pythonlock.h"
#include "common/tostring.h"
#include "common/trace.h"
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <iostream>
#include <pygobject.h>
#include <pygtk/pygtk.h>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool OOFCanvas::initialized = 0;

OOFCanvas::OOFCanvas(bool antialias)
  : isnew(true),
    empty(true),
    mousedown(false),
    mouse_callback(0),
    config_callback(0),
    mouse_handler_id(0),
    config_handler_id(0),
    rubberband(0),
    underlayer(0),
    pixels_per_unit(1.0),
    current_layer(0),
    lineWidth(0),
    lineColor(0),
    fillColor(0),
    margin(1.0)
{
  if(!OOFCanvas::initialized) {
    OOFCanvas::initialized = 1;
    PyGILState_STATE pystate = acquirePyLock();
    try {
      init_pygobject();
      init_pygtk();
    } 
    catch (...) {
      releasePyLock(pystate);
      throw;
    }
    releasePyLock(pystate);
  }

  if(antialias) {
    canvas = gnome_canvas_new_aa();
  }
  else {
    canvas = gnome_canvas_new();
  }

  // Don't get too many motion events.  If this is used, then only the
  // first of a series of motion events is returned, and it's
  // necessary to call gdk_window_get_pointer() to get subsequent
  // events.
//   gtk_widget_add_events(canvas, GDK_POINTER_MOTION_HINT_MASK);

  root = gnome_canvas_root(GNOME_CANVAS(canvas));

  g_signal_connect(canvas, "destroy",
		   G_CALLBACK(OOFCanvas::gtk_destroy),
		   this);

  // Flip the y axis.  The default GTK+ coordinate system has y=0 at
  // the top of the window, which bothers us.
  art_affine_scale(affineflip, 1.0, -1.0);
  gnome_canvas_item_affine_absolute(GNOME_CANVAS_ITEM(root), affineflip);

  // Create the underlayer.
  underlayer = new OOFCanvasLayer(this);

  clear();
  show();
}

PyObject *OOFCanvas::widget() { 
  PyObject *wdgt;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    wdgt = pygobject_new((GObject*) canvas);
  }
  catch (...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return wdgt;
}

PyObject *OOFCanvas::rootitem() {
  PyObject *rtitem;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    rtitem = pygobject_new((GObject*) root);
  }
  catch (...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return rtitem;
}


void OOFCanvas::set_underlay_params(const std::vector<gushort> *color,
				    double f) {
  set_margin_local(f);
  set_bgColor_local(color);
  underlay();
}

void OOFCanvas::set_bgColor(const std::vector<gushort> *color) {
  set_bgColor_local(color);
  underlay();
}

void OOFCanvas::set_margin(double f) {
  set_margin_local(f);
  underlay();
}

void OOFCanvas::set_bgColor_local(const std::vector<gushort> *color) {
  GtkStyle *style = gtk_style_copy(gtk_widget_get_style(canvas));
  GdkColor &bgcolor = style->bg[0];
  GdkColormap *colormap = gtk_widget_get_colormap(canvas);
  bgcolor.red = (*color)[0];
  bgcolor.green = (*color)[1];
  bgcolor.blue = (*color)[2];
  gdk_colormap_alloc_color(colormap, &style->bg[0], FALSE, TRUE);
  gtk_widget_set_style(canvas, style);
}

void OOFCanvas::set_margin_local(double f) {
  margin = f;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


OOFCanvas::~OOFCanvas() {
  // When destroying the canvas, first destroy the gtk part.  That
  // will eventually call OOFCanvas::destroy(), which does the real
  // work of destroying the C++ part.  Check for canvas!=0 so that
  // there's no infinite loop of destruction.
  if(canvas && GTK_IS_OBJECT(canvas) /*&& !GTK_OBJECT_DESTROYED(canvas)*/) {
    gtk_object_destroy(GTK_OBJECT(canvas));
  }
}

void OOFCanvas::gtk_destroy(GtkWidget*, gpointer data) {
  // This is a static function.  It's the gtk callback for the
  // "destroy" signal.
  OOFCanvas *oofcanvas = (OOFCanvas*)(data);
  oofcanvas->destroy();
  delete oofcanvas;
}

void OOFCanvas::destroy() {
  for(std::vector<OOFCanvasLayer*>::size_type i=0; i<layers.size(); i++)
    delete layers[i];
  delete underlayer;
  
  if(mouse_callback) {
    gtk_signal_disconnect(GTK_OBJECT(root), mouse_handler_id);
    PyGILState_STATE pystate = acquirePyLock();
    Py_XDECREF(mouse_callback);
    releasePyLock(pystate);
  }

  if(config_callback) {
    gtk_signal_disconnect(GTK_OBJECT(canvas), config_handler_id);
    PyGILState_STATE pystate = acquirePyLock();
    Py_XDECREF(config_callback);
    releasePyLock(pystate);
  }

  canvas = 0;
}

void OOFCanvas::show() {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  gtk_widget_show_all(canvas);
  underlay();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Dimensions of the window, in pixels.

int OOFCanvas::get_width_in_pixels() const {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  GtkAllocation &allocation = canvas->allocation;
  return allocation.width;
}

int OOFCanvas::get_height_in_pixels() const {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  GtkAllocation &allocation = canvas->allocation;
  return allocation.height;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Limits of everything that's been drawn, independent of the scroll region.

CRectangle OOFCanvas::get_bounds() const {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  double x1, x2, y1, y2;
  gnome_canvas_item_get_bounds(GNOME_CANVAS_ITEM(root), &x1, &y1, &x2, &y2);
  return CRectangle(Coord(x1, y1), Coord(x2, y2));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Scaling functions

void OOFCanvas::set_pixels_per_unit(double ppu) {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  pixels_per_unit = ppu;
  gnome_canvas_set_pixels_per_unit(GNOME_CANVAS(canvas), ppu);
}

void OOFCanvas::zoom(double zoomfactor) {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  pixels_per_unit *= zoomfactor;
  gnome_canvas_set_pixels_per_unit(GNOME_CANVAS(canvas), pixels_per_unit);
//   underlay();			// is this necessary?
}

PyObject *OOFCanvas::get_hadjustment() const {
  PyObject *obj;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    GtkAdjustment *adj = gtk_layout_get_hadjustment(GTK_LAYOUT(canvas));
    obj = pygobject_new((GObject*) adj);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return obj;
}

PyObject *OOFCanvas::get_vadjustment() const {
  PyObject *obj;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    GtkAdjustment *adj = gtk_layout_get_vadjustment(GTK_LAYOUT(canvas));
    obj = pygobject_new((GObject*) adj);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return obj;
}

ICoord OOFCanvas::get_allocation() const {
  return ICoord(canvas->allocation.width, canvas->allocation.height);
}

void OOFCanvas::zoomAbout(double zoomfactor, const Coord *focuspt) {
  // The given focuspt is in the physical coordinate system in which y
  // increases *up* the screen.  All internal canvas calculations are
  // done in the system in which y increases *down* the screen.
  // Convert focuspt to this system:
  Coord focus((*focuspt)(0), -(*focuspt)(1)); // world coordinates
  // window coordinates of focus point
  Coord focus_window = window_coord(&focus);
  ICoord oldscroll_offset = get_scroll_offsets();

  zoom(zoomfactor);

  ICoord newscroll_offset = get_scroll_offsets();
  // World coords of the point that's now where the focus used to be:
  Coord newfocus = world_coord(focus_window +
			       (newscroll_offset - oldscroll_offset));
  Coord world_delta = (newfocus - focus);
  Coord window_delta = world_delta*pixels_per_unit;

  GtkAdjustment *hadj = gtk_layout_get_hadjustment(GTK_LAYOUT(canvas));
  gdouble hpos = gtk_adjustment_get_value(hadj);
  gtk_adjustment_set_value(hadj, hpos - int(window_delta(0)));
  GtkAdjustment *vadj = gtk_layout_get_vadjustment(GTK_LAYOUT(canvas));
  gdouble vpos = gtk_adjustment_get_value(vadj);
  gtk_adjustment_set_value(vadj, vpos - int(window_delta(1)));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void OOFCanvas::set_scrollregion(const CRectangle &rect) {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
//   std::cerr << "Calling gnome_canvas_set_scroll_region" << std::endl;
  gnome_canvas_set_scroll_region(GNOME_CANVAS(canvas),
				 rect.xmin(), rect.ymin(),
				 rect.xmax(), rect.ymax());
//   std::cerr << "Back from gnome_canvas_set_scroll_region" << std::endl;
}

CRectangle OOFCanvas::get_scrollregion() const {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  double x1, y1, x2, y2;
  gnome_canvas_get_scroll_region(GNOME_CANVAS(canvas), &x1, &y1, &x2, &y2);
  return CRectangle(Coord(x1, y1), Coord(x2, y2));
}

void OOFCanvas::set_scroll_offsets(const ICoord *offset) {
  gnome_canvas_scroll_to(GNOME_CANVAS(canvas), (*offset)(0), (*offset)(1));
}

Coord OOFCanvas::world_coord(int cx, int cy) const {
  double x, y;
  gnome_canvas_window_to_world(GNOME_CANVAS(canvas), cx, cy, &x, &y);
  return Coord(x, y);
}

Coord OOFCanvas::world_coord(const Coord &c) const {
  double x, y;
  gnome_canvas_window_to_world(GNOME_CANVAS(canvas), c(0), c(1), &x, &y);
  return Coord(x, y);
}

Coord OOFCanvas::window_coord(const Coord *c) const {
  double wx, wy;
  gnome_canvas_world_to_window(GNOME_CANVAS(canvas),
			       (*c)(0), (*c)(1), &wx, &wy);
  return Coord(wx, wy);
}

ICoord OOFCanvas::get_scroll_offsets() const {
  int cx, cy;
  gnome_canvas_get_scroll_offsets(GNOME_CANVAS(canvas), &cx, &cy);
  return ICoord(cx, cy);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// "Underlay" function -- draws a rectangle in the background color
// which can catch mouse events outside the image.

void OOFCanvas::underlay() {
  // Remove the old underlay object.
  underlayer->clear();

  double x1, x2, y1, y2;
  // Get the bounds in the absence of the old underlayer.
  gnome_canvas_item_get_bounds(GNOME_CANVAS_ITEM(root), &x1, &y1, &x2, &y2);
  double xmargin = (x2-x1)*margin;
  double ymargin = (y2-y1)*margin;

  x1 -= xmargin; x2 += xmargin;
  y1 -= ymargin; y2 += ymargin;

  // Get the color.
  GtkStyle *style = gtk_style_copy(gtk_widget_get_style(canvas));
  GdkColor bgcolor = style->bg[0];

  // Draw yourself.
  GnomeCanvasItem *item = gnome_canvas_item_new(underlayer->group(),
 					    gnome_canvas_rect_get_type(),
 					    "x1", x1,
 					    "y1", y1,
 					    "x2", x2, 
 					    "y2", y2,
  					    "fill_color_gdk",  &bgcolor,
 					    NULL);
  // The bounds were computed in the coordinate system of the root's
  // *parent*, which hasn't had the affine transformation applied.  So
  // the bounds have to be flipped, because the underlayer is being
  // drawn in the root's transformed coordinate system.  Actually, we
  // should be applying the inverse of affineflip here, but
  // fortunately it's its own inverse.
  gnome_canvas_item_affine_absolute(item, affineflip);
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


void OOFCanvas::clear() {
  CRectangle scrollregion = get_scrollregion();
  for(std::vector<OOFCanvasLayer*>::iterator i=layers.begin(); i!=layers.end();
      ++i)
    {
      (*i)->destroy();
      delete *i;
    }
//   GnomeCanvasGroup *r = gnome_canvas_root(GNOME_CANVAS(canvas));
  layers.resize(0);
  (void) newLayer();		// a new blank slate, so to speak
  set_scrollregion(scrollregion);
  empty = true;
}

void OOFCanvas::deleteLayer(OOFCanvasLayer *layer) {
  layer->destroy();
  for(std::vector<OOFCanvasLayer*>::iterator i=layers.begin(); i!=layers.end(); 
      ++i)
    {
      if(*i == layer) {
	layers.erase(i);
	return;
      }
    }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void OOFCanvas::set_lineWidth(unsigned int w) {
  lineWidth = w;
}

void OOFCanvas::set_lineColor(guint32 *color) {
  lineColor = *color;
}

void OOFCanvas::set_fillColor(guint32 *color, unsigned char alpha) {
  // The color arg has had its alpha channel set to 255 by the guint32
  // *color typemap in oofcanvas.swg.  
  static guint32 transwhite = GNOME_CANVAS_COLOR_A(255, 255, 255, 0);
  static guint32 opaqueblack = GNOME_CANVAS_COLOR_A(0, 0, 0, 255);
  fillColor = (*color & transwhite) | ((int) alpha & opaqueblack);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

OOFCanvasLayer *OOFCanvas::newLayer() {
  OOFCanvasLayer *layer = new OOFCanvasLayer(this);
  layers.push_back(layer);
  current_layer = layer;
  return layer;
}

OOFCanvasLayer::OOFCanvasLayer(OOFCanvas *canvas)
  : canvas(canvas)
{
  // By defining two groups, one within the other, we can clear a
  // layer without changing its z-position in the canvas.  The outer
  // group (grp) maintains the position, while the inner group
  // (subgrp) can be destroyed and recreated.
  grp = gnome_canvas_item_new(canvas->root,
			    gnome_canvas_group_get_type(),
			    "x", 0.0,
			    "y", 0.0,
			    NULL);
  subgrp = gnome_canvas_item_new(GNOME_CANVAS_GROUP(grp),
			       gnome_canvas_group_get_type(),
			       "x", 0.0,
			       "y", 0.0,
			       NULL);
}

OOFCanvasLayer::~OOFCanvasLayer() {
  // The gtk object will be destroyed when the canvas is destroyed, or
  // when OOFCanvasLayer::destroy() is called.  There's really nothing
  // to do here.  Move along, now.
}

void OOFCanvasLayer::make_current() {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  canvas->current_layer = this;
}

void OOFCanvasLayer::clear() {
  // Destroy the subgroup and recreate an empty one.
  gtk_object_destroy(GTK_OBJECT(subgrp));
  subgrp = gnome_canvas_item_new(GNOME_CANVAS_GROUP(grp),
			       gnome_canvas_group_get_type(),
			       "x", 0.0,
			       "y", 0.0,
			       NULL);
}

void OOFCanvasLayer::destroy() {
  gtk_object_destroy(GTK_OBJECT(grp));
  grp = 0;
  subgrp = 0;
}

GnomeCanvasGroup *OOFCanvasLayer::group() const {
  return GNOME_CANVAS_GROUP(subgrp);
}

void OOFCanvasLayer::raise_layer(int howfar) {
  gnome_canvas_item_raise(grp, howfar);
}

void OOFCanvasLayer::raise_to_top() {
  gnome_canvas_item_raise_to_top(grp);
}

void OOFCanvasLayer::lower_layer(int howfar) {
  gnome_canvas_item_lower(grp, howfar);
}

void OOFCanvasLayer::show() {
  gnome_canvas_item_show(grp);
}

void OOFCanvasLayer::hide() {
  gnome_canvas_item_hide(grp);
}

void OOFCanvasLayer::move(double dx, double dy) {
  gnome_canvas_item_move(grp, dx, dy);
}
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void OOFCanvas::draw_dot(const Coord *dot) {
//   std::cerr << "OOFCanvas::draw_dot" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  empty = false;
  gnome_canvas_item_new(current_layer->group(),
			gnome_canvas_dot_get_type(),
			"x", (*dot)(0),
			"y", (*dot)(1),
			"size", lineWidth,
			"fill_color_rgba", lineColor,
			NULL);
}

void OOFCanvas::draw_triangle(const Coord *triangle, double angle) {
//   std::cerr << "OOFCanvas::draw_triangle" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  empty = false;
  gnome_canvas_item_new(current_layer->group(),
			gnome_canvas_triangle_get_type(),
			"x", (*triangle)(0),
			"y", (*triangle)(1),
			"size", lineWidth,
			"angle", angle, 
			"fill_color_rgba", lineColor,
			NULL);
}

void OOFCanvas::draw_segment(const GnomeCanvasPoints *points) {
//   std::cerr << "OOFCanvas::draw_segment" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  empty = false;
  gnome_canvas_item_new(current_layer->group(),
			gnome_canvas_line_get_type(),
			"points", points,
			"fill_color_rgba", lineColor,
			"width_pixels", lineWidth,
			NULL);
}

void OOFCanvas::draw_segments(const std::vector<GnomeCanvasPoints*> *segs) {
//   std::cerr << "OOFCanvas::draw_segments" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  empty = false;
  for(std::vector<GnomeCanvasPoints*>::size_type i=0; i<segs->size(); i++)
    draw_segment((*segs)[i]);
}

void OOFCanvas::draw_curve(const GnomeCanvasPoints *points) {
//   std::cerr << "OOFCanvas::draw_curve" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  empty = false;
  gnome_canvas_item_new(current_layer->group(),
			gnome_canvas_line_get_type(),
			"points", points,
			"fill_color_rgba", lineColor,
			"width_pixels", lineWidth,
			NULL);
}

// TODO OPT: One of the reasons for doing this by segments was to avoid an
// apparent libArt rendering bug, which resulted in error reports
// about gtk objects being in a list twice.  Apparently doing polygons
// this way has not eliminated this error report, it's been seen
// again.

void OOFCanvas::draw_polygon(const GnomeCanvasPoints *points) {
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  
  // Hacky workaround to avoid gnome_canvas_polyon operations -- draw
  // the segments individually.  See comment below for motivation.
  GnomeCanvasPoints *work;
  int size = points->num_points;
  for(int i=0;i<size;i++) {
    int end = (2*i+2)%(2*size);
    work = gnome_canvas_points_new(2);
    work->coords[0]=points->coords[2*i];
    work->coords[1]=points->coords[2*i+1];
    work->coords[2]=points->coords[end];
    work->coords[3]=points->coords[end+1];
    draw_segment(work);
    gnome_canvas_points_free(work);
  }


//   empty = false;
//   gnome_canvas_item_new(current_layer->group(),
// 			gnome_canvas_polygon_get_type(),
// 			"points", points,
// 			"outline_color_rgba", lineColor,
// 			"width_pixels", lineWidth,
// 			NULL);

//   Debugging code.  The canvas bounding box is computed incorrectly
//   for polygons.  This appears to be a GnomeCanvas bug.  This bug is
//   still present in libgnomecanvas 2.8.0.  To reproduce in OOF, just
//   create a microstructure which is 0.0001 x 0.0001 physical units,
//   then create a 4x4 skeleton, and draw the skeleton.  The bounds
//   will be much larger than the actual skeleton, and zooming will
//   fail.  It is as though there is a "minimum bounding box" or
//   something.

//   static bool first = true;
//   if(first) {
//     std::cerr << lineWidth << std::endl;
//     first = false;
//     std::cerr << "OOFCanvas::draw_polygon: first poly=[";
//     for(int i=0; i<points->num_points; i++)
//       std::cerr << std::endl << "           (" << points->coords[2*i]
//  		<< ", " << points->coords[2*i+1] << " )";
//     std::cerr << "]" << std::endl;
//     std::cerr << "                        bbox=" << get_bounds() << std::endl;
//   }
}

void OOFCanvas::fill_polygon(const GnomeCanvasPoints *points) {
//   std::cerr << "OOFCanvas::fill_polygon" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  empty = false;
  gnome_canvas_item_new(current_layer->group(),
			gnome_canvas_polygon_get_type(),
			"points", points,
			"fill_color_rgba", fillColor,
			NULL);
}

void OOFCanvas::draw_circle(const Coord &center, double radius) {
//   std::cerr << "OOFCanvas::draw_circle" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  empty = false;
  gnome_canvas_item_new(current_layer->group(),
			gnome_canvas_ellipse_get_type(),
			"x1", center(0) - radius,
			"y1", center(1) - radius,
			"x2", center(0) + radius,
			"y2", center(1) + radius,
			"outline_color_rgba", lineColor,
			NULL);
}

void OOFCanvas::fill_circle(const Coord &center, double radius) {
//   std::cerr << "OOFCanvas::fill_circle" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  empty = false;
  gnome_canvas_item_new(current_layer->group(),
			gnome_canvas_ellipse_get_type(),
			"x1", center(0) - radius,
			"y1", center(1) - radius,
			"x2", center(0) + radius,
			"y2", center(1) + radius,
			"fill_color_rgba", fillColor,
			NULL);
}

static void destStrImage(guchar *pixbuf_data, gpointer si) {
  delete (StringImage*) si;
}

void OOFCanvas::draw_image(const AbstractImage *image, const Coord *location,
			   const Coord *size)
{
//   std::cerr << "OOFCanvas::draw_image" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  ICoord isize(image->sizeInPixels());
  if(isize(0) > 0 && isize(1) > 0) {
    empty = false;
    StringImage *stringimage = new StringImage(&isize, size);
    image->fillstringimage(stringimage);
    GdkPixbuf *pixbuf = gdk_pixbuf_new_from_data(
			stringimage->getString(), // const guchar* data
			GDK_COLORSPACE_RGB, // GdkColorspace colorspace
			false, // gboolean has_alpha
			8, // int bits_per_sample
			isize(0), isize(1), // int width, height
			3*isize(0), // int rowstride
			destStrImage, // GdkPixbufDestroyNotify destroy_fn
			(gpointer) stringimage); // gpointer destroy_fn_data
    // The image is drawn with its lower left corner at the given
    // location.  Using "anchor=GTK_ANCHOR_SOUTH_WEST" fails on some
    // machines, though, so we use GTK_ANCHOR_NORTH_WEST and offset
    // the location by the y-component of the image size.
    GnomeCanvasItem *item = gnome_canvas_item_new(
					current_layer->group(),
					gnome_canvas_pixbuf_get_type(),
					"pixbuf", pixbuf,
					"x", (*location)(0),
					"y", (*location)(1)-(*size)(1),
					"anchor", GTK_ANCHOR_NORTH_WEST,
					"width", (*size)(0),
					"height", (*size)(1),
					"width-set", TRUE,
					"height-set", TRUE,
					NULL);
    g_object_unref(G_OBJECT(pixbuf));
    gnome_canvas_item_affine_absolute(item, affineflip);
  }
}

static void destAlphaStrImage(guchar *pixbuf_data, gpointer si) {
  delete (AlphaStringImage*) si;
}

void OOFCanvas::draw_alpha_image(const AbstractImage *image,
																 const Coord *location, const Coord *size)
																 //unsigned char alpha)
{
//   std::cerr << "OOFCanvas::draw_alpha_image" << std::endl;
  if(!canvas) throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  ICoord isize(image->sizeInPixels());
  if(isize(0) > 0 && isize(0) > 0) {
    empty = false;
    AlphaStringImage *stringimage = new AlphaStringImage(&isize, size);
    image->fillalphastringimage(stringimage);
    GdkPixbuf *pixbuf = gdk_pixbuf_new_from_data(
			       stringimage->getString(),
			       GDK_COLORSPACE_RGB,
			       true, // has_alpha
			       8,
			       isize(0), isize(1),
			       4*isize(0),
			       destAlphaStrImage, 
			       (gpointer) stringimage);
    // The image is drawn with its lower left corner at the given
    // location.  Using "anchor=GTK_ANCHOR_SOUTH_WEST" fails on some
    // machines, though, so we use GTK_ANCHOR_NORTH_WEST and offset
    // the location by the y-component of the image size.
    GnomeCanvasItem *item = gnome_canvas_item_new(
				  current_layer->group(),
				  gnome_canvas_pixbuf_get_type(),
				  "pixbuf", pixbuf,
				  "x", (*location)(0),
				  "y", (*location)(1)-(*size)(1),
				  "anchor", GTK_ANCHOR_NORTH_WEST,
				  "width", (*size)(0),
				  "height", (*size)(1),
				  "width-set", TRUE,
				  "height-set", TRUE,
				  NULL);
    g_object_unref(pixbuf);
    gnome_canvas_item_affine_absolute(item, affineflip);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Mouse event handling

void OOFCanvas::set_mouse_callback(PyObject *callback) {
  // callback must be a Python callable object which takes four arguments:
  //    event:  a string, either 'up', 'down', or 'move'
  //        x:  x position of the event
  //        y:  y position of the event, measured going *up* the screen
  //        s:  an int, 0 = no shift key, 1 = shift key
  //        c:  an int, 0 = no control key, 1 = control key
  mouse_callback = callback;
  PyGILState_STATE pystate = acquirePyLock();
  Py_XINCREF(callback);
  releasePyLock(pystate);
  mouse_handler_id = 
    gtk_signal_connect(GTK_OBJECT(root), "event",
		       GTK_SIGNAL_FUNC(OOFCanvas::mouse_event), this);
}

gint OOFCanvas::mouse_event(GnomeCanvasItem *item, GdkEvent *event,
			    gpointer data)
{
  OOFCanvas *oofcanvas = (OOFCanvas*)(data);
  oofcanvas->mouse_eventCB(item, event);
  return FALSE;   // Returning FALSE propagates the event to parent items.
}

void OOFCanvas::mouse_eventCB(GnomeCanvasItem *item, GdkEvent *event) {
  PyObject *args = 0;
  bool shift;
  bool ctrl;
  // Steal the focus so that other widgets know that their turn is over.
  // gtk_widget_grab_focus(canvas);
  // Protect the Python interpreter calls from thread interference
  // by obtaining the global interpreter lock.
  PyGILState_STATE state = (PyGILState_STATE) pyg_gil_state_ensure();
  try {
    switch(event->type) {
    case GDK_BUTTON_PRESS:
      shift = event->button.state & GDK_SHIFT_MASK;
      ctrl = event->button.state & GDK_CONTROL_MASK;
      args = Py_BuildValue("sddii", "down",
			   event->button.x, -event->button.y, // flip y axis!
			   shift, ctrl);
      mousedown_point = Coord(event->button.x, -event->button.y);// flip y axis!
      mousedown = true;
      break;
    case GDK_BUTTON_RELEASE:
      shift = event->button.state & GDK_SHIFT_MASK;
      ctrl = event->button.state & GDK_CONTROL_MASK;
      args = Py_BuildValue("sddii", "up",
			   event->button.x, -event->button.y, // flip y axis!
			   shift, ctrl);
      if(rubberband && rubberband->active()) {
	rubberband->stop();
      }
      mousedown = false;
      break;
    case GDK_MOTION_NOTIFY:
      shift = event->motion.state & GDK_SHIFT_MASK;
      ctrl = event->motion.state & GDK_CONTROL_MASK;
      args = Py_BuildValue("sddii", "move",
			   event->motion.x, -event->motion.y, // flip y axis!
			   shift, ctrl);
      if(mousedown && rubberband) {
	if(!rubberband->active()) {
	  rubberband->start(mousedown_point);
	}
	rubberband->redraw(canvas, Coord(event->motion.x, -event->motion.y)); // flip y axis!
      }
      break;
    default:
      ;				// (compiler warning suppression)
    }

    if(args) {
      PyObject *result = PyObject_CallObject(mouse_callback, args);
      if (result == NULL) {
	// pygtk1 used to have PyGtk_FatalExceptions.  Apparently
	// pygtk2 has no equivalent.
	PyErr_Print();
	PyErr_Clear();
      }
      Py_XDECREF(args);
      Py_XDECREF(result);
    }
  }
  catch(...) {
    pyg_gil_state_release(state);
    throw;
  }
  pyg_gil_state_release(state);
}


// Configuration event handling -- mainly we want to catch resizes.

void OOFCanvas::set_configure_callback(PyObject *callback) {
  config_callback = callback;
  PyGILState_STATE pystate = acquirePyLock();
  Py_XINCREF(callback);
  releasePyLock(pystate);
  config_handler_id = 
    gtk_signal_connect(GTK_OBJECT(canvas), "size-allocate", 
		       GTK_SIGNAL_FUNC(OOFCanvas::configure_event), this);
}

gint OOFCanvas::configure_event(GnomeCanvas *item, GtkAllocation *alloc,
				gpointer data)
{
  OOFCanvas *local_canvas = (OOFCanvas*)data;
  local_canvas->configure_eventCB(alloc);
  return FALSE;
}

void OOFCanvas::configure_eventCB(GtkAllocation *a) {
  gtk_widget_grab_focus(canvas);
  PyGILState_STATE state = (PyGILState_STATE) pyg_gil_state_ensure();
  try {
    PyObject *args = Py_BuildValue("iiii", 
				   (int)(a->x), (int)(a->y), 
				   (int)(a->width), (int)(a->height));
    if (args) {
//       std::cerr << "OOFCanvas Calling config_callback" << std::endl;
      PyObject *result = PyObject_CallObject(config_callback, args);
//       std::cerr << "OOFCanvas back from config_callback" << std::endl;
      if (result==NULL) {
	// pygtk1 used to have a way to check for fatal errors...
	PyErr_Print();
	PyErr_Clear();
      }
      Py_XDECREF(result);
      Py_XDECREF(args);
    }
  }
  catch (...) {
    pyg_gil_state_release(state);
    throw;
  }
  pyg_gil_state_release(state);
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void OOFCanvas::set_rubberband(RubberBand *rb) {
  rubberband = rb;
}

