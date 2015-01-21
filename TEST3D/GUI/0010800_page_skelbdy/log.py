# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.9 $
# $Author: langer $
# $Date: 2014/05/08 14:40:40 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Basic skeleton boundaries selections

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane').set_position(300)
assert tests.sensitization0()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 67)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/two_walls.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Solver page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint Solver page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint pinnodes page sensitized
checkpoint pinnodes page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Activity Viewer').resize(400, 300)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.File.Load.Data
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
assert tests.sensitization1()
findWidget('OOF3D:Skeleton Boundaries Page:Pane').set_position(300)
findWidget('OOF3D').resize(550, 350)
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:fill').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 704))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 704))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 703))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 703))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 692))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 692))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 672))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 672))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 664))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 664))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 657))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 657))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 649))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 649))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 643))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 643))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 640))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 640))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 639))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((13,))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 9.0000000000000e+00)
checkpoint OOF.Graphics_1.Layer.Select
tree=findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(2)
tree.row_activated((13,), column)
checkpoint toplevel widget mapped Dialog-Edit Graphics Layer
findWidget('Dialog-Edit Graphics Layer').resize(291, 191)
setComboBox(findWidget('Dialog-Edit Graphics Layer:how:Bitmap:filter:Chooser'), 'Not')
findWidget('Dialog-Edit Graphics Layer').resize(336, 221)
setComboBox(findWidget('Dialog-Edit Graphics Layer:how:Bitmap:filter:Not:a:Chooser'), 'Group')
findWidget('Dialog-Edit Graphics Layer').resize(368, 249)
setComboBox(findWidget('Dialog-Edit Graphics Layer:how:Bitmap:filter:Not:a:Group:group'), '#000000')
findWidget('Dialog-Edit Graphics Layer:gtk-ok').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Edit
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1500000000000e+02,y= 9.6000000000000e+01,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.4600000000000e+02,y= 1.1500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
assert tests.voxelSelectionPageStatusCheck('','','')
assert tests.boundariesCheck('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin','a string unlikely to be a boundary name','XmaxYmax','XmaxYmin','XmaxZmax','XmaxZmin','XminYmax','XminYmin','XminZmax','XminZmin','YmaxZmax','YmaxZmin','YminZmax','YminZmin','a string unlikely to be a boundary name','XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin')
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((0,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('Xmax', 'Face', 8)
assert tests.boundariesSelectedCheck('Xmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.6000000000000e+02,y= 2.2600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7500000000000e+02,y= 2.1500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((1,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('Xmin', 'Face', 8)
assert tests.boundariesSelectedCheck('Xmin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0200000000000e+02,y= 3.9500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.1000000000000e+02,y= 4.1400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((2,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('Ymax', 'Face', 8)
assert tests.boundariesSelectedCheck('Ymax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0500000000000e+02,y= 1.0600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8800000000000e+02,y= 1.3800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((3,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('Ymin', 'Face', 8)
assert tests.boundariesSelectedCheck('Ymin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.6400000000000e+02,y= 3.8700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2000000000000e+02,y= 2.9200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((4,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('Zmax', 'Face', 32)
assert tests.boundariesSelectedCheck('Zmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5700000000000e+02,y= 4.5500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7200000000000e+02,y= 4.7800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((5,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('Zmin', 'Face', 32)
assert tests.boundariesSelectedCheck('Zmin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9700000000000e+02,y= 4.2600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.1800000000000e+02,y= 4.1500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((7,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XmaxYmax', 'Edge', 1)
assert tests.boundariesSelectedCheck('XmaxYmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0100000000000e+02,y= 5.1200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8500000000000e+02,y= 4.8000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((8,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XmaxYmin', 'Edge', 1)
assert tests.boundariesSelectedCheck('XmaxYmin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4300000000000e+02,y= 4.9400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4500000000000e+02,y= 4.6500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.4992923739494e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.9985847478988e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0497877121848e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3997169495798e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.7496461869747e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.0995754243696e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.7496461869747e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((9,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.7400000000000e+02)
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XmaxZmax', 'Edge', 4)
assert tests.boundariesSelectedCheck('XmaxZmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2800000000000e+02,y= 4.5900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4400000000000e+02,y= 4.6900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((10,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XmaxZmin', 'Edge', 4)
assert tests.boundariesSelectedCheck('XmaxZmin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8900000000000e+02,y= 4.7500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.5400000000000e+02,y= 4.6800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((11,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XminYmax', 'Edge', 1)
assert tests.boundariesSelectedCheck('XminYmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.7300000000000e+02,y= 4.8700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2600000000000e+02,y= 4.3600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((12,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XminYmin', 'Edge', 1)
assert tests.boundariesSelectedCheck('XminYmin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8700000000000e+02,y= 5.2900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.9100000000000e+02,y= 5.0100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((13,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XminZmax', 'Edge', 4)
assert tests.boundariesSelectedCheck('XminZmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.4800000000000e+02,y= 4.8000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.3000000000000e+02,y= 4.8100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((14,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XminZmin', 'Edge', 4)
assert tests.boundariesSelectedCheck('XminZmin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.9600000000000e+02,y= 4.7300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.3500000000000e+02,y= 4.8000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((15,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('YmaxZmax', 'Edge', 4)
assert tests.boundariesSelectedCheck('YmaxZmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8300000000000e+02,y= 5.1800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8200000000000e+02,y= 5.1400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.0899292373949e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4398584747899e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.7897877121848e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.1397169495798e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((16,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.1300000000000e+02)
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('YmaxZmin', 'Edge', 4)
assert tests.boundariesSelectedCheck('YmaxZmin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.0500000000000e+02,y= 5.0800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.3800000000000e+02,y= 5.5500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((17,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('YminZmax', 'Edge', 4)
assert tests.boundariesSelectedCheck('YminZmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.2700000000000e+02,y= 5.5000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.1900000000000e+02,y= 5.2100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((18,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('YminZmin', 'Edge', 4)
assert tests.boundariesSelectedCheck('YminZmin')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.9700000000000e+02,y= 5.0000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.0600000000000e+02,y= 4.9500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((20,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XmaxYmaxZmax', 'Point', 1)
assert tests.boundariesSelectedCheck('XmaxYmaxZmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.5000000000000e+02,y= 5.1300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7800000000000e+02,y= 5.1700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((21,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XmaxYmaxZmin', 'Point', 1)
assert tests.boundariesSelectedCheck('XmaxYmaxZmin')
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((22,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XmaxYminZmax', 'Point', 1)
assert tests.boundariesSelectedCheck('XmaxYminZmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2300000000000e+02,y= 5.2100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.2300000000000e+02,y= 4.8600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.4799292373949e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.9000707626051e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((23,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.9000000000000e+02)
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XmaxYminZmin', 'Point', 1)
assert tests.boundariesSelectedCheck('XmaxYminZmin')
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((24,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XminYmaxZmax', 'Point', 1)
assert tests.boundariesSelectedCheck('XminYmaxZmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.3800000000000e+02,y= 4.3500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.1000000000000e+02,y= 4.5800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((25,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XminYmaxZmin', 'Point', 1)
assert tests.boundariesSelectedCheck('XminYmaxZmin')
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.2499292373949e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.2500000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((26,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XminYminZmax', 'Point', 1)
assert tests.boundariesSelectedCheck('XminYminZmax')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2000000000000e+02,y= 4.8300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3400000000000e+02,y= 4.6900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 605)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.3400000000000e+02,y= 4.6900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((27,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.sensitization2()
assert tests.voxelSelectionPageStatusCheck('XminYminZmin', 'Point', 1)
assert tests.boundariesSelectedCheck('XminYminZmin')
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('boundary.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('boundary.log')
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
checkpoint OOF.Graphics_1.File.Close
