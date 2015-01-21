# -*- python -*-
# $RCSfile: genericinfotoolbox.py,v $
# $Revision: 1.1.2.5 $
# $Author: fyc $
# $Date: 2014/07/28 22:16:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import ringbuffer
from ooflib.common import toolbox
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

class GenericInfoMode:
    def __init__(self, tlbox):
        # tlbox is an instance of a subclass of toolbox.Toolbox, not
        # toolboxGUI.GfxToolbox.
        self.toolbox = tlbox 
        self.gfxtoolbox = None
        self.gfxmode = None

    def setGfxToolbox(self, tbox):
        self.gfxtoolbox = tbox

    def setGfxMode(self, mode):
        self.gfxmode = mode
        mode.setMode(self)

    def sendQuerySignals(self, indx):
        # update gui
        switchboard.notify((self.toolbox, "query"), self.gfxmode, indx)
        # update canvas
        switchboard.notify(
            (self.toolbox.gfxwindow(), "query " + self.toolbox.whoClassName))

    def sendPeekSignals(self, indx):
        # update gui
        switchboard.notify((self.toolbox, "peek"), self.gfxmode)
        # update canvas
        switchboard.notify(
            (self.toolbox.gfxwindow(), "peek " + self.toolbox.whoClassName), 
            self)

    # Subclasses must provide
    # resolveQuery(self, meshctxt, index) : returns the queried object

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class GenericInfoToolbox(toolbox.Toolbox):
    def __init__(self, gfxwindow, name, modes):
        toolbox.Toolbox.__init__(self, name, gfxwindow)

        self.modeobjdict = {}
        for mode in modes:
            self.modeobjdict[mode.targetName] = mode
        
        
        # Previous queries are stored as (mode, index) pairs.
        self.queries = ringbuffer.RingBuffer(49)
        self.queries.push((modes[0], None))

        # The current peek state is stored as a dictionary of indices,
        # keyed by mode.  No history is maintained.
        self.peek = {}

        self.context = None     # MeshContext or SkeletonContext or ...

        self.sbcallbacks = [
            switchboard.requestCallback((self.gfxwindow(), "layers changed"),
                                        self.newLayers),
            switchboard.requestCallback(("who changed", self.whoClassName),
                                        self.whoChangedCB)]


    def makeMenu(self, menu):
        self.menu = menu
        menu.addItem(oofmenu.OOFMenuItem(
                'Query',
                callback=self.queryObj,
                params=[
                    parameter.StringParameter(
                        'mode', tip="The type of object being queried."),
                    parameter.IntParameter(
                        'index', tip="The queried object's index.")],
                help="Query the object with the given index."))
        menu.addItem(oofmenu.OOFMenuItem(
                "Peek",
                callback=self.peekObj,
                params=[
                    parameter.StringParameter(
                        'mode', tip="The type of object being queried."),
                    parameter.IntParameter(
                        'index', tip="The queried object's index.")],
                help="Query the object with the given index."))
        menu.addItem(oofmenu.OOFMenuItem(
                'Prev',
                callback=self.prevQuery,
                help="Go to the previous query."))
        menu.addItem(oofmenu.OOFMenuItem(
                'Next',
                callback=self.nextQuery,
                help="Go to the next query."))
        menu.addItem(oofmenu.OOFMenuItem(
                'Clear',
                callback=self.clear,
                help='Clear the toolbox.'))
        
    def getMode(self, modename):
        return self.modeobjdict[modename]

    def queryObj(self, menuitem, mode, index):
        modeobj = self.modeobjdict[mode]
        self.peek = {}
        self.queries.push((modeobj, index))
        modeobj.sendQuerySignals(index)
        self.gfxwindow().draw()

    def peekObj(self, menuitem, mode, index):
        modeobj = self.modeobjdict[mode]
        self.peek[modeobj] = index
        modeobj.sendPeekSignals(index)
        self.gfxwindow().draw()

    def prevQuery(self, menuitem):
        mode, indx = self.queries.prev()
        self.peek = {}
        mode.sendQuerySignals(indx)
        self.gfxwindow().draw()

    def nextQuery(self, menuitem):
        mode, indx = self.queries.next()
        self.peek = {}
        mode.sendQuerySignals(indx)
        self.gfxwindow().draw()

    def clear(self, menuitem):
        self.clearQuery()
        switchboard.notify((self, "clear"))
        switchboard.notify((self.gfxwindow(), "query " + self.whoClassName))
        self.gfxwindow().draw()

    def clearQuery(self): 
        # clearQuery is called by the Clear menu item and also
        # directly by gui toolbox, so it should *not* invoke any gui
        # toolbox methods via the switchboard.
        self.queries.push((self.currentMode(), None))
        self.peek = {}

    def purgeQueries(self):
        # purgeQueries is like clearQuery, except that it completely
        # erases the history in the RingBuffer, instead of pushing an
        # empty selection.
        mode = self.currentMode()
        self.queries.clear()
        self.queries.push((mode, None))
        self.peek = {}

    def activate(self):
        self.context = self.gfxwindow().topwho(self.whoClassName)

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)

    def getContext(self):
        return self.context

    def newLayers(self):        # sb "layers changed" callback
        lastctxt = self.getContext()
        self.context = self.gfxwindow().topwho(self.whoClassName)
        if lastctxt is not self.context:
            self.purgeQueries()
            self.currentMode().sendQuerySignals(None)

    def whoChangedCB(self, who): # sb ("who changed", classname) callback
        ## TODO OPT: Instead of clearing all the info, use the
        ## SkeletonSelectable parent/child relations to select a
        ## parent or child if possible.
        self.purgeQueries()
        self.currentMode().sendQuerySignals(None)

    def currentQuery(self):
        return self.queries.current()

    def currentMode(self):
        try:
            return self.queries.current()[0]
        except IndexError:
            return None

    def allPeekModes(self):
        return self.peek.keys()

    def nQueries(self):
        return len(self.queries)

    def getQueryObject(self):
        # Return value is (mode, object)
        cq = self.currentQuery()
        if cq is None:
            return (None, None)
        mode, indx = cq
        if indx is not None:
            return (mode, mode.resolveQuery(self.context, indx))
        return (mode, None)

    def getPeekObject(self, mode):
        assert isinstance(mode, GenericInfoMode) # not GenericInfoModeGUI!
        try:
            indx = self.peek[mode]
        except KeyError:
            return None
        if indx is not None:
            return mode.resolveQuery(self.context, indx)
