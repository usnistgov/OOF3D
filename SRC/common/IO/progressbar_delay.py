# -*- python -*-
# $RCSfile: progressbar_delay.py,v $
# $Revision: 1.14.2.1 $
# $Author: langer $
# $Date: 2013/01/28 16:58:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 



# Time, in milliseconds, between the time that a progressbar object is
# created and the time that it is installed in the ActivityViewer
# window.
delay = 2000

# Time in milliseconds between progress bar updates.
period = 200

def set_delay(menuitem, milliseconds):
    global delay
    delay = milliseconds
