# -*- python -*-
# $RCSfile: rationalize.py,v $
# $Revision: 1.88.2.6 $
# $Author: langer $
# $Date: 2014/08/20 02:21:22 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


## NOTE: Each RationalizeMethod is initialized with an internal
## gerund parameter. This parameter reports via the progress bar
## (through the progress bar message) the gerund of the action
## (rationalize method) that is being executed. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import progress
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common import cregisteredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
from ooflib.SWIG.engine import cskeletonmodifier
from ooflib.SWIG.engine import crationalizers
import random

##################################################

# Subclasses of Rationalizer must have a function "findAndFix" which
# takes a skeleton and an element as arguments and returns a list of
# ProvisionalChanges objects indicating what can be done.
# ProvisionalChanges is defined in skeleton.py. (Skeleton.mergeNode()
# returns one.)  They must also have a "fixAll" function that does the
# same thing, but doesn't bother checking the elements first.

# When using AutomaticRationalization, the Rationalizers are called in
# the order of their Registrations.  Therefore the Rationalizers that
# need to be called last (eg RemoveBadTriangle) need to have large
# 'ordering's.

# class Rationalizer(registeredclass.RegisteredClass):
#     registry = []

#     def __call__(self, skel, context, targets, criterion, fixer):
#         prog = progress.findProgress("Rationalize")
#         # Copy the element list from skeleton.element before
#         # rationalizing. This is necessary because rationalizing
#         # modifies the Skeleton's element list. 
#         elements = targets(skel, context, copy=1)
#         random.shuffle(elements)
#         executed_action = self.getRegistration().gerund
#         processed = {}
#         count = 0
#         done = 0  # No. of rationalized elements
#         nel = len(elements)  # No. of elements in the list
#         for element in elements:
#             count += 1  # The i-th element being processed ... for progress bar
#             if not processed.has_key(element) and element.active(skel):
#                 # fixer is either self.findAndFix or self.fixAll. They
#                 # return a list of ProvisionalChanges objects, from
#                 # which we pick the best one.
#                 changes = fixer(skel, element)
#                 bestchange = criterion(changes, skel)
#                 if bestchange is not None:
#                     done += bestchange.nRemoved()
#                     # Accepting the change converts provisional
#                     # elements to actual elements.
#                     bestchange.accept(skel)
#                     for elephant in bestchange.removed:
#                         processed[elephant] = 1
#                     for oldel, newel in bestchange.substitutions:
#                         # If an unprocessed element has been replaced,
#                         # its replacement still has to be processed.
#                         # The element being replaced should *not* be
#                         # processed, in any case, since it's no longer
#                         # in the skeleton.
#                         # If the criterion is "Unconditional" or
#                         # "Limited Unconditional", it doesn't add subs to
#                         # the list.
#                         if not processed.has_key(oldel):
#                             processed[oldel] = 1
#                             if criterion.addSubstitute(elements, newel):
#                                 nel += 1
#             if prog.stopped():
#                 break
#             else:
#                 prog.setFraction(1.0*count/nel)
#                 prog.setMessage(executed_action + " %d/%d" % (count, nel))
#         skel.cleanUp()

        
#         reporter.report("%d elements rationalized : %s."
#                         % (done, self.getRegistration().name()))

#     tip = "Specific tools to remove badly shaped Elements from Skeletons."
#     discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/reg/rationalizer.xml')

################################################################

## In order for the widget for the list of RationalizeMethods to come
## up by default with all of the methods enabled, the "methods"
## parameter needs to be set to a list containing an instance of each
## RationalizeMethod.  This list is constructed here, and it's updated
## each time a new RationalizeMethod is created.  The update is done
## carefully, so that the id of the list doesn't change, so that the
## RegisteredListParameter still refers to the correct list.
    
def _updateDefaults():
    # rebuild list in place.  Don't just do "defaults = [...]" !
    global defaults
    del defaults[:]                   
    defaults += [reg() for reg in crationalizers.RationalizerPtr.registry]

defaults = []
_updateDefaults()
switchboard.requestCallback(crationalizers.RationalizerPtr, _updateDefaults)

################################################################

class RationalizeMethod(registeredclass.RegisteredClass):
    registry = []
    tip = "Strategies for removing bad elements from a Skeleton"
    discussion = xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/rationalizemethod.xml')

## The Automatic RationalizeMethod applies the rationalizers to *all*
## elements in the target set and picks the best rationalization, or
## reverts to the original element.  It has no criteria (minimum
## angles, etc), unlike the Specified RationalizeMethod.

class AutomaticRationalization(RationalizeMethod):
    def rationalize(self, skel, targets, criterion):
        prog = progress.getProgress("Rationalize", progress.DEFINITE)
        for ratreg in crationalizers.RationalizerPtr.registry:
            # Create a Rationalizer from a Registration.  Since fixAll
            # doesn't use the Rationalizer's parameters, just use the
            # default values.
            ratmethod = ratreg()
            ratmethod.rationalizeAll(skel, targets, criterion)
            if prog.stopped():
                break
        prog.finish()
    
registeredclass.Registration(
    'Automatic',
    RationalizeMethod,
    AutomaticRationalization, 
    ordering=1,
    tip = 'Automatically fix badly shaped Skeleton elements.',
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/ration_automatic.xml')
    ) 

class SpecificRationalization(RationalizeMethod):
    def __init__(self, rationalizers):
        self.rationalizers = rationalizers

    def rationalize(self, skel, targets, criterion):
        prog = progress.getProgress("Rationalize", progress.DEFINITE)
        for rationalizer in self.rationalizers:
            rationalizer.findAndRationalize(skel, targets, criterion)
            if prog.stopped(): 
                break
        prog.finish()

registeredclass.Registration(
    'Specified',
    RationalizeMethod,
    SpecificRationalization,
    ordering=0,
    params = [
        parameter.RegisteredListParameter('rationalizers',
                                          crationalizers.RationalizerPtr,
                                          value=defaults,
                                          tip = 'Which rationalizer(s) to use.')
        ],
    tip = 'Apply specific tools to fix badly shaped Skeleton elements.',
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/ration_specified.xml'))

################################################################

class Rationalize(cskeletonmodifier.CSkeletonModifierBase):
    def __init__(self, targets, criterion, method):
        self.targets = targets          # all or selected
        self.criterion = criterion      # unconditional or conditional
        self.method = method            # automatic or specified
        cskeletonmodifier.CSkeletonModifierBase.__init__(self)

    def apply(self, oldskeleton): #, context):
        skel = oldskeleton.completeCopy()
        self.method.rationalize(skel, self.targets, self.criterion)
        return skel

    def postProcess(self,context):
        pass


#########################

cregisteredclass.Registration(
    'Rationalize',
    cskeletonmodifier.CSkeletonModifierBasePtr,
    Rationalize,
    ordering=5,
    params=[
        parameter.RegisteredParameter(
            'targets', cskeletonmodifier.CSkelModTargets,
            tip = 'Which elements to modify.'),
        parameter.RegisteredParameter(
            'criterion',
            cskeletonmodifier.CSkelModCriterion,
            tip = 'Acceptance criterion'),
        parameter.RegisteredParameter(
            'method',
            RationalizeMethod,
            tip = 'Methods for rationalization.')
        ],
    tip = 'Fix badly shaped elements in a Skeleton.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/rationalize.xml'))


