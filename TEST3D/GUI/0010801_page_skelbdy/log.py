# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.11 $
# $Author: fyc $
# $Date: 2014/09/19 22:52:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing the different ways of creating a skeleton boundary
#From Nodes, From Segments, From Faces, From Elements

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
findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.0000000000000e+00)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.0000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.0000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.0000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.0000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.0000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.0000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((13,))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.5000000000000e+01)
checkpoint OOF.Graphics_1.Layer.Select
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.2000000000000e+01)
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
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9300000000000e+02,y= 3.4700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9300000000000e+02,y= 3.4600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9400000000000e+02,y= 3.4500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9500000000000e+02,y= 3.4000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9500000000000e+02,y= 3.3900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9500000000000e+02,y= 3.3500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9500000000000e+02,y= 3.3400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9700000000000e+02,y= 3.3200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9700000000000e+02,y= 3.3100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9700000000000e+02,y= 3.3000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9800000000000e+02,y= 3.2700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0100000000000e+02,y= 3.2300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0200000000000e+02,y= 3.1900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0400000000000e+02,y= 3.1500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0500000000000e+02,y= 3.1500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0700000000000e+02,y= 3.1100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0900000000000e+02,y= 3.0900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1100000000000e+02,y= 3.0500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1300000000000e+02,y= 3.0000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1400000000000e+02,y= 3.0000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1500000000000e+02,y= 2.9700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1500000000000e+02,y= 2.9400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1600000000000e+02,y= 2.9100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1600000000000e+02,y= 2.8900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1600000000000e+02,y= 2.8400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1600000000000e+02,y= 2.8300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1700000000000e+02,y= 2.8300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1700000000000e+02,y= 2.8100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1700000000000e+02,y= 2.8000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1700000000000e+02,y= 2.7900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1700000000000e+02,y= 2.7900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Skeleton Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0300000000000e+02,y= 3.8000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0300000000000e+02,y= 3.8000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Messages 1').resize(543, 200)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane').set_position(227)
findWidget('OOF3D:Skeleton Selection Page:Mode:Face').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
findWidget('OOF3D').resize(550, 376)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceAction:Chooser'), 'Select from Selected Elements')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.FaceSelection.Select_from_Selected_Elements
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6400000000000e+02,y= 1.6900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4500000000000e+02,y= 1.7200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4500000000000e+02,y= 1.7200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane').set_position(300)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Face boundary from faces')
findWidget('Dialog-New Boundary').resize(368, 153)
assert tests.BoundaryNewDialogCheck0('Face boundary from faces','Outward','Inward',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','Outward')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.4400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), 'Inward')
assert tests.BoundaryNewDialogCheck0('Face boundary from faces','Outward','Inward',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','Inward')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.4400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.6800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from faces')
assert tests.BoundaryNewDialogCheck0('Point boundary from faces')
assert tests.BoundaryNewDialogCheck1('Point boundary from faces','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.6800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.7100000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.7100000000000e+02)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.FaceSelection.Clear
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1100000000000e+02,y= 2.5700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.2600000000000e+02,y= 2.7900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2600000000000e+02,y= 2.7900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Method:Chooser'), 'ByDominantPixel')
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.9000000000000e+01,y= 2.3300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.9000000000000e+01,y= 2.3300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Messages 1').resize(553, 200)
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.FaceSelection.Select_from_Selected_Elements
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Face boundary from faces')
assert tests.BoundaryNewDialogCheck0('Face boundary from faces')
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.9200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.9200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), 'Outward')
assert tests.BoundaryNewDialogCheck0('Face boundary from faces','Outward','Inward',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','Outward')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.9200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.1600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceSelection.Clear
checkpoint skeleton selection page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(404, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Face boundary from elements')
assert tests.BoundaryNewDialogCheck0('Face boundary from elements','Outward','Inward',)
assert tests.BoundaryNewDialogCheck1('Face boundary from elements','<selection>','Outward')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from elements:direction'), 'Inward')
assert tests.BoundaryNewDialogCheck0('Face boundary from elements','Outward','Inward',)
assert tests.BoundaryNewDialogCheck1('Face boundary from elements','<selection>','Inward')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.6400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Segment').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Select from Selected Elements')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_from_Selected_Elements
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(404, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from segments')
assert tests.BoundaryNewDialogCheck0('Point boundary from segments')
assert tests.BoundaryNewDialogCheck1('Point boundary from segments','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.9100000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.9100000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from segments')
assert tests.BoundaryNewDialogCheck2('Edge boundary from segments','No edge sequence',)
assert tests.BoundaryNewDialogCheck3('Edge boundary from segments','<selection>','No edge sequence')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Undo
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Mode:Node').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:NodeAction:Chooser'), 'Select from Selected Elements')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:NodeHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint OOF.NodeSelection.Select_from_Selected_Elements
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Point boundary from nodes')
assert tests.BoundaryNewDialogCheck1('Point boundary from nodes','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.1500000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.1500000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheck2('Edge boundary from nodes','No edge sequence',)
assert tests.BoundaryNewDialogCheck3('Edge boundary from nodes','<selection>','No edge sequence')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.NodeSelection.Clear
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Segment').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0000000000000e+02,y= 1.4000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9500000000000e+02,y= 1.3800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9500000000000e+02,y= 1.3800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1900000000000e+02,y= 5.3200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1900000000000e+02,y= 5.3200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2700000000000e+02,y= 4.0900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2700000000000e+02,y= 4.0900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8100000000000e+02,y= 3.8700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8100000000000e+02,y= 3.8700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9400000000000e+02,y= 3.2100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.9400000000000e+02,y= 3.2100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1800000000000e+02,y= 2.8900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1800000000000e+02,y= 2.8900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0500000000000e+02,y= 3.3600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0500000000000e+02,y= 3.3600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5300000000000e+02,y= 3.7400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5300000000000e+02,y= 3.7400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from segments')
assert tests.BoundaryNewDialogCheck0('Point boundary from segments')
assert tests.BoundaryNewDialogCheck1('Point boundary from segments','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.3900000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from segments')
assert tests.BoundaryNewDialogCheck0('Edge boundary from segments','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z')
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','-X to +X')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.6300000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.8000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.8000000000000e+02)
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8500000000000e+02,y= 1.5400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8400000000000e+02,y= 1.5400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5600000000000e+02,y= 1.5400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5500000000000e+02,y= 1.5400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheck0('Edge boundary from segments','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.8000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.0400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheck0('Edge boundary from segments','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','+Y to -Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.0400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.2800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheck0('Edge boundary from segments','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.2800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.5200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheck0('Edge boundary from segments','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.5200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.7600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheck0('Edge boundary from segments','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','-Z to +Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.7600000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:NodeAction:Chooser'), 'Select from Selected Segments')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:NodeHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeSelection.Select_from_Selected_Segments
checkpoint skeleton selection page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0700000000000e+02,y= 2.6400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1400000000000e+02,y= 2.6400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1600000000000e+02,y= 2.6400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Point boundary from nodes')
assert tests.BoundaryNewDialogCheck1('Point boundary from nodes','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.3500000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.0700000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheck2('Edge boundary from nodes','No edge sequence',)
assert tests.BoundaryNewDialogCheck3('Edge boundary from nodes','<selection>','No edge sequence')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeSelection.Clear
checkpoint skeleton selection page updated
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0100000000000e+02,y= 2.9400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2600000000000e+02,y= 3.0000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2600000000000e+02,y= 3.0000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Node').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.6200000000000e+02,y= 5.2200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.6200000000000e+02,y= 5.2200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4100000000000e+02,y= 4.0500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4100000000000e+02,y= 4.0500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1800000000000e+02,y= 3.0000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1800000000000e+02,y= 3.0000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9100000000000e+02,y= 2.9300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.9100000000000e+02,y= 2.9300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.3100000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-X to +X')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.2400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.2400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.2400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.4800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+Y to -Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.4800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.7200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.7200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.9600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.9600000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.2000000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-Z to +Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.2000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.4400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1000000000000e+02,y= 1.9100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1800000000000e+02,y= 1.9300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1800000000000e+02,y= 1.9300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7500000000000e+02,y= 2.0300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7500000000000e+02,y= 2.0300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Point boundary from nodes')
assert tests.BoundaryNewDialogCheck1('Point boundary from nodes','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.2700000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.9900000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-Z to +Z')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0200000000000e+02,y= 3.0000000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.0200000000000e+02,y= 3.0000000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-Z to +Z')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.6800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.6800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.6800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.9200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.9200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.1600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+Y to -Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.1600000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.4000000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.4000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.6400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '-X to +X')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-X to +X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.6400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.8800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1500000000000e+02,y= 2.2600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8200000000000e+02,y= 2.2400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8200000000000e+02,y= 2.2400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5100000000000e+02,y= 1.6000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4100000000000e+02,y= 1.7100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4100000000000e+02,y= 1.7100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3500000000000e+02,y= 2.4500000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3500000000000e+02,y= 2.4500000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6100000000000e+02,y= 1.5500000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6100000000000e+02,y= 1.5500000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Point boundary from nodes')
assert tests.BoundaryNewDialogCheck1('Point boundary from nodes','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0950000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1670000000000e+03)
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3800000000000e+02,y= 2.3900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4400000000000e+02,y= 2.1900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4400000000000e+02,y= 2.1900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheck2('Edge boundary from nodes','No edge sequence',)
assert tests.BoundaryNewDialogCheck3('Edge boundary from nodes','<selection>','No edge sequence')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9700000000000e+02,y= 3.6600000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.9700000000000e+02,y= 3.6600000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9600000000000e+02,y= 3.6600000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.9600000000000e+02,y= 3.6600000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1910000000000e+03)
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3700000000000e+02,y= 2.0800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3800000000000e+02,y= 2.0900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1000000000000e+02,y= 2.2900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-X to +X')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8600000000000e+02,y= 2.3500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8700000000000e+02,y= 2.3500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1200000000000e+02,y= 2.3400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1200000000000e+02,y= 2.3400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3300000000000e+02,y= 2.3600000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3300000000000e+02,y= 2.3600000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7200000000000e+02,y= 1.7000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7200000000000e+02,y= 1.7000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.7600000000000e+02,y= 1.9300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.7600000000000e+02,y= 1.9300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8400000000000e+02,y= 1.3600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8400000000000e+02,y= 1.3600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2150000000000e+03)
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5200000000000e+02,y= 1.6000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5200000000000e+02,y= 1.5900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4900000000000e+02,y= 1.4500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4900000000000e+02,y= 1.4500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2700000000000e+02,y= 1.2600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2800000000000e+02,y= 1.2700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4400000000000e+02,y= 1.3600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5700000000000e+02,y= 1.5800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4900000000000e+02,y= 1.5400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4900000000000e+02,y= 1.5400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-X to +X')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2390000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0120000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0120000000000e+03)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4400000000000e+02,y= 2.6600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.4400000000000e+02,y= 2.6700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0800000000000e+02,y= 3.4200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0800000000000e+02,y= 3.4200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0120000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0360000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+Y to -Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0360000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0600000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0600000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0840000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0840000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1080000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheck0('Edge boundary from nodes','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','-Z to +Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1080000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1320000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Node:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Clear
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
