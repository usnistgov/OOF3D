/*  -*- c -*-
   $RCSfile: canvasdot.c,v $
   $Revision: 1.16.18.1 $
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

/* Custom canvas item, draws a circle on the canvas whose 
   radius can be specified in pixels.  For some strange reason,
   the rectangle/ellipse functions of the stock canvas do not do this. 
   This item is a subclass of the GnomeCanvasRE. */

#include "canvasdot.h"
#include <math.h>
#include <stdio.h>
#include <libart_lgpl/art_vpath.h>
#include <libart_lgpl/art_svp.h>
#include <libart_lgpl/art_svp_vpath.h>
#include <libart_lgpl/art_svp_vpath_stroke.h>

#include <libgnomecanvas/gnome-canvas-shape.h>

enum {
  PROP_0,
  PROP_X,
  PROP_Y,
  PROP_SIZE
};

static void gnome_canvas_dot_class_init(GnomeCanvasDotClass *class);
static void gnome_canvas_dot_init(GnomeCanvasDot *poly);
static void gnome_canvas_dot_destroy(GtkObject *object);
static void gnome_canvas_dot_set_property(GObject *object,
					  guint param_id,
					  const GValue *value,
					  GParamSpec *pspec);
static void gnome_canvas_dot_get_property(GObject *object,
					  guint param_id,
					  GValue *value,
					  GParamSpec *pspec);

static void gnome_canvas_dot_update(GnomeCanvasItem *item,
				    double *affine,
				    ArtSVP *clip_path,
				    int flags);
static double gnome_canvas_dot_point(GnomeCanvasItem *item,
				     double x, double y, int cx, int cy,
				     GnomeCanvasItem **actual_item);
static void gnome_canvas_dot_bounds(GnomeCanvasItem *item,
				    double *x1, double *y1,
				    double *x2, double *y2);

static GnomeCanvasItemClass *parent_class;

GType
gnome_canvas_dot_get_type (void)
{
  static GType dot_type;
  
  if (!dot_type) {
    static const GTypeInfo object_info = {
      sizeof (GnomeCanvasDotClass),
      (GBaseInitFunc) NULL,
      (GBaseFinalizeFunc) NULL,
      (GClassInitFunc) gnome_canvas_dot_class_init,
      (GClassFinalizeFunc) NULL,
      NULL,			/* class_data */
      sizeof (GnomeCanvasDot),
      0,			/* n_preallocs */
      (GInstanceInitFunc) gnome_canvas_dot_init,
      NULL			/* value_table */
    };
    
    dot_type = g_type_register_static(GNOME_TYPE_CANVAS_SHAPE, "GnomeCanvasDot",
				      &object_info, 0);
  }

  return dot_type;
}

static void
gnome_canvas_dot_class_init (GnomeCanvasDotClass *class)
{
  GObjectClass *gobject_class;
  GtkObjectClass *object_class;
  GnomeCanvasItemClass *item_class;

  gobject_class = (GObjectClass *) class;
  object_class = (GtkObjectClass *) class;
  item_class = (GnomeCanvasItemClass *) class;

  parent_class = g_type_class_peek_parent (class);

  gobject_class->set_property = gnome_canvas_dot_set_property;
  gobject_class->get_property = gnome_canvas_dot_get_property;

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

  object_class->destroy = gnome_canvas_dot_destroy;

  item_class->update = gnome_canvas_dot_update;
  item_class->point = gnome_canvas_dot_point;
  item_class->bounds = gnome_canvas_dot_bounds;

}

static void
gnome_canvas_dot_init(GnomeCanvasDot *dot)
{
  dot->x = 0.0;
  dot->y = 0.0;
  dot->size = 0;
}

static void
gnome_canvas_dot_destroy(GtkObject *object)
{
  GnomeCanvasDot *dot;
  g_return_if_fail(object != NULL);
  g_return_if_fail(GNOME_IS_CANVAS_DOT (object));
  dot = GNOME_CANVAS_DOT(object);
  
  if(GTK_OBJECT_CLASS(parent_class)->destroy)
    (*GTK_OBJECT_CLASS(parent_class)->destroy)(object);
}

static void
gnome_canvas_dot_set_property(GObject *object,
			      guint param_id,
			      const GValue *value,
			      GParamSpec *pspec)
{
  GnomeCanvasItem *item;
  GnomeCanvasDot *dot;
  
  g_return_if_fail(object != NULL);
  g_return_if_fail(GNOME_IS_CANVAS_DOT(object));
  item = GNOME_CANVAS_ITEM(object);
  dot = GNOME_CANVAS_DOT(object);

  switch(param_id) {
  case PROP_X:
    dot->x = g_value_get_double(value);
    gnome_canvas_item_request_update(item);
    break;
  case PROP_Y:
    dot->y = g_value_get_double(value);
    gnome_canvas_item_request_update(item);
    break;
  case PROP_SIZE:
    dot->size = g_value_get_int(value);
    gnome_canvas_item_request_update(item);
    break;
  default:
    G_OBJECT_WARN_INVALID_PROPERTY_ID(object, param_id, pspec);
    break;
  }
}

static void
gnome_canvas_dot_get_property(GObject *object,
			      guint param_id,
			      GValue *value,
			      GParamSpec *pspec)
{
  GnomeCanvasDot *dot;
  g_return_if_fail(object != NULL);
  g_return_if_fail(GNOME_IS_CANVAS_DOT(object));
  dot = GNOME_CANVAS_DOT(object);

  switch(param_id) {
  case PROP_X:
    g_value_set_double(value, dot->x);
    break;
  case PROP_Y:
    g_value_set_double(value, dot->y);
    break;
  case PROP_SIZE:
    g_value_set_double(value, dot->size);
    break;
  default:
    G_OBJECT_WARN_INVALID_PROPERTY_ID(object, param_id, pspec);
    break;
  }
}

static double get_world_radius(GnomeCanvasItem *item) {
  GnomeCanvasDot *dot;
  dot = GNOME_CANVAS_DOT(item);
  return ((double) dot->size)/(item->canvas->pixels_per_unit);
}

static void
gnome_canvas_dot_update(GnomeCanvasItem *item, double *affine,
			ArtSVP *clip_path, int flags)
{
  GnomeCanvasPathDef *path_def;
  GnomeCanvasDot *dot;
  gdouble cx, cy, rw, rw2;
  gdouble rs8, rc8;

  dot = GNOME_CANVAS_DOT(item);
  cx = dot->x;
  cy = dot->y;

  rw = get_world_radius(item);
  rw2 = rw*M_SQRT1_2;
  rs8 = rw*0.3826834324;	/* sin(pi/8) */
  rc8 = rw*0.9238795325;	/* cos(pi/8) */

  path_def = gnome_canvas_path_def_new();
  gnome_canvas_path_def_moveto(path_def, cx+rw,  cy); /* E */
  gnome_canvas_path_def_lineto(path_def, cx+rc8, cy-rs8);
  gnome_canvas_path_def_lineto(path_def, cx+rw2, cy-rw2); /* SE */
  gnome_canvas_path_def_lineto(path_def, cx+rs8, cy-rc8);
  gnome_canvas_path_def_lineto(path_def, cx,     cy-rw); /* S */
  gnome_canvas_path_def_lineto(path_def, cx-rs8, cy-rc8);
  gnome_canvas_path_def_lineto(path_def, cx-rw2, cy-rw2); /* SW */
  gnome_canvas_path_def_lineto(path_def, cx-rc8, cy-rs8);
  gnome_canvas_path_def_lineto(path_def, cx-rw,  cy); /* W */
  gnome_canvas_path_def_lineto(path_def, cx-rc8, cy+rs8);
  gnome_canvas_path_def_lineto(path_def, cx-rw2, cy+rw2); /* NW */
  gnome_canvas_path_def_lineto(path_def, cx-rs8, cy+rc8);
  gnome_canvas_path_def_lineto(path_def, cx,     cy+rw); /* N */
  gnome_canvas_path_def_lineto(path_def, cx+rs8, cy+rc8);
  gnome_canvas_path_def_lineto(path_def, cx+rw2, cy+rw2); /* NE */
  gnome_canvas_path_def_lineto(path_def, cx+rc8, cy+rs8);
  gnome_canvas_path_def_lineto(path_def, cx+rw,  cy); /* E */
  gnome_canvas_path_def_closepath_current(path_def);
  gnome_canvas_shape_set_path_def(GNOME_CANVAS_SHAPE(dot), path_def);
  gnome_canvas_path_def_unref(path_def); 

  if(parent_class->update)
    (*parent_class->update)(item, affine, clip_path, flags);
}

static double gnome_canvas_dot_point(GnomeCanvasItem *item,
				     double x, double y, int cx, int cy,
				     GnomeCanvasItem **actual_item)
{
  /* Calculate the distance from an item to the specified point.  It also
   * returns a canvas item which is the item itself in the case of the
   * object being an actual leaf item, or a child in case of the object
   * being a canvas group.  (cx, cy) are the canvas pixel coordinates that
   * correspond to the item-relative coordinates (x, y).
   */
  GnomeCanvasDot *dot;
  double dx, dy, w_radius, rr;

  dot = GNOME_CANVAS_DOT(item);
  *actual_item = item;
  dx = dot->x - x;
  dy = dot->y - y;
  w_radius = get_world_radius(item);
  rr = dx*dx + dy*dy;
  if(rr < (w_radius*w_radius))
    return 0.0;
  else
    return rr;
}
 
static void gnome_canvas_dot_bounds(GnomeCanvasItem *item,
				      double *x1, double *y1,
				      double *x2, double *y2)
{
  GnomeCanvasDot *dot;
  double wr = get_world_radius(item);

  dot = GNOME_CANVAS_DOT(item);
  *x1 = dot->x - wr; 
  *y1 = dot->y - wr; 
  *x2 = dot->x + wr;
  *y2 = dot->y + wr;

}

