# -*- python -*-
# $RCSfile: microstructurePage.py,v $
# $Revision: 1.5.10.9 $
# $Author: langer $
# $Date: 2014/11/05 16:55:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.orientationmap import orientmapdata
from ooflib.common.IO import microstructuremenu
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import microstructurePage
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
import gtk
import os

# Create a MicrostructurePageInfoPlugIn that displays the Orientation
# map file name in the page's info box.

def _orientationmapinfo(microstructure):
    filename = orientmapdata.getOrientationMapFile(microstructure.getObject())
    if filename:
        direct, basename = os.path.split(filename)
        return 'Orientation Map file: ' + basename + '\ndirectory: ' + direct
    return 'Orientation Map file: <None>'

plugin = microstructurePage.addMicrostructureInfo(callback=_orientationmapinfo,
                                                  ordering=1)

def _updateCB(ms):
    plugin.update()
    
switchboard.requestCallback('OrientationMap changed', _updateCB)

####################

# Add a button to the Microstructure page for the "New from
# Orientation Map" command.
if config.dimension() == 2:
    def _newMSfromOrientationMap(button):
        menuitem = microstructuremenu.micromenu.Create_From_OrientationMap_File
        if parameterwidgets.getParameters(
            title='Create Microstructure from Orientation Map file',
            *menuitem.params):
            menuitem.callWithDefaults()

    newfromorientmapbutton = gtkutils.StockButton(gtk.STOCK_NEW,
                                            "New from Orientation Map")
    gtklogger.setWidgetName(newfromorientmapbutton, "NewFromOrientationMap")
    gtklogger.connect(newfromorientmapbutton, 'clicked',
                      _newMSfromOrientationMap)
    tooltips.set_tooltip_text(newfromorientmapbutton,
              "Create a new Microstructure from an Orientation Map data file.")

    microstructurePage.addNewButton(newfromorientmapbutton)



elif config.dimension() == 3:
    ## TODO 3.1:  Update for new fileselector.
    from ooflib.common.IO.GUI import fileselector
    def _newMSfromOrientationMaps(button):
        menuitem = microstructuremenu.micromenu.Create_From_OrientationMap_File
#         if parameterwidgets.getParameters(
#             title='Create Microstructure from Orientation Map files',
#             *menuitem.params):
        fmt = menuitem.get_arg('format')
        file = fileselector.fileSelector(
            ident='Orientation Maps',
            mode='r',
            title='Load Orientation Maps and create Microstructure',
            params=(fmt,),
            pattern=True)
        menuitem.callWithDefaults(filename=file)

    newfromorientmapbutton = gtkutils.StockButton(gtk.STOCK_NEW,
                                            "New from Orientation Maps")
    gtklogger.setWidgetName(newfromorientmapbutton, "NewFromOrientationMaps")
    gtklogger.connect(newfromorientmapbutton, 'clicked',
                      _newMSfromOrientationMaps)
    tooltips.set_tooltip_text(newfromorientmapbutton,
              "Create a new Microstructure from Orientation Map data files.")

    ## TODO 3.1: Uncomment this after adding support for 3D EBSD images
    # microstructurePage.addNewButton(newfromorientmapbutton)

