# -*- python -*-
# $RCSfile: chooser.py,v $
# $Revision: 1.81.2.7 $
# $Author: langer $
# $Date: 2014/09/15 15:08:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import guitop
from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import tooltips
import gobject
import gtk
import types

# The ChooserWidget creates a pull-down menu containing the given list
# of names.  The currently selected name is shown when the menu isn't
# being pulled down.

# Calls the callback, if specified, with the gtk-selecting object
# and the name.  Backward compatible with other callbacks that way.
# Also has an "update_callback" which gets called, with the new
# current selection, when the list of things is updated, with one
# exception -- it is *not* called at __init__-time.

# The ChooserListWidgets in this file have both a list of names that
# they display, and an optional list of objects corresponding to those
# names.  When asked for their 'value', they return the object, not
# the name.  For historical reasons, the ChooserWidget does not do
# this, although it could be made to do so easily.

class ChooserWidget:
    def __init__(self, namelist, callback=None, callbackargs=(),
                 update_callback=None, update_callback_args=(), helpdict={},
                 name=None, separator_func=None):
        debug.mainthreadTest()
        assert name is not None
        
        # If this is used as a base class for another widget, self.gtk
        # will be redefined.  So if a ChooserWidget function needs to
        # refer to the ComboBox gtk widget, it must use
        # self.combobox instead of self.gtk.
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        self.combobox = gtk.ComboBox(liststore)
        if name:
            gtklogger.setWidgetName(self.combobox, name)
        cell = gtk.CellRendererText()
        self.combobox.pack_start(cell, True)
        self.combobox.set_cell_data_func(cell, self.cell_layout_data_func)
        # If separator_func is provided, it must be a function that
        # takes a gtk.TreeModel and gtk.TreeIter as arguments, and
        # return True if the row given by model[iter] is to be
        # represented by a separator in the TreeView.
        if separator_func:
            self.combobox.set_row_separator_func(separator_func)
        self.gtk = self.combobox
        self.current_string = None
        self.callback = callback
        self.callbackargs = callbackargs
        self.helpdict = {}
        self.tipmap = {}                # see cell_layout_data_func()
        self.signal = gtklogger.connect(self.combobox, 'changed',
                                       self.changedCB)
        # make sure that the update_callback isn't installed until
        # after the widget is initialized.
        self.update_callback = None
        self.update_callback_args = ()
        self.update(namelist, helpdict)
        self.update_callback = update_callback
        self.update_callback_args = update_callback_args

    def cell_layout_data_func(self, cell_view, cell_renderer, model, iter):
        # This adds tooltips to the menu items.  It's a bit of a hack
        # and doesn't do a great job: the tips flicker if the mouse is
        # moved.  Thanks to Phil Dumont on the pygtk mailing list for
        # this code.  If you figure out how to get rid of the flicker,
        # please tell Phil.

        debug.mainthreadTest()
        idx = model.get_path(iter)[0]
        item_text = model.get_value(iter, 0)
        cell_renderer.set_property('text', item_text)
        try:
            tip_text = self.helpdict[item_text]
        except KeyError:
            pass
        else:
            # When navigating using the arrow keys, cell_view is
            # sometimes a TreeViewColumn instead of a CellView.
            # TreeViewColumns aren't widgets and don't have
            # get_parent(), so we just ignore them.
            try:
                cv_parent = cell_view.get_parent()
            except AttributeError:
                pass
            else:
                if isinstance(cv_parent, gtk.MenuItem) \
                       and (cv_parent not in self.tipmap or
                            self.tipmap[cv_parent] != tip_text):
                    self.tipmap[cv_parent] = tip_text
                    tooltips.set_tooltip_text(cv_parent,tip_text)

    def show(self):
        debug.mainthreadTest()
        self.gtk.show_all()

    def hide(self):
        debug.mainthreadTest()
        self.gtk.hide()

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

    def suppress_signals(self):
        debug.mainthreadTest()
        self.signal.block()
    def allow_signals(self):
        debug.mainthreadTest()
        self.signal.unblock()

    def changedCB(self, combobox):
        debug.mainthreadTest()
        model = combobox.get_model()
        index = combobox.get_active()
        self.current_string = model[index][0]
        self.set_tooltip()
        if self.callback:
            self.callback(* (combobox, self.current_string)+self.callbackargs)

    def update(self, namelist, helpdict={}):
        debug.mainthreadTest()
        # Replace the widget's list of names with the given list.  The
        # original value of self.current_string will be restored if it
        # still exists in the updated namelist.
        try:
            current_index = namelist.index(self.current_string)
        except ValueError:
            if len(namelist) > 0:
                current_index = 0
            else:
                current_index = -1      # no selection
        self.helpdict = helpdict
        self.suppress_signals()
        liststore = self.combobox.get_model()
        liststore.clear()
        for name in namelist:
            liststore.append([name])
        self.combobox.set_active(current_index)
        if current_index >= 0:
            self.current_string = liststore[current_index][0]
        else:
            self.current_string = None
        self.allow_signals()
        self.set_tooltip()
        if self.update_callback:
            self.update_callback(*(self.gtk, self.current_string)+
                                 self.update_callback_args)
        self.combobox.set_sensitive(len(namelist) > 0)

        # Make the widget wide enough to fit the longest name it
        # might display, plus some extra space for the arrow
        # decoration.
        if namelist:
            maxlen = max([len(name) for name in namelist])
            self.combobox.set_size_request(30+maxlen*guitop.top().charsize, -1)
                                  
    def set_tooltip(self):
        debug.mainthreadTest()
        tooltips.set_tooltip_text(self.combobox,
            self.helpdict.get(self.current_string, None))

    def set_state(self, arg):
        debug.mainthreadTest()
        self.suppress_signals()
        model = self.combobox.get_model()
        if type(arg) == types.IntType:
            self.combobox.set_active(arg)
            self.current_string = model[arg][0]
        elif type(arg) == types.StringType:
            names = [row[0] for row in model]
            try:
                index = names.index(arg)
            except ValueError:
                self.combobox.set_active(0)
                self.current_string = names[0]
            else:
                self.combobox.set_active(index)
                self.current_string = arg
        self.allow_signals()
        self.set_tooltip()
        if self.update_callback:
            self.update_callback(*(self.gtk, self.current_string)+
                                 self.update_callback_args)
           
    def get_value(self):
        return self.current_string
    def nChoices(self):
        return len(self.combobox.get_model())
    def choices(self):
        model = self.combobox.get_model()
        return [x[0] for x in iter(model)]

class FakeChooserWidget:
    # For debugging only.
    def __init__(self, namelist, callback=None, callbackargs=(),
                 update_callback=None, update_callback_args=(), helpdict={}):
        debug.mainthreadTest()
        self.gtk = gtk.Label("Gen-u-wine Fake Widget")
        debug.fmsg(namelist)
    def show(self):
        pass
    def destroy(self):
        pass
    def setsize(self, namelist):
        pass
    def update(self, namelist, helpdict={}):
        debug.fmsg(namelist)
    def set_state(self, arg):
        pass
    def get_value(self):
        pass
    def nChoices(self):
        pass

## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ##

# The NewChooserWidget has a pulldown menu and a button.  The default
# text on the button is "New...".  The intent is that the callback for
# the button will create a new object to be listed in the pulldown
# menu. The button callback is responsible for updating the menu (with
# ChooserWidget.update) and selecting the new entry (with
# ChooserWidget.set_state).

class NewChooserWidget(ChooserWidget):
    def __init__(self, namelist, callback=None, callbackargs=(),
                 update_callback=None, update_callback_args=(),
                 button_callback=None, button_callback_args=(),
                 buttontext="New...",
                 separator_func=None):
        ChooserWidget.__init__(self, namelist,
                               callback=callback, callbackargs=callbackargs,
                               update_callback=update_callback,
                               update_callback_args=update_callback_args,
                               helpdict={}, separator_func=separator_func)

        self.button_callback = button_callback
        self.button_callback_args = button_callback_args
        
        # Wrap the ChooserWidget's gtk in a GtkHBox and make it become self.gtk
        hbox = gtk.HBox()
        hbox.pack_start(self.gtk, expand=1, fill=1, padding=2)
        self.gtk = hbox

        self.newbutton = gtk.Button(buttontext)
        hbox.pack_start(self.newbutton, expand=0, fill=0, padding=2)
        gtklogger.connect(self.newbutton, 'clicked', self.newbuttonCB)
    def newbuttonCB(self, button):
        if self.button_callback:
            self.button_callback(*self.button_callback_args)
    def set_button_sensitivity(self, sensitivity):
        debug.mainthreadTest()
        self.newbutton.set_sensitive(sensitivity)
            

## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ##    

# Like a ChooserWidget, but makes a list instead of a pull-down menu.
# Locally stateful.  Callback gets called when selection state
# changes, with the newly-selected string or "None".  Takes both a
# list of objects, and a list of display strings for those objects.
# If comparison of two objects is nontrivial and not implemented by
# the objects' __eq__ function, the 'comparator' arg should be
# provided.  It should be a function of two objects that returns 1 if
# they are equal.

# 'callback' is called when an item is selected in the list.
# 'dbcallback' is called when an item is double-clicked, or 'return'
# is pressed when an item is selected and the list has focus.

## TODO 3.1: Use helpdict to put tooltips on the list items.  This
## probably isn't important.  Most, maybe all, ChooserListWidgets
## display user-created objects, and don't have helpdicts.

class ChooserListWidgetBase:
    def __init__(self, objlist=None, displaylist=[], callback=None,
                 dbcallback=None, autoselect=True, helpdict={},
                 comparator=None, markup=False,
                 name=None, separator_func=None,
                 cbargs=None, cbkwargs=None):
        debug.mainthreadTest()
        self.liststore = gtk.ListStore(gobject.TYPE_STRING,
                                       gobject.TYPE_PYOBJECT)
        self.treeview = gtk.TreeView(self.liststore)
        self.gtk = self.treeview
        self.treeview.set_property("headers-visible", 0)
        cell = gtk.CellRendererText()
        if markup:
            # Expect to find pango markup in displaylist, which is
            # stored in column 0 of the ListStore.
            self.tvcol = gtk.TreeViewColumn("", cell, markup=0)
        else:
            self.tvcol = gtk.TreeViewColumn("", cell)
        self.treeview.append_column(self.tvcol)
        self.tvcol.add_attribute(cell, 'text', 0)
        self.autoselect = autoselect
        self.callback = callback or (lambda x, interactive=False: None)
        self.dbcallback = dbcallback or (lambda x: None)
        self.cbargs = cbargs or []
        self.cbkwargs = cbkwargs or {}
        self.comparator = comparator or (lambda x, y: x == y)
        self.activatesignal = gtklogger.connect(self.treeview, 'row-activated',
                                               self.rowactivatedCB)

        # If separator_func is provided, it must be a function that
        # takes a gtk.TreeModel and gtk.TreeIter as arguments, and
        # return True if the row given by model[iter] is to be
        # represented by a separator in the TreeView.
        if separator_func:
            self.treeview.set_row_separator_func(separator_func)

        if name:
            gtklogger.setWidgetName(self.treeview, name)
        selection = self.treeview.get_selection()
        gtklogger.adoptGObject(selection, self.treeview,
                              access_method=self.treeview.get_selection)
        self.selectsignal = gtklogger.connect(selection, 'changed',
                                             self.selectionchangedCB)
        self.update(objlist or [], displaylist, helpdict=helpdict)

    def grab_focus(self):
        self.treeview.grab_focus()

    def suppress_signals(self):
        debug.mainthreadTest()
        self.activatesignal.block()
        self.selectsignal.block()
    def allow_signals(self):
        debug.mainthreadTest()
        self.activatesignal.unblock()
        self.selectsignal.unblock()

    def find_obj_index(self, obj):
        debug.mainthreadTest()
        if obj is not None:
            objlist = [r[1] for r in self.liststore]
            for which in range(len(objlist)):
                if self.comparator(obj, objlist[which]):
                    return which
        raise ValueError

    def rowactivatedCB(self, treeview, path, col):
        self.dbcallback(self.get_value(), *self.cbargs, **self.cbkwargs)
    def selectionchangedCB(self, treeselection):
        self.callback(self.get_value(), interactive=True, *self.cbargs, 
                      **self.cbkwargs)

    def show(self):
        debug.mainthreadTest()
        self.gtk.show_all()
    def hide(self):
        debug.mainthreadTest()
        self.gtk.hide()
    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

    def scroll_to_line(self, lineno):
        self.treeview.scroll_to_cell(lineno)


class ChooserListWidget(ChooserListWidgetBase):
    # Get the index of the current selection.
    def get_index(self):
        debug.mainthreadTest()
        treeselection = self.treeview.get_selection() # gtk.TreeSelection obj
        (model, iter) = treeselection.get_selected() #gtk.ListStore,gtk.TreeIter
        if iter is not None:
            return model.get_path(iter)[0]  # integer!
    def has_selection(self):
        debug.mainthreadTest()
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        return iter is not None
    def get_value(self):
        debug.mainthreadTest()
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter is not None:
            return model[iter][1]
    def set_selection(self, obj):
        debug.mainthreadTest()
        self.suppress_signals()
        treeselection = self.treeview.get_selection()
        try:
            which = self.find_obj_index(obj)
        except ValueError:
            treeselection.unselect_all()
        else:
            treeselection.select_path(which)
            self.treeview.scroll_to_cell(which)
        self.allow_signals()

        
    # Replace the contents, preserving the selection state, if
    # possible.
    def update(self, objlist, displaylist=[], helpdict={}):
        debug.mainthreadTest()
        self.suppress_signals()
        old_obj = self.get_value()
        self.liststore.clear()
        for obj, dispname in map(None, objlist, displaylist):
            if dispname is not None:
                self.liststore.append([dispname, obj])
            else:
                self.liststore.append([obj, obj])
        try:
            index = self.find_obj_index(old_obj)
        except ValueError:
            if self.autoselect and len(objlist) == 1:
                # select the only object in the list
                treeselection = self.treeview.get_selection()
                treeselection.select_path(0)
            # New value differs from old value, so callback must be invoked.
            self.callback(self.get_value(), interactive=False,
                          *self.cbargs, **self.cbkwargs)
        else:                           # reselect current_obj
            treeselection = self.treeview.get_selection()
            treeselection.select_path(index)
        self.allow_signals()

# List widget that allows multiple selections

class MultiListWidget(ChooserListWidgetBase):
    def __init__(self, objlist, displaylist=[], callback=None,
                 dbcallback=None, autoselect=True, helpdict={},
                 comparator=None, name=None, separator_func=None,
                 markup=False, cbargs=None, cbkwargs=None):
        ChooserListWidgetBase.__init__(self, objlist, displaylist, callback,
                                       dbcallback, autoselect, helpdict,
                                       comparator=comparator, name=name,
                                       separator_func=separator_func,
                                       markup=markup,
                                       cbargs=cbargs, cbkwargs=cbkwargs)
        selection = self.treeview.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
    def get_value(self):
        debug.mainthreadTest()
        selection = self.treeview.get_selection()
        model, rows = selection.get_selected_rows()
        return [model[r][1] for r in rows]
    def has_selection(self):
        debug.mainthreadTest()
        selection = self.treeview.get_selection()
        model, rows = selection.get_selected_rows()
        return len(rows) > 0
    def update(self, objlist, displaylist=[], helpdict={}):
        debug.mainthreadTest()
        self.suppress_signals()
        old_objs = self.get_value()
        self.liststore.clear()
        for obj, dispname in map(None, objlist, displaylist):
            if dispname is not None:
                self.liststore.append([dispname, obj])
            else:
                self.liststore.append([obj, obj])
        treeselection = self.treeview.get_selection()
        for obj in old_objs:
            try:
                index = self.find_obj_index(obj)
            except ValueError:
                pass
            else:
                treeselection.select_path(index)
                
        self.allow_signals()
    def set_selection(self, selectedobjs):
        # does not unselect anything, or emit signals
        debug.mainthreadTest()
        self.suppress_signals()
        objlist = [r[1] for r in self.liststore]
        treeselection = self.treeview.get_selection()
        if selectedobjs:
            for obj in selectedobjs:
                try:
                    index = self.find_obj_index(obj)
                except ValueError:
                    pass
                else:
                    treeselection.select_path(index)
        self.allow_signals()
        self.callback(self.get_value(), interactive=False)

    def clear(self):
        debug.mainthreadTest()
        self.suppress_signals()
        selection = self.treeview.get_selection()
        selection.unselect_all()
        self.allow_signals()

##################################################

class ChooserComboWidget:
    def __init__(self, namelist, callback=None, name=None):
        # If a callback is provided, it's called a *lot* of times.
        # It's called for every keystroke in the entry part of the
        # widget and every time a selection is made in the list part
        # of the widget.
        debug.mainthreadTest()
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        self.combobox = gtk.ComboBoxEntry(liststore, 0)
        if name:
            gtklogger.setWidgetName(self.combobox, name)
        self.gtk = self.combobox
        self.namelist = []
        self.current_string = None
        self.update(namelist)
        self.signal = gtklogger.connect(self.combobox, 'changed',
                                        self.changedCB)
        self.callback = callback

    def show(self):
        debug.mainthreadTest()
        self.gtk.show_all()

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

    def suppress_signals(self):
        self.signal.block()
    def allow_signals(self):
        self.signal.unblock()

    def update(self, namelist):
        debug.mainthreadTest()
        current_string = self.combobox.child.get_text()
        try:
            current_index = namelist.index(current_string)
        except ValueError:
            if len(namelist) > 0:
                current_index = 0
            else:
                current_index = -1
        liststore = self.combobox.get_model()
        liststore.clear()
        for name in namelist:
            liststore.append([name])
        self.combobox.set_active(current_index)

    def changedCB(self, combobox):
        self.callback(self)

    def get_value(self):
        debug.mainthreadTest()
        val = self.combobox.child.get_text()
        return val

    def set_state(self, arg):
        debug.mainthreadTest()
        if type(arg) == types.IntType:
            liststore = self.combobox.get_model()
            self.combobox.child.set_text(liststore[arg][0])
        elif type(arg) == types.StringType:
            self.combobox.child.set_text(arg)
        self.combobox.child.set_position(-1)


        
## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ##
## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ##

# Variants of the above widgets...

class FramedChooserListWidget(ChooserListWidget):
    def __init__(self, objlist=None, displaylist=[],
                 callback=None, dbcallback=None, autoselect=True,
                 comparator=None, name=None, cbargs=None, cbkwargs=None):
        ChooserListWidget.__init__(self,
                                   objlist=objlist,
                                   displaylist=displaylist,
                                   callback=callback,
                                   dbcallback=dbcallback,
                                   autoselect=autoselect,
                                   comparator=comparator,
                                   name=name,
                                   cbargs=cbargs, cbkwargs=cbkwargs)
        self.gtk = gtk.Frame()
        self.gtk.set_shadow_type(gtk.SHADOW_IN)
        self.gtk.add(self.treeview)

class ScrolledChooserListWidget(ChooserListWidget):
    def __init__(self, objlist=None, displaylist=[], callback=None,
                 dbcallback=None, autoselect=True, comparator=None, name=None,
                 separator_func=None, markup=False, cbargs=None, cbkwargs=None):
        ChooserListWidget.__init__(self,
                                   objlist=objlist,
                                   displaylist=displaylist,
                                   callback=callback,
                                   dbcallback=dbcallback,
                                   autoselect=autoselect,
                                   comparator=comparator,
                                   name=name,
                                   separator_func=separator_func,
                                   markup=markup,
                                   cbargs=cbargs, cbkwargs=cbkwargs)
        self.gtk = gtk.ScrolledWindow()
        gtklogger.logScrollBars(self.gtk, name=name+"Scroll")
        self.gtk.set_shadow_type(gtk.SHADOW_IN)
        self.gtk.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.gtk.add(self.treeview)


class ScrolledMultiListWidget(MultiListWidget):
    def __init__(self, objlist=None, displaylist=[],
                 callback=None, dbcallback=None,
                 name=None,
                 separator_func=None, markup=False,
                 cbargs=None, cbkwargs=None):
        MultiListWidget.__init__(self, objlist, displaylist,
                                 callback, dbcallback=dbcallback,
                                 name=name, separator_func=separator_func,
                                 markup=markup,
                                 cbargs=cbargs, cbkwargs=cbkwargs)
        mlist = self.gtk
        self.gtk = gtk.ScrolledWindow()
        self.gtk.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.gtk.add(mlist)
        
## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ##
## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ##
        
## NOT USED?

# class ChooserDialog:
#     OK = 1
#     CANCEL = 2
#     def __init__(self, prompt, names, helpdict={}, parentwindow=None):
#         debug.mainthreadTest()
#         parent = parentwindow or guitop.top().gtk
#         self.dialog = gtklogger.Dialog(title='OOF2: ' + prompt,
#                                        parent=parent,
#                                        flags=gtk.DIALOG_MODAL)
#         self.chooserwidget = ChooserWidget(names, helpdict=helpdict)
#         hbox = gtk.HBox()
#         self.dialog.vbox.pack_start(hbox, expand=1, fill=1, padding=5)
#         hbox.pack_start(gtk.Label(prompt), expand=0, padding=5)
#         hbox.pack_start(self.chooserwidget.gtk, expand=1, padding=5)
#         self.dialog.add_button("OK", self.OK)
#         self.dialog.add_button("Cancel", self.CANCEL)
#         hbox.show_all()
#     def run(self):
#         debug.mainthreadTest()
#         return self.dialog.run()
#     def close(self):
#         debug.mainthreadTest()
#         self.dialog.destroy()
#     def get_value(self):
#         return self.chooserwidget.get_value()

# def chooser(prompt, names, helpdict={}, parentwindow=None):
#     if names:
#         dialog = ChooserDialog(prompt, names)
#         result = dialog.run()
#         dialog.close()
#         if result in (ChooserDialog.CANCEL, gtk.RESPONSE_DELETE_EVENT):
#             return None
#         return dialog.get_value()
#     else:
#         raise "No names!"

