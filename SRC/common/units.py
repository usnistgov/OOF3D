# -*- python -*-
# $RCSfile: units.py,v $
# $Revision: 1.5.10.3 $
# $Author: langer $
# $Date: 2014/09/17 21:13:28 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import enum
from ooflib.common import registeredclass

## TODO 3.1: This file defines both an old Enum and a new
## RegisteredClass.  I started to switch to the RegisteredClass
## because adding units to RegionSelector was much easier if the units
## object could do some of the work.  However, the Enum is used in a
## lot of places that I don't want to update right now (eg, it's used
## for a parameter to RefinementCriterion subclasses, which use an
## enum2string typemap).  So I've changed the RegisteredClass name to
## UnitsRC and I'm not deleting the Enum.  This should be fixed later.

if config.dimension() == 2:
    pixel = "pixel"
    Pixel = "Pixel"
if config.dimension() == 3:
    pixel = "voxel"
    Pixel = "Voxel"


class Units(enum.EnumClass(
    (Pixel, 'Lengths are relative to the '+pixel+' size'),
    ("Physical", 'Lengths are given in physical units'),
    ("Fractional", 'Lengths are fractions of the dimensions of the microstructure')
    )):
    tip="Specify units for inputs"
    discussion="""<para>

    This type is used to specify whether a length is being given in
    <link linkend="Section:Concepts:Microstructure:Coordinates">physical</link>
    units, or as a multiple of the """+pixel+""" size in the relevant &micro;,
    or as a fraction of the microstructure dimensions.

    </para>"""


class UnitsRC(registeredclass.RegisteredClass):
    registry = []


class PixelUnits(UnitsRC):
    def scale(self, ms, obj):
        return obj.scaled(ms.sizeOfPixels())

class FractionalUnits(UnitsRC):
    def scale(self, ms, obj):
        return obj.scaled(ms.size())

class PhysicalUnits(UnitsRC):
    def scale(self, ms, obj):
        return obj
    
registeredclass.Registration(
    Pixel,
    UnitsRC,
    PixelUnits,
    ordering=0,
    tip='Lengths are relative to the '+pixel+'size.')

registeredclass.Registration(
    "Physical",
    UnitsRC,
    PhysicalUnits,
    ordering=1,
    tip='Lengths are given in physical units.')

registeredclass.Registration(
    "Fractional",
    UnitsRC,
    FractionalUnits,
    ordering=1,
    tip='Lengths are fractions of the dimensions of the microstructure.')

