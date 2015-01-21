# -*- python -*-
# $RCSfile: reporter.py,v $
# $Revision: 1.53.2.8 $
# $Author: langer $
# $Date: 2014/08/01 17:55:31 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Generic error-reporting machine.  Should be able to either simply
# log errors, or request a course of action from the user.

from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import threadstate
from ooflib.common import debug
from ooflib.common import parallel_enable
from ooflib.common import thread_enable
from ooflib.common import utils
from ooflib.common.IO import questioner
import ooflib.SWIG.common.lock
import sys
import traceback


# List of allowed message classes.
messageclasses = ["Log", "Warning", "Report", "Query", "Error"]

messagedescriptions = {
    "Log" : "menu commands which have been executed.",
    "Warning": "messages indicating risky or undefined behavior.",
    "Report": "supplementary data about the state of a command.",
    "Query": "questions posed to you by OOF, and your answers.",
    "Error": "reasons why OOF was unable to complete a task."}

# Message-handling class, which maintains a database of different
# types of message.  
# In GUI mode, this thing gets a special window.

# It may be desirable to set an upper limit on the number of
# messages stored, so as not to chew up too much memory.

class MessageManager:
    def __init__(self):
        # Set flags.  For each type of message, if the flag is set,
        # then the messages of that type should be displayed to the
        # user.
        self.gui_mode = False
        self.flag_dict = {}
        for f in messageclasses:
            self.flag_dict[f] = True

        # Message list is a list of tuples, of the form (message, category).
        self.message_list = []
        self._pop_up_warnings = True
        self._warnings_are_errors = False
        
         # bar_text is the current contents of the progress bar.  It's
         # initialized to "" instead of None so that its len is always
         # computable.
        self.bar_text = ""
        # thread_bars contains the progress bar text from each thread,
        # keyed by thread number.  It's an ordered dict so that the
        # bars for the oldest threads are displayed first.
        self.thread_bars = utils.OrderedDict()

        self.lock = ooflib.SWIG.common.lock.SLock()    # locks message_list
        self.outlock = ooflib.SWIG.common.lock.SLock() # locks bars and output

    def get_warning_pop_up(self):
        return self._pop_up_warnings

    def set_warning_pop_up(self, arg=True):
        self._pop_up_warnings = arg

    def set_warning_error(self, arg):
        self._warnings_are_errors = arg
    
    def set_flag(self, flag, value):
        self.flag_dict[flag] = value

    def get_flag(self, flag):
        return self.flag_dict[flag]

    # "Smart write" routine -- the complexity originates in the need
    # to be able to write out messages (in text mode) while
    # partially-drawn text progress bars are in place. 
    
    def _write(self, msg):
        if not self.gui_mode:
            self.outlock.acquire()
            try:
                if not self.bar_text:
                    print msg
                    sys.stdout.flush()
                else: 
                    # This is the "smart" case -- erase the bar, write
                    # the message, then redraw the bar.
                    # erase bar
                    sys.stdout.write('\r' + len(self.bar_text)*' ' + '\r')
                    print msg
                    sys.stdout.write(self.bar_text)
                    sys.stdout.flush()
            finally:
                self.outlock.release()

    # Draw a new progressbar.
    def display_bar(self, newbars=None):
        if sys.stdout.isatty(): # Don't try to write progressbars to a file!
            self.outlock.acquire()
            try:
                if newbars:
                    # Use '|' to separate progress bars from the same thread
                    txt = " | ".join(filter(None, newbars))
                    self.thread_bars[threadstate.findThreadNumber()] = txt
                
                # Erase old bar display
                oldlen = len(self.bar_text)
                if oldlen:      # overwrite old bar
                    sys.stdout.write('\r' + oldlen*' ' + '\r')
                    
                # Redisplay all bars from all threads.  Use '||' to
                # separate progress bars from different threads.
                self.bar_text = ' || '.join(txt
                                          for txt in self.thread_bars.values()
                                            if txt)

                sys.stdout.write(self.bar_text)
                sys.stdout.flush()
            finally:
                self.outlock.release()
        
    def undisplay_bar(self):
        if sys.stdout.isatty():
            self.outlock.acquire()
            try:
                threadno = threadstate.findThreadNumber()
                if threadno in self.thread_bars:
                    del self.thread_bars[threadno]
            finally:
                self.outlock.release()
                self.display_bar()

    # All of the "normal" (i.e. non-progress-bar) messaging calls
    # eventually call "_append", which adds the message to the
    # database.  This function also returns the message, although
    # most of the calls discard it, except "warning".
    def _append(self, type, *args):
        message = ' '.join([str(x) for x in args])
        self.lock.acquire()
        try:
            if debug.debug() and type!="Log" and guitop.top():
                print message
            self.message_list.append( (message, type) )
            if self.flag_dict[type]:
                self._write(message)
        finally:
            self.lock.release()
        switchboard.notify( "write message", (message, type) )
        return message
    
    def all_messages(self):
        return self.message_list
    
    def log(self, *args):
        self._append("Log", *args)
        
    def warn(self, *args):
        if self._warnings_are_errors:
            raise ooferror.ErrWarning(' '.join(args))
        message = self._append("Warning", *args)
        switchboard.notify("messagemanager warning", message)

    def report(self, *args):
        self._append("Report", *args)

    # Arguments for this are different, this wraps the questioner.
    def query(self, question, *answers, **kwargs):
        ans = questioner.questioner(question, *answers, **kwargs)
        self._append("Query", question, ans)
        return ans

    def error(self, *args):
        self._append("Error", *args)


# The one and only.
messagemanager = MessageManager()

# Convenience, make functions available at the module level.
def report(*args):
    messagemanager.report(*args)

def log(*args):
    messagemanager.log(*args)

# Warning: The warning function can bring up a pop-up, but doesn't
# block in threads.  Blocking behavior can be provided by calling it
# with mainthread.runBlock.
def warn(*args):
    messagemanager.warn(*args)

# This function must block the child thread in thread mode,
# and so should be called with mainthread.runBlock by
# threaded menu items.
def query(question, *args, **kwargs):
    return messagemanager.query(question, *args, **kwargs)

# error() should not be called directly most of the time.  Menu
# callback code should instead raise an exception, which will be
# caught and handled by the menu code.  That code will call the
# error() function.
def error(*args):
    messagemanager.error(*args)


# Over-ride-able function for generating a new display -- does nothing
# in command-line mode.
def _new_messages():
    pass

## progress bar module level functions

def removeProgressBar():
    # (Should be) Called only by TextThreadedWorker.meanwhile()!
    messagemanager.undisplay_bar()

def showProgressBar(text):
    # Called only by TextThreadedWorker.meanwhile()
    messagemanager.display_bar(text)
    
######################

# Object providing a file-like interface to the message manager's
# "report" function, useful for outputs which do not know/care what
# they're writing to.
class ReportFile:
    def __init__(self):
        self.buffer = ""
    def close(self):
        pass
    # Not quite file-like -- a call to "flush" will add a line separator
    # at the end of the flushed buffer data.
    def flush(self):
        global messagemanager
        if self.buffer:
            messagemanager.report(self.buffer)
        self.buffer=""
    def write(self, data):
        global messagemanager
        self.buffer += data
        stringset = self.buffer.split('\n')
        for s in stringset[:-1]:
            messagemanager.report(s)
        self.buffer = stringset[-1]

fileobj = ReportFile()

