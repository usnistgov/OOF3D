# -*- python -*-
# $RCSfile: skeletonmenu.py,v $
# $Revision: 1.142.2.29 $
# $Author: langer $
# $Date: 2014/12/02 21:52:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Skeleton menu.  Contains the commands for creating and
# refining/modifying skeletons.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import cskeleton2
from ooflib.SWIG.engine import cskeletonmodifier
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import labeltree
from ooflib.common import microstructure
from ooflib.common import parallel_enable
from ooflib.common.IO import automatic
from ooflib.common.IO import datafile
from ooflib.common.IO import filenameparam
from ooflib.common.IO import mainmenu
from ooflib.common.IO import microstructureIO
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import autoskeleton
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import skeletonIO
import ooflib.common.units
import sys

OOF = mainmenu.OOF
RegisteredParameter = parameter.RegisteredParameter
IntParameter = parameter.IntParameter
WhoParameter = whoville.WhoParameter
microStructures = microstructure.microStructures
AutoWhoNameParameter = whoville.AutoWhoNameParameter
WhoNameParameter = whoville.WhoNameParameter

skeletonmenu = OOF.addItem(oofmenu.OOFMenuItem(
    'Skeleton',
    cli_only=1,
    help='Create and modify mesh Skeletons.',
    discussion="""<para>
    The <command>Skeleton</command> menu contains tools to create and
    modify &skels;.
    </para>"""
    ))

#####################

def skeletonNameResolver(param, startname):
    if param.automatic():
        basename = 'skeleton'
    else:
        basename = startname
    msname = param.group['microstructure'].value
    mspath = labeltree.makePath(msname)
    # In the command-line case, msname may not be set yet -- return
    # "None" so the menu system will prompt the user.
    if not mspath:
        return None
    return skeletoncontext.skeletonContexts.uniqueName(mspath + [basename])

######################

if config.dimension() == 2:

    def _skeleton_from_mstructure(menuitem, name, microstructure,
                                  x_elements, y_elements,
                                  skeleton_geometry):
        if parallel_enable.enabled():  # PARALLEL
            skel = cskeleton2.initialSkeletonParallel(name, microstructure,
                                             x_elements, y_elements,
                                             skeleton_geometry)
        else:
            ms = microStructures[microstructure].getObject()
            skel = cskeleton2.initialSkeleton(name, ms,
                                            x_elements, y_elements,
                                            skeleton_geometry)
        switchboard.notify("redraw")

    skelparams=parameter.ParameterGroup(
        AutoWhoNameParameter('name', value=automatic.automatic,
                             resolver=skeletonNameResolver,
                             tip="Name of the new skeleton."),
        WhoParameter('microstructure', microStructures,
                     tip=parameter.emptyTipString),
        IntParameter('x_elements', 4,
                     tip="No. of elements in the x-direction."),
        IntParameter('y_elements', 4,
                     tip="No. of elements in the y-direction."),
        RegisteredParameter('skeleton_geometry', skeleton.SkeletonGeometry,
                            skeleton.QuadSkeleton(),
                            tip="The shape of the elements."))

elif config.dimension() == 3:

    def _skeleton_from_mstructure(menuitem, name, microstructure,
                                  x_elements, y_elements, z_elements,
                                  skeleton_geometry):
        if parallel_enable.enabled():  # PARALLEL
            skel = cskeleton2.initialSkeletonParallel(name, microstructure,
                                             x_elements, y_elements,
                                             z_elements, skeleton_geometry)
        else:
            ms = microStructures[microstructure].getObject()
            skel = cskeleton2.initialSkeleton(
                name, ms, x_elements, y_elements, z_elements,
                skeleton_geometry)
        switchboard.notify("redraw")

    skelparams=parameter.ParameterGroup(
        AutoWhoNameParameter('name', value=automatic.automatic,
                             resolver=skeletonNameResolver,
                             tip="Name of the new skeleton."),
        WhoParameter('microstructure', microStructures,
                     tip=parameter.emptyTipString),
        IntParameter('x_elements', 4
                     , tip="No. of elements in the x-direction."),
        IntParameter('y_elements', 4,
                     tip="No. of elements in the y-direction."),
        IntParameter('z_elements', 4,
                     tip="No. of elements in the z-direction."),
        RegisteredParameter('skeleton_geometry',
                            cskeleton2.SkeletonGeometry,
                            cskeleton2.TetraSkeleton(),
                            tip="The shape of the elements."))


skeletonmenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=_skeleton_from_mstructure,
    threadable=oofmenu.THREADABLE,
    params=skelparams,
    help="Create a new Skeleton in a Microstructure.",
    discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/skeleton_new.xml')
    ))

#########################

    
def _simple_skeleton_from_ms(menuitem, name, microstructure, skeleton_geometry):
    ms = microStructures[microstructure].getObject()
    x_elements = ms.sizeInPixels()[0]
    y_elements = ms.sizeInPixels()[1]
    if config.dimension() == 2:
        skel = cskeleton2.simpleSkeleton(name, ms, x_elements, y_elements,
                                   skeleton_geometry)
    elif config.dimension() == 3:
        z_elements = ms.sizeInPixels()[2]
        skel = cskeleton2.simpleSkeleton(name, ms, x_elements, y_elements,
                                       z_elements, skeleton_geometry) 
    switchboard.notify("redraw")

if config.dimension() == 2:
    simpleparams=parameter.ParameterGroup(
        AutoWhoNameParameter('name', value=automatic.automatic,
                             resolver=skeletonNameResolver,
                             tip="Name of the simple skeleton."),
        WhoParameter('microstructure', microStructures,
                     tip=parameter.emptyTipString),
        RegisteredParameter('skeleton_geometry', cskeleton2.SkeletonGeometry, cskeleton2.QuadSkeleton(),
                  tip="Geometry of elements, quadrilateral or triangle."))

elif config.dimension() == 3:
    simpleparams=parameter.ParameterGroup(
        AutoWhoNameParameter('name', value=automatic.automatic,
                             resolver=skeletonNameResolver,
                             tip="Name of the simple skeleton."),
        WhoParameter('microstructure', microStructures,
                     tip=parameter.emptyTipString),
        RegisteredParameter('skeleton_geometry', cskeleton2.SkeletonGeometry, cskeleton2.TetraSkeleton(),
                  tip="Geometry of elements (currently the only choice is Tetra)."))

    

skeletonmenu.addItem(oofmenu.OOFMenuItem(
    'Simple',
    callback=_simple_skeleton_from_ms,
    threadable=oofmenu.THREADABLE,
    params=simpleparams,
    help="Create a new Skeleton with one quadrilateral or two triangular elements per pixel of the Microstructure.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/skeleton_simple.xml')
    ))

#########################

def signal(selection):
  switchboard.notify(selection.mode().changedselectionsignal,
                     selection=selection)
  switchboard.notify("redraw")

def _skeleton_delete(menuitem, skeleton):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    
    elementselection = skelcontext.elementselection
    faceselection = skelcontext.faceselection
    segmentselection = skelcontext.segmentselection
    nodeselection = skelcontext.nodeselection
    
    if elementselection is not None:
	elementselection.begin_writing()
	try:
	    elementselection.start()
	    elementselection.clear()
	finally:
	    elementselection.end_writing()
	signal(elementselection)
	
    if faceselection is not None:
	faceselection.begin_writing()
	try:
	    faceselection.start()
	    faceselection.clear()
	finally:
	    faceselection.end_writing()
	signal(faceselection)
	
    if segmentselection is not None:
	segmentselection.begin_writing()
	try:
	    segmentselection.start()
	    segmentselection.clear()
	finally:
	    segmentselection.end_writing()
	signal(segmentselection)
	
    if nodeselection is not None:
	nodeselection.begin_writing()
	try:
	    nodeselection.start()
	    nodeselection.clear()
	finally:
	    nodeselection.end_writing()
	signal(nodeselection)
	
    if parallel_enable.enabled():
        from ooflib.engine.IO import skeletonIPC
        skeletonIPC.smenu.Delete(skeleton=skeleton)
    else:
        skelctxt = skeletoncontext.skeletonContexts[skeleton]
        skelobj = skelctxt.getObject()
        skeletoncontext.skeletonContexts[skeleton].lockAndDelete()
#         # Debugging
#         debug.fmsg("Skeleton context refcount =", sys.getrefcount(skelctxt)-2)
#         debug.fmsg("Skeleton refcount =", sys.getrefcount(skelobj)-2)
#         import gc
#         gc.collect()
#         debug.fmsg("garbage=", gc.garbage)
#         debug.fmsg("context referrers=")
#         debug.dumpReferrers(obj=skelctxt, levels=2)
#         debug.fmsg("skeleton referrers=")
#         debug.dumpReferrers(obj=skelobj, levels=2)
#         del skelctxt
#         del skelobj
#         from ooflib.SWIG.engine import cskeleton
#         debug.fmsg("There are", cskeleton.get_globalNodeCount(),
#                    "leftover nodes")
#         debug.fmsg("There are", cskeleton.get_globalElementCount(),
#                    "leftover elements")
#         from ooflib.SWIG.engine import femesh
#         debug.fmsg("There are", femesh.get_globalFEMeshCount(), 
#                    "leftover meshes")

skeletonmenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=_skeleton_delete,
    params=[WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                         tip=parameter.emptyTipString)],
    help="Delete a Skeleton.",
    discussion= """<para>
    Delete a &skel; and all of its associated data, including any
    &meshes; that have been derived from it.
    </para>"""))


#########################

def _skeleton_copy(menuitem, skeleton, name):
    if parallel_enable.enabled():
        from ooflib.engine.IO import skeletonIPC
        skeletonIPC.smenu.Copy(skeleton=skeleton, name=name)
        return

    # skeleton is a colon separated string
    oldskelpath = labeltree.makePath(skeleton)
    oldskelcontext = skeletoncontext.skeletonContexts[skeleton]
    if name is automatic.automatic:
        nm = skeletoncontext.skeletonContexts.uniqueName(skeleton)
    else:
        nm = name
        
    orig = oldskelcontext.getObject()
    newskel = oldskelcontext.resolveCSkeleton(orig.completeCopy())
    for e in oldskelcontext.edgeboundaries.values():
        newskel.mapBoundary(e, orig, local=None)
    for p in oldskelcontext.pointboundaries.values():
        newskel.mapBoundary(p, orig, local=None)
    for f in oldskelcontext.faceboundaries.values():
        newskel.mapBoundary(f, orig, local=None)

    msname = oldskelpath[0]
    # "add" calls the SkeletonContext constructor, which calls
    # "disconnect" on the skeleton, ensuring that the propagation
    # we just did doesn't mess up the old skeleton context.
    skeletoncontext.skeletonContexts.add(
        [msname, nm], newskel,
        parent=microstructure.microStructures[msname])

    newskelcontext = skeletoncontext.skeletonContexts[ [msname, nm] ]
    newskelcontext.groupCopy(oldskelcontext)


def copySkeletonNameResolver(param, startname):
    if param.automatic():
        basename = 'skeleton'
    else:
        basename = startname
    skelname = param.group['skeleton'].value
    skelcontext = skeletoncontext.skeletonContexts[skelname]
    return skelcontext.uniqueName(basename)

skeletonmenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=_skeleton_copy,
    params=parameter.ParameterGroup(
    WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                 tip=parameter.emptyTipString),
    AutoWhoNameParameter('name', resolver=copySkeletonNameResolver,
                         value=automatic.automatic, tip="Name of the copy.")
    ),
    help="Copy a Skeleton.",
    discussion=
    """<para>
    Make a copy of a &skel;.  The new &skel; belongs to the same
    &micro; as the original.  &meshes; belonging to the original
    &skel; will <emphasis>not</emphasis> be copied.
    </para>""" ))


########################

def _skeleton_rename(menuitem, skeleton, name):
    if parallel_enable.enabled():
        from ooflib.engine.IO import skeletonIPC
        skeletonIPC.smenu.Rename(skeleton=skeleton, name=name)
        return

    # skeleton is a colon separated string
    oldskelpath = labeltree.makePath(skeleton)
    skel = skeletoncontext.skeletonContexts[oldskelpath]
    skel.reserve()
    skel.begin_writing()
    try:
        skel.rename(name, exclude=oldskelpath[-1])
    finally:
        skel.end_writing()
        skel.cancel_reservation()

skeletonmenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=_skeleton_rename,
    params=parameter.ParameterGroup(
    WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                 tip=parameter.emptyTipString),
    WhoNameParameter('name', value='', tip='New name for the skeleton.')
    ),
    help="Rename a Skeleton.",
    discussion="<para> Assign a new name to a &skel;. </para>"
    ))


########################

def _modify_callback(menuitem, skeleton, modifier):
    if parallel_enable.enabled():
        from ooflib.engine.IO import skeletonIPC
        skeletonIPC.smenu.Modify(skeleton=skeleton, modifier=modifier)
    else:
        _modify(menuitem, skeleton, modifier)

def _modify(menuitem, skeleton, modifier):
    context = skeletoncontext.skeletonContexts[skeleton]
    context.reserve()
    start_nnodes = context.getObject().nnodes()
    start_nelems = context.getObject().nelements()
    try:
        context.begin_writing()
        try:
            skel = modifier.apply(context.getObject())
            ## skel is None whenever the modifier fails
            ## or is interrupted from finishing its task
            if skel is None:
                reporter.warn("Modify Process Interrupted")
                return
            context.pushModification(skel)
            skel.needsHash()
        finally:
            context.end_writing()
            
        ## If the skeleton is modified in postProcess, use
        ## begin/end_writing inside the function call to guarantee
        ## that no dead-locking occurs because of possible switchboard
        ## calls that may make use of begin/end_reading(). See
        ## cfiddlenodes.spy for an example.
        modifier.postProcess(context)
        modifier.cleanUp()
        skel.incrementTimestamp()

        end_nnodes = context.getObject().nnodes()
        end_nelems = context.getObject().nelements()
        if end_nnodes > start_nnodes:
            reporter.report(end_nnodes-start_nnodes, "more nodes.")
        elif end_nnodes < start_nnodes:
            reporter.report(start_nnodes-end_nnodes, "fewer nodes.")
        if end_nelems > start_nelems:
            reporter.report(end_nelems-start_nelems, "more elements.")
        elif end_nelems < start_nelems:
            reporter.report(start_nelems-end_nelems, "fewer elements.")
    finally:
        context.cancel_reservation()

    # "Skeleton modified" indicates that a specific modifier has been
    # applied.  "Skeleton changed" indicates that something has
    # changed, which might or might not have involved a
    # SkeletonModifier.  "Skeleton changed" is not redundant with "who
    # changed", because "who changed" is issued by pushModification
    # before postProcess is called, and postProcess might do most of
    # the work in a SkeletonModifier.
    ## TODO OPT: Some modifiers send these notifications in
    ## postProcess.  Don't send them again here.
    switchboard.notify('Skeleton modified', skeleton, modifier)
    switchboard.notify('Skeleton changed', skeleton)
    switchboard.notify('redraw')

skeletonmenu.addItem(oofmenu.OOFMenuItem(
    "Modify",
    callback=_modify_callback,
    threadable=oofmenu.THREADABLE,
    params=[WhoParameter('skeleton',
                         skeletoncontext.skeletonContexts,
                         tip=parameter.emptyTipString),
            RegisteredParameter('modifier',
                                cskeletonmodifier.CSkeletonModifierBase,
                                tip="Skeleton modifier to apply.")],
    help="Modify a Skeleton in various ways.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/skeleton_modify.xml')
    ))

########################

def _undo(menuitem, skeleton):
    if parallel_enable.enabled():
        from ooflib.engine.IO import skeletonIPC
        skeletonIPC.smenu.Undo(skeleton=skeleton)
    
    context = skeletoncontext.skeletonContexts[skeleton]
    if not context.undoable():
        raise ooferror.ErrUserError("Can't undo skeleton modification!")

    context.begin_writing()
    try:
        context.undoModification()
    finally:
        context.end_writing()
        switchboard.notify('redraw')

skeletonmenu.addItem(oofmenu.OOFMenuItem(
    "Undo",
    callback=_undo,
    params=[WhoParameter('skeleton',
                         skeletoncontext.skeletonContexts,
                         tip=parameter.emptyTipString)],
    help="Undo a Skeleton modification.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/skeleton_undo.xml')
    ))
        
def _redo(menuitem, skeleton):
    if parallel_enable.enabled():
        from ooflib.engine.IO import skeletonIPC
        skeletonIPC.smenu.Redo(skeleton=skeleton)
    
    context = skeletoncontext.skeletonContexts[skeleton]
    if not context.redoable():
        raise ooferror.ErrUserError("Can't redo skeleton modification!")

    context.begin_writing()
    try:
        context.redoModification()
    finally:
        context.end_writing()
        switchboard.notify('redraw')

skeletonmenu.addItem(oofmenu.OOFMenuItem(
    "Redo",
    callback=_redo,
    params=[WhoParameter('skeleton',
                         skeletoncontext.skeletonContexts,
                         tip=parameter.emptyTipString)],
    help="Redo a Skeleton modification.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/skeleton_redo.xml')
    ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# AutoSkeleton creation

if config.dimension() == 2:
    periodicityParams = parameter.ParameterGroup(
        parameter.BooleanParameter('x_periodicity', value=False,
            tip="Whether or not the skeleton is periodic in the x direction"),
        parameter.BooleanParameter("y_periodicity", value=False,
            tip="Whether or not the skeleton is periodic in the y direction"))
if config.dimension() == 3:
    ## TODO 3.1: 3D autoskeleton is probably completely untested.  The
    ## periodicity args are certainly irrelevant because 3D periodic
    ## skeletons aren't supported yet.
    periodicityParams = parameter.ParameterGroup(
        parameter.BooleanParameter('x_periodicity', value=False,
            tip="Whether or not the skeleton is periodic in the x direction"),
        parameter.BooleanParameter("y_periodicity", value=False,
            tip="Whether or not the skeleton is periodic in the y direction"),
        parameter.BooleanParameter("z_periodicity", value=False,
            tip="Whether or not the skeleton is periodic in the z direction"))

skeletonmenu.addItem(oofmenu.OOFMenuItem(
    'Auto',
    callback=autoskeleton.autoSkeleton,
    threadable=oofmenu.THREADABLE,
    no_log=True,                        # because it calls other menu items
    params=parameter.ParameterGroup(
    parameter.AutomaticNameParameter('name',
                           value=automatic.automatic,
                           resolver=skeletonNameResolver,
                           tip="Name of the new skeleton."),
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString)) +
    periodicityParams +
    parameter.ParameterGroup(
    parameter.FloatParameter('maxscale', value=1.0,
                             tip="Rough size of the largest elements."),
    parameter.FloatParameter("minscale", value=1.0,
                             tip="Rough size of the smallest elements."),
    enum.EnumParameter('units', ooflib.common.units.Units, value='Physical',
                       tip="Units for minscale and maxscale."),
    parameter.FloatRangeParameter('threshold', (0.0, 1.0, 0.01),
                                  value=0.90,
                                  tip="Minimum acceptable homogeneity")
    ),                                  # end of ParameterGroup
    help="Automatically create and refine a &skel;.",
    discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/menu/autoskel.xml")
    ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def sanity_check(menuitem, skeleton, quick):
    skelctxt = skeletoncontext.skeletonContexts[skeleton]
    if quick:
        sane = skelctxt.getObject().quick_sanity_check()
    else:
        sane = skelctxt.sanity_check()
    skelctxt.sane = sane        # used by skeleton_modification_test.py
    if not sane:
        raise ooferror.ErrPyProgrammingError("Skeleton sanity check failed!")

OOF.Help.Debug.addItem(oofmenu.OOFMenuItem(
    'Sanity_Check',
    callback=sanity_check,
    ordering=100,
    params=[WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                         tip=parameter.emptyTipString),
            parameter.BooleanParameter('quick', 1,
                                       tip="quick or thorough?")],
    help="Check for errors in Skeleton construction.",
    discussion="""<para>

    The quick check (<varname>quick</varname>=<constant>1</constant>)
    just checks for <link
    linkend='Section-Concepts-Skeleton-Illegality'>illegal
    elements</link>.  The thorough check
    (<varname>quick</varname>=<constant>0</constant>) also checks that
    the internal data structures are self-consistent.  This command
    should never be needed by end-users, but some of them have found
    it reassuring.

    </para>"""
    ))

#####################

def saveSkeleton(menuitem, filename, mode, format, skeleton):
    skelcontext = skeletoncontext.skeletonContexts[skeleton]
    if format==datafile.ABAQUS:
        skeletonIO.writeABAQUSfromSkeleton(filename, mode.string(),
                                           skelcontext)
    else:
        dfile = datafile.writeDataFile(filename, mode.string(), format)
        microstructureIO.writeMicrostructure(dfile, skelcontext.getParent())
        skeletonIO.writeSkeleton(dfile, skelcontext)
        dfile.close()

OOF.File.Save.addItem(oofmenu.OOFMenuItem(
    'Skeleton',
    callback = saveSkeleton,
    ordering=70,
    params = [
    filenameparam.WriteFileNameParameter('filename', tip="Name of the file."),
    filenameparam.WriteModeParameter(
                'mode', tip="'w' for (over)write and 'a' to append."),
    enum.EnumParameter('format', datafile.DataFileFormatExt, datafile.ASCII,
                       tip="Format of the file."),
    whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                          tip=parameter.emptyTipString)],
    help="Save a Skeleton to a file.",
    discussion="""
    <para>Store a &skel; in a file in one of several <link
    linkend='Section-Concepts-FileFormats'><varname>formats</varname></link>.
    The file can be reloaded by <xref
    linkend='MenuItem-OOF.File.Load.Script'/> or <xref
    linkend='MenuItem-OOF.File.Load.Data'/>, depending on the file
    format.</para>
    """
    ))

def _fixmenu(*args):
    if skeletoncontext.skeletonContexts.nActual() == 0:
        OOF.File.Save.Skeleton.disable()
    else:
        OOF.File.Save.Skeleton.enable()

_fixmenu()

switchboard.requestCallback(('new who', 'Skeleton'), _fixmenu)
switchboard.requestCallback(('remove who', 'Skeleton'), _fixmenu)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _compareSkeletons(menuitem, skeleton1, skeleton2, tolerance):
    skel1 = skeletoncontext.skeletonContexts[skeleton1].getObject()
    skel2 = skeletoncontext.skeletonContexts[skeleton2].getObject()
    status = skel1.compare(skel2, tolerance)
    if status:
        reporter.report("Skeleton comparison failed:", status)
    else:
        reporter.report("Skeleton comparison succeeded.")


from ooflib.common.IO import mainmenu
mainmenu.debugmenu.addItem(oofmenu.OOFMenuItem(
        'Compare_Skeletons',
        callback=_compareSkeletons,
        ordering=100,
        params=[
            whoville.WhoParameter('skeleton1',
                                  skeletoncontext.skeletonContexts),
            whoville.WhoParameter('skeleton2',
                                  skeletoncontext.skeletonContexts),
            parameter.FloatParameter('tolerance', 1.e-13)],
        secret = not debug.debug()
        ))
