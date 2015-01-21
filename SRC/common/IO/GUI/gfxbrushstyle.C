// -*- C++ -*-
// $RCSfile: gfxbrushstyle.C,v $
// $Revision: 1.3.18.2 $
// $Author: langer $
// $Date: 2014/12/14 22:49:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/GUI/gfxbrushstyle.h"
#include "common/coord.h"

void GfxCircleBrush::drawStyle(GnomeCanvasItem *rb, GdkBitmap *stipple,
			    GdkBitmap *stubble, const guint32 &black,
			    const guint32 &white, const Coord &current) {
  // Circle
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
 		      gnome_canvas_ellipse_get_type(),
 		      "x1", current(0)-r, "y1", (current(1)-r),
 		      "x2", current(0)+r, "y2", (current(1)+r),
 		      "outline_color_rgba", black,
 		      "outline_stipple", stipple,
 		      "width_pixels", 0,
 		      NULL);
  gnome_canvas_item_new(GNOME_CANVAS_GROUP(rb),
 		      gnome_canvas_ellipse_get_type(),
 		      "x1", current(0)-r, "y1", (current(1)-r),
 		      "x2", current(0)+r, "y2", (current(1)+r),
 		      "outline_color_rgba", white,
 		      "outline_stipple", stubble,
 		      "width_pixels", 0,
 		      NULL);
}

void GfxSquareBrush::drawStyle(GnomeCanvasItem *rb, GdkBitmap *stipple,
			    GdkBitmap *stubble, const guint32 &black,
			    const guint32 &white, const Coord &current) {
  GnomeCanvasPoints *pts = gnome_canvas_points_new(4);
  pts->coords[0] = current(0) - size;
  pts->coords[1] = current(1) + size;
  pts->coords[2] = current(0) - size;
  pts->coords[3] = current(1) - size;
  pts->coords[4] = current(0) + size;
  pts->coords[5] = current(1) - size;
  pts->coords[6] = current(0) + size;
  pts->coords[7] = current(1) + size;
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
}
