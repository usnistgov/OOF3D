checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:24 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
checkpoint page installed Materials
findWidget('OOF2').resize(684, 350)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
checkpoint Materials page updated
checkpoint property selected
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1,), open_all=False)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0), open_all=False)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_0=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_0.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_0.window))
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Isotropic
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic').resize(282, 72)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0, 0), open_all=False)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance
assert tests.convertibleCij("Isotropic;instance", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
assert tests.sensitiveConvCij("Isotropic;instance", c11=1, c12=1, c44=1)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance').resize(372, 244)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Cij:0,0').set_text('.0')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Cij:0,0').set_text('2.0')
widget_1=findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Cij:0,0')
widget_1.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_1.window))
assert tests.convertibleCij("Isotropic;instance", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=2.0, c44=0.75, c55=0.75, c66=0.75)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'Lame')
assert tests.other('Isotropic;instance', 'Lame', lmbda=0.5, mu=0.75)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'E and nu')
assert tests.other('Isotropic;instance', 'E and nu', young=1.8, poisson=0.2)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'Bulk and Shear')
assert tests.other('Isotropic;instance', 'Bulk and Shear', bulk=1.0, shear=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Bulk and Shear:bulk').set_text('.0000000000000002')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Bulk and Shear:bulk').set_text('2.0000000000000002')
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'E and nu')
assert tests.other('Isotropic;instance', 'E and nu', young=2.0, poisson=1./3.)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'Lame')
assert tests.other('Isotropic;instance', 'Lame', lmbda=1.5, mu=0.75)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'Cij')
assert tests.convertibleCij('Isotropic;instance', c11=3.0, c12=1.5, c13=1.5, c22=3.0, c23=1.5, c33=3.0, c44=0.75, c55=0.75, c66=0.75)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'E and nu')
assert tests.other('Isotropic;instance', 'E and nu', young=2.0, poisson=1./3.)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:E and nu:poisson').set_text('0.5')
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'Bulk and Shear')
checkpoint toplevel widget mapped Warning
findWidget('Warning').resize(310, 85)
findWidget('Warning:OK').clicked()
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:cijkl:Chooser'), 'Cij')
assert tests.convertibleCij('Isotropic;instance', c11=3.0, c12=1.5, c13=1.5, c22=3.0, c23=1.5, c33=3.0, c44=0.75, c55=0.75, c66=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.instance
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
widget_2=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_2.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_2.window))
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Isotropic;instance
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic;instance').resize(282, 72)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic;instance:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
widget_3=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_3.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_3.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0, 1), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2').resize(372, 244)
assert tests.convertibleCij('Isotropic;instance_2', c11=3.0, c12=1.5, c13=1.5, c22=3.0, c23=1.5, c33=3.0, c44=0.75, c55=0.75, c66=0.75)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2:cijkl:Chooser'), 'Lame')
assert tests.other('Isotropic;instance_2', 'Lame', lmbda=1.5, mu=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2:cijkl:Lame:lmbda').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2:cijkl:Lame:lmbda').set_text('3')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.instance_2
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Isotropic;instance_2
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic;instance_2').resize(282, 72)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic;instance_2:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3').resize(214, 128)
findWidget('OOF2:Materials Page:Pane').set_position(272)
assert tests.other('Isotropic;instance_3', 'Lame', lmbda=3.0, mu=0.75)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:Chooser'), 'E and nu')
assert tests.other('Isotropic;instance_3', 'E and nu', young=2.1, poisson=0.4)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3').resize(223, 128)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:E and nu:poisson').set_text('0.5')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.instance_3
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Warning
findWidget('Warning').resize(310, 85)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Warning:OK').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3
assert tests.other('Isotropic;instance_3', 'E and nu', young=2.1, poisson=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3').resize(223, 128)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:E and nu:poisson').set_text('0.4')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.instance_3
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 4.0000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
widget_4=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_4.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_4.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0, 2), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3').resize(223, 128)
assert tests.other('Isotropic;instance_3', 'E and nu', young=2.1, poisson=0.4)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:E and nu:poisson').set_text('0.5')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.instance_3
checkpoint toplevel widget mapped Error
findWidget('Error').resize(592, 166)
findWidget('Error:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane:Material:RemoveProperty').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Remove_property
widget_5=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_5.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_5.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0, 2), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Warning
findWidget('Warning').resize(310, 85)
findWidget('Warning:OK').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3').resize(223, 128)
assert tests.other('Isotropic;instance_3', 'E and nu', young=2.1, poisson=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.instance_3
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint toplevel widget mapped Error
findWidget('Error').resize(592, 166)
findWidget('Error:gtk-ok').clicked()
widget_6=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_6.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_6.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0, 2), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Warning
findWidget('Warning').resize(310, 85)
findWidget('Warning:OK').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3
assert tests.other('Isotropic;instance_3', 'E and nu', young=2.1, poisson=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3').resize(223, 128)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:cijkl:E and nu:poisson').set_text('0.4')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.instance_3
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 4.0000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Isotropic;instance_3
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic;instance_3').resize(282, 72)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic;instance_3:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 1.4000000000000e+01)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4
assert tests.other('Isotropic;instance_4', 'E and nu', young=2.1, poisson=0.4)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4').resize(223, 128)
findWidget('OOF2:Materials Page:Pane').set_position(272)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4:cijkl:Chooser'), 'Bulk and Shear')
assert tests.other('Isotropic;instance_4', 'Bulk and Shear', bulk=3.5, shear=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4:cijkl:Bulk and Shear:shear').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4:cijkl:Bulk and Shear:shear').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.instance_4
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 6.2000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 1.8000000000000e+01)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Materials').activate()
checkpoint toplevel widget mapped Dialog-Materials
findWidget('Dialog-Materials').resize(190, 187)
findWidget('Dialog-Materials:materials').get_selection().unselect_all()
findWidget('Dialog-Materials:materials').get_selection().select_path((0,))
findWidget('Dialog-Materials:filename').set_text('i')
findWidget('Dialog-Materials:filename').set_text('is')
findWidget('Dialog-Materials:filename').set_text('iso')
findWidget('Dialog-Materials:filename').set_text('isom')
findWidget('Dialog-Materials:filename').set_text('isoma')
findWidget('Dialog-Materials:filename').set_text('isomat')
findWidget('Dialog-Materials:filename').set_text('isomat.')
findWidget('Dialog-Materials:filename').set_text('isomat.d')
findWidget('Dialog-Materials:filename').set_text('isomat.da')
findWidget('Dialog-Materials:filename').set_text('isomat.dat')
findWidget('Dialog-Materials:gtk-ok').clicked()
checkpoint OOF.File.Save.Materials
assert tests.filediff('isomat.dat')
findWidget('OOF2:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.Delete
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(194, 72)
findWidget('Dialog-Data:filename').set_text('i')
findWidget('Dialog-Data:filename').set_text('is')
findWidget('Dialog-Data:filename').set_text('iso')
findWidget('Dialog-Data:filename').set_text('isom')
findWidget('Dialog-Data:filename').set_text('isoma')
findWidget('Dialog-Data:filename').set_text('isomat')
findWidget('Dialog-Data:filename').set_text('isomat.')
findWidget('Dialog-Data:filename').set_text('isomat.d')
findWidget('Dialog-Data:filename').set_text('isomat.da')
findWidget('Dialog-Data:filename').set_text('isomat.dat')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.File.Load.Data
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 6.2000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 1.8000000000000e+01)
findWidget('OOF2').resize(684, 356)
findWidget('OOF2').resize(688, 366)
findWidget('OOF2').resize(714, 417)
findWidget('OOF2').resize(738, 447)
findWidget('OOF2').resize(738, 449)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2').resize(738, 449)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_7=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_7.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_7.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0, 0), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance').resize(372, 244)
assert tests.convertibleCij('Isotropic;instance', c11=3.0, c12=1.5, c13=1.5, c22=3.0, c23=1.5, c33=3.0, c44=0.75, c55=0.75, c66=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0, 1))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_8=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_8.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_8.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0, 1), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2').resize(214, 128)
assert tests.other('Isotropic;instance_2', 'Lame', lmbda=3.0, mu=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_2:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0, 2))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_9=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_9.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_9.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0, 2), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3').resize(223, 128)
assert tests.other('Isotropic;instance_3', 'E and nu', young=2.1, poisson=0.4)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_3:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0, 3))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_10=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_10.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_10.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0, 3), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4').resize(210, 128)
assert tests.other('Isotropic;instance_4', 'Bulk and Shear', bulk=3.5, shear=1.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;instance_4:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().unselect_all()
checkpoint Materials page updated
checkpoint property deselected
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').collapse_row((1, 0, 0))
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0, 1), open_all=False)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 0))
checkpoint Materials page updated
checkpoint property selected
widget_11=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_11.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_11.window))
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic
findWidget('Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic').resize(282, 72)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0, 1, 0), open_all=False)
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance').resize(372, 244)
assert tests.convertibleCij("Anisotropic;Cubic;instance", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
assert tests.sensitiveConvCij("Anisotropic;Cubic;instance", c11=1, c12=1, c44=1)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Cij:0,0').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Cij:0,0').set_text('2')
widget_12=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Cij:0,0')
widget_12.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_12.window))
assert tests.convertibleCij("Anisotropic;Cubic;instance", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=2.0, c44=0.25, c55=0.25, c66=0.25)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'Lame')
assert tests.other("Anisotropic;Cubic;instance", "Lame", lmbda=0.5, mu=0.75, aniso=1./3.)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'E and nu')
assert tests.other("Anisotropic;Cubic;instance", "E and nu", young=1.8, poisson=0.2, aniso=1./3.)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'Bulk and Shear')
assert tests.other("Anisotropic;Cubic;instance", "Bulk and Shear", bulk=1.0, shear=0.75, aniso=1./3.)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Bulk and Shear:aniso').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Bulk and Shear:aniso').set_text('0.5')
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'Cij')
assert tests.convertibleCij("Anisotropic;Cubic;instance", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=2.0, c44=0.375, c55=0.375, c66=0.375)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'Lame')
assert tests.other("Anisotropic;Cubic;instance", "Lame", lmbda=0.5, mu=0.75, aniso=0.5)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'E and nu')
assert tests.other("Anisotropic;Cubic;instance", "E and nu", young=1.8, poisson=0.2, aniso=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:E and nu:poisson').set_text('0.5')
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'Lame')
checkpoint toplevel widget mapped Warning
findWidget('Warning').resize(310, 85)
findWidget('Warning:OK').clicked()
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'E and nu')
assert tests.other("Anisotropic;Cubic;instance", "E and nu", young=1.8, poisson=0.2, aniso=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:E and nu:poisson').set_text('0.5')
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'Cij')
checkpoint toplevel widget mapped Warning
findWidget('Warning').resize(310, 85)
findWidget('Warning:OK').clicked()
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:cijkl:Chooser'), 'E and nu')
assert tests.other("Anisotropic;Cubic;instance", "E and nu", young=1.8, poisson=0.2, aniso=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.instance
findWidget('OOF2 Messages 1').resize(575, 200)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance
findWidget('Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance').resize(282, 72)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_2
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_2').resize(223, 152)
assert tests.other("Anisotropic;Cubic;instance_2", "E and nu", young=1.8, poisson=0.2, aniso=0.5)
findWidget('OOF2:Materials Page:Pane').set_position(272)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_2:cijkl:Chooser'), 'Cij')
assert tests.convertibleCij("Anisotropic;Cubic;instance_2", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=2.0, c44=0.375, c55=0.375, c66=0.375)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_2').resize(372, 244)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_2:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.instance_2
findWidget('OOF2 Messages 1').resize(588, 200)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance_2
findWidget('Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance_2').resize(282, 72)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance_2:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3').resize(372, 244)
assert tests.convertibleCij("Anisotropic;Cubic;instance_3", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=2.0, c44=0.375, c55=0.375, c66=0.375)
findWidget('OOF2:Materials Page:Pane').set_position(272)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3:cijkl:Chooser'), 'Lame')
assert tests.other("Anisotropic;Cubic;instance_3", "Lame", lmbda=0.5, mu=0.75, aniso=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3:cijkl:Lame:mu').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3:cijkl:Lame:mu').set_text('0.5')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.instance_3
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance_3
findWidget('Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance_3').resize(282, 72)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('Dialog-Copy property Mechanical;Elasticity;Anisotropic;Cubic;instance_3:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint property selected
checkpoint OOF.Property.Copy
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4').resize(214, 152)
findWidget('OOF2:Materials Page:Pane').set_position(272)
assert tests.other('Anisotropic;Cubic;instance_4', 'Lame', lmbda=0.5, mu=0.5, aniso=0.5)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4:cijkl:Chooser'), 'Bulk and Shear')
assert tests.other('Anisotropic;Cubic;instance_4', 'Bulk and Shear', bulk=0.8333333, shear=0.5, aniso=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4:cijkl:Bulk and Shear:aniso').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4:cijkl:Bulk and Shear:aniso').set_text('0.3')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.instance_4
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:name:Auto').clicked()
findWidget('Dialog-New material:name:Text').set_text('c')
findWidget('Dialog-New material:name:Text').set_text('cu')
findWidget('Dialog-New material:name:Text').set_text('cub')
findWidget('Dialog-New material:name:Text').set_text('cubi')
findWidget('Dialog-New material:name:Text').set_text('cubic')
findWidget('Dialog-New material:name:Text').set_text('cubics')
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 0, 2))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_13=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_13.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_13.window))
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 0, 1))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_14=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_14.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_14.window))
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 0, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_15=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_15.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_15.window))
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property

findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Materials').activate()
checkpoint toplevel widget mapped Dialog-Materials
findWidget('Dialog-Materials').resize(194, 170)
findWidget('Dialog-Materials:filename').set_text('c')
findWidget('Dialog-Materials:filename').set_text('cu')
findWidget('Dialog-Materials:filename').set_text('cub')
findWidget('Dialog-Materials:filename').set_text('cubi')
findWidget('Dialog-Materials:filename').set_text('cubic')
findWidget('Dialog-Materials:filename').set_text('cubics')
findWidget('Dialog-Materials:filename').set_text('cubics.')
findWidget('Dialog-Materials:filename').set_text('cubics.d')
findWidget('Dialog-Materials:filename').set_text('cubics.da')
findWidget('Dialog-Materials:filename').set_text('cubics.dat')
findWidget('Dialog-Materials:materials').get_selection().unselect_all()
findWidget('Dialog-Materials:materials').get_selection().select_path((0,))
findWidget('Dialog-Materials:gtk-ok').clicked()
checkpoint OOF.File.Save.Materials
assert tests.filediff('cubics.dat')
findWidget('OOF2:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Delete
# Accidentally load the data file as a script...
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Script').activate()
checkpoint toplevel widget mapped Dialog-Script
findWidget('Dialog-Script').resize(194, 72)
findWidget('Dialog-Script:filename').set_text('c')
findWidget('Dialog-Script:filename').set_text('cu')
findWidget('Dialog-Script:filename').set_text('cub')
findWidget('Dialog-Script:filename').set_text('cubi')
findWidget('Dialog-Script:filename').set_text('cubic')
findWidget('Dialog-Script:filename').set_text('cubics')
findWidget('Dialog-Script:filename').set_text('cubics.')
findWidget('Dialog-Script:filename').set_text('cubics.d')
findWidget('Dialog-Script:filename').set_text('cubics.da')
findWidget('Dialog-Script:filename').set_text('cubics.dat')
findWidget('Dialog-Script:gtk-ok').clicked()
checkpoint toplevel widget mapped Error
findWidget('Error').resize(592, 166)
findWidget('OOF2 Activity Viewer').resize(400, 300)
findWidget('Error:gtk-ok').clicked()
# Load the data file correctly.
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
checkpoint OOF.File.Load.Script
findWidget('Dialog-Data').resize(194, 72)
findWidget('Dialog-Data:filename').set_text('c')
findWidget('Dialog-Data:filename').set_text('cu')
findWidget('Dialog-Data:filename').set_text('cub')
findWidget('Dialog-Data:filename').set_text('cubi')
findWidget('Dialog-Data:filename').set_text('cubic')
findWidget('Dialog-Data:filename').set_text('cubics')
findWidget('Dialog-Data:filename').set_text('cubics.')
findWidget('Dialog-Data:filename').set_text('cubics.d')
findWidget('Dialog-Data:filename').set_text('cubics.da')
findWidget('Dialog-Data:filename').set_text('cubics.dat')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.File.Load.Data
widget_16=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_16.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_16.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 0, 0), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance').resize(223, 152)
assert tests.other('Anisotropic;Cubic;instance', 'E and nu', young=1.8, poisson=0.2, aniso=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 0, 1))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_17=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_17.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_17.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 0, 1), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_2
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_2').resize(372, 244)
assert tests.convertibleCij('Anisotropic;Cubic;instance_2', c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=2.0, c44=0.375, c55=0.375, c66=0.375)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_2:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 0, 2))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_18=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_18.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_18.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 0, 2), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3').resize(214, 152)
assert tests.other('Anisotropic;Cubic;instance_3', 'Lame', lmbda=0.5, mu=0.5, aniso=0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_3:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 0, 3))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_19=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_19.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_19.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 0, 3), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4').resize(210, 152)
assert tests.other('Anisotropic;Cubic;instance_4', 'Bulk and Shear', bulk=0.8333333333, shear=0.5, aniso=0.3)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Cubic;instance_4:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().unselect_all()
checkpoint Materials page updated
checkpoint property deselected
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').collapse_row((1, 0, 1, 0))
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:name:Text').set_text('')
findWidget('Dialog-New material:name:Text').set_text('a')
findWidget('Dialog-New material:name:Text').set_text('an')
findWidget('Dialog-New material:name:Text').set_text('ani')
findWidget('Dialog-New material:name:Text').set_text('anis')
findWidget('Dialog-New material:name:Text').set_text('aniso')
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 1))
checkpoint Materials page updated
checkpoint property selected
widget_20=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_20.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_20.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 1), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal').resize(368, 212)
assert tests.anisoCij("Hexagonal", c11=1.0, c12=0.5, c22=1.0, c66=0.25)
assert tests.sensitiveAnisoCij("Hexagonal", c11=1, c12=1, c13=1, c33=1, c44=1, c66=1)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,0').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,0').set_text('2')
widget_21=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,0')
widget_21.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_21.window))
assert tests.anisoCij("Hexagonal", c11=2.0, c12=0.5, c22=2.0, c66=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,1').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,1').set_text('3')
widget_22=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,1')
widget_22.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_22.window))
assert tests.anisoCij("Hexagonal", c11=2.0, c12=3.0, c22=2.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,2').set_text('4')
widget_23=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,2')
widget_23.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_23.window))
assert tests.anisoCij("Hexagonal", c11=2.0, c12=3.0, c13=4.0, c22=2.0, c23=4.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:2,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:2,2').set_text('1')
widget_24=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:2,2')
widget_24.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_24.window))
assert tests.anisoCij("Hexagonal", c11=2.0, c12=3.0, c13=4.0, c22=2.0, c23=4.0, c33=1.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:3,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:3,3').set_text('2')
widget_25=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:3,3')
widget_25.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_25.window))
assert tests.anisoCij("Hexagonal", c11=2.0, c12=3.0, c13=4.0, c22=2.0, c23=4.0, c33=1.0, c44=2.0 , c55=2.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:5,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:5,5').set_text('-')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:5,5').set_text('-1')
widget_26=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:5,5')
widget_26.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_26.window))
assert tests.anisoCij("Hexagonal", c11=2.0, c12=4.0, c13=4.0, c22=2.0, c23=4.0, c33=1.0, c44=2.0 , c55=2.0, c66=-1.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Hexagonal
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 2))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_27=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_27.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_27.window))
widget_28=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_28.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_28.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 2), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal').resize(368, 212)
assert tests.anisoCij("Tetragonal", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0)
assert tests.sensitiveAnisoCij("Tetragonal", c11=1, c12=1, c13=1, c16=1, c33=1, c44=1, c66=1)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,0').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,0').set_text('2')
widget_29=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,0')
widget_29.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_29.window))
assert tests.anisoCij("Tetragonal", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=1.0)
widget_30=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,1')
widget_30.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_30.window))
assert tests.anisoCij("Tetragonal", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=1.0)
findWidget('OOF2').resize(738, 449)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,1').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,1').set_text('3')
widget_31=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,1')
widget_31.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_31.window))
assert tests.anisoCij("Tetragonal", c11=2.0, c12=3.0, c13=0.5, c22=2.0, c23=0.5, c33=1.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,2').set_text('4')
widget_32=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,2')
widget_32.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_32.window))
assert tests.anisoCij("Tetragonal", c11=2.0, c12=3.0, c13=4.0, c22=2.0, c23=4.0, c33=1.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,5').set_text('5')
widget_33=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,5')
widget_33.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_33.window))
assert tests.anisoCij("Tetragonal", c11=2.0, c12=3.0, c13=4.0, c16=5.0, c22=2.0, c23=4.0, c26=-5.0, c33=1.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:2,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:2,2').set_text('6')
widget_34=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:2,2')
widget_34.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_34.window))
assert tests.anisoCij("Tetragonal", c11=2.0, c12=3.0, c13=4.0, c16=5.0, c22=2.0, c23=4.0, c26=-5.0, c33=6.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:3,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:3,3').set_text('7')
widget_35=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:3,3')
widget_35.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_35.window))
assert tests.anisoCij("Tetragonal", c11=2.0, c12=3.0, c13=4.0, c16=5.0, c22=2.0, c23=4.0, c26=-5.0, c33=6.0, c44=7.0, c55=7.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:5,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:5,5').set_text('8')
widget_36=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:5,5')
widget_36.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_36.window))
assert tests.anisoCij("Tetragonal", c11=2.0, c12=3.0, c13=4.0, c16=5.0, c22=2.0, c23=4.0, c26=-5.0, c33=6.0, c44=7.0, c55=7.0, c66=8.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Tetragonal
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 3))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_37=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_37.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_37.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 3), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA
assert tests.anisoCij("TrigonalA", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
assert tests.sensitiveAnisoCij("TrigonalA", c11=1, c12=1, c13=1, c14=1, c15=1, c33=1, c44=1, c66=1)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA').resize(368, 212)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,0').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,0').set_text('2')
widget_38=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,0')
widget_38.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_38.window))
assert tests.anisoCij("TrigonalA", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,1').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,1').set_text('3')
widget_39=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,1')
widget_39.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_39.window))
assert tests.anisoCij("TrigonalA", c11=2.0, c12=3.0, c13=0.5, c22=2.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,2').set_text('4')
widget_40=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,2')
widget_40.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_40.window))
assert tests.anisoCij("TrigonalA", c11=2.0, c12=3.0, c13=4.0, c22=2.0, c23=4.0, c33=1.0, c44=0.25, c55=0.25, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,3').set_text('5')
widget_41=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,3')
widget_41.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_41.window))
assert tests.anisoCij("TrigonalA", c11=2.0, c12=3.0, c13=4.0, c14=5.0, c22=2.0, c23=4.0, c24=-5.0, c33=1.0, c44=0.25, c55=0.25, c56=5.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,4').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,4').set_text('6')
widget_42=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,4')
widget_42.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_42.window))
assert tests.anisoCij("TrigonalA", c11=2.0, c12=3.0, c13=4.0, c14=5.0, c15=6.0, c22=2.0, c23=4.0, c24=-5.0, c25=-6.0, c33=1.0, c44=0.25, c46=-6.0, c55=0.25, c56=5.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:2,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:2,2').set_text('7')
widget_43=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:2,2')
widget_43.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_43.window))
assert tests.anisoCij("TrigonalA", c11=2.0, c12=3.0, c13=4.0, c14=5.0, c15=6.0, c22=2.0, c23=4.0, c24=-5.0, c25=-6.0, c33=7.0, c44=0.25, c46=-6.0, c55=0.25, c56=5.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:3,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:3,3').set_text('8')
widget_44=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:3,3')
widget_44.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_44.window))
assert tests.anisoCij("TrigonalA", c11=2.0, c12=3.0, c13=4.0, c14=5.0, c15=6.0, c22=2.0, c23=4.0, c24=-5.0, c25=-6.0, c33=7.0, c44=8.0, c46=-6.0, c55=8.0, c56=5.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:5,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:5,5').set_text('-')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:5,5').set_text('-1')
widget_45=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:5,5')
widget_45.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_45.window))
assert tests.anisoCij("TrigonalA", c11=2.0, c12=4.0, c13=4.0, c14=5.0, c15=6.0, c22=2.0, c23=4.0, c24=-5.0, c25=-6.0, c33=7.0, c44=8.0, c46=-6.0, c55=8.0, c56=5.0, c66=-1.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.TrigonalA
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 4))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_46=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_46.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_46.window))
widget_47=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_47.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_47.window))
widget_48=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_48.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_48.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 4), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB').resize(368, 212)
assert tests.anisoCij("TrigonalB", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
assert tests.sensitiveAnisoCij("TrigonalB", c11=1, c12=1, c13=1, c14=1, c33=1, c44=1, c66=1)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,0').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,0').set_text('2')
widget_49=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,0')
widget_49.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_49.window))
assert tests.anisoCij("TrigonalB", c11=2.0, c12=0.5, c13=0.5, c22=2.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.75)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,1').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,1').set_text('3')
widget_50=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,1')
widget_50.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_50.window))
assert tests.anisoCij("TrigonalB", c11=2.0, c12=3.0, c13=0.5, c22=2.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,2').set_text('4')
widget_51=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,2')
widget_51.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_51.window))
assert tests.anisoCij("TrigonalB", c11=2.0, c12=3.0, c13=4.0, c22=2.0, c23=4.0, c33=1.0, c44=0.25, c55=0.25, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,3').set_text('5')
widget_52=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,3')
widget_52.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_52.window))
assert tests.anisoCij("TrigonalB", c11=2.0, c12=3.0, c13=4.0, c14=5.0, c22=2.0, c23=4.0, c24=-5.0, c33=1.0, c44=0.25, c55=0.25, c56=5.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:2,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:2,2').set_text('6')
widget_53=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:2,2')
widget_53.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_53.window))
assert tests.anisoCij("TrigonalB", c11=2.0, c12=3.0, c13=4.0, c14=5.0, c22=2.0, c23=4.0, c24=-5.0, c33=6.0, c44=0.25, c55=0.25, c56=5.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:3,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:3,3').set_text('7')
widget_54=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:3,3')
widget_54.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_54.window))
assert tests.anisoCij("TrigonalB", c11=2.0, c12=3.0, c13=4.0, c14=5.0, c22=2.0, c23=4.0, c24=-5.0, c33=6.0, c44=7.0, c55=7.0, c56=5.0, c66=-0.5)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:5,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:5,5').set_text('8')
widget_55=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:5,5')
widget_55.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_55.window))
assert tests.anisoCij("TrigonalB", c11=2.0, c12=-14.0, c13=4.0, c14=5.0, c22=2.0, c23=4.0, c24=-5.0, c33=6.0, c44=7.0, c55=7.0, c56=5.0, c66=8.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.TrigonalB
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 5))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_56=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_56.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_56.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 5), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic
assert tests.anisoCij("Orthorhombic", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
assert tests.sensitiveAnisoCij("Orthorhombic", c11=1, c12=1, c13=1, c22=1, c23=1, c33=1, c44=1, c55=1, c66=1)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic').resize(368, 212)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,0').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,0').set_text('2')
widget_57=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,0')
widget_57.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_57.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,1').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,1').set_text('3')
widget_58=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,1')
widget_58.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_58.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,2').set_text('4')
widget_59=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,2')
widget_59.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_59.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=4.0, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:1,1').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:1,1').set_text('5')
widget_60=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:1,1')
widget_60.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_60.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=4.0, c22=5.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:1,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:1,2').set_text('6')
widget_61=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:1,2')
widget_61.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_61.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=4.0, c22=5.0, c23=6.0, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:2,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:2,2').set_text('7')
widget_62=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:2,2')
widget_62.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_62.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=4.0, c22=5.0, c23=6.0, c33=7.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:3,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:3,3').set_text('8')
widget_63=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:3,3')
widget_63.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_63.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=4.0, c22=5.0, c23=6.0, c33=7.0, c44=8.0, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:4,4').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:4,4').set_text('9')
widget_64=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:4,4')
widget_64.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_64.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=4.0, c22=5.0, c23=6.0, c33=7.0, c44=8.0, c55=9.0, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:5,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:5,5').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:5,5').set_text('10')
widget_65=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:5,5')
widget_65.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_65.window))
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=4.0, c22=5.0, c23=6.0, c33=7.0, c44=8.0, c55=9.0, c66=10.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Orthorhombic
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 2.9000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2').resize(738, 449)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 6))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.0000000000000e+00)
widget_66=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_66.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_66.window))
widget_67=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_67.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_67.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 6), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic
assert tests.anisoCij("Monoclinic", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=0.25, c44=0.25, c55=0.25, c66=0.25)
assert tests.sensitiveAnisoCij("Monoclinic", c11=1, c12=1, c13=1, c15=1, c22=1, c23=1, c25=1, c33=1, c35=1, c44=1, c46=1, c55=1, c66=1)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic').resize(368, 212)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,0').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,0').set_text('2')
widget_68=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,0')
widget_68.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_68.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=0.25, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,1').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,1').set_text('3')
widget_69=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,1')
widget_69.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_69.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=0.5, c22=1.0, c23=0.5, c33=0.25, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,2').set_text('4')
widget_70=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,2')
widget_70.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_70.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c22=1.0, c23=0.5, c33=0.25, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,4').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,4').set_text('5')
widget_71=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,4')
widget_71.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_71.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=1.0, c23=0.5, c33=0.25, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,1').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,1').set_text('6')
widget_72=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,1')
widget_72.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_72.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=0.5, c33=0.25, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,2').set_text('7')
widget_73=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,2')
widget_73.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_73.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c33=0.25, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,4').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,4').set_text('8')
widget_74=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:1,4')
widget_74.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_74.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c25=8.0, c33=0.25, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:2,2').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:2,2').set_text('9')
widget_75=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:2,2')
widget_75.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_75.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c25=8.0, c33=9.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:2,4').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:2,4').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:2,4').set_text('10')
widget_76=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:2,4')
widget_76.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_76.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c25=8.0, c33=9.0, c35=10, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:3,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:3,3').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:3,3').set_text('11')
widget_77=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:3,3')
widget_77.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_77.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c25=8.0, c33=9.0, c35=10, c44=11.0, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:3,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:3,5').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:3,5').set_text('12')
widget_78=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:3,5')
widget_78.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_78.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c25=8.0, c33=9.0, c35=10, c44=11.0, c46=12.0, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:4,4').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:4,4').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:4,4').set_text('13')
widget_79=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:4,4')
widget_79.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_79.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c25=8.0, c33=9.0, c35=10, c44=11.0, c46=12.0, c55=13.0, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:5,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:5,5').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:5,5').set_text('14')
widget_80=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:5,5')
widget_80.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_80.window))
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c25=8.0, c33=9.0, c35=10, c44=11.0, c46=12.0, c55=13.0, c66=14.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Monoclinic
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 5.1000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 2.9000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 7))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_81=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_81.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_81.window))
widget_82=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_82.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_82.window))
widget_83=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_83.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_83.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 7), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic
assert tests.anisoCij("Triclinic", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
assert tests.sensitiveAnisoCij("Triclinic", c11=1, c12=1, c13=1, c14=1, c15=1, c16=1, c22=1, c23=1, c24=1, c25=1, c26=1, c33=1, c34=1, c35=1, c36=1, c44=1, c45=1, c46=1, c55=1, c56=1, c66=1)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic').resize(368, 212)
widget_84=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:0,0')
widget_84.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_84.window))
assert tests.anisoCij("Triclinic", c11=1.0, c12=0.5, c13=0.5, c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:0,5').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:0,5').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:0,5').set_text('12')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:0,5').set_text('123')
widget_85=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:0,5')
widget_85.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_85.window))
assert tests.anisoCij("Triclinic", c11=1.0, c12=0.5, c13=0.5, c16=123., c22=1.0, c23=0.5, c33=1.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:1,4').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:1,4').set_text('4')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:1,4').set_text('45')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:1,4').set_text('456')
widget_86=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:1,4')
widget_86.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_86.window))
assert tests.anisoCij("Triclinic", c11=1.0, c12=0.5, c13=0.5, c16=123., c22=1.0, c23=0.5, c25=456., c33=1.0, c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:2,3').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:2,3').set_text('7')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:2,3').set_text('78')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:2,3').set_text('789')
widget_87=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:2,3')
widget_87.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_87.window))
assert tests.anisoCij("Triclinic", c11=1.0, c12=0.5, c13=0.5, c16=123., c22=1.0, c23=0.5, c25=456., c33=1.0, c34=789., c44=0.25, c55=0.25, c66=0.25)
widget_88=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:2,4')
widget_88.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_88.window))
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Triclinic
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 7.3000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Materials').activate()
checkpoint toplevel widget mapped Dialog-Materials
findWidget('Dialog-Materials').resize(194, 170)
findWidget('Dialog-Materials:filename').set_text('a')
findWidget('Dialog-Materials:filename').set_text('an')
findWidget('Dialog-Materials:filename').set_text('ani')
findWidget('Dialog-Materials:filename').set_text('anis')
findWidget('Dialog-Materials:filename').set_text('aniso')
findWidget('Dialog-Materials:filename').set_text('aniso.')
findWidget('Dialog-Materials:filename').set_text('aniso.d')
findWidget('Dialog-Materials:filename').set_text('aniso.da')
findWidget('Dialog-Materials:filename').set_text('aniso.dat')
findWidget('Dialog-Materials:materials').get_selection().unselect_all()
findWidget('Dialog-Materials:materials').get_selection().select_path((0,))
findWidget('Dialog-Materials:gtk-ok').clicked()
checkpoint OOF.File.Save.Materials
assert tests.filediff('aniso.dat')
findWidget('OOF2:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.Delete
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(194, 72)
findWidget('Dialog-Data:filename').set_text('a')
findWidget('Dialog-Data:filename').set_text('an')
findWidget('Dialog-Data:filename').set_text('ani')
findWidget('Dialog-Data:filename').set_text('anis')
findWidget('Dialog-Data:filename').set_text('aniso')
findWidget('Dialog-Data:filename').set_text('aniso.')
findWidget('Dialog-Data:filename').set_text('aniso.d')
findWidget('Dialog-Data:filename').set_text('aniso.da')
findWidget('Dialog-Data:filename').set_text('aniso.dat')
findWidget('Dialog-Data:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 7.3000000000000e+01)
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
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
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.File.Load.Data
findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll:PropertyList').get_selection().select_path((0,))
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
tree=findWidget('OOF2:Materials Page:Pane:Material:PropertyListScroll:PropertyList')
column = tree.get_column(0)
tree.row_activated((0,), column)
widget_89=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_89.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_89.window))
widget_90=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_90.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_90.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 1), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal
assert tests.anisoCij("Hexagonal", c11=2.0, c12=4.0, c13=4.0, c22=2.0, c23=4.0, c33=1.0, c44=2.0 , c55=2.0, c66=-1.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal').resize(368, 212)
widget_91=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:0,0')
widget_91.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_91.window))
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Hexagonal:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 2))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_92=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_92.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_92.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 2), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal
assert tests.anisoCij("Tetragonal", c11=2.0, c12=3.0, c13=4.0, c16=5.0, c22=2.0, c23=4.0, c26=-5.0, c33=6.0, c44=7.0, c55=7.0, c66=8.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal').resize(368, 212)
widget_93=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:0,0')
widget_93.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_93.window))
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Tetragonal:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 3))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_94=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_94.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_94.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 3), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA
assert tests.anisoCij("TrigonalA", c11=2.0, c12=4.0, c13=4.0, c14=5.0, c15=6.0, c22=2.0, c23=4.0, c24=-5.0, c25=-6.0, c33=7.0, c44=8.0, c46=-6.0, c55=8.0, c56=5.0, c66=-1.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA').resize(368, 212)
widget_95=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:0,0')
widget_95.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_95.window))
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalA:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 4))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_96=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_96.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_96.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 4), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB
assert tests.anisoCij("TrigonalB", c11=2.0, c12=-14.0, c13=4.0, c14=5.0, c22=2.0, c23=4.0, c24=-5.0, c33=6.0, c44=7.0, c55=7.0, c56=5.0, c66=8.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB').resize(368, 212)
widget_97=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:0,0')
widget_97.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_97.window))
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;TrigonalB:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 5))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_98=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_98.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_98.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 5), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic
assert tests.anisoCij("Orthorhombic", c11=2.0, c12=3.0, c13=4.0, c22=5.0, c23=6.0, c33=7.0, c44=8.0, c55=9.0, c66=10.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic').resize(368, 212)
widget_99=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:0,0')
widget_99.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_99.window))
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Orthorhombic:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 6))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_100=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_100.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_100.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 6), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic
assert tests.anisoCij("Monoclinic", c11=2.0, c12=3.0, c13=4.0, c15=5.0, c22=6.0, c23=7.0, c25=8.0, c33=9.0, c35=10, c44=11.0, c46=12.0, c55=13.0, c66=14.0)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic').resize(368, 212)
widget_101=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:0,0')
widget_101.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_101.window))
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Monoclinic:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 1, 7))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_102=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_102.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_102.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 1, 7), column)
checkpoint Materials page updated
checkpoint property selected
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic
assert tests.anisoCij("Triclinic", c11=1.0, c12=0.5, c13=0.5, c16=123., c22=1.0, c23=0.5, c25=456., c33=1.0, c34=789., c44=0.25, c55=0.25, c66=0.25)
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic').resize(368, 212)
widget_103=findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:0,0')
widget_103.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_103.window))
findWidget('Dialog-Parametrize Mechanical;Elasticity;Anisotropic;Triclinic:gtk-cancel').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.0222222222222e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1901234567901e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.3580246913580e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.5259259259259e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.8617283950617e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.1975308641975e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.5333333333333e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 4.7012345679012e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 5.2049382716049e+01)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 5.3728395061728e+01)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('m')
findWidget('Dialog-Python_Log:filename').set_text('ma')
findWidget('Dialog-Python_Log:filename').set_text('mat')
findWidget('Dialog-Python_Log:filename').set_text('matt')
findWidget('Dialog-Python_Log:filename').set_text('matte')
findWidget('Dialog-Python_Log:filename').set_text('mattes')
findWidget('Dialog-Python_Log:filename').set_text('mattest')
findWidget('Dialog-Python_Log:filename').set_text('mattest1')
findWidget('Dialog-Python_Log:filename').set_text('mattest1.')
findWidget('Dialog-Python_Log:filename').set_text('mattest1.l')
findWidget('Dialog-Python_Log:filename').set_text('mattest1.lo')
findWidget('Dialog-Python_Log:filename').set_text('mattest1.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('mattest1.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
