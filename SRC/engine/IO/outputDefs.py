# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This file generates concrete Outputs from the Outputs defined in
# outputClones.py.  The concrete Outputs are stored in a tree
# structure which can easily be converted to a menu.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import flux
from ooflib.SWIG.engine import outputval
from ooflib.SWIG.engine import planarity
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import primitives
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import problem
from ooflib.engine.IO import output
from ooflib.engine.IO import outputClones
from ooflib.engine.IO import propertyoutputreg

from types import *

######################################

# Special displacement outputs, which used to be here, aren't needed
# in 3D and won't be needed in 2D after the merge.  Their role is
# played by the MeshNodePosition class.

######################

## Is there any point in outputting the surface normal?  Maybe if
## it were computed using displaced coordinates...
# output.defineOutput("Surface Normal",
#                              outputClones.SurfaceNormalOutput,
#                              ordering=500)
normalFluxOutput = outputClones.DotProduct.clone(
    name="Flux Normal"
)
normalFluxOutput.connect('a', outputClones.FluxOutput)
normalFluxOutput.connect('b', outputClones.SurfaceNormalOutput)
normalFluxOutput.aliasParam('a:flux', 'flux')
output.defineOutput("Flux:Normal:Value", normalFluxOutput, ordering=100)

normalFluxInvariantOutput = outputClones.InvariantOutput.clone(
    name="flux normal invariant",
    tip="Compute invariants of Flux normals at a surface.")
normalFluxInvariantOutput.connect("field", normalFluxOutput)
normalFluxInvariantOutput.aliasParam('field:flux', 'flux')
output.defineOutput("Flux:Normal:Invariant", normalFluxInvariantOutput,
                    ordering=101)

######################

output.defineOutput('Field:Value', outputClones.FieldOutput,
                    ordering=1.0)
output.defineOutput('Field:Derivative:Value', outputClones.FieldDerivOutput,
                    ordering=1.1)
output.defineOutput('Field:Invariant', outputClones.FieldInvariantOutput,
                    ordering=1.2)

output.defineOutput('Flux:Value', outputClones.FluxOutput,
                    ordering=2.0)
output.defineOutput('Flux:Invariant', outputClones.FluxInvariantOutput,
                    ordering=2.1)

output.defineOutput('Field:Component', outputClones.FieldCompOutput, 
                    ordering=1.0)
output.defineOutput('Field:Derivative:Component',
                    outputClones.FieldDerivCompOutput, ordering=1.2)
output.defineOutput('Field:Derivative:Invariant',
                    outputClones.FieldDerivInvariantOutput, ordering=1.3)

output.defineOutput('Flux:Component', outputClones.FluxCompOutput, 
                    ordering=2.0)

xyzfunc = outputClones.ScalarFunctionOutput.clone(
    tip='Compute an arbitrary scalar function of x, y, and z.',
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/output/funcOutput.xml'))
output.defineOutput('XYZFunction:Scalar', xyzfunc, ordering=100)

xyzvecfunc = outputClones.VectorFunctionOutput.clone(
    tip='Compute an arbitrary vector function of x, y and z.')
output.defineOutput('XYZFunction:Vector', xyzvecfunc, ordering=100)

###########

negElectricFieldOutput = outputClones.FieldDerivOutput.clone(
    params=dict(field=field.getField("Voltage"))
    )
electricFieldOutput = outputClones.NegateOutput.clone()
electricFieldOutput.connect("scalee", negElectricFieldOutput)
#output.defineOutput('E Field', electricFieldOutput)
eFieldCompOutput = outputClones.ComponentOutput.clone()
eFieldCompOutput.connect('field', electricFieldOutput)
#output.defineOutput('E Field:component', eFieldCompOutput)

## TODO 3.1: Uncomment the above two defineOutput lines, but only after
## fixing the problems with the MeshParamWidgets.  The problem is that
## the widget for the component of the E field looks for a
## FieldWidget, and doesn't find one because the Field isn't a
## settable parameter.

######################

# PropertyOutputs, which are computed by the Property objects in a
# Material, only have to be identified by name, type, and (possibly)
# initializer here.  The computations are all done by the
# PropertyOutput<TYPE> classes and the various Property::output virtual
# functions.

class EnergyType(enum.EnumClass(
    ("Total", "All contributions to the energy"),
    ("Elastic", "Elastic energy-- one half stress times elastic strain"),
    ("Electric", "Electric energy-- one half total polarization times electric field")
    )):
    tip="Varieties of Energy."
    discussion="""<para>
    <classname>EnergyType</classname> indicates which energy is to be
    computed by the <xref linkend='Output-Scalar-Energy'/> Output.
    </para>"""

def _Energy_shortrepr(self):
    etype = self.findParam("etype").value
    return etype.string() + " Energy"

# ScalarPropertyOutputRegistration places the output in both the
# ScalarOutput and AggregateOutput trees.

propertyoutputreg.ScalarPropertyOutputRegistration(
    "Energy",
    parameters=[enum.EnumParameter("etype", EnergyType, default="Total",
                                  tip='The type of energy to compute.')],
    ordering=3,
    srepr = _Energy_shortrepr,
    tip='Compute an energy density.',
    discussion="""
      <para>Compute the energy density of the &fields; on the &mesh;.
      Different values of <varname>etype</varname> include different
      contributions to the energy.</para>"""
    )


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Parameters used for PropertyParameterOutputs

class ReferenceFrame(enum.EnumClass(
        ("Lab", "The laboratory reference frame"),
        ("Crystal", "The crystal reference frame")
        )):
    tip="Evaluate quantities in the lab or crystal reference frame."

class VoigtPairListParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if not isinstance(x, (ListType, TupleType)):
            parameter.raiseTypeError(type(x), "list of Voigt index pairs")
        for s in x:
            if not (isinstance(s, StringType) and len(s)==2 and
                    s[0] in "123456" and s[1] in "123456"):
                parameter.raiseTypeError("list of %s" % typename(type(s)),
                                         "list of Voigt index pairs [1-6][1-6]")
    def valueDesc(self):
        return "A list of character strings of the form 'XY'" \
            " where X and Y are digits from 1 to 6."

class SymmIndexPairListParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if not isinstance(x, (ListType, TupleType)):
            parameter.raiseTypeError(type(x), "list of index pairs")
        for s in x:
            if not (isinstance(s, StringType) and len(s)==2 and
                    s[0] in "123" and s[1] in "123"):
                parameter.raiseTypeError("list of %s" % typename(type(s)),
                                         "list of index pairs [1-3][1-3]")
    def valueDesc(self):
        return "A list of character strings of the form 'XY'" \
            "where X and Y are digits from 1 to 3."

class Rank3TensorIndexParameter(parameter.ListOfStringsParameter):
    # Pair of integers, ([1-3], [1-6])
    # This class is poorly named because the name doesn't indicate the
    # symmetry of the tensor (ie, 2nd index is Voigt).
    def checker(self, x):
        if not isinstance(x, (ListType, TupleType)):
            parameter.raiseTypeError(type(x), "list of index pairs")
        for s in x:
            if not (isinstance(s, StringType) and len(s)==2 and
                    s[0] in "123" and s[1] in "123456"):
                parameter.raiseTypeError("list of %s" % typename(type(s)),
                                         "list of index pairs [1-3][1-6]")
    def valueDesc(self):
        return "A list of character strings of the form 'XY'" \
            "where X is a digit from 1 to 3 and Y is a Voigt index from 1 to 6."

# PropertyParameterOutputs, which output the parameters defining
# material properties.  The ordering of the registrations should echo
# the ordering of the Properties in the Materials page.

## TODO: Can these registrations be created automatically by the
## Property registrations?  It wouldn't be easy, because there's not a
## one-to-one relationship between the Property registrations and the
## PropertyOutput registrations.

# Mechanical

propertyoutputreg.ModulusPropertyOutputRegistration(
    name="Material Constants:Mechanical:Elastic Modulus C",
    symbol="C",
    parameters=[
        VoigtPairListParameter(
            "components",
            tip="Evaluate the selected components of the modulus."),
        enum.EnumParameter(
            "frame", ReferenceFrame, default="Crystal",
            tip="Report the modulus in this reference frame.")
    ],
    ordering=10)

propertyoutputreg.ModulusPropertyOutputRegistration(
    name="Material Constants:Mechanical:Stress-free Strain epsilon0",
    symbol="epsilon0",
    parameters=[
        SymmIndexPairListParameter(
            "components",
            tip="Evaluate the selected components of the stress-free strain."),
        enum.EnumParameter(
            "frame", ReferenceFrame, default="Crystal",
            tip="Report the stress-free strain in this reference frame.")
        ],
    ordering=11)

propertyoutputreg.ThreeVectorParamPropertyOutputRegistration(
    name="Material Constants:Mechanical:Force Density F",
    symbol="F",
    ordering=12)

propertyoutputreg.ScalarParamOutputRegistration(
    name="Material Constants:Mechanical:Mass Density",
    srepr=lambda s: "Mass Density",
    ordering=13)

propertyoutputreg.ScalarParamOutputRegistration(
    name="Material Constants:Mechanical:Damping",
    srepr=lambda s: "Damping",
    ordering=15)

propertyoutputreg.ModulusPropertyOutputRegistration(
    name="Material Constants:Mechanical:Viscosity",
    symbol="g",
    parameters=[
        VoigtPairListParameter(
            "components",
            tip="Evaluate the selected components of the modulus"),
        enum.EnumParameter(
            "frame", ReferenceFrame, default="Crystal",
            tip="Report the viscosity in this reference frame.")
        ],
    ordering=14)

# Thermal

propertyoutputreg.ModulusPropertyOutputRegistration(
    name="Material Constants:Thermal:Conductivity K",
    symbol="K",
    parameters=[
        SymmIndexPairListParameter(
            "components",
            tip="Evaluate the selected components of the conductivity."),
        enum.EnumParameter(
            "frame", ReferenceFrame, default="Crystal",
            tip="Report the conductivity in this reference frame.")
        ],
    ordering=20)

propertyoutputreg.ScalarParamOutputRegistration(
    name="Material Constants:Thermal:Heat Capacity",
    srepr=lambda s: "Heat Capacity",
    ordering=21)

propertyoutputreg.ScalarParamOutputRegistration(
    name="Material Constants:Thermal:Heat Source",
    srepr=lambda s: "Heat Source",
    ordering=22)

propertyoutputreg.ModulusPropertyOutputRegistration(
    name="Material Constants:Electric:Dielectric Permittivity epsilon",
    symbol="epsilon",
    parameters=[
        SymmIndexPairListParameter(
            "components",
            tip="Evaluate the selected components of the permittivity."),
        enum.EnumParameter(
            "frame", ReferenceFrame, default="Crystal",
            tip="Report the permittivity in this reference frame.")
        ],
    ordering=30)

propertyoutputreg.ScalarParamOutputRegistration(
    name="Material Constants:Electric:Space Charge",
    srepr=lambda s: "Space Charge",
    ordering=31)

# Couplings

propertyoutputreg.ModulusPropertyOutputRegistration(
    name="Material Constants:Couplings:Thermal Expansion alpha",
    symbol="alpha",
    parameters=[
        SymmIndexPairListParameter(
            "components",
            tip="Evaluate the selected components of the thermal expansion coefficient"),
        enum.EnumParameter(
            "frame", ReferenceFrame, default="Crystal",
            tip="Report the thermal expansion coefficient in this reference frame.")],
    ordering=50)

propertyoutputreg.ScalarParamOutputRegistration(
    name="Material Constants:Couplings:Thermal Expansion T0",
    srepr=lambda s: "T0",
    ordering=50.5)

propertyoutputreg.ModulusPropertyOutputRegistration(
    name="Material Constants:Couplings:Piezoelectric Coefficient D",
    symbol="D",
    parameters=[
        Rank3TensorIndexParameter(
            "components",
            tip="Evaluate the selected components of the piezoelectric coefficient."),
        enum.EnumParameter(
            "frame", ReferenceFrame, default="Crystal",
            tip="Report the stress-free strain in this reference frame.")
        ],
    ordering=51)

# TODO: PyroElectricity

# Orientation

propertyoutputreg.OrientationPropertyOutputRegistration(
    "Material Constants:Orientation",
    ordering=1000,
    tip="Compute the orientation at each point.")

