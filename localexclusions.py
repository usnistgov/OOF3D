# -*- python -*-
# $RCSfile: localexclusions.py,v $
# $Revision: 1.1.2.1 $
# $Author: langer $
# $Date: 2014/07/07 19:41:23 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Lists of files and directories that are to be excluded from the
# distribution.  This file is imported by make_dist, and contains only
# the exclusions that are specific to this version of OOF2.  When the
# 2D and 3D versions are merged, this file will no longer be
# necessary.

# Directories to be excluded no matter where they occur in the
# directory tree.
globalExcludeDirs = []

# Files to be excluded no matter where they occur.
globalExcludeFiles = []

# Directories to be excluded.  Path names are relative to the the top
# OOF2 directory.
excludeDirs = ["TEST"]

# Files to be excluded.  Path names are relative to the the top OOF2
# directory.
excludeFiles = []
