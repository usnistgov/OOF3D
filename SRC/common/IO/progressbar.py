# -*- python -*-
# $RCSfile: progressbar.py,v $
# $Revision: 1.2.2.4 $
# $Author: langer $
# $Date: 2014/12/02 21:52:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import progress
from ooflib.common import debug

_suppressBars = False

class ProgressBar(object):
    def __init__(self, progress):
        self.progress = progress # a Progress object
    def halted(self):
        # A progress object has been "halted" if it's been started and
        # stopped.  If it's already been destroyed, it's assumed to
        # have been halted.
        return not self.progress or (self.progress.started() and
                                     (self.progress.finished() or
                                      self.progress.stopped()))

class TextProgressBar(ProgressBar):
    def __init__(self, progress):
        ProgressBar.__init__(self, progress)
        self.total_bar = " "
        self.name = progress.name()
    def bar(self):
        if _suppressBars:
            return ""
        msg = self.progress.message()
        return "[%s] %s: %s" % (self.buildBar(), self.name, msg)

class DefiniteTextProgressBar(TextProgressBar):
    def buildBar(self):
        return "%3d%%" % int(100.*self.progress.getFraction())
        
def _makeDefTextBar(progobj):
    return DefiniteTextProgressBar(progobj)

progress.DefiniteProgressPtr.makeTextBar = _makeDefTextBar  

class IndefiniteTextProgressBar(TextProgressBar):
    def __init__(self, progress):
        TextProgressBar.__init__(self, progress)
        self.lastcount = None
        self.bartext = None
        self.counter = 0

    chars = r"-\|/"
    def buildBar(self):
        count = self.progress.pulsecount()
        if count != self.lastcount:
            self.lastcount = count
            self.counter = (self.counter + 1) % len(self.chars)
            self.bartext = self.chars[self.counter]
        return self.bartext

def _makeIndefTextBar(progobj):
    return IndefiniteTextProgressBar(progobj)

progress.IndefiniteProgressPtr.makeTextBar = _makeIndefTextBar

def suppressProgressBars():
    global _suppressBars
    _suppressBars = True


###########

## TODO MAYBE: If users want to write scripts with loops that are
## interruptible via the ActivityViewer window, they can't use the
## usual Python "for" loops.  We could add machinery to let them do
## this:
##   for x in finiteProgressBarLoop(xmax):
##       etc
## or
##   while infiniteProgressBarLoop():
##       etc
## or something like that.  This will be nontrivial because the
## current progress bars only work when invoked from OOFMenuItem
## callbacks.
