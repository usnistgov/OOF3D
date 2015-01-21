# -*- python -*-
# $RCSfile: pinnodes.py,v $
# $Revision: 1.36.18.5 $
# $Author: langer $
# $Date: 2013/06/06 19:37:20 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import view
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import toolbox
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletoncontext
from ooflib.engine import pinnodesmodifier

# Toolbox for pinning nodes.  Pinned nodes don't move during mesh
# modification operations.  They *can* move during equilibration --
# they're not boundary conditions.  Pinned nodes are treated much like
# Skeleton Selectables, and share a lot of code with them.

class PinnedNodesToolbox(toolbox.Toolbox):
    def __init__(self, gfxwindow):
        toolbox.Toolbox.__init__(self, 'Pin_Nodes', gfxwindow)
        self.skeleton_param = whoville.WhoParameter(
            'skeleton', whoville.getClass('Skeleton'),
            tip=parameter.emptyTipString)
                   
    def makeMenu(self, menu):
        self.menu = menu
        if config.dimension() == 2:
            pinparams = [self.skeleton_param,
                         primitives.PointParameter('point',
                                                   tip='Target point.')]
        else:                   # 3D
            pinparams = [self.skeleton_param,
                         primitives.PointParameter('point',
                                                   tip='Target point'),
                         view.ViewParameter('view')]


        menu.addItem(oofmenu.OOFMenuItem(
            'Pin',
            callback = self.pin,
            params=pinparams,
            help="Pin the node closest to the given point.",
            discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/pin.xml')
            ))
        menu.addItem(oofmenu.OOFMenuItem(
            'UnPin',
            callback = self.unpin,
            params=pinparams,
            help="Unpin the node closest to the given point.",
            discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/unpin.xml')
            ))
        menu.addItem(oofmenu.OOFMenuItem(
            'TogglePin',
            callback=self.togglepin,
            params=pinparams,
            help="Toggle the pinnedness of the node closest to the given point.",
            discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/toggle_pin.xml')
            ))
        menu.addItem(oofmenu.OOFMenuItem(
            'UnPinAll',
            callback = pinnodesmodifier.unpinall,
            params=[self.skeleton_param],
            help="Unpin all nodes.",
            discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/unpin_all.xml')
            ))
        menu.addItem(oofmenu.OOFMenuItem(
            'Invert',
            callback = pinnodesmodifier.invert,
            params=[self.skeleton_param],
            help="Invert pinned nodes.",
            discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/invert_pin.xml')
            ))

        menu.addItem(oofmenu.OOFMenuItem(
            'Undo',
            callback=pinnodesmodifier.undo,
            params=[self.skeleton_param],
            help="Undo the latest pin.",
            discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/undo_pin.xml')
            ))
        menu.addItem(oofmenu.OOFMenuItem(
            'Redo',
            callback=pinnodesmodifier.redo,
            params=[self.skeleton_param],
            help="Redo the latest undone pin.",
            discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/redo_pin.xml')
            ))

    if config.dimension() == 2:
        def pin(self, menuitem, skeleton, point):
            skelcontext = skeletoncontext.skeletonContexts[skeleton]
            skelcontext.pinnednodes.start()
            skelcontext.pinnednodes.pinPoint(point)
            skelcontext.pinnednodes.signal()

        def unpin(self, menuitem, skeleton, point):
            skelcontext = skeletoncontext.skeletonContexts[skeleton]
            skelcontext.pinnednodes.start()
            skelcontext.pinnednodes.unpinPoint(point)
            skelcontext.pinnednodes.signal()

        def togglepin(self, menuitem, skeleton, point):
            skelcontext = skeletoncontext.skeletonContexts[skeleton]
            skelcontext.pinnednodes.start()
            skelcontext.pinnednodes.togglepinPoint(point)
            skelcontext.pinnednodes.signal()
    else:                       # 3D
        def pin(self, menuitem, skeleton, point, view):
            skelcontext = skeletoncontext.skeletonContexts[skeleton]
            if not skelcontext:
                return
            pt = self.gfxwindow().findClickedPoint(skelcontext, point, view)
            if pt is not None:
                skelcontext.pinnednodes.start()
                skelcontext.pinnednodes.pinPoint(pt)
                skelcontext.pinnednodes.signal()

        def unpin(self, menuitem, skeleton, point, view):
            skelcontext = skeletoncontext.skeletonContexts[skeleton]
            if not skelcontext:
                return
            pt = self.gfxwindow().findClickedPoint(skelcontext, point, view)
            if pt is not None:
                skelcontext.pinnednodes.start()
                skelcontext.pinnednodes.unpinPoint(pt)
                skelcontext.pinnednodes.signal()

        def togglepin(self, menuitem, skeleton, point, view):
            skelcontext = skeletoncontext.skeletonContexts[skeleton]
            if not skelcontext:
                return
            pt = self.gfxwindow().findClickedPoint(skelcontext, point, view)
            if pt is not None:
                skelcontext.pinnednodes.start()
                skelcontext.pinnednodes.togglepinPoint(pt)
                skelcontext.pinnednodes.signal()

    tip="Pin nodes."

    discussion="""<para>
    Pinned nodes are immobile during &skel; modifications.  This menu
    contains tools for pinning and unpinning nodes with mouse input.
    </para>"""

toolbox.registerToolboxClass(PinnedNodesToolbox, ordering=2.7)
