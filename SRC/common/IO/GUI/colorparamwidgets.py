# -*- python -*-
# $RCSfile: colorparamwidgets.py,v $
# $Revision: 1.30.18.2 $
# $Author: fyc $
# $Date: 2014/07/22 17:56:23 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Color selection widget, customized for rgb, hsv, and gray.
# The colors are a convertible class, meaning that they express
# a single object or value in one of several different representations,
# in this case, HSV, Gray, or RGB.  The different widgets allow the
# user to set the color according to a particular representation.

## TODO OPT: Add widgets for RGBA, etc?  Or just have opacity be a
## separate parameter when it's appropriate.

from ooflib.common import color
from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import labelledslider
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
import gtk
import math

# Collection of labelledsliders, passing through the value-changed
# callback.
class LabelledSliderSet:
    def __init__(self, label=[], min=None, max=None):
        debug.mainthreadTest()
        self.min = min or [0.0]*len(label)
        self.max = max or [1.0]*len(label)

        self.gtk = gtk.Table()
        self.sliders = []

        self.callback = None

        for i in range(len(label)):
            newlabel = gtk.Label(label[i])
            self.gtk.attach(newlabel,0,1,i,i+1)

            newslider = labelledslider.FloatLabelledSlider(
                value=self.min[i], vmin=self.min[i], vmax=self.max[i],
                step=(self.max[i]-self.min[i])/100.0,
                callback=self.slider_callback, name=label[i] )
            
            self.gtk.attach(newslider.gtk, 1,2,i,i+1)
            self.sliders.append(newslider)

    def set_values(self, values):
        debug.mainthreadTest()
        for i in range(len(values)):
            self.sliders[i].set_value(values[i])

    def get_values(self):
        debug.mainthreadTest()
        return map( lambda x: x.get_value(), self.sliders)

    def set_callback(self, func):
        self.callback = func

    # Callback gets called when any of the sliders changes value.
    # Arguments are the slider which changed value, and the new value.
    # Pass them on through.
    def slider_callback(self, slider, value):
        if self.callback:
            self.callback(slider, value)
            

# Wrapper class for the color-difference box, containing a
# gtk.DrawingArea which has two rectangles of different colors.
class Delta:
    def __init__(self,xsize=100,ysize=100):
        debug.mainthreadTest()
        self.gtk = gtk.DrawingArea()
        self.gtk.set_size_request(xsize,ysize)
        self.gtk.connect("configure_event",self.configure)
        self.gtk.connect("expose_event",self.configure)
        self.xsize = xsize
        self.ysize = ysize
        #
        self.fg_color = None
        self.bg_color = None
    def set_background(self,gdkcol):
        debug.mainthreadTest()
        style = self.gtk.get_style().copy()
        style.bg[0]=gdkcol
        self.gtk.set_style(style)
        self.bg_color = gdkcol
    # Draw the rectangle, using the actual size of the window.
    def set_foreground(self,gdkcol):
        debug.mainthreadTest()
        self.fg_color = gdkcol
        if self.gtk.window:
            self.configure(self.gtk,None)
    def configure(self,gtko,event):
        debug.mainthreadTest()
        if self.fg_color:
            drawable = self.gtk.window
            xsize, ysize = drawable.get_geometry()[2:4]
            drawable_gc = drawable.new_gc(foreground=self.fg_color,
                                          background=self.bg_color,
                                          fill=gtk.gdk.SOLID)
            # Should be gtk, not gtko -- want global draw_rectangle routine.
            drawable.draw_rectangle(drawable_gc, True,
                                    xsize/2, 0, (xsize/2)+1, ysize)


# Somewhat pathologically, a "Colorbox" is a "Delta" with a
# different configure routine, which draws the whole box.  This
# means its "set_background" is a bit strange, since the background
# is never visible.  
class ColorBox(Delta):
    def __init__(self, xsize=100, ysize=100):
        Delta.__init__(self, xsize, ysize)
    def configure(self,gtko,event):
        debug.mainthreadTest()
        if self.fg_color:
            drawable = self.gtk.window
            xsize, ysize = drawable.get_geometry()[2:4]
            drawable_gc = drawable.new_gc(foreground=self.fg_color,
                                          background=self.bg_color,
                                          fill=gtk.gdk.SOLID)
            drawable.draw_rectangle(drawable_gc, True, 0, 0, xsize, ysize)




# Params will be a list of floats, in r,g,b order corresponding
# to the registration parameters for RGBColor.
class RGBWidget(parameterwidgets.ParameterWidget):
    def __init__(self,params,old_base,delta_class,scope=None,name=None):
        debug.mainthreadTest()
        parameterwidgets.ParameterWidget.__init__(self, gtk.HBox(), scope, name)
        self.params = params
        # VBox for the color patch.
        self.vbox = gtk.VBox()
        self.delta = delta_class(160,40)
        #
        self.gtk.pack_start(self.vbox, expand=0, fill=0)
        #
        self.slider = LabelledSliderSet(["Red", "Green", "Blue"])
        self.vbox.pack_start(self.slider.gtk, expand=1, fill=1)
        self.vbox.pack_start(self.delta.gtk, expand=0, fill=0)
        #
        if old_base:
            self.gdkcol = self.gtk.get_colormap().alloc_color(
                int(65535*old_base.getRed()),
                int(65535*old_base.getGreen()),
                int(65535*old_base.getBlue()))
        else:
            self.gdkcol = self.gtk.get_colormap().alloc_color(0,0,0)
        #
        self.delta.set_background(self.gdkcol)
        #
        self.set_values() # Copies values from params to the sliders.
        #
        self.slider.set_callback(self.newrgb)
        self.widgetChanged(1, interactive=0)

    def newrgb(self, slider, value):
        debug.mainthreadTest()
        self.values = self.slider.get_values()
        self.gdkcol = self.gtk.get_colormap().alloc_color(
            int(65535*self.values[0]),
            int(65535*self.values[1]),
            int(65535*self.values[2]))
        self.delta.set_foreground(self.gdkcol)
        self.widgetChanged(1, interactive=1)


    # Set the widget from the parameters.
    def set_values(self,values=None):
        debug.mainthreadTest()
        self.values = values or [p.value for p in self.params]
        self.slider.set_values(self.values)
        self.gdkcol = self.gtk.get_colormap().alloc_color(
            int(65535*self.values[0]),
            int(65535*self.values[1]),
            int(65535*self.values[2]))
        self.delta.set_foreground(self.gdkcol)
        self.widgetChanged(1, interactive=0)
        
    def get_values(self):
        for p,v in map(None, self.params, self.values):
            p.value = v

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()

class DiffRGBWidget(RGBWidget):
    def __init__(self,params,old_base,scope=None, name=None):
        RGBWidget.__init__(self, params, old_base, Delta, scope, name)

class NewRGBWidget(RGBWidget):
    def __init__(self, params, old_base, scope=None, name=None):
        RGBWidget.__init__(self, params, old_base, ColorBox, scope, name)
        

regclassfactory.addWidget(color.ColorParameter, color.RGBColor, DiffRGBWidget)
regclassfactory.addWidget(color.NewColorParameter, color.RGBColor, NewRGBWidget)

# The "oldcolor" is currently passed in as an hsv, which means that
# within the widget, rgb2hsv is actually never called by anybody.  Yet.
class HSVWidget(parameterwidgets.ParameterWidget):
    def __init__(self,params,old_base,delta_class,scope=None,name=None):
        debug.mainthreadTest()
        parameterwidgets.ParameterWidget.__init__(self, gtk.HBox(), scope, name)
        self.params = params
        self.vbox = gtk.VBox()
        self.delta = delta_class(160,40)
        #
        self.gtk.pack_start(self.vbox, expand=0, fill=0)
        #
        self.slider = LabelledSliderSet(["Hue","Saturation","Value"],
                                        max=[360.0, 1.0, 1.0])

        self.vbox.pack_start(self.slider.gtk, expand=0, fill=0)
        self.vbox.pack_start(self.delta.gtk, expand=0, fill=0)
        #
        if old_base:
            self.gdkcol = self.gtk.get_colormap().alloc_color(
                int(65535*old_base.getRed()),
                int(65535*old_base.getGreen()),
                int(65535*old_base.getBlue()))
        else:
            self.gdkcol = self.gtk.get_colormap().alloc_color(0,0,0)
        self.delta.set_background(self.gdkcol)
        self.set_values()
        self.slider.set_callback(self.newhsv)
        self.widgetChanged(1, interactive=0)

    def newhsv(self, slider, value):
        debug.mainthreadTest()
        self.values = self.slider.get_values()
        rgb = self.hsv2rgb(self.values)
        self.gdkcol = self.gtk.get_colormap().alloc_color(
            int(65535*rgb[0]),
            int(65535*rgb[1]),
            int(65535*rgb[2]))
        self.delta.set_foreground(self.gdkcol)
        self.widgetChanged(1, interactive=1)

    # Set slider values from the params.
    def set_values(self,values=None):
        debug.mainthreadTest()
        self.values = values or [p.value for p in self.params]
        self.slider.set_values(self.values)
        rgb = self.hsv2rgb(self.values)
        self.gdkcol = self.gtk.get_colormap().alloc_color(
            int(65535*rgb[0]),
            int(65535*rgb[1]),
            int(65535*rgb[2]))
        self.delta.set_foreground(self.gdkcol)
        self.widgetChanged(1, interactive=0)

    def get_values(self):
        for p,v in map(None, self.params, self.values):
            p.value = v

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()


    def hsv2rgb(self,hsv):
        (h,s,v) = hsv
        #
        if s==0.0:
            (r,g,b) = (v,v,v)
        else:
            h_sector = int(math.floor(h/60.0)) # Pick a sector, 0->5.
            h_fraction = (h/60.0)-h_sector
            #
            p = v*(1.0-s)
            q = v*(1.0-s*h_fraction)
            t = v*(1.0-s*(1.0-h_fraction))
            # If h=360.0, we can get artificial wrap-around -- catch it.
            if (h_sector == 0) or (h_sector == 6):
                (r,g,b) = (v,t,p)
            elif h_sector == 1:
                (r,g,b) = (q,v,p)
            elif h_sector == 2:
                (r,g,b) = (p,v,t)
            elif h_sector == 3:
                (r,g,b) = (p,q,v)
            elif h_sector == 4:
                (r,g,b) = (t,p,v)
            else:
                (r,g,b) = (v,p,q)
                
        return (r,g,b)


class DiffHSVWidget(HSVWidget):
    def __init__(self,params,old_base,scope=None,name=None):
        HSVWidget.__init__(self, params, old_base, Delta, scope, name)

class NewHSVWidget(HSVWidget):
    def __init__(self,params,old_base,scope=None,name=None):
        HSVWidget.__init__(self, params, old_base, ColorBox, scope, name)

        
regclassfactory.addWidget(color.ColorParameter, color.HSVColor, DiffHSVWidget)
regclassfactory.addWidget(color.NewColorParameter, color.HSVColor, NewHSVWidget)

# Param will be a single Float parameter, corresponding to the
# registry for GrayColor.
class GrayWidget(parameterwidgets.ParameterWidget):
    def __init__(self,params,old_base,delta_class,scope=None,name=None):
        debug.mainthreadTest()
        parameterwidgets.ParameterWidget.__init__(self, gtk.HBox(), scope, name)
        self.params = params
        self.vbox = gtk.VBox()
        self.delta = delta_class(160,40)
        #
        self.gtk.pack_start(self.vbox, expand=0, fill=0)
        #
        self.slider = LabelledSliderSet(["Gray"], min=[0.0],max=[1.0])
        #
        self.vbox.pack_start(self.slider.gtk, expand=0, fill=0)
        self.vbox.pack_start(self.delta.gtk, expand=0, fill=0)
        #
        if old_base:
            self.gdkcol = self.gtk.get_colormap().alloc_color(
                int(65535*old_base.getRed()),
                int(65535*old_base.getGreen()),
                int(65535*old_base.getBlue()))
        else:
            self.gdkcol = self.gtk.get_colormap().alloc_color(0,0,0)
        self.delta.set_background(self.gdkcol)
        self.set_values()
        self.slider.set_callback(self.newgray)
        self.widgetChanged(1, interactive=0)

    def set_values(self,values=None):
        debug.mainthreadTest()
        self.values = values or [p.value for p in self.params]
        self.slider.set_values(self.values)
        rgb = self.gray2rgb(self.values[0])
        self.gdkcol = self.gtk.get_colormap().alloc_color(int(65535*rgb[0]),
                                                          int(65535*rgb[1]),
                                                          int(65535*rgb[2]))
        self.delta.set_foreground(self.gdkcol)
        self.widgetChanged(1, interactive=0)
        
    def get_values(self):
        self.params[0].value = self.values[0]

    def destroy(self):
        debug.mainthreadTest()
        self.gtk.destroy()
        
    def newgray(self, slider, value):
        debug.mainthreadTest()
        self.values = [value]
        rgb = self.gray2rgb(self.values[0])
        self.gdkcol = self.gtk.get_colormap().alloc_color(int(65535*rgb[0]),
                                                          int(65535*rgb[1]),
                                                          int(65535*rgb[2]))
        self.delta.set_foreground(self.gdkcol)
        self.widgetChanged(1, interactive=1)
        
    def gray2rgb(self, gray):
        return (gray, gray, gray)

class DiffGrayWidget(GrayWidget):
    def __init__(self,params,old_base,scope=None,name=None):
        GrayWidget.__init__(self, params, old_base, Delta, scope, name)

class NewGrayWidget(GrayWidget):
    def __init__(self,params,old_base,scope=None,name=None):
        GrayWidget.__init__(self, params, old_base, ColorBox, scope, name)

regclassfactory.addWidget(color.ColorParameter, color.Gray, DiffGrayWidget)
regclassfactory.addWidget(color.NewColorParameter, color.Gray, NewGrayWidget)
