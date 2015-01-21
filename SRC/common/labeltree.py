# -*- python -*-
# $RCSfile: labeltree.py,v $
# $Revision: 1.61.2.4 $
# $Author: langer $
# $Date: 2014/12/08 19:41:51 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# LabelTree is a tree whose contents are indexed by a colon separated
# list of names.  Each node has a string label.  The sequence of
# labels that goes from the root to a node of the tree is the node's
# "path". The path can be specified either as a single string, with
# colons between the nodes' labels, or a list of strings.  That is,
# tree["a:b"] is the same as tree[["a", "b"]].  The function
# makePath() converts from the colon form to the list form.

# The LabelTree differs from a plain old dictionary in that within
# each subtree, the nodes are ordered in the order in which they were
# added.  This lets menus constructed from the tree have their items
# in a specified order.

# The LabelTree classes can construct a corresponding OOFMenu
# heirarchy with the makeOOFMenu() function.  Because it may be
# necessary to make more than one OOFMenu from a single LabelTree, the
# makeOOFMenu() and getOOFMenu() functions take a 'key' argument,
# which can be anything, almost.  The tree objects use the keys to
# store their associated OOFMenu objects in a WeakKeyDictionary.

# LabelTree.makeOOFMenu() takes two specific arguments:
#   name:  the name of the menu.  If None, it defaults to the name
#          of the top node of the tree.  All other entries in the menu
#          derive their names from the corresponding tree nodes.
#   key:   described above.

# All other arguments to makeOOFMenu() are passed through to the
# OOFMenu and OOFMenuItem constructors.  This allows you to specify a
# callback function for the menus.  However, it's not possible to
# specify a different callback for different menu items.  Therefore,
# the 'data' member of the OOFMenuItem is set to the LabelTreeLeaf
# object.  If the menuitem should have parameters, they are created by
# calling a callback, which is passed in as the param_func argument to
# makeOOFMenu().  The argument to param_func is the object stored in
# the LabelTreeLeaf.  It must return a list of Parameter objects.
# Similarly, the kwarg_func argument to makeOOFMenu() is a callback
# function that is called to get extra keyword arguments that need to
# be passed to the OOFMenuItem constructor.

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.ooferror import ErrUserError
from ooflib.common import debug
from ooflib.common.IO import oofmenu
from types import *
import string
import sys

# Data class for holding arguments to the menu within the
# Labeltree object.  Separates the position argument tuple
# from the keyword argument dictionary in the usual way.
# Also carries the parameter-retrieval function around.
class MenuArgs:
    def __init__(self, paramfunc, kwarg_func, args, kwargs):
        self.paramfunc = paramfunc
        self.kwarg_func = kwarg_func
        self.args = args
        self.kwargs = kwargs

def makePath(name):
    # turn a name into a path, which is a list of strings
    if name is None:                    # special case
        return None
    if type(name)==ListType and type(name[0])==StringType: # it's already a path
        return name[:]                  # return a copy
    elif type(name)==StringType:
        path = name.split(':')          # separate colon delimited substrings
##        while path and not path[-1]:
##            path = path[:-1]
        return path
    else:
        raise TypeError('Bad argument to labeltree.makePath: %s' % name)

# LabelTree is the root class of an ordered set of objects, all of
# which (except the root itself) are LabelTreeNode objects.
# This tree is almost homogeneous, and dynamic, in that the
# corresponding menu objects can be created on-the-fly during
# tree construction, or all at once after the initial menuless
# tree has been constructed.

class LabelTreeKeyError:
    def __init__(self, key):
        self.key = key
    def add(self, path):
        self.key = path + ":" + self.key
        return self

class LabelTreeNode:
    def __init__(self, name="", parent=None, object=None, ordering=0):
        self.name = name
        self.parent = parent
        if parent:
            self.root = parent.root
        else:
            self.root = self
        self.object = object
        self.ordering = ordering
        self.nodes = []
        self.menus = {}

    def secret(self):
        try:
            return self.object and self.object.secret()
        except AttributeError:
            return 0

    def subTree(self, name):
        if not name or not name[0]:
            raise LabelTreeKeyError("<empty string>")
        path = makePath(name)
        return self._subTreeSearch(path)
    def _subTreeSearch(self, path):
        for node in self.nodes:
            if node.name == path[0]:
                if len(path) == 1:
                    return node
                else:
                    try:
                        return node._subTreeSearch(path[1:])
                    except LabelTreeKeyError, exc:
                        raise exc.add(path[0])
        raise LabelTreeKeyError(':'.join(path))
    def __getitem__(self, name):
        return self.subTree(name)

    def __len__(self):                  # counts nodes in the tree
        return 1 + reduce(lambda x,y: x+len(y), self.nodes, 0)

    def __hash__(self):
        return id(self) % sys.maxint
##        return hash(self.parent) | hash(self.name) | hash(self.ordering)

    def nleaves(self):
        if len(self.nodes) == 0:
            return 1
        return reduce(lambda x,y: x + y.nleaves(), self.nodes, 0)



    # Menu construction.
    
    # The param_func argument is an optional function
    # which can be used to retrieve object-specific parameters.
    def makeOOFMenu(self, name=None, key=None,
                    param_func=None, kwarg_func=None, *args, **kwargs):

        name = name or self.name

        if param_func:
            argdict = {}
            argdict.update(kwargs)
            
            par_list = param_func(self.object)
            try: # Create a new list.  Do *not* use +=!
                argdict['params'] = argdict['params'] + par_list
            except KeyError:
                argdict['params'] = par_list

        else:
            argdict = kwargs

        if kwarg_func:
            argdict.update(kwarg_func(self.object))

        menu = oofmenu.OOFMenuItem(name, *args, **argdict)
        menu.data = self.object
        self.menus[key] = menu
        # This loop is a no-op if nodes is an empty list.
        for node in self.nodes:
            menu.addItem(node.makeOOFMenu(node.name, key,
                                          param_func, kwarg_func,
                                          *args, **kwargs))
        return menu



    
    # Store the menu arguments in the root.
    def set_menu_args(self, key, paramfunc, kwarg_func, args, kwargs):
        self.root.menuargs[key] = MenuArgs(paramfunc, kwarg_func, args, kwargs)

    def get_menu_args(self,key):
        return self.root.menuargs[key]

    def __setitem__(self, name, obj, ordering=0):
        # 'name' is a colon separated path along the tree...
        path = makePath(name)

        if len(path) == 1:
            # At the end of the path.  Create a leaf.  Object finally
            # gets assigned.
            leaf = LabelTreeNode(name=path[0], parent=self,
                                 object=obj, ordering=ordering)
            # Add the new leaf to the reverse dictionary.
            self.root.reverse_dict[obj]=leaf
            # Add the menu(s)
            for (k, menu) in self.menus.items():
                menuargs = self.get_menu_args(k) # Get menu args from root.

##                # Take care of help string
##                try:
##                    if menuargs.kwargs.has_key('help') and leaf.object.help:
##                        try:
##                            menuargs.kwargs['help'] = leaf.object.help[k]
##                        except AttributeError:
##                            menuargs.kwargs['help'] = leaf.object.help
##                        except KeyError:
##                            pass
##                except AttributeError:
##                        pass
##                # Take care of "discussion"
##                try:
##                    if menuargs.kwargs.has_key('discussion') and \
##                           leaf.object.discussion is not None:
##                        try:
##                            menuargs.kwargs['discussion'] = \
##                                                      leaf.object.discussion[k]
##                        except AttributeError:
##                            menuargs.kwargs['discussion'] = \
##                                                      leaf.object.discussion
##                        except KeyError:
##                            pass
##                except AttributeError:
##                        pass
                
                menu.addItem(leaf.makeOOFMenu(leaf.name, k, menuargs.paramfunc,
                                              menuargs.kwarg_func,
                                              *menuargs.args, **menuargs.kwargs)
                             )
##                menuargs.kwargs['help'] = None
##                menuargs.kwargs['discussion'] = None
                
            # 
            self.nodes.append(leaf)
            self.nodes.sort() # SORT
            #
            # Notify the switchboard, passing the parent of the
            # tree.
            switchboard.notify( (self.root, "insert"), self, leaf)
        else:
            # Not at the end of the path.  Recursively descend a level.
            nodename = path[0]
            # Look for existing subtree.
            for node in self.nodes:
                if node.name == nodename:
                    if node.ordering > ordering:
                        node.ordering = ordering
                        if self.parent:
                            self.parent.nodes.sort() # SORT using __cmp__ 
                    # Descend into existing subtree.  Pass the ordering.
                    node.__setitem__(path[1:], obj, ordering)
                    return
            # Didn't find an existing subtree.  Make one, but don't
            # assign the object.
            newnode = LabelTreeNode(name=path[0], parent=self,
                                    object=None, ordering=ordering)
            # Add intermediate-level menu
            for (k, menu) in self.menus.items():
                menuargs = self.get_menu_args(k)
                menu.addItem(
                    newnode.makeOOFMenu(newnode.name, k, menuargs.paramfunc,
                                        *menuargs.args, **menuargs.kwargs))
            self.nodes.append(newnode)
            self.nodes.sort()  # SORT.
            switchboard.notify((self.root, "insert"), self, newnode)
            # Recursive call to __setitem__.  Propagate the ordering.
            newnode.__setitem__(path[1:], obj, ordering)
    #
    # Delete needs to get rid of the entry, and clean up the menus
    # and the reverse dictionary.  Coordinates with the GUI dictionary
    # via the switchboard callback.
    def delete(self, name):
        path = makePath(name)
        if len(path) == 1:
            for i in range(len(self.nodes)): # Use index so "del" works.
                if self.nodes[i].name==path[0]:
                    # Think of the children.
                    if len(self.nodes[i].nodes)!=0:
                        raise ErrUserError(
                            "Attempt to delete non-leaf from labeltree.")
                    else:
                        # Then do the deletion, in the tree and
                        # in the menus and reverse dictionary.
                        oldnode = self.nodes[i]
                        if self.nodes[i].object is not None:
                            del self.root.reverse_dict[self.nodes[i].object]
                        del self.nodes[i]
                        for menu in self.menus.values():
                            menu.removeItem(path[0])
                        # Tell the switchboard...
                        switchboard.notify((self.root, "delete"), oldnode)
                    break 
                        
        # Otherwise, not at bottom. Recurse. 
        else:
            nodename = path[0]
            for node in self.nodes:
                if node.name == nodename:
                    node.delete(path[1:])
                    break

    # prune() is like delete(), except that after removing the given
    # node, it recursively deletes parent nodes if the parents have no
    # other children.
    def prune(self, name):
        path = makePath(name)
        self.delete(path)
        path = path[:-1]
        while path and not self.subTree(path).nodes:
            self.delete(path)
            path = path[:-1]

    def depth(self, d=0):
        # Probably not terribly efficient, but cute, if it works...
        # Returns the depth of the deepest node.
        return max([x.depth(d+1) for x in self.nodes] + [d])
    
    def rename(self, newname):
        # Only works at local level.  newname can't be a path.
        oldpath = self.pathlist()
        self.name = newname
        # need to fix menus and gui trees
        for menu in self.menus.values():
            menu.name = newname
        switchboard.notify((self.root, 'rename'), self)
    
    # Returns a list of strings leading up to this node.
    def pathlist(self):
        if self.parent:
            return self.parent.pathlist() + [self.name]
        else:
            return []
    def path(self):
        return string.join(self.pathlist(), ':')

    # Returns a list of paths to all leaves of the subtree rooted at this node.
    def leafpaths(self, condition=lambda x: 1):
        plist = []
        for node in self.nodes:
            pl = node.leafpaths(condition=condition)
            if pl:
                for lst in pl:
                    plist.append([node.name] + lst)
            else:
                if node.object and condition(node.object):
                    plist.append([node.name])
        return plist

    # Same as leafpaths(), but also includes non-leaf nodes.  UNTESTED
##    def nodepaths(self):
##        plist = []
##        for node in self.nodes:
##            pl = node.nodepaths()
##            plist += [[node.name]] + [[node.name] + x for x in pl]
##        return plist

    def children(self):
        return [node.name for node in self.nodes]

    def numberOneChild(self):
        if self.object is not None:
            return self.object
        if self.nodes:
            return self.nodes[0].numberOneChild()

    def getObjects(self):
        objlist = []
        if self.object is not None:
            objlist.append(self.object)
        for node in self.nodes:
            objlist += node.getObjects()
        return objlist

    def dump(self, prefix):
        repr = prefix + self.name + "\n"
        for node in self.nodes:
            repr += node.dump(prefix + '  ')
        return repr
    def apply(self, function):
        if self.object is not None:
            function(self.object)
        for node in self.nodes:
            node.apply(function)
    def apply2(self, function, postfunc=None, *args, **kwargs):
        function(self.path(), self.object, *args, **kwargs)
        for node in self.nodes:
            node.apply2(function, postfunc, *args, **kwargs)
        if postfunc:
            postfunc(self.path(), self.object, *args, **kwargs)
    def __repr__(self):
        repr = ["%s(%s):" % (self.__class__.__name__, self.name)] + \
               [n.name for n in self.nodes]
        return string.join(repr, ' ')
##        repr = "%s(%s):\n" % (self.__class__.__name__, self.name)
##        for node in self.nodes:
##            repr += node.dump('')
        return repr
  
    # Menu construction only occurs in the root instance, so it's in
    # the LabelTree class.  Menu retrieval is in the LabelTreeNode
    # class because it can be invoked at any level.
    def getOOFMenu(self, key):
        return self.menus[key]
    
    # Comparison routine for sorting on orderings.
    def __cmp__(self,other):
        return cmp(self.ordering, other.ordering)

# Special object for the root of a labeltree.
class LabelTree(LabelTreeNode):
    def __init__(self, name="", object=None, ordering=0):
        self.reverse_dict = {}
        LabelTreeNode.__init__(self, name=name, parent=None,
                               object=object, ordering=ordering)
        self.menuargs = {} # Set at menu-time.
        # Dictionary keyed by the .object objects, with corresponding
        # LabelTreeNode objects as values.  Maintained in __setitem__.
        # which can be used to retrieve object-specific parameters.

    def subTree(self, name):
        # The unnamed subtree of a LabelTree is the whole tree.  This
        # *doesn't* apply to nodes not at the root of the tree.
        if not name or not name[0]:
            return self
        return LabelTreeNode.subTree(self, name)
    
    # Root version of MakeOOFMenu stores the menu args,
    # so newly-added objects can get the same ones.  Args include
    # a parameter-retrieval function, param_func, which must
    # return a list of parameters.
    def makeOOFMenu(self, name=None, key=None,
                    param_func=None, kwarg_func=None, *args, **kwargs):

        # Create an OOFMenu for the tree.  Store the arguments in
        # the root so newly-added objects can get the same menu.
        # Also locally store the parameter-retrieval function.
        # Keys allow for multiple menus per labeltree.
        self.set_menu_args(key, param_func, kwarg_func, args, kwargs)

        return LabelTreeNode.makeOOFMenu(self, name, key,
                                         param_func, kwarg_func,
                                         *args, **kwargs)
    

    # Given an object stored in the tree, return its path.  That is,
    #     tree[tree.objpath(object)] is object.
    def objpath(self, obj):
        return self.reverse_dict[obj].path()

    def contains(self, obj):
        return obj in self.reverse_dict
