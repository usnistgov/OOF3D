# -*- python -*-
# $RCSfile: panedlogger.py,v $
# $Revision: 1.2.12.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:16 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import gtk
import widgetlogger

## To log the changes in a Paned's divider position, connect (with
## connect_passive, probably) to its 'notify::position' signal.

class PanedLogger(widgetlogger.WidgetLogger):
    classes = (gtk.Paned,)
    def record(self, obj, signal, *args):
        if signal == 'notify::position':
            return ["%s.set_position(%d)" % (self.location(obj, *args),
                                             obj.get_position())]
        return super(PanedLogger, self).record(obj, signal, args)
