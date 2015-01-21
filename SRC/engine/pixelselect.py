# -*- python -*-
# $RCSfile: pixelselect.py,v $
# $Revision: 1.21.18.3 $
# $Author: langer $
# $Date: 2014/09/10 21:28:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.engine import pixelselectioncouriere
from ooflib.common import debug
from ooflib.common import pixelselection
from ooflib.common import pixelselectionmod
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.engine import materialmanager
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import materialparameter

ElementSelection = pixelselectioncouriere.ElementSelection
class SelectPixelsInElement(pixelselectionmod.SelectionModifier):
    def __init__(self, skeleton):
        self.skeleton = skeleton
    def __call__(self, ms, selection):
        skel = skeletoncontext.skeletonContexts[self.skeleton].getObject()
        selection.start()
        for el in skel.elements:
            if el.selected:
                selection.select(ElementSelection(ms, el))

## TODO 3.1: 3D Fix this method and uncomment the Registration.
# registeredclass.Registration(
#     'Select Element Pixels',
#     registeredclass=pixelselectionmod.SelectionModifier,
#     subclass=SelectPixelsInElement,
#     ordering=100,
#     params=[whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
#                                   tip=parameter.emptyTipString)
#     ],
#     tip="Select the pixels lying under the selected elements.",
#     discussion="""<para>
#     Select all pixels that intersect the currently selected &skel; elements.
#     </para>""")

SegmentSelection = pixelselectioncouriere.SegmentSelection
class SelectPixelsUnderSegment(pixelselectionmod.SelectionModifier):
    def __init__(self, skeleton):
        self.skeleton = skeleton
    def __call__(self, ms, selection):
        skel = skeletoncontext.skeletonContexts[self.skeleton].getObject()
        selection.start()        
        for segment in skel.segments.values():
            if segment.selected:
                n0 = segment.nodes()[0].position()
                n1 = segment.nodes()[1].position()
                selection.select(SegmentSelection(ms, n0, n1))

## TODO 3.1: 3D Fix this method and uncomment the Registration.
# registeredclass.Registration(
#     'Select Segment Pixels',
#     registeredclass=pixelselectionmod.SelectionModifier,
#     subclass=SelectPixelsUnderSegment,
#     ordering=105,
#     params=[whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
#                                   tip=parameter.emptyTipString)
#             ],
#     tip="Select the pixels lying under the selected skeleton segments",
#     discussion="""<para>
    
#     Select all pixels that intersect the currently selected &skel; segments.

#     </para>""")

#########################

MaterialSelection = pixelselectioncouriere.MaterialSelection
AnyMaterialSelection = pixelselectioncouriere.AnyMaterialSelection
NoMaterialSelection = pixelselectioncouriere.NoMaterialSelection

class SelectMaterialPixels(pixelselectionmod.SelectionModifier):
    def __init__(self, material):
        self.material = material
    def __call__(self, ms, selection):
        selection.start()
        if self.material == '<Any>':
            selection.select(AnyMaterialSelection(ms))
        elif self.material == '<None>':
            courier = NoMaterialSelection(ms)
            selection.select(courier)
        else:
            selection.select(MaterialSelection(
                ms, materialmanager.getMaterial(self.material)))

registeredclass.Registration(
    'Select Material',
    registeredclass=pixelselectionmod.SelectionModifier,
    subclass=SelectMaterialPixels,
    ordering=110,
    params=[materialparameter.AnyMaterialParameter('material',
                                    tip='The name of a material, or \'None\'.'
    )
            ],
    tip="Select pixels to which a given Material has been assigned.",
    discussion="""

    <para> Select all pixels to which the given <varname>material</varname>
    has been assigned.  If <varname>material</varname> is"&lt;None&gt;", only pixels
    without an assigned &material; will be selected.  If
    <varname>material</varname> is "&lt;Any&gt;", pixels with any assigned &material;
    will be selected.
    
    </para>

    """
    )
