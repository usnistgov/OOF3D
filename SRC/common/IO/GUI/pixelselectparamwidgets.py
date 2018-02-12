# -*- python -*-
# $RCSfile: pixelselectparamwidgets.py,v $
# $Revision: 1.1.2.1 $
# $Author: rdw1 $
# $Date: 2015/08/07 12:56:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common import pixelselectionmethod
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.SWIG.common import switchboard
import gtk
import math

# VoxelRegionSelectWidgets are the GTK widgets to be built by the
# PixelSelectToolboxGUI's registered class factory for selection
# method registrations such as "Box", "Ellipsoid", etc. that let the
# user select 3D regions of voxels. The created widget is a wrapper
# for a ParameterTable, in case the selection method has parameters
# which the user should be able to adjust from the gtk part of the
# GUI. The main new feature of VoxelRegionSelectWidgets is that they
# have a 'Done' button which the user can press when the user is done
# performing any steps in the 3D oofcanvas necessary for specifying
# the 3D region enclosing all the voxels they wish to select.  Each
# widget is associated with a SelectionMethodGUI.

# The SelectionMethodGUI is an object that manages both the gtk-based
# VoxelRegionSelectWidget and any associated vtk-based 3D widget on
# the oofcanvas which the user may be interacting with via the
# mouse. The SelectionMethodGUI handles communication between these
# two parts of the GUI. These two parts of the GUI must go
# hand-in-hand, since it makes little sense for them to exist
# separately.

class VoxelRegionSelectWidget(parameterwidgets.ParameterWidget):
    def __init__(self, selectionmethodGUI, params, scope=None, name=None, showLabels=True, data={}, verbose=False):
        debug.mainthreadTest()
        self.selectionmethodGUI = selectionmethodGUI
        self.params = params

        # A VBox, which will be the self.gtk attribute of this
        # ParameterWidget.
        base = gtk.VBox()
        parameterwidgets.ParameterWidget.__init__(self, base, scope=scope, name=name, verbose=verbose)

        # A ParameterTable for the params passed into the constructor.
        self.parameterTable = parameterwidgets.ParameterTable(params, scope=scope, name=name, showLabels=showLabels, data=data, verbose=verbose)
        base.pack_start(self.parameterTable.gtk, expand=0, fill=0)

        # This is a VBox holding extra GUI content that we want a
        # PixelSelectionMethodFactory to build for certain
        # PixelSelectionMethodRegistrations.
        self.extraGUIbox = gtk.VBox()
        base.pack_start(self.extraGUIbox, expand=0, fill=0)

        # Instructions for using the associated pixel SelectionMethod.
        # TODO: Make these look nicer. Tailor them to different region
        # shapes (e.g. we probably want different instructions if
        # we're trying to select an ellipsoid-shaped region).
        label = gtk.Label("How to use this tool:\n  Click image to begin editing a box-shaped region.\n  (Click a face/edge/corner of the box)+Move to\n    adjust the boundaries of the box.\n  Click 'Done' to finish editing the region, and\n    select all voxels within that region.")

        label.set_justify(gtk.JUSTIFY_LEFT)
        self.extraGUIbox.pack_start(label, fill=0, expand=0, padding=2)

        # COSMETIC: This aligns the button that we are creating with
        # the center of extraGUIBox.       
        alignment = gtk.Alignment(xalign=0.5, yalign=0.5)
        self.extraGUIbox.pack_start(alignment, expand=0, fill=0)

        # COSMETIC: hbox is simply here in order to contain the 'Done'
        # button, thereby forcing the 'Done' button to remain a fixed
        # width.
        # TODO?: Stick a 'Cancel' button in here so that the user can
        # quit editing a region without selecting any voxels.
        hbox = gtk.HBox()
        alignment.add(hbox)
        hbox.set_homogeneous(True)

        # Clicking the "Start" button brings up the voxel selection
        # widget.
        self.startbutton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD, 'Start')
        gtklogger.setWidgetName(self.startbutton, "Start")
        gtklogger.connect(self.startbutton, 'clicked', self.startCB)
        tooltips.set_tooltip_text(self.startbutton,
                                  "Start choosing voxels graphically.")
        hbox.pack_start(self.startbutton, expand=0, fill=0)
       
        # A button that the user presses once they are done adjusting
        # the region containing the voxels which they wish to select,
        # and are ready to perform the actual selection.
        self.donebutton = gtkutils.StockButton(gtk.STOCK_APPLY, 'Done')
        gtklogger.setWidgetName(self.donebutton, "Done")
        gtklogger.connect(self.donebutton, 'clicked', self.doneCB)
        tooltips.set_tooltip_text(self.donebutton, "Click when you are done editing the displayed region. All the voxels within that region will then be selected.")
        hbox.pack_start(self.donebutton, expand=0, fill=0) 

        self.cancelbutton = gtkutils.StockButton(gtk.STOCK_CANCEL, "Cancel")
        gtklogger.setWidgetName(self.cancelbutton, 'Cancel')
        gtklogger.connect(self.cancelbutton, 'clicked', self.cancelCB)
        tooltips.set_tooltip_text(
            self.cancelbutton,
            "Stop choosing voxels without selecting anything.")
        hbox.pack_start(self.cancelbutton, expand=0, fill=0)
        
        self.sensitize()

    def show(self):
        # This had to be redefined from base class ParameterWidget.
        debug.mainthreadTest()
        self.gtk.show()
        self.parameterTable.show()
        self.extraGUIbox.show_all()
    
    def destroy(self):
        # Redefined from base class.
        self.parameterTable.destroy()
        parameterwidgets.ParameterWidget.destroy(self)

    def cleanUp(self):
        # Redefined from base class. This must tell its
        # selectmethodGUI that it is destroyed.
        self.selectionmethodGUI.widget = None
        self.selectionmethodGUI = None
        parameterwidgets.ParameterWidget.cleanUp(self)

    def get_values(self):
        debug.mainthreadTest()
        self.parameterTable.get_values()
        self.params = self.parameterTable.params

    def startCB(self, button):
        self.selectionmethodGUI.start()
        self.sensitize()

    def cancelCB(self, button):
        self.selectionmethodGUI.done()
        self.sensitize()

    def doneCB(self, button):
        # Switchboard callback, called when the 'Done' button is
        # pressed. This causes the 'Done' button to be desensitized.
        self.selectionmethodGUI.done()
        self.sensitize()
        # TODO: Actually make the selection

    def sensitize(self):
        # Decides whether or not the 'Done' button should be sensitive
        # (clickable) at the moment. If the user is currently editing
        # the region that will bound all the voxels that the user
        # wishes to select, then
        # self.selectionmethodGUI.region_editing_in_progress will be
        # True. In this case, the 'Done' button will become sensitive.
        # Otherwise, the button will remain insensitive until the user
        # begins editing a new region to be selected.
        self.donebutton.set_sensitive(
            self.selectionmethodGUI.region_editing_in_progress)

