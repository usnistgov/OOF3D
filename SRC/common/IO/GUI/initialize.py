# -*- python -*-
# $RCSfile: initialize.py,v $
# $Revision: 1.52.2.4 $
# $Author: fyc $
# $Date: 2014/09/04 19:45:57 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config

import ooflib.common.initialize
# gtkutils must be imported before any other modules that use gtk
import ooflib.common.IO.GUI.gtkutils

import ooflib.common.IO.GUI.questioner
import ooflib.common.IO.GUI.guilogger

# Import GUI widgets before importing the pages that use them, or else
# the first time the page is displayed it may use a generic widget for
# some inputs.

import ooflib.common.IO.GUI.colorparamwidgets
import ooflib.common.IO.GUI.pixelgroupwidget
import ooflib.common.IO.GUI.whowidget
import ooflib.common.IO.GUI.displaymethodwidget

import ooflib.common.IO.GUI.oofGUI
import ooflib.common.IO.GUI.reporter_GUI
import ooflib.common.IO.GUI.mainmenuGUI
import ooflib.common.IO.GUI.microstructurePage
import ooflib.common.IO.GUI.console
import ooflib.common.IO.GUI.pixelPage
import ooflib.common.IO.GUI.introPage
import ooflib.common.IO.GUI.pixelselecttoolboxGUI
import ooflib.common.IO.GUI.workerGUI
import ooflib.common.IO.GUI.mainthreadGUI
import ooflib.common.IO.GUI.activeareaPage
import ooflib.common.IO.GUI.progressbarGUI
import ooflib.common.IO.GUI.tutorialsGUI
import ooflib.common.IO.GUI.reporterrorGUI
# import ooflib.common.IO.GUI.layereditorGUI

from ooflib.SWIG.common.IO.GUI import progressGUI

if config.dimension() == 2:
    import ooflib.common.IO.GUI.gfxwindow
    import ooflib.common.IO.GUI.viewertoolboxGUI
    import ooflib.common.IO.GUI.pixelinfoGUI
    import ooflib.SWIG.common.IO.GUI.gfxbrushstyle

else:
    import ooflib.common.IO.GUI.viewertoolbox3dGUI
    import ooflib.common.IO.GUI.voxelinfoGUI
    import ooflib.common.IO.GUI.gfxwindow3d












