# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
import types

def goSensitive(sensitive):
    return is_sensitive("OOF2:Boundary Analysis Page:Go") == sensitive

def bdyList(*bdys):
    return chooserCheck(
        "OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList",
        bdys)


def msgFloat(*expectedvals, **kwargs):
    tolerance = kwargs.get('tolerance', 1.e-10)
    msgbuffer = gtklogger.findWidget("OOF2 Messages 1:Text").get_buffer()
    text = msgbuffer.get_text(msgbuffer.get_start_iter(),
                              msgbuffer.get_end_iter())
    lastline = text.split('\n')[-2]
    actualvals = eval(lastline)
    if type(actualvals) is not types.TupleType:
        actualvals = (actualvals,)
    if len(actualvals) != len(expectedvals):
        print >> sys.stderr, \
            "Expected %d values, but found $d" % (len(expectedvals), 
                                                  len(actualvals))
    for actual, expected in zip(actualvals, expectedvals):
        if abs(actual - expected) > tolerance:
            print >> sys.stderr, "Expected %g, got %g" % (expected, actual)
            return False
    return True

# def msgVector(expected, tolerance=1.e-10):
#     msgbuffer = gtklogger.findWidget("OOF2 Messages 1:Text").get_buffer()
#     text = msgbuffer.get_text(msgbuffer.get_start_iter(),
#                               msgbuffer.get_end_iter())
#     lastline = text.split('\n')[-2]
#     actual = eval(lastline)
#     if len(actual) != len(expected):
#         print >> sys.stderr, \
#               "Expected a vector of length %d, got one of length %d" \
#               % (len(expected), len(actual))
#         return False
#     for exp, act in zip(expected, actual):
#         if abs(exp - act) > tolerance:
#             print >> sys.stderr, "Expected %s, got %s" % (`expected`, `actual`)
#             return False
#     return True
