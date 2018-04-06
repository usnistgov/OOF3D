# -*- python -*-

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
from ooflib.common.IO import parameter
from ooflib.common.IO import pixelselectionmenu
from ooflib.common.IO import whoville
from ooflib.engine import materialmanager
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import materialparameter

ElementSelection = pixelselectioncouriere.ElementSelection
class SelectPixelsInElement(pixelselection.VoxelSelectionModifier):
    def __init__(self, skeleton):
        self.skeleton = skeleton
    def __call__(self, ms, selection):
        skel = skeletoncontext.skeletonContexts[self.skeleton].getObject()
        for el in skel.elements:
            if el.selected:
                selection.select(ElementSelection(ms, el))

## TODO 3.1: 3D Fix this method and uncomment the Registration.
# pixelselection.VoxelSelectionModRegistration(
#     'Select Element Pixels',
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
class SelectPixelsUnderSegment(pixelselection.VoxelSelectionModifier):
    def __init__(self, skeleton):
        self.skeleton = skeleton
    def __call__(self, ms, selection):
        skel = skeletoncontext.skeletonContexts[self.skeleton].getObject()
        for segment in skel.segments.values():
            if segment.selected:
                n0 = segment.nodes()[0].position()
                n1 = segment.nodes()[1].position()
                selection.select(SegmentSelection(ms, n0, n1))

## TODO 3.1: 3D Fix this method and uncomment the Registration.
# pixelselection.VoxelSelectionModRegistration(
#     'Select Segment Pixels',
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

class SelectMaterialPixels(pixelselection.VoxelSelectionModifier):
    def __init__(self, material, operator):
        self.material = material
        self.operator = operator
    def select(self, ms, selection):
        mobj = ms.getObject()
        if self.material == '<Any>':
            courier = pixelselectioncouriere.AnyMaterialSelection(mobj)
        elif self.material == '<None>':
            courier = pixelselectioncouriere.NoMaterialSelection(mobj)
        else:
            courier = pixelselectioncouriere.MaterialSelection(
                mobj, materialmanager.getMaterial(self.material))
        self.operator.operate(selection, courier)

pixelselection.VoxelSelectionModRegistration(
    'Select Material',
    subclass=SelectMaterialPixels,
    ordering=110,
    params=[
        materialparameter.AnyMaterialParameter(
            'material', tip='The name of a material, or \'None\'.'),
        pixelselectionmenu.operatorParam
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
