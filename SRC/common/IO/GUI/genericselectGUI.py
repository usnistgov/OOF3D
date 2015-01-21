# -*- python -*-
# $RCSfile: genericselectGUI.py,v $
# $Revision: 1.40.8.20 $
# $Author: fyc $
# $Date: 2014/07/21 18:09:12 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Base class for Selection toolboxes.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common.IO.GUI import rubberband3d as rubberband
from ooflib.common import debug
from ooflib.SWIG.common import guitop
from ooflib.common import primitives
from ooflib.common import subthread
from ooflib.common import mainthread
from ooflib.common import utils
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import historian
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.common.IO.GUI import tooltips
import gtk, sys

class HistoricalSelection:
    def __init__(self, selectionMethod, points):
        # Store a copy of the selection method.
        self.selectionMethod = selectionMethod
        self.points = points            # mouse coordinates
    def __repr__(self):
        return "HistoricalSelection(%s, %s)" %\
               (self.selectionMethod, self.points)


# Base class common to all selection toolboxes.  Needs access to the
# selectionmethod registry in order to build the
# registeredclassfactory.

# Subclasses *must* provide:
#  getSource()  returns the Who object within which the selection is made
#  finish_up()  completes the selection operation
#  undoCB()     gtk callback for undo button
#  redoCB()
#  clearCB()
#  invertCB()
#  methodFactory()  Returns a RegisteredClassFactory for the
#                                                 appropriate registry.

class GenericSelectToolboxGUI(toolboxGUI.GfxToolbox,
                              mousehandler.MouseHandler):
    def __init__(self, name, toolbox, method):
        debug.mainthreadTest()
        toolboxGUI.GfxToolbox.__init__(self, name, toolbox)
        self.method = method            # RegisteredClass of selection methods
        self.points = []                # locations of mouse events
        # Was a modifier key pressed during the last button event?
        self.shift = 0                 
        self.ctrl = 0

        outerbox = gtk.VBox(spacing=2)
        self.gtk.add(outerbox)

##        scroll = gtk.ScrolledWindow()
##        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
##        outerbox.pack_start(scroll, expand=1, fill=1)

        # Retrieve the registered class factory from the subclass.
        self.selectionMethodFactory = self.methodFactory()
        # self.selectionMethodFactory = regclassfactory.RegisteredClassFactory(
        #     method.registry, title="Method:", name="Method")
##        scroll.add_with_viewport(self.selectionMethodFactory.gtk)
        outerbox.pack_start(self.selectionMethodFactory.gtk, expand=1, fill=1)
        self.historian = historian.Historian(self.setHistory,
                                             self.sensitizeHistory)
        self.selectionMethodFactory.set_callback(self.historian.stateChangeCB)

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

        # Selection history
        frame = gtk.Frame('History')
        frame.set_shadow_type(gtk.SHADOW_IN)
        outerbox.pack_start(frame, expand=0, fill=0)
        vbox = gtk.VBox()

        frame.add(vbox)
        
        table = gtk.Table(rows=2, columns=3)
        vbox.pack_start(table, expand=0, fill=0)
        table.attach(gtk.Label('down'), 0,1, 0,1, xoptions=0, yoptions=0)
        table.attach(gtk.Label('up'), 0,1, 1,2, xoptions=0, yoptions=0)

        self.xdownentry = gtk.Entry()
        self.ydownentry = gtk.Entry()
        self.xupentry = gtk.Entry()
        self.yupentry = gtk.Entry()
        gtklogger.setWidgetName(self.xdownentry, 'xdown')
        gtklogger.setWidgetName(self.ydownentry, 'ydown')
        gtklogger.setWidgetName(self.xupentry, 'xup')
        gtklogger.setWidgetName(self.yupentry, 'yup') # yessirree, Bob!
        entries = [self.xdownentry, self.ydownentry, self.xupentry,
                   self.yupentry]
        if config.dimension() == 3:
            self.zdownentry = gtk.Entry()  
            self.zupentry = gtk.Entry()
            gtklogger.setWidgetName(self.zdownentry, 'zdown')  
            gtklogger.setWidgetName(self.zdownentry, 'zup')
            entries.append(self.zdownentry)
            entries.append(self.zupentry)
        self.entrychangedsignals = []
        for entry in entries:
            entry.set_size_request(12*guitop.top().digitsize, -1)
            self.entrychangedsignals.append(
                gtklogger.connect(entry, "changed", self.poschanged))
        table.attach(self.xdownentry, 1,2, 0,1)
        table.attach(self.ydownentry, 2,3, 0,1)
        table.attach(self.xupentry, 1,2, 1,2)
        table.attach(self.yupentry, 2,3, 1,2)
        if config.dimension() == 3:
            table.attach(self.zdownentry, 3,4, 0,1)
            table.attach(self.zupentry, 3,4, 1,2)
        hbox = gtk.HBox(spacing=2)
        vbox.pack_start(hbox, expand=0, fill=0)
        self.prevmethodbutton = gtkutils.prevButton()
        self.repeatbutton = gtkutils.StockButton(gtk.STOCK_REFRESH, 'Repeat')
        gtklogger.setWidgetName(self.repeatbutton, 'Repeat')
        self.nextmethodbutton = gtkutils.nextButton()
        hbox.pack_start(self.prevmethodbutton, expand=0, fill=0)
        hbox.pack_start(self.repeatbutton, expand=1, fill=0)
        hbox.pack_start(self.nextmethodbutton, expand=0, fill=0)
        gtklogger.connect(self.repeatbutton, 'clicked', self.repeatCB)
        gtklogger.connect(self.repeatbutton, 'button-release-event',
                          self.repeateventCB)
        gtklogger.connect(self.prevmethodbutton, 'clicked',
                          self.historian.prevCB)
        gtklogger.connect(self.nextmethodbutton, 'clicked',
                         self.historian.nextCB)
        tooltips.set_tooltip_text(self.prevmethodbutton,
              "Recall the settings and mouse coordinates for the previous"
             " selection method.")
        tooltips.set_tooltip_text(self.nextmethodbutton,
              "Recall the settings and mouse coordinates for the next"
              " selection method.")
        tooltips.set_tooltip_text(self.repeatbutton,
              "Execute the selection method as if the mouse had been clicked"
              " at the above coordinates.  Hold the shift key to retain the"
              " previous selection.  Hold the control key to toggle the"
              " selection state of the selected pixels.")
        

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
            switchboard.requestCallback((self.toolbox.gfxwindow(),
                                         'layers changed'),
                                        self.setInfo_subthread)
        ]

    def activate(self):
        if not self.active:
            toolboxGUI.GfxToolbox.activate(self)
            self.sensitize()
            self.sensitizeHistory()
            self.setInfo()

            self.gfxwindow().setMouseHandler(self)
            if config.dimension() == 3:
                self.gfxwindow().toolbar.setSelect()

    def deactivate(self):
        if self.active:
            # self.gfxwindow().setRubberband(rubberband.NoRubberBand())
            toolboxGUI.GfxToolbox.deactivate(self)

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        toolboxGUI.GfxToolbox.close(self)

    def getSourceName(self):
        source = self.getSource()
        if source is not None:
            return source.path()

    def layerChangeCB(self):
        # Called when layers have been added, removed, or moved in the gfxwindow
        self.sensitize()

    def newSelection(self, selectionMethod, pointlist): # switchboard callback
        debug.mainthreadTest()
        if selectionMethod is not None:
            self.historian.record(HistoricalSelection(selectionMethod,
                                                      pointlist))
            self.setCoordDisplay(selectionMethod.getRegistration(), pointlist)
            self.selectionMethodFactory.setByRegistration(
                selectionMethod.getRegistration())
            self.sensitize()

    def changedSelection(self, selection): # switchboard callback
        self.sensitize()
        self.setInfo()

    def poschanged(self, *args):
        self.sensitizeHistory()
            
    def setHistory(self, historicalSelection):
        self.selectionMethodFactory.set(historicalSelection.selectionMethod,
                                        interactive=1)
        self.setCoordDisplay(
            historicalSelection.selectionMethod.getRegistration(),
            historicalSelection.points)

    def sensitize(self):
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
        #gtklogger.checkpoint(self.gfxwindow().name + " " + self._name + " sensitized")
        
    def _set_button_sensitivities(self, u,r,c,i):
        debug.mainthreadTest()
        self.undobutton.set_sensitive(u)
        self.redobutton.set_sensitive(r)
        self.clearbutton.set_sensitive(c)
        self.invertbutton.set_sensitive(i)
        self.sensitizeHistory()

    def sensitizeHistory(self):
        debug.mainthreadTest()
        self.nextmethodbutton.set_sensitive(self.historian.nextSensitive())
        self.prevmethodbutton.set_sensitive(self.historian.prevSensitive())
        self.repeatbutton.set_sensitive(len(self.historian) > 0
                                        and self.repeatable())

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

    ###################################

    # Command history
    
    def repeatCB(self, button):
        debug.mainthreadTest()
        selmeth = self.selectionMethodFactory.getRegistration()
        if selmeth is not None:
            # Get the coordinates of the points from the widgets.  If
            # the selection method uses 'move' events, then those
            # points have to come from the Historian, because there's
            # no widget for them.
            if 'move' in selmeth.events:
                points = self.historian.current().points[:]
            else:
                points = [None]         # dummy array, will be filled later
            # Also, the list of points from the Historian might not
            # have the right length. 
            if 'up' in selmeth.events and 'down' in selmeth.events:
                # need two points, at least
                if len(points) == 1:
                    points.append(None)
            # Get the (possibly) edited values from the widgets
            try:
                if 'down' in selmeth.events:
                    if config.dimension() == 2:
                        points[0] = primitives.Point(
                            utils.OOFeval(self.xdownentry.get_text()),
                            utils.OOFeval(self.ydownentry.get_text()))
                    elif config.dimension() == 3:
                        points[0] = primitives.Point(
                            utils.OOFeval(self.xdownentry.get_text()),
                            utils.OOFeval(self.ydownentry.get_text()),
                            utils.OOFeval(self.zdownentry.get_text()))
                if 'up' in selmeth.events:
                    if config.dimension() == 2:
                        points[-1] = primitives.Point(
                            utils.OOFeval(self.xupentry.get_text()),
                            utils.OOFeval(self.yupentry.get_text()))
                    elif config.dimension() == 3:
                        points[-1] = primitives.Point(
                            utils.OOFeval(self.xupentry.get_text()),
                            utils.OOFeval(self.yupentry.get_text()),
                            utils.OOFeval(self.zupentry.get_text()))
            except:        # Shouldn't happen, if sensitization is working
                raise "Can't evaluate coordinates!"
            actual_who = self.getSource()
            if actual_who:
                self.selectionMethodFactory.set_defaults()
                menuitem = getattr(self.toolbox.menu, selmeth.name())
                self.toolbox.setSourceParams(menuitem, actual_who)
                menuitem.callWithDefaults(points=points,
                                          shift=self.shift, ctrl=self.ctrl)

    def repeateventCB(self, button, gdkevent):
        # Callback for 'button-release-event' on the 'Repeat' button.
        # This function is called before repeatCB and stores the
        # modifier key state.  This function is called whenever the
        # mouse is released as long as it was pushed on the 'Repeat'
        # button, so it can't be used as the actual button callback.
        # repeatCB is called only if the mouse is actually released on
        # the button, but doesn't have access to the modifier keys
        # like repeateventCB does.
        self.shift = (gdkevent.state & gtk.gdk.SHIFT_MASK != 0)
        self.ctrl = (gdkevent.state & gtk.gdk.CONTROL_MASK != 0)

    def repeatable(self):
        # Check that the mouse coord entry widgets contain appropriate
        # data.
        debug.mainthreadTest()
        selmeth = self.selectionMethodFactory.getRegistration()
        try:
            if 'down' in selmeth.events:
                # OOFeval raises exceptions if the text is not a valid
                # Python expression
                utils.OOFeval(self.xdownentry.get_text())
                utils.OOFeval(self.ydownentry.get_text())
                if config.dimension() == 3:
                    utils.OOFeval(self.zdownentry.get_text())
            if 'up' in selmeth.events:
                utils.OOFeval(self.xupentry.get_text())
                utils.OOFeval(self.yupentry.get_text())
                if config.dimension() == 3:
                    utils.OOFeval(self.zupentry.get_text())
        except:
            return 0
        return 1

    def setCoordDisplay(self, selectionMethodReg, points):
        debug.mainthreadTest()
        for sig in self.entrychangedsignals:
            sig.block()
        try:
            if 'down' in selectionMethodReg.events:
                self.xdownentry.set_text(("%-8g" % points[0].x).rstrip())
                self.ydownentry.set_text(("%-8g" % points[0].y).rstrip())
                if config.dimension() == 3:
                    self.zdownentry.set_text(("%-8g" % points[0].z).rstrip())
            else:
                self.xdownentry.set_text('--')
                self.ydownentry.set_text('--')
                if config.dimension() == 3:
                    self.zdownentry.set_text('--')
            if 'up' in selectionMethodReg.events:
                self.xupentry.set_text(("%-8g" % points[-1].x).rstrip())
                self.yupentry.set_text(("%-8g" % points[-1].y).rstrip())
                if config.dimension() == 3:
                    self.zupentry.set_text(("%-8g" % points[-1].z).rstrip())
            else:
                self.xupentry.set_text('--')
                self.yupentry.set_text('--')
                if config.dimension() == 3:
                    self.zdownentry.set_text('--')
        except IndexError:
            pass
        finally:
            for sig in self.entrychangedsignals:
                sig.unblock()


    ###################################
        
    # MouseHandler functions
    
    def down(self, x, y, shift, ctrl):  # mouse down
        debug.mainthreadTest()
        self.selmeth = self.selectionMethodFactory.getRegistration()
        self.selectionMethodFactory.set_defaults()
        #self.gfxwindow().setRubberband(self.selmeth.getRubberBand(self.selmeth))
        # Start collecting points
        self.points = [primitives.Point(x,y)]

    def move(self, x, y, shift, ctrl):  # mouse move
        # Continue the collection of points, if it's been started...
        if self.points:
            self.points.append(primitives.Point(x,y))

    def up(self, x, y, shift, ctrl):    # mouse up
        debug.mainthreadTest()
        # Finish the collection of points
        self.points.append(primitives.Point(x,y))
        if self.selmeth is not None:
            # Construct the list of points that the method needs
            ptlist = []
            if 'down' in self.selmeth.events:
                ptlist.append(self.points[0])
            if 'move' in self.selmeth.events and len(self.points) > 2:
                ptlist.extend(self.points[1:-2])
            if 'up' in self.selmeth.events:
                ptlist.append(self.points[-1])

            source = self.getSource()

            canvas = self.toolbox.gfxwindow().oofcanvas
            view = canvas.get_view()
            ## TODO OPT: display2Physical is potentially expensive, since
            ## it calls set_view.  If more than one point is being
            ## processed, they should all be processed in one call to
            ## display2Physical.
            realptlist = [canvas.display2Physical(view, pt.x, pt.y)
                          for pt in ptlist]

            if source:
                # We've done as much generic work as we can do --
                # we have a mouse-up event, a set of points,
                # a selection method, and a who.
                # Child classes know what to do next.
                ## TODO MER: In 3D, are all finish_up routines actually
                ## identical except for calling a different menu item?
                ## Maybe they can be all done inline here, despite
                ## what the comment says.
                self.finish_up(realptlist, view, shift, ctrl, self.selmeth)
                
            self.points = []            # get ready for next event
            
    def acceptEvent(self, eventtype): #L ocked the validation for just these three events.
        if eventtype == 'up' or eventtype == 'down' or eventtype == 'move':
	  return True
	else:
	  return False

