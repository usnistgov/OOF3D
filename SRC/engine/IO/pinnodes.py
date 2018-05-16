# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import view
from ooflib.common import debug
from ooflib.common import toolbox
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import pointparameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletoncontext
from ooflib.engine import pinnodesmodifier

# Toolbox for pinning nodes.  Pinned nodes don't move during mesh
# modification operations.  They *can* move during equilibration --
# they're not boundary conditions.  Pinned nodes are treated much like
# Skeleton Selectables, and share a lot of code with them.

# The PinnedNodes toolbox is *not* derived from GenericSelectToolbox
# because it doesn't require different kinds of mousehandlers for
# different selection methods. 

class PinnedNodesToolbox(toolbox.Toolbox):
    def __init__(self, gfxwindow):
        toolbox.Toolbox.__init__(self, 'Pin Nodes', gfxwindow)

    tip="Pin nodes."

    discussion="""<para>
    Pinned nodes are immobile during &skel; modifications.  This menu
    contains tools for pinning and unpinning nodes with mouse input.
    </para>"""

toolbox.registerToolboxClass(PinnedNodesToolbox, ordering=2.7)
