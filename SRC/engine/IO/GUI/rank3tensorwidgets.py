# -*- python -*-
# $RCSfile: rank3tensorwidgets.py,v $
# $Revision: 1.24.18.2 $
# $Author: langer $
# $Date: 2014/05/15 15:06:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Contains size-specific descendants of SymmetricMatrixInput,
# which have as values objects of the SymmMatrix type
# from SWIG.engine.SymmMatrix.


from ooflib.SWIG.engine import fieldindex
from ooflib.SWIG.engine import rank3tensor
from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import matrixparamwidgets

MatrixInput = matrixparamwidgets.MatrixInput

## Subclasses of Rank3TensorWidget don't have to define an __init__,
## if they have a class-level list called "excluded" which lists the
## settable ij values.  

class Rank3TensorWidget(MatrixInput):
    def __init__(self, param, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        MatrixInput.__init__(self, "", 3,6, value=None, scope=scope, name=name,
                             verbose=verbose)
        for (k,f) in self.floats.items():
            if k not in self.excluded:
                f.gtk.set_editable(0)
                f.gtk.set_sensitive(0)
            else:
                gtklogger.connect(f.gtk, "activate", self.new_value, None)
                gtklogger.connect(f.gtk, "focus_out_event", self.new_value)
        self.set_values(param.value)
    def get_value(self):
        return self.value

########################################

class C1Rank3TensorWidget(Rank3TensorWidget):
    # Doesn't use Rank3TensorWidget.__init__ because the "excluded"
    # list is too long.
    def __init__(self, param, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        MatrixInput.__init__(self, "", 3, 6, value=None, scope=scope, name=name,
                             verbose=verbose)
            
        for i in range(3):
            for j in range(6):
                gtklogger.connect(self.floats[(i, j)].gtk, 
                                  "activate", self.new_value, None)
                gtklogger.connect(self.floats[(i, j)].gtk,
                                  "focus_out_event", self.new_value)
        
        self.set_values(param.value)
    
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0,0, 0))
                self.floats[(0,1)].set_value(self.value.get(0,1, 1))
                self.floats[(0,2)].set_value(self.value.get(0,2, 2))
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1))
                self.floats[(0,4)].set_value(self.value.get(0,0, 2))
                self.floats[(0,5)].set_value(self.value.get(0,0, 1))
                ##
                self.floats[(1,0)].set_value(self.value.get(1,0, 0))
                self.floats[(1,1)].set_value(self.value.get(1,1, 1))
                self.floats[(1,2)].set_value(self.value.get(1,2, 2))
                self.floats[(1,3)].set_value(self.value.get(1, 2, 1))
                self.floats[(1,4)].set_value(self.value.get(1,0, 2))
                self.floats[(1,5)].set_value(self.value.get(1,0, 1))
                ##
                self.floats[(2,0)].set_value(self.value.get(2,0, 0))
                self.floats[(2,1)].set_value(self.value.get(2,1, 1))
                self.floats[(2,2)].set_value(self.value.get(2,2, 2))
                self.floats[(2,3)].set_value(self.value.get(2, 2, 1))
                self.floats[(2,4)].set_value(self.value.get(2,0, 2))
                self.floats[(2,5)].set_value(self.value.get(2,0, 1))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C1Rank3Tensor(
                d11= self.floats[(0,0)].get_value(),
                d12 = self.floats[(0,1)].get_value(),
                d13 = self.floats[(0,2)].get_value(),
                d14 = self.floats[(0,3)].get_value(),
                d15 = self.floats[(0,4)].get_value(),
                d16 = self.floats[(0,5)].get_value(),
                d21 = self.floats[(1,0)].get_value(),
                d22 = self.floats[(1,1)].get_value(),
                d23 = self.floats[(1,2)].get_value(),
                d24 = self.floats[(1,3)].get_value(),
                d25 = self.floats[(1,4)].get_value(),
                d26 = self.floats[(1,5)].get_value(),
                d31 = self.floats[(2,0)].get_value(),
                d32 = self.floats[(2,1)].get_value(),
                d33 = self.floats[(2,2)].get_value(),
                d34 = self.floats[(2,3)].get_value(),
                d35 = self.floats[(2,4)].get_value(),
                d36 = self.floats[(2,5)].get_value()
                )
        finally:
            self.set_values(result)

def _C1Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C1Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C1Rank3TensorParameter.makeWidget = _C1Rank3Tensor_makeWidget


########################################

class C2Rank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,3), (0,5), (1,0), (1,1), (1,2), (1,4), (2,3), (2,5)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1))
                self.floats[(0,5)].set_value(self.value.get(0,0, 1))
                ##
                self.floats[(1,0)].set_value(self.value.get(1,0, 0))
                self.floats[(1,1)].set_value(self.value.get(1,1, 1))
                self.floats[(1,2)].set_value(self.value.get(1,2, 2))
                self.floats[(1,4)].set_value(self.value.get(1,0, 2))
                ##
                self.floats[(2,3)].set_value(self.value.get(2, 2, 1))
                self.floats[(2,5)].set_value(self.value.get(2,0, 1))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C2Rank3Tensor(
                d14 = self.floats[(0,3)].get_value(),
                d16 = self.floats[(0,5)].get_value(),
                d21 = self.floats[(1,0)].get_value(),
                d22 = self.floats[(1,1)].get_value(),
                d23 = self.floats[(1,2)].get_value(),
                d25 = self.floats[(1,4)].get_value(),
                d34 = self.floats[(2,3)].get_value(),
                d36 = self.floats[(2,5)].get_value()
                )
        finally:
            self.set_values(result)

def _C2Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C2Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C2Rank3TensorParameter.makeWidget = _C2Rank3Tensor_makeWidget


########################################

class CsRank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,0), (0,1), (0,2), (0,4), (1,3),
                (1,5), (2,0), (2,1), (2,2), (2,4)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0,0, 0))
                self.floats[(0,1)].set_value(self.value.get(0,1, 1))
                self.floats[(0,2)].set_value(self.value.get(0,2, 2))
                self.floats[(0,4)].set_value(self.value.get(0,0, 2))
                ##
                self.floats[(1,3)].set_value(self.value.get(1, 2, 1))
                self.floats[(1,5)].set_value(self.value.get(1,0, 1))
                ##
                self.floats[(2,0)].set_value(self.value.get(2,0, 0))
                self.floats[(2,1)].set_value(self.value.get(2,1, 1))
                self.floats[(2,2)].set_value(self.value.get(2,2, 2))
                self.floats[(2,4)].set_value(self.value.get(2,0, 2))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.CsRank3Tensor(
                d11= self.floats[(0,0)].get_value(),
                d12 = self.floats[(0,1)].get_value(),
                d13 = self.floats[(0,2)].get_value(),
                d15 = self.floats[(0,4)].get_value(),
                d24 = self.floats[(1,3)].get_value(),
                d26 = self.floats[(1,5)].get_value(),
                d31 = self.floats[(2,0)].get_value(),
                d32 = self.floats[(2,1)].get_value(),
                d33 = self.floats[(2,2)].get_value(),
                d35 = self.floats[(2,4)].get_value()
                )
        finally:
            self.set_values(result)

def _CsRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return CsRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.CsRank3TensorParameter.makeWidget = _CsRank3Tensor_makeWidget


########################################

class D2Rank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,3), (1,4), (2,5)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1))
                self.floats[(1,4)].set_value(self.value.get(1,0, 2))
                self.floats[(2,5)].set_value(self.value.get(2,0, 1))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.D2Rank3Tensor(
                d14 = self.floats[(0,3)].get_value(),
                d25 = self.floats[(1,4)].get_value(),
                d36 = self.floats[(2,5)].get_value()
                )
        finally:
            self.set_values(result)

def _D2Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return D2Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.D2Rank3TensorParameter.makeWidget = _D2Rank3Tensor_makeWidget

########################################

class C2vRank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,4), (1,3), (2,0), (2,1), (2,2)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,4)].set_value(self.value.get(0,0, 2))
                self.floats[(1,3)].set_value(self.value.get(1, 2, 1))
                self.floats[(2,0)].set_value(self.value.get(2,0, 0))
                self.floats[(2,1)].set_value(self.value.get(2,1, 1))
                self.floats[(2,2)].set_value(self.value.get(2,2, 2))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C2vRank3Tensor(
                d15 = self.floats[(0,4)].get_value(),
                d24 = self.floats[(1,3)].get_value(),
                d31 = self.floats[(2,0)].get_value(),
                d32 = self.floats[(2,1)].get_value(),
                d33 = self.floats[(2,2)].get_value()
                )
        finally:
            self.set_values(result)

def _C2vRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C2vRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C2vRank3TensorParameter.makeWidget = _C2vRank3Tensor_makeWidget

########################################

class C4Rank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,3), (0,4), (2,0), (2,2)]
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C4Rank3Tensor(
                d14 = self.floats[(0,3)].get_value(),
                d15 = self.floats[(0,4)].get_value(),
                d31 = self.floats[(2,0)].get_value(),
                d33 = self.floats[(2,2)].get_value() )
        finally:
            self.set_values(result)
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1))
                self.floats[(1,4)].set_value(-self.value.get(0,2,1))
                ##
                self.floats[(2,0)].set_value(self.value.get(2,0, 0))
                self.floats[(2,1)].set_value(self.value.get(2,0, 0))
                ##
                self.floats[(0,4)].set_value(self.value.get(0,0, 2))
                self.floats[(1,3)].set_value(self.value.get(0,0, 2))
                ##
                self.floats[(2,2)].set_value(self.value.get(2,2, 2))
            finally:
                self.unblock_signals()
        self.gtk.show_all()

def _C4Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C4Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C4Rank3TensorParameter.makeWidget = _C4Rank3Tensor_makeWidget

########################################

class C4iRank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,3), (0,4), (2,0), (2,5)]
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1))
                self.floats[(1,4)].set_value(self.value.get(0,2,1))
                ##
                self.floats[(2,0)].set_value(self.value.get(2,0, 0))
                self.floats[(2,1)].set_value(-self.value.get(2,0, 0))
                ##
                self.floats[(0,4)].set_value(self.value.get(0,0, 2))
                self.floats[(1,3)].set_value(-self.value.get(0,0, 2))
                ##
                self.floats[(2,5)].set_value(self.value.get(2,0, 1))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C4iRank3Tensor(
                d14 = self.floats[(0,3)].get_value(),
                d15 = self.floats[(0,4)].get_value(),
                d31 = self.floats[(2,0)].get_value(),
                d36 = self.floats[(2,5)].get_value()
                )
        finally:
            self.set_values(result)

def _C4iRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C4iRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C4iRank3TensorParameter.makeWidget = _C4iRank3Tensor_makeWidget


########################################

class D4Rank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,3)]
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1))
                self.floats[(1,4)].set_value(-self.value.get(0,2,1))
            finally:
                self.unblock_signals()
            ##
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.D4Rank3Tensor(
                d14 = self.floats[(0,3)].get_value()
                )
        finally:
            self.set_values(result)

def _D4Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return D4Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.D4Rank3TensorParameter.makeWidget = _D4Rank3Tensor_makeWidget


########################################

class C4vRank3TensorWidget(Rank3TensorWidget):
    excluded = [(2,0), (2,2), (0,4)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(2,0)].set_value(self.value.get(2,0, 0))
                self.floats[(2,1)].set_value(self.value.get(2,0, 0))
                self.floats[(2,2)].set_value(self.value.get(2,2,2))
                self.floats[(0,4)].set_value(self.value.get(0,0,2))
                self.floats[(1,3)].set_value(self.value.get(1,1,2))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C4vRank3Tensor(
                d15 = self.floats[(0,4)].get_value(),
                d31= self.floats[(2,0)].get_value(),
                d33 = self.floats[(2,2)].get_value())
        finally:
            self.set_values(result)

def _C4vRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C4vRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C4vRank3TensorParameter.makeWidget = _C4vRank3Tensor_makeWidget


########################################

class D2dRank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,3), (2,5)]
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1))
                self.floats[(1,4)].set_value(self.value.get(0,2,1))
                self.floats[(2,5)].set_value(self.value.get(2,0, 1))
            finally:
                self.unblock_signals()

        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.D2dRank3Tensor(
                d14 = self.floats[(0,3)].get_value(),
                d36 = self.floats[(2,5)].get_value()
                )
        finally:
            self.set_values(result)

def _D2dRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return D2dRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.D2dRank3TensorParameter.makeWidget = _D2dRank3Tensor_makeWidget

########################################

class C3Rank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,0), (0,3), (0,4), (1,1), (2,0), (2,2)]
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0, 0, 0)) # d11
                self.floats[(0,1)].set_value(-self.value.get(0, 0, 0)) # -d11
                self.floats[(1,5)].set_value(-2*self.value.get(0, 0, 0)) # 2*d11
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1)) # d14
                self.floats[(1,4)].set_value(-self.value.get(0, 2, 1)) #-d14
                self.floats[(0,4)].set_value(self.value.get(0, 0, 2)) # d15
                self.floats[(1,3)].set_value(self.value.get(0, 0, 2)) # d15
                self.floats[(1,1)].set_value(self.value.get(1,1,1)) # d22
                self.floats[(1,0)].set_value(-self.value.get(1,1,1)) # -d22
                self.floats[(0,5)].set_value(-2.0*self.value.get(1,1,1)) #-2*d22
                self.floats[(2,0)].set_value(self.value.get(2,0,0)) # d31
                self.floats[(2,1)].set_value(self.value.get(2,0,0)) # d31
                self.floats[(2,2)].set_value(self.value.get(2,2,2)) # d33
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C3Rank3Tensor(
                d11 = self.floats[(0,0)].get_value(),
                d14 = self.floats[(0,3)].get_value(),
                d15 = self.floats[(0,4)].get_value(),
                d22 = self.floats[(1,1)].get_value(),
                d31 = self.floats[(2,0)].get_value(),
                d33 = self.floats[(2,2)].get_value()
                )
        finally:
            self.set_values(result)

def _C3Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C3Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C3Rank3TensorParameter.makeWidget = _C3Rank3Tensor_makeWidget

########################################

class D3Rank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,0), (0,3)]
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0, 0, 0)) ## d11
                self.floats[(0,1)].set_value(-self.value.get(0, 0, 0)) ## -d11
                self.floats[(1,5)].set_value(-2*self.value.get(0, 0, 0))## 2*d11
                self.floats[(0,3)].set_value(self.value.get(0, 2, 1)) ## d14
                self.floats[(1,4)].set_value(-self.value.get(0, 2, 1))##-d14
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.D3Rank3Tensor(
                d11 = self.floats[(0,0)].get_value(),
                d14 = self.floats[(0,3)].get_value()
                )
        finally:
            self.set_values(result)

def _D3Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return D3Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.D3Rank3TensorParameter.makeWidget = _D3Rank3Tensor_makeWidget



########################################

class C3vRank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,4), (1,1), (2,0), (2,2)]
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,4)].set_value(self.value.get(0, 0, 2)) ## d15
                self.floats[(1,3)].set_value(self.value.get(0, 0, 2)) ## d15
                self.floats[(1,1)].set_value(self.value.get(1,1,1)) ## d22
                self.floats[(1,0)].set_value(-self.value.get(1,1,1)) ## -d22
                self.floats[(0,5)].set_value(-2.0*self.value.get(1,1,1))##-2*d22
                self.floats[(2,0)].set_value(self.value.get(2,0,0)) ## d31
                self.floats[(2,1)].set_value(self.value.get(2,0,0)) ## d31
                self.floats[(2,2)].set_value(self.value.get(2,2,2)) ## d33
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C3vRank3Tensor(
                d15 = self.floats[(0,4)].get_value(),
                d22 = self.floats[(1,1)].get_value(),
                d31 = self.floats[(2,0)].get_value(),
                d33 = self.floats[(2,2)].get_value()
                )
        finally:
            self.set_values(result)

def _C3vRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C3vRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C3vRank3TensorParameter.makeWidget = _C3vRank3Tensor_makeWidget


########################################

class C6Rank3TensorWidget(Rank3TensorWidget):
    excluded = [(2,0), (2,2), (0,4), (0,3)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(2,0)].set_value(self.value.get(2,0, 0))
                self.floats[(2,1)].set_value(self.value.get(2,0, 0))
                self.floats[(2,2)].set_value(self.value.get(2,2,2))
                self.floats[(0,4)].set_value(self.value.get(0,0,2))
                self.floats[(1,3)].set_value(self.value.get(1,1,2))
                self.floats[(0,3)].set_value(self.value.get(0,2,1))
                self.floats[(1,4)].set_value(-self.value.get(0,2,1))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C6Rank3Tensor(
                d14 = self.floats[(0,3)].get_value(),
                d15 = self.floats[(0,4)].get_value(),
                d31 = self.floats[(2,0)].get_value(),
                d33 = self.floats[(2,2)].get_value()
                )
        finally:
            self.set_values(result)

def _C6Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C6Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C6Rank3TensorParameter.makeWidget = _C6Rank3Tensor_makeWidget



########################################

class D6iRank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,0), (1,1)]
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0, 0, 0)) ## d11
                self.floats[(0,1)].set_value(-self.value.get(0, 0, 0)) ## -d11
                self.floats[(1,5)].set_value(-2*self.value.get(0, 0, 0))## 2*d11

                self.floats[(1,1)].set_value(self.value.get(1,1,1)) ## d22
                self.floats[(1,0)].set_value(-self.value.get(1,1,1)) ## -d22
                self.floats[(0,5)].set_value(-2.0*self.value.get(1,1,1))##-2*d22
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.D6iRank3Tensor(
                d11 = self.floats[(0,0)].get_value(),
                d22 = self.floats[(1,1)].get_value()
                )
        finally:
            self.set_values(result)

def _D6iRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return D6iRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.D6iRank3TensorParameter.makeWidget = _D6iRank3Tensor_makeWidget




########################################

class D6Rank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,3)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,3)].set_value(self.value.get(0,2,1))
                self.floats[(1,4)].set_value(-self.value.get(0,2,1))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.D6Rank3Tensor(
                d14 = self.floats[(0,3)].get_value()
                )
        finally:
            self.set_values(result)

def _D6Rank3Tensor_makeWidget(self, scope=None, verbose=False):
    return D6Rank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.D6Rank3TensorParameter.makeWidget = _D6Rank3Tensor_makeWidget




########################################

class C6vRank3TensorWidget(Rank3TensorWidget):
    excluded = [(2,0), (2,2), (0,4)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(2,0)].set_value(self.value.get(2,0, 0))
                self.floats[(2,1)].set_value(self.value.get(2,0, 0))
                self.floats[(2,2)].set_value(self.value.get(2,2,2))
                self.floats[(0,4)].set_value(self.value.get(0,0,2))
                self.floats[(1,3)].set_value(self.value.get(1,1,2))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.C6vRank3Tensor(
                d15 = self.floats[(0,4)].get_value(),
                d31= self.floats[(2,0)].get_value(),
                d33 = self.floats[(2,2)].get_value()   )
        finally:
            self.set_values(result)

def _C6vRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return C6vRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.C6vRank3TensorParameter.makeWidget = _C6vRank3Tensor_makeWidget



########################################

class D3hRank3TensorWidget(Rank3TensorWidget):
    excluded = [(1,1)]
    def set_values(self, value): 
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(1,1)].set_value(self.value.get(1,1,1)) ## d22
                self.floats[(1,0)].set_value(-self.value.get(1,1,1)) ## -d22
                self.floats[(0,5)].set_value(-2.0*self.value.get(1,1,1))##-2*d22
            finally:
                self.unblock_signals()

        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.D3hRank3Tensor(
                d22 = self.floats[(1,1)].get_value()
                )
        finally:
            self.set_values(result)

def _D3hRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return D3hRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.D3hRank3TensorParameter.makeWidget = _D3hRank3Tensor_makeWidget


########################################

class TdRank3TensorWidget(Rank3TensorWidget):
    excluded = [(0,3)]
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,3)].set_value(self.value.get(0,2,1))
                self.floats[(1,4)].set_value(self.value.get(0,2,1))
                self.floats[(2,5)].set_value(self.value.get(0,2,1))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def get_value(self):
        return self.value

    def new_value(self, gtk, event):
        result = self.value
        try:
            result = rank3tensor.TdRank3Tensor(
                d14 = self.floats[(0,3)].get_value()
                )
        finally:
            self.set_values(result)

def _TdRank3Tensor_makeWidget(self, scope=None, verbose=False):
    return TdRank3TensorWidget(self, scope, name=self.name, verbose=verbose)

rank3tensor.TdRank3TensorParameter.makeWidget = _TdRank3Tensor_makeWidget


