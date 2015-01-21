# -*- python -*-
# $RCSfile: oof2setuputils.py,v $
# $Revision: 1.14.8.9 $
# $Author: langer $
# $Date: 2014/09/17 21:39:33 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# This file contains routines used by the main OOF2 setup.py script.
# These routines are also used by oof2extutils.py, which is used by
# the authors of external OOF2 extensions.

import os, sys, string, stat, time

# Utilities for running xxxxx-config programs that get the flags and
# libs required to link with external libraries.  "clib" is a CLibInfo
# object. "cmd" is a command to run that returns the required data,
# such as "Magick++-config --cflags".

def add_third_party_includes(cmd, clib):
    f = os.popen(cmd, 'r')
    for line in f.readlines():
        for flag in line.split():
            if flag[:2] == '-I':
                clib.includeDirs.append(flag[2:])
            else:
                clib.extra_compile_args.append(flag)

def add_third_party_libs(cmd, clib):
    f = os.popen(cmd, 'r')
    for line in f.readlines():
        for flag in line.split():
            if flag[:2] == '-l':
                clib.externalLibs.append(flag[2:])
            elif flag[:2] == '-L':
                clib.externalLibDirs.append(flag[2:])
            else:
                clib.extra_link_args.append(flag)

# Check for packages that use pkg-config for their options.  Include
# their compiler and linker flags if they're found, and complain if
# they're not.

def pkg_check(package, version, clib=None):
    if check_exec('pkg-config'):
        if os.system("pkg-config --atleast-version=%s %s" % (version, package)):
            print "Can't find %s! Version %s or later required" % (package,
                                                                   version)
            sys.exit()
        if clib:
            add_third_party_libs("pkg-config --libs %s" % package, clib)
            add_third_party_includes("pkg-config --cflags %s" % package, clib)
    else:
        print "Can't find pkg-config!"
        sys.exit()
    


# Check that an executable file exists in the environment's PATH.

pathdirs = os.getenv("PATH").split(":")

def check_exec(xfile):          # is xfile an executable file in the path?
    for dir in pathdirs:
        try:
            if os.path.exists(dir):
                files = os.listdir(dir)
                if xfile in files:
                    fullname = os.path.join(dir, xfile)
                    if os.access(fullname, os.X_OK):
#                         print >> sys.stderr, "Found", xfile, "as", fullname
                        return 1
        except: # Ignore permission errors
            pass
    if sys.platform == 'cygwin' and not xfile.endswith('.exe'):
        return check_exec(xfile + '.exe')
    print "Warning!", xfile, "not found!"

# See if a given file exists in a list of directories.  Return the
# directory containing the file, or None if the file can't be found.

def find_file(filename, dirs):
    for dir in dirs:
        if os.path.exists(os.path.join(dir, filename)):
            return dir

# Add dirs to the given path environment variable.

def extend_path(envpath, *dirs):
    try:
        pathstring = os.environ[envpath]
    except KeyError:
        path = []
    else:
        path = pathstring.split(':')
    # prepend directories to the path
    path[0:0] = [d for d in dirs if os.path.exists(d)]
    if path:
        os.environ[envpath] = ':'.join(path)
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

SWIG = 'swig'                           # must be swig 1.1 build 883
SWIGARGS = ["-shadow", "-dnone", "-python", "-c++", "-c"]

def run_swig(srcdir, swigfile, destdir, cext="_.C", include_dirs=[],
             dry_run=False, force=False, extra_args=[],
             with_swig=None, DIM_3=0):

    # srcdir is a directory.  swigfile is the name of the input swig
    # file, specfied *relative* to srcdir.  The output files will go
    # into destdir.  If swigfile has subdirectories as part of its
    # name, then those subdirectories will be created in destdir.  For
    # example, if srcdir is "A/B", swigfile is "C/swig.swg", and
    # destdir is "E/F", then the file "A/B/C/swig.swg" will be swigged
    # to create "E/F/C/swig_.C" and "E/F/C/swig.py".

    # cext is the extension to use on the output C++ file.

    swig = with_swig or SWIG

    srcdir = os.path.abspath(srcdir)
    destdir = os.path.abspath(destdir)
    relpath = os.path.split(swigfile)[0]
    infile = os.path.join(srcdir, swigfile)
    indir = os.path.join(srcdir, relpath)
    outdir = os.path.join(destdir, relpath)

    swigfilename = os.path.split(swigfile)[1]
    basename = os.path.splitext(swigfilename)[0]
    cfile = os.path.join(destdir, relpath, basename + cext)
    pyfile = os.path.join(destdir, relpath, basename + ".py")

    infiletime = os.stat(infile)[stat.ST_MTIME]
    uptodate = os.path.exists(cfile) and os.path.exists(pyfile) and \
               (os.stat(cfile)[stat.ST_MTIME] > infiletime) and \
               (os.stat(pyfile)[stat.ST_MTIME] > infiletime)

    if DIM_3 and "-DDIM_3" not in extra_args:
        extra_args.append("-DDIM_3")
    
    if force or not uptodate:

        # Make sure that outdir exists.
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        # Make sure that all directories from destdir to outdir
        #  contain __init__.py.
        destdepth = len(destdir.split(os.sep))
        outsplit = outdir.split(os.sep)[destdepth:]
        addInitPy(destdir)
        odir = destdir
        for subdir in outsplit:
            odir = os.path.join(odir, subdir)
            addInitPy(odir)

        incls = [os.path.abspath(dir) for dir in include_dirs]
        if srcdir not in incls:
            incls.append(srcdir)
        if indir not in incls:
            incls.append(indir)
        
        # The following command cds to the source directory and runs
        # swig.  It uses absolute path names for all of the
        # directories so that we don't have to worry about the effect
        # of the cd.  The cd is necessary because the swig
        # 'pragma(python) include' lines don't seem to respect the -I
        # flags.
        
        cmd = 'cd %(indir)s; %(swig)s %(swigargs)s %(includes)s -module %(module)s -o %(cfile)s %(infile)s' \
              %  {'indir' : indir,
                  'swig': swig,
                  'swigargs' : string.join(SWIGARGS+extra_args, " "),
                  'includes' : string.join(['-I'+file for file in incls], ' '),
                  'module' : basename,
                  'cfile' : cfile,
                  'infile' : infile}
        print cmd
        if not dry_run:
            ## TODO: Check the return status of cmd and raise an
            ## exception (abort?) if it failed.
            os.system(cmd)

    return dict(basename=basename,
                indir=indir,
                outdir=outdir,
                cfile=cfile
                )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def addInitPy(subdir):
    initpy = os.path.join(subdir, '__init__.py')
    if not os.path.exists(initpy):
        print >> sys.stderr, "Creating", initpy
        initfile = open(initpy, 'w')
        print >> initfile, "# This file no verb"
        initfile.close()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class InstallationFile:
    def __init__(self, stdout, stderr):
	self.filename = None
	self.saved = []
	self.stdout = stdout    # The original stdout
	self.stderr = stderr    # The original stderr
        sys.stderr = self
        sys.stdout = self
	self.file = None
        self.needHeader = False
        ## TODO: Add date and time to log file
    def __del__(self):
        self.close()
    def setFilename(self, filename):
	self.filename = filename
    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None
	sys.stdout = self.stdout
	sys.stderr = self.stderr
    def flush(self):
	if self.file is not None:
            self.file.flush()

    def mkdir(self):
        if self.filename is not None:
            head, tail = os.path.split(self.filename)
            if not os.path.exists(head):
                os.makedirs(head)
    def clear(self):
        if self.file is not None:
            self.file.close()
            self.file = None
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        self.saved = []
        self.needHeader = True

    def write(self, data):
        self.stdout.write(data)
        self.write_file(data)

    def write_file(self, data):
        if self.filename is not None and self.file is None:
            self.mkdir()
            self.file = open(self.filename, 'a')
            if self.needHeader:
                self.file.write("logdata = ")
                self.file.write("\"" + time.ctime() + "\\n\"")
                self.needHeader = False
            for line in self.saved:
                self.file.write("\"" + line.replace("\n", "\\n") + "\"")
            self.saved = []
        if self.file is None:
            self.saved.append(data)
        else:
            self.file.write("\"" + data.replace("\n", "\\n") + "\"")

    def fileno(self):
	return self.file.fileno()
