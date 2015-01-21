# -*- python -*-
# $RCSfile: color.py,v $
# $Revision: 1.37.10.8 $
# $Author: langer $
# $Date: 2014/07/30 21:28:35 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import math, types
from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

FloatParameter = parameter.FloatParameter
FloatRangeParameter = parameter.FloatRangeParameter

# Color is a convertible registered class.  The same color can be
# parametrized as either rgb or hsv, or gray.

class Color(registeredclass.ConvertibleRegisteredClass):
    registry = []
    # Generic comparator for colors.  Subclasses must provide
    # getRed(), getGreen() and getBlue() functions, which they need
    # for other reasons anyways.
    def __cmp__(self,other):
        try:
            if self.getRed() < other.getRed(): return -1
            if self.getRed() > other.getRed(): return 1
            if self.getGreen() < other.getGreen(): return -1
            if self.getGreen() > other.getGreen(): return 1
            if self.getBlue() < other.getBlue(): return -1
            if self.getBlue() > other.getBlue(): return 1
            if self.getAlpha() < other.getAlpha(): return -1
            if self.getAlpha() > other.getAlpha(): return 1
        except AttributeError:
            return 1
        return 0
    # Also need to over-ride RegisteredClass's __eq__ and __ne__ functions.
    def __eq__(self,other):
        return self.__cmp__(other)==0
    def __ne__(self,other):
        return self.__cmp__(other)!=0
    
    def rgb(self):
        return (self.getRed(), self.getGreen(), self.getBlue())

    tip = "Various ways of describing a color."
    discussion = """<para>
    The <classname>Color</classname> contains various ways of
    describing colors.  The different representations are provided for
    convenience.  The behavior of the program never depends on the
    format in which a color was specified.
    </para>"""


# TODO 3.1: Separate registries for Colors and Translucent colors...

    def rgba(self):
        return (self.getRed(), self.getGreen(), self.getBlue(), self.getAlpha())
        
# Structured type to hold the base values for color parameters, and
# which can be type-checked.  Also contains the comparator for colors.
# (TODO 3.1: Is there any reason not to just use RGBAColor as the base
# representation?)
class ColorValueBase:
    def __init__(self,red,green,blue,alpha=1):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
    def getRed(self):
        return self.red
    def getGreen(self):
        return self.green
    def getBlue(self):
        return self.blue
    def getAlpha(self):
        return self.alpha
    # Comparator, same semantics as instance comparator, but usable
    # if you don't yet have an instance.  (Does this ever happen?)
    def __cmp__(self,other):
        try:
            if self.red < other.red: return -1
            if self.red > other.red: return 1
            if self.green < other.green: return -1
            if self.green > other.green: return 1
            if self.blue < other.blue: return -1
            if self.blue > other.blue: return 1
            if self.alpha < other.alpha: return -1
            if self.alpha > other.alpha: return 1
        except AttributeError:
            return 1                    # 'other' is (probably) not a CVB.
        return 0
    def __repr__(self):
        return "ColorValueBase(red=%.5f, green=%.5f, blue=%.5f, alpha=%.5f)" % \
               (self.red, self.green, self.blue, self.alpha)
    
# Registration assigns the conversion routines, which make
# Color into a nontrivial convertible class.  "to_base" and
# "from_base" arguments are required at this level, in general.
# For the particular case of Color, however, all of the instances
# can answer "base" queries (r, g, or b) more efficiently at
# the instance level, so "to_base" functions are not provided.
class ColorRegistration(registeredclass.ConvertibleRegistration):
    def __init__(self, name, subclass, ordering,
                 from_base, params=[], tip=None, discussion=None, secret=0):
        registeredclass.ConvertibleRegistration.__init__(
            self, name, Color, subclass, ordering, from_base=from_base,
            params=params, tip=tip, discussion=discussion, secret=secret)

    # ConvertibleRegistration.to_base is only called by
    # ConvertibleRegistration.getParamValuesAsBase and by
    # ConvertibleRegisteredClass.__eq__, so by redefining
    # getParamValuesAsBase and Color.__eq__, we don't need to provide
    # any to_base functions.
    def getParamValuesAsBase(self):
        temp = self()
        return ColorValueBase(temp.getRed(), temp.getGreen(), temp.getBlue())



class RGBColor(Color):
    """
    Initialize with key word arguments or rgb values:
      RGBColor(red, green, blue)
      RGBColor(red=x, green=y, blue=z)
    """
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = 1
    def getRed(self):
        return self.red
    def getGreen(self):
        return self.green
    def getBlue(self):
        return self.blue
    def getAlpha(self):
        return 1

    # RGBColor needs some extra functions because it is used as a
    # dictionary key when categorizing pixels (see
    # image.IO.imagemenu.createPixelGroups).  The generic versions of
    # these functions are too slow.  Only RGBColor needs these
    # functions, because colors stored in images are returned to
    # Python as RGBColors.
    def __hash__(self):
        return hash(self.red) ^ hash(self.green) ^ hash(self.blue)
    def __eq__(self, other):
        try:
            if self.red < other.red or self.red > other.red or \
                   self.green < other.green or self.green > other.green or \
                   self.blue < other.blue or self.blue > other.blue or \
                   self.alpha < other.alpha or self.alpha > other.alpha:
                return 0
        except AttributeError:
            return Color.__eq__(self, other)
        return 1
    def __ne__(self, other):
        return 1 - self.__eq__(other)
    def __cmp__(self, other):
        try:
            if self.red < other.red: return -1
            if self.red > other.red: return 1
            if self.green < other.green: return -1
            if self.green > other.green: return 1
            if self.blue < other.blue: return -1
            if self.blue > other.blue: return 1
            if self.alpha < other.alpha: return -1
            if self.alpha > other.alpha: return 1
        except AttributeError:
            return Color.__cmp__(self, other)
        return 0

    # RGBColor overrides the default repr defined in RegisteredClass,
    # because the default one writes too many digits. The repr is used
    # when creating names for automatically generated pixel groups
    # (see image.IO.imagemenu.createPixelGroups).  The extra digits
    # are distracting, and can lead to architecture-dependent names,
    # which confuses testing scripts.
    def __repr__(self):
        return "RGBColor(red=%.5f,green=%.5f,blue=%.5f)" % (self.red,
                                                            self.green,
                                                            self.blue)


# RGB conversion functions are nearly trivial.
def _rgb_from_base(rgb, base):
    if isinstance(base,ColorValueBase):
        return [base.red, base.green, base.blue]

def rgb_from_hex(hexstr):
    assert hexstr[0] == '#'
    return RGBColor(eval('0x'+hexstr[1:3])/255.,
                    eval('0x'+hexstr[3:5])/255.,
                    eval('0x'+hexstr[5:7])/255.)


ColorRegistration(
    'RGBColor',
    RGBColor,
    1,
    params=[FloatRangeParameter('red', (0., 1., 0.01), 0.0,
                                tip="Value of Red."),
            FloatRangeParameter('green', (0., 1., 0.01), 0.0,
                                tip="Value of Green."),
            FloatRangeParameter('blue', (0., 1., 0.01), 0.0,
                                tip="Value of Blue.")],
    from_base=_rgb_from_base,
    tip="Color specified as a Red, Green, Blue triplet.",
    discussion=xmlmenudump.loadFile("DISCUSSIONS/common/reg/rgbcolor.xml")
    )

# class RGBAColor(RGBColor):
#     """
#     Initialize with key word arguments or rgba values:
#       RGBAColor(red, green, blue, alpha)
#       RGBAColor(red=x, green=y, blue=z, alpha=a)
#     """
#     def __init__(self, red, green, blue, alpha):
#         self.red = red
#         self.green = green
#         self.blue = blue
#         self.alpha = alpha
#     def getAlpha(self):
#         return self.alpha
#     def __hash__(self):
#         return hash(self.red) ^ hash(self.green) ^ hash(self.blue) ^ hash(self.alpha)
#     # RGBAColor needs an explicit repr because it's derived from
#     # RGBColor, which overrides the generic RegisteredClass repr.
#     def __repr__(self):
#         return "RGBAColor(red=%.5f,green=%.5f,blue=%.5f,alpha=%.5f)" % (
#             self.red, self.green, self.blue, self.alpha)


# def _rgba_from_base(rgba, base):
#     if isinstance(base,ColorValueBase):
#         return [base.red, base.green, base.blue, base.alpha]


# ColorRegistration(
#     'RGBAColor',
#     RGBAColor,
#     4,
#     params=[FloatRangeParameter('red', (0., 1., 0.01), 0.0,
#                                 tip="Value of Red."),
#             FloatRangeParameter('green', (0., 1., 0.01), 0.0,
#                                 tip="Value of Green."),
#             FloatRangeParameter('blue', (0., 1., 0.01), 0.0,
#                                 tip="Value of Blue."),
#             FloatRangeParameter('alpha', (0., 1., 0.01), 1.0,
#                                 tip="Opacity.")],
#     from_base=_rgba_from_base,
#     tip="Color specified as a Red, Green, Blue, Alpha quartet.",
#     discussion=xmlmenudump.loadFile("DISCUSSIONS/common/reg/rgbcolor.xml")
#     )

    
class Gray(Color):
    def __init__(self, value):
        self.value = value
        self.alpha = 1
    def getRed(self):
        return self.value
    def getGreen(self):
        return self.value
    def getBlue(self):
        return self.value
    def getAlpha(self):
        return self.alpha

# Gray conversion functions.
def _gray_from_base(gray, base):
    if isinstance(base,ColorValueBase):
        g = (base.red+base.green+base.blue)/3.0
        return [g]
        

ColorRegistration(
    'Gray',
    Gray, 3,
    params=[FloatRangeParameter('value', (0., 1., 0.01), 0.0,
                                tip="Gray value (0==black, 1==white).")],
    from_base=_gray_from_base,
    tip="A gray color.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/graycolor.xml')
    )

# class TranslucentGray(Gray):
#     def __init__(self, value, alpha):
#         self.value = value
#         self.alpha = alpha

# # Gray conversion functions.
# def _tgray_from_base(gray, base):
#     if isinstance(base,ColorValueBase):
#         g = (base.red+base.green+base.blue)/3.0
#         return [g,base.alpha]
 
# ColorRegistration(
#     'TranslucentGray',
#     TranslucentGray, 6,
#     params=[FloatRangeParameter('value', (0., 1., 0.01), 0.0,
#                                 tip="Gray value (0==black, 1==white)."),
#             FloatRangeParameter('alpha', (0., 1., 0.01), 0.0,
#                                 tip="Opacity.")],
#     from_base=_tgray_from_base,
#     tip="A gray color with an opacity component.",
#     discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/graycolor.xml')
#     )
        

class HSVColor(Color):
    def __init__(self, hue, saturation, value):
        if hue >= 360 or hue < 0:
            hue = hue % 360
        self.hue = hue
        self.saturation = saturation
        self.value = value
        self._rgb = None                # cache conversion to rgb
        self.alpha = 1

    def findrgb(self):
        ## HSV to RGB algorithm stolen from
        ## http://www.cs.rit.edu/~ncs/color/t_convert.html
        if self._rgb:
            return
        if self.saturation == 0.0: # gray
            self._rgb = (self.value, self.value, self.value)
        else:
            h = self.hue/60.
            i = int(math.floor(h))    # sextant of the color wheel
            f = h - i                 # fractional part of h
            p = self.value * (1 - self.saturation)
            q = self.value * (1 - self.saturation*f)
            t = self.value * (1 - self.saturation*(1-f))
            if (i == 0) or (i == 6):  # For h=360.0, can get i=6.
                self._rgb = (self.value, t, p)
            elif i == 1:
                self._rgb = (q, self.value, p)
            elif i == 2:
                self._rgb = (p, self.value, t)
            elif i == 3:
                self._rgb = (p, q, self.value)
            elif i == 4:
                self._rgb = (t, p, self.value)
            elif i == 5:
                self._rgb = (self.value, p, q)

    def getRed(self):
        self.findrgb()
        return self._rgb[0]
    def getGreen(self):
        self.findrgb()
        return self._rgb[1]
    def getBlue(self):
        self.findrgb()
        return self._rgb[2]
    def getAlpha(self):
        return 1



# HSV conversion functions are nontrivial.
def hsv_from_rgb(r, g, b):
     maxval = max((r,g,b))
     minval = min((r,g,b))
     #
     v = maxval
     #
     delta = maxval-minval
     #
     if maxval==0.0:
         (h,s,v) = (0.0, 0.0, 0.0) # If s=0, h and v don't matter.
     elif delta==0.0:  # It's gray, r=g=b.
         (h,s,v) = (0.0, 0.0, maxval)
     else:
         s = delta/maxval
         #
         if r==maxval:
             h = (g-b)/delta
         elif g==maxval:
             h = 2.0+(b-r)/delta
         else:
             h = 4.0+(r-g)/delta
         h *= 60.0
         if h<0:
             h+=360.0
     return (h, s, v)

def _hsv_from_base(hsv, base):
    if isinstance(base, ColorValueBase):
        (h, s, v) = hsv_from_rgb(base.red, base.green, base.blue)
        return [h,s,v]
    
ColorRegistration(
    'HSVColor',
    HSVColor, 2,
    params=[FloatRangeParameter('hue', (0.0, 360.0, 1.), 0.0,
                                tip="Value of Hue."),
            FloatRangeParameter('saturation', (0., 1., .01), 0.0,
                                tip="Value of Saturation."),
            FloatRangeParameter('value', (0., 1., .01),  0.0,
                                tip="Value of ... hmmm ... Value.")],
    from_base=_hsv_from_base,
    tip="Color specified by Hue, Saturation, and Value.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/hsvcolor.xml'))

# class HSVAColor(HSVColor):
#     def __init__(self, hue, saturation, value, alpha):
#         HSVColor.__init__(self, hue, saturation, value)
#         self.alpha = alpha

#     def getAlpha(self):
#         return self.alpha

# def _hsva_from_base(hsv, base):
#     if isinstance(base, ColorValueBase):
#         (h, s, v) = hsv_from_rgb(base.red, base.green, base.blue)
#         return [h,s,v, base.alpha]

# ColorRegistration(
#     'HSVAColor',
#     HSVAColor, 5,
#     params=[FloatRangeParameter('hue', (0.0, 360.0, 1.), 0.0,
#                                 tip="Value of Hue."),
#             FloatRangeParameter('saturation', (0., 1., .01), 0.0,
#                                 tip="Value of Saturation."),
#             FloatRangeParameter('value', (0., 1., .01),  0.0,
#                                 tip="Value of ... hmmm ... Value."),
#             FloatRangeParameter('alpha', (0., 1., 0.01), 0.0,
#                                 tip="Opacity.")],
#     from_base=_hsva_from_base,
#     tip="Color specified by Hue, Saturation, Value, and Alpha.",
#     discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/hsvcolor.xml'))


#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#

# ColorParameter and NewColorParameter differ only in the widgets that
# are assigned to them in graphics mode.  The ColorParameter widget
# displays both the selected color and the old value.
# NewColorParameter only displays the selected color.

class ColorParameter(parameter.ConvertibleRegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.ConvertibleRegisteredParameter.__init__(
            self, name, Color, value, default, tip, auxData)
    def clone(self):
        return self.__class__(self.name, self.value, self.default, self.tip)

class NewColorParameter(ColorParameter): pass

#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#

def alpha(opacity):
    if opacity == 1.0:
        return 255
    return int(opacity*256)

#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#=-=#

## Standard colors

black =   Gray(0.0)
white =   Gray(1.0)
red =     RGBColor(1.0, 0.0, 0.0)
green =   RGBColor(0.0, 1.0, 0.0)
blue =    RGBColor(0.0, 0.0, 1.0)
cyan =    RGBColor(0.0, 1.0, 1.0)
yellow =  RGBColor(1.0, 1.0, 0.0)
orange =  RGBColor(1.0, 0.5, 0.0)
magenta = RGBColor(1.0, 0.0, 1.0)
gray50 =  Gray(0.5)

from ooflib.common import utils
utils.OOFdefine('black', black)
utils.OOFdefine('white', white)
utils.OOFdefine('red', red)
utils.OOFdefine('green', green)
utils.OOFdefine('blue', blue)
utils.OOFdefine('cyan', cyan)
utils.OOFdefine('yellow', yellow)
utils.OOFdefine('orange', orange)
utils.OOFdefine('magenta', magenta)
utils.OOFdefine('gray50', gray50)
