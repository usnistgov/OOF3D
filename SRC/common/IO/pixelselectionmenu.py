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
from ooflib.common import pixelselectionmethod
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump

 # 'microstructure' is a param name
from ooflib.common import microstructure as msmodule

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

selectmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'VoxelSelection',
    help='Tools for selecting pixels.',
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/pixelselection.xml'),
    cli_only=1))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

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
        parameter.RegisteredParameter(
            'method',
            pixelselectionmethod.VoxelSelectionMethod,
            tip="How the pixels will be selected.")
        ],
    callback=select,
    help="Select some voxels."
))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def clear(menuitem, microstructure):
    ms = msmodule.microStructures[microstructure]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        selection.start()
        selection.clear()
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')

selectmenu.addItem(oofmenu.OOFMenuItem(
    'Clear',
    params=[whoville.WhoParameter('microstructure',
                                  msmodule.microStructures,
                                  tip=parameter.emptyTipString)],
    callback=clear,
    help="Clear the current selection.",
    discussion="<para>Clear the current selection.</para>"))

    
def undo(menuitem, microstructure):
    ms = msmodule.microStructures[microstructure]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        selection.undo()
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')

selectmenu.addItem(oofmenu.OOFMenuItem(
    'Undo',
    params=[whoville.WhoParameter('microstructure',
                                  msmodule.microStructures,
                                  tip=parameter.emptyTipString)],
    callback=undo,
    help="Undo the latest selection.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/undo_pixsel.xml')
))


def redo(menuitem, microstructure):
    ms = msmodule.microStructures[microstructure]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        selection.redo()
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')

selectmenu.addItem(oofmenu.OOFMenuItem(
    'Redo',
    params=[whoville.WhoParameter('microstructure',
                                  msmodule.microStructures,
                                  tip=parameter.emptyTipString)],
    callback=redo,
    help="Redo the latest undone selection.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/redo_pixsel.xml')
))

    
def invert(menuitem, microstructure):
    ms = msmodule.microStructures[microstructure]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        selection.start()
        selection.invert()
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')

selectmenu.addItem(oofmenu.OOFMenuItem(
    'Invert',
    params=[whoville.WhoParameter('microstructure',
                                  msmodule.microStructures,
                                  tip=parameter.emptyTipString)],
    callback=invert,
    help="Invert the current selection.",
    discussion="<para>Invert the current selection.</para>"))


# def buildSelectionModMenu():
#     selectmenu.clearMenu()
#     selectmenu.addItem(oofmenu.OOFMenuItem(
#         'Undo',
#         params=[whoville.WhoParameter('microstructure',
#                                       microstructure.microStructures,
#                                       tip=parameter.emptyTipString)],
#         callback=pixelselectionmod.undo,
#         help="Undo the latest selection.",
#         discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/undo_pixsel.xml')
#         ))
    
#     selectmenu.addItem(oofmenu.OOFMenuItem(
#         'Redo',
#         params=[whoville.WhoParameter('microstructure',
#                                       microstructure.microStructures,
#                                       tip=parameter.emptyTipString)],
#         callback=pixelselectionmod.redo,
#         help="Redo the latest undone selection.",
#         discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/redo_pixsel.xml')
#         ))

#     selectmenu.addItem(oofmenu.OOFMenuItem(
#         'Clear',
#         params=[whoville.WhoParameter('microstructure',
#                                       microstructure.microStructures,
#                                       tip=parameter.emptyTipString)],
#         callback=pixelselectionmod.clear,
#         help="Clear the current selection.",
#         discussion="<para>Clear the current selection.</para>"))
    
#     for registration in pixelselectionmod.SelectionModifier.registry:
#         # Help string
#         try:
#             help = registration.tip
#         except AttributeError:
#             help = None
#         # Discussion
#         try:
#             discussion = registration.discussion
#         except AttributeError:
#             discussion = None
#         menuitem = selectmenu.addItem(
#             oofmenu.OOFMenuItem(utils.space2underscore(registration.name()),
#                                 callback=pixelselectionmod.doSelectionMod,
#                                 threadable=oofmenu.THREADABLE,
#                                 params=[
#             whoville.WhoParameter('microstructure',
#                                   microstructure.microStructures,
#                                   tip=parameter.emptyTipString)
#             ]+registration.params,
#                                 help=help,
#                                 discussion=discussion))
#         menuitem.data = registration
    
# # Rebuild the selection modification menu whenever a new
# # SelectionModifier Registration is created.  Hopefully this won't be
# # too often.

# switchboard.requestCallback(pixelselectionmod.SelectionModifier,
#                             buildSelectionModMenu)


# buildSelectionModMenu()
