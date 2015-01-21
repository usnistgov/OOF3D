# -*- python -*-
# $RCSfile: profiler.py,v $
# $Revision: 1.5 $
# $Author: vrc $
# $Date: 2007/09/26 22:02:18 $

"""
This software was produced by NIST, an agency of the U.S. government,
and by statute is not subject to copyright in the United States.
Recipients of this software assume all responsibilities associated
with its operation, modification and maintenance.

Written by Steve Langer.  Loosely based on profile.py by James
Roskind.  Some attempt has been made to preserve the interface
presented by Roskind's classes, but the code itself is not based on
his.

The documentation from Roskind's profile.py gives a good overview of
what profiling is and how it works.  However, that profiler does not
always handle exceptions correctly*, and can generate incorrect
results. On the other hand, it's definitely faster than this one.

*Update: Python 2.something fixed the problems with handling
exceptions, but profile.py and hotshot.py still choke on the oof code.

Usage:

 import profiler
 prof = profiler.Profiler(filename, timer, fudge)
 <code to be profiled>
 prof.stop()

   filename is the file to which the profiling data will be written.
     Use displayprof.py to read the file and present the data.
     If the filename is omitted, no data will be written, which could be
     useful in some limited circumstances.
   timer is an optional argument.  It must be a function which
     returns a float or int representation of the time.  The default
     is time.time, which returns **wall-clock** time in seconds.  If
     you want cpu time, use time.clock instead.  Unfortunately,
     time.clock usually isn't very precise.  But time.time isn't
     very accurate, since wall clock time may not be a good
     approximation of cpu time.  You pays yer money and you takes
     yer choice.
   fudge is an optional argument giving an approximation to the overhead
     per call to the profiler, in the same units used by timer.  It
     can be estimated by the calibrate_profiler function in this
     file, or by running 'python profiler.py -c <n>', where <n> is a
     large integer.  The arguments to calibrate_profiler are n (the
     aforementioned large integer) and the timer, which should be
     the same timer used in Profiler.  The timer defaults to
     time.time if it's not specified.

To analyze the results, use displayprof.py or gfxprof2.py
"""

import sys
import time
import struct
import atexit

class Function:
    "Class for maintaining statistics on a single Python function."
    def __init__(self, id):
        self.id = id                    # (filename, lineno, functionname)
        self.ncalls = 0
        self.subroutines = {}           # time spent calling subroutines
        self.suproutines = {}           # time spent being called
        self.owntime = 0.0              # time spent in self
        self.totaltime = 0.0            # total time,
                                        # not double counting recursive calls
        self.depth = 0                  # recursion depth

    def cleansubs(self, func):
        "Remove func from the list of subroutines and suproutines"
        try:
            del self.subroutines[func]
        except KeyError:
            pass
        try:
            del self.suproutines[func]
        except KeyError:
            pass
            
    def dump(self, file):
        name = `self`
        namelen = len(name)
        file.write(struct.pack('<i', namelen))
        # self.idno is assigned by Profiler.stop()
        file.write(struct.pack('<%dsi'%namelen, name, self.idno))
        nsubs = len(self.subroutines)
        nsups = len(self.suproutines)
        file.write(struct.pack('<iiiff', self.ncalls, nsubs, nsups,
                               self.owntime, self.totaltime))
        for sub,data in self.subroutines.items():
            file.write(struct.pack('<iif', sub.idno, data.ncalls, data.time))
        for sup,data in self.suproutines.items():
            file.write(struct.pack('<iif', sup.idno, data.ncalls, data.time))


    def getSubroutineData(self, subfunction):
        """
        Return a SubroutineData object for the given function.  The
        SubroutineData object stores the number of time the subroutine was
        called from this Function and how long it took.
        """
        try:
            return self.subroutines[subfunction]
        except KeyError:
            subcall = SubroutineData()
            self.subroutines[subfunction] = subcall
            return subcall

    def getSuproutineData(self, supfunction):
        try:
            return self.suproutines[supfunction]
        except KeyError:
            supcall = SubroutineData()
            self.suproutines[supfunction] = supcall
            return supcall

    def __repr__(self):
        return "%s:%d:%s" % self.id

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

class SubroutineData:
    "Data about a function as called by another function."
    def __init__(self):
        self.ncalls = 0
        self.time = 0.0
    def add_time(self, time):
        self.time += time
        self.ncalls += 1
    def __repr__(self):
        return "(%d, %f)" % (self.ncalls, self.time)

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

class StackItem:
    def __init__(self, func, back, time):
        self.func = func
        self.suproutinedata = func.getSuproutineData(back)
        self.subroutinedata = None
        self.depth = func.depth
        self.time = time                # time item was put on stack
    def newcall(self, subr):
        self.subroutinedata = self.func.getSubroutineData(subr)
    def __repr__(self):
        return "%s depth=%d supr=%s subr=%s" % (self.func, self.depth,
                                                self.suproutinedata,
                                                self.subroutinedata)

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# fudge values:
#  450 MHz PIII laptop: 1.7e-05
#  1.2 GHz Athlon desktop: 5e-6
#  1.67 GHz G4 laptop: 2.89e-06

def _stopprof():
    if Profiler.profiler:
        Profiler.profiler.stop()

class Profiler:
    profiler = None     # ensures that only one Profiler is active
    def __init__(self, filename=None, timer=time.time, fudge=5e-6):
        if Profiler.profiler:
            Profiler.profiler.stop()
        Profiler.profiler = self
        self.filename = filename
        self.timer = timer
        self.funcdict = {}
        self.stack = []
        self.fudge = fudge
        self.overhead = 0.
        # time is measured in elapsed time since the program began,
        # not counting time spent in the profiler.
        self.lasteventtime = 0.
        self.ncalls = 0
        # Put a dummy function in the dictionary.  It will pretend to
        # be the calling function when we don't know the real one.
        dummyid = ('?', 0, '?')
        self.dummyfunc = Function(dummyid)
        self.funcdict[dummyid] = self.dummyfunc

        atexit.register(_stopprof)

        # starttime is the time the Profiler was started PLUS an
        # estimate of all of the time spent running the Profiler
        # itself.  That is, it's an estimate of when a non-profiled
        # program would have been started if it were at the same point
        # that the profiled program is now.  starttime is continually
        # updated.
        self.starttime = timer()
        # Ok, here we go...
        sys.setprofile(self.handler)

    def stop(self, dump=1):
        totaltime = self.timer() - self.starttime
        profiler = None
        sys.setprofile(None)
        if dump and self.filename:
            file = open(self.filename, "wb")
            file.write(struct.pack('<fi', totaltime, self.ncalls))
            # assign integer id's to all functions for easy reference
            for func,i in zip(self.funcdict.values(),range(len(self.funcdict))):
                func.idno = i
                func.cleansubs(self.dummyfunc) # remove references to dummyfunc
            for func in self.funcdict.values():
                if not func is self.dummyfunc:
                    func.dump(file)
            file.close()

    def getPyFunction(self, frame):
        if not frame:
            return self.dummyfunc
        code = frame.f_code
        frameid = (code.co_filename, code.co_firstlineno, code.co_name)
        try:
            return self.funcdict[frameid]
        except KeyError:
            func = Function(frameid)
            self.funcdict[frameid] = func
            return func

    def getCFunction(self, cfunc):
        if cfunc.__module__ is not None:
            funcid = (cfunc.__module__, 0, cfunc.__name__)
        else:
            # must be a method
##            print 'cfunc.__self__', cfunc.__self__, type(cfunc.__self__)
##            print cfunc.__class__.__name__, cfunc.__name__
            funcid = ("(%s)" % cfunc.__class__.__name__,
                      0, cfunc.__name__)
        try:
            return self.funcdict[funcid]
        except KeyError:
            func = Function(funcid)
            self.funcdict[funcid] = func
            return func

    eventdict = {}
    def return_handler(self, frame, arg, eventtime):
        if len(self.stack)==0:
            # Because profiling starts within Profiler.__init__,
            # the first profiling event must be a 'return'. The
            # only way that the stack can be empty at this point
            # is if it hasn't been initialized (otherwise it would
            # always at least contain the current function).  So
            # if we're here, we must have just caught that first
            # 'return'.  It's time to initialize the stack,
            # pretending that all functions in the stack were
            # called at the same time (now).

            # Construct a list of all active frames.
            base_frame = frame
            frames = [base_frame]
            while base_frame.f_back:
                base_frame = base_frame.f_back
                frames.append(base_frame)
            frames.reverse()
            # frames is a list of all active frames, now in
            # correct order.  Use it to construct the stack.  We
            # can't construct the stack in reverse by simply
            # following the f_back trail, because then the
            # recursion depths would be wrong.

            # This construction assumes that there are no c functions
            # in the stack.  C functions have the same frame as the
            # Python function that called them. (True or false?)
            base_func = self.getPyFunction(base_frame)
            base_func.depth += 1
            self.stack = [StackItem(base_func, self.dummyfunc, eventtime)]
            self.stack[0].newcall(self.dummyfunc)
            for tmp_frame in frames[1:]:
                tmp_func = self.getPyFunction(tmp_frame)
                tmp_back = self.getPyFunction(tmp_frame.f_back)
                self.stack[-1].newcall(tmp_func)
                self.stack.append(StackItem(tmp_func, tmp_back, eventtime))
                tmp_func.depth += 1
##            print "----Initial Stack----"
##            self.print_stack()
        self.charge_time(eventtime - self.lasteventtime)
        self.function_returned(eventtime)

    eventdict['return'] = return_handler
    eventdict['c_return'] = return_handler

    def call_handler(self, frame, arg, eventtime):
        # A Python function has *just* been called.
        func = self.getPyFunction(frame)
        self.ncalls += 1
        func.ncalls += 1
        self.charge_time(eventtime - self.lasteventtime)
        caller = self.stack[-1]
        caller.newcall(func) # create subr. data for caller
        caller.subroutinedata.ncalls += 1
        self.stack.append(StackItem(func, caller.func, eventtime))
        func.depth += 1
        self.stack[-1].suproutinedata.ncalls += 1

    eventdict['call'] = call_handler

    def c_call_handler(self, frame, arg, eventtime):
        # A C function is *about* to be called.
        func = self.getCFunction(arg)
        self.ncalls += 1
        func.ncalls += 1
        self.charge_time(eventtime - self.lasteventtime)
        caller = self.stack[-1]
        caller.newcall(func)
        caller.subroutinedata.ncalls += 1
        self.stack.append(StackItem(func, caller.func, eventtime))
        func.depth += 1
        self.stack[-1].suproutinedata.ncalls +=1

    eventdict['c_call'] = c_call_handler

    def exception_handler(self, frame, arg, eventtime):
        self.charge_time(eventtime - self.lasteventtime)
        self.function_returned(eventtime)

    eventdict['exception'] = exception_handler
    eventdict['c_exception'] = exception_handler
            
    def handler(self, frame, eventstr, arg):
        """
        The Python interpreter calls this function whenever a function
        is called or returns, or when an exception is raised or
        propagated.
        """
        now = self.timer()
        eventtime = now - self.starttime # when this event occurred

        # call the handler for this type of event
        self.eventdict[eventstr](self, frame, arg, eventtime)

        self.lasteventtime = eventtime
        # pretend that this all never happened
        wastedtime = self.timer() - now
        self.overhead += wastedtime
        self.starttime += wastedtime + self.fudge

    def function_returned(self, time):
        from_func = self.stack.pop(-1)  # function we're returning from
        from_func.func.depth -= 1
        dt = time - from_func.time      # total time func was on the stack
        from_func.suproutinedata.time += dt
        if self.stack:
            self.stack[-1].subroutinedata.time += dt
        
    def charge_time(self, dt):
        self.stack[-1].func.owntime += dt
        for stackitem in self.stack:
            # This time slice gets charged to each function's
            # totaltime just once, even if the function has been
            # called recursively.
            if stackitem.depth == 0:
                stackitem.func.totaltime += dt

    def print_stack(self):
        print '----Stack----'
        for stackitem in self.stack:
            print '   ', stackitem

    def get_time(self, funcname):
        """
        Get the total time used by a function.  This is used by the
        calibration routine, and isn't meant for general consumption.
        In particular, it's not smart about multiple functions with
        the same name.
        """
        for funcid in self.funcdict.keys():
            if funcname == funcid[2]:
                return self.funcdict[funcid].totaltime

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#


def a_very_long_function_name():
    x = 1

def calibrate_profiler(n, timer=time.time):
    """
    Calibration routine to returns the fudge factor.  The fudge factor
    is the amount of time it takes to call and return from the
    profiler handler.  The profiler can't measure this time, so it
    will be attributed to the user code unless it's subtracted off.
    """
    starttime = timer()
    p = Profiler(fudge=0.0)
    for i in range(n):
        a_very_long_function_name()
    p.stop()
    stoptime = timer()
    simpletime = p.get_time('a_very_long_function_name')
    realtime = stoptime - starttime
    profiletime = simpletime + p.overhead
    losttime = realtime - profiletime
    return losttime/(2*n)               # 2 profile events per function call

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#
        
if __name__ == '__main__':
    # This example tests whether or not recursion and exceptions are
    # handled correctly.
    import math, sys, getopt, string

    class A:
        pass
        def __getattr__(self, x):
            raise AttributeError
    def h():
        pass
    def gee():
        # use some time
        x = 0
        for j in range(10):
            x += math.sin(j*math.pi/6.)
        # create a hidden exception call
        a = A()
        # The internal exception in hasattr confused the Python
        # Profile class in early versions of Python.  This line is
        # here to test for that.
        if hasattr(a, 'b'):
            x += 2
        h()
    def f(i):
        if i > 1:
            f(i-1)
        else:
            gee()
    try:
        optlist, arg = getopt.getopt(sys.argv[1:], 'c:on:f:d:')
    except getopt.error, message:
        print message
        sys.exit(1)

    ncycles = 10
    oldprof = 0
    filename = None
    fudge = 5.e-6

    for opt in optlist:
        if opt[0] == '-o':
            oldprof = 1
        elif opt[0] == '-n':
            ncycles = string.atoi(opt[1])
        elif opt[0] == '-f':
            filename = opt[1]
        elif opt[0] == '-c':
            n = string.atoi(opt[1])
            print calibrate_profiler(n)
        elif opt[0] == '-d':
            fudge = string.atof(opt[1])
            
                

    if not oldprof:
        p = Profiler(filename, fudge=fudge)
        f(ncycles)
        p.stop()
    else:
        import profile
        import time
        p = profile.Profile(time.time)
        p.run('f(ncycles)')
        p.dump_stats(filename)
