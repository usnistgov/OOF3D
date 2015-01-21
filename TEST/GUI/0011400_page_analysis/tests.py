# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:13 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
import types

removefile('junk.data')
removefile('cs.data')
removefile('msg.data')

def goSensitive(sensitive):
    return is_sensitive('OOF2:Analysis Page:Go') == sensitive

def samplingOptions(*opts):
    return chooserCheck('OOF2:Analysis Page:bottom:Sampling:Sampling:Chooser', opts)

def samplingParams(sampling, paramnames):
    widgetnames = gtklogger.findAllWidgets(
        'OOF2:Analysis Page:bottom:Sampling:Sampling:%s' % sampling)
    if not chooserStateCheck('OOF2:Analysis Page:bottom:Sampling:Sampling:Chooser',
                             sampling):
        return False
    # The first item in the list is the sampling type, not a param, so
    # we skip it.  The remaining names are of the form
    # "samplingtype:paramname" or "samplingtype:paramname:subwidget".
    # If there are subwidgets, there may be more than one, so we have
    # to pull out the paramnames and make sure they're unique.
    wnamedict = {}
    for wname in widgetnames[1:]:
        wnamedict[wname.split(':')[1]] = 1
    wnames = wnamedict.keys()
    
    if len(paramnames) != len(wnames):
        print >> sys.stderr, "Wrong number of parameter names!"
        print >> sys.stderr, "  widgetnames=", widgetnames
        return False
    for widgetname in wnames:
        if widgetname not in paramnames:
            print >> sys.stderr, "Unexpected parameter named %s" % widgetname
            return False
    return True

def msgTextValue(*vals, **kwargs):
    tolerance = kwargs['tolerance']
    msgbuffer = gtklogger.findWidget('OOF2 Messages 1:Text').get_buffer()
    lines = msgbuffer.get_text(msgbuffer.get_start_iter(),
                               msgbuffer.get_end_iter()).split('\n')
    textvals = eval(lines[-2])
    if type(textvals) is not types.TupleType:
        textvals = (textvals,)
    for textval, val in zip(textvals, vals):
        if abs(textval - val) > tolerance:
            return False
    return True
    
def csWidgetCheck(names, new, copy, edit, rename, remove):
    if not chooserCheck(
        'OOF2:Analysis Page:top:Domain:DomainRCF:Cross Section:cross_section:List',
        names):
        print >> sys.stderr, "CS names don't agree"
        return False
    if not sensitizationCheck(
        {'New':new,
         'Copy':copy,
         'Edit':edit,
         'Rename':rename,
         'Remove':remove},
        base="OOF2:Analysis Page:top:Domain:DomainRCF:Cross Section:cross_section"):
        return False
    return True

def csWidgetCheck0():
    return csWidgetCheck(names=[], new=1, copy=0, edit=0, rename=0, remove=0)

def csWidgetCheck1():
    return csWidgetCheck(names=['cs', 'cs<2>'],
                         new=1, copy=1, edit=1, rename=1, remove=1)

def csWidgetCheck2():
    return csWidgetCheck(names=['cs'],
                         new=1, copy=1, edit=1, rename=1, remove=1)

def datacheck0():
    file = open('cs.data', 'r')
    lines = file.readlines()
    if len(lines) != 69:
        print >> sys.stderr, "Wrong number of lines in cs.data"
        return False
    if lines[-2] != "# 2. average of Displacement[x]\n":
        print >> sys.stderr, "Wrong header"
        return False
    expectedvals = (0.0, -0.0328012742088)
    # expectedval = -0.032833055  # from static code
    actualvals = eval(lines[-1])
    for actual, expected in zip(actualvals, expectedvals):
        if abs(actual - expected) >= 1.e-10:
            print >> sys.stderr, "Wrong value, diff=", abs(actual- expected)
            return False
    return True
