# -*- python -*-
# $RCSfile: oofimageIPC.py,v $
# $Revision: 1.16.12.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:39 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.SWIG.common import cmicrostructure
from ooflib.SWIG.common import mpitools
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.image import oofimage
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import primitives
from ooflib.common.IO import automatic
from ooflib.common.IO import mainmenu
from ooflib.common.IO import microstructureIO
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import socket2me
from ooflib.common.IO import whoville
from ooflib.image import imagemodifier
from ooflib.image.IO import imagemenu
import ooflib.common.microstructure


_rank = mpitools.Rank()
_size = mpitools.Size()

## OOF.LoadData.IPC.Image
imenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Image',
                        secret=1,
                        no_log=1)
    )

#####################################

def createMSFromImage_Parallel(menuitem, msname, image):
    if _rank==0:
        return
    #Already done in imagemenu for process 0
    imagepath = labeltree.makePath(image)
    imagecontext = oofimage.imageContexts[image]
    immidge = imagecontext.getObject().clone(imagepath[-1])
    ms = ooflib.common.microstructure.Microstructure(msname,
                                                   immidge.sizeInPixels(),
                                                   immidge.size())
    newimagecontext = oofimage.imageContexts.add([msname, immidge.name()],
                                                 immidge,
                                                 parent=ooflib.common.microstructure.microStructures[msname])
    ms.addImage(newimagecontext)

imenu.addItem(oofmenu.OOFMenuItem(
    'Create_From_Image_Parallel',
    callback = createMSFromImage_Parallel,
    secret = 1,
    no_log = 1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = parameter.ParameterGroup(
    parameter.AutomaticNameParameter('msname', imagemenu.msImageNameResolver,
                                     automatic.automatic,
                                     tip="Name of the new Microstructure."),
    parameter.StringParameter('image'))
    ))

#####################################

def createImage(msname, imagename, origin=0):
    if _rank == origin:
        image = oofimage.getImage([msname, imagename])
        destinations = range(1,_size)
        oofimage.Send_Image(image, destinations)
    else:
        image = oofimage.Recv_Image(origin)
    return image

def createMSFromImageFile_Parallel(menuitem, msname, imagename):
    # Create image for the rear-end processes.
    image = createImage(msname, imagename)
    # The front-end has nothing to do at this point.
    if _rank == 0:
        return
    
    ms = ooflib.common.microstructure.Microstructure(msname,
                                                   image.sizeInPixels(),
                                                   image.size())
    imagecontext = oofimage.imageContexts.add([ms.name(), image.name()], image,
                                              parent=ooflib.common.microstructure.microStructures[ms.name()])
    ms.addImage(imagecontext)

imenu.addItem(oofmenu.OOFMenuItem(
    'Create_From_Imagefile_Parallel',
    callback = createMSFromImageFile_Parallel,
    secret = 1,
    no_log = 1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = [
    parameter.StringParameter('msname',
                              tip= 'Name of the new Microstructure.'),
    parameter.StringParameter('imagename',
                              tip= 'Name of the new Image.')]
    ))

#####################################

def doImageMod_Parallel(menuitem, image, **params):
    # For the rear-end processes
    global _rank
    if _rank == 0:
        return

    # image is the image name, actually
    imagecontext = oofimage.imageContexts[image]
    imagecontext.reserve()
    try:
        immidge = imagecontext.getObject()  # OOFImage object
        newimmidge = immidge.clone(immidge.name())
        registration = menuitem.data
        imageModifier = registration(**params) # create ImageModifier obj
        imagecontext.begin_writing()
        try:
            imageModifier(newimmidge)   # call its __call__ method on the image
            oofimage.pushModification(image, newimmidge)
        finally:
            imagecontext.end_writing()
    finally:
        imagecontext.cancel_reservation()

#####################################

modmenu = imenu.addItem(
    oofmenu.OOFMenuItem('Modify',
                        secret=1,
                        no_log=1)
    )

# Using the same menu building mechanism as in the serial mode ("imagemenu.py")
# But rather a stripped dwon version.

def buildImageModMenu_Parallel():
    modmenu.clearMenu()
    for registration in imagemodifier.ImageModifier.registry:
        params = [parameter.StringParameter('image')] \
                 + registration.params
        menuitem = modmenu.addItem(
            oofmenu.OOFMenuItem(registration.name(),
                                callback=doImageMod_Parallel,
                                secret = 1,
                                no_log = 1,
                                threadable = oofmenu.PARALLEL_THREADABLE,
                                params=params)
            )
        menuitem.data = registration

switchboard.requestCallback(imagemodifier.ImageModifier,
                            buildImageModMenu_Parallel)
buildImageModMenu_Parallel()

#####################################

## createPixelGroups_Parallel is currently broken, because the
## non-parallel version was modified to have a name_template argument.
## Group names can no longer be inferred simply from the pixel color.
## There will have to be some way of resolving conflicts when two
## processors both want to create 'group6' using different pixel
## colors.

def createPixelGroups_Parallel(menuitem, image, name_template):
    # For the back-end processes
    global _rank
    if _rank == 0:
        return
    # A stripped down version of "createPixelGroups"(imagemenu.py)
    imagecontext = oofimage.imageContexts[image]
    ms = imagecontext.getMicrostructure()
    mscontext = ooflib.common.microstructure.microStructures[ms.name()]
    immidge = imagecontext.getObject()
    pixellistdict = {}
    colornamedict = {}
    newgrps = []
    grpcount = 0

    mscontext.begin_writing()
    try:
        for coord in ms.coords():
            color = immidge[coord]
            # Don't recreate the group name for each pixel -- it's too slow.
            try:
                grpname = colornamedict[color]
            except KeyError:
                grpname = name_template.replace('%c', `color`).\
                          replace('%n', `grpcount`)
                grpcount += 1
                colornamedict[color] = grpname
            # The pixel group is being added.
            (grp, newness) = ms.getGroup(grpname)
            #In single process mode, newgrps is used to remove the groups if the process
            #of auto grouping is interrupted in the GUI.
##            if newness:
##                newgrps.append(grp) #TODO 3.1: The use of newgrps in this parallel version may be incomplete
            try:
                pixellistdict[grp].append(coord)
            except KeyError:
                pixellistdict[grp] = [coord]
                
        for grp, pixellist in pixellistdict.items():
            grp.add(pixellist)

    finally:
        mscontext.end_writing()

imenu.addItem(oofmenu.OOFMenuItem(
    'AutoGroup_Parallel',
    callback = createPixelGroups_Parallel,
    secret=1,
    no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('image'),
            parameter.StringParameter('name_template', value='%c',
                                      tip='Name for the pixel groups. %n is replaced by a number, %c by the pixel color.')
            ]
    ))

#####################################

def undoImageMod_Parallel(menuitem, image):
    global _rank
    if _rank == 0:
        return
    
    # The back-end processes
    who = oofimage.imageContexts[image]
    who.begin_writing()
    oofimage.undoModification(image)
    who.end_writing()

imenu.addItem(oofmenu.OOFMenuItem(
    'Undo',
    callback = undoImageMod_Parallel,
    secret=1,
    no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('image')]
    ))

def redoImageMod_Parallel(menuitem, image):
    global _rank
    if _rank == 0:
        return
    
    # The back-end processes
    who = oofimage.imageContexts[image]
    who.begin_writing()
    oofimage.redoModification(image)
    who.end_writing()
    
imenu.addItem(oofmenu.OOFMenuItem(
    'Redo',
    callback = redoImageMod_Parallel,
    secret=1,
    no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('image')]
    ))
