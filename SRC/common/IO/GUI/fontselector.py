# -*- python -*-
# $RCSfile: fontselector.py,v $
# $Revision: 1.5.18.3 $
# $Author: langer $
# $Date: 2014/08/01 17:55:31 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
import gtk

# TODO MAYBE: Add logging for FontSelection.  This is difficult
# because different fonts will be installed on different systems.

class FontSelector:
    OK = 1
    CANCEL = 2
    def __init__(self, parent=None):
        debug.mainthreadTest()
        self.dialog = gtklogger.Dialog(title="OOF2 Font Selector",
                                       parent=parent)
        gtklogger.newTopLevelWidget(self.dialog, "FontSelector")
        self.dialog.add_button(gtk.STOCK_OK, self.OK)
        self.dialog.add_button(gtk.STOCK_CANCEL, self.CANCEL)
        self.fontselector = gtk.FontSelection()
        self.dialog.vbox.pack_start(self.fontselector, expand=1, fill=1)
    def run(self):
        debug.mainthreadTest()
        self.dialog.show_all()
        return self.dialog.run()
    def close(self):
        debug.mainthreadTest()
        self.dialog.destroy()
    def hide(self):
        debug.mainthreadTest()
        self.dialog.hide()
    def get_font_name(self):
        debug.mainthreadTest()
        return self.fontselector.get_font_name()

_fsdialog = None

def getFontName(parentwindow=None):
    global _fsdialog
    if not _fsdialog:
        _fsdialog = FontSelector(parentwindow)
    result = _fsdialog.run()
    if result in (FontSelector.CANCEL, gtk.RESPONSE_DELETE_EVENT,
                  gtk.RESPONSE_NONE):
        _fsdialog.hide()
        return None
    fname = _fsdialog.get_font_name()
    _fsdialog.hide()
    return fname
