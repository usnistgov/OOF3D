# -*- python -*-
# $RCSfile: viewertoolbox3dGUI.py,v $
# $Revision: 1.3.10.39 $
# $Author: langer $
# $Date: 2014/10/17 21:48:05 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import direction
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import utils
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
        

        ## TODO 3.1: Clipping plane operations
        ##   Delete all
        ##   Save/Load?
        ##   Copy to/from other window
        ##   Click & drag editing
        
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
        


        # # position information
        # voxelinfoFrame = gtk.Frame("Voxel Info")
        # voxelinfoFrame.set_shadow_type(gtk.SHADOW_IN)
        # mainbox.pack_start(voxelinfoFrame)
        # voxelinfoBox = gtk.VBox()
        # voxelinfoFrame.add(voxelinfoBox)
        # voxelinfotable = gtk.Table(rows=3,columns=2)
        # voxelinfoBox.pack_start(voxelinfotable, expand=False, fill=False)
        # label = gtk.Label('x=')
        # label.set_alignment(1.0, 0.5)
        # voxelinfotable.attach(label, 0,1, 0,1, xpadding=5, xoptions=gtk.FILL)
        # self.xtext = gtk.Entry()
        # self.xtext.set_size_request(ndigits*guitop.top().digitsize, -1)
        # voxelinfotable.attach(self.xtext, 1,2, 0,1,
        #                   xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        # label = gtk.Label('y=')
        # label.set_alignment(1.0, 0.5)
        # voxelinfotable.attach(label, 0,1, 1,2, xpadding=5, xoptions=gtk.FILL)
        # self.ytext = gtk.Entry()
        # self.ytext.set_size_request(ndigits*guitop.top().digitsize, -1)
        # voxelinfotable.attach(self.ytext, 1,2, 1,2,
        #                   xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        # label = gtk.Label('z=')
        # label.set_alignment(1.0, 0.5)
        # voxelinfotable.attach(label, 0,1, 2,3, xpadding=5, xoptions=gtk.FILL)
        # self.ztext = gtk.Entry()
        # self.ztext.set_size_request(ndigits*guitop.top().digitsize, -1)
        # voxelinfotable.attach(self.ztext, 1,2, 2,3,
        #                   xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)


        self.sbcallbacks = [
            switchboard.requestCallbackMain("view changed", self.viewChangedCB),
            switchboard.requestCallbackMain("view restored",
                                            self.viewRestoredCB),
            switchboard.requestCallbackMain("new view", self.newViewCB),
            switchboard.requestCallbackMain("view deleted", self.viewDeletedCB),
            switchboard.requestCallbackMain("clip planes changed",
                                            self.updateClipList)
            ]

        self.sensitize()

    def activate(self):
        if not self.active:
            toolboxGUI.GfxToolbox.activate(self)
            self.gfxwindow().setMouseHandler(self)
            self.gfxwindow().toolbar.setSelect()

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        toolboxGUI.GfxToolbox.close(self)

    def sensitize(self):
        planeOK = self.currentClipPlane() is not None
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
    ## vtkImplicitPlaneWidget.

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
        plane = self.currentClipPlane()
        planeID = self.currentClipPlaneNo()
        normarg = menuitem.get_arg("normal")
        # Hack.  See direction.spy.
        normarg.set(direction.Direction.rewrap(plane.normal()))
        offsetarg = menuitem.get_arg("offset")
        offsetarg.set(plane.offset())
        if parameterwidgets.getParameters(normarg, offsetarg, 
                                          title="Edit Clipping Plane"):
            menuitem.callWithDefaults(plane=planeID)

    def delClipCB(self, button):
        plane = self.currentClipPlaneNo()
        if plane is not None:
            menuitem = self.toolbox.menu.Clip.Delete
            menuitem.callWithDefaults(plane=plane)

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

    def updateClipList(self, gfxwindow): # sb callback for "clip planes changed"
        if gfxwindow is self.gfxwindow():
            ## Don't use historian.current() to get the clip
            ## planes!  The historian doesn't record new views if the
            ## old and new views differ only in their clip planes.
            ## The current clip planes have to come from the canvas
            ## itself.
            currentView = self.gfxwindow().oofcanvas.get_view()
            self.clippingList.clear()
            for i in range(currentView.nClipPlanes()):
                plane = currentView.getClipPlane(i).clone()
                self.clippingList.append([plane, i])
            self.sensitize()

    def clipSelectionChangedCB(self, selection):
        debug.mainthreadTest()
        self.sensitize()

    def currentClipPlane(self):
        # Get the currently selected clipping plane from the
        # clippingList.
        debug.mainthreadTest()
        selection = self.clippingListView.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][0]
        
    def currentClipPlaneNo(self):
        # Get the index of the currently selected clipping plane in
        # the clipping List.  The list is in the same order as the
        # list stored in the canvas, so this int is used as the arg
        # for list modification menu items.
        debug.mainthreadTest()
        selection = self.clippingListView.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][1]

    # Save and Restore Views
    ############################################################

    def viewChangedCB(self, gfxwindow):
        # switchboard "view changed" callback.
        if gfxwindow is self.gfxwindow():
            view = gfxwindow.oofcanvas.get_view()
            self.historian.record(view)
            self.updateCameraInfo()
            name, names = viewertoolbox.retrieveViewNames(gfxwindow)
            self.viewChooser.update(names)
            self.viewChooser.set_state(name)

    def viewRestoredCB(self, gfxwindow):
        # switchboard "view restored" callback.  This is just like
        # viewChangedCB, but it doesn't record the new state in the
        # historian.  The new state just came from the historian.
        if gfxwindow is self.gfxwindow():
            self.updateCameraInfo()
            name, names = viewertoolbox.retrieveViewNames(gfxwindow)
            self.viewChooser.update(names)
            self.viewChooser.set_state(name)

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
        # calls viewChangedCB (above), which calls historian.record,
        # which shouldn't be called when recovering a previous view.
        # This menu item invokes viewRestoredCB, instead.
        menuitem = self.toolbox.menu.Restore_View
        menuitem.callWithDefaults(view=view)

    # Mouse interactions

    ###############################################################
    # def acceptEvent(self, eventtype):
    #     return eventtype == "up"

    # def up(self, x, y, shift, ctrl):
    #     # TODO OPT: should we pass in the bounds of the microstructure?
    #     p = self.gfxwindow().oofcanvas.screen_coords_to_3D_coords(x,y)
    #     MS = self.findMicrostructure()
    #     if p is not None and MS is not None:
    #         voxel = MS.pixelFromPoint(primitives.Point(p[0],p[1],p[2]));
    #         self.xtext.set_text(str(voxel[0]))
    #         self.ytext.set_text(str(voxel[1]))
    #         self.ztext.set_text(str(voxel[2]))

    ##############################################################

    ## Moved to ghostgfxwindow.py
    # def findMicrostructure(self):
    #     who = self.toolbox.gfxwindow().topwho('Microstructure', 'Image',
    #                                           'Skeleton', 'Mesh')
    #     if who is not None:
    #         return who.getMicrostructure()

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
