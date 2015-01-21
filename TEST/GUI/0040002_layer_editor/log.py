checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
# This test is really very basic -- just loads a mesh, opens a
# graphics window, and changes the display properties of the
# cross-section set.  The test is that the OK button should be
# sensitized in the default case.  The bug was that the who widgets
# were returning "None" in the proxy case, instead of the proxy
# string, which was causing confusion down the line in this case.
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
findWidget('OOF2 Messages 1').resize(630, 200)
findWidget('OOF2').resize(550, 350)
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
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
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.File.LoadStartUp.Data
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
findWidget('OOF2 Graphics 1:Pane0').set_position(280)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1').resize(800, 803)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(317)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Mesh Cross Section')
checkpoint Graphics_1 Mesh Cross Section sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(317)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(716)
findWidget('OOF2 Graphics 1:Pane0').set_position(317)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 9.4411764705882e+00,y=-3.3494117647059e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.9588235294118e+00,y=-3.3235294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.0994117647059e+01,y=-3.2200000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3064705882353e+01,y=-3.0647058823529e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.5135294117647e+01,y=-2.9611764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7723529411765e+01,y=-2.8576470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0311764705882e+01,y=-2.7023529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2900000000000e+01,y=-2.5988235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.5488235294118e+01,y=-2.4952941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.8076470588235e+01,y=-2.3917647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.0147058823529e+01,y=-2.2882352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2217647058824e+01,y=-2.2364705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.4288235294118e+01,y=-2.1329411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.5841176470588e+01,y=-2.0811764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6358823529412e+01,y=-2.0552941176471e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.6876470588235e+01,y=-2.0294117647059e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.7394117647059e+01,y=-2.0035294117647e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.7652941176471e+01,y=-1.9776470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.7911764705882e+01,y=-1.9517647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8170588235294e+01,y=-1.9517647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8429411764706e+01,y=-1.9258823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8688235294118e+01,y=-1.9000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.8947058823529e+01,y=-1.8741176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.9205882352941e+01,y=-1.8741176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0241176470588e+01,y=-1.7705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.0758823529412e+01,y=-1.7705882352941e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.1017647058824e+01,y=-1.7188235294118e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.1535294117647e+01,y=-1.6929411764706e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2052941176471e+01,y=-1.6670588235294e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2570588235294e+01,y=-1.6411764705882e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4123529411765e+01,y=-1.5376470588235e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4641176470588e+01,y=-1.5117647058824e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5158823529412e+01,y=-1.4858823529412e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5417647058824e+01,y=-1.4600000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5676470588235e+01,y=-1.4600000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5935294117647e+01,y=-1.4341176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6194117647059e+01,y=-1.4341176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6711764705882e+01,y=-1.4341176470588e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.6970588235294e+01,y=-1.4082352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7488235294118e+01,y=-1.4082352941176e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.7747058823529e+01,y=-1.3823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8005882352941e+01,y=-1.3823529411765e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8005882352941e+01,y=-1.3564705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8264705882353e+01,y=-1.3564705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8264705882353e+01,y=-1.3564705882353e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Messages 1').resize(639, 200)
checkpoint Graphics_1 Mesh Cross Section sensitized
checkpoint OOF.Mesh.Cross_Section.New
findWidget('OOF2 Graphics 1:Pane0').set_position(317)
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Long_Layer_Names').activate()
checkpoint OOF.Graphics_1.Settings.Long_Layer_Names
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:List_All_Layers').activate()
checkpoint Graphics_1 Mesh Cross Section sensitized
checkpoint OOF.Graphics_1.Settings.List_All_Layers
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((9,))
checkpoint OOF.Graphics_1.Layer.Select
tree=findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(3)
tree.row_activated((9,), column)
checkpoint layereditor layerset changed
checkpoint toplevel widget mapped OOF2 Graphics Layer Editor
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Edit
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:Edit').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Mesh <contourable>
findWidget('Dialog-New Display Method for Mesh <contourable>').resize(403, 215)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:color:Gray:Gray:slider').get_adjustment().set_value( 5.0793650793651e-01)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:color:Gray:Gray:slider').get_adjustment().set_value( 5.5555555555556e-01)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:color:Gray:Gray:slider').get_adjustment().set_value( 5.8730158730159e-01)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:color:Gray:Gray:slider').get_adjustment().set_value( 7.1428571428571e-01)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:color:Gray:Gray:slider').get_adjustment().set_value( 7.6190476190476e-01)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:color:Gray:Gray:slider').get_adjustment().set_value( 8.8888888888889e-01)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:color:Gray:Gray:slider').get_adjustment().set_value( 1.0000000000000e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 1.0526315789474e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 1.1578947368421e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 1.2631578947368e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 1.3684210526316e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 1.5789473684211e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 1.6842105263158e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 1.8947368421053e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.0000000000000e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.1052631578947e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.2105263157895e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.3157894736842e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.4210526315789e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.5263157894737e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.6315789473684e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.7368421052632e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.8421052631579e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 2.9473684210526e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 3.0526315789474e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 3.1578947368421e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 3.2631578947368e+00)
findWidget('Dialog-New Display Method for Mesh <contourable>:method:Cross Section:linewidth:slider').get_adjustment().set_value( 3.3684210526316e+00)
#
# Check OK button -- should be sensitized.
assert tests.is_sensitive('Dialog-New Display Method for Mesh <contourable>:gtk-ok')
#
findWidget('Dialog-New Display Method for Mesh <contourable>:gtk-ok').clicked()
checkpoint layer editor updated
checkpoint Graphics_1 Mesh Cross Section sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Mesh Cross Section sensitized
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Replace_Method
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
findWidget('OOF2 Graphics 1:Pane0').set_position(317)
widget_0=findWidget('OOF2')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
checkpoint toplevel widget mapped Questioner
postpone if not handled_0: widget_0.destroy()
findWidget('Questioner').resize(358, 93)
findWidget('Questioner:gtk-delete').clicked()
checkpoint OOF.ActivityViewer.File.Close
checkpoint OOF.Graphics_1.File.Close
