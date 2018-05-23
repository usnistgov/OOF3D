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

# Menu item for simple voxel selection operations.  The callback does
# *not* call PixelSelectionContext.start(), because then the Undo and
# Redo commands couldn't use the callbacks.  The "select" methods in
# the VoxelSelectionMethod and VoxelSelectionModifier subclasses have
# to call selection.start().

class SimpleVoxelSelectionCB(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, menuitem, microstructure):
        ms = ooflib.common.microstructure.microStructures[microstructure]
        selection = ms.getSelectionContext()
        selection.reserve()
        selection.begin_writing()
        try:
            self.func(selection)
        finally:
            selection.end_writing()
            selection.cancel_reservation()
        switchboard.notify('pixel selection changed', selection)
        switchboard.notify('redraw')

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

for i, func in enumerate((undo, redo, invert, clear)):
    selectmenu.addItem(oofmenu.OOFMenuItem(
        func.__name__.capitalize(),
        params=[whoville.AnyWhoParameter('microstructure',
                                         tip=parameter.emptyTipString)],
        callback=SimpleVoxelSelectionCB(func),
        ordering=0.1*i))

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
    # "pixel selection changed" tells UI components that reflect the
    # pixel selection status to update themselves.
    switchboard.notify('pixel selection changed', selection)
    # The notify method for some selection methods sends a switchboard
    # message indicating that the method has been used, so that it can
    # be recorded in the voxel selection page's historian, for example.
    method.notify()
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

