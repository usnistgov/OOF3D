checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:07 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
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
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/k')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_s')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_sm')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_sma')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_smam')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_sma')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_smal')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_small')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_small;')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_small')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_small.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_small.p')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_small.pg')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/K1_small.pgm')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint mesh bdy page updated
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
checkpoint OOF.Microstructure.Create_From_ImageFile
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
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
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Pixel Selection')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Chooser'), 'Burn')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 1.7460317460317e-01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 1.5873015873016e-01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 1.4285714285714e-01)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.4065217391304e+01,y=-4.8071739130435e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.4065217391304e+01,y=-4.8071739130435e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.9317391304348e+01,y=-4.7676086956522e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.9317391304348e+01,y=-4.8071739130435e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.9317391304348e+01,y=-4.8071739130435e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Pixel Selection')
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Despeckle')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Despeckle
assert tests.pixelSelectionPageStatusCheck(177, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 7.9428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 7.8285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 7.7714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 7.6000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 7.5428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 7.4857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 7.4285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint pixel page updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Despeckle
assert tests.pixelSelectionPageStatusCheck(177, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.9714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.9142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.8571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.8000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Despeckle
assert tests.pixelSelectionPageStatusCheck(177, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.7428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.6857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.6285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.5714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.5142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.4571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.4000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.3428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.2857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.2285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.1714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.1142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.0571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 6.0000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.9428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.8857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.8285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.7714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.7142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Despeckle
assert tests.pixelSelectionPageStatusCheck(178, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.5428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.4857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.4285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.3714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.3142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.2571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.2000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.1428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.0857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 5.0285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.9714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.9142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.8571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Despeckle
assert tests.pixelSelectionPageStatusCheck(492, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.7428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.6857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.4000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.2285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.0571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 4.0000000000000e+00)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(273)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(296)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(316)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(318)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(319)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(320)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(327)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(330)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(331)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(333)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(333)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(334)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(335)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:local_flammability:slider').get_adjustment().set_value( 7.5757575757576e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:local_flammability:slider').get_adjustment().set_value( 6.0606060606061e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:local_flammability:slider').get_adjustment().set_value( 4.5454545454545e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:local_flammability:slider').get_adjustment().set_value( 3.0303030303030e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 1.2121212121212e-01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 1.0606060606061e-01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 9.0909090909091e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 7.5757575757576e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 6.0606060606061e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 4.5454545454545e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 3.0303030303030e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 1.5151515151515e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 3.0303030303030e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 4.5454545454545e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 3.0303030303030e-02)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.1186956521739e+01,y=-5.2028260869565e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.1186956521739e+01,y=-5.2028260869565e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
assert tests.pixelSelectionPageStatusCheck(1, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0108695652174e+01,y=-4.6489130434783e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0108695652174e+01,y=-4.6489130434783e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
assert tests.pixelSelectionPageStatusCheck(1, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4569565217391e+01,y=-4.1741304347826e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4569565217391e+01,y=-4.1741304347826e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
assert tests.pixelSelectionPageStatusCheck(1, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 3.1303000000000e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 3.2303000000000e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 3.3303000000000e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:global_flammability:slider').get_adjustment().set_value( 3.4303000000000e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:local_flammability:slider').get_adjustment().set_value( 3.1303000000000e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:local_flammability:slider').get_adjustment().set_value( 3.2303000000000e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:local_flammability:slider').get_adjustment().set_value( 3.3303000000000e-02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Burn:local_flammability:slider').get_adjustment().set_value( 3.4303000000000e-02)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3778260869565e+01,y=-3.8180434782609e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.4173913043478e+01,y=-3.7389130434783e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4173913043478e+01,y=-3.7389130434783e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
assert tests.pixelSelectionPageStatusCheck(28, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1404347826087e+01,y=-3.7389130434783e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1404347826087e+01,y=-3.7389130434783e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
assert tests.pixelSelectionPageStatusCheck(1, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.9713043478261e+01,y=-4.6093478260870e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.9713043478261e+01,y=-4.6093478260870e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
assert tests.pixelSelectionPageStatusCheck(1, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8921739130435e+01,y=-4.0554347826087e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8921739130435e+01,y=-4.0554347826087e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.pixelSelectionPageStatusCheck(10, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Elkcepsed')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.pixelSelectionPageStatusCheck(4, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Undo').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Undo
assert tests.pixelSelectionPageStatusCheck(10, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.pixelSelectionPageStatusCheck(10, 8372)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.0142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.0571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.1428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.2285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.2714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.3142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.4000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.4428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.4857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.5714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.6571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.7857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.8285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.9142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 4.0000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.pixelSelectionPageStatusCheck(0, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Undo').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Undo
assert tests.pixelSelectionPageStatusCheck(10, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.9571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.8714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.8285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.7857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.7428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.6142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.4857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.0571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 3.0142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.9714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.9285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.7571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.6714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.5857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.5428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.5000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.4571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.pixelSelectionPageStatusCheck(8, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Undo').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Undo
assert tests.pixelSelectionPageStatusCheck(10, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.4142857142857e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.3714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.3285714285714e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.2857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 2.2000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.9857142857143e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.9000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.5571428571429e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.3428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.1714285714286e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.0428571428571e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.pixelSelectionPageStatusCheck(10, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.PixelSelection.Undo
assert tests.pixelSelectionPageStatusCheck(10, 8372)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(358, 94)
findWidget('Questioner:gtk-delete').clicked()
