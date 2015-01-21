# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.8 $
# $Author: fyc $
# $Date: 2014/04/30 21:07:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This test validate the image page handling.
# All the Methods are tested with the different parts that they have.
# The test start by loading the images in the folder specified in args to create a new the microstructure.

import tests

findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D Messages 1').resize(603, 200)
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
findWidget('OOF3D:Navigation:Next').clicked()
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D:Navigation:Next').clicked()
assert tests.sensitization0()
assert tests.chooserCheck('OOF3D:Image Page:Microstructure', ['5color'])
assert tests.chooserCheck('OOF3D:Image Page:Image', ['5color'])
assert tests.chooserStateCheck('OOF3D:Image Page:Image', '5color')
checkpoint page installed Image
findWidget('OOF3D').resize(601, 350)
findWidget('OOF3D:Image Page:Pane').set_position(395)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Gray
assert tests.sensitization1()
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
assert tests.sensitization2()
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'Flip')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Flip:axis'), 'y')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Flip:axis'), 'z')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Flip:axis'), 'xy')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Flip:axis'), 'yz')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Flip:axis'), 'xz')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Flip:axis'), 'xyz')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
assert tests.sensitization4()
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
assert tests.sensitization4()
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
assert tests.sensitization4()
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
assert tests.sensitization4()
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
assert tests.sensitization4()
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
assert tests.sensitization4()
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
assert tests.sensitization5()
findWidget('OOF3D:Image Page:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy Image
findWidget('Dialog-Copy Image').resize(316, 93)
findWidget('Dialog-Copy Image:gtk-ok').clicked()
checkpoint microstructure page sensitized
checkpoint OOF.Image.Copy
assert tests.chooserCheck('OOF3D:Image Page:Image', ['5color', '5color<2>'])
assert tests.chooserStateCheck('OOF3D:Image Page:Image', '5color<2>')
findWidget('OOF3D:Image Page:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy Image
findWidget('Dialog-Copy Image').resize(316, 93)
findWidget('Dialog-Copy Image:name:Auto').clicked()
findWidget('Dialog-Copy Image:name:Text').set_text('c')
findWidget('Dialog-Copy Image:name:Text').set_text('co')
findWidget('Dialog-Copy Image:name:Text').set_text('cop')
findWidget('Dialog-Copy Image:name:Text').set_text('copy')
findWidget('Dialog-Copy Image:gtk-ok').clicked()
checkpoint microstructure page sensitized
checkpoint OOF.Image.Copy
assert tests.chooserCheck('OOF3D:Image Page:Image', ['5color', '5color<2>', 'copy'])
assert tests.chooserStateCheck('OOF3D:Image Page:Image', 'copy')
setComboBox(findWidget('OOF3D:Image Page:Image'), '5color')
setComboBox(findWidget('OOF3D:Image Page:Image'), '5color<2>')
findWidget('OOF3D:Image Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(200, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint microstructure page sensitized
checkpoint Field page sensitized
##checkpoint skeleton page sensitized
checkpoint OOF.Image.Delete
assert tests.sensitization5()
assert tests.chooserCheck('OOF3D:Image Page:Image', ['5color', 'copy'])
assert tests.chooserStateCheck('OOF3D:Image Page:Image', '5color')
findWidget('OOF3D:Image Page:Group').clicked()
checkpoint toplevel widget mapped Dialog-AutoGroup
findWidget('Dialog-AutoGroup').resize(222, 67)
findWidget('Dialog-AutoGroup:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.Image.AutoGroup
findWidget('OOF3D:Navigation:Prev').clicked()
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(246)
assert tests.micro_sensitization()
findWidget('OOF3D:Navigation:Next').clicked()
checkpoint page installed Image
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'Permute_Axes')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Permute_Axes
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Permute_Axes:axes'), 'xzy')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Permute_Axes
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Permute_Axes:axes'), 'zyx')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Permute_Axes
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Permute_Axes:axes'), 'yzx')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Permute_Axes
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Permute_Axes:axes'), 'zxy')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Permute_Axes
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'Fade')
findWidget('OOF3D:Image Page:Pane').set_position(364)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Fade
findWidget('OOF3D:Image Page:Pane:Method:Fade:factor:slider').get_adjustment().set_value( 1.0769230769231e-01)
findWidget('OOF3D:Image Page:Pane:Method:Fade:factor:slider').get_adjustment().set_value( 4.6153846153846e-01)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Fade
findWidget('OOF3D:Image Page:Pane:Method:Fade:factor:slider').get_adjustment().set_value( 4.7692307692308e-01)
findWidget('OOF3D:Image Page:Pane:Method:Fade:factor:slider').get_adjustment().set_value( 7.8461538461538e-01)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Fade
findWidget('OOF3D:Image Page:Pane:Method:Fade:factor:slider').get_adjustment().set_value( 7.6923076923077e-01)
findWidget('OOF3D:Image Page:Pane:Method:Fade:factor:slider').get_adjustment().set_value( 1.6923076923077e-01)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Fade
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Fade
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'Dim')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Dim
findWidget('OOF3D:Image Page:Pane:Method:Dim:factor:slider').get_adjustment().set_value( 8.9230769230769e-01)
findWidget('OOF3D:Image Page:Pane:Method:Dim:factor:slider').get_adjustment().set_value( 4.4615384615385e-01)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Dim
findWidget('OOF3D:Image Page:Pane:Method:Dim:factor:slider').get_adjustment().set_value( 4.6153846153846e-01)
findWidget('OOF3D:Image Page:Pane:Method:Dim:factor:slider').get_adjustment().set_value( 8.1538461538462e-01)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Dim
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'Blur')
findWidget('OOF3D:Image Page:Pane').set_position(395)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Blur
findWidget('OOF3D:Image Page:Pane:Method:Blur:radius').set_text('0.')
findWidget('OOF3D:Image Page:Pane:Method:Blur:radius').set_text('0.5')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Blur
findWidget('OOF3D:Image Page:Pane:Method:Blur:sigma').set_text('')
findWidget('OOF3D:Image Page:Pane:Method:Blur:sigma').set_text('0')
findWidget('OOF3D:Image Page:Pane:Method:Blur:sigma').set_text('0.')
findWidget('OOF3D:Image Page:Pane:Method:Blur:sigma').set_text('0.5')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Blur
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'Contrast')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Contrast
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('')
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('0')
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('0.')
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('0.5')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Contrast
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('0')
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('01')
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('0')
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('')
findWidget('OOF3D:Image Page:Pane:Method:Contrast:factor').set_text('1')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Contrast
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'MedianFilter')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.MedianFilter
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('')
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('0')
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('0.')
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('0.5')
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('0.')
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('0')
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('')
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('2')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.MedianFilter
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('')
findWidget('OOF3D:Image Page:Pane:Method:MedianFilter:radius').set_text('3')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.MedianFilter
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'Negate')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Negate
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Negate
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Negate
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Negate
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'Normalize')
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Normalize
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.Normalize
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
setComboBox(findWidget('OOF3D:Image Page:Pane:Method:Chooser'), 'ThresholdImage')
findWidget('OOF3D:Image Page:Pane').set_position(394)
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.ThresholdImage
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.ThresholdImage
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.ThresholdImage
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.ThresholdImage
findWidget('OOF3D:Image Page:Pane:OK').clicked()
checkpoint OOF.Image.Modify.ThresholdImage
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Image Page:Pane:Undo').clicked()
checkpoint OOF.Image.Undo
findWidget('OOF3D:Navigation:Prev').clicked()
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(315, 199)
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(174)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
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
checkpoint OOF.Microstructure.New
findWidget('OOF3D:Navigation:Next').clicked()
assert tests.chooserCheck('OOF3D:Image Page:Microstructure', ['5color', 'microstructure'])
assert tests.chooserStateCheck('OOF3D:Image Page:Microstructure', '5color')
checkpoint page installed Image
setComboBox(findWidget('OOF3D:Image Page:Microstructure'), 'microstructure')
assert tests.chooserStateCheck('OOF3D:Image Page:Microstructure', 'microstructure')
assert tests.chooserCheck('OOF3D:Image Page:Image', [])
assert tests.sensitization6()
setComboBox(findWidget('OOF3D:Image Page:Microstructure'), '5color')
assert tests.sensitization5()
assert tests.chooserCheck('OOF3D:Image Page:Image', ['5color', 'copy'])
assert tests.chooserStateCheck('OOF3D:Image Page:Image', '5color')
findWidget('OOF3D:Image Page:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename Image
findWidget('Dialog-Rename Image').resize(190, 67)
findWidget('Dialog-Rename Image:name').set_text('')
findWidget('Dialog-Rename Image:name').set_text('r')
findWidget('Dialog-Rename Image:name').set_text('re')
findWidget('Dialog-Rename Image:name').set_text('ren')
findWidget('Dialog-Rename Image:name').set_text('rena')
findWidget('Dialog-Rename Image:name').set_text('renam')
findWidget('Dialog-Rename Image:name').set_text('rename')
findWidget('Dialog-Rename Image:name').set_text('renamed')
findWidget('Dialog-Rename Image:gtk-ok').clicked()
checkpoint OOF.Image.Rename
assert tests.sensitization5()
assert tests.chooserCheck('OOF3D:Image Page:Image', ['renamed', 'copy'])
assert tests.chooserStateCheck('OOF3D:Image Page:Image', 'renamed')
findWidget('OOF3D:Image Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Image
findWidget('Dialog-Save Image').resize(190, 123)
findWidget('Dialog-Save Image:filename').set_text('')
findWidget('Dialog-Save Image:filename').set_text('p')
findWidget('Dialog-Save Image:filename').set_text('pn')
findWidget('Dialog-Save Image:filename').set_text('png')
findWidget('Dialog-Save Image:filename').set_text('png_')
findWidget('Dialog-Save Image:filename').set_text('png_i')
findWidget('Dialog-Save Image:filename').set_text('png_im')
findWidget('Dialog-Save Image:filename').set_text('png_ima')
findWidget('Dialog-Save Image:filename').set_text('png_imag')
findWidget('Dialog-Save Image:filename').set_text('png_image')
findWidget('Dialog-Save Image').resize(198, 123)
findWidget('Dialog-Save Image:gtk-ok').clicked()
checkpoint OOF.File.Save.Image
findWidget('OOF3D:Image Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Image
findWidget('Dialog-Save Image').resize(190, 123)
findWidget('Dialog-Save Image:filename').set_text('')
findWidget('Dialog-Save Image:filename').set_text('b')
findWidget('Dialog-Save Image:filename').set_text('bm')
findWidget('Dialog-Save Image:filename').set_text('bmp')
findWidget('Dialog-Save Image:filename').set_text('bmp_')
findWidget('Dialog-Save Image:filename').set_text('bmp_i')
findWidget('Dialog-Save Image:filename').set_text('bmp_im')
findWidget('Dialog-Save Image:filename').set_text('bmp_ima')
findWidget('Dialog-Save Image:filename').set_text('bmp_imag')
findWidget('Dialog-Save Image:filename').set_text('bmp_image')
findWidget('Dialog-Save Image').resize(198, 123)
setComboBox(findWidget('Dialog-Save Image:format'), 'bmp')
findWidget('Dialog-Save Image:gtk-ok').clicked()
checkpoint OOF.File.Save.Image
findWidget('OOF3D:Image Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Image
findWidget('Dialog-Save Image').resize(190, 123)
findWidget('Dialog-Save Image:filename').set_text('')
findWidget('Dialog-Save Image:filename').set_text('j')
findWidget('Dialog-Save Image:filename').set_text('jp')
findWidget('Dialog-Save Image:filename').set_text('jpg')
findWidget('Dialog-Save Image:filename').set_text('jpg_')
findWidget('Dialog-Save Image:filename').set_text('jpg_i')
findWidget('Dialog-Save Image:filename').set_text('jpg_im')
findWidget('Dialog-Save Image:filename').set_text('jpg_ima')
findWidget('Dialog-Save Image:filename').set_text('jpg_imag')
findWidget('Dialog-Save Image:filename').set_text('jpg_image')
findWidget('Dialog-Save Image').resize(198, 123)
setComboBox(findWidget('Dialog-Save Image:format'), 'jpg')
findWidget('Dialog-Save Image:gtk-ok').clicked()
checkpoint OOF.File.Save.Image
findWidget('OOF3D:Image Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Image
findWidget('Dialog-Save Image').resize(190, 123)
findWidget('Dialog-Save Image:filename').set_text('')
findWidget('Dialog-Save Image:filename').set_text('p')
findWidget('Dialog-Save Image:filename').set_text('pn')
findWidget('Dialog-Save Image:filename').set_text('pnm')
findWidget('Dialog-Save Image:filename').set_text('pnm_')
findWidget('Dialog-Save Image:filename').set_text('pnm_i')
findWidget('Dialog-Save Image:filename').set_text('pnm_im')
findWidget('Dialog-Save Image:filename').set_text('pnm_ima')
findWidget('Dialog-Save Image:filename').set_text('pnm_imag')
findWidget('Dialog-Save Image:filename').set_text('pnm_image')
findWidget('Dialog-Save Image').resize(198, 123)
setComboBox(findWidget('Dialog-Save Image:format'), 'pnm')
findWidget('Dialog-Save Image:gtk-ok').clicked()
checkpoint OOF.File.Save.Image
findWidget('OOF3D:Image Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Image
findWidget('Dialog-Save Image').resize(190, 123)
findWidget('Dialog-Save Image:filename').set_text('')
findWidget('Dialog-Save Image:filename').set_text('p')
findWidget('Dialog-Save Image:filename').set_text('ps')
findWidget('Dialog-Save Image:filename').set_text('ps_')
findWidget('Dialog-Save Image:filename').set_text('ps_i')
findWidget('Dialog-Save Image:filename').set_text('ps_im')
findWidget('Dialog-Save Image:filename').set_text('ps_ima')
findWidget('Dialog-Save Image:filename').set_text('ps_imag')
findWidget('Dialog-Save Image:filename').set_text('ps_image')
findWidget('Dialog-Save Image').resize(198, 123)
setComboBox(findWidget('Dialog-Save Image:format'), 'ps')
findWidget('Dialog-Save Image:gtk-ok').clicked()
checkpoint OOF.File.Save.Image
findWidget('OOF3D:Image Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Image
findWidget('Dialog-Save Image').resize(190, 123)
findWidget('Dialog-Save Image:filename').set_text('')
findWidget('Dialog-Save Image:filename').set_text('t')
findWidget('Dialog-Save Image:filename').set_text('ti')
findWidget('Dialog-Save Image:filename').set_text('tif')
findWidget('Dialog-Save Image:filename').set_text('tiff')
findWidget('Dialog-Save Image:filename').set_text('tiff_')
findWidget('Dialog-Save Image:filename').set_text('tiff_i')
findWidget('Dialog-Save Image:filename').set_text('tiff_im')
findWidget('Dialog-Save Image:filename').set_text('tiff_ima')
findWidget('Dialog-Save Image:filename').set_text('tiff_imag')
findWidget('Dialog-Save Image:filename').set_text('tiff_image')
findWidget('Dialog-Save Image').resize(198, 123)
setComboBox(findWidget('Dialog-Save Image:format'), 'tiff')
findWidget('Dialog-Save Image:gtk-ok').clicked()
checkpoint OOF.File.Save.Image
findWidget('OOF3D:Image Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint microstructure page sensitized
checkpoint Field page sensitized
##checkpoint skeleton page sensitized
checkpoint OOF.Image.Delete
findWidget('OOF3D:Image Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint microstructure page sensitized
checkpoint Field page sensitized
##checkpoint skeleton page sensitized
checkpoint OOF.Image.Delete
assert tests.sensitization6()
assert tests.chooserCheck('OOF3D:Image Page:Image', [])
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('image.log')
findWidget('Dialog-Python_Log').resize(198, 95)
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('image.log')
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
