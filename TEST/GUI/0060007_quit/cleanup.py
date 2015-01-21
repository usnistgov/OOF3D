# -*- python -*-
# $RCSfile: cleanup.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:14:04 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# This file is run with execfile from within guitests.py.  "dir" is
# set to the directory containing the test files.

import filecmp
assert filecmp.cmp("quit.log", os.path.join(dir, "quit.log"))
removefile("quit.log")
