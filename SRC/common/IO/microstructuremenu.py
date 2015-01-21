# -*- python -*-
# $RCSfile: microstructuremenu.py,v $
# $Revision: 1.72.2.6 $
# $Author: langer $
# $Date: 2014/05/16 20:48:12 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import activearea
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import cmicrostructure
if config.dimension() == 2:
    from ooflib.SWIG.image import oofimage
else:
    from ooflib.SWIG.image import oofimage3d as oofimage
from ooflib.common import enum
from ooflib.common import debug
from ooflib.common import pixelselection
from ooflib.common import parallel_enable
from ooflib.common import primitives
from ooflib.common.IO import automatic
from ooflib.common.IO import datafile
from ooflib.common.IO import filenameparam
from ooflib.common.IO import mainmenu
from ooflib.common.IO import microstructureIO
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.image import imagecontext
import ooflib.common.microstructure
from types import *

if parallel_enable.enabled():
    from ooflib.common.IO import microstructureIPC

micromenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'Microstructure',
    help="Create and manipulate &micro; objects.",
    cli_only=1))
#######################

if config.dimension() == 2:
    sizeparams = parameter.ParameterGroup(
        parameter.FloatParameter('width', 1., tip='Width in physical units.'),
        parameter.FloatParameter('height', 1.,tip='Height in physical units.'),
        parameter.IntParameter('width_in_pixels', 10, tip='Width in pixels.'),
        parameter.IntParameter('height_in_pixels', 10, tip='Height in pixels.'))
    
    
    def newMicrostructure(menuitem, name,
                          width, height,
                          width_in_pixels, height_in_pixels):
        if width<=0 or height<=0 or width_in_pixels<=0 or height_in_pixels<=0:
            raise ooferror.ErrUserError("Negative size values are not allowed.")

        if parallel_enable.enabled():
            # For the rear-end guys
            microstructureIPC.msmenu.New_Parallel(name=name,
                                                 width=width, height=height,
                                                 width_in_pixels=width_in_pixels,
                                                 height_in_pixels=height_in_pixels)

        # Serial mode & #0 in parallel mode
        ms = ooflib.SWIG.common.cmicrostructure.CMicrostructure( 
            name, primitives.iPoint(width_in_pixels,
                                    height_in_pixels),
            primitives.Point(width, height)
            )

elif config.dimension() == 3:

    sizeparams = parameter.ParameterGroup(
        parameter.FloatParameter('width', 1., tip='Width in physical units.'),
        parameter.FloatParameter('height', 1., tip='Height in physical units.'),
        parameter.FloatParameter('depth', 1., tip='Depth in physical units.'),
        parameter.IntParameter('width_in_pixels', 10, tip='Width in pixels.'),
        parameter.IntParameter('height_in_pixels', 10, tip='Height in pixels.'),
        parameter.IntParameter('depth_in_pixels', 10, tip='Depth in pixels.'))

    def newMicrostructure(menuitem, name,
                      width, height, depth,
                      width_in_pixels, height_in_pixels,
                      depth_in_pixels):
        if width<=0 or height<=0 or depth<=0 \
               or width_in_pixels<=0 or height_in_pixels<=0 or depth_in_pixels<=0:
            raise ooferror.ErrUserError("Negative size values are not allowed.")

        if parallel_enable.enabled():
            # For the rear-end guys
            microstructureIPC.msmenu.New_Parallel(name=name,
                                             width=width, height=height, depth=depth,
                                             width_in_pixels=width_in_pixels,
                                             height_in_pixels=height_in_pixels,
                                             depth_in_pixels=depth_in_pixels)

        # Serial mode & #0 in parallel mode
        ms = ooflib.SWIG.common.cmicrostructure.CMicrostructure( 
            name, primitives.iPoint(width_in_pixels,
                                    height_in_pixels,
                                    depth_in_pixels),
            primitives.Point(width, height, depth)
            )


def msNameResolver(param, name):
    if param.automatic():
        nm = 'microstructure'
    else:
        nm = name
    return ooflib.common.microstructure.microStructures.uniqueName(nm)
    
micromenu.addItem(
    oofmenu.OOFMenuItem(
    'New',
    callback=newMicrostructure,
    params=parameter.ParameterGroup(whoville.AutoWhoNameParameter('name', 
                                    resolver=msNameResolver,
                                    value=automatic.automatic,
                                    tip="Name of the new Microstructure.")) \
    + sizeparams,
    help="Create a new Microstructure.",
    discussion="""
    <para>This command creates a new empty &micro; with no associated
    &images;.  To create a &micro; with an &image;, see <xref
    linkend='MenuItem:OOF.Microstructure.Create_From_Image'/> or <xref
    linkend='MenuItem:OOF.Microstructure.Create_From_ImageFile'/>.  To
    add an &image; to an existing &micro;, see <xref
    linkend='MenuItem:OOF.File.Load.Image'/>.</para>"""
    ))

############################

def renameMicrostructure(menuitem, microstructure, name):
    if parallel_enable.enabled():
        microstructureIPC.msmenu.Rename(microstructure=microstructure,name=name)
        return

    ms = ooflib.common.microstructure.microStructures[microstructure]
    ms.reserve()
    try:
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
    finally:
        ms.cancel_reservation()

micromenu.addItem(
    oofmenu.OOFMenuItem('Rename',
                        callback=renameMicrostructure,
                        params=[
    parameter.StringParameter('microstructure', '',
                              tip='Old name for the microstructure.'),
    whoville.WhoNameParameter('name', value='', 
                              tip='New name for the microstructure.')
    ],
                        help="Rename a Microstructure.",
                        discussion="""<para>
                        Change the name of an existing &micro;.
                        </para>"""
                        ))

############################

def copyMicrostructure(menuitem, microstructure, name):
    if parallel_enable.enabled():
        microstructureIPC.msmenu.Copy(microstructure=microstructure,name=name)
        return

    ms = ooflib.common.microstructure.microStructures[microstructure]
    ms.begin_reading()
    grouplist = []
    try:
        sourceMS = ms.getObject()
        newMS = sourceMS.nominalCopy(name)
        newMScontext = ooflib.common.microstructure.microStructures[name]
        # First, copy images and load them to copied MS.
        for imagectxt in sourceMS.getImageContexts():
            sourceimage = imagectxt.getObject()
            immidge = sourceimage.clone(sourceimage.name())
            imagecontext.imageContexts.add(
                [newMS.name(),immidge.name()], immidge,
                parent=newMScontext)
        # Copy pixel groups
        for grpname in sourceMS.groupNames():
            sourcegrp = sourceMS.findGroup(grpname)
            # Ignore "newness", all groups will be new.
            (newgrp, newness) = newMS.getGroup(grpname)
            newgrp.addGroup(sourcegrp)
            newgrp.set_meshable(sourcegrp.is_meshable())
            grouplist.append(newgrp)
    finally:
        ms.end_reading()
        
    for g in grouplist:
        switchboard.notify("new pixel group", g)

micromenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=copyMicrostructure,
    params=[parameter.StringParameter('microstructure', '',
                                      tip='The source microstructure.'),    
            parameter.AutomaticNameParameter('name', 
                                             resolver=msNameResolver,
                                             value=automatic.automatic,
                                         tip="Name of the new Microstructure.")
            ],
    help="Copy a Microstructure.",
    discussion=
    """<para>A copied &micro; has the same physical size and pixel
    size as the original &micro;, and includes
    <emphasis>copies</emphasis> of all &images; and <link
    linkend='Section:Concepts:Microstructure:Pixel_Group'>pixel
    groups</link> contained in the original.  It does
    <emphasis>not</emphasis> include any &skels; or &meshes; from the
    original.</para>"""
    ))

#############################

def deleteMicrostructure(menuitem, microstructure):
    if parallel_enable.enabled():
        microstructureIPC.msmenu.Delete(microstructure=microstructure)
    else:
        mscontext = ooflib.common.microstructure.microStructures[microstructure]
        mscontext.lockAndDelete()

micromenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=deleteMicrostructure,
    params=[
    parameter.StringParameter('microstructure', '',
                              tip='Name of the microstructure to be deleted.')],
    help="Destroy a Microstructure.",
    discussion=
    """<para>Delete a &micro; and all of its associated &images;,
    &skels;, and &meshes;.  Be really sure that you want to do this
    before you do it. </para>"""
    ))


#########################

def saveMicrostructure(menuitem, filename, mode, format, microstructure):
    ms = ooflib.common.microstructure.microStructures[microstructure]
    dfile = datafile.writeDataFile(filename, mode.string(), format)
    microstructureIO.writeMicrostructure(dfile, ms)
    dfile.close()

mainmenu.OOF.File.Save.addItem(oofmenu.OOFMenuItem(
    'Microstructure',
    callback=saveMicrostructure,
    ordering=30,
    params=[
    filenameparam.WriteFileNameParameter('filename', tip="Name of the file."),
    filenameparam.WriteModeParameter('mode', tip="write or append?"),
    enum.EnumParameter('format', datafile.DataFileFormat, datafile.ASCII,
                       tip="File format."),
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString)],
    help="Save a Microstructure in a file.",
    discussion="""
    <para>Store a &micro; in a file in one of several <link
    linkend='Section:Concepts:FileFormats'><varname>formats</varname></link>.
    The file can be reloaded by <xref
    linkend='MenuItem:OOF.File.Load.Script'/> or <xref
    linkend='MenuItem:OOF.File.Load.Data'/>, depending on the file
    format.</para>
    """
   ))

def _fixmenu(*args):
    import sys
    if ooflib.common.microstructure.microStructures.nActual() == 0:
        mainmenu.OOF.File.Save.Microstructure.disable()
    else:
        mainmenu.OOF.File.Save.Microstructure.enable()
_fixmenu()
    
switchboard.requestCallback(('new who', 'Microstructure'), _fixmenu)
switchboard.requestCallback(('remove who', 'Microstructure'), _fixmenu)
