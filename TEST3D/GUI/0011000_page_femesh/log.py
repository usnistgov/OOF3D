# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.9 $
# $Author: langer $
# $Date: 2014/05/08 14:40:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Basic Testing of the FE Mesh Page: Testing Mesh Handling Buttons and 
#Subproblems Handling Buttons

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
assert tests.FEMeshPageInfoCheck()
assert tests.FEMeshPageCheck0()
assert tests.FEMeshPageSubproblemsCheck0()
assert tests.FEMeshPageOperationsCheck0()
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 67)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/triangle.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint microstructure page sensitized
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
checkpoint skeleton selection page updated
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
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint microstructure page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
findWidget('OOF3D').resize(601, 357)
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
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
findWidget('OOF3D:FE Mesh Page:Pane').set_position(355)
findWidget('OOF3D:FE Mesh Page:New').clicked()
assert tests.MeshNewDialogCheck0()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(373, 237)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
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
#assert tests.FEMeshPageInfoCheck('Unsolved',161,318,318)
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh')
assert tests.subproblemsCheck(['default'])
findWidget('OOF3D').resize(602, 357)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(356)
findWidget('OOF3D').resize(603, 358)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(428)
findWidget('OOF3D').resize(674, 402)
findWidget('OOF3D:FE Mesh Page:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename mesh mesh
findWidget('Dialog-Rename mesh mesh').resize(190, 67)
findWidget('Dialog-Rename mesh mesh:name').set_text('mesh_renamed')
findWidget('Dialog-Rename mesh mesh:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Rename
#assert tests.FEMeshPageInfoCheck('Unsolved',161,318,318)
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh_renamed'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh_renamed')
findWidget('OOF3D:FE Mesh Page:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy a mesh
findWidget('Dialog-Copy a mesh').resize(304, 127)
findWidget('Dialog-Copy a mesh:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
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
checkpoint OOF.Mesh.Copy
#assert tests.FEMeshPageInfoCheck('Unsolved',161,318,318)
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh_renamed','mesh'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh')
findWidget('OOF3D:FE Mesh Page:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy a mesh
findWidget('Dialog-Copy a mesh').resize(304, 127)
findWidget('Dialog-Copy a mesh:name:Auto').clicked()
findWidget('Dialog-Copy a mesh:name:Text').set_text('mesh_copied')
findWidget('Dialog-Copy a mesh:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
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
checkpoint OOF.Mesh.Copy
#assert tests.FEMeshPageInfoCheck('Unsolved',161,318,318)
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh_renamed','mesh','mesh_copied'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh_copied')
setComboBox(findWidget('OOF3D:FE Mesh Page:Mesh'), 'mesh_renamed')
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
#assert tests.FEMeshPageInfoCheck('Unsolved',161,318,318)
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh_renamed','mesh','mesh_copied'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh_renamed')
findWidget('OOF3D:FE Mesh Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(345, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Delete
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh','mesh_copied'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh')
findWidget('OOF3D:FE Mesh Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Mesh "triangle;skeleton;mesh"
findWidget('Dialog-Save Mesh "triangle;skeleton;mesh"').resize(190, 123)
findWidget('Dialog-Save Mesh "triangle;skeleton;mesh":filename').set_text('mesh_save.mesh')
findWidget('Dialog-Save Mesh "triangle;skeleton;mesh":gtk-ok').clicked()
checkpoint OOF.File.Save.Mesh
assert tests.filediff('mesh_save.mesh')
widget_1=findWidget('OOF3D Graphics 1')
handled_1=widget_1.event(event(gtk.gdk.DELETE,window=widget_1.window))
postpone if not handled_1: widget_1.destroy()
checkpoint OOF.Graphics_1.File.Close

findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('meshpage.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('meshpage.log')
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))