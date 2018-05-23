# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import pointparameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import pinnodesmodifier
from ooflib.engine import skeletoncontext
from ooflib.engine import skeletonselectable

def undo(menuitem, skeleton):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        skelcontext.pinnednodes.undo()
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()

def redo(menuitem, skeleton):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        skelcontext.pinnednodes.redo()
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()

def pin(menuitem, skeleton, node):
    # 'node' is a node position.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.clear()
        skelcontext.pinnednodes.pinPoint(node)
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()

def addpin(menuitem, skeleton, node):
    # 'node' is a node position.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.pinPoint(node)
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()
    
def unpin(menuitem, skeleton, node):
    # 'node' is a node position.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.unpinPoint(node)
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()

def toggle(menuitem, skeleton, node):
    # 'node' is a node position.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.togglepinPoint(node)
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()
    

def unpinall(menuitem, skeleton):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.clear()
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()

def invert(menuitem, skeleton):
    ## TODO 3.1: This is inefficient, and probably doesn't work correctly.
    ## Since a node can be pinned in one skeleton and unpinned in
    ## another (if a parent was at a different position than a child
    ## when the node was pinned), unpinning all the nodes and then
    ## pinning the ones that weren't pinned will invert the pinned
    ## state of the current skeleton, but might not correctly invert
    ## the state of its parents or children.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        newpinned = skelcontext.getObject().notPinnedNodes()
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.clear()
        skelcontext.pinnednodes.pinList(newpinned)
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()

def pinnodesmod(menuitem, skeleton, **params):
    registration = menuitem.data
    modifier = registration(**params)
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skelcontext.begin_writing()
    try:
        modifier(skelcontext)
    finally:
        skelcontext.end_writing()
    skelcontext.pinnednodes.signal()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

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

    skelparam = whoville.WhoParameter('skeleton',
                                      skeletoncontext.skeletonContexts,
                                      tip=parameter.emptyTipString)

    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'Pin',
        callback=pin,
        params=[skelparam,
                pointparameter.PointParameter('node')],
        help="Pin the node at the given point and unpin all others."))

    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'AddPin',
        callback=addpin,
        params=[skelparam,
                pointparameter.PointParameter('node')],
        help="Pin the node at the given point without unpinning all others."))

    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'UnPin',
        callback=unpin,
        params=[skelparam,
                pointparameter.PointParameter('node')],
        help="Unpin the node at the given point."))

    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'TogglePin',
        callback=toggle,
        params=[skelparam,
                pointparameter.PointParameter('node')],
        help="Pin the node at the given point if it's unpinned, and vice versa."
    ))

    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'Undo',
        callback=undo,
        params=[whoville.WhoParameter('skeleton',
                                      skeletoncontext.skeletonContexts,
                                      tip=parameter.emptyTipString)],
        help="Undo the pinning operation.",
        discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/pinnodes_undo.xml')
        ))
    
    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'Redo',
        callback=redo,
        params=[whoville.WhoParameter('skeleton',
                                      skeletoncontext.skeletonContexts,
                                      tip=parameter.emptyTipString)],
        help="Undo the undone pinning operation.",
        discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/pinnodes_redo.xml')
        ))
        
    pinnodesmenu.addItem(oofmenu.OOFMenuItem(
        'UnPinAll',
        callback=unpinall,
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
        callback=invert,
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
            callback=pinnodesmod,
            params=[whoville.WhoParameter('skeleton',
                                          skeletoncontext.skeletonContexts,
                                          tip=parameter.emptyTipString)]
            +registration.params,
            help=help,
            discussion=discussion))
        menuitem.data = registration

# Make menu when a new entry has been made to the registration.
# This probably never happens.
switchboard.requestCallback(pinnodesmodifier.PinNodesModifier,
                            makeMenu)

makeMenu()

######################

def _setPinnedNode_UndoBufferSize(menuitem, size):
    skeletonselectable.pinstacksize = size
    switchboard.notify('pinnednode ringbuffer resize', size+1)

mainmenu.OOF.Settings.UndoBuffer_Size.addItem(oofmenu.OOFMenuItem(
    'Pinned_Nodes',
    ordering=2,
    callback=_setPinnedNode_UndoBufferSize,
    params=[parameter.IntParameter(
                'size', skeletonselectable.pinstacksize,
                tip='number of previous pinned node configurations to retain')],
    help='Set the history buffer size for node pinning operations',
    discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/pinnodebufsize.xml')
    ))
