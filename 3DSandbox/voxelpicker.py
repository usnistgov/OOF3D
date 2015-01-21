#import vtk
from math import *

# Eventually, when incorporated into OOF, we will want to write this
# in C++ and inherit from the vtkPointPicker class.  However, for now,
# we want to do the prototype code in Python, so it's easier to
# rewrite a simplified version.  Inheriting from C++ to Python is a
# major pain in this case.

class VoxelPicker:

    def __init__(self):
        self.PointId = -1
        self.PickedVoxel = None
        self.image = None
        self.tol = 0.025
        self.bounds = None


    def GetPointId(self):
        return self.PointId


    def GetPickedVoxel(self):
        return self.PickedVoxel


    # basically a copy of vtkPicker::Pick, need to override so call to
    # IntersectWithLine goes to our version
    def Pick(self, selectionX, selectionY, selectionZ, renderer):

        mapper = None
        picked = 0

        # in an initialize function?
        self.PickPosition = [0.0,0.0,0.0]
        self.PickedVoxel = None

        #self.basepicker.Initialize() #what will this do?
        self.Renderer = renderer
        self.SelectionPoint = (selectionX, selectionY, selectionZ)

        #should throw error if renderer is null

        # get camera focal point and position, convert to display
        # coordinates
        camera = renderer.GetActiveCamera()
        cameraPos = list(camera.GetPosition())
        cameraPos.append(1.0)
        cameraFP = list(camera.GetFocalPoint())
        cameraFP.append(1.0)

        renderer.SetWorldPoint(cameraFP)
        renderer.WorldToDisplay()
        displayCoords = renderer.GetDisplayPoint()
        selectionZ = displayCoords[2]

        # convert selection point into world coordinates
        renderer.SetDisplayPoint(selectionX, selectionY, selectionZ)
        renderer.DisplayToWorld()
        worldCoords = renderer.GetWorldPoint()
        if (worldCoords[3] == 0.0):
            print "Bad homogenous coordinates" #?
            return 0
        for i in xrange(3):
            self.PickPosition[i] = worldCoords[i]/worldCoords[3]

        # compute ray endpoints. The ray is along the line running
        # from the camera position to the selection point, starting where
        # this line intersects the front clipping plane, and terminating
        # where this line intersects the back clipping plane.
        ray = [0.0,0.0,0.0]
        for i in xrange(3):
            ray[i] = self.PickPosition[i] - cameraPos[i]
        cameraDOP = camera.GetDirectionOfProjection()
        
        rayLength = Dot(cameraDOP,ray)
        if rayLength == 0.0:
            print "cannot process points"
            return 0

        clipRange = camera.GetClippingRange()

        # not implementing parallel projection yet

        tF = clipRange[0] / rayLength
        tB = clipRange[1] / rayLength
        p1World = [0.0,0.0,0.0,0.0]
        p2World = [0.0,0.0,0.0,0.0]
        for i in xrange(3):
            p1World[i] = cameraPos[i] + tF*ray[i]
            p2World[i] = cameraPos[i] + tB*ray[i]
        p1World[3] = p2World[3] = 1.0

        # Compute the tolerance in world coordinates.  Do this by
        # determining the world coordinates of the diagonal points of the
        # window, computing the width of the window in world coordinates, and 
        # multiplying by the tolerance.
        viewport = renderer.GetViewport()
        winSize = renderer.GetRenderWindow().GetSize()
        x = winSize[0] + viewport[0]
        y = winSize[1] + viewport[1]
        renderer.SetDisplayPoint(x,y,selectionZ)
        renderer.DisplayToWorld()
        windowLowerLeft = renderer.GetWorldPoint()
        
        x = winSize[0] + viewport[2]
        y = winSize[1] + viewport[3]
        renderer.SetDisplayPoint(x,y,selectionZ)
        renderer.DisplayToWorld()
        windowUpperRight = renderer.GetWorldPoint()

        tol = 0.0
        for i in xrange(3):
            tol += (windowUpperRight[i] - windowLowerLeft[i]) * \
            (windowUpperRight[i] - windowLowerLeft[i])

        tol = sqrt(tol) * self.tol

        # end of stuff that was basically copied from vtkPicker::Pick

        # at this point, p1World is the point (in world coordinates)
        # where the ray intersects the first clipping plane, p2Worls
        # is where the ray intersects the back clipping plane.  tol is
        # the tolerance in world coordinates.

        # we want the point indices and/or point id of the voxel that
        # 1. intersects the ray 2. is in the front and 3. is within
        # the bounds of the image (not one of the padding voxels).

        # simple strategy, increment along the ray by the tolerance
        # until we find a point that is within the image
        # bounds. Truncate the coordinates of this point and take that
        # as our picked point.  This method assumes the spacing is
        # 1,1,1 and that the world coordinates correspond to image
        # coordinates, etc.  This is the case for our test code, at least.

        if self.image == None:
            print "picker image not initialzed"
            return 0

        currentPoint = p1World[0:3]
        lengthTraversed = 0.0
        rayInClippingRange = [p2World[0]-p1World[0], p2World[1]-p1World[1], p2World[2]-p1World[2]]
        rayInCRLength = Norm(rayInClippingRange)
        direction = Normalize(rayInClippingRange)
        inc = (direction[0]*tol,direction[1]*tol,direction[2]*tol)
        while (lengthTraversed <= rayInCRLength and self.PickedVoxel == None):
            # if currentpoint in bounds, truncate and return
            if self.InBounds(currentPoint):
                self.PickedVoxel = [int(currentPoint[0]),int(currentPoint[1]),int(currentPoint[2])]
                self.PointId = self.image.FindPoint(self.PickedVoxel)
                return 1
            currentPoint = [currentPoint[0]+inc[0],currentPoint[1]+inc[1],currentPoint[2]+inc[2]]
            lengthTraversed += tol

        return 0


    def InBounds(self, point):
        if self.bounds == None:
            print "image bounds not initialized in picker"
            return 0

        x,y,z = point
        xmin,xmax,ymin,ymax,zmin,zmax = self.bounds
        if x >= xmin and x <= xmax and y >= ymin and y <= ymax and z >= zmin and z <= zmax:
            return 1
        else:
            return 0
        


    def SetImage(self, image):
        self.image = image
        self.bounds = image.GetBounds()


    def SetTolerance(self, tolerance):
        self.tol = tolerance


    def GetTolerance(self):
        return self.tol


def Normalize(v):
    denom = sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    return (v[0]/denom,v[1]/denom,v[2]/denom)

def Dot(v1,v2):
    return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]

def Norm(v):
    return sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
