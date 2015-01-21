# -*- python -*-
# $RCSfile: skeletonIO.py,v $
# $Revision: 1.76.2.27 $
# $Author: langer $
# $Date: 2014/11/05 16:54:40 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Menu commands for reading a Skeleton from a file.

# TODO 3.1: the name of the Skeleton appears many times in the file, in
# each menu command.  That makes it hard for the user to edit the file
# to change the name.  Ugly solution: have a global "currentskeleton"
# variable which is set by the initial Skeleton.New command.
# Difficult solution: allow variables to be set locally *in* the data
# file, and store the skeleton name there.

# even easier solution: users can just use sed or the find/change
# option in most text editors

## TODO 3.1: Add a progress bar for saving Skeletons.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import cskeletonboundary
from ooflib.SWIG.engine import cskeletonface
from ooflib.SWIG.engine import cskeletonsegment
from ooflib.SWIG.engine import cskeletonselectable
from ooflib.common import debug
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.engine import materialmanager
from ooflib.engine import skeletonboundary
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import materialmenu
import ooflib.common.microstructure
#Interface branch
#from ooflib.engine import skeletonsegment
from ooflib.SWIG.engine import cskeleton2

OOFMenuItem = oofmenu.OOFMenuItem

OOF = mainmenu.OOF

skelmenu = OOF.LoadData.addItem(OOFMenuItem('Skeleton'))

if config.dimension() == 2:
    # The names of the periodicity arguments in 2D have not been
    # changed to x_poeriodicity and y_periodicity to preserve
    # compatibility with old data files.
    def _newSkelPeriodic(menuitem, name, microstructure,
                         left_right_periodicity=False,
                         top_bottom_periodicity=False):
        cskeleton2.newEmptySkeleton(name, microstructure,
                                  left_right_periodicity,
                                  top_bottom_periodicity)
        
    periodicparams = [
        parameter.StringParameter('name', tip="Name for the Skeleton."),
        whoville.WhoParameter(
            'microstructure',
            ooflib.common.microstructure.microStructures,
            tip=parameter.emptyTipString),
        parameter.BooleanParameter(
            'left_right_periodicity',
            tip="Whether the skeleton is periodic in the horizontal direction"),
        parameter.BooleanParameter(
            'top_bottom_periodicity',
            tip="Whether the skeleton is periodic in the vertical direction")]

elif config.dimension() == 3:

    def _newSkelPeriodic(menuitem, name, microstructure,
                         x_periodicity=False,
                         y_periodicity=False,
                         z_periodicity=False):
        cskeleton2.newEmptySkeleton(name, microstructure,
                                  x_periodicity,
                                  y_periodicity,
                                  z_periodicity)

    periodicparams = [
        parameter.StringParameter('name', tip="Name for the Skeleton."),
        whoville.WhoParameter(
            'microstructure',
            ooflib.common.microstructure.microStructures,
            tip=parameter.emptyTipString),
        parameter.BooleanParameter(
            'x_periodicity',
            tip="Whether the skeleton is periodic in the x direction"),
        parameter.BooleanParameter(
            'y_periodicity',
            tip="Whether the skeleton is periodic in the y direction"),
        parameter.BooleanParameter(
            'z_periodicity',
            tip="Whether the skeleton is periodic in the z direction")]


skelmenu.addItem(OOFMenuItem(
    'NewPeriodic',
    callback=_newSkelPeriodic,
    params=periodicparams,
    help="Load Skeleton. Used internally in data files.",
    discussion="<para>Initiate loading a &skel; from a data file.</para>"))

## Optional arguments don't work in binary data files, so for
## backwards compatibility we need a menu item called "New" that
## doesn't take periodicity arguments.

def _newSkelAperiodic(menuitem, name, microstructure):
    ooflib.engine.cskeleton2.newEmptySkeleton(name, microstructure,
                                            False, False)

skelmenu.addItem(OOFMenuItem(
    'New',
    callback=_newSkelAperiodic,
    params=[parameter.StringParameter('name', tip="Name for the Skeleton."),
            whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString)],
    help="Load Skeleton. Used internally in data files.",
    discussion="<para>Initiate loading a &skel; from a data file.</para>"))

###

## The order of the nodes in a Skeleton must not change when the
## Skeleton is saved and reloaded, or the Field values on an
## associated Mesh will be assigned to the wrong nodes. See comment in
## meshIO.py.

def _loadNodes(menuitem, skeleton, points):
##    debug.fmsg()
    # read nodes as (x,y) tuples of floats
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skeleton = skelcontext.getObject()
    for node in points:
        skeleton.addNode(node)
    if config.dimension() == 2:
        skelcontext.updateGroupsAndSelections()
    switchboard.notify(('who changed', 'Skeleton'), skelcontext)

skelmenu.addItem(OOFMenuItem(
    'Nodes',
    callback=_loadNodes,
    params=[whoville.WhoParameter(
                'skeleton', skeletoncontext.skeletonContexts,
                tip=parameter.emptyTipString),
            parameter.ListOfTuplesOfFloatsParameter(
                'points',
                tip="List of points (nodes).")],
    help="Load Nodes. Used internally in data files.",
    discussion="<para>Load "
    "<link linkend='Section-Concepts-Skeleton-Node'>nodes</link>"
    " from a <link linkend='MenuItem-OOF.File.Save.Skeleton'>saved</link>"
    " Skeleton.</para>"
    ))

###

def _loadPartnerships(menuitem, skeleton, partnerlists):
    # Read partners as (i,j,k,l) tuples of int node indices.  Each
    # node in the tuple is a partner of every other node.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skeleton = skelcontext.getObject()
    for nodes in partnerlists:
        nnodes = len(nodes)
        for i in range(nnodes-1):
            for j in range(i+1, nnodes):
                node0 = skeleton.getNode(nodes[i])
                node1 = skeleton.getNode(nodes[j])
                node0.addPartner(node1) # updates partner info for *both* nodes
    skelcontext.updateGroupsAndSelections()
    switchboard.notify(('who changed', 'Skeleton'), skelcontext)

skelmenu.addItem(OOFMenuItem(
    'Partnerships',
    callback=_loadPartnerships,
    params=[whoville.WhoParameter(
                'skeleton', skeletoncontext.skeletonContexts,
                tip=parameter.emptyTipString),
            parameter.ListOfTuplesOfIntsParameter(
                'partnerlists',
                tip="List of tuples containing partner sets.")],
    help="Load Partnerships. Used internally in data files.",
    discussion="<para>Load node partnerships for periodic skeletons from a"
    " <link linkend='MenuItem-OOF.File.Save.Skeleton'>saved</link> Skeleton."
    "</para>"
    ))

###

def _loadElements(menuitem, skeleton, nodes):
##    debug.fmsg()
    # read elements as tuples of node indices
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skeleton = skelcontext.getObject()
    for nodelist in nodes:
        skeleton.loadElement(nodelist)
    # skelcontext.getTimeStamp(None).increment()
    if config.dimension() == 2:
        skelcontext.updateGroupsAndSelections()
    switchboard.notify(('who changed', 'Skeleton'), skelcontext)

skelmenu.addItem(OOFMenuItem(
    'Elements',
    callback=_loadElements,
    params=[whoville.WhoParameter(
                'skeleton', skeletoncontext.skeletonContexts,
                tip=parameter.emptyTipString),
            parameter.ListOfTuplesOfIntsParameter(
                'nodes',
                tip="List of element connectivities (List of node indices).")],
    help="Load Elements. Used internally in data files.",
    discussion="<para>Load <link linkend='Section-Concepts-Skeleton-Element'>"
    "elements</link> from a <link linkend='MenuItem-OOF.File.Save.Skeleton'>"
    "saved</link> Skeleton.</para>"
    ))

###

def _loadPinnedNodes(menuitem, skeleton, nodes):
##    debug.fmsg()
    # "nodes" is a list of integer indices into skeleton.nodes
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skeleton = skelcontext.getObject()
    pinned = skelcontext.pinnednodes
    for i in nodes:
        pinned.pin(skeleton.getNode(i))
        #pinned.pin([skeleton.nodes[i] for i in nodes])
    pinned.signal()

skelmenu.addItem(OOFMenuItem(
        'PinnedNodes',
        callback = _loadPinnedNodes,
        params = [
            whoville.WhoParameter(
                'skeleton', skeletoncontext.skeletonContexts,
                tip=parameter.emptyTipString),
            parameter.ListOfIntsParameter(
                'nodes', tip="List of indices of pinned nodes.")],
        help="Load pinned Nodes. Used internally in data files.",
        discussion="<para>Load <link linkend='MenuItem-OOF.Graphics_n.Toolbox.Pin_Nodes.Pin'>pinned</link> nodes from a &skel; data file.</para>"
    ))

###
    
def _loadPointBoundary(menuitem, skeleton, name, nodes, exterior):
##    debug.fmsg()
    # "nodes" is a list of integer indices into skeleton.nodes
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skeleton = skelcontext.getObject()
    skelcontext.createPointBoundary(name, [skeleton.getNode(i) for i in nodes],
                                    exterior, autoselect=0)
    # autoselect=0 prevents the boundary from being selected in the
    # skelcontext. Selection shouldn't happen except by explicit user
    # action.

skelmenu.addItem(OOFMenuItem(
    'PointBoundary',
    callback=_loadPointBoundary,
    params=[
        whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                              tip=parameter.emptyTipString),
        parameter.StringParameter('name', tip="Name of Point Boundary."),
        parameter.ListOfIntsParameter('nodes', tip="List of node indices."),
        # TODO 3.1: Use BoolParameter. Will have to change test reference files.
        parameter.IntParameter(
            'exterior', 0,
            tip="1 (true) for an exterior boundary and 0 (false) otherwise.")
    ],
    help="Load Point Boundary. Used internally in data files.",
    discussion="<para>Load a <link linkend='Section-Concepts-Skeleton-Boundary-Point'><classname>PointBoundary</classname></link> from a Skeleton data file.</para>"
    ))

###

def _loadEdgeBoundary(menuitem, skeleton, name, edges, exterior):
    # "edges" is a list of pairs of integer indices into skeleton.nodes
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skeleton = skelcontext.getObject()
    seglist = [skeleton.findExistingSegment(*[skeleton.getNode(i) for i in e])
               for e in edges]
    startNode = skeleton.getNode(edges[0][0])
    segSeq = cskeletonsegment.sequenceSegments(seglist, startNode)
    if segSeq:
        # autoselect=0 prevents the boundary from being selected in
        # the skelcontext. Selection shouldn't happen except by
        # explicit user action.
        skelcontext.createEdgeBoundary3D(name, segSeq, exterior, autoselect=0)
#     else:
#         directionlist=[]
#         for i in range(len(edges)):
#             if seglist[i].get_nodes()[0]==skeleton.nodes[edges[i][0]]:
#                 directionlist.append(1)
#             else:
#                 directionlist.append(-1)
#         skelcontext.createNonsequenceableEdgeBoundary(name, seglist,
#                                                       directionlist,
#                                                       exterior, autoselect=0)


    
skelmenu.addItem(OOFMenuItem(
    'EdgeBoundary',
    callback=_loadEdgeBoundary,
    params=[
        whoville.WhoParameter(
            'skeleton', skeletoncontext.skeletonContexts,
            tip=parameter.emptyTipString),
        parameter.StringParameter('name', tip="Name of Edge Boundary."),
        parameter.ListOfTuplesOfIntsParameter(
            'edges', tip="List of Edges -- tuple of two nodes."),
        parameter.IntParameter( # TODO 3.1: Use BoolParameter
            'exterior', 0,
            tip="1 (true) for an exterior boundary and 0 (false) otherwise.")
    ],
    help="Load Edge Boundary. Used internally in data files.",
    discussion="<para>Load a <link linkend='Section-Concepts-Skeleton-Boundary-Edge'><classname>EdgeBoundary</classname></link> from a Skeleton data file.</para>"
    ))


def _loadFaceBoundary(menuitem, skeleton, name, faces, exterior):
    # "faces" is a list of triples of integer indices into skeleton.nodes
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skeleton = skelcontext.getObject()
    facelist = [skeleton.findExistingFace(*[skeleton.getNode(i) for i in f])
                for f in faces]
    # The first face determines the orientation of the whole surface.
    face0 = skeleton.createOrientedFace(
        *[skeleton.getNode(i) for i in faces[0]])
    ofaces = cskeletonface.orientFaces(skeleton, facelist, face0)
    # autoselect=0 prevents the boundary from being selected in the
    # skelcontext. Selection shouldn't happen except by explicit user
    # action.
    skelcontext.createFaceBoundary(name, ofaces, exterior, autoselect=0)

    
skelmenu.addItem(OOFMenuItem(
    'FaceBoundary',
    callback=_loadFaceBoundary,
    params=[
        whoville.WhoParameter(
            'skeleton', skeletoncontext.skeletonContexts,
            tip=parameter.emptyTipString),
        parameter.StringParameter('name', tip="Name of Face Boundary."),
        parameter.ListOfTuplesOfIntsParameter(
            'faces',
            tip="List of Faces -- tuple of two nodes."),
        parameter.IntParameter( # TODO 3.1: Use BoolParameter
            'exterior', 0,
            tip="1 (true) for an exterior boundary and 0 (false) otherwise.")
    ],
    help="Load Face Boundary. Used internally in data files.",
    discussion="<para>Load a <link linkend='Section-Concepts-Skeleton-Boundary-Face'><classname>FaceBoundary</classname></link> from a Skeleton data file.</para>"
        ))



######

def _loadNodeGroup(menuitem, skeleton, name, nodes):
##    debug.fmsg()
    # nodes is a list of integer indices into skeleton.nodes.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skeleton = skelcontext.getObject()
    groupset = skelcontext.nodegroups
    groupset.addGroup(name)
    groupset.addToGroup(**{name : [skeleton.getNode(i) for i in nodes]})

skelmenu.addItem(OOFMenuItem(
        'NodeGroup',
        callback=_loadNodeGroup,
        params=[
            whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                                  tip=parameter.emptyTipString),
            parameter.StringParameter('name', tip="Name for the node group."),
            parameter.ListOfIntsParameter(
                'nodes', tip="List of node indices.")],
        help="Load Node Group. Used internally in data files.",
        discussion="<para>Load a node <link linkend='Section-Concepts-Skeleton-Groups'>group</link>.</para>"
        ))

def _loadElementGroup(menuitem, skeleton, name, elements):
##    debug.fmsg()
    # elements is a list of integer indices into skeleton.elements.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skel = skelcontext.getObject()
    groupset = skelcontext.elementgroups
    groupset.addGroup(name)
    groupset.addToGroup(**{name : [skel.getElement(i) for i in elements]})

skelmenu.addItem(OOFMenuItem(
        'ElementGroup',
        callback=_loadElementGroup,
        params=[
            whoville.WhoParameter(
                'skeleton', skeletoncontext.skeletonContexts,
                tip=parameter.emptyTipString),
            parameter.StringParameter(
                'name', tip="Name for the element group."),
            parameter.ListOfIntsParameter(
                'elements', tip="List of element indices")],
        help="Load Element Group. Used internally in data files.",
        discussion="<para>Load an element <link linkend='Section-Concepts-Skeleton-Groups'>group</link>.</para>"
        ))

def _loadSegmentGroup(menuitem, skeleton, name, segments):
##    debug.fmsg()
    # segments is a list of tuples of integer indices into skeleton.nodes.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skel = skelcontext.getObject()
    groupset = skelcontext.segmentgroups
    groupset.addGroup(name)
    groupset.addToGroup(
        **{name : [skel.getSegmentByNodeIndices(i, j) for (i,j) in segments]})

skelmenu.addItem(OOFMenuItem(
        'SegmentGroup',
        callback=_loadSegmentGroup,
        params=[
            whoville.WhoParameter(
                'skeleton', skeletoncontext.skeletonContexts,
                tip=parameter.emptyTipString),
            parameter.StringParameter(
                'name', tip="Name for the segment group."),
            parameter.ListOfTuplesOfIntsParameter(
                'segments',
                tip="List of segments -- tuple of two node indices.")
            ],
        help="Load Segment Group. Used internally in data files.",
        discussion="<para>Load a segment <link linkend='Section-Concepts-Skeleton-Groups'>group</link>.</para>"
        ))

def _loadFaceGroup(menutiem, skeleton, name, faces):
    # faces is a list of tuples of integer indices into skeleton.nodes.
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skel = skelcontext.getObject()
    groupset = skelcontext.facegroups
    groupset.addGroup(name)
    groupset.addToGroup(
        **{name : [skel.getFaceByNodeIndices(i, j, k) for (i, j, k) in faces]})

skelmenu.addItem(OOFMenuItem(
        'FaceGroup',
        callback=_loadFaceGroup,
        params=[
            whoville.WhoParameter(
                'skeleton', skeletoncontext.skeletonContexts,
                tip=parameter.emptyTipString),
            parameter.StringParameter(
                'name', tip="Name for the face group."),
            parameter.ListOfTuplesOfIntsParameter(
                'faces',
                tip="List of faces -- tuple of three node indices.")
            ],
        help="Load Face Group.  Used internally in data files."))

def _addMaterialToElementGroup(menuitem, skeleton, group, material):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    groupset = skelcontext.elementgroups
    groupset.assignMaterial(group, materialmanager.getMaterial(material))

skelmenu.addItem(OOFMenuItem(
        'AddMaterialToGroup',
        callback=_addMaterialToElementGroup,
        params=[
            whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                                  tip=parameter.emptyTipString),
            parameter.StringParameter('group', tip="Name of the element group"),
            parameter.StringParameter('material', tip="Name of the material.")]
        ))
        
def _loadElementSelection(menuitem, skeleton, elements):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skel = skelcontext.getObject()
    trackerlist = skelcontext.elementselection.currentSelection()
    tracker = trackerlist.selected[skel]
    for elementSource in elements:
      for elementReference in skelcontext.elementselection.get_objects():
	if elementSource == elementReference.getIndex():
	  tracker.add(elementReference)
	  break
    tracker.write()
    switchboard.notify(
        skelcontext.elementselection.mode().changedselectionsignal,
        selection=skelcontext.elementselection)

skelmenu.addItem(OOFMenuItem(
        'ElementSelection',
        callback=_loadElementSelection,
        params=[
            whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                                  tip=parameter.emptyTipString),
            parameter.ListOfIntsParameter(
                'elements', tip="List of element indices.")],
        help="Load Element Selection. Used internally in data files.",
        discussion="<para>Load an element <link linkend='Section-Concepts-Skeleton-Selection'>selection</link>.</para>"
        ))
        
def _loadFaceSelection(menuitem, skeleton, faces):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skel = skelcontext.getObject()
    trackerlist = skelcontext.faceselection.currentSelection()
    tracker = trackerlist.selected[skel]
    for (i, j, k) in faces:
      tracker.add(skel.getFaceByNodeIndices(i, j, k))
    tracker.write()
    switchboard.notify(
        skelcontext.faceselection.mode().changedselectionsignal,
        selection=skelcontext.faceselection)

skelmenu.addItem(OOFMenuItem(
        'FaceSelection',
        callback=_loadFaceSelection,
        params=[
            whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                                  tip=parameter.emptyTipString),
            parameter.ListOfTuplesOfIntsParameter(
                'faces', tip="List of face indices.")],
        help="Load Face Selection. Used internally in data files.",
        discussion="<para>Load a face <link linkend='Section-Concepts-Skeleton-Selection'>selection</link>.</para>"
        ))
        
def _loadSegmentSelection(menuitem, skeleton, segments):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skel = skelcontext.getObject()
    trackerlist = skelcontext.segmentselection.currentSelection()
    tracker = trackerlist.selected[skel]
    for (i, j) in segments:
      tracker.add(skel.getSegmentByNodeIndices(i, j))
    tracker.write()
    switchboard.notify(
        skelcontext.segmentselection.mode().changedselectionsignal,
        selection=skelcontext.segmentselection)

skelmenu.addItem(OOFMenuItem(
        'SegmentSelection',
        callback=_loadSegmentSelection,
        params=[
            whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                                  tip=parameter.emptyTipString),
            parameter.ListOfTuplesOfIntsParameter(
                'segments', tip="List of segment indices.")],
        help="Load Segment Selection. Used internally in data files.",
        discussion="<para>Load a segment <link linkend='Section-Concepts-Skeleton-Selection'>selection</link>.</para>"
        ))
        
def _loadNodeSelection(menuitem, skeleton, nodes):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    skel = skelcontext.getObject()
    trackerlist = skelcontext.nodeselection.currentSelection()
    tracker = trackerlist.selected[skel]
    for nodeSource in nodes:
      for nodeReference in skelcontext.nodeselection.get_objects():
	if nodeSource == nodeReference.getIndex():
	  tracker.add(nodeReference)
	  break
    tracker.write()
    switchboard.notify(
        skelcontext.nodeselection.mode().changedselectionsignal,
        selection=skelcontext.nodeselection)

skelmenu.addItem(OOFMenuItem(
        'NodeSelection',
        callback=_loadNodeSelection,
        params=[
            whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                                  tip=parameter.emptyTipString),
            parameter.ListOfIntsParameter(
                'nodes', tip="List of element nodes.")],
        help="Load Node Selection. Used internally in data files.",
        discussion="<para>Load a node <link linkend='Section-Concepts-Skeleton-Selection'>selection</link>.</para>"
        ))

#############

## TODO 3.1 OPT: Can data be written directly from C++?  

def writeSkeleton(datafile, skelcontext):
    skelcontext.begin_reading()
    try:
        # debug.fmsg()
        skeleton = skelcontext.getObject()
        skelpath = skelcontext.path()

        # Create skeleton.
        datafile.startCmd(skelmenu.NewPeriodic)
        datafile.argument('name', skelcontext.name())
        datafile.argument('microstructure', skeleton.getMicrostructure().name())
        if config.dimension() == 2:
            # The names of the periodicity arguments in 2D have not been
            # changed to x_poeriodicity and y_periodicity to preserve
            # compatibility with old data files.
            datafile.argument('left_right_periodicity',
                              skeleton.getPeriodicity(0))
            datafile.argument('top_bottom_periodicity',
                              skeleton.getPeriodicity(1))
        if config.dimension() == 3:
            datafile.argument('x_periodicity', skeleton.getPeriodicity(0)) 
            datafile.argument('y_periodicity', skeleton.getPeriodicity(1))
            datafile.argument('z_periodicity', skeleton.getPeriodicity(2))
        datafile.endCmd()

        # debug.fmsg("nodes")
        # Define nodes.
        datafile.startCmd(skelmenu.Nodes)
        datafile.argument('skeleton', skelpath)
        if config.dimension()==2:
            datafile.argument('points', [(nd.position().x, nd.position().y)
                                         for nd in skeleton.nodes])
        elif config.dimension()==3:
            datafile.argument(
                'points',
                [tuple(node.position()) for node in skeleton.getNodes()])
        datafile.endCmd()

        # Nodes are written and read in the order in which they're stored
        # in the Skeleton's nodes list.  This is not the same as the
        # nodes' internal index, so we need to create a dictionary of
        # indices in the nodes list so that the elements' node tuples are
        # correct.
#         nodedict = {}
#         c = 0
#         for node in skeleton.nodes:
#             nodedict[node] = c
#             c += 1
#         # same for elements
#         elementdict = {}
#         c = 0
#         for element in skeleton.elements:
#             elementdict[element] = c
#             c += 1

        # Write node partnerships using the node indices in nodedict
#         if skeleton.x_periodicity or skeleton.y_periodicity \
#                or (config.dimension()==3 and skeleton.z_periodicity):
#             partners = []
# #            for node in skeleton.nodes:
#             for i in range(skeleton.nnodes()):
#                 node = skeleton.getNode(i)
#                 #nodeno = nodedict[node]
#                 partnernos = [nodedict[n] for n in node.getPartners()]
#                 # Only save nontrivial partnerships, and only save
#                 # each set of partners once.  Partnerships are saved
#                 # as a tuple of node indices.  Order is unimportant.
#                 if partnernos and nodeno < min(partnernos):
#                     partners.append(tuple([nodeno] + partnernos))
#             datafile.startCmd(skelmenu.Partnerships)
#             datafile.argument('skeleton', skelpath)
#             datafile.argument('partnerlists', partners)
#             datafile.endCmd()

        # Define elements, using the node indices
        # debug.fmsg("elements")
        datafile.startCmd(skelmenu.Elements)
        datafile.argument('skeleton', skelpath)
        datafile.argument('nodes',
                          [tuple(node.getIndex() for node in element.getNodes())
                           for element in skeleton.getElements()])
        datafile.endCmd()


        # Node groups
        # debug.fmsg("node groups")
        for group in skelcontext.nodegroups.groups:
            datafile.startCmd(skelmenu.NodeGroup)
            datafile.argument('skeleton', skelpath)
            datafile.argument('name', group)
            datafile.argument(
                'nodes', 
                [node.getIndex()
                 for node in skelcontext.nodegroups.get_group(group)])
            datafile.endCmd()

        # Element groups
        # debug.fmsg("element groups")
        for group in skelcontext.elementgroups.groups:
            datafile.startCmd(skelmenu.ElementGroup)
            datafile.argument('skeleton', skelpath)
            datafile.argument('name', group)
            datafile.argument(
                'elements',
                [el.getIndex()
                 for el in skelcontext.elementgroups.get_group(group)])
            datafile.endCmd()

        # debug.fmsg("segment groups")
        for group in skelcontext.segmentgroups.groups:
            datafile.startCmd(skelmenu.SegmentGroup)
            datafile.argument('skeleton', skelpath)
            datafile.argument('name', group)
            segs = [tuple(n.getIndex() for n in seg.getNodes())
                     for seg in skelcontext.segmentgroups.get_group(group)]
            datafile.argument('segments', segs)
            datafile.endCmd()

        # debug.fmsg("face groups")
        for group in skelcontext.facegroups.groups:
            datafile.startCmd(skelmenu.FaceGroup)
            datafile.argument('skeleton', skelpath)
            datafile.argument('name', group)
            faces = [tuple(n.getIndex() for n in face.getNodes())
                     for face in skelcontext.facegroups.get_group(group)]
            datafile.argument('faces', faces)
            datafile.endCmd()

        # Materials assigned to Element Groups.  If a Material
        # isn't assigned to pixels in the Microstructure, be sure
        # to save the Material's definition first.
        # debug.fmsg("materials")
        msmatls = ooflib.SWIG.engine.material.getMaterials(
            skeleton.getMicrostructure())
        groupmats = skelcontext.elementgroups.getAllMaterials()
        # skelmatls is a list of Materials used in the Skeleton
        # that aren't in the Microstructure.
        skelmatls = [m for (g, m) in groupmats if m not in msmatls]
        # Construct a list of Properties already defined in the
        # data file, so that they're not written twice.
        excludeProps = {}
        for mat in msmatls:
            for prop in mat.properties():
                excludeProps[prop.registration().name()] = prop
        materialmenu.writeMaterials(datafile, skelmatls, excludeProps)
        # Now assign Materials to Groups.
        for group, material in groupmats:
            datafile.startCmd(skelmenu.AddMaterialToGroup)
            datafile.argument('skeleton', skelpath)
            datafile.argument('group', group)
            datafile.argument('material', material.name())
            datafile.endCmd()

        # Pinned nodes
        datafile.startCmd(skelmenu.PinnedNodes)
        datafile.argument('skeleton', skelpath)
        datafile.argument(
            'nodes', 
            [node.getIndex() for node in skelcontext.pinnednodes.retrieve()])
        datafile.endCmd()

        # debug.fmsg("boundaries")
        # Point boundaries
        # sort keys to print in a consistent order
        pointboundaries = skeleton.getPointBoundaries()
        sortedKeys = pointboundaries.keys()
        sortedKeys.sort()
        #for pbname, pbdy in skeleton.pointboundaries.items():
        for pbname in sortedKeys:
            pbdy = pointboundaries[pbname]
            datafile.startCmd(skelmenu.PointBoundary)
            datafile.argument('skeleton', skelpath)
            datafile.argument('name', pbname)
            datafile.argument('nodes',
                              [node.getIndex() for node in pbdy.getNodes()])
            exterior = 0
            if isinstance(pbdy,
                          cskeletonboundary.ExteriorCSkeletonPointBoundaryPtr):
                exterior = 1
            datafile.argument('exterior', exterior)
            datafile.endCmd()

        # Edge boundaries
        # sort keys to print in a consistent order
        edgeboundaries = skeleton.getEdgeBoundaries()
        sortedKeys = edgeboundaries.keys()
        sortedKeys.sort()
        # for ebname, ebdy in skeleton.edgeboundaries.items():
        for ebname in sortedKeys:
            ebdy = edgeboundaries[ebname]
            datafile.startCmd(skelmenu.EdgeBoundary)
            datafile.argument('skeleton', skelpath)
            datafile.argument('name', ebname)
#             #Interface branch
#             if ebdy._sequenceable==1:
#                 edgeset = rearrangeEdges([
#                     tuple([nodedict[x] for x in edge.get_nodes()])
#                     for edge in ebdy.edges
#                     ])
#             else:
            edgeset = [
                tuple(edge.getNode(i).getIndex() for i in (0,1))
                for edge in ebdy.getOrientedSegments()
                ]
            datafile.argument('edges', edgeset)
            exterior = 0
            if isinstance(ebdy,
                          cskeletonboundary.ExteriorCSkeletonEdgeBoundaryPtr):
                exterior = 1
            datafile.argument('exterior', exterior)
            datafile.endCmd()

#             #Interface branch
#             interfacematname=skelcontext.getBoundary(ebname)._interfacematerial
#             if interfacematname is not None:
#                 datafile.startCmd(OOF.LoadData.Material.Interface.Assign)
#                 datafile.argument('microstructure',skeleton.getMicrostructure().name())
#                 datafile.argument('material',interfacematname)
#                 datafile.argument('interfaces',[skelcontext.name()+":"+ebname])
#                 datafile.endCmd()

        # Face boundaries
        # sort keys to print in a consistent order
        # debug.fmsg("face boundaries")
        faceboundaries = skeleton.getFaceBoundaries()
        # debug.fmsg("got faceboundaries")
        sortedKeys = faceboundaries.keys()
        sortedKeys.sort()
        # for ebname, ebdy in skeleton.faceboundaries.items():
        for fbname in sortedKeys:
            # debug.fmsg("fbname=", fbname)
            fbdy = faceboundaries[fbname]
            datafile.startCmd(skelmenu.FaceBoundary)
            datafile.argument('skeleton', skelpath)
            datafile.argument('name', fbname)
            faceset = [
                tuple(face.getNode(i).getIndex() for i in range(3))
                for face in fbdy.getFaces()
                    ]
            # debug.fmsg("got faceset")
            faceset.sort()
            datafile.argument('faces', faceset)
            exterior = 0
            if isinstance(fbdy,
                          cskeletonboundary.ExteriorCSkeletonFaceBoundaryPtr):
                exterior = 1
            datafile.argument('exterior', exterior)
            datafile.endCmd()

	# debug.fmsg("selections")
	# Element selection
	datafile.startCmd(skelmenu.ElementSelection)
        datafile.argument('skeleton', skelpath)
        datafile.argument(
	    'elements',
	    [el.getIndex()
	      for el in skelcontext.elementselection.retrieve()])
	datafile.endCmd()
	
	# Face selection
	datafile.startCmd(skelmenu.FaceSelection)
        datafile.argument('skeleton', skelpath)
	fas =  [tuple(n.getIndex() for n in fa.getNodes())
	      for fa in skelcontext.faceselection.retrieve()]
        datafile.argument('faces', fas)
	datafile.endCmd()
	
	# Segment selection
	datafile.startCmd(skelmenu.SegmentSelection)
        datafile.argument('skeleton', skelpath)
	segs =  [tuple(n.getIndex() for n in se.getNodes())
	      for se in skelcontext.segmentselection.retrieve()]
        datafile.argument('segments', segs)
	datafile.endCmd()
	
	# Node selection
	datafile.startCmd(skelmenu.NodeSelection)
        datafile.argument('skeleton', skelpath)
        datafile.argument(
	    'nodes',
	    [no.getIndex()
	      for no in skelcontext.nodeselection.retrieve()])
	datafile.endCmd()

    finally:
        # debug.fmsg("done")
        skelcontext.end_reading()

###########################################################

# A function to put edges in a right order.  Used only in abaqus output.
def rearrangeEdges(edges):
    # 'edges' is a list of tuples of integers.  Each tuple is an edge,
    # and each integer is a node index (from nodedict in
    # writeSkeleton, above).
    if len(edges) == 1:
        return edges

    # Construct dictionaries of edges keyed by their starting and end points.
    tails = {}           
    heads = {}         
    for edge in edges:
        heads[edge[0]] = edge
        tails[edge[1]] = edge

    newedges = [edges[0]]

    # Build the list of contiguous edges going backwards from the
    # start point of edges[0].  This loop exits when either it runs
    # out of tails and throws a key error, or when it loops back on
    # itself and the conditional fails.
    lastpt = edges[0][0]
    try:
        while tails[lastpt] not in newedges:
            next = tails[lastpt]
            newedges.append(next)
            lastpt = next[0]

    except KeyError:
        pass

    newedges.reverse()

    # Extend the list of contiguous edges going forwards from the end
    # point of edges[0].  If the previous block found a loop, then
    # this block's while-conditional will fail, and it will do
    # nothing.
    lastpt = edges[0][1]
    try:
        while heads[lastpt] not in newedges:
            next = heads[lastpt]
            newedges.append(next)
            lastpt = next[1]
    except KeyError:
        pass

    return newedges


#TODO 3.1: Needs update in general, for new storage in C++ and interfaces
##########
# ABAQUS #
##########
import datetime
import string
def writeABAQUSfromSkeleton(filename, mode, skelcontext):
    skelcontext.begin_reading()
    try:
        skeleton = skelcontext.getObject()

        buffer="*HEADING\nABAQUS-style file created by OOF2 on %s from a skeleton " % (datetime.datetime.today())
        buffer+="of the microstructure %s.\n" % skeleton.getMicrostructure().name()

        # Build dictionary (instead of using index()) for elements and nodes
        #  as was done in previous writeXXX() methods
        nodedict = {}
        i = 1
        for node in skeleton.nodes:
            nodedict[node] = i
            i += 1
        # same for elements
        elementdict = {}
        i = 1
        for el in skeleton.elements:
            elementdict[el] = i
            i += 1

        # Collect elements with the same dominant material together in a
        #  dictionary, with a key given by the material name.
        #  Some elements may not have a material assigned and
        #  these should not be included in the dictionary(?). Have a feeling
        #  something like this has been done in the OOF universe.
        materiallist={}
        elementlist={}
        for el in skeleton.elements:
            matl = el.material(skeleton)
            if matl:
                matname = matl.name()
                elindex = elementdict[el]
                try:
                    elementlist[matname].append(elindex)
                except KeyError:
                    elementlist[matname] = [elindex]
                    materiallist[matname] = matl

        buffer+="** Materials defined by OOF2:\n"
        for matname, details in materiallist.items():
            buffer+="**   %s:\n" % (matname)
            for prop in details.properties():
                for param in prop.registration().params:
                    buffer+="**     %s: %s\n" % (param.name,param.value)

        buffer+="** Notes:\n**   The nodes for a skeleton are always located at vertices or corners.\n"
        buffer+="**   More information may be obtained by saving ABAQUS from a mesh.\n"

        listbuf=["*NODE\n"]
        for node in skeleton.nodes:
            listbuf.append("%d, %s, %s\n" % (nodedict[node],node.position().x,node.position().y))
        buffer+=string.join(listbuf,"")

        # Only expecting 3 or 4 noded skeleton elements
        for numnodes in [3,4]:
            listbuf=["** The element type provided for ABAQUS is only a guess " \
                     "and may have to be modified by the user to be meaningful.\n*ELEMENT, TYPE=CPS%d\n" % numnodes]
            for el in skeleton.elements:
                if el.nnodes()==numnodes:
                    listbuf2=["%d" % (elementdict[el])]
                    for node in el.nodes:
                        listbuf2.append("%d" % (nodedict[node]))
                    listbuf.append(string.join(listbuf2,", ")+"\n")
            if len(listbuf)>1:
                buffer+=string.join(listbuf,"")

        for group in skelcontext.nodegroups.groups:
            buffer+="*NSET, NSET=%s\n" % (group)
            listbuf=[]
            i=0
            for node in skelcontext.nodegroups.get_group(group):
                if i>0 and i%16==0:
                    listbuf.append("\n%d" % (nodedict[node]))
                else:
                    listbuf.append("%d" % (nodedict[node]))
                i+=1
            buffer+=string.join(listbuf,", ")+"\n"

        for elgroup in skelcontext.elementgroups.groups:
            buffer+="*ELSET, ELSET=%s\n" % (elgroup)
            listbuf=[]
            i=0
            for el in skelcontext.elementgroups.get_group(elgroup):
                if i>0 and i%16==0:
                    listbuf.append("\n%d" % (elementdict[el]))
                else:
                    listbuf.append("%d" % (elementdict[el]))
                i+=1
            buffer+=string.join(listbuf,", ")+"\n"

        buffer+="** Include point and edge boundaries from OOF2.\n"
        for pbname, pbdy in skeleton.pointboundaries.items():
            buffer+="*NSET, NSET=%s\n" % (pbname)
            listbuf=[]
            i=0
            for node in pbdy.nodes:
                if i>0 and i%16==0:
                    listbuf.append("\n%d" % (nodedict[node]))
                else:
                    listbuf.append("%d" % (nodedict[node]))
                i+=1
            buffer+=string.join(listbuf,", ")+"\n"

        # Use rearrangeEdges() to chain the edges together, then pick the
        #  unique nodes. It seems the edges can't be selected if they
        #  are empty, so edgeset=[(a,b),(b,c),...] is not checked
        #  for null content
        for ebname, ebdy in skeleton.edgeboundaries.items():
            edgeset = rearrangeEdges([
                tuple(nodedict[node] for node in edge.get_nodes())
                for edge in ebdy.edges
                ])
            buffer+="*NSET, NSET=%s\n" % (ebname)
            listbuf=["%d" % edgeset[0][0]]
            i=1
            for edge in edgeset:
                if i%16==0:
                    listbuf.append("\n%d" % (edge[1]))
                else:
                    listbuf.append("%d" % (edge[1]))
                i+=1
            buffer+=string.join(listbuf,", ")+"\n"

        for matname in materiallist:
            buffer+="*ELSET, ELSET=%s\n" % matname
            listbuf=[]
            i=0
            for elindex in elementlist[matname]:
                if i>0 and i%16==0:
                    listbuf.append("\n%d" % (elindex))
                else:
                    listbuf.append("%d" % (elindex))
                i+=1
            buffer += (string.join(listbuf,", ") + 
                       "\n*SOLID SECTION, ELSET=%s, MATERIAL=%s\n"
                       % (matname,matname))

        for matname in materiallist:
            buffer+="*MATERIAL, NAME=%s\n** Use the information in the header to complete these fields under MATERIAL\n" % matname

        # Save/Commit to file. Perhaps should be done outside the
        # current method.
        fp=open(filename,mode)
        fp.write(buffer)
        fp.close()
    finally:
        skelcontext.end_reading()
