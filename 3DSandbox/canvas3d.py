import gtk
from gtk import gdk
import vtk
import math
from voxelpicker import VoxelPicker


class Canvas3DBase(gtk.DrawingArea):

    def __init__(self, *args):
        gtk.DrawingArea.__init__(self)

        self._RenderWindow = vtk.vtkRenderWindow()
        # private attributes
        self.__Created = 0

        # used by the LOD actors
        self._DesiredUpdateRate = 15
        self._StillUpdateRate = 0.0001

        self.ConnectSignals()
        
        # need this to be able to handle key_press events.
        self.set_flags(gtk.CAN_FOCUS)
        # default size
        self.set_size_request(300, 300)
        
    def ConnectSignals(self):
        self.connect("realize", self.OnRealize)
        self.connect("expose_event", self.OnExpose)
        self.connect("configure_event", self.OnConfigure)
        self.connect("button_press_event", self.OnButtonDown)
        self.connect("button_release_event", self.OnButtonUp)
        self.connect("motion_notify_event", self.OnMouseMove)
        self.connect("enter_notify_event", self.OnEnter)
        self.connect("leave_notify_event", self.OnLeave)
        self.connect("key_press_event", self.OnKeyPress)
        self.connect("delete_event", self.OnDestroy)
        self.add_events(gdk.EXPOSURE_MASK|
                        gdk.BUTTON_PRESS_MASK |
                        gdk.BUTTON_RELEASE_MASK |
                        gdk.KEY_PRESS_MASK |
                        gdk.POINTER_MOTION_MASK |
                        gdk.POINTER_MOTION_HINT_MASK |
                        gdk.ENTER_NOTIFY_MASK |
                        gdk.LEAVE_NOTIFY_MASK)
        
    def GetRenderWindow(self):
        return self._RenderWindow

    def GetRenderer(self):
        self._RenderWindow.GetRenderers().InitTraversal()
        return self._RenderWindow.GetRenderers().GetNextItem()

    def SetDesiredUpdateRate(self, rate):
        """Mirrors the method with the same name in
        vtkRenderWindowInteractor."""
        self._DesiredUpdateRate = rate

    def GetDesiredUpdateRate(self):
        """Mirrors the method with the same name in
        vtkRenderWindowInteractor."""
        return self._DesiredUpdateRate 
        
    def SetStillUpdateRate(self, rate):
        """Mirrors the method with the same name in
        vtkRenderWindowInteractor."""
        self._StillUpdateRate = rate

    def GetStillUpdateRate(self):
        """Mirrors the method with the same name in
        vtkRenderWindowInteractor."""
        return self._StillUpdateRate

    def Render(self):
        if self.__Created:
            self._RenderWindow.Render()

    def OnRealize(self, *args):
        if self.__Created == 0:
            # you can't get the xid without the window being realized.
            self.realize()
            win_id = str(self.widget.window.xid)
            self._RenderWindow.SetWindowInfo(win_id)
            self.__Created = 1
        return True

    def Created(self):
        return self.__Created
    
    def OnConfigure(self, wid, event=None):
        self.widget=wid
        sz = self._RenderWindow.GetSize()
        
        if (event.width != sz[0]) or (event.height != sz[1]):
            self._RenderWindow.SetSize(event.width, event.height)
        return True

    def OnExpose(self, *args):
        self.Render()
        return True

    def OnDestroy(self, *args):
        self.hide()
        del self._RenderWindow
        self.destroy()
        return True

    def OnButtonDown(self, wid, event):
        """Mouse button pressed."""
        self._RenderWindow.SetDesiredUpdateRate(self._DesiredUpdateRate)
        return True
    
    def OnButtonUp(self, wid, event):
        """Mouse button released."""
        self._RenderWindow.SetDesiredUpdateRate(self._StillUpdateRate)
        return True

    def OnMouseMove(self, wid, event):
        """Mouse has moved."""
        return True

    def OnEnter(self, wid, event):
        """Entering the vtkRenderWindow."""
        return True

    def OnLeave(self, wid, event):
        """Leaving the vtkRenderWindow."""
        return True
    
    def OnKeyPress(self, wid, event):
        """Key pressed."""
        return True

    def OnKeyRelease(self, wid, event):
        "Key released."
        return True


class Canvas3D(Canvas3DBase):
    """ An example
    of a fully functional GtkGLExtVTKRenderWindow that is based on the
    vtkRenderWidget.py provided with the VTK sources."""
    def __init__(self, demowindow, *args):

        Canvas3DBase.__init__(self)
        
        self._CurrentRenderer = None
        self._CurrentCamera = None
        self._CurrentDolly = 1.0
        self._CurrentLight = None

        self._ViewportCenterX = 0
        self._ViewportCenterY = 0

        self._ClippingRange = (0,0)
        
        self._Picker = VoxelPicker()
        self._Picker.SetTolerance(.5)
        
        self._OldFocus = None

        # these record the previous mouse position
        self._LastX = 0
        self._LastY = 0

        # keeps reference to window - a hack to let this class manipulate the greater gui
        self.demowindow = demowindow


    def OnButtonDown(self, wid, event):
        self.demowindow.viewmenu.set_active(-1)
        self._RenderWindow.SetDesiredUpdateRate(self._DesiredUpdateRate)
        return self.StartMotion(wid, event)

    
    def OnButtonUp(self, wid, event):
        self._RenderWindow.SetDesiredUpdateRate(self._StillUpdateRate)
        if ((event.state & gdk.SHIFT_MASK) == gdk.SHIFT_MASK):
            m = self.get_pointer()
            self.VoxelInfo(m[0],m[1])
        return self.EndMotion(wid, event)

    def OnMouseMove(self, wid, event=None):
        # don't do anything if the shift key is pressed
        if ((event.state & gdk.SHIFT_MASK) == gdk.SHIFT_MASK):
            pass
        elif ((event.state & gdk.BUTTON1_MASK) == gdk.BUTTON1_MASK):
                m = self.get_pointer()
                self.MouseTumble(m[0], m[1])
                return True
        elif ((event.state & gdk.BUTTON2_MASK) == gdk.BUTTON2_MASK):
            m = self.get_pointer()
            self.MouseTrack(m[0], m[1])
            return True
        elif ((event.state & gdk.BUTTON3_MASK) == gdk.BUTTON3_MASK):
            m = self.get_pointer()
            self.MouseDolly(m[0], m[1])
            return True
        else:
            return False

    def OnEnter(self, wid, event=None):
        self.grab_focus()
        w = self.get_pointer()
        self.UpdateRenderer(w[0], w[1])
        return True

    def OnLeave(self, wid, event):
        return True


    def SetPickerImage(self, image):
        self._Picker.SetImage(image)


    def Render(self):
        if (self._CurrentLight):
            light = self._CurrentLight
            light.SetPosition(self._CurrentCamera.GetPosition())
            light.SetFocalPoint(self._CurrentCamera.GetFocalPoint())

        Canvas3DBase.Render(self)

        if self.GetCurrentRenderer() is not None:
            self.demowindow.updateCameraInfo()

    def UpdateRenderer(self,x,y):
        """
        UpdateRenderer will identify the renderer under the mouse and set
        up _CurrentRenderer, _CurrentCamera, and _CurrentLight.
        """

        windowX,windowY  = self.widget.window.get_size()

        renderers = self._RenderWindow.GetRenderers()
        numRenderers = renderers.GetNumberOfItems()

        self._CurrentRenderer = None
        renderers.InitTraversal()
        for i in range(0,numRenderers):
            renderer = renderers.GetNextItem()
            vx,vy = (0,0)
            if (windowX > 1):
                vx = float(x)/(windowX-1)
            if (windowY > 1):
                vy = (windowY-float(y)-1)/(windowY-1)
            (vpxmin,vpymin,vpxmax,vpymax) = renderer.GetViewport()
            
            if (vx >= vpxmin and vx <= vpxmax and
                vy >= vpymin and vy <= vpymax):
                self._CurrentRenderer = renderer
                self._ViewportCenterX = float(windowX)*(vpxmax-vpxmin)/2.0\
                                        +vpxmin
                self._ViewportCenterY = float(windowY)*(vpymax-vpymin)/2.0\
                                        +vpymin
                self._CurrentCamera = self._CurrentRenderer.GetActiveCamera()
                lights = self._CurrentRenderer.GetLights()
                lights.InitTraversal()
                self._CurrentLight = lights.GetNextItem()
                break

        self._LastX = x
        self._LastY = y        

    def GetCurrentRenderer(self):
        return self._CurrentRenderer
                
    def StartMotion(self, wid, event=None):
        x = event.x
        y = event.y
        self.UpdateRenderer(x,y)
        return True

    def EndMotion(self, wid, event=None):
        if self._CurrentRenderer:
            self.Render()
        return True


    def MouseTumble(self,x,y):
        """ By manipulating the camera position, create the appearance
        of tumbling the microstructure using the mouse."""
        if self._CurrentRenderer:
            
            self._CurrentCamera.Azimuth(self._LastX - x)
            self._CurrentCamera.Elevation(y - self._LastY)
            self._CurrentCamera.OrthogonalizeViewUp()
            
            self._LastX = x
            self._LastY = y
            
            self.ResetClippingRange()
            self.Render()


    def MouseTrack(self,x,y):
        # convert x,y translation in Display coordinates to World Coordinates
        if self._CurrentRenderer:
            
            renderer = self._CurrentRenderer
            camera = self._CurrentCamera
            (pPoint0,pPoint1,pPoint2) = camera.GetPosition()
            (fPoint0,fPoint1,fPoint2) = camera.GetFocalPoint()

            # Specify a point location in world coordinates
            renderer.SetWorldPoint(fPoint0,fPoint1,fPoint2,1.0)
            renderer.WorldToDisplay()
            # Convert world point coordinates to display coordinates
            dPoint = renderer.GetDisplayPoint()
            focalDepth = dPoint[2]

            aPoint0 = self._ViewportCenterX + (x - self._LastX)
            aPoint1 = self._ViewportCenterY - (y - self._LastY)

            renderer.SetDisplayPoint(aPoint0,aPoint1,focalDepth)
            renderer.DisplayToWorld()

            (rPoint0,rPoint1,rPoint2,rPoint3) = renderer.GetWorldPoint()
            if (rPoint3 != 0.0):
                rPoint0 = rPoint0/rPoint3
                rPoint1 = rPoint1/rPoint3
                rPoint2 = rPoint2/rPoint3

            self._LastX = x
            self._LastY = y

            self.Track(fPoint0 - rPoint0,fPoint1 - rPoint1,fPoint2 - rPoint2)
            

    def Track(self,x,y,z):
        camera = self._CurrentCamera
        (pPoint0,pPoint1,pPoint2) = camera.GetPosition()
        (fPoint0,fPoint1,fPoint2) = camera.GetFocalPoint()
        camera.SetFocalPoint(x + fPoint0, 
                             y + fPoint1,
                             z + fPoint2) 
                
        camera.SetPosition(x + pPoint0, 
                           y + pPoint1,
                           z + pPoint2)
        
        self.Render()


    def MouseDolly(self,x,y):
            dollyFactor = math.pow(1.02,(0.5*(self._LastY - y)))
            self._CurrentDolly = self._CurrentDolly * dollyFactor
            self.Dolly(dollyFactor)
            self._LastX = x
            self._LastY = y

    def Dolly(self,dollyFactor):
        if self._CurrentRenderer:

            renderer = self._CurrentRenderer
            camera = self._CurrentCamera

            if camera.GetParallelProjection():
                parallelScale = camera.GetParallelScale()/dollyFactor
                camera.SetParallelScale(parallelScale)
            else:
                camera.Dolly(dollyFactor)
                self.ResetClippingRange()

            self.Render()

    def Reset(self):
        if self._CurrentRenderer:
            self._CurrentRenderer.ResetCamera()
            
        self.Render()


    def ResetClippingRange(self):
        self._CurrentRenderer.ResetCameraClippingRange()
        self._ClippingRange = self._CurrentCamera.GetClippingRange()
        self.demowindow.clippingadj.set_value(100)

    def GetClippingRange(self):
        return self._ClippingRange


    def VoxelInfo(self,x,y):
        if self._CurrentRenderer:

            renderer = self._CurrentRenderer
            picker = self._Picker

            windowY = self.widget.window.get_size()[1]
            foundVox = picker.Pick(x,(windowY - y - 1),0.0,renderer)

            if foundVox:
                pointid = picker.GetPointId()
                voxelPoint = picker.GetPickedVoxel()
                
                self.demowindow.xtext.set_text(str(voxelPoint[0]))
                self.demowindow.ytext.set_text(str(voxelPoint[1]))
                self.demowindow.ztext.set_text(str(voxelPoint[2]))
                self.demowindow.setRGB(pointid)
                self.demowindow.DrawVoxelFrame(voxelPoint)


## main script for testing the image + cube problem on mac, causes
## some errors because it doesn't send a demowindow to the canvas, but
## is still good enough to check whether both actors show up.

## if __name__ == "__main__":

##     window = gtk.Window()
##     window.set_title("The Canvas 3D Test")
##     window.connect("destroy", gtk.mainquit)
##     window.connect("delete_event", gtk.mainquit)
##     window.set_border_width(10)

##     vtkda = Canvas3D(None)
##     vtkda.show()

    
##     vbox = gtk.VBox(spacing=3)
##     vbox.show()
##     vbox.pack_start(vtkda)

##     button = gtk.Button('My Button')
##     button.show()
##     vbox.pack_start(button)
##     window.add(vbox)
    
##     window.set_size_request(400, 400)

##     window.show()

##     # The VTK stuff.
##     cone = vtk.vtkConeSource()
##     cone.SetResolution(80)
##     coneMapper = vtk.vtkPolyDataMapper()
##     coneMapper.SetInput(cone.GetOutput())
##     #coneActor = vtk.vtkLODActor()
##     coneActor = vtk.vtkActor()
##     coneActor.SetMapper(coneMapper)    
##     coneActor.GetProperty().SetColor(0.5, 0.5, 1.0)
##     ren = vtk.vtkRenderer()
##     vtkda.GetRenderWindow().AddRenderer(ren)
##     ren.AddActor(coneActor)

##     # this doesn't cause the error and shows both cones on a mac!
## ##     cone2 = vtk.vtkConeSource()
## ##     cone2.SetResolution(80)
## ##     d = cone.GetDirection()
## ##     cone2.SetDirection(-1*d[0],-1*d[1],-1*d[2])
## ##     coneMapper2 = vtk.vtkPolyDataMapper()
## ##     coneMapper2.SetInput(cone2.GetOutput())
## ##     coneActor2 = vtk.vtkActor()
## ##     coneActor2.SetMapper(coneMapper2)    
## ##     coneActor2.GetProperty().SetColor(1.0, 0.5, 0.5)
## ##     ren.AddActor(coneActor2)
## ##     #vtkda.GetRenderWindow().AddRenderer(ren)


##     # if one of the cones from above is not commented out, shows only
##     # the cone on a mac, otherwise, it shows
##     reader = vtk.vtkJPEGReader()
##     reader.SetDataExtent(0,5,0,5,0,5)
##     reader.SetFilePrefix('mini/colorchecker.jpg')
##     image = reader.GetOutput()
##     mapper = vtk.vtkFixedPointVolumeRayCastMapper()
##     mapper.SetInput(image)
##     mapper.SetSampleDistance(.2)
##     volproperty = vtk.vtkVolumeProperty()
##     color = vtk.vtkPiecewiseFunction()
##     color.AddSegment(0,0,255,1)
##     volproperty.SetColor(color)
##     volume = vtk.vtkVolume()
##     volume.SetMapper(mapper)
##     volume.SetProperty(volproperty)
##     ren.AddActor(volume)
##     ren.ResetCamera()

##     # show the main window and start event processing.
##     #window.show()
##     gtk.main()






