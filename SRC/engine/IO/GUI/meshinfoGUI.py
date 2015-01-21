# -*- python -*-
# $RCSfile: meshinfoGUI.py,v $
# $Revision: 1.111.2.27 $
# $Author: langer $
# $Date: 2014/11/05 16:54:53 $

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
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import ooferror2
from ooflib.SWIG.engine import planarity
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import utils
from ooflib.common.IO.GUI import gtklogger
from ooflib.engine import subproblemcontext
from ooflib.engine.IO import meshinfo
from ooflib.engine.IO.GUI import meshdataGUI
from ooflib.engine.IO.GUI import genericinfoGUI

import gtk

## TODO: Add SegmentMode (and FaceMode, in 3D) to display interface
## materials.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# _modes stores the MeshInfoMode subclasses for each info mode.  The
# keys are the mode names: "Element", "Node", etc.  It's an OrderedDict
# to ensure that the initially selected mode is always the same.

_modes = utils.OrderedDict()

class MeshInfoModeMetaClass(type):
    def __init__(cls, name, bases, dct):
        super(MeshInfoModeMetaClass, cls).__init__(name, bases, dct)
        try:
            targetName = dct['targetName']
        except KeyError:
            pass
        else:
            _modes[targetName] = cls
            

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Subclasses of MeshInfoModeGUI are in charge of displaying
# information in the toolbox and handling mouse clicks (peeks) on
# their lists.

## TODO: It would be nice if the MeshInfoModeGUI subclasses were also
## derived from the corresponding MeshInfoMode subclasses.  This is
## currently impossible, because the Mode classes need to know their
## Toolbox when initialized, and the ModeGUI classes need to know
## their GfxToolbox, but the Toolbox is constructed before the
## GfxToolbox.

class MeshInfoModeGUI(genericinfoGUI.GenericInfoModeGUI):
    # Base class for ElementModeGUI, NodeModeGUI.
    __metaclass__ = MeshInfoModeMetaClass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
    
class ElementModeGUI(MeshInfoModeGUI):
    targetName = "Element"
    def __init__(self, gfxtoolbox):
        MeshInfoModeGUI.__init__(self, gfxtoolbox)

        self.labelmaster((0,1), (0,1), 'index=')
        self.index = self.entrymaster((1,2), (0,1))
        gtklogger.setWidgetName(self.index, 'index')

        self.labelmaster((0,1), (1,2), 'type=')
        self.type = self.entrymaster((1,2), (1,2))
        gtklogger.setWidgetName(self.type, 'type')

        self.labelmaster((0,1), (2,3), 'nodes=')
        self.nodes = self.makeObjList("Node", (1,2), (2,3))

        self.labelmaster((0,1), (3,4), 'material=')
        self.material = self.entrymaster((1,2), (3,4))
        gtklogger.setWidgetName(self.material, 'material')

    def findObjectIndex(self, position, view):
        meshctxt = self.gfxtoolbox.getMeshContext()
        if meshctxt is not None:
            cellID, clickpos = self.gfxtoolbox.gfxwindow().findClickedCellID(
                meshctxt, position, view)
            return cellID

    def update(self, indx):
        debug.subthreadTest()
        if indx is not None:
            meshctxt = self.gfxtoolbox.getMeshContext()
            meshctxt.begin_reading()
            try:
                element = meshctxt.getObject().getElement(indx)
                # element probably can't be None, but it doesn't hurt
                # to check.
                if element is not None:
                    self.updateNodeList(element.nodes())
                    mat = element.material()
                    if mat:
                        matname = mat.name()
                    else:
                        matname = "<No material>"
                    mainthread.runBlock(self.update_thread,
                                        (element.masterelement().name(),
                                         `element.uiIdentifier()`,
                                         matname))
                    return
            finally:
                meshctxt.end_reading()
        # Nothing to display
        mainthread.runBlock(self.update_thread, ("", "", ""))
        self.updateNodeList([])

    def update_thread(self, etype, indx, matname):
        debug.mainthreadTest()
        self.type.set_text(etype)
        self.index.set_text(indx)
        self.material.set_text(matname)

    def updateNodeList(self, nodes):
        namelist = ["%s %d at %s"
                    % (node.classname(),
                       node.uiIdentifier(),
                       genericinfoGUI.posString(node.position()))
                    for node in nodes]
        mainthread.runBlock(self.nodes.update, (nodes, namelist))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class NodeModeGUI(MeshInfoModeGUI):
    targetName = "Node"
    fieldspacing = 6 # spacing between Fields in the table
    def __init__(self, gfxtoolbox):
        MeshInfoModeGUI.__init__(self, gfxtoolbox)

        self.labelmaster((0,1), (0,1), 'index=')
        self.index = self.entrymaster((1,3), (0,1))
        gtklogger.setWidgetName(self.index, 'index')

        self.labelmaster((0,1), (1,2), 'type=')
        self.type = self.entrymaster((1,3), (1,2))
        gtklogger.setWidgetName(self.type, 'type')

        self.labelmaster((0,1), (2,3), 'position=')
        self.pos = self.entrymaster((1,3), (2,3))
        gtklogger.setWidgetName(self.pos, 'position')

        self.baserows = self.table.get_property("n-rows")
        self.table.set_col_spacing(1, 4)
        self.fieldslisted = []
        # fieldvalEntries is a dict of the gtk.Entrys for displaying
        # the values of the DoFs at a Node.  The keys are (Field,
        # component) tuples.
        self.fieldvalEntries = {}
        # fieldvalWidgets contains the labels and separators in the
        # part of the gtk.Table used to display the DoF values. This
        # part of the table is dynamic, so we need to keep track of
        # these extra widgets so that they can be destroyed when the
        # table is rebuilt.
        self.fieldvalWidgets = set()

    def findObjectIndex(self, position, view):
        meshctxt = self.gfxtoolbox.getMeshContext()
        if meshctxt is not None:
            pt = self.gfxtoolbox.gfxwindow().findClickedPoint(
                meshctxt, position, view)
            factor = self.gfxtoolbox.toolbox.meshlayer.where.factor()
            if pt is not None:
                node = meshctxt.getObject().closestNode(pt, factor)
                if node:
                    return node.index()
    
    def update(self, indx):
        debug.subthreadTest()
        if indx is not None:
            meshctxt = self.gfxtoolbox.getMeshContext()
            meshctxt.begin_reading()
            try:
                femesh = meshctxt.getObject()
                node = femesh.getNode(indx)
                # node probably can't be None, but it doesn't hurt to
                # check.
                if node is not None:
                    # Find out which fields are defined at the node
                    fieldnames = node.fieldNames() # compound field names
                    nfieldrows = 0
                    listedfields = []
                    for fieldname in fieldnames:
                        fld = field.getField(fieldname)
                        nfieldrows += fld.ndof()
                        listedfields.append(fld)
                        if config.dimension() == 2:
                            zfld = fld.out_of_plane()
                            if node.hasField(zfld):
                                listedfields.append(zfld)
                                nfieldrows += zfld.ndof()
                        tfld = fld.time_derivative()
                        if node.hasField(tfld):
                            listedfields.append(tfld)
                            nfieldrows += tfld.ndof()
                    # Rebuild the table of field values, but only if the
                    # fields have changed.
                    if self.fieldslisted != listedfields:
                        mainthread.runBlock(self.rebuildFieldTable,
                                            (nfieldrows, listedfields,))

                    # Get the field values for the table.
                    fieldvals = []
                    # The structure of this loop must match the loop
                    # in update_thread, below.
                    for fld in self.fieldslisted:
                        fcomp = fld.iterator(planarity.ALL_INDICES)
                        while not fcomp.end():
                            fieldvals.append(
                                fld.value(femesh, node, fcomp.integer()))
                            fcomp.next()
                    # end loop over field values
                    mainthread.runBlock(
                        self.update_thread,
                        (`node.index()`,
                         node.classname(),
                         genericinfoGUI.posString(node.position()),
                         fieldvals
                         ))
                    return
                # end if node is not None
            finally:
                meshctxt.end_reading()
        # end if indx is not None
        
        # No node
        mainthread.runBlock(self.update_thread, ("", "", "", []))

    def rebuildFieldTable(self, nfieldrows, listedfields):
        for entry in self.fieldvalEntries.values():
            entry.destroy()
        for widget in self.fieldvalWidgets:
            widget.destroy()
        self.fieldvalEntries.clear()
        self.fieldvalWidgets.clear()
        self.table.resize(rows=self.baserows+nfieldrows, columns=3)
        frow = self.baserows # starting row for a field
        for fld in listedfields:
            sep = gtk.HSeparator()
            self.fieldvalWidgets.add(sep)
            self.table.attach(sep, 0,3, frow,frow+1, 
                              xoptions=gtk.FILL)
            frow += 1
            label = gtk.Label(fld.name())
            label.set_alignment(1.0, 0.5)
            self.fieldvalWidgets.add(label)
            self.table.attach(label,
                              0,1, frow, frow+fld.ndof(),
                              xoptions=0)
            fcomp = fld.iterator(planarity.ALL_INDICES)
            while not fcomp.end():
                row = frow + fcomp.integer()
                label = gtk.Label(" " + fcomp.shortrepr() + "=")
                self.fieldvalWidgets.add(label)
                self.table.attach(label, 1,2, row,row+1,
                                  xoptions=gtk.FILL)
                e = gtk.Entry()
                e.set_size_request(10*guitop.top().charsize, -1)
                e.set_editable(False)
                self.fieldvalEntries[(fld, fcomp.integer())] = e
                self.table.attach(e, 2,3, row,row+1,
                                  xoptions=gtk.EXPAND|gtk.FILL)
                fcomp.next()
            frow += fld.ndof()
        # end loop over listedfields
        self.table.show_all()
        self.fieldslisted = listedfields
        

    def update_thread(self, indx, nodetype, pos, fieldvals):
        debug.mainthreadTest()
        self.index.set_text(indx)
        self.type.set_text(nodetype),
        self.pos.set_text(pos)
        if fieldvals:
            vals = iter(fieldvals)
            # The structure of this loop must match the loop in update(),
            # above.
            for fld in self.fieldslisted:
                fcomp = fld.iterator(planarity.ALL_INDICES)
                while not fcomp.end():
                    e = self.fieldvalEntries[(fld, fcomp.integer())]
                    e.set_text("%-13.6g" % vals.next())
                    fcomp.next()
        else:
            # Clear the Field widgets.  This is done here, rather than
            # in rebuildFieldTable(), because it has to be done both
            # if there are no Fields and if there is no Node.
            for entry in self.fieldvalEntries.values():
                entry.destroy()
            for widget in self.fieldvalWidgets:
                widget.destroy()
            self.fieldslisted = []
            self.fieldvalWidgets.clear()
            self.fieldvalEntries.clear()
            #self.table.resize(rows=0, columns=0)

    def peek(self, modename):
        pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=

class MeshInfoToolboxGUI(genericinfoGUI.GenericInfoToolboxGUI):

    def __init__(self, meshinfotb):
        genericinfoGUI.GenericInfoToolboxGUI.__init__(self, "Mesh Info",
                                                      meshinfotb)

        self.sbcallbacks.extend([
                switchboard.requestCallback("mesh changed", self.meshChanged),
                switchboard.requestCallback("mesh data changed",
                                            self.meshDataChanged),
                switchboard.requestCallback("subproblem changed",
                                            self.subproblemChanged),
                switchboard.requestCallback("field defined",
                                            self.fieldDefsChanged)
            ])

    ## TODO MER: Use the addExtraWidgets hook to insert a button that
    ## brings up a data viewer window.  Here's the code from the old
    ## MeshInfoToolboxGUI.__init__ that did that:
    # if config.dimension() == 2:
    #     align = gtk.Alignment(xalign=0.5)
    #     self.mainbox.pack_start(align, expand=0, fill=0, padding=2)
    #     centerbox = gtk.HBox()
    #     align.add(centerbox)
    #     self.meshdatabutton = gtkutils.StockButton(gtk.STOCK_DIALOG_INFO,
    #                                                'New Data Viewer...')
    #     gtklogger.setWidgetName(self.meshdatabutton, "NewDataViewer")
    #     centerbox.pack_start(self.meshdatabutton, expand=0, fill=0)
    #     gtklogger.connect(self.meshdatabutton, 'clicked', self.meshdataCB)
    #     tooltips.set_tooltip_text(
    #         self.meshdatabutton,
    #         "Open a window to display fields, fluxes, and other"
    #         " quantities evaluated at the mouse click location.")

    def modeClassDict(self):
        # Returns an ordered dictionary containing modename:modeClass,
        # used by GenericInfoToolboxGUI.__init__
        return _modes

    def packModeButtons(self, hbox, buttons):
        for button in buttons:
            hbox.pack_start(button, expand=0, fill=0)
        
    def getMeshContext(self):
        return self.toolbox.context

    def meshChanged(self, meshcontext): # sb "mesh changed"
        if self.getMeshContext() is meshcontext:
            self.update()
    def meshDataChanged(self, meshcontext): # sb "mesh data changed"
        if self.getMeshContext() is meshcontext:
            self.update()
    def subproblemChanged(self, subpcontext): # sb "subproblem changed"
        self.meshChanged(subpcontext.getParent())

    def fieldDefsChanged(self, subprobname, fieldname, defined):
        # sb "field defined"
        subprob = subproblemcontext.subproblems[subprobname]
        meshctxt = subprob.getParent()
        if self.getMeshContext() is meshctxt:
            self.update()

    def meshdataCB(self, button):
        meshdataGUI.openMeshData(self.gfxwindow(), self.toolbox.currentPoint())
                              

def _makeGUI(self):
    return MeshInfoToolboxGUI(self)

meshinfo.MeshInfoToolbox.makeGUI = _makeGUI
