# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.9 $
# $Author: fyc $
# $Date: 2014/09/19 22:52:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Voxel Selection')
checkpoint page installed Voxel Selection
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(336)
assert tests.sensitization0()
assert tests.voxelSelectionPageNoMSCheck()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(401, 215)
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('TEST_DATA/5color')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Auto').clicked()
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('1')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('1.')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('1.0')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(603, 200)
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint meshable button set
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint microstructure page sensitized
checkpoint OOF.Microstructure.Create_From_ImageFile
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
findWidget('OOF3D Graphics 1').resize(1000, 800)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
findWidget('OOF3D Graphics 1').resize(1000, 800)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Voxel Selection')
assert tests.voxelSelectionPageStatusCheck(0, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 0)
assert tests.sensitization1()
checkpoint page installed Voxel Selection
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(336)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Voxel Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Method:Chooser'), 'Burn')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3400000000000e+02,y= 2.7600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3400000000000e+02,y= 2.7600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
assert tests.voxelSelectionPageStatusCheck(2313, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 2313)
assert tests.sensitization2()
findWidget('OOF3D Graphics 1').resize(1000, 800)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:name:Auto').clicked()
findWidget('Dialog-Create new voxel group:name:Text').set_text('l')
findWidget('Dialog-Create new voxel group:name:Text').set_text('lo')
findWidget('Dialog-Create new voxel group:name:Text').set_text('low')
findWidget('Dialog-Create new voxel group:name:Text').set_text('lowe')
findWidget('Dialog-Create new voxel group:name:Text').set_text('lower')
findWidget('Dialog-Create new voxel group:name:Text').set_text('lowerl')
findWidget('Dialog-Create new voxel group:name:Text').set_text('lowerle')
findWidget('Dialog-Create new voxel group:name:Text').set_text('lowerlef')
findWidget('Dialog-Create new voxel group:name:Text').set_text('lowerleft')
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New
checkpoint microstructure page sensitized
checkpoint meshable button set
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Voxel Selection')
checkpoint page installed Voxel Selection
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Invert
assert tests.voxelSelectionPageStatusCheck(5687, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 5687)
assert tests.sensitization2()
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Undo
assert tests.voxelSelectionPageStatusCheck(2313, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 2313)
assert tests.sensitization3()
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Clear').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Clear
assert tests.voxelSelectionPageStatusCheck(0, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 0)
assert tests.sensitization4()
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Group')
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(328)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Group
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
assert tests.voxelSelectionPageStatusCheck(2313, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 2313)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7800000000000e+02,y= 9.4000000000000e+01,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7800000000000e+02,y= 9.4000000000000e+01,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Burn
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:name:Text').set_text('')
findWidget('Dialog-Create new voxel group:name:Text').set_text('u')
findWidget('Dialog-Create new voxel group:name:Text').set_text('up')
findWidget('Dialog-Create new voxel group:name:Text').set_text('upp')
findWidget('Dialog-Create new voxel group:name:Text').set_text('uppe')
findWidget('Dialog-Create new voxel group:name:Text').set_text('upper')
findWidget('Dialog-Create new voxel group:name:Text').set_text('upperl')
findWidget('Dialog-Create new voxel group:name:Text').set_text('upperle')
findWidget('Dialog-Create new voxel group:name:Text').set_text('upperlef')
findWidget('Dialog-Create new voxel group:name:Text').set_text('upperleft')
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Voxel Selection')
checkpoint page installed Voxel Selection
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Group
assert tests.voxelSelectionPageStatusCheck(3518, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 3518)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Group:operator:Chooser'), 'Unselect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Group
assert tests.voxelSelectionPageStatusCheck(1205, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 1205)
findWidget('OOF3D Graphics 1').resize(1000, 800)
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Method:Chooser'), 'Point')
findWidget('OOF3D').resize(550, 350)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8900000000000e+02,y= 1.6800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8900000000000e+02,y= 1.6800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0700000000000e+02,y= 1.7600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.0700000000000e+02,y= 1.7600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1600000000000e+02,y= 1.5500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1600000000000e+02,y= 1.5500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3200000000000e+02,y= 1.5800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3200000000000e+02,y= 1.5800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4300000000000e+02,y= 1.6000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4300000000000e+02,y= 1.6000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6500000000000e+02,y= 1.5700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6500000000000e+02,y= 1.5700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8000000000000e+02,y= 1.6100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8000000000000e+02,y= 1.6100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9800000000000e+02,y= 1.5800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9800000000000e+02,y= 1.5800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1700000000000e+02,y= 1.6100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1700000000000e+02,y= 1.6100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3100000000000e+02,y= 1.5900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3100000000000e+02,y= 1.5900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4200000000000e+02,y= 1.6100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4200000000000e+02,y= 1.6100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5200000000000e+02,y= 1.6100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5200000000000e+02,y= 1.6100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2900000000000e+02,y= 1.8000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2900000000000e+02,y= 1.8000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2300000000000e+02,y= 1.9100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2300000000000e+02,y= 1.9100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2200000000000e+02,y= 2.0500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2200000000000e+02,y= 2.0500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2100000000000e+02,y= 2.2200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2100000000000e+02,y= 2.2200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3600000000000e+02,y= 2.2100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3600000000000e+02,y= 2.2100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5200000000000e+02,y= 2.1900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5200000000000e+02,y= 2.1900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5500000000000e+02,y= 2.0700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5500000000000e+02,y= 2.0700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6400000000000e+02,y= 2.0200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6400000000000e+02,y= 2.0200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8500000000000e+02,y= 2.0500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8500000000000e+02,y= 2.0500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8700000000000e+02,y= 2.1700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8700000000000e+02,y= 2.1700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8200000000000e+02,y= 2.3100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8200000000000e+02,y= 2.3100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8000000000000e+02,y= 2.4900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8000000000000e+02,y= 2.4900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7000000000000e+02,y= 2.6200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7000000000000e+02,y= 2.6200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5100000000000e+02,y= 2.7400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5100000000000e+02,y= 2.7400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1500000000000e+02,y= 2.0500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1500000000000e+02,y= 2.0500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1400000000000e+02,y= 2.1800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1400000000000e+02,y= 2.1800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1300000000000e+02,y= 2.3400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1300000000000e+02,y= 2.3400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1000000000000e+02,y= 2.5000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1000000000000e+02,y= 2.5000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2700000000000e+02,y= 2.6400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2700000000000e+02,y= 2.6400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3500000000000e+02,y= 2.8000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3500000000000e+02,y= 2.8000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Undo
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4300000000000e+02,y= 2.8000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4300000000000e+02,y= 2.8000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2600000000000e+02,y= 2.0800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2600000000000e+02,y= 2.0800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4400000000000e+02,y= 2.0600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4400000000000e+02,y= 2.0600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5400000000000e+02,y= 2.0700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5400000000000e+02,y= 2.0700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5700000000000e+02,y= 2.1600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5700000000000e+02,y= 2.1600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Undo
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Selection:Undo').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Undo
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4100000000000e+02,y= 2.2000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4100000000000e+02,y= 2.2000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5200000000000e+02,y= 2.2000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5200000000000e+02,y= 2.2000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5900000000000e+02,y= 2.1800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5900000000000e+02,y= 2.1800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7400000000000e+02,y= 2.2100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7400000000000e+02,y= 2.2100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7400000000000e+02,y= 2.0900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7400000000000e+02,y= 2.0900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7600000000000e+02,y= 1.9000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7600000000000e+02,y= 1.9000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7500000000000e+02,y= 1.7500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7500000000000e+02,y= 1.7500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8600000000000e+02,y= 1.7000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8600000000000e+02,y= 1.7000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.9600000000000e+02,y= 1.7200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.9600000000000e+02,y= 1.7200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.9900000000000e+02,y= 1.7200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.9900000000000e+02,y= 1.7200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
assert tests.pixelSelectionSizeCheck('1.0', 1235)
assert tests.voxelSelectionPageStatusCheck(1235, 8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Group:operator:Chooser'), 'Intersect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Group
assert tests.voxelSelectionPageStatusCheck(0, 8000)
assert tests.pixelSelectionSizeCheck('1.0', 0)
assert tests.sensitization5()
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Region')
findWidget('OOF3D').resize(550, 411)
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(264)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:xComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:xComponenent').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:yComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:yComponenent').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:zComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:zComponenent').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(64, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:zComponenent').set_text('42.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(320, 8000)
findWidget('OOF3D').resize(550, 411)
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7700000000000e+02,y= 9.4000000000000e+01,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8200000000000e+02,y= 8.9000000000000e+01,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8200000000000e+02,y= 8.9000000000000e+01,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:xComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:xComponenent').set_text('5.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:yComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:yComponenent').set_text('5.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:zComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:zComponenent').set_text('0.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:xComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:xComponenent').set_text('1.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:yComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:yComponenent').set_text('1.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:zComponenent').set_text('10.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(390, 8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Intersect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(15, 8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Select Only')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:zComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:zComponenent').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:zComponenent').set_text('42.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:zComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:zComponenent').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:zComponenent').set_text('42.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0, 8000)
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5400000000000e+02,y= 1.9500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0200000000000e+02,y= 2.1800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.0200000000000e+02,y= 2.1800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Unselect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0, 8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:yComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:yComponenent').set_text('1.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:yComponenent').set_text('10.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:xComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:xComponenent').set_text('1.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point0:xComponenent').set_text('10.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0600000000000e+02,y= 2.1600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0800000000000e+02,y= 2.1500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0800000000000e+02,y= 2.1500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:xComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:xComponenent').set_text('0.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:yComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:yComponenent').set_text('0.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:zComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Box:point1:zComponenent').set_text('0.0')
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Select Only')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8600000000000e+02,y= 2.0200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5700000000000e+02,y= 1.9100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.4000000000000e+01,y= 1.8500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.0100000000000e+02,y= 1.9200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1400000000000e+02,y= 1.9400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5400000000000e+02,y= 2.0300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5400000000000e+02,y= 2.0300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Unselect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0, 8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Chooser'), 'Circle')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:center:zComponenent').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:center:zComponenent').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:center:zComponenent').set_text('42.0')
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Select')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0, 8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7200000000000e+02,y= 1.5100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2100000000000e+02,y= 1.5500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.2100000000000e+02,y= 1.5500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('1.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('10.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('0.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('20.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('0.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('30.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3200000000000e+02,y= 1.9100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2400000000000e+02,y= 1.7800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.4400000000000e+02,y= 2.3500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.5400000000000e+02,y= 2.4400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5400000000000e+02,y= 2.4400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0000000000000e+02,y= 2.4800000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7200000000000e+02,y= 2.7600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7200000000000e+02,y= 2.7600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0400000000000e+02,y= 3.1400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6200000000000e+02,y= 2.6900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.6200000000000e+02,y= 2.6900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7500000000000e+02,y= 2.5600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8100000000000e+02,y= 2.7900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8100000000000e+02,y= 2.7900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8100000000000e+02,y= 2.7900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8100000000000e+02,y= 2.6700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8100000000000e+02,y= 2.6700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('3.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Circle:radius').set_text('32.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.6400000000000e+02,y= 2.5900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.5500000000000e+02,y= 2.8700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5500000000000e+02,y= 2.8700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
assert tests.voxelSelectionPageStatusCheck(2193,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Intersect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(24,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Select Only')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(2193,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Unselect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Chooser'), 'Ellipse')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Ellipse:point1:zComponenent').set_text('42.0')
assert tests.voxelSelectionPageStatusCheck(0,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Select')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0,8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:shape:Ellipse:point1:yComponenent').set_text('10.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Intersect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Select Only')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Region:operator:Chooser'), 'Unselect')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Region
assert tests.voxelSelectionPageStatusCheck(0,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Despeckle')
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(287)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 1.4676923076923e+01)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 1.4676923076923e+01)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(0,8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 1.5415384615385e+01)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 2.6000000000000e+01)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(0,8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('2.2061538461538e+01')
widget_0=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_0.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_0.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('2.6000000000000e+01')
widget_1=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_1.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_1.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9400000000000e+02,y= 1.7300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0100000000000e+02,y= 1.6000000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0100000000000e+02,y= 1.6000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry').set_text('1.0000000000000e+01')
widget_2=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:entry')
widget_2.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_2.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(0,8000)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 1.0246153846154e+01)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Despeckle:neighbors:slider').get_adjustment().set_value( 1.8861538461538e+01)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Despeckle
assert tests.voxelSelectionPageStatusCheck(0,8000)
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Elkcepsed')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 8.9384615384615e+00)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.3000000000000e+01)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.voxelSelectionPageStatusCheck(0,8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8800000000000e+02,y= 1.5100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2600000000000e+02,y= 8.2000000000000e+01,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.2600000000000e+02,y= 8.2000000000000e+01,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.2261538461538e+01)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.voxelSelectionPageStatusCheck(0,8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9400000000000e+02,y= 1.3200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.4400000000000e+02,y= 1.2600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4400000000000e+02,y= 1.2600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 1.1846153846154e+00)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Elkcepsed:neighbors:slider').get_adjustment().set_value( 6.3538461538462e+00)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Elkcepsed
assert tests.voxelSelectionPageStatusCheck(0,8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5400000000000e+02,y= 3.0600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9400000000000e+02,y= 2.6500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.9400000000000e+02,y= 2.6500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Expand')
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(336)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Expand
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8200000000000e+02,y= 2.9900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3900000000000e+02,y= 3.2300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.3900000000000e+02,y= 3.2300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Shrink')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Shrink
assert tests.voxelSelectionPageStatusCheck(0,8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4800000000000e+02,y= 2.0200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4200000000000e+02,y= 2.6300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.4200000000000e+02,y= 2.6300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('1.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Shrink
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('2.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('20.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Shrink
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3600000000000e+02,y= 1.4900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9200000000000e+02,y= 1.5700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.9200000000000e+02,y= 1.5700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('0.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('30.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Shrink
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7100000000000e+02,y= 2.0600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1800000000000e+02,y= 2.0400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.1700000000000e+02,y= 2.0400000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('3.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('4.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Shrink:radius').set_text('42.0')
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Shrink
assert tests.voxelSelectionPageStatusCheck(0,8000)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1000000000000e+02,y= 1.5400000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])

window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1400000000000e+02,y= 1.3500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.1400000000000e+02,y= 1.3500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Chooser'), 'Color Range')
findWidget('OOF3D').resize(550, 505)
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(175)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Red:entry').set_text('1.0000000000000e+00')
widget_3=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Red:entry')
widget_3.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_3.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:entry').set_text('1.0000000000000e+00')
widget_4=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:entry')
widget_4.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_4.window))
widget_5=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Blue:entry')
widget_5.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_5.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Red:entry').set_text('1.0000000000000e-02')
widget_6=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Red:entry')
widget_6.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_6.window))
widget_7=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Red:entry')
widget_7.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_7.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Green:entry').set_text('1.0000000000000e-02')
widget_8=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Green:entry')
widget_8.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_8.window))
widget_9=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Green:entry')
widget_9.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_9.window))
widget_10=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Red:entry')
widget_10.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_10.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Green:slider').get_adjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:reference:RGBColor:Red:slider').get_adjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_red:entry').set_text('1.0000000000000e-02')
widget_11=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_red:entry')
widget_11.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_11.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_green:entry').set_text('1.0000000000000e-02')
widget_12=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_green:entry')
widget_12.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_12.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_blue:entry').set_text('1.0000000000000e-02')
widget_13=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_blue:entry')
widget_13.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_13.window))
widget_14=findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:Method:Color Range:range:DeltaRGB:delta_blue:entry')
widget_14.event(event(gtk.gdk.FOCUS_CHANGE, in_=0, window=widget_14.window))
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Color_Range
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4200000000000e+02,y= 1.2500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8000000000000e+02,y= 2.1100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 396)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8000000000000e+02,y= 2.1100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 430))
checkpoint OOF.Graphics_1.Settings.Camera.View
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy microstructure
findWidget('Dialog-Copy microstructure').resize(246, 67)
findWidget('Dialog-Copy microstructure:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
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
checkpoint OOF.Microstructure.Copy
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Voxel Selection')
checkpoint page installed Voxel Selection
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
findWidget('OOF3D:Skeleton Page:Pane').set_position(199)
findWidget('OOF3D').resize(601, 505)
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
checkpoint skeleton page sensitized
findWidget('OOF3D:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(380, 191)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(246)
findWidget('OOF3D:Microstructure Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(225, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint microstructure page sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint Field page sensitized
##checkpoint skeleton page sensitized
checkpoint OOF.Microstructure.Delete
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('pixsel.log')
findWidget('Dialog-Python_Log').resize(198, 95)
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('pixsel.log')
widget_15=findWidget('OOF3D')
handled_0=widget_15.event(event(gtk.gdk.DELETE,window=widget_15.window))
