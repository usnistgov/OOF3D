checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:37 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
assert tests.sensitization0()
findWidget('OOF2').resize(550, 377)
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(194, 72)
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
findWidget('OOF2 Activity Viewer').resize(400, 300)
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
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
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
assert tests.sensitization1()
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
assert tests.is_sensitive('Dialog-Create a new mesh:gtk-ok')
setComboBox(findWidget('Dialog-Create a new mesh:element_types:Map'), '2')
assert not tests.is_sensitive('Dialog-Create a new mesh:gtk-ok')
setComboBox(findWidget('Dialog-Create a new mesh:element_types:Func'), '2')
assert tests.is_sensitive('Dialog-Create a new mesh:gtk-ok')
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
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
assert tests.sensitization2()
assert tests.subproblemNameCheck('default')
assert tests.selectedSubproblem('default')
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
findWidget('OOF2').resize(684, 377)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material material to pixels
findWidget('Dialog-Assign material material to pixels').resize(576, 108)
setComboBox(findWidget('Dialog-Assign material material to pixels:pixels'), '<all>')
findWidget('Dialog-Assign material material to pixels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(356)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
findWidget('Dialog-Create a new Element group').resize(249, 72)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(356)
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(356)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
setComboBox(findWidget('OOF2:FE Mesh Page:Pane:ElementOps:Method:Assign Material:target:Chooser'), 'Element Group')
assert tests.groupChooserCheck('elementgroup')
assert tests.sensitization3()
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(288, 104)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'Material')
findWidget('Dialog-Create a new subproblem').resize(288, 132)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.New
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 1.0000000000000e+00)
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 0.0000000000000e+00)
assert tests.sensitization4()
assert tests.subproblemNameCheck('default', 'subproblem')
assert tests.selectedSubproblem('subproblem')
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(288, 132)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'Union')
findWidget('Dialog-Create a new subproblem').resize(302, 160)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Union:another'), 'subproblem')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(712, 200)
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.New
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 2.3000000000000e+01)
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 1.0000000000000e+00)
assert tests.sensitization4()
assert tests.subproblemNameCheck('default', 'subproblem', 'subproblem<2>')
assert tests.selectedSubproblem('subproblem<2>')
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll:subprobChooser').get_selection().select_path((1,))
checkpoint mesh page subproblems sensitized
assert tests.sensitization4()
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(359, 94)
findWidget('Questioner:gtk-yes').clicked()
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 0.0000000000000e+00)
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Delete
assert tests.sensitization3()
assert tests.subproblemNameCheck('default')
assert tests.selectedSubproblem('default')
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(288, 160)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'PixelGroup')
findWidget('Dialog-Create a new subproblem').resize(636, 160)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.New
assert tests.sensitization4()
assert tests.subproblemNameCheck('default', 'subproblem')
assert tests.selectedSubproblem('subproblem')
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 1.0000000000000e+00)
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 0.0000000000000e+00)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(684, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Skeleton.New
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
assert tests.sensitization4()
assert tests.subproblemNameCheck('default', 'subproblem')
setComboBox(findWidget('OOF2:FE Mesh Page:Skeleton'), 'skeleton<2>')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
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
assert tests.sensitization1()
assert tests.subproblemNameCheck()
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
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
assert tests.sensitization2()
assert tests.subproblemNameCheck('default')
assert tests.selectedSubproblem('default')
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
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
assert tests.sensitization2()
assert tests.subproblemNameCheck('default')
assert tests.selectedSubproblem('default')
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(636, 132)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.New
assert tests.sensitization5()
assert tests.subproblemNameCheck('default', 'subproblem')
assert tests.selectedSubproblem('subproblem')
setComboBox(findWidget('OOF2:FE Mesh Page:Mesh'), 'mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
assert tests.sensitization2()
assert tests.subproblemNameCheck('default')
assert tests.selectedSubproblem('default')
setComboBox(findWidget('OOF2:FE Mesh Page:Skeleton'), 'skeleton')
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
assert tests.sensitization3()
assert tests.subproblemNameCheck('default', 'subproblem')
assert tests.selectedSubproblem('default')
setComboBox(findWidget('OOF2:FE Mesh Page:Skeleton'), 'skeleton<2>')
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
assert tests.sensitization2()
assert tests.subproblemNameCheck('default')
assert tests.selectedSubproblem('default')
findWidget('OOF2:FE Mesh Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(318, 94)
findWidget('Questioner:gtk-yes').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Mesh.Delete
assert tests.sensitization6()
assert tests.subproblemNameCheck('default', 'subproblem')
assert tests.selectedSubproblem(None)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
findWidget('OOF2:Skeleton Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(220, 94)
findWidget('Questioner:gtk-ok').clicked()
checkpoint skeleton page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Delete
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
assert tests.sensitization7()
assert tests.subproblemNameCheck('default', 'subproblem')
assert tests.selectedSubproblem(None)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:RemoveMaterial').clicked()
checkpoint toplevel widget mapped Dialog-Remove the assigned material from pixels
findWidget('Dialog-Remove the assigned material from pixels').resize(576, 108)
setComboBox(findWidget('Dialog-Remove the assigned material from pixels:pixels'), '<all>')
findWidget('Dialog-Remove the assigned material from pixels:gtk-ok').clicked()
checkpoint OOF.Material.Remove
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
assert tests.sensitization7()
assert tests.subproblemNameCheck('default', 'subproblem')
assert tests.selectedSubproblem(None)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
findWidget('OOF2:Materials Page:Pane:Material:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.Delete
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
assert tests.sensitization6()
assert tests.subproblemNameCheck('default', 'subproblem')
assert tests.selectedSubproblem(None)
findWidget('OOF2:FE Mesh Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(289, 94)
findWidget('Questioner:gtk-yes').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Mesh.Delete
assert tests.sensitization1()
assert tests.subproblemNameCheck()
assert tests.selectedSubproblem(None)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('m')
findWidget('Dialog-Python_Log:filename').set_text('me')
findWidget('Dialog-Python_Log:filename').set_text('mes')
findWidget('Dialog-Python_Log:filename').set_text('mesh')
findWidget('Dialog-Python_Log:filename').set_text('meshp')
findWidget('Dialog-Python_Log:filename').set_text('meshpa')
findWidget('Dialog-Python_Log:filename').set_text('meshpat')
findWidget('Dialog-Python_Log:filename').set_text('meshpate')
findWidget('Dialog-Python_Log:filename').set_text('meshpat')
findWidget('Dialog-Python_Log:filename').set_text('meshpa')
findWidget('Dialog-Python_Log:filename').set_text('meshpag')
findWidget('Dialog-Python_Log:filename').set_text('meshpage')
findWidget('Dialog-Python_Log:filename').set_text('meshpage.')
findWidget('Dialog-Python_Log:filename').set_text('meshpage.l')
findWidget('Dialog-Python_Log:filename').set_text('meshpage.lo')
findWidget('Dialog-Python_Log:filename').set_text('meshpage.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('meshpage.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
