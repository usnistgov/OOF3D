checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests, os
tbox = "OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info"
elbox = tbox+":ElementInformation"
ndbox = tbox+":NodeInformation"
sgbox = tbox+":SegmentInformation"
cbox = tbox+":Click"
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
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1').resize(800, 406)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(286)
findWidget('OOF2 Graphics 1').resize(800, 408)
findWidget('OOF2 Graphics 1').resize(800, 420)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(300)
findWidget('OOF2 Graphics 1').resize(800, 426)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(306)
findWidget('OOF2 Graphics 1').resize(800, 452)
findWidget('OOF2 Graphics 1').resize(800, 460)
findWidget('OOF2 Graphics 1').resize(800, 476)
findWidget('OOF2 Graphics 1').resize(800, 482)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(362)
findWidget('OOF2 Graphics 1').resize(800, 490)
findWidget('OOF2 Graphics 1').resize(800, 493)
findWidget('OOF2 Graphics 1').resize(800, 498)
findWidget('OOF2 Graphics 1').resize(800, 500)
findWidget('OOF2 Graphics 1').resize(800, 502)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(382)
findWidget('OOF2 Graphics 1').resize(800, 503)
findWidget('OOF2 Graphics 1').resize(800, 508)
findWidget('OOF2 Graphics 1').resize(800, 510)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(390)
findWidget('OOF2 Graphics 1').resize(800, 521)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(401)
findWidget('OOF2 Graphics 1').resize(800, 523)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(403)
findWidget('OOF2 Graphics 1').resize(800, 527)
findWidget('OOF2 Graphics 1').resize(800, 530)
findWidget('OOF2 Graphics 1').resize(800, 532)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(412)
findWidget('OOF2 Graphics 1').resize(800, 533)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(413)
findWidget('OOF2 Graphics 1').resize(800, 541)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1').resize(800, 543)
findWidget('OOF2 Graphics 1').resize(800, 544)
findWidget('OOF2 Graphics 1').resize(800, 547)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(427)
findWidget('OOF2 Graphics 1').resize(800, 548)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(428)
findWidget('OOF2 Graphics 1').resize(800, 549)
findWidget('OOF2 Graphics 1').resize(800, 550)
findWidget('OOF2 Graphics 1').resize(800, 551)
findWidget('OOF2 Graphics 1').resize(800, 553)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(433)
findWidget('OOF2 Graphics 1').resize(800, 554)
findWidget('OOF2 Graphics 1').resize(800, 555)
findWidget('OOF2 Graphics 1').resize(800, 560)
findWidget('OOF2 Graphics 1').resize(800, 561)
findWidget('OOF2 Graphics 1').resize(800, 562)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(442)
findWidget('OOF2 Graphics 1').resize(800, 564)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(444)
findWidget('OOF2 Graphics 1').resize(800, 565)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(445)
findWidget('OOF2 Graphics 1').resize(800, 575)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(455)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(454)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(451)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(447)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(431)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(425)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(418)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(414)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(408)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(403)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(401)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Skeleton Info')
checkpoint Graphics_1 Skeleton Info sensitized

# Toolbox now selected, check state.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'','Y Text':''},cbox)
assert tests.gtkMultiTextCompare({'Material':'','Group':'','Shape':'','Homog':'','Dom pixel':'','Area':'','Index':'','Type':''},elbox)
assert tests.sensitizationCheck({'Prev':False,'Clear':False,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",[])
assert tests.chooserCheck(elbox+":NodeList",[])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
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
findWidget('Dialog-Data:filename').set_text('../../examples/s')
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
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint active area status updated
checkpoint mesh bdy page updated
checkpoint pixel page updated
checkpoint Field page sensitized
checkpoint Materials page updated
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
checkpoint interface page updated
checkpoint skeleton selection page groups sensitized
findWidget('OOF2 Activity Viewer').resize(400, 300)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
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
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
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
checkpoint mesh bdy page updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
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
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint contourmap info updated for Graphics_1
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

# Skeleton loaded, check data.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'','Y Text':''},cbox)
assert tests.gtkMultiTextCompare({'Material':'','Group':'','Shape':'','Homog':'','Dom pixel':'','Area':'','Index':'','Type':''},elbox)
assert tests.sensitizationCheck({'Prev':False,'Clear':False,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",[])

setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(221)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(200)
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:GroupListScroll:GroupList').get_selection().select_path((0,))
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941)
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941)').resize(194, 71)
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941):new_name').set_text('')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941):new_name').set_text('y')
checkpoint microstructure page sensitized
checkpoint meshable button set
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941):new_name').set_text('ye')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941):new_name').set_text('yel')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941):new_name').set_text('yell')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941):new_name').set_text('yello')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941):new_name').set_text('yellow')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.000000, green=1.000000, blue=0.752941):gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(639, 200)
checkpoint interface page updated
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.PixelGroup.Rename
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:GroupListScroll:GroupList').get_selection().select_path((1,))
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename pixelgroup RGBColor(red=0.000000, green=0.000000, blue=1.000000)
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.000000, green=0.000000, blue=1.000000)').resize(194, 71)
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.000000, green=0.000000, blue=1.000000):new_name').set_text('')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.000000, green=0.000000, blue=1.000000):new_name').set_text('b')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.000000, green=0.000000, blue=1.000000):new_name').set_text('bl')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.000000, green=0.000000, blue=1.000000):new_name').set_text('blu')
checkpoint microstructure page sensitized
checkpoint meshable button set
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.000000, green=0.000000, blue=1.000000):new_name').set_text('blue')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.000000, green=0.000000, blue=1.000000):gtk-ok').clicked()
checkpoint interface page updated
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.PixelGroup.Rename
checkpoint meshable button set

# Pixel groups renamed for ease of comparison, no test required here.

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.0000000000000e+01,y=-5.5000000000000e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.0000000000000e+01,y=-5.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Element query.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':30,'Y Text':55},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'','Dom pixel':'blue','Index':'59','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.418601,'Homog':0.992461,'Area':137.5},elbox)
assert tests.sensitizationCheck({'Prev':False,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 135, nodes (36, 44) (length: 15.4029)","Segment 134, nodes (36, 37) (length: 15.5)","Segment 70, nodes (37, 45) (length: 12.5)","Segment 128, nodes (44, 45) (length: 6.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 36 at (22, 50) (angle: 54.2461)","Node 37 at (37.5, 50) (angle: 90)","Node 45 at (37.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3529411764706e+01,y=-6.0588235294118e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3529411764706e+01,y=-6.0588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Another element query.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':23.53,'Y Text':60.59},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'','Dom pixel':'yellow','Index':'60','Type':'triangle'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.030177,'Homog':0.975899,'Area':115.625000},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 68, nodes (36, 43) (length: 15.7003)", "Segment 135, nodes (36, 44) (length: 15.4029)", "Segment 130, nodes (43, 44) (length: 18.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 36 at (22, 50) (angle: 72.9887)","Node 44 at (31, 62.5) (angle: 54.2461)", "Node 43 at (12.5, 62.5) (angle: 52.7652)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Node').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Switched into node mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':23.53,'Y Text':60.59},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'free','Position':'(31, 62.5)','Index':'44'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 52","Element 54","Element 59","Element 60"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5294117647059e+01,y=-7.3235294117647e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5294117647059e+01,y=-7.3235294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Direct node query.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':15.29,'Y Text':73.24},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'free','Position':'(12.5, 75)','Index':'52'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 30","Element 35","Element 54","Element 55"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.3235294117647e+01,y=-5.9705882352941e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.3235294117647e+01,y=-5.9705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Direct node query.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':13.24,'Y Text':59.71},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'free','Position':'(12.5, 62.5)','Index':'43'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 26","Element 30","Element 54","Element 60"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Segment').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Segment mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':13.24,'Y Text':59.71},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'','Index':'68'},sgbox)
assert tests.gtkMultiFloatCompare({'Length':15.700318468107582},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 26","Element 60"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 36 at (22, 50)","Node 43 at (12.5, 62.5)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.4411764705882e+01,y=-6.1764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4411764705882e+01,y=-6.1470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.4411764705882e+01,y=-6.1176470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.4411764705882e+01,y=-6.1176470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Direct segment query.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':24.41,'Y Text':61.18},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'','Index':'130'},sgbox)
assert tests.gtkMultiFloatCompare({'Length':18.5},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 54","Element 60"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 43 at (12.5, 62.5)","Node 44 at (31, 62.5)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.4411764705882e+01,y=-6.9705882352941e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.4411764705882e+01,y=-6.9705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Direct segment query.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':14.41,'Y Text':69.71},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'','Index':'79'},sgbox)
assert tests.gtkMultiFloatCompare({'Length':12.5},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 30","Element 54"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 43 at (12.5, 62.5)","Node 52 at (12.5, 75)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Element').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Switched to element mode.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':14.41,'Y Text':69.71},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'','Dom pixel':'yellow','Index':'54','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.308000,'Homog':0.988881,'Area':287.500000},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 79, nodes (43, 52) (length: 12.5)","Segment 130, nodes (43, 44) (length: 18.5)","Segment 127, nodes (44, 53) (length: 15.4029)","Segment 131, nodes (52, 53) (length: 27.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 43 at (12.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)","Node 53 at (40, 75) (angle: 54.2461)","Node 52 at (12.5, 75) (angle: 90)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Skeleton Selection')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Element:Method:Chooser'), 'ByDominantPixel')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.1176470588235e+01,y=-4.3823529411765e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.1176470588235e+01,y=-4.3823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Element sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(569, 424)
findWidget('OOF2:Skeleton Page:Pane').set_position(211)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
checkpoint skeleton page sensitized
findWidget('Dialog-Create a new Element group').resize(250, 71)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
findWidget('Dialog-Create a new Element group:name:Auto').clicked()
findWidget('Dialog-Create a new Element group:name:Text').set_text('e')
findWidget('Dialog-Create a new Element group:name:Text').set_text('el')
findWidget('Dialog-Create a new Element group:name:Text').set_text('els')
findWidget('Dialog-Create a new Element group:name:Text').set_text('else')
findWidget('Dialog-Create a new Element group:name:Text').set_text('elset')
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:Add').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Add_to_Group

# Skeleton element group constructed.
# Skeleton Info toolbox is not up, no tests possible.

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Node').clicked()
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Method:Chooser'), 'Circle')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.9411764705882e+01,y=-9.1470588235294e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.9705882352941e+01,y=-9.1470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.9705882352941e+01,y=-9.1176470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.9705882352941e+01,y=-9.0882352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0000000000000e+01,y=-9.0294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0294117647059e+01,y=-9.0000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0588235294118e+01,y=-8.9705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1764705882353e+01,y=-8.8529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2058823529412e+01,y=-8.7941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2352941176471e+01,y=-8.7647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3529411764706e+01,y=-8.6470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.4705882352941e+01,y=-8.5294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5000000000000e+01,y=-8.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6176470588235e+01,y=-8.3823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6470588235294e+01,y=-8.3529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.7647058823529e+01,y=-8.2352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8823529411765e+01,y=-8.1176470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9117647058824e+01,y=-8.0882352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9411764705882e+01,y=-8.0588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9705882352941e+01,y=-8.0294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.0882352941176e+01,y=-7.9117647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1176470588235e+01,y=-7.8823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1470588235294e+01,y=-7.8529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1764705882353e+01,y=-7.7941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2352941176471e+01,y=-7.7647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2647058823529e+01,y=-7.7352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2941176470588e+01,y=-7.6764705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3235294117647e+01,y=-7.6470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3823529411765e+01,y=-7.6176470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4117647058824e+01,y=-7.5882352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4705882352941e+01,y=-7.5588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5000000000000e+01,y=-7.5294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5294117647059e+01,y=-7.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5588235294118e+01,y=-7.4705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5882352941176e+01,y=-7.4411764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6176470588235e+01,y=-7.4117647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6470588235294e+01,y=-7.4117647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6764705882353e+01,y=-7.3823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7058823529412e+01,y=-7.3823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7352941176471e+01,y=-7.3529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7647058823529e+01,y=-7.3529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7941176470588e+01,y=-7.3235294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8235294117647e+01,y=-7.2941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8529411764706e+01,y=-7.2647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8823529411765e+01,y=-7.2647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9117647058824e+01,y=-7.2352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9411764705882e+01,y=-7.2352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9705882352941e+01,y=-7.2058823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0000000000000e+01,y=-7.1764705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.0000000000000e+01,y=-7.1764705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Circle
findWidget('OOF2:Skeleton Selection Page:Mode:Node').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page updated
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Node group
findWidget('Dialog-Create a new Node group').resize(250, 71)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
findWidget('Dialog-Create a new Node group:name:Auto').clicked()
findWidget('Dialog-Create a new Node group:name:Text').set_text('n')
findWidget('Dialog-Create a new Node group:name:Text').set_text('nd')
findWidget('Dialog-Create a new Node group:name:Text').set_text('nds')
findWidget('Dialog-Create a new Node group:name:Text').set_text('ndse')
findWidget('Dialog-Create a new Node group:name:Text').set_text('ndset')
findWidget('Dialog-Create a new Node group:gtk-ok').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.New_Group
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:Add').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint OOF.NodeGroup.Add_to_Group

# Skeleton node group constructed.

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Segment').clicked()
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Node').clicked()
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Node sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Clear').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Clear
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(240)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Segment').clicked()
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Segment:Method:Chooser'), 'Circle')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.1176470588235e+01,y=-7.9411764705882e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1176470588235e+01,y=-7.8823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1176470588235e+01,y=-7.8235294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1470588235294e+01,y=-7.7647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1764705882353e+01,y=-7.7058823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2058823529412e+01,y=-7.6470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2352941176471e+01,y=-7.5882352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3529411764706e+01,y=-7.4705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3823529411765e+01,y=-7.4411764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5000000000000e+01,y=-7.3235294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5294117647059e+01,y=-7.2941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5588235294118e+01,y=-7.2647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6176470588235e+01,y=-7.2352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6470588235294e+01,y=-7.2058823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6764705882353e+01,y=-7.1764705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.7941176470588e+01,y=-7.0588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8235294117647e+01,y=-7.0588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8529411764706e+01,y=-7.0294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8823529411765e+01,y=-7.0000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9411764705882e+01,y=-6.9705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.0000000000000e+01,y=-6.9411764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.0588235294118e+01,y=-6.9117647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.0882352941176e+01,y=-6.8823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1470588235294e+01,y=-6.8529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2058823529412e+01,y=-6.8235294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2352941176471e+01,y=-6.7941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2647058823529e+01,y=-6.7941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2941176470588e+01,y=-6.7941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3235294117647e+01,y=-6.7647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3529411764706e+01,y=-6.7352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3823529411765e+01,y=-6.7058823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4117647058824e+01,y=-6.7058823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4411764705882e+01,y=-6.6764705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4705882352941e+01,y=-6.6470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5000000000000e+01,y=-6.6176470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5294117647059e+01,y=-6.5882352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5588235294118e+01,y=-6.5588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5882352941176e+01,y=-6.5294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5882352941176e+01,y=-6.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6176470588235e+01,y=-6.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6176470588235e+01,y=-6.4705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6470588235294e+01,y=-6.4411764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6470588235294e+01,y=-6.4117647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6764705882353e+01,y=-6.3823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.6764705882353e+01,y=-6.3529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7058823529412e+01,y=-6.3529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7058823529412e+01,y=-6.3235294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7352941176471e+01,y=-6.2941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7352941176471e+01,y=-6.2647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7647058823529e+01,y=-6.2352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7941176470588e+01,y=-6.2058823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8235294117647e+01,y=-6.1764705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8529411764706e+01,y=-6.1470588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8823529411765e+01,y=-6.1176470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9117647058824e+01,y=-6.0882352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9411764705882e+01,y=-6.0882352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.9705882352941e+01,y=-6.0588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0000000000000e+01,y=-6.0588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0294117647059e+01,y=-6.0294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0588235294118e+01,y=-6.0294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0882352941176e+01,y=-6.0294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.1176470588235e+01,y=-6.0000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.1470588235294e+01,y=-6.0000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.1764705882353e+01,y=-6.0000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2058823529412e+01,y=-5.9705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2352941176471e+01,y=-5.9705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2352941176471e+01,y=-5.9411764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2647058823529e+01,y=-5.9411764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2941176470588e+01,y=-5.9117647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.3235294117647e+01,y=-5.8823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.3529411764706e+01,y=-5.8529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.3823529411765e+01,y=-5.8529411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.4117647058824e+01,y=-5.8235294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.4411764705882e+01,y=-5.7941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.4411764705882e+01,y=-5.7941176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Circle
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2:Skeleton Selection Page:Mode:Segment').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(208)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(250, 71)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(208)
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(208)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:Add').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(208)
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group

# Skeleton segment group constructed.

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(208)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
findWidget('OOF2').resize(664, 424)
findWidget('OOF2:Materials Page:Pane').set_position(267)
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(250, 71)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material material to pixels
findWidget('Dialog-Assign material material to pixels').resize(258, 106)
setComboBox(findWidget('Dialog-Assign material material to pixels:pixels'), 'yellow')
findWidget('Dialog-Assign material material to pixels:gtk-ok').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Assign
findWidget('OOF2 Graphics 1:Pane0').set_position(399)

# Material added to microstructure.

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Skeleton Info')
checkpoint Graphics_1 Skeleton Info sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(399)
findWidget('OOF2 Graphics 1').resize(800, 582)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(406)
findWidget('OOF2 Graphics 1').resize(800, 595)
findWidget('OOF2 Graphics 1').resize(800, 598)
findWidget('OOF2 Graphics 1').resize(800, 601)
findWidget('OOF2 Graphics 1').resize(800, 604)
findWidget('OOF2 Graphics 1').resize(800, 607)
findWidget('OOF2 Graphics 1').resize(800, 615)
findWidget('OOF2 Graphics 1').resize(800, 618)
findWidget('OOF2 Graphics 1').resize(800, 621)
findWidget('OOF2 Graphics 1').resize(800, 629)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(453)
findWidget('OOF2 Graphics 1').resize(800, 632)
findWidget('OOF2 Graphics 1').resize(800, 640)
findWidget('OOF2 Graphics 1').resize(800, 648)
findWidget('OOF2 Graphics 1').resize(800, 651)
findWidget('OOF2 Graphics 1').resize(800, 653)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(477)
findWidget('OOF2 Graphics 1').resize(800, 662)
findWidget('OOF2 Graphics 1').resize(800, 666)
findWidget('OOF2 Graphics 1').resize(800, 677)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(501)
findWidget('OOF2 Graphics 1').resize(800, 695)
findWidget('OOF2 Graphics 1').resize(800, 697)
findWidget('OOF2 Graphics 1').resize(800, 698)
findWidget('OOF2 Graphics 1').resize(800, 700)
findWidget('OOF2 Graphics 1').resize(800, 702)
findWidget('OOF2 Graphics 1').resize(800, 704)
findWidget('OOF2 Graphics 1').resize(800, 707)
findWidget('OOF2 Graphics 1').resize(800, 708)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(532)
findWidget('OOF2 Graphics 1').resize(800, 710)
findWidget('OOF2 Graphics 1').resize(800, 713)
findWidget('OOF2 Graphics 1').resize(800, 715)
findWidget('OOF2 Graphics 1').resize(800, 720)
findWidget('OOF2 Graphics 1').resize(800, 724)
findWidget('OOF2 Graphics 1').resize(800, 725)
findWidget('OOF2 Graphics 1').resize(800, 727)
findWidget('OOF2 Graphics 1').resize(800, 728)
findWidget('OOF2 Graphics 1').resize(800, 729)
findWidget('OOF2 Graphics 1').resize(800, 730)
findWidget('OOF2 Graphics 1').resize(800, 731)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(555)
findWidget('OOF2 Graphics 1').resize(800, 732)
findWidget('OOF2 Graphics 1').resize(800, 733)
findWidget('OOF2 Graphics 1').resize(800, 734)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(558)
findWidget('OOF2 Graphics 1').resize(800, 735)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(559)
findWidget('OOF2 Graphics 1').resize(800, 736)
findWidget('OOF2 Graphics 1').resize(800, 737)
findWidget('OOF2 Graphics 1').resize(800, 738)
findWidget('OOF2 Graphics 1').resize(800, 739)
findWidget('OOF2 Graphics 1').resize(800, 744)
findWidget('OOF2 Graphics 1').resize(800, 746)
findWidget('OOF2 Graphics 1').resize(800, 752)
findWidget('OOF2 Graphics 1').resize(800, 755)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(579)
findWidget('OOF2 Graphics 1').resize(800, 764)
findWidget('OOF2 Graphics 1').resize(800, 765)
findWidget('OOF2 Graphics 1').resize(800, 766)
findWidget('OOF2 Graphics 1').resize(800, 767)
findWidget('OOF2 Graphics 1').resize(800, 769)
findWidget('OOF2 Graphics 1').resize(800, 771)
findWidget('OOF2 Graphics 1').resize(800, 773)
findWidget('OOF2 Graphics 1').resize(800, 775)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(599)
findWidget('OOF2 Graphics 1').resize(800, 781)
findWidget('OOF2 Graphics 1').resize(800, 784)
findWidget('OOF2 Graphics 1').resize(800, 786)
findWidget('OOF2 Graphics 1').resize(800, 788)
findWidget('OOF2 Graphics 1').resize(800, 790)
findWidget('OOF2 Graphics 1').resize(800, 794)
findWidget('OOF2 Graphics 1').resize(800, 795)
findWidget('OOF2 Graphics 1').resize(800, 796)
findWidget('OOF2 Graphics 1').resize(800, 798)
findWidget('OOF2 Graphics 1').resize(800, 799)
findWidget('OOF2 Graphics 1').resize(800, 800)
findWidget('OOF2 Graphics 1').resize(800, 801)
findWidget('OOF2 Graphics 1').resize(800, 802)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Window organized, groups added, toolbox re-selected in element mode.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':14.41,'Y Text':69.71},cbox)
assert tests.gtkMultiTextCompare({'Material':'material','Group':'','Dom pixel':'yellow','Index':'54','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.308000,'Homog':0.988881,'Area':287.500000},elbox)
assert tests.sensitizationCheck({'Prev':False,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 79, nodes (43, 52) (length: 12.5)","Segment 130, nodes (43, 44) (length: 18.5)","Segment 127, nodes (44, 53) (length: 15.4029)","Segment 131, nodes (52, 53) (length: 27.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 43 at (12.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)","Node 53 at (40, 75) (angle: 54.2461)","Node 52 at (12.5, 75) (angle: 90)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4117647058824e+01,y=-5.6764705882353e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4117647058824e+01,y=-5.6764705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct element query.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':34.12,'Y Text':56.76},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'elset','Dom pixel':'blue','Index':'59','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.418601,'Homog':0.992461,'Area':137.500000},elbox)
assert tests.sensitizationCheck({'Prev':False,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 135, nodes (36, 44) (length: 15.4029)", "Segment 134, nodes (36, 37) (length: 15.5)", "Segment 70, nodes (37, 45) (length: 12.5)", "Segment 128, nodes (44, 45) (length: 6.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 36 at (22, 50) (angle: 54.2461)","Node 37 at (37.5, 50) (angle: 90)","Node 45 at (37.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.3823529411765e+01,y=-8.5294117647059e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.3823529411765e+01,y=-8.5294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct element query.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':43.82,'Y Text':85.29},cbox)
assert tests.gtkMultiTextCompare({'Material':'material','Group':'','Dom pixel':'yellow','Index':'45','Type':'triangle'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.133975,'Homog':0.982564,'Area':81.250000},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 118, nodes (53, 61) (length: 12.7475)","Segment 119, nodes (53, 62) (length: 18.0278)","Segment 109, nodes (61, 62) (length: 12.7475)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 53 at (40, 75) (angle: 45)","Node 62 at (50, 90) (angle: 45)","Node 61 at (37.5, 87.5) (angle: 90)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3235294117647e+01,y=-9.5000000000000e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3235294117647e+01,y=-9.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct element query.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':53.24,'Y Text':95},cbox)
assert tests.gtkMultiTextCompare({'Material':'material','Group':'','Dom pixel':'yellow','Index':'46','Type':'triangle'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.155097,'Homog':0.999600,'Area':62.500000},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 110, nodes (62, 70) (length: 10)","Segment 120, nodes (62, 71) (length: 16.0078)","Segment 121, nodes (70, 71) (length: 12.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 62 at (50, 90) (angle: 51.3402)","Node 71 at (62.5, 100) (angle: 38.6598)","Node 70 at (50, 100) (angle: 90)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.8823529411765e+01,y=-6.5588235294118e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8823529411765e+01,y=-6.5588235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct element query.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':58.82,'Y Text':65.59},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'elset','Dom pixel':'blue','Index':'31','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.580223,'Homog':0.992404,'Area':162.625000},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 81, nodes (46, 53) (length: 16.0078)","Segment 74, nodes (46, 47) (length: 16)","Segment 82, nodes (47, 54) (length: 7.38241)","Segment 83, nodes (53, 54) (length: 23.2863)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 46 at (50, 62.5) (angle: 128.66)","Node 47 at (66, 62.5) (angle: 61.6992)","Node 54 at (62.5, 69) (angle: 133.232)","Node 53 at (40, 75) (angle: 36.4088)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Node').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Switched to node mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':58.82,'Y Text':65.59},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'ndset','Mobility':'free','Position':'(62.5, 69)','Index':'54'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 31","Element 32","Element 47","Element 49"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.9117647058824e+01,y=-9.9117647058824e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.9117647058824e+01,y=-9.9117647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct node query.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':39.12,'Y Text':99.12},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'ndset','Mobility':'x only','Position':'(37.5, 100)','Index':'69'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 40","Element 41"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0588235294118e+00,y=-9.7647058823529e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.0588235294118e+00,y=-9.7647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct node query.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':2.059,'Y Text':97.65},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'topleft','Group':'','Mobility':'fixed','Position':'(0, 100)','Index':'66'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 38"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8823529411765e+01,y=-6.0000000000000e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8823529411765e+01,y=-6.0000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct node query.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':48.82,'Y Text':60},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'free','Position':'(50, 62.5)','Index':'46'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 27","Element 28","Element 31","Element 44"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 7.3235294117647e+01,y=-4.7352941176471e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.3235294117647e+01,y=-4.7352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct node query.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':73.24,'Y Text':47.35},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'free','Position':'(72, 50)','Index':'39'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 24","Element 28","Element 57","Element 61","Element 62","Element 63"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Segment').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Segment mode switch.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':73.24,'Y Text':47.35},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'','Index':'137','Length':'14.401976728695566'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 62","Element 63"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 33 at (78.1981, 37)","Node 39 at (72, 50)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2647058823529e+01,y=-9.7647058823529e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.2647058823529e+01,y=-9.7647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct segment query.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'42.65','Y Text':'97.65'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'top','Groups':'segmentgroup','Index':'111','Length':'12.5'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 41"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 69 at (37.5, 100)","Node 70 at (50, 100)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.2352941176471e+00,y=-9.7647058823529e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.2352941176471e+00,y=-9.7647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct segment query.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'8.235','Y Text':'97.65'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'top','Groups':'','Index':'102','Length':'12.5'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 38"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 66 at (0, 100)","Node 67 at (12.5, 100)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.3235294117647e+01,y=-1.7647058823529e+00,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.3235294117647e+01,y=-1.7647058823529e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct segment query.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'53.24','Y Text':'1.765'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'bottom','Groups':'','Index':'13','Length':'12.5'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 4"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 4 at (50, 0)","Node 5 at (62.5, 0)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.7058823529412e+01,y=-8.2352941176471e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.7058823529412e+01,y=-8.2352941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct segment query.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'47.06','Y Text':'82.35'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'segmentgroup','Index':'119','Length':'18.027756377319946'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 45","Element 49"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 53 at (40, 75)","Node 62 at (50, 90)"])

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.2941176470588e+01,y=-8.7058823529412e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.2941176470588e+01,y=-8.7058823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegment
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Direct segment query.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'62.94','Y Text':'87.06'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'segmentgroup','Index':'123','Length':'25.124689052802225'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 47","Element 48"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 62 at (50, 90)","Node 63 at (75, 87.5)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Prev').clicked()
checkpoint Graphics_1 Skeleton Info sensitized

# Previous button.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'47.06','Y Text':'82.35'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'segmentgroup','Index':'119','Length':'18.027756377319946'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':True},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 45","Element 49"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 53 at (40, 75)","Node 62 at (50, 90)"])

findWidget('OOF2 Graphics 1:Pane0').set_position(626)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Prev').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Previous button.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'53.24','Y Text':'1.765'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'bottom','Groups':'','Index':'13','Length':'12.5'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':True},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 4"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 4 at (50, 0)","Node 5 at (62.5, 0)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Node').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Switched to node mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'53.24','Y Text':'1.765'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'x only','Position':'(50, 0)','Index':'4'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 3","Element 4"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Prev').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Segment').clicked()
checkpoint Graphics_1 Skeleton Info sensitized

# Previous button click triggers switch to segment mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'53.24','Y Text':'1.765'},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'bottom','Groups':'','Index':'13','Length':'12.5'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':True},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 4"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 4 at (50, 0)","Node 5 at (62.5, 0)"])

findWidget('OOF2 Graphics 1:Pane0').set_position(626)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Prev').clicked()
checkpoint Graphics_1 Skeleton Info sensitized

# Previous button again.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':8.235,'Y Text':97.65},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'top','Groups':'','Index':'102'},sgbox)
assert tests.gtkMultiFloatCompare({'Length':12.5},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':True},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 38"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 66 at (0, 100)","Node 67 at (12.5, 100)"])

findWidget('OOF2 Graphics 1:Pane0').set_position(626)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Element').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(626)

# Switch to element mode.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':8.235,'Y Text':97.65},cbox)
assert tests.gtkMultiTextCompare({'Material':'material','Group':'','Dom pixel':'yellow','Index':'38','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.0,'Homog':1.0, 'Area':156.25}, elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 100, nodes (58, 66) (length: 12.5)","Segment 94, nodes (58, 59) (length: 12.5)","Segment 101, nodes (59, 67) (length: 12.5)","Segment 102, nodes (66, 67) (length: 12.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 58 at (0, 87.5) (angle: 90)","Node 59 at (12.5, 87.5) (angle: 90)","Node 67 at (12.5, 100) (angle: 90)","Node 66 at (0, 100) (angle: 90)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Prev').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Segment').clicked()
checkpoint Graphics_1 Skeleton Info sensitized

# Previous triggers switch to segment mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':8.235,'Y Text':97.65},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'top','Groups':'','Index':'102'},sgbox)
assert tests.gtkMultiFloatCompare({'Length':12.5},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':True},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 38"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 66 at (0, 100)","Node 67 at (12.5, 100)"])

findWidget('OOF2 Graphics 1:Pane0').set_position(626)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Prev').clicked()
checkpoint Graphics_1 Skeleton Info sensitized

# Previous.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':42.65,'Y Text':97.65},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'top','Groups':'segmentgroup','Index':'111'},sgbox)
assert tests.gtkMultiFloatCompare({'Length':12.5},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':True},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 41"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 69 at (37.5, 100)","Node 70 at (50, 100)"])

findWidget('OOF2 Graphics 1:Pane0').set_position(626)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Next').clicked()
checkpoint Graphics_1 Skeleton Info sensitized

# Next.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':8.235,'Y Text':97.65},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'top','Groups':'','Index':'102'},sgbox)
assert tests.gtkMultiFloatCompare({'Length':12.5},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':True},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 38"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 66 at (0, 100)","Node 67 at (12.5, 100)"])

findWidget('OOF2 Graphics 1:Pane0').set_position(626)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Clear').clicked()
checkpoint Graphics_1 Skeleton Info sensitized

# Info box cleared, still in segment mode.
assert not findWidget(tbox+":Click:Element").get_active()
checkpoint contourmap info updated for Graphics_1
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'','Y Text':''},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'','Index':'','Length':''},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':False,'Next':True},tbox)
assert tests.chooserCheck(sgbox+":ElementList",[])
assert tests.chooserCheck(sgbox+":NodeList",[])

findWidget('OOF2 Graphics 1:Pane0').set_position(626)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Node').clicked()

# Node mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'','Y Text':''},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'','Position':'','Index':''},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':False,'Next':True},tbox)
assert tests.chooserCheck(ndbox+":ElementList",[])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Element').clicked()

# Element mode.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'','Y Text':''},cbox)
assert tests.gtkMultiTextCompare({'Material':'','Group':'','Shape':'','Homog':'','Dom pixel':'','Area':'','Index':'','Type':''},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':False,'Next':True},tbox)
assert tests.chooserCheck(elbox+":SegmentList",[])
assert tests.chooserCheck(elbox+":NodeList",[])

findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
checkpoint OOF.Graphics_1.Layer.Select
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:Delete').activate()
findWidget('OOF2 Graphics 1:Pane0').set_position(626)
checkpoint contourmap info updated for Graphics_1
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
checkpoint Graphics_1 Element sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Layer.Delete

# Skeleton layer removed.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiTextCompare({'X Text':'','Y Text':''},cbox)
assert tests.gtkMultiTextCompare({'Material':'','Group':'','Shape':'','Homog':'','Dom pixel':'','Area':'','Index':'','Type':''},elbox)
assert tests.sensitizationCheck({'Prev':False,'Clear':False,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",[])
assert tests.chooserCheck(elbox+":NodeList",[])


findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 71)
findWidget('Dialog-Python_Log:filename').set_text('s')
findWidget('Dialog-Python_Log:filename').set_text('sk')
findWidget('Dialog-Python_Log:filename').set_text('ske')
findWidget('Dialog-Python_Log:filename').set_text('skel')
findWidget('Dialog-Python_Log:filename').set_text('skeli')
findWidget('Dialog-Python_Log:filename').set_text('skelin')
findWidget('Dialog-Python_Log:filename').set_text('skelinf')
findWidget('Dialog-Python_Log:filename').set_text('skelinfo')
findWidget('Dialog-Python_Log:filename').set_text('skelinfot')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotb')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbo')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox.')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox.l')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox.lo')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('skelinfotbox.log')
os.remove('skelinfotbox.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
