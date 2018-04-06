# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# See NOTES/selection_machinery.txt

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import pixelselection
from ooflib.common import selectionoperators
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
import ooflib.common.microstructure # 'microstructure' is a param name

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

selectmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'VoxelSelection',
    help='Tools for selecting pixels.',
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/pixelselection.xml'),
    cli_only=1))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Generic selection menu callbacks.


# Menu item for simple voxel selection operations.  The callback does
# *not* call PixelSelectionContext.start(), because then the Undo and
# Redo commands couldn't use the callbacks.  The "select" methods in
# the VoxelSelectionMethod and VoxelSelectionModifier subclasses have
# to call selection.start().


def simpleSelectionCB(menuitem, microstructure):
    ms = ooflib.common.microstructure.microStructures[microstructure]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        # SimpleVoxelSelectionModRegistration sets menuitem.data to a
        # VoxelSelectionModifier subclass, which has a static select()
        # method.
        menuitem.data.select(selection)
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')


# Menu item for complex voxel selection operations.  This one *does*
# call PixelSelectionContext.start(), so the subclasses should not
# call it.

def select(menuitem, source, method):
    # source is the name of a Microstructure or Image.  Get the object.
    whopath = labeltree.makePath(source)
    if len(whopath) == 1:
        ms = whoville.getClass('Microstructure')[whopath]
        source = ms
    else:
        assert len(whopath) == 2
        ms = whoville.getClass('Microstructure')[whopath[0:1]]
        source = whoville.getClass('Image')[whopath]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        selection.start()
        method.select(source, selection)
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')
    

selectmenu.addItem(oofmenu.OOFMenuItem(
    'Select',
    params=[
        whoville.AnyWhoParameter('source', tip="A Microstructure or Image."),
        parameter.MultiRegisteredParameter(
            'method',
            (pixelselection.VoxelSelectionMethod,
             pixelselection.VoxelSelectionModifier),
            tip="How the pixels will be selected.")
        ],
    callback=select,
    help="Select some voxels."
))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Many (but not all) selection methods will have a
# PixelSelectionOperator argument that indicates how the new selection
# combines with the previous selection.  That argument will appear in
# the toolbox GUI for the selection method.  In many cases, however,
# its value should be set by modifier keys (shift, ctrl, etc) and not
# by the toolbox widget for the parameter.  To make it less confusing
# (we hope) for the user, the parameter widget can be made passive, so
# it reflects the state of the modifier keys but does not affect them.
# This parameter object can be used in all such cases:
passiveOperatorParam = parameter.RegisteredParameter(
    'operator',
    selectionoperators.PixelSelectionOperator,
    tip=
    """\
How the new selection modifies the existing selection.
Use control and shift keys while clicking on the canvas
to change the value of this parameter.""",
    value=selectionoperators.Select())
passiveOperatorParam.set_data('passive widget', True)

# Selection methods that require more than a single click will want to
# get their selection operator directly from the toolbox instead of
# from a mouse click, and should use this parameter, which is settable
# by the user:
operatorParam = parameter.RegisteredParameter(
    'operator',
    selectionoperators.PixelSelectionOperator,
    tip='How the new selection modifies the existing selection.',
    value=selectionoperators.Select())
