# -*- python -*-
# $RCSfile: problem.py,v $
# $Revision: 1.64.2.3 $
# $Author: fyc $
# $Date: 2014/07/28 22:15:17 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import equation
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import fieldindex
from ooflib.SWIG.engine import flux
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import xmlmenudump
from ooflib.engine import conjugate
from ooflib.engine import propertyregistration
import sys
import types

def _advertise(obj):
    utils.OOFdefine(obj.name(), obj)
    return obj

def advertiseField(fld):
    field.newCompoundField(fld)
    _advertise(fld)
    td = _advertise(fld.time_derivative())
    field.newField(td)
    if config.dimension() == 2:
        field.newField(_advertise(fld.out_of_plane()))
        field.newField(_advertise(fld.out_of_plane_time_derivative()))
    # "new field" is sent here, instead of from the Field constructor,
    # because it must be called *after* the field is defined in the
    # OOF namespace.
    switchboard.notify("new field")
    return fld

def advertiseFlux(flx):
    _advertise(flx)
    switchboard.notify("new flux")
    return flx

def advertiseEquation(eqn):
    _advertise(eqn)
    switchboard.notify("new equation")
    return eqn

def advertise(obj):
    # This code is ugly, but at least it's compact.  It's not much
    # uglier than the previous version, which required other code to
    # call advertiseField, et al, directly.
    if isinstance(obj, field.FieldPtr):
        return advertiseField(obj)
    if isinstance(obj, flux.FluxPtr):
        return advertiseFlux(obj)
    if isinstance(obj, equation.EquationPtr):
        return advertiseEquation(obj)
    raise ooferror.ErrPyProgrammingError("Don't know what to do with %s!"% obj)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Define a field.  This creates an object named 'Temperature' in the
# OOF namespace.
Temperature = advertise(field.ScalarField('Temperature'))
# Define a flux
Heat_Flux = advertise(flux.VectorFlux('Heat_Flux'))
# And equations
HeatBalanceEquation = advertise(equation.DivergenceEquation(
    'Heat_Eqn',
    Heat_Flux,
    1
    ))

if config.dimension() == 2:
    HeatOutOfPlane = advertise(equation.PlaneFluxEquation(
            'Plane_Heat_Flux', Heat_Flux, 1))

## this creates the Displacement, Stress, and Force Balance equations
if config.dimension() == 2:
    Displacement = advertise(field.TwoVectorField('Displacement'))
elif config.dimension() == 3:
    Displacement = advertise(field.ThreeVectorField('Displacement'))
Stress = advertise(flux.SymmetricTensorFlux('Stress'))

ForceBalanceEquation = advertise(equation.DivergenceEquation(
    'Force_Balance',
    Stress,
    config.dimension()
    ))

if config.dimension() == 2:
    ForcesOutOfPlane = \
        advertise(equation.PlaneFluxEquation('Plane_Stress',
                                             Stress, 3))


## Define electrostatic potential
Voltage = advertise(field.ScalarField('Voltage'))
## Define total polarization vector
Total_Polarization = advertise(flux.VectorFlux('Total_Polarization'))
## Differential form of Coulomb's Law
CoulombEquation = advertise(equation.DivergenceEquation(
    'Coulomb_Eqn', Total_Polarization, 1))
if config.dimension() == 2:
    PolarizationOutOfPlane = advertise(equation.PlaneFluxEquation(
            'InPlanePolarization', Total_Polarization, 1))


# Plasticity -- start with the yield equation.
# TODO 3.1: Make hidden equations.

# YieldEquation = advertise(equation.NaturalEquation(
#     'Yield_Eqn',1))


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Define conjugate quantities for all fields and equations

## Force balance equation
##
## In-plane components (u,v)
##
## The 3D displacement vector is (u, v, w),
## where
## u lies along the x-direction,
## v, along the y-direction,
## and w, out-of-the-plane, or along
## the z-direction
u = fieldindex.VectorFieldIndex(0)
v = fieldindex.VectorFieldIndex(1)

fx = fieldindex.VectorFieldIndex(0)
fy = fieldindex.VectorFieldIndex(1)

if config.dimension() == 2:
    # fx is conjugate to u and fy is conjugate to v for Elasticity
    conjugate.conjugatePair("Elasticity", ForceBalanceEquation, [fx, fy],
                        Displacement, [u, v]) 

    ## out-of-plane compoments

    ## The available out-of-plane components of stress are $\sigma_{zz},
    ## \sigma_{zy}, \sigma_{zx}$, in *that* order, (0, 1, 2).  The
    ## out-of-plane displacement is (\frac{\partial u}{\partial z},
    ## \frac{\partial v}{partial z}, \frac{\partial w}{\partial z}.

    u_xz = fieldindex.VectorFieldIndex(0)
    u_yz = fieldindex.VectorFieldIndex(1)
    u_zz = fieldindex.VectorFieldIndex(2)
    sigma_xz = fieldindex.OutOfPlaneSymTensorIndex(2,0)
    sigma_yz = fieldindex.OutOfPlaneSymTensorIndex(2,1)
    sigma_zz = fieldindex.OutOfPlaneSymTensorIndex(2,2)

    ## \sigma_{zz} is conjugate to \frac{\partial w}{\partial z}
    ## \sigma_{xz} is conjugate to \frac{\partial u}{\partial z}
    ## \sigma_{yz} is conjugate to \frac{\partial v}{\partial z}

    conjugate.conjugatePair("Elasticity",
                            ForcesOutOfPlane, [sigma_zz, sigma_xz, sigma_yz],
                            Displacement.out_of_plane(), [u_zz, u_xz, u_yz])

elif config.dimension() == 3:
    w = fieldindex.VectorFieldIndex(2)
    fz = fieldindex.VectorFieldIndex(2)
    conjugate.conjugatePair("Elasticity", ForceBalanceEquation, [fx, fy, fz],
                            Displacement, [u, v, w])

###############################################################
##
## Heat flux equation
##
## In-plane components, T
##
T = fieldindex.ScalarFieldIndex()
DivJ = fieldindex.ScalarFieldIndex()

conjugate.conjugatePair("ThermalConductivity", HeatBalanceEquation, DivJ,
                        Temperature, T)
 ## $\nabla \cdot \vec{J}$ is conjugate to T

## out-of-plane components, $\frac{\partial T}{\partial z}$
if config.dimension() == 2:
    T_z = fieldindex.OutOfPlaneVectorFieldIndex(2)
    J_z = fieldindex.OutOfPlaneVectorFieldIndex(2)

    conjugate.conjugatePair("ThermalConductivity", HeatOutOfPlane, J_z,
                            Temperature.out_of_plane(), T_z)
 ##  $J_{z}$ is conjugate to $\frac{\partial T}{\partial z}$

###############################################################
##
## Coulomb equation
##
## In-plane components, phi
##
phi = fieldindex.ScalarFieldIndex()
DivD = fieldindex.ScalarFieldIndex()

conjugate.conjugatePair("DielectricPermittivity",
                        CoulombEquation, DivD,
                        Voltage, phi)
 ## $\nabla \cdot \vec{D}$ is conjugate to D

## out-of-plane components, $\frac{\partial D}{\partial z}$
if config.dimension() == 2:
    phi_z = fieldindex.OutOfPlaneVectorFieldIndex(2)
    D_z = fieldindex.OutOfPlaneVectorFieldIndex(2)

    conjugate.conjugatePair("DielectricPermittivity",
                            PolarizationOutOfPlane, D_z,
                            Voltage.out_of_plane(), phi_z)
 ##  $D_{z}$ is conjugate to $\frac{\partial phi}{\partial z}$



#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#=
#-=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#=-

# xmldump generates the manual page for the built-in physics.

def xmldump(phile):
    print >> phile, "<section id='Section-Builtin'>"
    print >> phile, " <title>Built-In Physics: Fields, Fluxes, Equations, and Properties</title>"
    print >> phile, """<para>
    &oof2; is designed to be extendible, so it is easy to add new
    &properties;, &fields;, &fluxes;, and &equations;.  That means
    that the following lists of <emphasis>built-in</emphasis>
    objects may not be complete.  </para>"""

    # Property documentation.  propdict is a dictionary listing the
    # Properties that contribute to each Equation and Flux, or use
    # each Field.
    propdict = propertyregistration.xmldocs(phile)

    # Fields
    print >> phile, "<section id='Section-Fields'>"
    print >> phile, "<title>Fields</title>"
    print >> phile, """<para>

This list contains all of the predefined &fields; in &oof2;.  Click on
a &field; to see a brief description and a list of all &properties;
that use the &field;.

</para>"""
    print >> phile, "<itemizedlist>"
    # List of Fields.
    for fld in field.allCompoundFields.values():
        print >> phile, "<listitem><simpara>"
        print >> phile, "<link linkend='Field-%s'><varname>%s</varname></link>"\
            % (fld.name(), fld.name())
        print >> phile, "</simpara></listitem>"
    print >> phile, "</itemizedlist>"
    # Reference page for each Field.
    for fld in field.allCompoundFields.values():
        name = fld.name()
        xmlmenudump.xmlIndexEntry(name, 'Field', 'Field-%s' % name)
        print >> phile, "<refentry xreflabel='%s' id='Field-%s'>" % (name, name)
        print >> phile, " <refnamediv>"
        print >> phile, "  <refname>%s</refname>" % name
        print >> phile, "  <refpurpose></refpurpose>"
        print >> phile, " </refnamediv>"
        print >> phile, " <refsect1>"
        print >> phile, "  <title>Details</title>"
        print >> phile, "  <itemizedlist>"
        print >> phile, "   <listitem><simpara>"
        print >> phile, "     Class: <classname>%s</classname>" % fld.__class__.__name__
        print >> phile, "   </simpara></listitem>"
        print >> phile, "   <listitem><simpara>"
        print >> phile, "     Dimension: ", fld.ndof()
        print >> phile, "   </simpara></listitem>"

        try:
            properties = propdict[fld]
        except KeyError:
            pass
        else:
            print >> phile, "<listitem><para>"
            print >> phile, "<varname>%s</varname> is used by the following &properties;:" % name
            print >> phile, "<itemizedlist>"
            for prop in properties:
                print >> phile, "<listitem><simpara>"
                print >> phile, "<xref linkend='Property-%s'/>" % (
                    prop.name().replace(':', '-'))
                print >> phile, "</simpara></listitem>"
            print >> phile, "</itemizedlist>"
            print >> phile, "</para></listitem>"
            
        print >> phile, "  </itemizedlist>"
        print >> phile, "</refsect1> <!-- Details -->"

        print >> phile, "<refsect1>"
        print >> phile, "<title>Description</title>"
        try:
            src = file("DISCUSSIONS/engine/builtin/field-%s.xml" % name, "r")
        except IOError:
            print >> phile, "<para>MISSING DISCUSSION for %s</para>" % name
        else:
            print >> phile, src.read()
            src.close()
        print >> phile, "</refsect1>"
        print >> phile, "</refentry> <!-- %s -->" % fld.name()
    print >> phile, "</section> <!-- Fields -->"

    # Fluxes
    print >> phile, "<section id='Section-Fluxes'>"
    print >> phile, "<title>Fluxes</title>"
    print >> phile, """<para>
This list contains all of the predefined &fluxes; in &oof2;.  Click on
a &flux; to see a brief description and a list of all &properties;
that contribute to the &flux;.
</para>"""
    # List of Fluxes
    print >> phile, "<itemizedlist>"
    for flx in flux.allFluxes:
        print >> phile, "<listitem><simpara>"
        print >> phile, "<link linkend='Flux-%s'><varname>%s</varname></link>"\
            % (flx.name(), flx.name())
        print >> phile, "</simpara></listitem>"
    print >> phile, "</itemizedlist>"
    # Reference page for each Flux
    for flx in flux.allFluxes:
        name = flx.name()
        xmlmenudump.xmlIndexEntry(name, 'Flux', 'Flux-%s' % name)
        print >> phile, "<refentry xreflabel='%s' id='Flux-%s'>" % (name, name)
        print >> phile, "<refnamediv>"
        print >> phile, "<refname>%s</refname>" % name
        print >> phile, "<refpurpose></refpurpose>"
        print >> phile, "</refnamediv>"
        print >> phile, "<refsect1>"
        print >> phile, "<title>Details</title>"
        print >> phile, "<itemizedlist>"
        print >> phile, "<listitem><simpara>"
        print >> phile, "Class: <classname>%s</classname>" % (
            flx.__class__.__name__[:-3]) # strip 'Ptr'
        print >> phile, "</simpara></listitem>"
        print >> phile, "<listitem><simpara>"
        print >> phile, "Dimension: ", flx.ndof()
        print >> phile, "</simpara></listitem>"
        try:
            properties = propdict[flx]
        except KeyError:
            pass
        else:
            print >> phile, "<listitem><simpara>"
            print >> phile, "The following &properties; contribute to <varname>%s</varname>:" % name
            print >> phile, "<itemizedlist>"
            for prop in properties:
                print >> phile, "<listitem><simpara>"
                print >> phile, "<xref linkend='Property-%s'/>" % (
                    prop.name().replace(':', '-'))
                print >> phile, "</simpara></listitem>"
            print >> phile, "</itemizedlist>"
            print >> phile, "</simpara></listitem>"

        print >> phile, "</itemizedlist>"
        print >> phile, "</refsect1> <!-- Details -->"
        print >> phile, "<refsect1>"
        print >> phile, "<title>Description</title>"
        try:
            src = file('DISCUSSIONS/engine/builtin/flux-%s.xml' % name, "r")
        except IOError:
            print >> phile, "<para>MISSING DISSCUSSION FOR %s</para>" % name
        else:
            print >> phile, src.read()
            src.close()
        print >> phile, "</refsect1> <!--Description-->"
        print >> phile, "</refentry>"
    print >> phile, "</section> <!-- Fluxes -->"

    print >> phile, "<section id='Section-Equations'>"
    print >> phile, "<title>Equations</title>"
    print >> phile, """<para>
This is a list of all of the predefined &equations; in &oof2;.  Click
on an &equation; to see a description and a list of all &properties;
that contribute to the &equation;.
</para>"""
    # List of Equations
    print >> phile, "<itemizedlist>"
    for eqn in equation.allEquations:
        print >> phile, "<listitem><simpara>"
        print >> phile, "<link linkend='Equation-%s'><varname>%s</varname></link>" % (eqn.name(), eqn.name())
        print >> phile, "</simpara></listitem>"
    print >> phile, "</itemizedlist>"
    # Reference page for each Equation
    links = {'PlaneFluxEquation' : 'Section-Concepts-Mesh-Equation-PlaneFlux',
             'DivergenceEquation' : 'Section-Concepts-Mesh-Equation-Divergence'}
    for eqn in equation.allEquations:
        name = eqn.name()
        xmlmenudump.xmlIndexEntry(name, 'Equation', 'Equation-%s' % name)
        classname = eqn.__class__.__name__[:-3] # strip off 'Ptr'
        print >> phile, "<refentry xreflabel='%s' id='Equation-%s'>" % (
            name, name)
        print >> phile, "<refnamediv>"
        print >> phile, "<refname>%s</refname>" % name
        print >> phile, "<refpurpose></refpurpose>"
        print >> phile, "</refnamediv>"
        print >> phile, "<refsect1>"
        print >> phile, "<title>Details</title>"
        print >> phile, "<itemizedlist>"
        print >> phile, "<listitem><simpara>"
        print >> phile, "Type: <link linkend='%s'><classname>%s</classname></link>" % (links[classname], classname)
        print >> phile, "</simpara></listitem>"
        print >> phile, "<listitem><simpara>"
        print >> phile, "Flux: <link linkend='Flux-%s'><varname>%s</varname></link>" % (eqn.fluxname(), eqn.fluxname())
        print >> phile, "</simpara></listitem>"
        print >> phile, "<listitem><simpara>"
        print >> phile, "Dimension:", eqn.ndof()
        print >> phile, "</simpara></listitem>"
        try:
            properties = propdict[eqn]
        except KeyError:
            pass
        else:
            print >> phile, "<listitem><simpara>"
            print >> phile, "The following &properties; make direct contributions to this &equation;:"
            print >> phile, "<itemizedlist>"
            for prop in properties:
                print >> phile, "<listitem><simpara>"
                print >> phile, "<xref linkend='Property-%s'/>" % (
                    prop.name().replace(':','-'))
                print >> phile, "</simpara></listitem>"
            print >> phile, "</itemizedlist>"
            print >> phile, "Other &properties; make indirect contributions to the &equation; through the <link linkend='Flux-%s'><classname>%s</classname></link>." % (eqn.fluxname(), eqn.fluxname())
            print >> phile, "</simpara></listitem>"
        print >> phile, "</itemizedlist>"
        print >> phile, "</refsect1> <!-- Details -->"
        print >> phile, "<refsect1>"
        print >> phile, "<title>Description</title>"
        try:
            src = file("DISCUSSIONS/engine/builtin/eqn-%s.xml" % name, "r")
        except IOError:
            print >> phile, "<para>MISSING DISCUSSION FOR %s</para>" % name
        else:
            print >> phile, src.read()
            src.close()
        print >> phile, "</refsect1> <!-- Description-->"
        
        print >> phile, "</refentry>"
        
    print >> phile, "</section> <!-- Equations -->"

    print >> phile, "</section> <!-- Built-In Physics -->"
    

xmlmenudump.addSection(xmldump, 5)


