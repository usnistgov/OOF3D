# -*- python -*-
# $RCSfile: newimageGUI.py,v $
# $Revision: 1.13.10.6 $
# $Author: langer $
# $Date: 2013/11/15 22:03:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Buttons for creating Microstructures from Images appear on the
# Microstructure page, but have to be defined here in the image
# module.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
if config.dimension() == 2:
    from ooflib.SWIG.image import oofimage
elif config.dimension() == 3:
    from ooflib.SWIG.image import oofimage3d
from ooflib.common import debug
from ooflib.common import microstructure
from ooflib.common.IO import microstructuremenu
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import microstructurePage
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips

from ooflib.image import imagecontext
import gtk

# Ensure that OOFMenuItems have been created before constructing this
# GUI.
from ooflib.image.IO import imagemenu 

def newMSfromImageFile(button):
    menuitem = microstructuremenu.micromenu.Create_From_ImageFile
    if parameterwidgets.getParameters(
        title='Load Image and create Microstructure',
        *menuitem.params):
        menuitem.callWithDefaults()

if config.dimension() == 2:
    newfromfilebutton = gtkutils.StockButton(
        gtk.STOCK_NEW, "New from Image File")
    gtklogger.setWidgetName(newfromfilebutton, "NewFromFile")
    gtklogger.connect(newfromfilebutton, 'clicked', newMSfromImageFile)
    tooltips.set_tooltip_text(
        newfromfilebutton,
        "Create a new microstructure with a new image"
        " that is being loaded.")

elif config.dimension() == 3:
    newfromfilebutton = gtkutils.StockButton(
        gtk.STOCK_NEW, "New from Image Files")
    gtklogger.setWidgetName(newfromfilebutton, "NewFromFile")
    gtklogger.connect(newfromfilebutton, 'clicked', newMSfromImageFile)
    tooltips.set_tooltip_text(
        newfromfilebutton,
        "Create a new microstructure with a new set of images"
        " that is being loaded.")
    

microstructurePage.addNewButton(newfromfilebutton)

