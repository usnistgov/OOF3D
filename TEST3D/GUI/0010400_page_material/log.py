# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.6 $
# $Author: fyc $
# $Date: 2014/09/19 22:52:12 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D Messages 1').resize(540, 200)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(401, 215)
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('TEST_DATA/5color')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(603, 200)
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint meshable button set
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint microstructure page sensitized
checkpoint OOF.Microstructure.Create_From_ImageFile
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:name:Auto').clicked()
findWidget('Dialog-Create new voxel group:name:Text').set_text('g')
findWidget('Dialog-Create new voxel group:name:Text').set_text('gr')
findWidget('Dialog-Create new voxel group:name:Text').set_text('gre')
findWidget('Dialog-Create new voxel group:name:Text').set_text('gree')
findWidget('Dialog-Create new voxel group:name:Text').set_text('green')
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New
checkpoint microstructure page sensitized
checkpoint meshable button set
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Voxel Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Method:Chooser'), 'Color')
findWidget('OOF3D Graphics 1').resize(1000, 800)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.4800000000000e+02,y= 4.2900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4800000000000e+02,y= 4.2900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Color
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection
widget_0=findWidget('OOF3D Graphics 1')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
checkpoint OOF.Graphics_1.File.Close
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Materials')
assert tests.sensitization2()
checkpoint page installed Materials
findWidget('OOF3D').resize(691, 350)
findWidget('OOF3D:Materials Page:Pane').set_position(278)
findWidget('OOF3D:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(300, 95)
findWidget('Dialog-New material:name:Auto').clicked()
findWidget('Dialog-New material:name:Text').set_text('t')
findWidget('Dialog-New material:name:Text').set_text('te')
findWidget('Dialog-New material:name:Text').set_text('tes')
findWidget('Dialog-New material:name:Text').set_text('test')
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.New
findWidget('OOF3D').resize(691, 350)
assert tests.sensitization3()
assert tests.materialListCheck('test')
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
checkpoint Materials page updated
checkpoint property selected
widget_1=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_1.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_1.window))
findWidget('OOF3D:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Color
findWidget('Dialog-Copy property Color').resize(280, 67)
findWidget('Dialog-Copy property Color:new_name:Auto').clicked()
findWidget('Dialog-Copy property Color:new_name:Text').set_text('g')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('gr')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('gre')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('gree')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('green')
findWidget('Dialog-Copy property Color:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((0,), open_all=False)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF3D').resize(691, 350)
assert tests.propertyTreeCheck('Color:green')
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF3D').resize(691, 350)
assert tests.materialPropertyListCheck('Color:green')
assert tests.sensitization4()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2,), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 0), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.2334645579118e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3501968368677e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 0, 1), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3000000000000e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 1, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_2=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_2.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_2.window))
findWidget('OOF3D:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic
findWidget('Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic').resize(241, 129)
findWidget('Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic:kappa:0,0').set_text('')
findWidget('Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic:kappa:0,0').set_text('1')
findWidget('Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic:kappa:0,0').set_text('12')
findWidget('Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic:kappa:0,0').set_text('123')
findWidget('Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Thermal.Conductivity.Anisotropic.Cubic
findWidget('OOF3D Messages 1').resize(653, 200)
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
assert tests.materialPropertyListCheck('Color:green', 'Thermal:Conductivity:Anisotropic:Cubic')
assert tests.sensitization5()
findWidget('OOF3D:Materials Page:Pane:Material:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Name for the new material.
findWidget('Dialog-Name for the new material.').resize(280, 67)
findWidget('Dialog-Name for the new material.:new_name:Auto').clicked()
findWidget('Dialog-Name for the new material.:new_name:Text').set_text('c')
findWidget('Dialog-Name for the new material.:new_name:Text').set_text('co')
findWidget('Dialog-Name for the new material.:new_name:Text').set_text('cop')
findWidget('Dialog-Name for the new material.:new_name:Text').set_text('copy')
findWidget('Dialog-Name for the new material.').resize(280, 67)
findWidget('Dialog-Name for the new material.:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Copy
assert tests.currentMaterialCheck('copy')
assert tests.materialListCheck('test', 'copy')
setComboBox(findWidget('OOF3D:Materials Page:Pane:Material:MaterialList'), 'test')
checkpoint Materials page updated
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.1832677210441e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.0665354420882e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_3=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_3.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_3.window))
assert tests.materialPropertyListCheck('Color:green', 'Thermal:Conductivity:Anisotropic:Cubic')
assert tests.currentMaterialCheck('test')
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_4=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_4.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_4.window))
widget_5=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_5.event(event(gtk.gdk.BUTTON_RELEASE,button=3,window=widget_5.window))
checkpoint toplevel widget mapped Dialog-Parametrize Color;green
findWidget('Dialog-Parametrize Color;green').resize(256, 137)
widget_6=findWidget('Dialog-Parametrize Color;green')
handled_1=widget_6.event(event(gtk.gdk.DELETE,window=widget_6.window))
postpone if not handled_1: widget_6.destroy()
assert tests.currentMaterialPropertyCheck('Color:green')
assert tests.sensitization0()
findWidget('OOF3D:Materials Page:Pane:Property:Delete').clicked()
assert tests.materialPropertyListCheck('Color:green', 'Thermal:Conductivity:Anisotropic:Cubic')
assert tests.propertyTreeCheck('Color:green')
assert tests.materialPropertyCheck('Color:green')
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(222, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().unselect_all()
checkpoint Materials page updated
checkpoint property deselected
checkpoint OOF.Property.Delete
findWidget('OOF3D:Materials Page:Pane:Material:Rename').clicked()
checkpoint toplevel widget mapped Dialog-New name for the material.
findWidget('Dialog-New name for the material.').resize(246, 67)
findWidget('Dialog-New name for the material.:name:Auto').clicked()
findWidget('Dialog-New name for the material.:name:Text').set_text('m')
findWidget('Dialog-New name for the material.:name:Text').set_text('ma')
findWidget('Dialog-New name for the material.:name:Text').set_text('mat')
findWidget('Dialog-New name for the material.:name:Text').set_text('mate')
findWidget('Dialog-New name for the material.:name:Text').set_text('mater')
findWidget('Dialog-New name for the material.:name:Text').set_text('materi')
findWidget('Dialog-New name for the material.:name:Text').set_text('materia')
findWidget('Dialog-New name for the material.:name:Text').set_text('material')
findWidget('Dialog-New name for the material.:name:Text').set_text('material ')
findWidget('Dialog-New name for the material.:name:Text').set_text('material t')
findWidget('Dialog-New name for the material.:name:Text').set_text('material te')
findWidget('Dialog-New name for the material.:name:Text').set_text('material tes')
findWidget('Dialog-New name for the material.:name:Text').set_text('material test')
findWidget('Dialog-New name for the material.:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Rename
assert tests.currentMaterialCheck('material test')
assert tests.materialPropertyListCheck('Thermal:Conductivity:Anisotropic:Cubic')
findWidget('OOF3D:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(300, 95)
findWidget('Dialog-New material:name:Text').set_text('atest')
findWidget('Dialog-New material:name:Text').set_text('antest')
findWidget('Dialog-New material:name:Text').set_text('anotest')
findWidget('Dialog-New material:name:Text').set_text('anottest')
findWidget('Dialog-New material:name:Text').set_text('anothtest')
findWidget('Dialog-New material:name:Text').set_text('anothetest')
findWidget('Dialog-New material:name:Text').set_text('anothertest')
findWidget('Dialog-New material:name:Text').set_text('another test')
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.New
assert tests.currentMaterialCheck('another test')
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 1, 0))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1000000000000e+01)
checkpoint Materials page updated
checkpoint property selected
widget_7=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_7.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_7.window))
assert tests.propertyTreeCheck('Thermal:Conductivity:Anisotropic:Cubic')
findWidget('OOF3D:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic').resize(280, 67)
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('c')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cu')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cub')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubi')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubic')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubic ')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubic c')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubic co')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubic cop')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubic copy')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:gtk-ok').clicked()
checkpoint OOF.Property.Copy
assert tests.propertyTreeCheck('Thermal:Conductivity:Anisotropic:Cubic')
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(653, 200)
findWidget('OOF3D:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic').resize(280, 67)
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubiccopy')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubic_copy')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 0, 1, 0), open_all=False)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Voxel Info')
checkpoint Graphics_1 Voxel Info updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3400000000000e+02,y= 4.1800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3400000000000e+02,y= 4.1800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
findWidget('OOF3D:Materials Page:Pane:Material:RemoveMaterial').clicked()
checkpoint toplevel widget mapped Dialog-Remove the assigned material from voxels
findWidget('Dialog-Remove the assigned material from voxels').resize(252, 103)
setComboBox(findWidget('Dialog-Remove the assigned material from voxels:pixels'), 'green')
findWidget('Dialog-Remove the assigned material from voxels:gtk-ok').clicked()
checkpoint OOF.Material.Remove
assert tests.checkTBMaterial()
findWidget('OOF3D').resize(691, 350)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.4000000000000e+02,y= 4.0100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4000000000000e+02,y= 4.0100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3500000000000e+02,y= 2.5100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3500000000000e+02,y= 2.5100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3900000000000e+02,y= 4.4300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3900000000000e+02,y= 4.4300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
findWidget('OOF3D:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material another test to voxels
findWidget('Dialog-Assign material another test to voxels').resize(252, 103)
setComboBox(findWidget('Dialog-Assign material another test to voxels:pixels'), '<every>')
findWidget('Dialog-Assign material another test to voxels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.5400000000000e+02,y= 4.6800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.5400000000000e+02,y= 4.6800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3400000000000e+02,y= 1.8900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3400000000000e+02,y= 1.8900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3400000000000e+02,y= 2.5200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3400000000000e+02,y= 2.5200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3800000000000e+02,y= 5.3200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3800000000000e+02,y= 5.3200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.5000000000000e+02,y= 5.0000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.5000000000000e+02,y= 5.0000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.4700000000000e+02,y= 2.1000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4700000000000e+02,y= 2.1000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.5700000000000e+02,y= 4.3200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.5700000000000e+02,y= 4.3200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
findWidget('OOF3D:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material another test to voxels
findWidget('Dialog-Assign material another test to voxels').resize(252, 103)
setComboBox(findWidget('Dialog-Assign material another test to voxels:pixels'), 'green')
findWidget('Dialog-Assign material another test to voxels:gtk-cancel').clicked()
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(226, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Delete
assert tests.checkTBMaterial()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3300000000000e+02,y= 4.1100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3300000000000e+02,y= 4.1100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3600000000000e+02,y= 1.9500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3600000000000e+02,y= 1.9500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5800000000000e+02,y= 1.9100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5800000000000e+02,y= 1.9100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9100000000000e+02,y= 4.9700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9100000000000e+02,y= 4.9700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.4600000000000e+02,y= 4.8500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4600000000000e+02,y= 4.8500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
findWidget('OOF3D:Materials Page:Pane:Material:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Material "material test"
findWidget('Dialog-Save Material "material test"').resize(190, 123)
findWidget('Dialog-Save Material "material test":filename').set_text('m')
findWidget('Dialog-Save Material "material test":filename').set_text('ma')
findWidget('Dialog-Save Material "material test":filename').set_text('mat')
findWidget('Dialog-Save Material "material test":filename').set_text('mate')
findWidget('Dialog-Save Material "material test":filename').set_text('mater')
findWidget('Dialog-Save Material "material test":filename').set_text('materi')
findWidget('Dialog-Save Material "material test":filename').set_text('materia')
findWidget('Dialog-Save Material "material test":filename').set_text('material')
findWidget('Dialog-Save Material "material test":filename').set_text('material.')
findWidget('Dialog-Save Material "material test":filename').set_text('material.d')
findWidget('Dialog-Save Material "material test":filename').set_text('material.da')
findWidget('Dialog-Save Material "material test":filename').set_text('material.dat')
findWidget('Dialog-Save Material "material test"').resize(198, 123)
findWidget('Dialog-Save Material "material test":gtk-ok').clicked()
checkpoint OOF.File.Save.Materials
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(284)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Materials')
checkpoint page installed Materials
assert tests.sensitization0()
assert tests.chooserCheck('OOF3D:Materials Page:Pane:Material:MaterialList', ['material test', 'copy'])
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(231, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Delete
assert tests.sensitization0()
assert tests.chooserCheck('OOF3D:Materials Page:Pane:Material:MaterialList', ['copy'])
assert tests.checkTBMaterial()
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Delete
assert tests.sensitization1()
assert tests.chooserCheck('OOF3D:Materials Page:Pane:Material:MaterialList', [])
assert tests.checkTBMaterial()
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('m')
findWidget('Dialog-Python_Log:filename').set_text('ma')
findWidget('Dialog-Python_Log:filename').set_text('mat')
findWidget('Dialog-Python_Log:filename').set_text('mate')
findWidget('Dialog-Python_Log:filename').set_text('mater')
findWidget('Dialog-Python_Log:filename').set_text('materi')
findWidget('Dialog-Python_Log:filename').set_text('materia')
findWidget('Dialog-Python_Log:filename').set_text('material')
findWidget('Dialog-Python_Log:filename').set_text('material.')
findWidget('Dialog-Python_Log:filename').set_text('material.l')
findWidget('Dialog-Python_Log:filename').set_text('material.lo')
findWidget('Dialog-Python_Log:filename').set_text('material.log')
findWidget('Dialog-Python_Log').resize(198, 95)
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('material.log')
widget_8=findWidget('OOF3D')
handled_2=widget_8.event(event(gtk.gdk.DELETE,window=widget_8.window))
postpone if not handled_2: widget_8.destroy()
checkpoint OOF.Graphics_1.File.Close