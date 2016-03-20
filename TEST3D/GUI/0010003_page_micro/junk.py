# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# We test how voxels selection groups are handled in a microstructure.
# Meaning what is the difference between Remove and Clear but also how can we provide some selections:
# graphicaly or by the Voxel Selection Page using a specific mehtod.
# This test is mainly directed to the way that the selections are handle through the voxels group.

import tests

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)

# create a microstructure with loaded files
findWidget('OOF3D:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(401, 215)
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('.')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('..')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../.')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../..')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3D')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DS')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSa')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSan')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSand')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandb')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbo')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5c')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5co')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5col')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5colo')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5color')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Auto').clicked()
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('m')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('mi')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('mic')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('micr')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('micro')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(603, 200)
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint active area status updated
checkpoint pixel page updated
checkpoint mesh bdy page updated
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint meshable button set
checkpoint Materials page updated
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
checkpoint microstructure page sensitized
checkpoint OOF.Microstructure.Create_From_ImageFile

# check that the new group button is sensitized
assert tests.sensitization1()

# open a graphics window
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))

# do some voxels selection
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Voxel Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8490000000000e+02,y= 2.56900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.84900000000000e+02,y= 2.56900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2100000000000e+02,y= 2.4900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2100000000000e+02,y= 2.4900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4000000000000e+02,y= 2.4300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4000000000000e+02,y= 2.4300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7900000000000e+02,y= 2.4600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7900000000000e+02,y= 2.4600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5900000000000e+02,y= 2.4500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5900000000000e+02,y= 2.4500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7700000000000e+02,y= 2.7000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7700000000000e+02,y= 2.7000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8300000000000e+02,y= 2.9600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8300000000000e+02,y= 2.9600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0700000000000e+02,y= 3.1400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0700000000000e+02,y= 3.1400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3100000000000e+02,y= 3.3900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3100000000000e+02,y= 3.3900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8800000000000e+02,y= 2.6600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8800000000000e+02,y= 2.6600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8200000000000e+02,y= 2.9600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8200000000000e+02,y= 2.9600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.6400000000000e+02,y= 3.2100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.6400000000000e+02,y= 3.2100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0600000000000e+02,y= 3.7000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0600000000000e+02,y= 3.7000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.6200000000000e+02,y= 3.7200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.6200000000000e+02,y= 3.7200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8300000000000e+02,y= 3.9600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8300000000000e+02,y= 3.9600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8000000000000e+02,y= 4.2400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8000000000000e+02,y= 4.2400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8200000000000e+02,y= 4.5400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8200000000000e+02,y= 4.5400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0600000000000e+02,y= 4.5400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0600000000000e+02,y= 4.5400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3600000000000e+02,y= 4.5100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3600000000000e+02,y= 4.5100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.6800000000000e+02,y= 4.4900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.6800000000000e+02,y= 4.4900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8800000000000e+02,y= 4.4900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8800000000000e+02,y= 4.4900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8600000000000e+02,y= 3.9500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8600000000000e+02,y= 3.9500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8600000000000e+02,y= 4.2700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8600000000000e+02,y= 4.2700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point

# # create a voxels group
# findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
# checkpoint toplevel widget mapped Dialog-Create new voxel group
# findWidget('Dialog-Create new voxel group').resize(246, 67)
# findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
# findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
# checkpoint meshable button set
# checkpoint meshable button set
# checkpoint microstructure page sensitized
# checkpoint skeleton selection page groups sensitized
# checkpoint OOF.PixelGroup.New
# checkpoint microstructure page sensitized
# checkpoint meshable button set

# # A group has been created in micro, but no voxels have been added
# assert tests.sensitization3()
# assert tests.meshableCheck(1)
# assert tests.voxelGroupListCheck('pixelgroup (0 voxels, meshable)')
# assert tests.selectedGroupCheck('pixelgroup (0 voxels, meshable)')

# # create another voxels group
# findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
# checkpoint toplevel widget mapped Dialog-Create new voxel group
# findWidget('Dialog-Create new voxel group').resize(246, 67)
# findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
# checkpoint meshable button set
# checkpoint meshable button set
# checkpoint microstructure page sensitized
# checkpoint skeleton selection page groups sensitized
# checkpoint OOF.PixelGroup.New

# # another group has been created but still no added voxels
# assert tests.meshableCheck(1)
# assert tests.voxelGroupListCheck('pixelgroup (0 voxels, meshable)',                                  'pixelgroup<2> (0 voxels, meshable)')
# assert tests.selectedGroupCheck('pixelgroup<2> (0 voxels, meshable)')

# # select the first created voxels group
# findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((0,))
# checkpoint microstructure page sensitized
# checkpoint meshable button set

# # add the voxel selection the first create voxels group
# findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
# checkpoint meshable button set
# checkpoint meshable button set
# checkpoint microstructure page sensitized
# checkpoint OOF.PixelGroup.AddSelection


# # do some more voxels selection
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0600000000000e+02,y= 3.2500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0600000000000e+02,y= 3.2500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.3300000000000e+02,y= 3.5000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.3300000000000e+02,y= 3.5000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0800000000000e+02,y= 3.7800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0800000000000e+02,y= 3.7800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.5900000000000e+02,y= 3.7700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.5900000000000e+02,y= 3.7700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.6200000000000e+02,y= 3.2400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.6200000000000e+02,y= 3.2400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8600000000000e+02,y= 3.0900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8600000000000e+02,y= 3.0900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:TBScroll:Voxel Selection:Undo').clicked()
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Undo
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8000000000000e+02,y= 3.0100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8000000000000e+02,y= 3.0100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.1600000000000e+02,y= 2.9200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.1600000000000e+02,y= 2.9200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8900000000000e+02,y= 3.9300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8900000000000e+02,y= 3.9300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.1300000000000e+02,y= 3.9500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.1300000000000e+02,y= 3.9500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3600000000000e+02,y= 3.9700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3600000000000e+02,y= 3.9700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3500000000000e+02,y= 2.9400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3500000000000e+02,y= 2.9400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.4400000000000e+02,y= 3.1700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4400000000000e+02,y= 3.1700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.4200000000000e+02,y= 3.4900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4200000000000e+02,y= 3.4900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.4000000000000e+02,y= 3.7400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.4000000000000e+02,y= 3.7400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5700000000000e+02,y= 3.2200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5700000000000e+02,y= 3.2200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2000000000000e+02,y= 3.4300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2000000000000e+02,y= 3.4300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5000000000000e+02,y= 3.7700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5000000000000e+02,y= 3.7700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0200000000000e+02,y= 3.6900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.0200000000000e+02,y= 3.6900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9800000000000e+02,y= 3.2100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.9800000000000e+02,y= 3.2100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7300000000000e+02,y= 2.9900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7300000000000e+02,y= 2.9900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8100000000000e+02,y= 3.9400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8100000000000e+02,y= 3.9400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5400000000000e+02,y= 4.0000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5400000000000e+02,y= 4.0000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.2600000000000e+02,y= 3.9900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2600000000000e+02,y= 3.9900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5300000000000e+02,y= 2.9400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5300000000000e+02,y= 2.9400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.2200000000000e+02,y= 2.9500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2200000000000e+02,y= 2.9500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.2400000000000e+02,y= 3.7600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2400000000000e+02,y= 3.7600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.2300000000000e+02,y= 3.4200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2300000000000e+02,y= 3.4200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.2400000000000e+02,y= 3.1800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
# canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
# canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.2400000000000e+02,y= 3.1800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point

# # select the second voxels group
# findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((1,))
# checkpoint microstructure page sensitized
# checkpoint meshable button set

# # now the current select voxels group has some voxels selection added
# assert tests.meshableCheck(1)
# assert tests.voxelGroupListCheck('pixelgroup (23 voxels, meshable)',                                  'pixelgroup<2> (0 voxels, meshable)')
# assert tests.selectedGroupCheck('pixelgroup<2> (0 voxels, meshable)')
# assert tests.sensitization3()

# # add the new selection to the select voxels group
# findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
# checkpoint meshable button set
# checkpoint meshable button set
# checkpoint microstructure page sensitized
# checkpoint OOF.PixelGroup.AddSelection

# # now the two created voxels groups have some voxels selection added
# assert tests.meshableCheck(1)
# assert tests.voxelGroupListCheck('pixelgroup (23 voxels, meshable)',                                  'pixelgroup<2> (51 voxels, meshable)')
# assert tests.selectedGroupCheck('pixelgroup<2> (51 voxels, meshable)')
# assert tests.sensitization4()

# # undo the last added voxels
# findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:TBScroll:Voxel Selection:Undo').clicked()
# checkpoint microstructure page sensitized
# checkpoint pixel page updated
# checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Undo
