# -*- python -*-
# $RCSfile: outputdestination.py,v $
# $Revision: 1.4.4.7 $
# $Author: langer $
# $Date: 2014/09/17 17:48:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import quit
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import datafile
from ooflib.common.IO import formatchars
from ooflib.common.IO import filenameparam
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
import os
import sys
import weakref

class OutputDestination(registeredclass.RegisteredClass):
    registry = []
    tip="What to do with Scheduled Output data."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/outputdest.xml')
    def open(self):
        pass
    # def open_append(self):
    #     pass
    def flush(self):
        pass
    def rewind(self):
        pass
    def close(self):
        pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class GfxWindowDestination(OutputDestination):
    def shortrepr(self):
        return "<Graphics Window>"

registeredclass.Registration(
    'Graphics Window',
    OutputDestination,
    GfxWindowDestination,
    rewindable=False,
    ordering=0,
    tip="Send graphics window updates to the graphics window.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/gfxoutputdest.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Deleting streams when shutting down is tricky because of side
# effects caused by disappearing weak references and because of the
# uncontrollable order in which module components are destroyed.  So
# if we're shutting down, as indicated by the shuttingdown flag, we
# just skip parts of the process.

# Note that renaming "shuttingdown" to "_shuttingdown" is a bad idea
# because Python destroys objects with names beginning with an
# underscore before it destroys other objects.

shuttingdown = False 

def cleanUp():
    global shuttingdown
    shuttingdown = True

switchboard.requestCallbackMain("shutdown", cleanUp)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#


# BaseOutputStream does the work for OutputStream, which writes Output
# data to a file.  More than one OutputStream can write to the same
# file, which they do by sharing a single BaseOutputStream.

_allStreams = utils.OrderedDict() # All BaseOutputStreams, keyed by filename
_streamsLock = lock.SLock()       # Controls access to _allStreams


class BaseOutputStream(object):
    def __init__(self, filename, mode, openfile):
        self.filename = filename
        self.file = None
        self.openfile = openfile # fn that actually opens the file
        # _streamsLock has always been aquired before __init__ is called.
        _allStreams[filename] = self
        self.referents = []     # all OutputStreams using this BaseOutputStream
        # lastOutput and lastargs are used to decide whether or not to
        # write the header info in the data file.  It's not written if
        # the output and its args are the same as they were for the
        # previous write.
        self.lastOutput = None
        self.lastargs = None
        self.seplast = True     # was the last thing written a separator?
        self.nOpen = 0          # net number of times this has been opened
        self.everOpened = False # has this been opened in this oof2 session?
        self.lock = lock.SLock() # controls access by OutputStreams
        self.mode = mode
        self.rewound = False
        self.appending = False
    def addStream(self, stream):
        self.lock.acquire()
        self.referents.append(weakref.ref(stream, self._removeStream))
        self.lock.release()
    def _removeStream(self, wref):
        if not shuttingdown:
            self.referents.remove(wref)
            self.lock.acquire()
            try:
                if len(self.referents) == 0 and self.file is not None:
                    self.file.close()
                    self.file = None
                    del _allStreams[self.filename]
            finally:
                self.lock.release()
            switchboard.notify("output destinations changed")
    def open(self):
        self.lock.acquire()
        try:
            if self.file is None:
                # The file should be opened with mode "w" if either of
                # these conditions holds:
                # * It hasn't been opened before during this
                #   session, and self.mode="w"
                # * It's been rewound since the last time it was
                #   opened.
                # In all other cases, it should be opened with mode "a".
                if (not self.everOpened and self.mode == "w") or self.rewound:
                    mowed = "w"
                    self.rewound = False
                    self.lastOutput = None
                    self.seplast = True
                    self.appending = False
                else:
                    mowed = "a"
                    self.appending = os.path.exists(self.filename)
                self.file = self.openfile(self.filename, mowed)
                self.everOpened = True
            self.nOpen += 1
        finally:
            self.lock.release()
    def rewind(self):
        self.lock.acquire()
        self.seplast = True
        self.rewound = True
        try:
            if self.file is not None:
                self.file.close()
                self.file = None
            self.mode = filenameparam.WriteMode("w")
            self.everOpened = False
            self.lastOutput = None
        finally:
            self.lock.release()
    def close(self):
        self.lock.acquire()
        try:
            self.nOpen -= 1
            assert self.nOpen >= 0
            if self.nOpen == 0:
                self.file.close()
                self.file = None
                self.seplast = True
        finally:
            self.lock.release()
    def flush(self):
        self.lock.acquire()
        try:
            if self.file is not None:
                self.file.flush()
        finally:
            self.lock.release()
    def printHeadersIfNeeded(self, output, *args, **kwargs):
        if self.lastOutput != output or self.lastargs != (args, kwargs):
            if self.appending or self.lastOutput is not None:
                self.file.write("\n") # insert extra blank line before header
            output.printHeaders(self, *args, **kwargs)
            self.lastOutput = output
            self.lastargs = (args, kwargs)
    def write(self, text):
        # When an object with a "write" method is used as the argument
        # of "print >>", write is called once for each printed string,
        # once for each space between printed strings, and once for
        # the newline at the end.
        if text == " " and not self.seplast:
            self.file.write(formatchars.getSeparator())
            self.seplast = True
        elif text == "\n":
            self.file.write(text)
            self.seplast = True
        else:
            self.file.write(text)
            self.seplast = False
    def comment(self, *args):
        self.file.write(" ".join([formatchars.getCommentChar()] + 
                                 [x for x in args] ))
        self.file.write("\n")
        self.seplast = False

def rewindStream(filename):
    stream = _allStreams[filename]
    stream.rewind()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# TextOutputDestination is an intermediate baseclass for
# OutputDestinations that produce some sort of human readable text
# (ie, not OOF2 data files which might be ascii or binary).  This
# includes the results of Analysis operations.  There are two
# subclasses: OutputStream, which writes to a file, and
# MessageWindowStream, which writes to the OOF2 Message Window.

class TextOutputDestination(OutputDestination):
    def __init__(self, basestream):
        # Multiple TextOutputDestinations can share the same
        # basestream, which is a BaseOutputStream.
        self.basestream = basestream
        basestream.addStream(self)
    def open(self):
        self.basestream.open()
    def rewind(self):
        self.basestream.rewind()
    def printHeadersIfNeeded(self, output, *args, **kwargs):
        self.basestream.printHeadersIfNeeded(output, *args, **kwargs)
    def write(self, text):
        self.basestream.write(text)
    def comment(self, *args):
        self.basestream.comment(*args)
    def close(self):
        self.basestream.close()


# OutputStream directs output to a file, specified by a file name and
# mode. If two OutputStreams have the same filename but different
# modes, the *last* mode specified is used.  TODO 3.1: Make sure that the
# documentation is correct about that. It used to be different.

class OutputStream(TextOutputDestination):
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        try:
            _streamsLock.acquire()
            try:
                basestream = _allStreams[filename]
            except KeyError:
                basestream = BaseOutputStream(filename, mode, file)
            else:
                basestream.mode = mode
        finally:
            _streamsLock.release()
        TextOutputDestination.__init__(self, basestream)
        switchboard.notify("output destinations changed")
    def shortrepr(self):
        return self.filename

# newreg is referred to in outputdestinationwidget.py.
newreg = registeredclass.Registration(
    'Output Stream',
    OutputDestination,
    OutputStream,
    ordering=1,
    rewindable=True,
    params=[
        filenameparam.WriteFileNameParameter(
            'filename', tip=parameter.emptyTipString),
        filenameparam.WriteModeParameter(
            'mode', tip="Whether to write or append to the file.")
        ],
    tip="Send output to a file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/outputstream.xml')
)
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

msgWindowName = "<Message Window>"
    
class MessageWindowStream(TextOutputDestination):
    def __init__(self):
        TextOutputDestination.__init__(
            self,
            BaseOutputStream(msgWindowName, filenameparam.WriteMode("w"),
                             lambda f,m: reporter.fileobj))
    def shortrepr(self):
        return "<Message Window>"

registeredclass.Registration(
    'Message Window',
    OutputDestination,
    MessageWindowStream,
    ordering=0,
    rewindable=False,
    tip="Send output to the Message Window.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/messagewindow.xml')
)

msgWindowOutputDestination = MessageWindowStream()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def allTextOutputStreams():
    _streamsLock.acquire()
    try:
        return [n for n in _allStreams.keys() if n != msgWindowName]
    finally:
        _streamsLock.release()

def forgetTextOutputStreams():
    _streamsLock.acquire()
    try:
        _allStreams.clear()
    finally:
        _streamsLock.release()
    switchboard.notify("output destinations changed")

def getLatestMode(filename, default):
    try:
        return _allStreams[filename].mode
    except KeyError:
        return default

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class DataFileOutput(OutputDestination):
    def __init__(self, filename, mode, format):
        self.filename = filename
        self.mode = mode
        self.format = format
        self._dfile = None
        self.everOpened = False
        self.rewound = False
    def open(self):
        ## See BaseOutputStream.open()
        assert self._dfile is None
        if (not self.everOpened and self.mode == "w") or self.rewound:
            mowed = "w"
            self.rewound = False
        else:
            mowed = "a"
        self._dfile = datafile.writeDataFile(
            self.filename, mowed, self.format)
        self.everOpened= True
    def dfile(self):
        assert self._dfile is not None
        return self._dfile
    def flush(self):
        if self.isOpen():
            self._dfile.flush()
    def close(self):
        if self.isOpen():
            self._dfile.close()
            self._dfile = None
    def isOpen(self):
        return self._dfile is not None
    def rewind(self):
        # In case we want to forbide rewind when the output file is oppened in append mode uncommnent the next line.
        # assert not ((not self.everOpened and self.mode == "w") or self.rewound) 
        self.close() 
        self._dfile = None
        self.rewound = True
        self.everOpened = False
    def shortrepr(self):
        return "%s (%s)" % (self.filename, self.format.string())

registeredclass.Registration(
    'Data File',
    OutputDestination,
    DataFileOutput,
    rewindable=True,
    params=[
        filenameparam.WriteFileNameParameter(
            "filename", tip=parameter.emptyTipString),
        filenameparam.WriteModeParameter(
            "mode", tip="Whether to write or append to the file."),
        enum.EnumParameter('format', datafile.DataFileFormat, datafile.ASCII,
                           tip="Format of the file.")
        ],
    ordering=3,
    tip="Send Mesh data to a file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/datafiledest.xml'))
        
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class OutputDestinationParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.RegisteredParameter.__init__(
            self, name=name, reg=OutputDestination,
            value=value, default=default, tip=tip, auxData=auxData)
    def clone(self):
        return self.__class__(self.name, self.value, self.default, self.tip)
