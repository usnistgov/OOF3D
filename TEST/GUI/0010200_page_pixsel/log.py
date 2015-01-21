checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:05 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Pixel Selection')
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
assert tests.sensitization0()
assert tests.pixelSelectionPageNoMSCheck()
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
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
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/c')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/co')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/com')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/comp')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/compo')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/compos')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/composi')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/composit')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/compositi')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/compositio')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/composition')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/composition.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/composition.p')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/composition.pn')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/composition.png')
findWidget('Dialog-Load Image and create Microstructure:width:Auto').clicked()
findWidget('Dialog-Load Image and create Microstructure:width:Text').set_text('1')
findWidget('Dialog-Load Image and create Microstructure:width:Text').set_text('1.')
findWidget('Dialog-Load Image and create Microstructure:width:Text').set_text('1.0')
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
checkpoint interface page updated
checkpoint OOF.Microstructure.Create_From_ImageFile
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
checkpoint OOF.Windows.Graphics.New
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Pixel Selection')
assert tests.pixelSelectionPageStatusCheck(0, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 0)
assert tests.sensitization1()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
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
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.3043478260870e-02,y=-2.2391304347826e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.3043478260870e-02,y=-2.2391304347826e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Messages 1').resize(548, 200)
findWidget('OOF2:Pixel Selection Page:Pane').set_position(281)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.pixelSelectionPageStatusCheck(1938, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 1938)
assert tests.sensitization2()
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2').resize(593, 350)
findWidget('OOF2:Image Page:Pane').set_position(380)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(165)
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new pixel group
findWidget('Dialog-Create new pixel group').resize(249, 72)
findWidget('Dialog-Create new pixel group:name:Auto').clicked()
findWidget('Dialog-Create new pixel group:name:Text').set_text('l')
findWidget('Dialog-Create new pixel group:name:Text').set_text('lo')
findWidget('Dialog-Create new pixel group:name:Text').set_text('low')
findWidget('Dialog-Create new pixel group:name:Text').set_text('lowe')
findWidget('Dialog-Create new pixel group:name:Text').set_text('lower')
findWidget('Dialog-Create new pixel group:name:Text').set_text('lowerl')
findWidget('Dialog-Create new pixel group:name:Text').set_text('lowerle')
findWidget('Dialog-Create new pixel group:name:Text').set_text('lowerlef')
findWidget('Dialog-Create new pixel group:name:Text').set_text('lowerleft')
findWidget('Dialog-Create new pixel group:gtk-ok').clicked()
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New
checkpoint meshable button set
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:Add').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Pixel Selection')
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint OOF.PixelSelection.Invert
assert tests.pixelSelectionPageStatusCheck(8062, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 8062)
assert tests.sensitization2()
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint selection info updated
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint OOF.PixelSelection.Undo
assert tests.pixelSelectionPageStatusCheck(1938, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 1938)
assert tests.sensitization3()
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Clear').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint OOF.PixelSelection.Clear
assert tests.pixelSelectionPageStatusCheck(0, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 0)
assert tests.sensitization4()
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Select Group')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint OOF.PixelSelection.Select_Group
assert tests.pixelSelectionPageStatusCheck(1938, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 1938)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.6739130434783e-01,y=-9.2826086956522e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.6739130434783e-01,y=-9.2826086956522e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new pixel group
findWidget('Dialog-Create new pixel group').resize(249, 72)
findWidget('Dialog-Create new pixel group:name:Text').set_text('')
findWidget('Dialog-Create new pixel group:name:Text').set_text('u')
findWidget('Dialog-Create new pixel group:name:Text').set_text('up')
findWidget('Dialog-Create new pixel group:name:Text').set_text('upp')
findWidget('Dialog-Create new pixel group:name:Text').set_text('uppe')
findWidget('Dialog-Create new pixel group:name:Text').set_text('upper')
findWidget('Dialog-Create new pixel group:name:Text').set_text('upperl')
findWidget('Dialog-Create new pixel group:name:Text').set_text('upperle')
findWidget('Dialog-Create new pixel group:name:Text').set_text('upperlef')
findWidget('Dialog-Create new pixel group:name:Text').set_text('upperleft')
findWidget('Dialog-Create new pixel group:gtk-ok').clicked()
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint OOF.PixelGroup.New
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:Add').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Pixel Selection')
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint OOF.PixelSelection.Select_Group
assert tests.pixelSelectionPageStatusCheck(1938, 10000)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Add Group')
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Add Group:group'), 'upperleft')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint OOF.PixelSelection.Add_Group
assert tests.pixelSelectionPageStatusCheck(3060, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 3060)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Unselect Group')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint OOF.PixelSelection.Unselect_Group
assert tests.pixelSelectionPageStatusCheck(1122, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 1122)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Chooser'), 'Rectangle')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9782608695652e-01,y=-5.8043478260870e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0217391304348e-01,y=-5.6304347826087e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0652173913043e-01,y=-5.3260869565217e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1086956521739e-01,y=-5.1086956521739e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1956521739130e-01,y=-4.8478260869565e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2391304347826e-01,y=-4.4565217391304e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5000000000000e-01,y=-4.0217391304348e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7608695652174e-01,y=-3.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0217391304348e-01,y=-3.2826086956522e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2826086956522e-01,y=-2.9347826086957e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.5000000000000e-01,y=-2.6739130434783e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6304347826087e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.7173913043478e-01,y=-2.5000000000000e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8043478260870e-01,y=-2.5000000000000e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.9782608695652e-01,y=-2.4565217391304e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.1521739130435e-01,y=-2.4565217391304e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2826086956522e-01,y=-2.4565217391304e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5000000000000e-01,y=-2.5000000000000e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7173913043478e-01,y=-2.5434782608696e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.9347826086957e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1086956521739e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3260869565217e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.4565217391304e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8478260869565e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1521739130435e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1956521739130e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4130434782609e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5000000000000e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5434782608696e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6304347826087e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7608695652174e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8478260869565e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9347826086957e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9782608695652e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0217391304348e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0652173913043e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.1086956521739e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.1521739130435e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.1956521739130e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2391304347826e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2826086956522e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.3260869565217e-01,y=-2.5434782608696e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.3260869565217e-01,y=-2.6304347826087e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.3260869565217e-01,y=-2.6304347826087e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Rectangle
assert tests.pixelSelectionSizeCheck('composition.png', 1815)
assert tests.pixelSelectionPageStatusCheck(1815, 10000)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Intersect Group')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint OOF.PixelSelection.Intersect_Group
assert tests.pixelSelectionPageStatusCheck(384, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 384)
assert tests.sensitization5()
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Despeckle')
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Expand')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint OOF.PixelSelection.Expand
assert tests.pixelSelectionPageStatusCheck(472, 10000)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Shrink')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('.0')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('4.0')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint pixel page updated
checkpoint selection info updated
checkpoint OOF.PixelSelection.Shrink
assert tests.pixelSelectionPageStatusCheck(156, 10000)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Color Range')
findWidget('OOF2').resize(593, 532)
findWidget('OOF2:Pixel Selection Page:Pane').set_position(221)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:slider').get_adjustment().set_value( 1.5873015873016e-02)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:slider').get_adjustment().set_value( 3.1746031746032e-02)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:slider').get_adjustment().set_value( 6.8253968253968e-01)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:slider').get_adjustment().set_value( 9.3650793650794e-01)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:slider').get_adjustment().set_value( 9.8412698412698e-01)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_red:slider').get_adjustment().set_value( 1.0000000000000e-02)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_green:slider').get_adjustment().set_value( 1.0000000000000e-02)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_blue:slider').get_adjustment().set_value( 1.0000000000000e-02)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(221)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Color_Range
assert tests.pixelSelectionPageStatusCheck(1428, 10000)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Copy')
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('OOF2:Microstructure Page:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy microstructure
findWidget('Dialog-Copy microstructure').resize(249, 72)
findWidget('Dialog-Copy microstructure:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Pane').set_position(165)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Pane').set_position(165)
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
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
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Microstructure.Copy
checkpoint meshable button set
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Pixel Selection')
assert tests.chooserCheck('OOF2:Pixel Selection Page:Microstructure', ['composition.png', 'microstructure'])
assert tests.chooserStateCheck('OOF2:Pixel Selection Page:Microstructure', 'composition.png')
assert tests.pixelSelectionPageStatusCheck(1428, 10000)
assert tests.pixelSelectionSizeCheck('microstructure', 0)
assert tests.pixelSelectionSizeCheck('composition.png', 1428)
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
setComboBox(findWidget('OOF2:Pixel Selection Page:Microstructure'), 'microstructure')
checkpoint pixel page updated
assert tests.pixelSelectionPageStatusCheck(0, 10000)
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint OOF.PixelSelection.Copy
assert tests.pixelSelectionPageStatusCheck(1428, 10000)
assert tests.pixelSelectionSizeCheck('microstructure', 1428)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
setComboBox(findWidget('OOF2:Skeleton Page:Microstructure'), 'composition.png')
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
checkpoint skeleton page sensitized
findWidget('Dialog-New skeleton').resize(334, 152)
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.New
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Pixel Selection')
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Select Element Pixels')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Skeleton Selection')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6304347826087e-01,y=-6.2826086956522e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6304347826087e-01,y=-6.2826086956522e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Element sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Select_Element_Pixels
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Clear').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Clear
assert tests.pixelSelectionPageStatusCheck(0, 10000)
assert tests.pixelSelectionSizeCheck('microstructure', 0)
assert tests.pixelSelectionSizeCheck('composition.png', 1428)
findWidget('OOF2 Graphics 1').resize(800, 400)
setComboBox(findWidget('OOF2:Pixel Selection Page:Microstructure'), 'composition.png')
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Clear').clicked()
checkpoint pixel page updated
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Clear
assert tests.pixelSelectionPageStatusCheck(0, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 0)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Select_Element_Pixels
assert tests.pixelSelectionPageStatusCheck(625, 10000)
assert tests.pixelSelectionSizeCheck('composition.png', 625)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Element:Clear').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Element').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Segment').clicked()
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5000000000000e-01,y=-3.7173913043478e-01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5000000000000e-01,y=-3.7173913043478e-01,state=257,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0652173913043e-01,y=-2.5000000000000e-01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0652173913043e-01,y=-2.5000000000000e-01,state=257,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
setComboBox(findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Select Segment Pixels')
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Select_Segment_Pixels
assert tests.pixelSelectionSizeCheck('composition.png', 675)
assert tests.pixelSelectionPageStatusCheck(675, 10000)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:Clear').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Clear
assert tests.pixelSelectionSizeCheck('composition.png', 0)
assert tests.pixelSelectionPageStatusCheck(0, 10000)
findWidget('OOF2:Pixel Selection Page:Pane:SelectionModification:OK').clicked()
findWidget('OOF2:Pixel Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Select_Segment_Pixels
assert tests.pixelSelectionSizeCheck('composition.png', 50)
assert tests.pixelSelectionPageStatusCheck(50, 10000)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Segment:Clear').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('OOF2:Microstructure Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(209, 94)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint microstructure page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint boundary page updated
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.Microstructure.Delete
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(209, 94)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('Questioner:gtk-yes').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Pane').set_position(212)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Pane').set_position(162)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint microstructure page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
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
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
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
checkpoint interface page updated
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint skeleton page sensitized
checkpoint OOF.Microstructure.Delete
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('p')
findWidget('Dialog-Python_Log:filename').set_text('pi')
findWidget('Dialog-Python_Log:filename').set_text('pix')
findWidget('Dialog-Python_Log:filename').set_text('pixs')
findWidget('Dialog-Python_Log:filename').set_text('pixse')
findWidget('Dialog-Python_Log:filename').set_text('pixsel')
findWidget('Dialog-Python_Log:filename').set_text('pixsel.')
findWidget('Dialog-Python_Log:filename').set_text('pixsel.l')
findWidget('Dialog-Python_Log:filename').set_text('pixsel.lo')
findWidget('Dialog-Python_Log:filename').set_text('pixsel.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('pixsel.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
