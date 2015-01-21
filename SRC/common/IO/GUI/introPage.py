# -*- python -*-
# $RCSfile: introPage.py,v $
# $Revision: 1.17.10.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:11 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import oofversion
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import oofGUI
import gtk
import pango

from ooflib.common.IO.words import words
# words['Credits'], words['Disclaimer'], and words['Copyright']
# are defined in common.IO.

if config.dimension() == 2:
    name = "OOF2"
    pixels = "pixels"
elif config.dimension() == 3:
    name = "OOF3D"
    pixels = "voxels"

words['Welcome'] = """

                          Welcome to %s!
                           Version %s

%s performs physical computations on microstructures, starting from a micrograph or other image of the microstructure.  The "Task" menu above brings up pages that lead you through the required steps.

Here is an extremely simplified description of the process, just to get you started.  For more details and examples, see the Tutorials in the Help menu and the manual, which may be found on-line at http://www.ctcms.nist.gov/~langer/oof2man.

First, create a Microstructure, which is %s's basic data type. A Microstructure is a map which assigns Materials to %s.  A Microstructure can contain Images.  You can select %s in an Image and assign Materials to those %s in the Microstructure.

After creating a Microstructure and assigning Materials to it, you need to create a Skeleton.  A Skeleton defines the geometry of a finite element mesh, specifying node positions and element edges only. It does not specify element type, equations, or boundary conditions. The Skeleton Modification tools allow you to adapt the Skeleton to the geometry of your Microstructure.  A Microstructure can contain more than one Skeleton.

The FE Mesh page creates a real finite element mesh from a Skeleton by specifying the types of elements to use.  A Skeleton can have more than one Mesh.

The Fields page determines what physical quantities are defined on the mesh (eg, Temperature).  Fields must be defined before they are given values.  Fields must be activated before they can be solved for.

The Equations page determines which equations will be solved. The Boundary Conditions page sets the boundary conditions (surprise!), and the Solver page finds the solution.  Finally, the Analysis and Boundary Analysis pages evaluate the results.

Graphics windows may be opened from the Windows menu.  They can be used to view Images, Microstructures, Skeletons, and Meshes, and to interactively operate on them.  The behavior of a graphics window is determined by the currently selected toolbox, which can be changed with the pull-down menu in the window's left pane. 

""" % (name,oofversion.version,name,name,pixels,pixels,pixels)

####################
   
##font = load_font("-*-fixed-*-*-*-*-*-120-*-*-*-*-iso8859-*")

class IntroPage(oofGUI.MainPage):
    def __init__(self):
        oofGUI.MainPage.__init__(self, name="Introduction", ordering=0,
                                 tip="Welcome to %s!"%name)
        vbox = gtk.VBox()
        self.gtk.add(vbox)
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "Scroll")
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        vbox.pack_start(scroll, expand=1, fill=1)
        self.textarea = fixedwidthtext.FixedWidthTextView()
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.add(self.textarea)
        self.textarea.set_editable(0)
        self.textarea.set_cursor_visible(0)
        self.textarea.set_wrap_mode(gtk.WRAP_WORD)

        buttonbox = gtk.HBox(homogeneous=1, spacing=2)
        buttonbox.set_border_width(2)
        vbox.pack_start(buttonbox, expand=0, fill=0)

        self.labels = ['Welcome', 'Credits', 'Copyright', 'Disclaimer']
        self.buttons = [gtk.ToggleButton(x) for x in self.labels]
        for button, label in zip(self.buttons, self.labels):
            buttonbox.pack_start(button, expand=1, fill=1)
            gtklogger.setWidgetName(button, label)
            gtklogger.connect(button, 'clicked', self.buttonCB, label)

        self.buttons[0].set_active(1)

    def buttonCB(self, button, which):
        if button.get_active():
            for button, label in zip(self.buttons, self.labels):
                if label == which:
                    button.set_sensitive(0)
                else:
                    button.set_sensitive(1)
                    button.set_active(0)
            self.textarea.get_buffer().set_text(words[which])
##            self.textarea.freeze()
##            self.textarea.set_point(0)
##            self.textarea.forward_delete(self.textarea.get_length())
##            self.textarea.insert(font, None, None, words[which])
##            self.textarea.thaw()
            
IntroPage()

    
