checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:34 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

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
checkpoint OOF.Microstructure.Create_From_ImageFile
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
checkpoint skeleton page sensitized
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
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
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Skeleton.New
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5263157894737e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.2631578947368e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.5157894736842e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.7684210526316e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0210526315789e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2736842105263e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5263157894737e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.7789473684211e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.0315789473684e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.0000000000000e+01)
checkpoint OOF.Graphics_1.Layer.Select
tree=findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(3)
tree.row_activated((10,), column)
checkpoint layereditor layerset changed
checkpoint toplevel widget mapped OOF2 Graphics Layer Editor
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Edit
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
assert tests.sensitivityCheck0()
assert tests.layerCheck("Graphics_1", "Bitmap", "Element Edges")
assert tests.selectedLayerCheck("Graphics_1", "Element Edges")
assert tests.layerEditorListCheck("Element Edges")
assert tests.layerEditorSelectionCheck("Element Edges")
setComboBox(findWidget('OOF2 Graphics Layer Editor:ObjectScroll:category'), 'Image')
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.DisplayedObject
assert tests.layerEditorListCheck("(invalid) Element Edges")
assert tests.layerEditorSelectionCheck("(invalid) Element Edges")
assert tests.sensitivityCheck1()
setComboBox(findWidget('OOF2 Graphics Layer Editor:ObjectScroll:category'), 'Skeleton')
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.DisplayedObject
assert tests.sensitivityCheck0()
assert tests.layerEditorListCheck("Element Edges")
assert tests.layerEditorSelectionCheck("Element Edges")
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
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Add_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.layerEditorListCheck("Element Edges", "Material Color")
assert tests.layerEditorSelectionCheck("Material Color")
assert tests.layerCheck("Graphics_1", "Bitmap", "Material Color", "Element Edges")
assert tests.selectedLayerCheck("Graphics_1", "Element Edges")
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:ListScroll:List').get_selection().select_path((0,))
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:Delete').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Delete_Method
assert tests.layerEditorListCheck("(invalid) <deleted>", "Material Color")
assert tests.layerEditorSelectionCheck(None)
assert tests.layerCheck("Graphics_1", "Bitmap", "Material Color", "Element Edges")
assert tests.selectedLayerCheck("Graphics_1", "Element Edges")
findWidget('OOF2 Graphics Layer Editor:Send').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.layerEditorListCheck("(invalid) <deleted>", "Material Color")
assert tests.layerEditorSelectionCheck(None)
assert tests.layerCheck("Graphics_1", "Bitmap", "Material Color")
assert tests.selectedLayerCheck("Graphics_1", None)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((13,))
checkpoint OOF.Graphics_1.Layer.Select
tree=findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(3)
tree.row_activated((13,), column)
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Edit
assert tests.layerEditorListCheck("Material Color")
assert tests.layerEditorSelectionCheck("Material Color")
assert tests.layerCheck("Graphics_1", "Bitmap", "Material Color")
assert tests.selectedLayerCheck("Graphics_1", "Material Color")
findMenu(findWidget('OOF2 Graphics Layer Editor:MenuBar'), 'Settings:AutoSend').activate()
checkpoint OOF.LayerEditor.Settings.AutoSend
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:Edit').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Skeleton skeleton
findWidget('Dialog-New Display Method for Skeleton skeleton').resize(253, 80)
findWidget('Dialog-New Display Method for Skeleton skeleton:gtk-ok').clicked()
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Replace_Method
assert tests.layerEditorListCheck("Material Color")
assert tests.layerEditorSelectionCheck("Material Color")
assert tests.layerCheck("Graphics_1", "Bitmap", "Material Color")
assert tests.selectedLayerCheck("Graphics_1", "Material Color")
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:Edit').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Skeleton skeleton
findWidget('Dialog-New Display Method for Skeleton skeleton').resize(253, 80)
setComboBox(findWidget('Dialog-New Display Method for Skeleton skeleton:method:Chooser'), 'Element Edges')
findWidget('Dialog-New Display Method for Skeleton skeleton').resize(333, 200)
findWidget('Dialog-New Display Method for Skeleton skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Replace_Method
assert tests.layerEditorListCheck("Element Edges")
assert tests.layerEditorSelectionCheck("Element Edges")
assert tests.layerCheck("Graphics_1", "Bitmap", "Material Color")
assert tests.selectedLayerCheck("Graphics_1", "Material Color")
findWidget('OOF2 Graphics Layer Editor:Send').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.layerEditorSelectionCheck("Element Edges")
assert tests.layerEditorListCheck("Element Edges")
assert tests.layerCheck("Graphics_1", "Bitmap", "Element Edges")
assert tests.selectedLayerCheck("Graphics_1", "Element Edges")
findMenu(findWidget('OOF2 Graphics Layer Editor:MenuBar'), 'Settings:AutoSend').activate()
checkpoint OOF.LayerEditor.Settings.AutoSend
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:Edit').clicked()
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
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Replace_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.layerEditorSelectionCheck("Material Color")
assert tests.layerEditorListCheck("Material Color")
assert tests.layerCheck("Graphics_1", "Bitmap", "Material Color")
assert tests.selectedLayerCheck("Graphics_1", "Material Color")
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('l')
findWidget('Dialog-Python_Log:filename').set_text('la')
findWidget('Dialog-Python_Log:filename').set_text('lay')
findWidget('Dialog-Python_Log:filename').set_text('laye')
findWidget('Dialog-Python_Log:filename').set_text('layer')
findWidget('Dialog-Python_Log:filename').set_text('layert')
findWidget('Dialog-Python_Log:filename').set_text('layerte')
findWidget('Dialog-Python_Log:filename').set_text('layertes')
findWidget('Dialog-Python_Log:filename').set_text('layertest')
findWidget('Dialog-Python_Log:filename').set_text('layertest2')
findWidget('Dialog-Python_Log:filename').set_text('layertest2.')
findWidget('Dialog-Python_Log:filename').set_text('layertest2.l')
findWidget('Dialog-Python_Log:filename').set_text('layertest2.lo')
findWidget('Dialog-Python_Log:filename').set_text('layertest2.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('layertest2.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint OOF.ActivityViewer.File.Close
checkpoint OOF.Graphics_1.File.Close
