# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

OBSOLETE


class MouseHandler(object):
    def acceptEvent(self, eventtype):
        # eventtype is either 'up', 'down', or 'move'.  Return True if it
        # can be handled.
        # Locked only the three events 
        if eventtype == 'up' or eventtype == 'down' or eventtype == 'move':
	  return True
	else:
	  return False
    def up(self, x, y, button, shift, ctrl):
        pass
    def down(self, x, y, button, shift, ctrl):
        pass
    def move(self, x, y, button, shift, ctrl):
        pass

class NullMouseHandler(MouseHandler):
    def acceptEvent(self, eventtype):
        return False

    
nullHandler = NullMouseHandler()            # doesn't do anything
