# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# A GfxWindow always has a current MouseHandler, which knows what to
# do with mouse events on the canvas.  The window's toolboxes can
# install new MouseHandlers.  The base class defined here does
# nothing.

## TODO: This is obsolete but still used.  Replace all occurences with
## common.IO.mousehandler

class MouseHandler(object):
    def acceptEvent(self, eventtype):
        # eventtype is either 'up', 'down', or 'move'.  Return True if it
        # can be handled.
        # Locked only the three events 
        if eventtype == 'up' or eventtype == 'down' or eventtype == 'move':
	  return True
	else:
	  return False
    def up(self, x, y, buttons):
        pass
    def down(self, x, y, buttons):
        pass
    def move(self, x, y, buttons):
        pass

    
nullHandler = MouseHandler()            # doesn't do anything

# Hack to tide us over until this file is removed.
from ooflib.common.IO.mousehandler import MouseButtons
