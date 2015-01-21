checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:56 $

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

findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(194, 69)
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
checkpoint interface page updated
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
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
findWidget('OOF2').resize(550, 350)
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
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(706)
findWidget('OOF2 Graphics 1:Pane0').set_position(284)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(706)
findWidget('OOF2 Graphics 1:Pane0').set_position(284)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(706)
findWidget('OOF2 Graphics 1:Pane0').set_position(284)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(284)
findWidget('OOF2 Graphics 1').resize(800, 412)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(296)
findWidget('OOF2 Graphics 1').resize(800, 424)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(308)
findWidget('OOF2 Graphics 1').resize(800, 438)
findWidget('OOF2 Graphics 1').resize(800, 454)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(338)
findWidget('OOF2 Graphics 1').resize(800, 476)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(360)
findWidget('OOF2 Graphics 1').resize(800, 498)
findWidget('OOF2 Graphics 1').resize(800, 526)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(410)
findWidget('OOF2 Graphics 1').resize(800, 550)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(434)
findWidget('OOF2 Graphics 1').resize(800, 570)
findWidget('OOF2 Graphics 1').resize(800, 588)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(472)
findWidget('OOF2 Graphics 1').resize(800, 598)
findWidget('OOF2 Graphics 1').resize(800, 604)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(488)
findWidget('OOF2 Graphics 1').resize(800, 603)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(487)
findWidget('OOF2 Graphics 1').resize(800, 605)
findWidget('OOF2 Graphics 1').resize(800, 606)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(490)
findWidget('OOF2 Graphics 1').resize(800, 607)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(491)
findWidget('OOF2 Graphics 1').resize(800, 611)
findWidget('OOF2 Graphics 1').resize(800, 612)
findWidget('OOF2 Graphics 1').resize(800, 613)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(497)
findWidget('OOF2 Graphics 1').resize(800, 614)
findWidget('OOF2 Graphics 1').resize(800, 617)
findWidget('OOF2 Graphics 1').resize(800, 620)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(504)
findWidget('OOF2 Graphics 1').resize(800, 622)
findWidget('OOF2 Graphics 1').resize(800, 624)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(508)
findWidget('OOF2 Graphics 1').resize(800, 625)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(509)
findWidget('OOF2 Graphics 1').resize(800, 626)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(510)
findWidget('OOF2 Graphics 1').resize(800, 629)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(513)
findWidget('OOF2 Graphics 1').resize(800, 630)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(514)
findWidget('OOF2 Graphics 1').resize(800, 631)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(515)
findWidget('OOF2 Graphics 1').resize(800, 633)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(517)
findWidget('OOF2 Graphics 1').resize(800, 635)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(519)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(519)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Skeleton Info')
checkpoint Graphics_1 Skeleton Info sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(519)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(519)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(516)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(513)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(499)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(497)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(495)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(489)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(481)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(475)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(467)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(457)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(449)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(448)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(446)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(445)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(444)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(443)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(433)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(432)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(431)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(432)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(433)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(434)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(436)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(437)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(438)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(440)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(441)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(442)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(443)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(256)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(723)
findWidget('OOF2 Graphics 1:Pane0').set_position(444)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2606177606178e+01,y=-6.8474903474903e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2606177606178e+01,y=-6.8474903474903e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(444)

# Direct element selection.  Dominant pixel test skipped, because it's
# a numerically-derived name which may be prone to roundoff, and is
# tested directly in the 01200 test.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':22.61,'Y Text':68.47},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'','Index':'54','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.308000,'Homog':0.988881,'Area':287.500000},elbox)
assert tests.sensitizationCheck({'Prev':False,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 79, nodes (43, 52) (length: 12.5)","Segment 130, nodes (43, 44) (length: 18.5)","Segment 127, nodes (44, 53) (length: 15.4029)","Segment 131, nodes (52, 53) (length: 27.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 43 at (12.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)","Node 53 at (40, 75) (angle: 54.2461)","Node 52 at (12.5, 75) (angle: 90)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:ElementInformation:NodeList').get_selection().select_path((1,))
findWidget('OOF2 Graphics 1:Pane0').set_position(444)

# Node peek.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':22.61,'Y Text':68.47},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'','Index':'54','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.308000,'Homog':0.988881,'Area':287.500000},elbox)
assert tests.sensitizationCheck({'Prev':False,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 79, nodes (43, 52) (length: 12.5)","Segment 130, nodes (43, 44) (length: 18.5)","Segment 127, nodes (44, 53) (length: 15.4029)","Segment 131, nodes (52, 53) (length: 27.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 43 at (12.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)","Node 53 at (40, 75) (angle: 54.2461)","Node 52 at (12.5, 75) (angle: 90)"])
assert tests.chooserListStateCheck(elbox+":NodeList",["Node 44 at (31, 62.5) (angle: 125.754)"])

tree=findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:ElementInformation:NodeList')
column = tree.get_column(0)
tree.row_activated((1,), column)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Node').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryNodeByID
findWidget('OOF2 Graphics 1:Pane0').set_position(444)

# Switched to node mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':31,'Y Text':62.5},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'free','Position':'(31, 62.5)','Index':'44'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 52","Element 54","Element 59","Element 60"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:NodeInformation:ElementList').get_selection().select_path((1,))
findWidget('OOF2 Graphics 1:Pane0').set_position(444)
tree=findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:NodeInformation:ElementList')

# Element peeked.
assert not findWidget(tbox+":Click:Element").get_active()
assert findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':31,'Y Text':62.5},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Group':'','Mobility':'free','Position':'(31, 62.5)','Index':'44'},ndbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(ndbox+":ElementList",["Element 52","Element 54","Element 59","Element 60"])
assert tests.chooserListStateCheck(ndbox+":ElementList",["Element 54"])

column = tree.get_column(0)
tree.row_activated((1,), column)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Element').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElementByID
findWidget('OOF2 Messages 1').resize(552, 200)
findWidget('OOF2 Graphics 1:Pane0').set_position(444)

# Switched to element mode.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':24,'Y Text':68.75},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'','Index':'54','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.308000,'Homog':0.988881,'Area':287.500000},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 79, nodes (43, 52) (length: 12.5)","Segment 130, nodes (43, 44) (length: 18.5)","Segment 127, nodes (44, 53) (length: 15.4029)","Segment 131, nodes (52, 53) (length: 27.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 43 at (12.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)","Node 53 at (40, 75) (angle: 54.2461)","Node 52 at (12.5, 75) (angle: 90)"])
assert tests.chooserListStateCheck(elbox+":NodeList",["Node 44 at (31, 62.5) (angle: 125.754)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:ElementInformation:SegmentList').get_selection().select_path((1,))
findWidget('OOF2 Graphics 1:Pane0').set_position(444)
tree=findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:ElementInformation:SegmentList')

# Segment peeked.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':24,'Y Text':68.75},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'','Index':'54','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.308000,'Homog':0.988881,'Area':287.500000},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 79, nodes (43, 52) (length: 12.5)","Segment 130, nodes (43, 44) (length: 18.5)","Segment 127, nodes (44, 53) (length: 15.4029)","Segment 131, nodes (52, 53) (length: 27.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 43 at (12.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)","Node 53 at (40, 75) (angle: 54.2461)","Node 52 at (12.5, 75) (angle: 90)"])
assert tests.chooserListStateCheck(elbox+":NodeList",["Node 44 at (31, 62.5) (angle: 125.754)"])
assert tests.chooserListStateCheck(elbox+":SegmentList",["Segment 130, nodes (43, 44) (length: 18.5)"])

column = tree.get_column(0)
tree.row_activated((1,), column)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Segment').clicked()
findWidget('OOF2 Messages 1').resize(566, 200)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QuerySegmentByID
findWidget('OOF2 Graphics 1:Pane0').set_position(444)

# Switched to segment mode.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':21.75,'Y Text':62.5},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'','Index':'130','Length':'18.5'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 54","Element 60"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 43 at (12.5, 62.5)","Node 44 at (31, 62.5)"])

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:SegmentInformation:ElementList').get_selection().select_path((0,))
findWidget('OOF2 Graphics 1:Pane0').set_position(444)
tree=findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:SegmentInformation:ElementList')

# Element peeked.
assert not findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':21.75,'Y Text':62.5},cbox)
assert tests.gtkMultiTextCompare({'Boundary':'','Groups':'','Index':'130','Length':'18.5'},sgbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(sgbox+":ElementList",["Element 54","Element 60"])
assert tests.chooserCheck(sgbox+":NodeList",["Node 43 at (12.5, 62.5)","Node 44 at (31, 62.5)"])
assert tests.chooserListStateCheck(sgbox+":ElementList",["Element 54"])

column = tree.get_column(0)
tree.row_activated((0,), column)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Info:Click:Element').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Skeleton_Info.QueryElementByID
findWidget('OOF2 Graphics 1:Pane0').set_position(444)

# Switched over to element mode.
assert findWidget(tbox+":Click:Element").get_active()
assert not findWidget(tbox+":Click:Node").get_active()
assert not findWidget(tbox+":Click:Segment").get_active()
assert tests.gtkMultiFloatCompare({'X Text':24,'Y Text':68.75},cbox)
assert tests.gtkMultiTextCompare({'Material':'<No material>','Group':'','Index':'54','Type':'quad'},elbox)
assert tests.gtkMultiFloatCompare({'Shape':0.308000,'Homog':0.988881,'Area':287.500000},elbox)
assert tests.sensitizationCheck({'Prev':True,'Clear':True,'Next':False},tbox)
assert tests.chooserCheck(elbox+":SegmentList",["Segment 79, nodes (43, 52) (length: 12.5)","Segment 130, nodes (43, 44) (length: 18.5)","Segment 127, nodes (44, 53) (length: 15.4029)","Segment 131, nodes (52, 53) (length: 27.5)"])
assert tests.chooserCheck(elbox+":NodeList",["Node 43 at (12.5, 62.5) (angle: 90)","Node 44 at (31, 62.5) (angle: 125.754)","Node 53 at (40, 75) (angle: 54.2461)","Node 52 at (12.5, 75) (angle: 90)"])
assert tests.chooserListStateCheck(elbox+":NodeList",["Node 44 at (31, 62.5) (angle: 125.754)"])
assert tests.chooserListStateCheck(elbox+":SegmentList",["Segment 130, nodes (43, 44) (length: 18.5)"])

findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
checkpoint OOF.Graphics_1.Layer.Select
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:Delete').activate()
findWidget('OOF2 Graphics 1:Pane0').set_position(444)
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
checkpoint OOF.Graphics_1.Layer.Delete

# Layer deleted.
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
findWidget('Dialog-Python_Log').resize(194, 69)
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
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_p')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_pe')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_pee')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_peek')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_peek.')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_peek.l')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_peek.lo')
findWidget('Dialog-Python_Log:filename').set_text('skelinfotbox_peek.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('skelinfotbox_peek.log')
os.remove('skelinfotbox_peek.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
