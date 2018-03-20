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

# class HistoricalSelection:
#     def __init__(self, selectionMethod, points):
#         # Store a copy of the selection method.
#         self.selectionMethod = selectionMethod
#         self.points = points            # mouse coordinates
#     def __repr__(self):
#         return "HistoricalSelection(%s, %s)" %\
#                (self.selectionMethod, self.points)


class SelectionMethodFactory(regclassfactory.RegisteredClassFactory):
    def __init__(self, registry, obj=None, title=None,
                 callback=None, fill=0, expand=0, scope=None, name=None,
                 widgetdict={}, *args, **kwargs):
        self.current_who_class = None
        regclassfactory.RegisteredClassFactory.__init__(
            self, registry, obj=obj, title=title, callback=callback,
            fill=fill, expand=expand, scope=scope, name=name,
            widgetdict=widgetdict, *args, **kwargs)
    def set_whoclass_name(self, name):
        self.current_who_class = name
    def includeRegistration(self, registration):
        if self.current_who_class is None:
            return True
        return self.current_who_class in registration.whoclasses

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class GenericSelectToolboxGUI(toolboxGUI.GfxToolbox):
    def __init__(self, toolbox, method):
        debug.mainthreadTest()
        toolboxGUI.GfxToolbox.__init__(self, toolbox)
        self.method = method            # RegisteredClass of selection methods
        self.points = []                # locations of mouse events
        # Was a modifier key pressed during the last button event?
        self.shift = 0                 
        self.ctrl = 0

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
        # self.historian = historian.Historian(self.setHistory,
        #                                      self.sensitizeHistory)
        # self.selectionMethodFactory.add_callback(self.historian.stateChangeCB)

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

        # # Selection history
        # frame = gtk.Frame('History')
        # frame.set_shadow_type(gtk.SHADOW_IN)
        # outerbox.pack_start(frame, expand=0, fill=0)
        # vbox = gtk.VBox()

        # frame.add(vbox)
        
        # table = gtk.Table(rows=2, columns=3)
        # vbox.pack_start(table, expand=0, fill=0)
        # table.attach(gtk.Label('down'), 0,1, 0,1, xoptions=0, yoptions=0)
        # table.attach(gtk.Label('up'), 0,1, 1,2, xoptions=0, yoptions=0)

        # ## TODO: Since the interpretation of the xyz values for the
        # ## mouse click position requires knowing what's been clicked,
        # ## can it be done here at all?  Does it make sense to display
        # ## the position?  Does repeating a selection make sense?  Is
        # ## there any point in keeping the history?  Repeating makes
        # ## sense if the user just wants to modifiy the parameters but
        # ## not the position for a selection.  But should it repeat at
        # ## the same screen coordinates or on the same clicked object?
        # self.xdownentry = gtk.Entry()
        # self.ydownentry = gtk.Entry()
        # self.xupentry = gtk.Entry()
        # self.yupentry = gtk.Entry()
        # gtklogger.setWidgetName(self.xdownentry, 'xdown')
        # gtklogger.setWidgetName(self.ydownentry, 'ydown')
        # gtklogger.setWidgetName(self.xupentry, 'xup')
        # gtklogger.setWidgetName(self.yupentry, 'yup') # yessirree, Bob!
        # entries = [self.xdownentry, self.ydownentry, self.xupentry,
        #            self.yupentry]
        # if config.dimension() == 3:
        #     self.zdownentry = gtk.Entry()  
        #     self.zupentry = gtk.Entry()
        #     gtklogger.setWidgetName(self.zdownentry, 'zdown')  
        #     gtklogger.setWidgetName(self.zdownentry, 'zup')
        #     entries.append(self.zdownentry)
        #     entries.append(self.zupentry)
        # self.entrychangedsignals = []
        # for entry in entries:
        #     entry.set_size_request(12*guitop.top().digitsize, -1)
        #     self.entrychangedsignals.append(
        #         gtklogger.connect(entry, "changed", self.poschanged))
        # table.attach(self.xdownentry, 1,2, 0,1)
        # table.attach(self.ydownentry, 2,3, 0,1)
        # table.attach(self.xupentry, 1,2, 1,2)
        # table.attach(self.yupentry, 2,3, 1,2)
        # if config.dimension() == 3:
        #     table.attach(self.zdownentry, 3,4, 0,1)
        #     table.attach(self.zupentry, 3,4, 1,2)
        # hbox = gtk.HBox(spacing=2)
        # vbox.pack_start(hbox, expand=0, fill=0)
        # self.prevmethodbutton = gtkutils.prevButton()
        # self.repeatbutton = gtkutils.StockButton(gtk.STOCK_REFRESH, 'Repeat')
        # gtklogger.setWidgetName(self.repeatbutton, 'Repeat')
        # self.nextmethodbutton = gtkutils.nextButton()
        # hbox.pack_start(self.prevmethodbutton, expand=0, fill=0)
        # hbox.pack_start(self.repeatbutton, expand=1, fill=0)
        # hbox.pack_start(self.nextmethodbutton, expand=0, fill=0)
        # gtklogger.connect(self.repeatbutton, 'clicked', self.repeatCB)
        # gtklogger.connect(self.repeatbutton, 'button-release-event',
        #                   self.repeateventCB)
        # gtklogger.connect(self.prevmethodbutton, 'clicked',
        #                   self.historian.prevCB)
        # gtklogger.connect(self.nextmethodbutton, 'clicked',
        #                  self.historian.nextCB)
        # tooltips.set_tooltip_text(self.prevmethodbutton,
        #       "Recall the settings and mouse coordinates for the previous"
        #      " selection method.")
        # tooltips.set_tooltip_text(self.nextmethodbutton,
        #       "Recall the settings and mouse coordinates for the next"
        #       " selection method.")
        # tooltips.set_tooltip_text(self.repeatbutton,
        #       "Execute the selection method as if the mouse had been clicked"
        #       " at the above coordinates.  Hold the shift key to retain the"
        #       " previous selection.  Hold the control key to toggle the"
        #       " selection state of the selected pixels.")
        

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

    def getSource(self):
        return self.toolbox.getSource()

    def getSourceName(self):
        return self.toolbox.getSourceName()

    def invokeMenuItem(self, method):
        # method is a SelectionMethod subclass
        menuitem = self.toolbox.menuitem
        source = method.getSourceName(self.gfxwindow())
        # self.toolbox.setSourceParams(menuitem, source)

        ## TODO: This assumes that the relevant mouse button state is
        ## what the handler recorded last.  Is that always a correct
        ## assumption?
        buttons = self.currentMouseHandler.buttons

        ## TODO: Move the selection operator stuff out of
        ## pixelselectionmod, because this file is for generic
        ## selections.

        menuitem.callWithDefaults(
            source=source,
            method=method,
            operator=pixelselectionmod.getSelectionOperator(buttons))

    def getParamValues(self, *paramnames):
        # Return the values of the given parameters from the
        # RegisteredClassFactory.
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
        source = self.getSource()
        if source:
            self.selectionMethodFactory.set_whoclass_name(source.getClassName())
        else:
            self.selectionMethodFactory.set_whoclass_name(None)
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
            # self.historian.record(HistoricalSelection(selectionMethod,
            #                                           pointlist))
            # self.setCoordDisplay(selectionMethod.getRegistration(), pointlist)
            self.selectionMethodFactory.setByRegistration(
                selectionMethod.getRegistration())
            self.sensitize()

    def changedSelection(self, selection): # switchboard callback
        # sb callback for 'pixel selection changed'.  
        self.sensitize()
        self.setInfo()

    # def poschanged(self, *args):
    #     self.sensitizeHistory()
            
    # def setHistory(self, historicalSelection):
    #     self.selectionMethodFactory.set(historicalSelection.selectionMethod,
    #                                     interactive=1)
    #     self.setCoordDisplay(
    #         historicalSelection.selectionMethod.getRegistration(),
    #         historicalSelection.points)

    def sensitize(self):
        if self.currentGUI is not None:
            self.currentGUI.sensitize()
        subthread.execute(self.sensitize_subthread)

    def sensitize_subthread(self):
        debug.subthreadTest()

        source = self.getSource()
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
        # self.sensitizeHistory()

    # def sensitizeHistory(self):
    #     debug.mainthreadTest()
    #     self.nextmethodbutton.set_sensitive(self.historian.nextSensitive())
    #     self.prevmethodbutton.set_sensitive(self.historian.prevSensitive())
    #     self.repeatbutton.set_sensitive(len(self.historian) > 0
    #                                     and self.repeatable())

    def setInfo(self):
        debug.mainthreadTest()
        subthread.execute(self.setInfo_subthread)

    def setInfo_subthread(self):
        debug.subthreadTest()
            
        source = self.getSource()
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
        selmeth = self.selectionMethodFactory.getRegistration().name()
        self.selectionMethodFactory.update(self.method.registry, obj=selmeth)

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def runSimpleMenuCommand(self, menuitem):
        # Call the Undo, Redo, Clear, or Invert menu items.  They all
        # take a single argument which might have different names but
        # whose value is always the Who object whose selection is
        # being cleared.
        assert menuitem.nargs() == 1
        menuitem.params[0].value = self.getSourceName()
        menuitem.callWithDefaults()

    def undoCB(self, button):
        self.runSimpleMenuCommand(self.toolbox.menu.Undo)
        # self.toolbox.menu.Undo(source=self.getSourceName())

    def redoCB(self, button):
        self.runSimpleMenuCommand(self.toolbox.menu.Redo)
        # self.toolbox.menu.Redo(source=self.getSourceName())

    def clearCB(self, button):
        self.runSimpleMenuCommand(self.toolbox.menu.Clear)
        # self.toolbox.menu.Clear(source=self.getSourceName())

    def invertCB(self, button):
        self.runSimpleMenuCommand(self.toolbox.menu.Invert)
        # self.toolbox.menu.Invert(source=self.getSourceName())


    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # Command history
    
    # def repeatCB(self, button):
    #     debug.mainthreadTest()
    #     selmeth = self.selectionMethodFactory.getRegistration()
    #     if selmeth is not None:
    #         # Get the coordinates of the points from the widgets.  If
    #         # the selection method uses 'move' events, then those
    #         # points have to come from the Historian, because there's
    #         # no widget for them.
    #         if 'move' in selmeth.events:
    #             points = self.historian.current().points[:]
    #         else:
    #             points = [None]         # dummy array, will be filled later
    #         # Also, the list of points from the Historian might not
    #         # have the right length. 
    #         if 'up' in selmeth.events and 'down' in selmeth.events:
    #             # need two points, at least
    #             if len(points) == 1:
    #                 points.append(None)
    #         # Get the (possibly) edited values from the widgets
    #         try:
    #             if 'down' in selmeth.events:
    #                 if config.dimension() == 2:
    #                     points[0] = primitives.Point(
    #                         utils.OOFeval(self.xdownentry.get_text()),
    #                         utils.OOFeval(self.ydownentry.get_text()))
    #                 elif config.dimension() == 3:
    #                     points[0] = primitives.Point(
    #                         utils.OOFeval(self.xdownentry.get_text()),
    #                         utils.OOFeval(self.ydownentry.get_text()),
    #                         utils.OOFeval(self.zdownentry.get_text()))
    #             if 'up' in selmeth.events:
    #                 if config.dimension() == 2:
    #                     points[-1] = primitives.Point(
    #                         utils.OOFeval(self.xupentry.get_text()),
    #                         utils.OOFeval(self.yupentry.get_text()))
    #                 elif config.dimension() == 3:
    #                     points[-1] = primitives.Point(
    #                         utils.OOFeval(self.xupentry.get_text()),
    #                         utils.OOFeval(self.yupentry.get_text()),
    #                         utils.OOFeval(self.zupentry.get_text()))
    #         except:        # Shouldn't happen, if sensitization is working
    #             raise "Can't evaluate coordinates!"
    #         actual_who = self.getSource()
    #         if actual_who:
    #             self.selectionMethodFactory.set_defaults()
    #             menuitem = getattr(self.toolbox.menu, selmeth.name())
    #             self.toolbox.setSourceParams(menuitem, actual_who)
    #             menuitem.callWithDefaults(points=points,
    #                                       shift=self.shift, ctrl=self.ctrl)

    # def repeateventCB(self, button, gdkevent):
    #     # Callback for 'button-release-event' on the 'Repeat' button.
    #     # This function is called before repeatCB and stores the
    #     # modifier key state.  This function is called whenever the
    #     # mouse is released as long as it was pushed on the 'Repeat'
    #     # button, so it can't be used as the actual button callback.
    #     # repeatCB is called only if the mouse is actually released on
    #     # the button, but doesn't have access to the modifier keys
    #     # like repeateventCB does.
    #     self.shift = (gdkevent.state & gtk.gdk.SHIFT_MASK != 0)
    #     self.ctrl = (gdkevent.state & gtk.gdk.CONTROL_MASK != 0)

    # def repeatable(self):
    #     # Check that the mouse coord entry widgets contain appropriate
    #     # data.
    #     debug.mainthreadTest()
    #     selmeth = self.selectionMethodFactory.getRegistration()
    #     try:
    #         if 'down' in selmeth.events:
    #             # OOFeval raises exceptions if the text is not a valid
    #             # Python expression
    #             utils.OOFeval(self.xdownentry.get_text())
    #             utils.OOFeval(self.ydownentry.get_text())
    #             if config.dimension() == 3:
    #                 utils.OOFeval(self.zdownentry.get_text())
    #         if 'up' in selmeth.events:
    #             utils.OOFeval(self.xupentry.get_text())
    #             utils.OOFeval(self.yupentry.get_text())
    #             if config.dimension() == 3:
    #                 utils.OOFeval(self.zupentry.get_text())
    #     except:
    #         return 0
    #     return 1

    # def setCoordDisplay(self, selectionMethodReg, points):
    #     debug.mainthreadTest()
    #     for sig in self.entrychangedsignals:
    #         sig.block()
    #     try:
    #         if 'down' in selectionMethodReg.events:
    #             self.xdownentry.set_text(("%-8g" % points[0].x).rstrip())
    #             self.ydownentry.set_text(("%-8g" % points[0].y).rstrip())
    #             if config.dimension() == 3:
    #                 self.zdownentry.set_text(("%-8g" % points[0].z).rstrip())
    #         else:
    #             self.xdownentry.set_text('--')
    #             self.ydownentry.set_text('--')
    #             if config.dimension() == 3:
    #                 self.zdownentry.set_text('--')
    #         if 'up' in selectionMethodReg.events:
    #             self.xupentry.set_text(("%-8g" % points[-1].x).rstrip())
    #             self.yupentry.set_text(("%-8g" % points[-1].y).rstrip())
    #             if config.dimension() == 3:
    #                 self.zupentry.set_text(("%-8g" % points[-1].z).rstrip())
    #         else:
    #             self.xupentry.set_text('--')
    #             self.yupentry.set_text('--')
    #             if config.dimension() == 3:
    #                 self.zdownentry.set_text('--')
    #     except IndexError:
    #         pass
    #     finally:
    #         for sig in self.entrychangedsignals:
    #             sig.unblock()


 
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

