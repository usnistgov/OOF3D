checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:46 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests, os
import time
tbox="OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Info"
findWidget('OOF2 Messages 1').resize(630, 200)
findWidget('OOF2').resize(550, 350)
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(151)
findWidget('OOF2:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(346, 140)
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
findWidget('OOF2:Microstructure Page:Pane').set_position(155)
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
findWidget('OOF2:Microstructure Page:Pane').set_position(155)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Pixel Info')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9676470588235e+01,y=-7.1441176470588e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0323529411765e+01,y=-7.1441176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.0323529411765e+01,y=-7.1441176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Pixel Info updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Info.Query
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Click!
assert tests.gtkMultiTextCompare({'X':'20','Y':'71','Image':'small.ppm:small.ppm','Text 1':'0.0','Text 2':'0.9882352941176471','Text 3':'0.0','MSText':'small.ppm','material':'<No material>'},tbox)
assert tests.sensitizationCheck({'Update':False,'Clear':True},tbox)
assert findWidget(tbox+':RGB selector').get_active()
assert tests.multiTextFPCompare({'Text 1':0.0,'Text 2':0.9882352941176471,'Text 3':0.0},tbox)

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Info:HSV selector').clicked()

# Switched to HSV.
assert tests.gtkMultiTextCompare({'X':'20','Y':'71','Image':'small.ppm:small.ppm','Text 1':'120.0','Text 2':'1.0','Text 3':'0.9882352941176471','MSText':'small.ppm','material':'<No material>'},tbox)
assert tests.sensitizationCheck({'Update':False,'Clear':True},tbox)
assert not findWidget(tbox+':RGB selector').get_active()
assert tests.multiTextFPCompare({'Text 1':120.0,'Text 2':1.0,'Text 3':0.9882352941176471},tbox)

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1479411764706e+02,y=-8.2441176470588e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.1479411764706e+02,y=-8.1794117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.1479411764706e+02,y=-8.1794117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Pixel Info updated
checkpoint OOF.Graphics_1.Toolbox.Pixel_Info.Query
findWidget('OOF2 Graphics 1:Pane0').set_position(280)

# Clicked on a point in HSV mode.
assert tests.gtkMultiTextCompare({'X':'114','Y':'81','Image':'small.ppm:small.ppm','Text 1':'240.0','Text 2':'1.0','Text 3':'0.97254901960784312','MSText':'small.ppm','material':'<No material>'},tbox)
assert tests.sensitizationCheck({'Update':False,'Clear':True},tbox)
assert not findWidget(tbox+':RGB selector').get_active()
assert tests.multiTextFPCompare({'Text 1':240.0,'Text 2':1.0,'Text 3':0.97254901},tbox)

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Pixel Info:RGB selector').clicked()

# Switched back to RGB.
assert tests.gtkMultiTextCompare({'X':'114','Y':'81','Image':'small.ppm:small.ppm','Text 1':'0.0','Text 2':'0.0','Text 3':'0.97254901960784312','MSText':'small.ppm','material':'<No material>'},tbox)
assert tests.sensitizationCheck({'Update':False,'Clear':True},tbox)
assert findWidget(tbox+':RGB selector').get_active()
assert tests.multiTextFPCompare({'Text 1':0.0,'Text 2':0.0,'Text 3':0.97254901},tbox)

findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 71)
findWidget('Dialog-Python_Log:filename').set_text('p')
findWidget('Dialog-Python_Log:filename').set_text('pi')
findWidget('Dialog-Python_Log:filename').set_text('pix')
findWidget('Dialog-Python_Log:filename').set_text('pixe')
findWidget('Dialog-Python_Log:filename').set_text('pixel')
findWidget('Dialog-Python_Log:filename').set_text('pixeli')
findWidget('Dialog-Python_Log:filename').set_text('pixelin')
findWidget('Dialog-Python_Log:filename').set_text('pixelinf')
findWidget('Dialog-Python_Log:filename').set_text('pixelinfo')
findWidget('Dialog-Python_Log:filename').set_text('pixelinfor')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforg')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgs')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforg')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgb')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgbh')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgbhs')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgbhsv')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgbhsv.')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgbhsv.l')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgbhsv.lo')
findWidget('Dialog-Python_Log:filename').set_text('pixelinforgbhsv.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('pixelinforgbhsv.log')
os.remove('pixelinforgbhsv.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
