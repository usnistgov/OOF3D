//
// $Header: /users/langer/FE/CVSoof/OOF2/OOFSWIG/swig_lib/stdlib.i,v 1.1.2.2 2014/06/27 20:30:19 langer Exp $
//
// stdlib.i
// Dave Beazley
// March 24, 1996
// SWIG file for some C stdlib functions
//
/* Revision history
 * $Log: stdlib.i,v $
 * Revision 1.1.2.2  2014/06/27 20:30:19  langer
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
 * Revision 1.1  2014/06/25 18:45:31  lck
 * *** empty log message ***
 *
 * Revision 1.1.1.1  1999/02/28 02:00:53  beazley
 * Swig1.1
 *
 * Revision 1.1  1996/05/22 17:27:01  beazley
 * Initial revision
 *
 */

%module stdlib
%{
#include <stdlib.h>
%}

typedef unsigned int size_t;

double atof(const char *s);
int    atoi(const char *s);
long   atol(const char *s);
int    rand();
void   srand(unsigned int seed);
void  *calloc(size_t nobj, size_t size);
void  *malloc(size_t size);
void  *realloc(void *ptr, size_t size);
void   free(void *ptr);
void   abort(void);
int    system(const char *s);
char  *getenv(const char *name);
int    abs(int n);
long   labs(long n);

