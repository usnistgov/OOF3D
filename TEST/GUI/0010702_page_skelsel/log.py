checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:29 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

## The "skeleton selection page grouplist" checkpoint was added by
## hand after this test was recorded, and is probably not present
## everywhere it ought to be.

import tests
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
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(150)
findWidget('OOF2:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(314, 168)
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
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
checkpoint OOF.Microstructure.New
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
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
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page updated
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(265)
findWidget('OOF2:Skeleton Selection Page:Mode:Segment').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page updated
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
assert tests.sgmtSelectionCheck([])
assert tests.sensitization0()
assert tests.selectionSizeCheck(0)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Skeleton Selection')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8043478260870e-01,y=-5.4565217391304e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8043478260870e-01,y=-5.4565217391304e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Messages 1').resize(553, 200)
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.5869565217391e-01,y=-5.7173913043478e-01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.5869565217391e-01,y=-5.7173913043478e-01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_from_Selected_Elements
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.selectionSizeCheck(6)
assert tests.sensitization1()
assert tests.sgmtSelectionCheck([[11, 12], [11, 16], [12, 13], [13, 18], [16, 17], [17, 18]])
assert tests.groupCheck([])
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(249, 72)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
findWidget('Dialog-Create a new Segment group:name:Auto').clicked()
findWidget('Dialog-Create a new Segment group:name:Text').set_text('l')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('lo')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('loo')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('loop')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('loop ')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('loop g')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('loop gr')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('loop gro')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('loop groo')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('loop groop')
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
assert tests.sensitization2()
assert tests.groupCheck(['loop groop (0 segments)'])
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:Add').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
assert tests.groupCheck(['loop groop (6 segments)'])
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select from Selected Elements:internal').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentSelection.Select_from_Selected_Elements
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.selectionSizeCheck(7)
assert tests.sgmtSelectionCheck([[11, 12], [11, 16], [12, 13], [12, 17], [13, 18], [16, 17], [17, 18]])
assert tests.sensitization3()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select from Selected Elements:boundary').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_from_Selected_Elements
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.selectionSizeCheck(1)
assert tests.sgmtSelectionCheck([[12, 17]])
assert tests.sensitization3()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.selectionSizeCheck(7)
assert tests.sgmtSelectionCheck([[11, 12], [11, 16], [12, 13], [12, 17], [13, 18], [16, 17], [17, 18]])
assert tests.sensitization4()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:Clear').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Clear
assert tests.selectionSizeCheck(0)
assert tests.sgmtSelectionCheck([])
assert tests.sensitization5()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Select Internal Boundary Segments')
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:New').activate()
checkpoint layereditor layerset changed
checkpoint toplevel widget mapped OOF2 Graphics Layer Editor
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.New
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
setComboBox(findWidget('OOF2 Graphics Layer Editor:ObjectScroll:category'), 'Microstructure')
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.DisplayedObject
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Microstructure microstructure
findWidget('Dialog-New Display Method for Microstructure microstructure').resize(381, 320)
findWidget('Dialog-New Display Method for Microstructure microstructure:method:Material:no_material:Gray:Gray:slider').get_adjustment().set_value( 3.1746031746032e-02)
findWidget('Dialog-New Display Method for Microstructure microstructure:method:Material:no_material:Gray:Gray:slider').get_adjustment().set_value( 9.5238095238095e-02)
findWidget('Dialog-New Display Method for Microstructure microstructure:method:Material:no_material:Gray:Gray:slider').get_adjustment().set_value( 2.3809523809524e-01)
findWidget('Dialog-New Display Method for Microstructure microstructure:method:Material:no_material:Gray:Gray:slider').get_adjustment().set_value( 3.8095238095238e-01)
findWidget('Dialog-New Display Method for Microstructure microstructure:method:Material:no_material:Gray:Gray:slider').get_adjustment().set_value( 5.7142857142857e-01)
findWidget('Dialog-New Display Method for Microstructure microstructure:method:Material:no_material:Gray:Gray:slider').get_adjustment().set_value( 6.5079365079365e-01)
findWidget('Dialog-New Display Method for Microstructure microstructure:method:Material:no_material:Gray:Gray:slider').get_adjustment().set_value( 8.2539682539683e-01)
findWidget('Dialog-New Display Method for Microstructure microstructure:method:Material:no_material:Gray:Gray:slider').get_adjustment().set_value( 8.4126984126984e-01)
findWidget('Dialog-New Display Method for Microstructure microstructure:gtk-ok').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Element sensitized
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Add_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics Layer Editor').destroy()
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
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:Method:Chooser'), 'Rectangle')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1739130434783e-03,y=-9.7608695652174e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1739130434783e-03,y=-9.7173913043478e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1739130434783e-03,y=-9.6739130434783e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8260869565217e-02,y=-9.1956521739130e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0000000000000e-02,y=-8.8043478260870e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.4782608695652e-02,y=-8.2826086956522e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3260869565217e-01,y=-7.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9782608695652e-01,y=-6.8478260869565e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.6739130434783e-01,y=-6.0217391304348e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2391304347826e-01,y=-5.4130434782609e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8043478260870e-01,y=-4.9347826086957e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2391304347826e-01,y=-4.5000000000000e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5000000000000e-01,y=-4.1521739130435e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6739130434783e-01,y=-3.9782608695652e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0217391304348e-01,y=-3.7608695652174e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1521739130435e-01,y=-3.6739130434783e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1956521739130e-01,y=-3.6304347826087e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2826086956522e-01,y=-3.7608695652174e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3260869565217e-01,y=-3.7608695652174e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.4130434782609e-01,y=-3.6739130434783e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5869565217391e-01,y=-3.6304347826087e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8043478260870e-01,y=-3.5000000000000e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9782608695652e-01,y=-3.4130434782609e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2826086956522e-01,y=-3.1956521739130e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6304347826087e-01,y=-2.8913043478261e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9347826086957e-01,y=-2.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2826086956522e-01,y=-2.2826086956522e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.7608695652174e-01,y=-1.9347826086957e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8478260869565e-01,y=-1.8913043478261e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8913043478261e-01,y=-1.8913043478261e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9347826086957e-01,y=-1.8913043478261e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8913043478261e-01,y=-1.8913043478261e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8913043478261e-01,y=-1.9347826086957e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8478260869565e-01,y=-1.9347826086957e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8478260869565e-01,y=-1.9782608695652e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8478260869565e-01,y=-2.0217391304348e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8478260869565e-01,y=-2.0652173913043e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8478260869565e-01,y=-2.1086956521739e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8478260869565e-01,y=-2.1521739130435e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8478260869565e-01,y=-2.1956521739130e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.8478260869565e-01,y=-2.1956521739130e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Rectangle
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
findWidget('OOF2').resize(684, 434)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material material to pixels
findWidget('Dialog-Assign material material to pixels').resize(268, 108)
findWidget('Dialog-Assign material material to pixels:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Material.Assign
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_Internal_Boundary_Segments
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
assert tests.sgmtSelectionCheck([[5, 6], [6, 7], [7, 8], [8, 13], [13, 18], [18, 23]])
assert tests.selectionSizeCheck(6)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Select Group')
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentSelection.Select_Group
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.sgmtSelectionCheck([[11, 12], [11, 16], [12, 13], [13, 18], [16, 17], [17, 18]])
assert tests.selectionSizeCheck(6)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:Undo').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Undo
assert tests.sgmtSelectionCheck([[5, 6], [6, 7], [7, 8], [8, 13], [13, 18], [18, 23]])
assert tests.selectionSizeCheck(6)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:Add').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
assert tests.groupCheck(['loop groop (11 segments)'])
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_Group
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.sgmtSelectionCheck([[5, 6], [6, 7], [7, 8], [8, 13], [11, 12], [11, 16], [12, 13], [13, 18], [16, 17], [17, 18], [18, 23]])
assert tests.selectionSizeCheck(11)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Select by Homogeneity')
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_by_Homogeneity
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.sgmtSelectionCheck([[0, 5], [1, 6], [2, 7], [3, 8], [8, 9], [13, 14], [18, 19], [23, 24]])
assert tests.selectionSizeCheck(8)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.9090909090909e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.8484848484848e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.7272727272727e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.6666666666667e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.5454545454545e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.4848484848485e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.3636363636364e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.3030303030303e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.1212121212121e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.0606060606061e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 8.0000000000000e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 7.8787878787879e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 7.8181818181818e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 7.7575757575758e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 7.6969696969697e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 7.6363636363636e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 7.5757575757576e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 7.5151515151515e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select by Homogeneity:threshold:slider').get_adjustment().set_value( 7.4545454545455e-01)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_by_Homogeneity
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
assert tests.sgmtSelectionCheck([])
assert tests.selectionSizeCheck(0)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:Invert').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Invert
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.selectionSizeCheck(40)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Unselect Group')
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Unselect_Group
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
assert tests.selectionSizeCheck(29)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Add Group')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Skeleton Selection')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Element').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Segment').clicked()
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Segment:Clear').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
assert tests.selectionSizeCheck(0)
assert tests.sgmtSelectionCheck([])
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7173913043478e-01,y=-2.4565217391304e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7173913043478e-01,y=-2.4565217391304e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7173913043478e-01,y=-2.4565217391304e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7173913043478e-01,y=-2.4565217391304e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.selectionSizeCheck(1)
assert tests.sgmtSelectionCheck([[5,6]])
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.SegmentSelection.Add_Group
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.sgmtSelectionCheck([[5, 6], [6, 7], [7, 8], [8, 13], [11, 12], [11, 16], [12, 13], [13, 18], [16, 17], [17, 18], [18, 23]])
assert tests.selectionSizeCheck(11)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4565217391304e-01,y=-1.2826086956522e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4565217391304e-01,y=-1.2826086956522e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.sgmtSelectionCheck([[1,6]])
assert tests.selectionSizeCheck(1)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.SegmentSelection.Add_Group
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.sgmtSelectionCheck([[1, 6], [5, 6], [6, 7], [7, 8], [8, 13], [11, 12], [11, 16], [12, 13], [13, 18], [16, 17], [17, 18], [18, 23]])
assert tests.selectionSizeCheck(12)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Intersect Group')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Segment:Clear').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
assert tests.sgmtSelectionCheck([])
assert tests.selectionSizeCheck(0)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.2391304347826e-01,y=-2.5434782608696e-01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2391304347826e-01,y=-2.5434782608696e-01,state=257,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
assert tests.sgmtSelectionCheck([[5,6]])
assert tests.selectionSizeCheck(1)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0217391304348e-01,y=-2.4130434782609e-01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0217391304348e-01,y=-2.4130434782609e-01,state=257,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint selection info updated
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
assert tests.sgmtSelectionCheck([[5,6], [6,7]])
assert tests.selectionSizeCheck(2)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.9782608695652e-01,y=-1.2391304347826e-01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.9782608695652e-01,y=-1.2391304347826e-01,state=257,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
assert tests.sgmtSelectionCheck([[2, 7], [5, 6], [6, 7]])
assert tests.selectionSizeCheck(3)
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.SegmentSelection.Intersect_Group
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.sgmtSelectionCheck([[5, 6], [6, 7]])
assert tests.selectionSizeCheck(2)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:x_elements').set_text('')
checkpoint skeleton page sensitized
findWidget('Dialog-New skeleton:x_elements').set_text('5')
findWidget('Dialog-New skeleton:y_elements').set_text('')
findWidget('Dialog-New skeleton:y_elements').set_text('5')
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
assert tests.chooserCheck('OOF2:Skeleton Selection Page:Skeleton', ['skeleton', 'skeleton<2>'])
assert tests.chooserStateCheck('OOF2:Skeleton Selection Page:Skeleton', 'skeleton')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Skeleton'), 'skeleton<2>')
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
assert tests.chooserStateCheck('OOF2:Skeleton Selection Page:Skeleton', 'skeleton<2>')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
assert tests.groupCheck([])
assert tests.selectionSizeCheck(0)
assert tests.sgmtSelectionCheck2([])
assert tests.sensitization6()
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(249, 72)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('Dialog-Create a new Segment group:name:Text').set_text('')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('g')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('gr')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('grp')
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
assert tests.groupCheck(['grp (0 segments)'])
assert tests.sensitization7()
setComboBox(findWidget('OOF2:Skeleton Selection Page:Skeleton'), 'skeleton')
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
assert tests.sgmtSelectionCheck([[5, 6], [6, 7]])
assert tests.groupCheck(['loop groop (11 segments)'])
assert tests.sensitization3()
setComboBox(findWidget('OOF2:Skeleton Selection Page:Skeleton'), 'skeleton<2>')
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
assert tests.groupCheck(['grp (0 segments)'])
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
assert tests.sensitization7()
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:Invert').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Invert
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.selectionSizeCheck(60)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Skeleton'), 'skeleton')
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:targets:Chooser'), 'All Elements')
findWidget('OOF2:Skeleton Page:Pane').set_position(355)
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Refine:degree:Chooser'), 'Bisection')
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Modify
setComboBox(findWidget('OOF2:Skeleton Page:Skeleton'), 'skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(355)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint OOF.Skeleton.Modify
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(367)
findWidget('OOF2:Navigation:Next').clicked()
assert tests.selectionSizeCheck(4)
assert tests.sgmtSelectionCheck([[30, 52], [31, 52], [31, 57], [32, 57]])
assert tests.groupCheck(['loop groop (22 segments)'])
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Skeleton'), 'skeleton<2>')
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
assert tests.selectionSizeCheck(120)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(355)
findWidget('OOF2:Skeleton Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
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
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Segment sensitized
findWidget('OOF2:Skeleton Page:Pane').set_position(355)
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Delete
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
assert tests.chooserCheck('OOF2:Skeleton Selection Page:Skeleton', ['skeleton<2>'])
assert tests.sensitization8()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(191)
findWidget('OOF2:Microstructure Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(209, 94)
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
findWidget('OOF2:Microstructure Page:Pane').set_position(187)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
assert tests.sensitization9()
assert tests.selectionSizeCheck(None)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(324)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('s')
findWidget('Dialog-Python_Log:filename').set_text('sk')
findWidget('Dialog-Python_Log:filename').set_text('ske')
findWidget('Dialog-Python_Log:filename').set_text('skel')
findWidget('Dialog-Python_Log:filename').set_text('skels')
findWidget('Dialog-Python_Log:filename').set_text('skelse')
findWidget('Dialog-Python_Log:filename').set_text('skelsel')
findWidget('Dialog-Python_Log:filename').set_text('skelsels')
findWidget('Dialog-Python_Log:filename').set_text('skelselse')
findWidget('Dialog-Python_Log:filename').set_text('skelselseg')
findWidget('Dialog-Python_Log:filename').set_text('skelselseg.')
findWidget('Dialog-Python_Log:filename').set_text('skelselseg.l')
findWidget('Dialog-Python_Log:filename').set_text('skelselseg.lo')
findWidget('Dialog-Python_Log:filename').set_text('skelselseg.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
checkpoint_count("boundary page updated")
assert tests.filediff('skelselseg.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
