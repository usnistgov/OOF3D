# -*- python -*-
# $RCSfile: placeholder.py,v $
# $Revision: 1.5.2.6 $
# $Author: langer $
# $Date: 2014/09/15 19:53:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
import types, sys

# Special types for representing the selection in aggregate parameters
# (ie parameters that can be set to a group or the currently selected
# objects).

_allPlaceHolders = []
_allPlaceHoldersDict = {}

def getPlaceHolderFromID(idno): # used in binaryReprs of Parameters
    if idno > 0:
        return _allPlaceHolders[idno - 1]

def getPlaceHolderFromString(strng):
    # returns strng if it's not a PlaceHolder id.  Used when parsing
    # widget values that can include both real Who object names and
    # placeholders.
    return _allPlaceHoldersDict.get(strng, strng)

## Each class derived from PlaceHolder must have a data member called
## 'idtag'.  A singleton object whose name is the value of idtag will
## be created in this module and the main OOF2 module.  The object's
## repr will be idtag, and it will have an IDstring member whose value
## is idtag in angle brackets, suitable for appearing in gui menus.
 
class PlaceHolderMetaClass(type):
    def __init__(cls, name, bases, dict):
        super(PlaceHolderMetaClass, cls).__init__(name, bases, dict)
        cls.idno = len(_allPlaceHolders) # used in binaryReprs of Parameters
        idname = dict['idtag']
        if idname:              # don't include PlaceHolder base class
            singleton = cls()   # make a singleton instance
            cls.IDstring = '<' + idname + '>' # for display in menus
            _allPlaceHoldersDict[cls.IDstring] = singleton
            _allPlaceHolders.append(singleton)
            utils.OOFdefine(idname, singleton)
            globals()[idname] = singleton

class PlaceHolder(object):
    __metaclass__ = PlaceHolderMetaClass
    # An empty idtag string keeps this class from being instantiated.
    idtag = ''                  
    def __repr__(self):
        return self.idtag
    def __cmp__(self, other):
        return cmp(self.__class__, other.__class__)

# Defining these classes automatically creates an instance of each
# class with a name given by the idtag.

class SelectionPlaceHolder(PlaceHolder):
    idtag = 'selection'

class EveryPlaceHolder(PlaceHolder):
    # idtag = 'all'
    idtag = 'every'

class NothingPlaceHolder(PlaceHolder):
    idtag = 'nothing'

class LatestPlaceHolder(PlaceHolder):
    idtag = 'latest'

class EarliestPlaceHolder(PlaceHolder):
    idtag = 'earliest'
                             

# TODO 3.1: update the docs.
xmlmenudump.XMLObjectDoc(
    'Placeholder',
    xmlmenudump.loadFile("DISCUSSIONS/common/object/placeholder.xml"))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# For historical reasons, the PlaceHolderParameter accepts the value
# 'all', which means the same thing as '"every"'.  The idtag for
# EveryPlaceHolder used to be "all", so scripts could contain arguments
# like pixels=all.  In Python 2.5 and beyond, 'all' is a built-in
# function, so it's unwise to redefine it as a PlaceHolder.  However,
# scripts may still contain pixels=all, so the PlaceHolderParameter
# was introduced.  It accepts the built-in function 'all' as a value,
# and interprets it as the PlaceHolder "every".

# PlaceHolderParameter doesn't use the default Parameter.set method,
# because that method doesn't handle the PlaceHolder metaclass
# properly.

class PlaceHolderParameter(parameter.Parameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        self.placeholders = [t for t in self.types
                             if isinstance(t, PlaceHolder)]
        self.othertypes = tuple(
            [t for t in self.types if t not in self.placeholders])
        parameter.Parameter.__init__(self, name, value=value,
                                     default=default, tip=tip, auxData=auxData)

    def set(self, value):
        if value is all:
            value = every
        if value is not None:
            if not (isinstance(value, self.othertypes) or
                    (self.placeholders and value in self.placeholders) or
                    (not self.placeholders and isinstance(value, PlaceHolder))):
                raise parameter.ParameterMismatch("Bad value", value,
                                                  "for Parameter", self.name)
        self._value = value
        # self.timestamp.increment()

    def binaryRepr(self, datafile, value):
        if isinstance(value, placeholder.PlaceHolder):
            return struct.pack(parameter.structIntFmt, value.idno)
        else:
            # just like a StringParameter's binaryRepr, but with a
            # preceding 0 to indictate that it's not a PlaceHolder
            # object.
            return struct.pack('>ii', 0, len(value)) + value
    def binaryRead(self, parser):
        b = parser.getBytes(parameter.structIntSize)
        (idno,) = struct.unpack(parameter.structIntFmt, b)
        if idno > 0:
            return placeholder.getPlaceHolderFromID(idno)
        b = parser.getBytes(parameter.structIntSize)
        (length,) = struct.unpack(parameter.structIntFmt, b)
        return parser.getBytes(length)


    def valueDesc(self):
        return "A character string, or a <link linkend='Object-PlaceHolder'>PlaceHolder</link> object."

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class TimeParameter(PlaceHolderParameter):
    types = (types.IntType, types.FloatType, earliest, latest)
    def valueDesc(self):
        return "A floating point number, or the earliest or latest time."

class GfxTimeParameter(TimeParameter):
    pass
