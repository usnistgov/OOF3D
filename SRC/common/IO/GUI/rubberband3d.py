# -*- python -*-
# $RCSfile: rubberband3d.py,v $
# $Revision: 1.2.10.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:12 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

OBSOLETE

#import vtk

class RubberBand:
    def __init__(self):
        self._active = False
        self.startpt = None
        self.current = None
        self.actor = None

    def active(self):
        return self._active

    def start(self, pt):
        self.startpt = pt
        self.current = pt
        self._active = True

    def stop(self, renderer):
        self._active = False
        self.clear(renderer)

    def redraw(self, renderer, point):
        self.clear(renderer)
        if(self._active):
            self.current = point
            self.updateActor()
            renderer.AddActor(self.actor)

    def clear(self, renderer):
        if renderer.GetActors().IsItemPresent(self.actor) and self.actor is not None:
            renderer.RemoveActor(self.actor)


class NoRubberBand(RubberBand):

    # sneakily, the NoRubberBand always returns false, this is to save
    # on expensive operations that aren't necessary with NoRubberBand
    def active(self):
        return False

    def draw(self, renderer):
        pass

class SpiderRubberBand(RubberBand):
    def __init__(self, pts):
        RubberBand.__init__(self)
        self.numpts = len(pts)
        self.points = vtk.vtkPoints()
        self.points.Allocate(self.numpts+1,self.numpts+1)
        self.points.InsertNextPoint(0,0,0)
        for pt in pts:
            self.points.InsertNextPoint(pt.x,pt.y,pt.z)
        self.mapper = vtk.vtkDataSetMapper()
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetRepresentationToWireframe()
        self.actor.GetProperty().SetColor(0,0,0)
        #self.actor.GetProperty().SetAmbient(1.0)
        self.actor.GetProperty().SetLineStipplePattern(31)

    def updateActor(self):
        self.points.SetPoint(0,self.current.x,self.current.y,self.current.z)
        poly = vtk.vtkPolyData()
        poly.Allocate(self.numpts,self.numpts)
        poly.SetPoints(self.points)
        for i in xrange(1,self.numpts+1):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            poly.InsertNextCell(line.GetCellType(), line.GetPointIds())
        self.mapper.SetInput(poly)
        
