# -*- python -*-
# $RCSfile: whowidget.py,v $
# $Revision: 1.50.2.6 $
# $Author: langer $
# $Date: 2014/05/08 14:39:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Widget for choosing from a WhoClass.  WhoWidget.get_value() returns
# the name of the selected object, which is what is necessary for
# scripting.  The function using the result presumably knows how to
# use WhoClass.__getitem__ to get the actual object.

# The optional 'callback' argument to the constructor is called when a
# selection is made.  The single argument to the callback function is
# the selected object (ie, the .obj member of the Who instance).

# The WhoWidget is different from the usual ParameterWidget (in
# parameterwidgets.py) because it contains a list of gtk objects
# instead of just one.  Therefore it's not derived from
# ParameterWidget, and must do the work of that class by itself.
# Perhaps this is a symptom of bad design.

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import chooser
#from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import widgetscope
import gtk
import string


class WhoWidgetBase:
    def __init__(self, whoclass, value, callback, scope, condition, sort,
                 widgettype, verbose=False):
        debug.mainthreadTest()
        self.whoclass = whoclass
        self.scope = scope              # WidgetScope object
        self.verbose = verbose
        # condition(obj) is a function that returns 1 if the object
        # should be listed.
        self.condition = condition

        # sort is a function that takes a list of names and sorts them
        # into the order in which they should appear in the GUI.
        self.sort = sort

        # widgettype must be either 'Chooser' or 'Combo'.  It
        # specifies the type of subwidget to use for the lowest widget
        # in the Who hierarchy.
        self.widgettype = widgettype

        if scope:
            scope.addWidget(self)
        self.callback = callback
        depth = len(whoclass.hierarchy())
        # self.proxycheck = gtk.CheckButton()
        self.proxy_names = []
        self.widgets = [None]*depth
        self.gtk = [None]*depth
        self.currentPath = ['']*depth
        self.destroysignals = [None]*depth
        self.buildWidgets(value)        # sets currentPath, widgets, and gtk
        self.sbcallbacks = []
        for whoklass in whoclass.hierarchy():
            self.sbcallbacks += [
                switchboard.requestCallbackMain(
                ('new who', whoklass.name()), self.newWhoCB),
                switchboard.requestCallbackMain(
                ('remove who', whoklass.name()), self.newWhoCB),
                switchboard.requestCallbackMain(
                ('rename who', whoklass.name()), self.renameWhoCB)
                ]

    def buildWidgets(self, value=None, interactive=0):
        debug.mainthreadTest()
        # Construct a Chooser widget for each WhoClass in the target
        # WhoClass's hierarchy.  interactive is 1 if this call is in
        # response to a user action.
##        oldvalue = self.get_value()
        oldpath = self.currentPath[:]
        classlist = self.whoclass.hierarchy()
        depth = len(classlist)

        # Make sure value is a list.
        value = labeltree.makePath(value)

        # Make a list of the allowed proxies for the lowermost tier of
        # the class hierarchy for this widget.  Allowed proxies are
        # those which satisfy both the passed-in condition *and* are
        # proxies.
        self.proxy_names = [x[0] for x in classlist[-1].keys(
            condition = lambda x: (self.condition(x) and
                                   not whoville.excludeProxies(x)),
            sort=self.sort)]
        
        # Make sure that value contains a setting for each chooser widget
        if value and len(value) < depth:
            value += [None]*(depth-len(value))
        for d in range(depth):
            try:
                # Exclude proxies from this part of the process...
                paths = classlist[d].keys(
                    base=self.currentPath[:d],
                    condition=lambda x:
                            self.condition(x) and whoville.excludeProxies(x) and not x.secret(),
                    sort=self.sort)
            except KeyError, exc:
                names = []
            else:
                names = [p[0] for p in paths]
            if d==0:
                # In the top-most level of the widget, include the
                # proxy names for the lowermost level.
                names += self.proxy_names
                
            if self.widgets[d] is None:
                if self.widgettype == 'Chooser' or d < depth-1:
                    self.widgets[d] = chooser.ChooserWidget(
                        names, callback=self.selectCB, callbackargs=(d,),
                        name=classlist[d].name())
                else:
                    self.widgets[d] = chooser.ChooserComboWidget(
                        names, callback=self.comboCB,
                        name=classlist[d].name())
                self.gtk[d] = self.widgets[d].gtk
                self.destroysignals[d] = self.gtk[d].connect('destroy',
                                                             self.destroyCB, d)
            else:
                # Update the list of choices in an existing ChooserWidget.
                self.widgets[d].update(names)
            if value and value[d] in names:
                # Set widget to the given value
                self.widgets[d].set_state(value[d])
                self.currentPath[d] = value[d]
            elif self.currentPath[d] in names:
                # ... or retain previous value
                self.widgets[d].set_state(self.currentPath[d])
            elif len(names) > 0:
                # ... or pick the first value in the list
                self.currentPath[d] = names[0]
                self.widgets[d].set_state(0)
            else:
                # ... or don't pick anything
                self.currentPath[d] = ''
            if self.widgettype == 'Chooser':
                self.gtk[d].set_sensitive(names != [])
        # end for d in range(depth)

        # The state of other widgets may depend on the state of this
        # one.  If so, they can use the WidgetScope mechanism to find
        # this widget and listen for the following switchboard
        # message.  (Note that it's not sufficient to check to see if
        # get_value()'s return value has changed.  The return value
        # can be None both before and after a state change.)
        if oldpath != self.currentPath:
            switchboard.notify(self, interactive=interactive)

    def destroyCB(self, gtkwidget, d):
        if self.widgets:
            self.cleanUp()

    def destroy(self):
        debug.mainthreadTest()
        for gtkwid in self.gtk:
            gtkwid.destroy()
        
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.sbcallbacks = []
        self.gtk = []
        self.widgets = []
        self.whoclass = None
        if self.scope:
            self.scope.removeWidget(self)
            self.scope = None

    def newWhoCB(self, whoname):        # switchboard ("new who", classname)
        self.buildWidgets()
    def renameWhoCB(self, oldpath, newname): # sb ("rename who", classname)
        # The object being renamed might be an internal node, in which
        # case the path being passed in will be shorter than required
        # for setting the state of this widget.
        opath = labeltree.makePath(oldpath) # old path to renamed object
        npath = opath[:-1] + [newname]  # new path to renamed object
        cpath = self.currentPath        # current path
        if opath == cpath[:len(opath)]: # path to current object is changing
            npath += cpath[len(opath):] # new path to current object
            self.buildWidgets(npath)
        else:                           # change does not affect current object
            self.buildWidgets()

    def selectCB(self, gtkobj, name, d): # ChooserWidget callback
        newpath = self.currentPath[:]
        newpath[d] = name
        self.buildWidgets(newpath, interactive=1) # sets currentPath
        if self.callback:
            self.callback(self.currentPath)
    def comboCB(self, widget):          # ChooserComboWidget callback
        # Since the ChooserComboWidget represents a leaf of the
        # WhoClass heirarchy, there's no need to rebuild the other
        # widgets.  We just have to tell the world that the value has
        # changed.
        switchboard.notify(self, interactive=1)
        
    def set_value(self, value):
        path = labeltree.makePath(value)
        self.buildWidgets(path)

class WhoWidget(WhoWidgetBase):
    def __init__(self, whoclass, value=None, callback=None, scope=None,
                 name=None,
                 condition=whoville.excludeProxies,
                 sort=whoville.proxiesLast,
                 verbose=False):
        WhoWidgetBase.__init__(self, whoclass, value, callback, scope,
                               condition, sort, widgettype='Chooser',
                               verbose=verbose)
    def get_value(self, depth=None):
        if depth is None:
            depth = len(self.currentPath)
        # In proxy case, ignore depth.
        if self.currentPath[0] in self.proxy_names:
            return self.currentPath[0]
        if '' in self.currentPath[:depth]:
            return None
        return string.join(self.currentPath[:depth], ':')
    def isValid(self):
        if self.currentPath[0] in self.proxy_names:
            return True
        return '' not in self.currentPath

# The NewWhoWidget is used in the NewWhoParameterWidget, and
# substitutes a ChooserCombo for the Chooser at the lowest level of
# the WhoClass hierarchy.  This allows the user to type in the name of
# a new Who object, instead of simply choosing between existing ones.
# The ChooserCombo doesn't support any callbacks, so the NewWhoWidget
# doesn't either.  This makes it appropriate for use only in passive
# situations.  It can't initiate any action on its own.

class NewWhoWidget(WhoWidgetBase):
    def __init__(self, whoclass, value=None, callback=None, scope=None,
                 name=None,
                 condition=whoville.excludeProxies,
                 sort=whoville.proxiesLast,
                 verbose=False):
        WhoWidgetBase.__init__(self, whoclass, value, callback, scope,
                               condition, sort, widgettype='Combo',
                               verbose=verbose)
    def get_value(self):
        # This is slightly nontrivial because the ChooserCombo doesn't
        # have a callback, so the last part of self.currentPath isn't
        # automatically updated.
        debug.mainthreadTest()
        if self.widgets and self.widgets[-1]:
            self.currentPath[-1] = self.widgets[-1].get_value()
        return string.join(self.currentPath, ':')
    def isValid(self):
        debug.mainthreadTest()
        if self.widgets and self.widgets[-1]:
            return self.widgets[-1].get_value()

        
###################################

# The WhoParameterWidget assembles the components of a WhoWidget into
# a table so that the WhoWidget can be placed in automatically
# generated GUI objects (eg, RegisteredClassFactories).  It is a
# WidgetScope and as such contains its WhoWidget, so that other
# widgets searching for the WhoWidget can find it.  Other widgets
# should never have to search for the WhoParameterWidget explicitly.

class WhoParameterWidgetBase(parameterwidgets.ParameterWidget,
                         widgetscope.WidgetScope):
    def __init__(self, whoclass, value=None, scope=None, name=None, sort=None,
                 condition=whoville.excludeProxies, verbose=False):
        debug.mainthreadTest()
        widgetscope.WidgetScope.__init__(self, scope)
        self.whowidget = self.makeSubWidgets(whoclass, value, condition, sort,
                                             verbose=verbose)
        # Put the WhoWidget's components into a box.
        depth = len(self.whowidget.gtk)
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        vbox = gtk.VBox()
        frame.add(vbox)
        parameterwidgets.ParameterWidget.__init__(self, frame, scope, name,
                                                  verbose=verbose)
        for d in range(depth):
            vbox.pack_start(self.whowidget.gtk[d], expand=0, fill=0)
        self.wwcallback = switchboard.requestCallbackMain(self.whowidget,
                                                          self.widgetCB)
        self.widgetCB(0)
    def set_value(self, value):
        self.whowidget.set_value(value)
    def get_value(self):
        return self.whowidget.get_value()
    def cleanUp(self):
        parameterwidgets.ParameterWidget.cleanUp(self)
        self.destroyScope()
        switchboard.removeCallback(self.wwcallback)
    def widgetCB(self, interactive):    # validity check
        val = self.get_value()
        self.widgetChanged(val and val[-1] != ':', interactive)

class WhoParameterWidget(WhoParameterWidgetBase):
    def makeSubWidgets(self, whoclass, value, condition, sort, verbose=False):
        return WhoWidget(whoclass, value, scope=self, condition=condition,
                         sort=sort, verbose=verbose)

class NewWhoParameterWidget(WhoParameterWidgetBase):
    def makeSubWidgets(self, whoclass, value, condition, sort, verbose=False):
        return NewWhoWidget(whoclass, value, scope=self, condition=condition,
                            sort=sort, verbose=verbose)

def _WhoParameter_makeWidget(self, scope=None, verbose=False):
    return WhoParameterWidget(self.whoclass, self.value, scope=scope,
                              name=self.name, verbose=verbose)

whoville.WhoParameter.makeWidget = _WhoParameter_makeWidget

def _NewWhoParameter_makeWidget(self, scope=None, verbose=False):
    return NewWhoParameterWidget(self.whoclass, self.value, scope=scope,
                                 name=self.name, verbose=verbose)

whoville.NewWhoParameter.makeWidget = _NewWhoParameter_makeWidget

###############################################

class WhoClassParameterWidget(parameterwidgets.ParameterWidget):
    def __init__(self, value, scope=None, name=None,
                 condition=whoville.noSecretClasses,
                 verbose=False):
        self.chooser = chooser.ChooserWidget(whoville.classNames(condition),
                                             callback=self.chooserCB,
                                             name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.chooser.gtk, scope,
                                                  verbose=verbose)
        self.sb = switchboard.requestCallbackMain('new who class',
                                                  self.newWhoClass)
        self.set_value(value)
        self.condition = condition
    def newWhoClass(self, classname):
        self.chooser.update(whoville.classNames(self.condition))
    def chooserCB(self, gtkobj, name):
        switchboard.notify(self, interactive=1)
        self.widgetChanged(self.get_value() is not None, interactive=1)
    def set_value(self, value):
        self.chooser.set_state(value)   # does not call chooserCB
        switchboard.notify(self, interactive=0)
        # Use self.get_value(), not value, to check validity, because
        # value may be None, in which case the actual value is
        # whatever's first in the Chooser.
        self.widgetChanged(self.get_value() is not None, interactive=0)
    def get_value(self):
        return self.chooser.get_value()
    def cleanUp(self):
        switchboard.removeCallback(self.sb)
        parameterwidgets.ParameterWidget.cleanUp(self)

def _WhoClassParameter_makeWidget(self, scope=None, verbose=False):
    return WhoClassParameterWidget(self.value, scope=scope, name=self.name,
                                   condition=self.condition,
                                   verbose=verbose)

whoville.WhoClassParameter.makeWidget = _WhoClassParameter_makeWidget

###############################################
                                   
class AnyWhoParameterWidget(parameterwidgets.ParameterWidget,
                            widgetscope.WidgetScope):
    # See comment in WhoParameterWidget about WidgetScope.
    def __init__(self, value, scope, name=None, verbose=False):
        widgetscope.WidgetScope.__init__(self, scope)
        parameterwidgets.ParameterWidget.__init__(self, gtk.VBox(), scope, name,
                                                  verbose=verbose)
        self.classwidget = scope.findWidget(
            lambda w: isinstance(w, WhoClassParameterWidget))
        self.whopwidget = None          # enclosed WhoParameterWidget
        self.whoclassname = None
        self.whoSignal = None
        self.buildWidget()
        self.set_value(value)
        self.classSignal = switchboard.requestCallbackMain(
            self.classwidget, self.classChangedCB)
    def cleanUp(self):
        parameterwidgets.ParameterWidget.cleanUp(self)
        switchboard.removeCallback(self.classSignal)
        if self.whoSignal:
            switchboard.removeCallback(self.whoSignal)
    def classChangedCB(self, *args, **kwargs):
        if self.classwidget.get_value() != self.whoclassname:
            self.buildWidget()
    def buildWidget(self):
        debug.mainthreadTest()
        if self.whopwidget:
            self.whopwidget.destroy()
        self.whoclassname = self.classwidget.get_value()
        whoclass = whoville.getClass(self.whoclassname)
        # Create a WhoWidget that doesn't exclude proxy who
        # objects. If it's necessary to create an
        # AnyWhoParameterWidget with a different exclusion policy,
        # then the AnyWhoParameter will need to have a 'condition'
        # attribute that can be passed in to the widget.
        self.whopwidget = WhoParameterWidget(whoclass, scope=self,
                                             sort=whoville.proxiesLast,
                                             condition=lambda x:1)
        if self.whoSignal:
            switchboard.removeCallback(self.whoSignal)
        self.whoSignal = switchboard.requestCallbackMain(self.whopwidget,
                                                         self.whoChangedCB)
        self.gtk.pack_start(self.whopwidget.gtk)
        self.gtk.show_all()
        self.widgetChanged(self.get_value() is not None, interactive=0)
    def whoChangedCB(self, *args):
        self.widgetChanged(self.get_value() is not None, interactive=1)
    def set_value(self, value):
        self.whopwidget.set_value(value)
        # Use self.get_value(), not value, to check validity, because
        # value may be None, in which case the actual value is
        # whatever's first in the Chooser.
        self.widgetChanged(self.get_value() is not None, interactive=0)
    def get_value(self):
        return self.whopwidget.get_value()

def _AnyWhoParameter_makeWidget(self, scope=None, verbose=False):
    return AnyWhoParameterWidget(self.value, scope=scope, name=self.name,
                                 verbose=verbose)

whoville.AnyWhoParameter.makeWidget = _AnyWhoParameter_makeWidget



