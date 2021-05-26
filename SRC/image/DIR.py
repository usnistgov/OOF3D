# -*- python -*- 

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'image'
clib = 'oof3dimage'
clib_order = 2

subdirs = ['IO']

cfiles = ['oofimage3d.C', 'burn.C', 'autogroupMP.C',
          'pixelselectioncourieri.C']

swigfiles = ['oofimage3d.swg', 'burn.swg', 'autogroupMP.swg',
             'pixelselectioncourieri.swg']

swigpyfiles = ['oofimage3d.spy', 'burn.spy']

hfiles = ['oofimage3d.h', 'burn.h', 'autogroupMP.h',
          'pixelselectioncourieri.h']


pyfiles = ['initialize.py', 'pixelselectionmethod.py',
           'pixelselectionmod.py', 'imagemodifier.py']



def set_clib_flags(c_lib):
    addVTKlibs(c_lib, ['vtkImagingColor', 'vtkImagingGeneral'])
        



