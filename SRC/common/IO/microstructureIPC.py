# -*- python -*-
# $RCSfile: microstructureIPC.py,v $
# $Revision: 1.16.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common.IO import automatic
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import socket2me
from ooflib.SWIG.common import mpitools
import ooflib.common.microstructure


_rank = mpitools.Rank()
_size = mpitools.Size()

# OOF.LoadData.IPC.Microstructure
msmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Microstructure',
                        secret=1,
                        no_log=1)
    )

def newMicrostructure_Parallel(menuitem, name,
                               width, height,
                               width_in_pixels, height_in_pixels):
    # Only for the back-end processes
    global _rank
    if _rank == 0:
        return
    
    ms = ooflib.common.microstructure.Microstructure(
        name, primitives.iPoint(width_in_pixels,
                                height_in_pixels),
        primitives.Point(width, height)
        )

msmenu.addItem(
    oofmenu.OOFMenuItem(
    'New_Parallel',
    callback = newMicrostructure_Parallel,
    secret = 1,
    no_log = 1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    parameter.StringParameter('name'),
    parameter.FloatParameter('width', 1., tip='Width in physical units.'),
    parameter.FloatParameter('height', 1.,tip='Height in physical units.'),
    parameter.IntParameter('width_in_pixels', 10, tip='Width in pixels.'),
    parameter.IntParameter('height_in_pixels', 10, tip='Height in pixels.')
    ]
    ))


### OOF.LoadData.IPC.Microstructure.Initialize
### Transfers the microstructure to the back-end

##def _parallel_init_mic(menuitem, microstructure, pixelsize, physicalsize):
##    debug.fmsg()
##    # microstructure is the name of the microstructure
##    global _rank
##    import ooflib.common.microstructure
##    # front-end work
##    if _rank == 0:
##        pass            
##    # back-end part of the work
##    else:
##        ooflib.common.microstructure.Microstructure(microstructure, pixelsize,
##                                                  physicalsize)

##msmenu.addItem(
##    oofmenu.OOFMenuItem('Initialize',
##                        callback = _parallel_init_mic,
##                        secret=1,
##                        no_log=1,
##                        threadable = oofmenu.PARALLEL_THREADABLE,
##                        params=[parameter.StringParameter('microstructure'),
##                                primitives.iPointParameter('pixelsize'),
##                                primitives.PointParameter('physicalsize')] ))

##def _add_img_context(menuitem, microstructure, imagecontext):
### arguments are microstructure name and image context name
##    global _rank
##    if _rank == 0:
##        # front-end sends imagecontext name and microstructure name
##        pass
##    else:
##        debug.fmsg()
##        # back-end resolves the ImageContext, and adds it to the right
##        # microstructure
##        # assume that img_context already exists
##        from ooflib.SWIG.image import oofimage ## avoid import loop
##        the_name = microstructure + ":" + imagecontext
##        img_context = oofimage.imageContexts[the_name]
##        import ooflib.common.microstructure
##        # actual microstructure
##        ms = ooflib.common.microstructure.microStructures[microstructure].getMicrostructure()
##        # adds image context to microstructure on the other side
##        ms.addImage(img_context)
##        # image.addMicrostructure will be set automatically once the name is resolved


### OOF.LoadData.Microstructure.AddImageContext
##msmenu.addItem(
##    oofmenu.OOFMenuItem('AddImageContext',
##                        callback = _add_img_context,
##                        secret=1,
##                        no_log=1,
##                        threadable = oofmenu.PARALLEL_THREADABLE,
##                        params=[parameter.StringParameter('microstructure'),
##                                parameter.StringParameter('imagecontext')] ))

############################

def renameMicrostructure_parallel(menuitem, microstructure, name):
    ms = ooflib.common.microstructure.microStructures[microstructure]
    ms.reserve()
    aa = ms.getObject().activearea
    aa.begin_writing()
    try:
        aa.rename(name)
    finally:
        aa.end_writing()
    ps = ms.getObject().pixelselection
    ps.begin_writing()
    try:
        ps.rename(name)
    finally:
        ps.end_writing()
    ms.begin_writing()
    try:
        ms.rename(name, exclude=ms.getObject().name())
    finally:
        ms.end_writing()
        ms.cancel_reservation()

msmenu.addItem(
    oofmenu.OOFMenuItem('Rename',
                        callback=renameMicrostructure_parallel,
                        threadable = oofmenu.PARALLEL_THREADABLE,
                        params=[
    parameter.StringParameter('microstructure', '',
                              tip='Old name for the microstructure.'),
    parameter.StringParameter('name', '',
                              tip='New name for the microstructure.')]
                        ))

############################

def copyMicrostructure_parallel(menuitem, microstructure, name):
    ms = ooflib.common.microstructure.microStructures[microstructure]
    ms.begin_reading()
    grouplist = []
    try:
        sourceMS = ms.getObject()
        newMS = sourceMS.nominalCopy(name)
        # First, copy images and load them to copied MS.
        for image in sourceMS.images:
            sourceimage = image.getObject()
            immidge = sourceimage.clone(sourceimage.name())
            imagecontext = oofimage.imageContexts.add(
                [newMS.name(),immidge.name()], immidge, parent=ms)
            newMS.addImage(imagecontext)
        # Copy pixel groups
        for grpname in sourceMS.groupNames():
            sourcegrp = sourceMS.findGroup(grpname)
            # Ignore "newness", all groups will be new.
            (newgrp, newness) = newMS.getGroup(grpname)
            newgrp.add(sourcegrp.members())
            newgrp.set_meshable(sourcegrp.is_meshable())
            grouplist.append(newgrp)
    finally:
        ms.end_reading()
        
    for g in grouplist:
        switchboard.notify("new pixel group", g)

msmenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=copyMicrostructure_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('microstructure', '',
                                      tip='The source microstructure.'),    
            parameter.StringParameter('name')
            ]
    ))

#############################

def deleteMicrostructure_parallel(menuitem, microstructure):
    mscontext = ooflib.common.microstructure.microStructures[microstructure]
    mscontext.lockAndDelete()

msmenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=deleteMicrostructure_parallel,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    parameter.StringParameter('microstructure', '',
                              tip='Name of the microstructure to be deleted.')]
    ))
