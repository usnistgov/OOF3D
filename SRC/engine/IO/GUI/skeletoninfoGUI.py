# -*- python -*-
# $RCSfile: skeletoninfoGUI.py,v $
# $Revision: 1.84.2.37 $
# $Author: langer $
# $Date: 2014/09/17 17:48:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import subthread
from ooflib.common import utils
from ooflib.common.IO.GUI import gtklogger
from ooflib.engine.IO import skeletoninfo
from ooflib.engine.IO.GUI import genericinfoGUI

import gtk

## Nodes and Elements are identified by index, because they can be
## looked up quickly that way.  Segments and Faces are identified by
## uid, because they don't have an index and aren't stored in vectors.
## In all cases, the uiIdentifier() method returns the appropriate
## identifier for use in the Info Toolbox.

## TODO 3.1: Display the number of segments, etc.

class SkeletonInfoModeGUI(genericinfoGUI.GenericInfoModeGUI):

    def updateNodeList(self, chsr, objlist, element=None):
        if element is None or config.dimension() == 3:
            namelist = ["Node %d at %s" 
                        % (obj.uiIdentifier(), 
                           genericinfoGUI.posString(obj.position()))
                        for obj in objlist]
        else:
            # 2D, element given.  Include angle info.
            namelist = ["Node %d at %s (angle: %g)"
                        % (obj.uiIdentifier(), 
                           genericinfoGUI.posString(obj.position()),
                           element.getRealAngle(element.nodes.index(obj)))
                        for obj in objlist]
        mainthread.runBlock(chsr.update, (objlist, namelist))

    def updateElementList(self, chsr, objlist):
        namelist = ["Element %d" % obj.uiIdentifier() for obj in objlist]
        mainthread.runBlock(chsr.update, (objlist, namelist))

    def updateSegmentList(self, chsr, objlist):
        namelist = ["Segment %d, nodes %s (length: %g)"
                    % (obj.uiIdentifier(), 
                       tuple(o.uiIdentifier() for o in obj.getNodes()),
                       obj.length())
                    for obj in objlist]
        mainthread.runBlock(chsr.update, (objlist, namelist))

    def updateFaceList(self, chsr, objlist):
        namelist = ["Face %d, nodes %s (area: %g)"
                    % (obj.uiIdentifier(),
                       tuple(o.uiIdentifier() for o in obj.getNodes()),
                       obj.area())
                    for obj in objlist]
        mainthread.runBlock(chsr.update, (objlist, namelist))

    def indexChangedCB(self, widget):
        self.activateOutputs(False)

    def indexChangeDoneCB(self, widget):
        try:
            indx = utils.OOFeval(self.index.get_text())
        except:
            pass
        else:
            self.menu.Query(mode=self.targetName, index=indx)


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementModeGUI(SkeletonInfoModeGUI):
    targetName = "Element"
    def __init__(self, gfxtoolbox):
        SkeletonInfoModeGUI.__init__(self, gfxtoolbox)

        row = 0
        self.labelmaster((0,1), (row,row+1), 'index=')
        self.index = self.entrymaster((1,2), (row,row+1), editable=True)
        gtklogger.setWidgetName(self.index, "Index")
        self.indexChangedSignal = gtklogger.connect(self.index, 'changed', 
                                                    self.indexChangedCB)
        gtklogger.connect(self.index, 'activate', self.indexChangeDoneCB)
        row += 1
        
        self.labelmaster((0,1), (row,row+1), 'type=')
        self.type = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.type, "Type")
        row += 1

        if config.dimension() == 3:
            self.labelmaster((0,1), (row,row+1), 'faces=')
            self.faces = self.makeObjList("Face", (1,2), (row,row+1))
            row += 1

        self.labelmaster((0,1), (row,row+1), 'segments=')
        self.segs = self.makeObjList("Segment", (1,2), (row,row+1))
        row += 1

        self.labelmaster((0,1), (row,row+1), 'nodes=')
        self.nodes = self.makeObjList("Node", (1,2), (row,row+1))
        row += 1

        if config.dimension() == 2:
            area = "area="
            Area = "Area"
        elif config.dimension() == 3:
            area = "volume="
            Area = "Volume"
        self.labelmaster((0,1), (row,row+1), area)
        self.area = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.area, Area)
        row += 1

        self.labelmaster((0,1), (row,row+1), 'dominant pixel=')
        self.domin = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.domin, "Dom pixel")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'homogeneity=')
        self.homog = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.homog, "Homog")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'shape energy=')
        self.shape = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.shape,"Shape")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'element groups=')
        self.group = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.group,"Group")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'material=')
        self.material = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.material,"Material")
        row += 1

    def findObjectIndex(self, position, view):
        skelctxt = self.getContext()
        if skelctxt is not None:
            cellID, clickpos = self.gfxtoolbox.gfxwindow().findClickedCellID(
                skelctxt, position, view)
            return cellID

    def activateOutputs(self, ok):
        self.type.set_sensitive(ok)
        if config.dimension() == 3:
            self.faces.gtk.set_sensitive(ok)
        self.segs.gtk.set_sensitive(ok)
        self.nodes.gtk.set_sensitive(ok)
        self.area.set_sensitive(ok)
        self.domin.set_sensitive(ok)
        self.homog.set_sensitive(ok)
        self.shape.set_sensitive(ok)
        self.group.set_sensitive(ok)
        self.material.set_sensitive(ok)

    def update(self, indx):
        debug.subthreadTest()
        skelctxt = self.getContext()
        if not skelctxt:
            return
        skeleton = skelctxt.getObject()
        if indx is not None and 0 <= indx < skeleton.nelements():
            skelctxt.begin_reading()
            try:
                microstructure = skeleton.getMicrostructure()
                # If the user typed the index, instead of clicking on
                # an element, it could be invalid.
                if indx < 0 or indx >= skeleton.nelements():
                    return

                element = skeleton.getElement(indx)
                assert element is not None

                if config.dimension() == 3:
                    self.updateFaceList(self.faces,
                                        skeleton.getElementFaces(element))
                self.updateSegmentList(self.segs,
                                       skeleton.getElementSegments(element))
                self.updateNodeList(self.nodes, element.getNodes(), element)

                eid = `indx`
                etype = skeleton.getElementType(element.getIndex())
                if config.dimension() == 3:
                    earea = "%g" % element.volume()
                elif config.dimension() == 2:
                    earea = "%g" % element.area()
                if not element.illegal():
                    domCat = element.dominantPixel(microstructure)
                    pixGrp = pixelgroup.pixelGroupNames(microstructure,
                                                        domCat)
                    pixgrps = ", ".join(pixGrp)
                    hom = "%f" % element.homogeneity(microstructure)
                    eshape = "%f" % element.energyShape()
                    mat = element.material(skeleton)
                    egrps = ','.join(element.groupNames())
                    if mat:
                        matname = mat.name()
                    else:
                        matname = "<No material>"
                else:           # illegal element
                    pixgrps = "???"
                    egrps = "???"
                    hom = "???"
                    eshape = "???"
                    matname = "???"
                mainthread.runBlock(self.update_thread,
                                    (etype, eid, earea, `domCat`, egrps, hom,
                                     eshape, matname))
                # mainthread.runBlock(self.update_thread,
                #                     (etype, eid, earea, pixgrps, egrps, hom,
                #                      eshape, matname))
                return
            finally:
                skelctxt.end_reading()
        # end if indx is not None
        # Nothing to display -- no element or no indx.
        mainthread.runBlock(self.update_thread,
                            ("", "", "", "", "", "", "", ""))
        mainthread.runBlock(self.clearObjLists)
        
    def update_thread(self, etype, eid, earea, pixgrps, egrps, hom, eshape,
                      matname):
        debug.mainthreadTest()
        self.activateOutputs(True)
        self.type.set_text(etype)
        self.indexChangedSignal.block()
        self.index.set_text(eid)
        self.indexChangedSignal.unblock()
        self.area.set_text(earea)
        self.domin.set_text(pixgrps)
        self.homog.set_text(hom)
        self.shape.set_text(eshape)
        self.material.set_text(matname)
        self.group.set_text(egrps)
                    

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class NodeModeGUI(SkeletonInfoModeGUI):
    targetName = "Node"
    def __init__(self, gfxtoolbox):
        SkeletonInfoModeGUI.__init__(self, gfxtoolbox)

        row = 0
        self.labelmaster((0,1), (row,row+1), 'index=')
        self.index = self.entrymaster((1,2), (row,row+1), editable=True)
        gtklogger.setWidgetName(self.index, "Index")
        self.indexChangedSignal = gtklogger.connect(self.index, 'changed',
                                                    self.indexChangedCB)
        gtklogger.connect(self.index, 'activate', self.indexChangeDoneCB)
        row += 1

        self.labelmaster((0,1), (row,row+1), 'position=')
        self.pos = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.pos, "Position")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'mobility=')
        self.mobility = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.mobility, "Mobility")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'elements=')
        self.elem = self.makeObjList("Element", (1,2), (row,row+1))
        row += 1
        
        if config.dimension() == 3:
            self.labelmaster((0,1), (row,row+1), 'faces=')
            self.faces = self.makeObjList("Face", (1,2), (row,row+1))
            row += 1

        self.labelmaster((0,1), (row,row+1), 'segments=')
        self.segs = self.makeObjList("Segment", (1,2), (row,row+1))
        row += 1

        self.labelmaster((0,1), (row,row+1), 'node groups=')
        self.group = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.group, "Group")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'boundary=')
        self.bndy = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.bndy, "Boundary")
        row += 1

    def findObjectIndex(self, position, view):
        skelctxt = self.getContext()
        if skelctxt is not None:
            pt = self.gfxtoolbox.gfxwindow().findClickedPoint(skelctxt,
                                                              position, view)
            node = pt is not None and skelctxt.getObject().nearestNode(pt)
            if node:
                return node.uiIdentifier()

    def activateOutputs(self, ok):
        self.pos.set_sensitive(ok)
        self.mobility.set_sensitive(ok)
        self.elem.gtk.set_sensitive(ok)
        if config.dimension() == 3:
            self.faces.gtk.set_sensitive(ok)
        self.segs.gtk.set_sensitive(ok)
        self.group.set_sensitive(ok)
        self.bndy.set_sensitive(ok)

    def update(self, indx):
        debug.subthreadTest()
        skelctxt = self.getContext()
        skeleton = skelctxt.getObject()
        if indx is not None and 0 <= indx < skeleton.nnodes():
            skelctxt.begin_reading()
            try:
                node = skeleton.getNode(indx)
                assert node is not None
                self.updateElementList(self.elem, node.getElements())
                self.updateSegmentList(self.segs,
                                       skeleton.getNodeSegments(node))
                if config.dimension() == 3:
                    self.updateFaceList(self.faces, skeleton.getNodeFaces(node))
                nuid = `indx`
                npos = genericinfoGUI.posString(node.position())
                
                movabilities = [node.movable_x(), node.movable_y()]
                if config.dimension() == 3:
                    movabilities.append(node.movable_z())
                    nmobile = sum(movabilities)
                    if nmobile == config.dimension():
                        mobstr = "free"
                    elif nmobile == 0:
                        if node.pinned():
                            mobstr = "pinned"
                        else:
                            mobstr = "fixed"
                    else:       # nmobile = 1 or 2
                        # mobstr is something like "x only" or "x and y only"
                        m = ["xyz"[i] for i in range(config.dimension())
                             if movabilities[i]]
                        mobstr = " and ". join(m) + " only"

                bdynames = [nm for (nm, bdy) in skelctxt.pointboundaries.items()
                            if bdy.current_boundary().hasNode(node)]

                ## TODO 3.1: node groups
                mainthread.runBlock(self.update_thread,
                                    (nuid, npos, mobstr,
                                     ", ".join(bdynames)))
                return
            finally:
                skelctxt.end_reading()
        # end if indx is not None
        # Nothing to display
        mainthread.runBlock(self.update_thread, ("", "", "", ""))
        mainthread.runBlock(self.clearObjLists)

    def update_thread(self, nuid, npos, mobstr, bdynames):
        self.activateOutputs(True)
        debug.mainthreadTest()
        self.indexChangedSignal.block()
        self.index.set_text(nuid)
        self.indexChangedSignal.unblock()
        self.pos.set_text(npos)
        self.mobility.set_text(mobstr)
        self.bndy.set_text(bdynames)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SegmentModeGUI(SkeletonInfoModeGUI):
    targetName = "Segment"
    def __init__(self, gfxtoolbox):
        SkeletonInfoModeGUI.__init__(self, gfxtoolbox)

        row = 0
        self.labelmaster((0,1), (row,row+1), 'index=')
        self.index = self.entrymaster((1,2), (row,row+1), editable=True)
        gtklogger.setWidgetName(self.index, "Index")
        self.indexChangedSignal = gtklogger.connect(self.index, 'changed',
                                                    self.indexChangedCB)
        gtklogger.connect(self.index, 'activate', self.indexChangeDoneCB)
        row += 1

        self.labelmaster((0,1), (row,row+1), 'elements=')
        self.elem = self.makeObjList("Element", (1,2), (row,row+1))
        row += 1

        if config.dimension() == 3:
            self.labelmaster((0,1), (row,row+1), 'faces=')
            self.faces = self.makeObjList("Face", (1,2), (row,row+1))
            row += 1

        self.labelmaster((0,1), (row,row+1), 'nodes=')
        self.nodes = self.makeObjList("Node", (1,2), (row,row+1))
        row += 1

        self.labelmaster((0,1), (row,row+1), 'length=')
        self.length = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.length, "Length")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'homogeneity=')
        self.homog = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.homog, "Homogeneity")
        row += 1

        self.labelmaster((0,1), (row,row+1), 'segment groups=')
        self.group = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.group, "Groups")
        self.group.set_sensitive(False) # TODO: remove this line when implemented
        row += 1

        self.labelmaster((0,1), (row,row+1), 'boundary=')
        self.bndy = self.entrymaster((1,2), (row,row+1))
        gtklogger.setWidgetName(self.bndy, "Boundary")
        row += 1

#         self.labelmaster((0,1), (row,row+1), 'material=')
#         self.material = self.entrymaster((1,2), (row,row+1))
#         gtklogger.setWidgetName(self.material, "Material")

    def findObjectIndex(self, position, view):
        skelctxt = self.getContext()
        if skelctxt is not None:
            pt = self.gfxtoolbox.gfxwindow().findClickedSegment(
                skelctxt, position, view)
            sgmt = pt is not None and skelctxt.getObject().nearestSegment(pt)
            if sgmt:
                return sgmt.uiIdentifier()

    def activateOutputs(self, ok):
        self.elem.gtk.set_sensitive(ok)
        if config.dimension() == 3:
            self.faces.gtk.set_sensitive(ok)
        self.nodes.gtk.set_sensitive(ok)
        self.length.set_sensitive(ok)
        self.homog.set_sensitive(ok)
        # self.group.set_sensitive(ok)
        self.bndy.set_sensitive(ok)
    
    def update(self, indx):
        debug.subthreadTest()
        if indx is not None:
            skelctxt = self.getContext()
            skelctxt.begin_reading()
            skeleton = skelctxt.getObject()
            try:
                segment = skeleton.getSegmentByUid(indx)
                if segment is not None:
                    self.updateElementList(self.elem,
                                           skeleton.getSegmentElements(segment))
                    self.updateNodeList(self.nodes, segment.getNodes())
                    if config.dimension() == 3:
                        self.updateFaceList(self.faces, 
                                            skeleton.getSegmentFaces(segment))
                    length = `segment.length()`
                    homogval = segment.homogeneity(skelctxt.getMicrostructure())
                    if 0.9999 < homogval < 1.0:
                        homog = "1 - (%e)" % (1.0 - homogval)
                    else:
                        homog = `homogval`
                    bdynames = [nm
                                for (nm, bdy) in skelctxt.edgeboundaries.items()
                                if bdy.current_boundary().hasSegment(segment)]
                    # TODO 3.1: List relevant  groups.
                    groups = ["<Not yet implemented>"]
                    # TODO 3.1: List interface material
                    mainthread.runBlock(self.update_thread,
                                        (`indx`, length, homog,
                                         ", ".join(bdynames),
                                         ", ".join(groups)))
                    return
            finally:
                skelctxt.end_reading()
        # end if indx is not None
        # Nothing to display
        mainthread.runBlock(self.update_thread, ("", "", "", "", ""))
        mainthread.runBlock(self.clearObjLists)

    def update_thread(self, indx, length, homog, bdynames, groups):
        debug.mainthreadTest()
        self.activateOutputs(True)
        self.indexChangedSignal.block()
        self.index.set_text(indx)
        self.indexChangedSignal.unblock()
        self.length.set_text(length)
        self.homog.set_text(homog)
        self.bndy.set_text(bdynames)
        self.group.set_text(groups)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FaceModeGUI(SkeletonInfoModeGUI):
    targetName = "Face"
    def __init__(self, gfxtoolbox):
        SkeletonInfoModeGUI.__init__(self, gfxtoolbox)

        self.labelmaster((0,1), (0,1), 'index=')
        self.index = self.entrymaster((1,2), (0,1), editable=True)
        gtklogger.setWidgetName(self.index, "Index")
        self.indexChangedSignal = gtklogger.connect(self.index, 'changed',
                                                    self.indexChangedCB)
        gtklogger.connect(self.index, 'activate', self.indexChangeDoneCB)

        self.labelmaster((0,1), (1,2), 'elements=')
        self.elem = self.makeObjList("Element", (1,2), (1,2))

        self.labelmaster((0,1), (2,3), 'segments=')
        self.segs = self.makeObjList("Segment", (1,2), (2,3))

        self.labelmaster((0,1), (3,4), 'nodes=')
        self.nodes = self.makeObjList("Node", (1,2), (3,4))

        self.labelmaster((0,1), (4,5), 'area=')
        self.area = self.entrymaster((1,2), (4,5))
        gtklogger.setWidgetName(self.area, "Area")

        self.labelmaster((0,1), (5,6), 'homogeneity=')
        self.homog = self.entrymaster((1,2), (5,6))
        gtklogger.setWidgetName(self.homog, "Homogeneity")
        self.homog.set_sensitive(False) # TODO 3.1: remove this when implemented

        self.labelmaster((0,1), (6,7), 'face groups=')
        self.group = self.entrymaster((1,2), (6,7))
        gtklogger.setWidgetName(self.group, "Groups")
        self.group.set_sensitive(False) # TODO 3.1: remove this when implemented

        self.labelmaster((0,1), (7,8), 'boundary=')
        self.bndy = self.entrymaster((1,2), (7,8))
        gtklogger.setWidgetName(self.bndy, "Boundary")

    def findObjectIndex(self, position, view):
        skelctxt = self.getContext()
        if skelctxt is not None:
            pt = self.gfxtoolbox.gfxwindow().findClickedPosition(
                skelctxt, position, view)
            face = pt is not None and skelctxt.getObject().nearestFace(pt)
            if face:
                return face.uiIdentifier()

    def activateOutputs(self, ok):
        self.elem.gtk.set_sensitive(ok)
        self.segs.gtk.set_sensitive(ok)
        self.nodes.gtk.set_sensitive(ok)
        self.area.set_sensitive(ok)
        # self.homog.set_sensitive(ok)
        # self.group.set_sensitive(ok)
        self.bndy.set_sensitive(ok)
        
    def update(self, indx):
        debug.subthreadTest()
        if indx is not None:
            skelctxt = self.getContext()
            skeleton = skelctxt.getObject()
            skelctxt.begin_reading()
            try:
                face = skeleton.getFaceByUid(indx)
                if face is not None:
                    self.updateElementList(self.elem,
                                           skeleton.getFaceElements(face))
                    self.updateSegmentList(self.segs, 
                                           skeleton.getFaceSegments(face))
                    self.updateNodeList(self.nodes, face.getNodes())
                    area = `face.area()`
                    ## TODO 3.1: Uncomment this when
                    ## CSkeletonFace::homogeneity has been implemented.
                    # homogval = face.homogeneity(skelctxt.getMicrostructure())
                    # if 0.9999 < homogval < 1.0:
                    #     homog = "1.0 - (%e)" % (1.0-homogval)
                    # else:
                    #     homog = `homogval`
                    homog = '<Not yet implemented.>'

                    bdynames = [nm
                                for (nm, bdy) in skelctxt.faceboundaries.items()
                                if bdy.current_boundary().hasFace(face)]

                    ## TODO 3.1: Display groups and materials.
                    groupnames = ["<Not yet implemented.>"]

                    mainthread.runBlock(self.update_thread,
                                        (`indx`, area, homog,
                                         ", ".join(bdynames), 
                                         ", ".join(groupnames)))

                    return
            finally:
                skelctxt.end_reading()
        # end if indx is not None
        # Nothing to display
        mainthread.runBlock(self.update_thread, ("", "", "", "", ""))
        mainthread.runBlock(self.clearObjLists)

    def update_thread(self, indx, area, homog, bdynames, groupnames):
        debug.mainthreadTest()
        self.activateOutputs(True)
        self.indexChangedSignal.block()
        self.index.set_text(indx)
        self.indexChangedSignal.unblock()
        self.area.set_text(area)
        self.homog.set_text(homog)
        self.bndy.set_text(bdynames)
        self.group.set_text(groupnames)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

_modes = utils.OrderedDict()

# The order in which the modes are inserted in _modes controls the
# order in which they appear in the GUI.  They're listed in order of
# decreasing dimension here and in other parts of the gui.

_modes[ElementModeGUI.targetName] = ElementModeGUI
if config.dimension() == 3:
    _modes[FaceModeGUI.targetName] = FaceModeGUI
_modes[SegmentModeGUI.targetName] = SegmentModeGUI
_modes[NodeModeGUI.targetName] = NodeModeGUI

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=

class SkeletonInfoToolboxGUI(genericinfoGUI.GenericInfoToolboxGUI):
    def __init__(self, skelinfotb):
        genericinfoGUI.GenericInfoToolboxGUI.__init__(self, "Skeleton Info",
                                                      skelinfotb)
        self.sbcallbacks.extend([
                switchboard.requestCallback('changed pixel group',
                                            self.grpChangedCB),
                switchboard.requestCallback('changed pixel groups',
                                            self.grpsChangedCB),
                switchboard.requestCallback('destroy pixel group',
                                            self.grpChangedCB),
                switchboard.requestCallback('renamed pixel group',
                                            self.grpRenamedCB),
                switchboard.requestCallback(
                    'materials changed in microstructure', self.matChangedCB),
                switchboard.requestCallback(
                    'materials changed in skeleton', self.matChangedSkelCB)
                ## TODO 3.1: add callbacks for skeleton group changes of all sorts
                ])

    def modeClassDict(self):
        return _modes

    def packModeButtons(self, hbox, buttons):
        table = gtk.Table(columns=2, rows=2)
        hbox.pack_start(table, expand=0, fill=0)
        b = iter(buttons)
        for row in range(0, 2):
            for col in range(0, 2):
                table.attach(b.next(), col,col+1, row,row+1)

    def getSkeletonContext(self):
        return self.toolbox.context

    def grpChangedCB(self, group, msname):
        skel = self.getSkeletonContext()
        if skel and skel.getMicrostructure().name() == msname:
            self.update()
    def grpsChangedCB(self, msname):
        skel = self.getSkeletonContext()
        if skel and skel.getMicrostructure().name() == msname:
            self.update()
    def grpRenamedCB(self, group, oldname, newname):
        self.update()
    def matChangedCB(self, ms):
        skel = self.getSkeletonContext()
        if skel and skel.getMicrostructure() is ms:
            self.update()
    def matChangedSkelCB(self, skelctxt):
        if skelctxt is self.getSkeletonContext():
            self.update()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _makeGUI(self):
    return SkeletonInfoToolboxGUI(self)

skeletoninfo.SkeletonInfoToolbox.makeGUI = _makeGUI
