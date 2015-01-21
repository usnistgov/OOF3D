# -*- python -*-
# $RCSfile: strawberry.py,v $
# $Revision: 1.9.8.1 $
# $Author: langer $
# $Date: 2014/09/27 22:35:14 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This file is meant to be a template for adding a new Field, Flux,
# Equation, and material Property to OOF2.  The physics defined in
# this file is speculative.

# For more details, including a complete description of all of the
# classes that can be used in this file, see the "Extending OOF2"
# chapter of the OOF2 manual.

from ooflib.engine import problem
from ooflib.SWIG.engine import equation
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import flux

# Define a new Field.  The available field classes are ScalarField
# (for scalars like Temperature) and TwoVectorField (for vectors like
# Displacement.  The 'Two' in 'TwoVectorField' refers to the number of
# in-plane components.  When OOF gets a third dimension, all
# VectorFields will have three components.)

Strawberry = problem.advertise(field.ScalarField('Strawberry'))

# Define a new Flux.  The available classes are VectorFlux (eg,
# HeatFlux, ElectricCurrent) and SymmetricTensorFlux (eg Stress).

Jam = problem.advertise(flux.VectorFlux('Strawberry_Jam'))

# Define a new Divergence Equation.  The equation equates the
# divergence of a given flux with some external forcing terms.  The
# external forces are specified by Material Properties.  The
# relationships between the Fields and the Flux are also given by
# Material Properties (ie, they're not specified here!).

JamEqn = problem.advertise(equation.DivergenceEquation(
    'Jam_Eqn', 
    Jam,
    1,                      # the number of components of the divergence
    ))


# Define a new PlaneFluxEquation.  When this equation is active, it
# specifies that the out-of-plane components of flux are zero.  Note
# that, unlike DivergenceEquation, PlaneFluxEquation is a pure swigged
# class, and can't take python keyword arguments.  See the OOF2 manual
# for more about out-of-plane components.

OutOfPlaneJam = problem.advertise(equation.PlaneFluxEquation(
    'Plane_Jam_Eqn',                    # name of the equation
    Jam,                                # the flux it applies to
    1                                   # the number of out-of-plane components
    ))


# Sometimes the finite element stiffness matrix can be made symmetric
# by putting the rows (equations) in the same order as the columns
# (degrees of freedom).  To do this, a correspondence has to be
# established between equation components and field components.  The
# conjugatePair class sets up this correspondence.  Each conjugatePair
# object specifies that a particular equation component corresponds to
# a particular Field component when coupled by a particular *type* of
# Property.  The Property type is just a string.  It appears in the
# PropertyRegistration specification (see below) and it has to be the
# same for all Property classes that play the same physical role (eg, all
# elasticity classes have type "Elasticity").

# If the conjugatePair information is omitted, OOF2 will still run
# properly, but it will not use the more efficient symmetric matrix
# solvers because it will not know how to symmetrize the matrix.

from ooflib.engine import conjugate
from ooflib.SWIG.engine import fieldindex

# Field and Equation components are both specified by instances of
# FieldIndex classes.  A ScalarFieldIndex has only one value.  It's
# only purpose is to make it possible to treat scalar fields the same
# way as other more complicated fields.
fx = fieldindex.ScalarFieldIndex()

conjugate.conjugatePair(
    "Frivolous",                        # the property type
    JamEqn, fx,                         # the equation, and its component
    Strawberry, fx)                     # the field, and its component

fz = fieldindex.OutOfPlaneVectorFieldIndex(2)
conjugate.conjugatePair("Frivolous",
                        OutOfPlaneJam, fz,
                        Strawberry.out_of_plane(), fz)


# A material Property is what connects a Field to a Flux.  Properties
# are almost always defined in C++ code, but their Registrations are
# in Python.

# Load the module containing the Property subclass code.
import fruitSWIG.fruitproperty

from ooflib.common.IO import parameter
from ooflib.engine import propertyregistration
from ooflib.SWIG.engine import symmmatrix

propertyregistration.PropertyRegistration(
    # The "name" is really a colon separated list of names, specifying a
    # hierarchical path in the tree of Property classes.  The name
    # here puts a property called 'StrawberryProp" in the "Fruits"
    # branch of the tree.
    name = "Fruits:StrawberryPropsicle",

    # "subclass" is the swigged C++ class that represents the
    # property.  It is a subclass of the Property C++ class.
    subclass = fruitSWIG.fruitproperty.FruitProperty,

    # "modulename" is the name of the Python module containing the swigged
    # property code.
    modulename="fruitSWIG.fruitproperty",

    # "ordering" determines the placement of the property in the lists
    # in the GUI.  It has no other significance.
    ordering=100000,

    # The remainder of the PropertyRegistration arguments are
    # optional.

    # "params" is a list of Parameter objects, describing the input
    # parameters for the property.  This example defines two
    # parameters, a Trigonal second rank tensor named "modulus" and a
    # scalar named "coupling".
    
    params = [
        symmmatrix.TrigonalRank2TensorParameter(
            "modulus",                      # name
            symmmatrix.TrigonalRank2Tensor(xx=1.0, zz=0.5), # default value
            tip="Nothing is real."),        # a helpful note
        parameter.FloatParameter("coupling", # name
                                 10.,       # default value
                                 tip="Nothing to get hung about.")
    ],

    # "fields" is a list of the Fields that the Property uses.  The
    # Property won't make any contribution to the finite element
    # computation unless all of these Fields are defined on the Mesh.
    fields = [Strawberry, problem.Temperature],

    # "fluxes" is a list of the Fluxes that this property contributes
    # to.  The Property will be ignored in finite element calculations
    # unless equations involving these fluxes are being solved.
    fluxes = [Jam],

    # The "propertyType" is the same string that identifies this
    # Property in the conjugatePair call, above.
    propertyType="Frivolous",

    # "outputs" is a list of the names of output quantities that this
    # Property contributes to.  Instructions for adding new kinds of
    # outputs will be written elsewhere.
    outputs=["Energy"],

    # "nonlinear is a boolean value indicating whether or not
    # equations using this Property will benefit from a non-linear
    # solver.
    nonlinear=False,

    # "secret" is a boolean indicating whether this Property should be
    # visible in the GUI.  You probably don't want to set its value.
    secret=False,

    # "tip" is a help string that will appear in the GUI tooltips.
    # Omit it or set it to parameter.emptyTipString if you don't want
    # anything to appear.
    
    tip="Living is easy with eyes closed.",

    # "discussion" is a longer explanation of the Property.  It
    # appears in the automatically generated reference section of the
    # OOF2 manual.  You can safely omit it.
    discussion = parameter.emptyTipString)
    
    
