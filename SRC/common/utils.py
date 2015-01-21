# -*- python -*-
# $RCSfile: utils.py,v $
# $Revision: 1.71.2.13 $
# $Author: langer $
# $Date: 2014/10/03 17:41:07 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import lock
from ooflib.common import debug
import string
import sys
import types

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Function to return adjacent pairs of a list, i.e. given [1,2,3],
# it returns [(1,2), (2,3)].
# def list_pairs(lst): # Old version, without generators
#     return [ (lst[i], lst[i+1]) for i in range(len(lst)-1) ]
def list_pairs(lst):
    for i in range(len(lst)-1):
        yield (lst[i],lst[i+1])

# Given a list, return all n*(n-1) pairs of objects in it. 
def unique_pairs(lst):
    for (i, a) in enumerate(lst):
        for (j, b) in enumerate(lst):
            if j < i:
                yield (b,a)
            else:
                break

def pairs(lst):
    for a in lst:
        for b in lst:
            if a is not b:
                yield (a,b)

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#
    
# Function to take a list of lists and flatten it into a single list.
def flatten(lols):
    result = []
    for l in lols:
        result += l
    return result

# Unfortunately, this version is much slower:
##   def flatten(lols): return [x for y in lols for x in y]
# and this is even slower than that:
##   def flatten(lols): return reduce(operator.concat, lols, [])

## flatten1 takes a list of lists and returns a list of the contents
## of all the sublist.  It *doesn't* do any recursion on the sublists.
## Creating a list of lists and calling flatten1 on it is much more
## efficient than creating the list by calling 'list += sublist' in a
## loop.

def flatten1(lols):
    length = reduce(lambda x,y: x+len(y), lols, 0)
    flatlist = [None]*length
    offset = 0
    for lst in lols:
        flatlist[offset:offset+len(lst)] = lst
        offset += len(lst)
    return flatlist

# What about not creating the list at all?  Create an iterable object
# that returns the list elements without duplicating the memory.  This
# is slower than flatten1 when tested on its own, but should be tested
# in situ.

def flatten2(lols):
    return Flattener(lols)

class Flattener(object):
    def __init__(self, lols):
        self.lols = lols
    def __iter__(self):
        if len(self.lols) == 0:
            return iter([])
        return _Flattener(self.lols)
class _Flattener(object):
    def __init__(self, lols):
        self.lols = lols
        self.outeriter = iter(lols)
        self.inneriter = iter(next(self.outeriter))
    def __iter__(self):
        return self
    def next(self):
        try:
            return next(self.inneriter)
        except StopIteration:
            self.inneriter = iter(next(self.outeriter))
            return next(self.inneriter)

#######

def flatten_all(lols):
    result = []
    for l in lols:
        if type(l) is types.ListType or type(l) is types.TupleType:
            result += flatten_all(l)
        else:
            result.append(l)
    return result

# Given a template which is a list of lists of lists to arbitrary
# depth, convert the flat datalist to a nested list with the same
# structure.  Each sublist of the result will have the same length as
# the corresponding sublist in the template.
def unflatten(template, datalist):
    which = 0
    result, which = _do_unflatten(template, datalist, which)
    return result

def _do_unflatten(template, datalist, which):
    result = []
    for obj in template:
        if type(obj) == types.ListType or type(obj) == types.TupleType:
            sublist, which = _do_unflatten(obj, datalist, which)
            result.append(sublist)
        else:
            result.append(datalist[which])
            which += 1
    return result, which


#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Given a generator, turn it into a list. Anything else is simply
# returned.

def degenerate(liszt):
    if type(liszt) is types.GeneratorType:
        return [x for x in liszt]
    return liszt

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Get a list of the classes to which an object or class belongs.  Just
# for debugging.

def classes(c):
    if type(c) == types.InstanceType: # only for old-style classes
        return classes(c.__class__)
    if type(c) == types.ClassType: # only for old-style classes
        if not c.__bases__:
            return [c]
        return [c] +  flatten(map(classes, c.__bases__))
    # Might be a new style class
    if c == object:
        return []
    if type(c) == types.TypeType:
        if c.__bases__ == (object,):
            return [c]
        return [c] + flatten(map(classes, c.__bases__))
    try:
        cls = c.__class__
    except AttributeError:
        return []              # not a class or an instance of a class
    return classes(cls)

# Get the *names* of the classes to which an object or class belongs.
# This loses namespace information, so it's not as robust as using
# classes().  But it's more readable.
def classnames(c):
    return [cl.__name__ for cl in classes(c)]

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Using PrintableClass as a metaclass allows a class (not the
# instances of the class!) to be printed cleanly. Instead of 
# class A(object):
#   pass
# print A
# ---->  <class '__main__.module.classname'> 
# use
# class A(object):
#   __metaclass__ = PrintableClass
# print A
# ---->  A

class PrintableClass(type):
    def __str__(cls):
        return cls.__name__
    def __repr__(cls):
        return cls.__name__

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Replaced by skeletonnode.canonicalorder, which queries indices.
# def canonicalorder(p0, p1):
#     if p0 < p1:
#         return (p0, p1)
#     return (p1, p0)

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Evaluate expressions, statements and files in the main oof namespace.

mainmodule = sys.modules['__main__']

def OOFexec(command):
    exec(command, mainmodule.__dict__)

def OOFexeclines(commands):
    for command in commands:
        debug.fmsg(command)
        exec(command, mainmodule.__dict__)

def OOFeval(expr):
    return eval(expr, mainmodule.__dict__)

def OOFexecfile(file):
    execfile(file, mainmodule.__dict__)

# Run a function as if it were defined in the main namespace.
def OOFrun(func, *args, **kwargs):
    # Change the function's globals dict so that it includes stuff
    # from main namespace.  The function's original dict is loaded
    # *after* the main namespace, so that it can override main space
    # definitions if necessary.
    fg = func.func_globals.copy()
    func.func_globals.clear()
    func.func_globals.update(mainmodule.__dict__)
    func.func_globals.update(fg)
    
    func(*args, **kwargs)

    # Restore the original globals dict, so that future calls aren't
    # messed up.
    func.func_globals.clear()
    func.func_globals.update(fg)

# Define an existing object in the main oof namespace.
def OOFdefine(name, obj):
    mainmodule.__dict__[name] = obj

# Safe, restricted evaluation: can't import or do anything malicious.
# Can only be used to evaluate things defined in the main namespace.
# Is used when loading data files.

def OOFeval_r(expr):
    if expr == 'None':
        return None
    return mainmodule.__dict__[expr]

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

### Parse an argument list, e.g. from inside an "eval" when the
### arguments arrive in string form.  IS THIS USED?

    
##def argback(*args,**kwargs):
##    return {"tuple":args, "dictionary":kwargs}

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Construct a name, based on the given name arg, that does not occur
# in the given list of other names.  If the given name isn't in the
# list, return it.  If it is, append "<number>" to it, where 'number'
# is chosen so that the result is unique.

# If the given name is an AutomaticName instance, then an
# AutomaticName instance is returned.

# The list of names passed to uniqueName is almost always a global
# list, and so in a threaded environment we need to prevent
# simultaneous uniqueName calls with the same name list.  Since the
# calls are quick and not done in time sensitive situations, we put a
# single mutex lock inside uniqueName, instead of requiring all
# callers to implement their own lock.

import re

_uniqueNameLock = lock.SLock()

def uniqueName(name, othernames, exclude=None):
    _uniqueNameLock.acquire()
    others = othernames[:]
    try:
        if exclude is not None:
            try:
                others.remove(exclude)
            except ValueError:
                pass
        if name not in others:
            return name
        from ooflib.common.IO import automatic # delayed to avoid import loop
        auto = isinstance(name, automatic.AutomaticName)
        # Strip '<number>' suffix, if any.
        basename = re.split('<[0-9]+>$', name)[0]
        # Find any existing names of the form 'basename<number>'.
        expr = re.compile("^" + re.escape(basename) + "<[0-9]+>$")
        matches = filter(expr.match, others)
        if matches:
            # Find largest existing "<number>".
            suffixes = [x[len(basename)+1:-1] for x in matches]
            lastsuffix = max(map(eval, suffixes))
        else:
            lastsuffix = 1
        newname = "%s<%d>" % (basename, lastsuffix+1)
        if auto:
            return automatic.AutomaticName(newname)
        return newname
    finally:
        _uniqueNameLock.release()
        
# Special version that uses underscores, for menu names.
def menUniqueName(name, othernames):
    _uniqueNameLock.acquire()
    try:
        if name not in othernames:
            return name
        from ooflib.common.IO import automatic # delayed to avoid import loop
        auto = isinstance(name, automatic.AutomaticName)
        # Strip '_number' suffix, if any.
        basename = re.split('_[0-9]+$', name)[0]
        # Find any existing names of the form 'basename_number'.
        expr = re.compile("^" + re.escape(basename) + "_[0-9]+$")
        matches = filter(expr.match, othernames)
        if matches:
            # Find largest existing "number".
            suffixes = [x[len(basename)+1:] for x in matches]
            lastsuffix = max(map(eval, suffixes))
        else:
            lastsuffix = 1
        return "%s_%d" % (basename, lastsuffix+1)
    finally:
        _uniqueNameLock.release()

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Convert a menu item name to the form displayed by the GUI.
# Underscores are replaced by spaces, and double underscores are
# replaced by underscores.  The sleazy implementation here also
# converts double spaces to underscores, but nobody in his right mind
# would put double spaces in menu item names, right?

def underscore2space(name):
    return name.replace("_", " ").replace("  ", "_")

# And the not-quite-inverse.
def space2underscore(name):
    return name.replace(" ", "_")

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

def screenwidth():
    try:
        import curses
        scr = curses.initscr()
        width = scr.getmaxyx()[1]
        curses.endwin()
    except ImportError:
        width = 80
    return width

# Function to format a long string so that it fits into strings of
# length width.  Returns a list of strings guaranteed to be shorter
# than width, provided there are some spaces in there somewhere.
def format(line, width):
    linelist = [string.strip(ell) for ell in line.split("\n")]
    outlist = []
    for str in linelist:
        while len(str) > width:
            breakpoint = string.rfind(str," ",0,width)
            outlist.append(str[0:breakpoint])
            str = str[breakpoint+1:]
        else:
            outlist.append(str)
    return outlist


#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Minimal ordered dictionary class.  If more functionality is
# required, get someone else's code off the web.  This class just
# ensures that the objects are returned in the order in which they
# were added.

class OrderedDict(dict):
    def __init__(self):
        dict.__init__(self)
        self._keys = []
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if key not in self._keys:
            self._keys.append(key)
    def setdefault(self, key, dflt):
        if key not in self._keys:
            self._keys.append(key)
        return super(OrderedDict, self).setdefault(key, dflt)
    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)
    def clear(self):
        self._keys = []
        dict.clear(self)
    def keys(self):
        return self._keys
    def values(self):
        return [dict.__getitem__(self, key) for key in self._keys]
    def items(self):
        return [(key, dict.__getitem__(self, key)) for key in self._keys]
    def reorder(self, keylist):
        # Make sure that our keys are in the order given by keylist.
        # keylist must contain all of our keys, but may contain more.

        ## Check for keys in self._keys that aren't in keylist
        unlisted = [key for key in self._keys if key not in keylist]

        self._keys = [key for key in keylist if key in self._keys] + unlisted
    def __eq__(self, other):
        return (isinstance(other, OrderedDict)
                and self._keys == other._keys
                and super(OrderedDict, self).__eq__(other))
    def iterkeys(self):
        return iter(self._keys)
    def replace(self, oldkey, newkey, newval):
        i = self._keys.index(oldkey)
        self._keys[i] = newkey
        dict.__delitem__(self, oldkey)
        dict.__setitem__(self, newkey, newval)
        

import itertools

## TODO 3.1: Should OrderedSet be derived from set, instead of containing an
## OrderedDict?

class OrderedSet:
    def __init__(self, iterable=None):
        self.data = OrderedDict()
        if iterable:
            for item in iterable:
                self.data[item] = 1
    def __len__(self):
        return len(self.data)
    def __contains__(self, item):
        return item in self.data
    def __iter__(self):
        return self.data.iterkeys()
    def add(self, item):
        self.data[item] = 1
    def remove(self, item):
        del self.data[item]
    def discard(self, item):
        try:
            del self.data[item]
        except KeyError:
            pass
    def replace(self, old, new):
        self.data.replace(old, new, 1)
    def clear(self):
        self.data = OrderedDict()
    def union(self, other):
        result = OrderedSet(self.data.keys())
        for item in other:
            result.add(item)
        return result
    def __or__(self, other):
        if not isinstance(other, OrderedSet):
            return NotImplemented
        return self.union(other)
    def intersection(self, other):
        common = itertools.ifilter(other.data.has_key, self)
        return self.__class__(common)
    def __and__(self, other):
        if not isinstance(other, OrderedSet):
            return NotImplemented
        return self.intersection(other)
    def copy(self):
        return OrderedSet(self)
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.data.keys())
    def __eq__(self, other):
        return self.data == other.data
    def __ne__(self, other):
        return self.data != other.data
    def __add__(self, other):
        return self.union(other)

    __str__ = __repr__
        
        
#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# A list-like object in which space can be reserved so that it doesn't
# have to be reallocated all the time.  It doesn't support all of the
# slice operations that a real list would. (__del__ and __setitem__
# aren't provided for slices.  __getitem__ is.)


class ReservableList:
    def __init__(self, n=0):
        self._list = [None]*n
        self._length = 0
    def __len__(self):
        return self._length
    def __getitem__(self, i):
        if type(i) is types.SliceType:
            start, stop, step = i.indices(self._length)
            # No need to check bounds on slices.
            return self._list[start:stop:step]
        else:                           # not a slice
            if i >= self._length or i < -self._length:
                raise IndexError(i, "is out of range")
            if i >= 0:
                return self._list[i]
            return self._list[self._length+i] # i < 0
    def __setitem__(self, i, val):
        if i >= 0:
            if i >= self._length:
                raise IndexError("Reservable list index out of range")
            self._list[i] = val
        else:
            if i < -self._length:
                raise IndexError("Reservable list index out of range")
            self._list[self._length+i] = val
    def capacity(self):
        return len(self._list)
    def reserve(self, size):
        if size <= len(self._list):
            return
        new_list = self._list + [None]*(size-len(self._list))
        self._list = new_list
    def reverse(self):
        oldsize = len(self._list)
        newlist = self._list[:self._length]
        newlist.reverse()
        self._list = newlist + [None]*(oldsize - self._length)
    def append(self, x):
        if self._length == len(self._list):
            self._list.append(x)
        else:
            self._list[self._length] = x
        self._length += 1
    def __delitem__(self, i):
        oldsize = len(self._list)
        if type(i) is types.IntType and i >= self._length or i<-self._length+1:
            raise IndexError(i, "is out of range")
        del self._list[i]
        self._length -= oldsize - len(self._list)
    def __repr__(self):
        return repr(self._list[:self._length])
    def __add__(self, other):
        return self._list[:self._length] + other
    def __radd__(self, other):
        return other + self._list[:self._length]
    def sort(self):
        if self._length == len(self._list):
            self._list.sort()
        else:
            self._list[:self._length] = sorted(self._list[:self._length])

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

def _find_machine_epsilon():
    eps = 1.0
    while 1.0 + eps/2. != 1.0:
        eps = eps/2.
    return eps

machine_epsilon = _find_machine_epsilon()

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

# Given iterable objects, obj0, obj1, ..., and a function fn, return
# another iterable object that is effectively
##    [fn(o0, o1, ...) for o in zip(obj0, obj1, ...)]
## ie
##    map(fn, obj0, obj1, ...)
# without actually constructing a list containing all of the fn(o)'s.

# Naive ways of doing this, using map or itertools.imap, convert the
# iterable into either a tuple, list, or generator.  Tuples and lists
# take up memory, and generators cannot be iterated over repeatedly.
# This method creates a multi-pass iterable.

# Usage:
#   x = some iterable object.
#   def f(y):  return some function of y
#   mapped_x = MappedIterable(f, x)
#   for y in mapped_x: do something with y
#   for y in mapped_x: do something with y again

class MappedIterable(object):
    def __init__(self, fn, *obj):
        self.iterables = obj
        self.fn = fn
    def __iter__(self):
        # Each iteration over self creates a new _MappedIterator, so
        # the iteration starts over at the beginning.
        return _MappedIterator(self)
    def __repr__(self):
        return "MappedIterable(fn=%s, iterables=%s)" % (self.fn, self.iterables)

class _MappedIterator(object):
    def __init__(self, mappediterable):
        self.iterators = map(iter, mappediterable.iterables)
        self.fn = mappediterable.fn
    def __iter__(self):
        return self
    def next(self):
        return self.fn(*map(next, self.iterators))

## For debugging, if you don't trust MappedIterable...
# def MappedIterable(fn, *obj):
#     return map(fn, *obj)

#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

if __name__=='__main__':
    l0 = [0, [1,2],[3,[4]], 5]
    l1 = ['zero', 'one', 'two', 'three', 'four', 'five']
    print unflatten(l0, l1)
