// -*- C++ -*-
// $RCSfile: rubberband.C,v $
// $Revision: 1.24.8.1 $
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

#include <oofconfig.h>

#include "common/threadstate.h"	// for debugging

#include "common/IO/GUI/rubberband.h"
#include "common/IO/GUI/oofcanvas.h"
#include "common/IO/GUI/rbstipple.xbm"
#include "common/IO/GUI/rbstubble.xbm"
#if DIM==2
#include "common/IO/GUI/gfxbrushstyle.h"
#endif
#include <math.h>

guint32 black = 0;
guint32 white = 0xffffffff;

RubberBand::RubberBand()
  : active_(false), rubberband(0)
{
  stipple = gdk_bitmap_create_from_data((GdkWindow*) 0,
					(const gchar*) rbstipple_bits,
					rbstipple_width, rbstipple_height);

  stubble = gdk_bitmap_create_from_data((GdkWindow*) 0,
					(const gchar*) rbstubble_bits,
					rbstubble_width, rbstubble_height);
}

void RubberBand::start(const Coord &pt) {
  startpt = pt;
  current = pt;
  active_ = true;
}

void RubberBand::stop() {
  clear();
  active_ = false;
}

RubberBand::~RubberBand() {
  clear();
  gdk_bitmap_unref(stipple);
  gdk_bitmap_unref(stubble);
}

void RubberBand::clear() {
  if(rubberband) {
    gtk_object_destroy(GTK_OBJECT(rubberband));
    rubberband = 0;
  }
}

void RubberBand::redraw(GtkWidget *canvas, const Coord &point) {
  clear();
  if(active_) {
    current = point;
    rubberband = draw(canvas);	// virtual function call
    gnome_canvas_item_show(rubberband);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

RectangleRubberBand::RectangleRubberBand()
  : pts(gnome_canvas_points_new(4))
{}

void RectangleRubberBand::start(const Coord &pt) {
  RubberBand::start(pt);
  // pts is an array of (x,y) pairs in clockwise order around the 
  // rectangle.  Fill in the parts we know.
  pts->coords[0] = startpt(0);
  pts->coords[1] = startpt(1);
  pts->coords[3] = startpt(1);
  pts->coords[6] = startpt(0);
}

RectangleRubberBand::~RectangleRubberBand() {
  gnome_canvas_points_unref(pts);
}

GnomeCanvasItem *RectangleRubberBand::draw(GtkWidget *canvas) {
  pts->coords[2] = current(0);
  pts->coords[4] = current(0);
  pts->coords[5] = current(1);
  pts->coords[7] = current(1);
  GnomeCanvasItem *rb = gnome_canvas_item_new(
				       gnome_canvas_root(GNOME_CANVAS(canvas)),
				       gnome_canvas_group_get_type(),
				       "x", 0.0, "y", 0.0,
				       NULL);
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
					  gnome_canvas_polygon_get_type(),
					  "points", pts,
					  "outline_color_rgba", black,
					  "width_pixels", 0,
					  "outline_stipple", stipple,
					  NULL);
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
					  gnome_canvas_polygon_get_type(),
					  "points", pts,
					  "outline_color_rgba", white,
					  "width_pixels", 0,
					  "outline_stipple", stubble,
					  NULL);
  return rb;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CircleRubberBand::CircleRubberBand()
  : pts(gnome_canvas_points_new(2))
{}

void CircleRubberBand::start(const Coord &pt)
{
  RubberBand::start(pt);
  pts->coords[0] = pt(0);
  pts->coords[1] = pt(1);
}

CircleRubberBand::~CircleRubberBand() {
  gnome_canvas_points_unref(pts);
}

GnomeCanvasItem *CircleRubberBand::draw(GtkWidget *canvas) {
  Coord radius = current - startpt;
  double r = sqrt(norm2(radius));
  GnomeCanvasItem *rb = gnome_canvas_item_new(
				      gnome_canvas_root(GNOME_CANVAS(canvas)),
				      gnome_canvas_group_get_type(),
				      "x", 0.0, "y", 0.0,
				      NULL);
   gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
 		      gnome_canvas_ellipse_get_type(),
 		      "x1", startpt(0)-r, "y1", (startpt(1)-r),
 		      "x2", startpt(0)+r, "y2", (startpt(1)+r),
 		      "outline_color_rgba", black,
 		      "outline_stipple", stipple,
 		      "width_pixels", 0,
 		      NULL);
   gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
 		      gnome_canvas_ellipse_get_type(),
 		      "x1", startpt(0)-r, "y1", (startpt(1)-r),
 		      "x2", startpt(0)+r, "y2", (startpt(1)+r),
 		      "outline_color_rgba", white,
 		      "outline_stipple", stubble,
 		      "width_pixels", 0,
 		      NULL);
   pts->coords[2] = current(0);
   pts->coords[3] = current(1);
   gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb), gnome_canvas_line_get_type(),
 		      "points", pts,
 		      "fill_color_rgba", black,
 		      "width_pixels", 0,
		       "fill_stipple", stipple,
		       NULL);
   gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb), gnome_canvas_line_get_type(),
 		      "points", pts,
 		      "fill_color_rgba", white,
 		      "width_pixels", 0,
		       "fill_stipple", stubble,
		       NULL);
  return rb;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The EllipseRubberBand does no preprocessing either in its
// constructor or its start routine, because the ellipse canvas item
// requires a particular ordering of the points, so we can't do
// anything until we know all the points.

GnomeCanvasItem *EllipseRubberBand::draw(GtkWidget *canvas) {
  GnomeCanvasItem *rb = gnome_canvas_item_new(
				       gnome_canvas_root(GNOME_CANVAS(canvas)),
				       gnome_canvas_group_get_type(),
				       "x", 0.0, "y", 0.0,
				       NULL);

  // The ellipse canvas item requires x1 < x2 and y1 < y2.
  double xmin, ymin, xmax, ymax;
  if(startpt(0) < current(0)) {
    xmin = startpt(0);
    xmax = current(0);
  }
  else {
    xmin = current(0);
    xmax = startpt(0);
  }
  if(startpt(1) < current(1)) {
    ymin = startpt(1);
    ymax = current(1);
  }
  else {
    ymin = current(1);
    ymax = startpt(1);
  }
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
 		      gnome_canvas_ellipse_get_type(),
 		      "x1", xmin, "y1", ymin,
 		      "x2", xmax, "y2", ymax,
 		      "outline_color_rgba", black,
		      "outline_stipple", stipple,
 		      "width_pixels", 0,
 		      NULL);
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
 		      gnome_canvas_ellipse_get_type(),
 		      "x1", xmin, "y1", ymin,
 		      "x2", xmax, "y2", ymax,
 		      "outline_color_rgba", white,
		      "outline_stipple", stubble,
 		      "width_pixels", 0,
 		      NULL);
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
		      gnome_canvas_rect_get_type(),
 		      "x1", xmin, "y1", ymin,
 		      "x2", xmax, "y2", ymax,
 		      "outline_color_rgba", black,
		      "outline_stipple", stipple,
 		      "width_pixels", 0,
 		      NULL);
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
		      gnome_canvas_rect_get_type(),
 		      "x1", xmin, "y1", ymin,
 		      "x2", xmax, "y2", ymax,
 		      "outline_color_rgba", white,
		      "outline_stipple", stubble,
 		      "width_pixels", 0,
 		      NULL);
  return rb;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SpiderRubberBand::SpiderRubberBand(const std::vector<Coord> *points)
  : segments(points->size())
{
  for(std::vector<Coord>::size_type i=0; i<points->size(); i++) {
    GnomeCanvasPoints *gtkpoints = gnome_canvas_points_new(2);
    segments[i] = gtkpoints;
    const Coord &pt = (*points)[i];
    gtkpoints->coords[2] = pt(0);
    gtkpoints->coords[3] = pt(1);
  }
}

SpiderRubberBand::~SpiderRubberBand() {
  for(std::vector<GnomeCanvasPoints*>::size_type i=0; i<segments.size(); i++)
    gnome_canvas_points_free(segments[i]);
}

GnomeCanvasItem *SpiderRubberBand::draw(GtkWidget *canvas) {
  GnomeCanvasItem *rb = gnome_canvas_item_new(
				      gnome_canvas_root(GNOME_CANVAS(canvas)),
				      gnome_canvas_group_get_type(),
				      "x", 0.0, "y", 0.0, NULL);
  for(std::vector<GnomeCanvasPoints*>::size_type i=0; i<segments.size(); i++) {
    segments[i]->coords[0] = current(0);
    segments[i]->coords[1] = current(1);

    gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
			gnome_canvas_line_get_type(),
			"points", segments[i],
			"fill_color_rgba", black,
			"width_pixels", 0,
			"fill_stipple", stipple,
			NULL);
    gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
			gnome_canvas_line_get_type(),
			"points", segments[i],
			"fill_color_rgba", white,
			"width_pixels", 0,
			"fill_stipple", stubble,
			NULL);
  }
  return rb;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

BrushRubberBand::BrushRubberBand(GfxBrushStyle *brush) :
  style(brush), trail(0)
{}

void BrushRubberBand::cleanup() {
  gnome_canvas_points_free(trail);
  trail = 0;
}

void BrushRubberBand::start(const Coord &pt)
{
  RubberBand::start(pt);
  // Gnome won't let us create a GnomeCanvasPoints object with only
  // one point, even temporarily, so we have to use our own npts
  // variable to keep track of how many points there really are.  The
  // GnomeCanvasPoints object won't actually be used until there are
  // at least 2 points in it, but at the moment we only know one
  // point.
  trail = gnome_canvas_points_new(2);
  trail->coords[0] = pt(0);
  trail->coords[1] = pt(1);
  npts = 1;
}

GnomeCanvasItem *BrushRubberBand::draw(GtkWidget *canvas) {
  GnomeCanvasItem *rb = gnome_canvas_item_new(
				      gnome_canvas_root(GNOME_CANVAS(canvas)),
				      gnome_canvas_group_get_type(),
				      "x", 0.0, "y", 0.0,
				      NULL);
  int n = trail->num_points;
  if(n == npts) {		// n!=npts when starting up. See start(), above.
    GnomeCanvasPoints *new_trail = gnome_canvas_points_new(n+1);  
    memcpy(new_trail->coords, trail->coords, 2*n*sizeof(double));
    gnome_canvas_points_free(trail);
    trail = new_trail;
  }
  trail->coords[2*npts] = current(0);
  trail->coords[2*npts+1] = current(1);
  npts += 1;

  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb), 
			gnome_canvas_line_get_type(),
			"points", trail,
			"fill_color_rgba", black,
			"width_pixels", 0,
			"fill_stipple", stipple,
			NULL);
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
			gnome_canvas_line_get_type(),
			"fill_color_rgba", white,
			"width_pixels", 0,
			"fill_stipple", stubble,
			NULL);
  style->drawStyle(rb, stipple, stubble, black, white, current);
  return rb;
}

void BrushRubberBand::stop() {
  RubberBand::stop();
  cleanup();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

LineRubberBand::LineRubberBand() : segment(gnome_canvas_points_new(2)) {
}

LineRubberBand::~LineRubberBand() {
  gnome_canvas_points_free(segment);
}

void LineRubberBand::start(const Coord &pt) {
  RubberBand::start(pt);
  segment->coords[0] = startpt(0);
  segment->coords[1] = startpt(1);
}

// When draw is called, current has been set by RubberBand::redraw.
GnomeCanvasItem *LineRubberBand::draw(GtkWidget *canvas) {
  GnomeCanvasItem *rb = gnome_canvas_item_new(
				  gnome_canvas_root(GNOME_CANVAS(canvas)),
				  gnome_canvas_group_get_type(),
				  "x", 0.0, "y", 0.0, 
				  NULL);
  segment->coords[2] = current(0);
  segment->coords[3] = current(1);
  
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb), gnome_canvas_line_get_type(),
		      "points", segment, 
		      "fill_color_rgba", black,
		      "width_pixels", 0, 
		      "fill_stipple", stipple,
		      NULL);

  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb), gnome_canvas_line_get_type(),
		      "points", segment, 
		      "fill_color_rgba", white,
		      "width_pixels", 0, 
		      "fill_stipple", stubble,
		      NULL);
  return rb;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const RubberBand &rb) {
  rb.print(os);
  return os;
}

void NoRubberBand::print(std::ostream &os) const {
  os << "NoRubberBand";
}

void RectangleRubberBand::print(std::ostream &os) const {
  os << "RectangleRubberBand";
}

void EllipseRubberBand::print(std::ostream &os) const {
  os << "EllipseRubberBand";
}

void CircleRubberBand::print(std::ostream &os) const {
  os << "CircleRubberBand";
}

void SpiderRubberBand::print(std::ostream &os) const {
  os << "SpiderRubberBand";
}

void BrushRubberBand::print(std::ostream &os) const {
  os << "BrushRubberBand";
}

void LineRubberBand::print(std::ostream &os) const {
  os << "LineRubberBand";
}
