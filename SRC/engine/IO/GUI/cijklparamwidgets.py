# -*- python -*-
# $RCSfile: cijklparamwidgets.py,v $
# $Revision: 1.25.18.4 $
# $Author: langer $
# $Date: 2014/11/05 16:54:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI.matrixparamwidgets import SymmetricMatrixInput
from ooflib.engine.IO import anisocijkl
from ooflib.engine.IO import isocijkl

CubicRank4TensorCij = anisocijkl.CubicRank4TensorCij
HexagonalRank4TensorCij = anisocijkl.HexagonalRank4TensorCij
TetragonalRank4TensorCij = anisocijkl.TetragonalRank4TensorCij
TrigonalARank4TensorCij = anisocijkl.TrigonalARank4TensorCij
TrigonalBRank4TensorCij = anisocijkl.TrigonalBRank4TensorCij
OrthorhombicRank4TensorCij = anisocijkl.OrthorhombicRank4TensorCij
MonoclinicRank4TensorCij = anisocijkl.MonoclinicRank4TensorCij
TriclinicRank4TensorCij = anisocijkl.TriclinicRank4TensorCij

## TODO: These classes can probably be simplified, putting more stuff
## in the base class and having fewer callbacks.  See
## rank3tensorwidgets.py.

class CijIsoCijklWidget(SymmetricMatrixInput):
    def __init__(self, params, base, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        self.params = params
        SymmetricMatrixInput.__init__(self, 'C', 6,6, value=None, scope=scope,
                                      name=name, verbose=verbose)
        # Block the appropriate ones, and hook up callbacks
        # to handle the c11/c12/c44 synchronization.
        for (k,f) in self.floats.items():
            if k!=(0,0) and k!=(0,1) and k!=(3,3):
                f.gtk.set_editable(0)
                f.gtk.set_sensitive(0)
                
        # Callbacks to cross-connect things so that c44 can be
        # entered, and gets maintained correctly.
        gtklogger.connect(self.floats[(0,0)].gtk, "activate",
                          self.new_c11_or_c12,None)
        gtklogger.connect(self.floats[(0,0)].gtk, "focus_out_event",
                          self.new_c11_or_c12)
        #
        gtklogger.connect(self.floats[(0,1)].gtk, "activate",
                          self.new_c11_or_c12,None)
        gtklogger.connect(self.floats[(0,1)].gtk, "focus_out_event",
                          self.new_c11_or_c12)
        #
        gtklogger.connect(self.floats[(3,3)].gtk, "activate",
                          self.new_c44,None)
        gtklogger.connect(self.floats[(3,3)].gtk, "focus_out_event",
                          self.new_c44)

        self.set_values()

    # Main setting routine.  Use this to guarantee consistency
    # at all times.  Takes c11 and c12, assigns the "values" string
    # (possibly redundantly), computes c44, and writes the duplicate
    # values into the inactive fields of the widget.
    def draw_values(self,c11,c12):
        debug.mainthreadTest()
        self.block_signals()
        try:
            self.values = [c11, c12]
            c44 = 0.5*(c11-c12)
            #
            self.floats[(0,0)].set_value(c11)
            self.floats[(1,1)].set_value(c11)
            self.floats[(2,2)].set_value(c11)
            #
            self.floats[(0,1)].set_value(c12)
            self.floats[(0,2)].set_value(c12)
            self.floats[(1,2)].set_value(c12)
            #
            self.floats[(3,3)].set_value(c44)
            self.floats[(4,4)].set_value(c44)
            self.floats[(5,5)].set_value(c44)
        finally:
            self.unblock_signals()
        
    # This widget understands its "values" to be c11 and c12,
    # in that order, for both setting and getting.
    def set_values(self, values=None):
        self.values = values or [p.value for p in self.params]
        self.draw_values(self.values[0], self.values[1])
        
    def get_values(self):
        for p, v in map(None, self.params, self.values):
            p.value = v

    # Callbacks -- called on return or focus_out.  These must not
    # throw exceptions, or the GTK's focus book-keeping can get
    # screwed up, because the error dialog will want the focus, and
    # the widget whose focus-out-callback this is will not have
    # released it yet, because it didn't return FALSE, because it
    # didn't return, because it threw an exception.  But we call
    # get_value(), which can throw an exception -- do not propagate
    # it.
    def new_c11_or_c12(self,gtk,event):
        c11 = self.params[0].value
        c12 = self.params[1].value
        try:
            c11 = self.floats[(0,0)].get_value()
            c12 = self.floats[(0,1)].get_value()
        finally:
            self.draw_values(c11,c12)

    def new_c44(self,gtk,event):
        c11 = self.params[0].value
        c12 = self.params[1].value
        try:
            c11 = self.floats[(0,0)].get_value()
            c44 = self.floats[(3,3)].get_value()
            c12 = c11-2.0*c44
        finally:
            self.draw_values(c11,c12)

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

regclassfactory.addWidget(isocijkl.IsotropicCijklParameter,
                          isocijkl.IsotropicRank4TensorCij, CijIsoCijklWidget)

############################################################################
############################################################################

class CijCubicCijklWidget(SymmetricMatrixInput):
    def __init__(self, params, base, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        self.params = params
        SymmetricMatrixInput.__init__(self, 'C',6,6, value=None, scope=scope,
                                      name=name, verbose=verbose)
        # Block the appropriate ones, and hook up callbacks
        # to handle the c11/c12/c44 synchronization.
        for (k,f) in self.floats.items():
            if k==(0,0) or k==(0,1) or k==(3,3):
                pass
            else:
                f.gtk.set_editable(0)
                f.gtk.set_sensitive(0)
                
        # Callbacks to cross-connect things so that c44 can be
        # entered, and gets maintained correctly.
        gtklogger.connect(self.floats[(0,0)].gtk, "activate", self.new_c, None)
        gtklogger.connect(self.floats[(0,0)].gtk, "focus_out_event", self.new_c)
        #
        gtklogger.connect(self.floats[(0,1)].gtk, "activate", self.new_c, None)
        gtklogger.connect(self.floats[(0,1)].gtk, "focus_out_event", self.new_c)
        #
        gtklogger.connect(self.floats[(3,3)].gtk, "activate", self.new_c, None)
        gtklogger.connect(self.floats[(3,3)].gtk, "focus_out_event", self.new_c)
        #
        self.set_values()

    # Main setting routine.  Use this to guarantee consistency
    # at all times.  Takes c11 and c12, assigns the "values" string
    # (possibly redundantly), computes c44, and writes the duplicate
    # values into the inactive fields of the widget.
    def draw_values(self,c11,c12,c44):
        debug.mainthreadTest()
        self.block_signals()
        try:
            self.values = [c11, c12, c44]
            #
            self.floats[(0,0)].set_value(c11)
            self.floats[(1,1)].set_value(c11)
            self.floats[(2,2)].set_value(c11)
            #
            self.floats[(0,1)].set_value(c12)
            self.floats[(0,2)].set_value(c12)
            self.floats[(1,2)].set_value(c12)
            #
            self.floats[(3,3)].set_value(c44)
            self.floats[(4,4)].set_value(c44)
            self.floats[(5,5)].set_value(c44)
        finally:
            self.unblock_signals()
    # This widget understands its "values" to be c11, c12, and c44,
    # in that order, for both setting and getting.
    def set_values(self, values=None):
        self.values = values or [p.value for p in self.params]
        self.draw_values(self.values[0], self.values[1], self.values[2])
        
    def get_values(self):
        for p, v in map(None, self.params, self.values):
            p.value = v

    # Callbacks.  Called on return or focus_out.
    def new_c(self,gtk,event):
        c11 = self.params[0].value
        c12 = self.params[1].value
        c44 = self.params[2].value
        try:
            c11 = self.floats[(0,0)].get_value()
            c12 = self.floats[(0,1)].get_value()
            c44 = self.floats[(3,3)].get_value()
        finally:
            self.draw_values(c11,c12,c44)

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

regclassfactory.addWidget(anisocijkl.CubicCijklParameter,
                          anisocijkl.CubicRank4TensorCij,
                          CijCubicCijklWidget)


###########################################################################
###########################################################################
#
# Base class for lower-symmetry Cijkl widgets.  These have
# special behavior, because they're not convertible registered
# types.  The base class also serves as an enforcement mechanism
# for the dictionary-of-values scheme for passing things around.
#
# Child classes must pass in a dictionary ('kset') 
# tuples corresponding to inputs, and value'd by strings corresponding
# to the attribute names in the corresponding Cijkl value class.
class AnisoWidgetBase(SymmetricMatrixInput):
    def __init__(self, params, kset, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        self.params = params
        self.kset = kset
        SymmetricMatrixInput.__init__(self, 'C', 6,6, value=None, scope=scope,
                                      name=name, verbose=verbose)
        #
        # Make default blocks according to the kset dictionary.
        for (k,f) in self.floats.items():
            if k in self.kset:
                pass
            else:
                f.gtk.set_editable(0)
                f.gtk.set_sensitive(0)
        #
        # Connect the "obvious" callbacks.  Child classes may add
        # additional callbacks.
        for k in self.kset:
            # "activate" needs a dummy argument for the "event" slot.
            gtklogger.connect(self.floats[k].gtk, "activate",self.new_c,None)
            gtklogger.connect(self.floats[k].gtk, "focus_out_event",self.new_c)

    # If no default value is set in the registration entry for the
    # property which has this as a value, then this will get called
    # with "None" as the argument, and with no parameters set.
    # "set_values" should probably throw an exception when this
    # happens.
    def set_values(self, values=None):
        self.value = values or self.params.value
        v_dict = {}
        for (k,v) in self.kset.items():
            v_dict[v] = getattr(self.value, v)
        self.draw_values(v_dict)

    # Unlike the convertible case, this routine must return the value.
    def get_value(self):
        self.params.value = self.value
        return self.value

    # Generic callback can live in the base class.
    def new_c(self,gtk,event):
        v_dict = {}
        for v in self.kset.values():
            v_dict[v] = getattr(self.params.value, v)
        try:
            for (k,v) in self.kset.items():
                v_dict[v] = self.floats[k].get_value()
        finally:
            self.draw_values(v_dict)

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()
        
# # # # # # # # # ################################### # # # # # # # # # # 
# Hexagonal


class HexagonalCijklWidget(AnisoWidgetBase):
    def __init__(self, params, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        kset = {(0,0): 'c11', (0,1): 'c12', (0,2): 'c13',
                (2,2): 'c33', (3,3): 'c44' }
        AnisoWidgetBase.__init__(self, params, kset, scope=scope, name=name,
                                 verbose=verbose)
        #
        # Base class will have blocked c66, so unblock it.
        self.floats[(5,5)].gtk.set_editable(1)
        self.floats[(5,5)].gtk.set_sensitive(1)
            
        #  ... and connect a special callback.
        gtklogger.connect(self.floats[(5,5)].gtk, "activate",
                          self.new_c66, None)
        gtklogger.connect(self.floats[(5,5)].gtk, "focus_out_event",
                          self.new_c66)
        #
        self.set_values()

    # c11 updates c22, c44 updates c55, c13 updates c23, and
    # c66=0.5*(c11-c12)
    def draw_values(self,var_dict):
        debug.mainthreadTest()
        self.value = HexagonalRank4TensorCij(var_dict['c11'], var_dict['c12'],
                                         var_dict['c13'], var_dict['c33'],
                                         var_dict['c44'])
        #
        self.block_signals()
        try:
            for (k,v) in self.kset.items():
                self.floats[k].set_value(var_dict[v])

            # Then do the extra, special ones.
            self.floats[(1,1)].set_value(var_dict['c11'])
            self.floats[(1,2)].set_value(var_dict['c13'])
            self.floats[(4,4)].set_value(var_dict['c44'])
            self.floats[(5,5)].set_value(0.5*(var_dict['c11']-var_dict['c12']))
        finally:
            self.unblock_signals()
    def new_c66(self,gtk,event):
        v_dict={}
        for v in self.kset.values():
            v_dict[v] = getattr(self.params.value, v)
        try:
            for (k,v) in self.kset.items():
                v_dict[v] = self.floats[k].get_value()
            c11 = v_dict['c11']
            c66 = self.floats[(5,5)].get_value()
            v_dict['c12'] = c11-2.0*c66
        finally:
            self.draw_values(v_dict)


def HexCijklParam_makeWidget(self, scope, verbose=False):
    return HexagonalCijklWidget(self, scope, verbose=verbose)

anisocijkl.HexagonalCijklParameter.makeWidget = HexCijklParam_makeWidget
    

# # # # # # # # # ################################### # # # # # # # # # # 
# Tetragonal.

class TetragonalCijklWidget(AnisoWidgetBase):
    def __init__(self, params, scope=None, name=None, verbose=False):
        kset = {(0,0): 'c11', (0,1): 'c12', (0,2): 'c13', (0,5): 'c16',
                (2,2): 'c33', (3,3): 'c44', (5,5): 'c66' }
        AnisoWidgetBase.__init__(self, params, kset, scope=scope, name=name,
                                 verbose=verbose)
        #
        self.set_values()

    # Tetragonal case, c13 updates c23, and c11 updates c12, and
    # c44 updates c55.
    # "var_dict" is indexed by the strings which are values in
    # self.kset.
    def draw_values(self,var_dict):
        debug.mainthreadTest()
        self.value = TetragonalRank4TensorCij(var_dict['c11'], var_dict['c12'],
                                          var_dict['c13'], var_dict['c33'],
                                          var_dict['c44'], var_dict['c66'],
                                          var_dict['c16'])
        #
        self.block_signals()
        try:
            for (k,v) in self.kset.items():
                self.floats[k].set_value(var_dict[v])

            # Then do the extra, special ones.
            self.floats[(1,1)].set_value(var_dict['c11'])
            self.floats[(1,2)].set_value(var_dict['c13'])
            self.floats[(4,4)].set_value(var_dict['c44'])
            self.floats[(1,5)].set_value(-var_dict['c16'])
        finally:
            self.unblock_signals()
def TetCijklParam_makeWidget(self, scope, verbose=False):
    return TetragonalCijklWidget(self, scope, verbose=verbose)

anisocijkl.TetragonalCijklParameter.makeWidget = TetCijklParam_makeWidget

# # # # # # # # # ################################### # # # # # # # # # #
# Trigonal A

class TrigonalACijklWidget(AnisoWidgetBase):
    def __init__(self, params, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        kset = {(0,0): 'c11', (0,1): 'c12', (0,2): 'c13',
                (2,2): 'c33', (3,3): 'c44', (0,3): 'c14', (0,4): 'c15' }
        AnisoWidgetBase.__init__(self, params, kset, scope=scope, name=name,
                                 verbose=verbose)
        #
        self.floats[(5,5)].gtk.set_editable(1)
        self.floats[(5,5)].gtk.set_sensitive(1)
        #
        gtklogger.connect(self.floats[(5,5)].gtk, "activate",
                          self.new_c66, None)
        gtklogger.connect(self.floats[(5,5)].gtk, "focus_out_event",
                          self.new_c66)
        #
        self.set_values()

    # TrigonalA.  c11 updates c22, c13 updates c23, c44 updates c55, and
    # c66 = 0.5*(c11-c12).  
    def draw_values(self,var_dict):
        debug.mainthreadTest()
        self.value = TrigonalARank4TensorCij(var_dict['c11'], var_dict['c12'],
                                         var_dict['c13'], var_dict['c33'],
                                         var_dict['c44'], var_dict['c14'],
                                         var_dict['c15'])
        #
        self.block_signals()
        try:
            for (k,v) in self.kset.items():
                self.floats[k].set_value(var_dict[v])

            # Then do the extra, special ones.
            self.floats[(1,1)].set_value(var_dict['c11'])
            self.floats[(1,2)].set_value(var_dict['c13'])
            self.floats[(4,4)].set_value(var_dict['c44'])
            # Propagate c14 to the subsidiary entries.
            self.floats[(1,3)].set_value(-var_dict['c14'])
            self.floats[(4,5)].set_value(var_dict['c14'])
            # And similarly, c15.
            self.floats[(1,4)].set_value(-var_dict['c15'])
            self.floats[(3,5)].set_value(-var_dict['c15'])
            #
            c66=0.5*(var_dict['c11']-var_dict['c12'])
            self.floats[(5,5)].set_value(c66)
        finally:
            self.unblock_signals()

    def new_c66(self, gtk, event):
        v_dict = {}
        for v in self.kset.values():
            v_dict[v] = getattr(self.params.value, v)
        try:
            for (k,v) in self.kset.items():
                v_dict[v] = self.floats[k].get_value()
            c11 = v_dict['c11']
            c66 = self.floats[(5,5)].get_value()
            v_dict['c12'] = c11-2.0*c66
        finally:
            self.draw_values(v_dict)
   
def TrigACijklParam_makeWidget(self, scope, verbose=False):
    return TrigonalACijklWidget(self, scope, verbose=verbose)

anisocijkl.TrigonalACijklParameter.makeWidget = TrigACijklParam_makeWidget



# # # # # # # # # ################################### # # # # # # # # # #
# Trigonal B

class TrigonalBCijklWidget(AnisoWidgetBase):
    def __init__(self, params, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        kset = {(0,0): 'c11', (0,1): 'c12', (0,2): 'c13',
                (2,2): 'c33', (3,3): 'c44', (0,3): 'c14' }
        AnisoWidgetBase.__init__(self, params, kset, scope=scope, name=name,
                                 verbose=verbose)
        #
        self.floats[(5,5)].gtk.set_editable(1)
        self.floats[(5,5)].gtk.set_sensitive(1)
        #
        gtklogger.connect(self.floats[(5,5)].gtk, "activate",
                          self.new_c66, None)
        gtklogger.connect(self.floats[(5,5)].gtk, "focus_out_event",
                          self.new_c66)
        #
        self.set_values()

    # TrigonalB.  c11 updates c22, c13 updates c23, c44 updates c55, and
    # c66 = 0.5*(c11-c12).  
    def draw_values(self,var_dict):
        debug.mainthreadTest()
        self.value = TrigonalBRank4TensorCij(var_dict['c11'], var_dict['c12'],
                                         var_dict['c13'], var_dict['c33'],
                                         var_dict['c44'], var_dict['c14'])
        #
        self.block_signals()
        try:
            for (k,v) in self.kset.items():
                self.floats[k].set_value(var_dict[v])

            # Then do the extra, special ones.
            self.floats[(1,1)].set_value(var_dict['c11'])
            self.floats[(1,2)].set_value(var_dict['c13'])
            self.floats[(4,4)].set_value(var_dict['c44'])
            # Propagate c14 to the subsidiary entries.
            self.floats[(1,3)].set_value(-var_dict['c14'])
            self.floats[(4,5)].set_value(var_dict['c14'])
            #
            c66=0.5*(var_dict['c11']-var_dict['c12'])
            self.floats[(5,5)].set_value(c66)
        finally:
            self.unblock_signals()

    def new_c66(self, gtk, event):
        v_dict = {}
        for v in self.kset.values():
            v_dict[v] = getattr(self.params.value, v)
        try:
            for (k,v) in self.kset.items():
                v_dict[v] = self.floats[k].get_value()
            c11 = v_dict['c11']
            c66 = self.floats[(5,5)].get_value()
            v_dict['c12'] = c11-2.0*c66
        finally:
            self.draw_values(v_dict)
   
def TrigBCijklParam_makeWidget(self, scope, verbose=False):
    return TrigonalBCijklWidget(self, scope, verbose=verbose)

anisocijkl.TrigonalBCijklParameter.makeWidget = TrigBCijklParam_makeWidget



# # # # # # # # # ################################### # # # # # # # # # #
# Orthorhombic

class OrthorhombicCijklWidget(AnisoWidgetBase):
    def __init__(self, params, scope=None, name=None, verbose=False):
        kset = {(0,0): 'c11', (0,1): 'c12', (0,2): 'c13',
                (1,1): 'c22', (1,2): 'c23',
                (2,2): 'c33', (3,3): 'c44', (4,4): 'c55',
                (5,5): 'c66' }
        AnisoWidgetBase.__init__(self, params, kset, scope=scope, name=name,
                                 verbose=verbose)
        #
        self.set_values()

    # Orthorhombic.  No cross-connections, just straight entries.
    def draw_values(self,var_dict):
        debug.mainthreadTest()
        self.value = OrthorhombicRank4TensorCij(var_dict['c11'], var_dict['c12'],
                                            var_dict['c13'], var_dict['c22'],
                                            var_dict['c23'], var_dict['c33'],
                                            var_dict['c44'], var_dict['c55'],
                                            var_dict['c66'])
        #
        self.block_signals()
        try:
            for (k,v) in self.kset.items():
                self.floats[k].set_value(var_dict[v])
        finally:
            self.unblock_signals()

def OrthCijklParam_makeWidget(self, scope, verbose=False):
    return OrthorhombicCijklWidget(self, scope, verbose=verbose)

anisocijkl.OrthorhombicCijklParameter.makeWidget = OrthCijklParam_makeWidget


# # # # # # # # # ################################### # # # # # # # # # # 
# Monoclinic

class MonoclinicCijklWidget(AnisoWidgetBase):
    def __init__(self, params, scope=None, name=None, verbose=False):
        kset = {(0,0): 'c11', (0,1): 'c12', (0,2): 'c13', (0,4): 'c15',
                (1,1): 'c22', (1,2): 'c23', (1,4): 'c25',
                (2,2): 'c33', (2,4): 'c35', 
                (3,3): 'c44', (3,5): 'c46', (4,4): 'c55', (5,5): 'c66' }
        AnisoWidgetBase.__init__(self, params, kset, scope=scope, name=name,
                                 verbose=verbose)
        #
        self.set_values()

    # Monoclinic.  No cross-connections, just straight entries.
    def draw_values(self,var_dict):
        debug.mainthreadTest()
        self.value = MonoclinicRank4TensorCij(var_dict['c11'], var_dict['c12'],
                                          var_dict['c13'], var_dict['c15'],
                                          var_dict['c22'], var_dict['c23'],
                                          var_dict['c25'], var_dict['c33'],
                                          var_dict['c35'], var_dict['c44'],
                                          var_dict['c46'], var_dict['c55'],
                                          var_dict['c66'])
        #
        self.block_signals()
        try:
            for (k,v) in self.kset.items():
                self.floats[k].set_value(var_dict[v])
        finally:
            self.unblock_signals()
        
def MonoCijklParam_makeWidget(self, scope, verbose=False):
    return MonoclinicCijklWidget(self, scope, verbose=verbose)

anisocijkl.MonoclinicCijklParameter.makeWidget = MonoCijklParam_makeWidget


# # # # # # # # # ################################### # # # # # # # # # # 
# Triclinic, the general case.

class TriclinicCijklWidget(AnisoWidgetBase):
    def __init__(self, params, scope=None, name=None, verbose=False):
        kset = {(0,0): 'c11', (0,1): 'c12', (0,2): 'c13', (0,3): 'c14',
                (0,4): 'c15', (0,5): 'c16', (1,1): 'c22', (1,2): 'c23',
                (1,3): 'c24', (1,4): 'c25', (1,5): 'c26', (2,2): 'c33',
                (2,3): 'c34', (2,4): 'c35', (2,5): 'c36', (3,3): 'c44',
                (3,4): 'c45', (3,5): 'c46', (4,4): 'c55', (4,5): 'c56',
                (5,5): 'c66' }
        AnisoWidgetBase.__init__(self, params, kset, scope=scope, name=name,
                                 verbose=verbose)
        #
        self.set_values()

    # Monoclinic.  No cross-connections, just straight entries.
    def draw_values(self,var_dict):
        debug.mainthreadTest()
        self.value = TriclinicRank4TensorCij(var_dict['c11'], var_dict['c12'],
                                         var_dict['c13'], var_dict['c14'],
                                         var_dict['c15'], var_dict['c16'],
                                         var_dict['c22'],
                                         var_dict['c23'], var_dict['c24'],
                                         var_dict['c25'], var_dict['c26'],
                                         var_dict['c33'], var_dict['c34'],
                                         var_dict['c35'], var_dict['c36'],
                                         var_dict['c44'], var_dict['c45'],
                                         var_dict['c46'],
                                         var_dict['c55'], var_dict['c56'],
                                         var_dict['c66'],
                                    )
        #
        self.block_signals()
        try:
            for (k,v) in self.kset.items():
                self.floats[k].set_value(var_dict[v])
        finally:
            self.unblock_signals()
        
def TriCijklParam_makeWidget(self, scope, verbose=False):
    return TriclinicCijklWidget(self, scope, verbose=verbose)

anisocijkl.TriclinicCijklParameter.makeWidget = TriCijklParam_makeWidget

