# -*- python -*-
# $RCSfile: materialsPage.py,v $
# $Revision: 1.110.2.9 $
# $Author: langer $
# $Date: 2014/11/05 16:54:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import material
from ooflib.common import debug
from ooflib.common import microstructure
from ooflib.common import runtimeflags
from ooflib.common.IO import mainmenu
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gfxLabelTree
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import materialmanager
from ooflib.engine import propertyregistration

AllProperties = propertyregistration.AllProperties

#Interface branch
from ooflib.engine.IO import interfaceparameters

import gtk

import types, string

if config.dimension()==2:
    pixstring = "pixel"
    Pixstring = "Pixel"
elif config.dimension()==3:
    pixstring = "voxel"
    Pixstring = "Voxel"


# Define some convenience variables.
OOF = mainmenu.OOF

class MaterialsPage(oofGUI.MainPage):
    def __init__(self):
        self.built = False
        oofGUI.MainPage.__init__(self, name="Materials", ordering=100,
                                 tip='Define Materials')
        pane = gtk.HPaned()              # Properties on left, Materials on R.
        gtklogger.setWidgetName(pane, 'Pane')
        self.gtk.add(pane)

        self.propertypane = PropertyPane(self)
        self.materialpane = MaterialPane(self)
        pane.pack1(self.propertypane.gtk, resize=0, shrink=0)
        pane.pack2(self.materialpane.gtk, resize=1, shrink=0)
        gtklogger.connect_passive(pane, 'notify::position')

        self.built = True

    def installed(self):
        self.sensitize()

    def currentMaterialName(self):
        return self.materialpane.currentMaterialName()
    def currentMaterial(self):
        return self.materialpane.currentMaterial()

    # Returns a tuple, (name, property-registration-object)
    def current_property(self):
        return self.propertypane.current_property
    
    def current_property_name(self):
        prop = self.current_property()
        if prop and not prop[1].secret():
            return prop[0]
        return None
    
    def sensitize(self):
        self.propertypane.do_sensitize()
        self.materialpane.do_sensitize()
        gtklogger.checkpoint("Materials page updated")
        
class PropertyPane:
    def __init__(self, parent):
        debug.mainthreadTest()
        self.parent = parent
        # Property selection state lives here.  When not None,
        # current_property is a tuple, (name, propertyregistration).
        # current_property mirrors the selection state of the
        # GfxLabelTree self.propertytree.
        self.current_property = None

        self.gtk = gtk.Frame('Property')
        gtklogger.setWidgetName(self.gtk, 'Property')
        self.gtk.set_shadow_type(gtk.SHADOW_IN)
        vbox = gtk.VBox(spacing=3)
        
        self.gtk.add(vbox)

        # Button box above the Property Tree
        buttonbox = gtk.HBox()
        vbox.pack_start(buttonbox, expand=0, fill=0)

        self.copybutton = gtkutils.StockButton(gtk.STOCK_COPY, 'Copy...')
        gtklogger.setWidgetName(self.copybutton, 'Copy')
        gtklogger.connect(self.copybutton, 'clicked', self.on_copy_property)
        tooltips.set_tooltip_text(self.copybutton,
                   'Create a named copy of the currently selected property')
        buttonbox.pack_start(self.copybutton, expand=1, fill=0)

        self.parambutton = gtkutils.StockButton(gtk.STOCK_EDIT,
                                                'Parametrize...')
        gtklogger.setWidgetName(self.parambutton, 'Parametrize')
        gtklogger.connect(self.parambutton, 'clicked', self.parametrize)
        tooltips.set_tooltip_text(self.parambutton,
                     "Set parameters for the currently selected Property.")
        buttonbox.pack_start(self.parambutton, expand=1, fill=0)
        

        self.deletebutton = gtkutils.StockButton(gtk.STOCK_DELETE, 'Delete')
        gtklogger.setWidgetName(self.deletebutton, 'Delete')
        gtklogger.connect(self.deletebutton, 'clicked', self.GUIdelete)
        tooltips.set_tooltip_text(self.deletebutton,
                             "Delete the currently selected Property.")
        buttonbox.pack_start(self.deletebutton, expand=1, fill=0)


        # Scrolling window containing the Property Tree
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "PropertyScroll")
        scroll.set_shadow_type(gtk.SHADOW_IN)
        vbox.pack_start(scroll, expand=1, fill=1)
        scroll.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
        self.propertytree = gfxLabelTree.GfxLabelTree(AllProperties.data,
                                                      expand=None,
                                                      callback=self.proptreeCB,
                                                      name="PropertyTree")
        self.propertytree.setRightClickCB(self.parametrize)
        scroll.add(self.propertytree.gtk)



        # The Load button.
        self.loadbutton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD,
                                               "Add Property to Material",
                                               reverse=True)
        gtklogger.setWidgetName(self.loadbutton, 'Add')
        align = gtk.Alignment(xalign=0.5)
        align.add(self.loadbutton)
        vbox.pack_start(align, expand=0, fill=0, padding=3)
        tooltips.set_tooltip_text(self.loadbutton,
            "Load the currently selected property into the current material.")
        gtklogger.connect(self.loadbutton, 'clicked',self.on_prop_load)

        # Utility callbacks.
        self.propertytree.gtk.connect("destroy", self.on_destroy)

        switchboard.requestCallbackMain("new property", self.newPropCB)

    def sensitize(self, *args):
        self.parent.sensitize()
    def do_sensitize(self):
        debug.mainthreadTest()
        sensitivity = self.current_property is not None
        deletable = sensitivity and hasattr(self.current_property[1], "parent")
        
        self.copybutton.set_sensitive(sensitivity)
        self.parambutton.set_sensitive(sensitivity)
        self.deletebutton.set_sensitive(deletable)

        matselected = self.parent.currentMaterialName() is not None

        #Interface branch
        currentmat=self.parent.currentMaterial()
        
        if runtimeflags.surface_mode:
            isInterfaceMat=(currentmat is not None and
                            currentmat.type()==material.MATERIALTYPE_INTERFACE)
        else:
            isInterfaceMat=False
            
        isInterfaceProp=(sensitivity and 
                         self.current_property[1].interfaceCompatibility() != 
                         interfaceparameters.COMPATIBILITY_BULK_ONLY)
        isBulkMat=(currentmat is not None and 
                   currentmat.type()==material.MATERIALTYPE_BULK)
        isBulkProp= (sensitivity and 
                     self.current_property[1].interfaceCompatibility() !=
                     interfaceparameters.COMPATIBILITY_INTERFACE_ONLY)
        #Check if the currently selected property node and the current
        #material are compatible
        matpropcompatible=(isBulkMat and isBulkProp) or (isInterfaceMat and isInterfaceProp)
        self.loadbutton.set_sensitive(sensitivity and matselected and \
                                      matpropcompatible)

        if sensitivity:
            mainmenu.OOF.File.Save.Property.enable()
        else:
            mainmenu.OOF.File.Save.Property.disable()
        

    # Although the load button is in the Property pane, loading is
    # a material-menu operation.
    def on_prop_load(self,button):      # gtk callback
        propname = self.current_property[0]
        mat = self.parent.currentMaterial()
        OOF.Material.Add_property(name=mat.name(), property=propname)
        self.parent.materialpane.select_property(propname)

    #######################################################################
    #
    
    # Master property selection and deselection routines, called
    # in response to both materialsPane and propertyPane selection events.

    def select_property(self, name):
        debug.mainthreadTest()
        treenode = AllProperties.data[name]
        self.propertytree.blockSignals()
        if treenode.object is not None and not treenode.object.secret():
            self.propertytree.expandToPath(name)
            self.propertytree.selectObject(treenode.object)
            self.current_property = (name, treenode.object)
        else:
            self.propertytree.deselect()
            self.current_property = None
        self.propertytree.unblockSignals()
        self.sensitize()
        gtklogger.checkpoint("property selected")
        
    def deselect_property(self, name):
        debug.mainthreadTest()
        if self.current_property: # and self.propertytree:
            if self.current_property[0]==name:
                self.propertytree.blockSignals()
                self.propertytree.deselect()
                self.propertytree.unblockSignals()
                self.current_property = None
                self.sensitize()
            else:
                print "Inconsistent selection state."
            gtklogger.checkpoint("property deselected")
        

    def proptreeCB(self, signal, treenode): # GfxLabelTree callback
        prop_name = treenode.path()
        if signal == "select":
            self.select_property(prop_name)
            self.parent.materialpane.select_property(prop_name)
        elif signal == "deselect":
            self.deselect_property(prop_name)
            self.parent.materialpane.deselect_property(prop_name)
        elif signal == "doubleclick":
            self.select_property(prop_name)
            self.parametrize()
        
            
    def newPropCB(self, propertyregistration): # switchboard 'new property'
        propname = propertyregistration.name()
        self.select_property(propname)
        self.parent.materialpane.select_property(propname)

    ####################################################################
    
    # Callback for the parametrize button, brings up a dialog box to
    # fill in the parameters of the currently-selected property.
    def parametrize(self, gtkobj=None):
        if self.current_property:
            reg = self.current_property[1]
            if reg is not None:
                # Get the associated LabelTree node.
                ltn = AllProperties.data.reverse_dict[reg]
                menuitem = ltn.menus[AllProperties.parametrizekey]
                # Copy parameters out of the PropertyRegistration, not
                # the menu item. 
                params = [p for p in reg.params if p.name != 'name']
                if parameterwidgets.getParameters(
                    title='Parametrize '+self.current_property[0],
                    *params):
                    menuitem.callParamList(params)
            else:                       # should never happen
                reporter.report("Property is not parametrizable.")
        else:                           # should never happen
            reporter.report("No property selected.")
            
    def on_destroy(self,gtk):
        self.gtktree = None
        
    def on_copy_property(self, button): # gtk callback
        menuitem = OOF.Property.Copy
        newnameparam = menuitem.get_arg('new_name')
        if parameterwidgets.getParameters(
            newnameparam,
            title='Copy property ' + self.current_property[0]):
            if newnameparam.nontrivial():
                menuitem.callWithDefaults(property=self.current_property[0])

    def GUIdelete(self, gtk):
        if reporter.query("Delete property %s?" % self.current_property[0],
                          "OK", "Cancel", default="OK") == "OK":
            OOF.Property.Delete(property=self.current_property[0])

########################################################################
########################################################################

class MaterialPane:
    def __init__(self, parent):
        debug.mainthreadTest()
        self.parent = parent

        self.gtk = gtk.Frame('Material')
        gtklogger.setWidgetName(self.gtk, 'Material')
        self.gtk.set_shadow_type(gtk.SHADOW_IN)
        vbox = gtk.VBox()
        self.gtk.add(vbox)

        buttonbox = gtk.HBox()
        vbox.pack_start(buttonbox, expand=0, fill=0)

        self.newmaterial = gtkutils.StockButton(gtk.STOCK_NEW, 'New...')
        gtklogger.setWidgetName(self.newmaterial, 'New')
        buttonbox.pack_start(self.newmaterial, expand=1, fill=0)
        tooltips.set_tooltip_text(self.newmaterial,'Create a new Material.')
        gtklogger.connect(self.newmaterial, "clicked",self.on_newmaterial)

        self.renamematerial = gtkutils.StockButton(gtk.STOCK_EDIT,
                                                   'Rename...')
        gtklogger.setWidgetName(self.renamematerial,'Rename')
        buttonbox.pack_start(self.renamematerial, expand=1, fill=0)
        tooltips.set_tooltip_text(self.renamematerial,
                             'Rename this material.')
        gtklogger.connect(self.renamematerial, "clicked", self.on_rename)
        
        self.copymaterial = gtkutils.StockButton(gtk.STOCK_COPY, 'Copy...')
        gtklogger.setWidgetName(self.copymaterial, 'Copy')
        buttonbox.pack_start(self.copymaterial, expand=1, fill=0)
        tooltips.set_tooltip_text(self.copymaterial,
                             'Create a copy of this material.')
        gtklogger.connect(self.copymaterial, "clicked", self.on_copy)

        self.deletebutton = gtkutils.StockButton(gtk.STOCK_DELETE, 'Delete')
        gtklogger.setWidgetName(self.deletebutton, 'Delete')
        buttonbox.pack_start(self.deletebutton, expand=1, fill=0)
        tooltips.set_tooltip_text(self.deletebutton,'Delete this material.')
        gtklogger.connect(self.deletebutton, "clicked", self.on_delete)

        self.savebutton = gtkutils.StockButton(gtk.STOCK_SAVE, 'Save...')
        gtklogger.setWidgetName(self.savebutton, 'Save')
        buttonbox.pack_start(self.savebutton, expand=1, fill=0)
        tooltips.set_tooltip_text(self.savebutton,'Save this material in a file.')
        gtklogger.connect(self.savebutton, 'clicked', self.on_save)

        self.materialName = chooser.ChooserWidget(
            materialmanager.getMaterialNames(),
            callback=self.newMatSelection,
            update_callback=self.newMatSelection,
            name="MaterialList")
        self.materialName.gtk.set_border_width(3)

        vbox.pack_start(self.materialName.gtk, expand=0, fill=0)
        tooltips.set_tooltip_text(self.materialName.gtk,
                             'Choose a Material to edit.')

        # The list of Properties belonging to a Material
        self.matproplist = chooser.ScrolledChooserListWidget(
            callback=self.matproplistCB, autoselect=False, name="PropertyList")
        self.matproplist.gtk.set_border_width(3)
        vbox.pack_start(self.matproplist.gtk, expand=1, fill=1)

        self.removebutton = gtk.Button('Remove Property from Material')
        gtklogger.setWidgetName(self.removebutton, "RemoveProperty")
        self.removebutton.set_border_width(3)
        vbox.pack_start(self.removebutton, expand=0, fill=0, padding=3)
        tooltips.set_tooltip_text(self.removebutton,
               'Remove the currently selected property from this material.')
        gtklogger.connect(self.removebutton, "clicked", self.on_remove)

        # Assignment of materials to pixels and removal of materials
        # from pixels may belong in a separate GUI page.  For now,
        # it's done via the dialog boxes raised by the buttons defined
        # here.
        assignframe = gtk.Frame()
        assignframe.set_shadow_type(gtk.SHADOW_IN)
        assignframe.set_border_width(3)
        vbox.pack_start(assignframe, expand=0, fill=0)

        # NB surface-mode flag is operative here.

        if runtimeflags.surface_mode:
            inner2vbox_pair=gtk.VBox()
        align = gtk.Alignment(xalign=0.5)
        inner2hbox_both=gtk.HBox()
        inner2vbox = gtk.VBox()
        if runtimeflags.surface_mode:
            assignframe.add(inner2hbox_both)
        else:
            assignframe.add(align) 
            align.add(inner2hbox_both) 
        inner2hbox_both.pack_start(inner2vbox)
        if runtimeflags.surface_mode:
            inner2hbox_both.pack_start(inner2vbox_pair) 
        
        # Assign materials to pixels
        self.assignbutton = gtk.Button('Assign Material to %ss...'%Pixstring)
        gtklogger.setWidgetName(self.assignbutton, "Assign")
        self.assignbutton.set_border_width(3)
        inner2vbox.pack_start(self.assignbutton, expand=0, fill=0)
        tooltips.set_tooltip_text(self.assignbutton,
                             'Assign the currently selected Material to %ss in a Microstructure.'%pixstring)
        gtklogger.connect(self.assignbutton, 'clicked', self.on_assignment)
        
        # Remove materials from pixels
        self.removematbutton = gtk.Button('Remove Materials from %ss...'%Pixstring)
        gtklogger.setWidgetName(self.removematbutton, "RemoveMaterial")
        self.removematbutton.set_border_width(3)
        inner2vbox.pack_start(self.removematbutton, expand=0, fill=0)
        tooltips.set_tooltip_text(self.removematbutton,
                             'Remove all Materials from %ss in a Microstructure.'%pixstring)
        gtklogger.connect(self.removematbutton, 'clicked',
                          self.on_MS_remove_material)


        if runtimeflags.surface_mode:

            self.assigninterfacebutton = gtk.Button('Assign to interface...')
            gtklogger.setWidgetName(self.assigninterfacebutton,
                                    "AssignInterface")
            self.assigninterfacebutton.set_border_width(3)
            inner2vbox_pair.pack_start(self.assigninterfacebutton,
                                       expand=0, fill=0)
            tooltips.set_tooltip_text(self.assigninterfacebutton,
                                      'Assign the currently selected Material to an interface in a Microstructure.')
            gtklogger.connect(self.assigninterfacebutton, 'clicked', self.on_interface_assign)
        
            # Remove material from interface
            self.removeinterfacebutton = gtk.Button('Remove from interface...')
            gtklogger.setWidgetName(self.removeinterfacebutton,
                                    "RemoveInterface")
            self.removeinterfacebutton.set_border_width(3)
            inner2vbox_pair.pack_start(self.removeinterfacebutton, expand=0, fill=0)
            tooltips.set_tooltip_text(self.removeinterfacebutton,
                                      'Remove Material from an interface in a Microstructure.')
            gtklogger.connect(self.removeinterfacebutton, 'clicked',
                              self.on_interface_remove)
        
        # End of surface-mode block.


        self.updatePropList()
        self.gtk.show_all()

        # Switchboard callbacks.
        switchboard.requestCallbackMain("new_material",self.new_mat)
        switchboard.requestCallbackMain("remove_material",self.del_mat)
        switchboard.requestCallbackMain("prop_added_to_material",
                                        self.prop_added)
        switchboard.requestCallbackMain("prop_removed_from_material",
                                        self.prop_removed)
        switchboard.requestCallbackMain(('new who', 'Microstructure'),
                                        self.sensitize)
        switchboard.requestCallbackMain(('remove who', 'Microstructure'),
                                        self.sensitize)

    def currentMaterialName(self):
        return self.materialName.get_value()
    def currentMaterial(self):
        name = self.currentMaterialName()
        if name:
            return materialmanager.getMaterial(name)
    def currentPropertyName(self):
        return self.matproplist.get_value()
    def currentProperty(self):
        name = self.currentPropertyName()
        if name:
            return AllProperties[name]

    def updatePropList(self):
        matl = self.currentMaterial()
        if matl is not None:
            props = matl.properties()
            self.matproplist.update([prop.name() for prop in props 
                                     if not prop.registration().secret()])
            self.matproplist.set_selection(self.parent.current_property_name())
        else:
            self.matproplist.update([])

    def select_property(self, propname):
        debug.mainthreadTest()
        self.matproplist.suppress_signals()
        self.matproplist.set_selection(propname)
        self.matproplist.allow_signals()

    def deselect_property(self, propname):
        debug.mainthreadTest()
        self.matproplist.suppress_signals()
        self.matproplist.set_selection(None)
        self.matproplist.allow_signals()

    #########

    def on_newmaterial(self, button):   # gtk callback
        menuitem = OOF.Material.New
        if parameterwidgets.getParameters(title='New material',
                                          *menuitem.params):
            if menuitem.get_arg('name').nontrivial():
                menuitem.callWithDefaults()

    def on_delete(self, button):        # gtk callback
        name = self.currentMaterialName()
        if name is not None:
            if reporter.query("Delete material %s?" % name,
                              'OK', 'Cancel', default='OK') == 'OK':
                OOF.Material.Delete(name=name)
            
    def new_mat(self, name):            # switchboard "new_material"
        names = materialmanager.getMaterialNames()
        self.materialName.update(names)
        self.materialName.set_state(name)
        self.updatePropList()
        self.sensitize()

    def del_mat(self, material):        # switchboard "remove_material"
        self.materialName.update(materialmanager.getMaterialNames())
        self.updatePropList()
        self.sensitize()

    def on_rename(self, button):     # gtk callback
        oldname = self.currentMaterialName()
        if oldname is not None:
            menuitem = OOF.Material.Rename
            newnameparam = menuitem.get_arg("name")
            if parameterwidgets.getParameters(
                newnameparam, title="New name for the material."):
                if newnameparam.nontrivial():
                    menuitem.callWithDefaults(material=oldname)
            

    def on_copy(self, button):          # gtk callback
        oldname = self.currentMaterialName()
        if oldname is not None:
            menuitem = OOF.Material.Copy
            newnameparam = menuitem.get_arg('new_name')
            if parameterwidgets.getParameters(
                newnameparam, title="Name for the new material."):
                if newnameparam.nontrivial():
                    menuitem.callWithDefaults(name=oldname)

    def on_remove(self, button):        # gtk callback
        name = self.currentMaterialName()
        if name is not None:
            propname = self.currentPropertyName()
            if propname is not None:
                OOF.Material.Remove_property(name=name, property=propname)

    def on_assignment(self, button):    # gtk callback
        menuitem = OOF.Material.Assign
        params = filter(lambda x: x.name != 'material', menuitem.params)
        materialname = self.currentMaterialName()
        if parameterwidgets.getParameters(
            title="Assign material %s to %ss" % (materialname,pixstring), *params):
            menuitem.callWithDefaults(material=materialname)

    def on_MS_remove_material(self, button): # gtk callback
        menuitem = OOF.Material.Remove
        if parameterwidgets.getParameters(
            title='Remove the assigned material from %ss'%pixstring, *menuitem.params):
            menuitem.callWithDefaults()

    #Interface branch
    def on_interface_assign(self, button):
        menuitem=OOF.Material.Interface.Assign
        params = filter(lambda x: x.name != 'material', menuitem.params)
        materialname = self.currentMaterialName()
        if parameterwidgets.getParameters(
            title="Assign material %s to an interface" % materialname, *params):
            menuitem.callWithDefaults(material=materialname)
    def on_interface_remove(self, button):
        menuitem = OOF.Material.Interface.Remove
        if parameterwidgets.getParameters(
            title='Remove the assigned material from interface', *menuitem.params):
            menuitem.callWithDefaults()

    def on_save(self, button):          # gtk callback
        # Save a single material
        menuitem = OOF.File.Save.Materials
        materialname = self.currentMaterialName()
        params = filter(lambda x: x.name != "materials", menuitem.params)
        if parameterwidgets.getParameters(
            title='Save Material "%s"' % materialname,
            ident='SaveMat',
            *params):
            menuitem.callWithDefaults(materials=[materialname])
        
    #########

    # switchboard "prop_added_to_material".
    def prop_added(self, material, property):
        if self.currentMaterialName() == material:
            self.updatePropList()
            self.select_property(property)
            self.parent.propertypane.select_property(property)
        self.sensitize()

    # switchboard "prop_removed_from_material"
    def prop_removed(self, material, name, property):
        if self.currentMaterialName() == material.name:
            self.updatePropList()
            self.sensitize()

    def sensitize(self, *args):
        self.parent.sensitize()
    def do_sensitize(self, *args):
        debug.mainthreadTest()
        mat_selected = self.currentMaterialName() is not None
        self.renamematerial.set_sensitive(mat_selected)
        self.copymaterial.set_sensitive(mat_selected)
        self.deletebutton.set_sensitive(mat_selected)
        self.savebutton.set_sensitive(mat_selected)

        nmicros = microstructure.microStructures.nActual()
        self.assignbutton.set_sensitive(
            mat_selected and nmicros > 0 and
            self.currentMaterial().type()==
            material.MATERIALTYPE_BULK)
        self.removematbutton.set_sensitive(nmicros > 0)

        self.removebutton.set_sensitive(
            self.currentPropertyName() is not None)

        #Interface branch
        if runtimeflags.surface_mode:
            self.assigninterfacebutton.set_sensitive(
                mat_selected and
                nmicros > 0 and
                self.currentMaterial().type()==
                material.MATERIALTYPE_INTERFACE)
            self.removeinterfacebutton.set_sensitive(nmicros > 0)

    ##############

    # Callback for the material chooser
    def newMatSelection(self, gtkobj, name):
        self.updatePropList()
        self.sensitize()

    # Callback for the property list
    def matproplistCB(self, prop, interactive):
        if self.parent.built:
            if interactive:
                propname = self.currentPropertyName()
                self.parent.propertypane.select_property(propname)
            self.sensitize()
        


        
# Create the page
materialspage = MaterialsPage()

#####################################

# GUI callbacks for the save-property menu item in the main FILE menu.

# Save the current property, if selected, etc.
def _save_prop(menuitem):
    global materialspage
    propname = materialspage.current_property_name()
    if propname:
        params = filter(lambda x: x.name!="property", menuitem.params)
        if parameterwidgets.getParameters(ident='PropMenu',
                                          title='Save Property',
                                          *params):
            menuitem.callWithDefaults(property=propname)
    else:
        reporter.report("No property selected for saving.")

mainmenu.OOF.File.Save.Property.add_gui_callback(_save_prop)
