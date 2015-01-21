# -*- python -*-
# $RCSfile: outputvalwidgets.py,v $
# $Revision: 1.13.4.1 $
# $Author: langer $
# $Date: 2013/11/08 20:45:11 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Widgets for displaying OutputVals.

from ooflib.SWIG.engine import fieldindex
from ooflib.SWIG.engine import outputval
from ooflib.SWIG.engine import symmmatrix
from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
import gtk

class GenericOVWidget:
    def __init__(self, val):
        debug.mainthreadTest()
        self.gtk = gtk.Entry()
        gtklogger.setWidgetName(self.gtk, 'generic')
        self.gtk.set_editable(False)
        self.gtk.set_text(`val`)
    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()
    def show(self):
        debug.mainthreadTest()
        self.gtk.show()

####################
        
class VectorWidget:
    def __init__(self, val):
        debug.mainthreadTest()
        self.gtk = gtk.Table(rows=val.size(), columns=2)
        iterator = val.getIterator()
        row = 0
        while not iterator.end():
            label = gtk.Label(iterator.shortrepr()+':')
            label.set_alignment(1.0, 0.5)
            self.gtk.attach(label, 0,1, row,row+1, xoptions=gtk.FILL)
            entry = gtk.Entry()
            gtklogger.setWidgetName(entry, iterator.shortrepr())
            entry.set_editable(False)
            entry.set_text("%-13.6g" % val[iterator])
            self.gtk.attach(entry, 1,2, row,row+1, xoptions=gtk.EXPAND|gtk.FILL)
            row += 1
            iterator.next()
    def show(self):
        debug.mainthreadTest()
        self.gtk.show_all()
    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

def _VectorOutputVal_makeWidget(self):
    return VectorWidget(self)

outputval.VectorOutputValPtr.makeWidget = _VectorOutputVal_makeWidget
        
####################

# There is another SymmMatrix3Widget object in tensorwidgets.py, but
# it's primarily used for the input of tensor-valued parameters in
# properties.  It's sufficiently different that combining the two is
# probably not useful.

class SymmMatrix3Widget:
    def __init__(self, val):
        debug.mainthreadTest()
        self.gtk = gtk.Table(rows=4, columns=4)
        iterator = val.getIterator()
        rowlabels = [None]*3
        collabels = [None]*3
        while not iterator.end():
            comps = iterator.components()
            row = comps[0]
            col = comps[1]
            ijstr = iterator.shortrepr()
            if not rowlabels[row]:
                rowlabels[row] = ijstr[0]
                label = gtk.Label(rowlabels[row]+': ')
                label.set_alignment(1.0, 0.5)
                self.gtk.attach(label, 0,1, row+1,row+2, xoptions=gtk.FILL)
            if not collabels[col]:
                collabels[col] = ijstr[1]
                label = gtk.Label(collabels[col])
                self.gtk.attach(label, col+1,col+2, 0,1,
                                xoptions=gtk.EXPAND|gtk.FILL)
            entry = gtk.Entry()
            gtklogger.setWidgetName(entry, rowlabels[row]+collabels[col])
            entry.set_editable(0)
            self.gtk.attach(entry, col+1,col+2, row+1,row+2,
                            xoptions=gtk.EXPAND|gtk.FILL)
            entry.set_text("%-13.6g" % val[iterator])
            iterator.next()
            
    def show(self):
        debug.mainthreadTest()
        self.gtk.show_all()
    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

def _SymmMatrix_makeWidget(self):
    return SymmMatrix3Widget(self)

symmmatrix.SymmMatrix3Ptr.makeWidget = _SymmMatrix_makeWidget
                

####################

def makeWidget(val):
    try:
        wfunc = val.makeWidget
    except AttributeError:
        return GenericOVWidget(val)
    return wfunc()

