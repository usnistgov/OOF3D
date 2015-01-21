# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.8 $
# $Author: fyc $
# $Date: 2014/09/19 22:52:29 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#This GUI test case is tight to the skeleton page global test.
#It aims to check if the skeleton Rationalize Method is reliabily working according
#to the sensitization of the OK button in case of an Heterogenity, Selection , Group situations.
#In this test case,we need to check the * Elements targets.

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
findWidget('OOF3D Graphics 1').resize(1000, 801)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 706))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 706))
findWidget('OOF3D Graphics 1').resize(1000, 808)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 713))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 713))
findWidget('OOF3D Graphics 1').resize(1000, 829)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 734))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 734))
findWidget('OOF3D Graphics 1').resize(1000, 849)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 754))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 754))
findWidget('OOF3D Graphics 1').resize(1000, 878)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 783))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 783))
findWidget('OOF3D Graphics 1').resize(1000, 890)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 795))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 795))
findWidget('OOF3D Graphics 1').resize(1000, 903)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 808))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 808))
findWidget('OOF3D Graphics 1').resize(1000, 916)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 821))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 821))
findWidget('OOF3D Graphics 1').resize(1000, 928)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 833))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 833))
findWidget('OOF3D Graphics 1').resize(1000, 936)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 841))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 841))
findWidget('OOF3D Graphics 1').resize(1000, 937)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 842))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 842))
findWidget('OOF3D Graphics 1').resize(1000, 938)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 843))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 843))
findWidget('OOF3D Graphics 1').resize(1000, 939)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 844))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 844))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 842))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 842))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 819))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 819))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 782))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 782))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 760))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 760))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 751))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 751))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 744))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 744))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 733))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 733))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 723))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 723))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 717))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 717))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 699))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 699))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 692))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 692))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 689))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 689))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 688))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 688))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 687))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 687))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 685))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 685))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 684))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 684))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.1997721191890e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.3995442383781e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 9.5993163575671e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.2799088476756e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.5998860595945e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.9198632715134e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2398404834323e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5598176953512e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.8797949072701e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9900000000000e+02)
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
findWidget('OOF3D').resize(550, 350)
#Going to the Skeleton Page
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
findWidget('OOF3D').resize(601, 357)
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
checkpoint skeleton page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
#Selecting the microstructure '0color'
setComboBox(findWidget('OOF3D:Skeleton Page:Microstructure'), '0color')
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
#Selecting Rationalize Method
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Chooser'), 'Rationalize')
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Rationalize')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','All Elements')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D').resize(631, 437)
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
checkpoint skeleton page sensitized
#By default the targets are on All Elements, meaning that the OK button should always be sensitized for any criterion
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
findWidget('OOF3D').resize(631, 481)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
#For the following case we need to check the Elements Selection
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:targets:Chooser'), 'Selected Elements')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','Selected Elements')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 684))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 684))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Skeleton Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 684))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 684))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 650)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.0600000000000e+02,y= 1.0600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 650)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.0600000000000e+02,y= 1.0600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 650)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1300000000000e+02,y= 2.8600000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 650)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.1300000000000e+02,y= 2.8600000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
#For this section we need to take a look at the number of Badly shaped Elements
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:targets:Chooser'), 'Badly Shaped Elements')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','Badly Shaped Elements')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
findWidget('OOF3D').resize(631, 503)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
#For this case we probably need to check if there are some suspected elements in the Skeleton Status
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:targets:Chooser'), 'Suspect Elements')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','Suspect Elements')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:targets:Chooser'), 'All Elements')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','All Elements')
#Selecting the microstructure '5color'
setComboBox(findWidget('OOF3D:Skeleton Page:Microstructure'), '5color')
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '24')
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Hide
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '23')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((23,))
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint OOF.Graphics_1.Layer.Show
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
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Rationalize')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','All Elements')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
#For the following one we will check the Elements Selection state
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:targets:Chooser'), 'Selected Elements')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','Selected Elements')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 650)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.0500000000000e+02,y= 1.1500000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 650)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.0500000000000e+02,y= 1.1500000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 650)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 9.7000000000000e+01,y= 2.6300000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 650)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 9.7000000000000e+01,y= 2.6300000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
#We need to check the number of Badly Shaped Elements in the Skeleton Status
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:targets:Chooser'), 'Badly Shaped Elements')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','Badly Shaped Elements')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
#We have to check here the number of Suspected Elements in the Skeleton Status
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:targets:Chooser'), 'Suspect Elements')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','Suspect Elements')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Automatic')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Automatic')
findWidget('OOF3D:Skeleton Page:Pane').set_position(305)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:method:Chooser'), 'Specified')
assert tests.skeletonMethodMethodListCheck('Rationalize','Specified','Automatic')
assert tests.currentSkeletonMethodMethodCheck('Rationalize','Specified')
findWidget('OOF3D:Skeleton Page:Pane').set_position(110)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Rationalize','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Rationalize','Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Rationalize:targets:Chooser'), 'All Elements')
assert tests.skeletonMethodTargetsListCheck('Rationalize','All Elements','Selected Elements','Badly Shaped Elements','Suspect Elements')
assert tests.currentSkeletonMethodTargetsCheck('Rationalize','All Elements')

findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('skelpagerationalize.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('skelpagerationalize.log')
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))