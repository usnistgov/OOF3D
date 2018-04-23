# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# The base classes for Skeleton selection operations are defined here.
# The interesting subclasses that do the actual work are in
# skeletonselectionmethod.py and skeletonselectionmod.py.

from ooflib.SWIG.common import config
from ooflib.common import registeredclass
from ooflib.common import genericselection

# The XXXXSelectionModifier classes describe operations that can be
# performed by the SkeletonSelectionPage, which invokes the
# OOF.XXXXSelection.Select menu item.  The same menu item is used for
# mouse-dependent selection operations performed by the Skeleton
# Selection toolbox.

class SkeletonSelectionModifier(genericselection.GenericSelectionModifier):
    pass

class NodeSelectionModifier(SkeletonSelectionModifier):
    registry = []
    def getSelection(self, skelcontext):
        return skelcontext.nodeselection

class SegmentSelectionModifier(SkeletonSelectionModifier):
    registry = []
    def getSelection(self, skelcontext):
        return skelcontext.segmentselection

class FaceSelectionModifier(SkeletonSelectionModifier):
    registry = []
    def getSelection(self, skelcontext):
        return skelcontext.faceselection

class ElementSelectionModifier(SkeletonSelectionModifier):
    registry = []
    def getSelection(self, skelcontext):
        return skelcontext.elementselection

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonSelectionModRegistration(registeredclass.Registration):
    def callMenuItem(self, skeleton, selectionModifier):
        # Called by the Skeleton Selection page when the "OK" button
        # is pressed.
        self.menuitem.callWithDefaults(skeleton=skeleton,
                                       method=selectionModifier)

class NodeSelectionModRegistration(SkeletonSelectionModRegistration):
    def __init__(self, name, subclass, ordering, params=[],
                 secret=False, **kwargs):
        SkeletonSelectionModRegistration.__init__(
            self, name,
            NodeSelectionModifier, subclass=subclass, params=params,
            ordering=ordering, secret=secret, **kwargs)
        from ooflib.engine.IO import skeletonselectmenu
        self.menuitem = skeletonselectmenu.nodeselectmenu.Select

class SegmentSelectionModRegistration(SkeletonSelectionModRegistration):
    def __init__(self, name, subclass, ordering, params=[],
                 secret=False, **kwargs):
        SkeletonSelectionModRegistration.__init__(
            self, name,
            SegmentSelectionModifier, subclass=subclass, params=params,
            ordering=ordering, secret=secret, **kwargs)
        from ooflib.engine.IO import skeletonselectmenu
        self.menuitem = skeletonselectmenu.segmentselectmenu.Select

class FaceSelectionModRegistration(SkeletonSelectionModRegistration):
    def __init__(self, name, subclass, ordering, params=[],
                 secret=False, **kwargs):
        SkeletonSelectionModRegistration.__init__(
            self, name,
            FaceSelectionModifier, subclass=subclass, params=params,
            ordering=ordering, secret=secret, **kwargs)
        from ooflib.engine.IO import skeletonselectmenu
        self.menuitem = skeletonselectmenu.faceselectmenu.Select

class ElementSelectionModRegistration(SkeletonSelectionModRegistration):
    def __init__(self, name, subclass, ordering, params=[],
                 secret=False, **kwargs):
        SkeletonSelectionModRegistration.__init__(
            self, name,
            ElementSelectionModifier, subclass=subclass, params=params,
            ordering=ordering, secret=secret, **kwargs)
        from ooflib.engine.IO import skeletonselectmenu
        self.menuitem = skeletonselectmenu.elementselectmenu.Select

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Common base class for the different types of skeleton selection
## method registrations.  

class SkeletonSelectionMethodRegistration(registeredclass.Registration):
    # Argh.  We can't have an argument named 'registeredclass' if we
    # also have a module named 'registeredclass'.  The choice of
    # argument name in registeredclass.Registration.__init__ was
    # unfortunate.

    # Some selection methods actually require a mouse click on
    # something other than a Skeleton. They should set whoclasses in
    # the args to their Registration's __init__. Otherwise, it's
    # automatically set to ['Skeleton'] here.

    def __init__(self, name, regclass, subclass,
                 ordering, params=[],
                 whoclasses = ['Skeleton'],
                 secret=0, **kwargs):
        registeredclass.Registration.__init__(
            self,
            name=name,
            registeredclass=regclass,
            subclass=subclass,
            ordering=ordering,
            params=params,
            whoclasses=whoclasses,
            secret=secret,
            **kwargs)
                                            


class NodeSelectionMethod(genericselection.GenericSelectionMethod):
    registry = []
    
class NodeSelectionMethodRegistration(SkeletonSelectionMethodRegistration):
    def __init__(self, name, subclass, ordering, params=[], secret=0, **kwargs):
        SkeletonSelectionMethodRegistration.__init__(
            self,
            name=name,
            regclass=NodeSelectionMethod,
            subclass=subclass,
            ordering=ordering,
            params=params,
            secret=secret,
            **kwargs)
        from ooflib.engine.IO import skeletonselectmenu
        self.menuitem = skeletonselectmenu.nodeselectmenu.Select

        
class SegmentSelectionMethod(genericselection.GenericSelectionMethod):
    registry = []

class SegmentSelectionMethodRegistration(SkeletonSelectionMethodRegistration):
    def __init__(self, name, subclass, ordering, params=[], secret=0, **kwargs):
        SkeletonSelectionMethodRegistration.__init__(
            self,
            name=name,
            regclass=SegmentSelectionMethod,
            subclass=subclass,
            ordering=ordering,
            params=params,
            secret=secret,
            **kwargs)
        from ooflib.engine.IO import skeletonselectmenu
        self.menuitem = skeletonselectmenu.segmentselectmenu.Select


class FaceSelectionMethod(genericselection.GenericSelectionMethod):
    registry = []
    def select(self, skeletoncontext, pointlist, selector):
        pass

class FaceSelectionMethodRegistration(SkeletonSelectionMethodRegistration):
    def __init__(self, name, subclass, ordering, params=[], secret=0,
                 **kwargs):
        SkeletonSelectionMethodRegistration.__init__(
            self,
            name=name,
            regclass=FaceSelectionMethod,
            subclass=subclass,
            ordering=ordering,
            params=params,
            secret=secret,
            **kwargs)
        from ooflib.engine.IO import skeletonselectmenu
        self.menuitem = skeletonselectmenu.faceselectmenu.Select

class ElementSelectionMethod(genericselection.GenericSelectionMethod):
    registry = []
    def select(self, *args, **kwargs):
        pass

class ElementSelectionMethodRegistration(SkeletonSelectionMethodRegistration):
    def __init__(self, name, subclass, ordering, params=[], secret=0, **kwargs):
        SkeletonSelectionMethodRegistration.__init__(
            self,
            name=name,
            regclass=ElementSelectionMethod,
            subclass=subclass,
            ordering=ordering,
            params=params,
            secret=secret,
            **kwargs)
        from ooflib.engine.IO import skeletonselectmenu
        self.menuitem = skeletonselectmenu.elementselectmenu.Select

        
