# -*- python -*-
# $RCSfile: director.py,v $
# $Revision: 1.14.12.8 $
# $Author: langer $
# $Date: 2014/07/31 15:09:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# The "Director" enum and related classes.  Used by the boundary
# constructor, but in common because it just might be useful elsewhere
# also.

from ooflib.SWIG.common import config
from ooflib.common import enum
from ooflib.common import utils

## TODO 3.1: Use a RegisteredClass instead of an Enum, and then make
## the axis part of the 3D loop directions an argument.  This would
## simplify the user interface for 3D loop directions.  As an enum,
## it's too easy to select the wrong axis because the strings all look
## alike.

# Toplogy hints, used by the DirectorWidget.
unclosedDirections = ['Left to right', 'Right to left',
                      'Top to bottom', 'Bottom to top']
if config.dimension() == 2:
    closedLoopDirections = ['Clockwise', 'Counterclockwise']
    closedSurfaceDirections = []
else:                           # 3D
    unclosedDirections = [
        '-X to +X', '+X to -X',
        '-Y to +Y', '+Y to -Y',
        '-Z to +Z', '+Z to -Z'
    ]
    closedLoopDirections = [
        'Clockwise-x', 'Clockwise-y', 'Clockwise-z',
        'Counterclockwise-x', 'Counterclockwise-y', 'Counterclockwise-z']
    closedSurfaceDirections = ['Outward', 'Inward']

_directions = (closedLoopDirections + unclosedDirections +
               closedSurfaceDirections)

#Interface branch
#_directions.append('Non-sequencable')

class Director(enum.EnumClass(*(unclosedDirections + closedLoopDirections))):
    tip = "Directions for arranging objects."
    discussion = """<para>
    <classname>Director</classname> objects are used to specify the
    direction of things like &skel; <link
    linkend='Section:Concepts:Skeleton:Boundary:Edge'>edge
    boundaries</link>.
    </para>"""

utils.OOFdefine('Director', Director)

# Trivial subclass allows directors to have a custom widget.
class DirectorParameter(enum.EnumParameter):
    def __init__(self, name, value=None, default=None, tip=None):
        enum.EnumParameter.__init__(self, name, Director, value, default, tip)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

#Interface branch
#Widget is in boundarybuilderGUI.py.
class DirectorInterfacesParameter(enum.EnumParameter):
    def __init__(self, name, value=None, default=None, tip=None):
        enum.EnumParameter.__init__(self, name, Director, value, default, tip)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## TODO 3.1: These directions aren't sufficient for orienting a
## surface.  A strip of faces that form a closed loop (but not a
## closed surface) can have a zero normal.  That's not a likely
## surface on which people will want to impose boundary conditions,
## though.

class SurfaceDirector(enum.EnumClass(*(unclosedDirections +
                                       closedSurfaceDirections))):
    tip="Directions for arranging surfaces."

utils.OOFdefine('SurfaceDirector', SurfaceDirector)

class SurfaceDirectorParameter(enum.EnumParameter):
    def __init__(self, name, value=None, default=None, tip=None):
        enum.EnumParameter.__init__(self, name, SurfaceDirector,
                                    value, default, tip)
