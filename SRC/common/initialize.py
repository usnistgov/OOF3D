# -*- python -*-
# $RCSfile: initialize.py,v $
# $Revision: 1.65.2.5 $
# $Author: fyc $
# $Date: 2014/09/04 19:45:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import utils
from ooflib.common import debug
from ooflib.SWIG.common import config
utils.OOFexec('import ooflib.SWIG.common.ooferror') # exception handling
utils.OOFexec('from ooflib.common.IO.mainmenu import OOF') # Main OOF menu
import ooflib.common.excepthook

import ooflib.common.IO.activeareamenu
import ooflib.common.IO.activeareamodmenu
import ooflib.common.IO.automatic
import ooflib.common.IO.automaticdoc
import ooflib.common.IO.bitmapdisplay
import ooflib.common.IO.bitoverlaydisplay
import ooflib.common.IO.colormap
import ooflib.common.IO.menudump
import ooflib.common.IO.microstructuremenu
import ooflib.common.IO.pixelgroupmenu
import ooflib.common.IO.pixelinfo
import ooflib.common.IO.pixelinfodisplay
import ooflib.common.IO.pixelselectionmenu
import ooflib.common.IO.pixelselectiontoolbox
import ooflib.common.IO.progressbar
import ooflib.common.IO.reporterIO
import ooflib.common.IO.reportermenu
import ooflib.common.IO.reporterror
import ooflib.common.IO.activityviewermenu
import ooflib.common.IO.topwho
import ooflib.common.IO.viewertoolbox
import ooflib.common.IO.words
import ooflib.common.color
import ooflib.common.microstructure
import ooflib.common.pixelselectionmethod
import ooflib.common.pixelselectionmod

if config.dimension() == 2:

    from ooflib.common import parallel_enable
    if parallel_enable.enabled():
        import ooflib.common.IO.parallelmainmenu
        import ooflib.common.IO.microstructureIPC


# Active area stuff

#import ooflib.common.IO.activeareamodmenu


