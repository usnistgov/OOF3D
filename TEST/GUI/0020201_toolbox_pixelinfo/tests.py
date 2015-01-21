# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:47 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
import sys, math

# It's supposed to mean, comparison as floats of widgets containing text.
def multiTextFPCompare(widgetdict, widgetbase, tolerance=1.e-6):
    for (wname, target) in widgetdict.items():
        val = eval(gtklogger.findWidget(widgetbase+":"+wname).get_text())
        res = math.fabs(val-target)
        if res>tolerance:
            print >> sys.stderr, \
                  "FP compare failed at %s: %s!<%s." % \
                  (widgetbase+":"+wname, res, tolerance)
            return False
    return True
