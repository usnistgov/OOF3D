# -*- python -*-
# $RCSfile: gfxprof2.py,v $
# $Revision: 1.5.54.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import pygtk
pygtk.require("2.0")
import gtk
import gobject

import displayprof
import sys, getopt, os

class ListEntry:
    def __init__(self, title, value, type, format="%s", xalign=1.0):
        self.title = title
        self.value = value              # function of displayprof.Function obj
        self.type = type
        self.xalign = xalign
        self.format = format
    def sorter(self, model, iter1, iter2, userdata):
        v1 = self.value(model[iter1][0])
        v2 = self.value(model[iter2][0])
        if self.type is int:
            return cmp(int(v1), int(v2))
        if self.type is float:
            return cmp(float(v1), float(v2))
        return cmp(v1, v2)
            
def percall(f):
    if f.ncalls > 0:
        return f.owntime/f.ncalls
    return 0.0

def totalpercall(f):
    if f.ncalls > 0:
        return f.totaltime/f.ncalls
    return 0.0

columns = [
    ListEntry('file ', lambda f: f.file, str),
    ListEntry('line ', lambda f: f.lineno, int),
    ListEntry('function', lambda f: f.name, str, xalign=0.0),
    ListEntry('ncalls ', lambda f: f.ncalls, int, format="%d"),
    ListEntry('self ', lambda f: 1000*f.owntime, float, format="%9.3f"),
    ListEntry('percall ', lambda f: 1000*percall(f), float, format="%9.3f"),
    ListEntry('total ', lambda f: 1000*f.totaltime, float, format="%9.3f"),
    ListEntry('total percall ', lambda f: 1000*totalpercall(f), float,
              format="%9.3f")
    ]



class GfxProfWindow:
    def __init__(self):

        self.stats = None               # displayprof.Stats object
        self.filename = None
        
        self.gtk = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.gtk.set_title('GfxProf')
        self.gtk.set_size_request(-1, 300)
        self.gtk.connect("destroy", gtk.main_quit)

        mainbox = gtk.VBox()
        self.gtk.add(mainbox)

        hbox = gtk.HBox()
        mainbox.pack_start(hbox, expand=0, fill=0, padding=5)

        self.infoarea = gtk.Label("")
        hbox.pack_start(self.infoarea, expand=1, fill=1, padding=5)

        loadbutton = gtk.Button('Load')
        loadbutton.connect('clicked', self.loadCB)
        hbox.pack_start(loadbutton, expand=0, fill=0, padding=2)
        self.selector = None

        self.stripbutton = gtk.Button('Strip Dirs')
        self.stripbutton.connect('clicked', self.stripCB)
        hbox.pack_start(self.stripbutton, expand=0, fill=0, padding=2)
        self.stripped = 0
        
        self.callerbutton = gtk.Button('Call View')
        self.callerbutton.connect('clicked', self.callerCB)
        hbox.pack_start(self.callerbutton, expand=0, fill=0, padding=2)
        
        quitbutton = gtk.Button("Quit")
        quitbutton.connect('clicked', gtk.main_quit)
        hbox.pack_start(quitbutton, expand=0, fill=0, padding=2)

        self.funclist = gtk.ListStore(gobject.TYPE_PYOBJECT)
        self.funcview = gtk.TreeView(self.funclist)
        self.funcview.set_search_column(2)
        self.funcview.set_headers_clickable(1)
        self.tvcolumns = [gtk.TreeViewColumn(col.title) for col in columns]
        self.cells = [gtk.CellRendererText() for col in columns]
        for colno in range(len(columns)):
            tvcol = self.tvcolumns[colno]
            cell = self.cells[colno]
            self.funcview.append_column(tvcol)
            tvcol.pack_start(cell, False)
            tvcol.set_cell_data_func(cell, self.render_cell,
                                     columns[colno])
            self.funclist.set_sort_func(colno, columns[colno].sorter, 0)
            tvcol.set_sort_column_id(colno)

        self.funcview.connect('row-activated', self.activateRowCB)

        selection = self.funcview.get_selection()
        selection.connect('changed', self.selChangedCB)
        
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        mainbox.pack_start(scroll, expand=1, fill=1)
        scroll.add(self.funcview)
        self.sensitize()

    def render_cell(self, treeviewcolumn, cell_renderer, model, iter,
                    listitem):
        cell_renderer.set_property(
            'text', listitem.format%listitem.value(model[iter][0]))
        cell_renderer.set_property('xalign', listitem.xalign)

    def sensitize(self):
        self.callerbutton.set_sensitive(self.selectedRow() is not None)
        self.stripbutton.set_sensitive(self.stats is not None
                                       and not self.stripped)

    def loadfile(self, filename):
        try:
            self.stats = displayprof.Stats(filename)
        except UserWarning:
            raiseAlert("Invalid profile file!")
            return
        self.filename = filename
        self.stripped = 0
        self.displaystats()

    def stripdirs(self):
        self.stats.strip_dirs()
        self.stripped = 1
    def stripCB(self, *args):
        self.stripdirs()
        self.displaystats()

    def displaystats(self):
        self.infoarea.set_text("%s: %d functions, %d calls, totaltime = %g ms"
                               % (os.path.basename(self.filename),
                                  len(self.stats.allfuncs),
                                  self.stats.ncalls,
                                  1000*self.stats.totaltime))

        self.funclist.clear()
        for func in self.stats.allfuncs:
            self.funclist.append([func])
        self.sensitize()

    def loadCB(self, *args):
        if not self.selector:
            self.selector = gtk.FileSelection(title='Read Profile file')
            self.selector.ok_button.connect('clicked', self.fileokCB)
            self.selector.cancel_button.connect('clicked', self.filecancelCB)
            self.selector.main_vbox.connect('destroy', self.filecancelCB)
            self.selector.set_modal(1)
            if self.filename:
                self.selector.set_filename(self.filename)
        self.filedone = 0
        self.filecancelled = 0
        self.selector.show()
        while not self.filedone:
            gtk.main_iteration()
        self.selector.hide()
        if not self.filecancelled:
            filename = self.selector.get_filename()
            self.loadfile(filename)

    def filecancelCB(self, *args):
        self.filedone = 1
        self.filecancelled = 1
    def fileokCB(self, *args):
        self.filedone = 1

    def activateRowCB(self, treeview, path, col):
        modelrow = self.funclist[path]  # a TreeModelRow object
        function = modelrow[-1]
        ButterflyWindow(self.stats, function)

    def selChangedCB(self, selection):
        self.sensitize()

    def selectedRow(self):
        selection = self.funcview.get_selection()
        (model, iter) = selection.get_selected()
        if iter is None:
            return                      # no selection
        return model[iter]
        
    def callerCB(self, *args):          # gtk button callback
        modelrow = self.selectedRow()
        if modelrow is not None:
            ButterflyWindow(self.stats, modelrow[-1])

#########################
            
def getLineNo(s):
    fullname = parseFunctionName(s[2])
    lineno = fullname[1]
    if lineno != '':
        return int(fullname[1])
    return 0
    

bfcols = [
    ListEntry('ncalls', lambda s: s[0] , int),
    ListEntry('%time', lambda s: s[1], float),
    ListEntry('file', lambda s: parseFunctionName(s[2])[0], str),
    ListEntry('line', getLineNo, int),
    ListEntry('function', lambda s: parseFunctionName(s[2])[2], str, xalign=0.0)
    ]

class ButterflyWindow:
    def __init__(self, stats, function):
        self.gtk = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.gtk.set_title('Call View')
        self.gtk.set_size_request(500, 300)
        self.history = []               # for "Prev" button
        self.future = []                # for "Next" button
        vpane = gtk.VPaned()
        self.gtk.add(vpane)
        frame = gtk.Frame('Callers')
        vpane.pack1(frame, resize=1, shrink=1)
        scroll = gtk.ScrolledWindow()
        frame.add(scroll)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.callerlist = gtk.ListStore(*[col.type for col in bfcols])
        self.callerview = gtk.TreeView(self.callerlist)
        scroll.add(self.callerview)
        self.callercols = [gtk.TreeViewColumn(col.title) for col in bfcols]
        self.callercells = [gtk.CellRendererText() for col in bfcols]
        for colno in range(len(bfcols)):
            tvcol = self.callercols[colno]
            cell = self.callercells[colno]
            cell.set_property('xalign', bfcols[colno].xalign)
            self.callerview.append_column(tvcol)
            tvcol.pack_start(cell, False)
            tvcol.set_attributes(cell, text=colno)
            tvcol.set_sort_column_id(colno)
        self.callerview.connect('row-activated', self.bfActivateRowCB)

        vbox = gtk.VBox()
        vpane.pack2(vbox, resize=1, shrink=1)

        thorax = gtk.HBox()
        vbox.pack_start(thorax, expand=0, fill=0, padding=5)
        self.thoraxlabel = gtk.Label("")
        self.thoraxlabel.set_alignment(0.0, 0.5)
        thorax.pack_start(self.thoraxlabel, expand=0, fill=0, padding=5)
        
        align = gtk.Alignment(xalign=1.0)
        thorax.pack_start(align, expand=1, fill=1)
        buttons = gtk.HBox()
        align.add(buttons)
        self.prevbutton = gtk.Button()
        self.prevbutton.add(gtk.Arrow(gtk.ARROW_LEFT, gtk.SHADOW_OUT))
        self.prevbutton.connect('clicked', self.prevCB)
        buttons.pack_start(self.prevbutton, expand=0, fill=0,padding=3)
        self.nextbutton = gtk.Button()
        self.nextbutton.add(gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_OUT))
        self.nextbutton.connect('clicked', self.nextCB)
        buttons.pack_start(self.nextbutton, expand=0, fill=0, padding=3)
        
        frame = gtk.Frame('Callees')
        vbox.pack_start(frame, expand=1, fill=1)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        frame.add(scroll)
        self.calleelist = gtk.ListStore(*[col.type for col in bfcols])
        self.calleeview = gtk.TreeView(self.calleelist)
        scroll.add(self.calleeview)
        self.calleecols = [gtk.TreeViewColumn(col.title) for col in bfcols]
        self.calleecells = [gtk.CellRendererText() for col in bfcols]
        for colno in range(len(bfcols)):
            tvcol = self.calleecols[colno]
            cell = self.calleecells[colno]
            cell.set_property('xalign', bfcols[colno].xalign)
            self.calleeview.append_column(tvcol)
            tvcol.pack_start(cell, False)
            tvcol.set_attributes(cell, text=colno)
            tvcol.set_sort_column_id(colno)
        self.calleeview.connect('row-activated', self.bfActivateRowCB)
        self.stats = stats
        self.set_function(function)
        self.gtk.show_all()

    def bfActivateRowCB(self, treeview, path, col):
        model = treeview.get_model()
        modelrow = model[path]
        try:
            file = modelrow[2]
            lineno = int(modelrow[3])
            fname = modelrow[4]
            function = self.stats.get_function(file, lineno, fname)
        except:
            pass
        else:
            if function:
                self.future = []
                self.set_function(function)

    def set_function(self, function):
        self.history.append(function)
        self.thoraxlabel.set_text("%s   totaltime=%f"
                                  % (function.fullname(), function.totaltime))
        sups = function.get_callers(self.stats.functions)
        sups.sort(displayprof.subsort)
        subs = function.get_callees(self.stats.functions)
        subs.sort(displayprof.subsort)
        self.do_subsup(sups, self.callerlist)
        self.do_subsup(subs, self.calleelist)

        self.prevbutton.set_sensitive(len(self.history) > 1)
        self.nextbutton.set_sensitive(len(self.future) > 0)

    def do_subsup(self, slist, liststore):
        liststore.clear()
        for subsup in slist:
            liststore.append([c.value(subsup) for c in bfcols])

    def prevCB(self, button):
        if len(self.history) > 1:
            self.future.append(self.history.pop())
            self.set_function(self.history.pop())
    def nextCB(self, button):
        if len(self.future) > 0:
            self.set_function(self.future.pop())

def raiseAlert(message):
    print message                       # wimp. should open a window.

def parseFunctionName(fullname):
    if fullname[0] == '<' and fullname[-1] == '>':
        return [fullname, '', '']
    # fullname is file:line(function)
    n = fullname.split(':')
    filename = n[0]
    nn = n[1].split('(')               # [line, (function)]
    line = nn[0]
    funcname = nn[1][:-1]
    return [filename, line, funcname]
                
if __name__ == '__main__':
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'df:')
    except getopt.error, message:
        print message
        sys.exit(1)

    filename = None
    stripdirs = 1
    for opt in optlist:
        if opt[0] == '-f':
            filename = opt[1]
        if opt[0] == '-d':
            stripdirs = 0

    gui = GfxProfWindow()

    if filename:
        gui.loadfile(filename)
        if stripdirs:
            gui.stripdirs()
        gui.displaystats()
    gui.gtk.show_all()
    gtk.main()
