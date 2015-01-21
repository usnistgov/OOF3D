# -*- python -*-
# $RCSfile: gtkutils.py,v $
# $Revision: 1.18.10.2 $
# $Author: langer $
# $Date: 2013/11/08 20:43:02 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
import gtk
import pango


## NOTE: The following function is commented out, because it doesn't
## work well.  There's no way in gtk2 to set the size of a widget
## except to call set_size_request, which sets the widget's minimum
## size.  This means that a window created with copyWidgetSizes won't
## be shrinkable.

# Make widget dest have the same size as widget source.  Since widgets
# get their sizes from their children, recursively set the children's
# sizes too.  This only works if both source and dest have the same
# structure, of course.  It's meant to be used when cloning windows.
# This doesn't work completely correctly.  Perhaps the allocation is
# not the right thing to be copying?

##def copyWidgetSizes(source, dest):
##    debug.mainthreadTest()
##    bbox = source.get_allocation()
##    dest.set_size_request(bbox.width, bbox.height)
##    if isinstance(source, gtk.Container) and isinstance(dest, gtk.Container):
##        for s,d in zip(source.get_children(), dest.get_children()):
##            copyWidgetSizes(s, d)

## For figuring out why importing the gui changes the random numbers.
## See comment in widgetFontSizes.
# _first = True
# def rdebug():
#     from ooflib.SWIG.common import crandom
#     import random
#     global _first
#     if _first:
#         random.seed(17)
#         crandom.rndmseed(17)
#         _first = False


# Return the char and digit sizes for a widget's font.

def widgetFontSizes(widget):
    debug.mainthreadTest()
    fontdesc = widget.get_style().font_desc
    fontcontext = widget.create_pango_context()

    ## This call to load_font appears to use random().  Calling rdebug
    ## after load_font causes a subsequent call to
    ## OOF.Help.Debug.Random to generate different numbers than it
    ## does if rdebug is called before load_font.  The values obtained
    ## by calling rdebug after load_font are the same as the ones
    ## obtained in text mode.
    #rdebug() 
    font = fontcontext.load_font(fontdesc)
    #rdebug() 

    #This one doesn't work on cygwin
    #fontmetrics = font.get_metrics(None)
    fontmetrics = font.get_metrics(fontcontext.get_language())
    return (fontmetrics.get_approximate_char_width()/pango.SCALE,
            fontmetrics.get_approximate_digit_width()/pango.SCALE)

def widgetCharSize(widget):
    return widgetFontSizes(widget)[0]

def widgetDigitSize(widget):
    return widgetFontSizes(widget)[1]

#########################

# A gtk.Button containing an image from the given stock item, (eg,
# gtk.STOCK_OK) and optional text.  If 'reverse' is true, the text
# will precede the image.

class StockButton(gtk.Button):
    def __init__(self, stock_id, labelstr=None, reverse=False, markup=False,
                 align=None):
        debug.mainthreadTest()
        gtk.Button.__init__(self)
        image = gtk.Image()
        image.set_from_stock(stock_id, gtk.ICON_SIZE_BUTTON)
        hbox = gtk.HBox()
        self.markup = markup
        self.reverse = reverse
        if reverse:
            if labelstr:
                if markup:
                    self.label = gtk.Label()
                    self.label.set_markup(labelstr + ' ')
                else:
                    self.label = gtk.Label(labelstr + ' ')
                if align is not None:
                    self.label.set_alignment(align, 0.5)
                hbox.pack_start(self.label, expand=1, fill=1)
            hbox.pack_start(image, expand=0, fill=0)
        else:                       # not reverse
            hbox.pack_start(image, expand=0, fill=0)
            if labelstr:
                if markup:
                    self.label = gtk.Label()
                    self.label.set_markup(' ' + labelstr)
                else:
                    self.label = gtk.Label(' ' + labelstr)
                if align is not None:
                    self.label.set_alignment(align, 0.5)
                hbox.pack_start(self.label, expand=1, fill=1)
        self.add(hbox)

    def relabel(self, labelstr):
        if self.markup:
            if self.reverse:
                self.label.set_markup(labelstr + ' ')
            else:
                self.label.set_markup(' ' + labelstr)
        else:
            if self.reverse:
                self.label.set_label(labelstr + ' ')
            else:
                self.label.set_label(' ' + labelstr)
                        
def prevButton():
    debug.mainthreadTest()
    button = StockButton(gtk.STOCK_GO_BACK, 'Prev')
    gtklogger.setWidgetName(button, "Prev")
    return button

def nextButton():
    debug.mainthreadTest()
    button = StockButton(gtk.STOCK_GO_FORWARD, 'Next', reverse=True)
    gtklogger.setWidgetName(button, "Next")
    return button


#####################

# Find and return a gtk widget of type 'widgetclass' in the widget
# hierarchy rooted at 'root' (which must be a gtk widget).

def findChild(widgetclass, root):
    debug.mainthreadTest()
    if isinstance(root, gtk.Container):
        for child in root.get_children():
            if isinstance(child, widgetclass):
                return child
            descendant = findChild(widgetclass, child)
            if descendant:
                return descendant

# findChildren is just like findChild, but it returns all matching
# child widgets.

def findChildren(widgetclasses, root):
    debug.mainthreadTest()
    kids = []
    if isinstance(root, gtk.Container):
        for child in root.get_children():
            for widgetclass in widgetclasses:
                if isinstance(child, widgetclass):
                    kids.append(child)
                    break
            kids.extend(findChildren(widgetclasses, child))
    return kids
