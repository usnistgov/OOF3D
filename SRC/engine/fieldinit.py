# -*- python -*-
# $RCSfile: fieldinit.py,v $
# $Revision: 1.47.2.4 $
# $Author: langer $
# $Date: 2014/04/08 21:00:57 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.engine import field
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common import strfunction
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.common.IO import placeholder
import ooflib.engine.mesh
import string
import struct
import types

# FieldInit subclasses must be derived from FieldInit *and* from
# RegisteredClass.

class FieldInit:
    def apply(self, femesh, field, time=None, singleFieldDef=False):
        if singleFieldDef:
            # The purpose of calling node.fieldDefCount is to ensure
            # that we don't set the value of a field that is defined
            # in more than one subproblem when that field gets defined
            # on the second subproblem.  Doing so would wipe out a
            # value that might have been set by the first subproblem.
            for node in femesh.funcnodes():
                if node.fieldDefCount(field)==1:
                    position = node.position()
                    for i in range(field.ndof()): # field component
                        field.setvalue(femesh, node, i,
                                       self.func(position, time, i))
        else:
            for node in femesh.funcnodes():
                if node.hasField(field):
                    position = node.position()
                    for i in range(field.ndof()): # field component
                        field.setvalue(femesh, node, i,
                                       self.func(position, time, i))

# The FieldInitParameter is not a simple RegisteredParameter because
# it has to handle more than one RegisteredClass, for different
# varieties of Fields. 

class FieldInitParameter(parameter.Parameter):
    types = (FieldInit,)
    def binaryRepr(self, datafile, value):
        return value.binaryRepr(datafile) # uses RegisteredClass.binaryRepr
    def binaryRead(self, parser):
        (regkey,) = struct.unpack('>i', parser.getBytes(struct.calcsize('>i')))
        registration = parser.getObject(regkey)
        argdict = {}
        for param in registration.params:
            argdict[param.name] = param.binaryRead(parser)
        return registration(**argdict)
    def valueDesc(self):
        return """A field initializer from one of the <link
        linkend='RegisteredClass-ScalarFieldInit'><classname>ScalarFieldInit</classname></link>
        or <link
        linkend='RegisteredClass-TwoVectorFieldInit'><classname>TwoVectorFieldInit</classname></link>
        classes."""

#############################

# Derived classes of FieldInit must provide func(position, time,
# component) that returns the value of a Field component at the given
# position and time.  They must also indicate what type of field they
# work for by inserting themselves into the fieldInitDict dictionary.

## We could get rid of fieldInitDict and make FieldInit a normal
## RegisteredClass by using the RegisteredClassFactory's
## includeRegistration feature.  (The FieldInit code predates
## includeRegistration.)  This wouldn't help much, though.  We'd need
## to somehow have a Field widget that the initializer widget could
## see, so that it could decide which initializers to display.  There
## is no Field widget at the moment.  It might be slightly neater to
## use a metaclass to automatically make entries into fieldInitDict,
## though.

fieldInitDict = {}

# ScalarFieldInit, TwoVectorFieldInit, ThreeVectorFieldInit,
# NVectorFieldInit and SymmetricTensorFieldInit are abstract derived
# classes of FieldInit.  They don't provide func().  They just
# separate the classes into categories.

class ScalarFieldInit(registeredclass.RegisteredClass, FieldInit):
    registry = []
    tip="Methods for initializing a scalar field."
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/scalar_field_init.xml')
fieldInitDict['ScalarField'] = ScalarFieldInit
fieldInitDict['ScalarFieldBase'] = ScalarFieldInit

class TwoVectorFieldInit(registeredclass.RegisteredClass, FieldInit):
    registry = []
    tip="Methods for initializing a two dimensional vector field."
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/two_vector_field_init.xml')
fieldInitDict['TwoVectorField'] = TwoVectorFieldInit
fieldInitDict['TwoVectorFieldBase'] = TwoVectorFieldInit


class ThreeVectorFieldInit(registeredclass.RegisteredClass, FieldInit):
    registry = []
    tip="Methods for initializing a three dimensional vector field."
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/three_vector_field_init.xml')

fieldInitDict['ThreeVectorField'] = ThreeVectorFieldInit
fieldInitDict['ThreeVectorFieldBase'] = ThreeVectorFieldInit

# NVectorField isn't swigged yet
##class NVectorFieldInit(registeredclass.RegisteredClass, FieldInit):
##    registry = []
##fieldInitDict[field.NVectorField] = NVectorFieldInit
   
class SymmetricTensorFieldInit(registeredclass.RegisteredClass, FieldInit):
    registry = []
    tip="Methods for initializing a symmetric tensor field."
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/symten_field_init.xml')

fieldInitDict['SymmetricTensorField'] = SymmetricTensorFieldInit

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# Initialization to a constant value.

class ConstScalarFieldInit(ScalarFieldInit):
    def __init__(self, value):
        self.value = value
    def func(self, position, time, component):
        return self.value
    def shortrepr(self):
        return str(self.value)

registeredclass.Registration(
    "Constant",
    ScalarFieldInit,
    ConstScalarFieldInit,
    0,
    params= [parameter.FloatParameter('value', 0.0,
                                      tip='Value to assign to the Field.')],
    tip="Initialize a scalar field with a constant value.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/const_scalar_field_init.xml')
    )

################

class ConstTwoVectorFieldInit(TwoVectorFieldInit):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
    def func(self, position, time, component):
        if component == 0:
            return self.cx
        return self.cy
    def shortrepr(self):
        return "cx=%s, cy=%s" % (str(self.cx), str(self.cy))

registeredclass.Registration(
    "Constant",
    TwoVectorFieldInit,
    ConstTwoVectorFieldInit,
    0,
    params=[
    parameter.FloatParameter('cx', 0.0,
                      tip='Value to assign to the x component of the Field.'),
    parameter.FloatParameter('cy', 0.0,
                      tip='Value to assign to the y component of the Field.')
    ],
    tip="Initialize a two-vector field with a constant value.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/const_twovec_init.xml')
    )

################

class ConstThreeVectorFieldInit(ThreeVectorFieldInit):
    def __init__(self, cx, cy, cz):
        # Because this is a registered class, it must have attributes
        # corresponding to its paramter names, so we can't be clever
        # with the storage scheme here.
        self.cx = cx
        self.cy = cy
        self.cz = cz
    def func(self, position, time, component):
        if component==0:
            return self.cx
        else:
            if component==1:
                return self.cy
            else:
                return self.cz
    def shortrepr(self):
        return "cx=%s, cy=%s, cz=%s" % (self.cx, self.cy, self.cz)

registeredclass.Registration(
    "Constant",
    ThreeVectorFieldInit,
    ConstThreeVectorFieldInit,
    0,
    params=[
    parameter.FloatParameter('cx', 0.0,
                   tip='Value to assign to the x component of the Field.'),
    parameter.FloatParameter('cy', 0.0,
                   tip='Value to assign to the y component of the Field.'),
    parameter.FloatParameter('cz', 0.0,
                   tip='Value to assign to the z component of the Field.') 
    ],
    tip="Initialize a two-vector field with a constant value.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/const_threevec_init.xml')
    )

################

class ConstSymmetricTensorFieldInit(SymmetricTensorFieldInit):
    mapping = ['vxx', 'vyy', 'vzz', 'vyz', 'vxz', 'vxy']
    def __init__(self, vxx, vyy, vzz, vyz, vxz, vxy):
        self.vxx = vxx
        self.vyy = vyy
        self.vzz = vzz
        self.vyz = vyz
        self.vxz = vxz
        self.vxy = vxy
    def func(self, position, time, component):
        return getattr(self, ConstSymmetricTensorFieldInit.mapping[component])
    def shortrepr(self):
        return "vxx=%s, vyy=%s, vzz=%s, vyz=%s, vxz=%s, vxy=%s" % \
               (str(self.vxx), str(self.vyy), str(self.vzz),
                str(self.vyz), str(self.vxz), str(self.vxy))



registeredclass.Registration(
    "Constant",
    SymmetricTensorFieldInit,
    ConstSymmetricTensorFieldInit,
    1,
    params=[
    strfunction.XYStrFunctionParameter('vxx', value='0.0',
                                       tip="The xx component of the field."),
    strfunction.XYStrFunctionParameter('vyy', value='0.0',
                                       tip="The yy component of the field."),
    strfunction.XYStrFunctionParameter('vzz', value='0.0',
                                       tip="The zz component of the field."),
    strfunction.XYStrFunctionParameter('vyz', value='0.0',
                                       tip="The yz component of the field."),
    strfunction.XYStrFunctionParameter('vxz', value='0.0',
                                       tip="The xz component of the field."),
    strfunction.XYStrFunctionParameter('vxy', value='0.0',
                                       tip="The xy component of the field."),
    
    ],
    tip="Initialize a symmetric tensor field with a constant value.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/const_symten_init.xml')
    )

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# Initialization from a function defined by a Python string.

if config.dimension() == 2:
    funcstring = "XYTFunction"
    funcofstring = "of x, y, and t"
elif config.dimension() == 3:
    funcstring = "XYZTFunction"
    funcofstring = "of x, y, z, and t"

class FuncScalarFieldInit(ScalarFieldInit):
    def __init__(self, function):
        self.function = function
    def func(self, position, time, component):
        return self.function(position, time)
    def shortrepr(self):
        return str(self.function)

registeredclass.Registration(
    funcstring,
    ScalarFieldInit,
    FuncScalarFieldInit,
    1,
    params=[
    strfunction.XYTStrFunctionParameter('function', default='0.0',
                                        tip='A function '+funcofstring)],
    tip="Initialize a scalar field with a function "+funcofstring+".",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/func_scalar_init.xml')
    )

################


class FuncTwoVectorFieldInit(TwoVectorFieldInit):
    def __init__(self, fx, fy):
        self.fx = fx
        self.fy = fy
    def func(self, position, time, component):
        if  component == 0:
            return self.fx(position, time)
        return self.fy(position, time)
    def shortrepr(self):
        return "fx=%s, fy=%s" % (str(self.fx), str(self.fy))


registeredclass.Registration(
    funcstring,
    TwoVectorFieldInit,
    FuncTwoVectorFieldInit,
    1,
    params=[
    strfunction.XYTStrFunctionParameter('fx', value='0.0',
                   tip="The x component of the field as a function "
                                       + funcofstring),
    strfunction.XYTStrFunctionParameter('fy', value='0.0',
                   tip="The y component of the field as a function "
                                       + funcofstring),
    ],
    tip="Initialize a two-vector field with a function of x and y.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/func_twovec_init.xml')
    )
                             
##################

class FuncThreeVectorFieldInit(ThreeVectorFieldInit):
    def __init__(self, fx, fy, fz):
        # Registered classes should have attributes corresponding to
        # their parameter names, otherwise these would be in a list.
        self.fx = fx
        self.fy = fy
        self.fz = fz
    def func(self, position, time, component):
        if component == 0:
            return self.fx(position, time)
        elif component == 1:
            return self.fy(position, time)
        else:
            return self.fz(position, time)
    def shortrepr(self):
        return "fx=%s, fy=%s, fz=%s" % (self.fx, self.fy, self.fz)


registeredclass.Registration(
    funcstring,
    ThreeVectorFieldInit,
    FuncThreeVectorFieldInit,
    1,
    params=[
    strfunction.XYTStrFunctionParameter('fx', value='0.0',
                   tip="The x component of the field as a function "
                                       + funcofstring),
    strfunction.XYTStrFunctionParameter('fy', value='0.0',
                   tip="The y component of the field as a function "
                                       + funcofstring),
    strfunction.XYTStrFunctionParameter('fz', value='0.0',
                   tip="The z component of the field as a function "
                                       + funcofstring)
    ],
    tip="Initialize a three-vector field with a function of x and y.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/func_threevec_init.xml')
    ) 

###############

class FuncSymmetricTensorFieldInit(SymmetricTensorFieldInit):
    mapping = ['fxx', 'fyy', 'fzz', 'fyz', 'fxz', 'fxy']
    def __init__(self, fxx, fyy, fzz, fyz, fxz, fxy):
        self.fxx = fxx
        self.fyy = fyy
        self.fzz = fzz
        self.fyz = fyz
        self.fxz = fxz
        self.fxy = fxy
    def func(self, position, time, component):
        func = getattr(self, FuncSymmetricTensorFieldInit.mapping[component])
        return func(position)
    def shortrepr(self):
        return "fxx=%s, fyy=%s, fzz=%s, fyz=%s, fxz=%s, fxy=%s" % \
               (str(self.fxx), str(self.fyy), str(self.fzz),
                str(self.fyz), str(self.fxz), str(self.fxy))

# NB re-uses the funcstring and funcofstring set above, depending on
# the dimension.

registeredclass.Registration(
    funcstring,
    SymmetricTensorFieldInit,
    FuncSymmetricTensorFieldInit,
    1,
    params=[
    strfunction.XYStrFunctionParameter(
            'fxx', value='0.0',
            tip="The xx component of the field as a function "+funcofstring),
    strfunction.XYStrFunctionParameter(
            'fyy', value='0.0',
            tip="The yy component of the field as a function "+funcofstring),
    strfunction.XYStrFunctionParameter(
            'fzz', value='0.0',
            tip="The zz component of the field as a function "+funcofstring),
    strfunction.XYStrFunctionParameter(
            'fyz', value='0.0',
            tip="The yz component of the field as a function "+funcofstring),
    strfunction.XYStrFunctionParameter(
            'fxz', value='0.0',
            tip="The xz component of the field as a function "+funcofstring),
    strfunction.XYStrFunctionParameter(
            'fxy', value='0.0',
            tip="The xy component of the field as a function "+funcofstring),
    
    ],
    tip="Initialize a symmetric tensor field with a function of x, y, and t.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/func_symten_init.xml')
    )

    
#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# OtherMeshFieldInit initializes a Field by copying it from another
# Mesh.  Subclasses of OtherMeshFieldInit are stubs, existing mainly
# to populate the dictionary.  The base class does everything.

class OtherMeshFieldInit:
    def __init__(self, mesh, time):
        self.mesh = mesh                # name of the other mesh
        self.time = time                # time in the other mesh
    def apply(self, femesh, field, time=None, singleFieldDef=False):
        # The 'time' argument isn't used.  It's the time in the Mesh
        # being initialized, not the Mesh from which the data is being
        # copied.  We don't need to know it here.
        meshctxt = ooflib.engine.mesh.meshes[self.mesh]
        meshctxt.restoreCachedData(meshctxt.getTime(self.time))
        try:
            meshobj = meshctxt.getObject()
            femesh.init_field(meshobj.skeleton, meshobj, field)
        finally:
            meshctxt.releaseCachedData()
    def shortrepr(self):
        return "mesh=%s" % self.mesh

othermeshparams = [
    whoville.WhoParameter(
        'mesh', ooflib.engine.mesh.meshes,
        tip='Copy field values from this Mesh.'),
    placeholder.TimeParameter(
        'time', value=placeholder.latest,
        tip='Use values at this time in the source Mesh.')]

class ScalarOtherMeshInit(OtherMeshFieldInit, ScalarFieldInit):
    pass
    
registeredclass.Registration(
    "Other Mesh",
    ScalarFieldInit,
    ScalarOtherMeshInit,
    2,
    params=othermeshparams,
    tip="Initialize a scalar field from the same field on another mesh.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/scalar_othermesh_init.xml')
    )

class TwoVectorOtherMeshInit(OtherMeshFieldInit, TwoVectorFieldInit):
    pass
            
registeredclass.Registration(
    "Other Mesh",
    TwoVectorFieldInit,
    TwoVectorOtherMeshInit,
    2,
    params=othermeshparams,
    tip="Initialize a two-vector field from the same field on another mesh.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/twovec_othermesh_init.xml')
    )

class ThreeVectorOtherMeshInit(OtherMeshFieldInit, ThreeVectorFieldInit):
    pass

registeredclass.Registration(
    "Other Mesh",
    ThreeVectorFieldInit,
    ThreeVectorOtherMeshInit,
    2,
    params=othermeshparams,
    tip="Initialize a three-vector field from the same field on another mesh.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/threevec_othermesh_init.xml')
    )

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# Because FieldInitParameters aren't normal RegisteredParameters, the
# classes have to be explicitly added to the xml docs.

xmlmenudump.addRegisteredClass(ScalarFieldInit)
xmlmenudump.addRegisteredClass(TwoVectorFieldInit)
xmlmenudump.addRegisteredClass(ThreeVectorFieldInit)
xmlmenudump.addRegisteredClass(SymmetricTensorFieldInit)

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# ResetFieldInit is used in Solve.Reset, to zero all Fields that don't
# have explicit initializers.

class ResetFieldInit(FieldInit):
    def func(self, position, time, index):
        return 0
