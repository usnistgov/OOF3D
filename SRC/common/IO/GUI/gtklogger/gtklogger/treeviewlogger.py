# -*- python -*-
# $RCSfile: treeviewlogger.py,v $
# $Revision: 1.3.12.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:16 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import gtk
import adopteelogger
import loggers
import widgetlogger

class TreeViewLogger(widgetlogger.WidgetLogger): # I'm a lumberjack and I'm OK.
    classes = (gtk.TreeView,)
    def record(self, obj, signal, *args):
        if signal == 'button-release-event':
            event = args[0]
            wvar = loggers.localvar('widget')
            return [
    "%s=%s" % (wvar, self.location(obj, *args)),
    "%(w)s.event(event(gtk.gdk.BUTTON_RELEASE,button=%(b)d,window=%(w)s.window))"
    % dict(w=wvar, b=event.button)
    ]
        if signal == 'row-activated':
            path = args[0]
            col = args[1]               # gtk.TreeViewColumn obj
            cols = obj.get_columns()
            for i in range(len(cols)):
                # TODO OPT is there a better way to find the column number?
                if cols[i] is col:
                    return ["tree=%s" % self.location(obj, *args),
                            "column = tree.get_column(%d)" % i,
                            "tree.row_activated(%s, column)" % `path`]
        if signal == 'row-expanded':
            path = args[1]
            return ["%s.expand_row(%s, open_all=False)"
                    % (self.location(obj, *args), `path`)]
        if signal == 'row-collapsed':
            path = args[1]
            return ["%s.collapse_row(%s)"
                    % (self.location(obj,*args), `path`)]
        return super(TreeViewLogger, self).record(obj, signal, *args)

class TreeViewColumnLogger(adopteelogger.AdopteeLogger):
    classes = (gtk.TreeViewColumn,)

class TreeSelectionLogger(adopteelogger.AdopteeLogger):
    classes = (gtk.TreeSelection,)
    def record(self, obj, signal, *args):
        if signal == 'changed':
            if obj.get_mode()==gtk.SELECTION_MULTIPLE:
                model, rows = obj.get_selected_rows()
                # Unselecting all rows and then selecting the selected
                # ones seems wrong, since unselecting and reselecting
                # might have side effects.  It would be much better
                # just to select or unselect the changed rows, but I
                # don't see how to do that simply.
                return ["%s.unselect_all()" % self.location(obj, *args)] + \
                       ["%s.select_path(%s)" % (self.location(obj,*args),row)
                        for row in rows]
            else:                       # single selection only
                model, iter = obj.get_selected()
                if iter is not None:
                    path = model.get_path(iter)
                    return ["%s.select_path(%s)" 
                            % (self.location(obj, *args), path)]
                else:
                    return ["%s.unselect_all()" % self.location(obj, *args)]
        return super(TreeSelectionLogger, self).record(obj, signal, *args)

class ListStoreLogger(adopteelogger.AdopteeLogger):
    classes = (gtk.ListStore,)
    insertrow = None                      # destination for row drag'n'drop
    def record(self, obj, signal, *args):
        # Drag-and-drop of a line within a ListStore creates a pair of
        # row-inserted and row-deleted signals, with row-inserted
        # coming first.  The two must be logged together, so we don't
        # actually return a non-trivial result until getting the
        # second signal.  If the user has two mice and drags rows of
        # two ListStores simultaneously, this won't work.
        if signal == "row-inserted":
            ListStoreLogger.insertrow = args[0][0] # args[0] is a gtk tree path
            return self.ignore
        if signal == "row-deleted":
            if ListStoreLogger.insertrow is None:
                return self.ignore
            deleterow = args[0][0]      # args[0] is a gtk tree path
            destrow = ListStoreLogger.insertrow # destination row
            # The row to be deleted contains the data that has to be
            # inserted in the new row. "deleterow" was set after the
            # new row was inserted (because 'row-deleted' was sent
            # after 'row-inserted'), so if the new row comes before
            # the deleted row in the list, then on replay, where
            # nothing has happened yet, the row to be deleted has a
            # different index than the source row.
            if ListStoreLogger.insertrow < deleterow:
                sourcerow = deleterow - 1
            else:
                sourcerow = deleterow
            ListStoreLogger.insertrow = None
            lvar = loggers.localvar('ls')
            dvar = loggers.localvar('data')
            return [
"%s = %s" % (lvar, self.location(obj, *args)),
"%(data)s = [%(ls)s.get_value(%(ls)s.get_iter((%(r)d,)),i) for i in range(%(ls)s.get_n_columns())]" % dict(r=sourcerow, data=dvar, ls=lvar),
"%s.insert(%d, %s)" % (lvar, destrow, dvar),
"%(ls)s.remove(%(ls)s.get_iter((%(r)d,)))" % dict(r=deleterow, ls=lvar)
                ]

        return super(ListStoreLogger, self).record(obj, signal, *args)

class CellRendererLogger(adopteelogger.AdopteeLogger):
    classes = (gtk.CellRenderer,)
    def record(self, obj, signal, *args):
        if signal == 'toggled':
            path = args[0]
            return ["%s.emit('toggled', %s)"
                    % (self.location(obj, *args), `path`)]
        return super(CellRendererLogger, self).record(obj, signal, *args)

