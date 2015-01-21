# -*- python -*-
# $RCSfile: autoskeleton.py,v $
# $Revision: 1.11.2.5 $
# $Author: langer $
# $Date: 2014/08/20 02:21:17 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

## This file defines a menu item that aggregates a bunch of other menu
## items in an attempt to create and adapt a Skeleton completely
## automatically.  The user must provide two length scales -- the size
## of the largest and smallest features of interest in the
## microstructure.  An initial Skeleton is created at the larger
## length scale and refined by homogeneity (using the provided
## threshold) to the smaller scale.  Then SnapRefine is applied once,
## the Skeleton is Rationalized, and finally it's Smoothed (after
## pinning internal boundary nodes).

from ooflib.SWIG.common import config
from ooflib.SWIG.common import progress
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
#from ooflib.engine.IO import skeletonmenu
import ooflib.common.microstructure
import math
import sys

if config.dimension() == 2:
    def autoSkeleton(menuitem, name, microstructure,
                      x_periodicity, y_periodicity,
                      maxscale, minscale, units, threshold):
        # Run the actual callback in the main namespace, so that it can
        # use menu and registeredclass names trivially.
        prog = progress.getProgress(menuitem.name, progress.DEFINITE)
        utils.OOFrun(_autoSkeletonMain, prog, name, microstructure,
                     x_periodicity, y_periodicity, False, 
                     maxscale, minscale, units, threshold)
        prog.finish()

elif config.dimension() == 3:
    def autoSkeleton(menuitem, name, microstructure,
                     x_periodicity, y_periodicity, z_periodicity,
                     maxscale, minscale, units, threshold):
        # Run the actual callback in the main namespace, so that it can
        # use menu and registeredclass names trivially.
        prog = progress.getProgress(menuitem.name, progress.DEFINITE)
        utils.OOFrun(_autoSkeletonMain, prog, name, microstructure,
                     x_periodicity, y_periodicity, z_periodicity,
                     maxscale, minscale, units, threshold)
        prog.finish()

# Autoskeleton takes a progress argument, and increments it as it goes
# along. If it gets a "stop" signal from the user, it just returns --
# since this operation is "script-like", stopping the process does not
# prevent the incremental skeleton modifications from being pushed on
# the stack, but the user can still "undo" them using the regular
# skeleton undo mechanism.

## TODO 3.1: Update for 3D and uncomment the menuitem.  The optimal
## sequence of skeleton modifications may be different in 3D.

def _autoSkeletonMain(prog, name, microstructure,
                      x_periodicity, y_periodicity, z_periodicity,
                      maxscale, minscale, units,
                      threshold):
    ms = ooflib.common.microstructure.microStructures[microstructure]
    if units == 'Pixel':
        size = ms.getObject().sizeInPixels()
        n0 = size/maxscale
        n1 = size/minscale
    elif units == 'Physical':
        size = ms.getObject().size()
        n0 = size/maxscale
        n1 = size/minscale
    else:    # A fraction of the x and y dimensions of the microstructure
        n = 1.0/maxscale
        n0 = [n for i in range(config.dimension())]
        n1 = [n for i in range(config.dimension())]
#         nx0 = 1.0/maxscale
#         ny0 = nx0
#         nx1 = 1.0/minscale
#         ny1 = nx1

    n0 = [max(n0[i],1) for i in range(config.dimension())]
    #nx0 = max(nx0, 1)
    #ny0 = max(ny0, 1)
    
    nrefine = int(math.ceil(max([math.log(n1[i]/n0[i])/math.log(2)
                                 for i in range(config.dimension())])))
    #nrefine_x = math.log(nx1/nx0)/math.log(2)
    #nrefine_y = math.log(ny1/ny0)/math.log(2)
    #nrefine = int(math.ceil(max(nrefine_x, nrefine_y)))

    # Magic number -- total number of lines executed is the number of
    # refines plus the "New", the "SnapRefine", the two rationalize
    # operations, the boundary node pinning, the smoothing, and the
    # unpinning.  Total is seven. 
    total_lines = nrefine + 7
    ftotal_lines = float(total_lines) # For computing fractional progress.
    lcount = 0

    skelname = microstructure+":"+name

    prog.setFraction(float(lcount)/ftotal_lines)
    prog.setMessage("%d/%d operations" % (lcount, total_lines))
    if prog.stopped():
        return
    
    if config.dimension() == 2:
        OOF.Skeleton.New(name=name, 
                         microstructure=microstructure,
                         x_elements=int(math.ceil(n0[0])),
                         y_elements=int(math.ceil(n0[1])),
                         skeleton_geometry=QuadSkeleton(
                             x_periodicity=x_periodicity,
                             y_periodicity=y_periodicity))
    elif config.dimension() == 3:
        OOF.Skeleton.New(name=name, 
                         microstructure=microstructure,
                         x_elements=int(math.ceil(n0[0])),
                         y_elements=int(math.ceil(n0[1])),
                         z_elements=int(math.ceil(n0[2])),
                         skeleton_geometry=TetraSkeleton(
                             x_periodicity=x_periodicity,
                             y_periodicity=y_periodicity,
                             z_periodicity=z_periodicity))
    lcount += 1
                     
    prog.setFraction(float(lcount)/ftotal_lines)
    prog.setMessage("%d/%d operations" % (lcount, total_lines))
    if prog.stopped():
        return
    

    # some dimensionally dependent objects
    if config.dimension() == 2:
        the_rule_set = 'liberal'
        the_rationalizers = [RemoveShortSide(ratio=5.0),
                             QuadSplit(angle=150),
                             RemoveBadTriangle(acute_angle=15,obtuse_angle=150)]
    elif config.dimension() == 3:
        the_rule_set = 'conservative'
        the_rationalizers = [RemoveBadTetra(acute_angle=15,obtuse_angle=150)]
  
    for i in range(nrefine):
        OOF.Skeleton.Modify(
            skeleton=skelname,
            modifier=Refine(targets=CheckHomogeneity(threshold=threshold),
                            criterion=Unconditionally(),
                            degree=Bisection(rule_set=the_rule_set),
                            alpha=0.8))
        lcount += 1
        prog.setFraction(float(lcount)/ftotal_lines)
        prog.setMessage("%d/%d operations" % (lcount, total_lines))
        if prog.stopped():
            return

    # For SnapRefine, set the min_distance between nodes to be 1/10 of
    # the pixel size.  This is arbitrary, but should be good enough.
    # It's virtually zero on any meaningful physical scale, but not so
    # small that round-off can create illegal elements.
    pxlsize = ms.getObject().sizeOfPixels()
    mindist = 0.1
    OOF.Skeleton.Modify(
        skeleton=skelname,
        modifier=SnapRefine(targets=CheckHomogeneity(threshold=threshold),
                            criterion=Unconditionally(),
                            min_distance=mindist))
    lcount += 1
    prog.setFraction(float(lcount)/ftotal_lines)
    prog.setMessage("%d/%d operations" % (lcount, total_lines))
    if prog.stopped():
        return
    
    for i in range(2):
        OOF.Skeleton.Modify(
            skeleton=skelname,
            modifier=Rationalize(targets=AllElements(),
                                 criterion=AverageEnergy(alpha=0.8),
                                 method=SpecificRationalization(
            rationalizers=the_rationalizers)
                                 )
            )
        lcount += 1
        prog.setFraction(float(lcount)/ftotal_lines)
        prog.setMessage("%d/%d operations" % (lcount, total_lines))
        if prog.stopped():
            return
        
    OOF.Skeleton.PinNodes.Pin_Internal_Boundary_Nodes(skeleton=skelname)
    lcount += 1
    prog.setFraction(float(lcount)/ftotal_lines)
    prog.setMessage("%d/%d operations" % (lcount, total_lines))
    if prog.stopped():
        return
    
    OOF.Skeleton.Modify(
        skeleton=skelname,
        modifier=Smooth(targets=AllNodes(),
                        criterion=AverageEnergy(alpha=0.3),
                        T=0.0,
                        iteration=FixedIteration(iterations=5)))
    lcount += 1
    prog.setFraction(float(lcount)/ftotal_lines)
    prog.setMessage("%d/%d operations" % (lcount, total_lines))
    if prog.stopped():
        return
    
    OOF.Skeleton.PinNodes.Undo(skeleton=skelname)
    lcount += 1
    prog.setFraction(float(lcount)/ftotal_lines)
    prog.setMessage("%d/%d operations" % (lcount, total_lines))


    # end _autoSkeletonMain

# # TODO 3.1: Should the menu item be in engine/IO, and not here?

# if config.dimension() == 2:
#     periodicityParams = parameter.ParameterGroup(
#         parameter.BooleanParameter('x_periodicity', value=False,
#             tip="Whether or not the skeleton is periodic in the horizontal direction"),
#         parameter.BooleanParameter("y_periodicity", value=False,
#             tip="Whether or not the skeleton is periodic in the vertical direction"))
# if config.dimension() == 3:
#     periodicityParams = parameter.ParameterGroup(
#         parameter.BooleanParameter('x_periodicity', value=False,
#             tip="Whether or not the skeleton is periodic in the horizontal direction"),
#         parameter.BooleanParameter("y_periodicity", value=False,
#             tip="Whether or not the skeleton is periodic in the vertical direction"),
#         parameter.BooleanParameter("z_periodicity", value=False,
#             tip="Whether or not the skeleton is periodic in the third direction"))


# skeletonmenu.skeletonmenu.addItem(oofmenu.OOFMenuItem(
#     'Auto',
#     callback=autoSkeleton,
#     threadable=oofmenu.THREADABLE,
#     no_log=True,                        # because it calls other menu items
#     params=parameter.ParameterGroup(
#     parameter.AutomaticNameParameter('name',
#                            value=automatic.automatic,
#                            resolver=skeletonmenu.skeletonNameResolver,
#                            tip="Name of the new skeleton."),
#     whoville.WhoParameter('microstructure',
#                           ooflib.common.microstructure.microStructures,
#                           tip=parameter.emptyTipString)) +
#     periodicityParams +
#     parameter.ParameterGroup(
#     parameter.FloatParameter('maxscale', value=1.0,
#                              tip="Rough size of the largest elements."),
#     parameter.FloatParameter("minscale", value=1.0,
#                              tip="Rough size of the smallest elements."),
#     enum.EnumParameter('units', ooflib.common.units.Units, value='Physical',
#                        tip="Units for minscale and maxscale."),
#     parameter.FloatRangeParameter('threshold', (0.0, 1.0, 0.01),
#                                   value=0.90,
#                                   tip="Minimum acceptable homogeneity")
#     ),                                  # end of ParameterGroup
#     help="Automatically create and refine a &skel;.",
#     discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/menu/autoskel.xml")
#     ))
