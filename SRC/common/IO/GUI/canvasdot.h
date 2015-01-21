/*  -*- c -*-
   $RCSfile: canvasdot.h,v $
   $Revision: 1.6.18.1 $
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

/* Custom canvas item, draws a circle on the canvas whose 
   radius can be specified in pixels.  For some strange reason,
   the rectangle/ellipse functions of the stock canvas do not do this. 
   This item is a subclass of the GnomeCanvasRE. */

/* Parameters:
   x               double     read/write   x-coord of center of dot
   y               double     read/write   y-coord of center of dot
   size            uint       read/write   size (radius) of dot in pixels. */

/* Fill color, stipple, graphics context, and so forth are set 
   from the parent class.  The parent class's outline parameters
   are ignored. */

#ifndef CANVASDOT_H
#define CANVASDOT_H

#include <libgnomecanvas/gnome-canvas.h>
#include <libgnomecanvas/gnome-canvas-shape.h>

G_BEGIN_DECLS

#define GNOME_TYPE_CANVAS_DOT            (gnome_canvas_dot_get_type ())
#define GNOME_CANVAS_DOT(obj)            (GTK_CHECK_CAST ((obj), GNOME_TYPE_CANVAS_DOT, GnomeCanvasDot))
#define GNOME_CANVAS_DOT_CLASS(klass)    (GTK_CHECK_CLASS_CAST ((klass), GNOME_TYPE_CANVAS_DOT, GnomeCanvasDotClass))
#define GNOME_IS_CANVAS_DOT(obj)         (GTK_CHECK_TYPE ((obj), GNOME_TYPE_CANVAS_DOT))
#define GNOME_IS_CANVAS_DOT_CLASS(klass) (GTK_CHECK_CLASS_TYPE ((klass), GNOME_TYPE_CANVAS_DOT))
#define GNOME_CANVAS_DOT_GET_CLASS(obj)  (GTK_CHECK_GET_CLASS ((obj), GNOME_TYPE_CANVAS_DOT, GnomeCanvasDotClass))


typedef struct _GnomeCanvasDot GnomeCanvasDot;
typedef struct _GnomeCanvasDotClass GnomeCanvasDotClass;

struct _GnomeCanvasDot {
  GnomeCanvasShape item;
  gdouble x, y;
  guint size;
};

struct _GnomeCanvasDotClass {
  GnomeCanvasShapeClass parent_class;
};


/* Standard Gtk function */
GType gnome_canvas_dot_get_type (void) G_GNUC_CONST;


G_END_DECLS

#endif /* CANVASDOT_H */
