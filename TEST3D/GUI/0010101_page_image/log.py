# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.3 $
# $Author: fyc $
# $Date: 2014/04/30 21:07:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

#Check that the "Load" button on the Image page is sensitized correctly.

import tests

findWidget('OOF3D').resize(550, 350)
findWidget('OOF3D:Navigation:Next').clicked()
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Navigation:Next').clicked()
checkpoint page installed Image
findWidget('OOF3D').resize(601, 350)
findWidget('OOF3D:Image Page:Pane').set_position(395)
assert tests.loadSensitive(0)
findWidget('OOF3D:Navigation:Prev').clicked()
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(246)
findWidget('OOF3D:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(315, 199)
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(174)
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
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Microstructure.New
findWidget('OOF3D:Navigation:Next').clicked()
checkpoint page installed Image
assert tests.loadSensitive(1)
findMenu(findWidget('OOF3D:MenuBar'), 'File:Quit').activate()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(359, 91)
findWidget('Questioner:gtk-delete').clicked()
