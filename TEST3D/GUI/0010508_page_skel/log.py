# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.7 $
# $Author: langer $
# $Date: 2014/05/08 14:40:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#This GUI test case is tight to the skeleton page global test.
#It aims to check if the skeleton Snap Nodes Elements Mehtod is reliabily working according
#to the sensitization of the OK button in case of an Heterogenity, Selection , Group situations.
#In this test case onlye the All Elements targets is to be always concidered as an OK sensitized situation.
#All the rest requires some checks on either the Skeleton Status either the Skeleton Selection or Groups

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
checkpoint skeleton page sensitized
findWidget('OOF3D').resize(601, 357)
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Chooser'), 'Snap Refine')
findWidget('OOF3D').resize(601, 431)
findWidget('OOF3D:Skeleton Page:Pane').set_position(274)
checkpoint skeleton page sensitized
assert tests.skeletonPageModificationSensitivityCheck0()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogenous Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Script').activate()
checkpoint toplevel widget mapped Dialog-Script
findWidget('Dialog-Script').resize(190, 67)
findWidget('Dialog-Script:filename').set_text('TEST_DATA/skelpagetestbase.log')
findWidget('Dialog-Script:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Solver page sensitized
checkpoint OOF.Microstructure.New
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint microstructure page sensitized
checkpoint OOF.Microstructure.Create_From_ImageFile
checkpoint Move Node toolbox info updated
checkpoint toplevel widget mapped OOF3D Graphics 1
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Messages 1').resize(593, 200)
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Simple
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Rename
findWidget('OOF3D Activity Viewer').resize(400, 300)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Copy
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Delete
checkpoint OOF.File.Save.Skeleton
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Skeleton.New
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint OOF.Graphics_1.Layer.Select
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Simple
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Rename
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Copy
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Delete
checkpoint OOF.File.Save.Skeleton
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.New
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Rename
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Rename
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.New
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Rename
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Simple
checkpoint Field page sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Rename
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Simple
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Simple
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Simple
checkpoint Field page sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint OOF.Skeleton.Rename
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Simple
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Field page sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Simple
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint OOF.Graphics_1.Layer.Select
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint OOF.Graphics_1.Layer.Select
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint OOF.File.Load.Script
widget_0=findWidget('OOF3D Activity Viewer')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
checkpoint OOF.ActivityViewer.File.Close
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogenous Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
#Check the Undo button here and all the rest
findWidget('OOF3D:Skeleton Page:Pane:Modification:OK').clicked()
checkpoint pinnodes page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint pinnodes page sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint pinnodes page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint pinnodes page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Modify
assert tests.skeletonPageModificationSensitivityCheck6()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint pinnodes page sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint pinnodes page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo
assert tests.skeletonPageModificationSensitivityCheck7()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Redo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint pinnodes page sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint pinnodes page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Redo
assert tests.skeletonPageModificationSensitivityCheck6()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint pinnodes page sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint pinnodes page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo
assert tests.skeletonPageModificationSensitivityCheck7()
findWidget('OOF3D Graphics 1').resize(1000, 802)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 707))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 707))
findWidget('OOF3D Graphics 1').resize(1000, 804)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 709))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 709))
findWidget('OOF3D Graphics 1').resize(1000, 811)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 716))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 716))
findWidget('OOF3D Graphics 1').resize(1000, 830)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 735))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 735))
findWidget('OOF3D Graphics 1').resize(1000, 845)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 750))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 750))
findWidget('OOF3D Graphics 1').resize(1000, 864)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 769))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 769))
findWidget('OOF3D Graphics 1').resize(1000, 881)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 786))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 786))
findWidget('OOF3D Graphics 1').resize(1000, 900)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 805))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 805))
findWidget('OOF3D Graphics 1').resize(1000, 904)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 809))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 809))
findWidget('OOF3D Graphics 1').resize(1000, 919)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 824))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 824))
findWidget('OOF3D Graphics 1').resize(1000, 928)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 833))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 833))
findWidget('OOF3D Graphics 1').resize(1000, 933)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 838))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 838))
findWidget('OOF3D Graphics 1').resize(1000, 935)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 840))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 840))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 839))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 839))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 834))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 834))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 819))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 819))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 804))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 804))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 794))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 794))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 784))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 784))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 774))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 774))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 762))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 762))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 751))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 751))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 740))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 740))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 732))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 732))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 724))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 724))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 712))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 712))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 704))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 704))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 694))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 694))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 689))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 689))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 687))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 687))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 685))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 685))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 683))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 683))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 682))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 682))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 681))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 681))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 676))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 676))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 674))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 674))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 673))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 673))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 671))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 671))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 670))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 670))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 668))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
findWidget('OOF3D Graphics 1:Pane0:Pane2:fill').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Skeleton Page:Microstructure'), '0color')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.3396801300040e+01)
checkpoint skeleton page info updated
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.6793602600080e+01)
checkpoint skeleton page info updated
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.0019040390012e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.3358720520016e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.6698400650020e+02)
checkpoint skeleton page sensitized
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0038080780024e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.3377760910028e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.6717441040032e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.8700000000000e+02)
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '29')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((29,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Hide
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '28')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((28,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Show
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((24,))
checkpoint OOF.Graphics_1.Layer.Select
tree=findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(1)
tree.row_activated((24,), column)
checkpoint toplevel widget mapped Dialog-Edit Graphics Layer
findWidget('Dialog-Edit Graphics Layer').resize(354, 305)
widget_1=findWidget('Dialog-Edit Graphics Layer')
handled_1=widget_1.event(event(gtk.gdk.DELETE,window=widget_1.window))
postpone if not handled_1: widget_1.destroy()
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '24')
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Show
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogenous Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
findWidget('OOF3D:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF3D Messages 1').resize(593, 200)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Modify
assert tests.skeletonPageModificationSensitivityCheck2()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
assert tests.skeletonPageModificationSensitivityCheck5()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Next').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(292)
findWidget('OOF3D:Skeleton Page:Pane:Modification:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Skeleton.Undo
assert tests.skeletonPageModificationSensitivityCheck3()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
assert tests.skeletonPageModificationSensitivityCheck4()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Next').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(292)
findWidget('OOF3D:Skeleton Page:Pane:Modification:Redo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Skeleton.Redo
findWidget('OOF3D:Skeleton Page:Pane:Modification:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Skeleton.Undo
findWidget('OOF3D:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
findWidget('OOF3D:Skeleton Page:Pane:Modification:Next').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(292)
findWidget('OOF3D').resize(601, 407)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Selected Elements')
assert tests.skeletonPageModificationSensitivityCheck3()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Selected Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF3D Messages 1').resize(593, 200)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Modify
assert tests.skeletonPageModificationSensitivityCheck2()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
assert tests.skeletonPageModificationSensitivityCheck8()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Skeleton.Undo
assert tests.skeletonPageModificationSensitivityCheck9()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Redo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Skeleton.Redo
findWidget('OOF3D:Skeleton Page:Pane:Modification:OK').clicked()
findWidget('OOF3D Messages 1').resize(593, 200)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Modify
findWidget('OOF3D:Skeleton Page:Pane:Modification:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Skeleton.Undo
assert tests.skeletonPageModificationSensitivityCheck11()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
assert tests.skeletonPageModificationSensitivityCheck12()
findWidget('OOF3D:Skeleton Page:Pane:Modification:Next').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(292)
findWidget('OOF3D:Skeleton Page:Pane:Modification:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Skeleton.Undo
findWidget('OOF3D:Skeleton Page:Pane:Modification:Prev').clicked()
findWidget('OOF3D:Skeleton Page:Pane').set_position(292)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 668))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Skeleton Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 668))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.6000000000000e+02,y= 1.5900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.6000000000000e+02,y= 1.5900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Selected Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D').resize(601, 407)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Elements In Group')
checkpoint skeleton page sensitized
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Elements In Group')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
findWidget('OOF3D').resize(601, 413)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane').set_position(278)
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Microstructure'), '0color')
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.6400000000000e+02,y= 1.5100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.6400000000000e+02,y= 1.5100000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5900000000000e+02,y= 1.7500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.5900000000000e+02,y= 1.7500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
findWidget('Dialog-Create a new Element group').resize(246, 67)
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton page sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
findWidget('OOF3D').resize(601, 413)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Undo').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Undo
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Add_to_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
checkpoint skeleton page sensitized
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Elements In Group')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'All Elements')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','All Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','All Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Heterogeneous Segments')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogeneous Segments')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D:Skeleton Page:Pane').set_position(211)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
findWidget('OOF3D').resize(601, 437)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Heterogeneous Segments:choose_from:Chooser'), 'Selected Elements')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'Selected Elements')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.4800000000000e+02,y= 1.7300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.4800000000000e+02,y= 1.7300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Heterogeneous Segments:choose_from:Chooser'), 'Selected Segments')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'Selected Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Segment').clicked()
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.3200000000000e+02,y= 1.3800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.3200000000000e+02,y= 1.3800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.0800000000000e+02,y= 1.5500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.0800000000000e+02,y= 1.5500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1000000000000e+02,y= 1.5700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.1000000000000e+02,y= 1.5700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5600000000000e+02,y= 1.8400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5600000000000e+02,y= 1.8400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.6800000000000e+02,y= 1.7100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.6800000000000e+02,y= 1.7100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.6600000000000e+02,y= 1.7300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.6600000000000e+02,y= 1.7300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5300000000000e+02,y= 1.8900000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5300000000000e+02,y= 1.8900000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.4500000000000e+02,y= 1.9300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.4500000000000e+02,y= 1.9300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.4500000000000e+02,y= 1.9600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.4500000000000e+02,y= 1.9600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1800000000000e+02,y= 1.4000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.1800000000000e+02,y= 1.4100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.1900000000000e+02,y= 1.4100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.2200000000000e+02,y= 1.4100000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.2200000000000e+02,y= 1.4200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.2800000000000e+02,y= 1.4500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.2900000000000e+02,y= 1.4500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3000000000000e+02,y= 1.4600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3100000000000e+02,y= 1.4800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3200000000000e+02,y= 1.4800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.3200000000000e+02,y= 1.4800000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
checkpoint OOF.Graphics_1.Settings.Camera.View
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3300000000000e+02,y= 2.3600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3300000000000e+02,y= 2.3700000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3300000000000e+02,y= 2.3800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3200000000000e+02,y= 2.3900000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3200000000000e+02,y= 2.4300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3200000000000e+02,y= 2.4400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3100000000000e+02,y= 2.4600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3100000000000e+02,y= 2.4600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
findWidget('OOF3D Graphics 1:Pane0:Pane2:select').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 668))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9200000000000e+02,y= 2.5100000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.9200000000000e+02,y= 2.5100000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Heterogeneous Segments:choose_from:Chooser'), 'All Segments')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Selected Segments')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Selected Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D:Skeleton Page:Pane').set_position(292)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Segments in Group')
checkpoint skeleton page sensitized
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Segments in Group')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Redo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Redo
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Segment').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonPageModificationSensitivityCheck9()
checkpoint skeleton page sensitized
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
checkpoint skeleton page sensitized
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Selected Faces')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Selected Faces')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Face').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8100000000000e+02,y= 2.1900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8100000000000e+02,y= 2.1900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8900000000000e+02,y= 2.2700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8900000000000e+02,y= 2.2700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8300000000000e+02,y= 2.4800000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8300000000000e+02,y= 2.4800000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1000000000000e+02,y= 2.6000000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 634)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1000000000000e+02,y= 2.6000000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Faces in Group')
checkpoint skeleton page sensitized
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Faces in Group')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonPageModificationSensitivityCheck9b()
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Face').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Face group
findWidget('Dialog-Create a new Face group').resize(246, 67)
findWidget('Dialog-Create a new Face group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.New_Group
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Undo').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Undo
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.Add_to_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Heterogenous Elements')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogenous Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Microstructure'), '5color')
checkpoint skeleton page info updated
assert tests.skeletonPageModificationSensitivityCheck9()
checkpoint skeleton page info updated
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogenous Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '24')
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '28')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((28,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Hide
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '29')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((29,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Show
findWidget('OOF3D').resize(601, 437)
findWidget('OOF3D Graphics 1').resize(1000, 936)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 841))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 841))
findWidget('OOF3D Graphics 1').resize(1000, 937)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 842))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 842))
findWidget('OOF3D Graphics 1').resize(1000, 943)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 848))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 848))
findWidget('OOF3D Graphics 1').resize(1000, 960)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 865))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 865))
findWidget('OOF3D Graphics 1').resize(1000, 965)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 870))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 870))
findWidget('OOF3D Graphics 1').resize(1000, 966)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 871))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 871))
findWidget('OOF3D Graphics 1').resize(1000, 967)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 872))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 872))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 871))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 871))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 854))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 854))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 841))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 841))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 829))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 829))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 808))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 808))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 770))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 770))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 761))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 761))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 758))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 758))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 749))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 749))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 738))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 738))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 736))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 736))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 736))
findWidget('OOF3D Graphics 1:Pane0:Pane2:fill').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 736))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.1610268787932e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.2300000000000e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9389731212068e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.6479462424136e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.3569193636204e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0658924848271e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.7748656060339e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0658924848271e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.3569193636204e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.6479462424136e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9389731212068e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.2300000000000e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9389731212068e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.6479462424136e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.3569193636204e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0658924848271e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.7748656060339e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.4838387272407e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.1928118484475e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 9.0178496965428e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.1075809086107e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.1973121206785e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.8704333274637e+00)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9102687879321e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.8205375758643e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 8.7308063637964e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.1641075151729e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.4551343939661e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.7461612727593e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0371881515525e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.3282150303457e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.6192419091389e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9102687879321e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.2012956667254e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((23,))
checkpoint OOF.Graphics_1.Layer.Select
tree=findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(1)
tree.row_activated((23,), column)
checkpoint toplevel widget mapped Dialog-Edit Graphics Layer
findWidget('Dialog-Edit Graphics Layer').resize(354, 305)
widget_0=findWidget('Dialog-Edit Graphics Layer')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '23')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.2000000000000e+02)
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Show
findWidget('OOF3D').resize(601, 437)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Selected Elements')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Selected Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D:Skeleton Page:Pane').set_position(292)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Element').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7900000000000e+02,y= 2.6900000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7900000000000e+02,y= 2.6900000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.8300000000000e+02,y= 3.1300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.8300000000000e+02,y= 3.1300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Elements In Group')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
checkpoint skeleton page sensitized
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Elements In Group')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Element').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
setComboBox(findWidget('OOF3D:Skeleton Selection Page:Microstructure'), '5color')
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
findWidget('Dialog-Create a new Element group').resize(246, 67)
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7400000000000e+02,y= 2.5300000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7400000000000e+02,y= 2.5300000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9200000000000e+02,y= 2.9500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9200000000000e+02,y= 2.9500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Add_to_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'All Elements')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','All Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Volume')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Volume')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Volume:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Volume','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Volume','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
#The following is a Hard_OK situation also.
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Heterogeneous Segments')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogeneous Segments')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D:Skeleton Page:Pane').set_position(211)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Heterogeneous Segments:choose_from:Chooser'), 'Selected Elements')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'Selected Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8500000000000e+02,y= 2.4000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8500000000000e+02,y= 2.4000000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.7900000000000e+02,y= 2.8200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.7900000000000e+02,y= 2.8200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Heterogeneous Segments:choose_from:Chooser'), 'Selected Segments')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'Selected Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Segment').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8200000000000e+02,y= 2.3700000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8200000000000e+02,y= 2.3700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8500000000000e+02,y= 2.9200000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.8500000000000e+02,y= 2.9200000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.4400000000000e+02,y= 2.9500000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.4400000000000e+02,y= 2.9500000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Heterogeneous Segments:choose_from:Chooser'), 'Selected Segments')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'Selected Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Heterogeneous Segments:choose_from:Chooser'), 'All Segments')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogeneous Segments')
assert tests.skeletonMethodTargetsListChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments','Selected Elements','Selected Segments')
assert tests.currentSkeletonMethodTargetsChooseFromCheck('Snap Refine', 'Heterogeneous Segments', 'All Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Selected Segments')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Selected Segments')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D:Skeleton Page:Pane').set_position(292)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Redo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Redo
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Segments in Group')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Segments in Group')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Segment').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Segment group
findWidget('Dialog-Create a new Segment group').resize(246, 67)
findWidget('Dialog-Create a new Segment group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.New_Group
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Undo').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Undo
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.SegmentGroup.Add_to_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Length')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Length')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Length:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Length','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Length','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Length')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
#The following is a Hard_OK situation also.
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Selected Faces')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Selected Faces')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Segment:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Select:Face').clicked()
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.7800000000000e+02,y= 2.6600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.7800000000000e+02,y= 2.6600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.9500000000000e+02,y= 2.9600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 702)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.9500000000000e+02,y= 2.9600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Single_Face
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
#The following is a Hard_OK situation too.
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Faces in Group')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Clear').clicked()
checkpoint skeleton page sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D:Skeleton Selection Page:Mode:Face').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Face group
findWidget('Dialog-Create a new Face group').resize(246, 67)
findWidget('Dialog-Create a new Face group:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.New_Group
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
checkpoint skeleton page sensitized
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton Selection')
checkpoint page installed Skeleton Selection
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Undo').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Undo
findWidget('OOF3D:Skeleton Selection Page:Pane:Groups:Add').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint OOF.FaceGroup.Add_to_Group
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Minimum Area')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
checkpoint skeleton page sensitized
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Minimum Area')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Physical')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Physical')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Fractional')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Fractional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Minimum Area:units'), 'Voxel')
assert tests.skeletonMethodCriterionUnitListCheck('Snap Refine','Minimum Area','Voxel','Physical','Fractional')
assert tests.currentSkeletonMethodCriterionUnitCheck('Snap Refine','Minimum Area','Voxel')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Area')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Refine:targets:Chooser'), 'Heterogenous Elements')
assert tests.skeletonPageModificationSensitivityCheck9()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Refine')
assert tests.skeletonMethodTargetsListCheck('Snap Refine','Heterogenous Elements','Selected Elements','Elements In Group','All Elements','Heterogeneous Segments','Selected Segments','Segments in Group','Selected Faces','Faces in Group',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Refine','Heterogenous Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Refine','Unconditional','Minimum Volume')
assert tests.currentSkeletonMethodCriterionCheck('Snap Refine','Unconditional')
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Face:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Face.Clear

findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('skelpagesnaprefine.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('skelpagesnaprefine.log')
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))