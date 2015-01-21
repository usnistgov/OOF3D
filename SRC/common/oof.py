# $RCSfile: oof.py,v $
# $Revision: 1.203.2.21 $
# $Author: langer $
# $Date: 2014/11/05 16:54:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import sys, os, types, string, random, code

## TODO OPT: Replace all expressions like 
##    if dictionary.has_key(x):
## with
##    if x in dictionary:
## and replace
##    for x in dictionary.keys():
## with
##    for x in dictionary:
## The new methods are faster in modern versions of python.
##
## Also, replace
##    try:
##       dictionary[key].append(item)
##    except KeyError:
##       dictionary[key] = [item]
## with
##    dictionary.setdefault(key, []).append(item)


# g++ code won't correctly resolve dynamic casts in shared libraries
# unless RTLD_GLOBAL is set when the library is loaded.  See
# http://gcc.gnu.org/faq.html#dso.  This must be done before any other
# oof modules are loaded.
try:
    sys.setdlopenflags(0x101)          # RTLD_GLOBAL (0x100) | RTLD_LAZY (0x001)
except AttributeError:
    pass

# The following calls initialize elements of the C++/Python interface,
# and must done before anything else that might call OOF C++ code.
# threadstate.py must be imported on the main thread before it's
# imported on any other thread.
from ooflib.SWIG.common import threadstate
# switchboard is used for communication between modules
import ooflib.SWIG.common.switchboard

# utils must be imported next because it inserts some code into
# __builtins__.
from ooflib.common import utils


# These can be imported in any order.
from ooflib.SWIG.common import config
from ooflib.SWIG.common import crandom
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
from ooflib.common import autoload
from ooflib.common import debug
from ooflib.common import garbage
from ooflib.common import mainthread
from ooflib.common import oof_getopt as getopt
from ooflib.common import oofversion
from ooflib.common import parallel_enable
from ooflib.common import runtimeflags
from ooflib.common import subthread
from ooflib.common import thread_enable
from ooflib.common.IO import automatic
from ooflib.common.IO import progressbar
from ooflib.common.IO import reporter

########################################

# Option processing:

# Recognized OOF options are processed and removed from sys.argv by
# the remove_option function.  Special options are provided for
# passing arguments through to some oof dependencies.  These work like
# "--non_oof_options="--non_oof_opt1 ...".  We also use a custom
# version of getopt, where unrecognized options are NOT AN ERROR --
# they remain in sys.argv, and may be consumed by various dependencies
# (in particular, mpi, but also gtk).  This subsequent processing may
# result in error messages which appear to come from OOF, but actually
# originate with dependencies.

def remove_option(item, argument=None):
    # item is the *full* name of an option, but it may not be spelled
    # out in full in sys.argv.  It also may have =argument appended to it
    # in sys.argv.  Look for the possible matches.
    for i in range(len(sys.argv)):
        if item.startswith(sys.argv[i].split('=')[0]):
            if argument is None:
                del sys.argv[i]
                return
            if '=' in sys.argv[i] and sys.argv[i].split('=',1)[1] == argument:
                del sys.argv[i]
                return
            if i+1 < len(sys.argv) and sys.argv[i+1] == argument:
                del sys.argv[i]
                del sys.argv[i]
                return
    # This should never happen.  getopt has already checked that the
    # options are well formed, so there should be nothing
    # unrecognizable in the list.
    raise ooferror.ErrPyProgrammingError("Failed to remove option: %s %s" %
                                         (item, argument))

def state_options_and_quit():
    main_options_string= """
This is %(name)s version %(version)s.

Usage: %(name)s [options]
The options are:
option      argument    description
--------------------------------------------------------------
--text                   Turn off graphics mode
--help                   Display valid options and exit
--version                Display version number and exit
--gtk=      gtk options  Extra options for graphics mode
--geometry  <width>x<height>  Size of the initial %(name)s window
--seed=     integer      Provide a random number seed
--quiet                  Quit quietly when done
--batch                  Quit immediately after running scripts (implies --text)
--autoload               Automatically load everything in the EXTENSIONS directory""" \
    % {'name':program_name, 'version':oofversion.version}

    devel_options_string = """
--parallel               Start-up parallel processing mode """

    data_options_string = """
    
The following options may be present more than once:
--script=    file         Load a script
--image=     file         Load an image
--data=      file         Load a data file
--command=   string       Execute the string as a Python command
--import=    module       Import a python extension module
--pathdir=   directory    Add a directory to the Python path
Extension modules are loaded first, and then the script, image, and
data files are loaded in the order that they are specified."""

    debug_options_string = """
The following options are for debugging:
--debug                  Turn on debugging mode
--record=   logfile      Save gui logging data
--rerecord= logfile      Read and re-record a gui log file 
--replay=    file        Load a gui log file (may be present more than once)
--replaydelay = integer  Time (in ms) between commands when replaying gui logs
--no-checkpoints         Ignore checkpoints in gui log files when replaying
--no-bars                Don't display progress bars
--no-rc                  Don't load .%src
--unthreaded             Don't use multiple execution threads
""" % program_name
    print main_options_string,
    if config.devel()>=1:
        print devel_options_string,
    print data_options_string
    print debug_options_string
    sys.exit(1)

def state_version_and_quit():
    print "This is %s version %s." % (program_name, oofversion.version)
    sys.exit(1)

##

# Other options are in runtimeflags.py.  If the options defined here
# have to be accessible in other modules, then they too should be
# moved to runtimeflags.py.
startupfiles = []
startupimports = []
gtk_options = None
randomseed = None
help_mode = False
version_mode = False
replaydelay = None
no_checkpoints = False
no_rc = False

def process_inline_options():
    # Defaults for option switches.
    global gtk_options
    global help_mode
    global record
    global replaydelay
    global randomseed
    global startupfiles
    global startupimports
    global version_mode
    global no_checkpoints
    global no_rc
    option_list = ['text', 'help', 'version', 'quiet', 'batch', 'no-rc',
                   'gtk=', 'unthreaded', 'socket=', 'script=', 'seed=',
                   'data=', 'image=', 'import=', 'debug', 'command=',
                   'record=', 'rerecord=', 'replay=', 'replaydelay=',
                   'pathdir=', 'no-checkpoints', 'autoload', 'geometry=',
                   'surface', 'no-bars']
    if config.enablempi():
        option_list += ['parallel']
    try:
        (optlist, args) = getopt.getopt(sys.argv[1:], '', option_list)
    except getopt.error, message:
        # Malformed arguments have been found.  Exit.
        print message
        state_options_and_quit()
    for opt in optlist:
        if opt[0] == '--gtk':
            gtk_options = opt[1]
            remove_option(opt[0],opt[1])
        elif opt[0] == '--parallel':
            parallel_enable.set(True)
            remove_option(opt[0])
        elif opt[0] in ('--unthreaded',):
            thread_enable.set(False)
            lock.disableLocks()
            remove_option(opt[0])
        elif opt[0] in ('--text',):
            runtimeflags.text_mode = True 
            remove_option(opt[0])
        elif opt[0] in ('--help',):
            help_mode = True
            remove_option(opt[0])
        elif opt[0] in ('--version',):
            version_mode = True
            remove_option(opt[0])
        elif opt[0] in ('--script',):
            startupfiles.append(StartUpScript(opt[1]))
            remove_option(opt[0],opt[1])
        elif opt[0] in ('--command',):
            startupfiles.append(StartUpCommand(opt[1]))
            remove_option(opt[0], opt[1])
        elif opt[0] in ('--image',):
            startupfiles.append(StartUpImage(opt[1]))
            remove_option(opt[0],opt[1])
        elif opt[0] in ('--data',):
            startupfiles.append(StartUpData(opt[1]))
            remove_option(opt[0],opt[1])
        elif opt[0] in ('--import',):
            startupimports.append(opt[1])
            remove_option(opt[0], opt[1])
        elif opt[0] in ('--debug',):
            debug.set_debug_mode()
            remove_option(opt[0])
        elif opt[0] in ('--record',):
            startupfiles.append(StartUpRecord(opt[1]))
            remove_option(opt[0], opt[1])
        elif opt[0] in ('--rerecord',):
            startupfiles.append(StartUpRerecord(opt[1]))
            remove_option(opt[0], opt[1])
        elif opt[0] in ('--replay',):
            startupfiles.append(StartUpReplay(opt[1]))
            remove_option(opt[0], opt[1])
        elif opt[0] in ('--replaydelay',):
            replaydelay = opt[1]
            remove_option(opt[0], opt[1])
        elif opt[0] in ('--no-checkpoints',):
            no_checkpoints = True
            remove_option(opt[0])
        elif opt[0] in ('--geometry',):
            runtimeflags.geometry = opt[1]
            remove_option(opt[0], opt[1])
        elif opt[0] in ('--no-rc',):
            no_rc = True
            remove_option(opt[0])
        elif opt[0] in ('--pathdir',):
            sys.path.append(opt[1])
            remove_option(opt[0], opt[1])
        elif opt[0] in ('--quiet',):
            from ooflib.common import quit
            quit.set_quiet()
            remove_option(opt[0])
        elif opt[0] in ('--batch',):
            runtimeflags.batch_mode = True
            runtimeflags.text_mode = True
            progressbar.suppressProgressBars()
            remove_option(opt[0])
        elif opt[0] in ('--no-bars',):
            progressbar.suppressProgressBars()
            remove_option(opt[0])
        elif opt[0] in ('--surface',):
            runtimeflags.surface_mode = True
            remove_option(opt[0])
        elif opt[0] in ('--autoload',):
            autoload.autoload = True
            remove_option(opt[0])
        elif opt[0] == '--seed':
            randomseed = int(opt[1])
            remove_option(opt[0],opt[1])
    if help_mode:
        state_options_and_quit()
    if version_mode:
        state_version_and_quit()

    if gtk_options :
        if not (runtimeflags.text_mode or config.no_gui()):
            sys.argv.extend(gtk_options.split())
            ## gtk commands are eaten upon importing module
        else:
            ## send warning message that --gtk was selected and --text was not
            print "gtk options are ignored in text mode"
    else:
        import ooflib.SWIG.common.argv
        ooflib.SWIG.common.argv.init_argv(sys.argv[1:])
    
    
        
## ######### Notes to ALL developers ######### 
## front_end() is the old run() in serial mode 
##
## If oof is compiled with an MPI implementation and --parallel is selected
## mpi is initialized at run time.
##
## If MPI was compiled but you run oof as you usually
## do, then only the front end is loaded and the back_end()
## remains *dormant*. MPI will be initialized.
##
## If MPI was not compiled, only the front end
## runs and everything works as usual. MPI will not be initialized.
##
## oof runs in parallel by typing:
##
## mpirun -np <N> <more MPI options> oof2 --graphics --parallel <more oof options>
##
## where <N> is the number of processors.
##
## if <N> > 1:
## the back end is loaded, and the new virtual machine
## waits for instructions to be executed.
## If <N> == 1 oof will run as usual, and the back end
## will NOT be loaded.

        
def front_end(no_interp=None):
    global startupfiles
    global gtk_options
    global randomseed
    ## From here on is the serial version.

    # When loading modules, use utils.OOFexec so that names are
    # imported into the oof environment, not the oof.run environment.
    if not (runtimeflags.text_mode or config.no_gui()):
	# The gtk import dance described below doesn't work when the program
        # has been packaged by cx_freeze.
        # TODO 3.1: is checking frozen required for gtk2?
        frozen = hasattr(sys, 'frozen')
	if not frozen:
            import pygtk
            pygtk.require("2.0")
            import gtk
            msg = gtk.check_version(2, 6, 0)
            if msg:
                print msg
                sys.exit(3)

        # The GUI initialization modules must be called before any
        # calls to mainthread.run(), because mainthread.run() is
        # redefined when mainthreadGUI.py is loaded (by
        # common/IO/GUI/initialize.py)
        import ooflib.common.IO.GUI.initialize
        import ooflib.engine.IO.GUI.initialize
        import ooflib.image.IO.GUI.initialize
        import ooflib.orientationmap.GUI.initialize
        import ooflib.tutorials.initialize

        if replaydelay is not None:
            from ooflib.common.IO.GUI import gtklogger
            gtklogger.set_delay(int(replaydelay))
    else:                               # text mode
        # Load non-gui initialization modules.
        import ooflib.common.initialize
        import ooflib.engine.initialize
        import ooflib.image.initialize
        import ooflib.orientationmap.initialize

    import ooflib.EXTENSIONS.initialize

    # The random number generator must be seeded *after* the gui has
    # been started, because libfontconfig is using random numbers.  We
    # want the numbers to be the same in text and gui modes, so that
    # the test suite gets predictable answers.
    if debug.debug() or randomseed is not None:
        if randomseed is None:
            randomseed = 17
        random.seed(randomseed)
        crandom.rndmseed(randomseed)

    for module in startupimports:
        exec('import ' + module)

    if not (runtimeflags.text_mode or config.no_gui()):
        reporter.report("Welcome to %s version %s!" % (program_name.upper(), 
                                                       oofversion.version))
        if not no_interp: # Default case, run on local thread.
            from ooflib.common.IO.GUI import oofGUI
            oofGUI.start(files=startupfiles) # This call never returns.
            print "This line should never be printed.  rank =", _rank
        else:
            # TODO 3.1: The gui and no_interp combination is
            # thinkable, but has problems.  You have to run the GUI on
            # a separate thread, but then exceptions show up as modal
            # dialog boxes in the GUI, and block the menu items which
            # raised them, causing a loss of control.  Also, the
            # current threading scheme requires that all gtk activity
            # happen on the main thread.
            print "GUI no_interp mode not implemented.  Sorry."
            raise NotImplementedError("GUI no_interp mode")
            
    else:                               # text mode
        from ooflib.common import quit
        # Allow exceptions to propagate to the user if in batch mode
        # or not running an interpreter.  Otherwise, exceptions are
        # caught and reported to the user, but the program keeps
        # running.
        if runtimeflags.batch_mode or no_interp:
            from ooflib.common import worker
            worker.propagate_exceptions = True

        threadstate.textMode();
        lock.disableLocks()      # disables Locks, but not SLocks

        if startupfiles:
            loadStartUpFiles(startupfiles)
            if runtimeflags.batch_mode:
                # Batch mode runs startupfiles and quits immediately.
                quit.set_quiet()
                quit.quit()
                if sys.exc_info()[0] is not None:
                    sys.exit(1)
                sys.exit(0)
        # Format the banner for the current line width.
        if not quit.quiet():
            width = utils.screenwidth()
            wiggles = "//=*=\\\\=*="
            nwiggles = (width-2)/len(wiggles)
            welcome = "Welcome to %s version %s!" % (program_name.upper(),
                                                     oofversion.version)
            nblanks = (width - len(welcome))/2
            banner = (wiggles*nwiggles + "//\n\n" 
                      + " "*nblanks + welcome + "\n"
                      + string.join(
                    utils.format(banner1%{'name':program_name.upper()}, width),
                    "\n")
                      + "\n\n" +  wiggles*nwiggles + "//\n"
                      + string.join(
                    utils.format(banner2%{'name':program_name.upper()}, width),
                    "\n")
                      )
        else:
            banner = ""
            
        if not no_interp:
            import code
            # Try to import readline, which allows command line
            # editing in text mode.  If it's not there, don't worry --
            # it's possible to live without it.  Some systems don't
            # seem to have it, although it's supposedly available on
            # all Unix systems.
            try:
                import readline
            except ImportError:
                pass
            # Start up the interpreter in the __main__ namespace.
            # This is the namespace that utils.OOFeval and OOFdefine
            # use.  It's not necessarily *this* namespace.
            interp = code.InteractiveConsole(sys.modules['__main__'].__dict__)
            interp.interact(banner)

banner1 = """
%(name)s was written at the National Institute of Standards and Technology (NIST).
NIST assumes no responsibility for the operation, modification, or maintenance of %(name)s."""

banner2 = """
Type "OOF.Copyright()" to see the copyrights associated with %(name)s.
Type "OOF.Disclaimer()" to see the full disclaimer.
Type "OOF.Credits()" for a list of the authors.
Type "help()" for Python help."""

###########################

class StartUpFile:
    def __init__(self, filename):
        self.filename = filename
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.filename)

class StartUpScript(StartUpFile):
    def load(self):
        mainmenu.OOF.File.LoadStartUp.Script(filename=self.filename)

class StartUpScriptNoLog(StartUpFile):
    def load(self):
        mainmenu.OOF.haltLog()
        mainmenu.OOF.File.LoadStartUp.Script(filename=self.filename)
        mainmenu.OOF.resumeLog()

class StartUpCommand:
    def __init__(self, cmd):
        self.cmd = cmd
    def load(self):
        utils.OOFexec(self.cmd)

class StartUpImage(StartUpFile):
    def load(self):
        if config.dimension() == 2:
            basename = os.path.basename(self.filename)
            mainmenu.OOF.Microstructure.Create_From_ImageFile(
                filename=self.filename,
                microstructure_name=basename,
                height=automatic.automatic, width=automatic.automatic)
        else:
            # This is an ugly hack to import names from the image
            # module without explicitly importing the module.
            ## TODO OPT: there should be a plug-in mechanism for start up
            ## items and command line arguments, so that the whole
            ## StartUpImage class can be defined in the image module.
            ThreeDImageDirectory = utils.OOFeval('ThreeDImageDirectory')
            NumericalOrder = utils.OOFeval('NumericalOrder')
            # self.filename might have a trailing '/', which must be
            # removed.
            filename = os.path.normpath(self.filename)
            basename = os.path.basename(filename)
            mainmenu.OOF.Microstructure.Create_From_ImageFile(
                filenames=ThreeDImageDirectory(
                    directory=filename,
                    sort=NumericalOrder()),
                microstructure_name=basename,
                height=automatic.automatic, width=automatic.automatic,
                depth=automatic.automatic)

class StartUpData(StartUpFile):
    def load(self):
        mainmenu.OOF.File.LoadStartUp.Data(filename=self.filename)

class StartUpReplay(StartUpFile):
    def load(self):
        mainmenu.OOF.Help.Debug.GUI_Logging.Replay(
            filename=self.filename,
            checkpoints=not no_checkpoints)
        # TODO 3.1: It would be nice if we could have oof returning
        # the last line number being executed in the log file.  So
        # that we could check in the guitests if there are some extra
        # lines in the log file to be executed outside of oof scope.
        # (Wouldn't it be better to have a separate file to be loaded
        # after the test finishes?)

class StartUpRecord(StartUpFile):
    def load(self):
        mainmenu.OOF.Help.Debug.GUI_Logging.Record(
            filename=self.filename,
            use_gui=True)
        #ToChange

class StartUpRerecord(StartUpFile):
    def load(self):
        mainmenu.OOF.Help.Debug.GUI_Logging.Rerecord(
            filename=self.filename,
            checkpoints = not no_checkpoints)
        #ToChange

def loadStartUpFiles(files):
    # Files is a list of StartUpFile-like objects
    for phile in files:
        phile.load()

## Parallel stuff for the old attempt at MPI.

## identifiers and other global variables for parallel machine live here.

_rank = 0  # process ID
def start_parallel_machine():
    global _rank
    try:
        from ooflib.SWIG.common import mpitools
    except ImportError:
        pass
    else:
        mpitools.Initialize(sys.argv)
        _rank = mpitools.Rank()

## sockets initialization front and back end
def start_sockets_Front_End():
    if parallel_enable.enabled():
        try:
            from ooflib.SWIG.common import mpitools
        except ImportError:
            raise ooferror.ErrSetupError(
                "Parallel option requested, but parallel code not present.")
        from ooflib.common.IO import socket2me
        ## Tell back end what port to listen
        s_name = mpitools.Get_processor_name()
        s_address = socket2me.socketPort.getPort()
        mpitools.bcast_string("%i"%s_address, 0)
        mpitools.bcast_string(s_name, 0)
        ## Tell back end the number of processors on the back end
        socket2me.socketPort.connect(mpitools.Size()-1)
        
def start_sockets_Back_End():
    if parallel_enable.enabled():
        from ooflib.common.IO import socket2me
        from ooflib.SWIG.common import mpitools
        ## receive from front end what port to listen
        s_address = mpitools.recv_bcast_string(0)
        s_name = mpitools.recv_bcast_string(0)
        ## create a unique SocketInput object
        socket2me.makeSocketInput(s_name, int(s_address), mpitools.Rank())




# Main routine.  Takes a "no_interp" argument, which, if not None,
# suppresses running the command interpreter.  This is meant to be
# used by "enclosing" Python routines which import oof and want to
# issue commands to it.  The appropriate way to do this is:
# from ooflib.common import oof
# oof.run(no_interp=1)
# For the moment, this only works in text mode.


def run(no_interp=None):
    global _rank
    global startupfiles
    global program_name

    program_name = os.path.basename(sys.argv[0])
    process_inline_options()  # execute well-formed oof options

    # Look for .oof2rc or .oof3drc in the user's home directory.
    if not no_rc:
        oofrcpath = os.path.join(os.path.expanduser("~"), ".%src"%program_name)
        if os.path.exists(oofrcpath):
            startupfiles = [StartUpScriptNoLog(oofrcpath)]+startupfiles

    if (thread_enable.query()
        and not (runtimeflags.text_mode or config.no_gui())):
        # TODO OPT: Is this still necessary?
        garbage.disable()               # work-around for gtk bug?

    start_parallel_machine()  # start parallel suite (if available)

    if _rank == 0:
        if parallel_enable.enabled():
            from ooflib.SWIG.common import mpitools
            _size = mpitools.Size()
            mpitools.Isend_Bool(thread_enable.enabled(), range(1,_size))
            
        if parallel_enable.enabled():
            from ooflib.common.IO import socket2me

        if config.petsc():
            print "Going to InitPETSc"
            from ooflib.SWIG.engine.PETSc.petsc_solverdriver import InitPETSc
            InitPETSc(sys.argv)
            for s in sys.argv:
                print s

        start_sockets_Front_End()
        # Import mainmenu only *after* processing command line options, so
        # that the options can affect which menus are loaded.
        global mainmenu
        from ooflib.common.IO import mainmenu
        front_end(no_interp)  # all non-parallel menu items are executed here.
    else:
        # parallel back-end
        parallel_enable.set(True)  # notify back-end of its parallel status

        # thread status at the back-ends
        from ooflib.SWIG.common import mpitools
        thread_enable.set(mpitools.Recv_Bool(0))
        if not thread_enable.enabled():
            lock.disableLocks()
        
        if parallel_enable.enabled():
            from ooflib.common.IO import socket2me

        if config.petsc():
            print "Going to InitPETSc"
            from ooflib.SWIG.engine.PETSc.petsc_solverdriver import InitPETSc
            InitPETSc(sys.argv)
            for s in sys.argv:
                print s

        debug.set_debug_mode()  # set for debugging parallel mode
        from ooflib.common import quit
        quit.set_quiet() ## back-end exits quietly.
        start_sockets_Back_End()  # socket initialization
        from ooflib.common import backEnd  # import back end machine
        # The back end shouldn't run the gui!
        runtimeflags.text_mode = True
        backEnd.back_end()  # back-end awaits for your command
