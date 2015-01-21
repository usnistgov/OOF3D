# -*- python -*-
# $RCSfile: meshcstoolboxGUI.py,v $
# $Revision: 1.47.4.3 $
# $Author: langer $
# $Date: 2013/11/08 20:45:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# GUI part of the Mesh cross-section toolbox.  Collects mouse
# clicks, draws paths, etc.

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO.GUI import rubberband
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import utils
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.common.IO.GUI import tooltips
from ooflib.engine import analysisdomain
from ooflib.engine import analysissample
from ooflib.engine import mesh
from ooflib.engine.IO import analyze
from ooflib.engine.IO import analyzemenu
from ooflib.engine.IO import meshcstoolbox
from ooflib.engine.IO import meshmenu
from ooflib.engine.IO import outputdestination
from ooflib.engine.IO.GUI import outputdestinationwidget
from ooflib.engine.IO.GUI import sampleregclassfactory
import gtk

# String displayed in the cross section chooser to mean that no cs is
# selected.
noCS = '<None>'

class CrossSectionToolboxGUI(toolboxGUI.GfxToolbox,
                             mousehandler.MouseHandler):
    def __init__(self, toolbox):
        toolboxGUI.GfxToolbox.__init__(
            self, utils.underscore2space(toolbox.name()), toolbox)

        mainbox = gtk.VBox()
        self.gtk.add(mainbox)

        sourceframe = gtk.Frame("Source")
        sourceframe.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(sourceframe, fill=0, expand=0)
        sourcescroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(sourcescroll, "Source")
        sourceframe.add(sourcescroll)
        sourcescroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_NEVER)
        datatable = gtk.Table(rows=2,columns=2)
        sourcescroll.add_with_viewport(datatable)
        
        meshlabel = gtk.Label("mesh = ")
        meshlabel.set_alignment(1.0, 0.5)
        self.meshname = gtk.Label()
        gtklogger.setWidgetName(self.meshname,"meshname")
        self.meshname.set_alignment(0.0, 0.5)

        datatable.attach(meshlabel, 0, 1, 0, 1)
        datatable.attach(self.meshname, 1, 2, 0, 1)

        layerlabel = gtk.Label("output = ")
        layerlabel.set_alignment(1.0, 0.5)
        self.layername = gtk.Label()
        gtklogger.setWidgetName(self.layername,"layername")
        self.layername.set_alignment(0.0, 0.5)

        datatable.attach(layerlabel, 0, 1, 1, 2)
        datatable.attach(self.layername, 1, 2, 1, 2)


        csframe = gtk.Frame("Cross Section")
        csframe.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(csframe, expand=0, fill=0)
        csbox = gtk.VBox()
        csframe.add(csbox)

        # Table contains the "current" and "points" widgets
        table = gtk.Table(rows=2, columns=2)
        csbox.pack_start(table, expand=0, fill=0)

        # Widget which shows the name of the current cross-section.
        label = gtk.Label("current: ")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, 0,1, xoptions=0)
        self.csChooser = chooser.ChooserWidget([], callback=self.csChooserCB,
                                               name='csList')
        table.attach(self.csChooser.gtk, 1,2, 0,1,
                     xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)

        # Widget for how to sample the cross-section.
        label = gtk.Label("points: ")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, 1,2, xoptions=0)

        self.cs_sample_widget = sampleregclassfactory.SampleRCF(
            name="Sampling", 
            domainClass=analysisdomain.CrossSectionDomain,
            operationClass=analyze.DirectOutput)
        table.attach(self.cs_sample_widget.gtk, 1,2, 1,2,
                     xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
        self.cs_sample_widget.update(analysissample.SampleSet.registry)
        self.int_valid_swcb = switchboard.requestCallbackMain(
            ('validity', self.cs_sample_widget), self.validCB)

        hbox = gtk.HBox()
        csbox.pack_start(hbox, expand=0, fill=0, padding=1)
        # Rename button.
        self.renamebutton = gtk.Button("Rename")
        gtklogger.setWidgetName(self.renamebutton, 'Rename')
        gtklogger.connect(self.renamebutton, 'clicked', self.csrenameCB)
        tooltips.set_tooltip_text(self.renamebutton,
                             "Rename the current cross-section.")
        hbox.pack_start(self.renamebutton,fill=1,expand=1, padding=1)
        # Edit button
        self.editbutton = gtkutils.StockButton(gtk.STOCK_EDIT, "Edit...")
        gtklogger.setWidgetName(self.editbutton, 'Edit')
        gtklogger.connect(self.editbutton, 'clicked', self.cseditCB)
        tooltips.set_tooltip_text(self.editbutton,"Edit the current cross-section.")
        hbox.pack_start(self.editbutton, fill=1, expand=1, padding=1)
        # Copy button
        self.copybutton = gtkutils.StockButton(gtk.STOCK_COPY, "Copy...")
        gtklogger.setWidgetName(self.copybutton, 'Copy')
        gtklogger.connect(self.copybutton, 'clicked', self.cscopyCB)
        tooltips.set_tooltip_text(self.copybutton,"Copy the current cross-section.")
        hbox.pack_start(self.copybutton, fill=1, expand=1, padding=1)
        # Delete button.
        self.csdeletebutton = gtkutils.StockButton(gtk.STOCK_DELETE, "Remove")
        gtklogger.setWidgetName(self.csdeletebutton, 'Remove')
        gtklogger.connect(self.csdeletebutton, "clicked", self.csdeleteCB)
        tooltips.set_tooltip_text(self.csdeletebutton,
                             "Remove the current cross-section.")
        hbox.pack_start(self.csdeletebutton,fill=1,expand=1, padding=1)

        goframe = gtk.Frame("Output")
        goframe.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(goframe,expand=0,fill=0)
        self.gobox = gtk.VBox()
        goframe.add(self.gobox)

        hbox = gtk.HBox()
        self.gobox.pack_start(hbox, expand=0, fill=0)
        label = gtk.Label("Destination: ")
        label.set_alignment(1.0, 0.5)
        hbox.pack_start(label, expand=0, fill=0)
        self.destwidget = outputdestinationwidget.TextDestinationWidget(
            name="Destination")
        self.dw_valid_swcb = switchboard.requestCallbackMain(
            ('validity', self.destwidget), self.validCB )
        hbox.pack_start(self.destwidget.gtk, expand=1, fill=1, padding=2)
        self.gobutton = gtkutils.StockButton(gtk.STOCK_EXECUTE, "Go!")
        gtklogger.setWidgetName(self.gobutton, 'Go')
        hbox.pack_start(self.gobutton,expand=1,fill=1, padding=2)
        tooltips.set_tooltip_text(self.gobutton,
            "Send the output to the destination.")
        gtklogger.connect(self.gobutton, "clicked", self.goCB)
        
        self.startpoint = None
        self.endpoint = None

        # Data needed by the "go" button.  Set in "show_data", when
        # the state of all the widgets is examined.
        self.meshobj = None
        self.current_cs_name = None
        
        # Shut off non-GUI toolbox's switchboard callbacks.  We will
        # take them over at activate-time.
        self.toolbox.stop_callbacks()

    def __del__(self):
        switchboard.removeCallback(self.dw_valid_swcb)
        self.dw_valid_swcb = None
            
    def close(self):
        toolboxGUI.GfxToolbox.close(self)

    def activate(self):
        debug.mainthreadTest()
        if not self.active:
            toolboxGUI.GfxToolbox.activate(self)
            self.gfxwindow().setMouseHandler(self)
            self.gfxwindow().setRubberband(rubberband.LineRubberBand())
            self.sb_callbacks = [
                switchboard.requestCallbackMain( (self.gfxwindow(),
                                                  "layers changed"),
                                                 self.newLayers ),
                switchboard.requestCallbackMain( (self.gfxwindow(),
                                                  "new contourmap layer"),
                                                 self.newLayers),
                # Need this signal to update the "current cross section" datum.
                switchboard.requestCallbackMain( "cross sections changed",
                                                 self.show_data),
                switchboard.requestCallbackMain(("rename who", "Mesh"),
                                                self.newLayers)
                ]
            self.show_data()

    def deactivate(self):
        debug.mainthreadTest()
        if self.active:
            toolboxGUI.GfxToolbox.deactivate(self)
            self.gfxwindow().removeMouseHandler()
            self.gfxwindow().setRubberband(rubberband.NoRubberBand())
            for s in self.sb_callbacks:
                switchboard.removeCallback(s)
            self.sb_callbacks = []
        
    def validCB(self, valid):
        self.show_data()

    def csChooserCB(self, gtkmenuitem, csname):
        if csname == noCS:
            self.toolbox.deselectCS()
        else:
            self.toolbox.selectCS(csname)
        self.cs_sample_widget.update(analysissample.SampleSet.registry)
        
    def show_data(self):
        debug.mainthreadTest()
        self.meshobj = self.toolbox.current_mesh
        meshok = self.meshobj is not None
        if meshok:
            text = mesh.meshes.getPath(self.meshobj)
        else:
            text = "No Mesh Displayed!"
        self.meshname.set_text(text)

        csok = 0
        if meshok:
            csname = self.meshobj.selectedCSName()
            csnames = self.meshobj.allCrossSectionNames()
            self.csChooser.update(csnames + [noCS])
            if csname:
                self.csChooser.set_state(csname)
            else:
                self.csChooser.set_state(noCS)
            self.current_cs_name = self.csChooser.get_value()
            csok = self.current_cs_name not in [noCS, None]
        else:
            self.csChooser.update([noCS])
        self.csdeletebutton.set_sensitive(csok)
        self.renamebutton.set_sensitive(csok)
        self.editbutton.set_sensitive(csok)
        self.copybutton.set_sensitive(csok)
                
        self.outputobj = self.toolbox.current_layer
        if self.outputobj is None:
            text =""
        else:
            text = self.outputobj.what.shortrepr()
        self.layername.set_text(text)

        self.gobutton.set_sensitive(self.outputobj is not None
                                    and meshok and csok
                                    and self.destwidget.isValid())
        gtklogger.checkpoint(self.gfxwindow().name + " " +
                             self._name + " sensitized")
        
    def newLayers(self, *args):
        self.toolbox.newLayers()
        self.show_data()

    # Button callback for cross-section deletion -- removes the
    # current cross-section from the current mesh.  
    def csdeleteCB(self, gtkobj):
        meshobj = self.toolbox.current_mesh
        csname = meshobj.selectedCSName()
        menuitem = meshmenu.csmenu.Remove
        menuitem.callWithDefaults(
            mesh=meshobj.path(), name=csname)

    # Callback for the "Rename" button
    def csrenameCB(self, gtkobj):
        meshobj = self.toolbox.current_mesh
        csname = meshobj.selectedCSName()
        menuitem = meshmenu.csmenu.Rename
        newnameparam = menuitem.get_arg('name')
        newnameparam.value = csname
        if parameterwidgets.getParameterValues(
            newnameparam, title="Rename cross section " + csname):
            menuitem.callWithDefaults(mesh=meshobj.path(), cross_section=csname)

    def cseditCB(self, gtkobj):
        meshobj = self.toolbox.current_mesh
        csname = meshobj.selectedCSName()
        menuitem = meshmenu.csmenu.Edit
        csparam = menuitem.get_arg('cross_section')
        csparam.value = meshobj.selectedCS()
        if parameterwidgets.getParameterValues(
            csparam,
            title='Edit cross section ' + csname):
            menuitem.callWithDefaults(mesh=meshobj.path(), name=csname)
            
    def cscopyCB(self, gtkobj):
        meshobj = self.toolbox.current_mesh
        menuitem = meshmenu.csmenu.Copy
        csname = meshobj.selectedCSName()
        targetmeshparam = menuitem.get_arg('mesh')
        targetmeshparam.value = meshobj.path()
        targetnameparam = menuitem.get_arg('name')
        targetnameparam.value = csname
        if parameterwidgets.getParameters(targetmeshparam,
                                          targetnameparam,
                                          title='Copy cross section ' + csname):
            menuitem.callWithDefaults(current=meshobj.path(),
                                      cross_section=csname)
            
    # Actually write an output to the destination.
    def goCB(self, gtkobj):
        menuitem = analyzemenu.ops_menu.Direct_Output
        cs_domain = analysisdomain.CrossSectionDomain(
            self.csChooser.get_value())
        menuitem.callWithDefaults(mesh=mesh.meshes.getPath(self.meshobj),
                                  time=self.meshobj.getCurrentTime(),
                                  data=self.toolbox.current_layer.what,
                                  domain=cs_domain,
                                  sampling=self.cs_sample_widget.get_value(),
                                  destination=self.destwidget.get_value())
        
    # Mouse-handler stuff.
    def acceptEvent(self, event):
        return event=='up' or event=='down'
    def down(self,x,y,shift,ctrl):
        self.startpoint = primitives.Point(x,y)
    def up(self,x,y,shift,ctrl):
        self.endpoint = primitives.Point(x,y)
        self.toolbox.makeCS(self.startpoint, self.endpoint)





def _makeGUI(self):
    return CrossSectionToolboxGUI(self)

meshcstoolbox.CrossSectionToolbox.makeGUI = _makeGUI
