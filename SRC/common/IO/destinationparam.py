# -*- python -*-
# $RCSfile: destinationparam.py,v $
# $Revision: 1.11.2.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common.IO import automatic
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.SWIG.common import ooferror
import types

# Special parameter type that can take either a string (generally
# assumed to be a filename) or a special value (currently
# "automatic").  Used to set the destination for outputs, the intended
# semantics are that "automatic" should cause the output to send its
# data to the message window via the reporter. 
class DestinationParameter(parameter.StringParameter):
    types = (types.StringType, automatic.Automatic)
    def __init__(self, name, value=None,
                 default=automatic.automatic, tip=None):
        parameter.StringParameter.__init__(
            self, name, value=value, default=default, tip=tip)
        
    def binaryRepr(self, datafile, value):
        stringvalue=value
        if value==automatic.automatic:
            stringvalue='automatic.automatic'
        return parameter.StringParameter.binaryRepr(self,datafile,stringvalue)
    def binaryRead(self, parser):
        stringvalue=parameter.StringParameter.binaryRead(self,parser)
        if stringvalue=='automatic.automatic':
            #automatic.automatic on the backend processes is not used,
            #but might as well return it.
            return automatic.automatic
        else:
            return stringvalue

# Utility function -- given the value of a destination parameter, it
# returns a file object to which data can be appended.
def get_file(destination, mode="a"):
    if destination==automatic.automatic:
        return reporter.fileobj
    else:
        return open(destination, mode)
