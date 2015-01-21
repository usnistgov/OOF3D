# -*- python -*- 
# $RCSfile: DIR.py,v $
# $Revision: 1.54.2.36 $
# $Author: langer $
# $Date: 2014/12/14 01:07:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = ['engine']
if not DIM_3:
    clib = 'oof2engine'
else:
    clib = 'oof3dengine'
clib_order = 1

subdirs = ['property', 'elements', 'SparseLib++',
           'IO']

if HAVE_PETSC:
    print "PETSC subdirectory appended"
    subdirs.append('PETSc')

cfiles = [
    'canonicalorder.C', 'cnonlinearsolver.C',
    'cskeleton2.C', 'cskeletonselectable.C', 'cskeletonmodifier.C', 
    'cskeletonnode2.C', 'crystalsymmetry.C',
    'cskeletonsegment.C', 'cskeletonelement.C', 'cskeletongroups.C',
    'cfiddlenodes.C', 'crefine.C', 'crefinementcriterion.C', 'csnapnodes.C', 'csnaprefine.C',
    'crationalizers.C', 'elementshape.C',
    'angle2color.C', 'bdyanalysis.C', 'boundarycond.C', 'cskeletonboundary.C',
    'cconjugate.C', 'celectricfield.C', 'cmatrixmethods.C',
    'compoundsubproblem.C', 'contourcell.C',
    'cscpatch.C', 'cstrain.C', 'csubproblem.C',
    'diagpre.C', 'dofmap.C', 'edge.C', 'edgeset.C',
    'eigenvalues.C', 'element.C', 'elementnodeiterator.C',
    'entiremeshsubproblem.C', 'equation.C', 'femesh.C', 'field.C',
    'fieldeqnlist.C', 'fieldindex.C', 'fixillegal.C', 'flux.C', 'fluxnormal.C',
    'freedom.C', 'gausspoint.C', 'icpre.C', 'ilupre.C', 'invariant.C',
    'linearizedsystem.C', 'mastercoord.C', 'materialset.C',
    'masterelement.C', 'material.C', 'materialsubproblem.C',
    'meshdatacache.C', 'meshiterator.C', 'nodalequation.C',
    'nodalfluxes.C', 'nodalscpatches.C', 'node.C', 'ooferror.C',
    'orientationimage.C', 'outputval.C', 'pixelgroupsubproblem.C',
    #'pixelintersection.C',
    'pixelselectioncouriere.C', 'pointdata.C', 'preconditioner.C',
    'property.C', 'pypropertywrapper.C', 'rank3tensor.C',
    'recoveredflux.C', 'shapefunction.C', 'shapefunctioncache.C',
    'smallsystem.C', 'sparsemat.C', 'steperrorscaling.C',
    'symeig3.C', 'symmmatrix.C', 'materialvoxelfilter.C'
]

swigfiles = [
    'cskeleton2.swg','cskeletonselectable.swg','cskeletonmodifier.swg', 
    'cskeletonnode2.swg', 'cnonlinearsolver.swg', 'crystalsymmetry.swg',
    'cskeletonsegment.swg', 'cskeletonelement.swg', 'cskeletongroups.swg',
    'cfiddlenodes.swg', 'crefine.swg', 'crefinementcriterion.swg', 'csnapnodes.swg', 'csnaprefine.swg',
    'crationalizers.swg', 'elementshape.swg',
    'angle2color.swg', 'bdyanalysis.swg', 'boundarycond.swg',
    'cconjugate.swg', 'cmatrixmethods.swg', 'compoundsubproblem.swg',
    'contourcell.swg', 'cstrain.swg',
    'cskeletonboundary.swg',
    'csubproblem.swg', 'diagpre.swg', 'dofmap.swg', 'edge.swg', 
    'edgeset.swg', 'element.swg', 'elementnodeiterator.swg',
    'entiremeshsubproblem.swg', 'equation.swg', 'femesh.swg', 'field.swg',
    'fieldindex.swg', 'fixillegal.swg', 'flux.swg', 'freedom.swg',
    'gausspoint.swg',
    'icpre.swg', 'ilupre.swg', 'invariant.swg', 'linearizedsystem.swg',
    'mastercoord.swg', 'masterelement.swg', 'material.swg',
    'materialsubproblem.swg', 'meshdatacache.swg', 'meshiterator.swg',
    'nodalequation.swg', 'node.swg', 'ooferror2.swg',
    'orientationimage.swg', 'outputval.swg', 'pixelgroupsubproblem.swg',
    'pixelselectioncouriere.swg', 'planarity.swg', 'preconditioner.swg',
    'pointdata.swg',
    'properties.swg', 'pypropertywrapper.swg', 'rank3tensor.swg',
    'smallsystem.swg', 'sparsemat.swg',
    'steperrorscaling.swg', 'symmmatrix.swg', 'materialvoxelfilter.swg'
    ]

pyfiles = [
    'analysisdomain.py', 'analysissample.py',
    'anneal.py', 'autoskeleton.py', 'bdycondition.py', 'boundary.py',
    'boundarybuilder.py', 'boundarymodifier.py', 'builtinprops.py',
    'component.py', 'conjugate.py', 
    'edgeswap.py', 'errorestimator.py', 'euler.py', 'iterationmanager.py',
    'fieldinit.py', 'initialize.py', 'instantnodemove.py',
    'interfaceplugin.py', 'coverage.py',
    'materialmanager.py', 'materialplugin.py', 'mergetriangles.py', 'mesh.py',
    'meshcrosssection.py', 'meshmod.py', 'meshstatus.py',
    'outputschedule.py', 'pinnodesmodifier.py', 'pixelselect.py',
    'problem.py', 'profile.py', 'profilefunction.py',
    'propertyregistration.py', 'pyproperty.py', 'rationalize.py',
    'rationalsharp.py', 'rationalshort.py', 'rationalwide.py',
    'relaxation.py', 'rk.py',
    'scpatch.py', 'skeleton.py', 'skeletonboundary.py',
    'skeletoncontext.py', 'skeletondiff.py', 'skeletonelement.py',
    'skeletongroups.py', 'skeletonnode.py',
    'skeletonsegment.py', 'skeletonselectable.py',
    'skeletonselectionmethod.py', 'skeletonselectionmod.py',
    'skeletonselectionmodes.py', 'skeletonselmodebase.py', 'snapnode.py',
    'snaprefine.py', 'snaprefinemethod.py', 'splitquads.py', 'ss22.py',
    'subproblemcontext.py', 'subproblemtype.py', 'symstate.py',
    'timestepper.py', 'twostep.py', 'solvermode.py'
    ]

swigpyfiles = [
    'cskeleton2.spy','cskeletonmodifier.spy', 'cfiddlenodes.spy', 'crefine.spy',
    'crefinementcriterion.spy', 'angle2color.spy', 'compoundsubproblem.spy', 'csnapnodes.spy', 
    'csnaprefine.spy', 'crystalsymmetry.spy',
    'cskeletongroups.spy','cskeletonelement.spy', 'cskeletonnode2.spy',
    'cskeletonboundary.spy', 'elementshape.spy',
    'contourcell.spy', 'cstrain.spy', 'crationalizers.spy',
    'csubproblem.spy', 'edge.spy', 'edgeset.spy',
    'element.spy', 'equation.spy',
    'femesh.spy', 'field.spy', 'fieldindex.spy', 'fixillegal.spy', 'flux.spy',
    'invariant.spy', 'linearizedsystem.spy', 'mastercoord.spy',
    'masterelement.spy', 'material.spy', 'materialsubproblem.spy',
    'meshdatacache.spy', 'node.spy', 'ooferror2.spy', 'outputval.spy',
    'pixelgroupsubproblem.spy', 'preconditioner.spy', 'property.spy',
    'pypropertywrapper.spy', 'rank3tensor.spy', 
    'steperrorscaling.spy', 'symmmatrix.spy', 'entiremeshsubproblem.spy',
    'materialvoxelfilter.spy'
    ]

hfiles = [
    'canonicalorder.h', 'cnonlinearsolver.h',
    'cskeleton2.h', 'cskeletonselectable.h', 'cskeletonmodifier.h',
    'cskeletonnode2.h', 'crystalsymmetry.h',
    'cskeletonsegment.h', 'cskeletonelement.h', 'cskeletongroups.h',
    'cfiddlenodes.h', 'crefine.h', 'crefinementcriterion.h', 'csnapnodes.h', 'csnaprefine.h',
    'crationalizers.h',
    'angle2color.h', 'bdyanalysis.h', 'cskeletonboundary.h',
    'boundarycond.h', 'cconjugate.h', 'celectricfield.h',
    'cmatrixmethods.h', 'compoundsubproblem.h', 'constraint.h',
    'contourcell.h', 'cscpatch.h', 
    'cstrain.h', 'csubproblem.h', 'diagpre.h', 'dofmap.h', 'edge.h', 
    'edgeset.h', 'eigenvalues.h', 'element.h',
    'elementnodeiterator.h', 'entiremeshsubproblem.h', 'equation.h',
    'femesh.h', 'field.h', 'fieldeqnlist.h', 'fieldindex.h', 'fixillegal.h', 
    'flux.h', 'elementshape.h',
    'fluxnormal.h', 'freedom.h', 'gausspoint.h', 'icpre.h',
    'ilupre.h', 'indextypes.h', 'invariant.h', 'linearizedsystem.h',
    'mastercoord.h', 'masterelement.h', 'material.h', 'materialset.h',
    'materialsubproblem.h', 'meshdatacache.h', 'meshiterator.h',
    'nodalequation.h', 'nodalfluxes.h', 'nodalscpatches.h', 'node.h',
    'ooferror.h', 'orientationimage.h', 'outputval.h',
    'pixelgroupsubproblem.h', 'pixelselectioncouriere.h', 
    'pointdata.h', 'planarity.h',
    'preconditioner.h', 'predicatesubproblem.h', 'property.h',
    'pypropertywrapper.h', 'rank3tensor.h', 'recoveredflux.h', 
    'shapefunction.h', 'shapefunctioncache.h', 'smalltensor.h',
    'smallsystem.h', 'sparsemat.h', 'steperrorscaling.h', 'symeig3.h',
    'symmmatrix.h', 'materialvoxelfilter.h', 'cskeletonselectable_i.h',
    'cskeleton2_i.h'
]


if DIM_3:
    pyfiles.extend(["faceselectdisplay.py"])
    hfiles.extend(["cskeletonface.h", "skeletonfilter.h"])
    cfiles.extend(["cskeletonface.C", "skeletonfilter.C"])
    swigfiles.extend(["cskeletonface.swg", "skeletonfilter.swg"])
    swigpyfiles.extend(["skeletonfilter.spy"])


def set_clib_flags(clib):
    if not DIM_3:
        clib.externalLibs.append('oof2common')
    else:
        clib.externalLibs.append('oof3dcommon')


# if HAVE_MPI:
#     cfiles.extend(['cfiddlenodesbaseParallel.C'])
#     swigfiles.extend(['cfiddlenodesbaseParallel.swg'])
#     swigpyfiles.extend(['cfiddlenodesbaseParallel.spy'])
#     hfiles.extend(['cfiddlenodesbaseParallel.h'])
#     pyfiles.extend(['fiddlenodesbaseParallel.py', 'refineParallel.py'])


