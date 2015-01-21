# -*- python -*-
# $RCSfile: pixelgroupparam.py,v $
# $Revision: 1.24.10.1 $
# $Author: langer $
# $Date: 2011/10/17 21:38:24 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
import types

# Parameter subclass for choosing a PixelGroup in a Microstructure

class PixelGroupParameter(parameter.StringParameter):
    def valueDesc(self):
        return "The name of a PixelGroup."

# Parameter subclass for choosing either a PixelGroup, every pixel, or
# the currently selected pixels.

class PixelAggregateParameter(placeholder.PlaceHolderParameter):
    types = (types.StringType, placeholder.selection, placeholder.every)

    def valueDesc(self):
        return "The name of a PixelGroup, or <link linkend='Object-Placeholder'><constant>every</constant></link> or <link linkend='Object-Placeholder'><constant>selected</constant></link>."

#Interface branch
class PixelGroupInterfaceParameter(parameter.StringParameter):
    def valueDesc(self):
        return "The name of a PixelGroup or &lt;No pixelgroup&gt;."
