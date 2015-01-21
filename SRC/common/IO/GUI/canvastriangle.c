/*  -*- c -*-
   $RCSfile: canvastriangle.c,v $
   $Revision: 1.14.18.1 $
   $Author: langer $
   $Date: 2014/09/27 22:34:08 $  */

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

/* Custom canvas item, draws an equilateral triangle on the canvas
   whose edge size is given in pixels and whose orientation is given
   in radians.  */



#include "canvastriangle.h"

#include <libart_lgpl/art_svp.h>
#include <libart_lgpl/art_svp_vpath.h>
#include <libart_lgpl/art_svp_vpath_stroke.h>
#include <libart_lgpl/art_vpath.h>
#include <libart_lgpl/art_vpath.h>
#include <math.h>
#include <stdio.h>

#include <libgnomecanvas/gnome-canvas-shape.h>

enum {
  PROP_0,
  PROP_X,
  PROP_Y,
  PROP_SIZE,
  PROP_ANGLE
};

static void gnome_canvas_triangle_class_init(GnomeCanvasTriangleClass *class);
static void gnome_canvas_triangle_init(GnomeCanvasTriangle *poly);
static void gnome_canvas_triangle_destroy(GtkObject *object);
static void gnome_canvas_triangle_set_property(GObject *object,
					       guint param_id,
					       const GValue *value,
					       GParamSpec *pspec);
static void gnome_canvas_triangle_get_property(GObject *object,
					       guint param_id,
					       GValue *value,
					       GParamSpec *pspec);

static void gnome_canvas_triangle_update(GnomeCanvasItem *item,
					 double *affine,
					 ArtSVP *clip_path,
					 int flags);
static double gnome_canvas_triangle_point(GnomeCanvasItem *item,
					  double x, double y, int cx, int cy,
					  GnomeCanvasItem **actual_item);
static void gnome_canvas_triangle_bounds(GnomeCanvasItem *item,
					   double *x1, double *y1,
					   double *x2, double *y2);

static GnomeCanvasItemClass *parent_class;

GType
gnome_canvas_triangle_get_type (void)
{
  static GType triangle_type;
  
  if (!triangle_type) {
    static const GTypeInfo object_info = {
      sizeof (GnomeCanvasTriangleClass),
      (GBaseInitFunc) NULL,
      (GBaseFinalizeFunc) NULL,
      (GClassInitFunc) gnome_canvas_triangle_class_init,
      (GClassFinalizeFunc) NULL,
      NULL,			/* class_data */
      sizeof (GnomeCanvasTriangle),
      0,			/* n_preallocs */
      (GInstanceInitFunc) gnome_canvas_triangle_init,
      NULL			/* value_table */
    };
    
    triangle_type = g_type_register_static(GNOME_TYPE_CANVAS_SHAPE,
					   "GnomeCanvasTriangle",
					   &object_info, 0);
  }
  return triangle_type;
}

static void
gnome_canvas_triangle_class_init (GnomeCanvasTriangleClass *class)
{
  GObjectClass *gobject_class;
  GtkObjectClass *object_class;
  GnomeCanvasItemClass *item_class;

  gobject_class = (GObjectClass *) class;
  object_class = (GtkObjectClass *) class;
  item_class = (GnomeCanvasItemClass *) class;

  parent_class = g_type_class_peek_parent (class);

  gobject_class->set_property = gnome_canvas_triangle_set_property;
  gobject_class->get_property = gnome_canvas_triangle_get_property;

  g_object_class_install_property
    (gobject_class,
     PROP_X,
     g_param_spec_double ("x", NULL, NULL,
			 -G_MAXDOUBLE, G_MAXDOUBLE, 0,
			 (G_PARAM_READABLE | G_PARAM_WRITABLE)));
  g_object_class_install_property
    (gobject_class,
     PROP_Y,
     g_param_spec_double ("y", NULL, NULL,
			 -G_MAXDOUBLE, G_MAXDOUBLE, 0,
			 (G_PARAM_READABLE | G_PARAM_WRITABLE)));
  g_object_class_install_property
    (gobject_class,
     PROP_SIZE,
     g_param_spec_int ("size", NULL, NULL,
		       0, G_MAXINT, 4, /* min, max, default */
		       (G_PARAM_READABLE | G_PARAM_WRITABLE)));
  g_object_class_install_property
    (gobject_class,
     PROP_ANGLE,
     g_param_spec_double("angle", NULL, NULL,
			 -G_MAXDOUBLE, G_MAXDOUBLE, 0,
			 (G_PARAM_READABLE | G_PARAM_WRITABLE)));

  object_class->destroy = gnome_canvas_triangle_destroy;

  item_class->update = gnome_canvas_triangle_update;
  item_class->point = gnome_canvas_triangle_point;
  item_class->bounds = gnome_canvas_triangle_bounds;
}

static void
gnome_canvas_triangle_init(GnomeCanvasTriangle *triangle)
{
  triangle->x = 0.0;
  triangle->y = 0.0;
  triangle->size = 0;
  triangle->angle = 0.0;
}

static void
gnome_canvas_triangle_destroy(GtkObject *object)
{
  GnomeCanvasTriangle *triangle;
  g_return_if_fail(object != NULL);
  g_return_if_fail(GNOME_IS_CANVAS_TRIANGLE (object));
  triangle = GNOME_CANVAS_TRIANGLE(object);
  if(GTK_OBJECT_CLASS(parent_class)->destroy)
    (*GTK_OBJECT_CLASS(parent_class)->destroy)(object);
}

static void
gnome_canvas_triangle_set_property(GObject *object,
			      guint param_id,
			      const GValue *value,
			      GParamSpec *pspec)
{
  GnomeCanvasItem *item;
  GnomeCanvasTriangle *triangle;
  
  g_return_if_fail(object != NULL);
  g_return_if_fail(GNOME_IS_CANVAS_TRIANGLE(object));
  item = GNOME_CANVAS_ITEM(object);
  triangle = GNOME_CANVAS_TRIANGLE(object);

  switch(param_id) {
  case PROP_X:
    triangle->x = g_value_get_double(value);
    gnome_canvas_item_request_update(item);
    break;
  case PROP_Y:
    triangle->y = g_value_get_double(value);
    gnome_canvas_item_request_update(item);
    break;
  case PROP_SIZE:
    triangle->size = g_value_get_int(value);
    gnome_canvas_item_request_update(item);
    break;
  case PROP_ANGLE:
    triangle->angle = g_value_get_double(value);
    gnome_canvas_item_request_update(item);
    break;
  default:
    G_OBJECT_WARN_INVALID_PROPERTY_ID(object, param_id, pspec);
    break;
  }
}

static void
gnome_canvas_triangle_get_property(GObject *object,
			      guint param_id,
			      GValue *value,
			      GParamSpec *pspec)
{
  GnomeCanvasTriangle *triangle;
  g_return_if_fail(object != NULL);
  g_return_if_fail(GNOME_IS_CANVAS_TRIANGLE(object));
  triangle = GNOME_CANVAS_TRIANGLE(object);

  switch(param_id) {
  case PROP_X:
    g_value_set_double(value, triangle->x);
    break;
  case PROP_Y:
    g_value_set_double(value, triangle->y);
    break;
  case PROP_SIZE:
    g_value_set_double(value, triangle->size);
    break;
  case PROP_ANGLE:
    g_value_set_double(value, triangle->angle);
    break;
  default:
    G_OBJECT_WARN_INVALID_PROPERTY_ID(object, param_id, pspec);
    break;
  }
}

static double get_world_radius(GnomeCanvasItem *item) {
  GnomeCanvasTriangle *triangle;
  triangle = GNOME_CANVAS_TRIANGLE(item);
  return ((double) triangle->size)/(item->canvas->pixels_per_unit);
}

static void
gnome_canvas_triangle_update(GnomeCanvasItem *item, double *affine,
			ArtSVP *clip_path, int flags)
{
  GnomeCanvasPathDef *path_def;
  GnomeCanvasTriangle *triangle;
  gdouble cx, cy, angle;
  double sq3;
  double x0, y0;
  double sqrt3 = sqrt(3.0);
  double sina, cosa, sinb, cosb, sinc, cosc;

  triangle = GNOME_CANVAS_TRIANGLE(item);
  cx = triangle->x;
  cy = triangle->y;
  angle = triangle->angle;

  sina = sin(angle);
  cosa = cos(angle);
  sinb = 0.5*(sqrt3*cosa - sina); /* sin(angle+2*pi/3) */
  cosb = -0.5*(cosa + sqrt3*sina); /* cos(angle+2*pi/3) */
  sinc = -0.5*(sina + sqrt3*cosa); /* sin(angle-2*pi/3) */
  cosc = 0.5*(sqrt3*sina - cosa); /* cos(angle-2*pi/3) */
  

  sq3 = get_world_radius(item)/sqrt3;
    
  path_def = gnome_canvas_path_def_new();

  /* A triangle pointing up the y axis has angle==0.  angle is
     measured counterclockwise. */
  x0 = cx - sq3*sina;
  y0 = cy + sq3*cosa;
  gnome_canvas_path_def_moveto(path_def, x0, y0);
  gnome_canvas_path_def_lineto(path_def, cx - sq3*sinb, cy + sq3*cosb);
  gnome_canvas_path_def_lineto(path_def, cx - sq3*sinc, cy + sq3*cosc);
  gnome_canvas_path_def_lineto(path_def, x0, y0);
  gnome_canvas_path_def_closepath_current(path_def);
  gnome_canvas_shape_set_path_def(GNOME_CANVAS_SHAPE(item), path_def);
  gnome_canvas_path_def_unref(path_def);

  if(parent_class->update)
    (*parent_class->update)(item, affine, clip_path, flags);
}

static double gnome_canvas_triangle_point(GnomeCanvasItem *item,
				     double x, double y, int cx, int cy,
				     GnomeCanvasItem **actual_item)
{
  /* Calculate the distance from an item to the specified point.  It also
   * returns a canvas item which is the item itself in the case of the
   * object being an actual leaf item, or a child in case of the object
   * being a canvas group.  (cx, cy) are the canvas pixel coordinates that
   * correspond to the item-relative coordinates (x, y).
   */
  GnomeCanvasTriangle *triangle;
  double dx, dy, w_radius, rr;
  triangle = GNOME_CANVAS_TRIANGLE(item);
  *actual_item = item;
  dx = triangle->x - x;
  dy = triangle->y - y;
  w_radius = get_world_radius(item);
  rr = dx*dx + dy*dy;
  if(rr < (w_radius*w_radius))
    return 0.0;
  else
    return rr;
}
 
static void gnome_canvas_triangle_bounds(GnomeCanvasItem *item,
					 double *x1, double *y1,
					 double *x2, double *y2)
{
  GnomeCanvasTriangle *triangle;
  double wr = get_world_radius(item);
  triangle = GNOME_CANVAS_TRIANGLE(item);
  *x1 = triangle->x - wr;
  *y1 = triangle->y - wr;
  *x2 = triangle->x + wr;
  *y2 = triangle->y + wr;
}
