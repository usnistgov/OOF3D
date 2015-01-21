checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:04 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests, os
tbox = 'OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pin Nodes'
findWidget('OOF2 Messages 1').resize(630, 200)
findWidget('OOF2').resize(550, 350)
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Pin Nodes')
checkpoint Graphics_1 Pin Nodes updated

# Pin nodes toolbox selected.

assert tests.gtkMultiTextCompare({'Mouse X':'','Mouse Y':'','Node X':'','Node Y':''},tbox)
assert findWidget(tbox+":Pin Label").get_text()==''
assert findWidget(tbox+":Status").get_text()=='0 nodes pinned.'
assert tests.sensitizationCheck({'Undo':False,'Invert':False,'Redo':False,'UnPinAll':False},tbox)

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(194, 71)
findWidget('Dialog-Data:filename').set_text('.')
findWidget('Dialog-Data:filename').set_text('..')
findWidget('Dialog-Data:filename').set_text('../')
findWidget('Dialog-Data:filename').set_text('../.')
findWidget('Dialog-Data:filename').set_text('../..')
findWidget('Dialog-Data:filename').set_text('../../')
findWidget('Dialog-Data:filename').set_text('../../e')
findWidget('Dialog-Data:filename').set_text('../../ex')
findWidget('Dialog-Data:filename').set_text('../../exa')
findWidget('Dialog-Data:filename').set_text('../../exam')
findWidget('Dialog-Data:filename').set_text('../../examp')
findWidget('Dialog-Data:filename').set_text('../../exampl')
findWidget('Dialog-Data:filename').set_text('../../example')
findWidget('Dialog-Data:filename').set_text('../../examples')
findWidget('Dialog-Data:filename').set_text('../../examples/')
findWidget('Dialog-Data:filename').set_text('../../examples/t')
findWidget('Dialog-Data:filename').set_text('../../examples/tr')
findWidget('Dialog-Data:filename').set_text('../../examples/tri')
findWidget('Dialog-Data:filename').set_text('../../examples/tria')
findWidget('Dialog-Data:filename').set_text('../../examples/trian')
findWidget('Dialog-Data:filename').set_text('../../examples/triang')
findWidget('Dialog-Data:filename').set_text('../../examples/triangl')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.s')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.sk')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.ske')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skel')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skele')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skelet')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skeleto')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
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
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint interface page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
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
checkpoint Graphics_1 Pin Nodes updated
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.File.Load.Data
findWidget('OOF2 Activity Viewer').resize(400, 300)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
# checkpoint Graphics_1 Pin Nodes updated
# checkpoint Graphics_1 Pin Nodes updated
# checkpoint Graphics_1 Pin Nodes updated

# Skeleton loaded.
assert tests.gtkMultiTextCompare({'Mouse X':'','Mouse Y':'','Node X':'','Node Y':''},tbox)
assert findWidget(tbox+":Pin Label").get_text()==''
assert findWidget(tbox+":Status").get_text()=='0 nodes pinned.'
assert tests.sensitizationCheck({'Undo':False,'Invert':True,'Redo':False,'UnPinAll':False},tbox)

findWidget('OOF2 Graphics 1').resize(800, 400)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-4.1372549019608e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-3.7058823529412e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-2.8431372549020e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-2.4117647058824e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-1.5490196078431e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-1.1176470588235e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7647058823529e-01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.0784313725490e-01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.4705882352941e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3333333333333e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7647058823529e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1960784313725e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0588235294118e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4901960784314e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.9215686274510e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3529411764706e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.7843137254902e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2156862745098e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6470588235294e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0784313725490e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.5098039215686e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9411764705882e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8039215686274e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.2352941176471e+00,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.0098039215686e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.0960784313725e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event

# Half-way there, by line-count.
assert tests.gtkMultiTextCompare({'Mouse X':'10.96','Mouse Y':'46.33','Node X':'13','Node Y':'37.5'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='0 nodes pinned.'
assert tests.sensitizationCheck({'Undo':False,'Invert':True,'Redo':False,'UnPinAll':False},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.1392156862745e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.1823529411765e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.2254901960784e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3117647058824e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3549019607843e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3980392156863e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.4411764705882e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.4843137254902e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.5274509803922e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.5705882352941e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.5705882352941e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.6137254901961e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.6568627450980e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7000000000000e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7431372549020e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7862745098039e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8294117647059e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8725490196078e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9156862745098e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9588235294118e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0019607843137e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0450980392157e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0882352941176e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1313725490196e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1745098039216e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2176470588235e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2607843137255e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event

# Arrived at node.
assert tests.gtkMultiTextCompare({'Mouse X':'22.61','Mouse Y':'45.47','Node X':'22','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='0 nodes pinned.'
assert tests.sensitizationCheck({'Undo':False,'Invert':True,'Redo':False,'UnPinAll':False},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2607843137255e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2607843137255e+01,y=-4.5470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox up event
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.Pin
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Pinned node.
assert tests.gtkMultiTextCompare({'Mouse X':'22.61','Mouse Y':'45.47','Node X':'22','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='pinned'
assert findWidget(tbox+":Status").get_text()=='1 node pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3039215686275e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3470588235294e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3901960784314e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4333333333333e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4764705882353e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5196078431373e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5627450980392e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.6058823529412e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.6490196078431e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.6921568627451e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7352941176471e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7784313725490e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8215686274510e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8647058823529e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9078431372549e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9509803921569e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9941176470588e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0372549019608e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0803921568627e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1235294117647e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.1666666666667e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2098039215686e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2529411764706e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2960784313725e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.3392156862745e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.3823529411765e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.4254901960784e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.4686274509804e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.5117647058824e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event

# Arrived at next node.
assert tests.gtkMultiTextCompare({'Mouse X':'35.12','Mouse Y':'45.47','Node X':'37.5','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='1 node pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5117647058824e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5117647058824e+01,y=-4.5470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox up event
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.Pin
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Pinned it.
assert tests.gtkMultiTextCompare({'Mouse X':'35.12','Mouse Y':'45.47','Node X':'37.5','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='pinned'
assert findWidget(tbox+":Status").get_text()=='2 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.5549019607843e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6411764705882e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6843137254902e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.7705882352941e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8137254901961e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.9000000000000e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0294117647059e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0725490196078e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.1588235294118e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2019607843137e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2450980392157e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2882352941176e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3313725490196e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3745098039216e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4176470588235e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4607843137255e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5039215686275e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5470588235294e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5901960784314e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6333333333333e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7196078431373e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7627450980392e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8058823529412e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8490196078431e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8921568627451e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.9352941176471e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.9784313725490e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0215686274510e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0647058823529e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1078431372549e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1509803921569e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1941176470588e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2372549019608e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1941176470588e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1509803921569e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1078431372549e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0647058823529e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event

# Arrived at third node.
assert tests.gtkMultiTextCompare({'Mouse X':'50.65','Mouse Y':'45.9','Node X':'50','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='2 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.0647058823529e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.0647058823529e+01,y=-4.5901960784314e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox up event
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.Pin
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Pinned it.
assert tests.gtkMultiTextCompare({'Mouse X':'50.65','Mouse Y':'45.9','Node X':'50','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='pinned'
assert findWidget(tbox+":Status").get_text()=='3 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1078431372549e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1509803921569e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1941176470588e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2372549019608e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3235294117647e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.4098039215686e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.4960784313725e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5823529411765e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6686274509804e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.7549019607843e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8411764705882e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9274509803922e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.0137254901961e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.0568627450980e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1000000000000e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1431372549020e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1862745098039e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2294117647059e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2725490196078e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3156862745098e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3588235294118e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4019607843137e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4450980392157e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4882352941176e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5745098039216e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6607843137255e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7039215686275e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7470588235294e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8333333333333e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8764705882353e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9196078431373e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9627450980392e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0058823529412e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0490196078431e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0921568627451e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event

# Arrived at fourth node.
assert tests.gtkMultiTextCompare({'Mouse X':'70.92','Mouse Y':'45.9','Node X':'72','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='3 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 7.0921568627451e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.0921568627451e+01,y=-4.5901960784314e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox up event
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.Pin
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Pinned it.
assert tests.gtkMultiTextCompare({'Mouse X':'70.92','Mouse Y':'45.9','Node X':'72','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='pinned'
assert findWidget(tbox+":Status").get_text()=='4 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0921568627451e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0490196078431e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0058823529412e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9196078431373e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8333333333333e+01,y=-4.5470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5745098039216e+01,y=-4.4607843137255e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3156862745098e+01,y=-4.3745098039216e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9705882352941e+01,y=-4.3745098039216e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6254901960784e+01,y=-4.2882352941176e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1941176470588e+01,y=-4.2882352941176e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7627450980392e+01,y=-4.2882352941176e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3313725490196e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8137254901961e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2960784313725e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7784313725490e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2607843137255e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8294117647059e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3980392156863e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.6666666666667e+00,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2156862745098e+00,y=-4.1156862745098e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9019607843137e+00,y=-4.1156862745098e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-1.5490196078431e+00,y=-4.0294117647059e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-2.8431372549020e+00,y=-4.0294117647059e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pin Nodes:Undo').clicked()
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Undid last pin.
assert tests.gtkMultiTextCompare({'Mouse X':'-2.843','Mouse Y':'40.29','Node X':'0','Node Y':'37.5'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='3 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':True,'UnPinAll':True},tbox)

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pin Nodes:Undo').clicked()
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Undid again.
assert tests.gtkMultiTextCompare({'Mouse X':'-2.843','Mouse Y':'40.29','Node X':'0','Node Y':'37.5'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='2 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':True,'UnPinAll':True},tbox)

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pin Nodes:Redo').clicked()
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.Redo
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Redid.
assert tests.gtkMultiTextCompare({'Mouse X':'-2.843','Mouse Y':'40.29','Node X':'0','Node Y':'37.5'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='3 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':True,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-2.8431372549020e+00,y=-2.6921568627451e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-2.5490196078431e-01,y=-2.7784313725490e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3333333333333e+00,y=-2.8647058823529e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.9215686274510e+00,y=-2.9509803921569e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.5098039215686e+00,y=-3.0372549019608e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.0098039215686e+01,y=-3.1235294117647e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.0960784313725e+01,y=-3.1666666666667e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3549019607843e+01,y=-3.2529411764706e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.4411764705882e+01,y=-3.2960784313725e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.5274509803922e+01,y=-3.3392156862745e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.6137254901961e+01,y=-3.3392156862745e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7000000000000e+01,y=-3.3823529411765e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7431372549020e+01,y=-3.4254901960784e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8294117647059e+01,y=-3.4686274509804e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9156862745098e+01,y=-3.4686274509804e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0019607843137e+01,y=-3.4686274509804e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0882352941176e+01,y=-3.5117647058824e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1313725490196e+01,y=-3.5117647058824e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2176470588235e+01,y=-3.5549019607843e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3039215686275e+01,y=-3.5549019607843e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3901960784314e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4764705882353e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5196078431373e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5627450980392e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.6058823529412e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.6490196078431e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.6921568627451e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7352941176471e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7784313725490e+01,y=-3.5980392156863e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8215686274510e+01,y=-3.6411764705882e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9078431372549e+01,y=-3.6843137254902e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.9941176470588e+01,y=-3.7274509803922e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2529411764706e+01,y=-3.8137254901961e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.3392156862745e+01,y=-3.8568627450980e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.4254901960784e+01,y=-3.9000000000000e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6843137254902e+01,y=-3.9862745098039e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.7274509803922e+01,y=-4.0294117647059e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8137254901961e+01,y=-4.0294117647059e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8568627450980e+01,y=-4.0725490196078e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.9000000000000e+01,y=-4.1156862745098e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.9431372549020e+01,y=-4.1156862745098e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.9862745098039e+01,y=-4.1588235294118e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0294117647059e+01,y=-4.1588235294118e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0294117647059e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0725490196078e+01,y=-4.2019607843137e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0725490196078e+01,y=-4.2450980392157e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.1156862745098e+01,y=-4.2450980392157e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.1588235294118e+01,y=-4.2450980392157e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2019607843137e+01,y=-4.2882352941176e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2450980392157e+01,y=-4.2882352941176e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2882352941176e+01,y=-4.2882352941176e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3745098039216e+01,y=-4.2882352941176e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4176470588235e+01,y=-4.2882352941176e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4176470588235e+01,y=-4.3313725490196e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4607843137255e+01,y=-4.3313725490196e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5039215686275e+01,y=-4.3313725490196e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5470588235294e+01,y=-4.3313725490196e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5470588235294e+01,y=-4.3745098039216e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5901960784314e+01,y=-4.3745098039216e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5901960784314e+01,y=-4.4176470588235e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6333333333333e+01,y=-4.4176470588235e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6333333333333e+01,y=-4.4607843137255e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6764705882353e+01,y=-4.5039215686275e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7196078431373e+01,y=-4.5470588235294e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7627450980392e+01,y=-4.5901960784314e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event

# Arrived at another node.
assert tests.gtkMultiTextCompare({'Mouse X':'47.63','Mouse Y':'45.9','Node X':'50','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='pinned'
assert findWidget(tbox+":Status").get_text()=='3 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':True,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.7627450980392e+01,y=-4.5901960784314e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.7627450980392e+01,y=-4.5901960784314e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox up event
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.TogglePin
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Ctrl-clicked to toggle it.
assert tests.gtkMultiTextCompare({'Mouse X':'47.63','Mouse Y':'45.9','Node X':'50','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='2 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7196078431373e+01,y=-4.5901960784314e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6764705882353e+01,y=-4.5901960784314e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6333333333333e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5901960784314e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5470588235294e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5039215686275e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4607843137255e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4176470588235e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3745098039216e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3313725490196e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2882352941176e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2450980392157e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2450980392157e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2882352941176e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3313725490196e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3745098039216e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4176470588235e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4607843137255e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5039215686275e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5470588235294e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5901960784314e+01,y=-4.6333333333333e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6333333333333e+01,y=-4.6333333333333e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6764705882353e+01,y=-4.6333333333333e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7196078431373e+01,y=-4.6333333333333e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7627450980392e+01,y=-4.6333333333333e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8058823529412e+01,y=-4.6764705882353e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event

# Arrived at another other further different node.
assert tests.gtkMultiTextCompare({'Mouse X':'48.06','Mouse Y':'46.76','Node X':'50','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='2 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8058823529412e+01,y=-4.6764705882353e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8058823529412e+01,y=-4.6764705882353e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox up event
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.TogglePin
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Toggled this one.
assert tests.gtkMultiTextCompare({'Mouse X':'48.06','Mouse Y':'46.76','Node X':'50','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='pinned'
assert findWidget(tbox+":Status").get_text()=='3 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7627450980392e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7196078431373e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6764705882353e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6333333333333e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5901960784314e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5470588235294e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5039215686275e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4607843137255e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4176470588235e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3745098039216e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3313725490196e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2882352941176e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2450980392157e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2019607843137e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event

# Arrived at another node.
assert tests.gtkMultiTextCompare({'Mouse X':'42.02','Mouse Y':'46.76','Node X':'37.5','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='pinned'
assert findWidget(tbox+":Status").get_text()=='3 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2019607843137e+01,y=-4.6764705882353e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.2019607843137e+01,y=-4.6764705882353e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox up event
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.UnPin
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Shift-clicked to unpin it.
assert tests.gtkMultiTextCompare({'Mouse X':'42.02','Mouse Y':'46.76','Node X':'37.5','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='2 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2019607843137e+01,y=-4.6764705882353e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.2019607843137e+01,y=-4.6764705882353e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox up event
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.UnPin
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Shift-clicked to unpin it again -- should be a no-op.
assert tests.gtkMultiTextCompare({'Mouse X':'42.02','Mouse Y':'46.76','Node X':'37.5','Node Y':'50'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='2 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.1156862745098e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0294117647059e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.9000000000000e+01,y=-4.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6411764705882e+01,y=-4.5901960784314e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.3823529411765e+01,y=-4.5039215686275e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0372549019608e+01,y=-4.4176470588235e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.7784313725490e+01,y=-4.2450980392157e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3470588235294e+01,y=-4.1588235294118e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0019607843137e+01,y=-4.0725490196078e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.6568627450980e+01,y=-3.9862745098039e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3980392156863e+01,y=-3.9000000000000e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.1392156862745e+01,y=-3.8137254901961e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8039215686274e+00,y=-3.7274509803922e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2156862745098e+00,y=-3.6411764705882e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6274509803922e+00,y=-3.5549019607843e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.0392156862745e+00,y=-3.4686274509804e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-1.5490196078431e+00,y=-3.3823529411765e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=-4.1372549019608e+00,y=-3.2960784313725e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Pin Nodes toolbox move event
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pin Nodes:Invert').clicked()
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.Invert
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Inverted pin state.
assert tests.gtkMultiTextCompare({'Mouse X':'-4.137','Mouse Y':'32.96','Node X':'0','Node Y':'37.5'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='73 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':True},tbox)

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pin Nodes:UnPinAll').clicked()
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Toolbox.Pin_Nodes.UnPinAll
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Unpinned nodes.
assert tests.gtkMultiTextCompare({'Mouse X':'-4.137','Mouse Y':'32.96','Node X':'0','Node Y':'37.5'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='0 nodes pinned.'
assert tests.sensitizationCheck({'Undo':True,'Invert':True,'Redo':False,'UnPinAll':False},tbox)

findWidget('OOF2 Graphics 1').resize(800, 405)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(285)
findWidget('OOF2 Graphics 1').resize(800, 407)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(287)
findWidget('OOF2 Graphics 1').resize(800, 419)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(299)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(299)
findWidget('OOF2 Graphics 1').resize(800, 428)
findWidget('OOF2 Graphics 1').resize(800, 430)
findWidget('OOF2 Graphics 1').resize(800, 438)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(318)
findWidget('OOF2 Graphics 1').resize(800, 440)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(320)
findWidget('OOF2 Graphics 1').resize(800, 444)
findWidget('OOF2 Graphics 1').resize(800, 447)
findWidget('OOF2 Graphics 1').resize(800, 452)
findWidget('OOF2 Graphics 1').resize(800, 454)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(334)
findWidget('OOF2 Graphics 1').resize(800, 456)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(336)
findWidget('OOF2 Graphics 1').resize(800, 462)
findWidget('OOF2 Graphics 1').resize(800, 464)
findWidget('OOF2 Graphics 1').resize(800, 465)
findWidget('OOF2 Graphics 1').resize(800, 469)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(349)
findWidget('OOF2 Graphics 1').resize(800, 471)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(351)
findWidget('OOF2 Graphics 1').resize(800, 472)
findWidget('OOF2 Graphics 1').resize(800, 474)
findWidget('OOF2 Graphics 1').resize(800, 478)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(358)
findWidget('OOF2 Graphics 1').resize(800, 480)
findWidget('OOF2 Graphics 1').resize(800, 481)
findWidget('OOF2 Graphics 1').resize(800, 482)
findWidget('OOF2 Graphics 1').resize(800, 483)
findWidget('OOF2 Graphics 1').resize(800, 484)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(364)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(362)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(355)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(352)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(349)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(340)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(326)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(317)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(314)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(312)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(306)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(298)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(296)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
checkpoint OOF.Graphics_1.Layer.Select
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:Delete').activate()
findWidget('OOF2 Graphics 1:Pane0').set_position(296)
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
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Delete

# Removed skeleton layer.
assert tests.gtkMultiTextCompare({'Mouse X':'-4.137','Mouse Y':'32.96','Node X':'0','Node Y':'37.5'},tbox)
assert findWidget(tbox+":Pin Label").get_text()=='unpinned'
assert findWidget(tbox+":Status").get_text()=='0 nodes pinned.'
assert tests.sensitizationCheck({'Undo':False,'Invert':False,'Redo':False,'UnPinAll':False},tbox)

findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 71)
findWidget('Dialog-Python_Log:filename').set_text('p')
findWidget('Dialog-Python_Log:filename').set_text('pi')
findWidget('Dialog-Python_Log:filename').set_text('pin')
findWidget('Dialog-Python_Log:filename').set_text('pinn')
findWidget('Dialog-Python_Log:filename').set_text('pinno')
findWidget('Dialog-Python_Log:filename').set_text('pinnod')
findWidget('Dialog-Python_Log:filename').set_text('pinnode')
findWidget('Dialog-Python_Log:filename').set_text('pinnodes')
findWidget('Dialog-Python_Log:filename').set_text('pinnodest')
findWidget('Dialog-Python_Log:filename').set_text('pinnodestb')
findWidget('Dialog-Python_Log:filename').set_text('pinnodestbo')
findWidget('Dialog-Python_Log:filename').set_text('pinnodestbox')
findWidget('Dialog-Python_Log:filename').set_text('pinnodestbox.')
findWidget('Dialog-Python_Log:filename').set_text('pinnodestbox.l')
findWidget('Dialog-Python_Log:filename').set_text('pinnodestbox.lo')
findWidget('Dialog-Python_Log:filename').set_text('pinnodestbox.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('pinnodestbox.log')
os.remove('pinnodestbox.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
