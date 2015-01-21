# -*- python -*-
# $RCSfile: filenameparam.py,v $
# $Revision: 1.3.4.2 $
# $Author: fyc $
# $Date: 2014/09/12 20:36:47 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import enum
from ooflib.common.IO import parameter

class FileNameParameter(parameter.StringParameter):
    def __init__(self, name, value=None, default="", tip=None, ident=None):
        self.ident = ident
        parameter.StringParameter.__init__(
            self, name, value, default, tip)

class FileOrDirectoryParameter(FileNameParameter):
    pass          
            
class WriteFileNameParameter(FileNameParameter):
    action='w'

class ReadFileNameParameter(FileOrDirectoryParameter):
    action='r'

class WriteMode(enum.EnumClass("w", "a")):
    pass

class WriteModeParameter(enum.EnumParameter):
    def __init__(self, name, value=None, default=None, tip=None):
        enum.EnumParameter.__init__(self, name, WriteMode, value, default, tip)

class OverwriteParameter(parameter.BooleanParameter):
    pass


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FileListParameter(parameter.ListOfStringsParameter):
    def __init__(self, name, value=None, default=[], tip=None, ident=None):
        self.ident = ident
        parameter.ListOfStringsParameter.__init__(
            self, name, value=value, default=default, tip=tip)

class PatternParameter(parameter.StringParameter):
    pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class DirectoryNameParameter(FileOrDirectoryParameter):
    pass
# The ImpliedDirectoryNameParameter is just like a
# DirectoryNameParameter, but it doesn't create a widget in the GUI.
# Instead, it looks for a FileSelectorWidget in the same scope and
# gets the directory name from it.  It should be used only in an
# OOFMenuItem or RegisteredClass which also uses a FileNameParameter
# or FileListParameter.

class ImpliedDirectoryNameParameter(DirectoryNameParameter):
    pass
