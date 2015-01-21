# -*- python -*-
# $RCSfile: mousehandler.py,v $
# $Revision: 1.6.10.2 $
# $Author: fyc $
# $Date: 2013/06/17 18:01:50 $

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


class MouseHandler:
    def acceptEvent(self, eventtype):
        # eventtype is either 'up', 'down', or 'move'.  Return True if it
        # can be handled.
        # Locked only the three events 
        if eventtype == 'up' or eventtype == 'down' or eventtype == 'move':
	  return True
	else:
	  return False
    def up(self, x, y, shift, ctrl):
        pass
    def down(self, x, y, shift, ctrl):
        pass
    def move(self, x, y, shift, ctrl):
        pass

    
nullHandler = MouseHandler()            # doesn't do anything
