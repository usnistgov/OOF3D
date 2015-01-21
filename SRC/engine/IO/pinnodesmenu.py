# -*- python -*-
# $RCSfile: pinnodesmenu.py,v $
# $Revision: 1.12.18.4 $
# $Author: langer $
# $Date: 2013/11/08 20:45:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletoncontext
from ooflib.engine import skeletonnode
from ooflib.engine import pinnodesmodifier


skelmenu = mainmenu.OOF.Skeleton
pinnodesmenu = skelmenu.addItem(oofmenu.OOFMenuItem(
    'PinNodes',
    cli_only=1,
    help='Pin and unpin nodes in a Skeleton.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/pinnodes.xml'))
    )

# Make menu
def makeMenu():
    pinnodesmenu.clearMenu()

    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'Undo',
        callback=pinnodesmodifier.undo,
        params=[whoville.WhoParameter('skeleton',
                                      skeletoncontext.skeletonContexts,
                                      tip=parameter.emptyTipString)],
        help="Undo the pinning operation.",
        discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/pinnodes_undo.xml')
        ))
    
    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'Redo',
        callback=pinnodesmodifier.redo,
        params=[whoville.WhoParameter('skeleton',
                                      skeletoncontext.skeletonContexts,
                                      tip=parameter.emptyTipString)],
        help="Undo the undone pinning operation.",
        discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/pinnodes_redo.xml')
        ))
        
    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'UnPinAll',
        callback=pinnodesmodifier.unpinall,
        params=[whoville.WhoParameter('skeleton',
                                      skeletoncontext.skeletonContexts,
                                      tip=parameter.emptyTipString)],
        help="Unpin all nodes of the Skeleton.",
        discussion="""<para>
        Unpin all of the <link
        linkend='MenuItem-OOF.Skeleton.PinNodes'>pinned</link> &nodes;
        in the given &skel;.
        </para>"""
        ))
    
    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'Invert',
        callback=pinnodesmodifier.invert,
        params=[whoville.WhoParameter('skeleton',
                                      skeletoncontext.skeletonContexts,
                                      tip=parameter.emptyTipString)],
        help="Pin the unpinned and unpin the pinned.",
        discussion="""<para>
        Invert the status of <link
        linkend='MenuItem-OOF.Skeleton.PinNodes'>pinned</link> &nodes;
        in the given &skel;. Pinned &nodes; will be released and free
        nodes will be pinned.
        </para>"""))

    for registration in pinnodesmodifier.PinNodesModifier.registry:
        try:
            help = registration.tip
        except AttributeError:
            help = None
        try:
            discussion = registration.discussion
        except AttributeError:
            discussion = None
        menuitem = pinnodesmenu.addItem(
            oofmenu.OOFMenuItem(
            utils.space2underscore(registration.name()),
            callback=pinnodesmodifier.pinnodesmod,
            params=[whoville.WhoParameter('skeleton',
                                          skeletoncontext.skeletonContexts,
                                          tip=parameter.emptyTipString)]
            +registration.params,
            help=help,
            discussion=discussion))
        menuitem.data = registration

# Make menu when a new entry has been made to the registration.
switchboard.requestCallback(pinnodesmodifier.PinNodesModifier,
                            makeMenu)

makeMenu()

######################

def _setPinnedNode_UndoBufferSize(menuitem, size):
    skeletonnode.stacksize = size
    switchboard.notify('pinnednode ringbuffer resize', size+1)

mainmenu.OOF.Settings.UndoBuffer_Size.addItem(oofmenu.OOFMenuItem(
    'Pinned_Nodes',
    ordering=2,
    callback=_setPinnedNode_UndoBufferSize,
    params=[parameter.IntParameter(
                'size', skeletonnode.stacksize,
                tip='number of previous pinned node configurations to retain')],
    help='Set the history buffer size for node pinning operations',
    discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/pinnodebufsize.xml')
    ))
