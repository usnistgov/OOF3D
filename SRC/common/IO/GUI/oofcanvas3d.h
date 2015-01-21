// -*- C++ -*-
// $RCSfile: oofcanvas3d.h,v $
// $Revision: 1.1.2.13 $
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

#ifndef OOFCANVAS3D_H
#define OOFCANVAS3D_H

class OOFCanvas3D;

#include "common/IO/GUI/rubberband3d.h"
#include "common/IO/ghostoofcanvas.h"
#include "common/ccolor.h"

#include <gtk/gtk.h>
#include <vector>

class OOFCanvas3D : public GhostOOFCanvas {
private:
  bool mousedown;
  double last_x, last_y;
  PyObject *mouse_callback;
  guint mouse_handler_id; //, config_handler_id;
  RubberBand *rubberband;
protected:
  GtkWidget *drawing_area;

public:
  OOFCanvas3D();
  ~OOFCanvas3D();

  PyObject *widget();
  void show();

  // Separate callbacks for mouse events and resize events.
  void set_mouse_callback(PyObject*);

  // Callback functions
  static void gtk_destroy(GtkWidget*, gpointer);
  void destroy();
  static gboolean gtk_realize(GtkWidget*, gpointer);
  gboolean realize();
  static gboolean gtk_configure(GtkWidget*, GdkEventConfigure*, gpointer);
  gboolean configure(GdkEventConfigure*);
  static gboolean gtk_expose(GtkWidget*, GdkEventExpose*, gpointer);
  gboolean expose();
  static gint mouse_event(GtkWidget*, GdkEvent*, gpointer);
  void mouse_eventCB(GtkWidget*, GdkEvent*);

  // movements
  void mouse_tumble(double x, double y);
  void mouse_track(double x, double y);
  void mouse_dolly(double x, double y);

  void set_rubberband(RubberBand*);

  friend class RubberBand;

};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#endif
