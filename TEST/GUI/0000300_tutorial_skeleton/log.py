checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:23 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

## This is more-or-less the skeleton tutorial.  The conditional
## iterations for the Anneal steps have been changed to unconditional
## ones, because round-off error makes conditional iteration
## unportable.

findMenu(findWidget('OOF2:MenuBar'), 'Help:Tutorials').activate()
findMenu(findWidget('OOF2:MenuBar'), 'Help:Tutorials').activate()
findMenu(findWidget('OOF2:MenuBar'), 'Help:Tutorials:Skeleton').activate()
checkpoint toplevel widget mapped Skeleton
findWidget('Skeleton').resize(500, 300)
findWidget('Skeleton:Next').clicked()
findWidget('Skeleton').resize(500, 300)
findWidget('Skeleton').resize(502, 303)
findWidget('Skeleton').resize(515, 342)
findWidget('Skeleton').resize(535, 391)
findWidget('Skeleton').resize(574, 468)
findWidget('Skeleton').resize(574, 467)
findWidget('Skeleton').resize(574, 466)
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(150)
findWidget('OOF2:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(342, 144)
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('..')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../..')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../e')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../ex')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../exa')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../exam')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examp')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../exampl')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../example')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/s')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/sm')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/sma')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/smal')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small.p')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small.pp')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small.ppm')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
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
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(593, 350)
findWidget('OOF2:Image Page:Pane').set_position(380)
findWidget('OOF2:Image Page:Group').clicked()
checkpoint toplevel widget mapped Dialog-AutoGroup
findWidget('Dialog-AutoGroup').resize(211, 72)
findWidget('Dialog-AutoGroup:gtk-ok').clicked()
findWidget('OOF2 Activity Viewer').resize(400, 300)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint OOF.Image.AutoGroup
findWidget('OOF2').resize(593, 350)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('Skeleton:Next').clicked()
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton page sensitized
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:name:Auto').clicked()
findWidget('Dialog-New skeleton:name:Text').set_text('b')
findWidget('Dialog-New skeleton:name:Text').set_text('bo')
findWidget('Dialog-New skeleton:name:Text').set_text('bon')
findWidget('Dialog-New skeleton:name:Text').set_text('bone')
findWidget('Dialog-New skeleton:name:Text').set_text('bones')
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton page sensitized
checkpoint mesh bdy page updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
assert tests.skeletonSizeCheck('small.ppm:bones', 16, 25)
findWidget('Skeleton:Next').clicked()
findMenu(findWidget('Skeleton:MenuBar'), 'Windows:Graphics:New').activate()
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
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2').resize(593, 434)
findWidget('Skeleton:Next').clicked()
findWidget('Skeleton').resize(574, 466)
findWidget('Skeleton').resize(574, 471)
findWidget('Skeleton').resize(574, 488)
findWidget('Skeleton').resize(577, 518)
findWidget('Skeleton').resize(585, 563)
findWidget('Skeleton').resize(587, 581)
findWidget('Skeleton').resize(587, 582)
findWidget('Skeleton').resize(588, 589)
findWidget('Skeleton').resize(591, 601)
findWidget('Skeleton').resize(592, 605)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Heterogeneous Elements:threshold:slider').get_adjustment().set_value( 9.2063492063492e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Heterogeneous Elements:threshold:slider').get_adjustment().set_value( 9.3650793650794e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Heterogeneous Elements:threshold:slider').get_adjustment().set_value( 9.8412698412698e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Heterogeneous Elements:threshold:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:alpha:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:alpha:entry').set_text('0.5')
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
assert tests.skeletonSizeCheck('small.ppm:bones', 140, 163)
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Skeleton Page:Pane:Modification:Undo').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Undo
assert tests.skeletonSizeCheck('small.ppm:bones', 16, 25)
findWidget('OOF2:Skeleton Page:Pane:Modification:Redo').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Redo
assert tests.skeletonSizeCheck('small.ppm:bones', 140, 163)
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Heterogeneous Elements:threshold:entry').set_text('')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Heterogeneous Elements:threshold:entry').set_text('0')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Heterogeneous Elements:threshold:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Heterogeneous Elements:threshold:entry').set_text('0.9')
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
assert tests.skeletonSizeCheck('small.ppm:bones', 777, 815)
findWidget('Skeleton:Next').clicked()
findWidget('Skeleton:Next').clicked()
findWidget('Skeleton:Next').clicked()
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Snap Nodes')
findWidget('OOF2:Skeleton Page:Pane').set_position(273)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:targets:Chooser'), 'Heterogeneous Elements')
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('Skeleton:Next').clicked()
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 5.1724137931034e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 5.5172413793103e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 6.5517241379310e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 7.5862068965517e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 8.7356321839080e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Merge Triangles')
findWidget('OOF2:Skeleton Page:Pane').set_position(273)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Rationalize')
findWidget('OOF2').resize(618, 581)
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
checkpoint skeleton page sensitized
findWidget('Skeleton').resize(592, 605)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Average Energy:alpha:entry').set_text('')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Average Energy:alpha:entry').set_text('0')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Average Energy:alpha:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Average Energy:alpha:entry').set_text('0.8')
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementAction:Chooser'), 'Select by Homogeneity')
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.ElementSelection.Select_by_Homogeneity
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.ElementSelection.Select_by_Homogeneity
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(301)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Split Quads')
findWidget('OOF2:Skeleton Page:Pane').set_position(290)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Split Quads:targets:Chooser'), 'Selected Elements')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Split Quads:criterion:Average Energy:alpha:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Split Quads:criterion:Average Energy:alpha:entry').set_text('0.9')
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(301)
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.ElementSelection.Select_by_Homogeneity
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Skeleton:Next').clicked()
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Anneal')
findWidget('OOF2:Skeleton Page:Pane').set_position(298)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:criterion:Average Energy:alpha:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:criterion:Average Energy:alpha:entry').set_text('0.9')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:iteration:Fixed Iterations:iterations').set_text('10')
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Messages 1').resize(571, 200)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('OOF2:Skeleton Page:Pane:Modification:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Undo
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:targets:Chooser'), 'Selected Nodes')
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:targets:Chooser'), 'Selected Elements')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 8.9000000000000e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:criterion:Average Energy:alpha:entry').set_text('0.8')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:criterion:Average Energy:alpha:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Anneal:criterion:Average Energy:alpha:entry').set_text('0.9')
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(301)
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.ElementSelection.Select_by_Homogeneity
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:Prev').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:Prev').clicked()
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(301)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
findWidget('OOF2:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(137)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(301)
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.ElementSelection.Select_by_Homogeneity
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementAction:Select by Homogeneity:threshold:entry').set_text('0.')
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementAction:Select by Homogeneity:threshold:entry').set_text('0.8')
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(290)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.ElementSelection.Select_by_Homogeneity
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(301)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(301)
setComboBox(findWidget('OOF2:Pin Nodes Page:Pane:Modify:Method:Chooser'), 'Pin Internal Boundary Nodes')
findWidget('OOF2:Pin Nodes Page:Pane:Modify:OK').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(301)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.PinNodes.Pin_Internal_Boundary_Nodes
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Skeleton:Next').clicked()
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(105)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Swap Edges')
findWidget('OOF2:Skeleton Page:Pane').set_position(298)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Swap Edges:criterion:Average Energy:alpha:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Swap Edges:criterion:Average Energy:alpha:entry').set_text('0.5')
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2').resize(618, 558)
findWidget('OOF2:Skeleton Page:Pane').set_position(298)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2').resize(620, 539)
findWidget('OOF2').resize(623, 510)
findWidget('OOF2').resize(623, 484)
findWidget('OOF2').resize(623, 458)
findWidget('OOF2').resize(623, 431)
findWidget('OOF2').resize(623, 420)
findWidget('OOF2').resize(623, 419)
findWidget('OOF2').resize(623, 418)
findWidget('OOF2').resize(623, 415)
findWidget('OOF2').resize(623, 412)
findWidget('OOF2').resize(623, 411)
findWidget('OOF2:Skeleton Page:Pane').set_position(303)
findWidget('OOF2').resize(623, 410)
findWidget('OOF2:Skeleton Page:Pane').set_position(303)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2').resize(624, 410)
findWidget('OOF2:Skeleton Page:Pane').set_position(304)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('OOF2:Skeleton Page:Pane:Modification:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Undo
findWidget('OOF2:Skeleton Page:Pane:Modification:Redo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Redo
findWidget('OOF2:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF2').resize(624, 581)
findWidget('OOF2:Skeleton Page:Pane').set_position(111)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Merge Triangles')
findWidget('OOF2:Skeleton Page:Pane').set_position(304)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Merge Triangles:criterion:Chooser'), 'Limited Unconditional')
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Merge Triangles:criterion:Limited Unconditional:shape_energy:slider').get_adjustment().set_value( 3.9682539682540e-01)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Merge Triangles:criterion:Limited Unconditional:alpha:entry').set_text('')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Merge Triangles:criterion:Limited Unconditional:alpha:entry').set_text('0')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Merge Triangles:criterion:Limited Unconditional:alpha:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Merge Triangles:criterion:Limited Unconditional:alpha:entry').set_text('0.5')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Merge Triangles:criterion:Limited Unconditional:shape_energy:entry').set_text('0.')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Merge Triangles:criterion:Limited Unconditional:shape_energy:entry').set_text('0.4')
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Messages 1').resize(589, 200)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('OOF2').resize(624, 577)
findWidget('OOF2').resize(624, 574)
findWidget('OOF2').resize(624, 562)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2').resize(624, 544)
findWidget('OOF2').resize(624, 525)
findWidget('OOF2').resize(624, 492)
findWidget('OOF2').resize(624, 478)
findWidget('OOF2').resize(624, 468)
findWidget('OOF2').resize(624, 441)
findWidget('OOF2').resize(624, 420)
findWidget('OOF2').resize(624, 411)
findWidget('OOF2').resize(624, 403)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2').resize(624, 402)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2').resize(624, 401)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2').resize(624, 400)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2').resize(624, 399)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2').resize(624, 398)
findWidget('OOF2').resize(625, 398)
findWidget('OOF2:Skeleton Page:Pane').set_position(250)
findWidget('OOF2:Skeleton Page:Pane:Modification:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Undo
findWidget('OOF2:Skeleton Page:Pane:Modification:Redo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Redo
findWidget('Skeleton:Next').clicked()
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Smooth')
findWidget('OOF2').resize(625, 430)
findWidget('OOF2:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Smooth:criterion:Chooser'), 'Limited Unconditional')
findWidget('OOF2').resize(625, 478)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane').set_position(250)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Messages 1').resize(806, 200)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
findWidget('Skeleton:Next').clicked()
findWidget('Skeleton:Next').clicked()
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Skeleton').activate()
checkpoint toplevel widget mapped Dialog-Skeleton
findWidget('Dialog-Skeleton').resize(194, 160)
findWidget('Dialog-Skeleton:filename').set_text('s')
findWidget('Dialog-Skeleton:filename').set_text('sk')
findWidget('Dialog-Skeleton:filename').set_text('ske')
findWidget('Dialog-Skeleton:filename').set_text('skel')
findWidget('Dialog-Skeleton:filename').set_text('skele')
findWidget('Dialog-Skeleton:filename').set_text('skelet')
findWidget('Dialog-Skeleton:filename').set_text('skeleto')
findWidget('Dialog-Skeleton:filename').set_text('skeleton')
findWidget('Dialog-Skeleton:filename').set_text('skeleton.')
findWidget('Dialog-Skeleton:filename').set_text('skeleton.d')
findWidget('Dialog-Skeleton:filename').set_text('skeleton.da')
findWidget('Dialog-Skeleton:filename').set_text('skeleton.dat')
findWidget('Dialog-Skeleton:gtk-ok').clicked()
checkpoint OOF.File.Save.Skeleton
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('s')
findWidget('Dialog-Python_Log:filename').set_text('sk')
findWidget('Dialog-Python_Log:filename').set_text('ske')
findWidget('Dialog-Python_Log:filename').set_text('skel')
findWidget('Dialog-Python_Log:filename').set_text('skelt')
findWidget('Dialog-Python_Log:filename').set_text('skeltu')
findWidget('Dialog-Python_Log:filename').set_text('skeltut')
findWidget('Dialog-Python_Log:filename').set_text('skeltut.')
findWidget('Dialog-Python_Log:filename').set_text('skeltut.l')
findWidget('Dialog-Python_Log:filename').set_text('skeltut.lo')
findWidget('Dialog-Python_Log:filename').set_text('skeltut.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('skeltut.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
