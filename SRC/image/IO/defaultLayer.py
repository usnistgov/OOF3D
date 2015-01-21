# -*- python -*-
# $RCSfile: defaultLayer.py,v $
# $Revision: 1.14.18.2 $
# $Author: langer $
# $Date: 2013/01/20 04:51:39 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import voxelfilter
if config.dimension() == 2:
    from ooflib.SWIG.image import oofimage
## elif config.dimension() == 3:
##     #from ooflib.SWIG.image import oofimage3d
##     from ooflib.image import oofimage3d
from ooflib.common.IO import bitmapdisplay
from ooflib.common.IO import ghostgfxwindow
from ooflib.image import imagecontext


def defaultImageDisplay():
    # The "filter" parameter to the BitmapDisplayMethod registration
    # may have an value that doesn't make sense for the new graphics
    # window, so the default display explicitly selects the AllVoxels
    # filter.  (For example, the registration might have last been
    # used to display only a particular voxel group, and that group
    # might not be defined in the Microstructure being displayed now.)
    return bitmapdisplay.bitmapDisplay(filter=voxelfilter.AllVoxels())

ghostgfxwindow.DefaultLayer(imagecontext.imageContexts, defaultImageDisplay)


