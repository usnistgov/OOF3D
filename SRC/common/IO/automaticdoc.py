# -*- python -*-
# $RCSfile: automaticdoc.py,v $
# $Revision: 1.4.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This has its own file to avoid an import loop.  It otherwise would
# be in automatic.py.

from ooflib.common.IO import xmlmenudump

xmlmenudump.XMLObjectDoc('automatic',
                 xmlmenudump.loadFile('DISCUSSIONS/common/object/automatic.xml')
                         )
