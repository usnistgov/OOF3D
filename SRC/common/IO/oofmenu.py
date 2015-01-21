# -*- python -*-
# $RCSfile: oofmenu.py,v $
# $Revision: 1.138.2.6 $
# $Author: langer $
# $Date: 2014/07/31 20:52:16 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.


""" The classes in oofmenu.py describe the menus of commands that
represent all of the actions that OOF performs.  These menus form the
API between the guts of the program and the user interfaces, both
graphical (GUI) and command-line (CLI).  The menus can be used
directly in CLI mode, and can be automatically converted to GTK+ menus
in GUI mode.  [The code in this file defines only the menus and their
CLI interface.  The GUI interface is defined in common.IO.GUI.gfxmenu.
This file is independent of that one, although some of the comments
here may refer to it.]

The menu commands can be logged (scripted), either as they're
performed or as an afterthought.  The log file (script) can be read
back in to re-execute the commands.


----------------

To enforce the scriptability of all commands, all GUI and CLI commands
have to come from a common set of menus.  But in some circumstances, a
menu item may demand different actions in GUI and CLI modes.  For
example, the command "File/Open" should open a dialog box in GUI mode,
but should open a file in CLI mode.  These menu items must therefore
have two callbacks, one for each mode.  The GUI callback should not be
logged, since presumably it's not going to perform an action that
affects the state of the guts of the program; it's just going to open
a window in which the action will be performed.

----------------

The fundamental class is the OOFMenuItem.  This is the base class for
all OOF menu objects, even the menus.  That's because, as explained
above, some menus look like commands in some contexts.  OOFMenuItems
have the following constructor arguments:

name:         A string.  The string must be a valid Python identifier, because
              in CLI mode it will be typed to execute the command.
              That means that it must begin with an underscore or a
              letter and can contain only underscores, letters, and
              digits.  Because it's nice to have spaces in GUI mode,
              before being displayed in the GUI single underscores are
              turned into spaces and double underscores are turned
              into single underscores.

callback:     The function to be called when the command is executed
              in CLI mode.  The function takes at least one argument,
              which is the OOFMenuItem which caused it to be called.
              More arguments can be specified with the params
              constructor argument.  The callback argument is
              optional, but a menu item isn't much use if a callback
              isn't provided. [default value = None]

gui_callback: The function to be called when the menu item is chosen
              in GUI mode.  GUI callbacks take exactly one argument,
              which is the OOFMenuItem that invoked them.  If the
              non-GUI callback for the OOFMenuItem has no additional
              params, and if gui_callback is None, then the non-GUI
              callback will be invoked from the GUI.  If the non-GUI
              callback does have params, but no GUI callback is provided,
              then a simple dialog box is created allowing the params to
              be set. [default value = None]

accel:	      A string describing the keyboard accelerator to be used
              in GUI mode.  The string must be a key symbol defined in
              GDK.py.  For example, accel='d' makes Alt-D the
              accelerator.  accel='equal' makes Alt-= the
              accelerator.  [default value = None]

secret:	      If secret=0, then the menu item is visible.  If secret=1, the
              menu item is not displayed in either GUI or CLI mode.
              However, explicitly requesting the display of a secret
              menu will display it.  This allows all of the OOF menus
              to live in a single menu hierarchy.  For example,
              OOF.Graphics.gfx_1 is a secret menu in the main Graphics
              menu, and contains the menu for the first graphics
              window.  That menu is actually displayed in the graphics
              window, because it was explicitly created with
              gfxmenu.gtkOOFMenuBar(OOF.Graphics.gfx1).  [default value
              = 0]
              
ellipsis:     If ellipsis=1, then the item's name has '...' appended to it
              when displayed. [default value = 0]
              
help:	      A helpful string.  Appears in tooltips.

discussion:   A longer helpful string.  It should be a series of xml
              elements legal for the body of a DocBook refsect1 element.

params:	      A list of Parameters that are provided as arguments to
              the non-GUI callback function.  The Parameter class is
              defined in commmon.IO.parameter.  The callback will be
              called with additional keyword arguments, one for each
              parameter, using Parameter.name and Parameter.value for
              the key and value.  [default value = []]

help_menu:    If help_menu=1, then this item is presumed to be a 'Help'
              menu and will be right justified in a GUI menu bar.  Setting
              help_menu=1 on anything other than a plain old OOFMenuItem with
              no callback doesn't make any sense, and may cause confusion.

ordering:     New items are added to menus just before the first item with
              a larger ordering number.  Items with the same ordering number
              appear in the order in which they're added. [default value=0]

Options:      Any additional keyword arguments to the OOFMenuItem
              constructor are options that apply to the menu item and
              to all its children (unless overridden in a child).  The
              allowed options are listed in _allowed_options, and are:
	        gui_only:  items appear only in GUI mode
		cli_only:  items appear only in CLI mode
		no_log:	   items are not logged
                no_doc:    items don't appear in documentation
	      If an option is not provided, its value is taken from
	      the menu items parent.

Functions:

root():	  Returns the root of the menu hierarchy.

log(string):  Adds the given string to the log.

add_gui_callback(function):  Assigns a separate callback to be use in gui mode.
                             The callback function takes a single
                             argument, which is the menu item.

Data:

data:	  This is just a convenient spot for storing any additional
          data that might need to be passed through to the callbacks.
          OOFMenuItem.data is not used by the OOFMenu classes.


Menus:

There used to be a separate class, named 'OOFMenu', derived from
OOFMenuItem.  That was deemed to be a mistake, and now there's no
distinction between menus and menu items, except that menus are menu
items that have subitems assigned to them.  The following functions
act on subitems:

addItem(item):  Adds a previously constructed OOFMenuItem to the menu.

getItem(name):  Returns the menuitem with the given name.

removeItem(name):  Removes the menuitem with the given name from the
                   menu. 

makeGroup():  Creates a group for radio menu items.  See
              RadioOOFMenuItem below.

apply(f):    Applies the function f to all OOFMenuItems in the hierarchy.
             (Remember that OOFMenus are OOFMenuItems, too.)  The first
             argument to f() is the OOFMenuItem.  Additional arguments to
             apply() are passed on as additional arguments to f().
             This function is used by the text menu dumping command.
             
-----------------------------

There are three special derived types of OOFMenuItem: OOFRootMenu,
CheckOOFMenuItem, RadioOOFMenuItem.

---------

OOFRootMenu:

The root of the menu hierarchy must be an OOFRootMenu instance.
OOFRootMenu is derived from OOFMenuItem, and adds the following
functions:

addLogger(logger):  Adds a new logging method.  'logger' must be a
              callable object that takes a string as an argument.  See
              MenuLogger, below.   More than one logging method can be
              active at once.

removeLogger(logger): Stops logging with the given logging method.

saveLog(file):  Write the internal log to a file.  file must be a
                Python file object, or something that looks like one.

clearLog():  Clears the internally maintained log.

haltLog():  Temporarily suspend logging.

resumeLog(): Resume logging after haltLog().  Each call to haltLog()
             must be matched by a call to resumeLog() before logging
             will actually resume.

When commands are logged, they are logged as Python expressions, like
"rootmenu.menu.submenu.etc.function(arg=...)".  The names of the
menus, submenus, and functions are the 'name' attributes of the
corresponding OOFMenuItems.  Therefore, the logged menu commands are
accessible in a script only if the script is executed in an
environment in which the root menu's name (as a Python reference) is
the same as its name attribute.


----------

Return values:

Menu commands do not return results -- they only change the state of
the system by the actions of their callbacks.  This makes it safe to
launch a menu callback on a subthread, and then proceed to launch
others on other threads without having to wait.

  
----------

CheckOOFMenuItem:

A CheckOOFMenuItem is an OOFMenuItem that has a value, which can be 0
or 1.  In GUI mode, a check box is drawn next to the menu item's name,
indicating the value.  A CheckOOFMenuItem can have no params.  Its
constructor has one additional argument, value, which is the item's
initial value.  The callback for a CheckOOFMenuItem has two arguments,
the calling CheckOOFMenuItem, and the value.  A CheckOOFMenuItem can
have no separately specified gui_callback.

-----------

RadioOOFMenuItem:

A RadioOOFMenuItem is a CheckOOFMenuItem that lives in a group.  One
item in the group has value=1.  All the others have value=0.  The
constructor takes one additional argument, group, which must be a
group returned from OOFMenu.makeGroup().  When a RadioOOFMenuItem is
executed, its callback is called with value=1, but first the callbacks
for all other items in the group are called with value=0, if they had
value=1.

----------------------------------

GUI callbacks:

Every object in the GUI that corresponds to a change in the state of
the OOF guts should have a corresponding menu item, so that it can be
scripted.  But it is common for the GUI to have many widgets that set
values that aren't used until some other widget is activated.  Here's
an example:

The filename input widget in a file selector dialog box isn't used
until the "OK" button is pressed.  So the filename input widget should
not correspond to a menu item.  Furthermore, the File/Open menu item
should correspond to a logged command in the CLI:
root.file.open(filename=name) but should simply open a window in the
GUI.  Therefore, the OOFMenuItem for file.open must have two
callbacks.  It might be constructed like this:

fileopen = OOFMenuItem('open',
                       callback=cli_fileopen_callback,
		       gui_callback = gui_fileopen_callback,
		       params=[StringParameter('filename')])
                                    
The CLI callback looks like this:

def cli_fileopen_callback(menuitem, filename):
   file = open(filename, "r")
   [whatever...]

The first argument, menuitem, is a reference to fileopen, the calling
OOFMenuItem.   The second argument is the first (and only, in this
case) Parameter from the params list in the OOFMenuItem constructor.

The GUI callback looks like this:

def gui_fileopen_callback(menuitem):
   fname = graphical_way_of_getting_filename()
   menuitem(filename=fname)

The last line calls the CLI callback, setting the filename argument to
the fname obtained by the GUI.  It's important to call the CLI
callback in this way, rather than invoking it directly, so that the
call can be logged.


Here's another example:

Imagine a menu item 'Dessert' that, in GUI mode opens a window on
which there are two buttons, 'Pie' and 'Cake'.  In the CLI mode,
however, 'Dessert' is a menu containing two items, 'Pie' and 'Cake'.
So the OOFMenuItem 'Dessert' needs to be an OOFMenu, constructed like
this:

dessert = OOFMenu('Dessert', callback=None, gui_callback=dessert_gui)
dessert.addItem(OOFMenuItem('Pie', callback=pie, cli_only=1))
dessert.addItem(OOFMenuItem('Cake', callback=cake, cli_only=1))

Note that the subitems are marked 'cli_only' so that they don't appear
in the GUI menu.

The CLI callbacks are straightforward:

def pie(menuitem): print "Yummm, pie!"

def cake(menuitem): print "Yummm, cake!"

The gui_callback for dessert creates a window and remembers the
OOFMenuItem that created it:

def dessert_gui(menuitem):
    gui = DessertGUI(menuitem)
   
class DessertGUI:
    def __init__(self, menuitem):
        self.menuitem = menuitem
        window = create_dessert_window(self.pie_button_cb, self.cake_button_cb)
	window.show()

The callbacks for the buttons in the GUI now can call the non-GUI callbacks:
    def pie_button_cb(self):
        self.menuitem.getItem('Pie')()  # Calls and logs pie()
    def cake_button_cb(self):
        self.menuitem.getItem('Cake')() # Calls and logs cake()

----------------------------------
----------------------------------

CLI Operation:

Assume that root is an OOFRootMenu instance.

>>> root.function()
executes the OOFMenuItem named 'function' in the menu.

If the function takes arguments (params), they can be provided as
  keywords:
>>> root.function(a='eh', pi=3.14)

If not all the arguments are provided in an interactive session, the
user will be prompted for the remainder:

>>> root.function(a='eh')
Enter pi [3.14]: 22/7

The value in braces is a default value to be used if the user doesn't
enter anything.  Any valid Python expression can be entered.  The
default value is the last value used for this parameter.

Items in submenus are accessed by typing the full path from the root
menu:

>>> root.submenu.subsubmenu.function()

To execute a number of commands from a single submenu, just define a
variable referring to the submenu:

>>> sub = root.submenu.subsubmenu
>>> sub.function()
>>> sub.otherfunction()

To get help, simply type an item's name, without the trailing parentheses.

"""

from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common import garbage
from ooflib.common import oofversion
from ooflib.common import parallel_enable
from ooflib.common import thread_enable
from ooflib.common import utils
from ooflib.common import worker
from ooflib.common.IO import menuparser
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
import string
import types
import weakref


#####################################

# Options for menu items are given by keyword arguments in the
# contructor.  The allowed options are listed here.  If an option is
# not set in an item, the setting of its parent's option is used.  All
# of these options must be set to reasonable default values in
# OOFRootMenu.__init__().

_allowed_options = [
    'gui_only',                         # item appears only in GUI menus
    'cli_only',                         # item appears only in CLI menus
    'no_log',                           # calls are not logged
    'disabled',                         # command and/or submenus are turned off
    'no_doc',                           # API dump ignores this menu item
    'pre_hook',                         # Function called before menu item
    'post_hook'                         # Function called after menu item
    ]

######################################

## These are available types of threadability that OOFMenuItem has. ##

UNTHREADABLE = "Unthreadable" ## never threadable
THREADABLE = "Threadable" ## always threadable (default)
THREADABLE_GUI = "Threadable GUI" ## only threadable in graphics mode
THREADABLE_TEXT = "Threadable Text" ## only threadable in textmode
PARALLEL_UNTHREADABLE = "Parallel" ## parallel type menu item that runs on the same thread
PARALLEL_THREADABLE = "Parallel Threadable" ## parallel type menu item that runs on a separate thread

_threadability_options = [
UNTHREADABLE,
THREADABLE,
THREADABLE_GUI,
THREADABLE_TEXT,
PARALLEL_UNTHREADABLE,
PARALLEL_THREADABLE
]

######################################
    
class OOFRadioMenuGroup:
    # Here, this class is just a list of weak references to radio menu
    # items.  (They're weak references because the menu items
    # themselves refer to this group, and we don't want circular
    # references.)  But the gfxmenu code adds attributes to the
    # OOFRadioMenuGroup when the gui is constructed.
    def __init__(self):
        self.items = []
    def add(self, item):
        self.items.append(weakref.ref(item))
    def __len__(self):
        return len(self.items)
    def __getitem__(self, idx):
        return self.items[idx]()

#################################

class OOFMenuItem:
    def __init__(self, name,
                 callback=None,         # callback for CLI 
                 gui_callback=None,     # callback for GUI (defaults to CLI cb)
                 accel=None,            # GUI accelerator
                 secret=0,              # not listed in parent
                 ellipsis=0,            # append '...' to displayed names?
                 help_menu=0,           # is this a right justified help menu?
                 help=None,             # string describing command
                 discussion=None,       # for manual, in docbook xml
                 threadable = THREADABLE,     # MenuItem is threaded if it receives a ThreadType object different from UNTHREADABLE
                 params=[],             # list of Parameter args for callback
                 ordering=0,
                 **kwargs):             # additional options
        # Check for legal name
        if name:
            if not (name[0].isalpha() or name[0] == '_'):
                raise NameError("Illegal name for menu item " + name)
            for char in name[1:]:
                if not (char.isalpha() or char.isdigit() or char == '_'):
                    raise NameError("Illegal name for menu item: " + name)
        
        self.name = name
        self.parent = None              # reset in OOFMenu.add_item()
        self.accel = accel              # keyboard accelerator
        self.secret= secret
        self.ellipsis = ellipsis
        self.options = {}
        self.callback = callback
        self.help_menu = help_menu
        self.gui_callback = gui_callback
        self.helpstr = help
        self.discussion = discussion
        self.ordering = ordering
        self.threadable = UNTHREADABLE
        global _threadability_options
        if threadable in _threadability_options: # check validity
            self.threadable = threadable ## assign threadable type
        else:
            raise AttributeError("threadability option not valid")
        self.params = params            # arguments for callback
        self.data = None                # optional user data
        # self.items is a list of menu items.  It has to be a list,
        # not a dictionary, so that the items can be ordered correctly
        # when displayed.
        self.items = []
        self.radiogroups = []

        # bar_name is the string representing the menu item in
        # progress bars.  It's set when the menu item is called.
        self.bar_name = None
        
        
        # additional options
        for opt,val in kwargs.items():
            if opt in _allowed_options: # check validity
                self.setOption(opt, val)
            else:
                raise AttributeError('Unknown OOFMenu option: ' + opt)

    def clone(self,name=None, help=None, discussion=None):
        # Clone menu item, but NOT its submenus.  self.params may be a
        # ParameterGroup or a list, so we have to check the type when
        # copying.  Unfortunately, list and ParameterGroup have
        # different constructor arguments.  (Changing ParameterGroup's
        # constructor arguments just to make this code a bit prettier
        # isn't worthwhile.)
        params = [p.clone() for p in self.params]
        if isinstance(self.params, parameter.ParameterGroup):
            params = parameter.ParameterGroup(*params)
        newitem = self.__class__(name=name or self.name,
                                 callback=self.callback,
                                 gui_callback=self.gui_callback,
                                 accel=self.accel,
                                 secret=self.secret,
                                 ellipsis=self.ellipsis,
                                 help_menu=self.help_menu,
                                 help=help or self.helpstr,
                                 discussion=discussion or self.discussion,
                                 threadable = self.threadable,
                                 params=params)
        newitem.options.update(self.options)
        return newitem
                              
    def addItem(self, item):            # add a menu item to this menu
        for i in range(len(self.items)): # see if new item replaces an old one
            if item.name == self.items[i].name:
                self.items[i] = item    # replace an old item
                break
        else:

            # Insert the new item just before an item with a larger
            # ordering number, but not after a help_menu.
            if item.help_menu:
                self.items.append(item)
            else:
                for olditem in self.items:
                    if olditem.help_menu or olditem.ordering > item.ordering:
                        pos = self.items.index(olditem)
                        self.items.insert(pos, item)
                        break
                else:
                    self.items.append(item)
        item.parent = self
        return item

    def getItem(self, name):
        for item in self.items:
            if item.name == name:
                return item
        raise KeyError("%s Menu has no item %s" % (self.name, name))

    def removeItem(self, name):
        for i in range(len(self.items)):
            if self.items[i].name == name:
                ## Don't set parent to None!  The menu item may still
                ## be running, and it may need to call getOption,
                ## which needs to know the parent.
                ## self.items[i].parent = None
                del self.items[i]
                return
        raise KeyError("%s Menu has no item %s" % (self.name, name))

    def add_gui_callback(self, callback):
        self.gui_callback = callback

    def getOption(self, option):
        try:
            return self.options[option]
        except KeyError:
            if self.parent is None:
                return None
            return self.parent.getOption(option)

    def setOption(self, option, value):
        self.options[option] = value

    def removeOption(self, option):
        del self.options[option]

    def visible_cli(self):
        return not (self.secret or self.getOption('gui_only'))

    def visible_gui(self):
        return not (self.secret or self.getOption('cli_only'))

    def gui_order(self):
        # Position of this menu item in a gui listing of its parent's items.
        if self.parent is not None:
            order = 0
            for item in self.parent.items:
                if item is self:
                    return order
                if item.visible_gui():
                    order += 1
        else:
            return 0
                    

    def clearMenu(self):
        self.callback = None
        self.gui_callback = None
        self.params = []
        self.data = None
        self.clearSubMenu()

    def clearSubMenu(self):
        for item in self.items:
##            item.parent = None  ## see removeItem
            item.clearMenu()
        self.items = []

    def disconnectSubMenu(self):
        for item in self.items:
            item.parent = None
        self.items = []
    
    def path(self):
        if self.parent is None:
            return self.name
        return self.parent.path() + "." + self.name

    def descendPath(self, path):
        if type(path) == types.StringType:
            return self.descendPath(string.split(path, '.'))
        if not path:
            return self
        return self.getItem(path[0]).descendPath(path[1:])

    def root(self):                     # return root of menu hierarchy
        if self.parent is None:
            return self
        return self.parent.root()

    def makeGroup(self):
        group = OOFRadioMenuGroup()
        self.radiogroups.append(group)
        return group

    def nargs(self):
        return len(self.params)

    def get_arg(self, name):
        for arg in self.params:
            if arg.name == name:
                return arg
        raise TypeError(
            "OOFMenuItem %s got an unexpected keyword argument '%s'"
            % (self.path(), name))

    def replace_args(self, params):
        self.params = params


    # disable() and enable() are called when it's necessary to
    # explicitly disable or enable a menu item.  Menu items are
    # *automatically* disabled if they don't have either a callback or
    # submenus.  The 'disabled' option only reflects the explicit
    # state, but the 'enabled()' function takes into account the
    # existance of callbacks and submenus.
    
    def disable(self):
        self.options['disabled'] = 1

    def enable(self):
        try:
            del self.options['disabled']
        except KeyError:
            pass

    def enabled(self):
        return (not self.getOption('disabled')) and \
               (self.items or self.callback or self.gui_callback)
    
    ################################
    #
    # Invocation functions.
        
    def __call__(self, **kwargs):
        """
        Execute the command as if it were called by the CLI.  This
        function is called directly by the CLI, and directly by the
        GUI if the command takes no arguments.  If the command takes
        arguments, a different GUI callback will construct the
        arguments and then call this function.
        """

        if self.callback is not None:
            # Set self.args from kwargs
            # Because parameters can interact, it's important to ensure
            # that all of the parameters have been set before any of their
            # values are extracted into the argdict.  That's why there are
            # two independent loops here.
            for argname,val in kwargs.items(): # set args provided as kwargs
                arg = self.get_arg(argname)
                arg.value = val             # might raise ParameterMismatch
            # Construct kwargs for function call
            argdict = {}
            for arg in self.params:
                if arg.name in kwargs:
                    argdict[arg.name] = arg.value
                else:
                    argdict[arg.name] = None # unset

            self.callWithArgdict(argdict)


    
    def callWithDefaults(self, **kwargs):
        argdict = {}
        for name,value in kwargs.items():
            argdict[name] = value
            
        # Because parameters can interact, it's important to ensure
        # that all of the parameters have been set before any of their
        # values are extracted into the argdict.  That's why there are
        # two independent loops here.
        for p in self.params:
            if p.name in argdict:
                p.value = argdict[p.name]
        for p in self.params:
            if not p.name in argdict:
                argdict[p.name] = p.value

        self.callWithArgdict(argdict)



    def callParamList(self, plist):
        """
        Alternative way of invoking an OOFMenuItem by passing in a list of
        Parameters.  Used in API, not interactively.
        """
        pdict = {}
        for p in plist:
            pdict[p.name] = p.value
        self.callWithArgdict(pdict)
        # return apply(self, (), pdict)

        
    # Common "tail" function for the previous three ways of invoking the
    # menu item.  This construction prevents duplication of effort,
    # and also prevents the menu item from writing a value into a
    # parameter unnecessarily.
    def callWithArgdict(self, argdict):
        # List arguments, taking values from the argdict, but
        # displaying them in the order in which they occur in the
        # self.params list.
        arglist = ["%s=%s" % (name, `argdict[name]`)
                   for name in [p.name for p in self.params]
                   if argdict[name] is not None]
        self.log(self.path() +'(' + string.join(arglist, ', ') + ')')
        self.bar_name = self.path() +'(' + string.join(arglist, ', ') + ')'

        self.hireWorker(argdict=argdict)

##    def callSecretly(self, **kwargs):   # Doesn't log. 
##        self.bar_name = self.path()
##        self.hireWorker(argdict=kwargs)

    def hireWorker(self, argtuple=(), argdict={}):
        # Create and start the appropriate kind of Worker to perform
        # the menu item.  If menuItem is threadable create a threaded
        # Worker and launch the thread.  There are different kinds of
        # threaded Workers.  getThreadedWorker returns the appropriate
        # one.

        # It is tempting to put "if parallel_enable.enabled():..." but
        # threadable can carry more options than just
        # PARALLEL_THREADABLE and PARALLEL_UNTHREADABLE.
        if (self.threadable is PARALLEL_UNTHREADABLE and 
            parallel_enable.enabled()):
            workerclass = worker.ParallelWorker
        elif (self.threadable is PARALLEL_THREADABLE and
              parallel_enable.enabled()):
            if thread_enable.enabled():
                workerclass = worker.getThreadedParallelWorker
            else:
                workerclass = worker.ParallelWorker
        elif (self.threadable is UNTHREADABLE or
              not thread_enable.enabled() or
              (self.threadable is THREADABLE_GUI and not guitop.top()) or
              (self.threadable is THREADABLE_TEXT and guitop.top())
              ):
            workerclass = worker.NonThreadedWorker
        else:
            # worker.getThreadedWorker returns a
            # TextThreadedWorker in text mode, and either a
            # ThreadedWorker of GUIThreadedWorkerBlock in GUI
            # mode.
            workerclass = worker.getThreadedWorker
        the_worker = workerclass(self, argtuple, argdict)
        garbage.collect()
        # Launch the thread (and wait for it to finish if in text
        # mode).
        the_worker.start()
           
    #####################################

    # precall and postcall are called by the Worker before and after
    # the menuitem's callback.  They provide a way of performing some
    # external bookkeeping commands before and after the menu command.

    def precall(self):
        fn = self.getOption('pre_hook')
        if fn:
            fn(self)

    def postcall(self, successful):
        # successful==True means that the menuitem callback finished
        # without raising an exception.
        fn = self.getOption('post_hook')
        if fn:
            fn(self, successful)

    ####################################

    
    def log(self, strng):
        if self.getOption('no_log') != 1:
            root = self.root()
            if root is self:
                raise "OOFMenuItem.log: No root menu?"
            root.log(strng)

    # Enable menu items to be invoked by, eg, menu.submenu.subsubmenu.item().
    def __getattr__(self, attr):
        for item in self.items:
            if item.name == attr:
                return item
        raise AttributeError('Menu %s has no entry %s!' % (self.path(), attr))

    def __getitem__(self, idx):
        return self.items[idx]
    def __len__(self):
        return len(self.items)
    def __repr__(self):
        return string.join([self.name+":"] + \
                           [item.name for item in self.items
                            if item.visible_cli()],
                           ' ')
    def help(self):
        return self.helpstr

    def dump(self, prefix=''):
        repr = prefix + self.name + '\n'
        for item in self.items:
            repr += item.dump(prefix + '  ')
        return repr

    # Return the name of the callback function and the name of its module.
    def getcallbackname(self):
        try:
            im_self_data = self.callback.im_self
        except AttributeError:
            funcname = ""
        else:
            funcname = im_self_data.__class__.__name__ + "."
        funcname += self.callback.__name__
        return (funcname, self.callback.func_globals['__name__'])

    # Apply "func" to this menu item and its subtree.
    def apply(self, func, *args, **kwargs):
        func(self, *args, **kwargs)
        for item in self.items:
            item.apply(func, *args, **kwargs)


    #########

    # Routines for creating the documentation.
    
    def xmlParams(self, file):          # make a list of parameters
        from ooflib.common.IO import xmlmenudump # delayed to avoid import loops
        if self.params:
            print >> file, "<listitem><para> Parameters:"
            print >> file, " <variablelist>"
            for param in self.params:
                xmlmenudump.process_param(param)
                print >> file, "  <varlistentry>"
                print >> file, "    <term><varname>%s</varname></term>" \
                      % param.name
                print >> file, "      <listitem>"
                if param.tip is not parameter.emptyTipString:
                    tip = param.tip or "MISSING TIP STRING"
                else:
                    tip =""
                print >> file, "       <simpara>%s <emphasis>Type</emphasis>: %s</simpara>" \
                      % (tip, param.valueDesc())
                print >> file, "      </listitem>"
                print >> file, "  </varlistentry>" 
            print >> file, " </variablelist>" # list of params
            print >> file, "</para></listitem>"
            
    def xmlSynopsis(self, file):        # make the Synopsis section
        print >> file, " <refsynopsisdiv><simpara>"
        args = string.join(['<varname>%s</varname>' % p.name
                            for p in self.params], ',')
        print >> file, "  <command>%s</command>(%s)" % (self.path(), args)
        print >> file, " </simpara></refsynopsisdiv>"

    
        
##################################
    
class CheckOOFMenuItem(OOFMenuItem):
    # CheckOOFMenuItems have a value which is either 0 or 1.
    def __init__(self, name, value, *args, **kwargs):
        kwargs['params'] = ()           # can have no arguments except 'value'
        kwargs['gui_callback'] = None
        OOFMenuItem.__init__(*((self, name)+args), **kwargs)
        self.value = value
    def __call__(self, *args):
        if len(args)==1:
            self.value = args[0]
        else:
            self.value = not self.value
        self.log('%s(%d)' % (self.path(), self.value))
        if self.callback:
            self.hireWorker(argtuple=(self.value,))

    def xmlSynopsis(self, file):
        print >> file, "<refsynopsisdiv><simpara>"
        print >> file, " <command>%s</command>(<varname>boolean</varname>)" \
              % self.path()
        print >> file, "</simpara></refsynopsisdiv>"        

    def xmlParams(self, file):
        print >> file, "<listitem><para>Parameters:"
        print >> file, " <variablelist>"
        print >> file, "  <varlistentry>"
        print >> file, "   <term><varname>boolean</varname></term>"
        print >> file, "   <listitem><simpara>"
        print >> file, "     A boolean value, <userinput>0</userinput> (false) or <userinput>1</userinput> (true). This is <emphasis>not</emphasis> a keyword parameter (just enter '0' or '1', not 'boolean=1')."
        print >> file, "   </simpara></listitem>"
        print >> file, "  </varlistentry>"
        print >> file, " </variablelist>"
        print >> file, "</para></listitem>"
        

##################################

class RadioOOFMenuItem(CheckOOFMenuItem):
    # RadioOOFMenuItems are CheckOOFMenuItems that live in groups.
    # Exactly one item in each group has the value 1, all the rest
    # have the value 0.  Calling an item turns it on and turns all the
    # others in the group off.
    def __init__(self, name, group=None, *args, **kwargs):
        self.group = group
        self.group.add(self)
        CheckOOFMenuItem.__init__(*((self, name)+args), **kwargs)
    def clone(self, group):
        newitem = OOFMenuItem.clone(self)
        newitem.group = group
        newitem.group.add(newitem)
        return newitem
    def __call__(self):
        self.value = 1
        self.log(self.path() + '()')
        # We've been turned on, so make sure everybody else is turned
        # off.  This explains why RadioOOFMenuItems haven't succeeded
        # as a species.
        for item in self.group:
            if not item is self:
                if item.value:
                    item.value = 0
                    item.callback(item, 0)
        self.callback(self, 1)

##################################

debugcounter = 0
        
class OOFRootMenu(OOFMenuItem):
    def __init__(self, *args, **kwargs):
        OOFMenuItem.__init__(*((self,)+args), **kwargs)
        if not 'cli_only' in self.options:
            self.options['cli_only'] = 0
        if not 'gui_only' in self.options:
            self.options['gui_only'] = 0
        if not 'no_log' in self.options:
            self.options['no_log'] = 0
##        if not 'disabled' in self.options:
##            self.options['disabled'] = 0
        if not 'help_menu' in self.options:
            self.options['help_menu'] = 0
        self.logbook = []
        self.loggers = []               # additional logging functions
        self._loghalted = 0
        self._logchanged = 0
        self.loglock = lock.SLock()
        self.quiet = 0
    def root(self):
        return self
    def log(self, strng):
        self.loglock.acquire()
        try:
            if debug.debug() and not self.quiet:
                global debugcounter
                if len(strng) < 1000:
                    dstr = strng
                else:
                    dstr = strng[:80] + '...' + strng[-20:]
                debug.msg("====%04d===="%debugcounter, dstr)
                #import pdb; pdb.set_trace()
                debugcounter += 1
            if self._loghalted == 0:
                self._logchanged = 1
                self.logbook.append(strng+'\n')
                for logger in self.loggers:
                    logger(strng)
        finally:
            self.loglock.release()
    def saveLog(self, file):
        self.loglock.acquire()
        try:
            print >> file, "# OOF version", oofversion.version
            file.writelines(self.logbook)
            self._logchanged = 0
        finally:
            self.loglock.release()
    def clearLog(self):
        self.loglock.acquire()
        try:
            self.logbook = []
            self._logchanged = 0
        finally:
            self.loglock.release()
    def logChanged(self):
        return self._logchanged
    def addLogger(self, logger):
        self.loggers.append(logger)
    def removeLogger(self, logger):
        self.loggers.remove(logger)
    def haltLog(self):
        self.loglock.acquire()
        try:
            self._loghalted += 1
        finally:
            self.loglock.release()
    def resumeLog(self):
        self.loglock.acquire()
        try:
            if self._loghalted >= 1:
                self._loghalted -= 1
        finally:
            self.loglock.release()
    def quietmode(self, q):
        self.quiet = q

#################################

class MenuLogger:
    def __init__(self, outputfn, prefix=""):
        self.outputfn = outputfn
        self.prefix = prefix
    def __call__(self, msg):
        self.outputfn(self.prefix + msg)
