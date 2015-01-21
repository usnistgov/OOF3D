# -*- python -*-
# $RCSfile: skeletonIPC.py,v $
# $Revision: 1.58.12.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:20 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import math, sys
from ooflib.common import debug
from ooflib.common import microstructure
from ooflib.common import object_id
from ooflib.common import primitives
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import binarydata
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import socket2me
from ooflib.common.IO import whoville
from ooflib.engine import skeleton
from ooflib.engine import skeletonboundary
from ooflib.engine import skeletoncontext
from ooflib.engine import skeletonmodifier
from ooflib.engine import skeletonsegment
from ooflib.engine import skeletonselectionmod
from ooflib.engine.IO import skeletonIO
from ooflib.engine.IO import skeletonmenu
from ooflib.SWIG.common import mpitools
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common import labeltree
from ooflib.SWIG.common import pixelgroup
import string

WhoParameter = whoville.WhoParameter
microStructures = microstructure.microStructures
RegisteredParameter = parameter.RegisteredParameter
IntParameter = parameter.IntParameter
StringParameter = parameter.StringParameter
AutomaticNameParameter = parameter.AutomaticNameParameter
microStructures = microstructure.microStructures
SkeletonModifier = skeletonmodifier.SkeletonModifier

## General definitions
#RCL: OOF does not seem to be referenced in this file
OOF = mainmenu.OOF
_rank = mpitools.Rank()
_size = mpitools.Size()

## OOF.LoadData.IPC.Skeleton
smenu = parallelmainmenu.ipcmenu.addItem(oofmenu.OOFMenuItem('Skeleton', secret=1, no_log=1))

# OOF.LoadData.IPC.Skeleton.Initialize
def _parallel_init(menuitem, name, microstructure, x_elements, y_elements,
                   skeleton_geometry):
    initializer = InitializeSkeletonParallel(name, microstructure,
                                             x_elements, y_elements,
                                             skeleton_geometry)
    skel = initializer.create()
##    if _rank == 0:
##        initializer.report_skeleton()
    mpitools.Barrier()

    mscontext = microStructures[microstructure]
    import ooflib.engine.skeletoncontext
    skeletoncontext.skeletonContexts.add([microstructure, name], skel, parent=mscontext)

smenu.addItem(oofmenu.OOFMenuItem(
    'Initialize',
    callback = _parallel_init,
    secret=1,
    no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = parameter.ParameterGroup(
    AutomaticNameParameter('name',
                           value=automatic.automatic,
                           resolver=skeletonmenu.skeletonNameResolver,
                           tip="Name of the new skeleton."),
    StringParameter('microstructure'),
    IntParameter('x_elements', 4, tip="No. of elements in the x-direction."),
    IntParameter('y_elements', 4, tip="No. of elements in the y-direction."),
    RegisteredParameter('skeleton_geometry', skeleton.SkeletonGeometry,
                        skeleton.QuadSkeleton())
    )
    ))


class InitializeSkeletonParallel:
    def __init__(self, skelname, msname, nx, ny, geometry):
        self.skelname = skelname
        self.msname = msname
        self.nx = nx
        self.ny = ny
        self.geometry = geometry
        self.dummy = None
        self.skeleton = None

    def create(self):
        MS = microStructures[self.msname].getObject()
        self.dummy = self.geometry(self.nx, self.ny, MS)
        self.partition_skeleton()
        return self.skeleton

    def partition_skeleton(self):
        self.mark_dummy()  # preliminary marking
        self.partition_dummy()  # partitioned
        self.create_skeleton()

    def mark_dummy(self):
        global _size
        width  = self.dummy.MS.size()[0]*1.0
        height = self.dummy.MS.size()[1]*1.0

        # Portrait or Landscape?
        landscape = True
        if width < height:
            landscape = False

        # The easiest one 1xN or Nx1
        if landscape:
            if math.ceil(width/height) >= _size:
                ix = _size
                iy = 1
            else:
                ix = int(math.ceil(math.sqrt(_size)))
                iy = int(math.floor(math.sqrt(_size)))
                if ix*iy < _size:
                    iy += 1
        else:  # portrait
            if math.ceil(height/width) >= _size:
                ix = 1
                iy = _size
            else:
                ix = int(math.floor(math.sqrt(_size)))
                iy = int(math.ceil(math.sqrt(_size)))
                if ix*iy < _size:
                    ix += 1 
            
        hx = width/ix
        hy = height/iy

        # Bounding box
        class BBox:
            def __init__(self, ll, ur):  # ll = (x0, y0), ur = (x1, y1)
                self.lowerLeft = ll
                self.upperRight = ur
                self.index = None
            def set_index(self, id):
                self.index = id

        bboxes = []
        for j in range(iy):
            for i in range(ix):
                bboxes.append( BBox((i*hx,j*hy), ((i+1)*hx,(j+1)*hy)) )
        count = 0
        for id in range(_size-1,-1, -1):
            if id==_rank:
                #RCL:Store the bounds of the subdomain of this process
                self.localbounds=primitives.Rectangle(primitives.Point(bboxes[count].lowerLeft[0],bboxes[count].lowerLeft[1]),
                                                      primitives.Point(bboxes[count].upperRight[0],bboxes[count].upperRight[1]))
            bboxes[count].set_index(id)
            count += 1
        bboxes[count-1].upperRight = bboxes[-1].upperRight  # extension
        bboxes = bboxes[:count]  # removal of dummy bboxes

        # Now, iterate over the boxes and mark elements
        # Check to see if the center of an element is in the box or not.
        for e in self.dummy.element_iterator():
            for bbox in bboxes:
                if(e.belongTo(bbox)):
                    e.resetProcID(bbox.index)
        
    def partition_dummy(self):
        # Separating nodes and at the same time
        # create a dict to store procIDs and
        # the corresponding indices for nodes.
        global _size
        self.nodePartitions = [[] for i in range(_size)]
        self.indexMap = {}  # (procID, initial index): remore index
        indicator = [0]*_size
        for nd in self.dummy.node_iterator():
            owners = nd.owners()
            for owner in owners:
                self.nodePartitions[owner].append(nd)
                # index dict
                #for i in range(_size):
                #    if owner == i:
                #        self.indexMap[(i, nd.getIndex())] = indicator[i]
                #        indicator[i] += 1
                #RCL: Loop seems unnecessary. indicator gives a "local" index of the node within the process
                self.indexMap[(owner, nd.getIndex())] = indicator[owner]
                indicator[owner] += 1

        # Separating elems
        self.elemPartitions = [[] for i in range(_size)]
        for el in self.dummy.element_iterator():
            self.elemPartitions[el.procID()].append(el)
        
    def create_skeleton(self):
        global _rank
        # create an empty Skeleton
        MS = microStructures[self.msname].getObject()
        self.skeleton = skeleton.Skeleton(MS)
        #RCL:Store the bounds of the subdomain of this process
        self.skeleton.localbounds=self.localbounds
        # create nodes
        for nd in self.nodePartitions[_rank]:
            node = self.skeleton.newNode(nd.position()[0], nd.position()[1])
            for owner in nd.owners():
                if owner != _rank:
                    node.sharesWith(owner,
                                    self.indexMap[(owner, nd.getIndex())])
        # create elements
        for el in self.elemPartitions[_rank]:
            nodes = []
            for n in el.nodes:
                nodes.append(self.skeleton.getNodeWithIndex(
                    self.indexMap[(_rank, n.getIndex())]))
            element = self.skeleton.newElement(nodes)
        # take care of boundaries
        self.set_boundaries()
        # Proc#0 collects minimal data from others for displaying
        mpitools.Barrier()
        self.collect_pieces()

    def set_boundaries(self):
        global _rank
        # point boundaries
        pbInfo = {'names':[], 'nodes':[], 'exterior':[]}
        for pbname, pb in self.dummy.pointboundaries.items():
            nodes = []
            for nd in pb.nodes:
                if _rank in nd.owners():
                    nodes.append(self.indexMap[(_rank, nd.getIndex())])
            #if nodes:  # something in it
            if 1: #RCL: admit boundaries without any nodes touching them.
                pbInfo['names'].append(pbname)
                pbInfo['nodes'].append(nodes)
                pbInfo['exterior'].append(pb.exterior())

        # edge boundaries
        ebInfo = {'names':[], 'edges':[], 'exterior':[]}
        for ebname, eb in self.dummy.edgeboundaries.items():
            edges = []
            for ed in eb.edges:
                nd0, nd1 = ed.get_nodes()
                if _rank in nd0.owners() and _rank in nd1.owners():
                    edges.append([self.indexMap[(_rank, nd0.getIndex())],
                                  self.indexMap[(_rank, nd1.getIndex())]])
            #if edges:  # something in it
            if 1: #RCL: admit boundaries without any nodes touching them.
                ebInfo['names'].append(ebname)
                ebInfo['edges'].append(edges)
                ebInfo['exterior'].append(eb.exterior())

        # point boundaries
        for name, nodes, exterior in zip(pbInfo['names'],
                                         pbInfo['nodes'],
                                         pbInfo['exterior']):
            pb = self.skeleton.getPointBoundary(name, exterior=exterior)
            for nd in nodes:
                pb.addNode(self.skeleton.getNodeWithIndex(nd))
        # edge boundaries
        for name, edges, exterior in zip(ebInfo['names'],
                                         ebInfo['edges'],
                                         ebInfo['exterior']):
            eb = self.skeleton.getEdgeBoundary(name, exterior=exterior)
            for ed in edges:
                seg = self.skeleton.findSegment(
                    self.skeleton.getNodeWithIndex(ed[0]),
                    self.skeleton.getNodeWithIndex(ed[1]))
                direction = (seg.nodeIndices() == ed)
                edge = skeletonsegment.SkeletonEdge(seg, direction=direction)
                eb.addEdge(edge)

    def collect_pieces(self):
        if _rank == 0:
            all = {"nodes":[], "elements":[]}
            all["nodes"] = [[(n.position()[0], n.position()[1])
                             for n in nodes]
                            for nodes in self.nodePartitions]
            all["elements"] = [[[self.indexMap[(i, n.getIndex())] for n in el.nodes]
                                for el in self.elemPartitions[i]]
                               for i in range(_size)]
            self.skeleton.all_skeletons = all
        #RCL:
        self.skeleton.maxnnodes=max([len(nodes) for nodes in self.nodePartitions])
            
    def report_skeleton(self):
        debug.fmsg("#NODES")
        for nd in self.skeleton.node_iterator():
            debug.fmsg("Node #", nd.getIndex(),
                       nd.position(), nd._remote_index)
        debug.fmsg("#ELEMENTS")
        for el in self.skeleton.element_iterator():
            debug.fmsg("Element #", el.getIndex(),
                       [n.getIndex() for n in el.nodes])

####################

# A function to collect partitioned skeleton -- not to be used in the end
def collect_pieces(skel):
    global _rank
    global _size
    # Gather minimal info for element polygons (to display Skeleton at #0)
    # Only the #0 will store the gathered information.
    # no. of nodes & no. of elements
    nnodes = mpitools.Allgather_Int(skel.nnodes())
    #RCL: Use maxnnodes as base offset for the indices of non-corner mesh nodes
    skel.maxnnodes = max(nnodes)
    nelems = mpitools.Allgather_Int(skel.nelements())
    myCoords = list(
        reduce(
        lambda x,y: x+y, [(skel.nodePosition(nd)[0],
                           skel.nodePosition(nd)[1])
                          for nd in skel.node_iterator()]
        ))

    coordSizes = [i*2 for i in nnodes]
    allCoords = mpitools.Allgather_DoubleVec(myCoords,
                                             size_known=coordSizes)
    # allCoords = [[(x0,y0),(x1,y1), ...], [...], ...]
    allCoords = [ [(allCoords[i][2*j],allCoords[i][2*j+1])
                   for j in range(nnodes[i])]
                  for i in range(_size) ]
    # element connectivity signature
    myEConSigs = [el.nnodes() for el in skel.element_iterator()]
    allEConSigs = mpitools.Allgather_IntVec(myEConSigs, size_known=nelems)
    # element connectivity
    myECons = [ [skel.node_index_dict[nd.getIndex()] for nd in el.nodes]
                for el in skel.element_iterator()]
    myECons = reduce(lambda x,y: x+y, myECons)
    conSizes = [reduce(lambda x,y: x+y, aECS) for aECS in allEConSigs]
    temp = mpitools.Allgather_IntVec(myECons, size_known=conSizes)

    def listrize(list, signature):
        nsig = len(signature)
        count = 0
        output = [[] for i in range(nsig)]
        for i in range(nsig):
            for j in range(signature[i]):
                output[i].append(list[count])
                count += 1
        return output

    allECons = [listrize(temp[i], allEConSigs[i]) for i in range(_size)]
    if _rank == 0:
        skel.all_skeletons = {"nodes": allCoords,
                              "elements": allECons}
            
####################

def _modify(menuitem, skeleton, modifier):
    global _rank

    if _rank == 0:
        ModifyProgressBar = menuitem.getProgressBar(
            modifier.get_progressbar_type())
        
    context = skeletoncontext.skeletonContexts[skeleton]
    context.reserve()
    try:
        context.begin_writing()
        try:
            if _rank == 0:
                reporter.start_progressbar()

            skel = modifier.apply_parallel(context.getObject(), context)

            if _rank == 0:
                reporter.progressbar_completed()
                reporter.end_progressbar()

            # skel is None whenever the modifier fails
            # or is interrupted from finishing its task
            if skel is None:
                reporter.warn("Modify Process Interrupted")
                # return will force all the finally's to be executed
                return

            mpitools.Barrier()
            context.pushModification(skel)
            skel.needsHash()
        finally:
            context.end_writing()

        if _rank == 0:
            reporter.start_progressbar()

        mpitools.Barrier()
        modifier.postProcess_parallel(context)

        if _rank == 0:
            reporter.progressbar_completed()
            reporter.end_progressbar()
            
        # If the skeleton is modified in postProcess, use
        # begin/end_writing inside the function call to guarantee
        # that no dead-locking occurs because of possible switchboard
        # calls to READ or REDRAW that may make use of
        # begin/end_reading(). See anneal.py for an example.
    finally:
        # guarantee that the reservation is cancelled even if an
        # exception is raised
        context.cancel_reservation()

        if _rank == 0:
            if ModifyProgressBar.query_stop() or \
                   ModifyProgressBar.get_success()<0:
                ModifyProgressBar.set_failure()
                ModifyProgressBar.set_message("Failed")
                return
            else:
                ModifyProgressBar.set_success()
                ModifyProgressBar.set_message("Succeeded")

        switchboard.notify('redraw')
        switchboard.notify('Skeleton modified', skeleton, modifier)

smenu.addItem(
    oofmenu.OOFMenuItem('Modify',
                        callback = _modify,
                        secret=1,
                        no_log=1,
                        threadable = oofmenu.PARALLEL_THREADABLE,
                        params = [StringParameter('skeleton'),
                                  RegisteredParameter('modifier', SkeletonModifier)]
                        ))

def _undo_skeleton(menuitem, skeleton):
    global _rank
    if _rank == 0:
        return

    from ooflib.engine import skeletoncontext
    skeletonwho = skeletoncontext.skeletonContexts[skeleton]
    if skeletonwho.undoable():
        skeletonwho.begin_writing()
        try:
            skeletonwho.undoModification()            
        finally:
            skeletonwho.end_writing()

smenu.addItem(
    oofmenu.OOFMenuItem(
    'Undo',
    callback=_undo_skeleton,
    secret=1,
    no_log=1,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[StringParameter('skeleton')]
    ))

def _redo_skeleton(menuitem, skeleton):
    global _rank
    if _rank == 0:
        return
    
    from ooflib.engine import skeletoncontext
    skeletonwho = skeletoncontext.skeletonContexts[skeleton]
    if skeletonwho.redoable():
        skeletonwho.begin_writing()
        try:
            skeletonwho.redoModification()
        finally:
            skeletonwho.end_writing()

smenu.addItem(
    oofmenu.OOFMenuItem(
    'Redo',
    callback=_redo_skeleton,
    secret=1,
    no_log=1,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[StringParameter('skeleton')]
    ))


#########################

#TODO OPT: Look closely to skeletonmenu _skeleton_delete. We have to clear the selections also.
# When enabling the parallel version. Make sure that the clear is done properly or  a symptome
# might be some unclean layers. Canvas still displaying objects that are gone.
def _skeleton_delete_parallel(menuitem, skeleton):
    skeletoncontext.skeletonContexts[skeleton].lockAndDelete()


smenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=_skeleton_delete_parallel,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                         tip=parameter.emptyTipString)]
    ))


#########################

def _skeleton_copy_parallel(menuitem, skeleton, name):
    # skeleton is a colon separated string
    oldskelpath = labeltree.makePath(skeleton)
    oldskelcontext = skeletoncontext.skeletonContexts[skeleton]
    if name is automatic.automatic:
        nm = skeletoncontext.skeletonContexts.uniqueName(skeleton)
    else:
        nm = name
        
    orig = oldskelcontext.getObject()
    newskel = orig.properCopy(fresh=True) 
    for e in oldskelcontext.edgeboundaries.values():
        newskel.mapBoundary(e, orig, local=None)
    for p in oldskelcontext.pointboundaries.values():
        newskel.mapBoundary(p, orig, local=None)

    msname = oldskelpath[0]
    # "add" calls the SkeletonContext constructor, which calls
    # "disconnect" on the skeleton, ensuring that the propagation
    # we just did doesn't mess up the old skeleton context.
    skeletoncontext.skeletonContexts.add(
        [msname, nm], newskel,
        parent=microstructure.microStructures[msname])

    newskelcontext = skeletoncontext.skeletonContexts[ [msname, nm] ]
    newskelcontext.groupCopy(oldskelcontext)


smenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=_skeleton_copy_parallel,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=parameter.ParameterGroup(
    WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                 tip=parameter.emptyTipString),
    StringParameter('name')
    )
    ))


########################

def _skeleton_rename_parallel(menuitem, skeleton, name):
    # skeleton is a colon separated string
    oldskelpath = labeltree.makePath(skeleton)
    skel = skeletoncontext.skeletonContexts[oldskelpath]
    skel.reserve()
    skel.begin_writing()
    try:
        skel.rename(name, exclude=oldskelpath[-1])
    finally:
        skel.end_writing()
        skel.cancel_reservation()

smenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=_skeleton_rename_parallel,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=parameter.ParameterGroup(
    WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                 tip=parameter.emptyTipString),
    StringParameter('name', '', tip='New name for the skeleton')
    )
    ))

####################################################################
# menus for querying information on the node, segment or element
# that a user has clicked on in the graphics window,
# invoked in skeletoninfo.py.

def parallel_skel_info_query(menuitem, targetname, position, skeleton):
    debug.fmsg()
    skelcontext = skeletoncontext.skeletonContexts[skeleton]        
    skelobj = skelcontext.getObject()
    skelcontext.begin_reading()
    try:
        if targetname=="Node":
            node = skelobj.nearestNode(position)
            nodeindex=-1
            reportstring=""
            distance2=-1
            if node:
                nodeindex=node.getIndex()
                distance2=(node.position()-position)**2
                if node.movable_x() and node.movable_y():
                    nmob = "free"
                elif node.movable_x() and not node.movable_y():
                    nmob = "x only"
                elif not node.movable_x() and node.movable_y():
                    nmob = "y only"
                elif node.pinned():
                    nmob = "pinned"
                else:
                    nmob = "fixed"
                nneighborelements="None"
                if node.neighborElements(skelobj):
                    nneighborelements=string.join(["Element %d" % obj.index
                                                   for obj in node.neighborElements(skelobj)],",")
                reportstring="""
    index=%d
    position=(%g,%g)
    mobility=%s
    neighborelements=%s""" % (nodeindex,
                                node.position().x,node.position().y,
                                nmob,
                                nneighborelements)

            if _rank==0:
                #Get list of squares of distance of node to the click point
                distance2list=[distance2]
                #Get list of reportstring(s) from each process
                reportstringlist=[reportstring]
                dmin=-1
                dmin_proc=-1
                msg="Skeleton Info Query Node IPC/MPI:\n"
                #Get report from other processes
                for proc in range(_size):
                    if proc!=0:
                        reportstringlist.append(mpitools.Recv_String(proc))
                        distance2list.append(mpitools.Recv_Double(proc))
                    if distance2list[proc]>=0:
                        dmin=distance2list[proc]
                        dmin_proc=proc
                    #msg+="From process %d:%s\n" % (proc,reportstringlist[proc])
                #Find closest node among those "nominated" by each process
                for proc in range(_size):
                    if distance2list[proc]>=0:
                        if distance2list[proc]<dmin:
                            dmin=distance2list[proc]
                            dmin_proc=proc
                if dmin_proc!=-1:
                    msg+="The closest node to the point clicked at (%g,%g) is from process %d:%s\n" % \
                    (position.x,position.y,dmin_proc,reportstringlist[dmin_proc])
                reporter.report(msg)
            else:
                #Backend sends report to front end
                mpitools.Send_String(reportstring,0)
                mpitools.Send_Double(distance2,0)
        ################################################################################
        elif targetname=="Segment":
            # Function to calculate the distance squared between a point and
            # a segment (the perpendicular distance or distance from endpoints),
            # taken from skeleton.py.
            def segdistance(pt, segment):
                nodes = segment.nodes()
                p0 = nodes[0].position()
                p1 = nodes[1].position()
                a = pt-p0
                b = p1-p0
                seglength2 = b**2
                f = ((a*b)/seglength2)
                if f < 0:
                    alpha = -f
                    r = pt - p0
                elif f > 1:
                    alpha = f-1
                    r = pt - p1
                else:
                    r = a-f*b
                    alpha = 0
                return (r**2, alpha*alpha*seglength2)

            sgmt = skelobj.nearestSgmt(position)
            reportstring=""
            distance2=(-1,-1)
            if sgmt:
                distance2=segdistance(position,sgmt)
                sindex = `sgmt.getIndex()`
                length = `sgmt.length()`
                homogval = sgmt.homogeneity(skelobj.MS)
                if 0.9999 < homogval < 1.0:
                    homog = "1 - (%e)" % (1.0-homogval)
                else:
                    homog = `homogval`

                reportstring="""
    index=%s
    nodes=%s
    elements=%s
    length=%s
    homogeneity=%s""" % (sindex,
                         string.join(["Node %d at (%g, %g)" % (obj.index,
                                                               obj.position().x,
                                                               obj.position().y)
                                      for obj in sgmt.get_nodes()],","),
                         string.join(["Element %d" % obj.index for obj in sgmt.getElements()],","),
                         length,
                         homogval)

            if _rank==0:
                distance2list=[distance2]
                #Get list of reportstring(s) from each process
                reportstringlist=[reportstring]
                dmin=(-1,-1)
                dmin_proc=-1
                msg="Skeleton Info Query Segment IPC/MPI:\n"
                #Get report from other processes
                for proc in range(_size):
                    if proc!=0:
                        reportstringlist.append(mpitools.Recv_String(proc))
                        distance2list.append((mpitools.Recv_Double(proc),mpitools.Recv_Double(proc)))
                    if distance2list[proc][0]>=0:
                        dmin=distance2list[proc]
                        dmin_proc=proc
                #Find closest segment among those "nominated" by each process
                for proc in range(_size):
                    if distance2list[proc][0]>=0:
                        if distance2list[proc]<dmin:
                            dmin=distance2list[proc]
                            dmin_proc=proc
                if dmin_proc!=-1:
                    msg+="From process %d:" % dmin_proc
                    msg+=reportstringlist[dmin_proc]
                    reporter.report(msg)
                else:
                    reporter.report("No segment found!\n")
            else:
                #Backend sends report to front end
                mpitools.Send_String(reportstring,0)
                mpitools.Send_Double(distance2[0],0)
                mpitools.Send_Double(distance2[1],0)
        ################################################################################
        elif targetname=="Element":
            #This gets the element closest to the clicked point.
            #If the point is not within the microstructure then the point
            #is moved to the boundaries of the microstructure.
            elem = skelobj.enclosingElement(position)
            reportstring=""
            distance2=-1
            if elem:
                distance2=(elem.center()-position)**2
                etype = `elem.type()`[1:-1] # strip quotes
                eindex = `elem.getIndex()`
                earea = "%g" % elem.area()

                if not elem.illegal():
                    domCat = elem.dominantPixel(skelobj.MS)
                    repPix = skelobj.MS.getRepresentativePixel(domCat)
                    pixGrp = pixelgroup.pixelGroupNames(skelobj.MS, repPix)
                    pixgrps = string.join(pixGrp, ", ")
                    ehom = "%f" % elem.homogeneity(skelobj.MS)
                    eshape = "%f" % elem.energyShape()

                    mat = elem.material(skelobj)
                    if mat:
                        matname = mat.name()
                    else:
                        matname = "<No material>"
                else:                           # illegal element
                    pixgrps = "???"
                    ehom = "???"
                    eshape = "???"
                    matname = "???"

                reportstring="""
    index=%s
    type=%s
    nodes=%s
    segments=%s
    area=%s
    dominant pixel=%s
    homogeneity=%s
    shape energy=%s
    material=%s""" % (eindex,
                      etype,
                      string.join(["Node %d at (%g, %g)" % (obj.index,
                                                            obj.position().x,
                                                            obj.position().y)
                                   for obj in elem.nodes],","),
                      string.join(["Segment %d, nodes (%d, %d) (length: %g)" %
                                   (obj.index, obj.nodes()[0].index, obj.nodes()[1].index,
                                    obj.length())
                                   for obj in elem.getSegments(skelobj)],","),
                      earea,
                      pixgrps,
                      ehom,
                      eshape,
                      matname)

            if _rank==0:
                distance2list=[distance2]
                #Get list of reportstring(s) from each process
                reportstringlist=[reportstring]
                dmin=-1
                dmin_proc=-1
                msg="Skeleton Info Query Element IPC/MPI:\n"
                #Get report from other processes
                for proc in range(_size):
                    if proc!=0:
                        reportstringlist.append(mpitools.Recv_String(proc))
                        distance2list.append(mpitools.Recv_Double(proc))
                    if distance2list[proc]>=0:
                        dmin=distance2list[proc]
                        dmin_proc=proc
                #Find closest element among those "nominated" by each process
                for proc in range(_size):
                    if distance2list[proc]>=0:
                        if distance2list[proc]<dmin:
                            dmin=distance2list[proc]
                            dmin_proc=proc
                if dmin_proc!=-1:
                    msg+="From process %d:" % dmin_proc
                    msg+=reportstringlist[dmin_proc]
                    reporter.report(msg)
                else:
                    reporter.report("No enclosing element found!\n")
            else:
                #Backend sends report to front end
                mpitools.Send_String(reportstring,0)
                mpitools.Send_Double(distance2,0)
    finally:
        skelcontext.end_reading()

smenu.addItem(oofmenu.OOFMenuItem(
    'Skel_Info_Query',
    callback=parallel_skel_info_query,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[StringParameter('targetname'),
            primitives.PointParameter('position', tip='Target point.'),
            WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                         tip=parameter.emptyTipString)]
    ))

#############################################################################
#

def parallel_move_node(menuitem, origin, destination,
                       allow_illegal,
                       skeletonpath):
    skelcontext = skeletoncontext.skeletonContexts[skeletonpath]
    #skelcontext = self.gfxwindow().topwho('Skeleton')
    if skelcontext:
        skeleton = skelcontext.getObject().deputyCopy()
        skeleton.activate()
        #If one looks at moveNodeGUI.py, origin here is already
        #set to the position of the nearest node.
        node = skeleton.nearestNode(origin)
        nodeindex=node.getIndex()
        distance2=(node.position()-origin)**2
        ###############################################################
        # Get nearest node distances from all processes
        if _rank==0:
            #Get list of squares of distance of node to the click point
            distance2list=[distance2]
            dmin=-1
            dmin_proc_list=[]
            #Get distances from other processes
            for proc in range(_size):
                if proc!=0:
                    distance2list.append(mpitools.Recv_Double(proc))
                if distance2list[proc]>=0:
                    dmin=distance2list[proc]
            #Find closest node among those "nominated" by each process
            for proc in range(_size):
                if distance2list[proc]>=0:
                    if distance2list[proc]<dmin:
                        dmin=distance2list[proc]
            for proc in range(_size):
                if distance2list[proc]==dmin:
                    dmin_proc_list.append(proc)
        else:
            #Backend sends report to front end
            mpitools.Send_Double(distance2,0)

        mpitools.Barrier()
        
        #Tell the processes in dmin_proc_list to try moving their nodes
        #and report back the result. Then really move the node if the
        #move is valid for all of them.
        if _rank==0:
            for proc in range(_size):
                if proc in dmin_proc_list:
                    if proc==0:
                        moveit=1
                    else:
                        mpitools.Send_Int(1,proc)
                else:
                    if proc==0:
                        moveit=0
                    else:
                        mpitools.Send_Int(0,proc)
        else:
            moveit=mpitools.Recv_Int(0)

        mpitools.Barrier()

        #
        ###############################################################
        skelcontext.reserve()
        skelcontext.begin_writing()
        try:
            if moveit:
                skeleton.moveNodeTo(node, destination)
                #TODO 3.1: If the node is shared, the move may be valid in one process
                #but invalid in another.
                if node.illegal():
                    if allow_illegal==1:
                        skeleton.setIllegal()
                    else:
                        node.moveBack()
                elif skeleton.illegal(): # node motion may have rehabilitated
                    skeleton.checkIllegality()
                skelcontext.pushModification(skeleton)
        finally:
            #
            collect_pieces(skeleton)
            #
            skelcontext.end_writing()
            skelcontext.cancel_reservation()
        skeleton.needsHash()
        switchboard.notify('redraw')

smenu.addItem(oofmenu.OOFMenuItem(
    'Move_Node_Helper',
    callback=parallel_move_node,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[primitives.PointParameter('origin',
                                      tip=parameter.emptyTipString),
            primitives.PointParameter('destination',
                                      tip=parameter.emptyTipString),
            IntParameter('allow_illegal', 0, tip=parameter.emptyTipString),
            WhoParameter('skeletonpath', skeletoncontext.skeletonContexts,
                         tip=parameter.emptyTipString)]
    ))
