# -*- python -*-
# $RCSfile: microstructure.py,v $
# $Revision: 1.151.10.5 $
# $Author: langer $
# $Date: 2014/08/20 02:21:13 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# A Microstructure object is a segmentation of an Image.  It stores the
# Pixelgroups to which the pixels in the Image have been assigned, as
# well as other PixelAttributes, such as Materials.

from ooflib.SWIG.common import config

from ooflib.SWIG.common import activearea
from ooflib.SWIG.common import cmicrostructure
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import cpixelselection
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import pixelselection
from ooflib.common import primitives
from ooflib.common import utils
from ooflib.common.IO import whoville
from types import *
import string
import sys

#############################

# MicrostructurePlugIns are objects that can be defined in other
# modules.  An instance of each plug-in is created when a
# Microstructure is created, and destroyed when it's destroyed.  What
# happens in between is up to the plug-in.  When the Microstructure is
# created, the plug-in's constructor is called with the Microstructure
# as an argument.

class MicrostructurePlugIn:
    def __init__(self, microstructure):
        self.microstructure = microstructure
    def destroy(self):
        self.microstructure = None

plugInClasses = {}

def registerMicrostructurePlugIn(plugIn, name):
    plugInClasses[name] = plugIn

#############################

class MicrostructureContext(whoville.Who):
    def getMicrostructure(self):
        return self.getObject()
    def getSelectionContext(self):
        return self.getObject().pixelselection
    def lockAndDelete(self):
        self.reserve()
        ms = self.getObject()
        try:
            # We have to remove Images, etc, from the Microstructure
            # *before* acquiring the write-lock on the Microstructure,
            # because we can't obtain the write locks on the Image and
            # the Microstructure at the same time.  (An Image can't be
            # locked unless it can obtain its Microstructure's read
            # lock.)
            for imagename in ms.imageNames():
                image = whoville.getClass('Image')[[self.name(), imagename]]
                image.begin_writing()
                try:
                    image.removeMicrostructure(ms)
                    ms.removeImage(image)
                finally:
                    image.end_writing()
            aa = activearea.activeareaWhoClass[self.name()]
            aa.begin_writing()
            try:
                activearea.activeareaWhoClass.remove(aa.name())
            finally:
                aa.end_writing()
            aa.setParent(None)
            pixsel = pixelselection.pixelselectionWhoClass[self.name()]
            pixsel.begin_writing()
            try:
                pixelselection.pixelselectionWhoClass.remove(pixsel.name())
            finally:
                pixsel.end_writing()
            pixsel.setParent(None)

            # Remove Skeletons
            skelclass = whoville.getClass('Skeleton')
            if skelclass is not None:
                for skeletonname in skelclass.keys(base=self.name()):
                    skelcontext = skelclass[[self.name(), skeletonname[0]]]
                    skelcontext.lockAndDelete()
                    skelcontext.setParent(None)
            self.begin_writing()
            try:
                microStructures.remove(self.name())
                ms.destroy()
            finally:
                self.end_writing()
        finally:
            self.cancel_reservation()

## TODO 3.1: Add a better mechanism for deletion.  Each WhoClass
## can know which other WhoClasses it's a parent of.  Then a Who
## object can automatically call lockAndDelete() for all of its
## children before it deletes itself.  Is that even worth it?

## microsctructures is an instance of the WhoClass, which hosts
## a set of MicrostructureContext objects. The MicrostructureContext
## class was subclassed from the Who class, and it contains
## a Microstructure object.
microStructures = whoville.WhoClass('Microstructure', 150,
                                    instanceClass=MicrostructureContext,
                                    proxyClasses=['<topmost>',
                                                  '<top bitmap>'])

# Handy utility function, returns the microstructure object, not the
# context, and so is not equivalent to microStructures[name].
def getMicrostructure(name):
    try:
        return microStructures[name].getObject()
    except KeyError:
        return None

def getMSContextFromMS(microstructure):
    return microStructures[microstructure.name()]

utils.OOFdefine('Microstructure', cmicrostructure.CMicrostructure)
utils.OOFdefine('getMicrostructure', getMicrostructure)
