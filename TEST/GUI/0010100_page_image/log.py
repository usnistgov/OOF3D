checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint pixel page updated
checkpoint active area status updated
checkpoint mesh bdy page updated
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint interface page updated
checkpoint OOF.Microstructure.Create_From_ImageFile
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2:Navigation:Next').clicked()
assert tests.sensitization0()
assert tests.chooserCheck('OOF2:Image Page:Microstructure', ['serendipity.png'])
assert tests.chooserCheck('OOF2:Image Page:Image', ['serendipity.png'])
assert tests.chooserStateCheck('OOF2:Image Page:Image', 'serendipity.png')
findWidget('OOF2').resize(593, 350)
findWidget('OOF2:Image Page:Pane').set_position(380)
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Gray
assert tests.sensitization1()
findWidget('OOF2:Image Page:Pane:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Undo
assert tests.sensitization2()
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Flip')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Flip:axis'), 'y')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Flip
assert tests.sensitization3()
findWidget('OOF2:Image Page:Pane:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Undo
assert tests.sensitization4()
findWidget('OOF2:Image Page:Pane:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Undo
assert tests.sensitization5()
findWidget('OOF2:Image Page:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy Image
findWidget('Dialog-Copy Image').resize(309, 101)
findWidget('Dialog-Copy Image:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint OOF.Image.Copy
assert tests.chooserCheck('OOF2:Image Page:Image', ['serendipity.png', 'serendipity.png<2>'])
assert tests.chooserStateCheck('OOF2:Image Page:Image', 'serendipity.png<2>')
findWidget('OOF2:Image Page:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy Image
findWidget('Dialog-Copy Image').resize(309, 101)
findWidget('Dialog-Copy Image:name:Auto').clicked()
findWidget('Dialog-Copy Image:name:Text').set_text('c')
findWidget('Dialog-Copy Image:name:Text').set_text('co')
findWidget('Dialog-Copy Image:name:Text').set_text('cop')
findWidget('Dialog-Copy Image:name:Text').set_text('copy')
findWidget('Dialog-Copy Image:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint OOF.Image.Copy
assert tests.chooserCheck('OOF2:Image Page:Image', ['serendipity.png', 'serendipity.png<2>', 'copy'])
assert tests.chooserStateCheck('OOF2:Image Page:Image', 'copy')
setComboBox(findWidget('OOF2:Image Page:Image'), 'serendipity.png')
setComboBox(findWidget('OOF2:Image Page:Image'), 'serendipity.png<2>')
findWidget('OOF2:Image Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(246, 94)
findWidget('Questioner:gtk-yes').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Image.Delete
assert tests.sensitization5()
assert tests.chooserCheck('OOF2:Image Page:Image', ['serendipity.png', 'copy'])
assert tests.chooserStateCheck('OOF2:Image Page:Image', 'serendipity.png')
findWidget('OOF2:Image Page:Group').clicked()
checkpoint toplevel widget mapped Dialog-AutoGroup
findWidget('Dialog-AutoGroup').resize(211, 72)
findWidget('Dialog-AutoGroup:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint OOF.Image.AutoGroup
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
assert tests.micro_sensitization()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Image Page:Pane').set_position(380)
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Dim')
findWidget('OOF2:Image Page:Pane').set_position(357)
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Dim
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Blur')
findWidget('OOF2:Image Page:Pane').set_position(380)
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Blur
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Contrast')
findWidget('OOF2:Image Page:Pane:Method:Contrast:sharpen').clicked()
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Contrast
findWidget('OOF2:Image Page:Pane:Method:Contrast:sharpen').clicked()
findWidget('OOF2:Image Page:Pane:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Undo
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Contrast
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Despeckle')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Despeckle
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Edge')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Edge
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Enhance')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Enhance
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Equalize')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Equalize
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'MedianFilter')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.MedianFilter
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Negate')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Negate
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Normalize')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Normalize
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'ReduceNoise')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.ReduceNoise
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Sharpen')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Sharpen
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'Reilluminate')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.Reilluminate
setComboBox(findWidget('OOF2:Image Page:Pane:Method:Chooser'), 'ThresholdImage')
findWidget('OOF2:Image Page:Pane:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Image.Modify.ThresholdImage
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('OOF2:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(314, 168)
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Pane').set_position(165)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Microstructure.New
findWidget('OOF2:Navigation:Next').clicked()
assert tests.chooserCheck('OOF2:Image Page:Microstructure', ['serendipity.png', 'microstructure'])
assert tests.chooserStateCheck('OOF2:Image Page:Microstructure', 'serendipity.png')
findWidget('OOF2:Image Page:Pane').set_position(380)
setComboBox(findWidget('OOF2:Image Page:Microstructure'), 'microstructure')
assert tests.chooserStateCheck('OOF2:Image Page:Microstructure', 'microstructure')
assert tests.chooserCheck('OOF2:Image Page:Image', [])
assert tests.sensitization6()
findWidget('OOF2:Image Page:Pane').set_position(380)
setComboBox(findWidget('OOF2:Image Page:Microstructure'), 'serendipity.png')
assert tests.sensitization3()
assert tests.chooserCheck('OOF2:Image Page:Image', ['serendipity.png', 'copy'])
assert tests.chooserStateCheck('OOF2:Image Page:Image', 'serendipity.png')
findWidget('OOF2:Image Page:Pane').set_position(380)
findWidget('OOF2:Image Page:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename Image
findWidget('Dialog-Rename Image').resize(194, 72)
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
assert tests.sensitization3()
assert tests.chooserCheck('OOF2:Image Page:Image', ['renamed', 'copy'])
assert tests.chooserStateCheck('OOF2:Image Page:Image', 'renamed')
findWidget('OOF2:Image Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Image
findWidget('Dialog-Save Image').resize(194, 72)
findWidget('Dialog-Save Image:filename').set_text('i')
findWidget('Dialog-Save Image:filename').set_text('im')
findWidget('Dialog-Save Image:filename').set_text('ima')
findWidget('Dialog-Save Image:filename').set_text('imag')
findWidget('Dialog-Save Image:filename').set_text('image')
findWidget('Dialog-Save Image:filename').set_text('image.')
findWidget('Dialog-Save Image:filename').set_text('image.p')
findWidget('Dialog-Save Image:filename').set_text('image.pp')
findWidget('Dialog-Save Image:filename').set_text('image.ppm')
findWidget('Dialog-Save Image:gtk-ok').clicked()
checkpoint OOF.File.Save.Image
# This test has been removed because the exact final image can depend
# upon which version of ImageMagick is being used.
## assert tests.filediff('image.ppm')
findWidget('OOF2:Image Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-yes').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Image.Delete
findWidget('OOF2:Image Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-yes').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Image Page:Pane').set_position(380)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Image.Delete
assert tests.sensitization6()
assert tests.chooserCheck('OOF2:Image Page:Image', [])
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('i')
findWidget('Dialog-Python_Log:filename').set_text('im')
findWidget('Dialog-Python_Log:filename').set_text('ima')
findWidget('Dialog-Python_Log:filename').set_text('imag')
findWidget('Dialog-Python_Log:filename').set_text('image')
findWidget('Dialog-Python_Log:filename').set_text('image.')
findWidget('Dialog-Python_Log:filename').set_text('image.l')
findWidget('Dialog-Python_Log:filename').set_text('image.lo')
findWidget('Dialog-Python_Log:filename').set_text('image.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('image.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
