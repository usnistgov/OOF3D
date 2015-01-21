# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:41 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# We will test some basic actions on a microstructure and some created voxels groups.

import tests

checkpoint toplevel widget mapped OOF3D
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D').resize(619, 350)
findWidget('OOF3D:Microstructure Page:Pane').set_position(254)
assert tests.sensitization0()

# create a microstructure named micro1
findWidget('OOF3D:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(315, 199)
findWidget('Dialog-Create Microstructure:name:Auto').clicked()
findWidget('Dialog-Create Microstructure:name:Text').set_text('m')
findWidget('Dialog-Create Microstructure:name:Text').set_text('mi')
findWidget('Dialog-Create Microstructure:name:Text').set_text('mic')
findWidget('Dialog-Create Microstructure:name:Text').set_text('micr')
findWidget('Dialog-Create Microstructure:name:Text').set_text('micro')
findWidget('Dialog-Create Microstructure:name:Text').set_text('micro1')
findWidget('Dialog-Create Microstructure:width').set_text('')
findWidget('Dialog-Create Microstructure:width').set_text('5')
findWidget('Dialog-Create Microstructure:height').set_text('')
findWidget('Dialog-Create Microstructure:height').set_text('5')
findWidget('Dialog-Create Microstructure:width_in_pixels').set_text('')
findWidget('Dialog-Create Microstructure:width_in_pixels').set_text('1')
findWidget('Dialog-Create Microstructure:width_in_pixels').set_text('10')
findWidget('Dialog-Create Microstructure:width_in_pixels').set_text('100')
findWidget('Dialog-Create Microstructure:height_in_pixels').set_text('')
findWidget('Dialog-Create Microstructure:height_in_pixels').set_text('1')
findWidget('Dialog-Create Microstructure:height_in_pixels').set_text('10')
findWidget('Dialog-Create Microstructure:height_in_pixels').set_text('100')
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(179)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint mesh bdy page updated
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint meshable button set
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
assert tests.sensitization1()

# create a voxels selection group named abcde
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:name:Auto').clicked()
findWidget('Dialog-Create new voxel group:name:Text').set_text('a')
findWidget('Dialog-Create new voxel group:name:Text').set_text('ab')
findWidget('Dialog-Create new voxel group:name:Text').set_text('abc')
findWidget('Dialog-Create new voxel group:name:Text').set_text('abcd')
findWidget('Dialog-Create new voxel group:name:Text').set_text('abcde')
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(254)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New
checkpoint microstructure page sensitized
checkpoint meshable button set

# check the voxels selection groups and buttons state
assert tests.sensitization2()
assert tests.chooserCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['abcde (0 voxels, meshable)'])
assert tests.chooserListStateCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['abcde (0 voxels, meshable)'])
assert tests.meshableButtonState() == 1

# create another voxels selection group named fghij
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:name:Text').set_text('')
findWidget('Dialog-Create new voxel group:name:Text').set_text('f')
findWidget('Dialog-Create new voxel group:name:Text').set_text('fg')
findWidget('Dialog-Create new voxel group:name:Text').set_text('fgh')
findWidget('Dialog-Create new voxel group:name:Text').set_text('fghi')
findWidget('Dialog-Create new voxel group:name:Text').set_text('fghij')
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New

# check the voxels selection groups and buttons state
assert tests.sensitization2()
assert tests.chooserCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['abcde (0 voxels, meshable)', 'fghij (0 voxels, meshable)'])
assert tests.chooserListStateCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['fghij (0 voxels, meshable)'])

# select the voxels selection group abcde
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList').get_selection().select_path((0,))
assert tests.chooserListStateCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['abcde (0 voxels, meshable)'])
checkpoint microstructure page sensitized
checkpoint meshable button set

# rename the voxels selection group abcde to klmno
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename voxelgroup abcde
findWidget('Dialog-Rename voxelgroup abcde').resize(190, 67)
findWidget('Dialog-Rename voxelgroup abcde:new_name').set_text('')
findWidget('Dialog-Rename voxelgroup abcde:new_name').set_text('k')
findWidget('Dialog-Rename voxelgroup abcde:new_name').set_text('kl')
findWidget('Dialog-Rename voxelgroup abcde:new_name').set_text('klm')
findWidget('Dialog-Rename voxelgroup abcde:new_name').set_text('klmn')
findWidget('Dialog-Rename voxelgroup abcde:new_name').set_text('klmno')
findWidget('Dialog-Rename voxelgroup abcde:gtk-ok').clicked()
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.Rename
checkpoint microstructure page sensitized
checkpoint meshable button set

# check the voxels selection groups and buttons state
assert tests.sensitization2()
assert tests.chooserCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['klmno (0 voxels, meshable)', 'fghij (0 voxels, meshable)'])
assert tests.chooserListStateCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['klmno (0 voxels, meshable)'])
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Meshable').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.Meshable

# check the voxels selection groups and buttons state
assert tests.chooserListStateCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['klmno (0 voxels)'])
assert tests.meshableButtonState() == 0

# delet ethe voxels selection group klmno
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

# create some voxels selection and add it to fghij
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Voxel Selection')
checkpoint page installed Voxel Selection
findWidget('OOF3D:Voxel Selection Page:Pane').set_position(405)
findWidget('OOF3D:Voxel Selection Page:Pane:SelectionModification:OK').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint OOF.PixelSelection.Invert
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Add').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.AddSelection

# clear the selection in fghij
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:Clear').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.Clear

# save the microstructure page
findWidget('OOF3D:Microstructure Page:Save').clicked()
checkpoint toplevel widget mapped Dialog-Save Microstructure "micro1"
findWidget('Dialog-Save Microstructure "micro1"').resize(190, 123)
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('m')
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('mi')
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('mic')
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('micr')
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('micro')
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('micro.')
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('micro.d')
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('micro.da')
findWidget('Dialog-Save Microstructure "micro1":filename').set_text('micro.dat')
findWidget('Dialog-Save Microstructure "micro1"').resize(198, 123)
findWidget('Dialog-Save Microstructure "micro1":gtk-ok').clicked()
checkpoint OOF.File.Save.Microstructure

# quit OOF3D by creating a Python Log File
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(359, 91)
findWidget('Questioner:gtk-save').clicked()
checkpoint toplevel widget mapped Dialog-Save Log File
findWidget('Dialog-Save Log File').resize(190, 95)
findWidget('Dialog-Save Log File:filename').set_text('m')
findWidget('Dialog-Save Log File:filename').set_text('mi')
findWidget('Dialog-Save Log File:filename').set_text('mic')
findWidget('Dialog-Save Log File:filename').set_text('micr')
findWidget('Dialog-Save Log File:filename').set_text('micro')
findWidget('Dialog-Save Log File:filename').set_text('micro.')
findWidget('Dialog-Save Log File:filename').set_text('micro.l')
findWidget('Dialog-Save Log File:filename').set_text('micro.lo')
findWidget('Dialog-Save Log File:filename').set_text('micro.log')
findWidget('Dialog-Save Log File').resize(198, 95)
findWidget('Dialog-Save Log File:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log