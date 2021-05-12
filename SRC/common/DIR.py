# -*- python -*- 


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'common'
subdirs = ['IO', 'EXTRA', 'VSB']
clib = 'oof3dcommon'
clib_order = 0

cfiles = [
    'activearea.C', 'argv.C', 'boolarray.C', 'cdebug.C', 'ccolor.C',
    'cmicrostructure.C', 'colordifference.C', 'coord.C', 'despeckle.C',
    'cpixelselection.C', 'identification.C', 'imagebase.C', 'lock.C',
    'ooferror.C', 'pixelattribute.C', 'expandgrp.C', 'bitmask.C',
    'pixelgroup.C', 'pixelselectioncourier.C',
    'random.C', 'swiglib.C', 'switchboard.C', 'threadstate.C',
    'timestamp.C', 'sincos.C', 'pythonlock.C', 'progress.C',
    'vtkColorLUT.C', 'guitop.C', 'direction.C', 'clip.C', 'voxelfilter.C',
    'geometry.C', 'doublevec.C', 'vectormath.C', 'smallmatrix.C',
    'voxelsetboundary.C', 'latticesystem.C', 'trace.C'
    ]

swigfiles = [
    'imagebase.swg', 'activearea.swg', 'argv.swg', 'boolarray.swg',
    'cdebug.swg', 'ccolor.swg','cmicrostructure.swg', 'colordifference.swg',
    'config.swg', 'coord.swg', 'cpixelselection.swg', 'crandom.swg',
    'doublearray.swg', 'geometry.swg', 'lock.swg', 'ooferror.swg',
    'pixelattribute.swg', 'pixelgroup.swg', 'pixelselectioncourier.swg',
    'switchboard.swg', 'threadstate.swg', 'timestamp.swg', 'progress.swg',
    'vtkColorLUT.swg', 'guitop.swg', 'direction.swg', 'clip.swg',
    'voxelfilter.swg', 'doublevec.swg', 'smallmatrix.swg', 'trace.swg',
    'identification.swg', 'voxelsetboundary.swg', 'latticesystem.swg'
    ]

pyfiles = [
    'color.py', 'debug.py', 'excepthook.py', 'garbage.py',
    'oof_getopt.py', 'oofversion.py', 'parallel_enable.py', 'quit.py',
    'subthread.py', 'thread_enable.py', 'utils.py', 'worker.py',
    'threadmanager.py', 'selectionshape.py', 'selectionoperators.py'
    ]

swigpyfiles = [
    'activearea.spy', 'cmicrostructure.spy', 'colordifference.spy',
    'coord.spy', 'geometry.spy', 'lock.spy', 'ooferror.spy', 'cdebug.spy',
    'pixelattribute.spy', 'pixelgroup.spy', 'switchboard.spy', 'guitop.spy',
    'direction.spy', 'clip.spy', 'voxelfilter.spy', 'doublevec.spy',
    'smallmatrix.spy', 'voxelsetboundary.spy', 'latticesystem.spy'
    ]

hfiles = [
    'imagebase.h', 'activearea.h', 'argv.h', 'boolarray.h', 'cdebug.swg',
    'ccolor.h', 'cmicrostructure.h', 'colordifference.h', 'coord.h',
    'cpixelselection.h', 'doublearray.h', 'geometry.h', 'identification.h',
    'lock.h', 'guitop.h', 'bitmask.h', 'doublevec.h', 'vectormath.h',
    'ooferror.h', 'pixelattribute.h', 'pixelgroup.h',
    'pixelselectioncourier.h', 'random.h',
    'swiglib.h', 'switchboard.h', 'threadstate.h', 'timestamp.h',
    'pythonlock.h', 'progress.h', 'sincos.h', 'vtkColorLUT.h', 
    'direction.h', 'clip.h', 'differ.h', 'voxelfilter.h', 'cleverptr.h',
    'smallmatrix.h', "pixelattribute_i.h", 'coord_i.h', 'trace.h',
    'setutils.h', 'derefcompare.h', 'voxelsetboundary.h', 'latticesystem.h'
    ]


if HAVE_MPI:
    cfiles.extend(['mpitools.C'])
    swigfiles.extend(['mpitools.swg'])
    swigpyfiles.extend(['mpitools.spy'])
    hfiles.extend(['mpitools.h'])

def set_clib_flags(clib):
    if HAVE_MPI:
        clib.externalLibs.append('pmpich++')
        clib.externalLibs.append('mpich')
    addVTKlibs(clib, [
        ## TODO: This needs to work for both vtk8 and vtk9
        ## libs for vtk9
        ## libs from the #defines created by FindNeededModules
        'vtkIOExportPDF',
        'vtkIOExportGL2PS',
        #'vtkRenderingContextOpenGL2', # doesn't exist
        'vtkInteractionStyle',
        'vtkRenderingFreeType',
        'vtkRenderingOpenGL2',
        'vtkRenderingUI',
        'vtkRenderingGL2PSOpenGL2',
        'vtkRenderingVolumeOpenGL2',
        ## Added due to 'undefined symbol' messages at run time
        'vtkFiltersExtraction',
        'vtkRenderingAnnotation',
        
        ## Libs included w/ vtk8
        # 'vtkCommonCore',
        # 'vtkCommonDataModel',
        # 'vtkCommonExecutionModel',
        # 'vtkCommonMisc',
        # 'vtkCommonTransforms',
        # 'vtkFiltersCore',
        # 'vtkFiltersExtraction',
        # 'vtkFiltersGeneral',
        # 'vtkFiltersModeling',
        # 'vtkFiltersSources',
        # 'vtkIOExport',
        # 'vtkIOExportPDF',
        # 'vtkIOExportOpenGL2',
        # 'vtkIOImage',
        # 'vtkIOXML',
        # 'vtkImagingCore',
        # 'vtkImagingColor',
        # 'vtkImagingGeneral',
        # 'vtkRenderingAnnotation',
        # 'vtkRenderingContextOpenGL2',
        # 'vtkRenderingCore',
        # 'vtkRenderingFreeType',
        # 'vtkRenderingOpenGL2',
        # 'vtkRenderingGL2PSOpenGL2',
        # 'vtkRenderingVolumeOpenGL2'
    ])
        
