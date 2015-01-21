# -*- python -*-
# $RCSfile: errorestimator.py,v $
# $Revision: 1.29.2.3 $
# $Author: fyc $
# $Date: 2014/07/24 21:36:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Error estimators for adaptive mesh refinement.  Error management for
# adaptive time stepping is in steperrorscaling.*.

## TODO OPT:  Move this to C++.  Skeleton refinement is in C++ in 3D.
from ooflib.SWIG.common import config
assert config.dimension() == 2

from ooflib.SWIG.common import progress
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import mainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import refinementtarget
from ooflib.engine.IO import meshparameters
import ooflib.engine.mesh
#AMR subproblem
import ooflib.engine.subproblemcontext


# ErrorEstimator base class
class ErrorEstimator(registeredclass.RegisteredClass):
    registry = []
    # If an ErrorEstimator needs a preprocess, it should be added.
    #AMR subproblem, pass subproblem
    def preprocess(self, subproblem):
        pass
    tip = "Error estimators."
    discussion = xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/errorestimator.xml')

####################################

class ErrorNorm(registeredclass.RegisteredClass):
    registry = []
    #AMR subproblem, pass subproblem
    def preprocess(self, subproblem, flux):  # to be overridden by child class.
        pass
    tip = "How to measure error?"
    discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/reg/errornorm.xml')

## TODO MER: The ErrorNorms defined here only work for the ZZ error
## estimator.  The classes need to rearranged so that the norm classes
## are independent of the estimator classes.  After all, we may
## someday have more than one estimator.  If it's not possible to
## refactor the classes like that, then the ErrorNorm classes must at
## least be renamed so that it's clear that they are only meant to be
## used with the ZZ estimator.
    
class L2ErrorNorm(ErrorNorm):
    #AMR subproblem, pass subproblem
    def __call__(self, element, subproblem, flux):
        return subproblem.zz_L2_estimate(element, flux)
    
registeredclass.Registration(
    'L2 Error Norm',
    ErrorNorm,
    L2ErrorNorm,
    ordering=0,
    tip="Use the root mean square of the components of the error.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/l2errornorm.xml'))

class WeightedL2ErrorNorm(ErrorNorm):
    def __init__(self):
        self.weights = None
    #AMR subproblem, pass subproblem
    def preprocess(self, subproblem, flux):
        bottom = 0.0  # [bottom, top] : the range normalized values
        top = 0.3     # to be weighted.
        self.weights = subproblem.zz_L2_weights(flux, bottom, top)
    #AMR subproblem, pass subproblem
    def __call__(self, element, subproblem, flux):
        index = element.get_index()
        return subproblem.zz_L2_estimate(element, flux)*self.weights[index]
    
registeredclass.Registration(
    'Weighted L2 Error Norm',
    ErrorNorm,
    WeightedL2ErrorNorm,
    ordering=1,
    tip="Use the weighted root mean square of the components of the error.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/l2weightednorm.xml')
    )

####################################

class ZZ_Estimator(ErrorEstimator):
    def __init__(self, norm, flux, threshold):
        self.norm = norm  # how to normalize at each point
        self.flux = flux  # which flux?
        self.threshold = threshold  # acceptable relative error (percent)
    def preprocess(self, subproblem):
        # Superconvergent patch recovery -- Recover flux at each node.
        meshcontext=subproblem.meshcontext
        skel = meshcontext.getSkeleton()
        subproblem.create_scpatch(skel) # in csubproblem.spy
        subproblem.flux_recovery()      # in csubproblem.spy
        self.norm.preprocess(subproblem, self.flux)
    def __call__(self, element, subproblem):
        # Perform an error estimation on the element.
        # FEMesh will take care of the computation.
#         result= self.threshold < self.norm(element, subproblem, self.flux)*100.
#         if result:
#             debug.fmsg("threshold=", self.threshold, "norm=",
#                        self.norm(element, subproblem, self.flux)*100)
#         return result
        return self.threshold < self.norm(element, subproblem, self.flux)*100.

# Dummy parameter for smart widget
class ZZFluxParameter(meshparameters.FluxParameter):
    pass

registeredclass.Registration(
    'Z-Z Estimator',
    ErrorEstimator,
    ZZ_Estimator,
    ordering=0.,
    params=[
    parameter.RegisteredParameter('norm',
                                  ErrorNorm,
                                  tip="How to measure the size of an error."),
    ZZFluxParameter('flux', tip=parameter.emptyTipString),
    parameter.FloatRangeParameter('threshold', (0.0, 100.0, 0.5),
                                  value=10.,
                                  tip='Maximum allowable percentage error.')
    ],
    tip="Error estimation by Zienkiewicz and Zhu's superconvergent patch recovery.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/zzspr.xml'))

################################

# RefinementTarget for AdaptiveMeshRefinement.  Marks all elements
# that fail the error estimator test.
class AdaptiveMeshRefine(refinementtarget.RefinementTarget):
    def __init__(self, subproblem, estimator):
        #self.mesh = mesh  # mesh
        self.subproblem = subproblem
        self.estimator = estimator  # ErrorEstimator instance
            
    def __call__(self, skeleton, context, divisions, markedEdges, criterion):
        subproblemobj = ooflib.engine.subproblemcontext.subproblems[
            self.subproblem].getObject()
        femesh=subproblemobj.mesh
        self.estimator.preprocess(subproblemobj)
        prog = progress.findProgress("Refine")
        elements = skeleton.activeElements()
        n = len(elements)
        for i, element in enumerate(elements):
            # If the refinement is done more than once from the skeleton
            # page (after a mesh has been created),
            # some of the new skeleton elements may not have
            # corresponding mesh elements, i.e. element.meshindex is
            # undefined. The second refinement could be done after
            # a new mesh is created from the first refinement.
            fe_element = femesh.getElement(element.meshindex)
            if not subproblemobj.contains(fe_element):
                continue
            if not fe_element.material():
                continue
            if (self.estimator(fe_element, subproblemobj) and 
                criterion(skeleton, element)):
                self.markElement(element, divisions, markedEdges)
            if prog.stopped() :
                return
            prog.setFraction(1.0*(i+1)/n)
            prog.setMessage("checked %d/%d elements" % (i+1, n))

#####################

# A trivial WhoParameter for a smart widget.
# When adaptively refining mesh, "OK" button (in Skeleton Page) should be
# available ONLY when the current skeleton is the base skeleton of
# the to-be-refined mesh.
# The widget is set in IO/GUI/adaptivemeshrefineWidget.py
class AMRWhoParameter(whoville.WhoParameter):
    pass

#####################

registeredclass.Registration(
    'Adaptive Mesh Refinement',
    refinementtarget.RefinementTarget,
    AdaptiveMeshRefine,
    ordering=6,
    params=[
##    AMRWhoParameter("mesh", ooflib.engine.mesh.meshes,
##                    tip="Apply adaptive refinement to this mesh."),
    AMRWhoParameter("subproblem", ooflib.engine.subproblemcontext.subproblems,
                    tip="Apply adaptive refinement to this subproblem."),
    parameter.RegisteredParameter("estimator",
                                  ErrorEstimator,
                                  tip="Which error estimator to use.")
    ],
    tip="Refine less accurate elements.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/adaptivemeshrefine.xml'))
