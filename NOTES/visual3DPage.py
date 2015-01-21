# To integrate this page into oof2, copy this file into SRC/engine/IO/GUI
# and modify DIR.py and initialize.py accordingly.
# I used python-gtkglext1 1.1.0-1 (Maintained by Robert Ancell)
# and python-vtk 5.0.1-1 (Maintained by A. Maitland Bottoms)
# on an Ubuntu 6.10 - the Edgy Eft - released in October 2006.

from oof2.engine import skeletoncontext
from oof2.common.IO import whoville
from oof2.common.IO.GUI import oofGUI
from oof2.common.IO.GUI import whowidget
import math
			
VTKtest=True
if VTKtest:
    import vtk
    from vtk.util.colors import peacock, hot_pink
    import time

# The user interface for this demo oof2 page is based on a
# sample code bundled with pygtkglext-1.1.0 (see Shapes.py comment below)

'''
Shapes.py

This program is based upon the shapes.c demo by Naofumi. This is not a
straight conversion from C to Python. The original idea of displaying
different shapes have been retained but here a range of widgets are
used to demonstrate the use of OpenGL in conjunction with a variety of
Gtk+ widgets. You can use sliders to rotate the object and change colours
for the foreground and background using the standard Gtk+ colour
selection dialog.

Alif Wahid, March, 2003
<awah005@users.sourceforge.net>
'''

import sys

import pygtk
pygtk.require('2.0')
from gtk.gtkgl.apputils import *

from OpenGL.GLE import *

# Implement the GLScene interface
# to have a shape rendered.

class Shapes(GLScene,
             GLSceneButton,
             GLSceneButtonMotion):
    
    def __init__(self):
        GLScene.__init__(self,
                         gtk.gdkgl.MODE_RGB   |
                         gtk.gdkgl.MODE_DEPTH |
                         gtk.gdkgl.MODE_DOUBLE)
        
        self.light_ambient = [0.0, 1.0, 0.0, 1.0]
        self.light_diffuse = [1.0, 1.0, 1.0, 1.0]
        self.light_specular = [1.0, 1.0, 1.0, 1.0]
        self.light_position = [1.0, 1.0, 1.5, 0.0]
        
        self.mat_ambient = [0.2, 0.2, 0.2, 1.0]
        self.mat_diffuse = [0.8, 0.8, 0.8, 1.0]
        self.mat_specular = [1.0, 0.0, 1.0, 1.0]
        self.mat_shininess = 50.0
        
        self.depth = 105.0
        
        self.rotx = 0
        self.roty = 0
        self.rotz = 0
        
        self.beginx = 0
        self.beginy = 0
        
        # Empirically derived value for the background
        # to make it the same colour as the background
        # of all the widgets. This way the shapes will
        # appear as though they have been drawn on top
        # of the current window. It's specific to the
        # default Gtk+-2.2 theme only though. You can
        # also assign the current colour of any part of
        # the window from the colourselection dialog
        # by using the eye dropper. That's how I derived
        # at these values for guiBg.
        self.guiBg = [0.8627, 0.8549, 0.8353]
        self.colourFg = [1.0, 0.0, 0.0]
        self.colourBg = self.guiBg
        
        self.is_solid = False
        
        self.__drawShape = { 'Helicoid'     : self.__draw_helicoid,
                             'Teapot'       : self.__draw_teapot,
                             'Torus'        : self.__draw_torus,
                             'Sphere'       : self.__draw_sphere,
                             'Cube'         : self.__draw_cube,
                             'Cone'         : self.__draw_cone,
                             'Tetrahedron'  : self.__draw_tetrahedron,
                             'Octahedron'   : self.__draw_octahedron,
                             'Dodecahedron' : self.__draw_dodecahedron,
                             'Icosahedron'  : self.__draw_icosahedron,
                             'Skeleton'         : self.__draw_skeleton,
                             'Skeleton(wrap x)' : self.__draw_skeletonwrapx,
                             'Skeleton(wrap y)' : self.__draw_skeletonwrapy,
                             'Skeleton(torus)'  : self.__draw_skeletonwrapxy }
        self.currentShape = 'Sphere'
        self.availableShapes = self.__drawShape.keys()

        self.GLlists=None

    def buildGLlists(self,skel):
        sx=skel.MS.size()[0]
        sy=skel.MS.size()[1]
        sscale=sx
        if sscale<sy:
            sscale=sy
        sscale=20.0/sscale
        
        self.GLlists=[]
        self.GLlists.append(glGenLists(1))
        glNewList(self.GLlists[0], GL_COMPILE)
        for el in skel.elements:
            glBegin(GL_LINE_LOOP)
            for nd in el.nodes:
                glVertex3f(sscale*nd.position().x,
                           sscale*nd.position().y,
                           0)
            glEnd()
        glEndList()

        self.GLlists.append(glGenLists(2))
        glNewList(self.GLlists[1], GL_COMPILE)
        for el in skel.elements:
            glBegin(GL_LINE_LOOP)
            for nd in el.nodes:
                theta=2*math.pi*nd.position().x/sx
                radius=sscale*sx/(2.0*math.pi)
                glVertex3f(radius*math.cos(theta),
                           sscale*nd.position().y,
                           radius*math.sin(theta))
            glEnd()
        glEndList()

        self.GLlists.append(glGenLists(3))
        glNewList(self.GLlists[2], GL_COMPILE)
        for el in skel.elements:
            glBegin(GL_LINE_LOOP)
            for nd in el.nodes:
                theta=2*math.pi*nd.position().y/sy
                radius=sscale*sy/(2.0*math.pi)
                glVertex3f(sscale*nd.position().x,
                           radius*math.cos(theta),
                           radius*math.sin(theta))
            glEnd()
        glEndList()

        self.GLlists.append(glGenLists(4))
        glNewList(self.GLlists[3], GL_COMPILE)
        for el in skel.elements:
            glBegin(GL_LINE_LOOP)
            for nd in el.nodes:
                theta=2*math.pi*nd.position().y/sy
                radius=sscale*sy/(2.0*math.pi)
                ry=radius*math.cos(theta)
                R=sscale*sx/(2.0*math.pi)+radius+ry
                theta2=2*math.pi*nd.position().x/sx
                glVertex3f(R*math.cos(theta2),
                           R*math.sin(theta2),
                           radius*math.sin(theta))
            glEnd()
        glEndList()

    def __draw_skeleton(self):
        if self.GLlists==None:
            return
        glPushMatrix()
        glCallList(self.GLlists[0])
        glPopMatrix()
    def __draw_skeletonwrapx(self):
        if self.GLlists==None:
            return
        glPushMatrix()
        glCallList(self.GLlists[1])
        glPopMatrix()
    def __draw_skeletonwrapy(self):
        if self.GLlists==None:
            return
        glPushMatrix()
        glCallList(self.GLlists[2])
        glPopMatrix()
    def __draw_skeletonwrapxy(self):
        if self.GLlists==None:
            return
        glPushMatrix()
        glCallList(self.GLlists[3])
        glPopMatrix()

    # Private methods that are used in the expose
    # method in a transparent manner to provide the
    # underlying rendering for a specific shape.

    def __draw_icosahedron(self):
        glPushMatrix()
        glScalef(12.0, 12.0, 12.0)
        gtk.gdkgl.draw_icosahedron(self.is_solid)
        glPopMatrix()
    
    def __draw_dodecahedron(self):
        glPushMatrix()
        glScalef(10.0, 10.0, 10.0)
        gtk.gdkgl.draw_dodecahedron(self.is_solid)
        glPopMatrix()
    
    def __draw_octahedron(self):
        glPushMatrix()
        glScalef(12.0, 12.0, 12.0)
        gtk.gdkgl.draw_octahedron(self.is_solid)
        glPopMatrix()
    
    def __draw_tetrahedron(self):
        glPushMatrix()
        glScalef(12.0, 12.0, 12.0)
        gtk.gdkgl.draw_tetrahedron(self.is_solid)
        glPopMatrix()
    
    def __draw_cone(self):
        gtk.gdkgl.draw_cone(self.is_solid, 6.0, 12.0, 30, 30)
    
    def __draw_cube(self):
        gtk.gdkgl.draw_cube(self.is_solid, 12)
    
    def __draw_helicoid(self):
        gleSetJoinStyle(TUBE_NORM_EDGE | TUBE_JN_ANGLE | TUBE_JN_CAP)
        gleHelicoid(1.0, 5.0, 1.0, -15.0, 6.0, None, None, 0.0, 1800.0)
    
    def __draw_teapot(self):
        gtk.gdkgl.draw_teapot(self.is_solid, 11.0)
    
    def __draw_torus(self):
        gtk.gdkgl.draw_torus(self.is_solid, 3.0, 12.0, 30, 30)
    
    def __draw_sphere(self):
        gtk.gdkgl.draw_sphere(self.is_solid, 12.0, 30, 30);
    
    # GLSceneInterface implementation.
    def init(self):
        glClearDepth(1.0)
        glClearColor(self.colourBg[0], self.colourBg[1], self.colourBg[2], 0.0)
        glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
        
        # The material properties are constant at this
        # stage, but if they need to be user selectable
        # then it'll be better to move these 4 calls
        # to the 'expose' method. That way everytime
        # the scene is rendered any change in materials
        # will be automatically detected without the
        # need for calling 'realize'.
        glMaterial(GL_FRONT, GL_AMBIENT,   self.mat_ambient)
        glMaterial(GL_FRONT, GL_DIFFUSE,   self.mat_diffuse)
        glMaterial(GL_FRONT, GL_SPECULAR,  self.mat_specular)
        glMaterial(GL_FRONT, GL_SHININESS, self.mat_shininess)
        
        glLight(GL_LIGHT0, GL_AMBIENT,  self.light_ambient)
        glLight(GL_LIGHT0, GL_DIFFUSE,  self.light_diffuse)
        glLight(GL_LIGHT0, GL_SPECULAR, self.light_specular)
        glLight(GL_LIGHT0, GL_POSITION, self.light_position)
        
        glLightModel(GL_LIGHT_MODEL_AMBIENT, self.light_ambient)
        glShadeModel(GL_SMOOTH)
        
        glDepthFunc(GL_LESS)
        
        glFrontFace(GL_CW)
        
        glEnable(GL_AUTO_NORMAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
    
    def display(self, width, height):
        # Set the background colour first as the user has
        # the option of changing it, so we need to take that
        # into account during every expose event.
        glClearColor(self.colourBg[0], self.colourBg[1], self.colourBg[2], 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -self.depth)
        glRotate(self.rotx, 1, 0, 0)
        glRotate(self.roty, 0, 1, 0)
        glRotate(self.rotz, 0, 0, 1)
        
        # Set the foreground colour as the user has
        # the option of changing it, so we need to take that
        # into account during every expose event.
        glColor(self.colourFg)
        self.__drawShape[self.currentShape]()
    
    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Calculate left/right and top/bottom clipping planes based on
        # the smallest square viewport.
        a = 13.0/min(width, height)
        clipping_planes = (a*width, a*height)
        # Setup the projection
        glFrustum(-clipping_planes[0], clipping_planes[0],
                  -clipping_planes[1], clipping_planes[1],
                  50.0, 150.0)
    
    def button_press(self, width, height, event):
        self.beginx = event.x
        self.beginy = event.y
    
    def button_release(self, width, height, event):
        pass
    
    def button_motion(self, width, height, event):
        if event.state == gtk.gdk.BUTTON1_MASK:
            self.rotx = self.rotx + ((event.y-self.beginy)/width)*360.0
            self.roty = self.roty + ((event.x-self.beginx)/height)*360.0
        elif event.state == gtk.gdk.BUTTON2_MASK:
            self.depth = self.depth - ((event.y-self.beginy)/(height))*50.0;
        
        if self.depth > 130.0: self.depth = 130.0;
        elif self.depth < 80.0: self.depth = 80.0;
        
        self.beginx = event.x
        self.beginy = event.y
        
        self.queue_draw()


# A window to show the Shapes scene
# in a GLArea widget along with two (three?)
# sliders for rotating the shape rendered
# in the scene. The shape can also be
# rotated using mouse button drag motion.

import gtk

class Visual3DPage(oofGUI.MainPage):
    def __init__(self):
        self.postponed_update = False
        oofGUI.MainPage.__init__(self, name="PyGtkGLExt Demo", ordering=121,
                                 tip='Display skeletons')
        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)
        
        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)

        self.skelwidget = whowidget.WhoWidget(whoville.getClass('Skeleton'),
                                              callback=self.select_skeleton,
                                              scope=self)
        label = gtk.Label('Microstructure=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.skelwidget.gtk[0], expand=1, fill=1)
        label = gtk.Label('Skeleton=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.skelwidget.gtk[1], expand=1, fill=1)

        ##### Begin portion based on Shapes.py
        
        # Set self attfibutes.
        #self.set_title('Shapes')
        #self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        #self.gtk.connect('destroy', lambda quit: gtk.main_quit())
        if sys.platform != 'win32':
            self.gtk.set_resize_mode(gtk.RESIZE_IMMEDIATE)
        self.gtk.set_reallocate_redraws(True)
        
        # Create the table that will hold everything.
        self.table = gtk.Table(4, 3)
        self.table.set_border_width(5)
        self.table.set_col_spacings(5)
        self.table.set_row_spacings(5)
        #self.table.show()
        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        align.add(self.table)
        
        # The Shapes scene and the
        # GLArea widget to
        # display it.
        self.shape = Shapes()
        self.glarea = GLArea(self.shape)
        self.glarea.set_size_request(300,300)
        #self.glarea.show()
        self.table.attach(self.glarea, 1, 2, 0, 1)
        
        # 3 Frames showing rotation sliders
        self.zframe = gtk.Frame('Z-Axis')
        #self.zframe.show()
        self.zfbox = gtk.VBox()
        self.zfbox.set_border_width(10)
        #self.zfbox.show()
        self.zadj = gtk.Adjustment(0.0, -360.0, 360.0, 5.0, 20.0, 0.0)
        self.zadj.connect('value_changed', self.zchanged)
        self.zscale = gtk.VScale(self.zadj)
        self.zscale.set_value_pos(gtk.POS_LEFT)
        #self.zscale.show()
        self.zfbox.add(self.zscale)
        self.zframe.add(self.zfbox)
        self.table.attach(self.zframe, 0, 1, 0, 1,
                          xoptions=gtk.FILL, yoptions=gtk.FILL)
        
        self.xframe = gtk.Frame('X-Axis')
        #self.xframe.show()
        self.xfbox = gtk.VBox()
        self.xfbox.set_border_width(10)
        #self.xfbox.show()
        self.xadj = gtk.Adjustment(0.0, -360.0, 360.0, 5.0, 20.0, 0.0)
        self.xadj.connect('value_changed', self.xchanged)
        self.xscale = gtk.VScale(self.xadj)
        self.xscale.set_value_pos(gtk.POS_RIGHT)
        #self.xscale.show()
        self.xfbox.add(self.xscale)
        self.xframe.add(self.xfbox)
        self.table.attach(self.xframe, 2, 3, 0, 1,
                          xoptions=gtk.FILL, yoptions=gtk.FILL)
        
        self.yframe = gtk.Frame('Y-Axis')
        #self.yframe.show()
        self.yfbox = gtk.VBox()
        self.yfbox.set_border_width(10)
        #self.yfbox.show()
        self.yadj = gtk.Adjustment(0.0, -360.0, 360.0, 5.0, 20.0, 0.0)
        self.yadj.connect('value_changed', self.ychanged)
        self.yscale = gtk.HScale(self.yadj)
        self.yscale.set_value_pos(gtk.POS_TOP)
        #self.yscale.show()
        self.yfbox.add(self.yscale)
        self.yframe.add(self.yfbox)
        self.table.attach(self.yframe, 1, 2, 1, 2,
                          xoptions=gtk.FILL, yoptions=gtk.FILL)
        
        # A box to hold some control interface stuff.
        self.cbox = gtk.HBox(True, spacing=10)
        #self.cbox.show()
        self.table.attach(self.cbox, 1, 2, 2, 3,
                          xoptions=gtk.FILL, yoptions=gtk.FILL)
        
        # A frame showing some colour changing buttons.
        self.colourFrame = gtk.Frame('Change Colour')
        #self.colourFrame.show()
        self.cbox.pack_start(self.colourFrame)
        
        self.fbox1 = gtk.VBox()
        self.fbox1.set_border_width(10)
        #self.fbox1.show()
        self.colourFrame.add(self.fbox1)
        
        self.colourButtonFg = gtk.Button('Foreground')
        self.colourButtonFg.connect('clicked', self.changeColourFg)
        #self.colourButtonFg.show()
        self.fbox1.pack_start(self.colourButtonFg, expand=True, padding=5)
        
        self.colourButtonBg = gtk.Button('Background')
        self.colourButtonBg.connect('clicked', self.changeColourBg)
        #self.colourButtonBg.show()
        self.fbox1.pack_start(self.colourButtonBg, expand=True, padding=5)
        
        # A frame holding menu and checkbutton for
        # changing the current shape attributes.
        self.shapeFrame = gtk.Frame('Shape Attributes')
        #self.shapeFrame.show()
        self.cbox.pack_start(self.shapeFrame)
        
        self.fbox2 = gtk.VBox()
        self.fbox2.set_border_width(10)
        #self.fbox2.show()
        self.shapeFrame.add(self.fbox2)
        # This is the option menu that lets the
        # user change the shape.
        self.shapeOptions = gtk.combo_box_new_text()
        for shape in self.shape.availableShapes:
            self.shapeOptions.append_text(shape)
        self.shapeOptions.connect('changed', self.shapeChanged)
        self.shapeOptions.set_active(0)
        #self.shapeOptions.show()
        self.fbox2.pack_start(self.shapeOptions, expand=True, padding=5)
        
        self.solidButton = gtk.CheckButton('Solid Shape')
        self.solidButton.connect('toggled', self.shapeSolidityToggled)
        #self.solidButton.show()
        self.fbox2.pack_start(self.solidButton, expand=True, padding=5)

        # Adding controls for VTK and skeleton GL list building
        self.cbox2=gtk.HBox(True, spacing=10)
        self.table.attach(self.cbox2, 1, 2, 3, 4,
                          xoptions=gtk.FILL, yoptions=gtk.FILL)
        if VTKtest:
            self.VTKbuttonFrame=gtk.Frame('Try VTK')
            self.cbox2.pack_start(self.VTKbuttonFrame)
            self.VTKbutton=gtk.Button('Go!')
            self.VTKbutton.connect('clicked',self.tryVTK)
            self.VTKbuttonFrame.add(self.VTKbutton)

        self.BuildListbuttonFrame=gtk.Frame('Build skeleton GL list')
        self.cbox2.pack_start(self.BuildListbuttonFrame)
        self.BuildListbutton=gtk.Button('Go!')
        self.BuildListbutton.connect('clicked',self.buildList)
        self.BuildListbuttonFrame.add(self.BuildListbutton)

    def buildList(self, button):
        skelname=self.skelwidget.get_value()
        if skelname==None:
            return
        skel=skeletoncontext.skeletonContexts[skelname].getObject()
        self.shape.buildGLlists(skel)
        
    def shapeChanged(self, option):
        self.shape.currentShape = self.shape.availableShapes[self.shapeOptions.get_active()]
        self.glarea.queue_draw()
    
    def shapeSolidityToggled(self, button):
        self.shape.is_solid = not self.shape.is_solid
        self.glarea.queue_draw()
    
    def changeColourBg(self, button):
        dialog = gtk.ColorSelectionDialog("Changing colour of Background")
        #dialog.set_transient_for(self)
        dialog.set_transient_for(None)
        
        colorsel = dialog.colorsel
        colorsel.set_has_palette(True)
        
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            colour = colorsel.get_current_color()
            self.shape.colourBg = [colour.red/65535.0, colour.green/65535.0, colour.blue/65535.0]
            self.glarea.queue_draw()
            
        dialog.destroy()
    
    def changeColourFg(self, button):
        dialog = gtk.ColorSelectionDialog("Choose colour of Object")
        #dialog.set_transient_for(self)
        dialog.set_transient_for(None)
        
        colorsel = dialog.colorsel
        colorsel.set_has_palette(True)
        
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            colour = colorsel.get_current_color()
            self.shape.colourFg = [colour.red/65535.0, colour.green/65535.0, colour.blue/65535.0]
            self.glarea.queue_draw()
        
        dialog.destroy()
    
    def zchanged(self, zadj):
        self.shape.rotz = zadj.value
        self.glarea.queue_draw()
    
    def xchanged(self, zadj):
        self.shape.rotx = zadj.value
        self.glarea.queue_draw()
    
    def ychanged(self, yadj):
        self.shape.roty = yadj.value
        self.glarea.queue_draw()
    
##    def run(self):
##        self.show()
##        gtk.main()

    ##### End portion based on Shapes.py

    def select_skeleton(self, *args): # WhoWidget callback
        self.glarea.queue_draw()


    if VTKtest:
        def returnActors(slef, skel, mode):
            sx=skel.MS.size()[0]
            sy=skel.MS.size()[1]
            smax=sx
            if smax<sy:
                smax=sy

            points = vtk.vtkPoints()
            ndindex={}
            i=0
            for nd in skel.nodes:
                if mode==0:
                    points.InsertPoint(i,
                                       nd.position().x,
                                       nd.position().y,
                                       0)
                elif mode==1:
                    theta=2*vtk.vtkMath.Pi()*nd.position().x/sx
                    radius=sx/(2.0*vtk.vtkMath.Pi())
                    points.InsertPoint(i,
                                       radius*math.cos(theta),
                                       nd.position().y,
                                       radius*math.sin(theta))
                elif mode==2:
                    theta=2*vtk.vtkMath.Pi()*nd.position().y/sy
                    radius=sy/(2.0*vtk.vtkMath.Pi())
                    points.InsertPoint(i,
                                       nd.position().x,
                                       radius*math.cos(theta),
                                       radius*math.sin(theta))
                elif mode==3:
                    theta=2*vtk.vtkMath.Pi()*nd.position().y/sy
                    radius=sy/(2.0*vtk.vtkMath.Pi())
                    ry=radius*math.cos(theta)
                    R=sx/(2.0*vtk.vtkMath.Pi())+radius+ry
                    theta2=2*vtk.vtkMath.Pi()*nd.position().x/sx
                    points.InsertPoint(i,
                                       R*math.cos(theta2),
                                       R*math.sin(theta2),
                                       radius*math.sin(theta))
                ndindex[nd.getIndex()]=i
                i+=1
            strips = vtk.vtkCellArray()
            for el in skel.elements:
                strips.InsertNextCell(el.nnodes())
                if el.nnodes()==4:
                    strips.InsertCellPoint(ndindex[el.nodes[0].getIndex()])
                    strips.InsertCellPoint(ndindex[el.nodes[1].getIndex()])
                    strips.InsertCellPoint(ndindex[el.nodes[3].getIndex()])
                    strips.InsertCellPoint(ndindex[el.nodes[2].getIndex()])
                else:
                    for nd in el.nodes:
                        strips.InsertCellPoint(ndindex[nd.getIndex()])

            profile = vtk.vtkPolyData()
            profile.SetPoints(points)
            profile.SetStrips(strips)

            extract = vtk.vtkExtractEdges()
            extract.SetInput(profile)
            tubes = vtk.vtkTubeFilter()
            tubes.SetInputConnection(extract.GetOutputPort())
            tubes.SetRadius(0.01*smax)
            tubes.SetNumberOfSides(6)

            mapEdges = vtk.vtkPolyDataMapper()
            mapEdges.SetInputConnection(tubes.GetOutputPort())
            edgeActor = vtk.vtkActor()
            edgeActor.SetMapper(mapEdges)
            edgeActor.GetProperty().SetColor(peacock)
            edgeActor.GetProperty().SetSpecularColor(1, 1, 1)
            edgeActor.GetProperty().SetSpecular(0.3)
            edgeActor.GetProperty().SetSpecularPower(20)
            edgeActor.GetProperty().SetAmbient(0.2)
            edgeActor.GetProperty().SetDiffuse(0.8)

            ball = vtk.vtkSphereSource()
            ball.SetRadius(0.025*smax)
            ball.SetThetaResolution(12)
            ball.SetPhiResolution(12)
            balls = vtk.vtkGlyph3D()
            balls.SetInput(profile)
            balls.SetSourceConnection(ball.GetOutputPort())
            mapBalls = vtk.vtkPolyDataMapper()
            mapBalls.SetInputConnection(balls.GetOutputPort())
            ballActor = vtk.vtkActor()
            ballActor.SetMapper(mapBalls)
            ballActor.GetProperty().SetColor(hot_pink)
            ballActor.GetProperty().SetSpecularColor(1, 1, 1)
            ballActor.GetProperty().SetSpecular(0.3)
            ballActor.GetProperty().SetSpecularPower(20)
            ballActor.GetProperty().SetAmbient(0.2)
            ballActor.GetProperty().SetDiffuse(0.8)

            return ballActor, edgeActor

        def tryVTK(self, button):
            skelname=self.skelwidget.get_value()
            if skelname==None:
                return
            skel=skeletoncontext.skeletonContexts[skelname].getObject()
            sx=skel.MS.size()[0]
            sy=skel.MS.size()[1]
            smax=sx
            if smax<sy:
                smax=sy

            # Create the rendering window, renderer, and interactive renderer
            ren1 = vtk.vtkRenderer()
            ren2 = vtk.vtkRenderer()
            ren3 = vtk.vtkRenderer()
            ren4 = vtk.vtkRenderer()
            renWin = vtk.vtkRenderWindow()
            renWin.AddRenderer(ren1)
            renWin.AddRenderer(ren2)
            renWin.AddRenderer(ren3)
            renWin.AddRenderer(ren4)

            # Add the actors to the renderer, set the background and size
            ballActor, edgeActor = self.returnActors(skel,0)
            ren1.AddActor(ballActor)
            ren1.AddActor(edgeActor)
            ren1.SetBackground(1, 1, 1)
            ren1.SetViewport(0.0, 0.5, 0.5, 1.0)

    ##        ren.ResetCamera()
    ##        ren.GetActiveCamera().Zoom(1.5)

            (ballActor, edgeActor)=self.returnActors(skel,1)
            ren2.AddActor(ballActor)
            ren2.AddActor(edgeActor)
            ren2.SetBackground(1, 1, 1)
            ren2.SetViewport(0.5, 0.5, 1.0, 1.0)

            (ballActor, edgeActor)=self.returnActors(skel,2)
            ren3.AddActor(ballActor)
            ren3.AddActor(edgeActor)
            ren3.SetBackground(1, 1, 1)
            ren3.SetViewport(0.0, 0.0, 0.5, 0.5)

            (ballActor, edgeActor)=self.returnActors(skel,3)
            ren4.AddActor(ballActor)
            ren4.AddActor(edgeActor)
            ren4.SetBackground(1, 1, 1)
            ren4.SetViewport(0.5, 0.0, 1.0, 0.5)

            renWin.SetSize(600, 600)

##            iren = vtk.vtkRenderWindowInteractor()
##            iren.SetRenderWindow(renWin)

##            # Interact with the data.
##            iren.Initialize()
##            renWin.Render()
##            iren.Start()

            ren1.ResetCamera()
            (near,far)=ren1.GetActiveCamera().GetClippingRange()
            ren1.GetActiveCamera().SetClippingRange(near-smax,far+smax)
            ren2.ResetCamera()
            (near,far)=ren2.GetActiveCamera().GetClippingRange()
            ren2.GetActiveCamera().SetClippingRange(near-smax,far+smax)
            ren3.ResetCamera()
            (near,far)=ren3.GetActiveCamera().GetClippingRange()
            ren3.GetActiveCamera().SetClippingRange(near-smax,far+smax)
            ren4.ResetCamera()
            (near,far)=ren4.GetActiveCamera().GetClippingRange()
            ren4.GetActiveCamera().SetClippingRange(near-smax,far+smax)
            for i in range(0,360):
                time.sleep(0.03)

                renWin.Render()
                ren1.GetActiveCamera().Azimuth( 1 )
                ren2.GetActiveCamera().Azimuth( 1 )
                ren3.GetActiveCamera().Azimuth( 1 )
                ren4.GetActiveCamera().Azimuth( 1 )


visual3dpage = Visual3DPage()
