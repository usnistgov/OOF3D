# -*- python -*-
# $RCSfile: widgetlogger.py,v $
# $Revision: 1.8.12.1 $
# $Author: langer $
# $Date: 2013/07/29 15:07:33 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import loggers
import gtk
import logutils

import string

class WidgetLogger(loggers.GtkLogger):
    classes = (gtk.Widget,)
    def location(self, widget, *args):
        name = logutils.getWidgetName(widget)
        if not name:
            raise logutils.GtkLoggerException("Unnamed widget")
        path = self._parentWidgetPath(widget) + [name]
        if path[0] not in logutils.getTopWidgetNames():
            raise logutils.GtkLoggerException(string.join(path, ':') + 
                                     " is not contained in a top-level widget")
        return "findWidget('%s')" % string.join(path, ':')
    def _parentWidgetPath(self, widget):
        parent = widget.get_parent()
        while parent is not None and logutils.getWidgetName(parent) is None:
            parent = parent.get_parent()
        if parent is None:
            return []
        return self._parentWidgetPath(parent) + [logutils.getWidgetName(parent)]
    def record(self, obj, signal, *args):
        if signal in ('button-press-event', 'button-release-event'):
            evnt = args[0]
            if signal == 'button-press-event':
                eventname = "BUTTON_PRESS"
            else:
                eventname = "BUTTON_RELEASE"
            wvar = loggers.localvar('widget')
            return [
                "%s = %s" % (wvar, self.location(obj, *args)),
                "%s.event(event(gtk.gdk.%s,x=%20.13e,y=%20.13e,button=%d,state=%d,window=%s.window))"
                % (wvar, eventname,
                   evnt.x, evnt.y, evnt.button, evnt.state, wvar)
                ]
        if signal == 'motion-notify-event':
            evnt = args[0]
            if logutils.suppress_motion_events(obj):
                return self.ignore
            wvar = loggers.localvar('widget')
            return [
                "%s = %s" % (wvar, self.location(obj, *args)),
                "%s.event(event(gtk.gdk.MOTION_NOTIFY,x=%20.13e,y=%20.13e,state=%d,window=%s.window))"
                % (wvar, evnt.x, evnt.y, evnt.state, wvar)
                ]
        if signal == 'focus-in-event':
            wvar = loggers.localvar('widget')
            return [
       "%s=%s" % (wvar, self.location(obj, *args)),
       "%(widget)s.event(event(gtk.gdk.FOCUS_CHANGE, in_=1, window=%(widget)s.window))" % dict(widget=wvar)
                ]
        if signal == 'focus-out-event':
            wvar = loggers.localvar('widget')
            return [
       "%s=%s" % (wvar,self.location(obj, *args)),
       "%(widget)s.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=%(widget)s.window))" % dict(widget=wvar)
                ]
            
        if signal == 'size-allocate':
            alloc = obj.get_allocation()
            parent = obj.get_parent()
            return ["%s.size_allocate(gtk.gdk.Rectangle(%d, %d, %d, %d))" \
                   % (self.location(obj, *args),
                      alloc.x, alloc.y, alloc.width, alloc.height)]
        return super(WidgetLogger, self).record(obj, signal, *args)
