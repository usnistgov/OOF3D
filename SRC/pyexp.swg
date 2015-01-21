// -*- C++ -*-
// $RCSfile: pyexp.swg,v $
// $Revision: 1.5.54.3 $
// $Author: langer $
// $Date: 2014/06/27 20:30:30 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This file (in this location) prevents _POSIX_C_SOURCE warnings when
// compiling SWIG-generated C code with compilers newer than gcc-2.95,
// or with Python versions newer than 2.1.

// It is a modified version of the SWIG-supplied pyexp.swg file.
// The only modification is the first include line, which includes
// Python.h before anything else -- this gets inserted before the
// rest of any SWIG-generated C code, and prevents _POSIX_C_SOURCE
// redefinition warnings.

// This works because SWIG follows a rigid search path for this
// file, and putting the modified one in the SRC directory pre-empts
// the stock as-distributed one.


#include <Python.h>
#include <string.h>
#include <stdlib.h>
/* Definitions for Windows/Unix exporting */
#if defined(__WIN32__)
#   if defined(_MSC_VER)
#	define SWIGEXPORT(a) __declspec(dllexport) a
#   else
#	if defined(__BORLANDC__)
#	    define SWIGEXPORT(a) a _export 
#	else
#	    define SWIGEXPORT(a) a 
#	endif
#   endif
#else
#   define SWIGEXPORT(a) a 
#endif

// We've changed the calling signature for some of the swig library
// functions, replacing "char*" with "const char*", because gcc 4.4
// complains when passing a string literal to a function expecting a
// char*.  We have our own versions of those functions in
// common/swiglib.C.

#include "common/swiglib.h"

