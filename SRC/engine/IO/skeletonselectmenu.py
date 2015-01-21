# -*- python -*-
# $RCSfile: skeletonselectmenu.py,v $
# $Revision: 1.20.18.4 $
# $Author: langer $
# $Date: 2013/11/08 20:45:04 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# The menu for node-selection modification operations, automatically
# added via switchboard callback.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.engine import skeletonselectionmod
from ooflib.engine import skeletoncontext
from ooflib.common.microstructure import getMicrostructure
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
import types

nodeselectmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'NodeSelection',
    cli_only=1,
    help='Select nodes in a Skeleton.',
    discussion="""<para>
    The <command>NodeSelection</command> menu contains commands for
    selecting sets of &skel; &nodes; and for modifying the set of
    selected &nodes;.  In the GUI, these commands originate in the
    <link linkend='Section-Tasks-SkeletonSelection'>Skeleton Selection
    task page</link>.  None of the commands rely upon mouse input.
    Commands that take mouse input are found in the <xref
    linkend='MenuItem-OOF.Graphics_n.Toolbox.Select_Node'/> menu and
    originate in the <link
    linkend='Section-Graphics-SkeletonSelection'>Skeleton Selection
    toolbox</link>.
    </para>"""
    ))

segmentselectmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'SegmentSelection',
    cli_only=1,
    help='Select segments in a Skeleton.',
    discussion="""<para>
    The <command>SegmentSelection</command> menu contains commands for
    selecting sets of &skel; &sgmts; and for modifying the set of
    selected &sgmts;.  In the GUI, these commands originate in the
    <link linkend='Section-Tasks-SkeletonSelection'>Skeleton Selection
    task page</link>.  None of the commands rely upon mouse input.
    Commands that take mouse input are found in the <xref
    linkend='MenuItem-OOF.Graphics_n.Toolbox.Select_Segment'/> menu
    and originate in the <link
    linkend='Section-Graphics-SkeletonSelection'>Skeleton Selection
    toolbox</link>.
    </para>"""
))

if config.dimension() == 3:
    faceselectmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
        'FaceSelection',
        cli_only=1,
        help='Select faces in a Skeleton.',
        discussion="""<para>
        The <command>FaceSelection</command> menu contains commands for
        selecting sets of &skel; &faces; and for modifying the set of
        selected &faces;.  In the GUI, these commands originate in the
        <link linkend='Section-Tasks-SkeletonSelection'>Skeleton Selection
        task page</link>.  None of the commands rely upon mouse input.
        Commands that take mouse input are found in the <xref
        linkend='MenuItem-OOF.Graphics_n.Toolbox.Select_Face'/> menu
        and originate in the <link
        linkend='Section-Graphics-SkeletonSelection'>Skeleton Selection
        toolbox</link>.
        </para>"""
    ))

elementselectmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'ElementSelection',
    cli_only=1,
    help='Select elements in a Skeleton.',
    discussion="""<para>
    The <command>ElementSelection</command> menu contains commands for
    selecting sets of &skel; &elems; and for modifying the set of
    selected &elems;.  In the GUI, these commands originate in the
    <link linkend='Section-Tasks-SkeletonSelection'>Skeleton Selection
    task page</link>.  None of the commands rely upon mouse input.
    Commands that take mouse input are found in the <xref
    linkend='MenuItem-OOF.Graphics_n.Toolbox.Select_Element'/> menu
    and originate in the <link
    linkend='Section-Graphics-SkeletonSelection'>Skeleton Selection
    toolbox</link>.
    </para>"""
))

def _undo(menuitem, skeleton):
    skelc = skeletoncontext.skeletonContexts[skeleton]
    selection = getattr(skelc, menuitem.data)
    selection.begin_writing()
    try:
        selection.undo()
    finally:
        selection.end_writing()
    selection.signal()

def _redo(menuitem, skeleton):
    skelc = skeletoncontext.skeletonContexts[skeleton]
    selection = getattr(skelc, menuitem.data)
    selection.begin_writing()
    try:
        selection.redo()
    finally:
        selection.end_writing()
    selection.signal()

def _clear(menuitem, skeleton):
    skelc = skeletoncontext.skeletonContexts[skeleton]
    selection = getattr(skelc, menuitem.data)
    selection.begin_writing()
    try:
        selection.start() # Clear should be undoable.
        selection.clear()
    finally:
        selection.end_writing()
    selection.signal()

def _invert(menuitem, skeleton):
    skelc = skeletoncontext.skeletonContexts[skeleton]
    selection = getattr(skelc, menuitem.data)
    selection.begin_writing()
    try:
        selection.start() # Invert should be undoable.
        selection.invert()
    finally:
        selection.end_writing()
    selection.signal()



def makeMenu(menu, modifier, selection_name):
    menu.clearMenu()

    objname = selection_name[:-9] # 'node', 'segment', 'face', or 'element'

    undo_item = menu.addItem(oofmenu.OOFMenuItem(
        "Undo", callback=_undo,
        params = [
        whoville.WhoParameter("skeleton",
                              whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString)],
        help="Undo the latest Skeleton %s selection operation." % objname,
        discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/%s_undo.xml'
                                        % objname)
        ))
    undo_item.data = selection_name

    redo_item = menu.addItem(oofmenu.OOFMenuItem(
        "Redo", callback=_redo,
              params = [
        whoville.WhoParameter("skeleton",
                              whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString)],
        help="Redo the latest undone Skeleton %s selection operation."\
        % objname,
        discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/%s_redo.xml'
                                        % objname)
        ))
    redo_item.data = selection_name

    clear_item = menu.addItem(oofmenu.OOFMenuItem(
        "Clear", callback=_clear,
        params = [
        whoville.WhoParameter("skeleton",
                              whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString)],
        help="Clear the current Skeleton %s selection." % objname,
        discussion="<para>Unselect all %ss in the &skel;.</para>" % objname))
    clear_item.data = selection_name

    invert_item = menu.addItem(oofmenu.OOFMenuItem(
        "Invert",
        callback=_invert,
        params = [
        whoville.WhoParameter("skeleton",
                              whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString)],
        help="Invert the current Skeleton %s selection." % objname,
        discussion="""<para>
        Select the unselected %ss, and unselect the selected %ss in the &skel;.
        </para>""" % (objname, objname)))
    invert_item.data = selection_name    
        
    for r in modifier.registry:
        # For help
        try:
            help = r.tip
        except AttributeError:
            help = None
        # For discussion
        try:
            discussion = r.discussion
        except AttributeError:
            discussion = None
        menuitem = menu.addItem(
            oofmenu.OOFMenuItem(utils.space2underscore(r.name()),
                                callback = skeletonselectionmod.modify,
                                params = [
            whoville.WhoParameter("skeleton",
                                  whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString)] +
                                r.params,
                                help=help,
                                discussion=discussion))
        menuitem.data = r

# Callback for new registration entries added in later imports.
switchboard.requestCallback(skeletonselectionmod.NodeSelectionModifier,
                            makeMenu, nodeselectmenu,
                            skeletonselectionmod.NodeSelectionModifier,
                            "nodeselection")

switchboard.requestCallback(skeletonselectionmod.SegmentSelectionModifier,
                            makeMenu, segmentselectmenu,
                            skeletonselectionmod.SegmentSelectionModifier,
                            "segmentselection")

if config.dimension() == 3:
    switchboard.requestCallback(skeletonselectionmod.FaceSelectionModifier,
                                makeMenu, faceselectmenu,
                                skeletonselectionmod.FaceSelectionModifier,
                                "faceselection")

switchboard.requestCallback(skeletonselectionmod.ElementSelectionModifier,
                            makeMenu, elementselectmenu,
                            skeletonselectionmod.ElementSelectionModifier,
                            "elementselection")


# Insert menu items for the ones already in the registry at
# import-time.
makeMenu(nodeselectmenu, skeletonselectionmod.NodeSelectionModifier,
         "nodeselection")

makeMenu(segmentselectmenu,
         skeletonselectionmod.SegmentSelectionModifier,
         "segmentselection")

if config.dimension() == 3:
    makeMenu(faceselectmenu,
             skeletonselectionmod.FaceSelectionModifier,
             "faceselection")

makeMenu(elementselectmenu,
         skeletonselectionmod.ElementSelectionModifier,
         "elementselection")
