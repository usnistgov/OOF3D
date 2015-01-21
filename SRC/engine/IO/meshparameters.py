# -*- python -*-
# $RCSfile: meshparameters.py,v $
# $Revision: 1.51.4.6 $
# $Author: langer $
# $Date: 2014/04/26 22:57:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Special file for the definitions of the parameters corresponding to
# mesh and subproblem objects.  These principally exist so that they
# can have widgets, which can auto-update with new lists of the
# relevant object when the GUI switches meshes.

from ooflib.SWIG.common import config
from ooflib.SWIG.engine import equation
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import flux
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
import types

class FieldParameterBase(parameter.ObjParameter, parameter.Parameter):
    def __init__(self, name, value=None, default=None, tip=None, outofplane=0,
                 auxData={}):
        # outofplane is meaningful only in 2D, but is harmless in 3D.
        self.outofplane = outofplane    # allow out-of-plane fields as values?
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    def clone(self):
        return self.__class__(self.name, self.value, self.default, self.tip,
                              self.outofplane)
    
    def checker(self, x):
        if not isinstance(x, field.FieldPtr):
            parameter.raiseTypeError(x, "Field")
        # if not self.outofplane and not isinstance(x, field.CompoundFieldPtr):
        #     parameter.raiseTypeError(x, "CompoundField")
            
    def incomputable(self, context):
        if not context:
            return noobjmsg
        incomp = parameter.Parameter.incomputable(self, context)
        if incomp:
            return incomp
##        if not context.is_defined_field(self.value): 
##            return nofieldmsg % self.value.name()
        return False
    def valueDesc(self):
        return "A <link linkend='Section-Concepts-Mesh-Field'><classname>Field</classname></link> object."

class FieldParameter(FieldParameterBase):
    noobjmsg = "Mesh is not defined."
##    nofieldmsg = "Field '%s' is not defined on the Mesh."

class SubProblemFieldParameter(FieldParameter):
    noobjmsg = "SubProblem is not defined."
##    nofieldmsg = "Field '%s' is not defined on the SubProblem."

##class FieldAnywayParameter(FieldParameter):
##    # Never is incomputable.  See Element::outputFieldsAnyway.
##    def incomputable(self, context):
##        return 0

# class TwoVectorFieldParameter(FieldParameter): # Not used?
#     def checker(self, x):
#         if not isinstance(x, field.TwoVectorFieldPtr):
#             parameter.raiseTypeError(x, "TwoVectorField")
#     def valueDesc(self):
#         return "A two component vector <link linkend='Section-Concepts-Mesh-Field'><classname>Field</classname></link>."
    
class FluxParameter(parameter.ObjParameter, parameter.Parameter):
    def checker(self, x):
        if not isinstance(x, flux.FluxPtr):
            parameter.raiseTypeError(x, "Flux")
    def valueDesc(self):
        return "A <link linkend='Section-Concepts-Mesh-Flux'><classname>Flux</classname></link> object."
    def incomputable(self, mesh):
        return (parameter.Parameter.incomputable(self, mesh)
                or not mesh.materialsConsistent())

class SubProblemFluxParameter(FluxParameter):
    pass

class EquationParameter(parameter.ObjParameter, parameter.Parameter):
    def checker(self, x):
        if not isinstance(x, equation.EquationPtr):
            parameter.raiseTypeError(x, "Equation")
    def valueDesc(self):
        return "An <link linkend='Section-Concepts-Mesh-Equation'><classname>Equation</classname></link> object."

class SubProblemEquationParameter(EquationParameter):
    pass

class EquationBCParameter(parameter.ObjParameter, parameter.Parameter):
    def checker(self, x):
        if not isinstance(x, equation.EquationPtr) or not x.allow_boundary_conditions():
            parameter.raiseTypeError(x, "Equation with BC capability")
    def valueDesc(self):
        return "An <link linkend='Section-Concepts-Mesh-Equation'><classname>Equation</classname></link> object which can be used in boundary conditions."

class SubProblemEquationBCParameter(EquationBCParameter):
    pass

class FieldIndexParameter(parameter.StringParameter):
    def valueDesc(self):
        return "A character string representing a field or flux index (eg, <userinput>'x'</userinput>)."

########################

# Special parameters for mesh boundaries -- these have widgets which
# present only the names of the right sorts of boundaries, and only
# those which are of nonzero size.

class MeshBoundaryParameter(parameter.StringParameter):
    def valueDesc(self):
        if config.dimension() == 2:
            return "The name of a point or edge boundary in a mesh."
        return "The name of a point, edge, or face boundary in a mesh."

if config.dimension() == 3:
    class MeshFaceBdyParameter(MeshBoundaryParameter):
        def valueDesc(self):
            return "The name of a face boundary in a mesh."

class MeshEdgeBdyParameter(MeshBoundaryParameter):
    def valueDesc(self):
        return "The name of an edge boundary in a mesh."

class MeshFaceBdyParameter(MeshBoundaryParameter):
    def valueDesc(self):
        return "The name of a face boundary in a mesh."

class MeshPeriodicEdgeBdyParameter(MeshBoundaryParameter):
    def valueDesc(self):
        return "A string containing the names of two periodic edge boundaries in a mesh, separated by a space."

class MeshPointBdyParameter(MeshBoundaryParameter):
    def valueDesc(self):
        return "The name of a point boundary in a mesh."

#Interface branch
class MeshEdgeBdyInterfaceParameter(MeshBoundaryParameter):
    def valueDesc(self):
        return "The name of an edge boundary or interface in a mesh."

#Includes "<every>"
class MeshEdgeBdyParameterExtra(placeholder.PlaceHolderParameter):
    types = (types.StringType, placeholder.every)
    def valueDesc(self):
        return "The name of an edge boundary in a mesh."
    
class MeshFaceBdyParameterExtra(placeholder.PlaceHolderParameter):
    types = (types.StringType, placeholder.every)
    def valueDesc(self):
        return "The name of an edge boundary in a mesh."
    
