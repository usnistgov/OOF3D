# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing the Subproblems types and methods

findWidget('OOF3D').resize(550, 350)
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 65)
findWidget('Dialog-Data:filename').set_text('')
findWidget('Dialog-Data:filename').set_text('TEST_DATA/triangle.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint named analysis chooser set
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
checkpoint toplevel widget mapped OOF3D Activity Viewer
findWidget('OOF3D Activity Viewer').resize(400, 300)
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
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
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
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
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
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.File.Load.Data
widget_0=findWidget('OOF3D Activity Viewer')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
checkpoint OOF.ActivityViewer.File.Close
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Materials')
checkpoint Materials page updated
checkpoint page installed Materials
findWidget('OOF3D').resize(691, 350)
findWidget('OOF3D:Materials Page:Pane').set_position(278)
findWidget('OOF3D:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(300, 92)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.New
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
checkpoint Materials page updated
checkpoint property selected
widget_1=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_1.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_1.window))
findWidget('OOF3D:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Color
findWidget('Dialog-Parametrize Color').resize(256, 134)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 1.5384615384615e-02)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 3.0769230769231e-02)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 4.6153846153846e-02)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 6.1538461538462e-02)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 7.6923076923077e-02)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 9.2307692307692e-02)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 1.0769230769231e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 1.2307692307692e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 1.5384615384615e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 1.6923076923077e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 1.8461538461538e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 2.0000000000000e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 2.1538461538462e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 2.3076923076923e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 2.4615384615385e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 2.6153846153846e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 2.7692307692308e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 2.9230769230769e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 3.0769230769231e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 3.2307692307692e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 3.3846153846154e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 3.5384615384615e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 3.6923076923077e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 3.8461538461538e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 4.0000000000000e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 4.1538461538462e-01)
findWidget('Dialog-Parametrize Color:color:Gray:Gray:slider').get_adjustment().set_value( 4.3076923076923e-01)
findWidget('Dialog-Parametrize Color:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Color
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF3D:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material material to voxels
findWidget('Dialog-Assign material material to voxels').resize(252, 100)
setComboBox(findWidget('Dialog-Assign material material to voxels:pixels'), 'environment')
findWidget('Dialog-Assign material material to voxels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
findWidget('OOF3D:Skeleton Page:Pane').set_position(340)
checkpoint skeleton page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
assert tests.FEMeshPageInfoCheck()
assert tests.FEMeshPageCheck1()
assert tests.FEMeshPageSubproblemsCheck0()
assert tests.FEMeshPageOperationsCheck0()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:FE Mesh Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Skeleton', 'skeleton')
findWidget('OOF3D:FE Mesh Page:Pane').set_position(445)
findWidget('OOF3D:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(373, 229)
assert tests.MeshNewDialogCheck0()
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
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
checkpoint OOF.Mesh.New
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh')
assert tests.subproblemsCheck(['default'])
findWidget('OOF3D').resize(696, 359)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(450)
findWidget('OOF3D').resize(697, 363)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(451)
findWidget('OOF3D').resize(698, 366)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(452)
findWidget('OOF3D').resize(699, 374)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(453)
findWidget('OOF3D').resize(700, 386)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(454)
findWidget('OOF3D').resize(702, 401)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(456)
findWidget('OOF3D').resize(703, 413)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(457)
findWidget('OOF3D').resize(703, 420)
findWidget('OOF3D').resize(703, 424)
findWidget('OOF3D').resize(704, 427)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(458)
findWidget('OOF3D').resize(704, 431)
findWidget('OOF3D').resize(704, 436)
findWidget('OOF3D').resize(704, 437)
findWidget('OOF3D').resize(705, 440)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(459)
findWidget('OOF3D').resize(705, 443)
findWidget('OOF3D').resize(705, 446)
findWidget('OOF3D').resize(705, 448)
findWidget('OOF3D').resize(705, 449)
findWidget('OOF3D').resize(706, 452)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(460)
findWidget('OOF3D').resize(706, 457)
findWidget('OOF3D').resize(706, 461)
findWidget('OOF3D').resize(706, 464)
findWidget('OOF3D').resize(707, 465)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(461)
findWidget('OOF3D').resize(707, 470)
findWidget('OOF3D').resize(706, 471)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(460)
findWidget('OOF3D').resize(706, 473)
findWidget('OOF3D').resize(706, 475)
findWidget('OOF3D').resize(706, 476)
findWidget('OOF3D').resize(706, 479)
findWidget('OOF3D').resize(707, 483)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(461)
findWidget('OOF3D').resize(707, 487)
findWidget('OOF3D').resize(707, 490)
findWidget('OOF3D').resize(707, 496)
findWidget('OOF3D').resize(707, 499)
findWidget('OOF3D').resize(707, 504)
findWidget('OOF3D').resize(707, 511)
findWidget('OOF3D').resize(707, 512)
findWidget('OOF3D').resize(707, 514)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(286, 94)
assert tests.MeshSubproblemNewDialogSelectEntireMesh0()
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(286, 94)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'Material')
findWidget('Dialog-Create a new subproblem').resize(302, 121)
assert tests.MeshSubproblemNewDialogSelectMaterial0('material')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(302, 121)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'VoxelGroup')
findWidget('Dialog-Create a new subproblem').resize(308, 121)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:VoxelGroup:group'), 'triangle')
assert tests.MeshSubproblemNewDialogSelectGroup0('triangle')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>','subproblem<3>'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(308, 121)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'Union')
findWidget('Dialog-Create a new subproblem').resize(337, 148)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Union:another'), 'subproblem')
assert tests.MeshSubproblemNewDialogSelectUnion0('default', 'subproblem')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
findWidget('OOF3D Messages 1').resize(853, 200)
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>','subproblem<3>','subproblem<4>'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(337, 148)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'Intersection')
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Intersection:one'), 'subproblem<2>')
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Intersection:another'), 'subproblem<3>')
assert tests.MeshSubproblemNewDialogSelectIntersection0('subproblem<2>', 'subproblem<3>')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(943, 200)
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>','subproblem<3>','subproblem<4>','subproblem<5>'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(337, 148)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'Xor')
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Xor:one'), 'subproblem<4>')
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Xor:another'), 'subproblem<4>')
assert tests.MeshSubproblemNewDialogSelectXor0('subproblem<4>', 'subproblem<4>')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>','subproblem<3>','subproblem<4>','subproblem<5>','subproblem<6>'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(337, 148)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'Complement')
findWidget('Dialog-Create a new subproblem').resize(389, 148)
assert tests.MeshSubproblemNewDialogSelectComplement0('default')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>','subproblem<3>','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>'])
assert tests.subproblemsSelectedCheck('subproblem<2>')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename subproblem subproblem<2>
findWidget('Dialog-Rename subproblem subproblem<2>').resize(190, 65)
findWidget('Dialog-Rename subproblem subproblem<2>:name').set_text('material_subproblem')
findWidget('Dialog-Rename subproblem subproblem<2>:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Rename
assert tests.subproblemsCheck(['default','subproblem','material_subproblem','subproblem<3>','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((3,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem','material_subproblem','subproblem<3>','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>'])
assert tests.subproblemsSelectedCheck('subproblem<3>')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Subproblem definition
findWidget('Dialog-Edit Subproblem definition').resize(308, 100)
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:VoxelGroup:group'), 'environment')
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:Chooser'), 'EntireMesh')
assert tests.MeshSubproblemEditDialogSelectEntireMesh0()
findWidget('Dialog-Edit Subproblem definition:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Edit
assert tests.subproblemsCheck(['default','subproblem','material_subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 2.8231080866431e+01)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 3.4000000000000e+01)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 5.7689191335691e+00)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((3,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem','material_subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>'])
assert tests.subproblemsSelectedCheck('subproblem<4>')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy a subproblem
findWidget('Dialog-Copy a subproblem').resize(246, 148)
findWidget('Dialog-Copy a subproblem:name:Auto').clicked()
findWidget('Dialog-Copy a subproblem:name:Text').set_text('subproblem_copy')
findWidget('Dialog-Copy a subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Copy
assert tests.subproblemsCheck(['default','subproblem','material_subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>','subproblem_copy'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 2.8231080866431e+01)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 5.6462161732862e+01)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 5.7000000000000e+01)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 2.8768919133569e+01)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 5.3783826713830e-01)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Info').clicked()
checkpoint OOF.Subproblem.Info
findWidget('OOF3D:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(373, 229)
assert tests.MeshNewDialogCheck0()
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint named analysis chooser set
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
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.New
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh','mesh<2>'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh<2>')
assert tests.subproblemsCheck(['default'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh','mesh<2>'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem','material_subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>','subproblem_copy'])
assert tests.subproblemsSelectedCheck('material_subproblem')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy a subproblem
findWidget('Dialog-Copy a subproblem').resize(246, 148)
setComboBox(findWidget('Dialog-Copy a subproblem:mesh:Mesh'), 'mesh<2>')
findWidget('Dialog-Copy a subproblem:name:Auto').clicked()
findWidget('Dialog-Copy a subproblem:name:Auto').clicked()
findWidget('Dialog-Copy a subproblem:name:Text').set_text('material_subproblem_copy')
findWidget('Dialog-Copy a subproblem:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Copy
assert tests.subproblemsCheck(['default','subproblem','material_subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>','subproblem_copy'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh<2>')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
assert tests.subproblemsCheck(['default','material_subproblem_copy'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem','material_subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>','subproblem_copy'])
assert tests.subproblemsSelectedCheck('material_subproblem')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(416, 87)
findWidget('Questioner:gtk-yes').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Delete
assert tests.subproblemsCheck(['default','subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>','subproblem_copy'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh<2>')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
assert tests.subproblemsCheck(['default','material_subproblem_copy'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>','subproblem_copy'])
assert tests.subproblemsSelectedCheck('subproblem<4>')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((1,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem','subproblem<4>','subproblem<5>','subproblem<6>','subproblem<7>','subproblem<3>','subproblem_copy'])
assert tests.subproblemsSelectedCheck('subproblem')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(354, 87)
findWidget('Questioner:gtk-yes').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Delete
assert tests.subproblemsCheck(['default','subproblem<5>','subproblem<7>','subproblem<3>'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh<2>')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
assert tests.subproblemsCheck(['default','material_subproblem_copy'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
assert tests.subproblemsCheck(['default','subproblem<5>','subproblem<7>','subproblem<3>'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh<2>')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((1,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','material_subproblem_copy'])
assert tests.subproblemsSelectedCheck('material_subproblem_copy')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Subproblem definition
findWidget('Dialog-Edit Subproblem definition').resize(302, 100)
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:Chooser'), 'EntireMesh')
findWidget('Dialog-Edit Subproblem definition:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Edit
assert tests.subproblemsCheck(['default','material_subproblem_copy'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((1,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','material_subproblem_copy'])
assert tests.subproblemsSelectedCheck('material_subproblem_copy')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy a subproblem
findWidget('Dialog-Copy a subproblem').resize(246, 148)
findWidget('Dialog-Copy a subproblem:name:Text').set_text('subproblem_copy')
findWidget('Dialog-Copy a subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Copy
assert tests.subproblemsCheck(['default','material_subproblem_copy','subproblem_copy'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Subproblem definition
findWidget('Dialog-Edit Subproblem definition').resize(244, 73)
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:Chooser'), 'Material')
findWidget('Dialog-Edit Subproblem definition').resize(302, 100)
findWidget('Dialog-Edit Subproblem definition:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Edit
assert tests.subproblemsCheck(['default','subproblem_copy','material_subproblem_copy'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem_copy','material_subproblem_copy'])
assert tests.subproblemsSelectedCheck('material_subproblem_copy')
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(484, 87)
findWidget('Questioner:gtk-yes').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Delete
assert tests.subproblemsCheck(['default','subproblem_copy'])
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('meshpage.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('meshpage.log')
widget_2=findWidget('OOF3D')
handled_1=widget_2.event(event(gtk.gdk.DELETE,window=widget_2.window))
