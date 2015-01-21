checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:24 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
findWidget('OOF2 Messages 1').resize(630, 200)
findWidget('OOF2').resize(550, 350)
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(692)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(692)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(692)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(715)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
# Check the text in the zoom factor, should be 1.5
assert tests.gtkTextCompare('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer:Zoom:Factor','1.5')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer:Info').clicked()
# Check tail of messages for text correctness.
assert tests.gtkTextviewTail('OOF2 Messages 1:Text',"Scroll region     :  CRectangle(Coord(0, 0), Coord(100, 100))\n")
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(152)
findWidget('OOF2:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(350, 140)
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
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2:Microstructure Page:Pane').set_position(157)
checkpoint meshable button set
checkpoint microstructure page sensitized
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
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
checkpoint OOF.Microstructure.Create_From_ImageFile
findWidget('OOF2:Microstructure Page:Pane').set_position(157)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer:Info').clicked()
findWidget('OOF2 Messages 1').resize(630, 200)
assert tests.gtkTextviewTail('OOF2 Messages 1:Text',"Scroll region     :  CRectangle(Coord(-7.5, -157.5), Coord(157.5, 7.5))\n")
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5794117647059e+01,y=-1.3485294117647e+02,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5794117647059e+01,y=-1.3485294117647e+02,state=256,window=findCanvasGdkWindow('Graphics_1')))
# Button-release.  Did the click happen correctly?
starting_ppu = tests.getCanvasPPU()
assert tests.gtkMultiTextCompare({'PixelX':'15','PixelY':'134','PhysicalX':'15.79','PhysicalY':'134.9'},'OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer:Zoom:In').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 6.4000000000000e+01)
checkpoint OOF.Graphics_1.Settings.Zoom.In
# Zoomed in once, check pixels per unit.
assert tests.checkCanvasPPU(starting_ppu, 1.5)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0970588235294e+01,y=-7.4676470588235e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.0970588235294e+01,y=-7.4676470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
# Check data.
assert tests.gtkMultiTextCompare({'PixelX':'20','PixelY':'74','PhysicalX':'20.97','PhysicalY':'74.68'},'OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer:Zoom:Out').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 0.0000000000000e+00)
checkpoint OOF.Graphics_1.Settings.Zoom.Out
# Zoomed out, recheck ppu.
assert tests.checkCanvasPPU(starting_ppu, 1.0)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer:Zoom:Out').clicked()
checkpoint OOF.Graphics_1.Settings.Zoom.Out
# Zoomed out again, recheck ppu.
assert tests.checkCanvasPPU(starting_ppu, 0.6666666)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.2450000000000e+02,y=-1.1285294117647e+02,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2450000000000e+02,y=-1.1285294117647e+02,state=256,window=findCanvasGdkWindow('Graphics_1')))
# Check coords on double-zoom-out.
assert tests.gtkMultiTextCompare({'PixelX':'124','PixelY':'112','PhysicalX':'124.5','PhysicalY':'112.9'},'OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer:Zoom:Fill').clicked()
checkpoint OOF.Graphics_1.Settings.Zoom.Fill_Window
# After zoom-fill, recheck ppu.
assert tests.checkCanvasPPU(starting_ppu, 1.0)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6794117647059e+01,y=-7.9205882352941e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6794117647059e+01,y=-7.9205882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# Check coords again.
assert tests.gtkMultiTextCompare({'PixelX':'26','PixelY':'79','PhysicalX':'26.79','PhysicalY':'79.21'},'OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.6794117647059e+01,y=-7.9205882352941e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6794117647059e+01,y=-7.9205882352941e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 6.4000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 6.1000000000000e+01)
checkpoint OOF.Graphics_1.Settings.Zoom.InFocussed
# Shift-click completed, check ppu.
assert tests.checkCanvasPPU(starting_ppu, 1.5)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4421568627451e+01,y=-6.9068627450980e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4421568627451e+01,y=-6.9068627450980e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# Regular click completed, recheck coords.
assert tests.gtkMultiTextCompare({'PixelX':'24','PixelY':'69','PhysicalX':'24.42','PhysicalY':'69.07'},'OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.9715686274510e+01,y=-6.6911764705882e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.9715686274510e+01,y=-6.6911764705882e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 4.0000000000000e+00)
checkpoint OOF.Graphics_1.Settings.Zoom.OutFocussed
# Ctrl-click completed, check ppu again again.
assert tests.checkCanvasPPU(starting_ppu, 1.0)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.9500000000000e+01,y=-6.1088235294118e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.9500000000000e+01,y=-6.1088235294118e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 7.0000000000000e+00)
checkpoint OOF.Graphics_1.Settings.Zoom.OutFocussed
# Second ctrl-click completed.  Ppu.
assert tests.checkCanvasPPU(starting_ppu, 0.66666666)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.2450000000000e+02,y=-6.9176470588235e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2450000000000e+02,y=-6.9176470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
# Regular click completed, check coords.
assert tests.gtkMultiTextCompare({'PixelX':'124','PixelY':'69','PhysicalX':'124.5','PhysicalY':'69.18'},'OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Viewer')
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 71)
findWidget('Dialog-Python_Log:filename').set_text('t')
findWidget('Dialog-Python_Log:filename').set_text('tb')
findWidget('Dialog-Python_Log:filename').set_text('tbo')
findWidget('Dialog-Python_Log:filename').set_text('tbox')
findWidget('Dialog-Python_Log:filename').set_text('tbox.')
findWidget('Dialog-Python_Log:filename').set_text('tbox.l')
findWidget('Dialog-Python_Log:filename').set_text('tbox.lo')
findWidget('Dialog-Python_Log:filename').set_text('tbox.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('tbox.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
