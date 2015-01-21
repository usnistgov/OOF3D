# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# We are mainly testing here how the meshable button state is changing.
# Specially through different voxels groups.

import tests

checkpoint toplevel widget mapped OOF3D
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D').resize(550, 350)

# create a microstructure named test
findWidget('OOF3D:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(315, 199)
findWidget('Dialog-Create Microstructure:name:Auto').clicked()
findWidget('Dialog-Create Microstructure:name:Text').set_text('t')
findWidget('Dialog-Create Microstructure:name:Text').set_text('te')
findWidget('Dialog-Create Microstructure:name:Text').set_text('tes')
findWidget('Dialog-Create Microstructure:name:Text').set_text('test')
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint mesh bdy page updated
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Microstructure.New

# create a voxels selection group named a
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:name:Auto').clicked()
findWidget('Dialog-Create new voxel group:name:Text').set_text('a')
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New
checkpoint microstructure page sensitized
checkpoint meshable button set
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename voxelgroup a
findWidget('Dialog-Rename voxelgroup a').resize(190, 67)
findWidget('Dialog-Rename voxelgroup a:gtk-cancel').clicked()

# create a voxels selection group named b
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:name:Text').set_text('')
findWidget('Dialog-Create new voxel group:name:Text').set_text('b')
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New

# create a voxels selection group with a generated name
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:name:Auto').clicked()
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New

# create another voxels selection group with a generated name
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll').get_hadjustment().set_value( 2.3000000000000e+01)
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll').get_hadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Meshable').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.Meshable

# check the meshable button
assert tests.meshableButtonState() == 0
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((2,))
checkpoint microstructure page sensitized
checkpoint meshable button set

# check the voxels selection groups state
# check the meshable button
assert tests.treeViewColValues('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList',0) == ['a (0 voxels, meshable)', 'b (0 voxels, meshable)', 'pixelgroup (0 voxels, meshable)', 'pixelgroup<2> (0 voxels)']
assert tests.meshableButtonState() == 1
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((3,))
checkpoint microstructure page sensitized
checkpoint meshable button set

# check the meshable button
assert tests.meshableButtonState() == 0
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((1,))
checkpoint microstructure page sensitized
checkpoint meshable button set

# check the meshable button
assert tests.meshableButtonState() == 1
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Meshable').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.Meshable

# check the meshable button
assert tests.meshableButtonState() == 0
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((3,))
checkpoint microstructure page sensitized
checkpoint meshable button set

# check the meshable button
assert tests.meshableButtonState() == 0
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((1,))
checkpoint microstructure page sensitized
checkpoint meshable button set

# check the meshable button
assert tests.meshableButtonState() == 0
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.Delete
checkpoint microstructure page sensitized
checkpoint meshable button set

# Check that the pixel group list has the right items, and that
# nothing is selected.
assert tests.sensitization1()
assert tests.treeViewColValues('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList',0) == ['a (0 voxels, meshable)', 'pixelgroup (0 voxels, meshable)', 'pixelgroup<2> (0 voxels)']
assert findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().get_selected()[1] is None
assert tests.meshableButtonState() == 0
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((0,))
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Image')
checkpoint page installed Image
findWidget('OOF3D').resize(601, 350)
findWidget('OOF3D:Image Page:Pane').set_position(395)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Voxel Selection')
checkpoint page installed Voxel Selection
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(387)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Invert
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure

# check the voxels selection groups buttons
assert tests.sensitization2()
assert tests.meshableButtonState() == 1
findWidget('OOF3D:Microstructure Page:Pane').set_position(212)
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((1,))
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection

# check the voxels selection groups buttons
assert tests.sensitization3()
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Remove').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.RemoveSelection

# check the voxels selection groups buttons
assert tests.sensitization2()
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(359, 91)
findWidget('Questioner:gtk-delete').clicked()
