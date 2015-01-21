# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:46 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# We test the basical ways of creating a microstructure and handling their voxels groups.
# And also saving a Python Log.

import tests

checkpoint toplevel widget mapped OOF3D
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)

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

# create a voxels selection named a
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

# create a voxels selection with a generated name
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

# create another voxels selection with a generated name
findWidget('OOF3D:Microstructure Page:Pane:VoxelGroups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create new voxel group
findWidget('Dialog-Create new voxel group').resize(246, 67)
findWidget('Dialog-Create new voxel group:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.PixelGroup.New

# create a microstructure with loaded files
findWidget('OOF3D:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(401, 215)
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('.')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('..')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../.')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../..')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3D')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DS')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSa')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSan')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSand')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandb')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbo')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5c')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5co')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5col')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5colo')
findWidget('Dialog-Load Image and create Microstructure:filenames:Entire Directory:directory').set_text('../../3DSandbox/5color')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(603, 200)
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
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
checkpoint microstructure page sensitized
checkpoint OOF.Microstructure.Create_From_ImageFile

# check the microstructures state
assert tests.sensitization4()
assert tests.chooserCheck('OOF3D:Microstructure Page:Microstructure', ['test', '5color'])
assert tests.chooserStateCheck('OOF3D:Microstructure Page:Microstructure', '5color')
assert tests.chooserCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', [])
assert tests.chooserListStateCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', [])

# select the microstructure test
setComboBox(findWidget('OOF3D:Microstructure Page:Microstructure'), 'test')
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized

# check the current microstructure voxels selection groups
assert tests.sensitization5()
assert tests.chooserCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', ['a (0 voxels, meshable)', 'pixelgroup (0 voxels, meshable)', 'pixelgroup<2> (0 voxels, meshable)'])
assert tests.chooserListStateCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', [])

# delete the microstructure test
findWidget('OOF3D:Microstructure Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint pixel page updated
checkpoint active area status updated
checkpoint mesh bdy page updated
checkpoint Materials page updated
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint skeleton page sensitized
checkpoint meshable button set
checkpoint OOF.Microstructure.Delete

# check that the microstructures list contain jusr 5color
assert tests.sensitization4()
assert tests.chooserCheck('OOF3D:Microstructure Page:Microstructure', ['5color'])
assert tests.chooserStateCheck('OOF3D:Microstructure Page:Microstructure', '5color')
assert tests.chooserCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', [])
assert tests.chooserListStateCheck('OOF3D:Microstructure Page:Pane:VoxelGroups:GroupListScroll:GroupList', [])

# delete the microstructure 5color too
findWidget('OOF3D:Microstructure Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint mesh bdy page updated
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
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Microstructure.Delete
checkpoint meshable button set

# quit OOF3D and create a saved python log file
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
findWidget('Dialog-Save Log File:filename').set_text('micro2')
findWidget('Dialog-Save Log File:filename').set_text('micro2.')
findWidget('Dialog-Save Log File:filename').set_text('micro2.l')
findWidget('Dialog-Save Log File:filename').set_text('micro2.lo')
findWidget('Dialog-Save Log File:filename').set_text('micro2.log')
findWidget('Dialog-Save Log File').resize(198, 95)
findWidget('Dialog-Save Log File:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('micro2.log')