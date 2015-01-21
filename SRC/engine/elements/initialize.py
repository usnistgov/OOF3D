# -*- python -*-
# $RCSfile: initialize.py,v $
# $Revision: 1.4.6.5 $
# $Author: langer $
# $Date: 2014/11/05 16:54:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config

## TODO: Import 1D elements here too.

import ooflib.SWIG.engine.elements.tri3
import ooflib.SWIG.engine.elements.tri3_6
import ooflib.SWIG.engine.elements.tri6
import ooflib.SWIG.engine.elements.tri6_3

import ooflib.SWIG.engine.elements.quad4
import ooflib.SWIG.engine.elements.quad4_8
import ooflib.SWIG.engine.elements.quad8
#     import ooflib.SWIG.engine.elements.quad8_4 # see quad8_4.spy
import ooflib.SWIG.engine.elements.quad9

if config.dimension() == 3:
    import ooflib.SWIG.engine.elements.tet4

from ooflib.SWIG.engine import masterelement
masterelement.makeMasterElementEnums()
