# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.common import registeredclass

# Base class for generic methods for selecting objects in the graphics
# window.  Subclasses should have registries.  Registrations should
# have a 'whoclasses' member that is a list or tuple of the names of the
# WhoClasses that the selector operates on.

class GenericSelectionMethod(registeredclass.RegisteredClass):
    def getSource(self, gfxwindow):
        return gfxwindow.topwho(*self.registration.whoclasses)
    def getSourceName(self, gfxwindow):
        src = self.getSource(gfxwindow)
        if src is not None:
            return src.path()
    def select(self, context, selection):
        raise ooferror.ErrPyProgrammingError(
            self.__class__.__name__, "has no 'select' method!")


class GenericSelectionModifier(registeredclass.RegisteredClass):
    def select(self, context, selection):
        raise ooferror.ErrPyProgrammingError(
            self.__class__.__name__, "has no 'select' method!")
