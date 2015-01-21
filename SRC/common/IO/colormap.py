# -*- python -*-
# $RCSfile: colormap.py,v $
# $Revision: 1.26.10.5 $
# $Author: langer $
# $Date: 2014/11/24 21:44:49 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Colormaps map numbers in the range [0,1] to colors

from ooflib.SWIG.common import config
from ooflib.common import color
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from types import *
import math

if config.dimension() == 3:
    from ooflib.SWIG.common import vtkColorLUT

FloatParameter = parameter.FloatParameter
FloatRangeParameter = parameter.FloatRangeParameter

class ColorMap(registeredclass.RegisteredClass):
    registry = []
    tip = "Color maps used in contour displays."
    discussion = """<para>
    <classname>ColorMap</classname> objects are used when generating
    contour displays.  They specify a way of converting numbers into
    colors.
    </para>"""

    def getVtkLookupTable(self, numcolors):
        lut = vtkColorLUT.New()
        vtkColorLUT.SetNumberOfColors(lut, numcolors)
        delta = 1./(numcolors - 1)
        for i in xrange(numcolors):
            color = self.__call__(i*delta)
            vtkColorLUT.SetTableValue(
                lut, i, color.getRed(), color.getGreen(), color.getBlue(), 1)
        return lut
        

class ColorMapRegistration(registeredclass.Registration):
    def __init__(self, name, subclass, ordering, params=[], tip=None,
                 discussion=None):
        registeredclass.Registration.__init__(self, name, ColorMap, subclass,
                                              ordering, params=params, tip=tip,
                                              discussion=discussion)
##########################


class GrayMap(ColorMap):
    def __call__(self, x):
        return color.Gray(x)

ColorMapRegistration(
    'Gray',
    GrayMap,
    0,
    tip="Linear gray scale.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/graymap.xml')
    )

class ThermalMap(ColorMap):
    "black->red->yellow->white"
    def __call__(self, x):
        if x < 0.33:
            return color.RGBColor(x/0.33, 0, 0)
        if x < 0.67:
            return color.RGBColor(1, (x-0.33)/0.34, 0)
        return color.RGBColor(1, 1, (x-0.67)/0.33)

ColorMapRegistration(
    'Thermal',
    ThermalMap,
    1,
    tip="Black to red to yellow to white.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/thermalmap.xml'))

class GammaGrayMap(ColorMap):
    def __init__(self, gamma):
        self.gamma = gamma
        self.invgamma = 1.0/gamma
    def __call__(self, x):
        return color.Gray(math.pow(x, self.invgamma))

ColorMapRegistration(
    'GammaGray',
    GammaGrayMap,
    0.1,
    [FloatParameter('gamma', 1.0, tip="gamma correction")],
    tip="gray = x^(1/gamma)",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/gammagray.xml')
    )

class HSVMap(ColorMap):
    def __init__(self, saturation=1.0, value=1.0, phase_shift=0.0):
        self.saturation = saturation
        self.value = value
        self.phase_shift = phase_shift
    def __call__(self, x):
        return color.HSVColor(hue=x*360+self.phase_shift,
                               saturation=self.saturation,
                               value=self.value)

ColorMapRegistration(
    'HSV',
    HSVMap,
    2,
    [FloatRangeParameter('saturation', (0., 1., .01), 1.0,
                         tip='0.0=weak, 1.0=strong'),
     FloatRangeParameter('value', (0., 1., .01), 1.0,
                         tip='0.0=dark, 1.0=light'),
     FloatRangeParameter('phase_shift', (0., 360., 1.), 0.0,
                         tip='initial hue, in degrees')],
    tip="Varying hue, at fixed saturation and value.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/hsvmap.xml'))

# The ROYGBIV map -- although, since it starts from blue, it's really
# the VIBGYOR map.
class SpectralMap(ColorMap):
    def __init__(self, saturation=1.0, value=1.0):
        self.saturation = saturation
        self.value = value
    def __call__(self,x):
        return color.HSVColor(hue=(1.0-x)*240,
                               saturation=self.saturation,
                               value=self.value)

ColorMapRegistration(
    'Spectral',
    SpectralMap,
    2.5,
    [FloatRangeParameter('saturation', (0, 1., .01), 1.0,
                         tip='0.0=weak, 1.0=strong'),
     FloatRangeParameter('value', (0, 1., .01), 1.0,
                         tip='0.0=dark, 1.0=light')],
    tip="blue, green, yellow, orange, red",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/spectralmap.xml'))


class TequilaSunrise(ColorMap):
    def __call__(self,x):
        return color.RGBColor(1.0, 0.86667*math.sqrt(x), 0.0)

ColorMapRegistration(
    'TequilaSunrise',
    TequilaSunrise,
    3.,
    tip="It's another Tequila sunrise/Stirrin' slowly 'cross the sky...",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/tequilamap.xml'))


# For parameters containing these, use the appropriate RegisteredParameter.
