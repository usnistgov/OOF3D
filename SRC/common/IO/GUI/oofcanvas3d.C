// -*- C++ -*-
// $RCSfile: oofcanvas3d.C,v $
// $Revision: 1.1.2.32 $
// $Author: langer $
// $Date: 2014/09/10 21:28:41 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/GUI/oofcanvas3d.h"
#include "common/IO/oofcerr.h"
#include "common/ooferror.h"
#include "common/pythonlock.h"
#include "common/threadstate.h"
#include "common/tostring.h"

#include <iostream>

#include <gdk/gdkx.h>
#include <gtk/gtk.h>
#include <pygobject.h>
#include <pygtk/pygtk.h>

#include <vtkCamera.h>
#include <vtkXOpenGLRenderWindow.h>


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


OOFCanvas3D::OOFCanvas3D() 
  : GhostOOFCanvas(),
    mousedown(false),
    last_x(0),
    last_y(0),
    mouse_callback(0),
    rubberband(0)
{
  assert(mainthread_query());

  if(!OOFCanvas3D::initialized) {
    OOFCanvas3D::initialized = 1;
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

  drawing_area = gtk_drawing_area_new(); 

  // we need to set the colormap of the drawing_area before it is realized
  Display* dis = GDK_DISPLAY();
  render_window->SetDisplayId(dis);
  XVisualInfo *v = render_window->GetDesiredVisualInfo();
  Colormap cm = render_window->GetDesiredColormap();
  GdkVisual *gdkv = gdkx_visual_get(v->visualid);
  GdkColormap *gdkcm = gdk_x11_colormap_foreign_new(gdkv, cm);
  gtk_widget_set_colormap(drawing_area, gdkcm);
  // free the memory allocated by GetDesiredVisualInfo
  XFree(v);

  g_signal_connect(drawing_area, "destroy",
		   G_CALLBACK(OOFCanvas3D::gtk_destroy),
		   this);
  g_signal_connect(drawing_area, "realize",
		   G_CALLBACK(OOFCanvas3D::gtk_realize),
		   this);
  g_signal_connect(drawing_area, "expose_event",
		   G_CALLBACK(OOFCanvas3D::gtk_expose),
		   this);
  g_signal_connect(drawing_area, "configure_event",
		   G_CALLBACK(OOFCanvas3D::gtk_configure),
		   this);
  gtk_widget_add_events(drawing_area, (GDK_EXPOSURE_MASK |
				       GDK_BUTTON_PRESS_MASK |
				       GDK_BUTTON_RELEASE_MASK |
				       GDK_KEY_PRESS_MASK |
				       GDK_POINTER_MOTION_MASK |
				       GDK_POINTER_MOTION_HINT_MASK |
				       GDK_ENTER_NOTIFY_MASK |
				       GDK_LEAVE_NOTIFY_MASK));

//         # need this to be able to handle key_press events.
//         self.set_flags(gtk.CAN_FOCUS)
//         # default size
//         self.set_size_request(300, 300)

  show();
}

OOFCanvas3D::~OOFCanvas3D() {}

PyObject *OOFCanvas3D::widget() { 
  PyObject *wdgt;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    wdgt = pygobject_new((GObject*) drawing_area);
  }
  catch (...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return wdgt;
}


// static
void OOFCanvas3D::gtk_destroy(GtkWidget*, gpointer data) {
  // This is a static function.  It's the gtk callback for the
  // "destroy" signal.
  OOFCanvas3D *oofcanvas = (OOFCanvas3D*)(data);
  oofcanvas->destroy();
  delete oofcanvas;
}

void OOFCanvas3D::destroy() {
  // for(DisplayLayerList::iterator i=layers.begin(); i!=layers.end(); ++i)
  //     delete *i;
  //delete underlayer;
  
//   if(mouse_callback) {
//     gtk_signal_disconnect(GTK_OBJECT(root), mouse_handler_id);
//     PyGILState_STATE pystate = acquirePyLock();
//     Py_XDECREF(mouse_callback);
//     releasePyLock(pystate);
//   }

//   if(config_callback) {
//     gtk_signal_disconnect(GTK_OBJECT(canvas), config_handler_id);
//     PyGILState_STATE pystate = acquirePyLock();
//     Py_XDECREF(config_callback);
//     releasePyLock(pystate);
//   }

  // TODO OPT: Does *drawing_area need to be explicitly destroyed?
  drawing_area = 0;
}

// static
gboolean OOFCanvas3D::gtk_realize(GtkWidget*, gpointer data) {
  OOFCanvas3D *oofcanvas = (OOFCanvas3D*)(data);
  return oofcanvas->realize();
}

gboolean OOFCanvas3D::realize() {
  assert(mainthread_query());
  if(!created) {
    gtk_widget_realize(drawing_area);
    XID wid = GDK_WINDOW_XID(drawing_area->window);
    // this version only works in gtk 2.14 and up  
    //GDK_WINDOW_XID(gtk_widget_get_window(drawing_area));
    //XID pid = GDK_WINDOW_XID(gtk_widget_get_parent_window(drawing_area));
    //render_window->SetParentId((void*)pid);
    render_window->SetWindowId((void*)wid);
    created = true;
  }
  return true;
}

// static
gboolean OOFCanvas3D::gtk_configure(GtkWidget*, GdkEventConfigure *config,
				    gpointer data) 
{
  assert(mainthread_query());
  OOFCanvas3D *oofcanvas = (OOFCanvas3D*)(data);
  return oofcanvas->configure(config);
}

gboolean OOFCanvas3D::configure(GdkEventConfigure *event) {
  assert(mainthread_query());
  int *sz;
  sz = render_window->GetSize();
  if(event->width != sz[0] || event->height != sz[1]) {
    render_window->SetSize(event->width, event->height);
  }
  return true;
}

// static
gboolean OOFCanvas3D::gtk_expose(GtkWidget*, GdkEventExpose *event,
				 gpointer data) 
{
  assert(mainthread_query());
  OOFCanvas3D *oofcanvas = (OOFCanvas3D*)(data);
  return oofcanvas->expose();
}

gboolean OOFCanvas3D::expose() {
  assert(mainthread_query());
  exposed = true;
  // This is called not just when the window is first exposed, but
  // whenever a part of it is re-exposed, so we have to call render().
  render();
  return true;
}

void OOFCanvas3D::show() {
  assert(mainthread_query());
  if(!drawing_area) 
    throw ErrProgrammingError("No canvas!", __FILE__, __LINE__);
  gtk_widget_show_all(drawing_area);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Mouse event handling

// Mouse click calling sequence:
//
// (1) OOFCanvas3D::mouse_event() receives an event and calls
// OOFCanvas3D::mouse_eventCB().  mouse_event() is a static method,
// and is the gtk callback for events in the drawing_area.
// mouse_eventCB is specific to a particular OOFCanvas3D.
// 
// (2) OOFCanvas3D::mouse_eventCB() constructs Python arguments and
// calls the Python callback function, GfxWindowBase.mouseCB().
// Arguments include the type of event ("down", "move", or "up") and
// its screen coordinates.
//
// (3) GfxWindowBase.mouseCB() calls the up(), down(), or move()
// method of the current mouseHandler, if the mouseHandler's
// acceptEvent() method says that it can handle the given event type.
// The mouseHandler is set when a toolbox or the toolbar calls
// GfxWindowBase.setMouseHandler(), usually in its activate() method.
// mouse handlers are subclasses of mousehandler.MouseHandler and
// (usually) toolboxGUI.GfxToolbox.
//
// (4) The mouseHandler uses the given x,y,shift,ctrl parameters to
// invoke a menu command.

void OOFCanvas3D::set_mouse_callback(PyObject *callback) {
  // callback must be a Python callable object which takes five arguments:
  //    event:  a string, either 'up', 'down', or 'move'
  //        x:  x position of the event
  //        y:  y position of the event
  //        s:  an int, 0 = no shift key, 1 = shift key
  //        c:  an int, 0 = no control key, 1 = control key
  mouse_callback = callback;
  PyGILState_STATE pystate = acquirePyLock();
  Py_XINCREF(callback);
  releasePyLock(pystate);
  mouse_handler_id = 
    gtk_signal_connect(GTK_OBJECT(drawing_area), "event",
		       GTK_SIGNAL_FUNC(OOFCanvas3D::mouse_event), this);
}

// static
gint OOFCanvas3D::mouse_event(GtkWidget *item, GdkEvent *event,
			    gpointer data)
{
  OOFCanvas3D *oofcanvas = (OOFCanvas3D*)(data);
  oofcanvas->mouse_eventCB(item, event);
  return FALSE;   // Returning FALSE propagates the event to parent items.
}

void OOFCanvas3D::mouse_eventCB(GtkWidget *item, GdkEvent *event) {
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
			   event->button.x, event->button.y, 
			   shift, ctrl);
      last_x = event->button.x;
      last_y = event->button.y;
      mousedown = true;
      break;
    case GDK_BUTTON_RELEASE:
      shift = event->button.state & GDK_SHIFT_MASK;
      ctrl = event->button.state & GDK_CONTROL_MASK;
      args = Py_BuildValue("sddii", "up",
			   event->button.x, event->button.y, 
			   shift, ctrl);
      if(rubberband && rubberband->active()) {
	rubberband->stop(renderer);
	render();
      }
      mousedown = false;
      break;
    case GDK_MOTION_NOTIFY:
      shift = event->motion.state & GDK_SHIFT_MASK;
      ctrl = event->motion.state & GDK_CONTROL_MASK;
      args = Py_BuildValue("sddii", "move",
			   event->motion.x, event->motion.y, 
			   shift, ctrl);
      // TODO 3.1: 3D rubberbands
      // if(mousedown && rubberband) {
      // 	double pt[3];
      // 	if(!rubberband->active()) {
      // 	  screen_coords_to_3D_coords(last_x, last_y, last_z, pt);
      // 	  rubberband->start(Coord(pt[0], pt[1], pt[2]));
      // 	}
      // 	// we include this condition because if the rubberband is
      // 	// NoRubberBand, active is always false, and we can avoid some
      // 	// expensive calls
      // 	if(rubberband->active()) {
      // 	  screen_coords_to_3D_coords(event->motion.x, event->motion.y, pt);
      // 	  rubberband->redraw(renderer, Coord(pt[0], pt[1], pt[2])); 
      // 	  render();
      // 	}
      // }
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Moving around

void OOFCanvas3D::mouse_tumble(double x, double y) {
  assert(mainthread_query());
  renderer->GetActiveCamera()->Azimuth(last_x - x);
  renderer->GetActiveCamera()->Elevation(y - last_y);
  renderer->GetActiveCamera()->OrthogonalizeViewUp();
  last_x = x;
  last_y = y;
}


void OOFCanvas3D::mouse_track(double x, double y) {
  assert(mainthread_query());

  // TODO OPT: Is there any reason not to always use the focal point?
  // Knowing what's been clicked on in nontrivial and context
  // dependent.
  // // if we click on a voxel, we will track that voxel, otherwise
  // // we track the focal point.
  // double clickedPoint[3], focalPoint[3], *trackPoint;
  // bool pointIn = screen_coords_to_3D_coords(x, y, clickedPoint);
  // renderer->GetActiveCamera()->GetFocalPoint(focalPoint);
  // if(pointIn)
  //   trackPoint = clickedPoint;
  // else
  //   trackPoint = focalPoint;
  double trackPoint[3];
  renderer->GetActiveCamera()->GetFocalPoint(trackPoint);

  // convert track point to display coordinates
  renderer->SetWorldPoint(trackPoint[0], trackPoint[1], trackPoint[2], 1.0);
  renderer->WorldToDisplay();
  double displayPoint[3];
  renderer->GetDisplayPoint(displayPoint);

  // add mouse displacement to track point in display coordinates
  double aPoint0 = (x - last_x);
  double aPoint1 = -(y - last_y);
  double newDPoint[3] = {displayPoint[0] + aPoint0,
			 displayPoint[1] + aPoint1,
			 displayPoint[2]};

  //convert newDisplayPoint to world coordinates
  renderer->SetDisplayPoint(newDPoint[0],newDPoint[1],newDPoint[2]);
  renderer->DisplayToWorld();
  double rPoint[4];
  renderer->GetWorldPoint(rPoint);
  if(rPoint[3] != 0.0){
    rPoint[0] = rPoint[0]/rPoint[3];
    rPoint[1] = rPoint[1]/rPoint[3];
    rPoint[2] = rPoint[2]/rPoint[3];
  }

  last_x = x;
  last_y = y;

  // track by displacement in display coordinates
  track(trackPoint[0] - rPoint[0],
	trackPoint[1] - rPoint[1],
	trackPoint[2] - rPoint[2]);
}

void OOFCanvas3D::mouse_dolly(double x, double y) {
  double factor = pow(1.02,(0.5*(last_y - y)));
  dolly(factor);
  last_x = x;
  last_y = y;
}

void OOFCanvas3D::set_rubberband(RubberBand *rb) {
  rubberband = rb;
}


