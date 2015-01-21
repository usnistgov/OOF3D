# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:22 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

import string, sys

# Custom function for doing an "ends-with" type of test, but with a
# floating-point tolerance.  Starts from the end of the file.  See
# also floatFileDiff in the "generics" file.
def floatTextTail(widgetpath, text, tolerance=1.0e-6,
                  comment="#", separator=","):
    textlines = string.split(text,'\n')
    msgbuffer = gtklogger.findWidget(widgetpath).get_buffer()
    msglines = msgbuffer.get_text(msgbuffer.get_start_iter(),
                                  msgbuffer.get_end_iter()).split('\n')
    # Text-lines is presumably shorter than the buffer.
    for i in range(len(textlines)):
        textdata = textlines[-(i+1)]
        msgdata = msglines[-(i+1)]

        if textdata==msgdata:
            continue

        # Comments are allowed to differ.
        if textdata[0]==comment or msgdata[0]==comment:
            continue

        textitems = string.split(textdata, separator)
        msgitems = string.split(msgdata, separator)

        for(i1,i2) in zip(textitems, msgitems):
            try:
                (f1, f2) = (float(i1), float(i2))
            except ValueError:
                if i1!=i2:
                    print >> sys.stderr, "Text mismatch, >%s< != >%s<." % (i1,i2)
                    return False
            else:
                if abs(f1-f2)>tolerance:
                    print >> sys.stderr,  "Float difference, %f too far from %f." % (f1,f2)
                    return False
                if f1!=0.0 and f2!=0.0 and abs((f1/f2)-1.0)>tolerance:
                    print >> sys.stderr, "Float difference, %f/%f too far from 1.0" % (f1,f2)
                    return False

    # If everything worked, it's a win.
    return True
