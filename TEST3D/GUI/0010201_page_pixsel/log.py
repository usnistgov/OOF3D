checkpoint toplevel widget mapped OOF3D Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.10 $
# $Author: fyc $
# $Date: 2014/05/22 16:03:33 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.
import tests

findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D Messages 1').resize(540, 200)
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
findWidget('Dialog-Load Image and create Microstructure').resize(401, 215)
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('TEST_DATA/5color')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(603, 200)
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint named analysis chooser set
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint meshable button set
checkpoint Materials page updated
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
checkpoint OOF.Microstructure.Create_From_ImageFile
findWidget('OOF3D').resize(550, 350)
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
checkpoint toplevel widget mapped OOF3D Graphics 1
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Skeleton Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Voxel Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Method:Chooser'), 'Burn')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Method:Burn:global_flammability:entry').set_text('1.4285714285714e-01')
widget_0=findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Method:Burn:global_flammability:entry')
widget_0.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_0.window))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1200000000000e+02,y= 3.1600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1200000000000e+02,y= 3.1600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
widget_1=findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Method:Burn:global_flammability:entry')
widget_1.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_1.window))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5200000000000e+02,y= 2.2900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5200000000000e+02,y= 2.2900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Voxel Selection')
checkpoint page installed Voxel Selection
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(336)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Despeckle')
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(287)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('18')
widget_2=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_2.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_2.window))
widget_3=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_3.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_3.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(2314, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('18')
widget_4=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_4.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_4.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(2314, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('18')
widget_5=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_5.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_5.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(2314, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('18')
widget_6=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_6.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_6.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(2314, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('18')
widget_7=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_7.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_7.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(2314, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('18')
widget_8=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_8.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_8.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(2314, 8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.7500000000000e+02,y= 2.3900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.7500000000000e+02,y= 2.3900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.voxelSelectionPageStatusCheck(0, 8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6800000000000e+02,y= 4.2400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6800000000000e+02,y= 4.2400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.voxelSelectionPageStatusCheck(0, 8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2900000000000e+02,y= 3.7900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2900000000000e+02,y= 3.7900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.voxelSelectionPageStatusCheck(0, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('18')
widget_9=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_9.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_9.window))
widget_10=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_10.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_10.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(0, 8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4100000000000e+02,y= 3.1500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4100000000000e+02,y= 3.1500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.voxelSelectionPageStatusCheck(2313, 8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.5300000000000e+02,y= 2.2800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.5300000000000e+02,y= 2.2800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.voxelSelectionPageStatusCheck(0, 8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6300000000000e+02,y= 4.1600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6300000000000e+02,y= 4.1600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.voxelSelectionPageStatusCheck(0, 8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6500000000000e+02,y= 1.7300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6500000000000e+02,y= 1.7300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.voxelSelectionPageStatusCheck(2385, 8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Elkcepsed')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Elkcepsed
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Undo
assert tests.voxelSelectionPageStatusCheck(2385, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:entry').set_text('7')
widget_11=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:entry')
widget_11.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_11.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.voxelSelectionPageStatusCheck(2370, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Undo
assert tests.voxelSelectionPageStatusCheck(2385, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:entry').set_text('7')
widget_12=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:entry')
widget_12.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_12.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.voxelSelectionPageStatusCheck(2370, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Undo
assert tests.voxelSelectionPageStatusCheck(2385, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:entry').set_text('7')
widget_13=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:entry')
widget_13.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_13.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.voxelSelectionPageStatusCheck(2370, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Undo
assert tests.voxelSelectionPageStatusCheck(2385, 8000)
widget_14=findWidget('OOF3D')
handled_0=widget_14.event(event(gtk.gdk.DELETE,window=widget_14.window))
checkpoint toplevel widget mapped Questioner
postpone if not handled_0: widget_14.destroy()
findWidget('Questioner').resize(359, 91)
findWidget('Questioner:gtk-delete').clicked()
checkpoint OOF.Graphics_1.File.Close
