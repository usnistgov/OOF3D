# -*- python -*-
# $RCSfile: parameterwidgets.py,v $
# $Revision: 1.153.2.20 $
# $Author: langer $
# $Date: 2014/10/03 14:29:56 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# GTK widgets for inputting Parameter objects.
from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import primitives
from ooflib.common import strfunction
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import widgetscope
from types import *
import gtk
import string
import sys

############################

class ParameterWidget:
    def __init__(self, gtk, scope=None, name=None, expandable=False,
                 verbose=False, faceless=False):
        debug.mainthreadTest()
        self.gtk = gtk                  # base of gtk widget heirarchy
        self.scope = scope              # WidgetScope containing this widget
        self.faceless = faceless
        self._valid = 0
        # expandable is used when the widget appears in a
        # ParameterTable to indicate if the widget should adjust its
        # y-dimension when the table is resized.  
        self.expandable = expandable

        self.verbose = verbose

        if scope:
            scope.addWidget(self)

        if self.gtk is not None: # can be None for faceless widgets
            self.gtk.connect('destroy', self.destroyCB)
            if name:
                gtklogger.setWidgetName(self.gtk, name)

    # Widgets that contain other widgets must redefine show().  show()
    # must call the show() function of each of the subwidgets, instead
    # of just calling gtk.show_all().  This is because the subwidgets
    # might have parts that shouldn't be shown in all contexts.
    def show(self):
        debug.mainthreadTest()
        if self.gtk is not None:
            self.gtk.show_all()

    # Widget destruction.  Destruction is initiated either when
    # external code calls ParameterWidget.destroy(), or when the gtk
    # widget is destroyed by gtk.  ParameterWidget.cleanUp() can be
    # redefined in derived classes if there's other stuff to be done.
    # The derived classes must then be sure to call the base class
    # cleanUp function.
    def destroy(self):
        debug.mainthreadTest()
        if self.gtk is not None:
            self.gtk.destroy()
    def destroyCB(self, *args):
        self.gtk = None
        self.cleanUp()
    def cleanUp(self):                  # redefine in derived classes
        if self.scope:
            self.scope.removeWidget(self)
            self.scope = None

    # Widget subclasses should call widgetChanged whenever their value
    # changes.  widgetChanged issues a switchboard call when the
    # validity changes.  The "interactive" flag is used to indicate
    # non-programmatic changes -- some widgets need to do extra
    # consistency work in that case.  TODO 3.1: Apparently the only
    # such widget is in the LayerEditorGUI, so this mechanism is not
    # very general.  This may be due to missed opportunities to use
    # it, or it may be that it's not as useful as we thought.
    def widgetChanged(self, validity, interactive):
        if self._valid and not validity:
            self._valid = 0
            switchboard.notify(('validity', self), 0)
        elif not self._valid and validity:
            self._valid = 1
            switchboard.notify(('validity', self), 1)
        switchboard.notify(self, interactive)
    def isValid(self):
        return self._valid
    def __repr__(self):
        return self.__class__.__name__

    # Widgets in a ParameterTable may want to synchronize themselves
    # in some way.  This function is called on all widgets in a
    # ParameterTable after they've all been added.  The arguments are
    # the ParameterTable and the widgets it contains.
    def parameterTableXRef(self, ptable, widgets):
        pass

# GenericWidget is a base class for several other widgets.  It can
# also be created as an instance itself, but currently this is not
# done.
class GenericWidget(ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=None):
        debug.mainthreadTest()
        widget = gtk.Entry()
        widget.set_size_request(10*guitop.top().charsize, -1)
        ParameterWidget.__init__(self, widget, scope=scope, name=name,
                                 verbose=verbose)
        self.signal = gtklogger.connect(widget, 'changed', self.changedCB)
        self.set_value(param.value)
        self.widgetChanged(self.validValue(param.value), interactive=0)
    def get_value(self):
        debug.mainthreadTest()
        text = self.gtk.get_text().lstrip()
        # Derived classes should redefine get_value() to do something
        # sensible, if possible, when there is no input.  They should
        # return None only if the input is invalid (which may or may
        # not be the same as having no input).
        if text:
            return utils.OOFeval(self.gtk.get_text())
        return None
    def set_value(self, newvalue):
        debug.mainthreadTest()
        valuestr = `newvalue`
        self.gtk.set_text(valuestr)
        self.gtk.set_position(0)        # makes MSD visible
    def changedCB(self, gtkobj):
        debug.mainthreadTest()
        self.widgetChanged(self.validValue(self.gtk.get_text()), interactive=1)
    def validValue(self, value):
        # Redefine this in derived classes if necessary.  The argument
        # to validValue is the raw string returned from the widget.
        # It will be run through 'eval' before being used, so the
        # checking here shouldn't be too strict.  In most cases it's
        # sufficient to check that the string isn't empty.  ACTUALLY,
        # validValue is also called from the widget constructor, where
        # the value passed is *not* the raw string.  So validValue()
        # must accept either a raw string or an instance of the class
        # that the widget represents.  TODO 3.1: This is rather
        # ugly, particularly in the subclasses.  This function should
        # either do the oofeval if it gets a string, or be broken up
        # into "validStringValue" and "validParameterValue" or
        # something similar.
        return value is not None and string.lstrip(value) != ""

    # GenericWidgets are sometimes included in other widgets with fake
    # parameters, which may need control over the emission of the
    # 'changed' signal.  (See matrixparamwidgets.py, for example.)
    # The need for these functions indicates that widgets *shouldn't*
    # be nested like this.
    def block_signal(self):
        debug.mainthreadTest()
        self.signal.block()
    def unblock_signal(self):
        debug.mainthreadTest()
        self.signal.unblock()

#########################

# StringParameter widget is almost a GenericWidget.
# It removes leading spaces from the result.

class StringWidget(GenericWidget):
    def get_value(self):
        debug.mainthreadTest()
        return self.gtk.get_text().lstrip()
    def set_value(self, value):
        debug.mainthreadTest()
        if type(value) == StringType and string.lstrip(value) != "":
            self.gtk.set_text(value)
            self.widgetChanged(1, interactive=0)
        else:
            self.gtk.set_text("")
            self.widgetChanged(0, interactive=0)

def _StringParameter_makeWidget(self, scope=None, verbose=False):
    return StringWidget(self, scope=scope, name=self.name, verbose=verbose)

parameter.StringParameter.makeWidget = _StringParameter_makeWidget

class RestrictedStringWidget(StringWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.exclude = param.exclude
        StringWidget.__init__(self, param, scope, name, verbose)
    def validValue(self, value):
        for x in self.exclude:
            if x in value:
                return False
        return StringWidget.validValue(self, value)

def _RSParam_makeWidget(self, scope=None, verbose=False):
    return RestrictedStringWidget(self, scope=scope,name=self.name,
                                  verbose=verbose)

parameter.RestrictedStringParameter.makeWidget = _RSParam_makeWidget
        
#########################

from ooflib.common.IO import automatic

# AutoWidget sets up and handles the basic geometry of automatic
# widgets -- puts in the checkbox, hooks up signals, etc.  Does not
# talk to the parameter, because AutoNameWidgets have special
# requirements for these.

## TODO OPT: Instead of using a checkbox, could the AutoWidgets contain
## only a gtk.Entry?  If the Entry is empty, the Widget's value would
## be 'automatic'.  The empty widget could display 'automatic' in
## grayed out text.  This would only work if an empty string is never
## a legal value for an automatic parameter.

class AutoWidget(ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        ParameterWidget.__init__(self, gtk.HBox(), scope=scope, name=name,
                                 verbose=verbose)
        self.autocheck = gtk.CheckButton()
        gtklogger.setWidgetName(self.autocheck, 'Auto')
        self.text = gtk.Entry()
        gtklogger.setWidgetName(self.text, 'Text')
        self.gtk.pack_start(self.autocheck, expand=0, fill=0)
        self.gtk.pack_start(self.text, expand=1, fill=1)
        gtklogger.connect(self.autocheck, "clicked", self.checkCB)
        self.textsignal = gtklogger.connect(self.text, 'changed', self.entryCB)
        
    def checkCB(self, gtkobj):
        debug.mainthreadTest()
        if self.autocheck.get_active():
            self.textsignal.block()
            self.text.set_editable(1)
            self.text.set_sensitive(1)
            self.text.set_text("")
            self.textsignal.unblock()
            self.widgetChanged(0, interactive=1)
        else:
            self.textsignal.block()
            self.text.set_editable(0)
            self.text.set_sensitive(0)
            self.text.set_text("automatic")
            self.textsignal.unblock()
            self.widgetChanged(1, interactive=1)

    def entryCB(self, entry):
        debug.mainthreadTest()
        self.widgetChanged(self.autocheck.get_active() and
                           self.validText(self.text.get_text()),
                           interactive=1)

    def validText(self, x):             # override in subclass
        return x != "" and x is not None

    def get_value(self):
        debug.mainthreadTest()
        if not self.autocheck.get_active():
            return automatic.automatic
        return self.text.get_text()

    def set_value(self, newvalue):
        debug.mainthreadTest()
        if newvalue is automatic.automatic:
            self.autocheck.set_active(0)
            self.checkCB(self.autocheck)
            self.widgetChanged(1, interactive=0)
        elif newvalue is None or newvalue == '':
            self.autocheck.set_active(1)
            self.checkCB(self.autocheck)
            self.text.set_text('')
            self.widgetChanged(0, interactive=0)
        else:
            self.autocheck.set_active(1)
            self.checkCB(self.autocheck)
            self.text.set_text(`newvalue`)
            self.text.set_position(0)
            self.widgetChanged(1, interactive=0)
    
class AutoNameWidget(AutoWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        AutoWidget.__init__(self, param, scope=scope, name=name, 
                            verbose=verbose)
        # Avoid querying param.value here, as it will trigger the
        # autoname resolution process if the parameter is an
        # AutomaticNameParameter or ContextualNameParameter.
        if param.automatic():
            self.set_value(automatic.automatic)
            self.widgetChanged(1, interactive=0)
        else:
            self.set_value(param.truevalue)
            self.widgetChanged(self.validText(param.truevalue), interactive=0)
        tooltips.set_tooltip_text(self.autocheck,
            'Switch between typed names and automatically generated names.')

    # AutoNameWidget's set-value doesn't take the repr of the value,
    # since it's a string -- just put it in directly.
    def set_value(self, newvalue):
        debug.mainthreadTest()
        ## TODO 3.1: When the parameter has been set to an automatic value
        ## from a script, the widget is subsequently initialized with
        ## the non-automatic string generated from the automatic
        ## value, because AutomaticNameParameter.value always returns
        ## the resolved name.  However, the widget should still be
        ## initialized to 'automatic' somehow.
        if newvalue is automatic.automatic:
            self.autocheck.set_active(0)
            self.checkCB(self.autocheck)
            self.widgetChanged(1, interactive=0)
        elif newvalue is None or newvalue == '':
            self.autocheck.set_active(1)
            self.checkCB(self.autocheck)
            self.text.set_text('')
            self.widgetChanged(0, interactive=0)
        else:
            self.autocheck.set_active(1)
            self.checkCB(self.autocheck)
            self.text.set_text(newvalue)
            self.text.set_position(0)
            self.widgetChanged(1, interactive=0)
    
def _AutoNameParameter_makeWidget(self, scope, verbose=False):
    return AutoNameWidget(self, scope=scope, name=self.name, verbose=verbose)
parameter.AutomaticNameParameter.makeWidget = _AutoNameParameter_makeWidget

class RestrictedAutoNameWidget(AutoNameWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.exclude = param.exclude
        AutoNameWidget.__init__(self, param, scope, name, verbose=verbose)
    def validText(self, x):
        if not x:
            return False
        for c in self.exclude:
            if c in x:
                return False
        return True

def _RestrictedAutoNameParam_makeWidget(self, scope, verbose=False):
    return RestrictedAutoNameWidget(self, scope=scope, name=self.name,
                                    verbose=verbose)
parameter.RestrictedAutomaticNameParameter.makeWidget = \
                                         _RestrictedAutoNameParam_makeWidget
#########################

# Allows a value of "automatic", or an integer.
class AutoNumberWidget(AutoWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        AutoWidget.__init__(self, param, scope=scope, name=name, 
                            verbose=verbose)
        self.set_value(param.value)
        self.widgetChanged(1, interactive=0)
        tooltips.set_tooltip_text(self.autocheck,
            "Switch between automatic and integer.")

    # The AutoWidget get_value returns automatic or a string, or none.
    # If we get a string, evaluate it and return the result.
    def get_value(self):
        v = AutoWidget.get_value(self)
        if v==automatic.automatic:
            return v
        return utils.OOFeval(v)
        

def _AutoNumberWidget_makeWidget(self, scope, verbose=False):
    return AutoNumberWidget(self, scope=scope, name=self.name, verbose=verbose)

parameter.AutoIntParameter.makeWidget = _AutoNumberWidget_makeWidget

parameter.AutoNumericParameter.makeWidget = _AutoNumberWidget_makeWidget
    

#########################

class BooleanWidget(ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        if param.value:
            labelstr = 'true'
        else:
            labelstr = 'false'
        self.label = gtk.Label(labelstr)
        ParameterWidget.__init__(self, gtk.Frame(), scope=scope, 
                                 verbose=verbose)
        self.button = gtk.CheckButton()
        self.gtk.add(self.button)
        self.button.add(self.label)
        # name is assigned to the button, not the frame, because it's
        # the button that gets connected.
        gtklogger.setWidgetName(self.button, name)
        self.signal = gtklogger.connect(self.button, 'clicked', self.buttonCB)
        self.set_value(param.value)
    def get_value(self):
        debug.mainthreadTest()
        return self.button.get_active()
    def set_value(self, newvalue):
        debug.mainthreadTest()
        self.signal.block()
        if newvalue:
            self.button.set_active(1)
        else:
            self.button.set_active(0)
        self.signal.unblock()
        self.widgetChanged(1, interactive=0)
    def buttonCB(self, obj):
        debug.mainthreadTest()
        if self.button.get_active():
            self.label.set_text('true')
        else:
            self.label.set_text('false')
        self.widgetChanged(1, interactive=1)

def _Boolean_makeWidget(self, scope, verbose=False):
    return BooleanWidget(self, scope=scope, name=self.name, verbose=verbose)
parameter.BooleanParameter.makeWidget = _Boolean_makeWidget

##########################

from ooflib.common.IO.GUI import labelledslider

# The order of the base classes for IntRangeWidget and
# FloatRangeWidget is important.  All of the base classes define
# parameterTableXRef, but the one in ParameterWidget is just a stub.

class IntRangeWidget(labelledslider.IntLabelledSlider, ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        if param.value is not None:
            val = param.value
        else:
            val = param.range[0]
        labelledslider.IntLabelledSlider.__init__(self, val,
                                               vmin=param.range[0],
                                               vmax=param.range[1],
                                               step=1,
                                               callback=self.sliderCB)
        ParameterWidget.__init__(self, self.gtk, scope=scope, name=name,
                                 verbose=verbose)
        self.widgetChanged(1, interactive=0) # always valid
    def sliderCB(self, slider, val):
        debug.mainthreadTest()
        self.widgetChanged(1, interactive=1)

def _IntRange_makeWidget(self, scope, verbose=False):
    return IntRangeWidget(self, scope=scope, name=self.name, verbose=verbose)

parameter.IntRangeParameter.makeWidget = _IntRange_makeWidget


class FloatRangeWidget(labelledslider.FloatLabelledSlider, ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        if param.value is not None:
            val = param.value
        else:
            val = param.range[0]
        labelledslider.FloatLabelledSlider.__init__(self, val,
                                               vmin=param.range[0],
                                               vmax=param.range[1],
                                               step=param.range[2],
                                               callback=self.sliderCB)
        ParameterWidget.__init__(self, self.gtk, scope=scope, name=name,
                                 verbose=verbose)
        self.widgetChanged(1, interactive=0) # always valid
    ## FloatRangeWidget uses LabelledSlider's get_value()
    def sliderCB(self, slider, val):
        self.widgetChanged(1, interactive=1)

def _FloatRange_makeWidget(self, scope=None, verbose=False):
    return FloatRangeWidget(self, scope=scope, name=self.name, verbose=verbose)
parameter.FloatRangeParameter.makeWidget = _FloatRange_makeWidget

##############################################

class FloatWidget(GenericWidget):
    def get_value(self):
        x = GenericWidget.get_value(self)
        if x is not None:
            # This doesn't have to convert the data to a Float,
            # because the GenericWidget eval's its input.
            return x
        return 0.0
    def validValue(self, val):
#         # Any string is a potentially valid value
#         return 1
        try:
            if type(val) is StringType:
                return type(1.0*utils.OOFeval(val)) is FloatType
            else:
                return isinstance(val, (FloatType, IntType))
        except:
            return False
    def set_value(self, newvalue):
        GenericWidget.set_value(self, 1.0*newvalue)

def _FloatParameter_makeWidget(self, scope=None, verbose=False):
    return FloatWidget(self, scope=scope, name=self.name, verbose=verbose)
parameter.FloatParameter.makeWidget = _FloatParameter_makeWidget

class PositiveFloatWidget(FloatWidget):
    def validValue(self, val):
        try:
            if type(val) is StringType:
                fval = 1.0*utils.OOFeval(val)
                return type(fval) is FloatType and fval > 0.0
            else:
                return isinstance(val, (FloatType, IntType)) and val > 0.0
        except:
            return False

def _PositiveFloatParameter_makeWidget(self, scope=None, verbose=False):
    return PositiveFloatWidget(self, scope=scope, name=self.name, 
                               verbose=verbose)
parameter.PositiveFloatParameter.makeWidget = _PositiveFloatParameter_makeWidget

class NonNegativeFloatWidget(FloatWidget):
    def validValue(self, val):
        try:
            if type(val) is StringType:
                fval = 1.0*utils.OOFeval(val)
                return type(fval) is FloatType and fval >= 0.0
            else:
                return isinstance(val, (FloatType, IntType)) and val >= 0.0
        except:
            return False

def _NonNegativeFloatParameter_makeWidget(self, scope=None, verbose=False):
    return NonNegativeFloatWidget(self, scope=scope, name=self.name, 
                               verbose=verbose)
parameter.NonNegativeFloatParameter.makeWidget = _NonNegativeFloatParameter_makeWidget

class ListOfFloatsWidget(GenericWidget):
    # See comments in FloatWidget
    def get_value(self):
        x = GenericWidget.get_value(self)
        if x is not None:
            return x
        return []
    def validValue(self, string):
        return 1

def _ListOfFloatsParameter_makeWidget(self, scope=None, verbose=False):
    return ListOfFloatsWidget(self, scope=scope, name=self.name,
                              verbose=verbose)
parameter.ListOfFloatsParameter.makeWidget = _ListOfFloatsParameter_makeWidget

#########################

class IntWidget(GenericWidget):
    # See comments in FloatWidget
    def get_value(self):
        x = GenericWidget.get_value(self)
        if x is not None:
            return x
        return 0
    def validValue(self, val):
#        return 1
        try:
            if type(val) is StringType:
                return type(utils.OOFeval(val)) is IntType
            else:
                return isinstance(val, IntType)
        except:
            return False
def _IntParameter_makeWidget(self, scope=None, verbose=False):
    return IntWidget(self, scope=scope, name=self.name, verbose=verbose)

parameter.IntParameter.makeWidget = _IntParameter_makeWidget

#######################

class XYStrFunctionWidget(GenericWidget):
    def get_value(self):
        debug.mainthreadTest()
        return strfunction.XYStrFunction(self.gtk.get_text().lstrip())
    def set_value(self, newvalue):
        debug.mainthreadTest()
        if newvalue is not None:
            self.gtk.set_text(newvalue.funcstr)
        else:
            self.gtk.set_text('')
    def validValue(self, value):
        if type(value) is StringType:
            try:
                fn = strfunction.XYStrFunction(value)
                return True
            except:
                return False
        return isinstance(value, strfunction.XYStrFunction)
            
def _XYStrFunctionParameter_makeWidget(self, scope=None, verbose=False):
    return XYStrFunctionWidget(self, scope=scope, name=self.name, 
                               verbose=verbose)
        
strfunction.XYStrFunctionParameter.makeWidget = \
                                              _XYStrFunctionParameter_makeWidget

class XYTStrFunctionWidget(GenericWidget):
    def get_value(self):
        debug.mainthreadTest()
        return strfunction.XYTStrFunction(self.gtk.get_text().lstrip())
    def set_value(self, newvalue):
        debug.mainthreadTest()
        if newvalue is not None:
            self.gtk.set_text(newvalue.funcstr)
        else:
            self.gtk.set_text('')
    def validValue(self, value):
        if type(value) is StringType:
            try:
                fn = strfunction.XYTStrFunction(value)
                return True
            except:
                return False
        return isinstance(value, strfunction.XYTStrFunction)
            
def _XYTStrFunctionParameter_makeWidget(self, scope=None, verbose=None):
    return XYTStrFunctionWidget(self, scope=scope, name=self.name,
                                verbose=verbose)
        
strfunction.XYTStrFunctionParameter.makeWidget = \
                                           _XYTStrFunctionParameter_makeWidget

############################################

class ParameterTable(ParameterWidget, widgetscope.WidgetScope):
    # A table of Parameter Widgets
    def __init__(self, params, scope=None, name=None, showLabels=True, data={},
                 verbose=False):
        debug.mainthreadTest()
        widgetscope.WidgetScope.__init__(self, scope)
        for key, value in data.items():
            self.setData(key, value)
        self.params = params            # list of Parameters
        if self.params:
            base = gtk.Table(rows=len(params), columns=2)
        else:
            base = gtk.VBox()
        ParameterWidget.__init__(self, base, scope, name, verbose=verbose)
        self.showLabels = showLabels
        self.labels = []
        self.widgets = []
        self.sbcallbacks = []           # switchboard callbacks
        self.subscopes = []             # Widgetscopes for ParameterGroups
        self.set_values()
        self.show()
##        self.base_value = None # Original, pre-selection value, in base form.

    def set_values(self):
        self.labels = []
        self.widgets = []
        self.validities = [0]*len(self.params)
        self.destroySubScopes()
        self.makeWidgets()
        self.show()
        self.signal(interactive=False)

    def makeWidgets(self):
        debug.mainthreadTest()
        subscopedict = {}
        self.expandable = False
        for i, param in enumerate(self.params):
            if param.group is None:
                scope = self
            else:
                # Get or make a WidgetScope for this ParameterGroup
                try:
                    scope = subscopedict[param.group]
                except KeyError:
                    scope = widgetscope.WidgetScope(self)
                    self.subscopes.append(scope)
                    subscopedict[param.group] = scope
            self.makeSingleWidget(param, i, scope)
        # Allow widgets to synchronize themselves, if they so desire.
        for widget in self.widgets:
            widget.parameterTableXRef(self, self.widgets)

    def makeSingleWidget(self, param, tablepos, scope):
        debug.mainthreadTest()
        # if self.verbose:
        #     debug.fmsg("Making widget for", param)
        widget = param.makeWidget(scope=scope, verbose=self.verbose)
        if self.verbose:
            # debug.fmsg("Made widget.")
            widget.verbose = True
        self.widgets.append(widget)

        # if self.verbose:
        #     debug.fmsg("requesting callback 2")
        self.sbcallbacks.append(
            switchboard.requestCallbackMain(widget, self.widgetChangeCB,
                                            verbose=self.verbose))
        # if self.verbose:
        #     debug.fmsg("requesting callback 1")
        self.sbcallbacks.append(
            switchboard.requestCallbackMain(('validity', widget), self.vcheck,
                                            tablepos, verbose=self.verbose))
            
        # if self.verbose:
        #     print >> sys.stderr, "makeSingleWidget: requested callbacks"
             # debug.fmsg("requested callbacks")
        self.validities[tablepos] = widget.isValid()
        # if self.verbose:
        #     debug.fmsg("validity =", self.validities[tablepos])

        if widget.faceless:
            return

        label = gtk.Label(param.name + ' =')
        label.set_alignment(1.0, 0.5)
        self.labels.append(label)
        if param.tip:
            tooltips.set_tooltip_text(label,param.tip)
        if widget.expandable:
            yoptions = gtk.EXPAND | gtk.FILL
            self.expandable = True
        else:
            yoptions = 0
        if self.showLabels:
            self.gtk.attach(label, 0, 1, tablepos, tablepos+1, xpadding=5,
                            xoptions=gtk.FILL, yoptions=yoptions)
        self.gtk.attach(widget.gtk, 1, 2, tablepos, tablepos+1, xpadding=5,
                        xoptions=gtk.EXPAND|gtk.FILL, yoptions=yoptions)
        # if self.verbose:
        #     debug.fmsg("done")
    def get_values(self):
        debug.mainthreadTest()
        exceptions = []
        for param, widget in zip(self.params, self.widgets):
            # Get as many values as possible, even if setting some of them
            # causes errors.
            try:
                val = widget.get_value()
                param.value = val
            except (Exception, ooferror.ErrError), exception:
                exceptions.append(exception)
        if exceptions:
            raise exceptions[0]
    def vcheck(self, widgetnumber, validity):
        # callback for ('validity', widget).  This just stores the
        # validity value.  The subsequent widget changed switchboard
        # call actually broadcasts the new validity by calling
        # widgetChanged.
        self.validities[widgetnumber] = validity
    def widgetChangeCB(self, interactive):
        self.signal(interactive)
    def signal(self, interactive):
        for v in self.validities:
            if not v:
                # self.dumpValidity()
                self.widgetChanged(False, interactive)
                return
        self.widgetChanged(True, interactive)
    def dumpValidity(self):
        debug.fmsg(zip([p.name for p in self.params], self.validities))
    def dumpValues(self):
        debug.fmsg(*["%s=%s" % (p.name, p.value) for p in self.params])
    def show(self):
        # Don't simply run self.gtk.show_all(), because it might show
        # too much of some child widgets.
        debug.mainthreadTest()
        for widget in self.widgets:
            widget.show()
        for label in self.labels:
            label.show_all()
        self.gtk.show()
    def cleanUp(self):
        # Make sure we don't have any circular references...
        map(switchboard.removeCallback, self.sbcallbacks)
        self.params = []
        self.widgets = []
        ParameterWidget.cleanUp(self)
        self.destroyScope()
        self.destroySubScopes()
    def destroySubScopes(self):
        for scope in self.subscopes:
            scope.destroyScope()
        self.subscopes = []


class HierParameterTable(ParameterTable):
    # ParameterTable that takes a hierarchical list of Parameters, and
    # puts them in a table with WidgetScopes defined for each level of
    # the hierarchy.  The hierarchical list is just a list of lists of
    # lists of Parameters, with arbitrarily deep nesting.
    ## TODO OPT: Is this necessary, now that ParameterGroups can be nested?
    def __init__(self, params, scope=None, verbose=False):
        self.paramhier = params
        ParameterTable.__init__(self, utils.flatten_all(params), scope,
                                verbose=verbose)
    def makeWidgets(self):
        debug.mainthreadTest()
        tablepos = 0
        self._doMakeWidgets(self, tablepos, self.paramhier)
        # Allow widgets to synchronize themselves, if they so desire.
        for widget in self.widgets:
            widget.parameterTableXRef(self, self.widgets)
    def _doMakeWidgets(self, scope, tablepos, phier):
        for obj in phier:  
            if isinstance(obj, parameter.Parameter):
                self.makeSingleWidget(obj, tablepos, scope)
                tablepos += 1
            else:                       # obj is a hierarchical list of params
                # Only thing to phier is phier itself...
                subscope = widgetscope.WidgetScope(scope)
                tablepos = self._doMakeWidgets(subscope, tablepos, obj)
        return tablepos
                
#####################################################################

# Modal dialog for setting Parameters

class ParameterDialog(widgetscope.WidgetScope):
    OK = 1
    CANCEL = 2
    def __init__(self, *parameters, **kwargs):
        debug.mainthreadTest()
        # A title for the dialog box can be specified by a REQUIRED
        # 'title' keyword argument.  A WidgetScope can be specified
        # with a 'scope' keyword.  If a parent window is specified
        # with the 'parentwindow' argument, the dialog will be brought
        # up as a transient window for it.
        try:
            scope = kwargs['scope']
        except KeyError:
            scope = None
        widgetscope.WidgetScope.__init__(self, scope)
        
        try:
	    hidden_params = kwargs['hidden_params']
	    for who_param in hidden_params:
		self.addWidget(who_param.makeWidget(scope=self))
	except KeyError:
            pass
	  
        try:
            data_dict = kwargs['dialog_data']
        except KeyError:
            pass
        else:
            self.__dict__.update(data_dict)

        try:
            parentwindow = kwargs['parentwindow']
        except KeyError:
            parentwindow=None

        try:
            scopedata = kwargs['data']
        except KeyError:
            pass
        else:
            for key,value in scopedata.items():
                self.setData(key, value)
            
        self.parameters = parameters
        self.dialog = gtklogger.Dialog(parent=parentwindow,
                                       flags=gtk.DIALOG_MODAL)
        self.dialog.set_keep_above(True)
        try:
            title = kwargs['title']
        except KeyError:
            raise ooferror.ErrPyProgrammingError("Untitled dialog!")
        gtklogger.newTopLevelWidget(self.dialog, 'Dialog-'+kwargs['title'])
        
        try:
            toplabel = gtk.Label(kwargs['topmessage'])
            toplabel.set_line_wrap(True)
        except KeyError:
            toplabel = None
            
        try:
            bottommlabel = gtk.Label(kwargs['bottommessage'])
            bottommlabel.set_line_wrap(True)
        except KeyError:
            bottommlabel = None

        self.dialog.set_title(title)
        if toplabel != None:
	   self.dialog.vbox.pack_start(toplabel)
	   toplabel.show()
        hbox = gtk.HBox()
        self.dialog.vbox.pack_start(hbox, expand=0, fill=0, padding=5)
        hbox.pack_start(gtk.Label(title), expand=1, fill=1, padding=10)

        self._button_hook()

        self.table = ParameterTable(self.parameters, scope=self)
        
        self.sbcallback = switchboard.requestCallbackMain(
            ('validity', self.table),
            self.validityCB)
        self.dialog.vbox.pack_start(self.table.gtk,
                                    expand=self.table.expandable,
                                    fill=True)
        if bottommlabel != None:
	   self.dialog.vbox.pack_start(bottommlabel)
	   bottommlabel.show()                       
        self.response = None
        self.sensitize()


    # Separate draw routine, overridden in subclasses.
    def _button_hook(self):
        debug.mainthreadTest()
        okbutton = self.dialog.add_button(gtk.STOCK_OK, self.OK)
        cancelbutton = self.dialog.add_button(gtk.STOCK_CANCEL, self.CANCEL)
        self.dialog.set_default_response(self.OK)
 
    def run(self):
        debug.mainthreadTest()
        self.table.show()
        return self.dialog.run()        # shows dialog & makes it modal
    def close(self):
        debug.mainthreadTest()
        switchboard.removeCallback(self.sbcallback)
        self.dialog.destroy()
        self.destroyScope()
    def get_values(self):
        self.table.get_values()
    def validityCB(self, validity):     # sb callback from ParameterTable
        self.sensitize()
    def sensitize(self):
        debug.mainthreadTest()
        self.dialog.set_response_sensitive(self.OK, self.table.isValid())
    def hide(self):
        debug.mainthreadTest()
        self.dialog.hide()

def getParameters(*params, **kwargs):
    # Given a bunch of Parameters, create a dialog box for setting
    # them.  If the function returns 1, then the parameters have been
    # set and their values can be extracted by the calling routine.
    # kwargs can contain 'title', 'scope', and 'data' arguments.
    # 'data' is a dict of values to be stored as the dialog's
    # widgetscope's data.  See WidgetScope.setData.
    dialog = ParameterDialog(*params, **kwargs)
    # dialog.table.dumpValidity()
    result = dialog.run()
    
    if result in (ParameterDialog.CANCEL,
                  gtk.RESPONSE_DELETE_EVENT,
                  gtk.RESPONSE_NONE):
        dialog.close()
        return None
    try:
        dialog.get_values()
        return 1
    finally:
        dialog.close()


def getParameterValues(*params, **kwargs):
    # This version of getParameters extracts and returns the Parameter
    # values, or returns None if they haven't been set. kwargs can
    # contain 'title' and 'scope' arguments.
    if getParameters(*params, **kwargs):
        return [p.value for p in params]

#####################################################################

class PersistentParameterDialog(ParameterDialog):
    OK = 1
    APPLY = 2
    CANCEL = 3
    def _button_hook(self):
        debug.mainthreadTest()
        okbutton = self.dialog.add_button(gtk.STOCK_OK, self.OK)
        applybutton = self.dialog.add_button(gtk.STOCK_APPLY, self.APPLY)
        cancelbutton = self.dialog.add_button(gtk.STOCK_CANCEL, self.CANCEL)
        self.dialog.set_default_response(self.OK)
    def sensitize(self):
        debug.mainthreadTest()
        ParameterDialog.sensitize(self)
        self.dialog.set_response_sensitive(self.APPLY, self.table.isValid())

# This function passes the params and kwargs on to a persistent
# parameter dialog box, which it leaves up until it gets OK or some
# cancellation event.  Any affirmative event (OK or APPLY) cause the
# passed-in menu item to be run with the provided defaults, via
# menuitem.callWithDefaults(**defaults).  OK events close the dialog,
# APPLY events cause the dialog to persist.
def persistentMenuitemDialog(menuitem, defaults, *params, **kwargs):
    rerun = True
    count = 0
    dialog = PersistentParameterDialog(*params,**kwargs)
    while rerun:
        result = dialog.run()
        if result in (PersistentParameterDialog.CANCEL,
                      gtk.RESPONSE_DELETE_EVENT,
                      gtk.RESPONSE_NONE):
            rerun = False
        elif result==PersistentParameterDialog.OK:
            try:
                dialog.get_values()
            finally:
                rerun = False
            menuitem.callWithDefaults(**defaults)
            count += 1
        else: #  result==PersistentParameterDialog.APPLY
            dialog.get_values()
            menuitem.callWithDefaults(**defaults)
            count += 1
    dialog.close()
    
    return count

def transientMenuItemDialog(menuitem, defaults, *params, **kwargs):
    dialog = ParameterDialog(*params, **kwargs)
    result = dialog.run()
    if result == ParameterDialog.OK:
        dialog.get_values()
        menuitem.callWithDefaults(**defaults)
    dialog.close()

#####################################################################

from ooflib.common.IO.GUI import chooser

# Widget base class for subclasses of the Enum class.
class EnumWidget(ParameterWidget):
    def __init__(self, enumclass, param, scope=None, name=None, verbose=False):
        self.enumclass = enumclass
        nameset = list(self.enumclass.names)
        self.widget = chooser.ChooserWidget(nameset, self.selection,
                                            helpdict=self.enumclass.helpdict,
                                            name=name)
        if param.value is not None:
            self.set_value(param.value)
        else:
            self.set_value(enumclass(enumclass.names[0]))
        self.sbcallback = switchboard.requestCallbackMain(enumclass,
                                                          self.update)
        ParameterWidget.__init__(self, self.widget.gtk, scope=scope,
                                 verbose=verbose)
        self.widgetChanged(len(nameset) > 0, interactive=0)
    def update(self):
        self.widget.update(list(self.enumclass.names), self.enumclass.helpdict)
        self.widgetChanged(len(self.enumclass.names) > 0, interactive=0)
    def selection(self, gtkobj, name):
        self.value = self.enumclass(name)
        self.widgetChanged(validity=1, interactive=1)
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
        self.widget.set_state(value.name)
    def cleanUp(self):
        switchboard.removeCallback(self.sbcallback)
        ParameterWidget.cleanUp(self)
    
def _EnumParameter_makeWidget(self, scope=None, verbose=False):
    return EnumWidget(self.enumclass, self, scope=scope, name=self.name,
                      verbose=verbose)

enum.EnumParameter.makeWidget = _EnumParameter_makeWidget


#######################################################################

# ValueSetParameter is valid if it's a nontrivial string, or if
# it's a positive integer, or if it's a tuple of things that can
# be converted to floats.
class ValueSetParameterWidget(GenericWidget):
    def validValue(self, value):
        if value is None:
            return 0
        if type(value) is StringType:
            if string.lstrip(value)=="":
                return 0
            return 1 # Nontrival strings are OK.
        
        if type(value) is IntType and value>0:
            return 1 # Ints greater than zero are OK.

        if type(value) is TupleType:
            for v in value:
                try:
                    x = float(v)
                except ValueError:
                    return 0
            return 1


def _makeVSPWidget(self, scope=None, verbose=False):
    return ValueSetParameterWidget(self, scope=scope, name=self.name,
                                   verbose=verbose)

parameter.ValueSetParameter.makeWidget = _makeVSPWidget

class AutomaticValueSetParameterWidget(AutoWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        AutoWidget.__init__(self, param, scope=scope, name=name, 
                            verbose=verbose)
        self.set_value(param.value)
        tooltips.set_tooltip_text(self.autocheck,
            "Switch between typed level specifications and automatic generation of levels.")

    def validValue(self, value):
        if value is None:
            return 0
        if type(value) is StringType:
            if string.lstrip(value)=="":
                return 0
            return 1
        
        if type(value) is IntType and value>0:
            return 1

        if value == automatic.automatic:
            return 1

        if type(value) is TupleType:
            for v in value:
                try:
                    x = float(v)
                except ValueError:
                    return 0
            return 1

    # Similarly to the AutoNumber widget, if we don't get automatic,
    # we should evaluate our text-string to get a result.
    def get_value(self):
        v = AutoWidget.get_value(self)
        if v==automatic.automatic:
            return v
        return utils.OOFeval(v)

def _makeAVSPWidget(self, scope=None, verbose=False):
    return AutomaticValueSetParameterWidget(self, scope=scope, name=self.name,
                                            verbose=verbose)

parameter.AutomaticValueSetParameter.makeWidget = _makeAVSPWidget

#######################################################################

class PointWidget(ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        table = gtk.Table(rows=config.dimension(), columns=2)
        frame.add(table)

        labels = "xyz"
        self.componentWidgets = []
        self.sbcallbacks = []
        for i in range(config.dimension()):
            label = gtk.Label(labels[i]+':')
            label.set_alignment(1.0, 0.5)
            table.attach(label, 0,1, i,i+1, xpadding=3,
                         xoptions=gtk.FILL, yoptions=0)
            p = parameter.FloatParameter(labels[i], 0.0) 
            widget = FloatWidget(p, name=labels[i]+"Componenent")
            self.componentWidgets.append(widget)
            table.attach(widget.gtk, 1,2, i,i+1, xpadding=3,
                         xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
            self.sbcallbacks.append(
                switchboard.requestCallbackMain(widget,
                                                self.widgetChangeCB))
        ParameterWidget.__init__(self, frame, scope=scope, name=name,
                                 verbose=verbose)
        self.set_value(param.value)
        valid = all(w.isValid() for w in self.componentWidgets)
        self.widgetChanged(valid, interactive=0)
    def set_value(self, point):
        for i in range(config.dimension()):
            self.componentWidgets[i].set_value(point[i])
    def get_value(self):
        components = tuple(w.get_value() for w in self.componentWidgets)
        return primitives.Point(*components)
    def widgetChangeCB(self, interactive):
        self.widgetChanged(all(w.isValid() for w in self.componentWidgets),
                           interactive)
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        ParameterWidget.cleanUp(self)

def _PointParameter_makeWidget(self, scope=None, verbose=False):
    return PointWidget(self, scope=scope, name=self.name, verbose=verbose)

primitives.PointParameter.makeWidget = _PointParameter_makeWidget
 
