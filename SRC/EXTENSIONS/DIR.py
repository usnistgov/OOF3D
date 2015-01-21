# -*- python -*- 
# $RCSfile: DIR.py,v $
# $Revision: 1.5.60.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:37 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# ------------------- #

# This file (DIR.py) is used by the OOF2 setup script.  The file lists
# all of the OOF2 source files in the current directory and provides
# information about what to do with them.  Every subdirectory
# containing OOF2 source code must have a DIR.py file.  It must also
# have an __init__.py file, which may be empty.

# All of the items listed below are optional, but if you leave them
# *all* out, you should wonder why you're here.

# List all subdirectories of this directory, like this:
#       subdirs = ['dir1', 'dir2']
subdirs = []

# List all of the C++ and C files in this directory, like this:
#       cfiles = ['abc.C', 'def.c']
# If you provide 'cfiles', you must also specify 'clib' (below).
cfiles = []

# Similarly, list all of the C++ and C header files in this directory:
hfiles = []

# Similarly, list all of the SWIG input files.
swigfiles = []

# List all of the python files.  These are python files that should be
# imported directly into OOF2 (as opposed to python files imported
# into swig files).  Python files that require *explicit* importation
# should be imported in EXTENSIONS/initialize.py *and* listed here.
pyfiles = []

# The SWIG input files can themselves import python files.  List those
# files here:
swigpyfiles = []

# All of the C and C++ files in this directory, if any, will be
# compiled into a shared library. "clib" specifies the name of the
# library.  DIR.py files from more than one directory can refer to the
# same shared library, but only one shared library can be referred to
# in each DIR.py file.  If you specify 'clib', you must also provide
# 'cfiles'.
clib = 'your-name-here'

# If a clib is named above, then an integer 'clib_order' must be
# specified.  Libraries are built in order of increasing clib_order.
# Low numbers are used by the OOF2 core modules.  Use something big.
# If a clib is built from more than one directory, only one of the
# DIR.py files should set clib_order.
clib_order = 10000

# Any non-standard compilation or link flags required to build the
# shared library are set by the function 'set_clib_flags'.  As with
# 'clib_order', even if a clib is built from more than one DIR.py
# file, 'set_clib_flags' should be defined in only one of them.  If no
# flags need to be set, omitting 'set_clib_flags' entirely is ok.

def set_clib_flags(c_lib):

    # The c_lib argument is a CLibInfo object, defined in setup.py in
    # the root oof2 directory.  It contains three lists which can be
    # manipulated here:
    #   externalLibs    -- names of libraries to link to
    #   externalLibDirs -- directories to search for those libraries
    #   includeDirs     -- directories to search for C++ header files

    # If you're linking to libraries that are built by another DIR.py
    # file, it's *not* necessary to specify the library location.  It
    # *is* necessary to specify the name.  For example, set_clib_flags
    # in SRC/engine/DIR.py only contains the line
    #      c_lib.externalLibs.append('oof2common')
    # 'oof2common' is the library built in SRC/common/DIR.py.

    # Many libraries provide configuration programs that can be run to
    # determine the compilation and link flags that they require.  The
    # module setuputils.py contains some functions that make it easy
    # to use these programs.

    import oof2setuputils

    #     oof2setuputils.check_exec(cmd)
    #          checks that a command actually exists on the system, eg:
    #          if not check_exec('Magick++-config'):
    #              print "you have to install ImageMagick!"

    #    oof2setuputils.add_third_party_includes(cmd, c_lib)
    #         cmd must be a command that prints the flags for
    #         specifying header file directories, eg:
    #         'Magick++-config --cppflags'

    #    oof2setuputils.add_third_party_libs(cmd, c_lib)
    #          cmd must be a command that prints the flags for
    #          specifying external libraries and their locations, eg:
    #          'Magick++-config --ldflags --libs'

    #    oof2setuputils.pkg_check(package, version, c_lib)
    #          If you're linking to libraries from packages that use
    #          pkg-config for their configuration options, you can set
    #          all of the flags with one call to pkg_check.  'package'
    #          is the name of the package, and 'version' is the
    #          minimum required version number of the package.

    # Examples of non-trivial set_clib_flags functions can be found in
    # SRC/common/IO/GUI/DIR.py, SRC/engine/DIR.py, and
    # SRC/image/DIR.py.
    
    pass                                # replace this line
