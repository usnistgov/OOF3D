# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'orientationmap'

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
    addOOFlibs(c_lib, 'oof3dcommon')

if not NO_GUI:
    subdirs = ['GUI']
