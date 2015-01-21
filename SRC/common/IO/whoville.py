# -*- python -*-
# $RCSfile: whoville.py,v $
# $Revision: 1.142.4.19 $
# $Author: langer $
# $Date: 2014/12/08 20:16:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# The 'who' of a display layer is the mesh or image or whatever that's
# being plotted.  An alternative name for 'Who' might be
# 'LayerContext', but we decided that that was too boring.

# Different kinds of Whos (eg, Meshes or Images) live in different
# WhoClasses.  There's a single WhoClass instance for each kind of
# Who.  The different kinds of Whos can correspond to different
# subclasses of Who, although they don't have to.  If a subclass is
# used, it must be passed in to the WhoClass constructor.

# For example, if there are display methods that work on Sneetches,
# then one could define
#    class SneetchWho(Who):
#        def __init__(self, name, classname, obj):
#             Who.__init__(self, name, classname, obj)
#             whatever...
# and create a WhoClass for them to live in like this:
#    sneetchclass = WhoClass('Sneetch', 6, SneetchWho)
# Each time a new Sneetch is created, it will have to be added to the
# class like this:
#    sneetch = Sneetch(...)
#    sneetchclass.add(name, sneetch)
# Then it will automatically be made available with the given name in
# the list of Sneetches in the LayerEditor.

# WhoClasses can be arranged hierarchically, by providing the "parent"
# argument to the WhoClass constructor.  The idea is that the objects
# stored in the child class somehow belong to their parent.  If a
# WhoClass has a parent, then when a Who object is added to the class,
# the "name" argument to WhoClass.add() must be a LabelTree path,
# either a colon separated string, or a list of strings.

# For an actual example, see the Mesh class in SRC/engine/mesh.py.
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
# from ooflib.SWIG.common import timestamp
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import ringbuffer
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from types import *
import string
import struct


whoClasses = []

# Since debugging the locking code here is a fairly common
# requirement, and commenting out the debugging lines is a pain, they
# can all be turned on and off by setting _debuglocks.
_debuglocks = False

class Who(object):
    ## A Who is a wrapper/container to administer objects of the
    ## same type. Subclasses and instances of this class are
    ## referred to as <something>Context or <something>Who.
    ## Please also read note below in the WhoClass class.
    def __init__(self, name, classname, obj, parent, secretFlag = 0):
        self._name = name
        self._obj = obj
        self.classname = classname      # not necessarily the Python class name,
                                        # but just a name to be listed in GUI.
        self.parent = parent
        self.switchboardCallbacks = []
        # self.timestamp = timestamp.TimeStamp()

        ## Locking variables
        self.have_reservation = 0
        
        ## Locking methods.
        self.reservation_lock = lock.Lock() ## holds the Who writing privileges

        # Create an rwlock.  Subclasses may share this lock with their
        # contained objects.
        self.rwLock = lock.RWLock()
            
        ## secret flag for hiding it from the user
        ## TODO 3.1: For some situation where this who object need to
        ## be secret for some kind of display and not for another the
        ## boolean type would not be enough. We will have to think of
        ## another structure to handle different kind of display and
        ## different kind of secrecy for those displays.
        self.secretFlag = secretFlag
        
    def secret(self):
        return self.secretFlag
    
    def name(self):
        return self._name

    def getObject(self, *args): 
        return self._obj

    # Returns string of colon-separated names.
    def path(self):
        # The lookup can fail if the object is in the process of being
        # deleted.
        try:
            return self.getClass().getPath(self)
        except KeyError:
            pass

    # The resolve() function allows for Who objects that are stand-ins
    # for other Who objects.  For example, there is a derived Who
    # class that refers to the topmost Who object in a graphics
    # window.  The resolve() function in the derived class returns the
    # topmost object in the base class.
    def resolve(self, *args, **kwargs):
        return self

    # When "exclude" is true, it'll exclude "name" from the look-up list
    # of names. This is specifically to allow renaming with the same name.
    def rename(self, name, exclude=None):
        # debug.fmsg()
        ## TODO 3.1: PARALLELIZE THIS FUNCTION
        oldpath = self.path()           # local copy! path will change
        # Make sure the new name is unique.  Changing the name
        # silently here is probably a bad idea.
        newname = self.getClass().uniqueName(
            labeltree.makePath(oldpath)[:-1]+[name], exclude=exclude)
        self._name = newname
        if hasattr(self._obj, "rename"):
            self._obj.rename(newname)
        self.pause_writing()
        # debug.fmsg("paused writing")
        switchboard.notify('rename who', self.classname, oldpath, self.name())
        # debug.fmsg("back from first sb call")
        switchboard.notify(('rename who', self.classname), oldpath, self.name())
        # debug.fmsg("resuming writing")
        self.resume_writing()
        # debug.fmsg("resumed writing")
    def uniqueName(self, name):
        path = labeltree.makePath(self.path())[:-1]
        return self.getClass().uniqueName(path + [name])
    def getClass(self):
        return getClass(self.classname)
    def getClassName(self):
        return self.classname
    def getParent(self):
        return self.parent
    def setParent(self, parent):
        self.parent = parent
    def requestCallback(self, *args):
        self.switchboardCallbacks.append(switchboard.requestCallback(*args))
    def remove(self):
        self._obj = None
        # This can't set parent=None, because self should be locked
        # when this function is called.  If we set parent=None here,
        # then the parent won't be unlocked when self is unlocked.
        map(switchboard.removeCallback, self.switchboardCallbacks)
        self.switchboardCallbacks = [] # removes possible circular references 
    def defunct(self):
        return self._obj is None
    def __repr__(self):
        return 'Who(%s, %s)' % (self.name(), self.classname)
    # def getTimeStamp(self, gfxwindow):
    #     if hasattr(self._obj, 'getTimeStamp'):
    #         return self._obj.getTimeStamp()   # modification time?
    #     return self.timestamp           # creation time

    ## 
    ## Only one thread can make a writing reservation
    ## (reserves the writing privileges). This
    ## thread is called the writing thread.
    ##
    ## If another thread attempts to make a writing reservation
    ## it will block until the thread that holds the writing
    ## privileges gives the privileges up.
    ##
    ## After, during, or before a reservation is made any
    ## thread can read. 
    ##    
    ## When the writing thread announces that it will start writing,
    ## if another thread is reading, the writing thread waits until
    ## reading ends.
    ##
    ## Similarly, when a thread announces that it will start reading,
    ## if another thread is writing, the reading thread will
    ## wait until the writing thread announces that it finished.
    ##

    ## TODO 3.1: Get rid of reserve() and cancel_reservation().
    ## Calling begin_writing(); pause_writing() has the same effect as
    ## reserve().  Doing this may be tricky (and therefore
    ## undesirable) if in some contexts it's hard to know whether to
    ## call begin_writing() or resume_writing().
    
    def reserve(self):
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg('reserving', self)
        self.reservation_lock.acquire()
        if _debuglocks:
            debug.fmsg('reserved', self)
        self.have_reservation = 1
        switchboard.notify("made reservation", self)
    def cancel_reservation(self):
        self.have_reservation = 0
        self.reservation_lock.release()
        switchboard.notify("cancelled reservation", self)
    def query_reservation(self):
        return self.have_reservation
    
    def begin_reading(self):
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg('acquiring read lock', self, id(self))
        self.rwLock.read_acquire()
        parent = self.getParent()
        if parent:
            parent.begin_reading()
        if _debuglocks:
            debug.fmsg('acquired read lock', self, id(self),
                       self.rwLock.nReaders())

    def end_reading(self):
        parent = self.getParent()
        if parent:
            parent.end_reading()
        self.rwLock.read_release()
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg('ended reading', self, id(self), self.rwLock.nReaders())

    def begin_writing(self):
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg('acquiring write lock', self, id(self))
        self.rwLock.write_acquire()
        # While changing an object, make sure that its parents don't
        # change as well, because that could effectively change the
        # object...  Since we're not actually changing the parent, we
        # just acquire the read lock.
        parent = self.getParent()
        if parent:
            parent.begin_reading()
        if _debuglocks:
            debug.fmsg('acquired write lock', self, id(self))

    def end_writing(self):
        parent = self.getParent()       # See comment above
        if parent:
            parent.end_reading() 
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg('end writing', self, id(self))
        self.rwLock.write_release()

    def pause_writing(self):
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg('pause writing', self, id(self))
        self.rwLock.write_pause()
        
    def resume_writing(self):           # a useful skill for job applicants
        if _debuglocks:
            debug.dumpCaller()
            debug.fmsg('resuming writing', self, id(self))
        self.rwLock.write_resume()
        if _debuglocks:
            debug.fmsg('resumed writing', self, id(self))

    def parallelize(self):
        pass ## redefined in subclasses, if needed

historysize = 50
        
class WhoDoUndo(Who):                   # that you do so well
    "A WhoClass that supports undo/redo operations."
    def __init__(self, path, classname, obj, parent, secretFlag=0,
                 overwritefn=None):
        Who.__init__(self, path, classname, obj, parent, secretFlag = 0)
        self.undobuffer = ringbuffer.RingBuffer(self.getClass().historysize+1,
                                                overwritefunc=overwritefn)
        # Make sure to call most-derived-class version of this.
        self.begin_writing()
        self.pushModification(obj)
        self.end_writing()

    def setUndoBufferSize(self, n):
        self.undobuffer.resize(n+1)

    def contains(self, obj):
        return obj in self.undobuffer

    def pushModification(self, obj, signal=True):
        old = self._obj
        self.undobuffer.push(obj)
        self._obj = self.undobuffer.current()
        # These signals are distinct.  'who changed' (sent in
        # pushModificationSignal) causes layers to be redrawn.
        # 'whodoundo push' triggers stuff that should be done before
        # any redraws (even redraws triggered by other objects).
        switchboard.notify(('whodoundo push', self.classname),
                           self, old, self._obj)
        # The 'who changed' signal will cause the graphics window to
        # be redrawn, so other threads may need to get read access.
        if signal:
            self.pushModificationSignal()

    def pushModificationSignal(self):
        self.pause_writing()
        # Switchboard callbacks usually run on subthreads -- this
        # pause/resume pair might be useless, but it's harmless.
        switchboard.notify(('who changed', self.classname), self)
##        self.parallelPushModification(self._obj)
        self.resume_writing()


    def parallelPushModification(self, obj = None):
        pass ## does the right thing on subclass
    
    def undoModification(self):
        try:
            old = self._obj
            self._obj = self.undobuffer.prev()
        except IndexError:
            pass
        else:
            self.undoHookFn(old, self._obj)
            # self._obj.getTimeStamp().increment()
            self.pause_writing()
            switchboard.notify(('who changed', self.classname), self)
##            self.parallelUndoModification() ## subclasses do the right thing
            self.resume_writing()
            
    def parallelUndoModification(self):
        pass

    def redoModification(self):
        try:
            old = self._obj
            self._obj = self.undobuffer.next()
        except IndexError:
            pass
        else:
            self.redoHookFn(old, self._obj)
            # self._obj.getTimeStamp().increment()
            self.pause_writing()
            switchboard.notify(('who changed', self.classname), self)
##            self.parallelRedoModification() ## subclasses do the right thing
            self.resume_writing()

    def parallelRedoModification(self):
        pass
    
    # Subclasses can redefine redoHookFn and undoHookFn to provide
    # extra processing after the stack has changed but before the "who
    # changed" signal is sent.
    
    def redoHookFn(self, oldobj, newobj):
        pass

    def undoHookFn(self, oldobj, newobj):
        pass

    def undoable(self):
        return not self.undobuffer.atBottom()

    def redoable(self):
        return not self.undobuffer.atTop()

    def remove(self):
        self.undobuffer.clear()
        self.undobuffer.overwrite = None
        Who.remove(self)

## TODO 3.1: Keep a copy of the original object, so that we can
## implement an Undo All feature.

## TODO 3.1: Keep some identification about what operations created
## each modification, so that the tooltips for the Undo and Redo
## buttons can say what they're undoing or redoing.

##################

# WhoProxies are objects that refer to real Who objects.  The object
# referred to can depend upon in which graphics window the Who is
# being displayed.  WhoProxy objects are created *automatically* for
# each WhoClass.  To define a new type of proxy, create a subclass of
# WhoProxyClass.  The subclass must define two functions:
#   WhoProxyClass.resolve(self, proxy, gfxwindow)
#      This returns the actual Who object that the given WhoProxy
#      refers to in the given graphics window.  It can use
#      proxy.whoclass to find out the WhoClass to which the proxy
#      belongs.
# #  WhoProxyClass.getTimeStamp(self, proxy, gfxwindow)
# #     This must return a TimeStamp object indicated when the proxy
# #     changed, ie, when it started referring to the object it's
# #     currently referring to.


class WhoProxyClass:
    allProxyClasses = {}
    def __init__(self, name):
        self._name = name
        WhoProxyClass.allProxyClasses[name] = self
        for whoclass in whoClasses:
            if name in whoclass.proxyClasses:
                whoclass.addProxy(self.makeProxy(whoclass))
    def name(self):
        return self._name
    def makeProxy(self, whoclass):
        return WhoProxy(self, whoclass)

        
class WhoProxy(Who):
    allProxies = []
    def __init__(self, proxyclass, whoclass):
        self.proxyclass = proxyclass
        self.whoclass = whoclass
        self.classname = whoclass.name()
    def getObject(self, gfxwindow):
        return self.resolve(gfxwindow).getObject()
    def resolve(self, gfxwindow):       # The actual Who we're a proxy for.
        return self.proxyclass.resolve(self, gfxwindow)
    def name(self):
        return self.proxyclass.name()
    # def getTimeStamp(self, gfxwindow):
    #     return max(self.proxyclass.getTimeStamp(self, gfxwindow),
    #                self.resolve(gfxwindow).getTimeStamp(gfxwindow))
        

# WhoWidgets can be told to include only certain Who objects.  The
# default is to exclude proxy objects, which is done by passing this
# function to the WhoWidget's constructor:

def excludeProxies(who):
    return not isinstance(who, WhoProxy)

# WhoWidgets can sort the list of displayed Who objects.  This is the
# default sorting.  Sorting functions take and return a list of paths,
# each of which is a list of names (eg, [['microstructure',
# 'skeleton'], ['mic2', 'skel2']]).

def proxiesLast(wholist):
    proxynames = [name for name in wholist if name[0] and name[0][0] == '<']
    othernames = [name for name in wholist if name[0] and name[0][0] != '<']
    return othernames + proxynames

#####################################
#####################################

## TODO OPT: Each WhoClass should probably have a lock on its LabelTree to
## make it thread safe.
    
class WhoClass:
    ## A WhoClass is a container, a manager of instances
    ## of Who objects. This wrapping is necessary, in order
    ## to maintain uniformity on the way aggregates of the
    ## same type of Who are handled.
    ## Subclasses and instances of the WhoClass are interchangeably
    ## referred as <something>contexts (<--note the "s") or <something>s
    def __init__(self, name, ordering, parentClass=None,
                 instanceClass=Who, proxyClasses=[], secret=0):
        self._name = name               # names must be unique!
        self.ordering = ordering
        self.parentClass = parentClass
        self.instanceClass = instanceClass
        # list of names of proxies that should be created for this class:
        self.proxyClasses = proxyClasses
        self.members = labeltree.LabelTree()
        self.nmembers = 0
        self.nproxies = 0
        ## TODO 3.1: For situations in which this whoclass object
        ## needs to be secret for some kinds of display and not for
        ## others the boolean type would not be enough. We will have
        ## to think of another structure to handle different kinds of
        ## secrecy for those displays.
        self.secret = secret            # does not appear in GUI if secret==1
        # Insert the new WhoClass in the list of all WhoClasses,
        # updating each class's index.
        global whoClasses
        nwho = len(whoClasses)
        for i in range(nwho):
            if whoClasses[i].ordering > ordering:
                whoClasses.insert(i, self)
                for j in range(i, nwho+1):
                    whoClasses[j]._index = j
                break
        else:
            whoClasses.append(self)
            self._index = nwho

        # Create proxy objects if requested.  The proxy class may not
        # have been loaded yet.  That's ok: when the class is created
        # it will create the proxy for this WhoClass.
        for whoproxyclassname in proxyClasses:
            try:
                whoproxyclass = WhoProxyClass.allProxyClasses[whoproxyclassname]
            except KeyError:
                pass
            else:
                self.addProxy(whoproxyclass.makeProxy(self))
            
        switchboard.notify('new who class', name)

        # Be notified when a who object changes its name, in case that
        # object's WhoClass is a parent class of this class.  If it
        # is, objects in this class need to update their paths.
        switchboard.requestCallback('rename who', self.renameWho)
    def name(self):
        return self._name
    def hierarchy(self):
        hier = [self]                   # list of classes in this hierarchy
        parent = self.parentClass
        while parent is not None:
            hier[0:0] = [parent]        # prepend parent to list
            parent = parent.parentClass
        return hier
    def add(self, name, obj, parent, **kwargs):
        assert (self.parentClass is None and parent is None) \
               or isinstance(parent, self.parentClass.instanceClass)
        path = labeltree.makePath(name)
        if len(path) != len(self.hierarchy()):
            raise ValueError(
                "%s is an invalid name for an object in WhoClass %s"
                             % (name, self.name()))
        # Silently overwrite an old object with the same name.  It's
        # assumed that if we got this far we know what we're doing.
        try:
            oldwho = self[path]
        except KeyError:
            pass
        else:
            self.remove(path)
        whoobj = self.instanceClass(path[-1], self.name(), obj, parent=parent,
                                    **kwargs)
        self.members[path] = whoobj
        self.nmembers += 1
        switchboard.notify('new who', self.name(), path) # generic version
        switchboard.notify(('new who', self.name()), path) # specific version
        whoobj.parallelize() # does useful work in parallel mode
        return whoobj
    def addProxy(self, proxy):
        self.members[proxy.name()] = proxy
        self.nmembers += 1
        self.nproxies += 1
    def clean(self, name):
        path = labeltree.makePath(name)
        try:
            obj = self[path]            # Who instance
        except KeyError:
            raise
        else:
            # Remove the leaf from the tree.  If it's the only leaf on
            # its branch, remove the branch.
            self.members.prune(path)
            obj.remove()
            self.nmembers -= 1
            # The order of these last two signals is important -- the
            # widgets catch the specific signal, and it's helpful to
            # the pages (which catch the generic signal) if the widget
            # is in the new state at page-update-time.
            obj.pause_writing()
            try:
                switchboard.notify(('remove who', self.name()), path) # specific
                switchboard.notify('remove who', self.name(), path) # generic
            finally:
                obj.resume_writing()
    def remove(self, name):
        path = labeltree.makePath(name)
        try: ## TODO: This outer try/except/else is meaningless
            obj = self[path]            # Who instance
        except KeyError:
            raise #pass                        # is "pass" necessary?
        else:
            obj.pause_writing()
            try:
                switchboard.notify('preremove who', self.name(), path)
                switchboard.notify(('preremove who', self.name()), path)
            finally:
                obj.resume_writing()
            # Remove the leaf from the tree.  If it's the only leaf on
            # its branch, remove the branch.
            self.members.prune(path)
            obj.remove()
            self.nmembers -= 1
            # The order of these last two signals is important -- the
            # widgets catch the specific signal, and it's helpful to
            # the pages (which catch the generic signal) if the widget
            # is in the new state at page-update-time.
            obj.pause_writing()
            try:
                switchboard.notify(('remove who', self.name()), path) # specific
                switchboard.notify('remove who', self.name(), path) # generic
            finally:
                obj.resume_writing()

    def renameWho(self, classname, oldpath, newname):
        # Switchboard callback, called when a Who object's name has
        # changed.  If that object is the parent of an object in this
        # class, then the path to objects in this class needs to
        # change as well.

        # First, check to see if the changed object's whoclass is a
        # parent class of this class.
        parents = [whoclass.name() for whoclass in self.hierarchy()]
        if classname not in parents:
            return                      # it's not.

        # Change the path to existing objects of this class, if their
        # paths contain the changed name.
        try:
            subtree = self.members[oldpath]
        except labeltree.LabelTreeKeyError:
            pass                        # this class has no changed children
        else:
            subtree.rename(newname)     # updates menus and guis

    def getPath(self, who):
        # Who objects don't know their paths.  To enforce consistency
        # the path is only stored in the WhoClass LabelTree.
        return self.members.objpath(who)

    def nActual(self):
        return self.nmembers - self.nproxies

    def actualMembers(self):            # returns a list of non-proxy members
        return [who for who in self.members.getObjects()
                if not isinstance(who, WhoProxy)]
        
    def __len__(self):
        return self.nmembers

    def __getitem__(self, which):
        try:
            subtree = self.members[which]
        except labeltree.LabelTreeKeyError, exc:
            obj = None
            missing = exc.key
        else:
            obj = subtree.object
            missing = which
        if obj is None:
            raise KeyError, "There is no %s named %s!" % (self.name(), missing)
        return obj

    # Return a list of all the names currently known, beginning at
    # "base" in the LabelTree.  Names of Who objects for which
    # condition(object) is false are omitted.
    def keys(self, base=None, condition=lambda x:1, sort=None):
        if not base:
            klist = self.members.leafpaths(condition)
        else:
            try:
                root = self.members[base]
            except labeltree.LabelTreeKeyError:
                return []
            else:
                klist = root.leafpaths(condition)
        if sort is not None:
            return sort(klist)
        return klist

    def uniqueName(self, name, exclude=None):
        # Given a LabelTree path (list of strings, or colon separated
        # substrings), returns a single string that doesn't already
        # name a leaf in the same tree.  For example, if the WhoClass
        # contains a Who called "Hey:Bee:Sea", and you call uniqueName
        # with the argument "Hey:Bee:Sea" or ["Hey", "Bee", "Sea"], it
        # will return "Sea<2>".  If you pass in "Hay:Bea:Sea" it will
        # return "Sea".
        path = labeltree.makePath(name)
        try:
            basenode = self.members[path[:-1]]
        except labeltree.LabelTreeKeyError:
            return path[-1]             # subtree doesn't exist yet
        return utils.uniqueName(path[-1], basenode.children(), exclude=exclude)

    def getIndex(self):                 # position of self in list of WhoClasses
        return self._index
    def getNonSecretIndex(self):
        # Position in all WhoClasses, not counting secret classes
        global whoClasses
        count = 0
        for who in whoClasses:
            if who is self:
                return count
            if not who.secret:
                count += 1
    def __repr__(self):
        return 'WhoClass(%s)' % self.name()
    def __cmp__(self, other):
        # comparing names is good enough, because WhoClass names are unique.
        return cmp(self.name(), other.name())

class WhoDoUndoClass(WhoClass):
    def __init__(self, name, ordering, parentClass=None,
                 instanceClass=WhoDoUndo, proxyClasses=[], secret=0):
        WhoClass.__init__(self, name, ordering, parentClass=parentClass,
                          instanceClass=instanceClass,
                          proxyClasses=proxyClasses, secret=secret)
        self.historysize = historysize
        mainmenu.bufsizemenu.addItem(oofmenu.OOFMenuItem(
            utils.space2underscore(name),
            callback=self.setUndoBufferSize,
            # TODO 3.1: Disallow size=0.
            params=[parameter.IntParameter('size', historysize,
                                           tip='number of previous versions to preserve')],
            help="Set the history buffer size for %ss" % name,
            discussion=xmlmenudump.loadFile(
               'DISCUSSIONS/common/menu/bufsize.xml',
               lambda text,obj: text.replace('CLASS', name))
            ))
    def setUndoBufferSize(self, menuitem, size):
        if size <= 0:
            size = 1
        self.historysize = size
        for path in self.members.leafpaths():
            obj = self.members[path].object
            if not isinstance(obj, WhoProxy):
                obj.setUndoBufferSize(size)
                switchboard.notify(('WhoDoUndo buffer change', self.name()))

def getClass(name):
    for whoclass in whoClasses:
        if whoclass.name() == name:
            return whoclass
    return None

#####################

# Functions to use as the "condition" argument in WhoClassParameterWidgets.

def noSecretClasses(whoclass):
    return not whoclass.secret

def allClasses(whoclass):
    return 1

def onlyWhoDoUndo(whoclass):
    return isinstance(whoclass, WhoDoUndoClass)

####################

def classNames(condition=noSecretClasses):
    return [whoclass.name() for whoclass in whoClasses if condition(whoclass)]

###################################################

# A Parameter whose value is the path to an existing object in a
# given WhoClass.

class WhoParameter(parameter.Parameter):
    def __init__(self, name, whoclass, value=None, default=None, tip=None,
                 auxData={}):
        if isinstance(whoclass, Who):
            self.whoclass = whoclass.getClass()
        elif isinstance(whoclass, WhoClass):
            self.whoclass = whoclass
        else:
            raise ValueError(
                "WhoParameter requires a WhoClass or Who instance.")
        parameter.Parameter.__init__(self, name, value=value, default=default,
                                         tip=tip, auxData=auxData)
    def checker(self, x):
        # x must be the name of a Who instance of the correct
        # WhoClass.
        if not (type(x) == StringType and 
                labeltree.makePath(x) in self.whoclass.keys()):
            raise TypeError("Expected the name of a %s instance."
                            % self.whoclass)
    def __repr__(self):
        return 'WhoParameter(%s, %s, %s, %s)' % (self.name, self.whoclass,
                                                 `self.value`, self.tip)
    def clone(self):
        return self.__class__(self.name, self.whoclass, value=self.value,
                              default=self.default, tip=self.tip)

    structfmt = '>i'
    structlen = struct.calcsize(structfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(WhoParameter.structfmt, len(value)) + value
    def binaryRead(self, parser):
        b = parser.getBytes(WhoParameter.structlen)
        (length,) = struct.unpack(WhoParameter.structfmt, b)
        return parser.getBytes(length)
    def classRepr(self):
        return "%s(%s)" % (self.__class__.__name__, self.whoclass.name())
    def valueDesc(self):
        return "The <link linkend='Section-Concepts-Path'>path</link> to an existing <classname>%s</classname> object." % \
               self.whoclass.name()

# An AnyWhoParameter can be set to the name of a Who object from any
# WhoClass.
class AnyWhoParameter(parameter.StringParameter):
    def valueDesc(self):
        return "The <link linkend='Section-Concepts-Path'>path</link> to an &oof2; object."


# A WhoNameParameter is the name of a Who object, with no restrictions
# on prior existence.  It forbids colons in the name.  It doesn't need
# to know the WhoClass.
class WhoNameParameter(parameter.RestrictedStringParameter):
    def __init__(self, name, value=None, default="", tip=None, auxData={}):
        parameter.RestrictedStringParameter.__init__(
            self, name, exclude=':',
            value=value, default=default, tip=tip, auxData=auxData)
    def __repr__(self):
        return "%s(name='%s', value=%s, default=%s)" % \
               (self.__class__.__name__, self.name, self.value, self.default)

class AutoWhoNameParameter(parameter.RestrictedAutomaticNameParameter):
    def __init__(self, name, resolver, value=None, default=None, tip=None,
                 auxData={}):
        parameter.RestrictedAutomaticNameParameter.__init__(
            self, name, exclude=':', resolver=resolver,
            value=value, default=default, tip=tip, auxData=auxData)
    def clone(self):
        return self.__class__(self.name, self.resolver, self.value,
                              self.default, self.tip, self.auxData)
    def __repr__(self):
        return "%s(name=%s, resolver=%s, truevalue=%s, tip=%s)" % (
            self.__class__.__name__,
            self.name, self.resolver, self.truevalue, self.tip)

# A NewWhoParameter can be set to the name an existing Who object, or
# a new name.  Its widget presents a list of existing objects and a
# place to type in a new name.
class NewWhoParameter(parameter.RestrictedStringParameter):
    def __init__(self, name, whoclass, value=None, default=None, tip=None,
                 auxData={}):
        if type(whoclass)!=InstanceType:
            raise ValueError(
                "WhoParameter requires a WhoClass or Who instance.")
        if isinstance(whoclass, Who):
            self.whoclass = whoclass.getClass()
        elif isinstance(whoclass, WhoClass):
            self.whoclass = whoclass
        else:
            raise ValueError(
                "WhoParameter requires a WhoClass or Who instance.")
        parameter.RestrictedStringParameter.__init__(
            self, name, exclude=':', value=value,
            default=default, tip=tip, auxData=auxData)
    def valueDesc(self):
        return \
            "The <link linkend='Section-Concepts-Path'>path</link> to an existing or new <classname>%s</classname> object." \
            % self.whoclass.name()


class WhoClassParameter(parameter.StringParameter):
    def __init__(self, name, value=None, default=None,
                 condition=noSecretClasses, tip=None, auxData={}):
        self.condition = condition
        parameter.StringParameter.__init__(self, name, value, default, tip)
    def clone(self):
        return WhoClassParameter(self.name, self.value, self.default,
                                 self.condition, self.tip, self.auxData)
    def checker(self, x):
        if x and getClass(x) is None:
            raise TypeError("Expected a WhoClass name. Got %s" % `x`)
    def valueDesc(self):
        return "The name of a class of OOF2 objects (eg, <userinput>'Microstructure'</userinput> or <userinput>'Skeleton'</userinput>)."
        
##########################

# noclass = WhoClass('Nothing', 0)
# nobody = noclass.add('Nobody', None, parent=None)
