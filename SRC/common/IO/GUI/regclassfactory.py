# -*- python -*-
# $RCSfile: regclassfactory.py,v $
# $Revision: 1.54.4.6 $
# $Author: fyc $
# $Date: 2014/07/22 17:57:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.


# The RegisteredClassFactory is the ParameterWidget associated with
# Parameters for RegisteredClass variables.  As such it is created
# automatically inside ParameterTables, ParameterDialogs, MenuDialogs,
# and other RegisteredClassFactories.  It can also be used directly in
# GUI pages.

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import widgetscope
import gtk
import types

###################

## RegisteredClass Parameter classes that have specialized widgets for
## some or all of their subclasses can register those widgets by
## calling addWidget().

widgetdictdict = {}

def addWidget(parameterclass, registeredclass, widgetclass):
    try:
        widgetdict = widgetdictdict[parameterclass]
    except KeyError:
        widgetdict = widgetdictdict[parameterclass] = {}
    widgetdict[registeredclass] = widgetclass

def _getWidgetDict(param):
    try:
        return widgetdictdict[param.__class__]
    except KeyError:
        return {}
    
####################

class RCFBase(parameterwidgets.ParameterWidget,
              widgetscope.WidgetScope):
    def __init__(self, gtk, scope, widgetdict, name, verbose=False):
        parameterwidgets.ParameterWidget.__init__(self, gtk, scope, name,
                                                  verbose=verbose)
        widgetscope.WidgetScope.__init__(self, scope)

        # Dictionary of classes of widget wrappers for RegisteredClass
        # types that don't want to use a simple ParameterTable
        self.widgetdict = widgetdict

    # includeRegistration() controls which Registrations in the
    # registry will be listed in the RegisteredClassFactory.  Derived
    # classes can redefine this function. The default behavior is to
    # exclude secret registrations.
    def includeRegistration(self, registration):
        return not registration.secret

    def set_callback(self, callback, *args, **kwargs):
        self.callback = callback
        self.callbackargs = args
        self.callbackkwargs = kwargs
    
    def cleanUp(self):
        del self.registry               # break possible circular references?
        parameterwidgets.ParameterWidget.cleanUp(self)
        self.destroyScope()

####################

class RegisteredClassFactory(RCFBase):
    def __init__(self, registry, obj=None, title=None,
                 callback=None, fill=0, expand=0, scope=None, name=None,
                 widgetdict={}, verbose=False,
                 *args, **kwargs):

        debug.mainthreadTest()
        # if verbose:
        #     debug.fmsg("RCF ctor: title=", title)
        self.registry = registry
        # The optionally supplied callback is called when a new
        # subclass is selected.  The args are the subclass's
        # registration, plus the extra args and kwargs given to
        # __init__.
        self.callback = callback
        self.callbackargs = args
        self.callbackkwargs = kwargs

        # fill & expand options are passed to the gtk pack command in
        # setByRegistration().
        self.fill = fill
        self.expand = expand    

        self.readonly = False
        RCFBase.__init__(self, gtk.Frame(), scope, widgetdict, name, 
                         verbose=verbose)
        
        self.box = gtk.VBox()
        self.gtk.add(self.box)
        self.options = chooser.ChooserWidget([], callback=self.optionCB,
                                             update_callback=self.updateCB,
                                             name='Chooser')
        if not title:
            self.box.pack_start(self.options.gtk, expand=0, fill=0)
            self.titlebox = None
        else:
            self.titlebox=gtk.HBox()
            self.box.pack_start(self.titlebox, expand=0, fill=0)
            self.titlebox.pack_start(gtk.Label(title), expand=0, fill=0)
            self.titlebox.pack_start(self.options.gtk, expand=1, fill=1)

        self.widgetcallback = None
        
        self.menu = None
        self.paramWidget = None
        self.currentOption = None

        # useDefault indicates whether or not the chooser should be set
        # to the first legal registration in the registry.  It should
        # be false only if the widget has been explicitly set, either
        # programmatically or by the user.
        self.useDefault = obj is None

        self.update(registry, obj, interactive=0)
        # if self.verbose:
        #     debug.fmsg("done")

    def refresh(self, obj=None):
        self.update(self.registry, obj)

    def update(self, registry, obj=None, interactive=0):
        # if self.verbose:
        #     debug.fmsg()
        debug.mainthreadTest()
        self.registry = registry
        regs = [reg for reg in registry if self.includeRegistration(reg)]
        names = [reg.name() for reg in regs]
        helpdict = {}
        for reg in regs:
            if reg.tip:
                helpdict[reg.name()] = reg.tip

        self.options.update(names, helpdict)

        if self.paramWidget:
            switchboard.removeCallback(self.widgetcallback)
            self.paramWidget.destroy()

        if self.currentOption is not None:
            oldoption = self.currentOption.name()
        else:
            oldoption = None

        self.paramWidget = None
        self.widgetcallback = None
        self.currentOption = None
        self.show()

        # If obj is None, see if there's a new option with the same
        # name as the old one, and use it to initialize the chooser
        # state.
        if obj is None and oldoption in names and not self.useDefault:
            obj = oldoption
        
        # Set initial values.
        if obj is not None:
            # If obj is a string, look for a registration with that
            # name.
            if type(obj)==types.StringType:
                for reg in registry:
                    if self.includeRegistration(reg) and reg.name()==obj:
                        self.setByRegistration(reg, interactive)
                        # if self.verbose:
                        #     debug.fmsg("done")
                        return
            else:
                # If obj is an instance of a legal subclass, set it.
                for reg in regs:
                    if isinstance(obj, reg.subclass):
                        self.set(obj, interactive)
                        # if self.verbose:
                        #     debug.fmsg("done")
                        return
                
        # obj is None, or is not a valid setting.  Use the first item
        # in the list instead.
        for registration in registry:
            if self.includeRegistration(registration):
                self.setByRegistration(registration, interactive)
                # if self.verbose:
                #     debug.fmsg("done")
                return
        # if self.verbose:
        #     debug.fmsg("done")

    # The "interactive" flag should be True when the change is not
    # programmatic, some widgets use it to make sure their displays
    # remain self-consistent.
    def set(self, obj, interactive):
        registration = obj.getRegistration()
        # if self.verbose:
        #     debug.fmsg("registration=", registration)
        if self.includeRegistration(registration):
            # Set the registration's parameters
            # if self.verbose:
            #     debug.fmsg("calling  setDefaultParams")
            obj.setDefaultParams()
            self.useDefault = False
            # if self.verbose:
            #     debug.fmsg("calling setByRegistration")
            self.setByRegistration(obj.getRegistration(), interactive)
        # if self.verbose:
        #     debug.fmsg("done")

    # Returns the currently-selected registration, or None.
    def getRegistration(self):
        return self.currentOption

    def setByRegistration(self, registration, interactive=0):
        debug.mainthreadTest()
        # setByRegistration() is almost the same as optionCB(), except
        # that it makes no attempt to set the new parameters from the
        # old ones, since it's not being used to switch between
        # convertible classes.  In fact, it may be used to switch to a
        # new instance of the same class, so it's important to throw
        # out the old parameter values.
        # if self.verbose:
        #     debug.fmsg("registration=", registration)
        if self.includeRegistration(registration):
            if self.paramWidget is not None:
                self.paramWidget.destroy()
                self.options.set_state(registration.name()) # TODO OPT: redundant?
                
            self.getBase(registration) # for convertible classes

            self.options.set_state(registration.name())
            self.currentOption = registration

            # if self.verbose:
            #     debug.fmsg("calling makeWidget", registration, id(self))
            self.paramWidget = self.makeWidget(registration)
            # if self.verbose:
            #     debug.fmsg("back from makeWidget")
            if self.readonly:
                self.makeUneditable()

            ## After the widget has once been set interactively, its
            ## default value isn't used.
            self.useDefault = self.useDefault and not interactive
            # if self.verbose:
            #     debug.fmsg("calling isValid")
            valid = self.paramWidget.isValid()
            # if self.verbose:
            #     debug.fmsg("valid=", valid, "calling widgetChanged")
            self.widgetChanged(valid, interactive)
            # if self.verbose:
            #     debug.fmsg("back from widgetChanged")

            self.box.pack_start(self.paramWidget.gtk, fill=self.fill,
                                expand=self.expand)
            self.show()
            if hasattr(registration, 'tip'):
                tooltips.set_tooltip_text(self.options.gtk,registration.tip)
        # else:
        #     if self.verbose:
        #         debug.fmsg("not included!")
        # if self.verbose:
        #     debug.fmsg("done")

    def cleanUp(self):
        if self.widgetcallback is not None:
            switchboard.removeCallback(self.widgetcallback)
            self.widgetcallback = None
        RCFBase.cleanUp(self)

    def show(self):
        debug.mainthreadTest()
        if self.titlebox is not None:
            self.titlebox.show_all()
        if self.paramWidget is not None:
            self.paramWidget.show()
        self.options.show()
        self.box.show()
        self.gtk.show()

    # Required by setByRegistration, but probably shouldn't be.
    def getBase(self, registration):
        pass
    
    # Actually instantiate a widget.  Convertible does this differently.
    def makeWidget(self, registration):
        debug.mainthreadTest()
        try:
            widgetclass = self.widgetdict[registration.subclass]
        except KeyError:
            widgetclass = parameterwidgets.ParameterTable
        # if self.verbose:
        #     debug.fmsg("Calling widgetclass ctor", widgetclass)
        widget = widgetclass(registration.params, scope=self,
                             name=registration.name(),
                             verbose=self.verbose)
        # if self.verbose:
        #     widget.verbose = True
        #     debug.fmsg("got widget")
        self.widgetcallback = switchboard.requestCallbackMain(widget,
                                                              self.widgetCB)
        return widget

#         try:
#             # Use the special widget from the widgetdict, if there is one
#             widget = self.widgetdict[registration.subclass](
#                 registration.params, scope=self, name=registration.name())
#         except KeyError:
#             # Otherwise, just use a parameter table.
#             widget = parameterwidgets.ParameterTable(
#                 registration.params, scope=self, name=registration.name())
#         self.widgetcallback = switchboard.requestCallbackMain(widget,
#                                                               self.widgetCB)
# ##        self.widgetChanged(widget.isValid(), interactive)
#         return widget

    def widgetCB(self, interactive):      # switchboard callback
        self.widgetChanged(self.paramWidget.isValid(), interactive)

    def dumpValidity(self):
        self.paramWidget.dumpValidity()
    
    # When called as an event callback for menu selection in the
    # GtkOptionMenu, self.currentOption is either the "outgoing"
    # registration entry, or None.  
    def optionCB(self, widget, regname):
        debug.mainthreadTest()
        oldbase = None
        if self.currentOption is not None:
            if self.paramWidget is not None:
                # If there is a current option and a current widget,
                # copy the values into the parameters, so that they
                # become the defaults the next time the current widget
                # is displayed.  Some parameters may not yet have
                # legal values.  That's ok, since they're not going to
                # be used right away.
                try:
                    self.paramWidget.get_values()
                except:
                    pass
                self.paramWidget.destroy()
            
        # Set the current option to the new registration, assign params.
        # In the convertible case, this is a separate registration
        # instance, of a related (by convertibility) type.
        self.currentOption = self.get_reg(regname)
        self.optionFinish(self.currentOption, interactive=1)

    def updateCB(self, *args):
        if self.paramWidget is not None:
            self.widgetChanged(
                self.options.nChoices() > 0 and self.paramWidget.isValid(), 
                interactive=False)

    def makeReadOnly(self):
        # Call makeReadOnly on a ConvertibleRegisteredClassFactory
        # that is being used just to display the various forms of a
        # value, rather than to get a new value.  It makes all Entrys
        # within the RCF uneditable.  This isn't quite the right thing
        # to do, but it's pretty close, and much easier than doing it
        # right.  Doing it right would involve desensitizing all
        # widgets except those that are used to switch between
        # equivalent ConvertibleRegisteredClass values (while not
        # densensitizing Entries, only making them uneditable, so text
        # could be copied...)
        # 
        # makeReadOnly is probably only useful for
        # ConvertibleRegisteredClassFactories, but it's defined here
        # in RegisteredClassFactory because it can work here too.
        self.readonly = True
        self.makeUneditable()
    def makeUneditable(self):
        # called by makeReadOnly and when subclass changes
        entries = gtkutils.findChildren([gtk.Entry], self.paramWidget.gtk)
        for entry in entries:
            entry.set_editable(0)
        sliders = gtkutils.findChildren([gtk.Scale, gtk.Button],
                                        self.paramWidget.gtk)
        for slider in sliders:
            slider.set_sensitive(0)
        
        
    def optionFinish(self, registration, interactive):
        debug.mainthreadTest()
        self.paramWidget = self.makeWidget(registration)
        if self.readonly:
            self.makeUneditable()
        self.widgetChanged(self.paramWidget.isValid(), interactive)
        
        self.box.pack_start(self.paramWidget.gtk, fill=0, expand=0)
        self.show()
        if hasattr(registration, 'tip'):
            tooltips.set_tooltip_text(self.options.gtk,registration.tip)

        self.useDefault = False
        if self.callback:
            self.callback(registration, *self.callbackargs,
                          **self.callbackkwargs)

    def get_reg(self, regname):
        for reg in self.registry:
            if reg.name() == regname and self.includeRegistration(reg):
                return reg

    def get_value(self):
##        if self.currentOption is not None and self.paramWidget is None:
##            print "currentOption=", self.currentOption
##            assert 0
        if self.currentOption is None:
            return None
        self.paramWidget.get_values()
        return self.currentOption()     # instantiates RegisteredClass

    def set_defaults(self):
        # Read widgets and set values in Registration, w/out creating object
        if self.currentOption is not None:
            self.paramWidget.get_values()

def _RegisteredClass_makeWidget(self, scope=None, title=None, verbose=False):
    return RegisteredClassFactory(self.registry, self.value, scope=scope,
                                  widgetdict=_getWidgetDict(self),
                                  title=title, name=self.name, verbose=verbose)

parameter.RegisteredParameter.makeWidget = _RegisteredClass_makeWidget

#####################################################################

# Subclass of the registeredclassfactory for convertible registered
# classes.  This is required because the widgets for convertible
# classes have more state information -- they need to know the
# original pre-instantiation value, in base form, as well as the
# current state data stored in the params.
class ConvertibleRegisteredClassFactory(RegisteredClassFactory):
    def __init__(self, registry, obj=None, title=None,
                 callback=None, fill=0, expand=0, scope=None, name=None,
                 widgetdict={},
                 *args, **kwargs):
        debug.mainthreadTest()
        self.base_value = None
        RegisteredClassFactory.__init__(self, registry, obj,
                                        title=title,
                                        callback=callback,
                                        fill=fill,
                                        expand=expand,
                                        scope=scope,
                                        name=name,
                                        widgetdict=widgetdict,
                                        *args, **kwargs)
        
    # The ConvertibleRCF's optionCB needs to extract the values from
    # the "outgoing" widgets in order to insert them, suitably
    # converted, into the "incoming" widgets.  Widgets whose
    # parameters have nontrivial ".value" retrievals (e.g. dependent
    # parts of ParameterGroups) should ensure that their resolver
    # does not throw spurious exceptions in this circumstance.
    def optionCB(self, widget, regname):
        if self.currentOption is not None:
            if self.paramWidget is not None:
                # If there is a current option and a current widget,
                # copy the values into the parameters.
                self.paramWidget.get_values()
                self.paramWidget.destroy()
            # Retrieve the current value of the outgoing option.
            try:
                old = self.getParamValues()
                got_old = True
            except ValueError, exc:
                reporter.warn(exc)
                got_old = False
            
        # Set the current option to the new registration, assign params.
        # In the convertible case, this is a separate registration
        # instance, of a related (by convertibility) type.
        self.currentOption = self.get_reg(regname)
        if got_old:
            self.setParams(old)
        self.optionFinish(self.currentOption, interactive=1)

    # All the functions here override virtual functions in the
    # immediate base class.
    def getBase(self, registration):
        # Get the original value of the parameter, in base form,
        # and store it so you can pass it to widgets for other representations.
        try:
            self.base_value = registration.getParamValuesAsBase()
        except ValueError, exc:
            reporter.warn(exc)

    def getParamValues(self):
        return self.currentOption.getParamValuesAsBase()

    def setParams(self, old):
        self.currentOption.setParamsFromBase(old)
        
    # In the convertible case, the widget constructor will take another
    # argument, the "base_value" which is the original value of the
    # parameter, in base form.  
    def makeWidget(self, registration):
        debug.mainthreadTest()
        try:
            widget = self.widgetdict[registration.subclass](
                registration.params,
                self.base_value,
                scope=self,
                name=registration.name())
        except KeyError:
            widget = parameterwidgets.ParameterTable(registration.params,
                                                     scope=self,
                                                     name=registration.name())
        self.widgetcallback = switchboard.requestCallbackMain(widget,
                                                              self.widgetCB)
##        self.widgetChanged(widget.isValid(), interactive)
        return widget
    
def _ConvertibleRegisteredClass_makeWidget(self, scope=None, verbose=False):
    return ConvertibleRegisteredClassFactory(self.registry, self.value,
                                             scope=scope,
                                             widgetdict=_getWidgetDict(self),
                                             name=self.name, verbose=verbose)

parameter.ConvertibleRegisteredParameter.makeWidget = \
                      _ConvertibleRegisteredClass_makeWidget


#####################################################################

# RegisteredClassListFactory

ParameterTable = parameterwidgets.ParameterTable

class RegistrationGUIData:
    def __init__(self, registration, rclfactory):
        debug.mainthreadTest()
        self.registration = registration
        self.rclfactory = rclfactory
        self._button = gtk.CheckButton()
        gtklogger.setWidgetName(self._button, registration.name()+'Toggle')
        # We could use an Expander instead of a CheckButton here, but
        # it might be confusing.  The check button makes it clear that
        # a method is selected.  Just expanding an Expander might not
        # be so obvious, especially if a Registration has no
        # Parameters.  Also, the whole RegisteredClassListFactory
        # would have to be redone.
        self._signal = gtklogger.connect(self._button, 'clicked', self.buttonCB)
        self._box = gtk.VBox()
        self._label = gtk.Label(registration.name())
        self._label.set_alignment(0.0, 0.5)
        if hasattr(registration, 'tip'):
            tooltips.set_tooltip_text(self._label,registration.tip)
        self.sbcallback = None
        self.makeWidget()
    def makeWidget(self):
        debug.mainthreadTest()
        if self.sbcallback:
            switchboard.removeCallback(self.sbcallback)
        self._box.foreach(gtk.Object.destroy)
        try:
            self._widget = self.rclfactory. \
                           widgetdict[self.registration.subclass] \
                           (registration.params, scope=self.rclfactory,
                            name=self.registration.name())
        except KeyError:                # no special widget defined
            self._widget = ParameterTable(self.registration.params,
                                          scope=self.rclfactory,
                                          name=self.registration.name())
        self._box.pack_start(self._widget.gtk, expand=0, fill=0)
        self.widgetcallback = switchboard.requestCallbackMain(self._widget,
                                                              self.widgetCB)
    def widgetCB(self, interactive):
        self.rclfactory.widgetCB(interactive)
    def isValid(self):
        return self._widget.isValid()
    def showWidget(self):
        debug.mainthreadTest()
        self._box.set_sensitive(self._button.get_active())
        self._box.show()
        self._widget.show()
    def name(self):
        return self.registration.name()
    def box(self):
        return self._box
    def button(self):
        return self._button
    def label(self):
        return self._label
    def setButton(self, active):
        debug.mainthreadTest()
        self._signal.block()
        self._button.set_active(active)
        self._signal.unblock()
        self.showWidget()
    def getButton(self):
        debug.mainthreadTest()
        return self._button.get_active()
    def buttonCB(self, *args):
        self.rclfactory.widgetCB(interactive=1)
        self.showWidget()
    def show(self):
        debug.mainthreadTest()
        self._label.show_all()
        self._button.show()
        self.showWidget()
    def get_value(self):
        debug.mainthreadTest()
        if self._button.get_active():
            self._widget.get_values()
            return self.registration()  # creates RegisteredClass instance
    def cleanUp(self):
        switchboard.removeCallback(self.widgetcallback)
        

class RegisteredClassListFactory(RCFBase):
    def __init__(self, registry, objlist=None, title=None, callback=None,
                 fill=0, expand=0, scope=None, name=None, widgetdict={},
                 *args, **kwargs):
        debug.mainthreadTest()

        self.registry = registry
        self.callback = callback
        self.callbackargs = args
        self.callbackkwargs = kwargs
        self.title = title
        self.fill = fill
        self.expand = expand

        frame = gtk.Frame()
        self.table = gtk.Table(rows=1, columns=2)
        frame.add(self.table)
        RCFBase.__init__(self, frame, scope, widgetdict, name)
        self.parent.addWidget(self)
        self.update(registry, objlist)

    def cleanUp(self):
        debug.mainthreadTest()
        del self.guidata
        RCFBase.cleanUp(self)

    def update(self, registry, objlist=[]):
        # Called during initialization and whenever the registry changes.
        debug.mainthreadTest()
        self.registry = registry
        self.table.foreach(gtk.Object.destroy) # clear the table
        row = 0
        if self.title:
            self.table.attach(gtk.Label(self.title), 0,2, row,row+1,
                              yoptions=0, ypadding=5)
            row += 1
            self.table.attach(gtk.HSeparator(), 0,2, row,row+1,
                              yoptions=0, ypadding=3)
            row += 1
        self.guidata = {}               # RegistrationGUIData, keyed by reg name
        for registration in registry:
            if self.includeRegistration(registration):
                data = RegistrationGUIData(registration, self)
                self.guidata[registration.name()] = data
                self.table.attach(data.button(), 0,1, row,row+1, xoptions=0,
                                  yoptions=0, xpadding=3, ypadding=3)
                self.table.attach(data.label(), 1,2, row,row+1,
                                  xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
                self.table.attach(data.box(), 1,2, row+1,row+2,
                                  xoptions=gtk.EXPAND|gtk.FILL, yoptions=0,
                                  xpadding=3, ypadding=3)
                self.table.attach(gtk.HSeparator(), 0,2, row+2, row+3,
                                  xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
                row += 3
        self.table.resize(rows=row-1, columns=2) # remove last gtk.HSeparator
        if objlist is not None:
            self.set(*objlist)
        self.widgetCB(interactive=0)

    def set(self, *objlist):
        for obj in objlist:
            obj.setDefaultParams()
        self.setByRegistrations([obj.getRegistration() for obj in objlist])

    def setByRegistrations(self, registrations):
        for reg in self.registry:
            if self.includeRegistration(reg):
                data = self.guidata[reg.name()]
                data.setButton(reg in registrations) # calls data.makeWidget
        self.show()

    def widgetCB(self, interactive):
        ok = 0
        for data in self.guidata.values():
            if data.getButton():
                if data.isValid():
                    ok = 1
                else:
                    self.widgetChanged(0, interactive)
                    return
        self.widgetChanged(ok, interactive)
            
    def show(self):
        debug.mainthreadTest()
        # Don't use self.gtk.show_all(), since it will show collapsed items.
        for data in self.guidata.values():
            data.show()
        self.table.show()
        self.gtk.show()
        
    def get_value(self):
        values = []
        for registration in self.registry:
            data = self.guidata[registration.name()]
            value = data.get_value()
            if value is not None:
                values.append(value)
        return values

    def set_defaults(self):
        # For the regular RegisteredClassFactory, this copies the
        # values out of the gui and into the Parameters in the
        # Registrations (which are the same as the Parameters in the
        # menus) so that calling menuitem.callWithDefaults() does the
        # right thing.  This doesn't make sense for the
        # RegisteredClassListFactory, since the menu Parameter is a
        # list of RegisteredClass objects, not the parameters of the
        # objects themselves.  So don't use this, use get_value() instead.
        raise ooferror.ErrPyProgrammingError(
            "Don't use RegisteredClassListFactory.set_defaults()!")

def _RegisteredClassList_makeWidget(self, scope=None, verbose=False):
    return RegisteredClassListFactory(self.registry, self.value, scope=scope,
                                      widgetdict=_getWidgetDict(self),
                                      name=self.name, verbose=verbose)

parameter.RegisteredListParameter.makeWidget = _RegisteredClassList_makeWidget
