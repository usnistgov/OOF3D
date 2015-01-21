# -*- python -*-
# $RCSfile: gfxprof.py,v $
# $Revision: 1.7.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

try:
    import pygtk
except ImportError:
    # Import error probably means you have a pre-2.0 pygtk, which only
    # has gtk.py and not pygtk.py -- pass, and allow subsequent gtk
    # imports to stand or fall on their own merits.
    pass
else:
    # pygtk has been imported properly.  This means that you have
    # gtk-2.0 installed, so we have to force you to use gtk-1.2
    # instead.
    try:
        pygtk.require("1.2")
    except AssertionError:
        # This is a hack to accomodate systems that have both gtk-1.2
        # and 2.0 installed, but don't have the python wrappers for
        # gtk-1.2 installed in the right place.  The old (pre-2.0) way
        # of doing things was to have gtk.py installed in
        # site-packages.  The new way is to have it installed in
        # site-packages/gtk-1.2.  Some installations (Macintoshes with
        # fink, for example) have gtk-1.2 installed the old way and
        # gtk-2.0 installed the new way, so the pygtk.require call
        # fails.  On these systems, the "import gtk" lines will get
        # the right gtk.py file anyway, so we can safely ignore the
        # error.
        pass

from gtk import *
import displayprof
import sys, getopt, os

class ListEntry:
    def __init__(self, title, value, repr):
        self.title = title
        self.value = value              # function of displayprof.Function obj
        self.repr = repr                # function of displayprof.Function obj

def percall(f):
    if f.ncalls > 0:
        return f.owntime/f.ncalls
    return 0.0

def totalpercall(f):
    if f.ncalls > 0:
        return f.totaltime/f.ncalls
    return 0.0

columns = [
    ListEntry('file ', lambda f: f.file, lambda f: f.file),
    ListEntry('line ', lambda f: f.lineno, lambda f: `f.lineno`),
    ListEntry(' function', lambda f: f.name, lambda f: f.name),
    ListEntry('ncalls ', lambda f: f.ncalls, lambda f: `f.ncalls`),
    ListEntry('self ', lambda f: f.owntime, lambda f:"%10.4f"%(1000*f.owntime)),
    ListEntry('percall ', lambda f: percall(f),
              lambda f: "%10.4f"%(1000*percall(f))),
    ListEntry('total ', lambda f: f.totaltime,
              lambda f: "%10.4f" % (1000*f.totaltime)),
    ListEntry('total percall ', lambda f: totalpercall(f),
              lambda f: "%10.4f" % (1000*totalpercall(f)))
    ]

class GfxProfWindow:
    def __init__(self):

        self.stats = None               # displayprof.Stats object
        
        self.gtk = GtkWindow(WINDOW_TOPLEVEL)
        self.gtk.set_title('GfxProf')
        self.gtk.set_usize(-1, 300)
        self.gtk.connect("destroy", mainquit)

        mainbox = GtkVBox()
        self.gtk.add(mainbox)

        hbox = GtkHBox()
        mainbox.add(hbox, expand=0, fill=0, padding=5)

        self.infoarea = GtkLabel()
        hbox.add(self.infoarea, expand=1, fill=1, padding=5)

        loadbutton = GtkButton('Load')
        loadbutton.connect('clicked', self.loadCB)
        hbox.add(loadbutton, expand=0, fill=0, padding=2)
        self.selector = None

        self.stripbutton = GtkButton('Strip Dirs')
        self.stripbutton.connect('clicked', self.stripCB)
        hbox.add(self.stripbutton, expand=0, fill=0, padding=2)
        self.stripped = 0
        
        self.callerbutton = GtkButton('Call View')
        self.callerbutton.connect('clicked', self.callerCB)
        hbox.add(self.callerbutton, expand=0, fill=0, padding=2)
        
        quitbutton = GtkButton("Quit")
        quitbutton.connect('clicked', mainquit)
        hbox.add(quitbutton, expand=0, fill=0, padding=2)

        self.funclist = GtkCList(cols=8, titles=[c.title for c in columns])
        self.funclist.column_titles_active()
        self.funclist.column_titles_show()
        self.funclist.connect('click-column', self.funclistheaderCB)
        self.funclist.connect('select-row', self.selectRowCB)
        self.funclist.connect('unselect-row', self.unselectRowCB)
        self.funclist.connect('button_press_event', self.buttonpressCB)
        for c in (0,1,3,4,5,6,7):
            self.funclist.set_column_justification(c, JUSTIFY_RIGHT)
        self.funclist.set_column_justification(2, JUSTIFY_LEFT)
        self.sorttype = -1              # descending
        self.sortcolumn = None
        self.selectedRow = None
        self.doubleclicked = 0

        scroll = GtkScrolledWindow()
        scroll.set_policy(POLICY_AUTOMATIC, POLICY_AUTOMATIC)
        mainbox.add(scroll, expand=1, fill=1)
        scroll.add(self.funclist)
        self.sensitize()

    def sensitize(self):
        self.callerbutton.set_sensitive(self.selectedRow is not None)
        self.stripbutton.set_sensitive(not self.stripped and self.stats is not None)

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
                               % (os.path.basename(filename),
                                  len(self.stats.allfuncs),
                                  self.stats.ncalls,
                                  1000*self.stats.totaltime))

        self.funclist.freeze()
        self.funclist.clear()
        for func in self.stats.allfuncs:
            self.funclist.append([c.repr(func) for c in columns])
        self.funclist.thaw()
        self.funclist.columns_autosize()
        self.selectedRow = None
        self.sensitize()

    def loadCB(self, *args):
        if not self.selector:
            self.selector = GtkFileSelection(title='Read Profile file')
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
            mainiteration()
        self.selector.hide()
        if not self.filecancelled:
            filename = self.selector.get_filename()
            self.loadfile(filename)

    def filecancelCB(self, *args):
        self.filedone = 1
        self.filecancelled = 1
    def fileokCB(self, *args):
        self.filedone = 1
        

    def selectRowCB(self, widget, row, col, gdkevent):
        self.selectedRow = row
        if self.doubleclicked:
            ButterflyWindow(self.stats, self.stats.allfuncs[self.selectedRow])
            self.doubleclicked = 0
        self.sensitize()
    def unselectRowCB(self, widget, row, col, gdkevent):
        self.selectedRow = None
        self.sensitize()
    def buttonpressCB(self, widget, gdkevent):
        if gdkevent.type == GDK._2BUTTON_PRESS:
            self.doubleclicked = 1
        
    def callerCB(self, *args):          # gtk button callback
        if self.selectedRow is not None:
            ButterflyWindow(self.stats, self.stats.allfuncs[self.selectedRow])

    def funclistheaderCB(self, obj, column):
        if column == self.sortcolumn:
            # switch sort type
            self.sorttype *= -1
        else:
            self.sorttype = -1
        self.sortcolumn = column
        self.stats.allfuncs.sort(self.colsorter)
        self.displaystats()
    
    def colsorter(self, a, b):
        func = columns[self.sortcolumn].value
        xa = func(a)
        xb = func(b)
        if xa < xb: return -self.sorttype
        if xa > xb: return self.sorttype
        return 0

butterflytitles = ['ncalls', '%time', 'file', 'line', 'function']

class ButterflyWindow:
    def __init__(self, stats, function):
        self.gtk = GtkWindow(WINDOW_TOPLEVEL)
        self.gtk.set_title('Call View')
        self.gtk.set_usize(500, 300)
        vpane = GtkVPaned()
        self.gtk.add(vpane)
        frame = GtkFrame('Callers')
        vpane.pack1(frame, resize=1, shrink=1)
        scroll = GtkScrolledWindow()
        frame.add(scroll)
        scroll.set_policy(POLICY_AUTOMATIC, POLICY_AUTOMATIC)
        self.callerlist = GtkCList(cols=5, titles=butterflytitles)
        self.callerlist.column_titles_passive()
        self.callerlist.column_titles_show()
        self.callerlist.connect('select-row', self.selectRowCB)
        self.callerlist.connect('unselect-row', self.unselectRowCB)
        self.callerlist.connect('button_press_event', self.buttonpressCB)
        scroll.add(self.callerlist)

        vbox = GtkVBox()
        vpane.pack2(vbox, resize=1, shrink=1)
        self.thorax = GtkLabel()
        vbox.add(self.thorax, expand=0, fill=0, padding=5)
        frame = GtkFrame('Callees')
        vbox.add(frame, expand=1, fill=1)
        scroll = GtkScrolledWindow()
        scroll.set_policy(POLICY_AUTOMATIC, POLICY_AUTOMATIC)
        frame.add(scroll)
        self.calleelist = GtkCList(cols=5, titles=butterflytitles)
        self.calleelist.column_titles_passive()
        self.calleelist.column_titles_show()
        self.calleelist.connect('select-row', self.selectRowCB)
        self.calleelist.connect('unselect-row', self.unselectRowCB)
        self.calleelist.connect('button_press_event', self.buttonpressCB)
        scroll.add(self.calleelist)

        for c in range(4):
            self.callerlist.set_column_justification(c, JUSTIFY_RIGHT)
            self.calleelist.set_column_justification(c, JUSTIFY_RIGHT)
        self.callerlist.set_column_justification(4, JUSTIFY_LEFT)
        self.calleelist.set_column_justification(4, JUSTIFY_LEFT)

        self.stats = stats
        self.set_function(function)
        self.doubleclicked = 0
        self.gtk.show_all()

    def set_function(self, function):
        self.thorax.set_text(function.fullname())
        self.function = function
        sups = function.get_callers(self.stats.functions)
        sups.sort(displayprof.subsort)
        subs = function.get_callees(self.stats.functions)
        subs.sort(displayprof.subsort)
        self.do_subsup(sups, self.callerlist)
        self.do_subsup(subs, self.calleelist)

    def do_subsup(self, slist, widget):
        widget.freeze()
        widget.clear()
        row = 0
        for subsup in slist:
            ncalls = subsup[0]
            percenttime = subsup[1]
            name = parseFunctionName(subsup[2]) # [file, line, function]
            widget.append([`ncalls`, "%6.2f"%percenttime] + name)
            widget.set_row_data(row, subsup)
            row += 1

        font = self.gtk.get_style().font
        for c in range(5):
            colwidth = widget.optimal_column_width(c)
            headwidth = font.width(butterflytitles[c])
            widget.set_column_width(c, max(headwidth, colwidth))

        widget.thaw()

    def selectRowCB(self, widget, row, col, gdkevent):
        if self.doubleclicked:
            self.doubleclicked = 0
            file, line, func = parseFunctionName(widget.get_row_data(row)[2])
            try:
                # Functions (such as <self>) that don't have a valid
                # line number can't be displayed.
                lineno = int(line)
            except ValueError:
                pass
            else:
                self.set_function(self.stats.get_function(file, lineno, func))
    def unselectRowCB(self, widget, row, col, gdkevent):
        self.doubleclicked = 0
    def buttonpressCB(self, widget, gdkevent):
        if gdkevent.type == GDK._2BUTTON_PRESS:
            self.doubleclicked = 1

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
    mainloop()
