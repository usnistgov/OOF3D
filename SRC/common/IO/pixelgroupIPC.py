# -*- python -*-
# $RCSfile: pixelgroupIPC.py,v $
# $Revision: 1.1.12.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Menu commands for manipulating PixelGroups

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import config
##from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.common import switchboard
##from ooflib.common import debug
##from ooflib.common import primitives
from ooflib.common.IO import parallelmainmenu
##from ooflib.common.IO import automatic
##from ooflib.common.IO import microstructureIO
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
##from ooflib.common.IO import xmlmenudump
##from ooflib.common.IO.mainmenu import OOF
from ooflib.common.IO import oofmenu
from ooflib.common.IO.oofmenu import OOFMenuItem
from ooflib.common.IO.pixelgroupparam import PixelGroupParameter
##from types import *
import ooflib.common.microstructure      # a local variable is named 'microstructure'

BooleanParameter = parameter.BooleanParameter
StringParameter = parameter.StringParameter

#OOF.LoadData.IPC.PixelGroup
ipcpixgrpmenu = parallelmainmenu.ipcmenu.addItem(
    OOFMenuItem('PixelGroup', secret=1, no_log=1)
    )

##########################

# PixelGroup menu items are responsible for issuing the appropriate
# switchboard notifications when pixel group memberships change, so
# that the skeletons etc. can recompute their homogeneity.  In
# particular, the "changed pixel group" signal is emitted in these
# menu items, outside of the microstructure lock.  This is so that
# switchboard callbacks don't have to worry about locking issues.

def newPixelGroup_parallel(menuitem, name, microstructure):
    if name and microstructure:
        mscontext = ooflib.common.microstructure.microStructures[microstructure]
        ms = mscontext.getObject()
        mscontext.begin_writing()
        try:
            if ms:
                (grp, newness) = ms.getGroup(name)  
        finally:
            mscontext.end_writing()

        if newness:
            switchboard.notify("new pixel group", grp)
        return grp
                
    reporter.report("Failed to create group", name, "in microstructure",
                    microstructure)

ipcpixgrpmenu.addItem(OOFMenuItem(
    'New',
    callback=newPixelGroup_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=parameter.ParameterGroup(
    StringParameter('name',
                    tip="Group name."),
    whoville.WhoParameter('microstructure', whoville.getClass('Microstructure'),
                          tip=
                          "Microstructure in which to create this PixelGroup.")
    ),
    help='Create a new PixelGroup in the given Microstructure.',
    discussion="""<para>

    Create a new &pixelgroup;.  The <varname>name</varname> of the
    group must be unique within the &micro;.  If it is not unique, a
    suffix of the form <userinput>&lt;x&gt;</userinput> will be
    appended, for some integer <userinput>x</userinput>.

    </para>"""))

##########################

def renamePixelGroup_parallel(menuitem, microstructure, group, new_name):
    # "group" arg is the old group name.
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    mscontext.begin_writing()
    renamed = False
    try:
        grp = ms.findGroup(group)
        # Don't just say "if grp" here.  PixelGroup has a __len__
        # function, so empty groups evaluate to "false".
        if grp is not None:
            ms.renameGroup(group, new_name)
            renamed = True
            #Interface branch (only implemented for 2D)
            if config.dimension() == 2:
                interfacemsplugin=ms.getPlugIn("Interfaces")
                interfacemsplugin.renameGroup(group, new_name)
        else:
            raise ooferror.ErrUserError("There is no pixel group named %s!"
                                        % group)
    finally:
        mscontext.end_writing()

    if renamed:
        switchboard.notify('renamed pixel group', grp, group, new_name)

ipcpixgrpmenu.addItem(OOFMenuItem(
    'Rename',
    callback=renamePixelGroup_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip='PixelGroup to be renamed.'),
    StringParameter('new_name', 
              tip='New name for the group, in quotation marks.')
    ],
    help='Rename an existing PixelGroup in the given Microstructure.',
    discussion="""<para>

    Assign a new name to a &pixelgroup;.  The
    <varname>new_name</varname> must be unique, just as it must be for
    a <link linkend='MenuItem:OOF.PixelGroup.New'>new</link> group.

    </para>"""))

##########################

def copyPixelGroup_parallel(menuitem, microstructure, group, name):
    if group != name:
        mscontext = ooflib.common.microstructure.microStructures[microstructure]
        ms = mscontext.getObject()
        mscontext.begin_writing()
        newness = False
        try:
            oldgroup = ms.findGroup(group)
            if oldgroup is not None:
                (newgroup, newness) = ms.getGroup(name)
                newgroup.addWithoutCheck(oldgroup.members())
            else:
                raise ooferror.ErrUserError("There is no pixel group named %s!"
                                            % group)
        finally:
            mscontext.end_writing()
            
        if newness:
            switchboard.notify("new pixel group", newgroup)
        switchboard.notify("changed pixel group", newgroup, microstructure)
        
            
ipcpixgrpmenu.addItem(OOFMenuItem(
    'Copy',
    callback=copyPixelGroup_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=parameter.ParameterGroup(
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip='PixelGroup to be copied.'),
    StringParameter('name',
                    tip="Group name.")
    ),
    help='Make a copy of an existing pixel group',
    discussion="""<para>

    Copy an exisiting &pixelgroup;.  The <varname>name</varname> must
    be unique, just as it must be for a <link
    linkend='MenuItem:OOF.PixelGroup.New'>new</link> group.

    </para>"""))

##########################

def destroyPixelGroup_parallel(menuitem, microstructure, group):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    mscontext.begin_writing()
    try:
        # Need the group object for the switchboard signal.
        grp = ms.findGroup(group)
        ms.removeGroup(group)  
    finally:
        mscontext.end_writing()

    if grp is not None:
        switchboard.notify("destroy pixel group", grp, microstructure)
    switchboard.notify('redraw')

ipcpixgrpmenu.addItem(OOFMenuItem(
    'Delete',
    callback=destroyPixelGroup_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip='PixelGroup to be destroyed.')
    ],
    help='Delete the selected Pixel Group.',
    discussion="<para>Remove a &pixelgroup; completely from a &micro;.</para>"))

##########################

def meshablePixelGroup_parallel(menuitem, microstructure, group, meshable):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    mscontext.begin_writing()
    try:
        grp = ms.findGroup(group)
        if grp is not None:
            grp.set_meshable(meshable)
            ms.recategorize()
        else:
            raise ooferror.ErrUserError("There is no pixel group named %s!"
                                        % group)
    finally:
        mscontext.end_writing()

    switchboard.notify('redraw')
    if grp is not None:
        switchboard.notify("changed pixel group", grp, microstructure)
        
ipcpixgrpmenu.addItem(OOFMenuItem(
    'Meshable',
    callback=meshablePixelGroup_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip="Pixel group."),
    BooleanParameter('meshable', tip="1 (true) for meshable and 0 (false) for non-meshable.")],
    help="Should adaptive Skeletons follow the boundaries of the given group?",
    discussion="""<para>

    If a &pixelgroup; is <constant>meshable</constant>, then the
    boundaries of the group are respected by the &skel; <link
    linkend='MenuItem:OOF.Skeleton.Modify'>modification</link>
    (adaptive meshing) tools.  That is, the tools attempt to create
    &skels; that resolve the <constant>meshable</constant> group
    boundaries as well as the &material; boundaries.  By default,
    <link linkend='MenuItem:OOF.PixelGroup.New'>new</link>
    &pixelgroups; are <constant>meshable</constant>.

    </para>"""))
        

##########################

#TODO: When a selection is made on the front end (process 0),
#there is no way yet for the other processes to know the selection,
#so addSelection and removeSelection won't work correctly.

def addSelection_parallel(menuitem, microstructure, group):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    ms.pixelselection.begin_reading()
    try:
        sel = ms.pixelselection.getObject()
        pxls = sel.members()
    finally:
        ms.pixelselection.end_reading()
    mscontext.begin_writing()
    try:
        grp = ms.findGroup(group)
        grp.add(pxls)
    finally:
        mscontext.end_writing()

    if grp is not None:
        switchboard.notify("changed pixel group", grp, microstructure)
    switchboard.notify('redraw')


ipcpixgrpmenu.addItem(OOFMenuItem(
    'AddSelection',
    callback=addSelection_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group',
                        tip="Group to which to add the selected pixels.")
            ],
    help='Add the currently selected pixels to the given PixelGroup.',
    discussion="""<para>
    The pixels that are currently <link
    linkend='Section:Concepts:Microstructure:PixelSelection'>selected</link>
    will be added to the given &pixelgroup;.
    </para>"""))
    
#########################

def removeSelection_parallel(menuitem, microstructure, group):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    ms.pixelselection.begin_reading()
    try:
        sel = ms.pixelselection.getObject()
        pxls = sel.members()
    finally:
        ms.pixelselection.end_reading()
    
    mscontext.begin_writing()
    try:
        grp = ms.findGroup(group)
        grp.remove(pxls)          # calls ms.recategorize(), which
                                  # increments the timestamp of ms AND
                                  # issues "changed pixel group" signal.
    finally:
        mscontext.end_writing()

    if grp is not None:
        switchboard.notify("changed pixel group", grp, microstructure)
    switchboard.notify('redraw')        
    

ipcpixgrpmenu.addItem(OOFMenuItem(
    'RemoveSelection',
    callback=removeSelection_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group',
                        tip="Group from which to remove the selected pixels.")
            ],
    help='Remove the currently selected pixels from the given PixelGroup.',
    discussion="""<para>

    Any pixels that are currently <link
    linkend='Section:Concepts:Microstructure:PixelSelection'>selected</link>
    and belong to the given &pixelgroup; will be removed from the
    group.

    </para>"""))

#########################

def clearGroup_parallel(menuitem, microstructure, group):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    mscontext.begin_writing()
    try:
        grp = ms.findGroup(group)
        grp.clear()
    finally:
        mscontext.end_writing()

    if grp is not None:
        switchboard.notify("changed pixel group", grp, microstructure)
    switchboard.notify('redraw')
        
ipcpixgrpmenu.addItem(OOFMenuItem(
    'Clear',
    callback=clearGroup_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip='Group from which to remove all pixels.')
    ],
    help="Remove all pixels from the given PixelGroup.",
    discussion="<para>Empty the selected &pixelgroup;.</para>"))
