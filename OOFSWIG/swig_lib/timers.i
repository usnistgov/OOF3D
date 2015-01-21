//
// $Header: /users/langer/FE/CVSoof/OOF2/OOFSWIG/swig_lib/timers.i,v 1.1.2.2 2014/06/27 20:30:20 langer Exp $
//
// timers.i
// A SWIG file for adding various timing functions. 
// Really, this is modeled after the timers in the CMMD
// message passing library for the CM-5.
// 
// Dave Beazley
// April 2, 1996
//
/* Revision history 
 * $Log: timers.i,v $
 * Revision 1.1.2.2  2014/06/27 20:30:20  langer
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
 * Revision 1.1  2014/06/25 18:45:33  lck
 * *** empty log message ***
 *
 * Revision 1.1.1.1  1999/02/28 02:00:53  beazley
 * Swig1.1
 *
 * Revision 1.1  1996/05/22 17:27:01  beazley
 * Initial revision
 *
 */

%module timers
%{

#include <time.h>
#define  SWIG_NTIMERS     64

static clock_t  telapsed[SWIG_NTIMERS];
static clock_t  tstart[SWIG_NTIMERS];
static clock_t  tend[SWIG_NTIMERS];

/*-----------------------------------------------------------------
 * SWIG_timer_clear(int i)
 *
 * Clears timer i.
 *----------------------------------------------------------------- */

void
SWIG_timer_clear(int i)
{
  if ((i >= 0) && (i < SWIG_NTIMERS))
   telapsed[i] = 0;
}


/*-----------------------------------------------------------------
 * SWIG_timer_start(int i)
 *
 * Starts timer i
 *----------------------------------------------------------------- */

void
SWIG_timer_start(int i)
{
  if ((i >= 0) && (i < SWIG_NTIMERS))
    tstart[i] = clock();
}


/*-----------------------------------------------------------------
 * SWIG_timer_stop(int i)
 *
 * Stops timer i and accumulates elapsed time
 *----------------------------------------------------------------- */

void
SWIG_timer_stop(int i)
{
  if ((i >= 0) && (i < SWIG_NTIMERS)) {
    tend[i] = clock();
    telapsed[i] += (tend[i] - tstart[i]);
  }
}

/*-----------------------------------------------------------------
 * SWIG_timer_elapsed(int i)
 *
 * Returns the time elapsed on timer i in seconds.
 *----------------------------------------------------------------- */

double
SWIG_timer_elapsed(int i)
{
  double   t;
  if ((i >= 0) && (i < SWIG_NTIMERS)) {
    t = (double) telapsed[i]/(double) CLOCKS_PER_SEC;
    return(t);
  } else {
    return 0;
  }
}

%}

%section "Timer Functions",pre,after,chop_left=3,nosort,info,chop_right = 0, chop_top=0,chop_bottom=0

%text %{
%include timers.i

This module provides a collection of timing functions designed for
performance analysis and benchmarking of different code fragments. 

A total of 64 different timers are available.   Each timer can be
managed independently using four functions :

    timer_clear(int n)          Clears timer n
    timer_start(int n)          Start timer n
    timer_stop(int n)           Stop timer n
    timer_elapsed(int n)        Return elapsed time (in seconds)

All timers measure CPU time.

Since each timer can be accessed independently, it is possible
to use groups of timers for measuring different aspects of code
performance.   To use a timer, simply use code like this :
%}

#if defined(SWIGTCL)
%text %{
      timer_clear 0
      timer_start 0
      .. a bunch of Tcl code ...
      timer_stop 0
      puts "[timer_elapsed 0] seconds of CPU time"
%}
#elif defined(SWIGPERL)
%text %{
      timer_clear(0);
      timer_start(0);
      .. a bunch of Perl code ...
      timer_stop(0);
      print timer_elapsed(0)," seconds of CPU time\n";
%}
#elif defined(SWIGPYTHON)
%text %{
      timer_clear(0)
      timer_start(0)
      ... a bunch of Python code ...
      timer_stop(0)
      print timer_elapsed(0)," seconds of CPU time"
%}      
#endif

%text %{
A single timer can be stopped and started repeatedly to provide
a cummulative timing effect.

As a general performance note, making frequent calls to the timing
functions can severely degrade performance (due to operating system
overhead).   The resolution of the timers may be poor for extremely
short code fragments.   Therefore, the timers work best for
computationally intensive operations.
%}


%name(timer_clear)   void SWIG_timer_clear(int n);   
/* Clears timer n. */

%name(timer_start)   void SWIG_timer_start(int n);   
/* Starts timer n. */

%name(timer_stop)    void SWIG_timer_stop(int n);    
/* Stops timer n. */

%name(timer_elapsed) double SWIG_timer_elapsed(int n); 
/* Return the elapsed time (in seconds) of timer n */




