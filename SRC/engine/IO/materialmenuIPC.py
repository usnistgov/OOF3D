# -*- python -*-
# $RCSfile: materialmenuIPC.py,v $
# $Revision: 1.11.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.common import debug
from ooflib.common import primitives
from ooflib.SWIG.common import switchboard
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import pixelgroupparam
from ooflib.common.IO import socket2me
from ooflib.common.IO import whoville
from ooflib.SWIG.common import mpitools
from ooflib.engine import materialmanager
from ooflib.engine.IO import materialparameter
import ooflib.common.microstructure

_rank = mpitools.Rank()
_size = mpitools.Size()
## OOF.LoadData.IPC.Microstructure
ipcmaterialmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Material', secret=1, no_log=1))


## OOF.LoadData.IPC.Material.New
## Mirrors a newly created material on the back-end

def _parallel_newmaterial(menuitem, name):
    #debug.fmsg()
    ## microstructure is the name of the microstructure
    global _rank
    ## front-end work
    if _rank == 0:
        pass            
    ## back-end part of the work
    else:
        materialmanager.materialmanager.add(name)


ipcmaterialmenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback = _parallel_newmaterial,
    #secret=1, no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('name')]
    ))


## OOF.LoadData.IPC.Material.Delete
## Applies a material destruction request on the back-end
def _parallel_deletematerial(menuitem, name):
    ## microstructure is the name of the microstructure
    global _rank
    ## front-end work
    if _rank == 0:
        pass            
    ## back-end part of the work
    else:
        materialmanager.materialmanager.delete(name)


ipcmaterialmenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback = _parallel_deletematerial,
    #secret=1, no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('name')]
    ))


## OOF.LoadData.IPC.Material.Copy
## Applies a material Copy command on the back-end
def _parallel_copymaterial(menuitem, name, new_name):
    ## microstructure is the name of the microstructure
    global _rank
    ## front-end work
    if _rank == 0:
        pass            
    ## back-end part of the work
    else:
        materialmanager.materialmanager.copy(name, new_name)
        

ipcmaterialmenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback = _parallel_copymaterial,
    #secret=1, no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('name'),
            parameter.StringParameter('new_name')]
    ))


## OOF.LoadData.IPC.Material.Add_property
## Adds a property to a material on the back-end
def _parallel_addprop(menuitem, name, property):
    ## property is assumed to be a string
    ## microstructure is the name of the microstructure
    global _rank
    ## front-end work
    if _rank == 0:
        pass            
    ## back-end part of the work
    else:
        materialmanager.materialmanager.add_prop(name, property)
        switchboard.notify("material changed", name)
        

ipcmaterialmenu.addItem(oofmenu.OOFMenuItem(
    'Add_property',
    callback = _parallel_addprop,
    #secret=1, no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('name'), parameter.StringParameter('property')]
    ))

## OOF.LoadData.IPC.Material.Remove_property
## Adds a property to a material on the back-end
def _parallel_removeprop(menuitem, name, property):
    ## property is assumed to be a string
    ## microstructure is the name of the microstructure
    global _rank
    ## front-end work
    if _rank == 0:
        pass            
    ## back-end part of the work
    else:
        materialmanager.materialmanager.remove_prop(name, property)
        switchboard.notify("material changed", name)
        

ipcmaterialmenu.addItem(oofmenu.OOFMenuItem(
    'Remove_property',
    callback = _parallel_removeprop,
    #secret=1, no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('name'), parameter.StringParameter('property')]
    ))


## OOF.LoadData.IPC.Material.Assign
## Assigns a material to the associated pixels on the back-end
def _parallel_assign(menuitem, material, microstructure, pixels):
    ## property is assumed to be a string
    ## microstructure is the name of the microstructure
    global _rank
    ## front-end work
    if _rank == 0:
        pass            
    ## back-end part of the work
    else:
        import ooflib.engine.IO.materialmenu
        ooflib.engine.IO.materialmenu._assignmat(material, microstructure, pixels)
        

ipcmaterialmenu.addItem(oofmenu.OOFMenuItem(
    'Assign',
    callback = _parallel_assign,
    #secret=1, no_log=1,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[materialparameter.MaterialParameter('material',
                                                tip="Material to be assigned."),
            whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString),
            pixelgroupparam.PixelAggregateParameter('pixels')]))

# Rename an existing material.
def parallel_renamematerial(menuitem, material, name):
    materialmanager.materialmanager.rename(material, name)

ipcmaterialmenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=parallel_renamematerial,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[parameter.StringParameter('material',
                                      tip='Old name of the material.'),
            parameter.StringParameter('name',
                                      tip='New name for the material.')]
    ))
