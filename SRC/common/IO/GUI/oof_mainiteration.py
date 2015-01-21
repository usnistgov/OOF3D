# -*- python -*-
# $RCSfile: oof_mainiteration.py,v $
# $Revision: 1.33.2.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:11 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import threadstate
from ooflib.common import debug
from ooflib.common import thread_enable
from ooflib.common.IO.GUI import mainthreadGUI
import gobject
import gtk
import threading

# Thread-safe GTK mainiteration call -- wraps the gtk.mainiteration in
# threads_enter and threads_leave in the appropriate circumstances,
# i.e. when the main thread is in an idle-callback.  This is required
# because both subthreads and idle_callbacks need to acquire the GTK
# lock before making GTK calls.

def mainiteration(block=True):
     debug.mainthreadTest()
     if mainthreadGUI.inside_idle_callback:
          gtk.gdk.threads_enter()
     try:
          gtk.main_iteration(block)
     finally:
          if mainthreadGUI.inside_idle_callback:
               gtk.gdk.threads_leave()

# Looping version, processes the full event queue.  This also
# wraps the events_pending call, which is necessary to prevent
# blocking.
def mainiteration_loop(block=True):
     debug.mainthreadTest()
     if mainthreadGUI.inside_idle_callback:
          gtk.gdk.threads_enter()
     try:
          while gtk.events_pending():
               gtk.main_iteration(block)
     finally:
          if mainthreadGUI.inside_idle_callback:
               gtk.gdk.threads_leave()

