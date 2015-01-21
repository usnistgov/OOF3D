# -*- python -*-
# $RCSfile: pypath.py,v $
# $Revision: 1.1.48.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:36 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# This file just prints the Python path, as modified by gtk.  It's the
# same thing that's done in oof.py.  See the comments there.  The code
# is extracted here so that it can be used for setting up cx_freeze
# (which we haven't tried for years so it's not clear why this file is
# still here...)

import sys, string
try:
    import pygtk
except ImportError:
    pass
else:
    try:
        pygtk.require("1.2")
    except AssertionError:
        pass
print string.join(sys.path, ":")
