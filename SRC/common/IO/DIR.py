# -*- python -*- 

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'IO'
clib = 'oof3dcommon'
if not NO_GUI:
    subdirs = ['GUI']

cfiles = [
    'bitoverlay.C',
    'ghostoofcanvas.C',
    'vtkutils.C', 'view.C', 'canvaslayers.C', 'oofcerr.C',
    'oofImageToGrid.C', 'oofOverlayVoxels.C', 'oofExcludeVoxels.C',
    'gridsourcebase.C', 'gridlayers.C', 'oofCellLocator.C',
    'imageformat.C'
]

swigfiles = [
    #'bitoverlay.swg',
    'ghostoofcanvas.swg', 'vtkutils.swg', 
    'view.swg', 'canvaslayers.swg', 'gridsourcebase.swg', 
    'gridlayers.swg', 'imageformat.swg']

pyfiles = [
    'activityviewermenu.py', 'automatic.py', 'automaticdoc.py',
    'binarydata.py', 'bitmapdisplay.py',
    #'bitoverlaydisplay.py',
    'clipplaneclickanddragdisplay.py', 'colordiffparameter.py',
    'colormap.py', 'datafile.py', 'display.py', 'genericselecttoolbox.py',
    'gfxmanager.py', 'ghostgfxwindow.py', 'mainmenu.py', 'menudump.py',
    'menuparser.py', 'microstructureIO.py', 'microstructuredisplay.py',
    'microstructuremenu.py', 'oofmenu.py', 'output.py', 'parameter.py',
    'pixelgroupmenu.py', 'pixelgroupparam.py', 'pixelinfo.py',
    'pixelinfodisplay.py', 'placeholder.py', 'pointparameter.py',
    'pointparameter.py', 'progressbar_delay.py', 'questioner.py',
    'reporter.py', 'reporterIO.py', 'reportermenu.py', 'scriptloader.py',
    'socket2me.py', 'topwho.py', 'typename.py', 'viewertoolbox.py',
    'voxelregionselectiondisplay.py', 'whoville.py', 'words.py',
    'xmlmenudump.py'
]

swigpyfiles = [#'bitoverlay.spy',
    'view.spy', 'imageformat.spy']

hfiles = [
    'bitoverlay.h',
    'vtkutils.h', 'view.h',
    'canvaslayers.h', 'oofcerr.h', 'gridsourcebase.h', 'gridlayers.h',
    'oofImageToGrid.h', 'oofOverlayVoxels.h', 'oofExcludeVoxels.h',
    'oofCellLocator.h', 'imageformat.h']
    
if HAVE_MPI:
    pyfiles.extend(['parallelmainmenu.py', 'microstructureIPC.py',
                    'pixelgroupIPC.py'])
