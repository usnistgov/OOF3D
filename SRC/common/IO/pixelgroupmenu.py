# -*- python -*-
# $RCSfile: pixelgroupmenu.py,v $
# $Revision: 1.56.12.7 $
# $Author: langer $
# $Date: 2014/09/15 15:08:55 $

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
from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import parallel_enable
from ooflib.common import runtimeflags
from ooflib.common.IO import automatic
from ooflib.common.IO import microstructureIO
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.common.IO.mainmenu import OOF
from ooflib.common.IO.oofmenu import OOFMenuItem
from ooflib.common.IO.pixelgroupparam import PixelGroupParameter
from types import *
import ooflib.common.microstructure      # a local variable is named 'microstructure'

if parallel_enable.enabled():
    from ooflib.common.IO import pixelgroupIPC

BooleanParameter = parameter.BooleanParameter
AutomaticNameParameter = parameter.AutomaticNameParameter
StringParameter = parameter.StringParameter

pixgrpmenu = OOF.addItem(OOFMenuItem(
    'PixelGroup', cli_only=1,
    help='Create and manipulate pixel groups.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/pixelgroup.xml')
    ))

##########################


# PixelGroup menu items are responsible for issuing the appropriate
# switchboard notifications when pixel group memberships change, so
# that the skeletons etc. can recompute their homogeneity.  In
# particular, the "changed pixel group" signal is emitted in these
# menu items, outside of the microstructure lock.  This is so that
# switchboard callbacks don't have to worry about locking issues.

def newPixelGroup(menuitem, name, microstructure):
    if parallel_enable.enabled():
        pixelgroupIPC.ipcpixgrpmenu.New(name=name,
                                        microstructure=microstructure)
        return
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

def pixelGroupNameResolver(param, startname):
    if param.automatic():
        basename = 'pixelgroup'
    else:
        basename = startname
    msname = param.group['microstructure'].value
    ms = ooflib.common.microstructure.getMicrostructure(msname)
    return ms.uniqueGroupName(basename)

pixgrpmenu.addItem(OOFMenuItem(
    'New',
    callback=newPixelGroup,
    params=parameter.ParameterGroup(
    AutomaticNameParameter('name', value=automatic.automatic,
                           resolver=pixelGroupNameResolver,
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

def renamePixelGroup(menuitem, microstructure, group, new_name):
    if parallel_enable.enabled():
        pixelgroupIPC.ipcpixgrpmenu.Rename(microstructure=microstructure,
                                           group=group,
                                           new_name=new_name)
        return

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
            if config.dimension() == 2 and runtimeflags.surface_mode:
                interfacemsplugin=ms.getPlugIn("Interfaces")
                interfacemsplugin.renameGroup(group, new_name)
        else:
            raise ooferror.ErrUserError("There is no pixel group named %s!"
                                        % group)
    finally:
        mscontext.end_writing()

    if renamed:
        switchboard.notify('renamed pixel group', grp, group, new_name)

pixgrpmenu.addItem(OOFMenuItem(
    'Rename', callback=renamePixelGroup,
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

def copyPixelGroup(menuitem, microstructure, group, name):
    if parallel_enable.enabled():
        pixelgroupIPC.ipcpixgrpmenu.Copy(microstructure=microstructure,
                                         group=group,
                                         name=name)
        return
    if group != name:
        mscontext = ooflib.common.microstructure.microStructures[microstructure]
        ms = mscontext.getObject()
        mscontext.begin_writing()
        newness = False
        try:
            oldgroup = ms.findGroup(group)
            if oldgroup is not None:
                (newgroup, newness) = ms.getGroup(name)
                newgroup.addWithoutCheck(oldgroup)
            else:
                raise ooferror.ErrUserError("There is no pixel group named %s!"
                                            % group)
        finally:
            mscontext.end_writing()
            
        if newness:
            switchboard.notify("new pixel group", newgroup)
        switchboard.notify("changed pixel group", newgroup, microstructure)
        
            
pixgrpmenu.addItem(OOFMenuItem(
    'Copy', callback=copyPixelGroup,
    params=parameter.ParameterGroup(
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip='PixelGroup to be copied.'),
    AutomaticNameParameter('name', value=automatic.automatic,
                           resolver=pixelGroupNameResolver,
                           tip="Group name.")
    ),
    help='Make a copy of an existing pixel group',
    discussion="""<para>

    Copy an exisiting &pixelgroup;.  The <varname>name</varname> must
    be unique, just as it must be for a <link
    linkend='MenuItem:OOF.PixelGroup.New'>new</link> group.

    </para>"""))

##########################

def destroyPixelGroup(menuitem, microstructure, group):
    if parallel_enable.enabled():
        pixelgroupIPC.ipcpixgrpmenu.Delete(microstructure=microstructure,
                                           group=group)
        return
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



pixgrpmenu.addItem(OOFMenuItem(
    'Delete',
    callback=destroyPixelGroup,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip='PixelGroup to be destroyed.')
    ],
    help='Delete the selected Pixel Group.',
    discussion="<para>Remove a &pixelgroup; completely from a &micro;.</para>"))

##########################

def meshablePixelGroup(menuitem, microstructure, group, meshable):
    if parallel_enable.enabled():
        pixelgroupIPC.ipcpixgrpmenu.Meshable(microstructure=microstructure,
                                             group=group,
                                             meshable=meshable)
        return

    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    mscontext.begin_writing()
    try:
        grp = ms.findGroup(group)
        if grp is not None:
            grp.set_meshable(meshable)
            # TODO OPT: Does this need to call buildAttributeChangeMap and
            # updateAttributeVector before recategorize()?
            ms.recategorize()
        else:
            raise ooferror.ErrUserError("There is no pixel group named %s!"
                                        % group)
    finally:
        mscontext.end_writing()

    switchboard.notify('redraw')
    if grp is not None:
        switchboard.notify("changed pixel group", grp, microstructure)
        
pixgrpmenu.addItem(OOFMenuItem(
    'Meshable',
    callback=meshablePixelGroup,
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

def addSelection(menuitem, microstructure, group):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    ms.pixelselection.begin_reading()
    try:
        sel = ms.pixelselection.getObject()
    finally:
        ms.pixelselection.end_reading()
    mscontext.begin_writing()
    try:
        grp = ms.findGroup(group)
        grp.add(sel)
    finally:
        mscontext.end_writing()

    if grp is not None:
        switchboard.notify("changed pixel group", grp, microstructure)
    switchboard.notify('redraw')


pixgrpmenu.addItem(OOFMenuItem(
    'AddSelection',
    callback=addSelection,
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

def removeSelection(menuitem, microstructure, group):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    ms.pixelselection.begin_reading()
    try:
        sel = ms.pixelselection.getObject()
    finally:
        ms.pixelselection.end_reading()
    
    mscontext.begin_writing()
    try:
        grp = ms.findGroup(group)
        grp.remove(sel)         # calls ms.recategorize(), which
                                  # increments the timestamp of ms AND
                                  # issues "changed pixel group" signal.
    finally:
        mscontext.end_writing()

    if grp is not None:
        switchboard.notify("changed pixel group", grp, microstructure)
    switchboard.notify('redraw')        
    

pixgrpmenu.addItem(OOFMenuItem(
    'RemoveSelection',
    callback=removeSelection,
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

def clearGroup(menuitem, microstructure, group):
    if parallel_enable.enabled():
        pixelgroupIPC.ipcpixgrpmenu.Clear(microstructure=microstructure,
                                          group=group)
        return

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
        
pixgrpmenu.addItem(OOFMenuItem(
    'Clear',
    callback=clearGroup,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip='Group from which to remove all pixels.')
    ],
    help="Remove all pixels from the given PixelGroup.",
    discussion="<para>Empty the selected &pixelgroup;.</para>"))

def queryGroup(menuitem, microstructure, group):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    mscontext.begin_reading()
    try:
        grp = ms.findGroup(group)
        nop = len(grp)
        areaOfGroup = nop*ms.areaOfPixels()
    finally:
        mscontext.end_reading()
    reporter.report(">>> ", nop, " pixels, ", "area = ", areaOfGroup)

pixgrpmenu.addItem(OOFMenuItem(
    'Query',
    callback=queryGroup,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    PixelGroupParameter('group', tip='Get information on this group.')
    ],
    help="Query the given PixelGroup.",
    discussion="<para>Print some information about the given &pixelgroup;.</para>"))
    
        
############################

# Functions for reading and writing pixelgroups in a data file. 

## TODO 3.1: Unmeshable groups aren't being stored in data files.  The
## DefineCategory command is missing.  This is related (or identical?)
## to the problem with saving active areas.  See the TODO about
## ActiveAreas in cmicrostructure.spy.

def _writeData(self, dfile, microstructure, reppxl):
    cat = microstructure.category(reppxl)
    grpnames = pixelgroup.pixelGroupNames(microstructure, cat)
    if grpnames:
        dfile.argument('groups', grpnames)
        return 1
    return 0

pixelgroup.PixelGroupAttributeRegistrationPtr.writeData = _writeData

def _readPixelGroups(menuitem, microstructure, category, groups):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    mscontext.begin_writing()
    new_group_list = []
    all_group_dict = {}
    try:
        pixels = microstructureIO.getCategoryPixels(microstructure, category)
        for groupname in groups:
            (grp, newness) = ms.getGroup(groupname)
            grp.addPixels(pixels)
            all_group_dict[grp]=1
            if newness:
                new_group_list.append(grp)
    finally:
        mscontext.end_writing()
        
    for g in all_group_dict.keys():
        switchboard.notify("changed pixel group", g, microstructure)
    for g in new_group_list:
        switchboard.notify("new pixel group", g)

microstructureIO.categorymenu.addItem(OOFMenuItem(
    pixelgroup.attributeReg.name(),
    callback=_readPixelGroups,
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    parameter.IntParameter('category', tip="Pixel category."),
    parameter.ListOfStringsParameter('groups', tip="List of names of pixel groups.")
    ],
    help="Assign pixel groups to pixel categories. Used internally in data files.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/pgroupcategory.xml')
    ))
