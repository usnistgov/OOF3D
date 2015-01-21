# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:14:16 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# Despite its name, the bug_activity_viewer test does not view the
# activity of bugs, but checks for the presence of an old activity
# viewer bug, involving incorrect order in the destruction of windows
# progress bars.  This test simply starts a progress bar and closes
# the activity viewer window before the progress bar is complete.  If
# the test runs to the end without raising an exception or crashing,
# it's successful.

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
findWidget('OOF2 Messages 1').resize(455, 200)
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
checkpoint microstructure page sensitized
checkpoint meshable button set
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
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(593, 350)
findWidget('OOF2:Image Page:Pane').set_position(380)
findWidget('OOF2:Image Page:Group').clicked()
checkpoint toplevel widget mapped Dialog-AutoGroup
findWidget('Dialog-AutoGroup').resize(211, 72)
findWidget('Dialog-AutoGroup:gtk-ok').clicked()
checkpoint toplevel widget mapped OOF2 Activity Viewer
findWidget('OOF2 Activity Viewer').resize(400, 300)
widget_0=findWidget('OOF2 Activity Viewer')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
checkpoint OOF.ActivityViewer.File.Close
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint OOF.Image.AutoGroup
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(358, 94)
findWidget('Questioner:gtk-delete').clicked()
