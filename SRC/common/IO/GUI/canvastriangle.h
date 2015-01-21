/*  -*- c -*-
   $RCSfile: canvastriangle.h,v $
   $Revision: 1.4.18.1 $
   $Author: langer $
   $Date: 2014/09/27 22:34:08 $  */

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

/* Custom canvas item, draws a triangle on the canvas whose 
   size can be specified in pixels.  For starters, the triangle
   is equilateral. */

/* Parameters:
   x               double     read/write   x-coord of center of dot
   y               double     read/write   y-coord of center of dot
   size            uint       read/write   edge size in pixels. 
   angle           double     read/write   rotation angle in radians. */

/* Fill color, stipple, graphics context, and so forth are set 
   from the parent class.  The parent class's outline parameters
   are ignored. */

#ifndef CANVASTRIANGLE_H
#define CANVASTRIANGLE_H

#include <libgnomecanvas/gnome-canvas.h>
#include <libgnomecanvas/gnome-canvas-shape.h>

G_BEGIN_DECLS

#define GNOME_TYPE_CANVAS_TRIANGLE            (gnome_canvas_triangle_get_type ())
#define GNOME_CANVAS_TRIANGLE(obj)            (GTK_CHECK_CAST ((obj), GNOME_TYPE_CANVAS_TRIANGLE, GnomeCanvasTriangle))
#define GNOME_CANVAS_TRIANGLE_CLASS(klass)    (GTK_CHECK_CLASS_CAST ((klass), GNOME_TYPE_CANVAS_TRIANGLE, GnomeCanvasTriangleClass))
#define GNOME_IS_CANVAS_TRIANGLE(obj)         (GTK_CHECK_TYPE ((obj), GNOME_TYPE_CANVAS_TRIANGLE))
#define GNOME_IS_CANVAS_TRIANGLE_CLASS(klass) (GTK_CHECK_CLASS_TYPE ((klass), GNOME_TYPE_CANVAS_TRIANGLE))
#define GNOME_CANVAS_TRIANGLE_GET_CLASS(obj)  (GTK_CHECK_GET_CLASS ((obj), GNOME_TYPE_CANVAS_TRIANGLE, GnomeCanvasTriangleClass))


typedef struct _GnomeCanvasTriangle GnomeCanvasTriangle;
typedef struct _GnomeCanvasTriangleClass GnomeCanvasTriangleClass;

struct _GnomeCanvasTriangle {
  GnomeCanvasShape item;
  gdouble x, y, angle;
  guint size;
};

struct _GnomeCanvasTriangleClass {
  GnomeCanvasShapeClass parent_class;
};


/* Standard Gtk function */
GType gnome_canvas_triangle_get_type (void) G_GNUC_CONST;

G_END_DECLS

#endif /* CANVASTRIANGLE_H */
