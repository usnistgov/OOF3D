//
// $Header: /users/langer/FE/CVSoof/OOF2/OOFSWIG/swig_lib/malloc.i,v 1.1.2.2 2014/06/27 20:30:15 langer Exp $
//
// malloc.i
// Dave Beazley
// March 24, 1996
// SWIG file for memory management functions
// (also contained in stdlib.i)
//
/* Revision History
 * $Log: malloc.i,v $
 * Revision 1.1.2.2  2014/06/27 20:30:15  langer
 * Copied Lulu's modified swig into OOFSWIG, and changed setup.py so that
 * it automatically builds and uses it.  The --with-swig option to setup.py
 * is still respected, if it's given, but it shouldn't be necessary any more.
 *
 * Changed make_dist so that the swig output files aren't included in
 * the distribution, and removed the --skip-swig option from setup.py.
 * Since everybody has swig now, it's no longer necessary.  This will
 * make the build take a little bit longer, but users won't have to
 * combine the build and install steps anymore.
 *
 * Removed the bit in pyexp.swg that suppressed the warnings that the old
 * swig code generated.  This means that if you use --with-swig, you'll
 * probably get lots of warnings.
 *
 * Added some explicit (char*) casts in PyObject_CallMethod calls in
 * swig typemaps, to get rid of warnings in swig generated code.
 * For unknown reasons, PyObject_CallMethod has char * arguments instead
 * of const char* arguments.   Other similar Python API calls use const.
 *
 * Revision 1.1  2014/06/25 18:45:28  lck
 * *** empty log message ***
 *
 * Revision 1.1.1.1  1999/02/28 02:00:53  beazley
 * Swig1.1
 *
 * Revision 1.1  1996/05/22 17:27:01  beazley
 * Initial revision
 *
 */

%module malloc
%{
#include <stdlib.h>
%}

%section "Memory Allocation Module",
         pre,info,after,nosort,chop_left=3,chop_right=0,chop_top=0,chop_bottom=0,skip=1

%text %{
%include malloc.i

This module provides access to a few basic C memory management functions.
All functions return void pointers, but realloc() and free() will operate
on any sort of pointer.   Sizes should be specified in bytes.
%}

void  *calloc(unsigned nobj, unsigned size);
/* Returns a pointer to a space for an array of nobj objects, each with
   size bytes.   Returns NULL if the request can't be satisfied. 
   Initializes the space to zero bytes. */

void  *malloc(unsigned size);
/* Returns a pointer to space for an object of size bytes.  Returns NULL
   upon failure. */

void  *realloc(void *ptr, unsigned size);
/* Changes the size of the object pointed to by ptr to size bytes. 
   The contents will be unchanged up the minimum of the old and new
   sizes.  Returns a pointer to the new space of NULL upon failure,
   in which case *ptr is unchanged. */

void   free(void *ptr);
/* Deallocates the space pointed to by ptr.  Does nothing if ptr is NULL.
   ptr must be a space previously allocated by calloc, malloc, or realloc. */

