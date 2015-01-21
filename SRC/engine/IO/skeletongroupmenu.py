# -*- python -*-
# $RCSfile: skeletongroupmenu.py,v $
# $Revision: 1.44.2.16 $
# $Author: langer $
# $Date: 2014/09/17 17:48:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This file builds the menu commands that operate the methods
# of the various selectable-groups, corresponding to methods
# of GenericGroupSet class in skeletongroups.py

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.engine import cskeleton2
from ooflib.common import debug
from ooflib.common import microstructure
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import automatic
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletongroups
from ooflib.engine import materialmanager
from ooflib.engine.IO import materialparameter
from ooflib.engine.IO import skeletongroupparams
# if config.dimension() == 2:
#     import ooflib.engine.skeleton as skeleton
# elif config.dimension() == 3:
#     import ooflib.engine.skeleton3d as skeleton
import types

AutomaticNameParameter = parameter.AutomaticNameParameter
NodeGroupParameter = skeletongroupparams.NodeGroupParameter
SegmentGroupParameter = skeletongroupparams.SegmentGroupParameter
ElementGroupParameter = skeletongroupparams.ElementGroupParameter
if config.dimension() == 3:
    FaceGroupParameter = skeletongroupparams.FaceGroupParameter

nodegroupmenu = oofmenu.OOFMenuItem(
    "NodeGroup",
    cli_only=1,
    help='Create and manage NodeGroups.',
    discussion="""<para>
    &nodegroups; provide a convenient way of operating on many &skel;
    &nodes; simultaneously.
    </para>""")

segmentgroupmenu = oofmenu.OOFMenuItem(
    "SegmentGroup",
    cli_only=1,
    help='Create and manage SegmentGroups.',
    discussion="""<para>
    &sgmtgroups; provide a convenient way of operating on many &skel;
    &sgmts; simultaneously.
    </para>""")

elementgroupmenu = oofmenu.OOFMenuItem(
    "ElementGroup",
    cli_only=1,
    help='Create and manage ElementGroups.',
    discussion="""<para>
    &elemgroups; provide a convenient way of operating on many &skel;
    &elems; simultaneously.
    </para>""")

facegroupmenu = oofmenu.OOFMenuItem(
    "FaceGroup",
    cli_only=1,
    help='Create and manage FaceGroups.',
    discussion="""<para>
    &facegroups; provide a convenient way of operating on many &skel;
    &faces; simultaneously.
    </para>""")


mainmenu.OOF.addItem(nodegroupmenu)
mainmenu.OOF.addItem(segmentgroupmenu)
mainmenu.OOF.addItem(elementgroupmenu)
mainmenu.OOF.addItem(facegroupmenu)


########################################################################

# Generic callbacks usable by all classes of selectables.  Menu items
# must have a "data" item which is a string corresponding to the name
# of the selection set in the skeletoncontext, e.g. "nodegroups", so
# that the menuitem callback can retrieve the right groupset.

# Make a new group name known.

def _new_group(menuitem, skeleton, name):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    if groupset.isGroup(name):
        raise ooferror.ErrUserError("Group %s already exists." % group)
    else:
        groupset.addGroup(name)

# Create groups from pixel groups.

def _auto_group(menuitem, skeleton):
    ## TODO OPT: Move this to C++
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    ms = skelc.getMicrostructure()
    mscontext = microstructure.microStructures[ms.name()]
    mscontext.begin_reading()
    # gdict is a dict of lists of objects to add to each group, keyed
    # by group name.
    gdict = {}
    try:
        # Create groups
        groupnames = ms.groupNames() # all pixel group names in ms
        newgrps = [name for name in groupnames if not groupset.isGroup(name)]
        groupset.addGroup(*newgrps)
        # Find objects to add to groups
        for obj in menuitem.iterator(skelc.getObject().sheriffSkeleton()):
            cat = obj.dominantPixel(ms) # dominant pxl category
            grplist = pixelgroup.pixelGroupNames(ms, cat)
            for name in grplist:
                gdict.setdefault(name, []).append(obj)
        # Actually add objects to groups
        groupset.addToGroup(**gdict)
    finally:
        mscontext.end_reading()
    
# Delete a group.
def _remove_group(menuitem, skeleton, group):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    if not groupset.isGroup(group):
        raise ooferror.ErrUserError("Group %s does not exist." % group)
    else:
        groupset.removeGroup(group)

# Delete all groups.
def _remove_all_groups(menuitem, skeleton):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    groupset.removeGroup(*groupset.allGroups().copy())
    
# Copy an existing group.
def _copy_group(menuitem, skeleton, group, new_name):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    if groupset.isGroup(new_name):
        raise ooferror.ErrUserError("Group %s already exists." % new_name)
    if groupset.isGroup(group):
        groupset.copyGroup(group, new_name)


# Add the current selection to the named group, creating
# the group if required.
def _add_selection_to_group(menuitem, skeleton, group):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    if not groupset.isGroup(group):
        groupset.addGroup(group)
    groupset.addSelectionToGroup(group)

# Remove the currently-selected objects from the named group.
def _remove_selection_from_group(menuitem, skeleton, group):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    groupset.removeSelectionFromGroup(group)

    
# Rename an existing group.
def _rename_group(menuitem, skeleton, group, new_name):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    groupset.renameGroup(group, new_name)
        

# Clear a group (remove all pixels from it, but don't delete the group).
def _clear_group(menuitem, skeleton, group):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    if not groupset.isGroup(group):
        raise ooferror.ErrUserError("Group %s does not exist." % group)
    groupset.clearGroup(group)

def _clear_all_groups(menuitem, skeleton):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    groupset.clearGroup(*groupset.allGroups())

def _assign_matl(menuitem, skeleton, group, material):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    if not groupset.isGroup(group):
        raise ooferror.ErrUserError("Group %s does not exist." % group)
    groupset.assignMaterial(group, materialmanager.getMaterial(material))

def _remove_matl(menuitem, skeleton, group):
    skelc = whoville.getClass('Skeleton')[skeleton]
    groupset = getattr(skelc, menuitem.data)
    if not groupset.isGroup(group):
        raise ooferror.ErrUserError("Group %s does not exist." % group)
    groupset.removeMaterial(group)

#######################################

class GroupNameResolver:
    # Callable object to be used as the resolver for the
    # AutomaticNameParameter for group names.  Requires derived
    # classes that define getBasename().
    def __init__(self, attrname):
        # attrname is the name of the SkeletonContext attribute that
        # holds the groupset, eg, "nodegroups".
        self.attrname = attrname
    def __call__(self, param, startname):
        skelname = param.group['skeleton'].value
        skelcontext = whoville.getClass('Skeleton')[skelname]
        groupset = getattr(skelcontext, self.attrname)
        return utils.uniqueName(self.getBasename(param, startname),
                                list(groupset.allGroups()))

class NewGroupNameResolver(GroupNameResolver):
    # Gets the default name from the constructor arguments.
    def __init__(self, basename, attrname):
        GroupNameResolver.__init__(self, attrname)
        # basename is the defaultname to be used for the groups.
        self.basename = basename
    def getBasename(self, param, startname):
        if param.automatic():
            return self.basename
        return startname

class CopyGroupNameResolver(GroupNameResolver):
    # Gets the default name from the object being copied (or renamed).
    def getBasename(self, param, startname):
        if param.automatic():
            return param.group['group'].value
        return startname
    
#######################################    

# Node-specific menu items:

new = oofmenu.OOFMenuItem(
    "New_Group",
    cli_only=1,
    callback=_new_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    AutomaticNameParameter("name", value=automatic.automatic,
                           resolver=NewGroupNameResolver("nodegroup",
                                                         "nodegroups"),
                           tip="Name of the group to be created.")),
    help="Create a new node group.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/newnodegroup.xml')
    )
new.data = "nodegroups"
nodegroupmenu.addItem(new)

auto = oofmenu.OOFMenuItem(
    "Auto_Group",
    cli_only=1,
    callback=_auto_group,
    params=[whoville.WhoParameter("skeleton", whoville.getClass("Skeleton"),
                                  tip=parameter.emptyTipString)],
    help="Create node groups for each pixel group.",
    discussion=
"""<para>Automatically create a &nodegroup; in the &skel; for every
&pixelgroup; in the &micro;.  All &skel; &nodes; lying on a pixel in a
&pixelgroup; will be added to a &nodegroup; with the same name as the
&pixelgroup;. New groups will be created if necessary.</para>"""
    )
auto.data = "nodegroups"
#auto.iterator = skeleton.Skeleton.node_iterator
auto.iterator = cskeleton2.CSkeletonBasePtr.getNodes
nodegroupmenu.addItem(auto)


rename = oofmenu.OOFMenuItem(
    "Rename_Group", cli_only=1,
    callback=_rename_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    NodeGroupParameter("group", tip="Name of the group to be renamed."),
    parameter.StringParameter("new_name", "",
                              tip="New name for the node group")),
    help="Rename a node group.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/renamenodegroup.xml')
    )
rename.data = "nodegroups"
nodegroupmenu.addItem(rename)


copy = oofmenu.OOFMenuItem(
    "Copy_Group",
    cli_only=1,
    callback=_copy_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    NodeGroupParameter("group", tip="Name of the group to be copied."),
    AutomaticNameParameter("new_name",
                           resolver=CopyGroupNameResolver("nodegroups"),
                           value=automatic.automatic,
                           tip="Name for the copy.")),
    help="Make a copy of a node group.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/copynodegroup.xml')
    )
copy.data = "nodegroups"
nodegroupmenu.addItem(copy)


remove = oofmenu.OOFMenuItem(
    "Delete_Group",
    cli_only=1,
    callback=_remove_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    NodeGroupParameter("group", tip="Name of the group to be deleted.")],
    help="Remove a node group.",
    discussion="""<para>
    Delete the given &nodegroup; from the &skel;. The &nodes;
    themselves are not affected.
    </para>""")
remove.data = "nodegroups"
nodegroupmenu.addItem(remove)

removeall = oofmenu.OOFMenuItem(
    "Delete_All",
    cli_only=1,
    callback=_remove_all_groups,
    params=[
    whoville.WhoParameter('skeleton', whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString)],
    help="Remove all node groups.",
    discussion="""<para>
    Delete all &nodegroups; from the &skel;.
    The &nodes; themselves are not affected.
    </para>""")
removeall.data = "nodegroups"
nodegroupmenu.addItem(removeall)

addselect = oofmenu.OOFMenuItem(
    "Add_to_Group",
    cli_only=1,
    callback=_add_selection_to_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    NodeGroupParameter("group", tip="Name of the group.")],
    help="Add selected nodes to the group.",
    discussion="""<para>
    Add the currently selected &skel; &nodes; to the given &nodegroup;.
    </para>""") 
addselect.data = "nodegroups"
nodegroupmenu.addItem(addselect)


removeselect = oofmenu.OOFMenuItem(
    "Remove_from_Group",
    cli_only=1,
    callback=_remove_selection_from_group,
    params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString),
            NodeGroupParameter("group", tip="Name of the group")],
    help="Remove selected nodes from the group.",
    discussion="""<para>
    Remove the currently selected &skel; &nodes; from the given &nodegroup;.
    </para>""") 
removeselect.data = "nodegroups"
nodegroupmenu.addItem(removeselect)


clear = oofmenu.OOFMenuItem(
    "Clear_Group", cli_only=1,
    callback=_clear_group,
    params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString),
            NodeGroupParameter("group", tip="Name of the group.")],
    help="Clear a node group.",
    discussion="""<para>
    Remove all &nodes; from the given &nodegroup;.  The group itself
    will <emphasis>not</emphasis> be deleted, but will be emptied.
    </para>""")
clear.data = "nodegroups"
nodegroupmenu.addItem(clear)


clearall = oofmenu.OOFMenuItem(
    "Clear_All",
    cli_only=1,
    callback=_clear_all_groups,
    params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString)],
    help="Clear all node groups.",
    discussion="""<para>
    Remove all &nodes; from all &nodegroups;.  The groups themselves will
    <emphasis>not</emphasis> be deleted, but will be emptied.
    </para>""")
clearall.data = "nodegroups"
nodegroupmenu.addItem(clearall)

def _query_node_group(menuitem, skeleton, group):
    skelc = whoville.getClass('Skeleton')[skeleton]
    members = skelc.nodegroups.get_group(group)
    plural="s"*(len(members)!=1)
    reporter.report(">>> ", len(members), " node"+plural )

nodegroupmenu.addItem(oofmenu.OOFMenuItem(
    "Query_Group",
    cli_only=1,
    callback=_query_node_group,
    params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString),
            NodeGroupParameter("group", tip="Name of the group.")],
    help="Query a node group.",
    discussion="<para>Print information about the given &nodegroup;.</para>") )

#########################################################

# Segments.

new = oofmenu.OOFMenuItem(
    "New_Group",
    cli_only=1,
    callback=_new_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    AutomaticNameParameter("name",
                           value=automatic.automatic,
                           resolver=NewGroupNameResolver("segmentgroup",
                                                         "segmentgroups"),
                           tip="Name of the group.")),
    help="Create a new segment group.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/newsegmentgroup.xml')
    )
new.data = "segmentgroups"
segmentgroupmenu.addItem(new)


auto = oofmenu.OOFMenuItem(
    "Auto_Group",
    cli_only=1,
    callback=_auto_group,
    params=[whoville.WhoParameter("skeleton", whoville.getClass("Skeleton"),
                                  tip=parameter.emptyTipString)],
    help="Create segment groups for each pixel group.",
    discussion=
"""<para>Automatically create a &sgmtgroup; in the &skel; for every
&pixelgroup; in the &micro;.  All &skel; &sgmts; lying on a pixel in a
&pixelgroup; will be added to a &sgmtgroup; with the same name as the
&pixelgroup;.  New groups will be created if necessary.</para>"""
    )
auto.data = "segmentgroups"
#auto.iterator = skeleton.Skeleton.segment_iterator
auto.iterator = cskeleton2.CSkeletonBasePtr.getSegments
segmentgroupmenu.addItem(auto)


rename = oofmenu.OOFMenuItem(
    "Rename_Group",
    cli_only=1,
    callback=_rename_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    SegmentGroupParameter("group", tip="Name of the group to be renamed."),
    parameter.StringParameter("new_name", "",
                              tip="New name for the segment group")),
    help="Rename a segment group.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/renamesegmentgroup.xml')
    )

rename.data = "segmentgroups"

segmentgroupmenu.addItem(rename)


copy = oofmenu.OOFMenuItem(
    "Copy_Group",
    cli_only=1,
    callback=_copy_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    SegmentGroupParameter("group", tip="Name of the group to be copied."),
    AutomaticNameParameter("new_name",
                           resolver=CopyGroupNameResolver("segmentgroups"),
                           value=automatic.automatic,
                           tip="New name for the copy.")),
    help="Copy a segment group.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/copysegmentgroup.xml')
    )
copy.data = "segmentgroups"
segmentgroupmenu.addItem(copy)


remove = oofmenu.OOFMenuItem(
    "Delete_Group",
    cli_only=1,
    callback=_remove_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    SegmentGroupParameter("group", tip="Name of the group.")],
    help="Remove a segment group.",
    discussion="""<para>
    Delete the given &sgmtgroup; from the &skel;.  The &sgmts;
    themselves are not affected.
    </para>""")
remove.data = "segmentgroups"
segmentgroupmenu.addItem(remove)


removeall = oofmenu.OOFMenuItem(
    "Delete_All",
    cli_only=1,
    callback=_remove_all_groups,
    params=[
    whoville.WhoParameter('skeleton', whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString)],
    help="Remove all segment groups.",
    discussion="""<para>
    Delete all &sgmtgroups; from the &skel;.
    The &sgmts; themselves are not affected.
    </para>""")
removeall.data = "segmentgroups"
segmentgroupmenu.addItem(removeall)


addselect = oofmenu.OOFMenuItem(
    "Add_to_Group",
    cli_only=1,
    callback=_add_selection_to_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    SegmentGroupParameter("group", tip="Name of the group.")],
    help="Add selected segments to the group.",
    discussion="""<para>
    Add the currently selected &skel; &sgmts; to the given &sgmtgroup;.
    </para>""") 
addselect.data = "segmentgroups"
segmentgroupmenu.addItem(addselect)


removeselect = oofmenu.OOFMenuItem(
    "Remove_from_Group",
    cli_only=1,
    callback=_remove_selection_from_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    SegmentGroupParameter("group", tip="Name of the group.")],
    help="Remove selected segments from the group.",
    discussion="""<para>
    Remove the currently selected &skel; &sgmts; from the given &sgmtgroup;.
    </para>""")
removeselect.data = "segmentgroups"
segmentgroupmenu.addItem(removeselect)


clear = oofmenu.OOFMenuItem(
    "Clear_Group",
    cli_only=1,
    callback=_clear_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    SegmentGroupParameter("group", tip="Name of the group.")],
    help="Clear a segment group.",
    discussion="""<para>
    Remove all &sgmts; from the given &sgmtgroup;.  The group itself
    will <emphasis>not</emphasis> be deleted, but will be emptied.
    </para>""")
clear.data = "segmentgroups"
segmentgroupmenu.addItem(clear)


clearall = oofmenu.OOFMenuItem(
    "Clear_All",
    cli_only=1,
    callback=_clear_all_groups,
    params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString)],
    help="Clear all segment groups.",
    discussion="""<para>
    Remove all &sgmts; from all &sgmtgroups;.  The groups themselves will
    <emphasis>not</emphasis> be deleted, but will be emptied.
    </para>""")
clearall.data = "segmentgroups"
segmentgroupmenu.addItem(clearall)


def _query_sgmt_group(menuitem, skeleton, group):
    skelc = whoville.getClass('Skeleton')[skeleton]
    members = skelc.segmentgroups.get_group(group)
    plural="s"*(len(members)!=1)
    reporter.report(">>> ", len(members), " segment"+plural )

segmentgroupmenu.addItem(oofmenu.OOFMenuItem(
    "Query_Group",
    cli_only=1,
    callback=_query_sgmt_group,
    params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString),
            SegmentGroupParameter("group", tip="Name of the group.")],
    help="Query a segment group.",
    discussion="<para>Print information about the given &sgmtgroup;.</para>"))

########################################################

# Elements

new = oofmenu.OOFMenuItem(
    "New_Group",
    cli_only=1,
    callback=_new_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    AutomaticNameParameter("name",
                           value=automatic.automatic,
                           resolver=NewGroupNameResolver("elementgroup",
                                                         "elementgroups"),
                           tip="Name for the element group to be created.")),
    help="Create a new element group.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/newelementgroup.xml')
    )
new.data = "elementgroups"
elementgroupmenu.addItem(new)


auto = oofmenu.OOFMenuItem(
    "Auto_Group",
    cli_only=1,
    callback=_auto_group,
    params=[whoville.WhoParameter("skeleton", whoville.getClass("Skeleton"),
                                  tip=parameter.emptyTipString)],
    help="Create element groups for each pixel group.",
    discussion=
"""<para>Automatically create an &elemgroup; in the &skel; for every
&pixelgroup; in the &micro;.  All &elems; whose dominant pixel is in a
&pixelgroup; will be added to a &elemgroup; with the same name as the
&pixelgroup;.  New groups will be created if necessary.</para>"""
    )
auto.data = "elementgroups"
#auto.iterator = skeleton.Skeleton.element_iterator
auto.iterator = cskeleton2.CSkeletonBasePtr.getElements
elementgroupmenu.addItem(auto)
   

rename = oofmenu.OOFMenuItem(
    "Rename_Group",
    cli_only=1,
    callback=_rename_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    ElementGroupParameter("group", tip="Name of the group to be renamed."),
    parameter.StringParameter("new_name", "",
                              tip="New name for the element group")),
    help="Rename an element group.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/renameelementgroup.xml')
    )
rename.data = "elementgroups"
elementgroupmenu.addItem(rename)


copy = oofmenu.OOFMenuItem(
    "Copy_Group",
    cli_only=1,
    callback=_copy_group,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    ElementGroupParameter("group", tip="Name of the group to be copied."),
    AutomaticNameParameter("new_name",
                           resolver=CopyGroupNameResolver("elementgroups"),
                           value=automatic.automatic,
                           tip="Name for the copy.")),
    help="Make a copy of an element group.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/copyelementgroup.xml')
    )
copy.data = "elementgroups"
elementgroupmenu.addItem(copy)


remove = oofmenu.OOFMenuItem(
    "Delete_Group",
    cli_only=1,
    callback=_remove_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    ElementGroupParameter("group", tip="Name of the group.")],
    help="Remove an element group.",
    discussion="""<para>
    Delete the given &elemgroup; from the &skel;. The &elems;
    themselves are not affected.
    </para>""") 
remove.data = "elementgroups"
elementgroupmenu.addItem(remove)


removeall = oofmenu.OOFMenuItem(
    "Delete_All",
    cli_only=1,
    callback=_remove_all_groups,
    params=[
    whoville.WhoParameter('skeleton', whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString)],
    help="Remove all element groups.",
    discussion="""<para>
    Delete all &elemgroups; from the &skel;.
    The &elems; themselves are not affected.
    </para>""")
removeall.data = "elementgroups"
elementgroupmenu.addItem(removeall)


addselect = oofmenu.OOFMenuItem(
    "Add_to_Group",
    cli_only=1,
    callback=_add_selection_to_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    ElementGroupParameter("group", tip="Name of the group.")],
    help="Add selected elements to the group.",
    discussion="""<para>
    Add the currently selected &skel; &elems; to the given &elemgroup;.
    </para>""")
addselect.data = "elementgroups"
elementgroupmenu.addItem(addselect)


removeselect = oofmenu.OOFMenuItem(
    "Remove_from_Group",
    cli_only=1,
    callback=_remove_selection_from_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    ElementGroupParameter("group", tip="Name of the group.")],
    help="Remove selected elements from the group.",
    discussion="""<para>
    Remove the currently selected &skel; &elems; from the given &elemgroup;.
    </para>""")
removeselect.data = "elementgroups"
elementgroupmenu.addItem(removeselect)


clear = oofmenu.OOFMenuItem(
    "Clear_Group",
    cli_only=1,
    callback=_clear_group,
    params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString),
            ElementGroupParameter("group", tip="Name of the group.")],
    help="Clear an element group.",
    discussion="""<para>
    Remove all &elems; from the given &elemgroup;.  The group itself
    will <emphasis>not</emphasis> be deleted, but will be emptied.
    </para>""")
clear.data = "elementgroups"
elementgroupmenu.addItem(clear)

clearall = oofmenu.OOFMenuItem(
    "Clear_All",
    cli_only=1,
    callback=_clear_all_groups,
    params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                  tip=parameter.emptyTipString)],
    help="Clear all element groups.",
    discussion="""<para>
    Remove all &elems; from all &elemgroups;.  The groups themselves will
    <emphasis>not</emphasis> be deleted, but will be emptied.
    </para>""")
clearall.data = "elementgroups"
elementgroupmenu.addItem(clearall)

#=--=##=--=##=--=##=--=#

def _query_elem_group(menuitem, skeleton, group):
    skelc = whoville.getClass('Skeleton')[skeleton]
    # TODO OPT: do the calculations within the element groups class
    # instead of manipulating a large list here.
    members = skelc.elementgroups.get_group(group)
    num = skelc.elementgroups.get_group_size(group)
    size = 0.0
    homog = 0.0
    if num > 0:
        if config.dimension() == 2:
            areaname = "area"
            for element in members:
                size += element.area()
        else:
            areaname = "volume"
            for element in members:
                size += element.volume()
        ms = skelc.getObject().getMicrostructure()
        for element in members:
            homog += element.homogeneity(ms)
        homog /= num
    plural="s"*(num!=1)
    strings = ["Group '%s'" % group,
               "%d element%s" % (num, plural),
               "%s=%s" % (areaname,size),
               "average homogeneity=%g" % homog
    ]

    matl = skelc.elementgroups.getMaterial(group)
    if matl is not None:
        strings.append("material=%s" % matl.name())
    reporter.report(">>>", ", ".join(strings))

elementgroupmenu.addItem(oofmenu.OOFMenuItem(
    "Query_Group",
    cli_only=1,
    callback=_query_elem_group,
    params=[
    whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                          tip=parameter.emptyTipString),
    ElementGroupParameter("group", tip="Name of the group.")],
    help="Query an element group.",
    discussion="<para>Print information about the given &elemgroup;. </para>"))

#=--=##=--=##=--=##=--=#

## TODO 3.1: Restore Assign_Material and Remove_Material, for handling
## materials assigned to element groups.  These operations are
## commented out for now because they have to be implemented in C++.
## In particular, CSkeletonElement::material() needs to be written.
## It will require a way of getting quick access to skeleton groups
## from within C++.  Currently an element can get the names of the
## groups to which it belongs, but not the groups themselves, so it
## can't find out what material has been assigned to the group.

# assignmatl = oofmenu.OOFMenuItem(
#     "Assign_Material",
#     cli_only=1,
#     callback=_assign_matl,
#     params=[
#         whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
#                               tip=parameter.emptyTipString),
#         ElementGroupParameter("group", tip="Name of the group."),
#         materialparameter.BulkMaterialParameter('material')],
#     help="Assign a bulk material to an element group.",
#     discussion=xmlmenudump.loadFile(
#         'DISCUSSIONS/engine/menu/assignelementmat.xml')
# )
# assignmatl.data = "elementgroups"
# elementgroupmenu.addItem(assignmatl)

# removematl = oofmenu.OOFMenuItem(
#     "Remove_Material",
#     cli_only=1,
#     callback=_remove_matl,
#     params=[
#         whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
#                               tip=parameter.emptyTipString),
#         ElementGroupParameter("group", tip="Name of the group.")],
#     help="Remove a bulk material from an element group.",
#     discussion=xmlmenudump.loadFile(
#         'DISCUSSIONS/engine/menu/removeelementmat.xml'))
# removematl.data = "elementgroups"
# elementgroupmenu.addItem(removematl)

#########################################################

# Faces.

if config.dimension() == 3:

    new = oofmenu.OOFMenuItem(
        "New_Group",
        cli_only=1,
        callback=_new_group,
        params=parameter.ParameterGroup(
        whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString),
        AutomaticNameParameter("name",
                               value=automatic.automatic,
                               resolver=NewGroupNameResolver("facegroup",
                                                             "facegroups"),
                               tip="Name of the group.")),
        help="Create a new face group.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/newfacegroup.xml')
        )
    new.data = "facegroups"
    facegroupmenu.addItem(new)


    rename = oofmenu.OOFMenuItem(
        "Rename_Group",
        cli_only=1,
        callback=_rename_group,
        params=parameter.ParameterGroup(
        whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString),
        FaceGroupParameter("group", tip="Name of the group to be renamed."),
        parameter.StringParameter("new_name", "",
                                  tip="New name for the face group")),
        help="Rename a face group.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/renamefacegroup.xml')
        )

    rename.data = "facegroups"

    facegroupmenu.addItem(rename)


    copy = oofmenu.OOFMenuItem(
        "Copy_Group",
        cli_only=1,
        callback=_copy_group,
        params=parameter.ParameterGroup(
        whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString),
        FaceGroupParameter("group", tip="Name of the group to be copied."),
        AutomaticNameParameter("new_name",
                               resolver=CopyGroupNameResolver("facegroups"),
                               value=automatic.automatic,
                               tip="New name for the copy.")),
        help="Copy a face group.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/copyfacegroup.xml')
        )
    copy.data = "facegroups"
    facegroupmenu.addItem(copy)


    remove = oofmenu.OOFMenuItem(
        "Delete_Group",
        cli_only=1,
        callback=_remove_group,
        params=[
        whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString),
        FaceGroupParameter("group", tip="Name of the group.")],
        help="Remove a face group.",
        discussion="""<para>
        Delete the given &sgmtgroup; from the &skel;.  The &sgmts;
        themselves are not affected.
        </para>""")
    remove.data = "facegroups"
    facegroupmenu.addItem(remove)


    removeall = oofmenu.OOFMenuItem(
        "Delete_All",
        cli_only=1,
        callback=_remove_all_groups,
        params=[
        whoville.WhoParameter('skeleton', whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString)],
        help="Remove all face groups.",
        discussion="""<para>
        Delete all &sgmtgroups; from the &skel;.
        The &sgmts; themselves are not affected.
        </para>""")
    removeall.data = "facegroups"
    facegroupmenu.addItem(removeall)


    addselect = oofmenu.OOFMenuItem(
        "Add_to_Group",
        cli_only=1,
        callback=_add_selection_to_group,
        params=[
        whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString),
        FaceGroupParameter("group", tip="Name of the group.")],
        help="Add selected faces to the group.",
        discussion="""<para>
        Add the currently selected &skel; &sgmts; to the given &sgmtgroup;.
        </para>""") 
    addselect.data = "facegroups"
    facegroupmenu.addItem(addselect)


    removeselect = oofmenu.OOFMenuItem(
        "Remove_from_Group",
        cli_only=1,
        callback=_remove_selection_from_group,
        params=[
        whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString),
        FaceGroupParameter("group", tip="Name of the group.")],
        help="Remove selected faces from the group.",
        discussion="""<para>
        Remove the currently selected &skel; &sgmts; from the given &sgmtgroup;.
        </para>""")
    removeselect.data = "facegroups"
    facegroupmenu.addItem(removeselect)


    clear = oofmenu.OOFMenuItem(
        "Clear_Group",
        cli_only=1,
        callback=_clear_group,
        params=[
        whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                              tip=parameter.emptyTipString),
        FaceGroupParameter("group", tip="Name of the group.")],
        help="Clear a face group.",
        discussion="""<para>
        Remove all &sgmts; from the given &sgmtgroup;.  The group itself
        will <emphasis>not</emphasis> be deleted, but will be emptied.
        </para>""")
    clear.data = "facegroups"
    facegroupmenu.addItem(clear)


    clearall = oofmenu.OOFMenuItem(
        "Clear_All",
        cli_only=1,
        callback=_clear_all_groups,
        params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                      tip=parameter.emptyTipString)],
        help="Clear all face groups.",
        discussion="""<para>
        Remove all &sgmts; from all &sgmtgroups;.  The groups themselves will
        <emphasis>not</emphasis> be deleted, but will be emptied.
        </para>""")
    clearall.data = "facegroups"
    facegroupmenu.addItem(clearall)


    def _query_face_group(menuitem, skeleton, group):
        skelc = whoville.getClass('Skeleton')[skeleton]
        members = skelc.facegroups.get_group(group)
        plural="s"*(len(members)!=1)
        reporter.report(">>> ", len(members), " face"+plural,)
        area = 0.
        for face in members:
            area += face.area()
        reporter.report(" area:", area)

    facegroupmenu.addItem(oofmenu.OOFMenuItem(
        "Query_Group",
        cli_only=1,
        callback=_query_face_group,
        params=[whoville.WhoParameter("skeleton", whoville.getClass('Skeleton'),
                                      tip=parameter.emptyTipString),
                FaceGroupParameter("group", tip="Name of the group.")],
        help="Query a face group.",
        discussion="<para>Print information about the given &sgmtgroup;.</para>"))
