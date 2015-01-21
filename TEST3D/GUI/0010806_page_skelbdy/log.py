# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.11 $
# $Author: fyc $
# $Date: 2014/09/19 22:52:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing Segments Boundary modification: Direction, Add and Remove Segments Boundaries

findWidget('OOF3D').resize(550, 350)
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
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Solver page sensitized
checkpoint microstructure page sensitized
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
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
checkpoint toplevel widget mapped OOF3D Activity Viewer
checkpoint boundary page updated
findWidget('OOF3D Activity Viewer').resize(400, 300)
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
checkpoint OOF.File.Load.Data
findWidget('OOF3D').resize(550, 350)
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.0000000000000e+00)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((13,))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.2000000000000e+01)
checkpoint OOF.Graphics_1.Layer.Select
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.5000000000000e+01)
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
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1100000000000e+02,y= 2.2400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1200000000000e+02,y= 2.2400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2200000000000e+02,y= 1.9500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2200000000000e+02,y= 1.9500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:dolly').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1300000000000e+02,y= 3.2800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1300000000000e+02,y= 3.2700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1100000000000e+02,y= 2.6100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1100000000000e+02,y= 2.6100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Skeleton Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Segment').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2900000000000e+02,y= 4.9700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2900000000000e+02,y= 4.9700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Messages 1').resize(543, 200)
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6700000000000e+02,y= 2.8000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6700000000000e+02,y= 2.8000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0300000000000e+02,y= 1.2900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0200000000000e+02,y= 1.2900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9300000000000e+02,y= 1.2700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.9300000000000e+02,y= 1.2700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.6700000000000e+02,y= 1.2500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.6800000000000e+02,y= 1.2500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7000000000000e+02,y= 1.2500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7000000000000e+02,y= 1.2500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1000000000000e+02,y= 4.0100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1000000000000e+02,y= 4.0100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.6000000000000e+01,y= 2.0500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.6000000000000e+01,y= 2.0500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane').set_position(227)
findWidget('OOF3D:Skeleton Selection Page:Mode:Segment').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
findWidget('OOF3D').resize(550, 376)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:name:Auto').clicked()
findWidget('Dialog-Create a new Segment group:name:Text').set_text('t')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('to')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('top')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('top_')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('top_r')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('top_ra')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('top_ran')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('top_rang')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('top_range')
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.0100000000000e+02,y= 1.6100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.0100000000000e+02,y= 1.6100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.3700000000000e+02,y= 1.8400000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.3700000000000e+02,y= 1.8400000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7800000000000e+02,y= 1.3800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7900000000000e+02,y= 1.3800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8700000000000e+02,y= 1.3800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8700000000000e+02,y= 1.3800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2400000000000e+02,y= 1.5600000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.2400000000000e+02,y= 1.5600000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2200000000000e+02,y= 1.1100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2200000000000e+02,y= 1.1200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0500000000000e+02,y= 1.1600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0500000000000e+02,y= 1.1600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7200000000000e+02,y= 5.4000000000000e+01,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7200000000000e+02,y= 5.4000000000000e+01,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:dolly').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7900000000000e+02,y= 1.4200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8000000000000e+02,y= 1.4200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8200000000000e+02,y= 1.6400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8200000000000e+02,y= 1.6400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5000000000000e+02,y= 1.2400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5100000000000e+02,y= 1.2400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5200000000000e+02,y= 1.4300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5200000000000e+02,y= 1.4300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8900000000000e+02,y= 2.1200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9000000000000e+02,y= 2.1200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9900000000000e+02,y= 2.0000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9900000000000e+02,y= 2.0000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:name:Text').set_text('_range')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('f_range')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('fo_range')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('for_range')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('fore_range')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('forei_range')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('foreig_range')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('foreign_range')
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_Group
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5800000000000e+02,y= 2.2200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.5800000000000e+02,y= 2.2100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.3300000000000e+02,y= 2.0700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3300000000000e+02,y= 2.0700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane').set_position(300)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from segments')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','top_range','foreign_range')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-X to +X')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.2700000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.2300000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','top_range','foreign_range')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3600000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.4700000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','top_range','foreign_range')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.6000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.7100000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','top_range','foreign_range')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.9500000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','top_range','foreign_range')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.1900000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','top_range','foreign_range')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-Z to +Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.4300000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Clear
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentAction:Select Group:group'), 'foreign_range')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentSelection.Select_Group
checkpoint skeleton selection page updated
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2400000000000e+02,y= 2.9200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2500000000000e+02,y= 2.9200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.7300000000000e+02,y= 3.1200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7300000000000e+02,y= 3.1200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4300000000000e+02,y= 2.9300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.4300000000000e+02,y= 2.9400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.5900000000000e+02,y= 3.3800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5900000000000e+02,y= 3.3800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:dolly').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7500000000000e+02,y= 1.3100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7500000000000e+02,y= 1.3200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8300000000000e+02,y= 1.6000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8300000000000e+02,y= 1.6000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4400000000000e+02,y= 1.4000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4400000000000e+02,y= 1.4100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5300000000000e+02,y= 1.5600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5300000000000e+02,y= 1.5600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3940397350993e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.8477483443709e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((19,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.8400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesCheck('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin','a string unlikely to be a boundary name','XmaxYmax','XmaxYmin','XmaxZmax','XmaxZmin','XminYmax','XminYmin','XminZmax','XminZmin','YmaxZmax','YmaxZmin','YminZmax','YminZmin','boundary','boundary<2>','boundary<3>','boundary<4>','boundary<5>','boundary<6>','a string unlikely to be a boundary name','XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin')
assert tests.boundariesSelectedCheck('boundary')
assert tests.voxelSelectionPageStatusCheck('boundary', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Reverse direction')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Reverse direction')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3600000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3600000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Add segments')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Add segments','<selection>','top_range','foreign_range')
assert tests.BoundaryModifyDialogSelectModifierGroup0('Add segments','<selection>')
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3600000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((20,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<2>')
assert tests.voxelSelectionPageStatusCheck('boundary<2>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Reverse direction')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Reverse direction')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.6000000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<2>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.6000000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<2>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Add segments')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Add segments','<selection>','top_range','foreign_range')
assert tests.BoundaryModifyDialogSelectModifierGroup0('Add segments','<selection>')
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.6000000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<2>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((21,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<3>')
assert tests.voxelSelectionPageStatusCheck('boundary<3>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Reverse direction')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Reverse direction')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<3>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<3>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Add segments')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Add segments','<selection>','top_range','foreign_range')
assert tests.BoundaryModifyDialogSelectModifierGroup0('Add segments','<selection>')
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<3>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((22,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<4>')
assert tests.voxelSelectionPageStatusCheck('boundary<4>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Reverse direction')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Reverse direction')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<4>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<4>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Add segments')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Add segments','<selection>','top_range','foreign_range')
assert tests.BoundaryModifyDialogSelectModifierGroup0('Add segments','<selection>')
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<4>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((23,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<5>')
assert tests.voxelSelectionPageStatusCheck('boundary<5>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Reverse direction')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Reverse direction')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3200000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<5>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3200000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<5>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Add segments')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Add segments','<selection>','top_range','foreign_range')
assert tests.BoundaryModifyDialogSelectModifierGroup0('Add segments','<selection>')
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3200000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.boundariesSelectedCheck('boundary<5>')
assert tests.voxelSelectionPageStatusCheck('boundary<5>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((24,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<6>')
assert tests.voxelSelectionPageStatusCheck('boundary<6>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Reverse direction')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Reverse direction')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.4300000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<6>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.4300000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<6>', 'Edge', 3)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(261, 75)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Add segments')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Add segments','<selection>','top_range','foreign_range')
assert tests.BoundaryModifyDialogSelectModifierGroup0('Add segments','<selection>')
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.4300000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<6>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Clear
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2900000000000e+02,y= 3.7800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2900000000000e+02,y= 3.7800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:name:Text').set_text('')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('b')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('ba')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_s')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_se')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_seg')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_segm')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_segme')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_segmeb')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_segmebt')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_segmeb')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_segme')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_segmen')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('bad_segment')
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9300000000000e+02,y= 3.9600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9300000000000e+02,y= 3.9600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:name:Text').set_text('_segment')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('g_segment')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('go_segment')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('goo_segment')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('good_segment')
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll').get_hadjustment().set_value( 2.9210526315789e+00)
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll').get_hadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentAction:Select Group:group'), 'bad_segment')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0513505932893e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.5367529664465e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((19,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.5300000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary')
assert tests.voxelSelectionPageStatusCheck('boundary', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Remove segments')
assert tests.BoundaryModifyDialogCheckModifierGroups0('Remove segments','<selection>','top_range','foreign_range','bad_segment','good_segment')
assert tests.BoundaryModifyDialogSelectModifierGroup0('Remove segments','<selection>')
findWidget('Dialog-Boundary modifier:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((20,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<2>')
assert tests.voxelSelectionPageStatusCheck('boundary<2>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
assert tests.BoundaryModifyDialogCheckModifierGroups1('Add segments')
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((21,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<3>')
assert tests.voxelSelectionPageStatusCheck('boundary<3>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
assert tests.BoundaryModifyDialogCheckModifierGroups1('Add segments')
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((22,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<4>')
assert tests.voxelSelectionPageStatusCheck('boundary<4>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
assert tests.BoundaryModifyDialogCheckModifierGroups1('Add segments')
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((23,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<5>')
assert tests.voxelSelectionPageStatusCheck('boundary<5>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
assert tests.BoundaryModifyDialogCheckModifierGroups1('Add segments')
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((24,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<6>')
assert tests.voxelSelectionPageStatusCheck('boundary<6>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
assert tests.BoundaryModifyDialogCheckModifierGroups1('Add segments')
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.5600662251656e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.6319867549669e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Clear
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentAction:Select Group:group'), 'good_segment')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.6300000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((19,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary')
assert tests.voxelSelectionPageStatusCheck('boundary', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Remove segments')
assert tests.BoundaryModifyDialogCheckModifierGroups1('Remove segments','<selection>','top_range','foreign_range','bad_segment','good_segment')
assert tests.BoundaryModifyDialogSelectModifierGroup1('Remove segments','<selection>')
findWidget('Dialog-Boundary modifier:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Remove').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(305, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Remove_from_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Clear
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5800000000000e+02,y= 3.9300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5800000000000e+02,y= 3.9300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((19,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary')
assert tests.voxelSelectionPageStatusCheck('boundary', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Remove segments')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3600000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((20,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<2>')
assert tests.voxelSelectionPageStatusCheck('boundary<2>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.6000000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<2>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((21,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<3>')
assert tests.voxelSelectionPageStatusCheck('boundary<3>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<3>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((22,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<4>')
assert tests.voxelSelectionPageStatusCheck('boundary<4>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<4>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((23,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<5>')
assert tests.voxelSelectionPageStatusCheck('boundary<5>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3200000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<5>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((24,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.boundariesSelectedCheck('boundary<6>')
assert tests.voxelSelectionPageStatusCheck('boundary<6>', 'Edge', 7)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(301, 103)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.4300000000000e+02)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.voxelSelectionPageStatusCheck('boundary<6>', 'Edge', 7)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:DeleteAll').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Delete_All
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3940397350993e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.7039072847682e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((19,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.7000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5500000000000e+02,y= 2.4800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5500000000000e+02,y= 2.4600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7400000000000e+02,y= 1.9200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7400000000000e+02,y= 1.9200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((20,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((21,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((22,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((23,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((24,))
checkpoint boundary page updated
checkpoint boundary page updated

findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('boundary.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('boundary.log')
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
