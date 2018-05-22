# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletoncontext
from ooflib.engine import skeletonselmodebase
from ooflib.engine import skeletonselectionmodes
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

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Generic selection modifiers that work on Elements, Faces, Segments,
# and Nodes.  These don't appear in the RegisteredClassFactories in
# the skeleton selection page or toolbox.  They have buttons instead.

## TODO: The voxel versions of these routine, in
## pixelselectionmenu.py, call selection.reserve() and
## selection.cancel_reservation().  Why don't these routines?  Is it
## required or not?

def undo(selection):
    selection.undo()

def redo(selection):
    selection.redo()

def invert(selection):
    selection.start()
    selection.invert()

def clear(selection):
    selection.start()
    selection.clear()

class SimpleSelectionCB(object):
    def __init__(self, mode, func):
        self.mode = mode        # SkeletonSelectionMode instance
        self.func = func        # one of the four functions defined above
    def __call__(self, menuitem, skeleton):
        skelctxt = skeletoncontext.skeletonContexts[skeleton]
        selection = self.mode.getSelectionContext(skelctxt)
        selection.begin_writing()
        try:
            self.func(selection)
        finally:
            selection.end_writing()
        selection.signal()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# select is the menu callback for all selection operations that are
# defined by a XXXXSelectionModifier or XXXXSelectionMethod.

def select(menuitem, skeleton, method):
    skelc = skeletoncontext.skeletonContexts[skeleton]
    # menuitem.data is set to the SkeletonSelectionMode when the menu
    # is constructed.
    selection = menuitem.data.getSelectionContext(skelc)
    # selection.reserve()
    selection.begin_writing()
    try:
        selection.start()
        try:
            method.select(skelc, selection)
        except:
            selection.unstart()
            raise
    finally:
        selection.end_writing()
        # selection.cancel_reservation()
    selection.signal() # sends switchboard "node selection changed", eg.
    method.notify(menuitem.data)   
    
def makeMenu_(mode):
    # methodclass is the registered class for the selection methods,
    # NodeSelectionMethod, FaceSelectionMethod, etc, that are invoked via
    # the Skeleton Selection graphics toolbox and mouse interaction.
    # modifierclass is the registered class for the selection
    # modifiers, NodeSelectionModifier, FaceSelectionModifier, etc,
    # that are called from the Skeleton Selection page and don't
    # involve the mouse.
    menu = mode.getSelectionMenu()
    menu.clearMenu()

    whoparam = whoville.WhoParameter('skeleton',
                                     whoville.getClass('Skeleton'),
                                     tip=parameter.emptyTipString)

    for i, func in enumerate((undo, redo, invert, clear)):
        menu.addItem(oofmenu.OOFMenuItem(
            func.__name__.capitalize(),
            params=[whoparam],
            ordering=0.1*i,
            callback=SimpleSelectionCB(mode, func)))

    select_item = menu.addItem(oofmenu.OOFMenuItem(
        "Select",
        callback=select,
        params = [
            whoparam,
            parameter.MultiRegisteredParameter(
                'method',
                (mode.methodclass, mode.modifierclass),
                tip="How the %ss will be selected." % mode.name)
            ],
        help="Select some %ss." % mode.name))
    select_item.data = mode

skeletonselectionmodes.initialize()

for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
    makeMenu_(mode)
    
