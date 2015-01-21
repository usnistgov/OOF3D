# -*- python -*-
# $RCSfile: fileselector.py,v $
# $Revision: 1.41.2.13 $
# $Author: langer $
# $Date: 2014/09/26 17:35:25 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import ringbuffer
from ooflib.common import utils
from ooflib.common.IO import filenameparam
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import guilogger
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import widgetscope
import cgi
import gtk
import os
import os.path
import re
import string
import weakref

## TODO 3.1: Typing <return> in the File entry should be the same as
## clicking "OK".  (This is hard to do. The OK button is part of a
## generic ParameterDialog, but the FileSelector is just a widget in
## the dialog box.  We don't have a mechanism for the widgets to talk
## to the ParameterDialog buttons.)

# Globals _last_file and _last_dir are dictionaries used to initialize
# FileSelectorWidgets to the final state of the previous widget with
# the same 'ident'.
_last_file = {}
_last_dir = {}
_last_hid = {}

# Installing a search callback via gtk.TreeView.set_search_equal_func
# causes pygtk 2.6 to dump core the second time a FileSelectorWidget
# is used.  We only need to use set_search_equal_func because there's
# pango markup in the file list, so we just don't use markup if we're
# using version 2.6.  (This shouldn't be an issue, pygtk 2.6 is
# ancient.)
use_markup = gtk.pygtk_version[:2] >= (2, 7)

class FileSelectorWidget(parameterwidgets.ParameterWidget):
    
    # Base class for ReadFileSelectorWidget, WriteFileSelectorWidget,
    # etc.  Derived classes must define self.chooserClass, which is
    # used to create the file list.
    
    def __init__(self, param, scope=None, name=None, ident=None,
                 verbose=False):
        debug.mainthreadTest()
        self.param = param
        self.ident = ident or param.ident

        self.lastFile = {}      # last file selected in each directory
        self.fileNames = []     # files in the current directory
        self.dirHier = []       # directories in the current hierarchy
        self.dirHistory = ringbuffer.RingBuffer(50)

        parameterwidgets.ParameterWidget.__init__(self, gtk.Frame(), scope,
                                                  name, expandable=True,
                                                  verbose=verbose)
        vbox = gtk.VBox()
        self.gtk.add(vbox)

        # Directory selector
        hbox = gtk.HBox()
        vbox.pack_start(hbox, expand=False, fill=False)
        hbox.pack_start(gtk.Label("Directory:"), expand=False, fill=False)
        self.dirWidget = chooser.ChooserComboWidget([],
                                                    callback=self.dirChangedCB, 
                                                    name="Directory")
        hbox.pack_start(self.dirWidget.gtk, expand=True, fill=True)

        # Directory selection buttons
        hbox = gtk.HBox(homogeneous=False)
        vbox.pack_start(hbox, expand=False, fill=False)

        self.backbutton = gtkutils.StockButton(gtk.STOCK_GO_BACK, "Back",
                                               align=0.0)
        gtklogger.setWidgetName(self.backbutton, "Back")
        gtklogger.connect(self.backbutton, 'clicked', self.backCB)
        hbox.pack_start(self.backbutton, expand=True, fill=True)

        self.addDirButtons(hbox)

        homebutton = gtkutils.StockButton(gtk.STOCK_HOME)
        gtklogger.setWidgetName(homebutton, "Home")
        gtklogger.connect(homebutton, 'clicked', self.homeCB)
        hbox.pack_start(homebutton, expand=False, fill=True)

        self.nextbutton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD, "Next",
                                               reverse=True, align=1.0)
        gtklogger.setWidgetName(self.nextbutton, "Next")
        gtklogger.connect(self.nextbutton, 'clicked', self.nextCB)
        hbox.pack_start(self.nextbutton, expand=True, fill=True)

        # File list
        self.fileList = self.chooserClass(
            name="FileList",
            callback=self.fileListCB, 
            dbcallback=self.fileListDoubleCB,
            markup=True)
        self.fileList.gtk.set_size_request(-1, 100)
        vbox.pack_start(self.fileList.gtk, expand=True, fill=True)
        # Set the comparison function used when typing in the file
        # list.  _filename_cmp matches the beginnings of file names,
        # ignoring the markup added to directories ane escaped
        # characters.
        if use_markup:
            self.fileList.treeview.set_search_equal_func(_filename_cmp, None)

        align = gtk.Alignment(xalign=1.0)
        vbox.pack_start(align, expand=False, fill=False)
        hbox = gtk.HBox()
        align.add(hbox)
        hbox.pack_start(gtk.Label("show hidden files"), expand=False, fill=False)
        self.hiddenButton = gtk.CheckButton()
        hbox.pack_start(self.hiddenButton, expand=False, fill=False)
        gtklogger.setWidgetName(self.hiddenButton, "ShowHidden")
        gtklogger.connect(self.hiddenButton, 'clicked', self.showHiddenCB)
        
        # Include additional widgets required by subclasses.
        self.addMoreWidgets(vbox)

    def initialize(self):
        # Initialize is called from parameterTableXRef, because the
        # initial state might depend on other widgets in the
        # parameterTable.

        if self.param.value is not None:
            directory, phile = os.path.split(self.param.value)
            # param.value might not have a directory component,
            # especially if the last value was set by a script or
            # command line argument.
            if not directory or not os.path.isdir(directory):
                directory = _last_dir.get(self.ident,
                                          os.path.abspath(os.getcwd()))
        else:
            directory = _last_dir.get(self.ident,
                                      os.path.abspath(os.getcwd()))
            phile = _last_file.get(self.ident, None)

        self.setDirectory(directory)

        self.fileList.suppress_signals()
        self.lastFile[directory] = phile
        if phile:
            self.fileList.set_selection(phile)
        self.fileList.allow_signals()

        self.initializeExtras(directory, phile)
        
        self.sensitize()
        self.widgetChanged(self.checkValidity(), interactive=False)
    
    def setDirectory(self, directory):
        self.hiddenButton.set_active(_last_hid.get(self.ident, False))
        directory = endSlash(directory)
        self.dirHistory.push(directory)
        self.dirWidget.suppress_signals()
        self.dirHier = getDirectoryHierarchy(directory)
        self.dirWidget.update(self.dirHier)
        self.dirWidget.set_state(directory)
        self.dirWidget.allow_signals()
        self.fileList.suppress_signals()
        self.updateFiles(directory)
        self.fileList.allow_signals()

    def parameterTableXRef(self, table, widgets):
        self.initialize()

    def show(self):
        parameterwidgets.ParameterWidget.show(self)
        # Don't let the directory widget have the focus.
        self.fileList.grab_focus()

    def cwd(self):              # Current working directory
        directory = self.dirWidget.get_value()
        if directory == "":
            # Return "" if directory is "".  normpath would return "."
            return ""
        return endSlash(os.path.normpath(directory))

    def updateHierarchy(self, directory):
        # Update the directory hierarchy in the pull down menu part of
        # the ChooserComboWidget.  *Don't* change the hierarchy if the
        # new directory is in the old hierarchy.  This lets the user
        # move up and down the hierarchy easily.
        if directory not in self.dirHier:
            newhier = getDirectoryHierarchy(directory)
            self.dirWidget.update(newhier)
            self.dirHier = newhier

    def updateFiles(self, directory):
        debug.mainthreadTest()
        # Update the displayed list and the internal list of files in
        # the current directory.
        self.fileNames = os.listdir(directory)
        if not self.hiddenButton.get_active():
            self.fileNames = [f for f in self.fileNames if f[0] != "."]
        self.fileNames.sort()
        displaylist = [_addMarkup(directory, filename)
                       for filename in self.fileNames]
        self.fileList.update(objlist=self.fileNames, displaylist=displaylist)
        # Make sure that the last file visited is still there.
        try:
            if self.lastFile[directory] not in self.fileNames:
                del self.lastFile[directory]
        except KeyError:
            pass

    def clearFile(self):
        self.fileList.set_selection(None)

    def switchDir(self, directory):
        debug.mainthreadTest()
        # switchDir is called when double-clicking a directory name in
        # the fileList, when typing a directory name in the fileEntry,
        # or after creating a new directory.  In all cases, both the
        # directory widget and the file widgets need to be updated.
        directory = endSlash(directory)
        self.fileList.suppress_signals()
        self.dirWidget.suppress_signals()
        try:
            self.preSwitchHook()
            self.updateHierarchy(directory)
            self.dirWidget.set_state(directory)
            self.updateFiles(directory)
            _last_dir[self.ident] = directory
            self.postSwitchHook(directory)
            self.sensitize()
            self.widgetChanged(self.checkValidity(), interactive=True)
        finally:
            self.dirWidget.allow_signals()
            self.fileList.allow_signals()

    # Subclasses can redefine these to do things before and after
    # switching directories.
    def preSwitchHook(self):
        pass
    def postSwitchHook(self, directory):
        pass

    def sensitize(self):
        debug.mainthreadTest()
        self.backbutton.set_sensitive(not self.dirHistory.atBottom())
        self.nextbutton.set_sensitive(not self.dirHistory.atTop())
        directory = self.cwd()
        dirok = os.path.isdir(directory)
        self.fileList.gtk.set_sensitive(dirok)
        self.sensitizeExtras(directory)

    # Callbacks

    def dirChangedCB(self, combobox): # directory widget callback
        self.preSwitchHook()
        directory = self.cwd()        # adds trailing slash if needed
        ## Don't do anything except sensitize widgets if the new
        ## directory isn't valid, or isn't different from the old one.
        ## Typing in the directory widget may cause it to be set to
        ## something that's not a directory.  Adding or deleting a "/"
        ## doesn't actually change the directory.
        if os.path.isdir(directory) and directory!=self.dirHistory.current():
            self.dirHistory.push(directory)
            _last_dir[self.ident] = directory
            self.updateFiles(directory)
            self.postSwitchHook(directory)
            self.dirWidget.suppress_signals()
            try:
                self.updateHierarchy(directory)
            finally:
                self.dirWidget.allow_signals()
        self.sensitize()
        self.widgetChanged(self.checkValidity(), interactive=True)

    def backCB(self, button):
        self.switchDir(self.dirHistory.prev())

    def nextCB(self, button):
        self.switchDir(self.dirHistory.next())

    def homeCB(self, button):
        directory = os.path.expanduser("~")
        self.dirHistory.push(directory)
        self.switchDir(directory)

    def fileListCB(self, filename, interactive):
        debug.mainthreadTest()
        if len(self.dirHistory) == 0: # not initialized yet
            return
        if filename:
            self.lastFile[self.dirHistory.current()] = filename
            _last_file[self.ident] = filename
        self.fileListCBextras(filename)
        self.widgetChanged(self.checkValidity(), interactive)

    def showHiddenCB(self, button):
        _last_hid[self.ident] = button.get_active()
        self.updateFiles(self.dirHistory.current())

    def fileListDoubleCB(self, filename):
        debug.mainthreadTest()
        self.lastFile[self.dirHistory.current()] = filename
        filepath = os.path.join(self.dirWidget.get_value(), filename)
        if os.path.isdir(filepath):
            self.dirHistory.push(endSlash(filepath))
            self.switchDir(filepath)
            
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FileOrDirectorySelectorWidget(FileSelectorWidget):
    chooserClass = chooser.ScrolledChooserListWidget
    def addDirButtons(self, hbox):
        pass
    def addMoreWidgets(self, vbox):
        pass
    def initializeExtras(self, directory, phile):
        pass
    def sensitizeExtras(self, directory):
        pass
    def fileListCBextras(self, filename):
        pass
    def postSwitchHook(self, directory):
        debug.mainthreadTest()
        # Set the file list and file entry to the name of the last
        # file visited in this directory, if any.  Called whenever the
        # directory changes.
        name = self.lastFile.get(directory, "")
        if not name:    # no last file
            self.fileList.set_selection(None)
            self.fileList.scroll_to_line(0)
            _last_file[self.ident] = None
        else:
            self.fileList.set_selection(name)
            _last_file[self.ident] = name
    def checkValidity(self):
        filename = self.fileList.get_value()
        return ((filename is not None and 
                os.path.isfile(os.path.join(self.cwd(), filename)))
                or
                (filename is not None and
                os.path.isdir(os.path.join(self.cwd(), filename)))
                or
                (filename is None and os.path.isdir(self.cwd())))
    def get_value(self):
        name = self.fileList.get_value()
        if name:
            return os.path.join(self.cwd(), name)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ReadFileSelectorWidget(FileOrDirectorySelectorWidget):
    def get_value(self):
        try:
            return os.path.join(self.cwd(), self.fileList.get_value())
        except:
            return None
    def checkValidity(self):
        filename = self.fileList.get_value()
        return (filename is not None and 
                os.path.isfile(os.path.join(self.cwd(), filename)))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class DirectorySelectorWidget(FileOrDirectorySelectorWidget):
    def checkValidity(self):
        filename = self.fileList.get_value()
        return ((filename is not None and
                os.path.isdir(os.path.join(self.cwd(), filename)))
                or
                (filename is None and os.path.isdir(self.cwd())))
    def get_value(self):
        name = self.fileList.get_value()
        if name:
            return os.path.join(self.cwd(), name)
        return self.cwd()
    def fileListCB(self, filename, interactive):
        debug.mainthreadTest()
        if len(self.dirHistory) == 0: # not initialized yet
            return
        if filename:
            # If a file has been clicked, send a signal so that other
            # widgets (such as a PatternParameterWidget) can adjust
            # themselves, but don't leave the file selected.  Only
            # directories can actually be selected.
            filepath = os.path.join(self.dirWidget.get_value(), filename)
            if os.path.isfile(filepath):
                switchboard.notify((self, "fileclicked"), filename)
                self.fileList.set_selection(None)
        self.widgetChanged(self.checkValidity(), interactive)

# ImpliedDirectorySelectorWidget is a "faceless" widget.  When used in
# a ParameterTable (which is the only place it should be used) it
# doesn't actually appear.  Instead, it looks for a FileSelector in
# the same table and returns the file selector's current directory.
# It's used in situations in which the file name(s) and directory name
# have to be returned by separate OOFMenuItem or RegisteredClass
# Parameters.  In those cases, the directory name Parameter should be
# an ImpliedDirectoryNameParameter.

class ImpliedDirectorySelectorWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        parameterwidgets.ParameterWidget.__init__(self, None, scope=scope,
                                                  name=name, faceless=True,
                                                  verbose=verbose)
        self.fileselector = None
        self.param = param
        # self.widgetChanged(self.checkValidity(), interactive=False)
    def get_value(self):
        return self.fileselector.cwd()
    def parameterTableXRef(self, ptable, widgets):
        for widget in widgets:
            if isinstance(widget, FileSelectorWidget):
                self.fileselector = widget
                switchboard.requestCallbackMain(self.fileselector, self.fsCB)
                # self.widgetChanged(self.checkValidity(), interactive=False)
                return
        raise ooferror.ErrPyProgrammingError(
            "ImpliedDirectorySelectorWidget has no FileSelectorWidget.")
    def checkValidity(self):
        return self.fileselector and self.fileselector.cwd()
    def fsCB(self, *args, **kwargs):
        self.widgetChanged(self.checkValidity(), interactive=False)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FileListWidget(ReadFileSelectorWidget):
    chooserClass = chooser.ScrolledMultiListWidget
    def get_value(self):
        return self.fileList.get_value()
    def fileListDoubleCB(self, filenames):
        debug.mainthreadTest()
        self.lastFile[self.dirHistory.current()] = filenames
        filepath = os.path.join(self.dirWidget.get_value(), filenames[0])
        if os.path.isdir(filepath):
            self.dirHistory.push(endSlash(filepath))
            self.switchDir(filepath)
    def checkValidity(self):
        filenames = self.fileList.get_value()
        if not filenames:
            return False
        for name in filenames:
            if not os.path.isfile(os.path.join(self.cwd(), name)):
                return False
        return True
    def initialize(self):
        # Get the directory from the associated
        # ImpliedDirectoryNameParameter.
        impliedDirWidget = self.scope.findWidget(
            lambda x: isinstance(x, ImpliedDirectorySelectorWidget))
        directory = None
        if impliedDirWidget is not None:
            directory = impliedDirWidget.param.value
        if directory is None:
            directory = os.getcwd()
        self.setDirectory(directory)
        files = self.param.value
        self.lastFile[directory] = files
        if files:
            self.fileList.suppress_signals()
            self.fileList.set_selection(files)
            self.fileList.allow_signals()
        self.initializeExtras(directory, files)
        self.widgetChanged(self.checkValidity(), interactive=False)
            
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class WriteFileSelectorWidget(FileSelectorWidget):

    ## TODO 3.1: Add an option for forbidding append mode.  It doesn't
    ## make sense to append to some types of files (such as images).

    chooserClass = chooser.ScrolledChooserListWidget

    def __init__(self, *args, **kwargs):
        self.savedName = ""
        FileSelectorWidget.__init__(self, *args, **kwargs)

    def addDirButtons(self, hbox): # directory navigation buttons
        self.newdirbutton = gtkutils.StockButton(gtk.STOCK_DIRECTORY, "New")
        gtklogger.setWidgetName(self.newdirbutton, "NewDir")
        gtklogger.connect(self.newdirbutton, 'clicked', self.newdirCB)
        hbox.pack_start(self.newdirbutton, expand=False, fill=True)

    def addMoreWidgets(self, vbox): # Widgets below the file list.
        hbox = gtk.HBox()
        vbox.pack_start(hbox, expand=False, fill=False)
        label = gtk.Label('File:')
        hbox.pack_start(gtk.Label('File:'), expand=False, fill=False)
        self.fileEntry = gtk.Entry()
        gtklogger.setWidgetName(self.fileEntry, 'File')
        self.fileEntrySignal = gtklogger.connect(self.fileEntry, 'changed',
                                                 self.entryChangeCB)
        hbox.pack_start(self.fileEntry, expand=True, fill=True)

        ## It's tempting to make hitting <return> in the fileEntry
        ## widget have the same effect as hitting the OK button, when
        ## this widget is used in a dialog.  However, here we don't
        ## know for sure that it's used in a dialog, and we have no
        ## easy access to the ParameterDialog's OK button in any case.
#         gtklogger.connect(self.fileEntry, 'activate', self.entryActivateCB)

        # Add file-name completion in the fileEntry widget.  The
        # fileList already has file-name completion in it.
        self.completion = gtk.EntryCompletion()
        self.fileEntry.set_completion(self.completion)
        self.completion.set_model(self.fileList.liststore)
        self.completion.set_text_column(0)

    def preSwitchHook(self):
        self.savedName = self.fileEntry.get_text()

    def show(self):
        FileSelectorWidget.show(self)
        # If the file entry widget doesn't grab focus here, then the
        # directory entry widget will have it, and careless users will
        # overwrite the directory name.
        self.fileEntry.grab_focus()

    def initializeExtras(self, directory, phile):
        if phile:
            self.fileEntrySignal.block()
            try:
                self.fileEntry.set_text(phile)
            finally:
                self.fileEntrySignal.unblock()

    def sensitizeExtras(self, directory):
        self.fileEntry.set_sensitive(os.path.isdir(directory))

    def postSwitchHook(self, directory):
        debug.mainthreadTest()
        # Set the file list and file entry to the name of the last
        # file visited in this directory, if any.  Called whenever the
        # directory changes.
        self.fileEntrySignal.block()
        try:
            name = self.lastFile.get(directory, self.savedName)
            if not name:
                self.fileEntry.set_text("")
                self.fileList.set_selection(None)
                self.fileList.scroll_to_line(0)
                _last_file[self.ident] = None
            else:
                self.fileEntry.set_text(name)
                self.fileList.set_selection(name)
                _last_file[self.ident] = name
        finally:
            self.fileEntrySignal.unblock()

    def get_value(self):
        debug.mainthreadTest()
        phile = os.path.join(self.cwd(), self.fileEntry.get_text())
        if not os.path.isdir(phile):
            return phile
        else:
            return None

    def checkValidity(self):
        debug.mainthreadTest()
        directory = self.cwd()
        filename = os.path.join(directory, self.fileEntry.get_text())
        return (os.path.isdir(directory) and 
                filename != "" and filename is not None and
                not os.path.isdir(filename))

    def newdirCB(self, button):
        dirnameparam = parameter.StringParameter('directory name')
        if parameterwidgets.getParameters(dirnameparam,
                                          title="New Directory"):
            if dirnameparam.value[0] != os.sep:
                dirname = os.path.join(self.cwd(), dirnameparam.value)
            else:
                dirname = dirnameparam.value
            os.mkdir(dirname)   # raises exception if file exists
            self.dirHistory.push(dirname)
            self.switchDir(dirname)

    def entryChangeCB(self, entry): # Typing in the file entry widget
        debug.mainthreadTest()
        self.widgetChanged(self.checkValidity(), interactive=True)
        # Set fileList, if typing matches
        filename = self.fileEntry.get_text()
        if filename in self.fileNames:
            self.fileList.set_selection(filename)
            _last_file[self.ident] = filename
        else:
            self.fileList.set_selection(None)
            if filename:
                # Scroll to the last match for the current text.
                ## TODO OPT: Is this going to be too slow for large
                ## directories?  The linear search may be inappropriate.
                # It would be cleaner to use 'reversed(enumerate(names))',
                # but reversed doesn't work on iterators.
                for rlineno, fname in enumerate(reversed(self.fileNames)):
                    if fname.startswith(filename):
                        self.fileList.scroll_to_line(
                            len(self.fileNames)-rlineno-1)
          
    ## See comment about about handling <return>.
#     def entryActivateCB(self, entry): 
#         pass

    def fileListCBextras(self, filename):
        if filename and not os.path.isdir(os.path.join(self.cwd(), filename)):
            self.fileEntrySignal.block()
            try:
                self.fileEntry.set_text(filename or "")
                self.fileEntry.set_position(-1) # cursor at end
            finally:
                self.fileEntrySignal.unblock()

# end WriteFileSelectorWidget
        
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
    
# Utility functions used by FileSelectorWidget

def _addMarkup(directory, filename):
    if use_markup:
        if filename and os.path.isdir(os.path.join(directory, filename)):
            return "<b>" + cgi.escape(filename) + "</b>"
        return cgi.escape(filename)
    return filename

def _filename_cmp(model, column, key, iter, data):
    # Comparisons made while searching in the file list use the raw
    # file name, in column 1 of the model, instead of the marked-up
    # file name in column 0. Only used if use_markup is True.
    name = model[iter][1]
    return not name.startswith(key)

def endSlash(dirname):
    # Make sure all directory names end consistently with "/" so that
    # string comparisons on them don't fail because of inconsequential
    # ending slashes.
    if not dirname:
        return os.sep
    if (dirname[-1] == os.sep or dirname.endswith(os.sep+".") or
        dirname.endswith(os.sep+"..")):
        return dirname
    return dirname + os.sep

def getDirectoryHierarchy(directory):
    # Return a list of all directories in the hierarchy from root
    # to the given directory, eg. ["/", "/Users/", "/Users/oofuser/"]
    names = filter(None, os.path.abspath(directory).split(os.sep))
    if names:
        return [os.sep] + [os.sep + os.path.join(*names[:n]) + os.sep
                           for n in range(1,len(names)+1)]
    return [os.sep]

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# When using gtklogger, the WriteFileSelectorWidget and
# ReadFileSelectorWidget are inconvenient.  Because the files are
# listed in a TreeView (inside the ScrolledChooserListWidget), when a
# file is selected the corresponding row number of the TreeView is
# logged.  If files are added or removed to the directory, the correct
# row number will change, breaking the test script.  So when recording
# or replaying, we replace the fancy FileSelectorWidget machinery with
# a simple StringWidget, which doesn't have this problem.  It's
# renamed to "FakeFileSelectorWidget" so that the WriteModeWidget can
# find it.

class FakeFileSelectorWidget(parameterwidgets.StringWidget):
    pass

def _WFileNameParameter_makeWidget(self, scope=None, verbose=False):
    if not (guilogger.recording() or guilogger.replaying()):
        return WriteFileSelectorWidget(self, scope=scope, name=self.name,
                                       verbose=verbose)
    else:
        return FakeFileSelectorWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)
    

def _FileOrDirectoryParameter_makeWidget(self, scope=None, verbose=False):
    if not (guilogger.recording() or guilogger.replaying()):
        return FileOrDirectorySelectorWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)
    else:
        return FakeFileSelectorWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)
   
def _RFileNameParameter_makeWidget(self, scope=None, verbose=False):
    if not (guilogger.recording() or guilogger.replaying()):
        return ReadFileSelectorWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)
    else:
        return FakeFileSelectorWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)

def _DirNameParameter_makeWidget(self, scope=None, verbose=False):
    if not (guilogger.recording() or guilogger.replaying()):
        return DirectorySelectorWidget(self, scope=scope, name=self.name,
                                       verbose=verbose)
    else:
        return FakeFileSelectorWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)

def _ImpliedDirName_makeWidget(self, scope=None, verbose=False):
    if not (guilogger.recording() or guilogger.replaying()):
        return ImpliedDirectorySelectorWidget(self, scope=scope, name=self.name,
                                              verbose=verbose)
    else:
        return FakeFileSelectorWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)

def _FileListParameter_makeWidget(self, scope=None, verbose=False):
    if not (guilogger.recording() or guilogger.replaying()):
        return FileListWidget(self, scope=scope, name=self.name, 
                              verbose=verbose)
    else:
        return FakeFileSelectorWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)

filenameparam.WriteFileNameParameter.makeWidget = _WFileNameParameter_makeWidget
filenameparam.FileOrDirectoryParameter.makeWidget= _FileOrDirectoryParameter_makeWidget
filenameparam.ReadFileNameParameter.makeWidget = _RFileNameParameter_makeWidget
filenameparam.DirectoryNameParameter.makeWidget = _DirNameParameter_makeWidget
filenameparam.FileListParameter.makeWidget = _FileListParameter_makeWidget
filenameparam.ImpliedDirectoryNameParameter.makeWidget = _ImpliedDirName_makeWidget

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# The WriteModeWidget sets a WriteModeParameter to either 'w' or 'a'.
# It's not a simple EnumWidget because the choices it presents to the
# user depend on whether or not the file selected in the associated
# FileSelectorWidget exists already or not.

# TODO 3.1: If there are ever two WriteFileNameParameters and two
# WriteModeParameters in the same widget scope, both
# WriteModeParameters will probably refer to the same
# WriteFileNameParameter.  Some cleverer scheme will have to be used.

class WriteModeWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.state = None
        self.widget = chooser.ChooserWidget([], self.chooserCB, name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk,
                                                  scope=scope, verbose=verbose)
        if not (guilogger.recording() or guilogger.replaying()):
            self.fileSelector = self.scope.findWidget(
                lambda x: (isinstance(x, WriteFileSelectorWidget)))
        else:
            self.fileSelector = self.scope.findWidget(
                lambda x: (isinstance(x, FakeFileSelectorWidget)))
        if self.fileSelector is None:
            raise ooferror.ErrPyProgrammingError("Can't find file selector")
        self.set_options()
        self.widgetChanged(True, True)
        self.sbcallback = switchboard.requestCallbackMain(self.fileSelector,
                                                          self.fileSelectorCB)
    
    def cleanUp(self):
        switchboard.removeCallback(self.sbcallback)
        parameterwidgets.ParameterWidget.cleanUp(self)

    def chooserCB(self, *args):
        self.set_options()
        self.widgetChanged(True, True)

    def fileSelectorCB(self, *args):
        self.set_options()

    def set_options(self):
        phile = self.fileSelector.get_value()
        if phile and os.path.exists(phile):
            if self.state != "overwrite":
                self.state = "overwrite"
                ## TODO 3.1: render "OVERWRITE" in bold
                self.widget.update(["OVERWRITE", "append"])
        else:
            if self.state != "write":
                self.state = "write"
                self.widget.update(["write", "append"])

    def get_value(self):
        widgetval = self.widget.get_value()
        if widgetval == "append":
            return 'a'
        return 'w'

def _writeModeParam_makeWidget(self, scope=None, verbose=False):
    return WriteModeWidget(self, scope=scope, name=self.name, verbose=verbose)

filenameparam.WriteModeParameter.makeWidget = _writeModeParam_makeWidget

# The OverwriteModeWidget is for files that can't be appended to.  The
# user has to agree to overwrite, or the widget declares itself to be
# in an invalid state, therefore disabling the associated dialog or
# page's OK button.

class OverwriteWidget(parameterwidgets.BooleanWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        parameterwidgets.BooleanWidget.__init__(self, param, scope, name,
                                                verbose=verbose)
        self.fileSelector = self.scope.findWidget(
            lambda x: (isinstance(x, WriteFileSelectorWidget)))
        if self.fileSelector is None:
            raise ooferror.ErrPyProgrammingError("Can't find file selector")
        self.set_validity()
        self.sbcallback = switchboard.requestCallbackMain(self.fileSelector,
                                                          self.fileSelectorCB)
    def cleanUp(self):
        switchboard.removeCallback(self.sbcallback)
        parameterwidgets.ParameterWidget.cleanUp(self)
        
    def set_validity(self):
        phile = self.fileSelector.get_value()
        if phile and os.path.exists(phile) and not self.get_value():
            self.widgetChanged(False, interactive=False)
        else:
            self.widgetChanged(True, interactive=False)

    def buttonCB(self, button):
        parameterwidgets.BooleanWidget.buttonCB(self, button)
        self.set_validity()

    def fileSelectorCB(self, *args):
        self.set_validity()

def _overwriteParam_makeWidget(self, scope=None, verbose=False):
    return OverwriteWidget(self, scope=scope, name=self.name, verbose=verbose)

filenameparam.OverwriteParameter.makeWidget = _overwriteParam_makeWidget

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Utilities that just get a file name or a file name and a mode.  If
# it's necessary to get a bunch of parameter values that include a
# FileNameParameter, use parameterwidgets.getParameters() instead.

def getFileAndMode(ident=None, title=""):
    fileparam = filenameparam.WriteFileNameParameter('filename', ident=ident)
    modeparam = filenameparam.WriteModeParameter('mode')
    if parameterwidgets.getParameters(fileparam, modeparam, title=title):
        return fileparam.value, modeparam.value.string()

def getFile(ident=None, title=""):
    fileparam = filenameparam.WriteFileNameParameter('filename', ident=ident)
    if parameterwidgets.getParameters(fileparam, title=title):
        return fileparam.value

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# PatternParameters are used in conjunction with
# DirectoryNameParameters.  A click on a filename in a
# DirectorySelectorWidget sends a signal to a PatternParameterWidget
# telling it to fill itself with a good guess for a pattern that would
# select the file.

class PatternParameterWidget(parameterwidgets.StringWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        parameterwidgets.StringWidget.__init__(self, param, scope, name,
                                               verbose=verbose)
    def parameterTableXRef(self, ptable, widgets):
        for widget in widgets:
            if isinstance(widget, FileSelectorWidget):
                switchboard.requestCallbackMain((widget, "fileclicked"),
                                                self.fileselectorCB)
                return
    def fileselectorCB(self, filename):
        # Construct a regular expression that matches the given
        # filename and any other names that differ only numerically.
        # If it looks like the numbers in the filename are padded on
        # the left with zeros, the expression will only match names
        # with the same number of digits. If it looks like they're not
        # padded, any number of digits is acceptable.  For example:

        # "abc001.png" will match "abc000.png" and abc100.png" but not
        # "abc001.gif" or "abc2.png", "abc02.png", or "abc0002.png".
        
        # "abc1.png" will match "abc2.png" but not "abc02.png".

        # "abc3" will match "abc34234" but not "abc3.gif".

        # Special case: "abc0.png" will match "abc1.png" and
        # "abc10.png", but not "abc01.png".  A single digit 0 is
        # assumed *not* to be padded.

        splitname = re.split("([0-9]+)", filename)
        # If the filename ends with digits, then the last item in
        # splitname is an empty string.
        if not splitname[-1]:
            splitname = splitname[:-1]
            lastdigits = True
        else:
            lastdigits = False
        for i, substr in enumerate(splitname):
            if substr.isdigit():
                if substr[0] == '0' and len(substr) > 1:
                    # Padding detected.  Match exactly len digits.
                    splitname[i] = "[0-9]{%d}" % len(substr)
                else:
                    # No padding.  Match any single digit including 0,
                    # or multiple digits not starting with 0.
                    splitname[i] = "(0|([1-9][0-9]*))"
            else:
                splitname[i] = substr.replace(".", r"\.")
        if lastdigits:
            splitname.append("$")
        f = "".join(splitname)
        self.set_value(f)
        self.widgetChanged(self.validValue(f), interactive=0)

def _patternParam_makeWidget(self, scope=None, verbose=False):
    return PatternParameterWidget(self, scope=scope, name=self.name,
                                  verbose=verbose)

filenameparam.PatternParameter.makeWidget = _patternParam_makeWidget
