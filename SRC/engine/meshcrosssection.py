# -*- python -*-
# $RCSfile: meshcrosssection.py,v $
# $Revision: 1.14.18.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:32 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Cross-section objects.  These are the domains of the cross-section
# outputs, and live (indexed by name) inside Mesh objects.  Currently,
# we only have one type, a simple straight-line path between two
# points (defined, obviously, by the two points).  Later, there may be
# others.

from ooflib.common import registeredclass
from ooflib.common import primitives
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

# Anticipating lots of different sorts of these, we make CrossSection
# a registered class.

class MeshCrossSection(registeredclass.RegisteredClass):
    registry = []

MeshCrossSection.tip = "Paths within a Mesh for post-processing."
MeshCrossSection.discussion = xmlmenudump.loadFile(
    "DISCUSSIONS/engine/reg/meshcrosssection.xml")

class StraightCrossSection(MeshCrossSection):
    # start and end should be primitives.Point objects...
    def __init__(self, start, end):
        self.start = start
        self.end = end
        

registeredclass.Registration(
    'Straight', MeshCrossSection, StraightCrossSection, 1,
    params=[primitives.PointParameter('start', tip="Starting point."),
            primitives.PointParameter('end', tip="Ending point.")],
    tip="Cross section defined by two points.",
    discussion="""<para>
    A Cross Section which is a straight line, defined by its endpoints.
    </para>""")
