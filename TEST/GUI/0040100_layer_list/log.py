# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:40 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# Test the right-click pop-up menu on the graphics window's layer
# list.

import tests

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
checkpoint interface page updated
checkpoint OOF.Microstructure.Create_From_ImageFile
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(285)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
checkpoint toplevel widget mapped OOF2 Graphics 1
findWidget('OOF2 Graphics 1').resize(800, 400)
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
checkpoint OOF.Windows.Graphics.New
assert tests.selectedLayerCheck(None)
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0').set_position(284)
findWidget('OOF2 Graphics 1:Pane0').set_position(275)
findWidget('OOF2 Graphics 1:Pane0').set_position(250)
findWidget('OOF2 Graphics 1:Pane0').set_position(221)
findWidget('OOF2 Graphics 1:Pane0').set_position(214)
findWidget('OOF2 Graphics 1:Pane0').set_position(201)
findWidget('OOF2 Graphics 1:Pane0').set_position(197)
findWidget('OOF2 Graphics 1:Pane0').set_position(194)
findWidget('OOF2 Graphics 1:Pane0').set_position(192)
findWidget('OOF2 Graphics 1:Pane0').set_position(191)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(656, 424)
findWidget('OOF2:Skeleton Page:Pane').set_position(303)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('PopUp-Layer').deactivate()
findWidget('Dialog-New skeleton').resize(388, 198)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint Move Node toolbox writable changed
checkpoint Graphics_1 Move Nodes sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Skeleton.New
assert tests.selectedLayerCheck(None)
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
widget_0 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_0.event(event(gtk.gdk.BUTTON_PRESS,x= 2.1500000000000e+02,y= 4.8000000000000e+01,button=3,state=0,window=widget_0.window))
checkpoint toplevel widget mapped PopUp-Layer
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
checkpoint OOF.Graphics_1.Layer.Select
assert tests.selectedLayerCheck('Element Edges')
findWidget('PopUp-Layer').deactivate()
findMenu(findWidget('PopUp-Layer'), 'Delete').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint Move Node toolbox writable changed
checkpoint Graphics_1 Move Nodes sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Delete
assert tests.selectedLayerCheck(None)
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
widget_1 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_1.event(event(gtk.gdk.BUTTON_PRESS,x= 2.0500000000000e+02,y= 3.3000000000000e+01,button=3,state=0,window=widget_1.window))
checkpoint toplevel widget mapped PopUp-Layer
findWidget('PopUp-Layer').deactivate()
findMenu(findWidget('PopUp-Layer'), 'New').activate()
checkpoint layereditor layerset changed
checkpoint toplevel widget mapped OOF2 Graphics Layer Editor
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.New
setComboBox(findWidget('OOF2 Graphics Layer Editor:ObjectScroll:category'), 'Skeleton')
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.DisplayedObject
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Skeleton skeleton
findWidget('PopUp-Layer').deactivate()
findWidget('Dialog-New Display Method for Skeleton skeleton').resize(339, 196)
findWidget('Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:slider').get_adjustment().set_value( 1.1764705882353e-01)
findWidget('Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:slider').get_adjustment().set_value( 2.3529411764706e-01)
findWidget('Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:slider').get_adjustment().set_value( 7.0588235294118e-01)
findWidget('Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:slider').get_adjustment().set_value( 1.4117647058824e+00)
findWidget('Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:slider').get_adjustment().set_value( 2.1176470588235e+00)
findWidget('Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:slider').get_adjustment().set_value( 2.8235294117647e+00)
findWidget('Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:slider').get_adjustment().set_value( 3.0588235294118e+00)
findWidget('Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:slider').get_adjustment().set_value( 3.2941176470588e+00)
findWidget('Dialog-New Display Method for Skeleton skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint Move Node toolbox writable changed
checkpoint Graphics_1 Move Nodes sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Add_Method
widget_2=findWidget('OOF2 Graphics Layer Editor')
handled_0=widget_2.event(event(gtk.gdk.DELETE,window=widget_2.window))
postpone if not handled_0: widget_2.destroy()
widget_3 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_3.event(event(gtk.gdk.BUTTON_PRESS,x= 1.8000000000000e+02,y= 8.0000000000000e+01,button=1,state=0,window=widget_3.window))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((14,))
checkpoint OOF.Graphics_1.Layer.Select
assert tests.selectedLayerCheck('Bitmap')
findWidget('PopUp-Layer').deactivate()
ls_0 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_model()
data_0 = [ls_0.get_value(ls_0.get_iter((14,)),i) for i in range(ls_0.get_n_columns())]
ls_0.insert(4, data_0)
ls_0.remove(ls_0.get_iter((15,)))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Raise.By
assert tests.selectedLayerCheck('Bitmap')
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Bitmap', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay')
widget_4 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_4.event(event(gtk.gdk.BUTTON_PRESS,x= 1.9400000000000e+02,y= 1.8000000000000e+01,button=3,state=0,window=widget_4.window))
checkpoint toplevel widget mapped PopUp-Layer
findWidget('PopUp-Layer').deactivate()
findMenu(findWidget('PopUp-Layer'), 'Reorder_All').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Reorder_All
assert tests.selectedLayerCheck('Bitmap')
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
widget_5 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_5.event(event(gtk.gdk.BUTTON_PRESS,x= 1.7700000000000e+02,y= 8.3000000000000e+01,button=3,state=0,window=widget_5.window))
checkpoint toplevel widget mapped PopUp-Layer
findWidget('PopUp-Layer').deactivate()
findMenu(findWidget('PopUp-Layer'), 'Hide').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Hide
# Here we should check that the layer is hidden and the checkbox is
# unchecked.  That's hard to do!?
widget_6 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_6.event(event(gtk.gdk.BUTTON_PRESS,x= 1.8300000000000e+02,y= 8.1000000000000e+01,button=3,state=0,window=widget_6.window))
checkpoint toplevel widget mapped PopUp-Layer
findWidget('PopUp-Layer').deactivate()
findMenu(findWidget('PopUp-Layer'), 'Show').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Show
widget_7 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_7.event(event(gtk.gdk.BUTTON_PRESS,x= 1.6500000000000e+02,y= 5.8000000000000e+01,button=1,state=0,window=widget_7.window))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
checkpoint OOF.Graphics_1.Layer.Select
widget_8 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_8.event(event(gtk.gdk.BUTTON_PRESS,x= 1.7000000000000e+02,y= 5.1000000000000e+01,button=3,state=0,window=widget_8.window))
checkpoint toplevel widget mapped PopUp-Layer
findWidget('PopUp-Layer').deactivate()
findMenu(findWidget('PopUp-Layer'), 'Delete').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Delete
widget_9 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_9.event(event(gtk.gdk.BUTTON_PRESS,x= 1.7700000000000e+02,y= 7.0000000000000e+01,button=1,state=0,window=widget_9.window))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((13,))
checkpoint OOF.Graphics_1.Layer.Select
widget_10 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_10.event(event(gtk.gdk.BUTTON_PRESS,x= 1.8700000000000e+02,y= 7.6000000000000e+01,button=3,state=0,window=widget_10.window))
checkpoint toplevel widget mapped PopUp-Layer
findWidget('PopUp-Layer').deactivate()
findMenu(findWidget('PopUp-Layer'), 'Delete').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Delete
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('PopUp-Layer').deactivate()
findWidget('Dialog-Python_Log').resize(194, 71)
findWidget('Dialog-Python_Log:filename').set_text('l')
findWidget('Dialog-Python_Log:filename').set_text('la')
findWidget('Dialog-Python_Log:filename').set_text('lay')
findWidget('Dialog-Python_Log:filename').set_text('laye')
findWidget('Dialog-Python_Log:filename').set_text('layer')
findWidget('Dialog-Python_Log:filename').set_text('layerl')
findWidget('Dialog-Python_Log:filename').set_text('layerli')
findWidget('Dialog-Python_Log:filename').set_text('layerlis')
findWidget('Dialog-Python_Log:filename').set_text('layerlist')
findWidget('Dialog-Python_Log:filename').set_text('layerlist.')
findWidget('Dialog-Python_Log:filename').set_text('layerlist.l')
findWidget('Dialog-Python_Log:filename').set_text('layerlist.lo')
findWidget('Dialog-Python_Log:filename').set_text('layerlist.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff("layerlist.log")
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint OOF.Graphics_1.File.Close
