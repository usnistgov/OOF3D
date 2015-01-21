# -*- python -*-
# $RCSfile: DIR.py,v $
# $Revision: 1.6.2.2 $
# $Author: langer $
# $Date: 2013/11/08 20:46:06 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'orientationmap'

if not DIM_3:
    clib = 'oof2orientmap'
else:
    clib = 'oof3dorientmap'
clib_order = 10

cfiles = [
    'orientmapdata.C',
    'orientmapproperty.C'
]

swigfiles = [
    'orientmapdata.swg',
    'orientmapproperty.swg'
]

pyfiles = [
    'hkl.py', 'tsl.py', 'initialize.py', 'orientmapdisplay.py',
    'orientmapmenu.py', 'orientmapIO.py']

swigpyfiles = [
    'orientmapdata.spy', 'orientmapproperty.spy']

hfiles = [
    'orientmapdata.h', 'orientmapproperty.h']

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
        c_lib.externalLibs.append('oof3dcommon')


if not NO_GUI:
    subdirs = ['GUI']
