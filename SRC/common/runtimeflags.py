# -*- python -*-
# $RCSfile: runtimeflags.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2013/02/01 20:31:05 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This file is just a resting place for run-time parameters that are
# set in oof.py and used elsewhere.  It prevents the other files from
# having to import oof.py (which is not allowed because it leads to
# import loops) or having to define the parameters themselves.  The
# other files may not be natural places for those parameters to live.

batch_mode = False
text_mode = False
surface_mode = False

geometry="550x350"
