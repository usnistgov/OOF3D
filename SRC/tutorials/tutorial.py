# -*- python -*-
# $RCSfile: tutorial.py,v $
# $Revision: 1.12.18.4 $
# $Author: langer $
# $Date: 2014/09/27 22:34:45 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

## TODO 3.1: Print tutorials

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import utils

from ooflib.common.IO import oofmenu
from ooflib.common.IO import mainmenu

allTutorials = {}
        
tutorialMenu = mainmenu.OOF.Help.addItem(
    oofmenu.OOFMenuItem('Tutorials', gui_only=1, no_log=1, ordering=-10))

def start_tutorial(tutorial, progress): # redefined in GUI mode
    pass

def startTutorial(menuitem):           
    start_tutorial(menuitem.data, 0)

class TutorialClass:
    def __init__(self, subject, ordering, lessons):
        self.subject = subject
        self.lessons = lessons
        self.ordering = ordering
        menuitem = tutorialMenu.addItem(
            oofmenu.OOFMenuItem(utils.space2underscore(subject),
                                ordering=ordering,
                                gui_callback=startTutorial,
                                threadable=oofmenu.UNTHREADABLE))
        menuitem.data = self
        allTutorials[subject] = self
        
    def getTutorId(self):
        return self.subject

class TutoringItem:
    def __init__(self, subject=None, comments=None, signal=None, done=0):
        self.subject = subject
        self.comments = comments
        self.signal = signal
        self.done = done

    def activate(self):
        if self.signal:
            self.switchboardCB = switchboard.requestCallback(self.signal,
                                                             self.signalCB)

    def deactivate(self):
        if self.signal:
            switchboard.removeCallback(self.switchboardCB)
            
    def signalCB(self, *args, **kwargs):
        switchboard.notify("task finished")
