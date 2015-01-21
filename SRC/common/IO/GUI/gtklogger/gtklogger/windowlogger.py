# -*- python -*-
# $RCSfile: windowlogger.py,v $
# $Revision: 1.3.12.1 $
# $Author: langer $
# $Date: 2013/07/25 20:02:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import widgetlogger
import loggers
import gtk

class WindowLogger(widgetlogger.WidgetLogger):
    classes = (gtk.Window,)
    def record(self, obj, signal, *args):
        # Don't log "destroy" signals, because they're sent for every
        # object that's destroyed, not just the one that initiated the
        # action.
        if signal == 'destroy':
            return self.ignore
        if signal == 'delete-event':

            # Simply re-emitting the delete event doesn't actually
            # destroy a window, so we have to explicitly destroy it.
            # This may be the wrong thing to do if a window intercepts
            # delete-event and doesn't propagate the signal.
            
##            return ["%s.destroy()" % self.location(obj, *args)]
            wvar = loggers.localvar('widget')
            hvar = loggers.localvar('handled')
            return [
                "%s=%s" % (wvar, self.location(obj, *args)),
                "%(h)s=%(w)s.event(event(gtk.gdk.DELETE,window=%(w)s.window))"
                % dict(w=wvar, h=hvar),
                "postpone if not %(h)s: %(w)s.destroy()" % dict(w=wvar, h=hvar),
                    ]
        if signal == 'configure-event':
            event = args[0]
            return ["%s.resize(%d, %d)" % (self.location(obj, *args),
                                          event.width, event.height)]
        return super(WindowLogger, self).record(obj, signal, *args)
