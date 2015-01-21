# -*- python -*-
# $RCSfile: tooltips.py,v $
# $Revision: 1.1.14.4 $
# $Author: langer $
# $Date: 2013/11/22 22:02:35 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## This file defines a function that lets us use the new gtk.Tooltip
## API when it's available.  As of gtk+2 2.20 or so, using the old API
## generates tons of annoying deprecation warnings, but some Linux
## distros (RH, Centos, ...)  don't have the new API yet.

import gtk

if gtk.gtk_version < (2, 12, 0):
    tooltips = gtk.Tooltips()
    def set_tooltip_text(widget, text):
        tooltips.set_tip(widget, text)
    def enable_tooltips():
        tooltips.enable()
    def disable_tooltips():
        tooldips.disable()

else:
    def set_tooltip_text(widget, text):
        widget.set_tooltip_text(text)
    def enable_tooltips():
        pass
    def disable_tooltips():
        pass
