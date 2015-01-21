# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

# We will test how two microstructures can be handled.
# This means visually in the Graphics window by creating layersNumberCheck.
# It means also the separation between each voxels groups and the operation on them too.

import tests

checkpoint toplevel widget mapped OOF3D
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)

# create a microstructure micro1
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
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('micro1')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(603, 200)
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
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
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Voxel Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8500000000000e+02,y= 2.6700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8500000000000e+02,y= 2.6700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.1300000000000e+02,y= 2.6700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.1300000000000e+02,y= 2.6700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5600000000000e+02,y= 2.6900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5600000000000e+02,y= 2.6900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0300000000000e+02,y= 2.6400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0300000000000e+02,y= 2.6400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.3300000000000e+02,y= 2.6700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.3300000000000e+02,y= 2.6700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7500000000000e+02,y= 3.0200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7500000000000e+02,y= 3.0200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0300000000000e+02,y= 3.2100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0300000000000e+02,y= 3.2100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3000000000000e+02,y= 3.2000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3000000000000e+02,y= 3.2000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5400000000000e+02,y= 3.2000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5400000000000e+02,y= 3.2000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8500000000000e+02,y= 3.1700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8500000000000e+02,y= 3.1700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0900000000000e+02,y= 3.1800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0900000000000e+02,y= 3.1800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.3300000000000e+02,y= 3.0000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.3300000000000e+02,y= 3.0000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point

# create another mircostructure micro2
findWidget('OOF3D:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(401, 215)
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('micro')
findWidget('Dialog-Load Image and create Microstructure:microstructure_name:Text').set_text('micro2')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
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
assert tests.microstructureListCheck('micro1', 'micro2')
assert tests.microstructureCheck('micro2')


# create a layer for the second microstructure micro2
findMenu(findWidget('OOF3D Graphics 1:MenuBar'), 'Layer:New').activate()
checkpoint toplevel widget mapped Dialog-New
findWidget('Dialog-New').resize(291, 191)
setComboBox(findWidget('Dialog-New:what:Microstructure'), 'micro2')
findWidget('Dialog-New:gtk-ok').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 704))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 704))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 693))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 693))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 686))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 686))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 681))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 681))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 674))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 674))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 663))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 663))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 658))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 658))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 650))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 650))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 643))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 643))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 638))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 638))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 631))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 631))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 626))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 626))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 623))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 623))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 622))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 622))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 619))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 619))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 616))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 616))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 612))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 612))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 610))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 610))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 609))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 609))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 607))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 607))

# check that there is exactly two layers
assert tests.layersNumberCheck() == 2

# create voxels selection group in micro2
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New

# A group has been created in micro2, but no voxels have been added
assert tests.sensitization2()
assert tests.meshableCheck(1)
assert tests.voxelGroupListCheck('pixelgroup (0 voxels, meshable)')
assert tests.selectedGroupCheck('pixelgroup (0 voxels, meshable)')

checkpoint microstructure page sensitized
checkpoint meshable button set
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9000000000000e+02,y= 1.9700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9000000000000e+02,y= 1.9700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.2800000000000e+02,y= 1.8200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.2800000000000e+02,y= 1.8200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7500000000000e+02,y= 1.8600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7500000000000e+02,y= 1.8600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2200000000000e+02,y= 1.8500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.2200000000000e+02,y= 1.8500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9200000000000e+02,y= 2.1100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9200000000000e+02,y= 2.1100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9300000000000e+02,y= 2.3500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9300000000000e+02,y= 2.3500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.3000000000000e+02,y= 2.2800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.3000000000000e+02,y= 2.2800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.7700000000000e+02,y= 2.3100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.7700000000000e+02,y= 2.3100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.1900000000000e+02,y= 2.2900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.1900000000000e+02,y= 2.2900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.6200000000000e+02,y= 1.8600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.6200000000000e+02,y= 1.8600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.6400000000000e+02,y= 2.1100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.6400000000000e+02,y= 2.1100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.7000000000000e+02,y= 2.2800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.7000000000000e+02,y= 2.2800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0800000000000e+02,y= 2.4600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0800000000000e+02,y= 2.4600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.6000000000000e+02,y= 2.4900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.6000000000000e+02,y= 2.4900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0000000000000e+02,y= 2.4600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0000000000000e+02,y= 2.4600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.4400000000000e+02,y= 2.4900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.4400000000000e+02,y= 2.4900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0500000000000e+02,y= 1.5700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0500000000000e+02,y= 1.5700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5400000000000e+02,y= 1.6300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5400000000000e+02,y= 1.6300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.9800000000000e+02,y= 1.5700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.9800000000000e+02,y= 1.5700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.4500000000000e+02,y= 1.5900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.4500000000000e+02,y= 1.5900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Select.Point
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection

# checking the micro2 voxels selection groups
assert tests.meshableCheck(1)
assert tests.voxelGroupListCheck('pixelgroup (20 voxels, meshable)')
assert tests.selectedGroupCheck('pixelgroup (20 voxels, meshable)')
assert tests.sensitization3()

# select the first microstructure micro1
setComboBox(findWidget('OOF3D:Microstructure Page:Microstructure'), 'micro1')
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
findWidget('OOF3D Graphics 1').resize(1000, 801)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
findWidget('OOF3D Graphics 1').resize(1000, 803)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 610))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 610))
findWidget('OOF3D Graphics 1').resize(1000, 812)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 619))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 619))
findWidget('OOF3D Graphics 1').resize(1000, 823)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 630))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 630))
findWidget('OOF3D Graphics 1').resize(1000, 825)
findWidget('OOF3D Graphics 1:Pane0:Pane1:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 632))
findWidget('OOF3D Graphics 1:Pane0:Pane1').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 632))
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '13')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((13,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Hide
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '12')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((12,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Hide
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '13')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((13,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Show

# create a voxels selection group for micro1
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New
checkpoint microstructure page sensitized
checkpoint meshable button set

# add the selection already made on the micro1 layer in graphics to this voxels group
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection
setComboBox(findWidget('OOF3D:Microstructure Page:Microstructure'), 'micro2')
checkpoint meshable button set
checkpoint microstructure page sensitized

# checking the micro2 voxels selection groups
assert tests.meshableCheck(1)
assert tests.voxelGroupListCheck('pixelgroup (20 voxels, meshable)')
assert tests.selectedGroupCheck('pixelgroup (20 voxels, meshable)')
assert tests.sensitization3()

# select the first created microstructure
setComboBox(findWidget('OOF3D:Microstructure Page:Microstructure'), 'micro1')
checkpoint meshable button set
checkpoint microstructure page sensitized

# checking the micro1 voxels selection groups
assert tests.meshableCheck(1)
assert tests.voxelGroupListCheck('pixelgroup (12 voxels, meshable)')
assert tests.selectedGroupCheck('pixelgroup (12 voxels, meshable)')
assert tests.sensitization3()

# select back the second created microstructure
setComboBox(findWidget('OOF3D:Microstructure Page:Microstructure'), 'micro2')
checkpoint meshable button set
checkpoint microstructure page sensitized

# checking the micro2 voxels selection groups
assert tests.meshableCheck(1)
assert tests.voxelGroupListCheck('pixelgroup (20 voxels, meshable)')
assert tests.selectedGroupCheck('pixelgroup (20 voxels, meshable)')
assert tests.sensitization3()

# delete the micro2 layer
findMenu(findWidget('OOF3D Graphics 1:MenuBar'), 'Layer:Delete').activate()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Delete

# check that there is just one layer remaining.
assert tests.layersNumberCheck() == 1

findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '12')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((12,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Show

# delete the microstructure micro2
findWidget('OOF3D:Microstructure Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint microstructure page sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
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
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Microstructure.Delete

assert tests.microstructureListCheck('micro1')
assert tests.microstructureCheck('micro1')

# save a python script log
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('m')
findWidget('Dialog-Python_Log:filename').set_text('me')
findWidget('Dialog-Python_Log:filename').set_text('mes')
findWidget('Dialog-Python_Log:filename').set_text('mesh')
findWidget('Dialog-Python_Log:filename').set_text('mesha')
findWidget('Dialog-Python_Log:filename').set_text('meshab')
findWidget('Dialog-Python_Log:filename').set_text('meshabl')
findWidget('Dialog-Python_Log:filename').set_text('meshable')
findWidget('Dialog-Python_Log:filename').set_text('meshable.')
findWidget('Dialog-Python_Log:filename').set_text('meshable.l')
findWidget('Dialog-Python_Log:filename').set_text('meshable.lo')
findWidget('Dialog-Python_Log:filename').set_text('meshable.log')
findWidget('Dialog-Python_Log').resize(198, 95)
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log

# quit OOF3D
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
checkpoint OOF.Graphics_1.File.Close
