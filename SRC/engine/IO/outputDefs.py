# -*- python -*-
# $RCSfile: outputDefs.py,v $
# $Revision: 1.78.4.9 $
# $Author: fyc $
# $Date: 2014/07/28 22:17:46 $

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
from ooflib.SWIG.engine.IO import propertyoutput
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import primitives
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import problem
from ooflib.engine.IO import output
from ooflib.engine.IO import outputClones

from types import *
import string

######################################

# Special displacement outputs, which used to be here, aren't needed
# in 3D and won't be needed in 2D after the merge.  Their role is
# played by the MeshNodePosition class.

######################

if config.dimension() == 3:
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

from ooflib.common import strfunction
if config.dimension() == 2:
    xyfunc = outputClones.ScalarFunctionOutput.clone(
        tip='Compute an arbitrary scalar function of x and y.',
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/output/funcOutput.xml'))
    output.defineOutput('XYFunction:Scalar', xyfunc, ordering=100)

    xyvecfunc = outputClones.VectorFunctionOutput.clone(
        tip='Compute an arbitrary vector function of x and y.',
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/output/vecfuncOutput.xml'))
    output.defineeOutput('XYFunction:Vector', xyvecfunc, ordering=100)

elif config.dimension() == 3:
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

propertyoutput.ScalarPropertyOutputRegistration(
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
