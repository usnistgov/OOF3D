# -*- python -*- 
# $RCSfile: DIR.py,v $
# $Revision: 1.11.10.5 $
# $Author: langer $
# $Date: 2014/09/19 03:24:06 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'image'
if not DIM_3:
    clib = 'oof2image'
else:
    clib = 'oof3dimage'
clib_order = 2

subdirs = ['IO']

if not DIM_3:
    
    cfiles = ['oofimage.C', 'burn.C', 'evenlyilluminate.C',
              'pixelselectioncourieri.C']
    
    swigfiles = ['oofimage.swg', 'burn.swg', 'pixelselectioncourieri.swg']
    
    swigpyfiles = ['oofimage.spy', 'burn.spy']
    

    hfiles = ['oofimage.h', 'burn.h', 'pixelselectioncourieri.h']

else:
    
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
    import oof2setuputils
    if not DIM_3:
        if oof2setuputils.check_exec('Magick++-config'):
            oof2setuputils.add_third_party_includes('Magick++-config --cppflags',
                                                    c_lib)
            oof2setuputils.add_third_party_libs('Magick++-config --ldflags --libs',
                                                c_lib)
        else:
            print "Can't find Magick++-config!  Your ImageMagick installation may be defective."
            
        c_lib.externalLibs.append('oof2common')

    else:

        c_lib.externalLibs.append('vtkImaging')
        c_lib.externalLibs.append('vtkCommon')
        # c_lib.externalLibs.append('vtkCommonPythonD')
        c_lib.externalLibs.append('vtkIO')
        # c_lib.externalLibs.append('vtkIOPythonD')
        c_lib.externalLibs.append('vtkFiltering')
        c_lib.externalLibs.append('vtkRendering')
        c_lib.externalLibs.append('vtkVolumeRendering')
        c_lib.externalLibs.append('oof3dcommon')




