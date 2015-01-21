# -*- python -*-
# $RCSfile: gfxLabelTree.py,v $
# $Revision: 1.43.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# A wrapper for a GTK+ Tree widget whose structure mirrors a given
# LabelTree.  The GfxLabelTree is automatically updated when the
# LabelTree changes.

# Selecting, deselecting, or double clicking a tree entry
# calls the user-supplied callback function.  The callback function
# takes at least two arguments: the name of the signal which triggered
# the callback ('select', 'deselect', or 'doubleclick') and the node
# of the tree that was selected or deselected.  Extra arguments to the
# GfxLabelTree constructor are also passed through to the callback.


from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
import gobject
import gtk
import string


class GfxLabelTree:
    def __init__(self, tree, expand=1, callback=None, name=None,
                 *callbackargs, **callbackkwargs):
        debug.mainthreadTest()
        self.tree = tree                # associated LabelTree
        self.callback = callback
        self.callbackargs = callbackargs
        self.callbackkwargs = callbackkwargs

        self.rccb = None

        # Create a TreeStore that mirrors the LabelTree.  The first
        # column is the label, and the second is the LabelTree node.
        self.treestore = gtk.TreeStore(gobject.TYPE_STRING,
                                       gobject.TYPE_PYOBJECT)
        self.gtk = gtk.TreeView(model=self.treestore)
        gtklogger.setWidgetName(self.gtk, name)
        self.gtk.set_property("headers-visible", False)
        tvcol = gtk.TreeViewColumn()
        self.gtk.append_column(tvcol)
        cell = gtk.CellRendererText()
        tvcol.pack_start(cell, expand=False)
        tvcol.set_attributes(cell, text=0) # display column 0 of the tree store
        
        selection = self.gtk.get_selection()
        gtklogger.adoptGObject(selection, self.gtk,
                              access_method=self.gtk.get_selection)
        self.selection_signal = gtklogger.connect(selection, 'changed',
                                                 self.selectionChangedCB)
        selection.set_select_function(self.selectFn)
        gtklogger.connect(self.gtk, 'row-activated', self.activateRowCB)
        gtklogger.connect_passive(self.gtk, 'row-expanded')
        gtklogger.connect_passive(self.gtk, 'row-collapsed')
        self.lt2treeiter = {}

        self.current_selection = None   # a LabelTreeNode

        for node in tree.nodes:
            self.constructGUI(node, None)

        self.gtk.connect("destroy", self.destroyCB)
        self.autoSelect()
        self.gtk.show_all()

        self.sbcallbacks = [
            switchboard.requestCallbackMain((tree, "insert"), self.insertCB),
            switchboard.requestCallbackMain((tree, "delete"), self.deleteCB),
            switchboard.requestCallbackMain((tree, "rename"), self.renameCB)
            ]

    def setRightClickCB(self, callback, *args, **kwargs):
        debug.mainthreadTest()
        self.rccb = callback
        self.rccbargs = args
        self.rccbkwargs = kwargs
        gtklogger.connect_after(self.gtk, "button-release-event",
                               self.buttonEventCB)

    def buttonEventCB(self, gtktree, event):
        if self.rccb:
            if event.button == 3:
                self.rccb(*self.rccbargs, **self.rccbkwargs)
                return True
        return False

    def blockSignals(self):
        debug.mainthreadTest()
        self.selection_signal.block()
    def unblockSignals(self):
        debug.mainthreadTest()
        self.selection_signal.unblock()

    def constructGUI(self, labeltreenode, gtktreeparent):
        debug.mainthreadTest()
        if labeltreenode.secret():
            return
        iter = self.treestore.append(gtktreeparent,
                              [labeltreenode.name, labeltreenode])
        self.lt2treeiter[labeltreenode] = iter
        if labeltreenode.nodes:
            for node in labeltreenode.nodes:
                self.constructGUI(node, iter)

    def selectionChangedCB(self, selection):
        debug.mainthreadTest()
        model, iter = selection.get_selected()
        if iter is None:                # nothing selected
            if self.callback and self.current_selection is not None:
                self.callback("deselect", self.current_selection,
                              *self.callbackargs, **self.callbackkwargs)
            self.current_selection = None
        else:
            ltnode = model[iter][1]
            if self.callback:
                if self.current_selection is not None:
                    self.callback("deselect", self.current_selection,
                                  *self.callbackargs, **self.callbackkwargs)
                self.callback("select", ltnode,
                              *self.callbackargs, **self.callbackkwargs)
            self.current_selection = ltnode

    def activateRowCB(self, treeview, path, col):
        debug.mainthreadTest()
        modelrow = self.treestore[path]       # TreeModelRow object
        ltnode = modelrow[1]
        if ltnode.object is not None:
            self.callback("doubleclick", ltnode,
                          *self.callbackargs, **self.callbackkwargs)
                
    def selectFn(self, path):
        # gtk callback called *before* a selection is made.  It
        # returns True if the node is selectable.  A node is
        # selectable if the LabelTreeNode stores an object.
        row = self.treestore[path]
        ltnode = row[1]
        return ltnode.object is not None

    # Programmatically select an object stored in the tree, without
    # calling the callback function.
    def selectObject(self, object):
        node = self.tree.reverse_dict[object]
        self.selectNode(node)

    # Programmatically select a LabelTree node, without calling the
    # callback function.
    def selectNode(self, node):
        debug.mainthreadTest()
        self.blockSignals()
        iter = self.lt2treeiter[node]
        self.gtk.get_selection().select_iter(iter)
        self.unblockSignals()
        self.current_selection = node
        
    def deselect(self):
        # Check self.tree to suppress deselect signals caused by
        # widget destruction.
        debug.mainthreadTest()
        if self.tree:
            self.blockSignals()
            selection = self.gtk.get_selection()
            selection.unselect_all()
            self.unblockSignals()
            self.current_selection = None
        
    def getSelection(self):
        debug.mainthreadTest()
        selection = self.gtk.get_selection()
        model, iter = selection.get_selected()
        if iter is not None:
            return self.treestore[iter][1]

    # Ensure that the given labeltree node is visible, by expanding
    # each node along the path.
    def expandToPath(self, path):
        debug.mainthreadTest()
        node = self.tree[path]
        iter = self.lt2treeiter[node]
        gtktreepath = self.treestore.get_path(iter)
        self.gtk.expand_to_path(gtktreepath)
        self.gtk.scroll_to_cell(gtktreepath)

    def autoSelect(self):
        debug.mainthreadTest()
        if self.getSelection() is None:
            # If the tree has only a single leaf, select it.
            leafpaths = self.tree.leafpaths()
            if len(leafpaths) == 1:
                node = self.tree[leafpaths[0]]
                self.selectNode(node)

    def destroyCB(self, *args):         # gtk callback
        debug.mainthreadTest()
        map(switchboard.removeCallback, self.sbcallbacks)
        # clean up possible circular references
        self.tree = None                
        del self.treestore
        del self.lt2treeiter
        del self.callback
        del self.callbackargs
        del self.callbackkwargs

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

    # Switchboard callbacks for insertion and deletion.  This allows
    # the GUI to remain synchronized to the dynamic state of the
    # underlying tree.

    def insertCB(self, parent, node):
        debug.mainthreadTest()
        # parent and node are LabelTreeNode objects
        # Currently ignores the fact that these lists are nominally ordered.

        # When inserting at the top level of the labeltree, parent
        # won't be in the lt2treeiter dictionary.  In that case, we
        # want gtkparent to be None, so we use lt2treeiter.get() instead
        # of lt2treeiter[] here.
        gtkparent = self.lt2treeiter.get(parent)
        self.constructGUI(node, gtkparent)
        self.autoSelect()

    def deleteCB(self, node):
        # node is a LabelTreeNode object
        debug.mainthreadTest()
        iter = self.lt2treeiter[node]
        self.treestore.remove(iter)
        del self.lt2treeiter[node]
        self.autoSelect()

    def renameCB(self, node):
        debug.mainthreadTest()
        # node is a LabelTreeNode object
        iter = self.lt2treeiter[node]
        row = self.treestore[iter]
        row[0] = node.name

######################################

# LabelTree representation as a pile of ChooserWidget objects.  Does
# not (yet) update itself when the tree changes.

class LabelTreeChooserWidget:
    def __init__(self, tree, value=None, callback=None, scope=None,
                 condition=None, sort=None, name=None):
        debug.mainthreadTest()
        self.callback = callback
        self.tree = tree
        self.condition = condition
        self.sort = sort
        self.name = name

        if scope:
            scope.addWidget(self)

        self.gtk = gtk.VBox()
        self.widgets = []
        if value is not None:
            self.set_value(value)
        else:
            self.set_value(tree.numberOneChild())
    def show(self):
        debug.mainthreadTest()
        self.gtk.show_all()

    def set_value(self, object):
        debug.mainthreadTest()
        path = labeltree.makePath(self.tree.objpath(object))
        depth = len(path)
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []
        tree = self.tree
        depth = 0
        for name in path:
            names = [node.name for node in tree.nodes]
            widget = chooser.ChooserWidget(names, callback=self.chooserCB,
                                           callbackargs=(depth,),
                                           name="%s_%d"%(self.name,depth))
            depth += 1
            widget.set_state(name)
            self.widgets.append(widget)
            self.gtk.pack_start(widget.gtk, expand=0, fill=0)
            tree = tree[name]
        self.gtk.show_all()
    def chooserCB(self, gtkobj, name, depth):
        leadpath = [self.widgets[d].get_value() for d in range(depth)]
        subtree = self.tree[leadpath+[name]]
        self.set_value(subtree.numberOneChild())
        if self.callback:
            self.callback()

    def get_value(self):
        path = [widget.get_value() for widget in self.widgets]
        if path:
            return self.tree[path].object
        
        

