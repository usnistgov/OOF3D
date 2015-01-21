# -*- python -*-
# $RCSfile: imagecontext.py,v $
# $Revision: 1.2.18.2 $
# $Author: langer $
# $Date: 2011/09/22 17:50:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common.IO import whoville
import ooflib.common.microstructure

class ImageContext(whoville.WhoDoUndo):
    def __init__(self, name, classname, oofimage, parent):
        whoville.WhoDoUndo.__init__(self, name, 'Image', oofimage, parent)
        # parent is a MicrostructureContext object
        ms = parent.getObject()
        oofimage.setMicrostructure(ms)
        self.microstructure = ms
        ms.addImage(self)
    def removeMicrostructure(self, ms): # called by Microstructure.removeImage()
        self.getObject().removeMicrostructure()
        self.microstructure = None
    def getMicrostructure(self):
        return self.microstructure
    def getSelectionContext(self):
        # Returns the object that holds the pixel selection, not the
        # selection itself.
        if self.microstructure is not None:
            return self.microstructure.pixelselection
    def writeImage(self, datafile):
        from ooflib.image.IO import imageIO    # delayed import to avoid loops
        imageIO.writeImage(datafile, self)

    def size(self):
        return self.getObject().size()

## The imageContexts is a WhoDoUndoClass that hosts
## a set of instances of the ImageContext class, which
## which are subclasses of the WhoDoUndo class.
## Each ImageContext object contains an actual OOFImage[3D] object.
## Please also see the note on microsctructure.microStructures
imageContexts = whoville.WhoDoUndoClass(
    'Image',
    100,
    parentClass=ooflib.common.microstructure.microStructures,
    instanceClass=ImageContext,
    proxyClasses=['<topmost>', '<top bitmap>'])
