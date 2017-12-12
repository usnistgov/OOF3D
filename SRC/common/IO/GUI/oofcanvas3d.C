// -*- C++ -*-


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
#include "common/smallmatrix.h"
#include "common/threadstate.h"
#include "common/tostring.h"

#include <iostream>

#include <gdk/gdk.h>
#include <gtk/gtk.h>
#include <pygobject.h>
#include <pygtk/pygtk.h>

#include <vtkCamera.h>

#ifdef OOF_USE_COCOA
// gdkquartz.h includes some ObjectiveC headers, so this file is
// wrapped by oofcanvas3d.mm when using Cocoa.
#include <gdk/gdkquartz.h>
#else // not OOF_USE_COCOA
#include <gdk/gdkx.h>
#include <vtkXOpenGLRenderWindow.h>
#endif // not OOF_USE_COCOA


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

#ifndef OOF_USE_COCOA
  Display* dis = GDK_DISPLAY();
  render_window->SetDisplayId(dis);
#endif // not OOF_USE_COCOA

  g_handlers.push_back(g_signal_connect(
			drawing_area,
			"realize",
			G_CALLBACK(OOFCanvas3D::gtk_realize),
			this));
  g_handlers.push_back(g_signal_connect(
			drawing_area,
			"expose_event",
			G_CALLBACK(OOFCanvas3D::gtk_expose),
			this));
  g_handlers.push_back(g_signal_connect(
			drawing_area,
			"configure_event",
			G_CALLBACK(OOFCanvas3D::gtk_configure),
			this));

  gtk_widget_add_events(drawing_area, (GDK_EXPOSURE_MASK
				       | GDK_BUTTON_PRESS_MASK
				       | GDK_BUTTON_RELEASE_MASK
				       | GDK_KEY_PRESS_MASK
				       | GDK_SCROLL_MASK
				       | GDK_POINTER_MOTION_MASK
				       | GDK_POINTER_MOTION_HINT_MASK
				       | GDK_ENTER_NOTIFY_MASK
				       | GDK_LEAVE_NOTIFY_MASK
				       ));
  show();
}

OOFCanvas3D::~OOFCanvas3D() {
  for(gulong handler : g_handlers) {
    g_signal_handler_disconnect(drawing_area, handler);
  }

  if(mouse_callback) {
    PyGILState_STATE pystate = acquirePyLock();
    Py_XDECREF(mouse_callback);
    releasePyLock(pystate);
  }

#ifndef OOF_USE_COCOA
  // We were getting this error when closing windows and using vtk8:
  //    [xcb] Unknown sequence number while processing queue
  //    [xcb] Most likely this is a multi-threaded client and XInitThreads
  //         has not been called
  //    [xcb] Aborting, sorry about that.
  //    python: ../../src/xcb_io.c:274: poll_for_event: Assertion
  //        `!xcb_xlib_threads_sequence_lost' failed.
  // However, calling XInitThreads (see initialize_X11 in vtkutils.C)
  // didn't make a difference (except for crashing earlier), and all
  // of the X calls should be coming from a single thread unless vtk is
  // making calls from more than one.  Anyway, either vtk or pygtk is
  // probably already calling XInitThreads.  The solution here seems
  // to be to flush the X11 event queue before closing the window.

  // TODO: discard only the events pertaining to this window.
  // Discarding all of them may cause problems with other open
  // graphics windows.
  XSync(GDK_DISPLAY(), false); // true ==> discard pending events

  // Both vtk7 and vtk8 sometimes generate a BadWindow error when
  // closing a vtkXOpenGLRenderWindow, although the errors arise at
  // different points, in different X function calls.  I think the
  // errors are due to gtk and vtk squabbling over who owns the
  // window.  I don't know if zeroing the WindowId here is the correct
  // solution, but it seems to work.
  render_window->SetWindowId(0);

#endif // OOF_USE_COCOA
}

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
gboolean OOFCanvas3D::gtk_realize(GtkWidget*, gpointer data) {
  OOFCanvas3D *oofcanvas = (OOFCanvas3D*)(data);
  return oofcanvas->realize();
}

gboolean OOFCanvas3D::realize() {
  assert(mainthread_query());
  if(!created) {
    gtk_widget_realize(drawing_area);
#ifndef OOF_USE_COCOA
    XID wid = GDK_WINDOW_XID(drawing_area->window);
    render_window->SetWindowId((void*) wid);

    // An old comment here said "this version only works in gtk
    // 2.14 and up", but the code following it didn't make sense.  I
    // *think* that it should have been the following, but I'm not
    // sure.  Anyhow it doesn't seem to work -- it crashes when the
    // window is closed, unless SetWindowId is also set, as above.
    // XID pid = GDK_WINDOW_XID(gtk_widget_get_parent_window(drawing_area));
    // render_window->SetParentId((void*) pid);
#else  // OOF_USE_COCOA
    render_window->SetRootWindow(gtk_widget_get_root_window(drawing_area));
    GdkWindow *gparent = gtk_widget_get_parent_window(drawing_area);
    NSView *pid = gdk_quartz_window_get_nsview(gparent);
    render_window->SetParentId((void*) pid);
#endif // OOF_USE_COCOA
    created = true;
  }
  return FALSE;	// Returning FALSE propagates the event to parent items.
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
   // oofcerr << "OOFCanvas3D::configure: w=" << event->width
   // 	   << " h=" << event->height
   // 	   << " x=" << event->x << " y=" << event->y
   // 	   << std::endl;
  assert(mainthread_query());
  // The height, width, x, and y elements of event are the same as
  // those of drawing_area->allocation.
  render_window->SetSize(event->width, event->height);

#ifdef OOF_USE_COCOA
  // vtk measures y *up* from the bottom edge of the top level
  // window, but gtk measures it down from the top of the window.
  GtkWidget *topwindow = gtk_widget_get_toplevel(drawing_area);
  assert(topwindow != nullptr);
  int top_height = topwindow->allocation.height;
  render_window->SetPosition(event->x, top_height - event->y - event->height);
#else
  render_window->SetPosition(event->x, event->y);
#endif // not OOF_USE_COCOA
  return FALSE;	// Returning FALSE propagates the event to parent items.
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
  // oofcerr << "OOFCanvas3D::expose" << std::endl;
  exposed = true;
  // This is called not just when the window is first exposed, but
  // whenever a part of it is re-exposed, so we have to call
  // Render(). It's also called after the 'configure' callback when a
  // window is resized.

  // On Linux, after a window is resized (with a 'configure' event)
  // the contents disappear unless Render() is called again.  Whatever
  // is clearing the window is happening after the 'configure',
  // 'configure_after', and 'expose' callbacks have completed, so
  // calling Render() from the callbacks isn't sufficient.  We need to
  // run it from an idle callback.
  g_idle_add(OOFCanvas3D::gtk_redrawIdle, this);
  return FALSE;	// Returning FALSE propagates the event to parent items.
}

// static
gboolean OOFCanvas3D::gtk_redrawIdle(gpointer data) {
  OOFCanvas3D *oofcanvas = (OOFCanvas3D*)(data);
  return oofcanvas->redrawIdle();
}

gboolean OOFCanvas3D::redrawIdle() {
  // gtk idle callback installed and run once by the expose event
  // callback.
  render_window->Render();
  return FALSE;			// FALSE means "run just once".
}

void OOFCanvas3D::show() {
  // oofcerr << "OOFCanvas3D::show" << std::endl;
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
  //        b:  an int, the mouse button number
  //        s:  an int, 0 = no shift key, 1 = shift key
  //        c:  an int, 0 = no control key, 1 = control key

  // TODO: Construct and return different types of objects for
  // different types of events.  Then the scroll direction wouldn't
  // have to be returned in the button number, as it is now.
  
  mouse_callback = callback;
  PyGILState_STATE pystate = acquirePyLock();
  Py_XINCREF(callback);
  releasePyLock(pystate);
  g_handlers.push_back(g_signal_connect(drawing_area, "event",
					G_CALLBACK(OOFCanvas3D::mouse_event),
					this));
}

// static
gboolean OOFCanvas3D::mouse_event(GtkWidget *item, GdkEvent *event,
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
  int buttonNumber;
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
      buttonNumber = event->button.button;
      args = Py_BuildValue("sddiii", "down",
			   event->button.x, event->button.y, 
			   buttonNumber, shift, ctrl);
      last_x = event->button.x;
      last_y = event->button.y;
      mousedown = true;
      break;
    case GDK_BUTTON_RELEASE:
      shift = event->button.state & GDK_SHIFT_MASK;
      ctrl = event->button.state & GDK_CONTROL_MASK;
      buttonNumber = event->button.button;
      args = Py_BuildValue("sddiii", "up",
			   event->button.x, event->button.y, 
			   buttonNumber, shift, ctrl);
      if(rubberband && rubberband->active()) {
	rubberband->stop(renderer);
	render();
      }
      mousedown = false;
      break;
    case GDK_MOTION_NOTIFY:
      shift = event->motion.state & GDK_SHIFT_MASK;
      ctrl = event->motion.state & GDK_CONTROL_MASK;
      buttonNumber = event->button.button;
      args = Py_BuildValue("sddiii", "move",
			   event->motion.x, event->motion.y,
			   buttonNumber, shift, ctrl);
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
    case GDK_SCROLL:
      shift = event->scroll.state & GDK_SHIFT_MASK;
      ctrl = event->scroll.state & GDK_CONTROL_MASK;
      args = Py_BuildValue("sddiii", "scroll",
			   event->scroll.x, event->scroll.y,
			   event->scroll.direction, shift, ctrl);
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

static void rotateCameraAndFocalPoint_(vtkCamera *camera, const Coord3D &pivot,
				      const SmallMatrix &R)
{
  Coord3D cameraPosition(camera->GetPosition());
  Coord3D focalPoint(camera->GetFocalPoint());
  cameraPosition = pivot + R*(cameraPosition - pivot);
  focalPoint = pivot + R*(focalPoint - pivot);
  camera->SetPosition(cameraPosition);
  camera->SetFocalPoint(focalPoint);
}

void OOFCanvas3D::mouse_tumble(double x, double y) {
  assert(mainthread_query());
  if(tumbleAroundFocalPoint) {
    renderer->GetActiveCamera()->Azimuth(last_x - x);
    renderer->GetActiveCamera()->Elevation(y - last_y);
    renderer->GetActiveCamera()->OrthogonalizeViewUp();
  }
  else {
    // TODO: Large changes in elevation sometimes do strange things.
    // Dolly way out and move the Microstructure off towards the left or
    // right side of the canvas, and then violently tumble it by moving
    // the mouse quickly up and down.  The Microstructure will jump to
    // the other side of the canvas.  I assume this has something to do
    // with choosing the wrong quadrant somewhere...

    // Get the rotation angles in radians. The factor converting degrees
    // to radians here is sort of arbitrary, since x and y aren't in
    // degrees, but it does give a reasonable rotation rate.  Making
    // factor much larger makes the tumbling too sensitive to the mouse
    // position, and making it much smaller makes it too sluggish.
    // Perhaps factor should be set so that moving the mouse by the size
    // of the canvas rotates it by a fixed amount.
    double factor = M_PI/180.;
    double dAzimuth = factor*(last_x - x);
    double dElevation = factor*(last_y - y);
    if(dElevation > 0.5*M_PI) dElevation = 0.5*M_PI;
    if(dElevation < -0.5*M_PI) dElevation = -0.5*M_PI;
    vtkCamera *camera = renderer->GetActiveCamera();
    camera->OrthogonalizeViewUp();
    // Rotate by dAzimuth about the view up vector. 
    SmallMatrix R0 = rotateAboutAxis(dAzimuth, camera->GetViewUp());
    rotateCameraAndFocalPoint_(camera, tumbleCenter, R0);
    // If the two rotation matrices are both calculated before
    // applying either of them, then the view up vector will be
    // incorrect for the second rotation, and the rotated object will
    // appear to walk across the screen if the rotations are large.
    // The two rotations have to be applied separately and view up
    // must be recomputed before each.
    camera->OrthogonalizeViewUp();
    // Rotate by dElevation about the normal to the view up vector and
    // the camera's projection direction.
    Coord3D projectionDir(camera->GetDirectionOfProjection());
    Coord3D elevationAxis = cross(projectionDir, camera->GetViewUp());
    SmallMatrix R1 = rotateAboutAxis(dElevation, elevationAxis);
    rotateCameraAndFocalPoint_(camera, tumbleCenter, R1);
  }
  last_x = x;
  last_y = y;
}


void OOFCanvas3D::mouse_track(double x, double y) {
  assert(mainthread_query());

  // TODO OPT: Is there any reason not to always use the focal point?
  // Knowing what's been clicked on is nontrivial and context
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


