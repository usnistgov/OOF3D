# -*- python -*-
# $RCSfile: distname.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/07/07 22:03:23 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Until we merge the 2D and 3D branches, we need a way to set the name
# of the distribution file that make_dist creates.  This file just
# contains that name.  Putting hte name here, instead of in make_dist,
# allows both versions to use the same make_dist script.

distname = 'oof3d'
