# -*- python -*-
# $RCSfile: toolbox.py,v $
# $Revision: 1.14.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:57 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Toolboxes for the graphics window and its ghost.

# A Toolbox represents a set of operations that can be performed in a
# graphics window.  Only one toolbox is active at any time.  The
# non-graphical toolboxes derived from the Toolbox class perform the
# actions (to the extent that they make sense in a non-graphical
# environment).  They have graphical counterparts derived from
# common.IO.GUI.toolboxGUI.GfxToolbox.  When in graphics mode, the
# makeGUI function must be overloaded to return a GfxToolbox instance.

# Toolbox subclasses must have an 'ordering' attribute, which is used
# to determine their placement in the GUI.  Each subclass must make
# itself known at *import* time by calling
# registerToolboxClass(subclass, ordering).

# Toolbox subclasses must have 'tip' and 'discussion' strings, which
# will be inserted into the documentation page for the
# OOF.Graphics_n.Toolbox.<ToolboxName> menu.  The discussion can be an
# xmlmenudump.DiscussionFile object, if necessary.

from ooflib.SWIG.common import switchboard
from ooflib.common import debug

class Toolbox:
    def __init__(self, name, gfxwindow):
        self._name = name
        self._gfxwindow = gfxwindow      # GhostGfxWindow or GfxWindow
    def name(self):
        return self._name
    def gfxwindow(self):
        return self._gfxwindow
    def makeGUI(self):                 
        return None # return an object with a gtk attribute
    def makeMenu(self, menu):
        pass                            # add subitems to menu
    def close(self):
        # Called when the graphics window is closing
        pass
    def __cmp__(self, other):           # used for sorting in ui
        return cmp(self.ordering, other.ordering)
    def __hash__(self):
        ## required because toolboxes are sometimes used as
        ## switchboard messages, which means they're stored in the
        ## switchboard's dictionary, and because objects with __cmp__
        ## methods also need __hash__ methods if they're to be used as
        ## dictionary keys.
        return hash(self._name) ^ hash(self._gfxwindow)

toolboxClasses = []

def registerToolboxClass(tbclass, ordering):
    global toolboxClasses
    tbclass.ordering = ordering
    toolboxClasses.append(tbclass)
    switchboard.notify('new toolbox class', tbclass)
        

