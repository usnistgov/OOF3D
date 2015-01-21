# -*- python -*-
# $RCSfile: pixelselectionmenu.py,v $
# $Revision: 1.14.18.1 $
# $Author: langer $
# $Date: 2011/10/18 15:46:51 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import microstructure
from ooflib.common import pixelselectionmod
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump

selmodmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'PixelSelection',
    help='Tools for selecting pixels.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/pixelselection.xml'),
    cli_only=1))

def buildSelectionModMenu():
    selmodmenu.clearMenu()
    selmodmenu.addItem(oofmenu.OOFMenuItem(
        'Undo',
        params=[whoville.WhoParameter('microstructure',
                                      microstructure.microStructures,
                                      tip=parameter.emptyTipString)],
        callback=pixelselectionmod.undo,
        help="Undo the latest selection.",
        discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/undo_pixsel.xml')
        ))
    
    selmodmenu.addItem(oofmenu.OOFMenuItem(
        'Redo',
        params=[whoville.WhoParameter('microstructure',
                                      microstructure.microStructures,
                                      tip=parameter.emptyTipString)],
        callback=pixelselectionmod.redo,
        help="Redo the latest undone selection.",
        discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/redo_pixsel.xml')
        ))

    selmodmenu.addItem(oofmenu.OOFMenuItem(
        'Clear',
        params=[whoville.WhoParameter('microstructure',
                                      microstructure.microStructures,
                                      tip=parameter.emptyTipString)],
        callback=pixelselectionmod.clear,
        help="Clear the current selection.",
        discussion="<para>Clear the current selection.</para>"))
    
    for registration in pixelselectionmod.SelectionModifier.registry:
        # Help string
        try:
            help = registration.tip
        except AttributeError:
            help = None
        # Discussion
        try:
            discussion = registration.discussion
        except AttributeError:
            discussion = None
        menuitem = selmodmenu.addItem(
            oofmenu.OOFMenuItem(utils.space2underscore(registration.name()),
                                callback=pixelselectionmod.doSelectionMod,
                                threadable=oofmenu.THREADABLE,
                                params=[
            whoville.WhoParameter('microstructure',
                                  microstructure.microStructures,
                                  tip=parameter.emptyTipString)
            ]+registration.params,
                                help=help,
                                discussion=discussion))
        menuitem.data = registration
    
# Rebuild the selection modification menu whenever a new
# SelectionModifier Registration is created.  Hopefully this won't be
# too often.

switchboard.requestCallback(pixelselectionmod.SelectionModifier,
                            buildSelectionModMenu)


buildSelectionModMenu()
