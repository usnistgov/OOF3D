# -*- python -*-
# $RCSfile: ghostgfxwindow.py,v $
# $Revision: 1.176.2.119 $
# $Author: langer $
# $Date: 2014/12/05 21:29:12 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# The GhostGfxWindow is the underlying non-GUI representation of a
# graphics window.  The actual graphics window, GfxWindow, is derived
# from GhostGfxWindow and overrides some of its functions.

## TODO 3.1: Hidden layers aren't being hidden in cloned windows.

## TODO 3.1: Synchronize the view parameters in multiple gfx windows,
## so that changes in one are reflected automatically in all the
## others.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import timestamp
from ooflib.SWIG.common.IO import ghostoofcanvas
from ooflib.SWIG.common.IO import view
from ooflib.SWIG.common.IO import vtkutils
from ooflib.SWIG.common.IO import imageformat
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import labeltree
from ooflib.common import mainthread
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import quit
from ooflib.common import subthread
from ooflib.common import toolbox
from ooflib.common import utils
from ooflib.common.IO import animationstyle
from ooflib.common.IO import animationtimes
from ooflib.common.IO import automatic
from ooflib.common.IO import display
from ooflib.common.IO import filenameparam
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine.IO import meshparameters
import copy
import os.path
import string
import sys
import types

FloatParameter = parameter.FloatParameter
FloatRangeParameter = parameter.FloatRangeParameter
IntParameter = parameter.IntParameter
StringParameter = parameter.StringParameter

OOF = mainmenu.OOF
OOFMenuItem = oofmenu.OOFMenuItem
CheckOOFMenuItem = oofmenu.CheckOOFMenuItem

# Since debugging the locking code here is a fairly common
# requirement, and commenting out the debugging lines is a pain, they
# can all be turned on and off by setting _debuglocks.
_debuglocks = False

#######################################

# Classes for describing the length and offset of the axis display.

class AxisOffset(registeredclass.RegisteredClass):
    registry = []
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class RelativeAxisOffset(AxisOffset):
    def resolve(self, gfxwindow):
        ms = gfxwindow.findMicrostructure()
        if ms is None:
            return primitives.Point(0,0,0)
        msize = ms.size()
        return primitives.Point(self.x*msize.x,
                                self.y*msize.y,
                                self.z*msize.z)

defaultOffset = (-0.05, -0.05, -0.05)

offsetparams = [
    parameter.FloatParameter('x'),
    parameter.FloatParameter('y'),
    parameter.FloatParameter('z')]


registeredclass.Registration(
    'Relative',
    AxisOffset,
    RelativeAxisOffset,
    ordering=1,
    params=offsetparams,
    tip="Offset the axes by a given fraction of the microstructure size.")

class AbsoluteAxisOffset(AxisOffset):
    def resolve(self, gfxwindow):
        return primitives.Point(self.x, self.y, self.z)

registeredclass.Registration(
    'Absolute',
    AxisOffset,
    AbsoluteAxisOffset,
    ordering=2,
    params=offsetparams,
    tip="Offset the axes by a given distance.")

##########

class AxisLength(registeredclass.RegisteredClass):
    registry = []
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def resolve(self, gfxwindow):
        ms = gfxwindow.findMicrostructure()
        if ms is None:
            return primitives.Point(1, 1, 1)
        msize = ms.size()
        return primitives.Point(
            self.resolve1(self.x, msize.x),
            self.resolve1(self.y, msize.y),
            self.resolve1(self.z, msize.z))

lengthparams = [
    parameter.AutoNumericParameter('x'),
    parameter.AutoNumericParameter('y'),
    parameter.AutoNumericParameter('z')]
    

class RelativeAxisLength(AxisLength):
    def resolve1(self, x, mx):
        if x == automatic.automatic:
            return 1.1*mx
        return x*mx

registeredclass.Registration(
    'Relative',
    AxisLength,
    RelativeAxisLength,
    ordering=1,
    params=lengthparams,
    tip="Set the axis length to a given fraction of the microstructure size.")

class AbsoluteAxisLength(AxisLength):
    def resolve1(self, x, mx):
        if s == automatic.automatic:
            return 1.1*mx
        return x

registeredclass.Registration(
    'Absolute',
    AxisLength,
    AbsoluteAxisLength,
    ordering=2,
    params=lengthparams,
    tip="Set the axis length to a given distance.")

#######################################

class GfxSettings:
    # Stores all the settable parameters for a graphics
    # window. Variables defined at the class level are the default
    # values. Assigning to a variable sets *both* the instance and
    # default values.  Therefore a new window will always use the
    # latest settings.
    bgcolor = color.Gray(0.95)
    zoomfactor = 1.5
    margin = 0.05
    longlayernames = 0                   # Use long form of layer reprs.
    listall = 0                          # Are all layers to be listed?
    autoreorder = 1                      # Automatically reorder layers?
    antialias = 0
    if config.dimension() == 2:
        aspectratio = 5           # Aspect ratio of the contourmap.
        contourmap_markersize = 2 # Size in pixels of contourmap marker.
        contourmap_markercolor = color.gray50 # contourmap position marker.
    elif config.dimension() == 3:
        showcontourmap = 1
        contourmap_bgcolor = color.Gray(0.5)
        contourmap_bgopacity = 0.5
        contourmap_textcolor = color.black
        contourmap_position = (0.9, 0.05)
        contourmap_size = (.1, 0.9)
        axesrequested = True
        axeslabelshowing = True
        axislabelcolor = color.black
        axisfontsize = 20
        axislength = RelativeAxisLength(automatic.automatic,
                                        automatic.automatic,
                                        automatic.automatic)
        axisoffset = RelativeAxisOffset(*defaultOffset)
        
    def __init__(self):
        # Copy all default (class) values into local (instance) variables.
        for key,val in GfxSettings.__dict__.items():
            # Exclude '__module__', etc, as well as all methods (such
            # as getTimeStamp).  Because (apparently) we're accessing
            # the methods via the dictionary, they're not recognized
            # as methods, and we have to check for FunctionType
            # instead of MethodType or UnboundMethodType.
            if key[0] != '_' and type(val) is not types.FunctionType:
                self.__dict__[key] = val

    def __setattr__(self, attr, val):
        self.__dict__[attr] = val       # local value
        GfxSettings.__dict__[attr] = val # default value



# Modules (eg, image or engine) can add graphics window settings by
# calling defineGfxSetting().  They should do this at initialization
# time, before any graphics windows are created.  defineGfxSetting
# does *not* create a menu item or callback for the setting.  That
# must be done by catching the "open graphics window" switchboard
# signal.

def defineGfxSetting(name, val):
    GfxSettings.__dict__[name] = val

#######################################

class GhostGfxWindow:
    initial_height = 400
    initial_width = 800
    def __init__(self, name, gfxmanager, clone=0):
        # In graphics mode, GhostGfxWindow.__init__ is run on a
        # subthread by GfxWindowBase.__init__, after running
        # GfxWindowBase.preinitialize on the main thread.  The
        # subthread is the menu thread for the Graphics.New command.

        self.oofcanvas = None
        self.viewInitialized = False
        self.viewInitializationRequired = False
        self.empty = True

        self.name = name
        self.gfxmanager = gfxmanager
        if not hasattr(self, 'gfxlock'): # may be already set by GfxWindow
            self.gfxlock = lock.Lock()
        self.current_contourmap_method = None
        self.layers = []
        self.selectedLayer = None
        self.sortedLayers = True
        self.displayTime = 0.0
        # self.displayTimeChanged = timestamp.TimeStamp()
        # self.layerChangeTime = timestamp.TimeStamp()
        if not hasattr(self, 'settings'):
            self.settings = GfxSettings()

        self.gtk_destruction_in_progress = False # see GfxWindowBase.destroyCB

        self.menu = OOF.addItem(OOFMenuItem(
            self.name,
            secret=1,
            help = "Commands dependent on a particular Graphics window.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/graphics.xml')
            ))

        # Put this window into the Windows/Graphics menu, so that it
        # can be raised in graphics mode.  Since this isn't meaningful
        # in text mode, there's no callback defined here.
        OOF.Windows.Graphics.addItem(OOFMenuItem(
            self.name,
            help="Raise the window named %s." % name, 
            gui_only=1,
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/graphicsraise.xml')
            ))
        filemenu = self.menu.addItem(OOFMenuItem(
            'File',
            help='General graphics window operations.'))
        filemenu.addItem(OOFMenuItem(
            'Clone',
            callback=self.cloneWindow,
            ellipsis=1,
            help='Make a copy of this window.',
            discussion="""<para>
            Duplicate this <link linkend='Chapter:Graphics'>Graphics
            window</link>.  All the settings and <link
            linkend='Section:Graphics:Layer'>layers</link> will be
            duplicated as well.
            </para>"""
            ))
        filemenu.addItem(OOFMenuItem(
            'Save_Canvas',
            callback=self.saveCanvas,
            ellipsis=1,
            params=[
                filenameparam.WriteFileNameParameter(
                    'filename', ident='gfxwindow',
                    tip="Name for the image file."),
                parameter.RegisteredParameter(
                    'imagetype',
                    imageformat.ImageFormatPtr,
                    tip="Image file format to use."),
                filenameparam.OverwriteParameter('overwrite')
            ],
            help="Save the contents of the graphics window.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/graphicssave.xml')
            ))
        if debug.debug():
            filemenu.addItem(OOFMenuItem(
                    'Save_VTK',
                    callback=self.saveVTK,
                    params=[filenameparam.WriteFileNameParameter(
                            'filename', ident='gfxwindow',
                            tip='Name for the vtk data file.'),
                            filenameparam.OverwriteParameter('overwrite')]
                    ))
        if config.dimension() == 2:
            filemenu.addItem(OOFMenuItem(
                'Save_Contourmap',
                callback=self.saveContourmap,
                ellipsis=1,
                params=[filenameparam.WriteFileNameParameter(
                            'filename', ident='gfxwindow',
                            tip="Name for the image file."),
                        filenameparam.OverwriteParameter('overwrite')],
                help="Save a postscript image of the contour map.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/graphicssavecontour.xml')))
        filemenu.addItem(OOFMenuItem(
            'Clear',
            callback=self.clear,
            help="Remove all user-defined graphics layers.",
            discussion = xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/graphicsclear.xml')
            ))

        filemenu.addItem(OOFMenuItem(
            'Animate',
            callback=self.animate,
            accel='a',
            params=[
                placeholder.GfxTimeParameter(
                        'start',
                        value=placeholder.earliest,
                        tip="Start the animation at this time."),
                placeholder.GfxTimeParameter(
                        'finish', value=placeholder.latest,
                        tip="End the animation at this time."),
                parameter.RegisteredParameter(
                        'times',
                        animationtimes.AnimationTimes),
                parameter.FloatParameter(
                        'frame_rate', 5.0,
                        tip='Update the display this many times per second.'
                        ),
                parameter.RegisteredParameter(
                        "style",
                        animationstyle.AnimationStyle,
                        tip="How to play the animation.")]
            ))

        filemenu.addItem(OOFMenuItem(
            'Redraw',
            callback=self.redraw,
            help="Force all graphics layers to be redrawn.",
            discussion="""<para>
            Redraw all graphics layers, whether they need it or not.
            This should never be necessary.
            </para>"""
            ))

        filemenu.addItem(OOFMenuItem(
            'Close',
            callback=self.close,
            accel='w',
            help="Close the graphics window.",
            discussion="<para>Close the graphics window.</para>"))
        filemenu.addItem(OOFMenuItem(
            'Quit',
            callback=quit.quit,
            accel='q',
            threadable = oofmenu.UNTHREADABLE,
            help= "TTFN",
            discussion="""<para>
            See <xref linkend='MenuItem:OOF.File.Quit'/>.
            </para>"""))
        self.toolboxmenu = self.menu.addItem(OOFMenuItem(
            'Toolbox',
            cli_only=1,
            help='Commands for the graphics toolboxes.',
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/toolbox.xml')
            ))
        layermenu = self.menu.addItem(OOFMenuItem(
            'Layer',
            help='Commands for manipulating graphics layers.',
            discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/layer.xml')
            ))

        layermenu.addItem(OOFMenuItem(
            'New',
            callback=self.newLayerCB,
            accel='n',
            ellipsis=1,
            params=[
                    whoville.WhoClassParameter("category"),
                    whoville.AnyWhoParameter(
                        "what", tip="The object to display."),
                    display.DisplayMethodParameter(
                        "how", tip="How to display it.")
                    ],
            help="Add a new graphics layer.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/newlayer.xml')
            ))
        layermenu.addItem(OOFMenuItem(
            'Edit',
            callback = self.editLayerCB,
            params=[IntParameter('n', 0, tip="Layer to edit."),
                    whoville.WhoClassParameter("category"),
                    whoville.AnyWhoParameter(
                        "what", tip="The object to display."),
                    display.DisplayMethodParameter(
                        "how", tip="How to display it.")],
            accel='e',
            ellipsis=1,
            help= "Edit the selected graphics layer.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/editlayer.xml')
                                      ))
        layermenu.addItem(OOFMenuItem(
            'Delete',
            callback=self.deleteLayerNumber,
            params=[IntParameter('n', 0, tip="Layer index.")],
            help="Delete the selected graphics layer.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/deletelayer.xml')
            ))
        layermenu.addItem(OOFMenuItem(
            'Select',
            callback=self.selectLayerCB,
            cli_only=1,
            params=[IntParameter('n', 0, tip="Layer index.")],
            help="Select the given graphics layer.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/selectlayer.xml')
            ))
        layermenu.addItem(OOFMenuItem(
            'Deselect',
            callback=self.deselectLayerCB,
            cli_only=1,
            params=[IntParameter('n', 0, tip="Layer index.")],
            help="Deselect the given graphics layer.",
            discussion="""<para>
            See <xref linkend='MenuItem:OOF.Graphics_n.Layer.Select'/>.
            </para>"""))
        layermenu.addItem(OOFMenuItem(
            'Hide',
            callback=self.hideLayer,
            accel='h',
            params=[IntParameter('n', 0, tip="Layer index.")],
            help="Hide the selected graphics layer.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/hidelayer.xml')
            ))
        layermenu.addItem(OOFMenuItem(
            'Show',
            callback=self.showLayer,
            accel='s',
            params=[IntParameter('n', 0, tip="Layer index.")],
            help="Show the selected and previously hidden graphics layer.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/showlayer.xml')
            ))
        layermenu.addItem(OOFMenuItem(
            'Freeze',
            callback=self.freezeLayer,
            params=[IntParameter('n', 0, tip="Layer index.")],
            help="Prevent the selected layer from being redrawn."
            ))
        layermenu.addItem(OOFMenuItem(
            'Unfreeze',
            callback=self.unfreezeLayer,
            params=[IntParameter('n', 0, tip="Layer index.")],
            help="Allow the selected layer to be redrawn."
            ))

        if config.dimension() == 2:
            layermenu.addItem(OOFMenuItem(
                'Hide_Contour_Map',
                callback=self.hideLayerContourmap,
                params=[IntParameter('n',0,tip="Contour map index.")],
                help="Hide the selected layer's contour map.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/hidecontour.xml')
                ))
            layermenu.addItem(OOFMenuItem(
                'Show_Contour_Map',
                callback=self.showLayerContourmap,
                params=[IntParameter('n',0, tip="Contour map index.")],
                help="Show the selected layer's contour map.",
                discussion="""<para>
                See <xref
                linkend='MenuItem:OOF.Graphics_n.Layer.Hide_Contour_Map'/>.
                </para>"""
                ))

            ## TODO 3.1: It's not clear that layer ordering has any
            ## meaning in 3D, so the menu items for raising, lowering,
            ## and sorting the layers aren't included in 3D.
            raisemenu = layermenu.addItem(OOFMenuItem(
                'Raise',
                help='Make a layer more visible.',
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/raiselayer.xml')
                ))
            raisemenu.addItem(OOFMenuItem(
                'One_Level',
                callback=self.raiseLayer,
                accel='r',
                params=[IntParameter('n', 0, tip="Layer index.")],
                help="Raise the selected graphics layer.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/raiseone.xml')
                ))
            raisemenu.addItem(OOFMenuItem(
                'To_Top',
                callback=self.raiseToTop,
                accel='t',
                params=[IntParameter('n', 0, tip="Layer index.")],
                help=\
                "Draw the selected graphics layer on top of all other layers.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/raisetop.xml')
                ))
            raisemenu.addItem(OOFMenuItem(
                'By',
                callback=self.raiseBy,
                cli_only = 1,
                params=[IntParameter('n', 0, tip="Layer index."),
                        IntParameter('howfar', 1,
                                     tip="How far to raise the layer.")
                        ],
                help="Raise the selected graphics layer over"
                " a given number of other layers.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/raiseby.xml')
                ))
            lowermenu = layermenu.addItem(OOFMenuItem(
                'Lower',
                help='Make a layer less visible.',
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/lowerlayer.xml')
                ))
            lowermenu.addItem(OOFMenuItem(
                'One_Level',
                callback=self.lowerLayer,
                accel='l',
                params=[IntParameter('n', 0, tip="Layer index.")],
                help="Lower the selected graphics layer.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/lowerone.xml')
                ))
            lowermenu.addItem(OOFMenuItem(
                'To_Bottom',
                callback=self.lowerToBottom,
                accel='b',
                params=[IntParameter('n', 0, tip="Layer index.")],
                help="Draw the selected graphics layer below all other layers.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/lowerbtm.xml')
                ))
            lowermenu.addItem(OOFMenuItem(
                'By',
                callback=self.lowerBy,
                cli_only = 1,
                params=[IntParameter('n', 0, tip="Layer index."),
                        IntParameter('howfar', 1,
                                     tip="How far to lower the layer.")
                        ],
                help="Lower the selected graphics layer under"
                " a given number of other layers.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/lowerby.xml')
                ))
            layermenu.addItem(OOFMenuItem(
                'Reorder_All',
                callback=self.reorderLayers,
                help="Put the graphics layers in their default order.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/reorderlayers.xml')
                ))
        settingmenu = self.menu.addItem(OOFMenuItem(
            'Settings',
            help='Control Graphics window behavior.',
            discussion="""<para>
            The <command>Settings</command> menu contains commands
            that set parameters that control the behavior of the
            Graphics window.
            </para>"""
            ))

        settingmenu.addItem(CheckOOFMenuItem(
                'Antialias',
                callback=self.toggleAntialias,
                value=self.settings.antialias,
                threadable=oofmenu.THREADABLE,
                help=
                "Use antialiased rendering.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/antialias.xml')
                ))
        if config.dimension() == 3:
            axesmenu = settingmenu.addItem(OOFMenuItem('Axes'))
            axesmenu.addItem(CheckOOFMenuItem(
                    'Show',
                    callback=self.showAxes,
                    value=self.settings.axesrequested,
                    help="Show the coordinate axes."))
            axesmenu.addItem(CheckOOFMenuItem(
                    'Show_Labels',
                    callback=self.showAxisLabels,
                    value=self.settings.axeslabelshowing,
                    help="Show the coordinate axis labels."))
            axesmenu.addItem(OOFMenuItem(
                    "Label_Size",
                    callback=self.setAxesLabelSize,
                    params=[
                        parameter.IntParameter(
                            'size', value=self.settings.axisfontsize)
                        ],
                    help="Set the size of the axis labels, in points"))
            axesmenu.addItem(OOFMenuItem(
                    "Label_Color",
                    callback=self.setAxesLabelColor,
                    params=[
                        color.ColorParameter("color", 
                                             self.settings.axislabelcolor)
                        ],
                    help="Set the color of the axis labels."))
            axesmenu.addItem(OOFMenuItem(
                    "Length",
                    callback=self.setAxesLength,
                    params=[
                        parameter.RegisteredParameter(
                            "lengths", AxisLength, self.settings.axislength)],
                    help="Set the length of the coordinate axes."))
            axesmenu.addItem(OOFMenuItem(
                    "Offset",
                    callback=self.setAxesOffset,
                    params=[
                        parameter.RegisteredParameter(
                            "offsets", AxisOffset, self.settings.axisoffset)],
                    help="Set the size of the axis offsets."))
                            
                            

            cmapmenu = settingmenu.addItem(OOFMenuItem('Contour_Map'))
            cmapmenu.addItem(CheckOOFMenuItem(
                'Show',
                callback=self.toggleContourMap,
                value=self.settings.showcontourmap,
                help="Show/hide the contourmap.",
                discussion="""<para>Show or hide the contour map.</para>"""
                ))
            cmapmenu.addItem(OOFMenuItem(
                    'Geometry',
                    callback=self.contourmapGeometry,
                    params=[
                        FloatRangeParameter(
                            'x', (0, 1, 0.01),
                            self.settings.contourmap_position[0],
                            tip="Horizontal position of the lower left corner,"
                            " as a fraction of the canvas width."),
                        FloatRangeParameter(
                            'y', (0, 1, 0.01),
                            self.settings.contourmap_position[1],
                            tip="Vertical position of the lower left corner,"
                            " as a fraction of the canvas height."),
                        FloatRangeParameter(
                            'width', (0, 1, 0.01),
                            self.settings.contourmap_size[0],
                            tip="Width of the contour map,"
                            " as a fraction of the canvas width."),
                        FloatRangeParameter(
                            'height', (0, 1, 0.01),
                            self.settings.contourmap_size[1],
                            tip="Height of the contour map,"
                            " as a fraction of the canvas height.")
                        ],
                    help="Set the position and size of the contour map."))
            cmapmenu.addItem(OOFMenuItem(
                    'Background', 
                    callback=self.contourmapBGColor,
                    params=[color.ColorParameter(
                            'color',
                            self.settings.contourmap_bgcolor,
                            tip="Color for the contour map background."),
                            FloatRangeParameter(
                            'opacity',
                            (0, 1, 0.01),
                            self.settings.contourmap_bgopacity,
                            tip="Opacity of the contour map background.")
                            ],
                    help="Change the contour map background.",
                    discussion="""<para>
                Change the color of the background of the contour map.
                </para>"""))
            cmapmenu.addItem(OOFMenuItem(
                    'Text_Color', 
                    callback=self.contourmapTextColor,
                    params=[
                        color.ColorParameter(
                            'color',
                            self.settings.contourmap_textcolor,
                            tip="Color for the contour map text.")],
                    ellipsis=1,
                    help="Change the contour map text color.",
                    discussion="""<para>
                Change the color of the text in the contour map.
                </para>"""))

                                                  
        settingmenu.addItem(CheckOOFMenuItem(
            'List_All_Layers',
            callback=self.toggleListAll,
            value=self.settings.listall,
            help="List all graphics layers, even predefined ones.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/listall.xml')
            ))
        settingmenu.addItem(CheckOOFMenuItem(
            'Long_Layer_Names',
            callback=self.toggleLongLayerNames,
            value=self.settings.longlayernames,
            help= "Use the long form of layer names in the layer list.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/longlayers.xml')
            ))
        settingmenu.addItem(CheckOOFMenuItem(
            'Auto_Reorder',
            callback=self.toggleAutoReorder,
            value=self.settings.autoreorder,
            help="Automatically reorder layers when new layers are created.",
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/autoreorder.xml')
            ))
        settingmenu.addItem(OOFMenuItem(
            'Time',
            callback=self.setTimeCB,
            params=[FloatParameter(
                'time', 0.0,
                tip='The time to use when displaying time-dependent layers.')
                    ],
            help='Set the time for display layers.',
            discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/common.menu.settime.xml')
        ))
        if config.dimension() == 2:
            settingmenu.addItem(OOFMenuItem(
                'Aspect_Ratio',
                callback=self.aspectRatio,
                params=[FloatParameter('ratio', 5.0,
                                       tip="Aspect ratio of the contour map.")],
                help="Set the aspect ratio of the contour map.",
                discussion="""<para>
                Set the aspect ratio (height/width) of the <link
                linkend='Section:Graphics:ContourMap'>contour map</link>
                display.
                </para>"""))


            settingmenu.addItem(OOFMenuItem(
                'Contourmap_Marker_Size',
                callback=self.contourmapMarkSize,
                ellipsis=1,
                params=[IntParameter('width',2,
                                     tip="Contour map marker line width.")],
                help="Width in pixels of the markers on the contour map.",
                discussion="""<para>
                Set the line <varname>width</varname>, in pixels, of the
                rectangle used to mark a region of the <link
                linkend='Section:Graphics:ContourMap'>contour map</link>.
                </para>"""))

            zoommenu = settingmenu.addItem(
                OOFMenuItem('Zoom', help="Change the scale in the display."))
            zoommenu.addItem(OOFMenuItem(
                'In',
                callback=self.zoomIn,
                accel='.',
                help='Magnify the image.',
                discussion="""<para>
                Magnify the graphics display by the current <link
                linkend='MenuItem:OOF.Graphics_n.Settings.Zoom.Zoom_Factor'>zoom
                factor</link>, keeping the center of the display fixed.
                </para>"""))
            zoommenu.addItem(OOFMenuItem(
                'InFocussed',
                callback=self.zoomInFocussed,
                secret=1,
                params=[primitives.PointParameter(
                            'focus', tip='Point to magnify about.')],
                help='Magnify the image about a mouse click.',
                discussion="""<para>
                Magnify the graphics display by the current <link
                linkend='MenuItem:OOF.Graphics_n.Settings.Zoom.Zoom_Factor'>zoom
                factor</link>, keeping the mouse click position fixed.
                </para>"""))
            zoommenu.addItem(OOFMenuItem(
                'Out',
                callback=self.zoomOut,
                accel=',',
                help='Demagnify by the current zoom factor.',
                discussion="""<para> 
                Demagnify the graphics display by the current <link
                linkend='MenuItem:OOF.Graphics_n.Settings.Zoom.Zoom_Factor'>zoom
                factor</link>, keeping the center of the display fixed.
                </para>"""))
            zoommenu.addItem(OOFMenuItem(
                'OutFocussed',
                callback=self.zoomOutFocussed,
                secret=1,
                params=[primitives.PointParameter(
                            'focus', tip='Point to demagnify about.')],
                help='Magnify the image about a mouse click.',
                discussion="""<para>
                Demagnify the graphics display by the current <link
                linkend='MenuItem:OOF.Graphics_n.Settings.Zoom.Zoom_Factor'>zoom
                factor</link>, keeping the mouse click position fixed.
                </para>"""))
            zoommenu.addItem(OOFMenuItem(
                'Fill_Window',
                callback=self.zoomFillWindow,
                accel='=',
                help='Fit the image to the window.',
                discussion="""<para>
                Zoom the display so that it fills the window.
                </para>"""))
            zoommenu.addItem(OOFMenuItem(
                'Zoom_Factor',
                callback = self.zoomfactorCB,
                params=[
                FloatParameter('factor', self.settings.zoomfactor,
                               tip="Zoom factor.")],
                ellipsis=1,
                help='Set the zoom magnification.',
                discussion="""<para>
                The scale of the display changes by
                <varname>factor</varname> or 1./<varname>factor</varname>
                when zooming in or out.
                </para>"""))
        colormenu = settingmenu.addItem(OOFMenuItem(
            'Color',
            help='Set the color of various parts of the display.'
            ))
        colormenu.addItem(OOFMenuItem(
            'Background',
            callback=self.bgColor,
            params=[color.ColorParameter('color', self.settings.bgcolor,
                                         tip="Color for the background.")],
            help='Change the background color.',
            discussion="<para> Set the background color. </para>"))
        if config.dimension() == 2:
            colormenu.addItem(OOFMenuItem(
                'Contourmap_Marker', 
                callback=self.contourmapMarkColor,
                params=[color.ColorParameter(
                            'color',
                            self.settings.contourmap_markercolor,
                            tip="Color for the contour map marker.")],
                help="Change the contour map marker color.",
                discussion="""<para>
                Change the color of the position marker on the contourmap pane.
                </para>"""))

        settingmenu.addItem(OOFMenuItem(
            'Margin',
            callback=self.marginCB,
            params=[FloatParameter(
                        'fraction', self.settings.margin,
                        tip="Margin as a fraction of the image size.")],
            ellipsis=1,
            help='Set the margin (as a fraction of the image size)'
            ' when zooming to full size.',
            discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/common/menu/margin.xml')
            ))

        if config.dimension() == 2:
            scrollmenu = settingmenu.addItem(OOFMenuItem(
                'Scroll',
                cli_only=1,
                help='Scroll the main display.'))
            scrollmenu.addItem(OOFMenuItem(
                'Horizontal',
                callback=self.hScrollCB,
                params=[FloatParameter('position', 0.,
                                       tip="Horizontal scroll position.")],
                help="Scroll horizontally.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/scrollhoriz.xml')
                ))
            scrollmenu.addItem(OOFMenuItem(
                'Vertical',
                callback=self.vScrollCB,
                params=[FloatParameter('position', 0.,
                                       tip="Vertical scroll position.")],
                help="Scroll vertically.",
                discussion=xmlmenudump.loadFile(
                        'DISCUSSIONS/common/menu/scrollvert.xml')
                ))
        if config.dimension() == 3:
            cameramenu = settingmenu.addItem(OOFMenuItem('Camera', cli_only=1))
            cameramenu.addItem(OOFMenuItem(
                    'View',
                    cli_only=1,
                    callback=self.viewCB,
                    params=[view.ViewParameter("view")],
                    help="Change the camera position."))

        # newCanvas creates GhostOOFCanvas or OOFCanvas3D as appropriate.
        mainthread.runBlock(self.newCanvas)

        # Create toolboxes.
        self.toolboxes = []
        map(self.newToolboxClass, toolbox.toolboxClasses)

        self.defaultLayerCreated = {}
        self.sensitize_menus()

        if not clone:
            self.createPredefinedLayers()

        # Switchboard callbacks.  Keep a list of them so that they can
        # all be removed when the window is closed.
        self.switchboardCallbacks = [
            switchboard.requestCallback('new who', self.newWho), # generic who
            switchboard.requestCallback('preremove who', self.removeWho),
            switchboard.requestCallback('new toolbox class',
                                        self.newToolboxClass),
            switchboard.requestCallback('deselect all gfxlayers',
                                        self.deselectAll),
            switchboard.requestCallback('redraw', self.draw),
            switchboard.requestCallback('draw at time', self.drawAtTime)
            ]

    # end __init__

    def addSwitchboardCallback(self, *callbacks):
        # "callback" is a switchboard callback that need to be removed
        # when the gfx window closes.
        self.switchboardCallbacks.extend(callbacks)

    def createPredefinedLayers(self):
        # Create pre-defined layers.  These are in all graphics
        # windows, regardless of whether or not they are drawable at
        # the moment.
        for predeflayer in PredefinedLayer.allPredefinedLayers:
            # The gfxlock has been acquired already, so we call
            # incorporateLayer with lock=False.
            layer, who = predeflayer.createLayer(self)
            self.incorporateLayer(layer, who, autoselect=False, lock=False)
        
        # Create default layers if possible.  One layer is created for
        # each WhoClass the first time that an instance of that class
        # is created.
        self.createDefaultLayers(lock=False)

        # latestTime can return None
        self.displayTime = self.latestTime() or 0.0
        
    def drawable(self):                 # used when testing the gui
        # return self.display.drawable(self)
        assert False, "Display.drawable needs to be reimplemented."
        
    def __repr__(self):
        return 'GhostGfxWindow("%s")' % self.name

    def acquireGfxLock(self):
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg('------------------------ acquiring gfxlock', self.name)
        self.gfxlock.acquire()
        if _debuglocks:
            debug.fmsg('------------------------ acquired', self.name)
    def releaseGfxLock(self):
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg("------------------------ releasing gfxlock", self.name)
        self.gfxlock.release()

    def createDefaultLayers(self, lock=True):
        # Call this with lock=True if the gfxlock has not been
        # acquired by the calling routine.
        if lock:
            self.acquireGfxLock()
        try:
            # Unselect all layers first, so that new layers don't
            # overwrite existing ones.
            selectedLayer = self.selectedLayer
            self.deselectAll()

            # Create a default layer for each WhoClass if this window
            # hasn't already created a default layer for that class
            # and if there's only a single member of the class.  (The
            # single member constraint is enforced in
            # DefaultLayer.createLayer().)
            for defaultlayer in DefaultLayer.allDefaultLayers:
                try:
                    layercreated = self.defaultLayerCreated[defaultlayer]
                except KeyError:
                    layercreated = False
                    self.defaultLayerCreated[defaultlayer] = layercreated
                if not layercreated:
                    layer, who = defaultlayer.createLayer()
                    if layer is not None:
                        self.incorporateLayer(layer, who,
                                              autoselect=False, lock=False)
                        self.defaultLayerCreated[defaultlayer] = True
            # Restore the previous selection state.
            if selectedLayer:
                self.selectLayer(self.layerID(selectedLayer))
        finally:
            if lock:
                self.releaseGfxLock()
                
    def sensitize_menus(self):
        ## TODO LATER: There appears to be a problem with the timing of
        ## double clicks in the LayerList --- can one thread be inside
        ## sensitize_menus() while another thread is setting
        ## self.selectedLayer to None?  Does there need to be a lock
        ## on self.selectedLayer?  --- 7/30/14 I'm not sure this bug
        ## still exists, so I'm not fixing it.
        if self.selectedLayer is not None and \
               (self.selectedLayer.listed or self.settings.listall):
            self.menu.Layer.Delete.enable()
            self.menu.Layer.Edit.enable()
            if self.selectedLayer.frozen:
                self.menu.Layer.Unfreeze.enable()
                self.menu.Layer.Freeze.disable()
            else:
                self.menu.Layer.Freeze.enable()
                self.menu.Layer.Unfreeze.disable()

            if config.dimension() == 2:
                if self.selectedLayer.hidden:
                    self.menu.Layer.Show.enable()
                    self.menu.Layer.Hide.disable()
                else:
                    self.menu.Layer.Show.disable()
                    self.menu.Layer.Hide.enable()
                if self.layerID(self.selectedLayer) == 0:
                    self.menu.Layer.Lower.disable()
                else:
                    self.menu.Layer.Lower.enable()
                if self.layerID(self.selectedLayer) == self.nlayers()-1:
                    self.menu.Layer.Raise.disable()
                else:
                    self.menu.Layer.Raise.enable()

                self.menu.Layer.Show_Contour_Map.disable()
                self.menu.Layer.Hide_Contour_Map.disable()
                if self.selectedLayer.contour_capable():
                    if not self.selectedLayer.contourmaphidden:
                        self.menu.Layer.Hide_Contour_Map.enable()
                    else:
                        self.menu.Layer.Show_Contour_Map.enable()
        else:                   # no selected layer
            self.menu.Layer.Delete.disable()
            self.menu.Layer.Show.disable()
            self.menu.Layer.Hide.disable()
            self.menu.Layer.Freeze.disable()
            self.menu.Layer.Unfreeze.disable()
            self.menu.Layer.Edit.disable()
            if config.dimension() == 2:
                self.menu.Layer.Raise.disable()
                self.menu.Layer.Lower.disable()
                self.menu.Layer.Show_Contour_Map.disable()
                self.menu.Layer.Hide_Contour_Map.disable()
        if config.dimension() == 2:
            if self.nlayers() == 0:
                self.menu.Settings.Zoom.disable()
            else:
                self.menu.Settings.Zoom.enable()
            if self.sortedLayers:
                self.menu.Layer.Reorder_All.disable()
            else:
                self.menu.Layer.Reorder_All.enable()

    def newCanvas(self):
        # This is redefined in GUI mode.
        if self.oofcanvas:
            view = self.oofcanvas.get_view()
        self.oofcanvas = ghostoofcanvas.GhostOOFCanvas()
        self.oofcanvas.set_bgColor(self.settings.bgcolor)

    def updateview(self):
        # Called after camera parameters have been changed. 
        mainthread.runBlock(self._updateview)
    def _updateview(self):
        self.oofcanvas.recalculate_clipping()
        self.oofcanvas.orthogonalize_view_up()
        self.oofcanvas.render()
    
    def is_empty(self):
        for layer in self.layers:
            if not isinstance(layer.who(), whoville.WhoProxy):
	        print layer.who().__class__.__name__
                return False
        return True
    
    def checkLayersGridsSizes(self):
        count = 0
        for layer in self.layers:
           count = count + layer.getGridSize()
        return count
    
    def layersNumber(self):
        return len(self.layers)
        
    ##############################

    # Menu callbacks.

    def cloneWindow(self, *args):
        self.acquireGfxLock()
        try:
            newwindow = self.gfxmanager.openWindow(clone=1)
            newwindow.settings = copy.deepcopy(self.settings)
            for layer in self.layers:
                newlayer = layer.clone(newwindow)
                newwindow.incorporateLayer(newlayer, layer.who())
                newwindow.deselectLayer(newwindow.selectedLayerNumber())
            if self.selectedLayer is not None:
                newwindow.selectLayer(self.layerID(self.selectedLayer))
            view = mainthread.runBlock(self.oofcanvas.get_view)
            newwindow.draw()
            newwindow.viewCB(None, view)
            ## TODO 3.1: Clone the view history.

            ## TODO: After cloning a window containing only a hidden
            ## image layer and showing the layer in the clone, the
            ## image is drawn at the wrong size and with a black
            ## border. Making any change to the view fixes it. 
        finally:
            self.releaseGfxLock()

    def close(self, menuitem, *args):
        # Before acquiring the gfx lock, kill all subthreads, or
        # this may deadlock!
        #self.device.destroy()

        self.acquireGfxLock()
        try:
            self.gfxmanager.closeWindow(self)

            # Things can be shut down via several pathways (ie, from
            # scripts or gtk events), so at each step we have to make sure
            # that the step won't be repeated.  This function has been
            # called from the menus, so here we turn off the menu
            # callback.
            menuitem.callback = None

            for callback in self.switchboardCallbacks:
                switchboard.removeCallback(callback)
            self.switchboardCallbacks = []

            for layer in self.layers[:]:
                layer.destroy(not self.gtk_destruction_in_progress)
            self.layers = []

            for toolbox in self.toolboxes:
                toolbox.close()

            # cleanup to prevent possible circular references
            ## del self.display
            del self.gfxmanager
            self.menu.clearMenu()
            OOF.Windows.Graphics.removeItem(self.name)
            OOF.removeItem(self.name)
            self.menu = None
            del self.selectedLayer
            del self.toolboxes
        finally:
            # Although the window is closing, it's important to
            # release the lock so that any remaining drawing threads
            # can finish.  They won't actually try to draw anything,
            # because of the device.destroy call, above.  TODO 3.1:
            # Fix this comment.  There's no device.destroy call. Could
            # the threads actually try to draw something?
            self.releaseGfxLock()

    def clear(self, *args, **kwargs):
        # Remove all user specified layers from the display.
        self.acquireGfxLock()
        try:
            # The layer list is modified as layers are deleted, so we
            # have to work with a copy.
            layers = self.layers[:]
            for layer in layers:
                if layer.listed:
                    self.removeLayer(layer)
        finally:
            self.releaseGfxLock()
        self.draw()

    def draw(self, *args, **kwargs):
        subthread.execute(self._draw, args, kwargs)

    def _draw(self, *args, **kwargs):
        self.acquireGfxLock()
        try:
            self.initializeView()
        finally:
            self.releaseGfxLock()

    def drawAtTime(self, *args, **kwargs):
        subthread.execute(self._draw, args, kwargs)

    def animate(self, *args, **kwargs):
        pass

    def setTimeCB(self, menuitem, time):
        # Called by the the Settings menu, and also by the
        # GraphicsUpdate ScheduledOutput class.  Redefined in
        # GUI/gfxwindowbase.py, where it also sets the slider widget
        # and calls draw() (via drawAtTime()).
        self.setDisplayTime(time)

    def setDisplayTime(self, time):
        if time != self.displayTime:
            self.displayTime = time
            # self.displayTimeChanged.increment()
            switchboard.notify((self, "time changed")) # caught by MeshDataGUI

    def backdate(self):
        # Backdate timestamps on the local display. 
        self.acquireGfxLock()
        try:
            for layer in self.layers:
                layer.modified()
        finally:
            self.releaseGfxLock()
        
    def redraw(self, menuitem):
        for layer in self.layers:
            if not layer.frozen:
                layer.redraw()
        # self.backdate()                    # backdates timestamps
        self.draw()

    def toggleAntialias(self, menuitem, antialias):
        self.settings.antialias = antialias
        mainthread.runBlock(self.oofcanvas.setAntiAlias, (antialias,))
        self.draw()

    def toggleListAll(self, menuitem, listall):
        self.acquireGfxLock()
        try:
            self.settings.listall = listall
            self.sensitize_menus()
            self.fillLayerList()
        finally:
            self.releaseGfxLock()

    def fillLayerList(self):    # redefined in GfxWindowBase
        pass

    def toggleAutoReorder(self, menuitem, autoreorder):
        self.acquireGfxLock()
        self.settings.autoreorder = autoreorder
        self.releaseGfxLock()

    def toggleLongLayerNames(self, menuitem, longlayernames):
        self.settings.longlayernames = longlayernames

    def showAxes(self, menuitem, show):
        self.settings.axesrequested = show
        mainthread.runBlock(self.updateAxes)
        self.draw()

    def showAxisLabels(self, menuitem, show):
        self.settings.axeslabelshowing = show
        mainthread.runBlock(self.oofcanvas.showAxisLabels, (show,))
        self.draw()

    def setAxesLabelSize(self, menuitem, size):
        self.settings.axisfontsize = size
        mainthread.runBlock(self.oofcanvas.setAxisLabelFontSize, (size,))
        self.draw()

    def setAxesLabelColor(self, menuitem, color):
        self.settings.axislabelcolor = color
        mainthread.runBlock(self.oofcanvas.setAxisLabelColor, (color,))
        self.draw()

    def setAxesLength(self, menuitem, lengths):
        self.settings.axislength = lengths
        mainthread.runBlock(self.oofcanvas.setAxisLength,
                            (lengths.resolve(self)),)
        self.draw()

    def setAxesOffset(self, menuitem, offsets):
        self.settings.axisoffset = offsets
        mainthread.runBlock(self.oofcanvas.setAxisOffset, 
                            (offsets.resolve(self),))
        self.draw()

    def aspectRatio(self, menuitem, ratio): # 2D
        self.settings.aspectratio = ratio
        
    def toggleContourMap(self, menuitem, show):
        self.settings.showcontourmap = show
        mainthread.runBlock(self.oofcanvas.showContourMap, (show,))
        self.draw()

    def contourmapMarkSize(self, menuitem, width): # 2D
        self.settings.contourmap_markersize = width

    def contourmapMarkColor(self, menuitem, color): # 2D
        self.settings.contourmap_markercolor = color

    def contourmapBGColor(self, menuitem, color, opacity):
        self.settings.contourmap_bgcolor = color
        self.settings.contourmap_bgopacity = opacity
        mainthread.runBlock(self.oofcanvas.setContourMapBGColor,
                            (color, opacity))
        self.draw()

    def contourmapTextColor(self, menuitem, color):
        self.settings.contourmap_textcolor = color
        mainthread.runBlock(self.oofcanvas.setContourMapTextColor, (color,))
        self.draw()

    def contourmapGeometry(self, menuitem, x, y, width, height):
        self.settings.contourmap_size = (width, height)
        mainthread.runBlock(self.oofcanvas.setContourMapSize, (width, height))
        mainthread.runBlock(self.oofcanvas.setContourMapPosition, (x, y))
        self.draw()

        
    def zoomIn(self, *args, **kwargs):
        pass
    def zoomOut(self, *args, **kwargs):
        pass
    def zoomInFocussed(self, *args, **kwargs):
        pass
    def zoomOutFocussed(self, *args, **kwargs):
        pass
    def zoomFillWindow(self, *args, **kwargs):
        pass

    def bgColor(self, menuitem, color):
        self.settings.bgcolor = color

    def marginCB(self, menuitem, fraction):
        self.settings.margin = fraction

    def zoomfactorCB(self, menuitem, factor):
        self.settings.zoomfactor = factor
        switchboard.notify("zoom factor changed")

    def hScrollCB(self, menuitem, position):
        self.hscrollvalue = position

    def vScrollCB(self, menuitem, position):
        self.vscrollvalue = position

    def viewCB(self, menuitem, view):
        # Menu callback for OOF.Graphics_n.Settings.Camera.View, which is
        # called at the end of mouse manipulations governed by the
        # toolbar buttons (Tumble, Dolly, etc).

        ## This function used to be in GfxwWindow3D, with an empty
        ## function body here in the base class.  It needs to be
        ## called here so that recalculate_clipping() can be called
        ## after camera parameters are changed, even when running from
        ## scripts.  Not doing so can cause mouse clips to be
        ## misinterpreted if the microstructure extends past the front
        ## and back clipping planes.

        # Here false ==> Don't set clip planes.
        mainthread.runBlock(self.oofcanvas.set_view, (view, False))
        switchboard.notify("view changed", self)
        ## TODO OPT: Check that calling updateview here isn't repeating
        ## work done elsewhere.
        self.updateview()


    if config.dimension() == 2:
        def saveCanvas(self, menuitem, filename, overwrite):
            pass
#             if overwrite or not os.path.exists(filename):
#                 pdevice = pdfoutput.PDFoutput(filename=filename)
#                 pdevice.set_background(self.settings.bgcolor)
#                 self.display.draw(self, pdevice)

    elif config.dimension() == 3:
        def saveCanvas(self, menuitem, filename, imagetype, overwrite):
            sfx = imagetype.suffix() # desired suffix
            if sfx:
                if filename.endswith("."+sfx):
                    fname = filename
                else:
                    fname = filename + "." + sfx
            else:
                # Some ImageFormat subclasses handle the suffix
                # themselves because of differences between
                # vtkExporter and vtkImageWriter classes.
                fname, ext = os.path.splitext(filename)
            mainthread.runBlock(self.oofcanvas.save_canvas, (fname, imagetype))

    def saveVTK(self, menuitem, filename, overwrite):
        if overwrite or not os.path.exists(filename):
            for layer in self.layers:
                layer.writeVTK(filename)
        
    def saveContourmap(self, menuitem, filename, overwrite):
        pass
#         if overwrite or not os.path.exists(filename):
#             pdevice = pdfoutput.PDFoutput(filename=filename)
#             pdevice.set_background(self.settings.bgcolor)
#             self.display.draw_contourmap(self, pdevice)



    # # Called as part of the "layers changed" in response to layer
    # # insertion, removal, or reordering.  Sets the current contourable
    # # layer to be the topmost one, unconditionally.
    # def contourmap_newlayers(self):
    #     self.current_contourmap_method = self.set_contourmap_topmost()
    #     switchboard.notify( (self, "new contourmap layer") )
    #     ## We probably should *not* call sensitize_menus here, since
    #     ## contourmap_newlayers is called from routines that also call
    #     ## sensitize_menus.
    #     # self.sensitize_menus()

    # # Alternate method -- manually set a particular layer to be the
    # # current contourable layer.
    # def set_contourmap_layer(self, method):
    #     self.current_contourmap_method.hide_contourmap()
    #     self.current_contourmap_method = method
    #     self.current_contourmap_method.show_contourmap()

    # # Return the contour-capable method with a non-hidden contourmap.
    # # There can only be one, so returning the first one is safe.
    # def get_contourmap_method(self):
    #     for layer in self.layers:
    #         if layer.contour_capable():
    #             if not layer.contourmaphidden:
    #                 return layer

    # # Find the topmost contourable method, and make it be the one with
    # # a non-hidden contourmap.
    # def set_contourmap_topmost(self):
    #     for layer in self.layers:
    #         layer.hide_contourmap()
    #     topmost = self.topcontourable()
    #     if topmost:
    #         topmost.show_contourmap()
    #         return topmost

    # # Contourmaps are drawn on the canvas directly by the gfxwindow,
    # # which has additional auxiliary info, like min/max values for the
    # # text boxes.  This routine is called for drawing it into a file,
    # # typically with the "device" being PSOutput.
    # def draw_contourmap(self, canvas):
    #     contourmap_layer = self.get_contourmap_method()
    #     if contourmap_layer:
    #         canvas.begin_layer()
    #         contourmap_layer.draw_contourmap(canvas)
    #         canvas.end_layer()
    #         canvas.show()
    

    
    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # Returns the index of the layer in the list.
    def layerID(self, layer):
        return self.layers.index(layer)

    def nlayers(self):
        return len(self.layers)

    def getLayer(self, layerNumber): # only used by layer editor, will go away
        return self.layers[layerNumber]

    ## TODO 3.1: It's not clear that layer ordering has any meaning in
    ## 3D, so the menu items for raising, lowering, and sorting the
    ## layers aren't included in 3D.  HOWEVER, if the layers aren't
    ## sorted in the canonical order when they're first constructed in
    ## 3D, the selected voxels don't appear, so sortLayers() *always*
    ## runs in 3D.

    def sortLayers(self, forced=False):
        if forced or config.dimension() == 3 or self.settings.autoreorder:
            self.layers.sort(display.layercomparator)
            self.sortedLayers = True

    def raise_layer_by(self, n, howfar):
        ## TODO OPT: Lock?
        if n < self.nlayers()-howfar:
            thislayer = self.layers[n]
            for i in range(howfar): # TODO OPT: Use slice copy instead of loop
                self.layers[n+i] = self.layers[n+i+1]
            self.layers[n+howfar] = thislayer
            thislayer.raise_layer(howfar) # Currently a no-op!
            self.sortedLayers = False
            # self.layerChangeTime.increment()
    def raise_layer(self, n):
        self.raise_layer_by(n, 1)
    def layer_to_top(self, n):
        self.raise_layer_by(n, self.nlayers()-n-1)
        
    def lower_layer_by(self, n, howfar):
        ## TODO OPT: Lock?
        if n >= howfar:
            thislayer = self.layers[n]
            for i in range(howfar): # TODO OPT: Use slice copy instead of loop
                self.layers[n-i] = self.layers[n-i-1]
            self.layers[n-howfar] = thislayer
            thislayer.lower_layer(howfar) # Currently a no-op!
            self.sortedLayers = False
            # self.layerChangeTime.increment()
    def lower_layer(self, n):
        self.lower_layer_by(n, 1)
    def layer_to_bottom(self, n):
        self.lower_layer_by(n, n)

    def topwho(self, *whoclasses):
        for i in range(self.nlayers()-1, -1, -1): # top down
            who = self.layers[i].who()
            if who is not None:
                classname = who.getClassName()
                if ((not isinstance(who, whoville.WhoProxy))
                    and not self.layers[i].hidden
                    and classname in whoclasses):
                    return who

    # Advanced function, returns a reference to the *layer* object
    # which draws the who object referred to.
    def topwholayer(self, *whoclasses):
        for i in range(self.nlayers()-1, -1, -1): # top down
            who = self.layers[i].who()
            if who is not None:
                classname = who.getClassName()
                if ((not isinstance(who, whoville.WhoProxy)) and 
                    not self.layers[i].hidden
                    and classname in whoclasses):
                    return self.layers[i]

    # Return all layers displaying the given who.
    def allwholayers(self, who, limit=-1):
        layerlist = []
        for i in range(self.nlayers()-1, -1, -1): # top down
            layer = self.layers[i]
            if not layer.hidden and layer.who() is who:
                layerlist.append(layer)
                if len(layerlist) == limit:
                    break
        return layerlist

    def topmost(self, *whoclasses):
        # Find the topmost layer whose 'who' belongs to the given
        # whoclass.  Eg, topmost('Image') returns the topmost image.
        who = self.topwho(*whoclasses)
        if who is not None:
            return who.getObject(self)

    def topMethod(self, *displaymethods):
        for i in range(self.nlayers()-1, -1, -1): # top down
            for method in displaymethods:
                if isinstance(self.layers[i], method):
                    return self.layers[i]

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def findMicrostructure(self):
        who = self.topwho('Microstructure', 'Image', 'Skeleton', 'Mesh')
        if who is not None:
            return who.getMicrostructure()

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def findClickedCell(self, who, point, view):
        self.acquireGfxLock()
        try:
            layerlist = self.allwholayers(who)
            for layer in layerlist:
                if layer.pickable():
                    return mainthread.runBlock(
                        clickErrorHandler,
                        (self.oofcanvas.findClickedCell,
                         point, view, layer.canvaslayer))
        finally:
            self.releaseGfxLock()

    def findClickedCellID(self, who, point, view):
        self.acquireGfxLock()
        try:
            layerlist = self.allwholayers(who, limit=1)
            for layer in layerlist:
                if layer.pickable():
                    rval = mainthread.runBlock(
                        clickErrorHandler,
                        (self.oofcanvas.findClickedCellID,
                         point, view, layer.canvaslayer))
                    if rval is None:
                        # findClickedCellID returns cellID, clickPosition
                        return (None, None)
                    # If the layer has a filter, then vtk's cell ID is
                    # different than the mesh's index.
                    try:
                        fltr = layer.filter
                    except AttributeError:
                        return rval
                    cellidx = fltr.getCellIndex(rval[0])
                    if cellidx == -1:
                        # This shouldn't happen...
                        raise ooferror.ErrPyProgrammingError(
                            "Filter failure in findClickedCellID")
                        # return (None, None)
                    return (cellidx, rval[1])
        finally:
            self.releaseGfxLock()

    def findClickedCellCenter(self, who, point, view):
        self.acquireGfxLock()
        try:
            layerlist = self.allwholayers(who)
            for layer in layerlist:
                if layer.pickable():
                    return mainthread.runBlock(
                        clickErrorHandler,
                        (self.oofcanvas.findClickedCellCenter,
                         point, view, layer.canvaslayer))
        finally:
            self.releaseGfxLock()

    def findClickedPosition(self, who, point, view):
        self.acquireGfxLock()
        try:
            layerlist = self.allwholayers(who)
            for layer in layerlist:
                if layer.pickable():
                    return mainthread.runBlock(
                        clickErrorHandler,
                        (self.oofcanvas.findClickedPosition,
                         point, view, layer.canvaslayer))
        finally:
            self.releaseGfxLock()

    def findClickedPoint(self, who, point, view):
        self.acquireGfxLock()
        try:
            layerlist = self.allwholayers(who)
            for layer in layerlist:
                if layer.pickable():
                    return mainthread.runBlock(
                        clickErrorHandler,
                        (self.oofcanvas.findClickedPoint,
                         point, view, layer.canvaslayer))
        finally:
            self.releaseGfxLock()

    def findClickedSegment(self, who, point, view):
        self.acquireGfxLock()
        try:
            layerlist = self.allwholayers(who)
            for layer in layerlist:
                if layer.pickable():
                    return mainthread.runBlock(
                        clickErrorHandler,
                        (self.oofcanvas.findClickedSegment,
                         point, view, layer.canvaslayer))
        finally:
            self.releaseGfxLock()

    def findClickedFace(self, who, point, view):
        self.acquireGfxLock()
        try:
            layerlist = self.allwholayers(who)
            for layer in layerlist:
                if layer.pickable():
                    return mainthread.runBlock(
                        clickErrorHandler,
                        (self.oofcanvas.findClickedFace,
                         point, view, layer.canvaslayer))
        finally:
            self.releaseGfxLock()

    #################################

    # Function for doing book-keeping whenever the set of layers has
    # changed.  Overridden in gfxwindow.

    def newLayerMembers(self):
        wasEmpty = self.empty
        self.empty = True
        switchboard.notify((self, 'layers changed'))
        for layer in self.layers:
            if isinstance(layer.who(), whoville.WhoProxy):
                layer.whoChanged()
            else:
                self.empty = False
            layer.layersChanged()
            
        mainthread.runBlock(self.updateAxes)

        # Tell the topmost contourable layer to draw its contour map.
        layer = self.topcontourable()
        if layer:
            mainthread.runBlock(layer.canvaslayer.installContourMap)
        else:
            mainthread.runBlock(self.oofcanvas.noContourMap)
        
        if not self.viewInitialized and wasEmpty and not self.empty:
            self.viewInitializationRequired = True

    def updateAxes(self):
        debug.mainthreadTest()
        show = self.settings.axesrequested and not self.empty
        if show:
            self.oofcanvas.setAxisLength(self.settings.axislength.resolve(self))
            self.oofcanvas.setAxisOffset(self.settings.axisoffset.resolve(self))
        self.oofcanvas.toggleAxes(show)

    def initializeView(self):
        # Called by draw().  The view should be initialized on the
        # first call to draw() *after* a non-proxy layer has been
        # added.
        if self.viewInitializationRequired and not self.viewInitialized:
            tb = self.getToolboxByName('Viewer')
            tb.restoreNamedView('Front')
            self.viewInitialized = True
            self.viewInitializationRequired = False

            
    ##################################

    def topImageIndex(self):
        # Find topmost image
        indices = [i for (i, layer) in enumerate(self.layers)
                   if layer.isImage() and not layer.hidden]
        if indices:
            return indices[-1]

    def topImage(self):
        which = self.topImageIndex()
        if which is not None:
            return self.layers[which]

    def getOverlayers(self):
        im = self.topImageIndex()
        if im is None:
            return []
        return [l for l in self.layers[im+1:]
                if (not l.hidden and l.isOverlayer())]
    
    #################################

    # incorporateLayer() is the routine that adds a DisplayMethod to the
    # graphics window.

    ## TODO OPT: Somehow ensure that only the topmost filled layer (bitmap
    ## or filled grid) is displayed.
            
    def incorporateLayer(self, layer, who, autoselect=True, lock=True):
        if lock:
            self.acquireGfxLock()
        try:
            if self.selectedLayer:
                if self.selectedLayer.__class__ is layer.__class__:
                    # The layer has just been edited.  Change the
                    # parameters of the old layer and discard the
                    # *new* one, allowing the old one's connections to
                    # remain in place.
                    self.selectedLayer.copyParams(layer)
                    if self.selectedLayer.setWho(who):
                        self.selectedLayer.setParams()
                    layer.destroy(destroy_canvaslayer=False)
                else:
                    # Replace old selected layer at the same location
                    # in the layer list.
                    which = self.layerID(self.selectedLayer)
                    layer.frozen = self.selectedLayer.frozen
                    oldlayer = self.selectedLayer
                    self.layers[which] = layer
                    # Do not call self.selectLayer here.  It'll try to
                    # call deselectLayer() on the previous selection,
                    # which is no longer in the list.  It also does
                    # too much in the way of switchboard and gui
                    # callbacks.
                    self.selectedLayer = layer
                    self.sortedLayers = False
                    self.sortLayers()
                    layer.build(self)
                    if layer.setWho(who):
                        layer.setParams()
                    # Don't destroy the old layer until after the new
                    # one is in place.  Its C++ guts may need to be
                    # disconnected when the new layer is being
                    # installed.
                    oldlayer.destroy(destroy_canvaslayer=True)
            else:
                # No layer is selected.  Add the new one at the end of
                # the layer list.
                self.layers.append(layer)
                self.sortedLayers = False
                self.sortLayers()
                layer.build(self)
                if layer.setWho(who):
                    layer.setParams()
                if autoselect:
                    self.selectLayer(self.layerID(layer))
            
            self.newLayerMembers()
            self.sensitize_menus()
        finally:
            if lock:
                self.releaseGfxLock()

    def newLayerCB(self, menuitem, category, what, how):
        self.selectedLayer = None
        whoclass = whoville.getClass(category)
        who = whoclass[what]
        self.incorporateLayer(how, who)
        self.draw()

    def editLayerCB(self, menuitem, n, category, what, how):
        whoclass = whoville.getClass(category)
        who = whoclass[what]
        # If there is a selected layer when incorporateLayer() is
        # called, the selected layer is replaced with the new one.
        self.selectedLayer = self.layers[n]
        self.incorporateLayer(how, who)
        self.draw()
        
    def deleteLayerNumber(self, menuitem, n):
        layer = self.layers[n]
        self.removeLayer(layer)
        # switchboard.notify((self, 'layers changed'))
        self.draw()

    def removeLayer(self, layer):       # extended in gfxwindowbase.py
        self.layers.remove(layer)
        # self.layerChangeTime.increment()
        if layer is self.selectedLayer:
            self.selectedLayer = None
            self.sensitize_menus()
        layer.destroy(True)
        self.newLayerMembers()
        
    def hideLayer(self, menuitem, n):
        layer = self.layers[n]
        layer.hidden = True
        if layer.canvaslayer is not None:
            layer.canvaslayer.hide(False)
            # switchboard.notify((self, 'layers changed'))
            self.newLayerMembers()
            self.draw()
            self.sensitize_menus()
            # self.contourmap_newlayers()

    def showLayer(self, menuitem, n):
        layer = self.layers[n]
        layer.hidden = False
        if layer.canvaslayer is not None:
            layer.canvaslayer.show(False)
            self.newLayerMembers()
            # switchboard.notify((self, 'layers changed'))
            self.draw()
            self.sensitize_menus()
            # self.contourmap_newlayers()

    def freezeLayer(self, menuitem, n):
        self.layers[n].freeze(self)
        switchboard.notify((self, 'layers frozen'))
        self.sensitize_menus()
    def unfreezeLayer(self, menuitem, n):
        self.layers[n].unfreeze(self)
        switchboard.notify((self, 'layers frozen'))
        self.sensitize_menus()
        self.draw()

    # Menu callbacks for layer operations.  Overridden in gfxwindow.
    def hideLayerContourmap(self, menuitem, n):
        self.layers[n].hide_contourmap()
        self.current_contourmap_method = None
        self.sensitize_menus()
    
    def showLayerContourmap(self, menuitem, n):
        # At most one contourmap can be shown at a time, so hide all
        # the others.
        for layer in self.layers:
            layer.hide_contourmap()
        self.current_contourmap_method = self.layers[n]
        self.current_contourmap_method.show_contourmap()
        self.sensitize_menus()

    # Topmost layer on which contours can be drawn -- such a layer
    # must have a mesh as its "who".
    def topcontourable(self):
        for i in range(len(self.layers)):
            layer = self.layers[-(i+1)]
            if (layer.contour_capable() and not layer.hidden and
                not layer.incomputable()):
                return layer

    def selectLayer(self, n):
        if n is not None:
            self.selectedLayer = self.layers[n]
            self.sensitize_menus()
    def deselectLayer(self, n):
        if self.selectedLayer is not None and \
           self.layerID(self.selectedLayer)==n:
            self.selectedLayer = None
            self.sensitize_menus()
    def deselectAll(self):
        if self.selectedLayer is not None:
            self.selectedLayer = None
            self.sensitize_menus()
    def selectedLayerNumber(self):
        if self.selectedLayer is not None:
            return self.layerID(self.selectedLayer)

    def selectLayerCB(self, menuitem, n):
        self.selectLayer(n)
    def deselectLayerCB(self, menuitem, n):
        self.deselectLayer(n)

    def raiseLayer(self, menuitem, n):
        self.raise_layer(n)
        self.sensitize_menus()
        self.newLayerMembers()
        self.draw()
        
    def raiseToTop(self, menuitem, n):
        self.layer_to_top(n)
        self.sensitize_menus()
        self.newLayerMembers()
        self.draw()

    def raiseBy(self, menuitem, n, howfar):
        self.raise_layer_by(n, howfar)
        self.sensitize_menus()
        self.newLayerMembers()
        self.draw()

    def lowerLayer(self, menuitem, n):
        self.lower_layer(n)
        self.sensitize_menus()
        self.newLayerMembers()
        self.draw()
        
    def lowerToBottom(self, menuitem, n):
        self.layer_to_bottom(n)
        self.sensitize_menus()
        self.newLayerMembers()
        self.draw()

    def lowerBy(self, menuitem, n, howfar):
        self.lower_layer_by(n, howfar)
        self.sensitize_menus()
        self.newLayerMembers()
        self.draw()

    def reorderLayers(self, menuitem):
        self.sortLayers(forced=True)
        self.sensitize_menus()
        self.newLayerMembers()
        self.draw()

    def listedLayers(self):             # for testing
        result = []
        for layer in self.layers:
            if layer.listed:
                result.append(layer)
        return result

    def updateLayerList(self, layer):
        pass
                
    #####################################
    
    def findAnimationTimes(self):
        # Return a lsit of all possible tiems that can appear in an
        # animation, by asking the unfrozen AnimationLaysers for their
        # times.
        times = set()
        for layer in self.layers:
            if (isinstance(layer, display.AnimationLayer)
                and layer.animatable()):
                when = layer.getParamValue('when')
                if when is placeholder.latest:
                    times.update(layer.animationTimes())
        times = list(times)
        times.sort()
        return times

    def latestTime(self):
        times = self.findAnimationTimes()
        if times:
            return times[-1]
        return None

    #####################################

    # switchboard callbacks

    def newWho(self, classname, who):
        # A new Who (layer context) has been created.  Display it
        # automatically, if nothing else is displayed.
        self.createDefaultLayers(lock=True)
        ## Don't call self.draw() here!  It should only be called when
        ## a menu item issues the "redraw" switchboard signal.
        ## Otherwise it can be called too often (such as when one menu
        ## item creates more than one new Who object).
        
    def removeWho(self, whoclassname, whoname):
        path = labeltree.makePath(whoname)
        for layer in self.layers[:]:
            layerpath = labeltree.makePath(layer.who().path())
            if (layerpath == path and
                layer.who().getClass().name() == whoclassname):
                ## TODO OPT: Should this do nothing for proxy layers?
                if self.selectedLayer is layer:
                    self.selectedLayer = None
                self.layers.remove(layer)
                layer.destroy(True)
        self.newLayerMembers()
        self.draw()
        
    def newToolboxClass(self, tbclass):
        tb = tbclass(self)              # constructs toolbox
        self.toolboxes.append(tb)
        menu = self.toolboxmenu.addItem(
            OOFMenuItem(tb.name(), help=tb.tip, discussion=tb.discussion))
        menu.data = tb
        tb.makeMenu(menu)

    def getToolboxByName(self, name):
        for toolbox in self.toolboxes:
            if toolbox.name() == name:
                return toolbox

#########################################

# An imported module can define a default layer for a graphics window
# by instantiating the DefaultLayer class.  Default layers are drawn
# in a new graphics window if and only if there is exactly one
# instance of the WhoClass which they display.

class DefaultLayer:
    allDefaultLayers = []
    def __init__(self, whoclass, displaymethodfn):
        DefaultLayer.allDefaultLayers.append(self)
        self.whoclass = whoclass
        self.displaymethodfn = displaymethodfn

    def createLayer(self):
        if self.whoclass.nActual() == 1:
            return self.displaymethodfn(), self.whoclass.actualMembers()[0]
        return None, None

    def __repr__(self):
        return "DefaultLayer(%s, %s)" % (self.whoclass, self.displaymethodfn)

# Predefined layers are created whenever a graphics window is opened
# by GhostGfxWindow.createPredefinedLayers(), without checking for the
# existence of an object in the WhoClass.  They are automatically
# unlisted.

class PredefinedLayer:
    allPredefinedLayers = []
    def __init__(self, whoclassname, path, displaymethodfn):
        PredefinedLayer.allPredefinedLayers.append(self)
        self.whoclass = whoville.getClass(whoclassname)
        self.path = path
        self.displaymethodfn = displaymethodfn
    def createLayer(self, gfxwindow):
        displaymethod = self.displaymethodfn()
        displaymethod.listed = 0
        return displaymethod, self.whoclass[self.path]

################################################

## Set default values for the gfx window size.  This isn't handled by
## GfxSettings, because the window size isn't set in the window's own
## settings menu.

def _setDefaultGfxSize(menuitem, width, height):
    GhostGfxWindow.initial_width = width
    GhostGfxWindow.initial_height = height

mainmenu.gfxdefaultsmenu.addItem(oofmenu.OOFMenuItem(
    'Window',
    callback=_setDefaultGfxSize,
    ordering=0,
    params=[parameter.IntParameter('width',
                                   GhostGfxWindow.initial_width,
                                   tip="Window width in pixels."),
            parameter.IntParameter('height',
                                   GhostGfxWindow.initial_height,
                                   tip="Window height in pixels.")],
    help="Set the initial size of graphics windows.",
    discussion="<para> Set the initial size of graphics windows. </para>"
    ))


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# clickErrorHandler is passed as the argument to mainthread.runBlock
# when calling one of the findClicked* methods.  It checks to see if
# the findClicked* method raised an ErrClickError, and returns None if
# it did.  This is necessary because findClicked* is a C++ function
# called on the main thread, but we need to catch the exception in
# Python on a subthread.  clickErrorHandler just catches the exception
# on the main thread before returning control to the subthread.

def clickErrorHandler(findClickedObj, *args, **kwargs):
    try:
        return findClickedObj(*args, **kwargs)
    except ooferror.ErrClickError:
        return None

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

