# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.8 $
# $Author: fyc $
# $Date: 2014/09/19 22:52:28 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#This GUI test case is tight to the skeleton page global test.
#It aims to check if the skeleton Surface Smooth Method is reliabily working according
#to the sensitization of the OK button in case of an Heterogenity, Selection , Group situations.
#This case has no targets. Base on our comments on the 0010501 in this test we should just check that the OK Button is always sensitized in all cases.

findWidget('OOF3D').resize(550, 350)
#Loading the script log file of the entry general skeleton page test case 0010500.
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
checkpoint Solver page sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
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
#Going to the Skeleton Page
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
findWidget('OOF3D').resize(601, 357)
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
checkpoint skeleton page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
#Selecting the Microstrure '0color'
setComboBox(findWidget('OOF3D:Skeleton Page:Microstructure'), '0color')
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
findWidget('OOF3D Graphics 1').resize(1000, 802)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 707))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 707))
findWidget('OOF3D Graphics 1').resize(1000, 806)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 711))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 711))
findWidget('OOF3D Graphics 1').resize(1000, 832)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 737))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 737))
findWidget('OOF3D Graphics 1').resize(1000, 857)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 762))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 762))
findWidget('OOF3D Graphics 1').resize(1000, 873)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 778))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 778))
findWidget('OOF3D Graphics 1').resize(1000, 883)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 788))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 788))
findWidget('OOF3D Graphics 1').resize(1000, 894)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 799))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 799))
findWidget('OOF3D Graphics 1').resize(1000, 897)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 802))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 802))
findWidget('OOF3D Graphics 1').resize(1000, 901)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 806))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 806))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 805))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 805))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 801))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 801))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 793))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 793))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 784))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 784))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 776))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 776))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 770))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 770))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 763))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 763))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 756))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 756))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 750))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 750))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 745))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 745))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 739))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 739))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 736))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 736))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 724))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 724))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 715))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 715))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 709))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 709))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 704))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 704))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 697))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 697))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 691))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 691))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 687))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 687))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 683))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 683))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 682))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 682))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 681))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 681))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 679))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 679))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.7979576943884e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.5959153887769e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 8.3938730831653e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.1191830777554e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.3989788471942e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.6787746166331e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.9585703860719e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2383661555107e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5181619249496e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.7979576943884e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.0777534638273e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.3200000000000e+02)
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
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '24')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((24,))
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Show
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 679))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 679))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.8600000000000e+02,y= 2.0100000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8600000000000e+02,y= 2.0200000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8700000000000e+02,y= 2.0300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8800000000000e+02,y= 2.0400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.8900000000000e+02,y= 2.0600000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9200000000000e+02,y= 2.0800000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9700000000000e+02,y= 2.1300000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9900000000000e+02,y= 2.1400000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0000000000000e+02,y= 2.1500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0300000000000e+02,y= 2.1500000000000e+02,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 645)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.0500000000000e+02,y= 2.1700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 679))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 679))
findWidget('OOF3D Graphics 1:Pane0:Pane2:fill').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 679))
findWidget('OOF3D').resize(601, 357)
#Selecting the Surface Smooth method
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Chooser'), 'Surface Smooth')
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Surface Smooth')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Average Energy')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D').resize(601, 401)
findWidget('OOF3D:Skeleton Page:Pane').set_position(274)
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Conditional Iteration')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Conditional Iteration')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
findWidget('OOF3D').resize(612, 475)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Energy Reduction Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Energy Reduction Rate')
findWidget('OOF3D:Skeleton Page:Pane').set_position(123)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Both')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Both')
findWidget('OOF3D').resize(612, 497)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Either')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Either')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Acceptance Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Fixed Iterations')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D:Skeleton Page:Pane').set_position(285)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Conditional Iteration')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Conditional Iteration')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
findWidget('OOF3D').resize(612, 475)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Energy Reduction Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Energy Reduction Rate')
findWidget('OOF3D:Skeleton Page:Pane').set_position(123)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Both')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Both')
findWidget('OOF3D').resize(612, 497)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Either')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Either')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Acceptance Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Fixed Iterations')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D:Skeleton Page:Pane').set_position(285)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(230)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Conditional Iteration')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Conditional Iteration')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
findWidget('OOF3D').resize(612, 475)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Energy Reduction Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Energy Reduction Rate')
findWidget('OOF3D:Skeleton Page:Pane').set_position(123)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Both')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Both')
findWidget('OOF3D').resize(612, 497)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Either')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Either')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Acceptance Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Fixed Iterations')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D:Skeleton Page:Pane').set_position(230)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Conditional Iteration')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Conditional Iteration')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
findWidget('OOF3D').resize(612, 475)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Energy Reduction Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Energy Reduction Rate')
findWidget('OOF3D:Skeleton Page:Pane').set_position(123)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Both')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Both')
findWidget('OOF3D').resize(612, 497)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Either')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Either')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Acceptance Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Fixed Iterations')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D:Skeleton Page:Pane').set_position(230)
#Selecting the microstructure '5color'
setComboBox(findWidget('OOF3D:Skeleton Page:Microstructure'), '5color')
checkpoint skeleton page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(285)
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '28')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((28,))
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Hide
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '24')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((24,))
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
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
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '23')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((23,))
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Show
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Conditional Iteration')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Conditional Iteration')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
findWidget('OOF3D').resize(612, 475)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Energy Reduction Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Energy Reduction Rate')
findWidget('OOF3D:Skeleton Page:Pane').set_position(123)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Both')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Both')
findWidget('OOF3D').resize(612, 497)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Either')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Either')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Acceptance Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Fixed Iterations')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D:Skeleton Page:Pane').set_position(285)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Conditional Iteration')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Conditional Iteration')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
findWidget('OOF3D').resize(612, 475)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Energy Reduction Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Energy Reduction Rate')
findWidget('OOF3D:Skeleton Page:Pane').set_position(123)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Both')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Both')
findWidget('OOF3D').resize(612, 497)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Either')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Either')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Acceptance Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Fixed Iterations')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D:Skeleton Page:Pane').set_position(285)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(230)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Conditional Iteration')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Conditional Iteration')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
findWidget('OOF3D').resize(612, 475)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Energy Reduction Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Energy Reduction Rate')
findWidget('OOF3D:Skeleton Page:Pane').set_position(123)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Both')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Both')
findWidget('OOF3D').resize(612, 497)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Either')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Either')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Acceptance Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Fixed Iterations')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D:Skeleton Page:Pane').set_position(230)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Conditional Iteration')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Conditional Iteration')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
findWidget('OOF3D').resize(612, 475)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Energy Reduction Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Energy Reduction Rate')
findWidget('OOF3D:Skeleton Page:Pane').set_position(123)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Both')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Both')
findWidget('OOF3D').resize(612, 497)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Either')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Either')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Conditional Iteration:condition:Chooser'), 'Acceptance Rate')
assert tests.skeletonMethodIterationConditionListCheck('Surface Smooth','Conditional Iteration','Acceptance Rate','Energy Reduction Rate','Both','Either',)
assert tests.currentSkeletonMethodIterationConditionCheck('Surface Smooth','Conditional Iteration','Acceptance Rate')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:iteration:Chooser'), 'Fixed Iterations')
assert tests.skeletonMethodIterationListCheck('Surface Smooth','Fixed Iterations','Conditional Iteration')
assert tests.currentSkeletonMethodIterationCheck('Surface Smooth','Fixed Iterations')
findWidget('OOF3D:Skeleton Page:Pane').set_position(230)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Surface Smooth:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Surface Smooth','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Surface Smooth','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(285)

findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('skelpagesurfsmooth.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('skelpagesurfsmooth.log')
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))