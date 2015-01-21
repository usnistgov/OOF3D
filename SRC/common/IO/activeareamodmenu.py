# -*- python -*-
# $RCSfile: activeareamodmenu.py,v $
# $Revision: 1.31.18.5 $
# $Author: langer $
# $Date: 2014/09/27 22:33:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import switchboard
from ooflib.common import activeareamod
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
import ooflib.common.microstructure


def _undo(menuitem, microstructure):
    ms = ooflib.common.microstructure.getMicrostructure(microstructure)
    activearea = ms.activearea
    activearea.begin_writing()
    activearea.undo()
    activearea.end_writing()
    switchboard.notify("active area modified", None)
    switchboard.notify("redraw")
    
def _redo(menuitem, microstructure):
    ms = ooflib.common.microstructure.getMicrostructure(microstructure)
    activearea = ms.activearea
    activearea.begin_writing()
    activearea.redo()
    activearea.end_writing()
    switchboard.notify("active area modified", None)
    switchboard.notify("redraw")
                                                    
def _override(menuitem, microstructure, override):
    ms = ooflib.common.microstructure.getMicrostructure(microstructure)
    ms.activearea.override(override)
    switchboard.notify("active area modified", None)
    switchboard.notify("redraw")

def activeAreaNameResolver(param, startname):
    if param.automatic():
        basename = 'activearea'
    else:
        basename = startname
    msname = param.group['microstructure'].value
    ms = ooflib.common.microstructure.getMicrostructure(msname)
    return utils.uniqueName(basename, ms.activeAreaNames())

def _store(menuitem, microstructure, name):
    ms = ooflib.common.microstructure.getMicrostructure(microstructure)
    ms.saveActiveArea(name)
    switchboard.notify('stored active areas changed', name)

def _rename(menuitem, microstructure, oldname, newname):
    ms = ooflib.common.microstructure.getMicrostructure(microstructure)
    ms.renameActiveArea(oldname, newname)
    switchboard.notify('stored active areas changed', newname)

def _restore(menuitem, microstructure, name):
    ms = ooflib.common.microstructure.getMicrostructure(microstructure)
    naa = ms.getNamedActiveArea(name)
    ms.activearea.begin_writing()
    ms.activearea.pushModification(naa)
    ms.activearea.end_writing()
    switchboard.notify('active area modified', None)
    switchboard.notify('redraw')

def _delete(menuitem, microstructure, name):
    ms = ooflib.common.microstructure.getMicrostructure(microstructure)
    ms.deleteActiveArea(name)
    switchboard.notify('stored active areas changed', name)

# Build menu items for active area modifications

aamodmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'ActiveArea',
    cli_only=1,
    help='Create and manipulate Active Areas.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/activearea.xml')
    ))
                                                                                
def buildActiveAreaModMenu():
    aamodmenu.clearMenu()
                                                                                
    aamodmenu.addItem(oofmenu.OOFMenuItem(
        'Undo',
        callback=_undo,
        params=[whoville.WhoParameter(
                    'microstructure',
                    ooflib.common.microstructure.microStructures,
                    tip=parameter.emptyTipString)
                ],
        help="Undo the latest active area modification.",
        discussion="""<para>
        Revert to the previous &active; in the given
        &micro;.</para>"""
        ))
                                                                                
    aamodmenu.addItem(oofmenu.OOFMenuItem(
        'Redo',
        callback=_redo,
        params=[whoville.WhoParameter(
                    'microstructure',
                    ooflib.common.microstructure.microStructures,
                    tip=parameter.emptyTipString)
                ],
        help="Redo the latest undone active area modification.",
        discussion="""<para>
        Undo the latest <xref linkend='MenuItem:OOF.ActiveArea.Undo'/>.
        </para>"""))

    aamodmenu.addItem(oofmenu.OOFMenuItem(
        'Override',
        params=[parameter.BooleanParameter(
                    'override', 0,
                    tip="Whether to override or not."),
                whoville.WhoParameter(
                    'microstructure',
                    ooflib.common.microstructure.microStructures,
                    tip=parameter.emptyTipString)
                ],
        callback=_override,
        help="Temporarily activate the entire Microstructure.",
        discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/common/menu/activearea_override.xml')))

    aamodmenu.addItem(oofmenu.OOFMenuItem(
        'Store',
        callback=_store,
        params=parameter.ParameterGroup(
        whoville.WhoParameter('microstructure',
                              ooflib.common.microstructure.microStructures,
                              tip=parameter.emptyTipString),
        parameter.AutomaticNameParameter(
                    'name', value=automatic.automatic,
                    resolver=activeAreaNameResolver,
                    tip = "The name of the active are to be stored")),
        help="Store the current active area.",
        discussion="""<para>

        Give the current &active; a <varname>name</varname>, and store
        it for future use.  This makes it easy to switch between
        different active regions of a &micro;.  If the given
        <varname>name</varname> is already being used for another
        &active; in the same &micro;, then
        <userinput>&lt;x&gt;</userinput> will be appended to it, where
        <userinput>x</userinput> is an integer chosen to make the name
        unique.

        </para>"""))

    aamodmenu.addItem(oofmenu.OOFMenuItem(
        'Restore',
        callback=_restore,
        params=[whoville.WhoParameter(
                    'microstructure',
                    ooflib.common.microstructure.microStructures,
                    tip=parameter.emptyTipString),
                parameter.StringParameter(
                    'name', tip="The name of the active area to be restored.")],
        help="Restore a named active area.",
        discussion="""<para>
        Set the current &active; to the given <link
        linkend='MenuItem:OOF.ActiveArea.Store'>stored</link>
        &active;.
        </para>"""))
    
    aamodmenu.addItem(oofmenu.OOFMenuItem(
        'Rename',
        callback=_rename,
        params=[
        whoville.WhoParameter('microstructure',
                              ooflib.common.microstructure.microStructures,
                              tip=parameter.emptyTipString),
        parameter.StringParameter('oldname',
                                  tip="The name of a stored active area."),
        parameter.StringParameter('newname', '',
                                  tip='A new name for the active area.')
        ],
        help="Rename the stored active area.",
        discussion="<para>Assign a new name to a stored active area.</para>"))
    
    aamodmenu.addItem(oofmenu.OOFMenuItem(
        'Delete',
        callback=_delete,
        params=[
        whoville.WhoParameter('microstructure',
                              ooflib.common.microstructure.microStructures,
                              tip=parameter.emptyTipString),
        parameter.StringParameter(
                    'name',
                    tip="The name of the active area to be deleted.")],
        help="Delete a stored active area.",
        discussion="""<para>
        Delete a <link
        linkend='MenuItem:OOF.ActiveArea.Store'>stored</link> active
        area.  This only deletes the stored copy of the active area.
        It does not affect the activity of any pixels.
        </para>"""))
    
                           
                                                                                
    for registration in activeareamod.ActiveAreaModifier.registry:
        # registration tip string => menuitem help string
        try:
            help = registration.tip
        except AttributeError:
            help = None
        # registration discussion => menuitem discussion
        try:
            discussion = registration.discussion
        except AttributeError:
            discussion = None
        menuitem = aamodmenu.addItem(
            oofmenu.OOFMenuItem(utils.space2underscore(registration.name()),
                                callback=activeareamod.modify,
                                params=[
            whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString)
            ] + registration.params,
                                help=help,
                                discussion=discussion))
        menuitem.data = registration
                                                                                
buildActiveAreaModMenu()
