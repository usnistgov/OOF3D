# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Base class for Selection toolboxes.
# See NOTES/selection_machinery.txt

from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import pixelselectionmod
from ooflib.common import subthread
from ooflib.common.IO import mousehandler
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.common.IO.GUI import tooltips

import gtk, sys

class SelectionMethodFactory(regclassfactory.RegisteredClassFactory):
    def __init__(self, registry, obj=None, title=None,
                 callback=None, fill=0, expand=0, scope=None, name=None,
                 widgetdict={}, *args, **kwargs):
        self.current_who_classes = []
        regclassfactory.RegisteredClassFactory.__init__(
            self, registry, obj=obj, title=title, callback=callback,
            fill=fill, expand=expand, scope=scope, name=name,
            widgetdict=widgetdict, *args, **kwargs)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class GenericSelectToolboxGUI(toolboxGUI.GfxToolbox):
    def __init__(self, toolbox, method):
        debug.mainthreadTest()
        toolboxGUI.GfxToolbox.__init__(self, toolbox)
        self.method = method            # RegisteredClass of selection methods
        self.currentGUI = None
        self.currentMouseHandler = mousehandler.nullHandler

        outerbox = gtk.VBox(spacing=2)
        self.gtk.add(outerbox)

        # Create an instance of each SelectionMethod's
        # SelectionMethodGUI and store it in a dictionary keyed by the
        # method's registration.
        self.methodGUIs = {reg.subclass : reg.gui(self)
                           for reg in method.registry if hasattr(reg, 'gui')}

        self.selectionMethodFactory = SelectionMethodFactory(
            method.registry, title="Method:", name="Method",
            scope=self, callback=self.changedSelectionMethod,
            widgetdict=self.methodGUIs)
        
        outerbox.pack_start(self.selectionMethodFactory.gtk, expand=1, fill=1)

        # Undo, Redo, Clear, and Invert buttons.  The callbacks for
        # these have to be defined in the derived classes.
        hbox = gtk.HBox(homogeneous=True, spacing=2)
        outerbox.pack_start(hbox, expand=0, fill=0)
        self.undobutton = gtk.Button(stock=gtk.STOCK_UNDO)
        self.redobutton = gtk.Button(stock=gtk.STOCK_REDO)
        hbox.pack_start(self.undobutton, expand=1, fill=1)
        hbox.pack_start(self.redobutton, expand=1, fill=1)
        gtklogger.setWidgetName(self.undobutton, "Undo")
        gtklogger.setWidgetName(self.redobutton, "Redo")
        gtklogger.connect(self.undobutton, 'clicked', self.undoCB)
        gtklogger.connect(self.redobutton, 'clicked', self.redoCB)
        tooltips.set_tooltip_text(self.undobutton,
                             "Undo the previous selection operation.")
        tooltips.set_tooltip_text(self.redobutton,
                             "Redo an undone selection operation.")

        self.clearbutton = gtk.Button(stock=gtk.STOCK_CLEAR)
        gtklogger.setWidgetName(self.clearbutton, "Clear")
        hbox.pack_start(self.clearbutton, expand=1, fill=1)
        gtklogger.connect(self.clearbutton, 'clicked', self.clearCB)
        tooltips.set_tooltip_text(self.clearbutton, "Unselect all objects.")

        self.invertbutton = gtk.Button('Invert')
        gtklogger.setWidgetName(self.invertbutton, "Invert")
        hbox.pack_start(self.invertbutton, expand=1, fill=1)
        gtklogger.connect(self.invertbutton, 'clicked', self.invertCB)
        tooltips.set_tooltip_text(
            self.invertbutton,
            "Select all unselected objects, and deselect all selected objects.")


        # Selection information
        hbox = gtk.HBox()
        outerbox.pack_start(hbox, expand=0, fill=0)
        hbox.pack_start(gtk.Label('Selection size: '), expand=0, fill=0)
        self.sizetext = gtk.Entry();
        gtklogger.setWidgetName(self.sizetext, 'size')
        hbox.pack_start(self.sizetext, expand=1, fill=1)
        self.sizetext.set_editable(False)
        self.sizetext.set_size_request(12*guitop.top().digitsize, -1)
        self.setInfo()

        # switchboard callbacks
        self.sbcallbacks = [
            switchboard.requestCallbackMain(method,
                                            self.updateSelectionMethods),
            switchboard.requestCallback((self.gfxwindow(),
                                         'layers changed'),
                                        self.setInfo_subthread),
            switchboard.requestCallbackMain((self.gfxwindow(),
                                             'layers changed'),
                                            self.layerChangeCB),
            switchboard.requestCallbackMain('new pixel selection',
                                            self.newSelection),
        ]

        # Make sure that the initial state is self-consistent
        self.changedSelectionMethod(
            self.selectionMethodFactory.getRegistration())


    def changedSelectionMethod(self, registration): # Chooser callback
        if registration is None:
            return
        # currentGUI can be None if the subclass doesn't have a GUI
        if self.currentGUI is not None:
            self.currentGUI.setCurrentRegistration(None)
        self.currentGUI = self.methodGUIs.get(registration.subclass, None)
        if self.currentGUI is not None:
            self.currentGUI.setCurrentRegistration(registration)
        self.installMouseHandler()

    def activate(self):
        if not self.active:
            super(GenericSelectToolboxGUI, self).activate()
            if self.currentGUI is not None:
                self.currentGUI.activate()
            self.sensitize()
            # self.sensitizeHistory()
            self.setInfo()
            self.installMouseHandler()
            self.layerChangeCB()
            if config.dimension() == 3:
                self.gfxwindow().toolbar.setSelect()

    def deactivate(self):
        if self.active:
            super(GenericSelectToolboxGUI, self).deactivate()
            self.currentMouseHandler.stop()
            if self.currentGUI is not None:
                self.currentGUI.deactivate()

    def installMouseHandler(self):
        self.currentMouseHandler.stop()
        if self.currentGUI is not None:
            self.currentMouseHandler = self.currentGUI.mouseHandler()
        else:
            self.currentMouseHandler = mousehandler.nullHandler
        self.gfxwindow().setMouseHandler(self.currentMouseHandler)
        self.currentMouseHandler.start()

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.currentMouseHandler.stop()
        for gui in self.methodGUIs.values():
            if gui is not None:
                gui.close()
        toolboxGUI.GfxToolbox.close(self)

    def getSelectionSource(self):
        return self.toolbox.getSelectionSource()

    def getSourceName(self):
        return self.toolbox.getSourceName()

    def invokeMenuItem(self, who, method):
        # method is a SelectionMethod subclass
        menuitem = self.toolbox.menuitem
        buttons = self.currentMouseHandler.buttons
        menuitem.callWithDefaults(source=who.path(), method=method)

    def getParamValues(self, *paramnames):
        # Return the values of the given parameters from the
        # RegisteredClassFactory.  If just one is given, return it.
        # If there's more than one, return a tuple.
        mainthread.runBlock(self.selectionMethodFactory.set_defaults)
        reg = self.selectionMethodFactory.getRegistration()
        values = [reg.getParameter(name).value for name in paramnames]
        if len(paramnames) == 1:
            return values[0]
        return values

    def setParamValues(self, **kwargs):
        # Set the values of the given parameters in the
        # RegisteredClassFactory.
        reg = self.selectionMethodFactory.getRegistration()
        for key,value in kwargs.items():
            reg.getParameter(key).value = value
        # TODO: Calling setByRegistration is inefficient here, because
        # we're not changing the RCF's current registration.
        # setByRegistration() will completely rebuild the widget.  Add
        # a new RCF function that just updates widgets with values
        # from the current registration.
        mainthread.runBlock(
            self.selectionMethodFactory.setByRegistration, (reg,))


    def layerChangeCB(self):
        # Called when layers have been added, removed, or moved in the gfxwindow
        self.updateSelectionMethods()
        self.sensitize()

    ## TODO: What's the difference between 'new pixel selection' and
    ## 'pixel selection changed', and why does the Pixel selection
    ## toolbox always respond to the first but not to the second
    ## unless the toolbox is active?

    def newSelection(self, selectionMethod, pointlist):
        # sb callback for 'new pixel selection' 
        debug.mainthreadTest()
        if selectionMethod is not None:
            self.selectionMethodFactory.setByRegistration(
                selectionMethod.getRegistration())
            self.sensitize()

    def changedSelection(self, selection): # switchboard callback
        # sb callback for 'pixel selection changed'.  
        self.sensitize()
        self.setInfo()

    def sensitize(self):
        if self.currentGUI is not None:
            self.currentGUI.sensitize()
        subthread.execute(self.sensitize_subthread)

    def sensitize_subthread(self):
        debug.subthreadTest()

        source = self.getSelectionSource()
        try:        # The source may not have been completely built yet...
            selection = source.getSelectionContext(**self.toolbox.extrakwargs)
        except AttributeError:
            selection = None
        if source is None or selection is None:
            (u,r,c,i) = (0,0,0,0)
        else:
            selection.begin_reading()
            try:
                u = selection.undoable()
                r = selection.redoable()
                c = selection.clearable()
                i = 1
            finally:
                selection.end_reading()
        mainthread.runBlock(self._set_button_sensitivities, (u,r,c,i))
        #gtklogger.checkpoint(self.gfxwindow().name + " " + self.name() + " sensitized")
        
    def _set_button_sensitivities(self, u,r,c,i):
        debug.mainthreadTest()
        self.undobutton.set_sensitive(u)
        self.redobutton.set_sensitive(r)
        self.clearbutton.set_sensitive(c)
        self.invertbutton.set_sensitive(i)

    def setInfo(self):
        debug.mainthreadTest()
        subthread.execute(self.setInfo_subthread)

    def setInfo_subthread(self):
        debug.subthreadTest()
            
        source = self.getSelectionSource()
        if source is not None:
            source.begin_reading()
            try:
                selection = source.getSelectionContext(
                    **self.toolbox.extrakwargs)
                ## Selection can be None because an Image must be created
                ## before a Microstructure, but the selection source for
                ## an Image is its Microstructure.
                if selection is not None:
                    selection.begin_reading()
                    try:
                        sizetextdata = `selection.size()`
                    finally:
                        selection.end_reading()
                else:
                    sizetextdata = '0'
            finally:
                source.end_reading()
        else:
            sizetextdata = self.toolbox.emptyMessage()

        mainthread.runBlock(self._write_text, (sizetextdata,))
        #gtklogger.checkpoint("selection info updated")
            
    def _write_text(self, txt):
        self.sizetext.set_text(txt)
        
    def updateSelectionMethods(self):
        reg = self.selectionMethodFactory.getRegistration()
        if reg:
            selmeth = self.selectionMethodFactory.getRegistration().name()
        else:
            selmeth = None
        self.selectionMethodFactory.update(self.method.registry, obj=selmeth)

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def _runSimpleMenuCommand(self, menuitem):
        # Call the Undo, Redo, Clear, or Invert menu items.  They all
        # take a single argument which might have different names but
        # whose value is always the Who object whose selection is
        # being cleared.
        assert menuitem.nargs() == 1
        menuitem.params[0].value = self.getSourceName()
        menuitem.callWithDefaults()

    def undoCB(self, button):
        self._runSimpleMenuCommand(self.toolbox.menu.Undo)

    def redoCB(self, button):
        self._runSimpleMenuCommand(self.toolbox.menu.Redo)

    def clearCB(self, button):
        self._runSimpleMenuCommand(self.toolbox.menu.Clear)

    def invertCB(self, button):
        self._runSimpleMenuCommand(self.toolbox.menu.Invert)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# SelectionMethodGUI is the base class for the GUIs for particular
# selection methods.  Each selection method that has non-trivial gui
# requirements has an associated SelectionMethodGUI.  The
# SelectionMethodGUIs handle or delegate the construction of the gtk
# widgets in the toolbox (the contents of the toolbox's
# RegisteredClassFactory for a selection method), specify the
# low-level and high-level mouse handlers, and interact with the vtk
# display layer that's providing user feedback.

# SelectionMethodGUIs are associated with SelectionMethods with this
# decorator, which is applied to the SelectionMethodGUI class. The
# argument(s) of the decorator are the GenericSelectionMethods that
# the gui applies to.  The decorator adds a "gui" member to the
# SelectionMethod's registration.

def selectionGUIfor(*_selectorClasses):
    def decorator(guicls):
        for cls in _selectorClasses:
            cls.registration.gui = guicls
        return guicls
    return decorator
    



class SelectionMethodGUI(mousehandler.MouseHandler):
    # Base class for PointSelctorGUI, RectangularPrismSelectorGUI, etc.
    def __init__(self, toolbox):
        self.toolbox = toolbox
        # When this GUI is active, methodRegistration is set to the
        # Registration of the SelectionMethod that it's constructing.
        self.methodRegistration = None
    def gfxwindow(self):
        return self.toolbox.gfxwindow()
    
    def __call__(self, params, scope=None, name=None, verbose=False):
        # This function may be redefined for derived classes.  It
        # should return a ParameterWidget of some sort.  It must be
        # called __call__ because it's called by
        # RegisteredClassFactory.makeWidget, which thinks it's
        # instantiating an object of a class.  The default version
        # here does what RegisteredClassFactory does if it doesn't a
        # specialized widget isn't defined.
        return parameterwidgets.ParameterTable(params,
                                               scope=scope,
                                               name=name,
                                               showLabels=True,
                                               verbose=verbose)
    
    # def cancel(self):
    #     # This function should be redefined for derived classes. It
    #     # should be used to notify a SelectionMethodGUI to cancel any
    #     # subthreads it started, and should be called when the
    #     # SelectionMethodGUI's toolboxGUI is being closed.
    #     pass

    def setCurrentRegistration(self, reg):
        self.methodRegistration = reg

    def mouseHandler(self):
        return mousehandler.NullMouseHandler()

    def close(self):
        # close() is called whent the toolbox is closing.  It should
        # do any necessary cleanup.  It can assume that the
        # mousehandler (if any) has already been stopped.
        pass

    # activate() and deactivate() are called when the toolbox is
    # activated and deactivated.
    def activate(self):
        pass
    def deactivate(self):
        pass

    def sensitize(self):
        pass

