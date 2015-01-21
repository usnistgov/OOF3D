# -*- python -*-
# $RCSfile: entrylogger.py,v $
# $Revision: 1.2.12.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import gtk
import widgetlogger

class EntryLogger(widgetlogger.WidgetLogger):
    classes = (gtk.Entry,)
    def record(self, obj, signal, *args):
        if signal == 'changed':
            text = obj.get_text().replace('\\', '\\\\')
            return ["%s.set_text('%s')" % (self.location(obj, *args),text)]
        return super(EntryLogger, self).record(obj, signal, *args)
