checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

## This file tests for the absence of a bug that was causing KeyErrors
## when switching to the Boundary Condition page after editing a
## Subproblem.

import tests

findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(150)
findWidget('OOF2:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(342, 144)
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
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../exampls')
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
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
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
checkpoint OOF.Microstructure.Create_From_ImageFile
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(593, 350)
findWidget('OOF2:Image Page:Pane').set_position(380)
findWidget('OOF2:Image Page:Group').clicked()
checkpoint toplevel widget mapped Dialog-AutoGroup
findWidget('Dialog-AutoGroup').resize(211, 72)
findWidget('Dialog-AutoGroup:gtk-ok').clicked()
findWidget('OOF2 Activity Viewer').resize(400, 300)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint OOF.Image.AutoGroup
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:x_elements').set_text('')
findWidget('Dialog-New skeleton:x_elements').set_text('1')
findWidget('Dialog-New skeleton:x_elements').set_text('10')
findWidget('Dialog-New skeleton:y_elements').set_text('')
findWidget('Dialog-New skeleton:y_elements').set_text('1')
findWidget('Dialog-New skeleton:y_elements').set_text('10')
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton page sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Skeleton.New
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(550, 200)
checkpoint mesh bdy page updated
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Mesh.New
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(288, 104)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'PixelGroup')
findWidget('Dialog-Create a new subproblem').resize(884, 132)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.New
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(676, 434)
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem')
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint OOF.Subproblem.Field.Undefine
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature in-plane').clicked()
checkpoint OOF.Mesh.Field.In_Plane
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem')
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Heat_Eqn active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Conditions')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(332)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 276)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(332)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(743, 200)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(332)
checkpoint OOF.Mesh.Boundary_Conditions.New
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Subproblem definition
findWidget('Dialog-Edit Subproblem definition').resize(884, 108)
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:PixelGroup:group'), 'RGBColor(red=0.97255,green=0.00000,blue=0.97255)')
findWidget('Dialog-Edit Subproblem definition:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Edit
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Conditions')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(332)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('b')
findWidget('Dialog-Python_Log:filename').set_text('bc')
findWidget('Dialog-Python_Log:filename').set_text('bcb')
findWidget('Dialog-Python_Log:filename').set_text('bcbu')
findWidget('Dialog-Python_Log:filename').set_text('bcbug')
findWidget('Dialog-Python_Log:filename').set_text('bcbugl')
findWidget('Dialog-Python_Log:filename').set_text('bcbuglo')
findWidget('Dialog-Python_Log:filename').set_text('bcbuglog')
findWidget('Dialog-Python_Log:filename').set_text('bcbuglo')
findWidget('Dialog-Python_Log:filename').set_text('bcbugl')
findWidget('Dialog-Python_Log:filename').set_text('bcbug')
findWidget('Dialog-Python_Log:filename').set_text('bcbug.')
findWidget('Dialog-Python_Log:filename').set_text('bcbug.l')
findWidget('Dialog-Python_Log:filename').set_text('bcbug.lo')
findWidget('Dialog-Python_Log:filename').set_text('bcbug.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('bcbug.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
