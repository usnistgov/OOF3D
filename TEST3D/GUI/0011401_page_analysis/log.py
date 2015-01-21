# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.7 $
# $Author: fyc $
# $Date: 2014/07/18 19:54:54 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing the Named Analyses section in the Analysis Page

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 67)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/two_walls.mesh')
findWidget('Dialog-Data:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
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
checkpoint microstructure page sensitized
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
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
checkpoint Solver page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint pinnodes page sensitized
checkpoint pinnodes page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint toplevel widget mapped OOF3D Activity Viewer
checkpoint boundary page updated
findWidget('OOF3D Activity Viewer').resize(400, 300)
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.File.Load.Data
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Analysis')
checkpoint page installed Analysis
findWidget('OOF3D:Analysis Page:bottom').set_position(287)
findWidget('OOF3D').resize(787, 350)
findWidget('OOF3D:Analysis Page:top').set_position(412)
findWidget('OOF3D:Analysis Page:bottom').set_position(412)
widget_0 = findWidget('OOF3D:Analysis Page:Name:Operations')
widget_0.event(event(gtk.gdk.BUTTON_PRESS,x= 1.6700000000000e+02,y= 1.6000000000000e+01,button=1,state=16,window=widget_0.window))
checkpoint toplevel widget mapped NamedOpsMenu
findWidget('NamedOpsMenu').deactivate()
findMenu(findWidget('NamedOpsMenu'), 'Create').activate()
checkpoint toplevel widget mapped Dialog-Name an analysis operation
findWidget('Dialog-Name an analysis operation').resize(246, 67)
findWidget('Dialog-Name an analysis operation:gtk-ok').clicked()
checkpoint OOF.Named_Analysis.Create
findWidget('OOF3D Messages 1').resize(763, 200)
setComboBox(findWidget('OOF3D:Analysis Page:Name:Retrieve'), '')
assert tests.SetAnalysisCheck(('','analysis'))
assert tests.SetAnalysisSelect('')
setComboBox(findWidget('OOF3D:Analysis Page:Name:Retrieve'), 'analysis')
assert tests.SetAnalysisCheck(('','analysis'))
assert tests.SetAnalysisSelect('analysis')
checkpoint retrieved named analysis
checkpoint OOF.Named_Analysis.RetrieveNamedAnalysis
widget_1 = findWidget('OOF3D:Analysis Page:Name:Operations')
widget_1.event(event(gtk.gdk.BUTTON_PRESS,x= 8.3000000000000e+01,y= 1.5000000000000e+01,button=1,state=16,window=widget_1.window))
checkpoint toplevel widget mapped NamedOpsMenu
findWidget('NamedOpsMenu').deactivate()
findMenu(findWidget('NamedOpsMenu'), 'Create').activate()
checkpoint toplevel widget mapped Dialog-Name an analysis operation
findWidget('Dialog-Name an analysis operation').resize(246, 67)
findWidget('Dialog-Name an analysis operation:name:Auto').clicked()
findWidget('Dialog-Name an analysis operation:name:Text').set_text('named_analysis')
findWidget('Dialog-Name an analysis operation:gtk-ok').clicked()
checkpoint OOF.Named_Analysis.Create
assert tests.SetAnalysisCheck(('','analysis','named_analysis'))
assert tests.SetAnalysisSelect('analysis')
assert tests.SetDestinationSelect('<Message Window>')
findWidget('OOF3D:Analysis Page:Destination:Rewind').clicked()
findWidget('OOF3D:Analysis Page:Destination:Clear').clicked()
findWidget('OOF3D:Analysis Page:Destination:New').clicked()
checkpoint toplevel widget mapped Dialog-Add a data destination
findWidget('Dialog-Add a data destination').resize(190, 95)
findWidget('Dialog-Add a data destination:filename').set_text('datadestination.dat')
findWidget('Dialog-Add a data destination:gtk-ok').clicked()
setComboBox(findWidget('OOF3D:Analysis Page:Destination:Chooser'), '<Message Window>')
assert tests.SetDestinationCheck(('<Message Window>','datadestination.dat'))
assert tests.SetDestinationSelect('<Message Window>')
setComboBox(findWidget('OOF3D:Analysis Page:Destination:Chooser'), 'datadestination.dat')
assert tests.SetDestinationCheck(('<Message Window>','datadestination.dat'))
assert tests.SetDestinationSelect('datadestination.dat')
findWidget('OOF3D:Analysis Page:Destination:Rewind').clicked()
checkpoint OOF.Mesh.Analyze.Rewind
findWidget('OOF3D:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Direct_Output
assert tests.filediff('datadestination.dat')
findWidget('OOF3D:Analysis Page:Destination:Clear').clicked()
widget_2 = findWidget('OOF3D:Analysis Page:Name:Operations')
widget_2.event(event(gtk.gdk.BUTTON_PRESS,x= 1.5900000000000e+02,y= 2.1000000000000e+01,button=1,state=16,window=widget_2.window))
checkpoint toplevel widget mapped NamedOpsMenu
findWidget('NamedOpsMenu').deactivate()
findMenu(findWidget('NamedOpsMenu'), 'Save').activate()
checkpoint toplevel widget mapped Dialog-Save Analysis Definitions
findWidget('Dialog-Save Analysis Definitions').resize(190, 168)
findWidget('Dialog-Save Analysis Definitions:filename').set_text('savedanalysis.dat')
findWidget('Dialog-Save Analysis Definitions').resize(283, 227)
findWidget('Dialog-Save Analysis Definitions:gtk-ok').clicked()
checkpoint OOF.Named_Analysis.SaveAnalysisDefs
assert tests.SetDestinationSelect('<Message Window>')
assert tests.filediff('savedanalysis.dat')
widget_3 = findWidget('OOF3D:Analysis Page:Name:Operations')
widget_3.event(event(gtk.gdk.BUTTON_PRESS,x= 1.7500000000000e+02,y= 1.2000000000000e+01,button=1,state=16,window=widget_3.window))
checkpoint toplevel widget mapped NamedOpsMenu
findWidget('NamedOpsMenu').deactivate()
findMenu(findWidget('NamedOpsMenu'), 'Delete').activate()
checkpoint toplevel widget mapped Dialog-Delete a named analysis
findWidget('Dialog-Delete a named analysis').resize(218, 73)
setComboBox(findWidget('Dialog-Delete a named analysis:name'), 'analysis')
findWidget('Dialog-Delete a named analysis:gtk-ok').clicked()
checkpoint OOF.Named_Analysis.Delete
findWidget('OOF3D:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Direct_Output
findWidget('NamedOpsMenu').deactivate()
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('analysispage.log')
findWidget('Dialog-Python_Log').resize(198, 92)
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('analysispage.log')
widget_1=findWidget('OOF3D')
handled_0=widget_1.event(event(gtk.gdk.DELETE,window=widget_1.window))