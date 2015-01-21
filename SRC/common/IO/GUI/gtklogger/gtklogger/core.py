# -*- python -*-
# $RCSfile: core.py,v $
# $Revision: 1.15.2.8 $
# $Author: langer $
# $Date: 2014/07/31 18:32:51 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## This file contains the API for gtk_logger.  Nothing outside of this
## file should have to be explicitly called by users.

from ooflib.common import debug
import gtk
import os
import string
import types
import weakref
import loggers
import logutils
import inspect
import checkpoint

_allexceptions = [Exception]

def start(filename, debugLevel=2, suppress_motion_events=True,
          logger_comments=True):
    global _suppress_motion_events
    logutils.set_debugLevel(debugLevel)
    _suppress_motion_events = suppress_motion_events
    #debug.fmsg()
    if logutils.recording():
      #print "gtklogger already recording."
      logutils.logfile().close()
    #else:
      #print "gtklogger recording starting."
    try:
	if logger_comments == True:
            # Open a pipe to the loggergui process for inserting
            # comments into the output stream.
            from GUI import loggergui
            guifile = os.path.abspath(loggergui.__file__)
            # The third argument of '1' to popen indicates that the
            # stream is line buffered.  This ensures that the comments
            # appear in the right place.
            ## TODO 3.1: os.popen is deprecated.  Use subprocess.Popen.
            process = os.popen("python " + guifile + " " + filename, "w", 1)
            logutils.set_logfile(process)
        elif type(filename) is types.StringType:
            logutils.set_logfile(open(filename, "w"))
        else:                   # filename is assumed to be a file
            logutils.set_logfile(filename)
    except:
        logutils.set_logfile(None)
        raise

def stop():
    if logutils.recording():
        try:
	  print "gtklogger recording stopping."
	  logutils.logfile().close()
        finally:
            logutils.set_logfile(None)


# Utility functions to temporarily turn on motion-event recording.

def log_motion_events():
    logutils.log_motion_events()

def dont_log_motion_events():
    logutils.dont_log_motion_events()

def suppress_motion_events():
    return logutils.suppress_motion_events()

def add_exception(excclass):
    logutils.add_exception(excclass)

##################################

# Any gtk.Widget that needs to have its signals logged and replayed
# must have a name, and enough of its widget ancestors must have names
# that the sequence of names uniquely identifies the widget.
# setWidgetName is used to assign the names.

def setWidgetName(widget, name):
    return logutils.setWidgetName(widget, name)

# Top-level widgets (mostly gtk.Windows) must have their names
# assigned by newTopLevelWidget() instead of setWidgetName().

def newTopLevelWidget(widget, name):
    return logutils.newTopLevelWidget(widget, name)

# gtk.GObjects which aren't gtk.Widgets but still need to have their
# signals logged should be registered with adoptGObject(). 'obj' is
# the object being registered.  'parent' is an actual gtk.Widget, and
# 'access_method' is a method of the parent class that retrieves the
# adopted GObject.  For example, to make the gtk.Adjustment that's
# part of a gtk.HRange loggable, call
#    adoptGObject(range.get_adjustment(), range, range.get_adjustment)
# If there's no such parent class method, then use access_function
# instead of access_method.  The function will be called with the
# parent widget as its first argument.  In either case, additional
# arguments to the function can be passed in as access_args or
# access_kwargs.

def adoptGObject(obj, parent, access_method=None, access_function=None,
                 access_args=(), access_kwargs={}):
    assert not hasattr(obj, 'oofparent')
    assert parent is not None
    assert access_method is not None or access_function is not None
    obj.oofparent = parent
    if access_method is not None:
        obj.oofparent_access_method = access_method.__name__
    else:
        obj.oofparent_access_function = access_function.__name__
    obj.oofparent_access_args = access_args
    obj.oofparent_access_kwargs = access_kwargs

# set_submenu should be used instead of gtk.MenuItem.set_submenu.

def set_submenu(menuitem, submenu):
    menuitem.set_submenu(submenu)
    submenu.oofparent = menuitem

# debug_connect makes the connection process very verbose.  It's useful
# if you need to find out what handlers go with which objects.  If you
# uncomment this function, also uncomment the @debug_connect lines
# below.

# def debug_connect(func):
#     def wrapper(obj, signal, *args, **kwargs):
#         guisignals = func(obj, signal, *args, **kwargs)
#         print "debug_connect: obj=", obj, "signal=", signal, \
#             "handlers=", guisignals.signals
#         return guisignals
#     return wrapper

# To have a gtk.GObject's actions logged, use gtklogger.connect or
# gtklogger.connect_after instead of gtk.GObject.connect.  If a widget
# that otherwise would have no callback needs to be logged, use
# gtklogger.connect_passive. 

# @debug_connect
def connect(obj, signal, callback, *args):
    return GUISignals(
        obj,
        obj.connect(signal, CallBackWrapper(signal, callback), *args) # Providing the callback signed to be able to trace for the connect method.
        )

# @debug_connect
def connect_after(obj, signal, callback, *args):
    return GUISignals(
        obj,
        obj.connect_after(signal, CallBackWrapper(signal, callback), *args) # Providing the callback signed to be able to trace for the connect after method.
        )

# connect_passive should be used when an action needs to be logged and
# replayed, but wouldn't otherwise have a callback.  For example,
# keypresses in a gtk.Entry often aren't connected, but still need to
# be logged.

# @debug_connect
def connect_passive(obj, signal, *args):
    return GUISignals(
        obj,
        obj.connect(signal, CallBackWrapper(signal), *args)
        )

# @debug_connect
def connect_passive_after(obj, signal, *args):
    return GUISignals(
        obj,
        obj.connect_after(signal, CallBackWrapper(signal), *args)
        )

class CallBackWrapper(object):
    def __init__(self, signal, callback=None):
        self.callback = callback
        self.signal = signal
    def __call__(self, obj, *args):
        loggers.signalLogger(obj, self.signal, *args)
        if self.callback:
	  self.result = self.callback(obj, *args)
        else:
	  self.result = False
        return self.result

# GUISignals basically just makes it easier to block and unblock
# signals, since the gtk method is sort of klunky.  It used to be more
# important, because gtklogger used to connect *two* signals for each
# call to gtklogger.connect.
class GUISignals:
    def __init__(self, widget, *signals):
        self.signals = signals
        self.alive = True
        self.widget = weakref.ref(widget)
        if isinstance(widget, gtk.Object):
            widget.connect('destroy', self.destroyCB)
    def block(self):
        if self.alive:
            map(self.widget().handler_block, self.signals)
    def unblock(self):
        if self.alive:
            map(self.widget().handler_unblock, self.signals)
    def block_log(self):
        if self.alive:
            self.widget().handler_block(self.signals[0])
    def unblock_log(self):
        if self.alive:
            self.widget().handler_unblock(self.signals[0])
    def disconnect(self):
        if self.alive:
            map(self.widget().disconnect, self.signals)
        self.signals = ()
    def destroyCB(self, *args):
        self.alive = False
    def __repr__(self):
        return "(widget=%s,signals=%s)" % (self.widget, self.signals)

# We need to be able to tell if a dialog is running (see
# GUILogLineRunner in replay.py).  We do that by using a modified
# Dialog class that keeps track of how many dialogs are open.
        
class Dialog(gtk.Dialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        connect_passive(self, 'delete-event')
        connect_passive(self, 'configure-event')
    def run(self):
        logutils.increment_dialog_level()
        try:
            result = super(Dialog, self).run()
        finally:
            logutils.decrement_dialog_level()
        return result
    def add_button(self, name, id):
        # Just to be nice to the programmer, turn on logging for the
        # buttons automatically.  Perhaps this should be optional.
        button = super(Dialog, self).add_button(name, id)
        assert type(name) is types.StringType
        setWidgetName(button, name)
        connect_passive(button, 'clicked')
        return button

# logScrollBars should be called on any ScrolledWindow whose scroll
# bars need to be logged.  It just encapsulates the adoptGObject calls
# that would otherwise be necessary.  It returns a pair of GUISignals
# objects, one for each scroll bar.  The return value can probably be
# ignored in most cases.

def logScrollBars(window, name=None):
    assert isinstance(window, gtk.ScrolledWindow)
    if name is not None:
        setWidgetName(window, name)
    adoptGObject(window.get_hadjustment(), window,
                 access_method=window.get_hadjustment)
    adoptGObject(window.get_vadjustment(), window,
                 access_method=window.get_vadjustment)
    return (
        connect_passive(window.get_hadjustment(), 'value-changed'),
        connect_passive(window.get_vadjustment(), 'value-changed'))



## Test for uniqueness by finding all named widgets and checking that
## findWidget(gtkPath(widget))==widget.

def sanity_check(widget, path=[]):
    widgetname = logutils.getWidgetName(widget)
    if widgetname:
        path = path + [widgetname]
        if logutils.findWidget(string.join(path, ':')) is not widget:
            raise ValueError("%s is not a unique widget name" % path)
    if isinstance(widget, gtk.Container):
        for child in widget.get_children():
            sanity_check(child, path)

def comprehensive_sanity_check():
    for widget in logutils.topwidgets.values():
        sanity_check(widget)
    
