# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.8 $
# $Author: fyc $
# $Date: 2014/09/19 22:52:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#This GUI test case is tight to the skeleton page global test.
#It aims to check if the skeleton Snap Nodes Method is reliabily working according
#to the sensitization of the OK button in case of an Heterogenity, Selection , Group situations.
#AS commented in the previous test case, we will sensitize the OK Button base on the targets only
#to not fall into a OK_Hard situation. Not all the targets are concerned of course.
#It is only Heterogeneous *, Selected * and * in Group.
#In here we two targets to check. Heterogeneous Elements and Selected Elements.
#In the other target OK should be sensitized by default.

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
findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D Graphics 1').resize(1000, 801)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 706))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 706))
findWidget('OOF3D Graphics 1').resize(1000, 802)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 707))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 707))
findWidget('OOF3D Graphics 1').resize(1000, 811)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 716))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 716))
findWidget('OOF3D Graphics 1').resize(1000, 824)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 729))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 729))
findWidget('OOF3D Graphics 1').resize(1000, 850)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 755))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 755))
findWidget('OOF3D Graphics 1').resize(1000, 873)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 778))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 778))
findWidget('OOF3D Graphics 1').resize(1000, 896)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 801))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 801))
findWidget('OOF3D Graphics 1').resize(1000, 912)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 817))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 817))
findWidget('OOF3D Graphics 1').resize(1000, 925)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 830))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 830))
findWidget('OOF3D Graphics 1').resize(1000, 932)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 837))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 837))
findWidget('OOF3D Graphics 1').resize(1000, 937)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 842))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 842))
findWidget('OOF3D Graphics 1').resize(1000, 938)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 843))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 843))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 841))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 841))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 836))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 836))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 830))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 830))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 821))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 821))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 809))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 809))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 800))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 800))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 794))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 794))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 788))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 788))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 780))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 780))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 771))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 771))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 762))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 762))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 754))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 754))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 745))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 745))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 736))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 736))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 728))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 728))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 724))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 724))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 722))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 722))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 717))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 717))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 712))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 712))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 706))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 706))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 702))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 702))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 699))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 699))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 694))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 694))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 691))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 691))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 687))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 687))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 682))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 682))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2:fill').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 680))
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.2350317596360e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.4700635192720e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 9.7050952789081e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.2940127038544e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.6175158798180e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.9410190557816e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2645222317452e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5880254077088e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9115285836724e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9600000000000e+02)
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
checkpoint OOF.Graphics_1.Layer.Select
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Show
#Going to the Skeleton Page
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
findWidget('OOF3D').resize(601, 357)
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
checkpoint skeleton page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
#Selecting Snap Nodes Method
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Chooser'), 'Snap Nodes')
findWidget('OOF3D:Skeleton Page:Pane').set_position(275)
checkpoint skeleton page sensitized
#Selecting the microstructure '0color'
setComboBox(findWidget('OOF3D:Skeleton Page:Microstructure'), '0color')
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Nodes')
assert tests.skeletonMethodTargetsListCheck('Snap Nodes','All Nodes','Selected Elements','Heterogeneous Elements',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Nodes','All Nodes')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
#By default the targets is All Nodes. In this all criterions cases the OK Button should be sensitized because of the OK_Hard situation here.
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D').resize(601, 379)
findWidget('OOF3D:Skeleton Page:Pane').set_position(220)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(275)
#For the following targets we need to check the homogeneity index to update the sensitized state of the OK Button
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:targets:Chooser'), 'Selected Elements')
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Nodes')
assert tests.skeletonMethodTargetsListCheck('Snap Nodes','All Nodes','Selected Elements','Heterogeneous Elements',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Nodes','Selected Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D').resize(601, 379)
findWidget('OOF3D:Skeleton Page:Pane').set_position(220)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(275)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 680))
setComboBox(findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBChooser'), 'Skeleton Selection')
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 680))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 680))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 646)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.3600000000000e+02,y= 1.6200000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 646)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.3600000000000e+02,y= 1.6200000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 646)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.3100000000000e+02,y= 1.9700000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 646)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3100000000000e+02,y= 1.9700000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D').resize(601, 379)
findWidget('OOF3D:Skeleton Page:Pane').set_position(220)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(275)
#For the following targets also we need to check the homogeneity index to update the sensitized state of the OK Button
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:targets:Chooser'), 'Heterogeneous Elements')
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Nodes')
assert tests.skeletonMethodTargetsListCheck('Snap Nodes','All Nodes','Selected Elements','Heterogeneous Elements',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Nodes','Heterogeneous Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D').resize(601, 379)
findWidget('OOF3D:Skeleton Page:Pane').set_position(220)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:targets:Chooser'), 'All Nodes')
findWidget('OOF3D:Skeleton Page:Pane').set_position(275)
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
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.6364968240364e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.3129936480728e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.9894904721092e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.6659872961456e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.3424841201820e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.0189809442184e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.9547776825478e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.7197459229118e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.8471416327578e+00)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.2350317596360e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.4700635192720e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 9.7050952789081e+01)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.2940127038544e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.6175158798180e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.9410190557816e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2645222317452e+02)
findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((23,))
checkpoint OOF.Graphics_1.Layer.Select
tree=findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(1)
tree.row_activated((23,), column)
checkpoint toplevel widget mapped Dialog-Edit Graphics Layer
findWidget('Dialog-Edit Graphics Layer').resize(354, 305)
widget_1=findWidget('Dialog-Edit Graphics Layer')
handled_1=widget_1.event(event(gtk.gdk.DELETE,window=widget_1.window))
postpone if not handled_1: widget_1.destroy()
findCellRenderer(findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '23')
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2600000000000e+02)
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Show
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Nodes')
assert tests.skeletonMethodTargetsListCheck('Snap Nodes','All Nodes','Selected Elements','Heterogeneous Elements',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Nodes','All Nodes')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
#By default the targets is  still All Nodes. In this all criterions cases the OK Button should be sensitized because of the OK_Hard situation here.
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D').resize(601, 379)
findWidget('OOF3D:Skeleton Page:Pane').set_position(220)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(275)
#For the following targets we need to check the homogeneity index to update the sensitized state of the OK Button
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:targets:Chooser'), 'Selected Elements')
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Nodes')
assert tests.skeletonMethodTargetsListCheck('Snap Nodes','All Nodes','Selected Elements','Heterogeneous Elements',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Nodes','Selected Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D').resize(601, 379)
findWidget('OOF3D:Skeleton Page:Pane').set_position(220)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(275)
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 646)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5600000000000e+02,y= 1.5600000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 646)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5600000000000e+02,y= 1.5600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 646)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.2500000000000e+02,y= 1.9400000000000e+02,button=1,state=17,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 646)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.2500000000000e+02,y= 1.9400000000000e+02,button=1,state=273,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D').resize(601, 379)
findWidget('OOF3D:Skeleton Page:Pane').set_position(220)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
#For the following targets also like with '0color' we need to check the homogeneity index to update the sensitized state of the OK Button
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:targets:Chooser'), 'Heterogeneous Elements')
assert tests.skeletonPageModificationSensitivityCheck1()
assert tests.skeletonMethodListCheck('Refine','Snap Nodes','Anneal','Smooth','Surface Smooth','Rationalize','Fix Illegal Elements','Snap Refine',)
assert tests.currentSkeletonMethodCheck('Snap Nodes')
assert tests.skeletonMethodTargetsListCheck('Snap Nodes','All Nodes','Selected Elements','Heterogeneous Elements',)
assert tests.currentSkeletonMethodTargetsCheck('Snap Nodes','Heterogeneous Elements')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Skeleton Selection:Element:Clear').clicked()
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Clear
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D').resize(601, 379)
findWidget('OOF3D:Skeleton Page:Pane').set_position(220)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Unconditional')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Unconditional')
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Chooser'), 'Average Energy')
assert tests.skeletonMethodCriterionListCheck('Snap Nodes','Average Energy','Unconditional')
assert tests.currentSkeletonMethodCriterionCheck('Snap Nodes','Average Energy')
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
setComboBox(findWidget('OOF3D:Skeleton Page:Pane:Modification:Method:Snap Nodes:targets:Chooser'), 'All Nodes')
findWidget('OOF3D:Skeleton Page:Pane').set_position(275)

findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 95)
findWidget('Dialog-Python_Log:filename').set_text('skelpagesnapnodes.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('skelpagesnapnodes.log')
widget_0=findWidget('OOF3D')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))