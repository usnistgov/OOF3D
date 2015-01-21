# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.11 $
# $Author: fyc $
# $Date: 2014/09/19 22:52:50 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing the effects of modifying the skeleton selection group used to create
#a boundary. Testing also the boundary custructor direction parameter values

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
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.6116626110202e+00)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.5223325222040e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2834987833061e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.0446650444081e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.8058313055101e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.5669975666121e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.3281638277142e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.0893300888162e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.8504963499182e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.5000000000000e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((13,))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.2000000000000e+01)
checkpoint OOF.Graphics_1.Layer.Select
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
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7300000000000e+02,y= 3.2200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7300000000000e+02,y= 3.2000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7300000000000e+02,y= 3.1900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7300000000000e+02,y= 3.1300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 3.1100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 3.0800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 3.0400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 3.0200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 2.9800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 2.9400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 2.9100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 2.8800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 2.8700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 2.8600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7300000000000e+02,y= 2.8400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7600000000000e+02,y= 2.8200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7600000000000e+02,y= 2.8100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7700000000000e+02,y= 2.7900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7800000000000e+02,y= 2.7800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7800000000000e+02,y= 2.7600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7900000000000e+02,y= 2.7300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7900000000000e+02,y= 2.7200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7900000000000e+02,y= 2.7100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8000000000000e+02,y= 2.7100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8100000000000e+02,y= 2.7200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8200000000000e+02,y= 2.7200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8300000000000e+02,y= 2.7300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8300000000000e+02,y= 2.7400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8300000000000e+02,y= 2.7500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8400000000000e+02,y= 2.7500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8500000000000e+02,y= 2.7500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8500000000000e+02,y= 2.7600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8600000000000e+02,y= 2.7600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8700000000000e+02,y= 2.7600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8700000000000e+02,y= 2.7600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
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
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8500000000000e+02,y= 4.9500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8500000000000e+02,y= 4.9500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Messages 1').resize(543, 200)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane').set_position(227)
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
findWidget('Dialog-Create a new Element group').resize(246, 67)
findWidget('Dialog-Create a new Element group:name:Auto').clicked()
findWidget('Dialog-Create a new Element group:name:Text').set_text('e')
findWidget('Dialog-Create a new Element group:name:Text').set_text('el')
findWidget('Dialog-Create a new Element group:name:Text').set_text('ele')
findWidget('Dialog-Create a new Element group:name:Text').set_text('elem')
findWidget('Dialog-Create a new Element group:name:Text').set_text('eleme')
findWidget('Dialog-Create a new Element group:name:Text').set_text('elemen')
findWidget('Dialog-Create a new Element group:name:Text').set_text('element')
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1800000000000e+02,y= 1.6500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1800000000000e+02,y= 1.6500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4700000000000e+02,y= 1.8700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4700000000000e+02,y= 1.8700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
findWidget('Dialog-Create a new Element group').resize(246, 67)
findWidget('Dialog-Create a new Element group:name:Text').set_text('')
findWidget('Dialog-Create a new Element group:name:Text').set_text('t')
findWidget('Dialog-Create a new Element group:name:Text').set_text('tw')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_e')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_el')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_ele')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_elem')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_eleme')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_elemen')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_element')
findWidget('Dialog-Create a new Element group:name:Text').set_text('two_elements')
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Method:Chooser'), 'ByDominantPixel')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9800000000000e+02,y= 3.6400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9800000000000e+02,y= 3.6400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Messages 1').resize(553, 200)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
findWidget('Dialog-Create a new Element group').resize(246, 67)
findWidget('Dialog-Create a new Element group:name:Auto').clicked()
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Face').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4900000000000e+02,y= 4.4700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4900000000000e+02,y= 4.4700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
findWidget('OOF3D:Skeleton Selection Page:Mode:Face').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
findWidget('OOF3D').resize(550, 376)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Face group
findWidget('Dialog-Create a new Face group').resize(246, 67)
findWidget('Dialog-Create a new Face group:name:Auto').clicked()
findWidget('Dialog-Create a new Face group:name:Text').set_text('f')
findWidget('Dialog-Create a new Face group:name:Text').set_text('fa')
findWidget('Dialog-Create a new Face group:name:Text').set_text('fac')
findWidget('Dialog-Create a new Face group:name:Text').set_text('face')
findWidget('Dialog-Create a new Face group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Clear
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2100000000000e+02,y= 1.6500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2100000000000e+02,y= 1.6500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4500000000000e+02,y= 1.8900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4500000000000e+02,y= 1.8900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Face group
findWidget('Dialog-Create a new Face group').resize(246, 67)
findWidget('Dialog-Create a new Face group:name:Text').set_text('')
findWidget('Dialog-Create a new Face group:name:Text').set_text('t')
findWidget('Dialog-Create a new Face group:name:Text').set_text('tw')
findWidget('Dialog-Create a new Face group:name:Text').set_text('two')
findWidget('Dialog-Create a new Face group:name:Text').set_text('two_')
findWidget('Dialog-Create a new Face group:name:Text').set_text('two_f')
findWidget('Dialog-Create a new Face group:name:Text').set_text('two_fa')
findWidget('Dialog-Create a new Face group:name:Text').set_text('two_fac')
findWidget('Dialog-Create a new Face group:name:Text').set_text('two_face')
findWidget('Dialog-Create a new Face group:name:Text').set_text('two_faces')
findWidget('Dialog-Create a new Face group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Clear
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceAction:Chooser'), 'Select from Selected Elements')
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceAction:Chooser'), 'Select Group')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Element').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.1400000000000e+02,y= 2.9300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.1400000000000e+02,y= 2.9300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
findWidget('OOF3D:Skeleton Selection Page:Mode:Element').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Mode:Face').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
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
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Face').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Face group
findWidget('Dialog-Create a new Face group').resize(246, 67)
findWidget('Dialog-Create a new Face group:name:Auto').clicked()
findWidget('Dialog-Create a new Face group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.New_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Undo').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Undo
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Undo').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Undo
findWidget('OOF3D:Skeleton Selection Page:Mode:Element').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Mode:Face').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Mode:Segment').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Segment').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2100000000000e+02,y= 4.7700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2100000000000e+02,y= 4.7700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6900000000000e+02,y= 3.9400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6900000000000e+02,y= 3.9400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3400000000000e+02,y= 4.1300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3400000000000e+02,y= 4.1300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1000000000000e+02,y= 4.1000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1000000000000e+02,y= 4.1000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:name:Auto').clicked()
findWidget('Dialog-Create a new Segment group:name:Text').set_text('f')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('fo')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('fou')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_s')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_se')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_seg')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_segm')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_segme')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_segmen')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_segment')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('four_segments')
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
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1500000000000e+02,y= 4.5300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1500000000000e+02,y= 4.5300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:name:Text').set_text('')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('s')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('se')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('seg')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('segm')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('segme')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('segmen')
findWidget('Dialog-Create a new Segment group:name:Text').set_text('segment')
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Element').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1700000000000e+02,y= 3.8300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.1700000000000e+02,y= 3.8300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
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
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:name:Text').set_text('')
findWidget('Dialog-Create a new Segment group:name:Auto').clicked()
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Clear
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Node').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2200000000000e+02,y= 5.0000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2200000000000e+02,y= 5.0000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF3D:Skeleton Selection Page:Mode:Node').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Node group
findWidget('Dialog-Create a new Node group').resize(246, 67)
findWidget('Dialog-Create a new Node group:name:Auto').clicked()
findWidget('Dialog-Create a new Node group:name:Text').set_text('n')
findWidget('Dialog-Create a new Node group:name:Text').set_text('no')
findWidget('Dialog-Create a new Node group:name:Text').set_text('nod')
findWidget('Dialog-Create a new Node group:name:Text').set_text('node')
findWidget('Dialog-Create a new Node group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Node:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Clear
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.6300000000000e+02,y= 1.4500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.6300000000000e+02,y= 1.4500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7500000000000e+02,y= 1.4700000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7500000000000e+02,y= 1.4700000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7100000000000e+02,y= 1.4800000000000e+02,button=1,state=20,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7100000000000e+02,y= 1.4800000000000e+02,button=1,state=276,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Node group
findWidget('Dialog-Create a new Node group').resize(246, 67)
findWidget('Dialog-Create a new Node group:name:Text').set_text('')
findWidget('Dialog-Create a new Node group:name:Text').set_text('t')
findWidget('Dialog-Create a new Node group:name:Text').set_text('tw')
findWidget('Dialog-Create a new Node group:name:Text').set_text('two')
findWidget('Dialog-Create a new Node group:name:Text').set_text('two_')
findWidget('Dialog-Create a new Node group:name:Text').set_text('two_n')
findWidget('Dialog-Create a new Node group:name:Text').set_text('two_no')
findWidget('Dialog-Create a new Node group:name:Text').set_text('two_nod')
findWidget('Dialog-Create a new Node group:name:Text').set_text('two_node')
findWidget('Dialog-Create a new Node group:name:Text').set_text('two_nodes')
findWidget('Dialog-Create a new Node group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.Add_to_Group
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Node:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Clear
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Element').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.9700000000000e+02,y= 2.9300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 671)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.9700000000000e+02,y= 2.9300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
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
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Node group
findWidget('Dialog-Create a new Node group').resize(246, 67)
findWidget('Dialog-Create a new Node group:name:Auto').clicked()
findWidget('Dialog-Create a new Node group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.New_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.Add_to_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.NodeSelection.Clear
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane').set_position(300)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Element').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint skeleton selection page groups sensitized
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Face boundary from elements')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from elements','<selection>','element','two_elements','elementgroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from elements','direction','Outward','Inward',)
assert tests.BoundaryNewDialogCheck1('Face boundary from elements','<selection>','direction','Outward')
findWidget('Dialog-New Boundary').resize(368, 153)
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
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from elements')
assert tests.BoundaryNewDialogCheckGroup0('Point boundary from elements','<selection>','element','two_elements','elementgroup')
assert tests.BoundaryNewDialogCheckScope0('Point boundary from elements','coverage','Exterior','Interior','All',)
assert tests.BoundaryNewDialogCheck1('Point boundary from elements','<selection>','coverage','Exterior')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.4400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.4700000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.4700000000000e+02)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Remove').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(263, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Remove_from_Group
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.0913505932893e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.8350593289302e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((6,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.8000000000000e+01)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0586494067107e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.4700000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((29,))
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint skeleton selection page groups sensitized
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.7100000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.7100000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Face boundary from elements')
assert tests.BoundaryNewDialogCheckGroup2('Face boundary from elements','<selection>','two_elements','elementgroup')
assert tests.BoundaryNewDialogCheckScope2('Face boundary from elements','direction','No orientable surface',)
assert tests.BoundaryNewDialogCheck3('Face boundary from elements','<selection>','direction','No orientable surface')
findWidget('Dialog-New Boundary').resize(404, 153)
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(222, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((29,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((30,))
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.9500000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.9500000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Face boundary from elements')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from elements','<selection>','elementgroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from elements','direction','Outward','Inward',)
assert tests.BoundaryNewDialogCheck1('Face boundary from elements','<selection>','direction','Outward')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.1900000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.6800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.6800000000000e+02)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(221, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3013505932893e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.2270118657860e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((6,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.2000000000000e+01)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((7,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2986494067107e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.1900000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((30,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((31,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((32,))
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Face').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint skeleton selection page groups sensitized
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceAction:Chooser'), 'Select Group')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.FaceSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(404, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from faces')
assert tests.BoundaryNewDialogCheckGroup0('Point boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Point boundary from faces')
assert tests.BoundaryNewDialogCheck1('Point boundary from faces','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.4300000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.4300000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from faces')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z','Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Counterclockwise-x')
findWidget('Dialog-New Boundary').resize(380, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.6700000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Counterclockwise-y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Counterclockwise-y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Counterclockwise-z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Counterclockwise-z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Clockwise-x')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Clockwise-x')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.5600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Clockwise-y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z','Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Clockwise-y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.8400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Clockwise-z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Clockwise-z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.3200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Face boundary from faces')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','-X to +X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.5600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.6800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.6800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.6800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.9200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','+Y to -Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.9200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.1600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.1600000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.6400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','face','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','-Z to +Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.6400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3654023731572e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((11,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3600000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((10,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((9,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((8,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((7,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.8135059328930e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((6,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.8000000000000e+01)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((7,))
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.FaceSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((8,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((9,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((10,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((11,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((12,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((13,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0300000000000e+02)
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.4086494067107e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.7872988134214e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((12,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.7800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint skeleton selection page groups sensitized
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.FaceSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '-X to +X')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','-X to +X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.1200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.1200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.3600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','+Y to -Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.3600000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.6000000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.6000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.8400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.8400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.0800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Face boundary from faces:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','-Z to +Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.0800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from faces')
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Clockwise-x')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Clockwise-x')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3200000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.3500000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.4400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Clockwise-y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Clockwise-y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.4400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.6800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Clockwise-z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Clockwise-z')
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
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Counterclockwise-x')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Counterclockwise-x')
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
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Counterclockwise-y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Counterclockwise-y')
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
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from faces:direction'), 'Counterclockwise-z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from faces','direction', 'Clockwise-x', 'Clockwise-y', 'Clockwise-z', 'Counterclockwise-x','Counterclockwise-y','Counterclockwise-z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from faces','<selection>','direction','Counterclockwise-z')
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
findWidget('Dialog-New Boundary').resize(380, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from faces')
assert tests.BoundaryNewDialogCheckGroup0('Point boundary from faces','<selection>','two_faces','facegroup')
assert tests.BoundaryNewDialogCheckScope0('Point boundary from faces')
assert tests.BoundaryNewDialogCheck1('Point boundary from faces','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.6400000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0710000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1430000000000e+03)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceSelection.Clear
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(196, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((56,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((57,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((54,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((57,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((58,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1051350593289e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.4008047463144e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((44,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.4000000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((43,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((42,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((41,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((40,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((39,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((38,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((37,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((36,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.0213505932893e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.6427011865786e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((35,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.6400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((34,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((33,))
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:FaceHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceSelection.Select_Group
checkpoint skeleton selection page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Face boundary from faces')
assert tests.BoundaryNewDialogCheckGroup0('Face boundary from faces','<selection>','facegroup',)
assert tests.BoundaryNewDialogCheckScope0('Face boundary from faces','direction','Outward','Inward',)
assert tests.BoundaryNewDialogCheck1('Face boundary from faces','<selection>','direction','Outward')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.9600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.5600000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.5600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from faces')
assert tests.BoundaryNewDialogCheckGroup2('Edge boundary from faces','<selection>','facegroup',)
assert tests.BoundaryNewDialogCheckScope2('Edge boundary from faces','direction', 'No edge sequence',)
assert tests.BoundaryNewDialogCheck3('Edge boundary from faces','<selection>','direction','No edge sequence')
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from faces')
assert tests.BoundaryNewDialogCheckGroup0('Point boundary from faces','<selection>','facegroup',)
assert tests.BoundaryNewDialogCheckScope0('Point boundary from faces')
assert tests.BoundaryNewDialogCheck1('Point boundary from faces','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.5600000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1190000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1910000000000e+03)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceSelection.Clear
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(195, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((58,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((57,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((56,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((55,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((60,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((59,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((58,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1531350593289e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1152701186579e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0774051779868e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0395402373157e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0016752966447e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.6381035597358e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((45,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.6300000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((44,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((43,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((42,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.2513505932893e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8727011865786e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((41,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8700000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((40,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((39,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((38,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.4913505932893e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.1127011865786e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.7340517798679e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((37,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.7300000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((36,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((35,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((34,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.3513505932893e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3221553396037e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((20,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.3200000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((19,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((18,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.9413505932893e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((17,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.1800000000000e+02)
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
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Select Group')
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
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from segments')
assert tests.BoundaryNewDialogCheckGroup0('Point boundary from segments','<selection>','four_segments','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Point boundary from segments')
assert tests.BoundaryNewDialogCheck1('Point boundary from segments','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.0800000000000e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1430000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2150000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from segments')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','four_segments','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-X to +X')
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
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','four_segments','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+X to -X')
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
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','four_segments','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+Y to -Y')
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
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','four_segments','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-Y to +Y')
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
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','four_segments','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+Z to -Z')
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
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','four_segments','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-Z to +Z')
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
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentSelection.Clear
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint skeleton selection page groups sensitized
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(227, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((51,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1698649406711e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3590000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((67,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((66,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3211350593289e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.4732189852577e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((7,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.4700000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((8,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((9,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((10,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((11,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((12,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((13,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((14,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((15,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.5100000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.8886494067107e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.6459482201321e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((16,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.6400000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((17,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((18,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((19,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((20,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.7100000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 3.0886494067107e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.8751434738177e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((34,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.8700000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((35,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((36,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((37,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((38,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.2486494067107e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.3845976268428e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((39,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.3800000000000e+02)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((40,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((41,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((42,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((43,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.7586494067107e+02)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0273247033553e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((44,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0270000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((45,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((46,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((47,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((48,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((49,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint skeleton selection page groups sensitized
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
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-X to +X')###
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-X to +X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1560000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1560000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1800000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+Y to -Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1800000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2040000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2040000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2280000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2280000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2520000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from segments:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from segments','<selection>','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from segments','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from segments','<selection>','direction','-Z to +Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2520000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2760000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from segments')
assert tests.BoundaryNewDialogCheckGroup0('Point boundary from segments','<selection>','segment','segmentgroup')
assert tests.BoundaryNewDialogCheckScope0('Point boundary from segments')
assert tests.BoundaryNewDialogCheck1('Point boundary from segments','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2760000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.4790000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.5270000000000e+03)
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
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((71,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((72,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((73,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((72,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.4891350593289e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0726207119472e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((54,))
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0720000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((53,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((52,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((51,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((50,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((49,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((48,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.SegmentSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.5030000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.5510000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from segments')
assert tests.BoundaryNewDialogCheckGroup2('Edge boundary from segments','<selection>','segmentgroup')
assert tests.BoundaryNewDialogCheckScope2('Edge boundary from segments','direction','No edge sequence',)
assert tests.BoundaryNewDialogCheck3('Edge boundary from segments','<selection>','direction','No edge sequence')
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
checkpoint OOF.SegmentSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(224, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.5131350593289e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.5510000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((73,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Node').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint skeleton selection page groups sensitized
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:NodeAction:Chooser'), 'Select Group')
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:NodeHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.NodeSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from nodes')
assert tests.BoundaryNewDialogCheckGroup0('Point boundary from nodes','<selection>','node','two_nodes','nodegroup')
assert tests.BoundaryNewDialogCheckScope0('Point boundary from nodes')
assert tests.BoundaryNewDialogCheck1('Point boundary from nodes','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.5750000000000e+03)
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
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((74,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint skeleton selection page groups sensitized
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:NodeHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.NodeSelection.Select_Group
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
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.5990000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 125)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from nodes','<selection>','two_nodes','nodegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from nodes','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','direction','-X to +X')
findWidget('Dialog-New Boundary').resize(368, 153)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3000000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3000000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+X to -X')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from nodes','<selection>','two_nodes','nodegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from nodes','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','direction','+X to -X')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3000000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3240000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+Y to -Y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from nodes','<selection>','two_nodes','nodegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from nodes','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','direction','+Y to -Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3240000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3480000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '-Y to +Y')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from nodes','<selection>','two_nodes','nodegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from nodes','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','direction','-Y to +Y')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3480000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3720000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '+Z to -Z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from nodes','<selection>','two_nodes','nodegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from nodes','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','direction','+Z to -Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3720000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3960000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), '-Z to +Z')
assert tests.BoundaryNewDialogCheckGroup0('Edge boundary from nodes','<selection>','two_nodes','nodegroup')
assert tests.BoundaryNewDialogCheckScope0('Edge boundary from nodes','direction','-X to +X','+X to -X','-Y to +Y','+Y to -Y','-Z to +Z','+Z to -Z',)
assert tests.BoundaryNewDialogCheck1('Edge boundary from nodes','<selection>','direction','-Z to +Z')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.3960000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.4000000000000e+01)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2685402373157e+03)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.NodeSelection.Clear
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(200, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.2680000000000e+03)
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((55,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((56,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((57,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((58,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((59,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((60,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
checkpoint boundary page updated
checkpoint boundary page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Selection:NodeHistory:OK').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.NodeSelection.Select_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(368, 153)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from nodes')
assert tests.BoundaryNewDialogCheckGroup0('Point boundary from nodes','<selection>','nodegroup')
assert tests.BoundaryNewDialogCheckScope0('Point boundary from nodes')
assert tests.BoundaryNewDialogCheck1('Point boundary from nodes','<selection>')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.7430000000000e+03)
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 7.0000000000000e+00)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.7670000000000e+03)
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
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(199, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.Delete_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Boundaries')
checkpoint page installed Skeleton Boundaries
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((83,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().unselect_all()
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
