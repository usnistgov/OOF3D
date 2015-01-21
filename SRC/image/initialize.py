# -*- python -*-
# $RCSfile: initialize.py,v $
# $Revision: 1.26.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:37 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import parallel_enable
from ooflib.common import utils
from ooflib.SWIG.common import config
import ooflib.SWIG.image.burn
if config.dimension() == 2:
    import ooflib.SWIG.image.oofimage
else:
    import ooflib.SWIG.image.oofimage3d
import ooflib.image.IO.defaultLayer
import ooflib.image.IO.imageIO
import ooflib.image.IO.imagemenu
import ooflib.image.pixelselectionmethod
import ooflib.image.pixelselectionmod

if parallel_enable.enabled():
    import ooflib.image.IO.oofimageIPC

if config.enable_segmentation():
    import ooflib.image.SEGMENTATION.initialize


