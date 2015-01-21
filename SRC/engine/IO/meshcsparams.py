# -*- python -*-
# $RCSfile: meshcsparams.py,v $
# $Revision: 1.6.10.1 $
# $Author: langer $
# $Date: 2011/10/17 21:38:42 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import ooferror
from ooflib.common.IO import placeholder
from ooflib.common.IO import parameter

# Special parameters for cross-sections.  There are two of them, one
# for a set of cross-sections, and one for a particular cross section
# name.  The former is used by the MeshCrossSectionDisplay, and the
# latter by the CrossSectionOutput object.

# Special parameter -- can either be a list of strings, or the special
# value, "<selection>".
class MeshCrossSectionSetParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if x==placeholder.selection:
            return # Success.
        parameter.ListOfStringsParameter.checker(self, x)
    def binaryRepr(self, datafile, value):
        raise ooferror.ErrPyProgrammingError(
            "binaryRepr not implemented for MessCrossSectionParameter.")
    def binaryRead(self, parser):
        raise ooferror.ErrPyProgrammingError(
            "binaryRead not implemented for MessCrossSectionParameter.")
    def valueDesc(self):
        return "The name of a Mesh cross section."


# Special parameter class for a single mesh cross section.
# Principally defined so that a special widget can exist.
# Used by the CrossSectionOuput class.
class MeshCrossSectionParameter(parameter.StringParameter):
    pass
