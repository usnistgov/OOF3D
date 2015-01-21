# -*- python -*-
# $RCSfile: relaxation.py,v $
# $Revision: 1.53.2.13 $
# $Author: langer $
# $Date: 2014/09/17 21:26:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## TODO MER: This file has not yet been merged with the 2D branch, and so
## does not use the modern solver and boundary condition code.

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import progress
from ooflib.SWIG.engine import equation
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import masterelement
from ooflib.SWIG.engine import material
from ooflib.SWIG.engine import preconditioner
from ooflib.SWIG.engine.property.elasticity.iso import iso
from ooflib.SWIG.engine.property.skeletonrelaxationrate import skeletonrelaxationrate
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import bdycondition
from ooflib.engine import evolve
from ooflib.engine import fieldinit
from ooflib.engine import linearity
from ooflib.engine import materialmanager
from ooflib.engine import matrixmethod
from ooflib.engine import profile
#from ooflib.engine import skeletonmodifier
from ooflib.SWIG.engine import cskeletonmodifier
from ooflib.engine import staticstep
from ooflib.engine.IO import meshmenu
import ooflib.engine.mesh
import sys

## TODO 3.1: Update for 3D. Move to C++.  The 2D code has changed
## since the branch.

# Make an instance of the elasticity property at oof2 start up time
# with default parameter values.  It can't be done when Relax is
# called because the parameters may have changed by then, and Relax
# expects to find the default values.  TODO 3.1: This is ugly. The values
# that Relax needs should be explicitly set by Relax, so that it
# doesn't have to rely on the default values.  What if the default
# values change?

stiffness = iso.IsotropicElasticity()

class Relax(cskeletonmodifier.CSkeletonModifier):

    materialName = '__bone_marrow__'

    def __init__(self, alpha, gamma, iterations):
        self.alpha = alpha
        self.gamma = gamma
        self.iterations = iterations
        self.count = 0
        self.solver_converged = True
        self.meshname = None

        ## create material
        materialmanager.materialmanager.add_secret(self.materialName)
        ## SkeletonRelaxationRateTensor is the PropertyRegistration for the
        ## SkeletonRelaxationRate property.
        beta_parameter = skeletonrelaxationrate.SkeletonRelaxationRateTensor.getParameter('beta')
        beta_parameter.value = self.alpha # having trouble deciding on a name?
        ## TODO 3.1: Change names in skeletonrelaxationrate.* so alpha can be alpha
        alpha_parameter = skeletonrelaxationrate.SkeletonRelaxationRateTensor.getParameter('alpha')
        alpha_parameter.value = self.gamma
        self.skelRelRate = skeletonrelaxationrate.SkeletonRelaxationRateTensor()
        ## assign properties for material
        materialmanager.materialmanager.add_prop(self.materialName,
                                                 stiffness.name())
        materialmanager.materialmanager.add_prop(self.materialName,
                                                 self.skelRelRate.name())

    def material(self):
        return materialmanager.getMaterial(self.materialName)

    def goodToGo(self, skeleton):
        #skeleton.checkIllegality()
        return (not skeleton.illegal()
                and self.count < self.iterations
                and self.solver_converged)
    def updateIteration(self):
        self.count +=1

    def set_fakematerial(self, skelelement, skeleton):
        return self.material()

    def create_mesh(self, context):
        ## context is a skeleton context
        ## setup element types
        edict = {}
        # get linear isoparametric master elements
        if config.dimension() == 2:
            edict['Triangle'] = masterelement.getMasterElementDict()['T3_3']
            edict['Quadrilateral'] = masterelement.getMasterElementDict()['Q4_4']
        elif config.dimension() == 3:
            edict['Tetrahedron'] = masterelement.getMasterElementDict()['TET4_4']
        skel = context.getObject()
        ## returns a Mesh (Who) object
        self.meshname = context.path() + ":__internal_mesh__"
        #Interface branch, pass skeleton path to femesh
        femesh = skel.femesh(edict, self.material()) #, self.set_fakematerial, context.path())
        meshcontext = ooflib.engine.mesh.meshes.add(
            self.meshname, femesh,
            parent=context,
            skeleton=skel, elementdict=edict)
        meshcontext.createDefaultSubProblem()
        
        return meshcontext

    def define_fields(self, meshctxt):
        femesh = meshctxt.femesh()
        subp = meshctxt.get_default_subproblem().getObject()
        displacement = field.getField('Displacement')
        subp.define_field(displacement)
        subp.activate_field(displacement)
        if config.dimension() == 2:
            meshctxt.set_in_plane_field(displacement, True)
        
    def activate_equations(self, meshctxt):
        meshctxt.get_default_subproblem().getObject().activate_equation(
            equation.getEquation('Force_Balance'))

    def set_boundary_conditions(self, mesh):
        ## here, mesh is a Mesh (Who) object
        displacement = field.getField('Displacement')
        ## left boundary
        self.leftBoundaryCondition = \
             bdycondition.DirichletBC(displacement,
                                      'x',
                                      equation.getEquation('Force_Balance'),
                                      'x',
                                      profile.ConstantProfile(0),
                                      'Xmin'
                                      )
        self.leftBoundaryCondition.add_to_mesh('left', mesh.path())

        ## right boundary
        self.rightBoundaryCondition = \
             bdycondition.DirichletBC(displacement,
                                      'x',
                                      equation.getEquation('Force_Balance'),
                                      'x',
                                      profile.ConstantProfile(0),
                                      'Xmax'
                                      )
        self.rightBoundaryCondition.add_to_mesh('right', mesh.path())

        ## top boundary
        self.topBoundaryCondition = \
             bdycondition.DirichletBC(displacement,
                                      'y',
                                      equation.getEquation('Force_Balance'),
                                      'y',
                                      profile.ConstantProfile(0),
                                      'Ymax'
                                      )
        self.topBoundaryCondition.add_to_mesh('top', mesh.path())

        ## bottom boundary
        self.bottomBoundaryCondition = \
             bdycondition.DirichletBC(displacement,
                                      'y',
                                      equation.getEquation('Force_Balance'),
                                      'y',
                                      profile.ConstantProfile(0),
                                      'Ymin'
                                      )
        self.bottomBoundaryCondition.add_to_mesh('bottom', mesh.path())

        if config.dimension() == 3:
            ## front boundary
            self.frontBoundaryCondition = \
                 bdycondition.DirichletBC(displacement,
                                          'z',
                                          equation.getEquation('Force_Balance'),
                                          'z',
                                          profile.ConstantProfile(0),
                                          'Zmax'
                                          )
            self.frontBoundaryCondition.add_to_mesh('front', mesh.path())

            ## back boundary
            self.backBoundaryCondition = \
                 bdycondition.DirichletBC(displacement,
                                          'z',
                                          equation.getEquation('Force_Balance'),
                                          'z',
                                          profile.ConstantProfile(0),
                                          'Zmin'
                                          )
            self.backBoundaryCondition.add_to_mesh('back', mesh.path())

    def update_node_positions(self, skeleton, mesh):
        skeleton.incrementTimestamp()
        ## mesh is a Mesh Who object
        femesh = mesh.getObject()
        displacement = field.getField('Displacement')
        # TODO OPT: this should probably be moved to C
        for i in range(skeleton.nnodes()):
            node = skeleton.getNode(i)
            #Interface branch
##            realnode = femesh.getNode(node.meshindex)
            skelel = node.getElement(0)
            realel = femesh.getElement(skelel.getIndex())
            realnode = realel.getCornerNode(skelel.getNodeIndexIntoList(node))

            dx = displacement.value(femesh, realnode, 0)
            dy = displacement.value(femesh, realnode, 1)
            if config.dimension() == 2:
                skeleton.moveNodeBy(node, primitives.Point(dx, dy))
            elif config.dimension() == 3:
                dz = displacement.value(femesh, realnode, 2)
                skeleton.moveNodeBy(node, (dx, dy, dz))

    def apply(self, oldskeleton):
        prog = progress.getProgress("Relax", progress.DEFINITE)
        prog.setMessage("Preparing to relax...")
        # oldskeleton.clearElementHomogeneityCache()
        return oldskeleton.deputyCopy()

    def initialize_fields(self, mesh):
        if config.dimension() == 2:
            initializer = fieldinit.ConstTwoVectorFieldInit(cx=0.0,cy=0.0)
        elif config.dimension() == 3:
            initializer = fieldinit.ConstTwoVectorFieldInit(cx=0.0,cy=0.0,cz=0.0)
        meshmenu.initField(self, self.meshname, field.getField('Displacement'),
                           initializer)
        meshmenu.applyFieldInits(self, self.meshname)

    def postProcess(self, context):
        ## This function first creates a mesh with custom-made properties,
        ## then assigns "temporary" properties to pixels
        ## and specifies BCs and equations.
        ## Next, iterates for the solution using the specified solver,
        ## accepts all node moves and redraws skeleton.
        ## It repeats these steps until iteration criteria has been met.
        ## Finally, the (temporary) mesh and the rest  of the temporary
        ## objects are cleaned up.

        ## create progress bar
        prog = progress.getProgress("Relax", progress.DEFINITE)
        
        ## get skeleton and calculate energy
        skeleton = context.getObject()
        before = skeleton.energyTotal(self.alpha)
        self.count = 0

        while self.goodToGo(skeleton) and not prog.stopped():
            ## femesh is created and properties are assigned
            mesh = self.create_mesh(context) # mesh context object
            
            ## define displacement and temperature fields
            self.define_fields(mesh)
            ## activate the mechanical balance equation
            self.activate_equations(mesh)
            mesh.changed("Relaxing") # TODO OPT: is this necessary?
            ## constrain the nodes on the boundaries to only slide
            ## along the edge
            self.set_boundary_conditions(mesh)

            # solve linear system.
            self.coreProcess(mesh, mesh.get_default_subproblem())
            if prog.stopped():
                break

            # Update positions of nodes in the Skeleton
            context.begin_writing()
            try:
                self.update_node_positions(skeleton, mesh)
            finally:
                context.end_writing()
            
            mesh.lockAndDelete()
                
            switchboard.notify("redraw")

            self.updateIteration() ## update iteration manager machinery
            prog.setFraction(1.0*self.count/self.iterations)
            prog.setMessage("%d/%d iterations" % (self.count, self.iterations))

        prog.finish()
        
        ## calculate total energy improvement, if any.
        after = skeleton.energyTotal(self.alpha)
        if before:
            rate = 100.0*(before-after)/before
        else:
            rate = 0.0
        diffE = after - before
        reporter.report("Relaxation complete: deltaE = %10.4e (%6.3f%%)"
                        % (diffE, rate))
        
        del self.topBoundaryCondition
        del self.leftBoundaryCondition
        del self.bottomBoundaryCondition
        del self.rightBoundaryCondition
        if config.dimension() == 3:
            del self.backBoundaryCondition
            del self.frontBoundaryCondition
        materialmanager.materialmanager.delete_prop(stiffness.name())
        materialmanager.materialmanager.delete_prop(self.skelRelRate.name())
        materialmanager.materialmanager.delete_secret(self.materialName)
#         del self.skeletonMaterial
        
        
    def coreProcess(self, meshctxt, subp):
        subp.solver = staticstep.StaticDriver(
            matrixmethod.ConjugateGradient(
                preconditioner.ILUPreconditioner(),
                1.e-5,          # tolerance
                1000            # max_iterations
                )
            )
        subp.solver_linearity = linearity.Linear()

        meshctxt.begin_writing()
        try:
            meshctxt.solver_precompute()
            try:
                evolve.evolve(meshctxt, 0.0, 0.0, False)
            except:
                # TODO 3.1: Be more explicit about what exceptions should
                # be handled here, to distinguish actual convergence
                # failures from programming errors.
                self.solver_converged = False
            else:
                self.solver_converged = True
        finally:
            meshctxt.end_writing()

    ## overriding some methods so that this will work in python
    def __repr__(self):
        return "Relaxation"

    def get_progressbar_type(self):
        return "continuous"

#################################################

if config.dimension() == 2:
    registeredclass.Registration(
        'Relax',
        cskeletonmodifier.CSkeletonModifier,
        Relax,
        ordering=0.5,
        params=[
            cskeletonmodifier.alphaParameter,
            parameter.FloatParameter(name = 'gamma', value = 0.5,
                                     tip='Node mobility'),
            parameter.IntParameter('iterations', value = 1,
                                   tip='number of steps')
            ],
        tip='Improve a skeleton by solving a finite element system where the properties are functions of the underlying homogeneity and shape',
        discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/relax.xml')
        )


# Old tip for gamma:
#    tip='Coefficient of mesh expansion or rate of
#    expansion/contraction per inhomogeneity or per deviation from
#    ideal shape. A small positive value is recommended for meshes
#    where element edges want to be made coincide with pixel group
#    edges.'
