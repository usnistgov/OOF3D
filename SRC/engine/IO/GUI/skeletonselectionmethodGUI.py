# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import selectionoperators
from ooflib.common.IO import mousehandler
from ooflib.common.IO.GUI import genericselectGUI
from ooflib.engine import skeletoncontext
from ooflib.engine import skeletonselectionmethod

class SingleClickSkelSelectionMethodGUI(genericselectGUI.SelectionMethodGUI):
    def mouseHandler(self):
        return mousehandler.SingleClickMouseHandler(self)

    def modkeys(self, buttons):
        self.toolbox.setParamValues(
            operator=selectionoperators.getSelectionOperator(buttons))

    def getSourceContext(self):
        return skeletoncontext.skeletonContexts[self.toolbox.getSourceName()]

    def getViewAndPoint(self, x, y):
        viewobj = mainthread.runBlock(self.gfxwindow().oofcanvas.get_view)
        point = mainthread.runBlock(self.gfxwindow().oofcanvas.display2Physical,
                                    (viewobj, x, y))
        return viewobj, point

    def getClickedPoint(self, x, y):
        # Return the position of a point that was clicked on from a
        # vtk object's vtkPoints set.
        viewobj, realpoint = self.getViewAndPoint(x, y)
        pt = self.gfxwindow().findClickedPoint(self.getSourceContext(),
                                               realpoint, viewobj)
        return pt

    def getClickedSegment(self, x, y):
        viewobj, realpoint = self.getViewAndPoint(x, y)
        endPtIds = self.gfxwindow().findClickedSegment(self.getSourceContext(),
                                                       realpoint, viewobj)
        return endPtIds

    def getClickedFace(self, x, y):
        viewobj, realpoint = self.getViewAndPoint(x, y)
        cornerIds = self.gfxwindow().findClickedFace(
            self.getSourceContext(), realpoint, viewobj)
        return cornerIds

    def getClickedCell(self, x, y):
        viewobj, realpoint = self.getViewAndPoint(x, y)
        cell = self.gfxwindow().findClickedCell(self.getSourceContext(),
                                                realpoint, viewobj)
        return realpoint, cell

    def getClickedVoxel(self, x, y):
        viewobj, realpoint = self.getViewAndPoint(x, y)
        layers = self.gfxwindow().allWhoClassLayers(
            *self.methodRegistration.whoclasses)
        result = self.gfxwindow().findClickedCellCenterMulti(
            layers, realpoint, viewobj)
        return result           # (clicked Who obj, position)

@genericselectGUI.selectionGUIfor(skeletonselectionmethod.SingleNodeSelect)
class NodeSelectorGUI(SingleClickSkelSelectionMethodGUI):
    def down(self, x, y, buttons):
        pt = self.getClickedPoint(x, y)
        self.toolbox.setParamValues(
            point=pt,
            operator=selectionoperators.getSelectionOperator(buttons))

    def up(self, x, y, buttons):
        who = self.toolbox.getSelectionSource()
        if who is not None:
            pt = self.getClickedPoint(x, y)
            if pt is not None:
                operator = selectionoperators.getSelectionOperator(buttons)
                self.toolbox.invokeMenuItem(
                    who, skeletonselectionmethod.SingleNodeSelect(pt, operator))
        
            
                                               
@genericselectGUI.selectionGUIfor(skeletonselectionmethod.SingleSegmentSelect)
class SegmentSelectorGUI(SingleClickSkelSelectionMethodGUI):
    def up(self, x, y, buttons):
        who = self.toolbox.getSelectionSource()
        if who is not None:
            endPts = self.getClickedSegment(x, y)
            if endPts is not None:
                # See comment and TODO in FaceSelectorGUI below
                nodes = [endPts[i] for i in (0,1)]
                operator = selectionoperators.getSelectionOperator(buttons)
                self.toolbox.invokeMenuItem(
                    who,
                    skeletonselectionmethod.SingleSegmentSelect(
                        nodes, operator))

@genericselectGUI.selectionGUIfor(skeletonselectionmethod.SingleFaceSelect)
class FaceSelectorGUI(SingleClickSkelSelectionMethodGUI):
    def up(self, x, y, buttons):
        who = self.toolbox.getSelectionSource()
        if who is not None:
            corners = self.getClickedFace(x, y) # vtkIdListPtr object
            if corners is not None:
                # Convert the vtkIdList object to a python list of int
                # node ids.
                ## TODO: This conversion could be avoided if we wanted
                ## to make the vtkIdListPtr object constructible in
                ## Python, and just use it directly in scripts.  The
                ## vtkIdList could be passed back in to C++ as the
                ## argument to findExistingFaceByIds (which used to
                ## take a vtkIdList).  Maybe make a vtkIdList
                ## parameter that can be set from and written as a
                ## python list of ints?
                nodes = [corners[i] for i in range(corners.size())]
                operator = selectionoperators.getSelectionOperator(buttons)
                self.toolbox.invokeMenuItem(
                    who,
                    skeletonselectionmethod.SingleFaceSelect(nodes, operator))

@genericselectGUI.selectionGUIfor(skeletonselectionmethod.SingleElementSelect)
class ElementSelectorGUI(SingleClickSkelSelectionMethodGUI):
    def up(self, x, y, buttons):
        who = self.toolbox.getSelectionSource()
        if who is not None:
            pt, cell = self.getClickedCell(x, y)
            if cell is not None:
                element = who.getObject().findElement(cell)
                operator = selectionoperators.getSelectionOperator(buttons)
                self.toolbox.invokeMenuItem(
                    who, skeletonselectionmethod.SingleElementSelect(
                        element.getIndex(), operator))
                        

@genericselectGUI.selectionGUIfor(skeletonselectionmethod.PixelElementSelect)
class PixelElementSelectorGUI(SingleClickSkelSelectionMethodGUI):
    def up(self, x,y, buttons):
        who = self.toolbox.getSelectionSource()
        if who is not None:
            msorimage, voxel = self.getClickedVoxel(x, y)
            ms = msorimage.getMicrostructure()
            category = ms.category(ms.pixelFromPoint(voxel))
            operator = selectionoperators.getSelectionOperator(buttons)
            self.toolbox.invokeMenuItem(
                who,
                skeletonselectionmethod.PixelElementSelect(category, operator))
