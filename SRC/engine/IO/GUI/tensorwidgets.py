# -*- python -*-
# $RCSfile: tensorwidgets.py,v $
# $Revision: 1.27.18.2 $
# $Author: langer $
# $Date: 2014/05/08 14:39:08 $

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
from ooflib.SWIG.engine import symmmatrix
from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI.matrixparamwidgets import SymmetricMatrixInput

# Used for triclinic materials with symmetric rank two tensors.  There
# is another SymmMatrix3Widget object in outputvalwidgets.py, but it's
# primarily used for display of values.  It's sufficiently different
# that combining the two is probably not useful.
class SymmMatrix3Widget(SymmetricMatrixInput):
    settable = symmmatrix.voigtIndices
    def __init__(self, param, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        SymmetricMatrixInput.__init__(self,"",3,3,value=None,scope=scope,
                                      name=name, verbose=verbose)
        for (k,f) in self.floats.items():
            if k not in self.settable:
                f.gtk.set_editable(0)
                f.gtk.set_sensitive(0)
            else:
                gtklogger.connect(f.gtk, "activate", self.new_value, None)
                gtklogger.connect(f.gtk, "focus_out_event", self.new_value)
        self.set_values(param.value)
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                for i in symmmatrix.voigtIndices:
                    self.floats[i].set_value(self.value.get(*i))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def get_value(self):
        return self.value
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = symmmatrix.SymmMatrix3(
                *[self.floats[i].get_value() for i in \
                  symmmatrix.voigtIndices] )
        finally:
            self.set_values(result)

def _SymmMatrix3Parameter_makeWidget(self, scope=None, verbose=False):
    return SymmMatrix3Widget(self, scope, name=self.name, verbose=verbose)

symmmatrix.SymmMatrix3Parameter.makeWidget = _SymmMatrix3Parameter_makeWidget

# For properties, we want a widget that will return a
# TriclinicRank2Tensor object, but otherwise behaves identically to
# the SymmMatrix3Widget.

class TriclinicRank2TensorParameterWidget(SymmMatrix3Widget):
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = symmmatrix.TriclinicRank2Tensor(
                *[self.floats[i].get_value() for i in symmmatrix.voigtIndices] )
        finally:
            self.set_values(result)
              
def _TR2TP_makeWidget(self, scope=None, verbose=False):
    return TriclinicRank2TensorParameterWidget(self, scope, name=self.name,
                                               verbose=verbose)

symmmatrix.TriclinicRank2TensorParameter.makeWidget = _TR2TP_makeWidget



## for symmetric monoclinic rank two tensors
class MonoclinicSymmWidget(SymmMatrix3Widget):
    settable = ((0,0), (1,1), (2,2), (0,2))
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0,0))
                self.floats[(1,1)].set_value(self.value.get(1,1))
                self.floats[(2,2)].set_value(self.value.get(2,2))
                self.floats[(0,2)].set_value(self.value.get(0,2))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = symmmatrix.MonoclinicRank2Tensor(
                self.floats[(0,0)].get_value(),
                self.floats[(1,1)].get_value(),
                self.floats[(2,2)].get_value(),
                self.floats[(0,2)].get_value())
        finally:
            self.set_values(result)

def _MonoclinicSymmParameter_makeWidget(self, scope=None, verbose=False):
    return MonoclinicSymmWidget(self, scope, name=self.name, verbose=verbose)

symmmatrix.MonoclinicRank2TensorParameter.makeWidget = _MonoclinicSymmParameter_makeWidget


## for symmetric orthorhombic rank two tensors
class OrthorhombicSymmWidget(SymmMatrix3Widget):
    settable = ((0,0), (1,1), (2,2))
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0,0))
                self.floats[(1,1)].set_value(self.value.get(1,1))
                self.floats[(2,2)].set_value(self.value.get(2,2))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = symmmatrix.OrthorhombicRank2Tensor(
                self.floats[(0,0)].get_value(),
                self.floats[(1,1)].get_value(),
                self.floats[(2,2)].get_value())
        finally:
            self.set_values(result)

def _OrthorhombicSymmParameter_makeWidget(self, scope=None, verbose=False):
    return OrthorhombicSymmWidget(self, scope, name=self.name, verbose=verbose)

symmmatrix.OrthorhombicRank2TensorParameter.makeWidget = _OrthorhombicSymmParameter_makeWidget


## For Tetragonal, Trigonal, Hexagonal symmetric rank two tensors
## for symmetric orthorhombic rank two tensors
class IsotropicPlaneSymmWidget(SymmMatrix3Widget):
    ## base class for Tetragonal, Trigonal, Hexagonal SymmWidgets.
    ## the function new_value is overwritten by subclasses
    settable=((0,0), (2,2))
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0,0))
                self.floats[(1,1)].set_value(self.value.get(0,0))
                self.floats[(2,2)].set_value(self.value.get(2,2))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = self.make_tensor(
                xx=self.floats[(0,0)].get_value(),
                zz=self.floats[(2,2)].get_value())
        finally:
            self.set_values(result)

def _IsotropicPlaneSymmParameter_makeWidget(self, scope=None, verbose=False):
    return IsotropicPlaneSymmWidget(self, scope, name=self.name, 
                                    verbose=verbose)

symmmatrix.IsotropicPlaneParameter.makeWidget = _IsotropicPlaneSymmParameter_makeWidget

# Nearly-trivial subclasses, which have functions which can generate a
# tensor of the appropriate type.
class TetragonalSymmWidget(IsotropicPlaneSymmWidget):
    def make_tensor(self, xx, zz):
        return symmmatrix.TetragonalRank2Tensor(xx=xx,zz=zz)

def _TetragonalSymmParameter_makeWidget(self, scope=None, verbose=False):
    return TetragonalSymmWidget(self, scope, name=self.name, verbose=verbose)

symmmatrix.TetragonalRank2TensorParameter.makeWidget = _TetragonalSymmParameter_makeWidget

class TrigonalSymmWidget(IsotropicPlaneSymmWidget):
    def make_tensor(self, xx, zz):
        return symmmatrix.TrigonalRank2Tensor(xx=xx,zz=zz)

def _TrigonalSymmParameter_makeWidget(self, scope=None, verbose=False):
    return TrigonalSymmWidget(self, scope, name=self.name, verbose=verbose)

symmmatrix.TrigonalRank2TensorParameter.makeWidget = _TrigonalSymmParameter_makeWidget

class HexagonalSymmWidget(IsotropicPlaneSymmWidget):
    def make_tensor(self, xx, zz):
        return symmmatrix.HexagonalRank2Tensor(xx=xx,zz=zz)

def _HexagonalSymmParameter_makeWidget(self, scope=None, verbose=False):
    return HexagonalSymmWidget(self, scope, name=self.name, verbose=verbose)

symmmatrix.HexagonalRank2TensorParameter.makeWidget = _HexagonalSymmParameter_makeWidget

## For CUBIC symmetric rank two tensors
class CubicSymmWidget(SymmMatrix3Widget):
    settable = [(0,0)]
    def new_value(self, gtk, event):
        result = self.value
        try:
            result = symmmatrix.CubicRank2Tensor(
                self.floats[(0,0)].get_value() )
        finally:
            self.set_values(result)
        
    def set_values(self, value):
        debug.mainthreadTest()
        self.value = value
        if value is not None:
            self.block_signals()
            try:
                self.floats[(0,0)].set_value(self.value.get(0,0))
                self.floats[(1,1)].set_value(self.value.get(0,0))
                self.floats[(2,2)].set_value(self.value.get(0,0))
            finally:
                self.unblock_signals()
        self.gtk.show_all()
                                          
def _CubicSymmParameter_makeWidget(self, scope=None, verbose=False):
    return CubicSymmWidget(self, scope, name=self.name, verbose=verbose)

symmmatrix.CubicRank2TensorParameter.makeWidget = _CubicSymmParameter_makeWidget
