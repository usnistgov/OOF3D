# -*- python -*-
# $RCSfile: skeletongroupparams.py,v $
# $Revision: 1.20.18.4 $
# $Author: langer $
# $Date: 2013/11/08 20:45:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Special parameter types for skeleton groups and boundaries.  They're
# basically strings, but the special parameter type means it can have
# a special widget in the GUI.

from ooflib.SWIG.common import config
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
import types


class NodeGroupParameter(parameter.StringParameter):
    def valueDesc(self):
        return """The name of a <link
        linkend='Section-Concepts-Skeleton-Groups'>group</link> of
        &skel; <link
        linkend='Section-Concepts-Skeleton-Node'>nodes</link>."""

class SegmentGroupParameter(parameter.StringParameter):
    def valueDesc(self):
        return """The name of a <link
        linkend='Section-Concepts-Skeleton-Groups'>group</link> of
        &skel; <link
        linkend='Section-Concepts-Skeleton-Segment'>segments</link>."""

class ElementGroupParameter(parameter.StringParameter):
    def valueDesc(self):
        return """The name of a <link
        linkend='Section-Concepts-Skeleton-Groups'>group</link> of
        &skel; <link
        linkend='Section-Concepts-Skeleton-Element'>elements</link>."""

class SkeletonBoundaryParameter(parameter.StringParameter):
    def valueDesc(self):
        return "The name of a boundary of the &skel;."

class SkeletonFaceBoundaryParameter(parameter.StringParameter):
    def valueDesc(self):
        return "The name of a face boundary of the &skel;."

class SkeletonEdgeBoundaryParameter(parameter.StringParameter):
    def valueDesc(self):
        return "The name of an edge boundary of the &skel;."
    
class SkeletonPointBoundaryParameter(parameter.StringParameter):
    def valueDesc(self):
        return "The name of a point boundary of the &skel;."


# Another parameter type for specifying "aggregates", which can
# include not only groups, but also the selection.  Subclassing is
# again for the purpose of having special widgets.

class SkelGroupSelParameter(placeholder.PlaceHolderParameter):
    types = (types.StringType, placeholder.selection)

class NodeAggregateParameter(SkelGroupSelParameter):
    def valueDesc(self):
        return """ The name of a <link
        linkend='Section-Concepts-Skeleton-Node'>node</link> <link
        linkend='Section-Concepts-Skeleton-Groups'>group</link>, or
        the <link linkend='Object-Placeholder'>placeholder</link>
        <userinput>selection</userinput>, referring to the currently
        selected nodes."""
        
class SegmentAggregateParameter(SkelGroupSelParameter):
    def valueDesc(self):
        return """The name of a <link
        linkend='Section-Concepts-Skeleton-Segment'>segment</link>
        <link linkend='Section-Concepts-Skeleton-Groups'>group</link>,
        or the <link linkend='Object-Placeholder'>placeholder</link>
        <userinput>selection</userinput>,
        referring to the currently selected segments."""

class ElementAggregateParameter(SkelGroupSelParameter):
    def valueDesc(self):
        return """The name of a <link
        linkend='Section-Concepts-Skeleton-Element'>element</link>
        <link linkend='Section-Concepts-Skeleton-Groups'>group</link>,
        or the <link linkend='Object-Placeholder'>placeholder</link>
        <userinput>selection</userinput>,
        referring to the currently selected elements."""

if config.dimension() == 3:
    class FaceGroupParameter(parameter.StringParameter):
        def valueDesc(self):
            return """The name of a <link
            linkend='Section-Concepts-Skeleton-Groups'>group</link> of
            &skel; <link
            linkend='Section-Concepts-Skeleton-Face'>faces</link>."""

    class FaceAggregateParameter(SkelGroupSelParameter):
        def valueDesc(self):
            return """The name of a <link
            linkend='Section-Concepts-Skeleton-Face'>face</link>
            <link linkend='Section-Concepts-Skeleton-Groups'>group</link>,
            or the <link linkend='Object-Placeholder'>placeholder</link>
            <userinput>selection</userinput>,
            referring to the currently selected faces."""
