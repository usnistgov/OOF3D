# -*- python -*-
# $RCSfile: fixedwidthtext.py,v $
# $Revision: 1.1.10.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO.GUI import mainmenuGUI
import gtk
import pango

class FixedWidthTextView(gtk.TextView):
    def __init__(self, *args, **kwargs):
        gtk.TextView.__init__(self, *args, **kwargs)
        self.sbcb = switchboard.requestCallbackMain('change fixed font',
                                                    self.changeFont)
        self.connect('destroy', self.destroyCB)
        self.changeFont(mainmenuGUI.getFixedFont())

    def changeFont(self, fontname):
        debug.mainthreadTest()
        font_desc = pango.FontDescription(fontname)
        if font_desc:
            self.modify_font(font_desc)

    def destroyCB(self, *args):
        switchboard.removeCallback(self.sbcb)
        
    def get_text(self):
        tbuf = self.get_buffer()
        return tbuf.get_text(tbuf.get_start_iter(), tbuf.get_end_iter())
