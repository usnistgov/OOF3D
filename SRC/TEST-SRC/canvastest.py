# -*- python -*-
# $RCSfile: canvastest.py,v $
# $Revision: 1.3.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


import oofpath
from gtk import *
from oofcpp import *

def open_graphics(button):
    window = GtkWindow(WINDOW_TOPLEVEL)
    window.set_title("Graphics")
    canvas = ScrolledOOFCanvas(CRectangle(Coord(0., 0.), Coord(1., 1.)), 0)
    canvas.draw_segment(CSegment(Coord(0., 0.), Coord(1., 1.)))
    canvas.draw_segment(CSegment(Coord(1., 0.), Coord(0., 1.)))
    canvas.add_self(window._o)
    window.show()

##window = GtkWindow(WINDOW_TOPLEVEL)
pyth##window.connect("destroy", mainquit)
##window.set_border_width(10)

####button = GtkButton("Graphics")
####button.connect("clicked", open_graphics)
####window.add(button)
####button.show()

##canvas = ScrolledOOFCanvas(CRectangle(Coord(0., 0.), Coord(1., 1.)), 0)
##canvas.draw_segment(CSegment(Coord(0., 0.), Coord(1., 1.)))
##canvas.draw_segment(CSegment(Coord(1., 0.), Coord(0., 1.)))
##canvas.add_self(window._o)

##window.show()
##mainloop()

testcanvas()
