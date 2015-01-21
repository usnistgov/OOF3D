# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.9 $
# $Author: fyc $
# $Date: 2014/09/22 22:17:31 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing the basic actions of the Analysis Page

findWidget('OOF3D').resize(550, 350)
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 65)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/two_walls.mesh')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint named analysis chooser set
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
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Solver page sensitized
checkpoint microstructure page sensitized
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
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint named analysis chooser set
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
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
checkpoint named analysis chooser set
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.File.Load.Data
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint microstructure page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane').set_position(304)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Analysis')
checkpoint page installed Analysis
findWidget('OOF3D:Analysis Page:bottom').set_position(287)
findWidget('OOF3D').resize(787, 350)
findWidget('OOF3D:Analysis Page:top').set_position(412)
findWidget('OOF3D:Analysis Page:bottom').set_position(412)
findWidget('OOF3D').resize(787, 350)
findWidget('OOF3D').resize(793, 355)
findWidget('OOF3D:Analysis Page:bottom').set_position(415)
findWidget('OOF3D:Analysis Page:top').set_position(415)
findWidget('OOF3D').resize(796, 356)
findWidget('OOF3D:Analysis Page:bottom').set_position(417)
findWidget('OOF3D:Analysis Page:top').set_position(417)
findWidget('OOF3D').resize(802, 359)
findWidget('OOF3D:Analysis Page:bottom').set_position(420)
findWidget('OOF3D:Analysis Page:top').set_position(420)
findWidget('OOF3D').resize(810, 363)
findWidget('OOF3D:Analysis Page:bottom').set_position(424)
findWidget('OOF3D:Analysis Page:top').set_position(424)
findWidget('OOF3D').resize(816, 369)
findWidget('OOF3D:Analysis Page:bottom').set_position(427)
findWidget('OOF3D:Analysis Page:top').set_position(427)
findWidget('OOF3D').resize(827, 377)
findWidget('OOF3D:Analysis Page:bottom').set_position(433)
findWidget('OOF3D:Analysis Page:top').set_position(433)
findWidget('OOF3D').resize(848, 390)
findWidget('OOF3D:Analysis Page:bottom').set_position(444)
findWidget('OOF3D:Analysis Page:top').set_position(444)
findWidget('OOF3D').resize(863, 398)
findWidget('OOF3D:Analysis Page:bottom').set_position(452)
findWidget('OOF3D:Analysis Page:top').set_position(452)
findWidget('OOF3D').resize(902, 423)
findWidget('OOF3D:Analysis Page:bottom').set_position(473)
findWidget('OOF3D:Analysis Page:top').set_position(473)
findWidget('OOF3D').resize(940, 447)
findWidget('OOF3D:Analysis Page:bottom').set_position(493)
findWidget('OOF3D:Analysis Page:top').set_position(493)
findWidget('OOF3D').resize(992, 479)
findWidget('OOF3D:Analysis Page:bottom').set_position(521)
findWidget('OOF3D:Analysis Page:top').set_position(521)
findWidget('OOF3D').resize(1031, 500)
findWidget('OOF3D:Analysis Page:bottom').set_position(541)
findWidget('OOF3D:Analysis Page:top').set_position(542)
findWidget('OOF3D').resize(1085, 528)
findWidget('OOF3D:Analysis Page:bottom').set_position(571)
findWidget('OOF3D:Analysis Page:top').set_position(571)
findWidget('OOF3D').resize(1143, 556)
findWidget('OOF3D:Analysis Page:bottom').set_position(602)
findWidget('OOF3D:Analysis Page:top').set_position(602)
findWidget('OOF3D').resize(1195, 584)
findWidget('OOF3D:Analysis Page:bottom').set_position(630)
findWidget('OOF3D:Analysis Page:top').set_position(630)
findWidget('OOF3D').resize(1230, 605)
findWidget('OOF3D:Analysis Page:bottom').set_position(649)
findWidget('OOF3D:Analysis Page:top').set_position(649)
findWidget('OOF3D').resize(1268, 619)
findWidget('OOF3D:Analysis Page:bottom').set_position(669)
findWidget('OOF3D:Analysis Page:top').set_position(669)
findWidget('OOF3D').resize(1295, 631)
findWidget('OOF3D:Analysis Page:bottom').set_position(683)
findWidget('OOF3D:Analysis Page:top').set_position(683)
findWidget('OOF3D').resize(1315, 643)
findWidget('OOF3D:Analysis Page:bottom').set_position(694)
findWidget('OOF3D:Analysis Page:top').set_position(694)
findWidget('OOF3D').resize(1331, 651)
findWidget('OOF3D:Analysis Page:bottom').set_position(702)
findWidget('OOF3D:Analysis Page:top').set_position(702)
findWidget('OOF3D').resize(1347, 659)
findWidget('OOF3D:Analysis Page:bottom').set_position(710)
findWidget('OOF3D:Analysis Page:top').set_position(710)
findWidget('OOF3D').resize(1352, 660)
findWidget('OOF3D:Analysis Page:bottom').set_position(713)
findWidget('OOF3D:Analysis Page:top').set_position(713)
findWidget('OOF3D').resize(1353, 661)
findWidget('OOF3D:Analysis Page:top').set_position(714)
findWidget('OOF3D:Analysis Page:bottom').set_position(714)
findWidget('OOF3D').resize(1356, 664)
findWidget('OOF3D:Analysis Page:bottom').set_position(716)
findWidget('OOF3D:Analysis Page:top').set_position(716)
findWidget('OOF3D').resize(1362, 670)
findWidget('OOF3D:Analysis Page:bottom').set_position(719)
findWidget('OOF3D:Analysis Page:top').set_position(719)
findWidget('OOF3D').resize(1368, 675)
findWidget('OOF3D:Analysis Page:bottom').set_position(722)
findWidget('OOF3D:Analysis Page:top').set_position(722)
findWidget('OOF3D').resize(1372, 678)
findWidget('OOF3D:Analysis Page:bottom').set_position(724)
findWidget('OOF3D:Analysis Page:top').set_position(724)
findWidget('OOF3D').resize(1372, 678)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Component')
assert tests.SetOutputCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetOutputSelect(0, 'Field')
assert tests.SetOutputCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetOutputSelect(1, 'Component')
assert tests.SetParameterCheck('component',('x','y','z'))
assert tests.SetParameterSelect('component','x')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:component'), 'y')
assert tests.SetParameterCheck('component',('x','y','z'))
assert tests.SetParameterSelect('component','y')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Derivative')
assert tests.SetOutputCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetOutputSelect(1, 'Derivative')
assert tests.SetParameterCheck('derivative',('x','y','z'))
assert tests.SetParameterSelect('derivative','x')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_2'), 'Invariant')
assert tests.SetOutputCheck(2, ('Value','Component','Invariant'))
assert tests.SetOutputSelect(2, 'Invariant')
assert tests.SetParameterCheck('derivative',('x','y','z'))
assert tests.SetParameterSelect('derivative','x')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_2'), 'Value')
assert tests.SetOutputCheck(2, ('Value','Component','Invariant'))
assert tests.SetOutputSelect(2, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Invariant')
assert tests.SetOutputCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetOutputSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Value')
assert tests.SetOutputCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetOutputSelect(1, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_0'), 'Flux')
assert tests.SetOutputCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetOutputSelect(0, 'Flux')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Component')
assert tests.SetOutputCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetOutputSelect(1, 'Component')
assert tests.SetParameterCheck('component',('xx','yy','zz','yz','xz','xy'))
assert tests.SetParameterSelect('component','xx')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Invariant')
assert tests.SetOutputCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetOutputSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Normal')
assert tests.SetOutputCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetOutputSelect(1, 'Normal')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Value')
assert tests.SetOutputCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetOutputSelect(1, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_0'), 'Energy')
assert tests.SetOutputCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetOutputSelect(0, 'Energy')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:etype'), 'Elastic')
assert tests.SetParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetParameterSelect('etype','Elastic')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:etype'), 'Electric')
assert tests.SetParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetParameterSelect('etype','Electric')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:etype'), 'Total')
assert tests.SetParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetParameterSelect('etype','Total')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_0'), 'Strain')
assert tests.SetOutputCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetOutputSelect(0, 'Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Geometric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Component')
assert tests.SetOutputCheck(1, ('Value','Component','Invariant'))
assert tests.SetOutputSelect(1, 'Component')
assert tests.SetParameterCheck('component',('xx','yy','zz','yz','xz','xy'))
assert tests.SetParameterSelect('component','xx')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Geometric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Geometric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Invariant')
assert tests.SetOutputCheck(1, ('Value','Component','Invariant'))
assert tests.SetOutputSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser'), 'Geometric Strain')
assert tests.SetTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetTypeSelect('Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Value')
assert tests.SetOutputCheck(1, ('Value','Component','Invariant'))
assert tests.SetOutputSelect(1, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_0'), 'XYZFunction')
assert tests.SetOutputCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetOutputSelect(0, 'XYZFunction')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Vector')
assert tests.SetOutputCheck(1, ('Scalar','Vector'))
assert tests.SetOutputSelect(1, 'Vector')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_1'), 'Scalar')
assert tests.SetOutputCheck(1, ('Scalar','Vector'))
assert tests.SetOutputSelect(1, 'Scalar')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_0'), 'Difference')
assert tests.SetOutputCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetOutputSelect(0, 'Difference')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_1'), 'Component')
assert tests.SetSubtrahendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetSubtrahendSelect(1, 'Component')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_1'), 'Derivative')
assert tests.SetSubtrahendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetSubtrahendSelect(1, 'Derivative')
checkpoint named analysis chooser set
findWidget('OOF3D').resize(1372, 686)
findWidget('OOF3D').resize(1372, 689)
findWidget('OOF3D').resize(1372, 696)
findWidget('OOF3D').resize(1372, 703)
findWidget('OOF3D').resize(1373, 710)
findWidget('OOF3D:Analysis Page:bottom').set_position(725)
findWidget('OOF3D:Analysis Page:top').set_position(725)
findWidget('OOF3D').resize(1374, 714)
findWidget('OOF3D:Analysis Page:bottom').set_position(726)
findWidget('OOF3D:Analysis Page:top').set_position(726)
findWidget('OOF3D').resize(1374, 720)
findWidget('OOF3D').resize(1374, 725)
findWidget('OOF3D').resize(1375, 729)
findWidget('OOF3D:Analysis Page:bottom').set_position(727)
findWidget('OOF3D:Analysis Page:top').set_position(727)
findWidget('OOF3D').resize(1376, 732)
findWidget('OOF3D:Analysis Page:bottom').set_position(728)
findWidget('OOF3D:Analysis Page:top').set_position(728)
findWidget('OOF3D').resize(1377, 739)
findWidget('OOF3D:Analysis Page:bottom').set_position(729)
findWidget('OOF3D:Analysis Page:top').set_position(729)
findWidget('OOF3D').resize(1377, 745)
findWidget('OOF3D').resize(1378, 750)
findWidget('OOF3D:Analysis Page:bottom').set_position(730)
findWidget('OOF3D:Analysis Page:top').set_position(730)
findWidget('OOF3D').resize(1379, 758)
findWidget('OOF3D:Analysis Page:bottom').set_position(731)
findWidget('OOF3D:Analysis Page:top').set_position(731)
findWidget('OOF3D').resize(1379, 761)
findWidget('OOF3D').resize(1379, 763)
findWidget('OOF3D').resize(1379, 765)
findWidget('OOF3D').resize(1380, 770)
findWidget('OOF3D:Analysis Page:bottom').set_position(732)
findWidget('OOF3D:Analysis Page:top').set_position(732)
findWidget('OOF3D').resize(1380, 773)
findWidget('OOF3D').resize(1380, 776)
findWidget('OOF3D').resize(1380, 778)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_2'), 'Component')
assert tests.SetSubtrahendCheck(2, ('Value','Component','Invariant'))
assert tests.SetSubtrahendSelect(2, 'Component')
checkpoint named analysis chooser set
findWidget('OOF3D').resize(1383, 785)
findWidget('OOF3D:Analysis Page:bottom').set_position(734)
findWidget('OOF3D:Analysis Page:top').set_position(734)
findWidget('OOF3D').resize(1384, 789)
findWidget('OOF3D:Analysis Page:bottom').set_position(735)
findWidget('OOF3D:Analysis Page:top').set_position(735)
findWidget('OOF3D').resize(1392, 801)
findWidget('OOF3D:Analysis Page:bottom').set_position(739)
findWidget('OOF3D:Analysis Page:top').set_position(739)
findWidget('OOF3D').resize(1399, 809)
findWidget('OOF3D:Analysis Page:bottom').set_position(743)
findWidget('OOF3D:Analysis Page:top').set_position(743)
findWidget('OOF3D').resize(1406, 819)
findWidget('OOF3D:Analysis Page:bottom').set_position(747)
findWidget('OOF3D:Analysis Page:top').set_position(747)
findWidget('OOF3D').resize(1414, 828)
findWidget('OOF3D:Analysis Page:bottom').set_position(751)
findWidget('OOF3D:Analysis Page:top').set_position(751)
findWidget('OOF3D').resize(1417, 833)
findWidget('OOF3D:Analysis Page:bottom').set_position(753)
findWidget('OOF3D:Analysis Page:top').set_position(753)
findWidget('OOF3D').resize(1419, 834)
findWidget('OOF3D:Analysis Page:bottom').set_position(754)
findWidget('OOF3D:Analysis Page:top').set_position(754)
findWidget('OOF3D').resize(1419, 834)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_2'), 'Invariant')
assert tests.SetSubtrahendCheck(2, ('Value','Component','Invariant'))
assert tests.SetSubtrahendSelect(2, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_2'), 'Value')
assert tests.SetSubtrahendCheck(2, ('Value','Component','Invariant'))
assert tests.SetSubtrahendSelect(2, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_1'), 'Invariant')
assert tests.SetSubtrahendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetSubtrahendSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_1'), 'Value')
assert tests.SetSubtrahendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetSubtrahendSelect(1, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Component')
assert tests.SetMinuendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetMinuendSelect(1, 'Component')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Derivative')
assert tests.SetMinuendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetMinuendSelect(1, 'Derivative')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_2'), 'Component')
assert tests.SetMinuendCheck(2, ('Value','Component','Invariant'))
assert tests.SetMinuendSelect(2, 'Component')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_2'), 'Invariant')
assert tests.SetMinuendCheck(2, ('Value','Component','Invariant'))
assert tests.SetMinuendSelect(2, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_2'), 'Value')
assert tests.SetMinuendCheck(2, ('Value','Component','Invariant'))
assert tests.SetMinuendSelect(2, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Invariant')
assert tests.SetMinuendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetMinuendSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Value')
assert tests.SetMinuendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetMinuendSelect(1, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_0'), 'Flux')
assert tests.SetMinuendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSelect(0, 'Flux')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Component')
assert tests.SetMinuendCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetMinuendSelect(1, 'Component')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Invariant')
assert tests.SetMinuendCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetMinuendSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Normal')
assert tests.SetMinuendCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetMinuendSelect(1, 'Normal')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_2'), 'Invariant')
assert tests.SetMinuendCheck(2, ('Value','Invariant'))
assert tests.SetMinuendSelect(2, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_2'), 'Value')
assert tests.SetMinuendCheck(2, ('Value','Invariant'))
assert tests.SetMinuendSelect(2, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Value')
assert tests.SetMinuendCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetMinuendSelect(1, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_0'), 'Energy')
assert tests.SetMinuendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSelect(0, 'Energy')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:etype'), 'Elastic')
assert tests.SetMinuendParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetMinuendParameterSelect('etype','Elastic')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:etype'), 'Electric')
assert tests.SetMinuendParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetMinuendParameterSelect('etype','Electric')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:etype'), 'Total')
assert tests.SetMinuendParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetMinuendParameterSelect('etype','Total')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_0'), 'Strain')
assert tests.SetMinuendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSelect(0, 'Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Geometric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Component')
assert tests.SetMinuendCheck(1, ('Value','Component','Invariant'))
assert tests.SetMinuendSelect(1, 'Component')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Geometric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Geometric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Invariant')
assert tests.SetMinuendCheck(1, ('Value','Component','Invariant'))
assert tests.SetMinuendSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser'), 'Geometric Strain')
assert tests.SetMinuendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendTypeSelect('Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Value')
assert tests.SetMinuendCheck(1, ('Value','Component','Invariant'))
assert tests.SetMinuendSelect(1, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_0'), 'XYZFunction')
assert tests.SetMinuendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSelect(0, 'XYZFunction')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Vector')
assert tests.SetMinuendCheck(1, ('Scalar','Vector'))
assert tests.SetMinuendSelect(1, 'Vector')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_1'), 'Scalar')
assert tests.SetMinuendCheck(1, ('Scalar','Vector'))
assert tests.SetMinuendSelect(1, 'Scalar')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_0'), 'Difference')
assert tests.SetMinuendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSelect(0, 'Difference')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Component')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetMinuendSubtrahendSelect(1, 'Component')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Derivative')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetMinuendSubtrahendSelect(1, 'Derivative')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_2'), 'Component')
assert tests.SetMinuendSubtrahendCheck(2, ('Value','Component','Invariant'))
assert tests.SetMinuendSubtrahendSelect(2, 'Component')
checkpoint named analysis chooser set
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 1.3970588235294e+00)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 2.7941176470588e+00)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 4.1911764705882e+00)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 5.5882352941176e+00)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 8.3823529411765e+00)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 9.7794117647059e+00)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 1.3970588235294e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 1.6764705882353e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 2.2352941176471e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 2.6544117647059e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 3.0735294117647e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 3.6323529411765e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 4.0514705882353e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 4.4705882352941e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 5.0294117647059e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 5.4485294117647e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 6.0073529411765e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 6.4264705882353e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 6.9852941176471e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 7.6838235294118e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 8.5220588235294e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 9.3602941176471e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 9.5000000000000e+01)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_2'), 'Invariant')
assert tests.SetMinuendSubtrahendCheck(2, ('Value','Component','Invariant'))
assert tests.SetMinuendSubtrahendSelect(2, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_2'), 'Value')
assert tests.SetMinuendSubtrahendCheck(2, ('Value','Component','Invariant'))
assert tests.SetMinuendSubtrahendSelect(2, 'Value')
checkpoint named analysis chooser set
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 6.8000000000000e+01)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Invariant')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetMinuendSubtrahendSelect(1, 'Invariant')
checkpoint named analysis chooser set
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 4.3000000000000e+01)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Value')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Derivative','Invariant'))
assert tests.SetMinuendSubtrahendSelect(1, 'Value')
checkpoint named analysis chooser set
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 1.4000000000000e+01)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_0'), 'Flux')
assert tests.SetMinuendSubtrahendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSubtrahendSelect(0, 'Flux')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Component')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetMinuendSubtrahendSelect(1, 'Component')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Invariant')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetMinuendSubtrahendSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Normal')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Invariant','Normal'))
assert tests.SetMinuendSubtrahendSelect(1, 'Normal')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_2'), 'Invariant')
assert tests.SetMinuendSubtrahendCheck(2, ('Value','Invariant'))
assert tests.SetMinuendSubtrahendSelect(2, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_2'), 'Value')
assert tests.SetMinuendSubtrahendCheck(2, ('Value','Invariant'))
assert tests.SetMinuendSubtrahendSelect(2, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_0'), 'Energy')
assert tests.SetMinuendSubtrahendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSubtrahendSelect(0, 'Energy')
checkpoint named analysis chooser set
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 0.0000000000000e+00)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:etype'), 'Elastic')
assert tests.SetMinuendSubtrahendParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetMinuendSubtrahendParameterSelect('etype','Elastic')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:etype'), 'Electric')
assert tests.SetMinuendSubtrahendParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetMinuendSubtrahendParameterSelect('etype','Electric')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:etype'), 'Total')
assert tests.SetMinuendSubtrahendParameterCheck('etype',('Total','Elastic','Electric'))
assert tests.SetMinuendSubtrahendParameterSelect('etype','Total')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_0'), 'Strain')
assert tests.SetMinuendSubtrahendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSubtrahendSelect(0, 'Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Component')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Invariant'))
assert tests.SetMinuendSubtrahendSelect(1, 'Component')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Geometric Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Geometric Strain')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Invariant')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Invariant'))
assert tests.SetMinuendSubtrahendSelect(1, 'Invariant')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Nonlinear Geometric Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Nonlinear Geometric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Elastic Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Elastic Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Thermal Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Thermal Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser'), 'Piezoelectric Strain')
assert tests.SetMinuendSubtrahendTypeCheck(('Geometric Strain','Nonlinear Geometric Strain','Elastic Strain','Thermal Strain','Piezoelectric Strain'))
assert tests.SetMinuendSubtrahendTypeSelect('Piezoelectric Strain')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Value')
assert tests.SetMinuendSubtrahendCheck(1, ('Value','Component','Invariant'))
assert tests.SetMinuendSubtrahendSelect(1, 'Value')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_0'), 'XYZFunction')
assert tests.SetMinuendSubtrahendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSubtrahendSelect(0, 'XYZFunction')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Vector')
assert tests.SetMinuendSubtrahendCheck(1, ('Scalar','Vector'))
assert tests.SetMinuendSubtrahendSelect(1, 'Vector')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_1'), 'Scalar')
assert tests.SetMinuendSubtrahendCheck(1, ('Scalar','Vector'))
assert tests.SetMinuendSubtrahendSelect(1, 'Scalar')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_0'), 'Difference')
assert tests.SetMinuendSubtrahendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSubtrahendSelect(0, 'Difference')
checkpoint named analysis chooser set
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 4.4114200584799e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 8.8228401169597e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 1.2600000000000e+02)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 8.1885799415201e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 3.7771598830403e+01)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_0'), 'Field')
assert tests.SetMinuendSubtrahendCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetMinuendSubtrahendSelect(0, 'Field')
checkpoint named analysis chooser set
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 1.4000000000000e+01)
findWidget('OOF3D:Analysis Page:top:Output').get_vadjustment().set_value( 0.0000000000000e+00)
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_0'), 'Field')
assert tests.SetOutputCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetOutputSelect(0, 'Difference')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Output:Outputs:Outputs_0'), 'Field')
assert tests.SetOutputCheck(0, ('Field','Flux','Energy','Strain','XYZFunction','Difference'))
assert tests.SetOutputSelect(0, 'Field')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Single Point')
assert tests.SetDomainCheck(('Entire Mesh','Single Point','Voxel Group','Linear Cross Section','Planar Cross Section','Face Boundary','Point Boundary','Element Group'))
assert tests.SetDomainSelect('Single Point')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Voxel Group')
assert tests.SetDomainCheck(('Entire Mesh','Single Point','Voxel Group','Linear Cross Section','Planar Cross Section','Face Boundary','Point Boundary','Element Group'))
assert tests.SetDomainSelect('Voxel Group')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Voxel Group:group'), '<every>')
assert tests.SetDomainParametersSimpleCheck('Voxel Group', 'group', ('<selection>','<every>','#cea039','#cb9836','#ca9735','#9a1200','#000000'))
assert tests.SetDomainParametersSimpleSelect('Voxel Group', 'group', '<every>')
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Voxel Group:group'), '#cea039')
assert tests.SetDomainParametersSimpleCheck('Voxel Group', 'group', ('<selection>','<every>','#cea039','#cb9836','#ca9735','#9a1200','#000000'))
assert tests.SetDomainParametersSimpleSelect('Voxel Group', 'group', '#cea039')
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Voxel Group:group'), '#cb9836')
assert tests.SetDomainParametersSimpleCheck('Voxel Group', 'group', ('<selection>','<every>','#cea039','#cb9836','#ca9735','#9a1200','#000000'))
assert tests.SetDomainParametersSimpleSelect('Voxel Group', 'group', '#cb9836')
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Voxel Group:group'), '#ca9735')
assert tests.SetDomainParametersSimpleCheck('Voxel Group', 'group', ('<selection>','<every>','#cea039','#cb9836','#ca9735','#9a1200','#000000'))
assert tests.SetDomainParametersSimpleSelect('Voxel Group', 'group', '#ca9735')
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Voxel Group:group'), '#9a1200')
assert tests.SetDomainParametersSimpleCheck('Voxel Group', 'group', ('<selection>','<every>','#cea039','#cb9836','#ca9735','#9a1200','#000000'))
assert tests.SetDomainParametersSimpleSelect('Voxel Group', 'group', '#9a1200')
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Voxel Group:group'), '#000000')
assert tests.SetDomainParametersSimpleCheck('Voxel Group', 'group', ('<selection>','<every>','#cea039','#cb9836','#ca9735','#9a1200','#000000'))
assert tests.SetDomainParametersSimpleSelect('Voxel Group', 'group', '#000000')
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Voxel Group:group'), '<selection>')
assert tests.SetDomainParametersSimpleCheck('Voxel Group', 'group', ('<selection>','<every>','#cea039','#cb9836','#ca9735','#9a1200','#000000'))
assert tests.SetDomainParametersSimpleSelect('Voxel Group', 'group', '<selection>')
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Linear Cross Section')
assert tests.SetDomainCheck(('Entire Mesh','Single Point','Voxel Group','Linear Cross Section','Planar Cross Section','Face Boundary','Point Boundary','Element Group'))
assert tests.SetDomainSelect('Linear Cross Section')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Planar Cross Section')
assert tests.SetDomainCheck(('Entire Mesh','Single Point','Voxel Group','Linear Cross Section','Planar Cross Section','Face Boundary','Point Boundary','Element Group'))
assert tests.SetDomainSelect('Planar Cross Section')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Planar Cross Section:normal:Chooser'), 'Angles')
assert tests.SetDomainParametersChooserCheck('Planar Cross Section', 'normal', ('X', 'Y','Z', 'Vector','Angles'))
assert tests.SetDomainParametersChooserSelect('Planar Cross Section', 'normal', 'Angles')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Planar Cross Section:normal:Chooser'), 'Vector')
assert tests.SetDomainParametersChooserCheck('Planar Cross Section', 'normal', ('X', 'Y','Z', 'Vector','Angles'))
assert tests.SetDomainParametersChooserSelect('Planar Cross Section', 'normal', 'Vector')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Planar Cross Section:side'), 'BACK')
assert tests.SetDomainParametersSimpleCheck('Planar Cross Section', 'side', ('FRONT','BACK'))
assert tests.SetDomainParametersSimpleSelect('Planar Cross Section', 'side', 'BACK')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Planar Cross Section:side'), 'FRONT')
assert tests.SetDomainParametersSimpleCheck('Planar Cross Section', 'side', ('FRONT','BACK'))
assert tests.SetDomainParametersSimpleSelect('Planar Cross Section', 'side', 'FRONT')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Face Boundary')
assert tests.SetDomainCheck(('Entire Mesh','Single Point','Voxel Group','Linear Cross Section','Planar Cross Section','Face Boundary','Point Boundary','Element Group'))
assert tests.SetDomainSelect('Face Boundary')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Face Boundary:boundary'), 'Xmin')
assert tests.SetDomainParametersSimpleCheck('Face Boundary', 'boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin'))
assert tests.SetDomainParametersSimpleSelect('Face Boundary', 'boundary', 'Xmin')
assert tests.SetSamplingCheck()
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Face Boundary:boundary'), 'Ymax')
assert tests.SetDomainParametersSimpleCheck('Face Boundary', 'boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin'))
assert tests.SetDomainParametersSimpleSelect('Face Boundary', 'boundary', 'Ymax')
assert tests.SetSamplingCheck()
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Face Boundary:boundary'), 'Ymin')
assert tests.SetDomainParametersSimpleCheck('Face Boundary', 'boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin'))
assert tests.SetDomainParametersSimpleSelect('Face Boundary', 'boundary', 'Ymin')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Face Boundary:boundary'), 'Zmax')
assert tests.SetDomainParametersSimpleCheck('Face Boundary', 'boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin'))
assert tests.SetDomainParametersSimpleSelect('Face Boundary', 'boundary', 'Zmax')
assert tests.SetSamplingCheck()
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Face Boundary:boundary'), 'Zmin')
assert tests.SetDomainParametersSimpleCheck('Face Boundary', 'boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin'))
assert tests.SetDomainParametersSimpleSelect('Face Boundary', 'boundary', 'Zmin')
assert tests.SetSamplingCheck()
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Face Boundary:boundary'), 'Xmax')
assert tests.SetDomainParametersSimpleCheck('Face Boundary', 'boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin'))
assert tests.SetDomainParametersSimpleSelect('Face Boundary', 'boundary', 'Xmax')
assert tests.SetSamplingCheck()
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Face Boundary:side'), 'BACK')
assert tests.SetDomainParametersSimpleCheck('Face Boundary', 'side', ('FRONT','BACK'))
assert tests.SetDomainParametersSimpleSelect('Face Boundary', 'side', 'BACK')
assert tests.SetSamplingCheck()
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Face Boundary:side'), 'FRONT')
assert tests.SetDomainParametersSimpleCheck('Face Boundary', 'side', ('FRONT','BACK'))
assert tests.SetDomainParametersSimpleSelect('Face Boundary', 'side', 'FRONT')
assert tests.SetSamplingCheck()
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Point Boundary')
assert tests.SetDomainCheck(('Entire Mesh','Single Point','Voxel Group','Linear Cross Section','Planar Cross Section','Face Boundary','Point Boundary','Element Group'))
assert tests.SetDomainSelect('Point Boundary')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Point Boundary:boundary'), 'XmaxYmaxZmin')
assert tests.SetDomainParametersSimpleCheck('Point Boundary', 'boundary', ('XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin'))
assert tests.SetDomainParametersSimpleSelect('Point Boundary', 'boundary', 'XmaxYmaxZmin')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Point Boundary:boundary'), 'XmaxYminZmax')
assert tests.SetDomainParametersSimpleCheck('Point Boundary', 'boundary', ('XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin'))
assert tests.SetDomainParametersSimpleSelect('Point Boundary', 'boundary', 'XmaxYminZmax')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Point Boundary:boundary'), 'XmaxYminZmin')
assert tests.SetDomainParametersSimpleCheck('Point Boundary', 'boundary', ('XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin'))
assert tests.SetDomainParametersSimpleSelect('Point Boundary', 'boundary', 'XmaxYminZmin')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Point Boundary:boundary'), 'XminYmaxZmax')
assert tests.SetDomainParametersSimpleCheck('Point Boundary', 'boundary', ('XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin'))
assert tests.SetDomainParametersSimpleSelect('Point Boundary', 'boundary', 'XminYmaxZmax')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Point Boundary:boundary'), 'XminYmaxZmin')
assert tests.SetDomainParametersSimpleCheck('Point Boundary', 'boundary', ('XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin'))
assert tests.SetDomainParametersSimpleSelect('Point Boundary', 'boundary', 'XminYmaxZmin')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Point Boundary:boundary'), 'XminYminZmax')
assert tests.SetDomainParametersSimpleCheck('Point Boundary', 'boundary', ('XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin'))
assert tests.SetDomainParametersSimpleSelect('Point Boundary', 'boundary', 'XminYminZmax')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Point Boundary:boundary'), 'XminYminZmin')
assert tests.SetDomainParametersSimpleCheck('Point Boundary', 'boundary', ('XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin'))
assert tests.SetDomainParametersSimpleSelect('Point Boundary', 'boundary', 'XminYminZmin')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Point Boundary:boundary'), 'XmaxYmaxZmax')
assert tests.SetDomainParametersSimpleCheck('Point Boundary', 'boundary', ('XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin'))
assert tests.SetDomainParametersSimpleSelect('Point Boundary', 'boundary', 'XmaxYmaxZmax')
assert tests.SetSamplingSelect('Discrete Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Element Group')
assert tests.SetDomainCheck(('Entire Mesh','Single Point','Voxel Group','Linear Cross Section','Planar Cross Section','Face Boundary','Point Boundary','Element Group'))
assert tests.SetDomainSelect('Element Group')
assert tests.SetSamplingCheck(('Grid Points','Spaced Grid Points'))
assert tests.SetSamplingSelect('Grid Points')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Entire Mesh')
assert tests.SetDomainCheck(('Entire Mesh','Single Point','Voxel Group','Linear Cross Section','Planar Cross Section','Face Boundary','Point Boundary','Element Group'))
assert tests.SetDomainSelect('Entire Mesh')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Spaced Grid Points')
assert tests.SetSamplingCheck(('Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Spaced Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Voxels')
assert tests.SetSamplingCheck(('Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Voxels')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Grid Points')
assert tests.SetSamplingCheck(('Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Range')
assert tests.SetOperationCheck(('Direct Output','Range','Average and Deviation','Average','Integral','Standard Deviation'))
assert tests.SetOperationSelect('Range')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Spaced Grid Points')
assert tests.SetSamplingCheck(('Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Spaced Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Voxels')
assert tests.SetSamplingCheck(('Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Voxels')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Grid Points')
assert tests.SetSamplingCheck(('Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Average and Deviation')
assert tests.SetOperationCheck(('Direct Output','Range','Average and Deviation','Average','Integral','Standard Deviation'))
assert tests.SetOperationSelect('Average and Deviation')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Spaced Grid Points')
assert tests.SetSamplingCheck(('Integrate','Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Spaced Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Voxels')
assert tests.SetSamplingCheck(('Integrate','Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Voxels')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Average')
assert tests.SetOperationCheck(('Direct Output','Range','Average and Deviation','Average','Integral','Standard Deviation'))
assert tests.SetOperationSelect('Average')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Grid Points')
assert tests.SetSamplingCheck(('Integrate','Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Spaced Grid Points')
assert tests.SetSamplingCheck(('Integrate','Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Spaced Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Voxels')
assert tests.SetSamplingCheck(('Integrate','Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Voxels')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Integral')
assert tests.SetOperationCheck(('Direct Output','Range','Average and Deviation','Average','Integral','Standard Deviation'))
assert tests.SetOperationSelect('Integral')
assert tests.SetSamplingSelect('Integrate')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Integrate')
assert tests.SetSamplingSelect('Integrate')
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Standard Deviation')
assert tests.SetOperationCheck(('Direct Output','Range','Average and Deviation','Average','Integral','Standard Deviation'))
assert tests.SetOperationSelect('Standard Deviation')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Grid Points')
assert tests.SetSamplingCheck(('Integrate','Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Spaced Grid Points')
assert tests.SetSamplingCheck(('Integrate','Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Spaced Grid Points')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Voxels')
assert tests.SetSamplingCheck(('Integrate','Grid Points','Spaced Grid Points','Voxels'))
assert tests.SetSamplingSelect('Voxels')
checkpoint named analysis chooser set
setComboBox(findWidget('OOF3D:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Direct Output')
assert tests.SetOperationCheck(('Direct Output','Range','Average and Deviation','Average','Integral','Standard Deviation'))
assert tests.SetOperationSelect('Direct Output')
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint named analysis chooser set
widget_0 = findWidget('OOF3D:Analysis Page:Name:Operations')
widget_0.event(event(gtk.gdk.BUTTON_PRESS,x= 2.4300000000000e+02,y= 1.3000000000000e+01,button=1,state=16,window=widget_0.window))
checkpoint toplevel widget mapped NamedOpsMenu
findWidget('NamedOpsMenu').deactivate()
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('analysispage.log')
findWidget('Dialog-Python_Log').resize(198, 92)
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('analysispage.log')
widget_1=findWidget('OOF3D')
handled_0=widget_1.event(event(gtk.gdk.DELETE,window=widget_1.window))