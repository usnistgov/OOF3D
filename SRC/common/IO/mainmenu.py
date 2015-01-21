# -*- python -*-
# $RCSfile: mainmenu.py,v $
# $Revision: 1.164.2.14 $
# $Author: langer $
# $Date: 2014/10/08 14:24:34 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

#
#  The main oof menu -- with recording capability and so forth.

# Lots of miscellaneous commands are defined in this file because they
# didn't seem to merit a file of their own.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import progress
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import threadstate
from ooflib.common import debug
from ooflib.common import runtimeflags
from ooflib.common import subthread
from ooflib.common import thread_enable
from ooflib.common import utils
from ooflib.common.IO import filenameparam
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import scriptloader
from ooflib.common.IO.gfxmanager import gfxManager
from ooflib.common.IO import xmlmenudump
from types import StringType, FloatType, IntType
import code
import sys
import tempfile
import atexit
import os
import os.path

# Parameter = parameter.Parameter
StringParameter = parameter.StringParameter
IntParameter = parameter.IntParameter
FloatParameter = parameter.FloatParameter

OOFMenuItem = oofmenu.OOFMenuItem
OOFRootMenu = oofmenu.OOFRootMenu
CheckOOFMenuItem = oofmenu.CheckOOFMenuItem

OOF = OOFRootMenu(
    'OOF',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/oof.xml'))

################

# Automatically log all menu commands to a temp file. The location of
# the temp file is taken from the OOFTMP environment variable, if it's
# defined.  Otherwise it's determined by the tempfile.mkstemp
# function, which looks in the environment variables TMPDIR, TEMP, and
# TMP, followed by the directories /tmp, /var/tmp, and /usr/tmp.

ooftmpdir = os.getenv('OOFTMP')
prefix = os.path.basename(sys.argv[0]) + '-'
if ooftmpdir is not None:
    fd, logpath = tempfile.mkstemp(prefix=prefix, suffix='.py', dir=ooftmpdir)
else:
    fd, logpath = tempfile.mkstemp(prefix=prefix, suffix='.py')
tmplogfile = os.fdopen(fd, 'w')

def _tmplog(s):
    if tmplogfile:
        print >> tmplogfile, s
        tmplogfile.flush()
    
OOF.addLogger(oofmenu.MenuLogger(_tmplog))

# Remove the log file automatically if the program exits cleanly
def cleanlog():
    global tmplogfile, logpath
    if tmplogfile:
        try:
            tmplogfile.close()
            os.remove(logpath)
        except:
            pass
        logpath = ""
        tmplogfile = None
atexit.register(cleanlog)


################

## File menu

_filemenu = OOF.addItem(OOFMenuItem(
    'File',
    help="Commands for saving and loading data, and quitting."))

_loadmenu = _filemenu.addItem(OOFMenuItem(
    'Load',
    help="Commands for loading datafiles and scripts.",
    discussion="<para>Commands to load datafiles and scripts.</para>"))

# Commands in _startupmenu are identical to commands in _loadmenu, but
# they have their own copies of the parameters.  This prevents startup
# file names from setting the default values of parameters in the load
# menu.
_startupmenu = _filemenu.addItem(OOFMenuItem(
    'LoadStartUp',
    secret=True,
    help="Load start-up datafiles and scripts.",
    discussion="<para>Commands to load datafiles and scripts at start-up time.</para>"))

class PScriptLoader(scriptloader.ScriptLoader):
    # A ScriptLoader that supports a progress bar.
    def __init__(self, filename, **kwargs):
        self.prog = progress.getProgress(os.path.basename(filename),
                                          progress.DEFINITE)
        scriptloader.ScriptLoader.__init__(
            self,
            filename=filename,
            locals=sys.modules['__main__'].__dict__,
            **kwargs)  
    def progress(self, current, total):
        self.prog.setFraction((1.0*current)/total)
        if current <= total:
            self.prog.setMessage("Read %d/%d lines" % (current, total))
        else:
            self.prog.setMessage("Done")
    def stop(self):                     # called by ScriptLoader. Abort loop?
        return self.prog.stopped()
    def done(self):                     # called by ScriptLoader when finished
        self.prog.finish()
        scriptloader.ScriptLoader.done(self)

subScriptErrorHandler = None       # redefined if GUI is loaded

def loadscript(menuitem, filename):
    if filename is not None:
        debug.fmsg('reading', filename, 'in thread',
                   threadstate.findThreadNumber())
        kwargs = {}
        if subScriptErrorHandler:
            kwargs['errhandler'] = subScriptErrorHandler
        interp = PScriptLoader(filename, **kwargs)
        interp.run()
        if interp.error:
            # If the interpreter raised an exception and we're in
            # batch mode, the shell error status won't be set unless a
            # new exception is raised here.  The old exception has
            # already been handled by the time we get to this point.
            # interp.error[0] is the class of the exception.
            # interp.error[1] is its value.
            errorname = interp.error[0].__name__
            if errorname.lower()[0] in "aeiou":
                article = "an"
            else:
                article = "a"
            raise ooferror.ErrUserError(
                "Script '%s' raised %s %s exception" %
                (filename, article, interp.error[0].__name__)
                # "Script '%s' raised %s %s exception: %s" %
                # (filename, article, interp.error[0].__name__, interp.error[1])
                )
        debug.fmsg('finished reading', filename)

# class PScriptLoader(scriptloader.ScriptLoader):
#     # A ScriptLoader that supports a progress bar.
#     def __init__(self, filename):
#         self.prog = progress.getProgress(os.path.basename(filename),
#                                           progress.DEFINITE)
#         scriptloader.ScriptLoader.__init__(self, filename,
#                                            sys.modules['__main__'].__dict__)  
#     def progress(self, current, total):
#         self.prog.setFraction((1.0*current)/total)
#         if current <= total:
#             self.prog.setMessage("Read %d/%d lines" % (current, total))
#         else:
#             self.prog.setMessage("Done")
#     def stop(self):                     # called by ScriptLoader. Abort loop?
#         return self.prog.stopped()
#     def done(self):                     # called by ScriptLoader when finished
#         self.prog.finish()
#         scriptloader.ScriptLoader.done(self)

# def loadscript(menuitem, filename):
#     if filename is not None:
#         debug.fmsg('reading', filename, 'in thread',
#                    threadstate.findThreadNumber())
#         interp = PScriptLoader(filename)
#         interp.run()
#         debug.fmsg('finished reading', filename)
#         if runtimeflags.batch_mode and interp.error:
#             # If the interpreter raised an exception and we're in
#             # batch mode, the shell error status won't be set unless a
#             # new exception is raised here.  The old exception has
#             # already been handled by the time we get to this point.
#             raise ooferror.ErrUserError(
#                 "Script '%s' raised a %s exception: %s" %
#                 (filename, interp.error[0].__name__, interp.error[1]))

_loadmenu.addItem(OOFMenuItem(
    'Script',
    callback=loadscript,
    params=[filenameparam.ReadFileNameParameter('filename', 'logfile',
                                                tip="Name of the file.",
                                                ident="load")],
    no_log=1,
    ellipsis=1,
    threadable=oofmenu.THREADABLE_GUI,
    accel='l',
    help="Execute a Python script.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/loadscript.xml')
    ))

_startupmenu.addItem(OOFMenuItem(
    'Script',
    callback=loadscript,
    params=[filenameparam.ReadFileNameParameter('filename', 'logfile',
                                                tip="Name of the file.",
                                                ident="load")],
    no_log=1,
    ellipsis=1,
    threadable=oofmenu.THREADABLE_GUI,
    accel='l',
    disabled=config.nanoHUB(),  # loading arbitrary scripts is a
                                # security hole on nanoHUB
    help="Execute a Python script.",
#    post_hook=None,
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/loadscript.xml')
    ))

# "Data" files are distinguished from scripts in that they're not read
# by the Python interpreter directly, and therefore can't contain
# arbitrary Python code.  They can only contain menu commands from the
# OOF.LoadData menu.  The command arguments can be constants or
# variables and functions that are defined in the main OOF namespace,
# or lists and tuples thereof.

def loaddata(menuitem, filename):
    if filename is not None:
        from ooflib.common.IO import datafile
        debug.fmsg('loading', filename)
        datafile.readDataFile(filename, OOF.LoadData)
        debug.fmsg('done loading', filename)

_loadmenu.addItem(OOFMenuItem(
    'Data',
    callback=loaddata,
    threadable=oofmenu.THREADABLE,
    params=[filenameparam.ReadFileNameParameter('filename', ident="load",
                                                tip="Name of the file.")],
    ellipsis=1,
    help="Load a data file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/loaddatafile.xml')
    ))

_startupmenu.addItem(OOFMenuItem(
    'Data',
    callback=loaddata,
    threadable=oofmenu.THREADABLE,
    params=[filenameparam.ReadFileNameParameter('filename', ident="load",
                                                tip="Name of the file.")],
    ellipsis=1,
    help="Load a data file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/loaddatafile.xml')
    ))

OOF.addItem(oofmenu.OOFMenuItem(
    "LoadData", secret=1,
    help="Commands used in data files.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/loaddata.xml'),
    post_hook=None, # Don't include checkpoints in gui logs
    ))


def saveLog(menuitem, filename, mode):
    file = open(filename, mode.string())
    menuitem.root().saveLog(file)
    file.close()

_savemenu = _filemenu.addItem(
    OOFMenuItem('Save', help='Create data files and scripts.'))

_savemenu.addItem(OOFMenuItem(
    'Python_Log',
    callback=saveLog,
    ordering=10,
    params=[filenameparam.WriteFileNameParameter('filename', ident="load",
                                                 tip="Name of the file."),
            filenameparam.WriteModeParameter('mode')],
    accel='s',
    ellipsis=1,
    no_log=1,
    help="Save the current session as a Python script.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/savelog.xml')
    ))

#################################

def quitCmd(menuitem):
    from ooflib.common import quit
    quit.quit()

_filemenu.addItem(OOFMenuItem(
    'Quit',
    callback=quitCmd,
    accel='q',
    help="Don't give up so easily!",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/quit.xml'),
    threadable = oofmenu.UNTHREADABLE,
    no_log=1
    )) 

##################################

settingsmenu = OOF.addItem(OOFMenuItem(
    'Settings',
    help="Global settings",
    discussion="""
    <para>
    Commands for setting parameters that don't belong anywhere else.
    </para>"""))

fontmenu = settingsmenu.addItem(OOFMenuItem(
    "Fonts",
    help="Set fonts used in the GUI."
    ))

def setFont(menuitem, fontname):
    switchboard.notify('change font', fontname)

fontmenu.addItem(OOFMenuItem(
    "Widgets",
    callback=setFont,
    params=[parameter.StringParameter('fontname', tip="The name of a font.")],
    help="Set the font to use for labels, menus, buttons, etc. in the graphical user interface.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/widgetfont.xml')
    ))

def setFixedFont(menuitem, fontname):
    switchboard.notify('change fixed font', fontname)

fontmenu.addItem(OOFMenuItem(
    "Fixed",
    callback=setFixedFont,
    params=[parameter.StringParameter('fontname', tip='The name of a font.')],
    help="Set the fixed-width font to use in text displays.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/textfont.xml')
    ))

def setTheme(menuitem, theme):
    switchboard.notify('change theme', theme)

settingsmenu.addItem(OOFMenuItem(
    "Theme",
    callback=setTheme,
    params=[parameter.StringParameter('theme',
                                      tip="The name of a gnome theme.")],
    help="Set the look and feel of the graphical user interface.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/theme.xml')
    ))

bufsizemenu = settingsmenu.addItem(OOFMenuItem(
    "UndoBuffer_Size",
    help="Set the size of history buffers."))

gfxdefaultsmenu = settingsmenu.addItem(OOFMenuItem(
    "Graphics_Defaults",
    help="Set various default parameters for graphics displays.",
    discussion="""<para>

    This menu contains commands for setting the default values of
    various parameters controlling how things are displayed in the
    graphics window.  Put these commands into your &oof2rc; file
    to set defaults for every &oof2; session.

    </para>"""))
gfxdefaultsmenu.addItem(OOFMenuItem(
    "Pixels",
    ordering=1,
    help="Set default parameters for displaying pixels.",
    discussion="""<para>

    This menu contains commands for setting the default values of
    various parameters controlling how pixels (from &images; and
    &micros;) are displayed in the graphics window.  Put
    these commands into your &oof2rc; file
    to set defaults for every &oof2; session.

    </para>"""))
gfxdefaultsmenu.addItem(OOFMenuItem(
    "Skeletons",
    ordering=2,
    help="Set default parameters for displaying Skeletons.",
    discussion="""<para>

    This menu contains commands for setting the default values of
    various parameters controlling how &skels; and &skel;
    components are displayed in the graphics window.  Put these
    commands into your &oof2rc; file
    to set defaults for every &oof2; session.

    </para>"""))
gfxdefaultsmenu.addItem(OOFMenuItem(
    "Meshes",
    ordering=3,
    help="Set default parameters for displaying Meshes.",
    discussion="""<para>

    This menu contains commands for setting the default values of
    various parameters controlling how &meshes; and &mesh;
    components are displayed in the graphics window.  Put these
    commands into your &oof2rc; file
    to set defaults for every &oof2; session.

    </para>"""))

import random
from ooflib.SWIG.common import crandom

def _randomseed(menuitem, seed):
    random.seed(seed)
    crandom.rndmseed(seed)

settingsmenu.addItem(oofmenu.OOFMenuItem(
        'Random_Seed',
        callback=_randomseed,
        params=[parameter.IntParameter('seed', 17)]
        ))


##################################

## Subwindows menu.

_windowmenu = OOFMenuItem(
    'Windows',
    help="Menus for opening and raising windows.")
OOF.addItem(_windowmenu)

def dummy(menuitem): pass   # Dummy callback, so trivial menu items get logged.

## TODO OPT: Put the program name in a central location.  This "if" is
## done in a bunch of places.
if config.dimension() == 2:
    mainwindowname = "OOF2"
else:
    mainwindowname = "OOF3D"

# Add an entry for the main window, which, when clicked, raises it.
_windowmenu.addItem(OOFMenuItem(
    mainwindowname,
    callback=dummy,
    help="Raise the main %s window." % mainwindowname,
    discussion="""<para>
    Every &oof2; subwindow has this menu available. It's a good way to
    locate the main &oof2; window, if it's out of sight.
    </para>"""))

# The Console is a no-op in text mode.

def consolation(menuitem):
    print "There, there, I'm sure everything will be fine."

_windowmenu.addItem(OOFMenuItem(
    'Console',
    callback=consolation,
    help="Open or raise the Python console interface.",
    no_log=1,
    disabled=config.nanoHUB(),  # executing arbitrary python is a
                                # security hole on nanoHUB.
    discussion="""<para>
    The &oof2; <link linkend='Section:Windows:Console'>Console</link>
    provides a way of executing arbitrary Python code while running
    &oof2; in graphics mode.
    </para>"""))

##################

_graphicsmenu = OOFMenuItem(
    'Graphics',
    help="Graphical display of &oof2; objects.",
    discussion="""<para>
    Graphics windows are discussed in <xref
    linkend='Chapter:Graphics'/>.
    </para>""" )

def openGfx(menuitem):
    # debug.fmsg()
    window = gfxManager.openWindow()
    
_graphicsmenu.addItem(OOFMenuItem("New",
                                  callback=openGfx,
                                  help="Open a new graphics window.",
                                  accel='g',
                                  discussion="<para>Create a new <link linkend='Chapter:Graphics'>Graphics Window</link>.</para>"))

_windowmenu.addItem(_graphicsmenu)

_windowmenu.addItem(OOFMenuItem(
    'Layer_Editor',
    callback=dummy,
    help="Open or raise the Layer Editor window.",
    discussion="""<para>
Raise the <link linkend='Section:Graphics:LayerEditor'>Layer
Editor</link> window, if it has already been opened. If not, open it.
</para>"""
    ))

_windowmenu.addItem(OOFMenuItem(
    'Activity_Viewer',
    callback=dummy,
    help="Open or raise the Activity Viewer window.",
    discussion="""<para>
Raise the <link linkend='Section:Windows:ActivityViewer'>Activity
Viewer</link> window, if it is open. If not, open it.
</para>"""
    ))

#################################

## Help menu

helpmenu = OOF.addItem(OOFMenuItem('Help', help_menu=1))

debugmenu = helpmenu.addItem(OOFMenuItem(
    'Debug',
    discussion=
    """
<para>Tools for figuring out what's going on when it's not going well.
Mostly of interest to the developers.</para>
"""
    ))

def set_debug(menuitem, state):
    if state:
        debug.set_debug_mode()
    else:
        debug.clear_debug_mode()
        
debugmenu.addItem(CheckOOFMenuItem(
    'Debug',
    debug.debug(),
    callback=set_debug,
    help='Turn debugging mode on and off.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/debug.xml')
    ))

debugmenu.addItem(CheckOOFMenuItem(
    'Verbose_Switchboard',
    switchboard.switchboard.verbose,
    callback=switchboard.verbose,
    help='Print all switchboard calls as they occur.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/verbosesb.xml')
    ))

if config.debug():
    # Debug data dump functions are only defined if the C++ code was
    # built in DEBUG mode.
    def _openDebugFile(menuitem, prefix):
        filename = "%s-%d" % (prefix, os.getpid())
        cdebug.openDebugFile(filename)

    def _closeDebugFile(menuitem):
        cdebug.closeDebugFile()

    dumpmenu = debugmenu.addItem(OOFMenuItem('DataDump'))
    dumpmenu.addItem(OOFMenuItem(
            "Open",
            _openDebugFile,
            params=[parameter.StringParameter("prefix")],
            help="Save debugging information in a file."))

    dumpmenu.addItem(OOFMenuItem(
            "Close",
            _closeDebugFile,
            help="Stop saving debugging information."))

def setWarnPopups(menuitem, value):
    reporter.messagemanager.set_warning_pop_up(value)

helpmenu.addItem(CheckOOFMenuItem(
    'Popup_warnings',1,
    ordering=-8,
    callback=setWarnPopups,
    help="Display warnings in a pop-up window or just in the message window?",
    discussion="""<para>
    If <command>Popup_warnings</command> is true, warning messages
    will appear in an annoying pop-up window.  If it's false, they'll
    appear only in the <link
    linkend='Section:Windows:Messages'>Messages</link> window.
    </para>"""))

## TODO 3.1: Remove No_Warnings.  Instead, add Warning_Mode, which can be
## set to IGNORE, NOTIFY, or FATAL.

def setWarnErrors(menuitem, value):
    reporter.messagemanager.set_warning_error(value)

helpmenu.addItem(CheckOOFMenuItem(
    'No_Warnings', 0,
    ordering=-7,
    callback=setWarnErrors,
    help="Treat warnings as errors.",
    discussion="""
<para> If <command>No_Warnings</command> is true, warning messages are
treated as errors and will abort the current calculation.</para>
"""))

# def testBars1(menuitem):
#     import time
#     prog = progress.getProgress("main", progress.DEFINITE)
#     yprog = progress.getProgress("why", progress.DEFINITE)
#     xmax = 100
#     ymax = 10000
#     for x in xrange(xmax+1):
# #        reporter.report("x=", x)
#         time.sleep(0.1)
#         prog.setMessage("xprog: " + `xmax-x`)
#         prog.setFraction(float(x)/xmax)
#         if prog.stopped():
#             break
#         for y in xrange(ymax+1):
#             yprog.setMessage("yprog: " + `x` + '/' + `y`)
#             yprog.setFraction(float(y)/ymax)
#             if yprog.stopped():
#                 break
#     yprog.finish()
#     prog.finish()

# def testBars2(menuitem):
#     import time
#     from ooflib.SWIG.common import progress
#     prog = progress.getProgress("main", progress.INDEFINITE)
#     xmax = 1000
#     for x in xrange(xmax):
# #        reporter.report("x=", x)
#         time.sleep(0.1)
#         prog.setMessage("testBars: " + `x`)
#         prog.pulse()
#         if prog.stopped():
#             break
#     prog.finish()

# debugmenu.addItem(OOFMenuItem('Bar1', callback=testBars1))
# debugmenu.addItem(OOFMenuItem('Bar2', callback=testBars2))

####################################

## Profiling functions, in the Debug menu

profmenu = debugmenu.addItem(OOFMenuItem('Profile'))
prof = None

def profile_start(menuitem, filename, fudge):
    global prof
##    import hotshot
##    prof = hotshot.Profile(filename)
##    prof.start()
    if thread_enable.enabled():
        reporter.warn(
            "Multithreaded profiling is unreliable!\n"
            "Use the --unthreaded startup option.")
    from ooflib.common.EXTRA import profiler
    prof = profiler.Profiler(filename, fudge=fudge)

def profile_stop(menuitem):
    global prof
    prof.stop()
##    prof.close()
    prof = None
    
profmenu.addItem(OOFMenuItem(
    'Start',
    callback=profile_start,
    threadable = oofmenu.UNTHREADABLE,
    params=[StringParameter('filename', 'prof.out', tip="File name."),
            FloatParameter('fudge', 2.89e-6, tip="Fudge factor.")],
    help="Begin measuring execution time.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/profileStart.xml')
    ))
    
profmenu.addItem(OOFMenuItem(
    'Stop',
    callback=profile_stop,
    threadable = oofmenu.UNTHREADABLE,
    help="Stop measuring execution time.",
    discussion="""<para>
Stop profiling, and save the data in the file specified in
<xref linkend='MenuItem:OOF.Help.Debug.Profile.Start'/>.</para>"""
                             ))

def proffudge(menuitem, iterations):
    from ooflib.common.EXTRA import profiler
    fudge = profiler.calibrate_profiler(iterations)
    helpmenu.Debug.Profile.Start.get_arg('fudge').value = fudge
    reporter.report('fudge =', fudge)

profmenu.addItem(OOFMenuItem(
    'FudgeFinder',
    callback=proffudge,
    threadable = oofmenu.UNTHREADABLE,
    params=[IntParameter('iterations', 1000, tip="Number of iterations.")],
    help='Find the factor to compensate for time spent in the profiler itself.',
    discussion="""
    <para>Find the machine dependent fudge factor that the profiler
    uses to compensate for function calling overhead in the profiler
    itself, by measuring how long it takes to call the profiler
    <varname>iterations</varname> times.  </para>
    """
    ))




####################################

## The following functions are visible only if --debug is provided on
## the command line at start up.  Users shouldn't be interested in
## them.  Some of them *are* used in the test suites, so the functions
## have to be present even if --debug isn't used.

def _noop(menuitem):
    pass

debugmenu.addItem(OOFMenuItem('NoOp', no_doc=True,
                              secret=not debug.debug(),
                              callback=_noop))

errmenu = debugmenu.addItem(OOFMenuItem('Error', no_doc=1, 
                                        secret=not debug.debug()))


def _warning(menuitem):
        reporter.warn("You'd better be home by 11, young lady!")

errmenu.addItem(OOFMenuItem('Warning', callback=_warning,
                            help='Actual numbers may vary.'))

from ooflib.SWIG.common import cdebug
def _segfault(menuitem, delay):
    cdebug.segfault(delay)

errmenu.addItem(OOFMenuItem('SegFault', callback=_segfault,
                             threadable=oofmenu.THREADABLE,
                             params=[IntParameter('delay', 10,
                                                  tip="Delay time.")],
                             help='For external use only.  Slippery when wet.'))

def _pyerror(menuitem):
    debug.fmsg()
    raise RuntimeError("Oops!")

errmenu.addItem(OOFMenuItem('PyError', callback=_pyerror,
                             threadable=oofmenu.THREADABLE,
                             help='Do not taunt PyError.'))

def _cerror(menuitem):
    debug.fmsg()
    cdebug.throwException()

errmenu.addItem(OOFMenuItem('CError', callback=_cerror,
                             threadable=oofmenu.THREADABLE))

def _cpyerror(menuitem):
    debug.fmsg()
    cdebug.throwPythonException()

errmenu.addItem(OOFMenuItem('CPyError', callback=_cpyerror,
                            threadable=oofmenu.THREADABLE))

def _cpycerror(menuitem):
    debug.fmsg()
#     menuitem = None
    cdebug.throwPythonCException()

errmenu.addItem(OOFMenuItem("CPyCError", callback=_cpycerror,
                            threadable=oofmenu.THREADABLE))


def loop(menuitem):
    while 1:
        pass
    debug.fmsg("What am I doing here?")

errmenu.addItem(OOFMenuItem('Infinite_Loop', callback=loop,
                             threadable=oofmenu.THREADABLE,
                             help="I hope you have lots of time."))

def spinCycle(menuitem, nCycles):
    cdebug.spinCycle(nCycles)

debugmenu.addItem(OOFMenuItem('SpinCycle', callback=spinCycle,
                              params=[IntParameter('nCycles', 100000)]))

import os
from ooflib.SWIG.common import lock
import time

rw = lock.RWLock()

lockmenu = debugmenu.addItem(OOFMenuItem("LockTest", no_doc=True,
                                         secret=not debug.debug()))

def _py_read(menuitem, seconds):
    global rw
    rw.read_acquire()
    print "Got read permission for %d seconds." % seconds
    time.sleep(seconds)
    print "Releasing read."
    rw.read_release()

def _py_write(menuitem, seconds):
    global rw
    rw.write_acquire()
    print "Got write permission for %d seconds." % seconds
    time.sleep(seconds)
    print "Releasing write."
    rw.write_release()

lockmenu.addItem(
    OOFMenuItem(
        'RWLock_read', callback=_py_read,
        no_doc=1,
        threadable=oofmenu.THREADABLE,
        params=[IntParameter('seconds', 10,
                             tip="Sleeping time.")],
        help='Safe when used as directed.  For entertainment purposes only.'))

lockmenu.addItem(
    OOFMenuItem(
        'RWLock_write', callback=_py_write,
        no_doc=1,
        threadable=oofmenu.THREADABLE,
        params=[IntParameter('seconds', 10,
                             tip="Sleeping time.")],
        help='Packaged by weight, contents may settle during shipping.')
    )


def _wait(menuitem, seconds):
    cdebug.wait(seconds)

lockmenu.addItem(OOFMenuItem('Wait', callback=_wait,
                             no_doc=1,
                             threadable=oofmenu.THREADABLE,
                             params=[IntParameter('seconds', 10,
                                                  tip="Waiting time.")],
                             help='For internal use only.'))


def _random(menuitem, n):
    for i in xrange(n):
        print >> sys.stderr, crandom.rndm()

debugmenu.addItem(OOFMenuItem(
        'Random',
        callback=_random,
        params=[IntParameter('n', 10, tip='How many')],
        secret=not debug.debug(),
        help='For debugging'))


def _doublevectest(menuitem):
    from ooflib.SWIG.common import doublevec
    doublevec.printVecSizes("initial")
    d = doublevec.DoubleVec(10)
    doublevec.printVecSizes("allocated")
    d.resize(100)
    doublevec.printVecSizes("resized")
    dd = d.clone()
    doublevec.printVecSizes("cloned")
    d.clear()
    doublevec.printVecSizes("cleared")
    del d
    doublevec.printVecSizes("deleted")
    del dd;
    doublevec.printVecSizes("deleted again")

debugmenu.addItem(OOFMenuItem(
    'DoubleVec',
    callback=_doublevectest,
    secret=not debug.debug()))
