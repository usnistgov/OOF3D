# -*- python -*-
# $RCSfile: loggers.py,v $
# $Revision: 1.3.2.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:16 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## The GtkLogger class hierarchy

## GtkLogger classes are in charge of recording the appropriate data
## from each type of Widget.  The GtkLogger class hierarchy mimics the
## GtkObject class hierarchy.  Each Widget class whose actions are to
## be recorded must correspond to a GtkLogger class which has a
## "record" method that can handle the action.

import gtk
import re
import sys
import types

import logutils

# _loggerDir is a sorted list of (gtk class, GtkLogger class)
# pairs.  The list is sorted so that each gtk class comes before its
# base classes, so that the GtkLogger corresponding to the most
# derived class is found first.

_loggerDir = []

def findLogger(obj):
    for klass, logger in _loggerDir:
        if isinstance(obj, klass):
            return logger()
    raise NotImplementedError("No GtkLogger for %s" % obj.__class__.__name__)

# localvar generates names for local variables in scripts.
_localvarcount = {}

def localvar(base):
    count = _localvarcount.get(base, 0)
    _localvarcount[base] = count + 1
    return "%s_%d" % (base, count)
        
# GtkLoggerMetaClass is the metaclass for GtkLogger.  It ensures that
# all GtkLogger classes are listed in the _loggerDir in the right
# order.  It requires that each GtkLogger subclass have a class-level
# tuple called 'classes' which contains the gtk classes to which the
# Logger applies.

class GtkLoggerMetaClass(type): 
    def __init__(cls, name, bases, dict):
        super(GtkLoggerMetaClass, cls).__init__(name, bases, dict)
        # get the list of gtk classes to which this logger applies
        klasses = dict.get('classes', ())
        # Make a _loggerDir entry for each gtk class.
        for klass in klasses:
            # Insertion sort!  The sorting criterion (subclasses
            # before base classes) doesn't define a unique ordering,
            # and we don't care about speed here, anyway.
            for i in range(len(_loggerDir)):
                if issubclass(klass, _loggerDir[i][0]):
                    _loggerDir.insert(i, (klass, cls))
                    break
            else:
                _loggerDir.append((klass, cls))
                

class GtkLogger(object):
    __metaclass__ = GtkLoggerMetaClass
    def location(self, obj, *args):
        ## location() returns a string that can be evaluated by Python
        ## to return the given object.  The string specifies the
        ## object's location, in some sense.
        raise logutils.GtkLoggerException("No location function")

    def record(self, obj, signal, *args):
        ## record() returns a *list* of strings that can be evaluated
        ## to recreate a gui action.  Each string is a single Python
        ## line.  Only Python statements that can be evaluated in a
        ## single line are allowed, because they aren't being read by
        ## a full Python parser.  That means that
        ##    tree = findWidget('window:tree')
        ##    tree.row_activated(...)
        ## is ok, but
        ##    if tree is not None:
        ##       tree.row_activated(...)
        ## is not.   Import statements and function calls are allowed.
        raise logutils.GtkLoggerException("No record function for",
                                 obj.__class__.__name__, signal,
                                 "in", self.__class__.__name__)
    # GtkLogger.record() should return GtkLogger.ignore if an event
    # should not be logged.
    class Ignore:
        pass
    ignore = Ignore()

####################


##############################################################
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##############################################################    

# This is the gtk signal handler that records everything.

def signalLogger(obj, signal, *args):
    if logutils.recording() and not logutils.replaying():
        try:
            records = findLogger(obj).record(obj, signal, *args)
        except logutils.GtkLoggerTopFailure, exc:
            if logutils.debugLevel() >= 3:
                print >> sys.stderr, "Can't log %s (%s): %s" \
                      (obj.__class__.__name__, signal, exc)
        except logutils.GtkLoggerException, exc:
            if logutils.debugLevel() >= 1:
                print >> sys.stderr, "Can't log %s (%s): %s" % \
                      (obj.__class__.__name__, signal, exc)
        else:
            if records is GtkLogger.ignore:
                pass
            elif records is not None:
                assert type(records) is types.ListType
                for record in records:
                    _writeline(record)
            else:
                if logutils.debugLevel() >= 1:
                    print >> sys.stderr, "No record function for", obj, signal
    return False                        # propagate events


## Some lines are logged too often.  This code eliminates redundant
## lines, making the log files easier to read and faster to run.

## _redundantlines is a list of regular expression objects that match
## lines that are redundant when repeated.
_redundantlines = [
    # Each time a Window is created, it emits four 'configure-event'
    # signals, which show up as four 'resize' lines in the log.
    re.compile(r".*\.resize\([0-9]+, [0-9]+\)$"),
    # set_position lines for HPaned and VPaned widgets are generated
    # from their children's 'size-allocate' signals, which are
    # repeated unnecessarily, as far as we're concerned.
    re.compile(r".*\.set_position\([0-9]+\)$")
    ]

def _not_redundant(line):
    for regexp in _redundantlines:
        if regexp.match(line) is not None:
            return False
    return True

_prevline = None
def _writeline(line):
    global _prevline
    if line != _prevline or _not_redundant(line):
        print >> logutils.logfile(), line
        try:
	  logutils.logfile().flush()
	except Exception as inst:
	  print inst
        if logutils.debugLevel() >= 2 and not logutils.replaying():
            print >> sys.stderr, "//////", line
    _prevline = line
    

