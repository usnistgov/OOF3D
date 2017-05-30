# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import clip
from ooflib.SWIG.common import coord
from ooflib.SWIG.common import direction
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import vtkutils
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import primitives
from ooflib.common import subthread
from ooflib.common import utils
from ooflib.common.IO import clipplaneclickanddragdisplay
from ooflib.common.IO import reporter
from ooflib.common.IO import viewertoolbox
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import historian
from ooflib.common.IO.GUI import labelledslider
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.common.IO.GUI import tooltips

import gtk
import gobject
import math

ndigits = 10

## TODO: When a clipping plane is set using Angles, it should stay
## in Angles after it's been edited by the plane and arrow widget.

## TODO: Continuous rotation mode.  Set angular velocity and axis
## direction.

## TODO: Rocker mode: rock back and forth on an axis.  Set axis
## direction, frequency, and amplitude.

THRESHOLD = 0.4

## TODO 3.1: Move axis parameters from the Settings menu to a new
## expander in the toolbox.  It should contains check buttons for
## showing the axes and their labels and a button that brings up a
## window for setting the axis parameters (lengths, offsets, label
## size, label color, arrow radius, arrow/shaft ratio). [Should arrow
## tip size be constant, in pixel units?]

## TODO 3.1 MAYBE: Add a button that brings up a separate, non-modal window
## that displays the current camera parameters.  This window should be
## updated in real time as the view changes.  Remove the Camera Info
## pane from the toolbox.

class ViewerToolbox3DGUI(toolboxGUI.GfxToolbox, mousehandler.MouseHandler):
    def __init__(self, vwrtoolbox):
        debug.mainthreadTest()

        toolboxGUI.GfxToolbox.__init__(self, "Viewer", vwrtoolbox)
        mainbox = gtk.VBox(spacing=3)
        self.gtk.add(mainbox)

        self.historian = historian.Historian(
            setCB=self.restoreHistoricalView,
            sensitizeCB=self.sensitize,
            compareCB=lambda v1, v2: v1.equiv(v2))

        # camera position
        infoExpander = gtk.Expander("Camera Info")
        gtklogger.setWidgetName(infoExpander, "CameraInfo")
        infoFrame = gtk.Frame()
        infoFrame.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(infoExpander, fill=0, expand=0)
        infoExpander.add(infoFrame)
        infoBox = gtk.VBox(spacing=3)
        infoFrame.add(infoBox)
        positionlabel = gtk.Label("Camera Position:")
        infoBox.pack_start(positionlabel,fill=0, expand=0)
        positiontable = gtk.Table(columns=3, rows=1)
        infoBox.pack_start(positiontable,fill=0, expand=0)
        self.camera_x = gtk.Entry()
        gtklogger.setWidgetName(self.camera_x, "CameraX")
        self.camera_x.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.camera_x.set_editable(0)
        positiontable.attach(self.camera_x,0,1,0,1)
        self.camera_y = gtk.Entry()
        gtklogger.setWidgetName(self.camera_y, "CameraY")
        self.camera_y.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.camera_y.set_editable(0)
        positiontable.attach(self.camera_y,1,2,0,1)
        self.camera_z = gtk.Entry()
        gtklogger.setWidgetName(self.camera_z, "CameraZ")
        self.camera_z.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.camera_z.set_editable(0)
        positiontable.attach(self.camera_z,2,3,0,1)
        focalpointlabel = gtk.Label("Focal Point:")
        infoBox.pack_start(focalpointlabel,fill=0, expand=0)
        focalpointtable = gtk.Table(columns=3, rows=1)
        infoBox.pack_start(focalpointtable,fill=0, expand=0)
        self.fp_x = gtk.Entry()
        gtklogger.setWidgetName(self.fp_x, "FocalX")
        self.fp_x.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.fp_x.set_editable(0)
        focalpointtable.attach(self.fp_x,0,1,0,1)
        self.fp_y = gtk.Entry()
        gtklogger.setWidgetName(self.fp_y, "FocalY")
        self.fp_y.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.fp_y.set_editable(0)
        focalpointtable.attach(self.fp_y,1,2,0,1)
        self.fp_z = gtk.Entry()
        gtklogger.setWidgetName(self.fp_z, "FocalZ")
        self.fp_z.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.fp_z.set_editable(0)
        focalpointtable.attach(self.fp_z,2,3,0,1)
        viewuplabel = gtk.Label("View Up Vector:")
        infoBox.pack_start(viewuplabel,fill=0, expand=0)
        viewuptable = gtk.Table(columns=3, rows=1)
        infoBox.pack_start(viewuptable,fill=0, expand=0)
        self.viewup_x = gtk.Entry()
        gtklogger.setWidgetName(self.viewup_x, "ViewUpX")
        self.viewup_x.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.viewup_x.set_editable(0)
        viewuptable.attach(self.viewup_x,0,1,0,1)
        self.viewup_y = gtk.Entry()
        gtklogger.setWidgetName(self.viewup_y, "ViewUpY")
        self.viewup_y.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.viewup_y.set_editable(0)
        viewuptable.attach(self.viewup_y,1,2,0,1)
        self.viewup_z = gtk.Entry()
        gtklogger.setWidgetName(self.viewup_z, "ViewUpZ")
        self.viewup_z.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.viewup_z.set_editable(0)
        viewuptable.attach(self.viewup_z,2,3,0,1)
        distancetable = gtk.Table(columns=2, rows=1)
        infoBox.pack_start(distancetable,fill=0, expand=0)
        distancelabel = gtk.Label("Distance:")
        distancetable.attach(distancelabel,0,1,0,1)
        self.distance = gtk.Entry()
        gtklogger.setWidgetName(self.distance, "Distance")
        self.distance.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.distance.set_editable(0)
        distancetable.attach(self.distance,1,2,0,1)
        angletable = gtk.Table(columns=2, rows=1)
        infoBox.pack_start(angletable,fill=0, expand=0)
        anglelabel = gtk.Label("View Angle:")
        angletable.attach(anglelabel,0,1,0,1)
        self.viewangle = gtk.Entry()
        gtklogger.setWidgetName(self.viewangle, "ViewAngle")
        self.viewangle.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.viewangle.set_editable(0)
        angletable.attach(self.viewangle,1,2,0,1)

        # Translation
        transExpander = gtk.Expander("Translate")
        gtklogger.setWidgetName(transExpander, "Translation")
        mainbox.pack_start(transExpander, fill=0, expand=0)
        transFrame = gtk.Frame()
        transFrame.set_shadow_type(gtk.SHADOW_IN)
        transExpander.add(transFrame)
        transBox = gtk.VBox()
        transFrame.add(transBox)
        # dolly
        dollyrow = gtk.HBox(homogeneous=1, spacing=2)
        transBox.pack_start(dollyrow, expand=0, fill=1, padding=2)
        inbutton = gtk.Button('Dolly In')
        gtklogger.setWidgetName(inbutton, 'DollyIn')
        tooltips.set_tooltip_text(
            inbutton,
            "Translate camera towards focal point by given factor.")
        dollyrow.pack_start(inbutton, expand=0, fill=1)
        gtklogger.connect(inbutton, 'clicked', self.dollyin)
        outbutton = gtk.Button('Dolly Out')
        gtklogger.setWidgetName(outbutton, 'DollyOut')
        tooltips.set_tooltip_text(
            outbutton, 
            "Translate camera away from focal point by given factor.")
        dollyrow.pack_start(outbutton, expand=0, fill=1)
        gtklogger.connect(outbutton, 'clicked', self.dollyout)
        fillbutton = gtk.Button('Fill')
        gtklogger.setWidgetName(fillbutton,'Fill')
        tooltips.set_tooltip_text(
            fillbutton,
            "Set the camera position so that the image"
            " approximately fills the window.")
        dollyrow.pack_start(fillbutton, expand=0, fill=1)
        gtklogger.connect(fillbutton, 'clicked', self.dollyfill)
        factorrow = gtk.HBox()
        transBox.pack_start(factorrow, expand=0, fill=0, padding=2)
        factorrow.pack_start(gtk.Label("Factor: "), expand=0, fill=0)
        self.dollyfactor = gtk.Entry()
        self.dollyfactor.set_editable(1)
        self.dollyfactor.set_size_request(ndigits*guitop.top().digitsize, -1)
        gtklogger.setWidgetName(self.dollyfactor, "DollyFactor")
        self.dollyfactor.set_text("1.5")
        tooltips.set_tooltip_text(
            self.dollyfactor,
            "Factor by which to multiply distance from camera to focal point.")
        factorrow.pack_start(self.dollyfactor, expand=1, fill=1)

        # track
        trackrow = gtk.HBox(homogeneous=1, spacing=2)
        transBox.pack_start(trackrow, expand=0, fill=1, padding=2)
        horizbutton = gtk.Button('Horizontal')
        tooltips.set_tooltip_text(
            horizbutton, "Shift camera and focal point horizontally")
        trackrow.pack_start(horizbutton, expand=0, fill=1)
        gtklogger.connect(horizbutton, 'clicked', self.trackh)
        vertbutton = gtk.Button('Vertical')
        tooltips.set_tooltip_text(
            vertbutton, "Shift camera and focal point vertically")
        trackrow.pack_start(vertbutton, expand=0, fill=1)
        gtklogger.connect(vertbutton, 'clicked', self.trackv)
        recenterbutton = gtk.Button('Recenter')
        tooltips.set_tooltip_text(recenterbutton,
                             "Recenter the microstructure in the viewport.")
        trackrow.pack_start(recenterbutton, expand=0, fill=1)
        gtklogger.connect(recenterbutton, 'clicked', self.recenter)        
        distrow = gtk.HBox()
        transBox.pack_start(distrow, expand=0, fill=0, padding=2)
        distrow.pack_start(gtk.Label("Distance: "), expand=0, fill=0)
        self.trackdist = gtk.Entry()
        self.trackdist.set_editable(1)
        self.trackdist.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.trackdist.set_text("10.0")
        tooltips.set_tooltip_text(
            self.trackdist,
            "Distance by which to track camera, in pixel units.")
        distrow.pack_start(self.trackdist, expand=1, fill=1)


        #rotate
        rotateExpander = gtk.Expander("Rotate")
        rotateFrame = gtk.Frame()
        rotateFrame.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(rotateExpander, fill=0, expand=0)
        rotateBox = gtk.VBox()
        rotateExpander.add(rotateFrame)
        rotateFrame.add(rotateBox)
        rotrow1 = gtk.HBox(homogeneous=1, spacing=2)
        rotateBox.pack_start(rotrow1, expand=0, fill=1, padding=2)
        rollbutton = gtk.Button('Roll')
        tooltips.set_tooltip_text(rollbutton,
                                  "Rotate about direction of projection.")
        rotrow1.pack_start(rollbutton, expand=0, fill=1)
        gtklogger.connect(rollbutton, 'clicked', self.roll)
        pitchbutton = gtk.Button('Pitch')
        tooltips.set_tooltip_text(
            pitchbutton,
            "Rotate about cross product of direction of projection and"
            " view up vector centered at camera position.")
        rotrow1.pack_start(pitchbutton, expand=0, fill=1)
        gtklogger.connect(pitchbutton, 'clicked', self.pitch)
        yawbutton = gtk.Button('Yaw')
        tooltips.set_tooltip_text(
            yawbutton, 
            "Rotate about view up vector centered at camera position.")
        rotrow1.pack_start(yawbutton, expand=0, fill=1)
        gtklogger.connect(yawbutton, 'clicked', self.yaw)
        rotrow2 = gtk.HBox(homogeneous=1, spacing=2)
        rotateBox.pack_start(rotrow2, expand=0, fill=1, padding=2)
        azbutton = gtk.Button('Azimuth')
        tooltips.set_tooltip_text(
            azbutton, "Rotate about view up vector centered at focal point.")
        rotrow2.pack_start(azbutton, expand=0, fill=1)
        gtklogger.connect(azbutton, 'clicked', self.azimuth)
        elbutton = gtk.Button('Elevation')
        tooltips.set_tooltip_text(
            elbutton,
            "Rotate about cross product of direction of projection and"
            " view up vector centered at focal point")
        rotrow2.pack_start(elbutton, expand=0, fill=1)
        gtklogger.connect(elbutton, 'clicked', self.elevation)
        anglerow = gtk.HBox()
        rotateBox.pack_start(anglerow, expand=0, fill=0, padding=2)
        anglerow.pack_start(gtk.Label("Angle: "), expand=0, fill=0)
        self.angle = gtk.Entry()
        self.angle.set_editable(1)
        self.angle.set_size_request(ndigits*guitop.top().digitsize, -1)
        self.angle.set_text("10.0")
        tooltips.set_tooltip_text(self.angle,
                             "Angle by which to rotate, in degrees.")
        anglerow.pack_start(self.angle, expand=1, fill=1)

        # Zoom
        zoomExpander = gtk.Expander('Zoom')
        gtklogger.setWidgetName(zoomExpander, 'Zoom')
        mainbox.pack_start(zoomExpander, fill=0, expand=0)
        zoomFrame = gtk.Frame()
        zoomFrame.set_shadow_type(gtk.SHADOW_IN)
        zoomExpander.add(zoomFrame)
        zoomBox = gtk.VBox()
        zoomFrame.add(zoomBox)
        buttonbox = gtk.HBox(homogeneous=1, spacing=2)
        zoomBox.pack_start(buttonbox, expand=0, fill=0)
        zoominbutton = gtk.Button('In')
        gtklogger.setWidgetName(zoominbutton, 'In')
        gtklogger.connect(zoominbutton, 'clicked', self.zoomInCB)
        buttonbox.pack_start(zoominbutton, expand=1, fill=1)
        tooltips.set_tooltip_text(zoominbutton, 
                   "Zoom in (decrease the viewing angle) by the given factor.")
        zoomoutbutton = gtk.Button('Out')
        gtklogger.setWidgetName(zoomoutbutton, 'Out')
        gtklogger.connect(zoomoutbutton, 'clicked', self.zoomOutCB)
        buttonbox.pack_start(zoomoutbutton, expand=1, fill=1)
        tooltips.set_tooltip_text(zoomoutbutton, 
                   "Zoom out (increase the viewing angle) by the given factor.")
        zoomfillbutton = gtk.Button('Fill')
        gtklogger.setWidgetName(zoomfillbutton, 'Fill')
        gtklogger.connect(zoomfillbutton, 'clicked', self.zoomFillCB)
        buttonbox.pack_start(zoomfillbutton, expand=1, fill=1)
        tooltips.set_tooltip_text(zoomfillbutton,
                    "Set the viewing angle so that the image fills the window.")
        zoomrow = gtk.HBox()
        zoomBox.pack_start(zoomrow, expand=0, fill=0)
        zoomrow.pack_start(gtk.Label("Factor: "), expand=0, fill=0)
        self.zoomfactor = gtk.Entry()
        self.zoomfactor.set_text("1.1")
        self.zoomfactor.set_editable(1)
        gtklogger.setWidgetName(self.zoomfactor, "Factor")
        gtklogger.connect_passive(self.zoomfactor, "changed")
        tooltips.set_tooltip_text(self.zoomfactor,
                             "Factor by which to multiply the camera angle.")
        zoomrow.pack_start(self.zoomfactor, expand=1, fill=1)
                    
        # Clipping planes
        clippingExpander = gtk.Expander("Clip")
        clippingFrame = gtk.Frame()
        gtklogger.setWidgetName(clippingExpander, "Clipping")
        clippingFrame.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(clippingExpander, fill=1, expand=1)
        clippingExpander.add(clippingFrame)
        clippingBox = gtk.VBox()
        clippingFrame.add(clippingBox)
        clippingScroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(clippingScroll, "Scroll")
        clippingScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        clippingBox.pack_start(clippingScroll, expand=1, fill=1)
        self.clippingList = gtk.ListStore(gobject.TYPE_PYOBJECT,
                                          gobject.TYPE_INT)
        self.clippingListView = gtk.TreeView(self.clippingList)
        gtklogger.setWidgetName(self.clippingListView, "ClippingList")
        clippingScroll.add(self.clippingListView)
        gtklogger.adoptGObject(self.clippingList, self.clippingListView,
                               access_method=self.clippingListView.get_model)
        gtklogger.adoptGObject(
            self.clippingListView.get_selection(),
            self.clippingListView,
            access_method=self.clippingListView.get_selection)
        self.clipSelectSignal = gtklogger.connect(
            self.clippingListView.get_selection(),
            'changed', self.clipSelectionChangedCB)
        gtklogger.connect(self.clippingListView, 'row-activated',
                          self.editClipCB)
        # A check button that enables or disables a clipping plane
        enablecell = gtk.CellRendererToggle()
        enablecol = gtk.TreeViewColumn("On")
        enablecol.pack_start(enablecell, expand=False)
        enablecol.set_cell_data_func(enablecell, self.renderEnableCell)
        self.clippingListView.append_column(enablecol)
        gtklogger.adoptGObject(enablecell, self.clippingListView,
                               access_function=gtklogger.findCellRenderer,
                               access_kwargs={'col':0, 'rend':0})
        gtklogger.connect(enablecell, 'toggled', self.enableCellCB)
        # A check button for inverting the plane
        flipcell = gtk.CellRendererToggle()
        flipcol = gtk.TreeViewColumn("Flip")
        flipcol.pack_start(flipcell, expand=False)
        flipcol.set_cell_data_func(flipcell, self.renderFlipCell)
        self.clippingListView.append_column(flipcol)
        gtklogger.adoptGObject(flipcell, self.clippingListView,
                               access_function=gtklogger.findCellRenderer,
                               access_kwargs={'col':1, 'rend':0})
        gtklogger.connect(flipcell, 'toggled', self.flipCellCB)
        # The normal to the clipping plane
        normalcell = gtk.CellRendererText()
        normalcol = gtk.TreeViewColumn("Normal")
        normalcol.set_resizable(True)
        normalcol.pack_start(normalcell, expand=True)
        normalcol.set_cell_data_func(normalcell, self.renderNormalCol)
        self.clippingListView.append_column(normalcol)
        # The offset
        offsetcell = gtk.CellRendererText()
        offsetcol = gtk.TreeViewColumn("Offset")
        offsetcol.set_resizable(True)
        offsetcol.pack_start(offsetcell, expand=True)
        offsetcol.set_cell_data_func(offsetcell, self.renderOffsetCol)
        self.clippingListView.append_column(offsetcol)

        # Buttons for operating on clipping planes
        bbox = gtk.HBox()
        bbox.set_homogeneous(True)
        clippingBox.pack_start(bbox, expand=0, fill=0)

        newclipbutton = gtk.Button("New")
        gtklogger.setWidgetName(newclipbutton, "New")
        gtklogger.connect(newclipbutton, 'clicked', self.newClipCB)
        tooltips.set_tooltip_text(newclipbutton, "Add a clipping plane.")
        bbox.pack_start(newclipbutton)

        self.editclipbutton = gtk.Button("Edit")
        gtklogger.setWidgetName(self.editclipbutton, "Edit")
        gtklogger.connect(self.editclipbutton, 'clicked', self.editClipCB)
        tooltips.set_tooltip_text(self.editclipbutton, "Edit a clipping plane.")
        bbox.pack_start(self.editclipbutton)

        self.delclipbutton = gtk.Button("Delete")
        gtklogger.setWidgetName(self.delclipbutton, "Delete")
        gtklogger.connect(self.delclipbutton, 'clicked', self.delClipCB)
        tooltips.set_tooltip_text(self.delclipbutton, 
                                  "Delete a clipping plane.")
        bbox.pack_start(self.delclipbutton)

        # Second row of buttons for clipping plane operations
        bbox = gtk.HBox()
        bbox.set_homogeneous(True)
        clippingBox.pack_start(bbox, expand=0, fill=0)

        self.invclipButton = gtk.CheckButton("Invert All")
        self.invclipButton.set_active(self.toolbox.invertClip)
        gtklogger.setWidgetName(self.invclipButton, "Invert")
        gtklogger.connect(self.invclipButton, 'clicked', self.invClipCB)
        tooltips.set_tooltip_text(self.invclipButton,
                                  "Invert clipping sense globally")
        bbox.pack_start(self.invclipButton)

        self.suppressButton = gtk.CheckButton("Suppress All")
        gtklogger.setWidgetName(self.suppressButton, "Suppress")
        gtklogger.connect(self.suppressButton, 'clicked', self.suppressCB)
        tooltips.set_tooltip_text(self.suppressButton,
                                  "Suppress all clipping planes.")
        bbox.pack_start(self.suppressButton)

        label0 = gtk.Label(
"""Select a clipping plane from the list to edit.
How to use the click-and-drag editing tool:
  (Click plane)+Move: Offset plane along its normal
  (Click arrow)+Move: Rotate plane
  (Ctrl+Click plane/arrow)+Move: Move base of 
    arrow in plane
To deselect a plane, Ctrl+Click the plane in the list."""
        )
        label0.set_pattern("             _______\n            ________\n            ________\n            ________\n            ________\n            ________\n             _______\n")
        label0.set_justify(gtk.JUSTIFY_LEFT)
        clippingBox.pack_start(label0, fill=0, expand=0, padding=2)

        ## TODO 3.1: Clipping plane operations
        ##   Delete all
        ##   Save/Load?
        ##   Undo/Redo
        ##   Copy to/from other window
        
        # save and restore
        historyFrame = gtk.Frame("Save and Restore Views")
        historyFrame.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(historyFrame, fill=0, expand=0)
        viewTable = gtk.Table(columns=2, rows=3)
        historyFrame.add(viewTable)
        align = gtk.Alignment(xalign=0.9, yalign=0.5)
        align.add(gtk.Label("Restore:"))
        viewTable.attach(align, 0,1, 0,1)
        self.viewChooser = chooser.ChooserWidget(viewertoolbox.viewNames(),
                                                 callback=self.setViewCB,
                                                 name="viewChooser")
        viewTable.attach(self.viewChooser.gtk, 1,2, 0,1)
        
        saveViewButton = gtk.Button("Save...")
        tooltips.set_tooltip_text(saveViewButton,
                                  "Save the current view settings.")
        gtklogger.setWidgetName(saveViewButton, "Save")
        gtklogger.connect(saveViewButton, 'clicked', self.saveViewCB)
        viewTable.attach(saveViewButton, 0,1, 1,2)
        deleteViewButton = gtk.Button("Delete...")
        tooltips.set_tooltip_text(deleteViewButton, "Delete a saved view.")
        gtklogger.setWidgetName(deleteViewButton, "Delete")
        gtklogger.connect(deleteViewButton, 'clicked', self.deleteViewCB)
        viewTable.attach(deleteViewButton, 1,2, 1,2)

        self.prevViewButton = gtkutils.prevButton()
        gtklogger.setWidgetName(self.prevViewButton, "Prev")
        gtklogger.connect(self.prevViewButton, 'clicked', self.historian.prevCB)
        tooltips.set_tooltip_text(self.prevViewButton,
                                  "Reinstate the previous view.")
        viewTable.attach(self.prevViewButton, 0,1, 2,3)

        self.nextViewButton = gtkutils.nextButton()
        gtklogger.setWidgetName(self.nextViewButton, "Next")
        gtklogger.connect(self.nextViewButton, 'clicked', self.historian.nextCB)
        tooltips.set_tooltip_text(self.nextViewButton,
                                  "Reinstate the next view.")
        viewTable.attach(self.nextViewButton, 1,2, 2,3)
        
        # Mouse handler for click-and-drag editing of clipping planes.
        self.clipMouseHandler = ClipPlaneMouseHandler(self, self.gfxwindow())

        self.sbcallbacks = [
            switchboard.requestCallbackMain("view changed", self.viewChangedCB),
            switchboard.requestCallbackMain("completed view change",
                                            self.completedViewChangeCB),
            switchboard.requestCallbackMain("new view", self.newViewCB),
            switchboard.requestCallbackMain("view deleted", self.viewDeletedCB),
            switchboard.requestCallbackMain(
                (self.toolbox, "clip planes changed"),
                self.updateClipList),
            switchboard.requestCallbackMain(
                (self.toolbox, "clip selection changed"),
                self.updateClipSelection),
            # switchboard.requestCallbackMain(
            #     (self.toolbox, "new clip plane"),
            #     self.newClipPlaneCB)
            ]

        self.sensitize()

    def activate(self):
        if not self.active:
            toolboxGUI.GfxToolbox.activate(self)
            # Get the current plane from the non-gui part of the
            # toolbox, where it's stored.
            plane = self.toolbox.currentClipPlane()
            if plane is not None:
                self.gfxwindow().oofcanvas.render()
                self.gfxwindow().toolbar.setSelect()

    def deactivate(self):
        if self.active:
            toolboxGUI.GfxToolbox.deactivate(self)
            plane = self.toolbox.currentClipPlane()
            if plane is not None:
                # switchboard.notify((self.toolbox, "clip selection changed"), None)
                self.gfxwindow().oofcanvas.render()

    def installMouseHandler(self):
        self.gfxwindow().setMouseHandler(self.clipMouseHandler)

    def close(self):
        self.clipMouseHandler.cancel()
        map(switchboard.removeCallback, self.sbcallbacks)
        toolboxGUI.GfxToolbox.close(self)

    def sensitize(self):
        planeOK = self.toolbox.currentClipPlane() is not None
        self.editclipbutton.set_sensitive(planeOK)
        self.delclipbutton.set_sensitive(planeOK)
        # self.invclipButton.set_sensitive(
        #     len(self.clippingListView.children()) > 0)
        self.prevViewButton.set_sensitive(self.historian.prevSensitive())
        self.nextViewButton.set_sensitive(self.historian.nextSensitive())
        self.gfxwindow().toolbar.sensitize(self)

    def camera_infoCB(self, *args):
        debug.mainthreadTest()
        #camera = self.gfxwindow().oofcanvas.getCamera()
        #reporter.report(camera)

    def updateCameraInfo(self):
        # TODO OPT: where should this be called???
        debug.mainthreadTest()
        canvas = self.gfxwindow().oofcanvas
        x,y,z = canvas.get_camera_position()
        self.camera_x.set_text("%f" %x)
        self.camera_y.set_text("%f" %y)
        self.camera_z.set_text("%f" %z)        
        x,y,z = canvas.get_camera_focal_point()
        self.fp_x.set_text("%f" %x)
        self.fp_y.set_text("%f" %y)
        self.fp_z.set_text("%f" %z)
        x,y,z = canvas.get_camera_view_up()
        self.viewup_x.set_text("%f" %x)
        self.viewup_y.set_text("%f" %y)
        self.viewup_z.set_text("%f" %z)
        dist = canvas.get_camera_distance()
        self.distance.set_text("%f" %dist)
        angle = canvas.get_camera_view_angle()
        self.viewangle.set_text("%f" %angle)


    # Translation callback functions
    ###########################################################

    def dollyin(self, *args):
        dollyfactor = float(self.dollyfactor.get_text())
        self.toolbox.menu.Dolly.In(factor=dollyfactor)

    def dollyout(self, *args):
        dollyfactor = float(self.dollyfactor.get_text())
        self.toolbox.menu.Dolly.Out(factor=dollyfactor)

    def dollyfill(self, *args):
        self.toolbox.menu.Dolly.Fill()

    def trackh(self, *args):
        d = float(self.trackdist.get_text())
        self.toolbox.menu.Track.Horizontal(distance=d)

    def trackv(self, *args):
        d = float(self.trackdist.get_text())
        self.toolbox.menu.Track.Vertical(distance=d)

    def recenter(self, *args):
        self.toolbox.menu.Track.Recenter()


    # Rotation Button Callback Functions
    ##############################################################

    def roll(self, *args):
        self._rotate(self.toolbox.menu.Rotate.Roll)

    def azimuth(self, *args):
        self._rotate(self.toolbox.menu.Rotate.Azimuth)
        
    def elevation(self, *args):
        self._rotate(self.toolbox.menu.Rotate.Elevation)

    def yaw(self, *args):
        self._rotate(self.toolbox.menu.Rotate.Yaw)

    def pitch(self, *args):
        self._rotate(self.toolbox.menu.Rotate.Pitch)

    def _rotate(self, menuitem):
        angle = float(self.angle.get_text())
        menuitem.callWithDefaults(angle=angle)

    # Zoom button callbacks

    def zoomInCB(self, *args):
        factor = float(self.zoomfactor.get_text())
        self.toolbox.menu.Zoom.In(factor=factor)

    def zoomOutCB(self, *args):
        factor = float(self.zoomfactor.get_text())
        self.toolbox.menu.Zoom.Out(factor=factor)

    def zoomFillCB(self, *args):
        self.toolbox.menu.Zoom.Fill()

    # Clipping
    ############################################################

    ## TODO 3.1: Edit clipping planes graphically using
    ## vtkImplicitPlaneWidget.  Or add a comment explaining why the
    ## ClipPlaneClickAndDragDisplay is better.

    def renderEnableCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        plane = model[iter][0]
        cell_renderer.set_active(plane.enabled())

    def enableCellCB(self, cell_renderer, path):
        plane, planeID = self.clippingList[path]
        if plane.enabled():
            self.toolbox.menu.Clip.Disable(plane=planeID)
        else:
            self.toolbox.menu.Clip.Enable(plane=planeID)

    def renderFlipCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        plane = model[iter][0]
        cell_renderer.set_active(plane.flipped())

    def flipCellCB(self, cell_renderer, path):
        plane, planeID = self.clippingList[path]
        if plane.flipped():
            self.toolbox.menu.Clip.Unflip(plane=planeID)
        else:
            self.toolbox.menu.Clip.Flip(plane=planeID)

    def renderNormalCol(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        assert model is self.clippingList
        plane = model[iter][0]
        cell_renderer.set_property('text', plane.normal().identifier())

    def renderOffsetCol(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        plane = model[iter][0]
        cell_renderer.set_property('text', `plane.offset()`)

    def newClipCB(self, button):
        menuitem = self.toolbox.menu.Clip.New
        if parameterwidgets.getParameters(title="New Clipping Plane",
                                          *menuitem.params):
            menuitem.callWithDefaults()
        
    def editClipCB(self, *args):
        # Edit button *and* double click callback.  Args aren't used.
        menuitem = self.toolbox.menu.Clip.Edit
        plane = self.toolbox.currentClipPlane()
        planeID = self.getCurrentClipPlaneNo()
        normarg = menuitem.get_arg("normal")
        # Hack.  See direction.spy.
        normarg.set(direction.Direction.rewrap(plane.normal()))
        offsetarg = menuitem.get_arg("offset")
        offsetarg.set(plane.offset())
        if parameterwidgets.getParameters(normarg, offsetarg, 
                                          title="Edit Clipping Plane"):
            menuitem.callWithDefaults(plane=planeID)
        
    def delClipCB(self, button):
        plane = self.getCurrentClipPlaneNo()
        if plane is not None:
            menuitem = self.toolbox.menu.Clip.Delete
            menuitem.callWithDefaults(plane=plane)
            # TODO: Is there a gtk signal associated with removing the
            # selection?  The mouse handler should be reset as a side
            # effect of that, probably in updateClipSelection
            self.gfxwindow().removeMouseHandler()

    def invClipCB(self, button):
        if self.invclipButton.get_active():
            menuitem = self.toolbox.menu.Clip.InvertOn
        else:
            menuitem = self.toolbox.menu.Clip.InvertOff
        menuitem.callWithDefaults()

    def suppressCB(self, button):
        if self.suppressButton.get_active():
            menuitem = self.toolbox.menu.Clip.SuppressOn
        else:
            menuitem = self.toolbox.menu.Clip.SuppressOff
        menuitem.callWithDefaults()

    def updateClipList(self, plane): 
        # Switchboard callback for "clip planes changed".  Called
        # after the graphics window is updated in response to a change
        # in clipping planes.  Rebuilds the list of clipping planes
        # using the clipping planes on the canvas.
        self.rebuildClipList()
        self.selectClipPlane(plane)
        self.sensitize()

    def rebuildClipList(self):
        # Don't use historian.current() to get the clip
        # planes!  The historian doesn't record new views if the
        # old and new views differ only in their clip planes.
        # The current clip planes have to come from the canvas
        # itself.
        currentView = self.gfxwindow().oofcanvas.get_view()
        curIndex = self.getCurrentClipPlaneNo()
        # We have to suppress the select signal, so that
        # self.clippingList.clear() won't call clipSelectionChangedCB.
        self.clipSelectSignal.block()
        selectedIter = None
        try:
            self.clippingList.clear()
            for i in range(currentView.nClipPlanes()):
                plane = currentView.getClipPlane(i).clone()
                newIter = self.clippingList.append([plane, i])
                # Reselect the plane at the same position in the list.
                # If the plane has been edited, it should remain
                # selected, even if it's now a different plane.  If
                # some other choice should have been made, the calling
                # routine will have to fix it.
                if i == curIndex:
                    selectedIter = newIter
            if selectedIter is not None:
                self.clippingListView.get_selection().select_iter(selectedIter)
        finally:
            self.clipSelectSignal.unblock()

    def clipSelectionChangedCB(self, selection): # gtk callback
        debug.mainthreadTest()
        plane, planeID = self.getCurrentClipPlaneAndID() # from widget
        if planeID == self.toolbox.currentClipPlaneNo:
            return

        if planeID is not None:
            menuitem = self.toolbox.menu.Clip.Select
            menuitem.callWithDefaults(plane=planeID)
        else:
            menuitem = self.toolbox.menu.Clip.Unselect
            menuitem.callWithDefaults()

    def updateClipSelection(self, plane): # "clip selection changed" sb callback
        # If a clipping plane has been selected in the list, set
        # the mouse handler to the mouse handler for
        # click-and-drag editing of clipping planes. Else, a
        # clipping plane has been unselected, so set the mouse
        # handler to self.
        if plane is not None:
            self.selectClipPlane(plane)
            # Put the toolbox in "Select" mode, so that the new plane
            # can be edited.
            self.gfxwindow().toolbar.setSelect() # installs mouse handler
        else:
            self.selectClipPlane(None)
            self.gfxwindow().removeMouseHandler()
        self.gfxwindow().updateview()

    def selectClipPlane(self, plane):
        # Select the given plane in the clipping list widget, without
        # invoking any callbacks.
        self.clipSelectSignal.block()
        try:
            selection = self.clippingListView.get_selection()
            selection.unselect_all()
            if plane is not None:
                # We have to check that plane is not None, because the
                # comparison in the if statement below will crash if
                # plane is None.  ClippingPlane.__eq__ isn't smart.
                model = self.clippingListView.get_model()
                iter = model.get_iter_first()
                while iter is not None:
                    if model[iter][0] == plane:
                        selection.select_iter(iter)
                        return
                    iter = model.iter_next(iter)
        finally:
            self.clipSelectSignal.unblock()

    def getCurrentClipPlane(self):
        # Get the currently selected clipping plane from the
        # clippingList.
        debug.mainthreadTest()
        selection = self.clippingListView.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][0]
        
    def getCurrentClipPlaneNo(self):
        # Get the index of the currently selected clipping plane in
        # the clipping List.  The list is in the same order as the
        # list stored in the canvas, so this int is used as the arg
        # for list modification menu items.
        debug.mainthreadTest()
        selection = self.clippingListView.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][1]

    def getCurrentClipPlaneAndID(self):
        selection = self.clippingListView.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return (model[iter][0], model[iter][1])
        else:
            return (None, None)

    # Save and Restore Views
    ############################################################

    def viewChangedCB(self, gfxwindow):
        # switchboard "view changed" callback.
        if gfxwindow is self.gfxwindow():
            view = gfxwindow.oofcanvas.get_view()
            # Do NOT update the historian here.  It should only record
            # complete changes, not the incremental steps that can
            # come from mouse motion on the canvas.
            self.updateCameraInfo()

    def completedViewChangeCB(self, gfxwindow):
        # switchboard callback for "completed view change".  When a
        # change in view is complete, the view must be recorded by the
        # historian.  This is not called when a new view is installed
        # *by* the historian.
        if gfxwindow is self.gfxwindow():
            view = gfxwindow.oofcanvas.get_view()
            self.historian.record(view)

    # Switchboard "new view" callback, called when a named View has
    # been created.
    def newViewCB(self, name):
        self.viewChooser.update(viewertoolbox.viewNames())
        self.viewChooser.set_state(name)

    def viewDeletedCB(self, name): # sb "view deleted"
        if self.viewChooser.get_value() == name:
            self.viewChooser.update(viewertoolbox.viewNames() + [""])
            self.viewChooser.set_state("")
        else:
            self.viewChooser.update(viewertoolbox.viewNames())

    def setViewCB(self, *args):   # viewChooser callback
        viewname = self.viewChooser.get_value()
        self.toolbox.setView(viewname)

    def saveViewCB(self, *args): # button callback
        menuitem = self.toolbox.menu.Save_View
        namearg = menuitem.get_arg('name')
        if parameterwidgets.getParameters(namearg,
                                          title="Save the current View"):
            menuitem.callWithDefaults()

    def deleteViewCB(self, *args): # button callback
        menuitem = self.toolbox.menu.Delete_View
        viewarg = menuitem.get_arg("view")
        if parameterwidgets.getParameters(viewarg,
                                          title="Choose a View to delete"):
            menuitem.callWithDefaults()
    
    def restoreHistoricalView(self, view):
        # Callback for the Prev and Next buttons, via the historian.
        # This can't just call Settings.Camera.View, because that
        # calls completedViewChangeCB (above).
        menuitem = self.toolbox.menu.Restore_View
        menuitem.callWithDefaults(view=view)

# End class ViewerToolbox3DGUI

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _makeGUI(self):
    return ViewerToolbox3DGUI(self)

viewertoolbox.ViewerToolbox.makeGUI = _makeGUI

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Widget that lists only the UserDefinedViews (ie the deletable ones).

class ViewNameWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        views = [vname for vname,view in viewertoolbox.namedViews.items()
                 if view.deletable]
        self.chooser = chooser.ChooserWidget(views, name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.chooser.gtk,
                                                  scope=scope, verbose=verbose)
        self.widgetChanged(len(views) > 0, interactive=False)
    def get_value(self):
        return self.chooser.get_value()
    def set_value(self, name):
        self.chooser.set_state(name)
    
def _makeViewWidget(self, scope=None, verbose=False):
    return ViewNameWidget(self, scope=scope, name=self.name, verbose=verbose)

viewertoolbox.ViewNameParameter.makeWidget = _makeViewWidget

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# ClipPlaneMouseHandler is the mouseHandler for
# click-and-drag editing of clipping planes.

# TODO: This does not work in unthreaded mode. See if something can be
# done about this.

class ClipPlaneMouseHandler(mousehandler.MouseHandler):
    def __init__(self, tbGUI, gfxwindow):
        self.gfxwindow = gfxwindow
        # Because this constructor has been called by the
        # ViewerToolbox3DGUI constructor, the ViewerToolbox3DGUI isn't
        # completely built yet, and we can't use
        # gfxwindow.getToolboxGUIByName to find it.  We hae to pass it
        # in as a constructor argument.
        self.toolboxGUI = tbGUI
        self.toolbox = self.toolboxGUI.toolbox
        

        # The ID of the clip plane being edited.
        self.planeID = None

        # The display method for the click-and-drag editing.
        self.layer = None

        # Which operation should be performed (e.g. translate, rotate).
        self.operation = None

        # Previous position, in display coordinates, of the mouse.
        self.last_x = None
        self.last_y = None

        # The clicked point on one of the vtkActors, in world
        # coordinates. Used when self.operation is 'translate in
        # plane'.
        self.click_pos = None

        # datalock is an EventLogSlock on the eventList data. It has
        # (internally) a newEvents flag that is set to true every time
        # it is acquired and then released by the mainthread in either
        # self.up, self.down, or self.move.
        #
        # If the subthread that is executing
        # self.processEvents_subthread tries to acquire this lock
        # while the newEvents flag is false, it will wait (block)
        # until this lock is acquired and subsequently released by the
        # mainthread, and then proceed to process whatever new mouse
        # event the mainthread has just logged.
        #
        # If, however, the newEvents flag is true when the subthread
        # comes back to the beginning of its internal loop, it means
        # at least one new event has already been logged while the
        # subthread was processing an earlier event. So, in this case,
        # the subthread will go ahead and process that new event
        # without waiting.
        self.datalock = lock.EventLogSLock()

        # For keeping track of which events have happened in what
        # order. This list has a EventLogSLock on it, datalock.  The
        # mainthread must acquire datalock in order to append a new
        # event to it, and the subthread must acquire datalock in
        # order to pop an event from it.
        self.eventlist = []

        # 'up' and 'move' mouse events will only be
        # accepted when self.downed is True.
        self.downed = False
        
        # # Will be True when the time comes for the subthread executing
        # # self.processEvents_subthread to be killed.
        # self.canceled = False

        # Process all mouse events in a subthread.
        ## TODO: Can we have just one daemon thread, shared by all
        ## toolboxes in all graphics windows?  One per toolbox seems
        ## excessive.  Have a shared eventlist, and store the toolbox
        ## as part of the event.
        self.eventThread = subthread.daemon(self.processEvents_subthread)
        
    def up(self, x, y, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            self.downed = False
            self.eventlist.append(('up', x, y, shift, ctrl))
        finally:
            self.datalock.logNewEvent_release()
        
    def down(self, x, y, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            self.downed = True
            self.eventlist.append(('down', x, y, shift, ctrl))
        finally:
            self.datalock.logNewEvent_release()

    def move(self, x, y, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            num_events = len(self.eventlist)
            if num_events == 0:
                # All events have been processed so far. Append the
                # new move event to the list.
               self.eventlist.append(('move', x, y, shift, ctrl))
            elif self.eventlist[num_events - 1][0] == 'down':
                # Previous event was a down event. Append the new move
                # event to the list.
                self.eventlist.append(('move', x, y, shift, ctrl))
            elif self.eventlist[num_events - 1][0] == 'move':
                # Previous event was a move event. Overwrite that
                # event with the new move event.
                self.eventlist[num_events - 1] = ('move', x, y, shift, ctrl)
        finally:
            self.datalock.logNewEvent_release()

    def processUp(self):
        # Commands which need to be run when an 'up' event is being
        # processed.  Called by processEvents_subthread on the
        # subthread.
        if self.operation in ('rotate about center', 'translate along normal'):
            # The mouse has been released after the user has edited
            # the clipping plane by clicking and dragging.  Any
            # changes to the currently selected clipping plane have
            # already occurred. We call logWithDefaults for the 'Edit'
            # menu item, thereby making sure the changes to that
            # clipping plane are logged (and thus are repeatable by a
            # script), while at the same time making sure that the
            # 'Edit' menu item callback, editCB in viewertoolbox.py,
            # does not get called. We don't want editCB to get called
            # because we don't want to perform changes we've already
            # made. Also, we've already acquired the gfxlock in
            # processEvents_subthread, and editCB tries to acquire the
            # gfxlock, so it doesn't work to have it called here.
            menuitem = self.toolbox.menu.Clip.Edit
            menuitem.logWithDefaults(plane=self.toolbox.currentClipPlaneNo(),
                                     normal=direction.Direction.rewrap(
                                         self.layer.canvaslayer.get_normal()),
                                     offset=self.layer.canvaslayer.get_offset())
            mainthread.runBlock(self.toolboxGUI.rebuildClipList)
            # mainthread.runBlock(self.toolboxGUI.updateClipList,
            #                     (self.gfxwindow,))
        self.operation = None
        self.last_x = None
        self.last_y = None
        self.layer = None
        self.click_pos = None
        self.planeID = None

    def processDown(self, x, y, ctrl):
        # Commands which need to be run when a 'down' event is being
        # processed.  Called by processEvents_subthread on the
        # subthread.

        # Figure out which clip plane is being edited.
        self.planeID = self.toolbox.currentClipPlaneNo()

        # Find the clicked point in physical coordinates.
        viewobj = mainthread.runBlock(self.gfxwindow.oofcanvas.get_view)
        point = mainthread.runBlock(self.gfxwindow.oofcanvas.display2Physical,
                                    (viewobj, x, y))
        self.last_x = x
        self.last_y = y
        if ctrl:
            # Ctrl button was pressed when mouse was clicked down.

            # Find the position at which a vtkActor, if any,  was
            # clicked.
            (self.click_pos, self.layer) = self.gfxwindow.findClickedPositionOnActor_nolock(
                clipplaneclickanddragdisplay.ClipPlaneClickAndDragDisplay,
                point, 
                viewobj)
            if self.click_pos is not None:
                # Either the plane or arrow has been
                # clicked. Perform the 'translate in plane'
                # operation.
                self.operation = 'translate in plane'
        else:
            # Ctrl button was not pressed when mouse was clicked down.

            # Find the vtkActors that have been clicked upon.
            (actors, self.layer) = self.gfxwindow.findClickedActors_nolock(
                clipplaneclickanddragdisplay.ClipPlaneClickAndDragDisplay,
                point, 
                viewobj)
            if actors is not None:
                # Something has been clicked.  Decide the operation to
                # perform based on which actors were clicked. A click
                # on the arrow takes precedence over a click on the
                # plane, so it is assumed that if the user clicked on
                # the arrow through the plane, the user still intended
                # to select the arrow, and not the plane.  This makes
                # some sense so long as the plane is rendered opaque
                # (so that the arrow can be seen through it); the only
                # time this would not be the case is if the
                # plane_opacity setting for self.layer were set to
                # 1.0.
                if (actors.hasActor(self.layer.canvaslayer.get_arrowActor())):
                    self.operation = 'rotate about center'
                elif (actors.hasActor(self.layer.canvaslayer.get_planeActor())):
                    self.operation = 'translate along normal'
     
    def processMove(self, x, y):
        # Commands which need to be run when a 'move' event is being
        # processed.  Called by processEvents_subthread on the
        # subthread.
        viewobj = mainthread.runBlock(self.gfxwindow.oofcanvas.get_view)
        if (self.operation == 'rotate about center'):
            last_mouse_coords_rotated_90_deg = mainthread.runBlock(
                self.gfxwindow.oofcanvas.display2Physical,
                (viewobj, -self.last_y, self.last_x))
            mouse_coords_rotated_90_deg = mainthread.runBlock(
                self.gfxwindow.oofcanvas.display2Physical,
                (viewobj, -y, x))
            axis_of_rotation =  (mouse_coords_rotated_90_deg -
                                 last_mouse_coords_rotated_90_deg)
            angle_of_rotation = math.sqrt((x - self.last_x) ** 2 +
                                          (y - self.last_y) ** 2)

            # Update the canvaslayer.
            self.layer.canvaslayer.rotate(axis_of_rotation, angle_of_rotation)

            # Update the actual clipping plane from the canvaslayer's
            # values.
            newplane = clip.ClippingPlane(self.layer.canvaslayer.get_normal(),
                                          self.layer.canvaslayer.get_offset())
            viewobj.replaceClipPlane(self.planeID, newplane)
            self.toolbox.setCurrentClipPlane(newplane)
            
        elif (self.operation == 'translate along normal'):
            last_mouse_coords = mainthread.runBlock(
                self.gfxwindow.oofcanvas.display2Physical,
                (viewobj, self.last_x, self.last_y))
            mouse_coords = mainthread.runBlock(
                self.gfxwindow.oofcanvas.display2Physical, (viewobj, x, y))
            diff = mouse_coords - last_mouse_coords
            diff_size = math.sqrt(diff ** 2)
            if diff_size == 0:
                return
            diff = diff / diff_size
            normal = self.layer.canvaslayer.get_normal_Coord3D()
            center = self.layer.canvaslayer.get_center()
            camera_pos = mainthread.runBlock(
                self.gfxwindow.oofcanvas.get_camera_position_v2)
            dist = math.sqrt((camera_pos - center) ** 2)
            view_angle = mainthread.runBlock(
                self.gfxwindow.oofcanvas.get_camera_view_angle)
            canvas_size = mainthread.runBlock(
                self.gfxwindow.oofcanvas.get_size)
            offset = (diff.dot(normal) * dist *
                      math.tan(math.radians(view_angle))
                      * math.sqrt((x - self.last_x) ** 2 +
                                  (y - self.last_y) ** 2) / canvas_size[1])

            # Update the canvaslayer.
            self.layer.canvaslayer.offset(offset) 

            # Update the actual clipping plane from the canvaslayer's
            # values.
            newplane = clip.ClippingPlane(self.layer.canvaslayer.get_normal(),
                                          self.layer.canvaslayer.get_offset())
            viewobj.replaceClipPlane(self.planeID, newplane)
            self.toolbox.setCurrentClipPlane(newplane.clone())
            ## TODO: Update the parameters of the plane in clippingListView
            
        elif (self.operation == 'translate in plane'):
            # NOTE: Sometimes this *appears* to leave the plane and
            # arrow widget in an incorrect location, in which the
            # widget's plane is offset from the actual clipping plane.
            # This is a trick of perspective due to a lack of depth
            # cues.  The planes do agree, but the square representing
            # the widget's plane does not intersect the intersection
            # of the plane with the Microstructure.
            mouse_coords = mainthread.runBlock(
                self.gfxwindow.oofcanvas.display2Physical, (viewobj, x, y))
            ray_to_mouse = mainthread.runBlock(
                self.gfxwindow.oofcanvas.findRayThroughPoint, (mouse_coords,))
            normal = self.layer.canvaslayer.get_normal_Coord3D()
            translation_vector \
                = (ray_to_mouse *
                   (self.click_pos - mouse_coords).dot(normal) +
                   ray_to_mouse.dot(normal) * (mouse_coords - self.click_pos))
            cam_direction = mainthread.runBlock(
                self.gfxwindow.oofcanvas.get_camera_direction_of_projection_v2)
            if (math.fabs(cam_direction.dot(normal)) < THRESHOLD):
                cross = cam_direction.cross(normal)
                translation_vector = ((translation_vector.dot(cross) * cross) /
                                      (cross ** 2))
            if math.fabs(ray_to_mouse.dot(normal)) == 0:
                return
            translation_vector = translation_vector / ray_to_mouse.dot(normal)
            self.click_pos = self.click_pos + translation_vector

            # Update the canvaslayer.
            self.layer.canvaslayer.translate(translation_vector)
        # Set the old x and y mouse positions to the current x and y
        # positions.
        self.last_x = x
        self.last_y = y

        mainthread.runBlock(self.gfxwindow.oofcanvas.set_view,
                            (viewobj, True))
        # Render the changes to the vtk plane and arrow and to the
        # actual clipping planes.
        mainthread.runBlock(self.gfxwindow.oofcanvas.render)

    def processEvents_subthread(self):
        # Executed in a subthread. Updates the click-and-drag editing
        # widget and determines what needs to be rendered based on the
        # mouse events that have occurred.
        while (True):
            # Get the data from a new event. If no new event has
            # occurred, handleNewEvents_acquire will block this
            # subthread until a new event occurs.
            self.datalock.handleNewEvents_acquire()
            try:
                (eventtype, x, y, shift, ctrl) = self.eventlist.pop(0);
            finally:
                self.datalock.handleNewEvents_release()

            # Acquire the gfxlock so that we can be sure that the
            # gfxwindow is not in the middle of being changed or
            # closed at this time.
            self.gfxwindow.acquireGfxLock()
            try:
                if eventtype is 'down':
                    self.processDown(x, y, ctrl)
                elif eventtype is 'move' and self.operation is not None:
                    self.processMove(x, y)
                elif eventtype is 'up':
                    self.processUp()
            finally:
                self.gfxwindow.releaseGfxLock()

    def cancel(self):
        # The subthread is a daemon thread and doesn't need to be
        # cancelled, but it should stop processing data.  If it
        # weren't a daemon, the program wouldn't exit until the thread
        # were killed.
        self.eventlist = []

    def acceptEvent(self, eventtype):
        return (eventtype == 'down' or
                (self.downed and eventtype in ('move', 'up')))

