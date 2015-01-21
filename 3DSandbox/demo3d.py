import sys, os, types, string, random, code
#import oof2.SWIG.common.switchboard          # message passing
import oof3d
sys.path.append(os.path.dirname(oof3d.__file__))
from ooflib.common.IO.GUI import gtklogger
#from ooflib.common.IO.GUI import gtkutils
import gtk
import vtk
import gobject
from math import *
from canvas3d import Canvas3D

# This isn't exactly representative of what I'd like to incorporate
# into oof3d.  This one script contains stuff that would ultimately be
# split up between gfx window, viewer toolbox, and the replacement for
# canvas.  I was just trying to keep this demo as simple and self
# contained as possible, so it's all here.


initial_width = 950
initial_height = 600

class View:

    def __init__(self,pos,focal,up,angle=30,clip=100,opacity=100):
        self.pos = pos
        self.focal = focal
        self.up = up
        self.angle = angle
        self.clip = clip
        self.opacity = opacity

class ImageImporter:

    def __init__(self,imagetype,prefix,extent):

        if imagetype == "jpg":
            reader = vtk.vtkJPEGReader()
        elif imagetype == "pnm":
            reader = vtk.vtkPNMReader()
        elif imagetype == "tif":
            reader = vtk.vtkTIFFReader()
        # todo: add more image types
        else:
            print "unknown type!"
            sys.exit()

        reader.SetDataExtent(extent)
        #reader.SetFilePrefix(prefix)
        reader.SetFilePattern(prefix)
        reader.SetDataSpacing(1,1,1)
        imageoriginal = reader.GetOutput()

        # pad the image with extra voxels because of vtk off by 1
        # annoyance in calculating image bounds
#         extentcopy = extent[:]
#         for i in xrange(1,7,2):
#             extentcopy[i] += 1
#         padder = vtk.vtkImageConstantPad()
#         padder.SetInput(imageoriginal)
#         padder.SetOutputWholeExtent(extentcopy) 
#         padder.SetConstant(255) # arbitrary
#         self.image = padder.GetOutput()
#         self.image.Update()
        self.image = imageoriginal
        self.image.Update()

        # must use this particular mapper so color images work, also
        # handles off by 1 annoyance in a slightly better way.
        mapper = vtk.vtkFixedPointVolumeRayCastMapper()
        mapper.IntermixIntersectingGeometryOn()
        min_extent = min(extent[1:6:2])
        # todo: can use a built in function for this
        # for very small images we need to reset the sample distance
        if min_extent < 50:
            mapper.SetSampleDistance(float(min_extent)/100)
            mapper.SetInteractiveSampleDistance(float(min_extent)/50)
        mapper.SetInput(self.image)

        volproperty = vtk.vtkVolumeProperty()
        volproperty.IndependentComponentsOff()

        # we initially set the opacity to a constant value of 1, but
        # we need the function so we can change it later
        self.opacity = vtk.vtkPiecewiseFunction()
        self.opacity.AddSegment(0,1,255,1)

        # the type of color function we use depends on how many
        # components the image has, 3 for a color image, 1 for a black
        # and white image
        num_components = self.image.GetNumberOfScalarComponents()
        
        if num_components == 1:
            color = vtk.vtkPiecewiseFunction()
            color.AddSegment(0,0,255,1)
            volproperty.SetColor(color)
            volproperty.SetScalarOpacity(self.opacity)
        elif num_components == 4:
##             red = vtk.vtkColorTransferFunction()
##             red.AddRGBSegment(0,0,0,0,255,1,0,0)
##             green = vtk.vtkColorTransferFunction()
##             green.AddRGBSegment(0,0,0,0,255,0,1,0)
##             blue = vtk.vtkColorTransferFunction()
##             blue.AddRGBSegment(0,0,0,0,255,0,0,1)
##             volproperty.SetColor(0,red)
##             volproperty.SetColor(1,green)
##             volproperty.SetColor(2,blue)
            volproperty.SetScalarOpacity(self.opacity)
##             volproperty.SetScalarOpacity(1,self.opacity)
##             volproperty.SetScalarOpacity(2,self.opacity)
        else:
            pass
        print num_components

        volume = vtk.vtkVolume()
        volume.SetMapper(mapper)
        volume.SetProperty(volproperty)

        self.ren = vtk.vtkRenderer()
        self.ren.AddActor(volume)
        # on mac, this shows only the cone
        #self.DrawCone()
        #print self.ren.VisibleActorCount()
        #print self.ren.VisibleVolumeCount()
        self.ren.ResetCamera()

    def GetRenderer(self):
        return self.ren

    def GetImage(self):
        return self.image

    def GetOpacityFunction(self):
        return self.opacity

    def DrawCone(self):
        # simple function for testing rendering multiple actors which
        # causes errors on a mac.
        cone = vtk.vtkConeSource()
        cone.SetResolution(80)
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInput(cone.GetOutput())
        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)    
        coneActor.GetProperty().SetColor(0.5, 0.5, 1.0)
        self.ren.AddActor(coneActor)
    

class Demo3D:

    def __init__(self):

        self.saved_views = {}

        self.gtk = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.gtk.set_title('Demo of a Mockup of OOF3D Interface')
        self.gtk.set_default_size(initial_width, initial_height)
        self.gtk.connect("destroy", self.destroy)
        self.gtk.connect("delete_event", self.destroy)

        self.cubeActor = None

        # set up areas
        self.panes = gtk.HPaned()
        self.gtk.add(self.panes)

        self.canvas = Canvas3D(self)
        self.panes.add2(self.canvas)

        
        self.toolboxframe = gtk.Frame()
        self.toolboxframe.set_shadow_type(gtk.SHADOW_IN)
        self.panes.add1(self.toolboxframe)

        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.toolboxframe.add(self.scroll)

        self.mainbox = gtk.VBox()
        self.scroll.add_with_viewport(self.mainbox)

        # viewer widgets
        viewerframe = gtk.Frame("Viewer Widgets")
        viewerframe.set_shadow_type(gtk.SHADOW_IN)
        self.mainbox.pack_start(viewerframe)
        viewerbox = gtk.VBox()
        viewerframe.add(viewerbox)

        self.tooltips = gtk.Tooltips()

        # camera position
        infoframe = gtk.Frame("Camera Info")
        infoframe.set_shadow_type(gtk.SHADOW_IN)
        viewerbox.pack_start(infoframe, fill=0, expand=0)
        infobox = gtk.VBox()
        infoframe.add(infobox)
        positionlabel = gtk.Label("Camera Position:")
        #self.tooltips.set_tip(positionlabel, "The position of the camera in world coordinates (pixel units)")
        infobox.pack_start(positionlabel,fill=0, expand=0)
        positiontable = gtk.Table(columns=3, rows=1)
        infobox.pack_start(positiontable,fill=0, expand=0)
        self.camera_x = gtk.Entry()
        self.camera_x.set_size_request(90,-1)
        self.camera_x.set_editable(0)
        positiontable.attach(self.camera_x,0,1,0,1)
        self.camera_y = gtk.Entry()
        self.camera_y.set_size_request(90,-1)
        self.camera_y.set_editable(0)
        positiontable.attach(self.camera_y,1,2,0,1)
        self.camera_z = gtk.Entry()
        self.camera_z.set_size_request(90,-1)
        self.camera_z.set_editable(0)
        positiontable.attach(self.camera_z,2,3,0,1)
        focalpointlabel = gtk.Label("Focal Point:")
        #self.tooltips.set_tip(focalpointlabel, "The position of the focal point in world coordinates (pixel units)")
        infobox.pack_start(focalpointlabel,fill=0, expand=0)
        focalpointtable = gtk.Table(columns=3, rows=1)
        infobox.pack_start(focalpointtable,fill=0, expand=0)
        self.fp_x = gtk.Entry()
        self.fp_x.set_size_request(90,-1)
        self.fp_x.set_editable(0)
        focalpointtable.attach(self.fp_x,0,1,0,1)
        self.fp_y = gtk.Entry()
        self.fp_y.set_size_request(90,-1)
        self.fp_y.set_editable(0)
        focalpointtable.attach(self.fp_y,1,2,0,1)
        self.fp_z = gtk.Entry()
        self.fp_z.set_size_request(90,-1)
        self.fp_z.set_editable(0)
        focalpointtable.attach(self.fp_z,2,3,0,1)
        viewuplabel = gtk.Label("View Up Vector:")
        #self.tooltips.set_tip(viewuplabel, "The vector that points up in the viewport")
        infobox.pack_start(viewuplabel,fill=0, expand=0)
        viewuptable = gtk.Table(columns=3, rows=1)
        infobox.pack_start(viewuptable,fill=0, expand=0)
        self.viewup_x = gtk.Entry()
        self.viewup_x.set_size_request(90,-1)
        self.viewup_x.set_editable(0)
        viewuptable.attach(self.viewup_x,0,1,0,1)
        self.viewup_y = gtk.Entry()
        self.viewup_y.set_size_request(90,-1)
        self.viewup_y.set_editable(0)
        viewuptable.attach(self.viewup_y,1,2,0,1)
        self.viewup_z = gtk.Entry()
        self.viewup_z.set_size_request(90,-1)
        self.viewup_z.set_editable(0)
        viewuptable.attach(self.viewup_z,2,3,0,1)
        distancetable = gtk.Table(columns=2, rows=1)
        infobox.pack_start(distancetable,fill=0, expand=0)
        distancelabel = gtk.Label("Distance:")
        #self.tooltips.set_tip(distancelabel, "The distance from the camera to the focal point")
        distancetable.attach(distancelabel,0,1,0,1)
        self.distance = gtk.Entry()
        self.distance.set_size_request(90,-1)
        self.distance.set_editable(0)
        distancetable.attach(self.distance,1,2,0,1)
        angletable = gtk.Table(columns=2, rows=1)
        infobox.pack_start(angletable,fill=0, expand=0)
        anglelabel = gtk.Label("View Angle:")
        #self.tooltips.set_tip(anglelabel, "The angle between the vectors from the camera to the focal point and from the camera to the top of the microstructure")
        angletable.attach(anglelabel,0,1,0,1)
        self.viewangle = gtk.Entry()
        self.viewangle.set_size_request(90,-1)
        self.viewangle.set_editable(0)
        angletable.attach(self.viewangle,1,2,0,1)
        printinfo = gtk.Button("Print Camera Info")
        gtklogger.connect(printinfo, 'clicked', self.printcam)
        self.tooltips.set_tip(printinfo, "Print the camera information in the console")
        infobox.pack_start(printinfo,fill=0, expand=0)

        # zoom - as in changing the viewing angle
        zoomframe = gtk.Frame("Zoom")
        zoomframe.set_shadow_type(gtk.SHADOW_IN)
        viewerbox.pack_start(zoomframe, fill=0, expand=0)
        zoombox = gtk.VBox()
        zoomframe.add(zoombox)
        buttonrow = gtk.HBox(homogeneous=1, spacing=2)
        zoombox.pack_start(buttonrow, expand=0, fill=1, padding=2)
        zinbutton = gtk.Button('Zoom In')
        self.tooltips.set_tip(zinbutton,"Decrease view angle to by given factor")
        buttonrow.pack_start(zinbutton, expand=0, fill=1)
        gtklogger.connect(zinbutton, 'clicked', self.zoomin)
        zoutbutton = gtk.Button('Zoom Out')
        self.tooltips.set_tip(zoutbutton, "Increase view angle by given factor")
        buttonrow.pack_start(zoutbutton, expand=0, fill=1)
        gtklogger.connect(zoutbutton, 'clicked', self.zoomout)
        zfillbutton = gtk.Button('Fill')
        self.tooltips.set_tip(zfillbutton, "Set view angle such that microstructure approximately fills viewport")
        buttonrow.pack_start(zfillbutton, expand=0, fill=1)
        gtklogger.connect(zfillbutton, 'clicked', self.zoomfill)
        factorrow = gtk.HBox()
        zoombox.pack_start(factorrow, expand=0, fill=0, padding=2)
        factorrow.pack_start(gtk.Label("Factor: "), expand=0, fill=0)
        self.zoomfactor = gtk.Entry()
        self.zoomfactor.set_editable(1)
        self.zoomfactor.set_size_request(80, -1)
        self.zoomfactor.set_text("1.5")
        self.tooltips.set_tip(self.zoomfactor, "Factor by which to shrink or magnify image")
        factorrow.pack_start(self.zoomfactor, expand=1, fill=1)        


        # Translation

        # dolly
        transframe = gtk.Frame("Translation")
        transframe.set_shadow_type(gtk.SHADOW_IN)
        viewerbox.pack_start(transframe, fill=0, expand=0)
        transbox = gtk.VBox()
        transframe.add(transbox)
        dollyrow = gtk.HBox(homogeneous=1, spacing=2)
        transbox.pack_start(dollyrow, expand=0, fill=1, padding=2)
        inbutton = gtk.Button('Dolly In')
        self.tooltips.set_tip(inbutton,"Translate camera towards focal point by given factor")
        dollyrow.pack_start(inbutton, expand=0, fill=1)
        gtklogger.connect(inbutton, 'clicked', self.dollyin)
        outbutton = gtk.Button('Dolly Out')
        self.tooltips.set_tip(outbutton, "Translate camera away from focal point by given factor")
        dollyrow.pack_start(outbutton, expand=0, fill=1)
        gtklogger.connect(outbutton, 'clicked', self.dollyout)
        fillbutton = gtk.Button('Fill')
        self.tooltips.set_tip(fillbutton, "Set camera position such that microstructure approximately fills viewport")
        dollyrow.pack_start(fillbutton, expand=0, fill=1)
        gtklogger.connect(fillbutton, 'clicked', self.dollyfill)
        factorrow = gtk.HBox()
        transbox.pack_start(factorrow, expand=0, fill=0, padding=2)
        factorrow.pack_start(gtk.Label("Factor: "), expand=0, fill=0)
        self.dollyfactor = gtk.Entry()
        self.dollyfactor.set_editable(1)
        self.dollyfactor.set_size_request(80, -1)
        self.dollyfactor.set_text("1.5")
        self.tooltips.set_tip(self.dollyfactor, "Factor by which to multiply distance from camera to focal point")
        factorrow.pack_start(self.dollyfactor, expand=1, fill=1)

        # track
        trackrow = gtk.HBox(homogeneous=1, spacing=2)
        transbox.pack_start(trackrow, expand=0, fill=1, padding=2)
        horizbutton = gtk.Button('Horizontal')
        self.tooltips.set_tip(horizbutton,"Shift camera and focal point horizontally")
        trackrow.pack_start(horizbutton, expand=0, fill=1)
        gtklogger.connect(horizbutton, 'clicked', self.trackh)
        vertbutton = gtk.Button('Vertical')
        self.tooltips.set_tip(vertbutton, "Shift camera and focal point vertically")
        trackrow.pack_start(vertbutton, expand=0, fill=1)
        gtklogger.connect(vertbutton, 'clicked', self.trackv)
        recenterbutton = gtk.Button('Recenter')
        self.tooltips.set_tip(recenterbutton, "Recenter the microstructure in the viewport")
        trackrow.pack_start(recenterbutton, expand=0, fill=1)
        gtklogger.connect(recenterbutton, 'clicked', self.recenter)        
        distrow = gtk.HBox()
        transbox.pack_start(distrow, expand=0, fill=0, padding=2)
        distrow.pack_start(gtk.Label("Distance: "), expand=0, fill=0)
        self.trackdist = gtk.Entry()
        self.trackdist.set_editable(1)
        self.trackdist.set_size_request(80, -1)
        self.trackdist.set_text("10.0")
        self.tooltips.set_tip(self.trackdist, "Distance by which to track camera in units of pixels")
        distrow.pack_start(self.trackdist, expand=1, fill=1)
        label = gtk.Label("Dolly: Right Mouse Button\nTrack: Middle Mouse Button")
        transbox.pack_start(label)

        #rotate
        rotateframe = gtk.Frame("Rotation")
        rotateframe.set_shadow_type(gtk.SHADOW_IN)
        viewerbox.pack_start(rotateframe, fill=0, expand=0)
        rotatebox = gtk.VBox()
        rotateframe.add(rotatebox)
        rotobjrow = gtk.HBox(homogeneous=1, spacing=2)
        rotatebox.pack_start(rotobjrow, expand=0, fill=1, padding=2)
        rollbutton = gtk.Button('Roll')
        self.tooltips.set_tip(rollbutton,"Rotate about direction of projection")
        rotobjrow.pack_start(rollbutton, expand=0, fill=1)
        gtklogger.connect(rollbutton, 'clicked', self.roll)
        azbutton = gtk.Button('Azimuth')
        self.tooltips.set_tip(azbutton, "Rotate about view up vector centered at focal point")
        rotobjrow.pack_start(azbutton, expand=0, fill=1)
        gtklogger.connect(azbutton, 'clicked', self.azimuth)
        elbutton = gtk.Button('Elevation')
        self.tooltips.set_tip(elbutton, "Rotate about cross product of direction of projection and view up vector centered at focal point")
        rotobjrow.pack_start(elbutton, expand=0, fill=1)
        gtklogger.connect(elbutton, 'clicked', self.elevation)
        rotcamrow = gtk.HBox(homogeneous=1, spacing=2)
        rotatebox.pack_start(rotcamrow, expand=0, fill=1, padding=2)
        yawbutton = gtk.Button('Yaw')
        self.tooltips.set_tip(yawbutton,"Rotate about view up vector centered at camera position")
        rotcamrow.pack_start(yawbutton, expand=0, fill=1)
        gtklogger.connect(yawbutton, 'clicked', self.yaw)
        pitchbutton = gtk.Button('Pitch')
        self.tooltips.set_tip(pitchbutton,"Rotate about cross product of direction of projection and view up vector centered at camera position")
        rotcamrow.pack_start(pitchbutton, expand=0, fill=1)
        gtklogger.connect(pitchbutton, 'clicked', self.pitch)
        anglerow = gtk.HBox()
        rotatebox.pack_start(anglerow, expand=0, fill=0, padding=2)
        anglerow.pack_start(gtk.Label("Angle: "), expand=0, fill=0)
        self.angle = gtk.Entry()
        self.angle.set_editable(1)
        self.angle.set_size_request(80, -1)
        self.angle.set_text("10.0")
        self.tooltips.set_tip(self.angle,"Angle in degrees by which to rotate by")
        anglerow.pack_start(self.angle, expand=1, fill=1)


        #clipping planes
        clippingframe = gtk.Frame("Clipping Range")
        clippingframe.set_shadow_type(gtk.SHADOW_IN)
        viewerbox.pack_start(clippingframe, fill=0, expand=0)
        clippingbox = gtk.VBox()
        clippingframe.add(clippingbox)
        self.clippingadj = gtk.Adjustment(value=100, lower=0, upper=100, step_incr=-1, page_incr=-5, page_size=0)
        gtklogger.connect(self.clippingadj, 'value_changed', self.setclipping)
        clippingscale = gtk.HScale(self.clippingadj)
        clippingscale.set_update_policy(gtk.UPDATE_DELAYED)
        self.tooltips.set_tip(clippingscale,"Adjust the near clipping plane to view cross section")
        clippingbox.pack_start(clippingscale)

        #opacity
        opacityframe = gtk.Frame("Opacity")
        opacityframe.set_shadow_type(gtk.SHADOW_IN)
        viewerbox.pack_start(opacityframe, fill=0, expand=0)
        opacitybox = gtk.VBox()
        opacityframe.add(opacitybox)
        self.opacityadj = gtk.Adjustment(value=100, lower=0, upper=100, step_incr=-1, page_incr=-5, page_size=0)
        gtklogger.connect(self.opacityadj, 'value_changed', self.setopacity)
        opacityscale = gtk.HScale(self.opacityadj)
        opacityscale.set_update_policy(gtk.UPDATE_DELAYED)
        self.tooltips.set_tip(opacityscale,"Adjust the opacity of the microstructure")
        opacitybox.pack_start(opacityscale)

        # save and restore
        saverestoreframe = gtk.Frame("Save and Restore Views")
        saverestoreframe.set_shadow_type(gtk.SHADOW_IN)
        viewerbox.pack_start(saverestoreframe, fill=0, expand=0)
        saverestorebox = gtk.VBox()
        saverestoreframe.add(saverestorebox)
        viewtable = gtk.Table(columns=2, rows=2)
        saverestorebox.pack_start(viewtable, fill=0, expand=0)
        saveviewbutton = gtk.Button("Save View:")
        self.tooltips.set_tip(saveviewbutton,"Save the current view settings")
        gtklogger.connect(saveviewbutton, 'clicked', self.saveview)
        viewtable.attach(saveviewbutton, 0,1,0,1)
        self.viewname = gtk.Entry()
        self.viewname.set_editable(1)
        self.viewname.set_size_request(80,-1)
        self.tooltips.set_tip(self.viewname,"Enter a name for the current view")
        viewtable.attach(self.viewname,1,2,0,1)
        setviewlabel = gtk.Label("Set View:")
        viewtable.attach(setviewlabel, 0,1,1,2)
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        self.viewmenu = gtk.ComboBox(liststore)
        cell = gtk.CellRendererText()
        self.viewmenu.pack_start(cell, True)
        self.viewmenu.add_attribute(cell, 'text', 0)
        #self.tooltips.set_tip(self.viewmenu,"Restore a saved view")
        # menu items filled in later when saved_views is initialized
        self.signal = gtklogger.connect(self.viewmenu, 'changed',
                                        self.setview)
        viewtable.attach(self.viewmenu, 1,2,1,2)


        # end viewer widgets

        # voxel info widgets
        voxelinfoframe = gtk.Frame("Voxel Info Widgets")
        voxelinfoframe.set_shadow_type(gtk.SHADOW_IN)
        self.mainbox.pack_start(voxelinfoframe)
        voxelinfobox = gtk.VBox()
        voxelinfoframe.add(voxelinfobox)
        voxelinfotable = gtk.Table(rows=7,columns=2)
        voxelinfobox.pack_start(voxelinfotable)
        label = gtk.Label('x=')
        label.set_alignment(1.0, 0.5)
        voxelinfotable.attach(label, 0,1, 0,1, xpadding=5, xoptions=gtk.FILL)
        self.xtext = gtk.Entry()
        self.xtext.set_size_request(80, -1)
        voxelinfotable.attach(self.xtext, 1,2, 0,1,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        label = gtk.Label('y=')
        label.set_alignment(1.0, 0.5)
        voxelinfotable.attach(label, 0,1, 1,2, xpadding=5, xoptions=gtk.FILL)
        self.ytext = gtk.Entry()
        self.ytext.set_size_request(80, -1)
        voxelinfotable.attach(self.ytext, 1,2, 1,2,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        label = gtk.Label('z=')
        label.set_alignment(1.0, 0.5)
        voxelinfotable.attach(label, 0,1, 2,3, xpadding=5, xoptions=gtk.FILL)
        self.ztext = gtk.Entry()
        self.ztext.set_size_request(80, -1)
        voxelinfotable.attach(self.ztext, 1,2, 2,3,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        self.xtsignal = gtklogger.connect(self.xtext, 'changed',
                                          self.voxinfoChanged)
        self.ytsignal = gtklogger.connect(self.ytext, 'changed',
                                          self.voxinfoChanged)
        self.ztsignal = gtklogger.connect(self.ztext, 'changed',
                                          self.voxinfoChanged)
       
        box = gtk.HBox(homogeneous=True, spacing=2)
        self.updatebutton = gtk.Button(gtk.STOCK_REFRESH) #gtkutils.stockButton(gtk.STOCK_REFRESH, 'Update')
        box.pack_start(self.updatebutton, expand=1, fill=1)
        gtklogger.connect(self.updatebutton, 'clicked', self.updateVoxButtonCB)
        self.clearbutton = gtk.Button(gtk.STOCK_CLEAR) #gtkutils.stockButton(gtk.STOCK_CLEAR, 'Clear')
        box.pack_start(self.clearbutton, expand=1, fill=1)
        gtklogger.setWidgetName(self.clearbutton, "Clear")
        gtklogger.connect(self.clearbutton, 'clicked', self.clearVoxButtonCB)
        voxelinfotable.attach(box, 0,2,3,4,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
        label = gtk.Label('red=')
        label.set_alignment(1.0, 0.5)
        voxelinfotable.attach(label, 0,1, 4,5, xpadding=5, xoptions=gtk.FILL)
        self.redtext = gtk.Entry()
        self.redtext.set_size_request(80, -1)
        voxelinfotable.attach(self.redtext, 1,2, 4,5,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        label = gtk.Label('green=')
        label.set_alignment(1.0, 0.5)
        voxelinfotable.attach(label, 0,1, 5,6, xpadding=5, xoptions=gtk.FILL)
        self.greentext = gtk.Entry()
        self.greentext.set_size_request(80, -1)
        voxelinfotable.attach(self.greentext, 1,2, 5,6,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        label = gtk.Label('blue=')
        label.set_alignment(1.0, 0.5)
        voxelinfotable.attach(label, 0,1, 6,7, xpadding=5, xoptions=gtk.FILL)
        self.bluetext = gtk.Entry()
        self.bluetext.set_size_request(80, -1)
        voxelinfotable.attach(self.bluetext, 1,2, 6,7,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        currentVoxel = None

        
        # voxel select widgets
##         voxelselectframe = gtk.Frame("Voxel Select Widgets")
##         voxelselectframe.set_shadow_type(gtk.SHADOW_IN)
##         self.mainbox.pack_start(voxelselectframe)
##         voxelselectbox = gtk.VBox()
##         voxelselectframe.add(voxelselectbox)
##         button = gtk.Button("Hello World")
##         voxelselectbox.pack_start(button)

        self.saveimage = gtk.Button("save image")
        gtklogger.connect(self.saveimage, 'clicked', self.saveimageCB)
        self.mainbox.pack_start(self.saveimage)
      
        
    def show(self):
        
        # show areas set up in init
        self.panes.show()
        self.panes.set_position(350)
        self.canvas.show()
        self.toolboxframe.show()
        self.scroll.show()
        self.mainbox.show_all()
        self.gtk.show()


    def updateCameraInfo(self):
        x,y,z = self.camera.GetPosition()
        self.camera_x.set_text("%f" %x)
        self.camera_y.set_text("%f" %y)
        self.camera_z.set_text("%f" %z)        
        x,y,z = self.camera.GetFocalPoint()
        self.fp_x.set_text("%f" %x)
        self.fp_y.set_text("%f" %y)
        self.fp_z.set_text("%f" %z)
        x,y,z = self.camera.GetViewUp()
        self.viewup_x.set_text("%f" %x)
        self.viewup_y.set_text("%f" %y)
        self.viewup_z.set_text("%f" %z)
        dist = self.camera.GetDistance()
        self.distance.set_text("%f" %dist)
        angle = self.camera.GetViewAngle()
        self.viewangle.set_text("%f" %angle)


    # ZOOM CALLBACK FUNCTIONS


    def zoomin(self, *args):
        zoomfactor = float(self.zoomfactor.get_text())
        self.zoombyfactor(zoomfactor)


    def zoomout(self, *args):
        zoomfactor = 1./float(self.zoomfactor.get_text())
        self.zoombyfactor(zoomfactor)


    def zoomfill(self, *args):
        dist = self.camera.GetDistance()
        # dont understand why dividing height by 2 here gives wrong behavior
        angle = atan( (self.height*1.25) / (dist - self.depth/2) ) * 180./pi
        self.camera.SetViewAngle(angle)
        self.viewchange()


    def zoombyfactor(self, factor):
        self.camera.Zoom(factor)
        self.viewchange()


    # TRANSLATION CALLBACK FUNCTIONS

    def dollyin(self, *args):
        dollyfactor = float(self.dollyfactor.get_text())
        self.camera.Dolly(dollyfactor)
        self.viewchange()


    def dollyout(self, *args):
        dollyfactor = 1./float(self.dollyfactor.get_text())
        self.camera.Dolly(dollyfactor)
        self.viewchange()


    def dollyfill(self, *args):
        # todo, this fills based on matching the height of the volume
        # to the height of the window.  Ideally it should find either
        # the height of the view or the width of the view and match
        # that to the window.
        angle = (float(self.camera.GetViewAngle())/2)*(pi/180)
        distance = ((self.height*1.25)/2)/tan(angle) + self.depth/2
        currentdistance = self.camera.GetDistance()
        dollyfactor = currentdistance/distance
        self.camera.Dolly(dollyfactor)        
        self.viewchange()


    def trackh(self, *args):
        d = float(self.trackdist.get_text())
        # Get the normalized vector which is horizontal on the screen
        (yp0,yp1,yp2) = self.camera.GetViewUp()
        (zp0,zp1,zp2) = self.camera.GetDirectionOfProjection()
        xp0=-zp1*yp2+yp1*zp2
        xp1=-zp2*yp0+yp2*zp0
        xp2=-zp0*yp1+yp0*zp1

        self.canvas.Track(xp0*d,xp1*d,xp2*d)
        self.viewchange()


    def trackv(self, *args):
        d = float(self.trackdist.get_text())
        (yp0,yp1,yp2) = self.camera.GetViewUp()
        self.canvas.Track(yp0*d,yp1*d,yp2*d)
        self.viewchange()


    def recenter(self, *args):
        d = self.camera.GetDistance()
        dop = self.camera.GetDirectionOfProjection()
        fp = (self.width/2, self.height/2, self.depth/2)
        self.camera.SetFocalPoint(fp)
        self.camera.SetPosition(fp[0]-d*dop[0],fp[1]-d*dop[1],fp[2]-d*dop[2])
        self.viewchange()


    # ROTATION CALLBACKS

    def roll(self, *args):
        angle = float(self.angle.get_text())
        self.camera.Roll(angle)
        self.viewchange()

    def azimuth(self, *args):
        angle =  float(self.angle.get_text())
        self.camera.Azimuth(angle)
        self.viewchange()
        
    def elevation(self, *args):
        angle =  float(self.angle.get_text())
        self.camera.Elevation(angle)
        self.viewchange()

    def yaw(self, *args):
        angle =  float(self.angle.get_text())
        self.camera.Yaw(angle)
        self.viewchange()

    def pitch(self, *args):
        angle =  float(self.angle.get_text())
        self.camera.Pitch(angle)
        self.viewchange()

    # when incorporated into oof, probably want to use switchboard for this
    def viewchange(self):
        self.camera.OrthogonalizeViewUp()
        self.canvas.ResetClippingRange()
        self.canvas.Render()
        self.viewmenu.set_active(-1)
        

    # SAVE AND RESTORE VIEWS

    def setview(self, *args):
        viewname = self.get_active_text(self.viewmenu)

        try:
            view = self.saved_views[viewname]
            
            self.camera.SetPosition(view.pos)
            self.camera.SetFocalPoint(view.focal)
            self.camera.SetViewUp(view.up)
            self.camera.SetViewAngle(view.angle)
            self.ren.ResetCameraClippingRange()
            self.clippingadj.set_value(view.clip)
            self.opacityadj.set_value(view.opacity)

            self.canvas.Render()

        except KeyError:
            pass


    def saveview(self, *args):
        viewname = self.viewname.get_text()

        pos = self.camera.GetPosition()
        focal = self.camera.GetFocalPoint()
        up = self.camera.GetViewUp()
        angle = self.camera.GetViewAngle()
        clip = float(self.clippingadj.get_value())
        opacity = float(self.opacityadj.get_value())

        self.saved_views[viewname]=View(pos,focal,up,angle,clip,opacity)
        self.viewmenu.append_text(viewname)


    # CLIPPING AND OPACITY

    # todo: eliminate the "padding" in the clipping range. see
    # vtkRenderer.cxx for the surprisingly complicated calculation
    def setclipping(self, *args):
        adj = float(self.clippingadj.get_value())
        (near, far) = self.canvas.GetClippingRange()
        newnear = far - (far-near)*(adj/100)
        self.camera.SetClippingRange(newnear,far)
        self.canvas.Render()

        
    def setopacity(self, *args):
        adj = float(self.opacityadj.get_value())
        value = 1-log(101-adj)/log(101)
        self.opacity.AddSegment(0.0,value,255,value)
        self.canvas.Render()


    # VOXEL INFO

    def voxinfoChanged(self, *args):
        pass

    def updateVoxButtonCB(self, *args):
        x = int(self.xtext.get_text())
        y = int(self.ytext.get_text())
        z = int(self.ztext.get_text())
        pointid = self.image.FindPoint(x,y,z)
        self.setRGB(pointid)
        self.DrawVoxelFrame([x,y,z])

    def setRGB(self, id):
        num_components = self.image.GetNumberOfScalarComponents()
        if num_components == 1:
            r = g = b = self.image.GetPointData().GetScalars().GetComponent(id,0)
        if num_components == 3:
            r = self.image.GetPointData().GetScalars().GetComponent(id,0)
            g = self.image.GetPointData().GetScalars().GetComponent(id,1)
            b = self.image.GetPointData().GetScalars().GetComponent(id,2)
        self.redtext.set_text(str(r))
        self.greentext.set_text(str(g))
        self.bluetext.set_text(str(b))


    def clearVoxButtonCB(self, *args):
        self.xtext.set_text("")
        self.ytext.set_text("")
        self.ztext.set_text("")
        self.redtext.set_text("")
        self.bluetext.set_text("")
        self.greentext.set_text("")
        if self.cubeActor != None:
            self.ren.RemoveActor(self.cubeActor)
            self.cubeActor = None
            self.canvas.Render()

    def get_active_text(self, combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]


    def destroy(self, widget, data=None):
        gtk.main_quit()

        
    def printcam(self, *args):
        camera = self.canvas.GetRenderer().GetActiveCamera()
        print camera

    def DrawVoxelFrame(self,point):

        if self.cubeActor != None:            
            self.ren.RemoveActor(self.cubeActor)
            self.cubeActor = None
            self.canvas.Render()
        
        x,y,z=point

##         voxelPoints = vtk.vtkPoints()
##         voxelPoints.SetNumberOfPoints(8)
##         inc = (0,1)
##         for i in inc:
##             for j in inc:
##                 for k in inc:
##                     voxelPoints.InsertPoint(i*4+j*2+k,x+inc[i],y+inc[j],z+inc[k])
##         aVoxel = vtk.vtkVoxel()
##         for i in xrange(8):
##             aVoxel.GetPointIds().SetId(i, i)
##         aVoxelGrid = vtk.vtkUnstructuredGrid()
##         aVoxelGrid.Allocate(1, 1)
##         aVoxelGrid.InsertNextCell(aVoxel.GetCellType(), aVoxel.GetPointIds())
##         aVoxelGrid.SetPoints(voxelPoints)

##         outline = vtk.vtkOutlineFilter()
##         outline.SetInputConnection(aVoxelGrid.GetProducerPort())

        # different way of drawing the selected voxels...

        cube = vtk.vtkCubeSource()
        cube.SetBounds(x,x+1,y,y+1,z,z+1)
        
        cubeMapper = vtk.vtkPolyDataMapper()
        cubeMapper.SetInput(cube.GetOutput()) #outline.GetOutputPort())
        self.cubeActor = vtk.vtkActor()
        self.cubeActor.SetMapper(cubeMapper)
        self.cubeActor.GetProperty().SetDiffuseColor(0, 0, 1)
        self.cubeActor.GetProperty().SetOpacity(1.0)
        self.cubeActor.GetProperty().SetRepresentationToSurface()

        # third way to draw cube - a one voxel image - for some
        # reason, this doesn't show up at all
##         cube = vtk.vtkImageData()
##         data = vtk.vtkUnsignedCharArray()
##         data.InsertNextValue(1)
##         cube.SetOrigin(x,y,z)
##         cube.SetExtent(0,1,0,1,0,1)
##         cube.GetPointData().SetScalars(data)
##         cube.Update()

##         mapper = vtk.vtkFixedPointVolumeRayCastMapper()
##         mapper.IntermixIntersectingGeometryOn()
##         mapper.SetInput(cube)

##         cubeOpacity = vtk.vtkPiecewiseFunction()
##         cubeOpacity.AddSegment(0,.5,255,.5)

##         cubeColor = vtk.vtkColorTransferFunction()
##         cubeColor.AddRGBSegment(0,0,0,1,255,0,0,1)
        
##         cubeProperty = vtk.vtkVolumeProperty()
##         cubeProperty.SetScalarOpacity(cubeOpacity)
##         cubeProperty.SetColor(cubeColor)

##         self.cubeActor = vtk.vtkVolume()
##         self.cubeActor.SetMapper(mapper)
##         self.cubeActor.SetProperty(cubeProperty)

        self.ren.AddActor(self.cubeActor)
        self.canvas.Render()


    def saveimageCB(self, *args):
        w2i = vtk.vtkWindowToImageFilter()
        writer = vtk.vtkTIFFWriter()
        renWin = self.canvas.GetRenderWindow()
        w2i.SetInput(renWin)
        print renWin
        renWin.Render()
        w2i.Update()
        print w2i.GetOutput()
        writer.SetInputConnection(w2i.GetOutputPort())
        writer.SetFileName("image.tif")
        writer.Write()

    def import3DImage(self,type,prefix,extent):

        importer = ImageImporter(type,prefix,extent)
        self.ren = importer.GetRenderer()
        self.image = importer.GetImage()
        self.camera = self.ren.GetActiveCamera()
        self.opacity = importer.GetOpacityFunction()

        d, width, d, height, d, depth = self.image.GetExtent()
        self.width = float(width)
        self.height = float(height)
        self.depth = float(depth)        

        self.canvas.GetRenderWindow().AddRenderer(self.ren)
        self.canvas.UpdateRenderer(0,0)
        self.canvas.ResetClippingRange()
        self.canvas.SetPickerImage(self.image)
        self.SetDefaultViews()

        # this causes the BadWindow Xerror on a mac - not clear
        # whether this is related to the problem where two actors
        # don't show if one of them is an image - also gives BadWindow
        # error on linux - it's due to calling canvas.Render() before
        # the window is drawn.
        #print "right before draw voxel"
        #self.DrawVoxelFrame((0,0,4))
        #print "right after draw voxel"
        

    def SetDefaultViews(self):
        distance = self.camera.GetDistance()
        center = (self.width/2, self.height/2, self.depth/2)
        y_up = (0,1,0)
        nz_up = (0,0,-1)
        pz_up = (0,0,1)

        self.saved_views["Front"]=View( (self.width/2, self.height/2, distance+self.depth/2),center,y_up)
        self.saved_views["Back"]=View( (self.width/2, self.height/2, -distance+self.depth/2),center,y_up)
        self.saved_views["Left"]=View( (-distance+self.width/2, self.height/2, self.depth/2),center,y_up)
        self.saved_views["Right"]=View( (distance+self.width/2, self.height/2, self.depth/2),center,y_up)
        self.saved_views["Top"]=View( (self.width/2, distance+self.height/2, self.depth/2),center,nz_up)
        self.saved_views["Bottom"]=View( (self.width/2, -distance+self.height/2, self.depth/2),center,pz_up)
        views = self.saved_views.keys()
        for view in views:
            self.viewmenu.append_text(view)



if __name__ == "__main__":

    demo = Demo3D()
    demo.show()
    #demo.import3DImage('pnm','pgm/slice.pgm',[0,99,0,99,0,99])
    #demo.import3DImage('pnm','mini/checkerboard6.pgm',[0,5,0,5,0,5])
    #demo.import3DImage('jpg','mini/colorchecker.jpg',[0,4,0,4,0,4])
    #demo.import3DImage('jpg','jpeg/slice.jpg',[0,99,0,99,0,99])
    demo.import3DImage('tif','../TEST3D/ms_data/5color/slice%i.tif',[0,20,0,20,0,20])

    gtk.main()

