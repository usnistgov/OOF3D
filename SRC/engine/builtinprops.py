# -*- python -*-
# $RCSfile: builtinprops.py,v $
# $Revision: 1.24.6.2 $
# $Author: langer $
# $Date: 2013/11/08 20:43:07 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# This file has the big block of imports which gets all the built-in
# property classes.  These imports run the initialization code in the
# property classes themselves, creating a PropertyRegistration entry,
# which then adds itself to the main OOF2 namespace.

from ooflib.SWIG.common import config

# Properties not in this list can be imported by the user at
# other points, so this list of properties is not guaranteed to
# be exhaustive.
import ooflib.SWIG.engine.properties

import ooflib.SWIG.engine.property.color.color
import ooflib.SWIG.engine.property.damping.damping
import ooflib.SWIG.engine.property.elasticity.aniso.aniso
import ooflib.SWIG.engine.property.elasticity.elasticity
import ooflib.SWIG.engine.property.elasticity.iso.iso
import ooflib.SWIG.engine.property.elasticity.largestrain.largestrain
import ooflib.SWIG.engine.property.elasticity.thermo.thermo
import ooflib.SWIG.engine.property.elasticity.visco.visco
import ooflib.SWIG.engine.property.elasticity.nonlinear.general_nonlinear_elasticity
import ooflib.SWIG.engine.property.forcedensity.forcedensity
import ooflib.SWIG.engine.property.forcedensity.nonconstant.nonconstant_force_density
import ooflib.SWIG.engine.property.forcedensity.nonlinear.nonlinear_force_density
import ooflib.SWIG.engine.property.heatcapacity.heatcapacity
import ooflib.SWIG.engine.property.heatconductivity.heatconductivity
import ooflib.SWIG.engine.property.heatconductivity.nonlinear.nonlinear_heat_conductivity
import ooflib.SWIG.engine.property.heatsource.heatsource
import ooflib.SWIG.engine.property.heatsource.nonconstant.nonconstant_heat_source
import ooflib.SWIG.engine.property.heatsource.nonlinear.nonlinear_heat_source
import ooflib.SWIG.engine.property.massdensity.massdensity
import ooflib.SWIG.engine.property.orientation.orientation
import ooflib.SWIG.engine.property.permittivity.permittivity
import ooflib.SWIG.engine.property.piezoelectricity.piezoelectricity
import ooflib.SWIG.engine.property.pyroelectricity.pyroelectricity
import ooflib.SWIG.engine.property.stressfreestrain.stressfreestrain
import ooflib.SWIG.engine.property.thermalexpansion.thermalexpansion
#import ooflib.engine.property.plasticity.plasticity

#Interface branch
if config.dimension() == 2:
    import ooflib.SWIG.engine.property.interfaces.surfacetension.simpletension.simpletension
    import ooflib.SWIG.engine.property.interfaces.surfacetest.surfacetest
#     import ooflib.SWIG.engine.property.interfaces.surfacetension.simpletension2.simpletension2


import ooflib.engine.property.heatconductivity.pyheatconductivity
import ooflib.engine.property.elasticity.pyelasticity
import ooflib.engine.property.stressfreestrain.pystressfreestrain
