import gtk
from gtk import gdk
import vtk
import math


class Canvas3DBase(gtk.DrawingArea):

    def __init__(self, *args):
        gtk.DrawingArea.__init__(self)

        self._RenderWindow = vtk.vtkRenderWindow()
        # private attributes
        self.__Created = 0

        self.ConnectSignals()
        
        # need this to be able to handle key_press events.
        self.set_flags(gtk.CAN_FOCUS)
        # default size
        self.set_size_request(300, 300)
        
    def ConnectSignals(self):
        self.connect("realize", self.OnRealize)
        self.connect("expose_event", self.OnExpose)
        self.connect("configure_event", self.OnConfigure)
        self.connect("delete_event", self.OnDestroy)
        
    def GetRenderWindow(self):
        return self._RenderWindow

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
        
        self._OldFocus = None

        # these record the previous mouse position
        self._LastX = 0
        self._LastY = 0

        # keeps reference to window - a hack to let this class manipulate the greater gui
        self.demowindow = demowindow


    def Render(self):
        if (self._CurrentLight):
            light = self._CurrentLight
            light.SetPosition(self._CurrentCamera.GetPosition())
            light.SetFocalPoint(self._CurrentCamera.GetFocalPoint())

        Canvas3DBase.Render(self)




## main script for testing the image + cube problem on mac, causes
## some errors because it doesn't send a demowindow to the canvas, but
## is still good enough to check whether both actors show up.

if __name__ == "__main__":

    window = gtk.Window()
    window.set_title("X11/VTK/GTK/Mac debug")
    window.connect("destroy", gtk.main_quit)
    window.connect("delete_event", gtk.main_quit)
    window.set_border_width(10)

    vtkda = Canvas3D(None)
    vtkda.show()

    vbox = gtk.VBox(spacing=3)
    vbox.show()
    vbox.pack_start(vtkda)

    button = gtk.Button('My Button')
    button.show()
    vbox.pack_start(button)
    window.add(vbox)
    
    window.set_size_request(400, 400)

    window.show()

    # The VTK stuff.
    cone = vtk.vtkConeSource()
    cone.SetResolution(80)
    cone.SetRadius(2)
    cone.SetHeight(2)
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)    
    coneActor.GetProperty().SetColor(0.5, 0.5, 1.0)

    # if one of the cones from above is not commented out, shows only
    # the cone on a mac, otherwise, it shows
    reader = vtk.vtkPNMReader()
    reader.SetFilePattern("mini/checkerboard%i.pgm")
    size = 5
    
    reader.SetDataExtent(0,size,0,size,0,size)
    reader.SetDataSpacing(1,1,1)
    reader.SetDataScalarTypeToUnsignedChar()
    image = reader.GetOutput()
    image.Update()
    
    mapper = vtk.vtkFixedPointVolumeRayCastMapper()
    mapper.SetInput(image)
    if size < 20:
        mapper.SetSampleDistance(float(size)/1000)
        mapper.SetInteractiveSampleDistance(float(size)/500)
    volproperty = vtk.vtkVolumeProperty()
    color = vtk.vtkPiecewiseFunction()
    color.AddSegment(0,0,255,1)
    volproperty.SetColor(0,color)
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volproperty)

    ren = vtk.vtkRenderer()
    ren.SetBackground(.5, .5, .5)
    vtkda.GetRenderWindow().AddRenderer(ren)
    ren.AddActor(coneActor)
    ren.AddActor(volume)
    ren.ResetCamera()

    # show the main window and start event processing.
    #window.show()
    gtk.main()






