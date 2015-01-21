# -*- python -*-
# $RCSfile: setup.py,v $
# $Revision: 1.100.2.26 $
# $Author: langer $
# $Date: 2014/11/07 22:31:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Usage:

#  In the top oof2 directory (the one containing this file) type
#  something like this:
#    python setup.py install     # installs in the default location
#    python setup.py install --prefix=/some/other/place
#    python setup.py [build [--debug]] install --prefix ...
#  The flags --3D, --enable-mpi, --enable-petsc, and --enable-devel
#  can occur anywhere after 'setup.py' in the command line.


# Required version numbers of required external libraries.  These
# aren't used explicitly in this file, but they are used in the DIR.py
# files that are execfile'd here.

GTK_VERSION = "2.6.0"
PYGTK_VERSION = "2.6"
GNOMECANVAS_VERSION = "2.6"
# If on a 64-bit system with Python 2.5 or later, make sure that
# pygobject is at least version 2.12.
try:
    import ctypes                       # only in 2.5 and later
    if ctypes.sizeof(ctypes.c_long) == 8:
        PYGOBJECT_VERSION = "2.12"
    else:
        PYGOBJECT_VERSION = "2.6"
except ImportError:
    PYGOBJECT_VERSION = "2.6"
    
# will need to add vtk

###############################

import distutils.core
from distutils.command import build
from distutils.command import build_ext
from distutils.command import build_py
from distutils.command import clean
from distutils.command import install
from distutils.command import build_scripts
from distutils import errors
from distutils import log
from distutils.dir_util import remove_tree
from distutils.sysconfig import get_config_var

import oof2installlib

import shlib # adds build_shlib and install_shlib to the distutils command set
from shlib import build_shlib

from oof2setuputils import run_swig, find_file, extend_path, InstallationFile

import os
import shlex
import stat
import string
import sys
import subprocess
import tempfile
import time
from types import *

# Tell distutils that .C is a C++ file suffix.
from distutils.ccompiler import CCompiler
CCompiler.language_map['.C'] = 'c++'

## needed to save installation log to a saved variable before
calledFromInstall = False # checks if build is being called from oof_install
log_file = InstallationFile(sys.stdout, sys.stderr)
## The file is used in build and install

# py2app stuff is commented out because, in python 2.3 at least,
# py2app installs itself in a way that's inconsistent with
# build_shlib, and build_shlib is more important for us.
##try:
##    import py2app                       # for creating a frozen Mac app.
##except ImportError:
##    have_py2app = False
##else:
##    have_py2app = True

DIRFILE = "DIR.py"                      # oof subdirectory manifest files
SWIGCFILEEXT = 'cmodule.C'              # suffix for swig output files
SWIGINSTALLDIR = "SWIG"


##############

# readDIRs() walks through the oof2 source directory looking for
# DIR.py files, reads the files, and fills in the CLibInfo objects.
# CLibInfo categorize all of the source files except for the python
# files for pure python modules.

# DIR.py files contain the following python variables.  All are optional.

# dirname: The name of the directory. It's actually not used.

# clib: the name of the library to be built from the C and C++ files
# in the directory.  The library will be called lib<name>.<suffix>,
# where suffix is system dependent.  More than one DIR.py file can use
# the same name.

# cfiles: a list of the names of all of the C and C++ files in the
# directory that need to be compiled to form lib<name>.

# hfiles: a list of the names of the header files that go with the C
# and C++ files.

# swigfiles: a list of the names of the swig input files in the
# directory.  Swig-generated C++ code will be compiled but *not*
# included in lib<name>.  Each swig input file will create a separate
# python-loadable module which will *link* to lib<name>.

# swigpyfiles: a list of the names of python files that are included
# in swig output files.

# clib_order: an integer specifying the order in which the libraries
# must be built.  Later libraries may link to earlier ones.  This
# linking is done by setting clib.externalLibs in the set_clib_flags
# function in a DIR.py file.

# set_clib_flags: a function which may be called to set compilation
# and linker flags for building the library.  Its argument is a
# CLibInfo object.  The includeDirs, externalLibDirs, and externalLibs
# members of the object may be modified by set_clib_flags.

# subdirs: a list of subdirectories that should be processed.  Each
# subdirectory must have its own DIR.py file.

# TODO: ensure that typemaps.swg files are included in the source
# distribution!

allCLibs = {}
purepyfiles = []

def getCLibInfo(name):
    try:
        return allCLibs[name]
    except KeyError:
        clib = allCLibs[name] = CLibInfo(name)
        return clib
                
class CLibInfo:
    def __init__(self, name):
        allCLibs[name] = self
        self.libname = name
        self.dirdata = {'cfiles': [],   # *.[Cc] -- c and c++ source code
                        'hfiles': [],   # *.h    -- c and c++ header files
                        'swigfiles': [], # *.swg  -- swig source code
                        'swigpyfiles': [], # *.spy  -- python included in swig
                        }
        self.externalLibs = []
        self.externalLibDirs = []
        self.includeDirs = []
        self.extra_link_args = []
        self.extra_compile_args = []
        self.extensionObjs = None
        self.ordering = None

    # Parse the file lists in a DIR.py file.  The file has been read
    # already, and its key,list pairs are in dirdict.  Only the data
    # relevant to CLibInfo is dealt with here.  The rest is handled
    # by readDIRs().
    def extractData(self, srcdir, dirdict):
        for key in self.dirdata.keys():
            try:
                value = dirdict[key]
                del dirdict[key]
            except KeyError:
                pass
            else:
                for filename in value:
                    self.dirdata[key].append(os.path.join(srcdir, filename))
        try:
            flagFunc = dirdict['set_clib_flags']
            del dirdict['set_clib_flags']
        except KeyError:
            pass
        else:
            flagFunc(self)
        try:
            self.ordering = dirdict['clib_order']
            del dirdict['clib_order']
        except KeyError:
            pass

    def get_extensions(self):
        if self.extensionObjs is None:
            self.extensionObjs = []
            for swigfile in self.dirdata['swigfiles']:
                # The [6:] in the following strips the "./SRC/" from
                # the beginning of the file names.  splitext(file)[0]
                # is the path to a file with the extension stripped.
                basename = os.path.splitext(swigfile)[0][6:]

                # swig 1.1 version
                modulename = os.path.splitext(basename + SWIGCFILEEXT)[0]
                sourcename = os.path.join(swigroot, basename+SWIGCFILEEXT)
                # swig 1.3 version                
##                modulename = '_' + basename
##                sourcename = os.path.join(swigroot, basename+'_wrap.cxx')
                
                extension = distutils.core.Extension(
                    name = os.path.join(OOFNAME,"ooflib", SWIGINSTALLDIR,
                                        modulename),
                    language = 'c++',
                    sources = [sourcename],
                    define_macros = platform['macros'],
                    extra_compile_args = self.extra_compile_args + \
                        platform['extra_compile_args'],
                    include_dirs = self.includeDirs + platform['incdirs'],
                    library_dirs = self.externalLibDirs + platform['libdirs'],
                    libraries = [self.libname] + self.externalLibs,
                                                        # + platform['libs'],
                    extra_link_args = self.extra_link_args + \
                        platform['extra_link_args']
                    )

                self.extensionObjs.append(extension)
        return self.extensionObjs

    def get_shlib(self):
        if self.dirdata['cfiles']:
            return build_shlib.SharedLibrary(
                self.libname,
                sources=self.dirdata['cfiles'],
                extra_compile_args=platform['extra_compile_args'],
                include_dirs=self.includeDirs + platform['incdirs'],
                libraries=self.externalLibs,# + platform['libs'],
                library_dirs=self.externalLibDirs +
                platform['libdirs'],
                extra_link_args=platform['extra_link_args'])

    # Find all directories containing at least one swig input file.  These
    # are used to create the swigged python packages.  This is done by
    # traversing the DIR.py files, so that random leftover .swg files in
    # strange places don't create packages, and so that modules can be
    # included conditionally by HAVE_XXX tests in DIR.py files.
    def find_swig_pkgs(self):
        pkgs = set()
        for swigfile in self.dirdata['swigfiles']:
            pkgs.add(os.path.split(swigfile)[0])
        # pkgs is a set of dirs containing swig files, relative to
        # the main OOF2 dir, eg, "./SRC/common".
        # Convert it to a list of dirs relative to the swigroot
        swigpkgs = []
        for pkg in pkgs:
            pkgdir = os.path.join(swigroot, pkg[6:]) # eg, SRC/SWIG/common
            pkgname = OOFNAME + '.' + pkgdir[4:].replace('/', '.') # oof2.ooflib.SWIG.common
            swigpkgs.append(pkgname)
        return swigpkgs

# end class CLibInfo

def moduleSort(moduleA, moduleB):
    if moduleA.ordering is not None:
        if moduleB.ordering is not None:
            return cmp(moduleA.ordering, moduleB.ordering)
        return -1
    else:                               # moduleA.ordering is None
        if moduleB.ordering is not None:
            return 1
        return cmp(moduleA.name, moduleB.name)

def allFiles(key):
    hierlist = [lib.dirdata[key] for lib in allCLibs.values()]
    flatlist = []
    for sublist in hierlist:
        flatlist.extend(sublist)
    return flatlist


def readDIRs(srcdir):
    dirfile = os.path.join(srcdir, DIRFILE)
    if os.path.exists(dirfile):
#         print >> sys.stderr, "LOADING", dirfile
        # dirfile defines variables whose names are the same as the
        # ModuleInfo.dirdata keys.  The variables contain lists of
        # file names.
        localdict = {}
        execfile(dirfile, globals(), localdict)
        # Now the variables and functions defined in dirfile are in localdict.
        try:
            dirname = localdict['dirname']
            del localdict['dirname']
        except KeyError:
            pass
        
        try:
            clib = localdict['clib']
            del localdict['clib']
        except KeyError:
            pass
        else:
            clibinfo = getCLibInfo(clib)
            clibinfo.extractData(srcdir, localdict)
            
        try:
            pyfiles = localdict['pyfiles']
            del localdict['pyfiles']
        except KeyError:
            pass
        else:
            for filename in pyfiles:
                purepyfiles.append(os.path.join(srcdir, filename))
        
        # dirfile also contains a list of subdirectories to process.
        try:
            subdirs = localdict['subdirs']
            del localdict['subdirs']
        except KeyError:
            pass
        else:
            # At this point, all args in localdict should have been processed.
            if len(localdict) > 0:
                print "WARNING: unrecognized values", localdict.keys(), \
                      "in", dirfile
            for subdir in subdirs:
                readDIRs(os.path.join(srcdir, subdir))

##########

# Find all python packages and subpackages in a directory by looking
# for __init__.py files.

def find_pkgs():
    pkglist = []
    os.path.walk('SRC', _find_pkgs, pkglist)
    return pkglist

def _find_pkgs(pkglist, dirname, subdirs):
    if os.path.exists(os.path.join(dirname, '__init__.py')):
        pkglist.append(dirname)

##########

def swig_clibs(dry_run, force, debug, build_temp, with_swig=None):
    # First make sure that swig has been built.
    if with_swig is None:
        ## TODO 3.1: swig is installed inside the distutils
        ## build/temp* directory to avoid conflicts if oof is being
        ## built for multiple architectures on a shared file system.
        ## However, swig's .o file and other intermediate files
        ## (parser.cxx, parser.h, config.log, Makefiles, etc) are
        ## still in OOFSWIG/SWIG.  They'll have to be removed manually
        ## before building on a different architecture.  It would be
        ## better if they were in build/temp* too, but that might
        ## require modifying the Makefile.
        swigsrcdir = os.path.abspath('OOFSWIG')
        swigbuilddir = os.path.join(os.path.abspath(build_temp), 'swig-build')
        if not os.path.exists(swigbuilddir):
            os.mkdir(swigbuilddir)
        swigexec = os.path.join(swigbuilddir, 'bin', 'swig')
        ## TODO 3.1: Add a --rebuild-swig option to the build command
        ## that forces swig to be rebuilt even if swigexec exists.
        ## This will help if we ever have to fix problems in swig.
        if not os.path.exists(swigexec):
            print "Building swig"
            status = os.system(
                'cd %s && ./configure --prefix=%s && make && make install' 
                % (swigsrcdir, swigbuilddir))
            if status:
                sys.exit(status)
    else:
        swigexec = with_swig
    srcdir = os.path.abspath('SRC')
    extra_args = platform['extra_swig_args']
    if debug:
        extra_args.append('-DDEBUG')
    for clib in allCLibs.values():
        for swigfile in clib.dirdata['swigfiles']:
            # run_swig requires a src dir and an input file path
            # relative to it.  The '+1' in the following line strips
            # off a '/', so that sfile doesn't look like an absolute
            # path.
            sfile = os.path.abspath(swigfile)[len(srcdir)+1:]
            run_swig(srcdir='SRC', swigfile=sfile, destdir=swigroot,
                     cext=SWIGCFILEEXT,
                     include_dirs = ['SRC'],
                     dry_run=dry_run,
                     extra_args=extra_args,
                     force=force,
                     with_swig=swigexec,
                     DIM_3=DIM_3
                     )

##########

# Get a file's modification time.  The time is returned as an integer.
# All we care about is that the integers are properly ordered.

def modification_time(phile):
    return os.stat(phile)[stat.ST_MTIME]

#########

# Look for and return the locations of the vtk include and lib
# directories.  vtk doesn't provide a program (vtk-config?) that tells
# us where to find the directories, and their names change from
# version to version.

def findvtk(basename):
    global vtkdir
    
    base = vtkdir or basename
        
    # First look for basename/include/vtk*
    incdir = os.path.join(base, 'include')
    files = os.listdir(incdir)
    vtkname = None
    for f in files:
        ## This may fail if there is more than one version of vtk
        ## installed.  listdir returns files in arbitrary order, and
        ## the first one found will be used.
        if f.startswith('vtk'):
            vtkname = f
            incvtk = os.path.join(base, 'include', vtkname)
            libvtk = os.path.join(base, 'lib', vtkname)
            if os.path.isdir(incvtk) and os.path.isdir(libvtk):
                return (incvtk, libvtk)
    return (None, None)

#########

# Define subclasses of the distutils build_ext and build_shlib class.
# We need subclasses so that oofconfig.h can be created before the
# files are compiled, and so that makedepend can be run.
# oof_build_xxxx contains the routines that are being added to both
# build_ext and build_shlib.

_dependencies_checked = 0
class oof_build_xxxx:
    def make_oofconfig(self):
        cfgfilename = os.path.normpath(os.path.join(self.build_temp,
                                                    'SRC/oofconfig.h'))
        includedir = os.path.join('include', OOFNAME)
        self.distribution.data_files.append((includedir, [cfgfilename]))
        # If oofconfig.h already exists, don't recreate it unless
        # forced to.  It would require everything that depends on it
        # to be recompiled unnecessarily.
        if self.force or not os.path.exists(cfgfilename):
            print "creating", cfgfilename
            if not self.dry_run:
                os.system('mkdir -p %s' % os.path.join(self.build_temp, 'SRC'))
                cfgfile = open(cfgfilename, "w")
                print >> cfgfile, """\
// This file was created automatically by the oof2 setup script.
// Do not edit it.
// Re-run setup.py to change the options.
#ifndef OOFCONFIG_H
#define OOFCONFIG_H
                """
                if HAVE_PETSC:
                    print >> cfgfile, '#define HAVE_PETSC 1'
                if HAVE_MPI:
                    print >> cfgfile, '#define HAVE_MPI 1'
                if HAVE_OPENMP: # TODO: is this necessary? _OPENMP is predefined
                    print >> cfgfile, '#define HAVE_OPENMP'
                if DEVEL:
                    print >> cfgfile, '#define DEVEL ', DEVEL
                if NO_GUI:
                    print >> cfgfile, '#define NO_GUI 1'
                if ENABLE_SEGMENTATION:
                    print >> cfgfile, '#define ENABLE_SEGMENTATION'
                if NANOHUB:
                    print >> cfgfile, '#define NANOHUB'
                if DIM_3:
                    print >> cfgfile, '#define DIM 3'
                    print >> cfgfile, '#define DIM_3'
                else: # for good measure
                    print >> cfgfile, '#define DIM 2'
                if self.check_header('<sstream>'):
                    print >> cfgfile, '#define HAVE_SSTREAM'
                    if DIM_3:
                        print >> cfgfile, '#define VTK_EXCLUDE_STRSTREAM_HEADERS'
                else:
                    print >> cfgfile, '// #define HAVE_SSTREAM'
                # Python pre-2.5 compatibility
                print >> cfgfile, """\
#include <Python.h>
#if PY_VERSION_HEX < 0x02050000 && !defined(PY_SSIZE_T_MIN)
typedef int Py_ssize_t;
#define PY_SSIZE_T_MAX INT_MAX
#define PY_SSIZE_T_MIN INT_MIN
#endif /* PY_VERSION_HEX check */
"""
                print >> cfgfile, "#endif"
                cfgfile.close()

    def check_header(self, headername):
        # Check that a c++ header file exists on the system.
        print "Testing for", headername
        tmpfiled, tmpfilename = tempfile.mkstemp(suffix='.C')
        tmpfile = os.fdopen(tmpfiled, 'w')
        print >> tmpfile, """\
        #include %s
        int main(int, char**) { return 1; }
        """ % headername
        tmpfile.flush()
        try:
            try:
                ofiles = self.compiler.compile(
                    [tmpfilename],
                    extra_postargs=platform['extra_compile_args'] +
                                   platform['prelink_suppression_arg']
                    )
            except errors.CompileError:
                return 0
            ofile = ofiles[0]
            dir = os.path.split(ofile)[0]
            os.remove(ofiles[0])
            if dir:
                try:
                    os.removedirs(dir)
                except:
                    pass
            return 1
        finally:
            os.remove(tmpfilename)

    def find_dependencies(self):
        # distutils doesn't provide a makedepend-like facility, so we
        # have to do it ourselves.  makedepend is deprecated, so we
        # use "gcc -MM" and hope that gcc is available.  This routine
        # runs "gcc -MM" and constructs a dictionary listing the
        # dependencies of each .o file and each swig-generated .C
        # file.

        # TODO: Check for the existence of gcc and makedepend and use
        # the one that's available.

        # depdict[file] is a list of sources that the file depends
        # upon.
        depdict = {}

        # Run "gcc -MM" on the C++ files to detect dependencies.  "gcc
        # -MM" only prints the file name of the target, not its path
        # relative to the build directory, so we have to use the -MT
        # flag to specify the target.  That means that we can't
        # process more than one C++ file at a time.
        print "Finding dependencies for C++ files."
        for phile in allFiles('cfiles'):
            ## Hack Alert.  We don't know the full paths to some of
            ## the system header files at this point.  The -MM flag is
            ## supposed to tell gcc to ignore the system headers, but
            ## apparently some versions still want to be able to find
            ## them, and fail when they don't.  So we use -MG, which
            ## tells gcc to add missing headers to the dependency
            ## list, and then we weed them out later.  At least this
            ## way, the "missing" headers don't cause errors.
            cmd = 'gcc -MM -MG -MT %(target)s -ISRC -I%(builddir)s -I%(buildsrc)s %(file)s' \
              % {'file' : phile,
                 'target': os.path.splitext(phile)[0] + ".o",
                 'builddir' : self.build_temp,
                 'buildsrc' : os.path.join(self.build_temp, 'SRC')
                 }
            proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                                    bufsize=4096)
            stdoutdata, stderrdata = proc.communicate()
            if stderrdata:
                print >> sys.stderr, "Command failed:", cmd
                print >> sys.stderr, stderrdata
                sys.exit(1)
            if not stdoutdata:
                print >> sys.stderr, "Command failed, no data received:", cmd
                sys.exit(1)
            # stdoutdata is a multiline string.  The first substring
            # is the name of the target file, followed by a colon.
            # The remaining substrings are the source files that the
            # target depends on, but there can also be line
            # continuation characters (backslashes) which must be
            # ignored.  It's even possible that the *first* line is
            # blank except for a backslash.
            files = [f for f in stdoutdata.split() if f != "\\"]
            target = files[0][:-1] # omit the colon
            realtarget = os.path.normpath(os.path.join(self.build_temp, target))
            for source in files[1:]:
                ## See Hack Alert, above.  Missing header files will
                ## all be outside of our directory hierarchy, so we
                ## just ignore any dependency that doesn't begin with
                ## "SRC/".
                if source.startswith('SRC/'):
                    depdict.setdefault(realtarget, []).append(source)

        # .C and.py files in the SWIG directory depend on those in the
        # SRC directory.  Run gcc -MM on the swig source files.
        print "Finding dependencies for .swg files."
        for phile in allFiles('swigfiles'):
            cmd = 'gcc -MM -MG -MT %(target)s -x c++ -I. -ISRC -I%(builddir)s %(file)s'\
              % {'file' : phile,
                 'target': os.path.splitext(phile)[0] + '.o',
                 'builddir' : self.build_temp
              }
            proc = subprocess.Popen(shlex.split(cmd), 
                                    stdout=subprocess.PIPE, bufsize=4096)
            stdoutdata, stderrdata = proc.communicate()
            if stderrdata:
                print >> sys.stderr, "Command failed:", cmd
                print >> sys.stderr, stderrdata
                sys.exit(1)
            files = [f for f in stdoutdata.split() if f != "\\"]
            # print "---\nstdoutdata=", stdoutdata
            # print "files=", files
            target = files[0][:-1]
            targetbase = os.path.splitext(target)[0]
            # On some systems, target begins with "SRC/".  On
            # others, it begins with "./SRC/".  Arrgh.  This
            # strips off either one.
            targetbase = targetbase.split("SRC/", 1)[1]
            targetc = os.path.normpath(
                os.path.join(swigroot, targetbase + SWIGCFILEEXT))
            targetpy = os.path.normpath(
                os.path.join(swigroot, targetbase + '.py'))
            for source in files[1:]:
                if source.startswith('SRC/'):
                    depdict.setdefault(targetc, []).append(source)
                    depdict.setdefault(targetpy,[]).append(source)

        ## Debugging:
        # def dumpdepdict(filename, depdict):
        #     print >> sys.stderr, "Dumping dependency information to", filename
        #     f = file(filename, "w")
        #     keys = depdict.keys()
        #     keys.sort()
        #     for target in keys:
        #         print >> f, target
        #         sources = depdict[target]
        #         sources.sort()
        #         for source in sources:
        #             print >> f, "   ", source
        #     f.close()
        # dumpdepdict("depdict", depdict)

        # Add in the implicit dependencies on the .swg files.
        for phile in allFiles('swigfiles'):
            # file is ./SRC/dir/whatver.swg
            base = os.path.splitext(phile)[0][4:] # dir/whatever
            cfile = os.path.normpath(os.path.join(swigroot,
                                                  base+SWIGCFILEEXT))
            pyfile = os.path.normpath(os.path.join(swigroot, base+'.py'))
            depdict.setdefault(cfile, []).append(phile)
            depdict.setdefault(pyfile, []).append(phile)
        # Add in the implicit dependencies on the .spy files.
        for underpyfile in allFiles('swigpyfiles'):
            base = os.path.splitext(underpyfile)[0] # drop .spy
            pyfile = os.path.normpath(os.path.join(swigroot,base[6:]+'.py'))
            depdict.setdefault(pyfile, []).append(underpyfile)

        return depdict

    # Remove out-of-date target files.  We have to do this because
    # distutils for Python 2.5 and earlier checks the dates of the .C
    # and .o files, but doesn't check for any included .h files, so it
    # doesn't rebuild enough.  For 2.6 and later, it doesn't check
    # anything, and it rebuilds far too much. To fix that, we
    # monkeypatch _setup_compile from Python 2.5 as well as remove the
    # out of date target files.

    def clean_targets(self, depdict):
        outofdate = False
        if not self.dry_run:
            for target, sources in depdict.items():
                if os.path.exists(target):
                    targettime = modification_time(target)
                    sourcetime = max([modification_time(x) for x in sources])
                    if sourcetime > targettime:
                        os.remove(target)
                        print "clean_targets: Removed out-of-date target", target
                        outofdate = True
                else:
                    outofdate = True
        if outofdate:
            ## TODO: Remove the .so file.  I can't figure out how to
            ## find its name at this point, though.
            pass

    def clean_dependencies(self):
        global _dependencies_checked
        if not _dependencies_checked:
            depdict = self.find_dependencies()
            self.clean_targets(depdict)
            _dependencies_checked = 1


# This does the swigging.
class oof_build_ext(build_ext.build_ext, oof_build_xxxx):
    description = "build the python extension modules for OOF2"
    user_options = build_ext.build_ext.user_options + [
        ('with-swig=', None, "specify the swig executable")]
    def initialize_options(self):
        self.with_swig = None
        build_ext.build_ext.initialize_options(self)
    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('with_swig', 'with_swig'))
        ## TODO: Add extra libraries (python2.x) for cygwin?
        build_ext.build_ext.finalize_options(self)
    # build_extensions is called by build_ext.run().
    def build_extensions(self):
        self.compiler.add_include_dir(os.path.join(self.build_temp, 'SRC'))
        self.compiler.add_include_dir('SRC')
        self.compiler.add_library_dir(self.build_lib)

        if self.debug:
            self.compiler.define_macro('DEBUG')
            # self.compiler.define_macro('Py_DEBUG')
            self.compiler.undefine_macro('NDEBUG')
        # Make the automatically generated .h files.
        self.make_oofconfig()
        # Run makedepend
        self.clean_dependencies()
        # Generate swigged .C and .py files
        swig_clibs(self.dry_run, self.force, self.debug, self.build_temp,
                   self.with_swig)
                                          
        # Build the swig extensions by calling the distutils base
        # class function
        build_ext.build_ext.build_extensions(self)

class oof_build_shlib(build_shlib.build_shlib, oof_build_xxxx):
    user_options = build_shlib.build_shlib.user_options + [
        ('with-swig=', None, "non-standard swig executable"),
        ('blas-libraries=', None, "libraries for blas and lapack"),
        ('blas-link-args=', None, "link arguments required for blas and lapack")
        ]
    def initialize_options(self):
        self.with_swig = None
        self.blas_libraries = None
        self.blas_link_args = None
        build_shlib.build_shlib.initialize_options(self)
    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('with_swig', 'with_swig'),
                                   ('blas_libraries', 'blas_libraries'),
                                   ('blas_link_args', 'blas_link_args'),
                                   ('libraries', 'libraries'),
                                   ('library_dirs', 'library_dirs'))
        build_shlib.build_shlib.finalize_options(self)
    def build_libraries(self, libraries):
        self.make_oofconfig()
        self.clean_dependencies()
        self.compiler.add_include_dir(os.path.join(self.build_temp, 'SRC'))
        self.compiler.add_include_dir('SRC')
        if self.debug:
            self.compiler.define_macro('DEBUG')

        # The blas libs and arguments weren't actually put into the
        # SharedLibrary objects when they were created, because we
        # didn't know until now whether or not the user had provided
        # alternates.  It's time to either use the predefined values
        # from "platform" or to use the command line arguments.

        if self.blas_libraries is not None:
            blaslibs = string.split(self.blas_libraries)
        else:
            blaslibs = platform['blas_libs']
        if self.blas_link_args is not None:
            blasargs = string.split(self.blas_link_args)
        else:
            blasargs = platform['blas_link_args']
        extrablaslibs = self.check_extra_blaslibs(blaslibs, blasargs)
        blaslibs.extend(extrablaslibs)
        
        for library in libraries:
            library.libraries.extend(blaslibs)
            library.extra_link_args.extend(blasargs)

        ## TODO: Add extra libraries (python2.x) for cygwin?
        build_shlib.build_shlib.build_libraries(self, libraries)

    def check_extra_blaslibs(self, blaslibs, linkargs):
        # Check to see if blas requires extra libraries to link
        # properly.  If it does, return a list of extra libraries.  If
        # it links without extra args, return [].  If it doesn't
        # link at all, raise an exception.  (This test is required
        # because different Linux distributions seem to build their
        # blas libraries differently, and we can't tell which
        # distribution we're using.)
        print "Testing if blas links correctly"
        # First create a temp directory to play in.
        tmpdir = tempfile.mkdtemp(dir=os.getcwd())
        tmpdirname = os.path.split(tmpdir)[1]
        # Create a file with dummy blas code in it.
        tmpfilename = os.path.join(tmpdirname, "blastest.C")
        tmpfile = open(tmpfilename, "w")
        print >> tmpfile, """\
        extern "C" {void dgemv_(char*, int*, int*, double*, double*, int*,
        double*, double*, double*, double*, int*);}
        int main(int argc, char **argv) {
        char c;
        int i;
        double x;
        dgemv_(&c, &i, &i, &x, &x, &i, &x, &x, &x, &x, &i);
        return 0;
        }
        """
        tmpfile.close()
        try:
            # Compile the dummy code.
            try:
                ofiles=self.compiler.compile(
                    [tmpfilename],
                    extra_postargs=(platform['extra_compile_args'] +
                                    platform['prelink_suppression_arg']),
                    )
            except errors.CompileError:
                raise errors.DistutilsExecError("can't compile blas test")
            # Try linking without extra args
            try:
                self.compiler.link(
                    target_desc=self.compiler.EXECUTABLE,
                    objects=ofiles,
                    output_filename=tmpfilename[:-2],
                    library_dirs=platform['libdirs'],
                    libraries=blaslibs,
                    extra_preargs=linkargs,
                    target_lang='c++')
            except errors.LinkError:
                pass
            else:
                return []               # Extra args not needed
            # Try linking with -lg2c and -lgfortran
            for libname in ('g2c', 'gfortran'):
                try:
                    self.compiler.link(
                        target_desc=self.compiler.EXECUTABLE,
                        objects=ofiles,
                        output_filename=tmpfilename[:-2],
                        library_dirs=platform['libdirs'],
                        libraries=blaslibs+[libname],
                        extra_preargs=linkargs,
                        target_lang='c++')
                except errors.LinkError:
                    pass
                else:
                    return [libname]   

        finally:
            # Clean out the temp directory
            remove_tree(tmpdirname)
        raise errors.DistutilsExecError("can't link blas!")

class oof_build(build.build):
    sep_by = " (separated by '%s')" % os.pathsep
    user_options = build.build.user_options + [
        ('with-swig=', None, "non-standard swig executable"),
        ('libraries=', None, 'external libraries to link with'),
        ('library-dirs=', None,
         "directories to search for external libraries" + sep_by),
        ('blas-libraries=', None, "libraries for blas and lapack"),
        ('blas-link-args=', None, "link args for blas and lapack")]
    def initialize_options(self):
        self.libraries = None
        self.library_dirs = None
        self.blas_libraries = None
        self.blas_link_args = None
        self.with_swig = None
        build.build.initialize_options(self)

    # override finalize_options in build.py in order to include the
    # dimension in the build directory.
    def finalize_options(self):
        if not DIM_3:
            dim = "2d"
        else:
            dim = "3d"
            
        plat_specifier = ".%s-%s-%s" % (build.get_platform(), 
                                        sys.version[0:3], dim) 

        if self.build_purelib is None:
            self.build_purelib = os.path.join(self.build_base, 'lib')
        if self.build_platlib is None:
            self.build_platlib = os.path.join(self.build_base,
                                              'lib' + plat_specifier)

        if self.build_lib is None:
	    filename = 'installationLog.py'
            if self.distribution.ext_modules:
                self.build_lib = self.build_platlib
                log_file.setFilename(
                    os.path.join(self.build_lib,
                                 'oof3d', 'ooflib','common',filename))
            else:
                self.build_lib = self.build_purelib
                log_file.setFilename(
                    os.path.join(self.build_lib,
                                 'oof3d', 'ooflib', 'common', filename))

        if self.build_temp is None:
            self.build_temp = os.path.join(self.build_base,
                                           'temp' + plat_specifier)
        if self.build_scripts is None:
            self.build_scripts = os.path.join(
                self.build_base, 'scripts-' + sys.version[0:3] + "-" + dim)

        try: #only in newer version of distutils
            if self.executable is None:
                self.executable = os.path.normpath(sys.executable)
        except AttributeError:
            pass
	  
    def run(self):
	if not calledFromInstall:
	    log_file.clear()
            log_file.write_file("System Arguments= "+ str(sys_args)+'\n')	

	build.build.run(self)

###################################################

## Modify the build_py command so that it creates oof2config.py.  The
## file is created in the build_lib directory so that it gets
## installed at the top level beside the oof2 or oof3d package.  We
## also need an init script in the oof2 or oof3d directory.

class oof_build_py(build_py.build_py):
    def run(self):
        self.make_oof2config()
        self.make_toplevel_init()
        build_py.build_py.run(self) #this is where swigroot is copied
    def make_toplevel_init(self):
        initname = os.path.join(self.build_lib,OOFNAME,'__init__.py')
        initfile = open(initname,'w')
        initfile.close()
    def make_oof2config(self):
        cfgscriptname = os.path.join(self.build_lib, OOFNAME+'config.py')
        cfgscript = open(cfgscriptname, 'w')

        install = self.get_finalized_command('install')
        build_shlib = self.get_finalized_command('build_shlib')
        install_shlib = self.get_finalized_command('install_shlib')
      
        print >> cfgscript, 'root = "%s"' % os.path.abspath('.')
        print >> cfgscript, 'version = "%s"' % self.distribution.get_version()
        print >> cfgscript, 'prefix = "%s"' % install.prefix
        idirs = build_shlib.include_dirs + [
            os.path.abspath('SRC'),
            os.path.join(install.prefix, 'include', OOFNAME)
            ] + platform['incdirs']
        print >> cfgscript, 'swig_include = ', [os.path.abspath('SRC')]
        print >> cfgscript, 'extra_compile_args =', \
              platform['extra_compile_args']
        print >> cfgscript, 'include_dirs =', idirs
        print >> cfgscript, 'library_dirs =', [install_shlib.install_dir]
        oof2installlib.shared_libs = [lib.name for lib in install_shlib.shlibs]
        print >> cfgscript, 'libraries =', oof2installlib.shared_libs
        print >> cfgscript, 'extra_link_args =', platform['extra_link_args']
        print >> cfgscript, "import sys; sys.path.append(root)"
        cfgscript.close()


    def build_module (self, module, module_file, package):
        if type(package) is StringType:
            package = string.split(package, '.')
        elif type(package) not in (ListType, TupleType):
            raise TypeError, \
                  "'package' must be a string (dot-separated), list, or tuple"

        # Now put the module source file into the "build" area -- this is
        # easy, we just copy it somewhere under self.build_lib (the build
        # directory for Python source).
        outfile = self.get_module_outfile(self.build_lib, package, module)
        outfile = outfile.replace(SWIGDIR, SWIGINSTALLDIR)
        dir = os.path.dirname(outfile)
        #dir = dir.replace(SWIGDIR,SWIGINSTALLDIR)
        self.mkpath(dir)
        return self.copy_file(module_file, outfile, preserve_mode=0)



###################################################

# Modify "build_scripts" so that it copies only oof2 or oof3d, but not
# both.  Both are in the scripts list so that they're both
# distributed, but only one should be installed.

class oof_build_scripts(build_scripts.build_scripts):
    def finalize_options(self):
        build_scripts.build_scripts.finalize_options(self)
        self.scripts = [OOFNAME]

###################################################

class oof_install(install.install):
    def run(self):
	global calledFromInstall
	calledFromInstall = True
	log_file.write_file("System Arguments= "+ str(sys_args)+'\n')
	install.install.run(self)
	calledFromInstall=False
	
###################################################

class oof_clean(clean.clean):
    user_options = clean.clean.user_options + [
        ('most', 'm', 'remove libraries and scripts, but not binary dist.'),
        ('swig', None, 'remove swig output files')]
    boolean_options = clean.clean.boolean_options + ['most', 'swig']

    def initialize_options(self):
        clean.clean.initialize_options(self)
        self.most = None
        self.swig = None
        
    def run(self):
        if self.most and not self.all:
            for d in [self.build_lib, self.build_scripts]:
                if os.path.exists(d):
                    remove_tree(d,dry_run=self.dry_run)
                else:
                    log.warn("'%s' does not exist -- can't clean it.", d)
        if self.swig and os.path.exists(swigroot):
            remove_tree(swigroot, dry_run=self.dry_run)
        clean.clean.run(self)
    
###################################################

def set_dirs():
    global swigroot, datadir, docdir
    swigroot = os.path.join('SRC', SWIGDIR)
    # Splitting and reassembling paths makes them portable to systems
    # that don't use '/' as the path separator.
    datadir = os.path.join(*DATADIR.split('/'))
    docdir = os.path.join(*DOCDIR.split('/'))

def get_global_args():
    # The --enable-xxxx flags in the command line have to be obtained
    # *before* we parse the DIR.py files, and the DIR.py files must be
    # parsed before calling distutils.core.setup (because the list of
    # source files comes from DIR.py).  But distutils.core.setup handles
    # the command line arguments, so we have to look for and remove the
    # --enable-xxxx flags here.

    # TODO: the more elegant way to do this would be to add a separate
    # distutils command that reads the DIR.py files and is always run
    # before any other command.  Then the --enable-xxxx flags could be
    # global distutils options, since they'd be processed *before*
    # DIR.py was read.  NO, that's not true.  DIR.py is read before
    # any distutils calls can possibly be made, because distutils.core
    # hasn't been called yet.

    global HAVE_MPI, HAVE_OPENMP, HAVE_PETSC, DEVEL, NO_GUI, \
        ENABLE_SEGMENTATION, \
        DIM_3, DATADIR, DOCDIR, OOFNAME, SWIGDIR, NANOHUB, vtkdir
    HAVE_MPI = _get_oof_arg('--enable-mpi')
    HAVE_PETSC = _get_oof_arg('--enable-petsc')
    DEVEL = _get_oof_arg('--enable-devel')
    NO_GUI = _get_oof_arg('--disable-gui')
    ENABLE_SEGMENTATION = _get_oof_arg('--enable-segmentation')
    DIM_3 = _get_oof_arg('--3D')
    NANOHUB = _get_oof_arg('--nanoHUB')
    HAVE_OPENMP = _get_oof_arg('--enable-openmp')
    vtkdir = _get_oof_arg('--vtkdir')

    # The following determine some secondary installation directories.
    # They will be created within the main installation directory
    # specified by --prefix. 

    if not DIM_3:
        DATADIR = "share/oof2"
        DOCDIR = "share/oof2/doc"
        OOFNAME = "oof2"
        SWIGDIR = "SWIG2D"           # root dir for swig output, inside SRC
    else:
        DATADIR = "share/oof3d"
        DOCDIR = "share/oof3d/doc"
        OOFNAME = "oof3d"
        SWIGDIR = "SWIG3D"           # root dir for swig output, inside SRC


def _get_oof_arg(arg):
    # Search for an argument which begins like "arg" -- if found,
    # return the trailing portion if any, or 1 if none, and remove the
    # argument from sys.argv.
    for s in sys.argv:
        splits = s.split('=')
        if splits[0] == arg:
            sys.argv.remove(s)
            if len(splits) > 1:         # found an =
                return splits[1]
            return 1                    # just a plain arg
    return 0                            # didn't find arg
        
platform = {}

def set_platform_values():
    ## Set platform-specific flags that don't specifically depend on
    ## OOF2 stuff.  They're stored in a dictionary just to keep things
    ## tidy.
    platform['extra_compile_args'] = []
    platform['macros'] = []
    platform['blas_libs'] = []
    platform['blas_link_args'] = []
    platform['libdirs'] = []
    platform['incdirs'] = [get_config_var('INCLUDEPY')]
    platform['extra_link_args'] = []
    platform['prelink_suppression_arg'] = []
    platform['extra_swig_args'] = []

    if os.path.exists('/usr/local/lib'):
        platform['libdirs'].append('/usr/local/lib')
    # if os.path.exists('/usr/site/lib'):
    #     platform['libdirs'].append('/usr/site/lib')
    if os.path.exists('/usr/site/include'):
        platform['incdirs'].append('/usr/site/include')

    # The prelink-suppression argument is used when running the compiler
    # to test for libraries.  Such builds need to be reasonably clean in
    # terms of not creating a lot of auxiliary files, and it's OK if
    # they're a bit slow.  Currently this is only set on SGIs, and it
    # prevents the creation of the "ii_files" subdirectory for the
    # library-check compilations.
    ## TODO: Is this still necessary?  Does the SGI OS exist anymore?
    platform['prelink_suppression_arg'] = []

    if sys.platform == 'darwin':
        platform['blas_link_args'].extend(['-faltivec',
                                           '-framework', 'Accelerate'])
        platform['extra_link_args'].append('-headerpad_max_install_names')
        if os.path.exists('/sw') and DIM_3: # fink
            platform['incdirs'].append('/sw/include')
            vtkinc, vtklib = findvtk('/sw')
            if vtkinc is not None:
                platform['libdirs'].append(vtklib)
                platform['incdirs'].append(vtkinc)
            # platform['libdirs'].append('/sw/lib/vtk-5.4')
            # platform['libdirs'].append('/sw/lib/vtk54')
            platform['incdirs'].append('/usr/X11/include/')
            platform['incdirs'].append('/usr/X11R6/include/')
        if os.path.exists('/opt') and DIM_3: # macports
            platform['incdirs'].append('/opt/local/include')
            vtkinc, vtklib = findvtk('/opt/local')
            if vtkinc is not None:
                platform['libdirs'].append(vtklib)
                platform['incdirs'].append(vtkinc)
        # If we're using anything later than Python 2.5 with macports,
        # the pkgconfig files for the python modules aren't in the
        # standard location.
        if (os.path.exists('/opt') and
            sys.version_info[0] >= 2 and sys.version_info[1] > 5):
            ## TODO: Having to encode such a long path here seems
            ## wrong.  If and when pkgconfig acquires a more robust
            ## way of finding its files, use it.
            pkgpath = "/opt/local/Library/Frameworks/Python.framework/Versions/%d.%d/lib/pkgconfig/" % (sys.version_info[0], sys.version_info[1])
            print >> sys.stdout, "Adding", pkgpath
            extend_path("PKG_CONFIG_PATH", pkgpath)
        # If we're using clang, we want to suppress some warnings
        # about oddities in swig-generated code:
        if 'clang' in get_config_var('CC'):
            platform['extra_compile_args'].append('-Wno-self-assign')
            
    elif sys.platform.startswith('linux'):
        # g2c isn't included here, because it's not always required.
        # We don't want to check whether or not it's required, either,
        # because the user might have provided a different blas
        # library on the command line.  The check is done later,just
        # before platform['blas_libs'] is used.
        platform['blas_libs'].extend(['lapack', 'blas', 'm'])
        if DIM_3:
            vtkinc, vtklib = findvtk('/usr')
            if vtkinc is not None:
                platform['incdirs'].append(vtkinc)
                platform['libdirs'].append(vtklib)
    elif sys.platform[:4] == 'irix':
        platform['extra_compile_args'].append('-LANG:std')
        platform['extra_link_args'].append('-LANG:std')
        platform['prelink_suppression_arg'].append('-no_prelink')
        platform['blas_libs'].extend(['lapack', 'blas', 'ftn', 'm'])
    elif sys.platform == 'cygwin':
        platform['blas_libs'].extend(['blas', 'lapack', 'm'])
        platform['libdirs'].append('/bin')
    elif sys.platform[:6] == 'netbsd':
        platform['blas_libs'].extend(['lapack', 'blas', 'm'])
        platform['libdirs'].append('/usr/pkg/lib')

    if HAVE_OPENMP:
        platform['extra_compile_args'].append('-fopenmp')
        platform['extra_link_args'].append('-fopenmp') # needed?

    if HAVE_MPI:
        # mpi.h
        basedirs = ['/usr/local', '/usr', '/usr/lib', '/usr/site', '/sw']
        mpisubdirs = ['.', 'mpich', 'mpi']
        mpidirs = [os.path.join(bdir, 'include', mdir) for bdir in basedirs
                   for mdir in mpisubdirs]
        incdir = find_file('mpi.h', mpidirs)
        if not incdir:
            print "Warning! Can't locate mpi.h!"
        else:
            if incdir not in platform['incdirs']:
                platform['incdirs'].append(incdir)
        # mpi++.h
        basedirs = ['/usr/local', '/usr', '/usr/lib', '/usr/site', '/sw']
        mpisubdirs = ['.', 'mpich', 'mpi', 'mpich/mpi2c++', 'mpi/mpi2c++']
        mpidirs = [os.path.join(bdir, 'include', mdir) for bdir in basedirs
                   for mdir in mpisubdirs]
        incdir = find_file('mpi++.h', mpidirs)
        if not incdir:
            print "Warning! Can't locate mpi++.h!"
        else:
            if incdir not in platform['incdirs']:
                platform['incdirs'].append(incdir)

        platform['extra_swig_args'].append('-DHAVE_MPI')
        if sys.platform == 'darwin':
            # TODO: Need to know what Mac needs for mpi++
            # This may have to be changed or removed just as in MPI below
            platform['libs'].extend(['mpich', 'pmpich'])
        elif sys.platform.startswith('linux'):
            # libpmpich++.a
            basedirs = ['/usr/local', '/usr', '/usr/lib', '/usr/site', '/sw']
            mpisubdirs = ['.', 'mpich', 'mpi', 'mpich/lib', 'mpi/lib']
            mpidirs = [os.path.join(bdir, mdir) for bdir in basedirs
                       for mdir in mpisubdirs]
            libdir = find_file('libpmpich++.a', mpidirs)
            if not libdir:
                print "Warning! Can't locate libpmpich++.a!"
            else:
                if libdir not in platform['libdirs']:
                    platform['libdirs'].append(libdir)
            #platform['libs'].extend(['pmpich++', 'mpich'])
        elif sys.platform[:4] == 'irix':
            pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# In Python 2.6 and 2.7, distutils doesn't check for an existing .o
# file, and recompiles everything whether it needs to or not.  Since
# we remove all of the out-of-date .o files, we don't want to
# recompile all of them.  Here we monkeypatch the relevant method from
# the Python 2.5 distutils.

if sys.hexversion > 0x02060000:
    from distutils.dep_util import newer_pairwise, newer_group
    from distutils.ccompiler import gen_preprocess_options
    def _setup_compile(self, outdir, macros, incdirs, sources, depends,
                       extra):
        """Process arguments and decide which source files to compile.

        Merges _fix_compile_args() and _prep_compile().
        """
        if outdir is None:
            outdir = self.output_dir
        elif type(outdir) is not StringType:
            raise TypeError, "'output_dir' must be a string or None"

        if macros is None:
            macros = self.macros
        elif type(macros) is ListType:
            macros = macros + (self.macros or [])
        else:
            raise TypeError, "'macros' (if supplied) must be a list of tuples"

        if incdirs is None:
            incdirs = self.include_dirs
        elif type(incdirs) in (ListType, TupleType):
            incdirs = list(incdirs) + (self.include_dirs or [])
        else:
            raise TypeError, \
                  "'include_dirs' (if supplied) must be a list of strings"

        if extra is None:
            extra = []

        # Get the list of expected output (object) files
        objects = self.object_filenames(sources,
                                        strip_dir=0,
                                        output_dir=outdir)
        assert len(objects) == len(sources)

        # XXX should redo this code to eliminate skip_source entirely.
        # XXX instead create build and issue skip messages inline

        if self.force:
            skip_source = {}            # rebuild everything
            for source in sources:
                skip_source[source] = 0
        elif depends is None:
            # If depends is None, figure out which source files we
            # have to recompile according to a simplistic check. We
            # just compare the source and object file, no deep
            # dependency checking involving header files.
            skip_source = {}            # rebuild everything
            for source in sources:      # no wait, rebuild nothing
                skip_source[source] = 1

            n_sources, n_objects = newer_pairwise(sources, objects)
            for source in n_sources:    # no really, only rebuild what's
                skip_source[source] = 0 # out-of-date
        else:
            # If depends is a list of files, then do a different
            # simplistic check.  Assume that each object depends on
            # its source and all files in the depends list.
            skip_source = {}
            # L contains all the depends plus a spot at the end for a
            # particular source file
            L = depends[:] + [None]
            for i in range(len(objects)):
                source = sources[i]
                L[-1] = source
                if newer_group(L, objects[i]):
                    skip_source[source] = 0
                else:
                    skip_source[source] = 1

        pp_opts = gen_preprocess_options(macros, incdirs)

        build = {}
        for i in range(len(sources)):
            src = sources[i]
            obj = objects[i]
            ext = os.path.splitext(src)[1]
            self.mkpath(os.path.dirname(obj))
            if skip_source[src]:
                log.debug("skipping %s (%s up-to-date)", src, obj)
            else:
                build[obj] = src, ext

        return macros, objects, extra, pp_opts, build
    CCompiler._setup_compile = _setup_compile

    # End of monkeypatch 

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

if __name__ == '__main__':
    global sys_args
    sys_args = sys.argv[:]      # make a copy for the installation log file
    get_global_args()           # modifies sys.argv
    set_dirs()
    set_platform_values()

    readDIRs('.')                       # Gather data from the DIR.py files.

    # Get the data to build the C++ extension modules.
    clibraries = allCLibs.values()
    clibraries.sort(moduleSort)
    extensions = []
    shlibs = []
    for clib in clibraries:
        extensions.extend(clib.get_extensions())
        shlib = clib.get_shlib()
        if shlib is not None:
            shlibs.append(shlib)

    # Construct the list of pure python packages. If a subdirectory has an
    # __init__.py file, then all the .py files in the subdirectory will
    # form a package.

    # find non-swigged files
    pkg_list = set()
    pkg_list.add(OOFNAME)
    pkgs = find_pkgs()                      # ['SRC', 'SRC/common', ...]
    for pkg in pkgs:
        if pkg != 'SRC':
            pkgname = OOFNAME + '.' + pkg[4:].replace('/', '.')
            pkg_list.add(pkgname)

    # Ask each CLibInfo object for the swigged python modules it
    # creates. 
    for clib in allCLibs.values():
        pkg_list.update(clib.find_swig_pkgs())

    # Make sure that intermediate directories are in the package list.
    allpkgs = set()
    for pkg in pkg_list:
        comps = pkg.split('.')  # components of the package path
        if comps[0] == OOFNAME:
            p = comps[0]
            # Add components one by one to the base component and add
            # the resulting path to the package list.
            for pp in comps[1:]:
                p = '.'.join([p, pp])
                allpkgs.add(p)
        else:
            allpkgs.add(pkg)

    # The top directory in the package hierarchy doesn't get picked up
    # by the above hackery. 
    allpkgs.add(OOFNAME)

    pkgs = [pkg.replace(OOFNAME, OOFNAME+'.ooflib') for pkg in allpkgs]

    # Find example files that have to be installed.
    examplefiles = []
    for dirpath, dirnames, filenames in os.walk('examples'):
        if filenames:
            examplefiles.append(
                (os.path.join(datadir, dirpath), # installation dir
                 [os.path.join(dirpath, phile) for phile in filenames
                  if not phile.endswith('~') and
                  os.path.isfile(os.path.join(dirpath, phile))]))

    # If this script is being used to create a frozen executable, the
    # Python path has to be set the same way it is during actual
    # execution.
    py2app_options = dict(argv_emulation=True)
    sys.path.append('SRC')                  # so that py2app can find imports
    try:
        import pygtk
        pygtk.require("2.0")
    except:
        pass
    
    setupargs = dict(
        name = OOFNAME,
        version = "unreleased",
        description = "Analysis of material microstructures, from NIST.",
        author = 'The NIST OOF Team',
        author_email = 'oof_manager@nist.gov',
        url = "http://www.ctcms.nist.gov/oof/oof3d/",
        # If more scripts are added here, change oof_build_scripts too.
        scripts = ['oof2', 'oof3d'],
        cmdclass = {"build" : oof_build,
                    "build_ext" : oof_build_ext,
                    "build_py" : oof_build_py,
                    "build_shlib": oof_build_shlib,
                    "build_scripts" : oof_build_scripts,
                    "install_lib": oof2installlib.oof_install_lib,
                    "clean" : oof_clean,
                    "install" : oof_install},
        packages = pkgs,
        package_dir = {OOFNAME+'.ooflib':'SRC'},
        shlibs = shlibs,
        ext_modules = extensions,
        data_files = examplefiles
        )

    # 'options' is a valid keyword arg in python 2.6 and above, and in
    # python 2.6 and above we need to use it to set the 'plat_name'
    # argument to the 'build' command.
    if sys.hexversion >= 0x020600F0: 
        options = dict(build = dict(plat_name = distutils.util.get_platform()))
        setupargs['options'] = options


##    if have_py2app:
##        setupargs['app'] = ['SRC/common/oof.py']
##        setupargs['options'] = {'py2app': py2app_options}

    distutils.core.setup(**setupargs)


