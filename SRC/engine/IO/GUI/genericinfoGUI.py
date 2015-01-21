# -*- python -*-
# $RCSfile: genericinfoGUI.py,v $
# $Revision: 1.1.2.7 $
# $Author: langer $
# $Date: 2014/11/05 16:54:51 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import subthread
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.common.IO.GUI import tooltips

import gtk

xpadding = 3
xoptions = gtk.EXPAND | gtk.FILL

class GenericInfoModeGUI(object):
    def __init__(self, gfxtoolbox):
        debug.mainthreadTest()
        self.mode = None        # corresponding non-gui GenericInfoMode object
        self.gfxtoolbox = gfxtoolbox # subclass of GenericInfoToolboxGUI
        self.menu = self.gfxtoolbox.toolbox.menu
        
        self.gtk = gtk.Frame(self.targetName + " Information")
        self.gtk.set_shadow_type(gtk.SHADOW_IN)
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, self.targetName+"Information")
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.gtk.add(scroll)
        # This vbox just keeps the table from expanding inside the
        # scrolledwindow.
        vbox = gtk.VBox()
        scroll.add_with_viewport(vbox)
        self.table = gtk.Table()
        vbox.pack_start(self.table, expand=0, fill=0)
        self.choosers = {}      # key = mode name, value=chooser listing objs
        self.sbcallbacks = []

    def getContext(self):
        return self.gfxtoolbox.toolbox.getContext()

    def destroy(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        mainthread.runBlock(self.gtk.destroy)
        self.gfxtoolbox = None

    def labelmaster(self, column, row, labeltext):
        debug.mainthreadTest()
        label = gtk.Label(labeltext)
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, column[0],column[1], row[0],row[1],
                          xpadding=xpadding, xoptions=gtk.FILL)

    def entrymaster(self, column, row, editable=0):
        debug.mainthreadTest()
        entry = gtk.Entry()
        entry.set_size_request(12*guitop.top().digitsize, -1)
        entry.set_editable(editable)
        self.table.attach(entry, column[0],column[1], row[0],row[1],
                          xpadding=xpadding, xoptions=xoptions)
        return entry

    def setMode(self, mode):
        self.mode = mode

    # Construct the list of other mode objects associated with an
    # object in this mode.  Only the name of the other mode is passed
    # in, because the other mode object might not exist yet.
    def makeObjList(self, othermodename, column, row):
        debug.mainthreadTest()
        chsr = chooser.FramedChooserListWidget(
            callback=self.singleClickCB, dbcallback=self.doubleClickCB,
            autoselect=0,
            name=othermodename+"List",
            cbkwargs=dict(modename=othermodename))
        self.table.attach(chsr.gtk, column[0], column[1], row[0], row[1],
                          xpadding=xpadding, xoptions=xoptions)
        self.choosers[othermodename] = chsr
        return chsr

    def clearObjLists(self):
        for chsr in self.choosers.values():
            chsr.update([])

    # All queryable objects must have a uiIdentifier() method
    # accessible from Python.  It must return an integer that
    # identifies the object, and which can be passed to the
    # corresponding GenericInfoMode subclass's resolveQuery() routine
    # to retrieve the object.
    def singleClickCB(self, obj, interactive, modename):
        if obj is None:
            indx = None
        else:
            indx = obj.uiIdentifier()
        if interactive:
            self.menu.Peek(mode=modename, index=indx)

    def doubleClickCB(self, obj, modename):
        self.gfxtoolbox.changeModeWithObjectID(
            obj.uiIdentifier(), self.gfxtoolbox.getGfxMode(modename))

    def peek(self, mode):
        peekobj = self.gfxtoolbox.toolbox.getPeekObject(
            self.gfxtoolbox.getMode(mode.targetName))
        try:
            self.choosers[mode.targetName].set_selection(peekobj)
        except KeyError:
            pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class GenericInfoToolboxGUI(toolboxGUI.GfxToolbox, mousehandler.MouseHandler):
    def __init__(self, name, infotb):
        toolboxGUI.GfxToolbox.__init__(self, name, infotb)
        self.mainbox = gtk.VBox()
        self.gtk.add(self.mainbox)

        ## TODO 3.1: Save the gui mode objects in the non-gui objects, and
        ## access them by asking the non-gui toolbox for the mode
        ## object (by name), and ask the mode object for the gui mode
        ## object.
        self.modeobjdict = {}   # key = mode name, value = mode instance

        self.clickIDs = {}

        clickframe = gtk.Frame()
        gtklogger.setWidgetName(clickframe, 'Click')
        clickframe.set_shadow_type(gtk.SHADOW_IN)
        self.mainbox.pack_start(clickframe, expand=0, fill=0)
        clickbox = gtk.VBox()
        clickframe.add(clickbox)

        hbox = gtk.HBox()
        clickbox.pack_start(hbox, expand=0, fill=0)
        hbox.pack_start(gtk.Label("Click on an: "), expand=0, fill=0)

        firstbutton = None
        firstmode = None
        self.modebuttonsignals = {}
        self.modebuttondict = {}
        buttons = []

        # Each subclass of GenericInfoToolboxGUI defines
        # modeClassDict(), which returns an ordered dictionary of
        # subclasses of GenericInfoModeGUI keyed by name.  The
        # dictionary is ordered just to make the initially selected
        # mode predictable.

        for modename, modeclass in self.modeClassDict().items():
            # Construct the GenericInfoModeGUI instances, which create
            # the widgets for the mode.
            mode = self.modeobjdict[modename] = modeclass(self)
            self.toolbox.getMode(modename).setGfxMode(mode)
            # Construct buttons for switching modes.
            if firstbutton is None:
                button = gtk.RadioButton(label=modename)
                firstbutton = button
                firstmode = mode
                # button.set_active(True)
                self.currentMode = modename
            else:
                button = gtk.RadioButton(label=modename, group=firstbutton)
                # button.set_active(False)
            buttons.append(button)
            gtklogger.setWidgetName(button, modename)
            self.modebuttondict[mode] = button
            tooltips.set_tooltip_text(button,
                                      "Show " + modename + " information.")
            self.modebuttonsignals[mode] = gtklogger.connect(
                button, 'clicked', self.changeModeCB, modename)

        firstbutton.set_active(True)

        # Place the button widgets in the hbox.  This is done by the
        # derived class, because the best arrangement may depend on
        # the number of buttons or other criteria.
        self.packModeButtons(hbox, buttons)

        # In 2D, information about the mouse click position is
        # displayed here.  It's not done in 3D because the conversion
        # from screen to physical coordinates depends on the query
        # mode.

        # Frame for info about the queried object.
        self.infoframe = gtk.Frame()
        self.infoframe.set_shadow_type(gtk.SHADOW_NONE)
        self.mainbox.pack_start(self.infoframe, expand=1, fill=1)
        
        # Install the first set of widgets.
        self.installInfoGUI(firstmode)

        # Subclasses may add extra buttons via this hook:
        self.addExtraWidgets(self.mainbox)

        # History buttons
        buttonbox = gtk.HBox()
        self.mainbox.pack_start(buttonbox, expand=0, fill=0)
        self.prev = gtkutils.prevButton()
        tooltips.set_tooltip_text(self.prev, "Go back to the previous object.")
        gtklogger.connect(self.prev, 'clicked', self.prevQuery)
        buttonbox.pack_start(self.prev, expand=0, fill=0, padding=2)
        
        self.clear = gtk.Button(stock=gtk.STOCK_CLEAR)
        gtklogger.setWidgetName(self.clear, 'Clear')
        gtklogger.connect(self.clear, 'clicked', self.clearButtonCB)
        tooltips.set_tooltip_text(self.clear, "Clear the current query.")
        buttonbox.pack_start(self.clear, expand=1, fill=1, padding=2)

        self.next = gtkutils.nextButton()
        tooltips.set_tooltip_text(self.next, "Go to the next object.")
        gtklogger.connect(self.next, 'clicked', self.nextQuery)
        buttonbox.pack_start(self.next, expand=0, fill=0, padding=2)


        self.mainbox.show_all()
        self.clearClickIDs()    # must be called after modeobjdict is filled
        self.sensitize()

        self.sbcallbacks = [
            switchboard.requestCallback((self.toolbox, "query"), self.queryCB),
            switchboard.requestCallbackMain((self.toolbox, "peek"),
                                            self.peekCB),
            switchboard.requestCallback((self.toolbox, "clear"), self.clearCB)
            ]

    def addExtraWidgets(self, vbox):
        pass

    def sensitize(self):
        debug.mainthreadTest()
        self.clear.set_sensitive(self.toolbox.currentQuery() != (None, None))
        self.prev.set_sensitive(not self.toolbox.queries.atBottom())
        self.next.set_sensitive(not self.toolbox.queries.atTop())
        #gtklogger.checkpoint(self.gfxwindow().name + " " + self._name + " sensitized")

    def activate(self):
        toolboxGUI.GfxToolbox.activate(self)
        self.gfxwindow().setMouseHandler(self)
        self.sensitize()
        if config.dimension() == 3:
            self.gfxwindow().toolbar.setSelect()

    def close(self):
        for modeobj in self.modeobjdict.values():
            modeobj.destroy()
        map(switchboard.removeCallback, self.sbcallbacks)
        toolboxGUI.GfxToolbox.close(self)

    def acceptEvent(self, eventtype):
        return eventtype == 'up'

    def up(self, x, y, shift, ctrl):
        canvas = self.toolbox.gfxwindow().oofcanvas
        view = canvas.get_view()
        realpt = canvas.display2Physical(view, x, y)
        subthread.execute(self.finish_up, (realpt, view))
    def finish_up(self, realpt, view):
        # Store object indices for *all* modes, so that the radio
        # buttons work correctly.
        for modename, mode in self.modeobjdict.items():
            self.clickIDs[modename] = mode.findObjectIndex(realpt, view)
        self.issueQueryCmd(self.modeobjdict[self.currentMode],
                           self.clickIDs[self.currentMode])

    def getGfxMode(self, modename):
        return self.modeobjdict[modename]

    def getMode(self, modename):
        return self.toolbox.getMode(modename)

    def replaceInfoGUI(self, mode):
        debug.mainthreadTest()
        assert isinstance(mode, GenericInfoModeGUI)
        if mode and self.currentMode != mode.targetName:
            if self.currentMode is not None:
                self.infoframe.remove(self.modeobjdict[self.currentMode].gtk)
            self.installInfoGUI(mode) # sets currentMode
            self.infoframe.show_all()

    def installInfoGUI(self, mode):
        assert isinstance(mode, GenericInfoModeGUI)
        self.currentMode = mode.targetName
        self.infoframe.add(self.modeobjdict[mode.targetName].gtk)
        # Set the radio button for the current mode, and unset the one
        # for the previous mode, without invoking the buttons'
        # callbacks.  The radio buttons invoke their callbacks both
        # when they're activated and when they're deactivated, so the
        # call to set_active() here will invoke the callback
        # (changeModeCB) twice.  However that callback only runs when
        # its button is active, so here we only have to block the
        # signal for the new mode, not the old one.
        self.modebuttonsignals[mode].block()
        self.modebuttondict[mode].set_active(True)
        self.modebuttonsignals[mode].unblock()

    def queryCB(self, mode, indx): # sb (toolbox, "query")
        mainthread.runBlock(self.replaceInfoGUI, (mode,)) 
        self.update()
        mainthread.runBlock(self.sensitize)

    def peekCB(self, mode): # sb (toolbox, "peek")
        mainthread.runBlock(self.modeobjdict[self.currentMode].peek, (mode,))
        self.sensitize()

    def update(self):
        # Update the info in the current mode object.
        mode, indx = self.toolbox.currentQuery()
        if mode:
            mode.gfxmode.update(indx)

    def clearClickIDs(self):
        # This is also used to initialize clickIDs, so it can't loop
        # over clickIDs.keys.
        for modename in self.modeobjdict:
            self.clickIDs[modename] = None

    def clearButtonCB(self, gtkobj):
        self.toolbox.menu.Clear()

    def clearCB(self):         # switchboard (toolbox, "clear")
        self.clearClickIDs()
        self.update()
        mainthread.runBlock(self.sensitize)

    def issueQueryCmd(self, mode, indx):
        self.toolbox.menu.Query(mode=mode.targetName, index=indx)

    def issuePeekCmd(self, mode, indx):
        self.toolbox.menu.Peek(mode=mode.targetName, index=indx)

    def changeModeCB(self, button, modename): # radio button callback
        if button.get_active():
            if self.currentMode != modename:
                if self.clickIDs[modename] is not None:
                    self.issueQueryCmd(self.modeobjdict[modename],
                                       self.clickIDs[modename])
                else:
                    # The new mode has no pre-clicked selection.  No
                    # menu command is issued, because there's no
                    # selection being made, so we need to do some
                    # extra housekeeping here. 
                    mode = self.modeobjdict[modename]
                    subthread.execute(mode.update, (None,))
                    self.replaceInfoGUI(mode)
                    self.toolbox.clearQuery()
                    # Update the gfx layer
                    switchboard.notify((self.gfxwindow(), 
                                        "query " + self.toolbox.whoClassName)) 
                    # Redraw
                    subthread.execute(self.gfxwindow().draw)
                self.sensitize()
            
    def changeModeWithObjectID(self, objid, mode):
        # Called from double-click callback on the node list.  Always
        # switches modes.
        oldmode, oldindx = self.toolbox.currentQuery()
        self.issueQueryCmd(mode, objid) # causes mode switch
        self.issuePeekCmd(oldmode, oldindx)
        self.sensitize()
        
    def prevQuery(self, gtkobj):
        self.clearClickIDs()
        self.toolbox.menu.Prev()

    def nextQuery(self, gtkobj):
        self.clearClickIDs()
        self.toolbox.menu.Next()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Utility function that converts a position to a string, either (x, y)
# or (x, y, z).  The __repr__ for the Point and Coord classes include
# the name of the class, which is too wordy for the Info GUIs.
## TODO: Move this function into the Point and/or Coord classes.

# fmt is "(%g, %g)" in 2D and "(%g, %g, %g)" in 3D
_fmt = "(" + ", ".join(["%g"]*config.dimension()) + ")"

def posString(pos):
    return _fmt % tuple(pos)
    
