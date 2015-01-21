# -*- python -*-
# $RCSfile: buttonlogger.py,v $
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

class ButtonLogger(widgetlogger.WidgetLogger):
    classes = (gtk.Button,)
    def record(self, obj, signal, *args):
        if signal == 'clicked':
            return ["%s.clicked()" % self.location(obj, *args)]
        return super(ButtonLogger, self).record(obj, signal, *args)

class RadioButtonLogger(widgetlogger.WidgetLogger):
    classes = (gtk.RadioButton,)
    def record(self, obj, signal, *args):
        if signal == 'clicked':
            # When a radio button is pressed, two 'clicked' signals
            # are sent, one to deactivate the old button and one to
            # activate the new one.  We only want to log the new one.
            if obj.get_active():
                return ["%s.clicked()" % self.location(obj, *args)]
            return self.ignore
        return super(RadioButtonLogger, self).record(obj, signal, *args)
        
