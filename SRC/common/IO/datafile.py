# -*- python -*-
# $RCSfile: datafile.py,v $
# $Revision: 1.32.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import progress
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import utils
from ooflib.common import oofversion
from ooflib.common.IO import mainmenu
from ooflib.common.IO import menuparser
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
import os.path
import string
import types

##############################

datafileversion = 1.0

##############################

# Data file formats

if not config.nanoHUB():
    class DataFileFormat(enum.EnumClass(
        ('script',
 'A fully functioning Python script.  Flexible and editable, but insecure.'),
        ('ascii', 'An ASCII file with Python-like syntax that will NOT be parsed by the Python interpreter.  Inflexible, editable, but secure.'),
        ('binary', 'A binary file. Inflexible and uneditable, but secure, compact and not subject to round-off error.')
        )):
        tip = "Types of &oof2; data files."
        discussion = "<para>See <xref linkend='Section:Concepts:FileFormats'/>.</para>"

else:                           # in nanoHUB mode scripts aren't allowed
    class DataFileFormat(enum.EnumClass(
        ('ascii', 'An ASCII file with Python-like syntax that will NOT be parsed by the Python interpreter.  Inflexible, editable, but secure.'),
        ('binary', 'A binary file. Inflexible and uneditable, but secure, compact and not subject to round-off error.')
        )):
        tip = "Types of &oof2; data files."
        discussion = "<para>See <xref linkend='Section:Concepts:FileFormats'/>.</para>"

utils.OOFdefine('DataFileFormat', DataFileFormat)


class DataFileFormatExt(
    enum.subClassEnum(DataFileFormat, ('abaqus', 'An ABAQUS-style text file'))):
    tip = "More types of &oof2; data files."
    discussion = "<para>See <xref linkend='Section:Concepts:FileFormats'/>.</para>"

    
utils.OOFdefine('DataFileFormatExt', DataFileFormatExt)

# These constants or objects are also instances of DataFileFormat
if not config.nanoHUB():
    SCRIPT = DataFileFormatExt("script")
else:
    SCRIPT = None
ASCII = DataFileFormatExt("ascii")
BINARY = DataFileFormatExt("binary")
ABAQUS = DataFileFormatExt("abaqus")

##############################

def versionCB(menuitem, number, format):
    if format == BINARY:
        menuitem.parser.binaryMode()

versionCmd = oofmenu.OOFMenuItem(
    'FileVersion',
    callback=versionCB,
    params=[parameter.FloatParameter('number',
                                     tip='file format version number'),
            enum.EnumParameter('format', DataFileFormat,
                               tip='format for the data file.')],
    help="Identify data file format.  Used internally in data files.",
    discussion="""
    <para>&oof2; data files must begin with a FileVersion command.
    The <varname>number</varname> parameter is used to maintain
    compatibility with older data files.  For now, its value should be
    <userinput>1.0</userinput>.  The <varname>format</varname>
    parameter must be one of the values discussed in <xref
    linkend='Section:Concepts:FileFormats'/>.</para>
    """)

mainmenu.OOF.LoadData.addItem(versionCmd)

class AsciiDataFile:
    def __init__(self, file, format):
        self.format = format
        self.file = file
        self.nargs = 0
        self.buffer = ""
    def startCmd(self, command):
        path = command.path()
        if self.format == ASCII:
            path = string.join(path.split('.')[2:], '.')
        self.buffer = path + "("
        self.nargs = 0
    def endCmd(self):
        self.file.write(self.buffer)
        self.file.write(")\n")
        self.file.flush()
        self.buffer = ""
    def discardCmd(self):
        self.buffer = ""
        self.nargs = 0
    def argument(self, name, value):
        if self.nargs > 0:
            self.buffer += ", "
        self.buffer += "%s=%s" % (name, `value`)
        self.nargs += 1
    def comment(self, remark):
        self.file.write("# %s\n" % remark)
    def close(self):
        self.file.close()

def writeDataFile(filename, mode, format):
    if format == BINARY:
        mode += 'b'
    file = open(filename, mode)
    if format == SCRIPT:
        versioncmd = "OOF.LoadData.FileVersion"
    else:
        versioncmd = "FileVersion"
    file.write("# OOF version %s\n%s(number=%s, format=%s)\n"
               % (oofversion.version, versioncmd, datafileversion, `format`))
    if format != BINARY:
        return AsciiDataFile(file, format)
    from ooflib.common.IO import binarydata    # avoid import loop
    return binarydata.BinaryDataFile(file)

def readDataFile(filename, menu):
    prog = progress.getProgress(os.path.basename(filename), progress.DEFINITE)
    try:
        source = menuparser.ProgFileInput(filename, prog)
        parser = menuparser.MenuParser(source, menu)
        parser.run()
    finally:
        prog.finish()
