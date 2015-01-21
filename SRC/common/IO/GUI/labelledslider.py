# -*- python -*-
# $RCSfile: labelledslider.py,v $
# $Revision: 1.20.18.3 $
# $Author: langer $
# $Date: 2014/03/21 20:32:49 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import guitop
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import tooltips
import gtk

class LabelledSlider:
    def __init__(self, value=None, vmin=0, vmax=1, step=0.01, callback=None,
                 name=None, immediate=True, adjustment=None):
        # "callback" is called when the user moves the slider.  If
        # immediate==True, then the callback will be called when any
        # character is typed in the Entry.  If it's false, the
        # callback won't be called until the entry loses focus.
        debug.mainthreadTest()
        self.immediate = immediate

        self.gtk = gtk.HPaned()
        if value is None:
            value = vmin
        if name is not None:
            gtklogger.setWidgetName(self.gtk, name)
        self.adjustment = adjustment or gtk.Adjustment(value=value,
                                             lower=vmin, upper=vmax,
                                             step_incr=step,
                                             page_incr=step)
        self.slider = gtk.HScale(self.adjustment)
        # If an adjustment object has been passed in, presumably it's
        # already been adopted by another widget.
        if not adjustment:
            gtklogger.adoptGObject(self.adjustment, self.slider,
                                   access_method=self.slider.get_adjustment)
        gtklogger.setWidgetName(self.slider, "slider")
        self.slider.set_size_request(100, -1)
        self.gtk.pack1(self.slider, resize=True, shrink=True)
        self.slider.set_draw_value(False)   # we'll display the value ourselves
        self.adjustmentsignal = gtklogger.connect(self.adjustment,
                                                  'value-changed',
                                                  self.text_from_slider)

        self.entry = gtk.Entry()
        gtklogger.setWidgetName(self.entry, "entry")
        self.gtk.pack2(self.entry, resize=True, shrink=True)

        # Make sure that the Entry is big enough to hold the min and
        # max values, or at least 8 digits.
        width = max(len(`vmin`), len(`vmax`), 8)
        self.entry.set_size_request(width*guitop.top().digitsize, -1)

        self.entrysignal = gtklogger.connect(self.entry, 'changed',
                                             self.entry_changed)
        if not adjustment:
            self.set_value(value)
        self.callback = callback
        self.changed = False

        gtklogger.connect(self.entry, 'activate', self.slider_from_text)
        gtklogger.connect(self.entry, 'focus-out-event', self.entry_lost_focus)
    
    def set_sensitive(self, sensitivity):
        self.slider.set_sensitive(sensitivity)
        self.entry.set_sensitive(sensitivity)

    def set_value(self, value):
        # set_value is called by the API, not the GUI, so it should
        # never call the callback function.
        debug.mainthreadTest()
        self.changed = False
        value = max(value, self.adjustment.lower)
        value = min(value, self.adjustment.upper)
        self.adjustmentsignal.block()
        self.entrysignal.block()
        try:
            self.adjustment.value = value
            self.set_entry(value)
        finally:
            self.adjustmentsignal.unblock()
            self.entrysignal.unblock()
            
    def text_from_slider(self, obj):
        debug.mainthreadTest()
        val = self.slider.get_value()
        self.entrysignal.block()
        try:
            self.set_entry(val)
        finally:
            self.entrysignal.unblock()
        self.entry.set_position(0)
        self.changed = False
        if self.callback:
            self.callback(self, val)
    def slider_from_text(self, obj):    # callback for 'activate' from GtkEntry
        debug.mainthreadTest()
        try:
            v0 = self.get_value()
        except:
            # Illegal values will raise an exception, but they
            # may be incomplete entries.  So don't do anything
            # about it here.
            pass
        else:
            self.changed = False
            val = self.clip(v0)
            self.adjustmentsignal.block()
            try:
                self.adjustment.set_value(val)
            finally:
                self.adjustmentsignal.unblock()
            if self.callback:
                self.callback(self, val)
    def entry_lost_focus(self, obj, event):
        if self.changed:
            self.slider_from_text(obj)
    def entry_changed(self, obj):
        if self.immediate:
            self.slider_from_text(obj)
        else:
            self.changed = True
    def clip(self, v):
        v = max(v, self.adjustment.lower)
        v = min(v, self.adjustment.upper)
        return v
    def parameterTableXRef(self, ptable, widgets):
        # Called after a LabelledSlider has been placed in a
        # ParameterTable.  All of the LabelledSliders in the table
        # should have their HPaned adjustments synchronized.
        self.syncsignals = [self.gtk.connect('notify', widget._syncothers)
                            for widget in widgets
                            if (isinstance(widget, LabelledSlider)
                                and widget is not self)]

    def _syncothers(self, pane, gparamspec):
        if gparamspec.name == 'position':
            pos = pane.get_property('position')
            for signal in self.syncsignals:
                self.gtk.handler_block(signal)
            self.gtk.set_position(pos)
            for signal in self.syncsignals:
                self.gtk.handler_unblock(signal)

    def setBounds(self, minval, maxval):
        val = self.adjustment.value
        attop = (val == self.adjustment.upper)
        atbot = (val == self.adjustment.lower)
        self.adjustmentsignal.block()
        try:
            self.adjustment.lower = minval
            self.adjustment.upper = maxval
            if attop:
                self.set_value(maxval)
            elif atbot:
                self.set_value(minval)
        finally:
            self.adjustmentsignal.unblock()

    def getBounds(self):
        return (self.adjustment.lower, self.adjustment.upper)
    
    def set_policy(self, policy):
        # Set how often the callback is called in response to slider
        # motion.  policy should be gtk.UPDATE_CONTINUOUS,
        # gtk.UPDATE_DELAYED, or gtk.UPDATE_DISCONTINUOUS.
        self.slider.set_update_policy(policy)

    def set_tooltips(self, slider=None, entry=None):
        if slider:
            tooltips.set_tooltip_text(self.slider,slider)
        if entry:
            tooltips.set_tooltip_text(self.entry,entry)

class FloatLabelledSlider(LabelledSlider):
    def set_digits(self, digits):
        # Sets number of digits after the decimal place.
        debug.mainthreadTest()
        self.slider.set_digits(digits)
    def set_entry(self, val):
        debug.mainthreadTest()
        self.entry.set_text(("%-8g" % val).rstrip())
    def get_value(self):
        debug.mainthreadTest()
        return self.clip(utils.OOFeval(self.entry.get_text()))


class IntLabelledSlider(LabelledSlider):
    def __init__(self, *args, **kwargs):
        LabelledSlider.__init__(self, *args, **kwargs)
        self.slider.set_digits(0)
    def set_entry(self, val):
        debug.mainthreadTest()
        self.entry.set_text("%d" % int(val))
    def get_value(self):
        debug.mainthreadTest()
        return self.clip(int(utils.OOFeval(self.entry.get_text())))
