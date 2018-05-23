# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# See NOTES/selection_machinery.txt

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import toolbox

# Base class for selection toolboxes.

# Selections are made to Selection objects that live inside some
# source object.  For example, the pixel selection lives inside a
# Microstructure.  Derived classes must provide a getSelectionSource()
# method that returns the Who object that contains the selection
# (probably a Microstructure or Skeleton).

class GenericSelectToolbox(toolbox.Toolbox):
    def __init__(self, name, method, menu, gfxwindow,
                 **extrakwargs):
        # Arguments:
        #
        # "name" is the menu tree entry, as well as the string that
        # will appear on the notebook tab in the GUI window.
        #
        # "method" is the base of a registered class hierarchy of
        # selection methods, derived from GenericSelectionMethod.
        #
        # menu is an OOFMenu containing 'Select', 'Undo', 'Redo', etc.
        #
        # extrakwargs are passed to the getSelectionContext() function
        # to retrieve the Who object of the current selection. For
        # example, the Skeleton selection toolboxes are defined with
        # an extra "mode" argument that distinguishes element
        # selections from node selections.
        
        toolbox.Toolbox.__init__(self, name, gfxwindow)
        self.method = method
        self.menu = menu
        self.menuitem = menu.Select

        self.extrakwargs = extrakwargs

        # TODO: Is this still needed?  Do subclasses use it?
        self.sb_callbacks = []

    def close(self):
        for s in self.sb_callbacks:
            switchboard.removeCallback(s)

    def getSourceName(self):
        source = self.getSelectionSource()
        if source is not None:
            return source.path()

    def getSelection(self):
        # This returns the object that holds the current selection.
        source = self.getSelectionSource()
        if source is not None:
            return source.getSelectionContext(**self.extrakwargs)

    def emptyMessage(self):
        # Called to get a string to display in the GUI when there's
        # nothing to make a selection from.  Redefined in subclasses
        # if more clarity is needed.
        return "No source!"
