# -*- python -*-
# $RCSfile: orientmapIO.py,v $
# $Revision: 1.5.18.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:41 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Read and write orientation map data in Microstructure data files.

from ooflib.SWIG.common import corientation
from ooflib.SWIG.orientationmap import orientmapdata
from ooflib.common.IO import microstructureIO
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
import ooflib.common.microstructure

def _loadOrientationMap(menuitem, microstructure, filename, orientations):
    # orientations is a list of 3-tuples representing ABG Euler
    # angles.
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    ms = mscontext.getObject()
    od = orientmapdata.OrientMap(ms.sizeInPixels(), ms.size())
    reader = orientmapdata.OrientMapReader() # just to borrow its set_angle fn
    count = 0
    for pixel in ms.coords():
        reader.set_angle(od, pixel,
                         corientation.COrientABG(*orientations[count]))
        count += 1
    orientmapdata.registerOrientMap(microstructure, od)
    orientmapplugin = mscontext.getObject().getPlugIn('OrientationMap')
    orientmapplugin.set_data(od, filename)
    orientmapplugin.timestamp.increment()
    orientmapdata.orientationmapNotify(ms) 

microstructureIO.micromenu.addItem(oofmenu.OOFMenuItem(
    'OrientationMap',
    callback=_loadOrientationMap,
    params=[whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString),
            parameter.StringParameter('filename',
                                      tip="File from which the map was read."),
            parameter.ListOfListOfFloatsParameter('orientations',
                                                  tip='Tuples containing ABG values.')],
    help="Load an Orientation Map.  Used internally in data files.",
    discussion="""<para>

    Load an <classname>Orientation Map</classname> into a &micro;.
    This command is used only in data files, and is only available if
    &oof2; was built with the
    <userinput>--enable-orientationmap</userinput> option.

    </para>"""
    ))
            

def writeOrientationMap(datafile, mscontext):
    ms = mscontext.getObject()
    data = orientmapdata.getOrientationMap(mscontext.getObject())
    if data:
        filename = orientmapdata.getOrientationMapFile(ms)
        orientations = [data.angle(pt).abg() for pt in ms.coords()]
        datafile.startCmd(microstructureIO.micromenu.OrientationMap)
        datafile.argument('microstructure', ms.name())
        datafile.argument('filename', filename)
        datafile.argument('orientations', [[a.alpha(), a.beta(), a.gamma()]
                                           for a in orientations])
        datafile.endCmd()
    
    
microstructureIO.registerMicrostructureIOPlugIn(writeOrientationMap)
