# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:20 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def dataWidgets(*widgetnames):
    # strip first result from findAllWidgets, because it's just "Data"
    wnames = gtklogger.findAllWidgets('Mesh Data 1:Data')[1:]
    # strip "Data:" from each name
    shortnames = [n[5:] for n in wnames]
    if len(shortnames) != len(widgetnames):
        print "Wrong number of data widgets"
        print shortnames
        return False
    for n in widgetnames:
        if n not in shortnames:
            print "Unexpected widgetname:", n
            print shortnames
            return False
    return True
