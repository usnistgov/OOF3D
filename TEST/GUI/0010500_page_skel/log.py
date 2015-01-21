# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.2 $
# $Author: fyc $
# $Date: 2013/07/19 20:54:42 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D:Navigation:Next').clicked()
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
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.8500000000000e+02,y= 4.6600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8500000000000e+02,y= 4.6600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
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
findWidget('OOF3D:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Color;green
findWidget('Dialog-Parametrize Color;green').resize(256, 137)
findWidget('Dialog-Parametrize Color;green:color:Gray:Gray:entry').set_text('4.1269841269841e-01')
widget_2=findWidget('Dialog-Parametrize Color;green:color:Gray:Gray:entry')
widget_2.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_2.window))
findWidget('Dialog-Parametrize Color;green:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Color.green
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
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.2334645579118e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3501968368677e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 0, 1), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3000000000000e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 1, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_3=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_3.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_3.window))
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
findWidget('OOF3D:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic').resize(280, 67)
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('c')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('co')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cop')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('copy')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 0, 1, 0), open_all=False)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.1832677210441e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.0665354420882e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 0.0000000000000e+00)
widget_4=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_4.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_4.window))
widget_5=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_5.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_5.window))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.5327102803738e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 7.0654205607477e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.0598130841121e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.4130841121495e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.7663551401869e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 2.1196261682243e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 2.4728971962617e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 2.8261682242991e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1794392523364e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.5327102803738e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.8859813084112e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.2392523364486e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.5925233644860e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.9457943925234e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 5.2990654205607e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 5.6523364485981e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.0056074766355e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.3588785046729e+01)
widget_6=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_6.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_6.window))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 1, 1))
checkpoint Materials page updated
checkpoint property deselected
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.6000000000000e+01)
checkpoint Materials page updated
checkpoint property selected
widget_7=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_7.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_7.window))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.4832677210441e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.6653544208820e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_8=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_8.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_8.window))
assert tests.currentPropertyCheck('Color:green')
findWidget('OOF3D:Materials Page:Pane:Property:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(222, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().unselect_all()
checkpoint Materials page updated
checkpoint property deselected
checkpoint OOF.Property.Delete
assert tests.currentPropertyCheck(None)
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
assert tests.currentPropertyCheck(None)
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
assert tests.materialPropertyListCheck()
assert tests.currentPropertyCheck(None)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 1, 0))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1000000000000e+01)
checkpoint Materials page updated
checkpoint property selected
widget_9=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_9.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_9.window))
findWidget('OOF3D:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic
findWidget('Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic').resize(241, 129)
findWidget('Dialog-Parametrize Thermal;Conductivity;Anisotropic;Cubic:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Thermal.Conductivity.Anisotropic.Cubic
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
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic').resize(280, 67)
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubiccopy')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:new_name:Text').set_text('cubic_copy')
findWidget('Dialog-Copy property Thermal;Conductivity;Anisotropic;Cubic:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.2000000000000e+01)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
assert tests.propertyTreeCheck('Thermal:Conductivity:Anisotropic:Cubic:cubic_copy')
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint OOF.Material.Add_property
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material another test to voxels
findWidget('Dialog-Assign material another test to voxels').resize(252, 103)
setComboBox(findWidget('Dialog-Assign material another test to voxels:pixels'), 'green')
#assert tests.chooserCheck('Dialog-Assign material another test to pixels:pixels', ['<selection>', '<every>', 'green'])
findWidget('Dialog-Assign material another test to voxels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Voxel Info')
checkpoint Graphics_1 Voxel Info updated
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.9100000000000e+02,y= 4.6100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.9100000000000e+02,y= 4.6100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
findWidget('OOF3D:Materials Page:Pane:Material:RemoveMaterial').clicked()
checkpoint toplevel widget mapped Dialog-Remove the assigned material from voxels
findWidget('Dialog-Remove the assigned material from voxels').resize(252, 103)
setComboBox(findWidget('Dialog-Remove the assigned material from voxels:pixels'), 'green')
findWidget('Dialog-Remove the assigned material from voxels:gtk-ok').clicked()
checkpoint OOF.Material.Remove
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9100000000000e+02,y= 4.7100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9100000000000e+02,y= 4.7100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9100000000000e+02,y= 4.7100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9100000000000e+02,y= 4.7100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5000000000000e+02,y= 1.8600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5000000000000e+02,y= 1.8600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.5500000000000e+02,y= 2.0100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.5500000000000e+02,y= 2.0100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6400000000000e+02,y= 4.5500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6400000000000e+02,y= 4.5500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
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
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8400000000000e+02,y= 1.9300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8400000000000e+02,y= 1.9300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7900000000000e+02,y= 3.0900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7900000000000e+02,y= 3.0900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7600000000000e+02,y= 2.3700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7600000000000e+02,y= 2.3700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7400000000000e+02,y= 4.4200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7400000000000e+02,y= 4.4200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6100000000000e+02,y= 4.3700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6100000000000e+02,y= 4.3700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
findWidget('OOF3D:Materials Page:Pane:Material:RemoveMaterial').clicked()
checkpoint toplevel widget mapped Dialog-Remove the assigned material from voxels
findWidget('Dialog-Remove the assigned material from voxels').resize(252, 103)
findWidget('Dialog-Remove the assigned material from voxels:gtk-ok').clicked()
checkpoint OOF.Material.Remove
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1700000000000e+02,y= 2.1700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1700000000000e+02,y= 2.1700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5400000000000e+02,y= 2.7600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5400000000000e+02,y= 2.7600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2300000000000e+02,y= 3.5000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2300000000000e+02,y= 3.5000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3200000000000e+02,y= 3.9900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3200000000000e+02,y= 3.9900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.1700000000000e+02,y= 2.2800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.1700000000000e+02,y= 2.2800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7800000000000e+02,y= 4.9400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7800000000000e+02,y= 4.9400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial()
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8600000000000e+02,y= 4.9900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8600000000000e+02,y= 4.9900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7400000000000e+02,y= 2.4900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7400000000000e+02,y= 2.4900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Toolbox.Voxel_Info.Query
assert tests.checkTBMaterial('another test')
findWidget('OOF3D:Materials Page:Pane:Material:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Material "another test"
findWidget('Dialog-Save Material "another test"').resize(190, 123)
findWidget('Dialog-Save Material "another test":filename').set_text('m')
findWidget('Dialog-Save Material "another test":filename').set_text('ma')
findWidget('Dialog-Save Material "another test":filename').set_text('mat')
findWidget('Dialog-Save Material "another test":filename').set_text('mate')
findWidget('Dialog-Save Material "another test":filename').set_text('mater')
findWidget('Dialog-Save Material "another test":filename').set_text('materi')
findWidget('Dialog-Save Material "another test":filename').set_text('materia')
findWidget('Dialog-Save Material "another test":filename').set_text('material')
findWidget('Dialog-Save Material "another test":filename').set_text('material.')
findWidget('Dialog-Save Material "another test":filename').set_text('material.d')
findWidget('Dialog-Save Material "another test":filename').set_text('material.da')
findWidget('Dialog-Save Material "another test":filename').set_text('material.dat')
findWidget('Dialog-Save Material "another test"').resize(198, 123)
findWidget('Dialog-Save Material "another test":gtk-ok').clicked()
checkpoint OOF.File.Save.Materials
#assert tests.filediff('material.dat')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(284)
findWidget('OOF3D:Microstructure Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint microstructure page sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint pixel page updated
checkpoint active area status updated
checkpoint mesh bdy page updated
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
findWidget('OOF3D:Microstructure Page:Pane').set_position(196)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton page sensitized
checkpoint meshable button set
checkpoint OOF.Microstructure.Delete
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Materials')
assert tests.sensitization0()
checkpoint page installed Materials
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(226, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint OOF.Material.Delete
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Property:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(479, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint OOF.Property.Delete
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
widget_10=findWidget('Error')
handled_1=widget_10.event(event(gtk.gdk.DELETE,window=widget_10.window))
postpone if not handled_1: widget_10.destroy()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 1, 0, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_11=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_11.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_11.window))
findWidget('OOF3D:Materials Page:Pane:Property:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(438, 91)
findWidget('Questioner:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().unselect_all()
checkpoint Materials page updated
checkpoint property deselected
checkpoint OOF.Property.Delete
setComboBox(findWidget('OOF3D:Materials Page:Pane:Material:MaterialList'), 'material test')
checkpoint Materials page updated
checkpoint Materials page updated
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(231, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Delete
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(226, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint OOF.Material.Delete
assert tests.chooserStateCheck('OOF3D:Materials Page:Pane:Material:MaterialList', 'another test')
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 1, 0, 0))
checkpoint Materials page updated
checkpoint property selected
widget_12=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_12.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_12.window))
findWidget('OOF3D:Materials Page:Pane:Property:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(479, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint OOF.Property.Delete
assert tests.chooserCheck('OOF3D:Materials Page:Pane:Material:MaterialList', ['another test'])
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
findWidget('OOF3D:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(226, 91)
findWidget('Questioner:gtk-ok').clicked()
checkpoint OOF.Material.Delete
checkpoint toplevel widget mapped Error
findWidget('Error').resize(604, 134)
findWidget('Error:gtk-ok').clicked()
assert tests.sensitization0()
assert tests.chooserCheck('OOF3D:Materials Page:Pane:Material:MaterialList', ['another test'])
assert tests.checkTBMaterial("???")
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
widget_13=findWidget('OOF3D')
handled_2=widget_13.event(event(gtk.gdk.DELETE,window=widget_13.window))
postpone if not handled_2: widget_13.destroy()
checkpoint OOF.Graphics_1.File.Close
