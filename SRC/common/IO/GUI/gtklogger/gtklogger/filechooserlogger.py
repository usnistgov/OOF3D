# -*- python -*-
# $RCSfile: filechooserlogger.py,v $
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

class FileChooserLogger(widgetlogger.WidgetLogger):
    classes = (gtk.FileChooserWidget, gtk.FileChooserDialog)
    # Although FileChooserDialog is listed here, it's not really
    # loggable because it doesn't use gtklogger.Dialog as a base
    # class.
    def record(self, obj, signal, *args):
        if signal == "selection-changed":
            filename = obj.get_filename() or ""
            return ["%s.set_filename('%s')" % (self.location(obj, *args),
                                               filename)]
        return super(FileChooserLogger, self).record(obj, signal, *args)
