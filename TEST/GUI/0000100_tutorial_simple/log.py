checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:17 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
findMenu(findWidget('OOF2:MenuBar'), 'Help:Tutorials').activate()
findMenu(findWidget('OOF2:MenuBar'), 'Help:Tutorials:A_Simple_Example').activate()
checkpoint toplevel widget mapped A Simple Example
findWidget('A Simple Example').resize(500, 300)
findWidget('A Simple Example').resize(500, 308)
findWidget('A Simple Example').resize(500, 369)
findWidget('A Simple Example').resize(501, 400)
findWidget('A Simple Example').resize(501, 402)
findWidget('A Simple Example').resize(498, 402)
findWidget('A Simple Example:Next').clicked()
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1').resize(800, 400)
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Windows.Graphics.New
findWidget('A Simple Example:Next').clicked()
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
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
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/c')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cy')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cya')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cyal')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cyall')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cyallo')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cyallow')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cyallow.')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cyallow.p')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cyallow.pn')
findWidget('Dialog-Load Image and create Microstructure:filename').set_text('../../examples/cyallow.png')
findWidget('Dialog-Load Image and create Microstructure:gtk-ok').clicked()



checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint mesh bdy page updated
checkpoint microstructure page sensitized
checkpoint pixel page updated
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
checkpoint skeleton selection page grouplist
checkpoint active area status updated
checkpoint interface page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint microstructure page sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Microstructure.Create_From_ImageFile
checkpoint skeleton selection page updated
checkpoint Graphics_1 Pixel Selection sensitized

findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(593, 350)
findWidget('OOF2:Image Page:Group').clicked()
checkpoint toplevel widget mapped Dialog-AutoGroup
findWidget('Dialog-AutoGroup').resize(211, 72)
findWidget('Dialog-AutoGroup:gtk-ok').clicked()

checkpoint contourmap info updated for Graphics_1
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.Image.AutoGroup
assert tests.checkGroupSizes()
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:GroupListScroll:GroupList').get_selection().select_path((0,))
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000)
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000)').resize(194, 72)
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000):new_name').set_text('')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000):new_name').set_text('y')
checkpoint microstructure page sensitized
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000):new_name').set_text('ye')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000):new_name').set_text('yel')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000):new_name').set_text('yell')
checkpoint meshable button set
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000):new_name').set_text('yello')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000):new_name').set_text('yellow')
findWidget('Dialog-Rename pixelgroup RGBColor(red=1.00000,green=1.00000,blue=0.00000):gtk-ok').clicked()
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:GroupListScroll:GroupList').get_selection().select_path((0,))
checkpoint interface page updated
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.Rename
checkpoint microstructure page sensitized
checkpoint meshable button set
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:GroupListScroll:GroupList').get_selection().select_path((1,))
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000)
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000)').resize(194, 72)
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('x')
checkpoint microstructure page sensitized
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('xy')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('xyN')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('xy')
checkpoint meshable button set
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('x')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('c')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('cy')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('cya')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):new_name').set_text('cyan')
findWidget('Dialog-Rename pixelgroup RGBColor(red=0.00000,green=1.00000,blue=1.00000):gtk-ok').clicked()
findWidget('OOF2:Microstructure Page:Pane:PixelGroups:GroupListScroll:GroupList').get_selection().select_path((1,))
checkpoint interface page updated
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint OOF.PixelGroup.Rename
checkpoint microstructure page sensitized
checkpoint meshable button set
assert tests.checkNewGroupNames()
assert tests.treeViewColCheck('OOF2:Microstructure Page:Pane:PixelGroups:GroupListScroll:GroupList', 0, ['yellow (1440 pixels, meshable)', 'cyan (2160 pixels, meshable)'])
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(684, 350)
assert tests.matlPageSensitizationCheck0()
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:name:Auto').clicked()
findWidget('Dialog-New material:name:Text').set_text('y')
findWidget('Dialog-New material:name:Text').set_text('ye')
findWidget('Dialog-New material:name:Text').set_text('yel')
findWidget('Dialog-New material:name:Text').set_text('yell')
findWidget('Dialog-New material:name:Text').set_text('yello')
findWidget('Dialog-New material:name:Text').set_text('yellow')
findWidget('Dialog-New material:name:Text').set_text('yellow-')
findWidget('Dialog-New material:name:Text').set_text('yellow-m')
findWidget('Dialog-New material:name:Text').set_text('yellow-ma')
findWidget('Dialog-New material:name:Text').set_text('yellow-mat')
findWidget('Dialog-New material:name:Text').set_text('yellow-mate')
findWidget('Dialog-New material:name:Text').set_text('yellow-mater')
findWidget('Dialog-New material:name:Text').set_text('yellow-materi')
findWidget('Dialog-New material:name:Text').set_text('yellow-materia')
findWidget('Dialog-New material:name:Text').set_text('yellow-material')
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.New
checkpoint_count("Materials page updated")
assert tests.chooserCheck('OOF2:Materials Page:Pane:Material:MaterialList', ['yellow-material'])
assert tests.matlPageSensitizationCheck1()
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:name:Text').set_text('-material')
findWidget('Dialog-New material:name:Text').set_text('c-material')
findWidget('Dialog-New material:name:Text').set_text('cy-material')
findWidget('Dialog-New material:name:Text').set_text('cya-material')
findWidget('Dialog-New material:name:Text').set_text('cyan-material')
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.New
assert tests.chooserCheck('OOF2:Materials Page:Pane:Material:MaterialList', [ 'cyan-material', 'yellow-material'])
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
checkpoint Materials page updated
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1,), open_all=False)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0), open_all=False)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0))
checkpoint Materials page updated
checkpoint Materials page updated
widget=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget.window))
assert tests.matlPageSensitizationCheck2()
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Isotropic
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic').resize(282, 72)
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Auto').clicked()
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('y')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('ye')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yel')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yell')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yello')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_e')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_el')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_ela')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elas')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elass')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elasst')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elass')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elas')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elast')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elasti')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elastic')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elastici')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elasticit')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('yellow_elasticity')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0, 0), open_all=False)
checkpoint Materials page updated
checkpoint OOF.Property.Copy
assert tests.matlPageSensitizationCheck3()
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity').resize(372, 244)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:Chooser'), 'Bulk and Shear')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:Bulk and Shear:bulk').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:Bulk and Shear:bulk').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:Bulk and Shear:bulk').set_text('1.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:Bulk and Shear:bulk').set_text('1.0')
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:Chooser'), 'E and nu')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:E and nu:young').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:E and nu:young').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:E and nu:young').set_text('1.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:E and nu:young').set_text('1.0')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:cijkl:E and nu:poisson').set_text('0.3')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;yellow_elasticity:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(581, 200)

checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.yellow_elasticity
assert tests.selectedPropertyCheck('Mechanical:Elasticity:Isotropic:yellow_elasticity')
findWidget('A Simple Example:Next').clicked()
setComboBox(findWidget('OOF2:Materials Page:Pane:Material:MaterialList'), 'yellow-material')
checkpoint Materials page updated
checkpoint Materials page updated
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Add_property
assert tests.matlPageSensitizationCheck4()
assert tests.selectedMatlPropertyCheck('Mechanical:Elasticity:Isotropic:yellow_elasticity')
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0))
checkpoint Materials page updated
checkpoint Materials page updated
widget=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget.window))
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Mechanical;Elasticity;Isotropic
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic').resize(282, 72)
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('_elasticity')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('c_elasticity')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('cy_elasticity')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('cya_elasticity')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:new_name:Text').set_text('cyan_elasticity')
findWidget('Dialog-Copy property Mechanical;Elasticity;Isotropic:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint OOF.Property.Copy
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic;cyan_elasticity
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;cyan_elasticity').resize(372, 244)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;cyan_elasticity:cijkl:Chooser'), 'E and nu')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;cyan_elasticity:cijkl:E and nu:young').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;cyan_elasticity:cijkl:E and nu:young').set_text('0.5')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;cyan_elasticity:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;cyan_elasticity:cijkl:E and nu:poisson').set_text('0.3')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic;cyan_elasticity:gtk-ok').clicked()
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.cyan_elasticity
assert tests.selectedPropertyCheck('Mechanical:Elasticity:Isotropic:cyan_elasticity')
findWidget('A Simple Example:Next').clicked()
setComboBox(findWidget('OOF2:Materials Page:Pane:Material:MaterialList'), 'cyan-material')
checkpoint Materials page updated
checkpoint Materials page updated
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Add_property
assert tests.materialCheck('cyan-material', ['Mechanical:Elasticity:Isotropic:cyan_elasticity'])
assert tests.selectedMatlPropertyCheck('Mechanical:Elasticity:Isotropic:cyan_elasticity')
findWidget('OOF2:Materials Page:Pane:Material:RemoveProperty').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Remove_property
assert tests.selectedMatlPropertyCheck(None)
assert tests.materialCheck('cyan-material', [])
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Add_property
assert tests.materialCheck('cyan-material', ['Mechanical:Elasticity:Isotropic:cyan_elasticity'])
assert tests.selectedMatlPropertyCheck('Mechanical:Elasticity:Isotropic:cyan_elasticity')
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
checkpoint Materials page updated
checkpoint Materials page updated
widget=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget.window))
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Color
findWidget('Dialog-Copy property Color').resize(282, 72)
findWidget('Dialog-Copy property Color:new_name:Text').set_text('')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('y')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('ye')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('yel')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('yell')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('yello')
findWidget('Dialog-Copy property Color:new_name:Text').set_text('yellow')
findWidget('Dialog-Copy property Color:gtk-ok').clicked()
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((0,), open_all=False)
checkpoint Materials page updated
checkpoint OOF.Property.Copy
checkpoint_count("Materials page updated")
assert tests.selectedPropertyCheck('Color:yellow')
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Color;yellow
findWidget('Dialog-Parametrize Color;yellow').resize(248, 144)
setComboBox(findWidget('Dialog-Parametrize Color;yellow:color:Chooser'), 'RGBColor')
findWidget('Dialog-Parametrize Color;yellow').resize(257, 192)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 1.5873015873016e-02)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 4.7619047619048e-02)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 2.2222222222222e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 3.9682539682540e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 6.5079365079365e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 7.4603174603175e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 8.2539682539683e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 9.2063492063492e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 9.5238095238095e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 9.6825396825397e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Red:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 1.5873015873016e-02)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 3.1746031746032e-02)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 1.1111111111111e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 1.9047619047619e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 2.8571428571429e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 9.5238095238095e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 9.8412698412698e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 9.6825396825397e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 9.5238095238095e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 9.3650793650794e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 9.2063492063492e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 9.0476190476190e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 8.8888888888889e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 8.7301587301587e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 8.5714285714286e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 8.4126984126984e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 8.2539682539683e-01)
findWidget('Dialog-Parametrize Color;yellow:color:RGBColor:Green:slider').get_adjustment().set_value( 8.0952380952381e-01)
findWidget('Dialog-Parametrize Color;yellow:gtk-ok').clicked()

checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Property.Parametrize.Color.yellow
setComboBox(findWidget('OOF2:Materials Page:Pane:Material:MaterialList'), 'yellow-material')
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint_count("Materials page updated")
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Add_property

checkpoint_count("Materials page updated")
assert tests.materialCheck('yellow-material',  ['Mechanical:Elasticity:Isotropic:yellow_elasticity', 'Color:yellow'])
assert tests.selectedMatlPropertyCheck('Color:yellow')
findWidget('OOF2:Materials Page:Pane:Property:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Copy property Color;yellow
findWidget('Dialog-Copy property Color;yellow').resize(282, 72)
findWidget('Dialog-Copy property Color;yellow:new_name:Text').set_text('')
findWidget('Dialog-Copy property Color;yellow:new_name:Text').set_text('c')
findWidget('Dialog-Copy property Color;yellow:new_name:Text').set_text('cy')
findWidget('Dialog-Copy property Color;yellow:new_name:Text').set_text('cya')
findWidget('Dialog-Copy property Color;yellow:new_name:Text').set_text('cyan')
findWidget('Dialog-Copy property Color;yellow:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint OOF.Property.Copy
findWidget('OOF2:Materials Page:Pane:Property:Parametrize').clicked()
checkpoint toplevel widget mapped Dialog-Parametrize Color;cyan
findWidget('Dialog-Parametrize Color;cyan').resize(257, 192)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Blue:slider').get_adjustment().set_value( 2.8571428571429e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Blue:slider').get_adjustment().set_value( 4.6031746031746e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Blue:slider').get_adjustment().set_value( 7.4603174603175e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Blue:slider').get_adjustment().set_value( 9.0476190476190e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Blue:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 9.8412698412698e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 9.5238095238095e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 9.2063492063492e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 8.4126984126984e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 7.4603174603175e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 6.3492063492063e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 5.5555555555556e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 4.6031746031746e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 3.6507936507937e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 2.6984126984127e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 1.9047619047619e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 1.1111111111111e-01)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 6.3492063492063e-02)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 1.5873015873016e-02)
findWidget('Dialog-Parametrize Color;cyan:color:RGBColor:Red:slider').get_adjustment().set_value( 0.0000000000000e+00)
findWidget('Dialog-Parametrize Color;cyan:gtk-ok').clicked()

checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Property.Parametrize.Color.cyan
setComboBox(findWidget('OOF2:Materials Page:Pane:Material:MaterialList'), 'cyan-material')
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint_count("Materials page updated")
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Add_property

checkpoint_count("Materials page updated")
assert tests.materialCheck('cyan-material',  ['Mechanical:Elasticity:Isotropic:cyan_elasticity', 'Color:cyan'])
assert tests.selectedMatlPropertyCheck('Color:cyan')
findWidget('A Simple Example:Next').clicked()
setComboBox(findWidget('OOF2:Materials Page:Pane:Material:MaterialList'), 'yellow-material')
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint_count("Materials page updated")
findWidget('OOF2:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material yellow-material to pixels
findWidget('Dialog-Assign material yellow-material to pixels').resize(244, 108)
setComboBox(findWidget('Dialog-Assign material yellow-material to pixels:pixels'), 'yellow')
findWidget('Dialog-Assign material yellow-material to pixels:gtk-ok').clicked()

checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Assign
findWidget('A Simple Example:Next').clicked()
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:Graphics_1').activate()
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.2558139534884e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.5116279069767e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.7674418604651e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 5.0232558139535e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 7.5348837209302e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 8.7906976744186e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.0046511627907e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.1302325581395e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.2558139534884e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.3813953488372e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.5069767441860e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.6325581395349e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.7581395348837e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.8837209302326e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.0093023255814e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.1348837209302e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.2604651162791e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.3860465116279e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.5116279069767e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.6372093023256e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.1395348837209e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.5162790697674e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.8930232558140e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.0186046511628e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.1441860465116e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.2697674418605e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.3953488372093e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.5209302325581e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.6465116279070e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.7720930232558e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.8976744186047e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 5.0232558139535e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 5.1488372093023e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 5.2744186046512e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 5.4000000000000e+01)
findWidget('A Simple Example:Next').clicked()
findWidget('A Simple Example:Back').clicked()
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:New').activate()
checkpoint layereditor layerset changed
checkpoint toplevel widget mapped OOF2 Graphics Layer Editor
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.New
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
assert tests.chooserStateCheck('OOF2 Graphics Layer Editor:ObjectScroll:category', 'Nothing')
assert tests.chooserCheck('OOF2 Graphics Layer Editor:ObjectScroll:object:Nothing', ['Nobody'])
assert tests.layerEditorSensitivityCheck0()
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.2558139534884e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.5116279069767e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.7674418604651e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 6.2790697674419e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 7.5348837209302e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 8.7906976744186e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.0046511627907e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.1302325581395e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.2558139534884e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.3813953488372e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.5069767441860e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.7581395348837e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.8837209302326e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.0093023255814e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.1348837209302e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.2604651162791e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.3860465116279e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.5116279069767e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.6372093023256e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.7627906976744e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.8883720930233e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.1395348837209e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.5162790697674e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.6418604651163e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.7674418604651e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.8930232558140e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.1441860465116e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.2697674418605e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.3953488372093e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.5209302325581e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.6465116279070e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.7720930232558e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.8976744186047e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 5.0232558139535e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 5.1488372093023e+01)
findWidget('A Simple Example:Next').clicked()
findWidget('A Simple Example:Next').clicked()
findWidget('A Simple Example:Back').clicked()
findWidget('OOF2 Graphics Layer Editor:NewLayer').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.New
assert tests.listViewSelectedRowNo('OOF2 Graphics 1:Pane0:LayerScroll:LayerList') == None
assert tests.layerEditorSensitivityCheck0()
findWidget('A Simple Example:Back').clicked()
setComboBox(findWidget('OOF2 Graphics Layer Editor:ObjectScroll:category'), 'Microstructure')
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.DisplayedObject
assert tests.chooserCheck('OOF2 Graphics Layer Editor:ObjectScroll:object:Microstructure', ['cyallow.png', '<topmost>', '<top bitmap>'])
assert tests.chooserStateCheck('OOF2 Graphics Layer Editor:ObjectScroll:object:Microstructure', 'cyallow.png')
assert tests.layerEditorSensitivityCheck1()
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.2558139534884e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 8.7906976744186e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.0046511627907e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.2558139534884e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.6325581395349e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.8837209302326e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.1348837209302e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.2604651162791e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.3860465116279e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.5116279069767e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.6372093023256e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.7627906976744e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.0139534883721e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.3906976744186e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.5162790697674e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.7674418604651e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.8930232558140e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.0186046511628e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.1441860465116e+01)
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Microstructure cyallow.png
findWidget('Dialog-New Display Method for Microstructure cyallow.png').resize(381, 320)
findWidget('Dialog-New Display Method for Microstructure cyallow.png:gtk-ok').clicked()
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

assert tests.treeViewLength('OOF2 Graphics Layer Editor:DisplayMethods:ListScroll:List') == 1
assert tests.chooserCheck('OOF2 Graphics Layer Editor:DisplayMethods:ListScroll:List', ['Material'])
assert tests.layerEditorSensitivityCheck2()
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5263157894737e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.0526315789474e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.7684210526316e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.2842105263158e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.8000000000000e+01)
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '12')

checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Hide

findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '12')

checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Show

findWidget('A Simple Example:Next').clicked()
setComboBox(findWidget('OOF2:Materials Page:Pane:Material:MaterialList'), 'cyan-material')
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint_count("Materials page updated")
findWidget('OOF2:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material cyan-material to pixels
findWidget('Dialog-Assign material cyan-material to pixels').resize(244, 108)
setComboBox(findWidget('Dialog-Assign material cyan-material to pixels:pixels'), 'cyan')
findWidget('OOF2').resize(684, 350)
findWidget('Dialog-Assign material cyan-material to pixels:gtk-ok').clicked()

checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Material.Assign
findWidget('OOF2').resize(684, 350)
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
checkpoint skeleton page sensitized
checkpoint_count("skeleton page sensitized")
assert tests.skeletonPageSensitivityCheck0()
findWidget('OOF2').resize(684, 434)
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().unselect_all()
checkpoint OOF.Graphics_1.Layer.Deselect
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton selection page selection sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint mesh bdy page updated
checkpoint Field page sensitized


checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized

checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint skeleton selection page grouplist
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton page sensitized



assert tests.skeletonPageSensitivityCheck1()
findWidget('A Simple Example:Next').clicked()
setComboBox(findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Chooser'), 'Snap Nodes')
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 3.0158730158730e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 3.3333333333333e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 6.3492063492063e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 7.4603174603175e-01)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 7.9365079365079e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 8.2539682539683e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 9.0476190476190e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 9.3650793650794e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 9.5238095238095e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 9.6825396825397e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 9.8412698412698e-01)
findWidget('OOF2:Skeleton Page:Pane:Modification:Method:Snap Nodes:criterion:Average Energy:alpha:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('OOF2:Skeleton Page:Pane:Modification:OK').clicked()
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint contourmap info updated for Graphics_1
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page selection sensitized

checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Skeleton.Modify
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
assert tests.skeletonPageSensitivityCheck2()
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.1875000000000e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 4.7500000000000e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 8.3125000000000e+00)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.3062500000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 1.7812500000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.1375000000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.4937500000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.6125000000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.7312500000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 2.8500000000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.0875000000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.3250000000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.4437500000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.5625000000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.6812500000000e+01)
findWidget('A Simple Example:TutorialScroll').get_vadjustment().set_value( 3.8000000000000e+01)
findWidget('A Simple Example:Next').clicked()
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
assert tests.meshPageSensitivityCheck0()
findWidget('OOF2').resize(684, 482)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint mesh bdy page updated
checkpoint mesh bdy page updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Mesh.New
assert tests.meshPageSensitivityCheck1()
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
assert tests.fieldPageSensitivityCheck0()
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Subproblem.Field.Define
assert tests.fieldPageSensitivityCheck1()
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement in-plane').clicked()
checkpoint Field page sensitized
checkpoint OOF.Mesh.Field.In_Plane
findWidget('A Simple Example:Next').clicked()
# findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
assert tests.bcPageSensitivityCheck0()
findWidget('A Simple Example:Next').clicked()
findWidget('A Simple Example:Next').clicked()
findWidget('A Simple Example').resize(498, 402)
findWidget('A Simple Example').resize(497, 416)
findWidget('A Simple Example').resize(496, 438)
findWidget('A Simple Example').resize(495, 455)
findWidget('A Simple Example').resize(495, 469)
findWidget('A Simple Example').resize(495, 483)
findWidget('A Simple Example').resize(495, 506)
findWidget('A Simple Example').resize(495, 512)
findWidget('A Simple Example').resize(495, 517)
findWidget('A Simple Example').resize(495, 530)
findWidget('A Simple Example').resize(495, 535)
findWidget('A Simple Example').resize(495, 537)
findWidget('A Simple Example').resize(495, 539)
findWidget('A Simple Example').resize(495, 543)
findWidget('A Simple Example').resize(495, 544)
findWidget('A Simple Example').resize(495, 546)
findWidget('A Simple Example').resize(495, 549)
findWidget('A Simple Example').resize(495, 550)
findWidget('A Simple Example').resize(495, 551)
findWidget('A Simple Example').resize(495, 553)
findWidget('A Simple Example').resize(495, 554)
findWidget('A Simple Example').resize(495, 556)
findWidget('A Simple Example').resize(495, 557)
findWidget('A Simple Example').resize(495, 558)
findWidget('A Simple Example').resize(495, 559)
findWidget('A Simple Example').resize(495, 561)
findWidget('A Simple Example').resize(495, 562)
findWidget('A Simple Example').resize(495, 563)
findWidget('A Simple Example').resize(495, 564)
findWidget('A Simple Example').resize(495, 565)
findWidget('A Simple Example').resize(495, 566)
findWidget('A Simple Example').resize(495, 567)
findWidget('A Simple Example').resize(495, 568)
findWidget('A Simple Example').resize(495, 569)
findWidget('A Simple Example').resize(495, 570)
findWidget('A Simple Example').resize(495, 572)
findWidget('A Simple Example').resize(495, 573)
findWidget('A Simple Example').resize(495, 574)
findWidget('A Simple Example').resize(495, 576)
findWidget('A Simple Example').resize(495, 582)
findWidget('A Simple Example').resize(495, 583)
findWidget('A Simple Example').resize(495, 585)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 300)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'left')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(792, 200)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList').get_selection().select_path((0,))
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.bcPageSensitivityCheck1()
assert tests.treeViewColCheck('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList', 0, ['bc'])
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 300)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:field_component'), 'y')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:eqn_component'), 'y')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'bottom')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.treeViewColCheck('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList', 0, ['bc', 'bc<2>'])
assert tests.listViewSelectedRowNo('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList') == 1
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 300)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:field_component'), 'x')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:eqn_component'), 'x')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Constant Profile:value').set_text('10.0')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'right')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.treeViewColCheck('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList', 0, ['bc', 'bc<2>', 'bc<3>'])
assert tests.listViewSelectedRowNo('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList') == 2
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()

findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((0,))
findWidget('OOF2:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(423, 212)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF2:Solver Page:end').set_text('0')
findWidget('OOF2:Solver Page:solve').clicked()
findWidget('OOF2:Solver Page:end').set_text('')

checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Mesh.Solve

findWidget('A Simple Example:Next').clicked()
findWidget('A Simple Example:Next').clicked()
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.6000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.5000000000000e+01)
findWidget('OOF2 Graphics 1').resize(799, 404)
findWidget('OOF2 Graphics 1').resize(799, 416)
findWidget('OOF2 Graphics 1').resize(799, 422)
findWidget('OOF2 Graphics 1').resize(799, 423)
findWidget('OOF2 Graphics 1').resize(799, 424)
findWidget('OOF2 Graphics 1').resize(800, 425)
findWidget('OOF2 Graphics 1').resize(800, 426)
findWidget('OOF2 Graphics 1').resize(800, 427)
findWidget('OOF2 Graphics 1').resize(800, 433)
findWidget('OOF2 Graphics 1').resize(800, 441)
findWidget('OOF2 Graphics 1').resize(800, 444)
findWidget('OOF2 Graphics 1').resize(800, 445)
findWidget('OOF2 Graphics 1').resize(800, 446)
findWidget('OOF2 Graphics 1').resize(800, 447)
findWidget('OOF2 Graphics 1').resize(800, 448)
widget_0 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_0.event(event(gtk.gdk.BUTTON_PRESS,x= 3.6600000000000e+02,y= 3.0000000000000e+00,button=1,state=0,window=widget_0.window))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
checkpoint OOF.Graphics_1.Layer.Select
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.1000000000000e+01)
widget_1 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_1.event(event(gtk.gdk.BUTTON_PRESS,x= 3.6700000000000e+02,y= 1.0000000000000e+01,button=1,state=0,window=widget_1.window))
widget_2 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_2.event(event(gtk.gdk.BUTTON_PRESS,x= 3.6700000000000e+02,y= 1.0000000000000e+01,button=1,state=0,window=widget_2.window))
widget_3 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_3.event(event(gtk.gdk.BUTTON_PRESS,x= 3.6700000000000e+02,y= 1.0000000000000e+01,button=1,state=0,window=widget_3.window))
tree=findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(4)
tree.row_activated((10,), column)
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint layereditor layerset changed
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Mesh mesh
findWidget('Dialog-New Display Method for Mesh mesh').resize(416, 247)
setComboBox(findWidget('Dialog-New Display Method for Mesh mesh:method:Chooser'), 'Filled Contour')
findWidget('Dialog-New Display Method for Mesh mesh').resize(431, 353)
setComboBox(findWidget('Dialog-New Display Method for Mesh mesh:method:Filled Contour:where:where_0'), 'actual')
findWidget('Dialog-New Display Method for Mesh mesh:gtk-ok').clicked()
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
checkpoint layereditor layerset changed
findMenu(findWidget('OOF2 Graphics Layer Editor:MenuBar'), 'File:Quit').activate()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(325, 91)
widget_4=findWidget('Questioner')
handled_0=widget_4.event(event(gtk.gdk.DELETE,window=widget_4.window))
postpone if not handled_0: widget_4.destroy()
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(325, 91)
findWidget('Questioner:gtk-delete').clicked()
