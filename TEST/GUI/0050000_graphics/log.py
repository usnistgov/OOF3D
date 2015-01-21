checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:42 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.sensitizationCheck0()
assert tests.layerCheck()
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay')
assert tests.noContourBounds()
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(277)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(244)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(244)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(144)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(139)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(137)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:List_All_Layers').activate()
checkpoint OOF.Graphics_1.Settings.List_All_Layers
checkpoint_count("contourmap info updated for Graphics_1")
# Unfortunately, there doesn't seem to be a way of checking that
# layers are listed, using the gtk.TreeView API.  tests.layerCheck
# just checks for the "listed" flag in the actual layer, and doesn't
# care whether or not the GUI is using the flag.  Toggling
# List_All_Layers doesn't change the flag.
assert tests.layerCheck()
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Long_Layer_Names').activate()
checkpoint OOF.Graphics_1.Settings.Long_Layer_Names
# Similarly, there's no way to check whether long layer names are being used.
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Long_Layer_Names').activate()
checkpoint OOF.Graphics_1.Settings.Long_Layer_Names
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:List_All_Layers').activate()
checkpoint OOF.Graphics_1.Settings.List_All_Layers
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(150)
findWidget('OOF2:Microstructure Page:NewFromFile').clicked()
checkpoint toplevel widget mapped Dialog-Load Image and create Microstructure
findWidget('Dialog-Load Image and create Microstructure').resize(342, 144)
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('..')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../..')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../e')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../ex')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../exa')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../exam')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examp')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../exampl')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../example')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/s')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/sm')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/sma')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/smal')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small.p')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small.pp')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/small.ppm')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
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
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Microstructure.Create_From_ImageFile
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.sensitizationCheck0()
assert tests.layerCheck("Bitmap")
assert tests.selectedLayerCheck(None)
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
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
checkpoint_count("contourmap info updated for Graphics_1")
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
assert tests.sensitizationCheck0()
assert tests.layerCheck("Bitmap", "Element Edges")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
checkpoint OOF.Graphics_1.Layer.Select
assert tests.sensitizationCheck1()
tree=findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(2)
tree.row_activated((10,), column)
checkpoint layereditor layerset changed
checkpoint toplevel widget mapped OOF2 Graphics Layer Editor
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Edit
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Skeleton skeleton
findWidget('Dialog-New Display Method for Skeleton skeleton').resize(333, 200)
setComboBox(findWidget('Dialog-New Display Method for Skeleton skeleton:method:Chooser'), 'Material Color')
findWidget('Dialog-New Display Method for Skeleton skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Add_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
assert tests.layerCheck("Bitmap", "Material Color", "Element Edges")
assert tests.selectedLayerCheck("Element Edges")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Material Color', 'Bitmap')
assert tests.sensitizationCheck1()
assert tests.noContourBounds()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:Delete').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Delete_Method
assert tests.layerCheck("Bitmap", "Material Color", "Element Edges")
assert tests.selectedLayerCheck("Element Edges")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Material Color', 'Bitmap')
assert tests.sensitizationCheck1()
findWidget('OOF2 Graphics Layer Editor:Send').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint contourmap info updated for Graphics_1
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
assert tests.layerCheck("Bitmap", "Element Edges")
assert tests.selectedLayerCheck("Element Edges")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
assert tests.sensitizationCheck1()
findWidget('OOF2 Graphics Layer Editor:Send').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
assert tests.layerCheck("Bitmap", "Element Edges")
assert tests.selectedLayerCheck("Element Edges")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
assert tests.sensitizationCheck1()
tree=findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(2)
tree.row_activated((10,), column)
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Edit
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Skeleton skeleton
findWidget('Dialog-New Display Method for Skeleton skeleton').resize(253, 80)
findWidget('Dialog-New Display Method for Skeleton skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Add_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
assert tests.layerCheck("Bitmap", "Material Color", "Element Edges")
assert tests.selectedLayerCheck("Element Edges")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Material Color', 'Bitmap')
assert tests.sensitizationCheck1()
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((14,))
checkpoint OOF.Graphics_1.Layer.Select
ls_0 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_model()
data_0 = [ls_0.get_value(ls_0.get_iter((14,)),i) for i in range(ls_0.get_n_columns())]
ls_0.insert(5, data_0)
ls_0.remove(ls_0.get_iter((15,)))
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Raise.By
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.sensitizationCheck2()
assert tests.layerCheck("Bitmap", "Element Edges", "Material Color")
assert tests.selectedLayerCheck("Material Color")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Material Color', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Bitmap')
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:Reorder_All').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Reorder_All
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
assert tests.sensitizationCheck1()
assert tests.layerCheck("Bitmap", "Material Color", "Element Edges")
assert tests.selectedLayerCheck("Material Color")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Material Color', 'Bitmap')
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((15,))
checkpoint OOF.Graphics_1.Layer.Select
ls_1 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_model()
data_1 = [ls_1.get_value(ls_1.get_iter((15,)),i) for i in range(ls_1.get_n_columns())]
ls_1.insert(0, data_1)
ls_1.remove(ls_1.get_iter((16,)))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2000000000000e+01)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Raise.By
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
assert tests.sensitizationCheck3()
assert tests.allLayerNames('Bitmap', 'Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Material Color')
assert tests.layerCheck("Material Color", "Element Edges", "Bitmap")
assert tests.selectedLayerCheck("Bitmap")
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:Reorder_All').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Reorder_All
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.sensitizationCheck4()
assert tests.layerCheck("Bitmap", "Material Color", "Element Edges")
assert tests.selectedLayerCheck("Bitmap")
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Material Color', 'Bitmap')
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((14,))
checkpoint OOF.Graphics_1.Layer.Select
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:Hide').activate()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Hide
# TODO: I don't know how to check the state of a CellRendererToggle,
# so there's no test here to see if the show/hide buttons are set
# correctly.
assert tests.sensitizationCheck5()
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '14')
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Show
assert tests.sensitizationCheck1()
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:List_All_Layers').activate()
checkpoint OOF.Graphics_1.Settings.List_All_Layers
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0370370370370e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.0740740740741e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.1111111111111e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 8.1481481481481e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.3148148148148e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.1296296296296e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.3333333333333e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.7407407407407e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 8.1481481481481e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 8.7592592592593e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 9.9814814814815e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.0796296296296e+02)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.2018518518519e+02)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.2833333333333e+02)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.3444444444444e+02)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.3851851851852e+02)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.4259259259259e+02)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.4462962962963e+02)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.4870370370370e+02)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.5074074074074e+02)
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:List_All_Layers').activate()
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 0.0000000000000e+00)
checkpoint OOF.Graphics_1.Settings.List_All_Layers
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Long_Layer_Names').activate()
checkpoint OOF.Graphics_1.Settings.Long_Layer_Names
# TODO: I don't know how to check the contents of a cell, so there's
# no test here to see if the long layer names are being used.
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Long_Layer_Names').activate()
checkpoint OOF.Graphics_1.Settings.Long_Layer_Names
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2').resize(593, 482)
findWidget('OOF2:FE Mesh Page:Pane').set_position(174)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint toplevel widget mapped Warning
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('Warning').resize(364, 85)
findWidget('OOF2 Activity Viewer').resize(400, 300)
findWidget('Warning:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findWidget('OOF2:FE Mesh Page:Pane').set_position(174)
checkpoint contourmap info updated for Graphics_1
checkpoint mesh bdy page updated
checkpoint mesh bdy page updated
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
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Mesh.New
checkpoint_count("contourmap info updated for Graphics_1")
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
findWidget('OOF2').resize(684, 482)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material material to pixels
findWidget('Dialog-Assign material material to pixels').resize(240, 108)
setComboBox(findWidget('Dialog-Assign material material to pixels:pixels'), '<all>')
findWidget('Dialog-Assign material material to pixels:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Assign
checkpoint_count("contourmap info updated for Graphics_1")
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Fields & Equations')
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint OOF.Subproblem.Field.Deactivate
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Solver')

checkpoint_count("contourmap info updated for Graphics_1")
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
tree=findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers')
column = tree.get_column(1)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Initialize field Temperature
findWidget('Dialog-Initialize field Temperature').resize(263, 102)
setComboBox(findWidget('Dialog-Initialize field Temperature:initializer:Chooser'), 'XYFunction')
findWidget('Dialog-Initialize field Temperature').resize(281, 102)
findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x')
findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*')
findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*y')
findWidget('Dialog-Initialize field Temperature:gtk-ok').clicked()
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().unselect_all()
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().unselect_all()
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().unselect_all()
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
checkpoint OOF.Mesh.Set_Field_Initializer
findWidget('OOF2:Solver Page:VPane:FieldInit:Apply').clicked()
checkpoint OOF.Mesh.Apply_Field_Initializers
checkpoint contourmap info updated for Graphics_1

# findWidget('OOF2:Solver Page:VPane:HPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
# tree=findWidget('OOF2:Solver Page:VPane:HPane:FieldInit:Scroll:Initializers')
# column = tree.get_column(1)
# tree.row_activated((0,), column)
# checkpoint toplevel widget mapped Dialog-Initialize field Temperature
# findWidget('Dialog-Initialize field Temperature').resize(243, 100)
# setComboBox(findWidget('Dialog-Initialize field Temperature:initializer:Chooser'), 'XYFunction')
# findWidget('Dialog-Initialize field Temperature').resize(261, 100)
# findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x')
# findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*')
# findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*y')
# findWidget('Dialog-Initialize field Temperature:gtk-ok').clicked()
# findWidget('OOF2:Solver Page:VPane:HPane:FieldInit:Scroll:Initializers').get_selection().unselect_all()
# findWidget('OOF2:Solver Page:VPane:HPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
# checkpoint contourmap info updated for Graphics_1
# checkpoint OOF.Mesh.Set_Field_Initializer
# findWidget('OOF2:Solver Page:VPane:HPane:FieldInit:Apply').clicked()
# checkpoint contourmap info updated for Graphics_1
# checkpoint OOF.Mesh.Apply_Field_Initializers
checkpoint_count("contourmap info updated for Graphics_1")
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
assert tests.noContourBounds()
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
checkpoint OOF.Graphics_1.Layer.Select
tree=findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(3)
tree.row_activated((10,), column)
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Edit
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Mesh mesh
findWidget('Dialog-New Display Method for Mesh mesh').resize(339, 232)
setComboBox(findWidget('Dialog-New Display Method for Mesh mesh:method:Chooser'), 'Solid Fill')
findWidget('Dialog-New Display Method for Mesh mesh').resize(414, 320)
findWidget('Dialog-New Display Method for Mesh mesh:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(594, 200)
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Add_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.contourBounds(352, 1.72e4, tolerance=1.e-3)
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Aspect_Ratio').activate()
checkpoint toplevel widget mapped Dialog-Aspect_Ratio
findWidget('Dialog-Aspect_Ratio').resize(194, 72)
findWidget('Dialog-Aspect_Ratio:ratio').set_text('')
findWidget('Dialog-Aspect_Ratio:ratio').set_text('3')
findWidget('Dialog-Aspect_Ratio:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Settings.Aspect_Ratio
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(241)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(667)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findWidget('OOF2 Graphics 1:Pane0:Pane1:ContourMap:Clear').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(241)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(667)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Contourmap_Marker_Size').activate()
checkpoint toplevel widget mapped Dialog-Contourmap_Marker_Size
findWidget('Dialog-Contourmap_Marker_Size').resize(194, 72)
findWidget('Dialog-Contourmap_Marker_Size:width').set_text('')
findWidget('Dialog-Contourmap_Marker_Size:width').set_text('5')
findWidget('Dialog-Contourmap_Marker_Size:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Settings.Contourmap_Marker_Size
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Color:Contourmap_Marker').activate()
checkpoint toplevel widget mapped Dialog-Contourmap_Marker
findWidget('Dialog-Contourmap_Marker').resize(248, 144)
setComboBox(findWidget('Dialog-Contourmap_Marker:color:Chooser'), 'RGBColor')
findWidget('Dialog-Contourmap_Marker').resize(257, 192)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 5.2380952380952e-01)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 5.3968253968254e-01)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 5.8730158730159e-01)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 6.0317460317460e-01)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 6.1904761904762e-01)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 6.6666666666667e-01)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 7.6190476190476e-01)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 7.7777777777778e-01)
findWidget('Dialog-Contourmap_Marker:color:RGBColor:Red:slider').get_adjustment().set_value( 7.9365079365079e-01)
findWidget('Dialog-Contourmap_Marker:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint OOF.Graphics_1.Settings.Color.Contourmap_Marker
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Color:Background').activate()
checkpoint toplevel widget mapped Dialog-Background
findWidget('Dialog-Background').resize(248, 144)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 9.8412698412698e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 9.5238095238095e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 9.3650793650794e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 9.2063492063492e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 9.0476190476190e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 8.8888888888889e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 8.7301587301587e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 8.2539682539683e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 8.0952380952381e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 7.9365079365079e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 7.7777777777778e-01)
findWidget('Dialog-Background:color:Gray:Gray:slider').get_adjustment().set_value( 7.9365079365079e-01)
findWidget('Dialog-Background:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(667)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint OOF.Graphics_1.Settings.Color.Background
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:In').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.8000000000000e+01)
checkpoint OOF.Graphics_1.Settings.Zoom.In
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:In').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 7.0000000000000e+01)
checkpoint OOF.Graphics_1.Settings.Zoom.In
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:In').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 1.3300000000000e+02)
checkpoint OOF.Graphics_1.Settings.Zoom.In
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:Fill_Window').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 0.0000000000000e+00)
checkpoint OOF.Graphics_1.Settings.Zoom.Fill_Window
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:Out').activate()
checkpoint OOF.Graphics_1.Settings.Zoom.Out
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:Out').activate()
checkpoint OOF.Graphics_1.Settings.Zoom.Out
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:Fill_Window').activate()
checkpoint OOF.Graphics_1.Settings.Zoom.Fill_Window
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Margin').activate()
checkpoint toplevel widget mapped Dialog-Margin
findWidget('Dialog-Margin').resize(194, 72)
findWidget('Dialog-Margin:fraction').set_text('0.00000000000000003')
findWidget('Dialog-Margin:fraction').set_text('0.010000000000000003')
findWidget('Dialog-Margin:gtk-ok').clicked()
checkpoint OOF.Graphics_1.Settings.Margin
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'File:Redraw').activate()
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.File.Redraw
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:Fill_Window').activate()
checkpoint OOF.Graphics_1.Settings.Zoom.Fill_Window
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Mesh mesh
findWidget('Dialog-New Display Method for Mesh mesh').resize(414, 320)
setComboBox(findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:what_0'), 'XYFunction')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x*')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**2')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**2 ')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**2 +')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**2 + ')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**2 + y')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**2 + y*')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**2 + y**')
findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:what:Parameters:f').set_text('x**2 + y**2')
setComboBox(findWidget('Dialog-New Display Method for Mesh mesh:method:Solid Fill:colormap:Chooser'), 'TequilaSunrise')
findWidget('Dialog-New Display Method for Mesh mesh:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(622, 200)
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Add_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.contourBounds(703, 3.45e4, tolerance=1.e-3)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=1, rend=0).emit('toggled', '17')
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((17,))
checkpoint OOF.Graphics_1.Layer.Select
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Layer.Show_Contour_Map
assert tests.allLayerNames('Info', 'Selected Nodes', 'Pinned Nodes', 'Moving Nodes', 'Pixel Info', 'Selected Segments', 'Illegal Elements', 'Info', 'Selected Boundary', 'Cross Section', 'Element Edges', 'Element Edges', 'Selected Elements', 'BitmapOverlay', 'BitmapOverlay', 'Material Color', 'Solid Fill', 'Solid Fill', 'Bitmap')
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.contourBounds(352, 1.72e4, tolerance=1.e-3)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(667)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=1, rend=0).emit('toggled', '16')
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((16,))
## TODO: This test often hangs at this point, apparently due to a
## python interpreter lock deadlock.  It may be more likely to fail
## when run with --debug.
checkpoint OOF.Graphics_1.Layer.Select
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Layer.Show_Contour_Map
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
assert tests.sensitizationCheck6()
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.contourBounds(703, 3.45e04, tolerance=1.e-3)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '16')
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Layer.Hide
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.contourBounds(352, 1.72e4, tolerance=1.e-3)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(667)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '16')
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Layer.Show
assert tests.contourBounds(703, 3.45e4, tolerance=1.e-3)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '17')
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((17,))
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.Graphics_1.Layer.Select
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Layer.Hide
assert tests.contourBounds(703, 3.45e4, tolerance=1.e-3)
checkpoint_count("contourmap info updated for Graphics_1")
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '17')
findWidget('OOF2 Graphics 1:Pane0').set_position(138)
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Graphics_1.Layer.Show
checkpoint_count("contourmap info updated for Graphics_1")
assert tests.contourBounds(703, 3.45e4, tolerance=1.e-3)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('g')
findWidget('Dialog-Python_Log:filename').set_text('gf')
findWidget('Dialog-Python_Log:filename').set_text('gfx')
findWidget('Dialog-Python_Log:filename').set_text('gfxt')
findWidget('Dialog-Python_Log:filename').set_text('gfxte')
findWidget('Dialog-Python_Log:filename').set_text('gfxtes')
findWidget('Dialog-Python_Log:filename').set_text('gfxtest')
findWidget('Dialog-Python_Log:filename').set_text('gfxtest.')
findWidget('Dialog-Python_Log:filename').set_text('gfxtest.l')
findWidget('Dialog-Python_Log:filename').set_text('gfxtest.lo')
findWidget('Dialog-Python_Log:filename').set_text('gfxtest.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff("gfxtest.log")
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
