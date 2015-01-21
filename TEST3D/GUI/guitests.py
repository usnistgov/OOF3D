# -*- python -*-
# $RCSfile: guitests.py,v $
# $Revision: 1.1.2.7 $
# $Author: fyc $
# $Date: 2014/09/23 15:35:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This file looks for all subdirectories of the current directory and
# runs the gui test contained in each one.  The tests are run in
# alphabetical order of the subdirectory name.  It is assumed that
# each subdirectory contains a file named "log.py".  The test is run by
# executing
#         oof3d --pathdir <subdirectory> --replay <subdirectory>/log.py
# and testing its return value. The subdirectory is added to the
# python path so that the log file can contain import statements that
# load tests from other files in the subdirectory.

# The subdirectory can contain a file called "args" which contains a
# single line of arguments to be added to the oof3d command.  It can
# also contain a file named 'cleanup.py' which will be run after the
# test, if the test is successful.  cleanup.py is run in the
# guitests.py environment.

# Any test that calls sys.exit() with an non-zero status is considered
# a failure.  If a test is *supposed* to return a non-zero status,
# that status should be put in a file called 'exitstatus' in the
# test subdirectory.

import getopt
import os
import shutil
import string
import sys
import tempfile
import imp

delaystr = None
debug = False
no_checkpoints = False
sync = False
unthreaded = False
forever = False
nocanvas = False

global tmpdir
tmpdir = None

def linkfile(homedir, filename):
    os.symlink(os.path.join(homedir, filename),
               os.path.join(tmpdir, filename))

def run_tests(dirs, rerecord, forever):
    homedir = os.getcwd()
    global tmpdir
    tmpdir = tempfile.mkdtemp(prefix='oof2temp_')
    print >> sys.stderr, "Using temp dir", tmpdir

    linkfile(homedir, 'examples')
    linkfile(homedir, 'TEST_DATA')
    os.symlink(os.path.abspath(os.path.join('..', 'UTILS')),
               os.path.join(tmpdir, 'UTILS'))
    os.chdir(tmpdir)
    try:
        if forever:
            counter = 0
            while 1:
                print >> sys.stderr, "******* %d ********" % counter
                counter += 1
                ok = really_run_tests(homedir, dirs, rerecord)
        else:
            really_run_tests(homedir, dirs, rerecord)
    except:
        print >> sys.stderr, "Not removing temp directory", tmpdir
        raise
    else:   # Successful execution. 
        pass
        # Remove everything from the temp directory.  There may be
        # *.pyc files left, as well as the subdirectories linked above,
        # even if everything ran correctly.
        for f in os.listdir(tmpdir):
            os.remove(f)
            # Remove the temp directory
        os.rmdir(tmpdir)

def really_run_tests(homedir, dirs, rerecord):
    nskipped = 0
    nrun = 0
    for dir in dirs:
        originaldir = os.path.join(homedir, dir)
        # Check that the directory and log file exist, and that
        # there's no SKIP file, before bothering to make the symlink
        # to the directory.
        if not os.path.isdir(originaldir):
            print >> sys.stderr, "Can't find directory", dir
            return
        if os.path.exists(os.path.join(originaldir, 'SKIP')) and len(dirs) > 1:
	    generalSkip = True
	    canvasSkip = False
	    globalSkip = False
	    #Add your filtering skip stuff here to False by default. generalSkip should be
	    #True by default.
	    with open(os.path.join(originaldir, 'SKIP'), mode='r', buffering=1) as skipfile:
	         for reason in skipfile:
		     if reason == "--canvas":
		        canvasSkip = True
		        generalSkip = False
		     
		     if reason == "--global":
		        globalSkip = True
		        generalSkip = False
	    if generalSkip or globalSkip:
	       print >> sys.stderr, " **** Skipping", dir, "****"
	       nskipped += 1
	       continue
	    if canvasSkip and nocanvas:
	       print >> sys.stderr, " **** Avoiding canvas interacting test", dir, "****"
	       nskipped += 1
               continue
        if not os.path.exists(os.path.join(originaldir, 'log.py')):
            print >> sys.stderr, " **** Skipping", dir, "(No log file!) ****"
            nskipped += 1
            continue

        # Ok, everything's there.  Get ready to run this test.  Make a
        # symlink to the test directory.
        ## TODO: Is the symlink really necessary? We could provide a
        ## full path to log.py.  The test directory is already putting
        ## into PYTHONPATH.
        testdir = os.path.join(tmpdir, dir)
        os.symlink(os.path.join(homedir, dir), testdir)

        # Read extra oof3d args from the args file, if it exists.
        if os.path.exists(os.path.join(dir, 'args')):
            argfile = open(os.path.join(dir, 'args'))
            extraargs = argfile.readline().rstrip()
            argfile.close()
        else:
            extraargs = ""
        # Read the expected exit status from the exitstatus file, if
        # it exists.
        if os.path.exists(os.path.join(originaldir, 'exitstatus')):
            exitstatfile = open(os.path.join(dir, 'exitstatus'))
            exitstatus = int(exitstatfile.readline())
            exitstatfile.close()
        else:
            exitstatus = 0
        
        global delaystr
        
        if delaystr:
            extraargs += " --replaydelay=" + delaystr
        if debug:
            extraargs += " --debug"
        if no_checkpoints:
            extraargs += " --no-checkpoints"
        if sync:
            extraargs += " --gtk=--sync"
        if unthreaded:
            extraargs += " --unthreaded"
        if rerecord:
            replayarg = 'rerecord'
        else:
            replayarg = 'replay'

        cmd = ("oof3d --pathdir . --pathdir %(test)s --pathdir %(home)s"
               " --pathdir UTILS --%(mode)s %(log)s %(extra)s" 
               % {"test" : dir, 
                  "home" : homedir,
                  "mode" : replayarg, 
                  "log" : os.path.join(dir, "log.py"),
                  "extra" : extraargs
                })
        print >> sys.stderr, "-------------------------"
        print >> sys.stderr, "--- Running %s" % cmd
        os.putenv('OOFTESTDIR', dir)
        result = os.system(cmd)
        if result != exitstatus*256: # os.system returns status in high byte
            print "Test", dir, "failed! Status =", result
            sys.exit(result)
        print >> sys.stderr, "--- Finished %s" % dir

        cleanupscript = os.path.join(dir, 'cleanup.py')
        if os.path.exists(cleanupscript):
            execfile(cleanupscript)

        os.remove(testdir)
        nrun += 1
          
    print >> sys.stderr, "%d test%s ran successfully!" % (nrun, "s"*(nrun!=1))
    print >> sys.stderr, "Skipped %d test%s." % (nskipped, "s"*(nskipped!=1))

excluded = ['CVS','TEST_DATA', 'examples']

def get_dirs():
    files = [f for f in os.listdir('.')
             if os.path.isdir(f) and f not in excluded]
    files.sort()
    return files

def checkdir(dir, dirs):
    if dir not in dirs:
        print >> sys.stderr, "There is no directory named", dir
        sys.exit(1)

def removefile(filename):
    fullname = os.path.normpath(os.path.join(tmpdir, filename))
    print >> sys.stderr, "Removing file", fullname
    if os.path.exists(fullname):
       os.remove(fullname)

def removefolder(pathname):
    if os.path.exists(pathname):
        shutil.rmtree(pathname)
    
if __name__ == '__main__':
    try:
        optlist, args = getopt.getopt(sys.argv[1:], '', 
                                      ['delay=', 'debug', 'nocanvas',
                                       'from=', 'after=', 'to=',
                                       'rerecord', 'no-checkpoints',
                                       'sync', 'unthreaded',
                                       'forever', 'help'])
    except getopt.error, message:
        print message
        sys.exit(1)
    fromdir = None
    afterdir = None
    todir = None
    rerecord = False
    nocanvas = False
    for opt in optlist:
        if opt[0] == "--debug":
            debug = True
        elif opt[0] == "--nocanvas":
            nocanvas = True
        elif opt[0] == "--delay":
            delaystr = opt[1]
        elif opt[0] == '--from':
            # normpath is necessary here because if the shell's
            # filename completion was used to construct the argument,
            # the directory name may have a trailing slash, and the
            # index() calls below will fail.
            fromdir = os.path.normpath(opt[1])
        elif opt[0] == '--after':
            afterdir = os.path.normpath(opt[1])
        elif opt[0] == '--to':
            todir = os.path.normpath(opt[1])
        elif opt[0] == '--rerecord':
            rerecord = True
        elif opt[0] == '--no-checkpoints':
            no_checkpoints = True
        elif opt[0] == '--unthreaded':
            unthreaded = True
        elif opt[0] == '--sync':
            sync = True
        elif opt[0] == '--forever':
            forever = True
        elif opt[0] == '--help':
            print >> sys.stderr, \
"""
Usage:  python guitests.py [options] [test directories]

Options are:
   --from=dir   Start tests at directory dir.
   --after=dir  Start tests at the first one following dir.
   --to=dir     End tests at directory dir.
   --delay=ms   Specify delay (in milliseconds) between lines of each test.
   --debug      Run tests in debug mode.
   --nocanvas   Skip all tests that have interact with the canvas.
   --unthreaded Run tests in unthreaded mode.
   --sync       Run tests in X11 sync mode (very slow over a network!).
   --rerecord   Re-record log files, and ignore 'assert' statements in them.
                This is useful if new checkpoints have been added.
   --no-checkpoints Ignore checkpoints in log files (not very useful).
   --forever    Repeat tests until they fail.
   --help       Print this message.
"""
            sys.exit(0)
            

    if args:         # test directories were explicitly listed on command line
        run_tests([os.path.normpath(a) for a in args], rerecord, forever)
    else:
        dirs = get_dirs()
        if afterdir:
            if fromdir:
                print >> sys.stderr, "You cannot use both --from and --after!"
                sys.exit(0)
            # Start at the directory following afterdir
            fromdir = dirs[dirs.index(afterdir)+1]

        if fromdir and not todir:
            checkdir(fromdir, dirs)
            start = dirs.index(fromdir)
            run_tests(dirs[start:], rerecord, forever)
        elif todir and not fromdir:
            checkdir(todir, dirs)
            end = dirs.index(todir)
            run_tests(dirs[:end+1], rerecord, forever)
        elif todir and fromdir:
            checkdir(fromdir, dirs)
            checkdir(todir, dirs)
            start = dirs.index(fromdir)
            end = dirs.index(todir)
            run_tests(dirs[start:end+1], rerecord, forever)
        else:                           # use all test directories
            run_tests(dirs, rerecord, forever)
                         
