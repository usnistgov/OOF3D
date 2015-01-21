# -*- python -*-
# $RCSfile: binarydata.py,v $
# $Revision: 1.15.18.1 $
# $Author: langer $
# $Date: 2014/05/08 14:38:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Routines for reading and writing binary data files.

# Binary data files, like the ascii data files, consist only of menu
# commands and their arguments.  The menu commands must be in the
# OOF.LoadData menu.  The arguments, like all OOFMenu arguments, are
# Parameter instances.  All Parameter classes have a binaryRepr
# function which returns a 'string' containing the binary
# representation of a parameter value (the string should be
# constructed by the Python struct module) and a binaryRead function
# which extracts a value from the data file.

# The menu items themselves are written as integer keys into a
# dictionary so that the full command does not have to be written each
# time it's used.  The dictionary is built as the commands are issued
# when writing the data file.  Before each command is used in the
# file, the file must contain the command that associates the new
# command with the integer key.  This command, OOF.LoadData.MenuKey,
# is preloaded into the dictionary.

# Other objects defined in the main oof namespace can be transmitted
# as binary keys as well.  The binaryRepr of the associated parameter
# must obtain the key from BinaryDataFile.oofObjID(), which returns a
# key and inserts the command defining it into the data file.  This
# command, OOF.LoadData.ObjKey, is also preloaded into the command
# dictionary.

# For all this machinery to work, the data file must be written *only*
# by the functions startCmd, argument, and endCmd in the
# BinaryDataFile class.

# Binary data files are read by the BinaryMenuParser, which is an
# instance of MenuParser, and supports the required getMenuItem and
# getArguments.  See menuparser.py.

from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import datafile
from ooflib.common.IO import mainmenu
from ooflib.common.IO import menuparser
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
import struct
import types

OOF = mainmenu.OOF

cmdformat = ">i"
cmdsize = struct.calcsize(cmdformat)

###########################

def menuKeyCB(menuitem, path, key):
    menuitem.parser.mode.defineMenuKey(path, key)

OOF.LoadData.addItem(oofmenu.OOFMenuItem(
    'MenuKey',
    callback=menuKeyCB,
    params=[parameter.StringParameter('path'),
            parameter.IntParameter('key')]
    ))

def objectKeyCB(menuitem, obj, key):
    menuitem.parser.mode.defineObjKey(utils.OOFeval_r(obj), key)

OOF.LoadData.addItem(oofmenu.OOFMenuItem(
    'ObjKey',
    callback=objectKeyCB,
    params=[parameter.StringParameter('obj'),
            parameter.IntParameter('key')]
    ))

############################

class BinaryDataFile:
    def __init__(self, file):
        self.file = file
        # cmdmap maps menuitems to integers.  It only contains items
        # actually used in the data file.
        self.cmdmap = {} 
        self.cmdmap[OOF.LoadData.MenuKey] = 0
        self.cmdmap[OOF.LoadData.ObjKey] = 1
        self.ncmds = len(self.cmdmap)
        self.curMenuItems = []
        # objmap maps objects in the OOF namespace to integers.  It
        # only contains objects actually used in the data file.
        self.objmap = {}
        self.nobjs = 0
        # argdict contains the arguments for the current command
        self.argdicts = []

    def close(self):
        self.file.close()

    def cmdID(self, menuitem):
        try:
            cmdid = self.cmdmap[menuitem]
        except KeyError:
            cmdid = self.cmdmap[menuitem] = self.ncmds
            self.ncmds += 1
            self.startCmd(OOF.LoadData.MenuKey)
            self.argument('path', menuitem.path()[len('OOF.LoadData.'):])
            self.argument('key', cmdid)
            self.endCmd()
        return cmdid

    def oofObjID(self, obj):
        try:
            objid = self.objmap[obj]
        except KeyError:
            objid = self.objmap[obj] = self.nobjs
            self.nobjs += 1
            # obj hasn't been used in the data file yet.  Insert the
            # command that defines it.
            self.startCmd(OOF.LoadData.ObjKey)
            if obj is None:
                self.argument('obj', 'None')
            elif type(obj) is types.ClassType:
                self.argument('obj', obj.__name__)
            else:
                try:
                    # Some types of objects, notably
                    # RegisteredClasses, need to insert themselves
                    # into the OOF namespace with a different name (in
                    # the case of RegisteredClasses, it's the
                    # Registrations that are inserted, but the name is
                    # the subclass name).  Those objects should define
                    # a binReprName function to return the correct
                    # name.
                    self.argument('obj', obj.binReprName())
                except AttributeError:
                    self.argument('obj', obj.name())
            self.argument('key', objid)
            self.endCmd()
        return objid

    # Writing is postponed until after the strings for all the
    # arguments have been acquired, since if the arguments use objects
    # not yet in objmap they'll have to write their definitions to the
    # file before the command is written.
    def startCmd(self, menuitem):
        self.curMenuItems.append(menuitem)
        self.argdicts.append({})
    def argument(self, name, value):
        self.argdicts[-1][name] = value
    def endCmd(self):
        menuitem = self.curMenuItems.pop()
        argdict = self.argdicts.pop()
        cmdstring = struct.pack(cmdformat, self.cmdID(menuitem))
        # argstrings contains the binary string representations of the
        # arguments, in the order in which they appear in the menu's
        # param list.
        argstrings = []
        for param in menuitem.params:
            value = argdict[param.name]
            argstrings.append(param.binaryRepr(self, value))
        # Now, write the data.
        self.file.write(cmdstring)
        for argstring in argstrings:
            self.file.write(argstring)
    def discardCmd(self):
        self.curMenuItems.pop()
        self.argdicts.pop()
    def comment(self, remark):
        pass
        
#######################

class BinaryMenuParser(menuparser.MenuParserMode):
    def __init__(self, masterparser):
        self.cmdmap = {}
        self.objmap = {}
        self.masterparser = masterparser # MenuParser object
        self.menu = masterparser.menu   # OOFMenuItem
        self.defineMenuKey('MenuKey', 0)
        self.defineMenuKey('ObjKey', 1)

    def getBytes(self, n):
        return self.masterparser.getBytes(n)

    def defineMenuKey(self, path, key):
        self.cmdmap[key] = self.menu.descendPath(path)

    def defineObjKey(self, obj, key):
        self.objmap[key] = obj

    def getObject(self, key):
        return self.objmap[key]

    def getMenuItem(self, menu):
        # menu arg is not used, since full path is stored in file
        try:
            b = self.getBytes(cmdsize)
        except ooferror.ErrDataFileError: # no bytes to read
            return
        (key,) = struct.unpack(cmdformat, b)
        return self.cmdmap[key]

    def getArguments(self, menuitem):
        argdict = {}
        for param in menuitem.params:
            argdict[param.name] = param.binaryRead(self)
        return (), argdict



