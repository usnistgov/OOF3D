# -*- python -*-
# $RCSfile: console.py,v $
# $Revision: 1.37.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# A window for interactively querying OOF while it's running
# in GUI mode.

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gfxmenu
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import mainmenuGUI
from ooflib.common.IO.GUI import oof_mainiteration
from ooflib.common.IO.GUI import quit
from ooflib.common.IO.GUI import subWindow
import code, sys, string
import gtk
import pango

tabspacing = 4

# Preprocessing for some string stuff.
ordinary_printable = string.digits + string.letters + string.punctuation + " "
KEYVAL_UP = gtk.gdk.keyval_from_name('Up')
KEYVAL_DOWN = gtk.gdk.keyval_from_name('Down')
KEYVAL_LEFT = gtk.gdk.keyval_from_name('Left')
KEYVAL_RIGHT = gtk.gdk.keyval_from_name('Right')
KEYVAL_BACKSPACE = gtk.gdk.keyval_from_name('BackSpace')
KEYVAL_TAB = gtk.gdk.keyval_from_name('Tab')


# Build the file menu outside of the instance, so it doesn't
# have to be managed when instances come and go.

current_console = None

# Main-thread menu callback.
def _close_console(menuitem):
    global current_console
    debug.mainthreadTest()
    current_console.gtk.destroy()
    
_console_menu = oofmenu.OOFMenuItem("Console", secret=1, gui_only=1, no_log=1)
mainmenu.OOF.addItem(_console_menu)

_console_file_menu = oofmenu.OOFMenuItem('File', gui_only=1, no_log=1)
_console_menu.addItem(_console_file_menu)

_console_file_menu.addItem(oofmenu.OOFMenuItem(
    'Close', help="Close the console window.",
    callback=_close_console, no_log=1, gui_only=1, accel='w',
    threadable=oofmenu.UNTHREADABLE))

_console_file_menu.addItem(oofmenu.OOFMenuItem(
    'Quit', help="Exit the OOF application.",
    threadable=oofmenu.UNTHREADABLE,
    callback=quit.queryQuit, no_log=1, gui_only=1, accel='q'))


# GUIConsole does not have a conventional "interact" function, but
# instead is event-driven by the GUI.
class GUIConsole(code.InteractiveConsole, subWindow.SubWindow):
    def __init__(self, locals):
        global _console_menu
        debug.mainthreadTest()
        code.InteractiveConsole.__init__(self, locals=locals)
        subWindow.SubWindow.__init__(
            self, title="%s Python Console"%subWindow.oofname(),
            menu=_console_menu)
                                    
        self.history_list = []
        self.history_pos = 0
        self.raw = None
        self.raw_result = None

        frame = gtk.Frame()
        frame.set_border_width(2)
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.mainbox.pack_start(frame, expand=1, fill=1)
    
        scroll = gtk.ScrolledWindow()
        frame.add(scroll)
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.text = fixedwidthtext.FixedWidthTextView()
        scroll.add(self.text)
        self.text.set_wrap_mode(gtk.WRAP_WORD)
        self.text.set_cursor_visible(0) # *mouse* cursor is invisible
        self.gtk.set_default_size(90*gtkutils.widgetCharSize(self.text), -1)

        self.bfr = self.text.get_buffer()
        # beginmark stays at the beginning of the last line of text
        self.beginmark = self.bfr.create_mark("beginmark",
                                              self.bfr.get_end_iter(),
                                              left_gravity=True)
        self.cursormark = self.bfr.create_mark("cursor",
                                               self.bfr.get_end_iter(),
                                               left_gravity=False)

        # The rvTag is used to show the text cursor in reverse video
        textattrs = self.text.get_default_attributes()
        self.rvTag = self.bfr.create_tag("reverse",
                                         background_gdk= textattrs.fg_color,
                                         foreground_gdk=textattrs.bg_color,
                                         #family="Monospace"
                                         )
        self.editableTag = self.bfr.create_tag("editable",
                                               editable=True,
                                               #family="Monospace"
                                               )
        self.uneditableTag = self.bfr.create_tag("uneditable",
                                                 editable=False,
                                                 #family="Monospace"
                                                 )
        
        self.text.connect("key-press-event", self.key_press)
        self.gtk.connect("destroy", self.local_destroy)

        # File emulation attributes.
        self.old_stdout = sys.stdout
        sys.stdout = self
        self.softspace = 0
        self.mode="a"
        #
        try:
            self.prompt1=sys.ps1
        except AttributeError:
            self.prompt1=">>> "
        try:
            self.prompt2=sys.ps2
        except AttributeError:
            self.prompt2="... "

        # Do the banner manually, since we don't have "interact".  The
        # extra space at the end is where the cursor will be drawn.
        self.textout(subWindow.oofname() + " Console:\n" + self.prompt1 + ' ')
        self.gtk.show_all()

    def grab_focus(self):
        debug.mainthreadTest()
        self.text.grab_focus()
    
    # Manually process keystrokes.  Wotta pain.  For ascii printable,
    # just print.  For cursor-up or cursor-down, do the history.
    # Does not currently accept text via paste (as in cut-and-)
    def key_press(self, gtkobj, event):
##        debug.fmsg('str:', event.string,
##                   'keyval:', gtk.gdk.keyval_name(event.keyval))
        debug.mainthreadTest()
        global ordinary_printable
        if event.string == "":
            if event.keyval == KEYVAL_UP:
                # replace the current line with the previous history line
                self.text.emit_stop_by_name("key_press_event")
                if self.history_pos != len(self.history_list):
                    self.history_pos += 1
                    line = self.history_list[-self.history_pos]
                    self.replace_line(line)
            elif event.keyval == KEYVAL_DOWN:
                # replace the current line with the next history line
                self.text.emit_stop_by_name("key_press_event")
                if self.history_pos != 0:
                    self.history_pos -= 1
                    if self.history_pos==0:
                        self.cursor_pos = 0
                        self.replace_line("")
                    else:
                        line = self.history_list[-self.history_pos]
                        self.cursor_pos = len(line)
                        self.replace_line(line)
            elif event.keyval == KEYVAL_LEFT:
                # move the cursor left, without changing the text
                self.text.emit_stop_by_name("key_press_event")
                iter = self.bfr.get_iter_at_mark(self.cursormark)
                if iter.compare(self.bfr.get_iter_at_mark(self.beginmark)) == 1:
                    iter.backward_char()
                    self.moveCursor(iter)
            elif event.keyval == KEYVAL_RIGHT:
                # move the cursor right, without changing the text
                self.text.emit_stop_by_name("key_press_event")
                iter = self.bfr.get_iter_at_mark(self.cursormark)
                if iter.compare(self.nextToLast()) == -1:
                    iter.forward_char()
                    self.moveCursor(iter)
            elif event.keyval == KEYVAL_BACKSPACE:
                self.backspace()
            elif event.keyval == KEYVAL_TAB:
                # Insert spaces so that the column number mod tabspacing is 0.
                self.text.emit_stop_by_name("key_press_event")
                iter = self.bfr.get_iter_at_mark(self.cursormark)
                start = self.bfr.get_iter_at_mark(self.beginmark)
                colno = iter.get_offset() - start.get_offset()
                pad = " " * (tabspacing - colno%tabspacing)
                self.bfr.insert_with_tags(iter, pad, self.editableTag)
            else:                       # we don't understand this key press
                return False            # key press not processed
            
        else:                           # event.string != ""
            if event.string in ordinary_printable:
                iter = self.bfr.get_iter_at_mark(self.cursormark)
                self.bfr.insert_with_tags(iter, event.string, self.editableTag)

            else:                       # special characters

                # new line or carriage return
                if event.string=='\r' or event.string=='\n':
                    self.bfr.remove_tag(
                        self.editableTag,
                        self.bfr.get_iter_at_mark(self.beginmark),
                        self.bfr.get_end_iter())
                    txt = self.bfr.get_text(
                        self.bfr.get_iter_at_mark(self.beginmark),
                        self.nextToLast())
                    if txt:
                        self.history_list.append(txt)
                    self.history_pos=0
                    # Put a newline on the screen, and reset
                    # beginmark.  Resetting beginmark means that the
                    # text that's just been retrieved won't be
                    # retrieved again.
                    self.textout('\n')
                    # In raw mode, just park the accumulated string
                    # and mark yourself as done.  Caller
                    # will handle the return.
                    if self.raw:
                        self.raw = None
                        self.raw_result = txt
                    # Otherwise, push the accumulated string to the
                    # interpreter.
                    else:
                        more = self.push(txt)
                        if more:
                            self.textout(self.prompt2)
                        else:
                            self.textout(self.prompt1)

                # ctrl-H and ASCII delete.
                elif event.string=="\x08" or event.string=='\x7f':
                    self.backspace()
                elif event.string=='\x0b': # control K kills to end of line
                    self.bfr.delete(self.bfr.get_iter_at_mark(self.cursormark),
                                    self.nextToLast())
                elif event.string=='\x01': # control A goes to beginning of line
                    self.moveCursor(self.bfr.get_iter_at_mark(self.beginmark))
                elif event.string=='\x05': # control E goes to end of line
                    self.moveCursor(self.nextToLast())
                elif event.string=='\x04': # control D kills char at cursor
                    iter = self.bfr.get_iter_at_mark(self.cursormark)
                    # The blank at the end of the line must be preserved.
                    if iter.compare(self.nextToLast()) == -1:
                        next = iter.copy()
                        next.forward_char()
                        self.bfr.delete(iter, next)
                        self.moveCursor(iter)
##                # Allow ctrl-D out of interpreter mode.  Disallow for
##                # raw mode, because otherwise the wrapping function
##                # will never return.
##                elif event.string=="\x04":
##                    if not self.raw:
##                        self.gtk.destroy()
                else:                   # we don't understand this key press
                    return False        # key press not processed
        self.autoscroll()
        return True                     # key press was processed

    def backspace(self):
        iter = self.bfr.get_iter_at_mark(self.cursormark)
        prev = iter.copy()
        prev.backward_char()
        if iter.compare(self.bfr.get_iter_at_mark(self.beginmark)) == 1:
            self.bfr.delete(prev, iter)

    def replace_line(self, newtext):
        debug.mainthreadTest()
        beginiter = self.bfr.get_iter_at_mark(self.beginmark)
        self.bfr.delete(beginiter, self.bfr.get_end_iter())
        # iterators are invalidated by deletion, so get beginiter again
        beginiter = self.bfr.get_iter_at_mark(self.beginmark)
        self.bfr.insert_with_tags(beginiter, newtext, self.editableTag)
        # put an empty space for the cursor at the end
        self.bfr.insert_with_tags(self.bfr.get_end_iter(), ' ',
                                  self.rvTag, self.editableTag)
        self.bfr.move_mark(self.cursormark, self.nextToLast())
        
    # Reporter messages generated by commands issued in the Console
    # can come from the wrong thread, so make sure we're in the main
    # thread before writing.
    def textout(self, string):
        mainthread.runBlock(self.textout_thread, (string,))
    def textout_thread(self, string):
        # Insert just *before* the final ' ' in the buffer.  Keep the
        # ' ' so the cursor can be drawn at the end of the line.
        self.bfr.insert_with_tags(self.nextToLast(), string, self.uneditableTag)
        self.moveCursor(self.nextToLast())
        self.bfr.move_mark(self.beginmark, self.nextToLast())
        self.autoscroll()

    def moveCursor(self, iter):
        self.bfr.remove_tag(self.rvTag, self.bfr.get_start_iter(),
                               self.bfr.get_end_iter())
        next = iter.copy()
        next.forward_char()
        self.bfr.apply_tag(self.rvTag, iter, next)
        self.bfr.move_mark(self.cursormark, iter)

    def nextToLast(self):
        iter = self.bfr.get_end_iter()
        iter.backward_char()
        return iter

    def autoscroll(self):
        mark = self.bfr.create_mark(None, self.bfr.get_end_iter())
        self.text.scroll_mark_onscreen(mark)
        self.bfr.delete_mark(mark)

    # Clean up output mechanisms that were hijacked before the init.
    def local_destroy(self, gtkobj):
        global current_console
        sys.stdout = self.old_stdout
        current_console = None

    # File-like functionality, allowing the console to stand
    # in for stdout.  Lots of no-ops.
    def close(self):
        pass

    def flush(self):
        pass

    def read(self, size=0):
        raise EOFError

    def readline(self, size=0):
        raise EOFError
    
    def seek(self, offset, whence=0):
        pass

    def tell(self):
        debug.mainthreadTest()
        return self.gtk.get_length()

    def write(self, data):
        self.textout(data)

    def writelines(self, lines):
        for l in lines:
            self.write(l)

    # Having isatty() return False prevents text progress bars from
    # appearing in the console window.  I'm not sure why they'd ever
    # be drawn there, but they tried to at one point, somehow.
    def isatty(self):
        return False
    
def make_console(menuitem):
    global current_console
    if current_console:
        current_console.raise_window()
    else:
        current_console = GUIConsole(sys.modules['__main__'].__dict__)
    current_console.grab_focus()

mainmenu.OOF.Windows.Console.add_gui_callback(make_console)

# Operate the console in "raw" mode -- writes out a prompt, then
# returns whatever was typed from then until a new line was
# encountered. 
def raw_input(prompt):
    global current_console
    if current_console:
        current_console.raw=1
        current_console.write(prompt)
        # Newline on input will kick the console out of "raw" mode,
        # that's when we're done.
        while current_console.raw:
            # gtk.mainiteration()
            oof_mainiteration.mainiteration()
        result = current_console.raw_result
        current_console.raw_result=None
        return result
    else:
        return sys.modules['__main__'].__builtins__.raw_input(prompt)


# Over-ride the "raw_input" function as seen from the
# OOF evaluation namespace.
utils.OOFdefine('raw_input', raw_input)
