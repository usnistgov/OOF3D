# -*- python -*-
# $RCSfile: deputyParallel.py,v $
# $Revision: 1.7.18.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# TODO MER: CLEANUP Obsolete module

from ooflib.common import debug
from ooflib.common import parallel_object_manager
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import parameter
from ooflib.engine import skeletoncontext
try:
    from ooflib.SWIG.common import mpitools
except ImportError:
    pass

## General definitions
_rank = mpitools.Rank()
_size = mpitools.Size()

def _parallel_init(self, skeleton, _id = None):
    ## here, skeleton is the name of the skeleton
    if _rank == 0:
        id = parallel_object_manager.parallelObjectManager.add(self)
        deputymenu.Create(skeleton = skeleton, id = id) ## back-end call
    else:
        parallel_object_manager.parallelObjectManager.add(self, _id)
        
deputymenu = parallelmainmenu.ipcmenu.addItem(oofmenu.OOFMenuItem('Deputy', secret=1, no_log=1))


def _create_deputy(menuitem, skeleton, id):
    ## skeleton skeleton is the full name of the skeleton
    global _rank
    if _rank != 0:
        skel = skeletoncontext.skeletonContexts[skeleton].getObject()
        deputy = skel.deputyCopy() ## creates back-end deputy with the correct id
        parallel_object_manager.parallelObjectManager.add(deputy, id)

deputymenu.addItem(oofmenu.OOFMenuItem('Create', callback = _create_deputy, secret=1, no_log=1, threadable = oofmenu.PARALLEL_UNTHREADABLE, params=[parameter.StringParameter('skeleton'), parameter.IntParameter('id')] ))
