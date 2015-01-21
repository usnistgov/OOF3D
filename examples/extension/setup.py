# -*- python -*-
# $RCSfile: setup.py,v $
# $Revision: 1.8.38.1 $
# $Author: langer $
# $Date: 2014/09/27 22:35:13 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This setup script compiles an oof2 extension.  It assumes that oof2
# is already installed correctly.

# We'll use the Python distutils to build the extension
import distutils.core

# oof2config contains information about the oof2 installation, and
# imports modules needed for building oof2. oof2config also adjusts
# sys.path so that oof2extutils can be located.  If oof2 has been
# installed correctly, and your PYTHONPATH is set correctly (if
# necessary), then oof2config is accessible.
import oof2config

# oof2extutils contains some helpful functions.  Import it *after*
# oof2config, or else Python may not be able to find it.
import oof2extutils

# One (or more) SharedLibrary object must be created from the user's
# C++ files (as opposed to C++ files created by swig).  'sources' is a
# list of C++ file names.  oof2extutils.SharedLibrary is derived from
# build_shlib.SharedLibrary, and accepts all arguments that
# build_shlib.SharedLibrary does.  oof2extutils.SharedLibrary
# automatically includes header files and libraries required by oof2.

fruitlib = oof2extutils.SharedLibrary(name="strawberry",
                                      sources=
                                      ['fruitproperty/fruitproperty.C',
                                       'fruitproperty/sub/sub.C'])

# get_swig_ext runs swig and creates an Extension object that contains
# the information necessary to build a Python extension module from
# the swig output files.  The destination directory will be created if
# necessary.  get_swig_ext returns the Extension object and the name
# of the Python package that contains the Python wrapper for the
# extension module.

fruitext, fruitpkg = oof2extutils.get_swig_ext(
    srcdir='fruitproperty',
    srcfile = 'fruitproperty.swg',
    destdir = 'fruitSWIG',
    libraries= ['strawberry'])

# More than one get_swig_ext call can use the same destination
# directory.  srcfile can contain subdirectory names, as shown here.

subext, subpkg = oof2extutils.get_swig_ext(
    srcdir='fruitproperty',
    srcfile = 'sub/sub.swg',
    destdir = 'fruitSWIG',
    libraries = ['strawberry'])

distutils.core.setup(
    # The first arguments here are pretty much self-explanatory.
    name = "strawberry",
    version = "0.0.0",
    author = "Your Name Here",
    author_email = "Your Address Here",
    url = "Your URL Here",

    # 'ext_modules' is a list of all of the Extension objects defined above.
    ext_modules = [fruitext, subext],

    # 'packages' is a list of all subdirectories that contain Python
    # files.  They must all have an __init__.py file.  Subdirectories
    # created by run_swig or get_swig_ext must also be listed here.
    # Their __init__.py files have been created automatically. 
    packages = ['fruitproperty', 'fruitproperty.sub', fruitpkg, subpkg],

    # shlibs is a list of all of the SharedLibrary objects defined above.
    shlibs = [fruitlib]
    )
