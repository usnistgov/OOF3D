# -*- python -*-
# $RCSfile: microstructuredisplay.py,v $
# $Revision: 1.26.10.18 $
# $Author: langer $
# $Date: 2014/09/10 21:28:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# DisplayMethod for showing the Materials assigned to a Microstructure.

from ooflib.SWIG.common import coord
from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import voxelfilter
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.SWIG.engine import material
if config.dimension() == 2:
    from ooflib.SWIG.engine import angle2color
    from ooflib.SWIG.engine import orientationimage
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import bitmapdisplay
from ooflib.common.IO import display
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

class MicrostructureMaterialDisplay(bitmapdisplay.BitmapDisplayMethod):
    def __init__(self, no_material, no_color, filter):
        self.no_material = no_material    # color if Material isn't assigned
        self.no_color = no_color    # color if Material has no ColorProperty
        bitmapdisplay.BitmapDisplayMethod.__init__(self, filter)
        self.matChangedSignals = [
            switchboard.requestCallback(
                "materials changed in microstructure", self.matMSChangedCB),
            switchboard.requestCallback(
                "material changed", self.matChangedCB)
            ]

    def destroy(self, destroy_canvaslayer):
        if self.matChangedSignals:
            map(switchboard.removeCallback, self.matChangedSignals)
        bitmapdisplay.BitmapDisplayMethod.destroy(self, destroy_canvaslayer)

    def draw(self, gfxwindow, canvas): # 2D only
        microstructure = self.who().getObject(gfxwindow)
        # The draw_image() routine requires an object with a
        # .fillstringimage() function.  We can't simply give
        # Microstructure such a function, since it can be displayed in
        # many ways, so we construct a temporary object,
        # MaterialImage, just to pass to draw_image().
        matlimage = material.MaterialImage(microstructure, self.no_material,
                                           self.no_color)
        canvas.draw_image(matlimage, coord.Coord(0,0), microstructure.size())

    def layerName(self):
        return "MicrostructureMaterial"

    def whoChanged(self):
        microstructure = self.who().getObject(self.gfxwindow)
        matlimage = material.MaterialImage(microstructure, self.no_material,
                                           self.no_color)
        self.canvaslayer.set_image(matlimage, coord.origin, matlimage.size())
        self.canvaslayer.set_filter(self.filter)
        self.setMicrostructure()
        return False            # don't call setParams

    def setParams(self):
        self.whoChanged()

    def matMSChangedCB(self, microstructure):
        context = self.who()
        if context and microstructure is context.getObject(self.gfxwindow):
            self.whoChanged()
    def matChangedCB(self, materialname):
        context = self.who()
        if context:
            ms = context.getObject(self.gfxwindow)
            if ms:
                mnames = [m.name() for m in material.getMaterials(ms)]
                if materialname in mnames:
                    self.whoChanged()


registeredclass.Registration(
    'Material',
    display.DisplayMethod,
    MicrostructureMaterialDisplay,
    ordering=0,
    layerordering=display.Planar(0.4),
    params=[
        color.ColorParameter(
            'no_material', color.black,
            tip="Color to use if no material has been assigned to a pixel"),
        color.ColorParameter(
            'no_color', color.blue,
            tip="Color to use if the assigned material has no assigned color"),
        parameter.RegisteredParameter(
            "filter",
            voxelfilter.VoxelFilterPtr,
            voxelfilter.AllVoxels(),
            tip="Voxels to include in the display.")
        ],
    whoclasses = ('Microstructure',),
    tip="Display the color of the Material assigned to each pixel.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/microstructuredisplay.xml')
    )

############################

if config.dimension() == 2:
    ## TODO MER: Update for new display layer methods and 3D.

    class OrientationDisplay(MSMaterialDisplay):
        def __init__(self, colorscheme, no_material=color.blue,
                     no_orientation=color.black):
            self.colorscheme = colorscheme
            self.no_orientation = no_orientation
            self.no_material = no_material
            MSMaterialDisplay.__init__(self)
        def draw(self, gfxwindow, canvas):
            msobj = self.who().getObject(gfxwindow)
            img = orientationimage.OrientationImage(msobj,
                                                    self.colorscheme,
                                                    self.no_material,
                                                    self.no_orientation)
            # Don't use OrientationImage.size() here, because
            # orientmapimage may be destroyed before drawing is
            # complete.  msobj.size() refers to an object that will be
            # persistent.
            canvas.draw_image(img, coord.Coord(0,0), msobj.size())

    registeredclass.Registration(
        'Orientation',
        display.DisplayMethod,
        OrientationDisplay,
        ordering=1,
        params=[
            parameter.RegisteredParameter(
                'colorscheme',
                angle2color.Angle2Color,
                tip='Method for converting angles to colors.'),
            color.ColorParameter(
                'no_material', color.blue,
                tip="Color to use for pixels with no assigned Material"),
            color.ColorParameter(
                'no_orientation', color.black,
                tip='Color to use for pixels with no Orientation Property')],
        layerordering=display.Planar(0.6),
        whoclasses = ('Microstructure',),
        tip="Display the Orientation Property of pixels.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/reg/orientationdisplay.xml')
        )
    
