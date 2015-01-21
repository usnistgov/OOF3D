# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.2 $
# $Author: fyc $
# $Date: 2013/07/19 17:38:45 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
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
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Voxel Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:TBScroll:Voxel Selection:Method:Chooser'), 'Color')
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7300000000000e+02,y= 4.5000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7300000000000e+02,y= 4.5000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
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
findWidget('OOF3D').resize(691, 350)
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
assert tests.propertyTreeCheck('Color:green')
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
assert tests.materialPropertyListCheck('Color:green')
assert tests.sensitization4()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2,), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 0), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 0, 1), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1000000000000e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.2167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3334645579118e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 1, 0))
checkpoint Materials page updated
checkpoint property deselected
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3000000000000e+01)
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
checkpoint OOF.Material.Add_property
assert tests.materialPropertyListCheck('Color:green')
assert tests.sensitization5()
# Error occured[AttributeError: ErrNoSuchProperty instance has no attribute 'message']
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
widget_3=findWidget('Error')
handled_1=widget_3.event(event(gtk.gdk.DELETE,window=widget_3.window))
postpone if not handled_1: widget_3.destroy()
findWidget('OOF3D:Materials Page:Pane:Material:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Name for the new material.
findWidget('Dialog-Name for the new material.').resize(280, 67)
findWidget('Dialog-Name for the new material.:new_name:Auto').clicked()
findWidget('Dialog-Name for the new material.:new_name:Text').set_text('c')
findWidget('Dialog-Name for the new material.:new_name:Text').set_text('co')
findWidget('Dialog-Name for the new material.:new_name:Text').set_text('cop')
findWidget('Dialog-Name for the new material.:new_name:Text').set_text('copy')
findWidget('Dialog-Name for the new material.:gtk-ok').clicked()
checkpoint Materials page updated
# Error occured[AttributeError: ErrNoSuchProperty instance has no attribute 'message']
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Copy
assert tests.currentMaterialCheck('copy')
assert tests.materialListCheck('test', 'copy')
#assert tests.currentPropertyCheck('Thermal:Conductivity:Anisotropic:Cubic')
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
widget_4=findWidget('Error')
handled_2=widget_4.event(event(gtk.gdk.DELETE,window=widget_4.window))
postpone if not handled_2: widget_4.destroy()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 8.7657142857143e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 8.4285714285714e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 8.0914285714286e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 7.7542857142857e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 7.4171428571429e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.7428571428571e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.0685714285714e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 5.3942857142857e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 5.0571428571429e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.3828571428571e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.0457142857143e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.7085714285714e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.3714285714286e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.0342857142857e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 2.6971428571429e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 2.3600000000000e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 2.0228571428571e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.6857142857143e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.3485714285714e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.0114285714286e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.7428571428571e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.3714285714286e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 0.0000000000000e+00)
setComboBox(findWidget('OOF3D:Materials Page:Pane:Material:MaterialList'), 'test')
checkpoint Materials page updated
checkpoint Materials page updated
assert tests.currentPropertyCheck('Thermal:Conductivity:Anisotropic:Cubic')
assert tests.materialPropertyListCheck('Color:green', 'Thermal:Conductivity:Anisotropic:Cubic')
assert tests.currentMaterialCheck('test')
findWidget('OOF3D:Materials Page:Pane:Material:PropertyListScroll:PropertyList').get_selection().select_path((0,))
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
findWidget('OOF3D:Materials Page:Pane:Material:PropertyListScroll:PropertyList').get_selection().select_path((1,))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.8000000000000e+01)
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
assert tests.currentPropertyCheck('Thermal:Conductivity:Anisotropic:Cubic')
assert tests.sensitization6()
findWidget('OOF3D:Materials Page:Pane:Material:RemoveProperty').clicked()
checkpoint OOF.Material.Remove_property
assert tests.materialPropertyListCheck('Color:green', 'Thermal:Conductivity:Anisotropic:Cubic')
assert tests.propertyTreeCheck('Thermal:Conductivity:Anisotropic:Cubic')
assert tests.materialPropertyCheck('Thermal:Conductivity:Anisotropic:Cubic')
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
# Error occured[KeyError: 'test']
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
checkpoint OOF.Material.Rename
assert tests.currentMaterialCheck('test')
assert tests.materialPropertyListCheck('Color:green', 'Thermal:Conductivity:Anisotropic:Cubic')
assert tests.currentPropertyCheck('Thermal:Conductivity:Anisotropic:Cubic')
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
widget_5=findWidget('Error')
# Error occured[KeyError: 'test']
handled_3=widget_5.event(event(gtk.gdk.DELETE,window=widget_5.window))
postpone if not handled_3: widget_5.destroy()
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
checkpoint OOF.Material.New
assert tests.currentMaterialCheck('another test')
#assert tests.materialPropertyListCheck()
#assert tests.currentPropertyCheck(None)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.2334645579118e+01)
widget_6=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_6.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_6.window))
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
# Error occured[NameError: Illegal name for menu item: cubic copy]
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
widget_7=findWidget('Error')
handled_4=widget_7.event(event(gtk.gdk.DELETE,window=widget_7.window))
postpone if not handled_4: widget_7.destroy()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3501968368677e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.2466929115824e+02)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.5583661394780e+02)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.8700393673735e+02)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.5583661394780e+02)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.2466929115824e+02)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.5583661394780e+02)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.2466929115824e+02)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3501968368677e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.2466929115824e+02)
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
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.2500000000000e+02)
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D').resize(691, 350)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Voxel Info')
checkpoint Graphics_1 Voxel Info updated
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7200000000000e+02,y= 4.6400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7200000000000e+02,y= 4.6400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
findWidget('OOF3D:Materials Page:Pane:Material:RemoveMaterial').clicked()
checkpoint toplevel widget mapped Dialog-Remove the assigned material from voxels
findWidget('Dialog-Remove the assigned material from voxels').resize(252, 103)
setComboBox(findWidget('Dialog-Remove the assigned material from voxels:pixels'), '<every>')
setComboBox(findWidget('Dialog-Remove the assigned material from voxels:pixels'), 'green')
findWidget('Dialog-Remove the assigned material from voxels:gtk-ok').clicked()
checkpoint OOF.Material.Remove
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9900000000000e+02,y= 4.6800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9900000000000e+02,y= 4.6800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.1700000000000e+02,y= 4.7600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.1700000000000e+02,y= 4.7600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6900000000000e+02,y= 1.9400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6900000000000e+02,y= 1.9400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2700000000000e+02,y= 1.9700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2700000000000e+02,y= 1.9700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5400000000000e+02,y= 4.0900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5400000000000e+02,y= 4.0900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.8400000000000e+02,y= 4.2500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8400000000000e+02,y= 4.2500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7100000000000e+02,y= 4.4600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7100000000000e+02,y= 4.4600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6600000000000e+02,y= 4.3600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6600000000000e+02,y= 4.3600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.8300000000000e+02,y= 2.6200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8300000000000e+02,y= 2.6200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6700000000000e+02,y= 1.8200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6700000000000e+02,y= 1.8200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7100000000000e+02,y= 4.7200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7100000000000e+02,y= 4.7200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.8800000000000e+02,y= 4.8500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8800000000000e+02,y= 4.8500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.4700000000000e+02,y= 2.0800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4700000000000e+02,y= 2.0800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7700000000000e+02,y= 4.6200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7700000000000e+02,y= 4.6200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
findWidget('OOF3D:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material another test to voxels
findWidget('Dialog-Assign material another test to voxels').resize(252, 103)
setComboBox(findWidget('Dialog-Assign material another test to voxels:pixels'), '<every>')
findWidget('Dialog-Assign material another test to voxels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8200000000000e+02,y= 2.0400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8200000000000e+02,y= 2.0400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7800000000000e+02,y= 4.8200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7800000000000e+02,y= 4.8200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
findWidget('OOF3D:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material another test to voxels
findWidget('Dialog-Assign material another test to voxels').resize(252, 103)
setComboBox(findWidget('Dialog-Assign material another test to voxels:pixels'), 'green')
widget_8=findWidget('Dialog-Assign material another test to voxels')
handled_5=widget_8.event(event(gtk.gdk.DELETE,window=widget_8.window))
postpone if not handled_5: widget_8.destroy()
findWidget('OOF3D:Materials Page:Pane:Material:RemoveMaterial').clicked()
checkpoint toplevel widget mapped Dialog-Remove the assigned material from voxels
findWidget('Dialog-Remove the assigned material from voxels').resize(252, 103)
findWidget('Dialog-Remove the assigned material from voxels:gtk-ok').clicked()
checkpoint OOF.Material.Remove
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9900000000000e+02,y= 2.1300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9900000000000e+02,y= 2.1300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5100000000000e+02,y= 4.4300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5100000000000e+02,y= 4.4300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.5800000000000e+02,y= 2.4600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.5800000000000e+02,y= 2.4600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.1100000000000e+02,y= 4.1700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.1100000000000e+02,y= 4.1700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('???')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6700000000000e+02,y= 4.4100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6700000000000e+02,y= 4.4100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
findWidget('OOF3D:Materials Page:Pane:Material:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Material "another test"
findWidget('Dialog-Save Material "another test"').resize(190, 123)
findWidget('Dialog-Save Material "another test":filename').set_text('0')
findWidget('Dialog-Save Material "another test":filename').set_text('00')
findWidget('Dialog-Save Material "another test":filename').set_text('001')
findWidget('Dialog-Save Material "another test":filename').set_text('0010')
findWidget('Dialog-Save Material "another test":filename').set_text('00104')
findWidget('Dialog-Save Material "another test":filename').set_text('001040')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_p')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_pa')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_pag')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_m')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_ma')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_mat')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_mate')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_mater')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_materi')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_materia')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/m')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/ma')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/mat')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/mate')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/mater')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/materi')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/materia')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/material')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/material.')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/material.d')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/material.da')
findWidget('Dialog-Save Material "another test":filename').set_text('0010400_page_material/material.dat')
findWidget('Dialog-Save Material "another test"').resize(198, 123)
findWidget('Dialog-Save Material "another test":gtk-ok').clicked()
checkpoint OOF.File.Save.Materials
#assert tests.filediff('material.dat')#Wierd problem here.
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(284)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Materials')
checkpoint page installed Materials
assert tests.sensitization0()
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(226, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Delete
assert tests.chooserStateCheck('OOF3D:Materials Page:Pane:Material:MaterialList', 'test')
assert tests.propertyTreeCheck('Thermal:Conductivity:Anisotropic:Cubic:cubic_copy')
setComboBox(findWidget('OOF3D:Materials Page:Pane:Material:MaterialList'), 'copy')
checkpoint Materials page updated
checkpoint Materials page updated
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint OOF.Material.Delete
assert tests.chooserCheck('OOF3D:Materials Page:Pane:Material:MaterialList', ['test', 'copy'])
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
setComboBox(findWidget('OOF3D:Materials Page:Pane:Material:MaterialList'), 'test')
checkpoint Materials page updated
checkpoint Materials page updated
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint OOF.Material.Delete
assert tests.sensitization0()
assert tests.chooserCheck('OOF3D:Materials Page:Pane:Material:MaterialList', ['test', 'copy'])
assert tests.checkTBMaterial()
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
widget_9=findWidget('Error')
# Cannot delete materials test and copy
handled_6=widget_9.event(event(gtk.gdk.DELETE,window=widget_9.window))
postpone if not handled_6: widget_9.destroy()
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('0')
findWidget('Dialog-Python_Log:filename').set_text('00')
findWidget('Dialog-Python_Log:filename').set_text('001')
findWidget('Dialog-Python_Log:filename').set_text('0010')
findWidget('Dialog-Python_Log:filename').set_text('00104')
findWidget('Dialog-Python_Log:filename').set_text('001040')
findWidget('Dialog-Python_Log:filename').set_text('0010400')
findWidget('Dialog-Python_Log:filename').set_text('0010400_')
findWidget('Dialog-Python_Log:filename').set_text('0010400_p')
findWidget('Dialog-Python_Log:filename').set_text('0010400_pa')
findWidget('Dialog-Python_Log:filename').set_text('0010400_pag')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_m')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_ma')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_mat')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_mate')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_mater')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_materi')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_materia')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/m')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/ma')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/mat')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/mate')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/mater')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/materi')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/materia')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/material')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/material.')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/material.l')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/material.lo')
findWidget('Dialog-Python_Log:filename').set_text('0010400_page_material/material.log')
findWidget('Dialog-Python_Log').resize(198, 95)
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
#assert tests.filediff('material.log')
widget_10=findWidget('OOF3D')
handled_7=widget_10.event(event(gtk.gdk.DELETE,window=widget_10.window))
postpone if not handled_7: widget_10.destroy()
checkpoint OOF.Graphics_1.File.Close
