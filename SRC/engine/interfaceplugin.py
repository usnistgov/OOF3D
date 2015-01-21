# -*- python -*-
# $RCSfile: interfaceplugin.py,v $
# $Revision: 1.25.2.5 $
# $Author: langer $
# $Date: 2014/09/17 17:47:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import material
from ooflib.common import labeltree
from ooflib.common import microstructure
from ooflib.common import registeredclass
from ooflib.common import runtimeflags
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import microstructureIO
from ooflib.common.IO import pixelgroupparam
from ooflib.engine import bdycondition
from ooflib.engine import materialmanager
from ooflib.engine import skeletoncontext
from ooflib.engine import skeletonelement
from ooflib.engine import subproblemcontext
from ooflib.engine.IO import interfaceparameters
from ooflib.engine.IO import materialmenu
from ooflib.engine.IO import materialparameter
import ooflib.engine.mesh

import sys

NO_MATERIAL=interfaceparameters.NO_MATERIAL_STR
NO_PIXELGROUP=interfaceparameters.NO_PIXELGROUP_STR
NORTH=interfaceparameters.NORTH_STR
SOUTH=interfaceparameters.SOUTH_STR
EAST=interfaceparameters.EAST_STR
WEST=interfaceparameters.WEST_STR
ANY=interfaceparameters.ANY_STR

# Return type for getAdjacentElements -- not very complicated, but
# nomenclature was a pretty big stumbling block to getting the
# interfaces right, so we're being extra-careful. Left and right are
# the elements whose materials correspond to the left-material and
# right-material (or pixel group, etc.) of the interface.
class AdjacentElements:
    def __init__(self,left=None,right=None):
        self.left = left
        self.right = right
    def __nonzero__(self):
        # If either element is not None, then we're "true".  Can't do
        # the obvious "return self.left or self.right", because this
        # can be None, but the allowed return values are True, False,
        # 0, or 1.
        if self.left or self.right:
            return True
        return False


#Region outside of mesh divided into four
#virtual materials or pixelgroups:
#
#         <North>
#         -------
#        |       |
# <West> |       | <East>
#        |       |
#         -------
#         <South>
#
# North commences the bidding....


# For some reason, just declining to register the plug-in doesn't
# remove references to MATERIALTYPE_INTERFACE.  So, we null it out
# here.  This egregious hackery will be removed once the surface stuff
# is working, and then removed even more when we migrate to 3D.
interface_mat_type = None
if runtimeflags.surface_mode:
    interface_mat_type = material.MATERIALTYPE_INTERFACE


OOF = mainmenu.OOF

class InterfaceMSPlugIn(microstructure.MicrostructurePlugIn):
    def __init__(self, ms):
        microstructure.MicrostructurePlugIn.__init__(self, ms)
        self.namedinterfaces=utils.OrderedDict()
        self._materialassignments={}
        self._selectedInterfaceName=None

        self.sbcallbacks = [
##            switchboard.requestCallback("materials changed in microstructure",
##                                        self.matChanged),
##            switchboard.requestCallback('destroy pixel group',
##                                        self.destpixgrp),
##            switchboard.requestCallback('changed pixel group', self.changedpixgrp)
            #TODO 3.1: Figure this out?
            #switchboard.requestCallback('changed pixel groups', self.chngdgrps)
            ]

        #TODO MER: Somehow use a timestamp in the mesh for interfaces (see mesh.py)

## I don't know what parts of this are actually used. The switchboard
## requests above were commented out, so I commented out their
## callbacks too.  I didn't follow through to find out which of the
## other methods are only called by the callbacks, nor do I know why
## the requests are commented out.  (SAL, July 9, 2009)

#     #This is a response to an (un)assignment of a material to a microstructure
#     def matChanged(self, msobj):
#         # switchboard "materials changed ..."
#         #TODO 3.1: Make this more specific (like check if the material
#         #that was assigned or unassigned is part of an interface
#         #definition...)  Would this clash with the other "materials
#         #changed..." handlers?
#         if msobj==self.microstructure:
#             if len(self.namedinterfaces)>0:
#                 #A rebuild is not trigggered by changes in the
#                 #skeleton boundaries
#                 self.rebuildMeshes()

#     def destpixgrp(self, group, ms_name):
#         # switchboard 'destroy pixel group'
#         self.deleteGroup(ms_name,group)

#     #Reaction to "changed pixel group" similar to "materials changed
#     #in microstructure"
#     def changedpixgrp(self, group, ms_name):
#         #Check if group is in the definition of one or more interfaces?
#         if ms_name==self.microstructure.name():
#             self.matChanged(self.microstructure)

#     def deleteGroup(self,ms_name,group):
#         if ms_name!=self.microstructure.name():
#             return
#         if len(self.namedinterfaces)==0:
#             return
#         interfacenames=self.getInterfaceNames()
#         doomedinterfaces=[]
#         for interfacename in interfacenames:
#             interfaceobj=self.namedinterfaces[interfacename]
#             if interfaceobj.hasGroup(group.name()):
#                 del self.namedinterfaces[interfacename]
#                 doomedinterfaces.append(interfacename)
#         self.removeMaterialFromInterfaces(doomedinterfaces)
#         #Remove boundary conditions that refer to the doomedinterfaces
#         meshclass=ooflib.engine.mesh.meshes
#         msname=self.microstructure.name()
#         for meshkey in meshclass.keys(base=msname):
#             meshctxt=meshclass[[msname]+meshkey]
#             for doomedinterfacename in doomedinterfaces:
#                 meshctxt.removeInterface(doomedinterfacename)
#         self.rebuildMeshes()
#         switchboard.notify("interface removed",self.microstructure)

    def renameGroup(self,oldgroupname,newgroupname):
        for interfaceobj in self.namedinterfaces.values():
            interfaceobj.renameGroup(oldgroupname,newgroupname)
        #A group has been renamed, it is possible the details of
        #one or more interfaces have been changed. 
        switchboard.notify("interface renamed",self.microstructure)

    def destroy(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        microstructure.MicrostructurePlugIn.destroy(self)

    def interfaceInfo(self,interfacename):
        try:
            return self.namedinterfaces[interfacename].__repr__()
        except KeyError:
            return ""

    def getInterfaceNames(self):
        return self.namedinterfaces.keys()[:]

    #Returns strings of the form "skeleton:bdkey"
    def getSkelBdyNames(self):
        msname=self.microstructure.name()
        skelclass=skeletoncontext.skeletonContexts
        names=[]
        for skelkey in skelclass.keys(base=msname):
            skelctxt=skelclass[[msname]+skelkey]
            for bname in skelctxt.allEdgeBoundaryNames():
                names.append(skelkey[0]+":"+bname)
        return names

    #Return skeleton boundary names in skeleton skelname
    def getOneSkelBdyNames(self,skelname):
        msname=self.microstructure.name()
        skelclass=skeletoncontext.skeletonContexts
        names=[]
        for skelkey in skelclass.keys(base=msname):
            if skelkey[0]!=skelname:
                continue
            skelctxt=skelclass[[msname]+skelkey]
            for bname in skelctxt.allEdgeBoundaryNames():
                names.append(bname)
        return names

    #Return skeleton boundary names common to all skeletons
    def getCommonSkelBdyNames(self):
        msname=self.microstructure.name()
        skelclass=skeletoncontext.skeletonContexts
        namedict={}
        numskels=len(skelclass.keys(base=msname))
        for skelkey in skelclass.keys(base=msname):
            skelctxt=skelclass[[msname]+skelkey]
            for bname in skelctxt.allEdgeBoundaryNames():
                try:
                    namedict[bname]=namedict[bname]+1
                except KeyError:
                    namedict[bname]=1
        names=[]
        for bname,count in namedict.items():
            if count==numskels:
                names.append(bname)
        return names

    def getInterfaceNamesWithMaterial(self,matname):
        try:
            names=self._materialassignments[matname][:]
            return names
        except KeyError:
            return []

    def getSkelBdyNamesWithMaterial(self,matname):
        msname=self.microstructure.name()
        skelclass=skeletoncontext.skeletonContexts
        names=[]
        for skelkey in skelclass.keys(base=msname):
            skelctxt=skelclass[[msname]+skelkey]
            for bname in skelctxt.allEdgeBoundaryNames():
                bdyctxt=skelctxt.getBoundary(bname)
                if bdyctxt._interfacematerial==matname:
                    names.append(skelkey[0]+":"+bname)
        return names

    #Get material assigned to interfacename
    def getInterfaceMaterialName(self,interfacename):
        for matname, interfacenamelist in self._materialassignments.items():
            if interfacename in interfacenamelist:
                return matname
        return None

    #This method returns materials assigned to interfaces and boundaries.
    #In contrast, materialmanager.getInterfaceMaterialNames returns
    #all interface materials listed on the Materials page.
    def getInterfaceMaterials(self):
        matdict={}
        for matname, interfacenames in self._materialassignments.items():
            if len(interfacenames)>0:
                matdict[matname]=1
        msname=self.microstructure.name()
        skelclass=skeletoncontext.skeletonContexts
        for skelkey in skelclass.keys(base=msname):
            skelctxt=skelclass[[msname]+skelkey]
            for bname in skelctxt.allEdgeBoundaryNames():
                bdyctxt=skelctxt.getBoundary(bname)
                if bdyctxt._interfacematerial is not None:
                    matdict[bdyctxt._interfacematerial]=1
        return matdict.keys()

    def addInterface(self,name,interfacedef):
        self.namedinterfaces[name]=interfacedef
        switchboard.notify("new interface created",self.microstructure)
        self.selectInterface(name)
        self.rebuildMeshes()

    def removeInterface(self,name):
        try:
            del self.namedinterfaces[name]
            interfacenames=self.getInterfaceNames()
            doomedinterfaces=[name]
            #Because of the possibility of compound interfaces (e.g. union),
            #we must search the other interfaces for the presence
            #of the interface corresponding to name.
            for interfacename in interfacenames:
                interfaceobj=self.namedinterfaces[interfacename]
                if interfaceobj.hasInterface(name):
                    del self.namedinterfaces[interfacename]
                    doomedinterfaces.append(interfacename)
            self.removeMaterialFromInterfaces(doomedinterfaces)
            self.unselectInterface()
            # #Remove boundary conditions that refer to the doomedinterfaces
            # meshclass=ooflib.engine.mesh.meshes
            # msname=self.microstructure.name()
            # for meshkey in meshclass.keys(base=msname):
            #     meshctxt=meshclass[[msname]+meshkey]
            #     for doomedinterfacename in doomedinterfaces:
            #         meshctxt.removeInterface(doomedinterfacename)
            self.rebuildMeshes()
            switchboard.notify("interface removed",self.microstructure)
        except KeyError:
            pass

    def getCurrentReservedNames(self):
        reservednamedict={}
        for iname in self.getInterfaceNames():
            reservednamedict[iname]=1
        skelclass=skeletoncontext.skeletonContexts
        msname=self.microstructure.name()
        for skelkey in skelclass.keys(base=msname):
            skelctxt=skelclass[[msname]+skelkey]
            for bname in skelctxt.allBoundaryNames():
                reservednamedict[bname]=1
        reservednamedict['top']=1
        reservednamedict['bottom']=1
        reservednamedict['left']=1
        reservednamedict['right']=1
        reservednamedict['topleft']=1
        reservednamedict['topright']=1
        reservednamedict['bottomleft']=1
        reservednamedict['bottomright']=1
        return reservednamedict.keys()

    def renameInterface(self,oldname,newname):
        if oldname==newname:
            return
        if newname in self.getCurrentReservedNames():
            raise ooferror.ErrSetupError("Name %s already in use." % newname)
        try:
            obj=self.namedinterfaces[oldname]
            del self.namedinterfaces[oldname]
            self.namedinterfaces[newname]=obj
            interfacenames=self.getInterfaceNames()
            #Because of the possibility of compound interfaces (e.g. union),
            #we must search the other interfaces for the presence
            #of the interface corresponding to oldname.
            for interfacename in interfacenames:
                interfaceobj=self.namedinterfaces[interfacename]
                interfaceobj.renameInterface(oldname,newname)
            #interface must also be renamed in the list of
            #material assignments
            matname=self.getInterfaceMaterialName(oldname)
            self.removeMaterialFromInterfaces([oldname])
            self.assignMaterialToInterfaces(matname,[newname])
            #Rename the interface in the boundary conditions
            #and in the edgements.
            meshclass=ooflib.engine.mesh.meshes
            msname=self.microstructure.name()
            for meshkey in meshclass.keys(base=msname):
                meshctxt=meshclass[[msname]+meshkey]
                meshctxt.renameInterface(oldname,newname)
            self.selectInterface(newname)
            switchboard.notify("interface renamed",self.microstructure)
        except KeyError:
            pass

    #Assign material (matname) to interfaces and boundaries in the list interfacenames
    def assignMaterialToInterfaces(self,matname,interfacenames,skeletonname=None):
        
        #Extract the skeleton boundary names from interfacenames.
        #The skeleton boundaries are not listed in _materialassignments.
        #The interfacematerial is an attribute of the
        #skeleton context edge boundary. This way,
        #we do not have to explicitly handle changes in the
        #names of skeletons and skeleton boundaries.
        msname=self.microstructure.name()
        skelclass=skeletoncontext.skeletonContexts
        skelbdynamesdict={}
        for skelkey in skelclass.keys(base=msname):
            if skeletonname!=interfaceparameters.SkelAllParameter.extranames[0] and \
                   skeletonname!=skelkey[0]:
                continue
            skelctxt=skelclass[[msname]+skelkey]
            for bname in skelctxt.allEdgeBoundaryNames():
                if bname in interfacenames:
                    skelbdynamesdict[bname]=1
                    bdyctxt=skelctxt.getBoundary(bname)
                    bdyctxt._interfacematerial=matname

        #Remove skeleton boundary names from interfacenames
        for bname in skelbdynamesdict:
            interfacenames.remove(bname)

        #First unassign interfacenames from any material
        self.removeMaterialFromInterfaces(interfacenames,skeletonname)
        try:
            interfacenamelist=self._materialassignments[matname]
            #After the call to removeMaterialFromInterfaces above,
            #there should be no duplicates in the sum on the right hand side
            self._materialassignments[matname]=interfacenamelist+interfacenames
        except KeyError:
            self._materialassignments[matname]=interfacenames[:]

##        print "assignments to interfaces", self._materialassignments
##        print "all assigned materials", self.getInterfaceMaterials()
        
    #Remove the interfaces indicated in interfacenames from their material
    #assignments
    def removeMaterialFromInterfaces(self,interfacenames,skeletonname=None):
        #The skeleton boundaries are not listed in _materialassignments.
        #The interfacematerial is an attribute of the
        #skeleton context edge boundary. This way,
        #we do not have to explicitly handle changes in the
        #names of skeletons and skeleton boundaries.
        msname=self.microstructure.name()
        skelclass=skeletoncontext.skeletonContexts
        for skelkey in skelclass.keys(base=msname):
            if skeletonname!=interfaceparameters.SkelAllParameter.extranames[0] and \
                   skeletonname!=skelkey[0]:
                continue
            skelctxt=skelclass[[msname]+skelkey]
            for bname in skelctxt.allEdgeBoundaryNames():
                if bname in interfacenames:
                    bdyctxt=skelctxt.getBoundary(bname)
                    bdyctxt._interfacematerial=None

        for matname, interfacenamelist in self._materialassignments.items():
            for interfacename in interfacenames:
                if interfacename in interfacenamelist:
                    interfacenamelist.remove(interfacename)
        
    #Implement changes to the interfaces when a material is deleted
    #in the materials page. If the material is an interface material,
    #remove entry for this material in _materialassignments.
    #If the material is a bulk material, interfaces that have this
    #material as an attribute are removed.
    #TODO 3.1: For a union of interfaces, not necessary to delete the whole
    #union.
    def deleteMaterial(self,matname,material_type):
        # if material_type==material.MATERIALTYPE_INTERFACE:
        if material_type == interface_mat_type:
            try:
                del self._materialassignments[matname]
            except KeyError:
                pass
            #Unassociate matname from skeleton boundaries
            msname=self.microstructure.name()
            skelclass=skeletoncontext.skeletonContexts
            for skelkey in skelclass.keys(base=msname):
                skelctxt=skelclass[[msname]+skelkey]
                for bname in skelctxt.allEdgeBoundaryNames():
                    bdyctxt=skelctxt.getBoundary(bname)
                    if bdyctxt._interfacematerial==matname:
                        bdyctxt._interfacematerial=None
        else:
            if len(self.namedinterfaces)==0:
                return
            interfacenames=self.getInterfaceNames()
            doomedinterfaces=[]
            for interfacename in interfacenames:
                interfaceobj=self.namedinterfaces[interfacename]
                if interfaceobj.hasBulkMaterial(matname):
                    del self.namedinterfaces[interfacename]
                    doomedinterfaces.append(interfacename)
            self.removeMaterialFromInterfaces(doomedinterfaces)
            #Remove boundary conditions that refer to the doomedinterfaces
            meshclass=ooflib.engine.mesh.meshes
            msname=self.microstructure.name()
            for meshkey in meshclass.keys(base=msname):
                meshctxt=meshclass[[msname]+meshkey]
                for doomedinterfacename in doomedinterfaces:
                    meshctxt.removeInterface(doomedinterfacename)
            self.rebuildMeshes()
            switchboard.notify("interface removed",self.microstructure)

    def renameMaterial(self,oldmatname,newmatname,material_type):
        # if material_type==material.MATERIALTYPE_INTERFACE:
        if material_type==interface_mat_type:
            try:
                interfacenamelist=self._materialassignments[oldmatname]
                del self._materialassignments[oldmatname]
                self._materialassignments[newmatname]=interfacenamelist
            except KeyError:
                pass
            #Rename materials associated with skeleton boundaries
            msname=self.microstructure.name()
            skelclass=skeletoncontext.skeletonContexts
            for skelkey in skelclass.keys(base=msname):
                skelctxt=skelclass[[msname]+skelkey]
                for bname in skelctxt.allEdgeBoundaryNames():
                    bdyctxt=skelctxt.getBoundary(bname)
                    if bdyctxt._interfacematerial==oldmatname:
                        bdyctxt._interfacematerial=newmatname
        else:
            for interfaceobj in self.namedinterfaces.values():
                interfaceobj.renameBulkMaterial(oldmatname,newmatname)
            #A material has been renamed, it is possible the details of
            #one or more interfaces have been changed. 
            switchboard.notify("interface renamed",self.microstructure)

    # The selected interface isn't actually used for anything directly,
    # but it's displayed in the GUI and its name is passed in as an
    # argument to commands that operate on interfaces.  
    def selectInterface(self, interfacename):
        self._selectedInterfaceName = interfacename
        #self.bdyselected.increment()    # timestamp
        switchboard.notify("interface selected",
                           self.microstructure, #ms object (microstructure.py)
                           interfacename)
        #switchboard.notify('redraw')
    def unselectInterface(self):
        if self._selectedInterfaceName is not None:
            self._selectedInterfaceName = None
            #self.bdyselected.increment()
            switchboard.notify("interface unselected",
                               self.microstructure)
            #switchboard.notify('redraw')
    def getSelectedInterfaceName(self):
        return self._selectedInterfaceName
    def getSelectedInterface(self):      # returns Interface object
        if self._selectedInterfaceName is not None:
            return self.namedinterfaces[self._selectedInterfaceName]

    #Cases when we want to rebuild the mesh:
    #(1) Interfaces added or removed
    #(2) Bulk materials get deleted
    #(3) Bulk materials get assigned to pixels
    #(4) Renaming an interface material might also trigger a rebuild(?)
    #(5) Pixel groups get destroyed or changed.
    def rebuildMeshes(self):
        meshclass = ooflib.engine.mesh.meshes
        msname = self.microstructure.name()
        for meshkey in meshclass.keys(base=msname):
            mesh = meshclass[[msname] + meshkey]
            mesh.begin_writing()
            try:
                mesh.interfacesChanged() # marks mesh as OutOfSync
            finally:
                mesh.end_writing()

microstructure.registerMicrostructurePlugIn(InterfaceMSPlugIn, "Interfaces")

#######################################################
#Interface definitions.  All interfaces are subclasses of InterfaceDef. 

class InterfaceDef(registeredclass.RegisteredClass):
    registry = []
    tip = "Tools to define interfaces."
    discussion = """<para>
    <classname>InterfaceDef</classname> objects are used by the
    <xref linkend='MenuItem-OOF.Microstructure.Interface.New'/> command
    to define interfaces in a &micro;.
    </para>"""
    def addToMS(self,interfacemsplugin,interfacename):
        interfacemsplugin.addInterface(interfacename,self)
    def check(self):
        pass
    def hasBulkMaterial(self,bulkmatname):
        return 0
    def renameBulkMaterial(self,oldname,newname):
        return 0
    # hasGroup and renameGroup are isomorphic to hasBulkMaterial and
    # renameBulkMaterial.  A generic function may be defined that does
    # hasGroup and hasBulkMaterial, for example, but I'll leave the
    # distinction here.
    def hasGroup(self,groupname):
        return 0
    def renameGroup(self,oldname,newname):
        return 0
    def hasInterface(self,interfacename):
##        if interfaceobj==self:
##            return 1
        return 0
    def renameInterface(self,oldname,newname):
        pass

class MaterialInterface(InterfaceDef):
    def __init__(self,left,right):
        #members must be spelled the same as the parameters
        self.left=left
        self.right=right
    def check(self):
        if self.left==self.right:
            return 'The two sides must have different materials!'
    #RegisteredClass already has a __repr__
##    def info(self):
##        return "Between Bulk Materials (%s,%s)" % (self.left,self.right)
    #Useful function for finding out if the pair of bulk materials
    #already has an interface material assigned to it.
##    def __eq__(self,other):
##        if self.__class__!=other.__class__:
##            return 0
##        return ((self._mat1==other._mat1 and \
##                 self._mat2==other._mat2) or
##                (self._mat1==other._mat2 and
##                 self._mat2==other._mat1))
    # This function is used by the mesh construction function to test
    # whether a skeleton segment is part of the interface.  For
    # segments which are parts of interfaces, it should return the
    # left and right elements.  One or the other of these may be null,
    # but they should reflect the correct local geometry in any case.
    def getAdjacentElements(self,seg,skelctxt):
        els = seg.getElements()
        if len(els) > 1:
            mat0 = els[0].material(skelctxt)
            mat1 = els[1].material(skelctxt)
            if mat0==mat1: #Optional, if check() is used.
                return AdjacentElements()

            mat0name=NO_MATERIAL
            if mat0:
                mat0name=mat0.name()
            mat1name=NO_MATERIAL
            if mat1:
                mat1name=mat1.name()

            if self.left==mat0name and self.right==mat1name:
                return AdjacentElements(els[0],els[1])
            if self.right==mat0name and self.left==mat1name:
                return AdjacentElements(els[1],els[0])
            if self.left==ANY:
                if self.right==mat0name:
                    return AdjacentElements(els[1],els[0])
                if self.right==mat1name:
                    return AdjacentElements(els[0],els[1])
            if self.right==ANY:
                if self.left==mat0name:
                    return AdjacentElements(els[0],els[1])
                if self.left==mat1name:
                    return AdjacentElements(els[1],els[0])
        else:
            # Only one element in the segment's element list -- we are
            # on the boundary.  We still might have a positive response.
            n0=seg.get_nodes()[0].position()
            n1=seg.get_nodes()[1].position()
            xmax=skelctxt.getMicrostructure().size().x
            ymax=skelctxt.getMicrostructure().size().y
            if n0.y==ymax and n1.y==ymax:
                compass=NORTH #golden
            elif n0.y==0.0 and n1.y==0.0:
                compass=SOUTH
            elif n0.x==xmax and n1.x==xmax:
                compass=EAST
            #elif n0.x==0.0 and n1.x==0.0:
            else:
                compass=WEST
            #
            matname=NO_MATERIAL
            mat = els[0].material(skelctxt)
            if mat:
                matname=mat.name()
            if (self.left==matname or self.left==ANY) \
                   and self.right==compass:
                return AdjacentElements(els[0],None)
            elif self.left==compass and \
                 (self.right==matname or self.right==ANY):
                return AdjacentElements(None,els[0])
        return AdjacentElements()
    def hasBulkMaterial(self,bulkmatname):
        if self.left==bulkmatname or self.right==bulkmatname:
            return 1
        return 0
    def renameBulkMaterial(self,oldname,newname):
        numrenamed=0
        if self.left==oldname:
            self.left=newname
            numrenamed+=1
        if self.right==oldname:
            self.right=newname
            numrenamed+=1
        return 0

registeredclass.Registration(
    "Between Bulk Materials",
    InterfaceDef,
    MaterialInterface,
    ordering=10,
    params = [
    materialparameter.BulkMaterialParameterExtra('left',
                                                 tip="Bulk Material."),
    materialparameter.BulkMaterialParameterExtra('right',
                                                 tip="Bulk Material.")
    ],
    tip="Define an interface between elements with different bulk materials.",
    discussion = """<para>

    The object constructed from this class represents an interface between
    two different bulk materials.

    </para>"""
    )

class SingleMaterialInterface(InterfaceDef):
    def __init__(self,left):
        self.left=left
    def check(self):
        if self.left==ANY:
            return 'Not a valid input!'
    #This function is used by the mesh construction function to test
    #whether a skeleton segment is part of the interface.
    def getAdjacentElements(self,seg,skelctxt):
        els = seg.getElements()
        if len(els) > 1:
            mat1 = els[0].material(skelctxt)
            mat2 = els[1].material(skelctxt)
            if mat1==mat2:
                return (0,None)
            if self.left==NO_MATERIAL:
                if (mat1 is None):
                    return AdjacentElements(els[0],els[1])
                if (mat2 is None):
                    return AdjacentElements(els[1],els[0])
            if (mat1 and self.left==mat1.name()):
                return AdjacentElements(els[0],els[1])
            if (mat2 and self.left==mat2.name()):
                return AdjacentElements(els[1],els[0])
        else:
            if self.left==NORTH:
                n0=seg.get_nodes()[0].position()
                n1=seg.get_nodes()[1].position()
                ymax=skelctxt.getMicrostructure().size().y
                if n0.y==ymax and n1.y==ymax:
                    return AdjacentElements(None,els[0])
                else:
                    return AdjacentElements()
            if self.left==SOUTH:
                n0=seg.get_nodes()[0].position()
                n1=seg.get_nodes()[1].position()
                if n0.y==0.0 and n1.y==0.0:
                    return AdjacentElements(None,els[0])
                else:
                    return AdjacentElements()
            if self.left==EAST:
                n0=seg.get_nodes()[0].position()
                n1=seg.get_nodes()[1].position()
                xmax=skelctxt.getMicrostructure().size().x
                if n0.x==xmax and n1.x==xmax:
                    return AdjacentElements(None,els[0])
                else:
                    return AdjacentElements()
            if self.left==WEST:
                n0=seg.get_nodes()[0].position()
                n1=seg.get_nodes()[1].position()
                if n0.x==0.0 and n1.x==0.0:
                    return AdjacentElements(None,els[0])
                else:
                    return AdjacentElements()
            mat = els[0].material(skelctxt)
            if mat:
                if self.left==mat.name():
                    return AdjacentElements(els[0],None)
        # Default...
        return InterfaceMaterial()
    def hasBulkMaterial(self,bulkmatname):
        if self.left==bulkmatname:
            return 1
        return 0
    def renameBulkMaterial(self,oldname,newname):
        if self.left==oldname:
            self.left=newname
            return 1
        return 0

registeredclass.Registration(
    "Around a Single Material",
    InterfaceDef,
    SingleMaterialInterface,
    ordering=15,
    params = [
    materialparameter.BulkMaterialParameterExtra('left',
                                                 tip="Bulk Material.")
    ],
    tip="Define an interface around elements with a given bulk material.",
    discussion = """<para>

    The object constructed from this class represents an interface between
    the specified bulk material and any other bulk material (or no material).

    </para>"""
    )

class PixelGroupInterface(InterfaceDef):
    def __init__(self,left,right):
        self.left=left
        self.right=right
    def check(self):
        if self.left==self.right:
            return 'The two sides must have different pixel groups!'
    #This function is used by the mesh construction function to test
    #whether a skeleton segment is part of the interface.
    def getAdjacentElements(self,seg,skelctxt):
        els = seg.getElements()
        if len(els) > 1:
            msobj=skelctxt.getMicrostructure()
            where = msobj.getRepresentativePixel(
                els[0].dominantPixel(msobj))
            grpnames1 = pixelgroup.pixelGroupNames(msobj, where)
            where = msobj.getRepresentativePixel(
                els[1].dominantPixel(msobj))
            grpnames2 = pixelgroup.pixelGroupNames(msobj, where)
            if self.left!=NO_PIXELGROUP and \
                    self.right!=NO_PIXELGROUP:
                if (self.left in grpnames1 and \
                        self.right in grpnames2):
                    return AdjacentElements(els[0],els[1])
                if (self.left in grpnames2 and \
                        self.right in grpnames1):
                    return AdjacentElements(els[1],els[0])
            elif self.left!=NO_PIXELGROUP:
                if (self.left in grpnames1 and \
                        len(grpnames2)==0):
                    return AdjacentElements(els[0],els[1])
                if (self.left in grpnames2 and \
                        len(grpnames1)==0):
                    return AdjacentElements(els[1],els[0])
            elif self.right!=NO_PIXELGROUP:
                if (self.right in grpnames1 and \
                        len(grpnames2)==0):
                    return AdjacentElements(els[1],els[0])
                if (self.right in grpnames2 and \
                        len(grpnames1)==0):
                    return AdjacentElements(els[0],els[1])
        else:
            #Determine on which external boundary the segment lies
            n0=seg.get_nodes()[0].position()
            n1=seg.get_nodes()[1].position()
            xmax=skelctxt.getMicrostructure().size().x
            ymax=skelctxt.getMicrostructure().size().y
            if n0.y==ymax and n1.y==ymax:
                compass=NORTH #golden
            elif n0.y==0.0 and n1.y==0.0:
                compass=SOUTH
            elif n0.x==xmax and n1.x==xmax:
                compass=EAST
            #elif n0.x==0.0 and n1.x==0.0:
            else:
                compass=WEST
            #
            msobj=skelctxt.getMicrostructure()
            where = msobj.getRepresentativePixel(
                els[0].dominantPixel(msobj))
            grpnames = pixelgroup.pixelGroupNames(msobj, where)
            if self.left==compass and \
                   ((self.right in grpnames) or self.right==ANY):
                return AdjacentElements(None,els[0])
            if self.right==compass and \
                   ((self.left in grpnames) or self.left==ANY):
                return AdjacentElements(els[0],None)
        return AdjacentElements()

    def hasGroup(self,groupname):
        if self.left==groupname or self.right==groupname:
            return 1
        return 0
    def renameGroup(self,oldname,newname):
        if self.left==oldname:
            self.left=newname
            return 1
        if self.right==oldname:
            self.right=newname
            return 1
        return 0

registeredclass.Registration(
    "Between Pixel Groups",
    InterfaceDef,
    PixelGroupInterface,
    ordering=20,
    params = [
    pixelgroupparam.PixelGroupInterfaceParameter('left',
                                                 tip="Pixels."),
    pixelgroupparam.PixelGroupInterfaceParameter('right',
                                                 tip="Pixels.")
    ],
    tip="Define an interface between elements with different pixel groups.",
    discussion = """<para>

    The object constructed from this class represents an interface between
    two different pixel groups.

    </para>"""
    )

class SinglePixelGroupInterface(InterfaceDef):
    def __init__(self,left):
        self.left=left
    def check(self):
        if self.left==ANY:
            return 'Not a valid input!'
    #This function is used by the mesh construction function to test
    #whether a skeleton segment is part of the interface.
    def getAdjacentElements(self,seg,skelctxt):
        els = seg.getElements()
        if len(els) > 1:
            msobj=skelctxt.getMicrostructure()
            where = msobj.getRepresentativePixel(
                els[0].dominantPixel(msobj))
            grpnames1 = pixelgroup.pixelGroupNames(msobj, where)
            where = msobj.getRepresentativePixel(
                els[1].dominantPixel(msobj))
            grpnames2 = pixelgroup.pixelGroupNames(msobj, where)
            if self.left!=NO_PIXELGROUP:
                if (self.left in grpnames1 and \
                    self.left not in grpnames2):
                    return AdjacentElements(els[0],els[1])
                if (self.left in grpnames2 and \
                    self.left not in grpnames1):
                    return AdjacentElements(els[1],els[0])
            else:
                if (len(grpnames1)>0 and len(grpnames2)==0):
                    return AdjacentElements(els[1],els[0])
                if (len(grpnames2)>0 and len(grpnames1)==0):
                    return AdjacentElements(els[0],els[1])
        else:
            if self.left==NORTH:
                n0=seg.get_nodes()[0].position()
                n1=seg.get_nodes()[1].position()
                ymax=skelctxt.getMicrostructure().size().y
                if n0.y==ymax and n1.y==ymax:
                    return AdjacentElements(None,els[0])
                else:
                    return AdjacentElements()
            if self.left==SOUTH:
                n0=seg.get_nodes()[0].position()
                n1=seg.get_nodes()[1].position()
                if n0.y==0.0 and n1.y==0.0:
                    return AdjacentElements(None,els[0])
                else:
                    return AdjacentElements()
            if self.left==EAST:
                n0=seg.get_nodes()[0].position()
                n1=seg.get_nodes()[1].position()
                xmax=skelctxt.getMicrostructure().size().x
                if n0.x==xmax and n1.x==xmax:
                    return AdjacentElements(None,els[0])
                else:
                    return AdjacentElements()
            if self.left==WEST:
                n0=seg.get_nodes()[0].position()
                n1=seg.get_nodes()[1].position()
                if n0.x==0.0 and n1.x==0.0:
                    return AdjacentElements(None,els[0])
                else:
                    return AdjacentElements()
            msobj=skelctxt.getMicrostructure()
            where = msobj.getRepresentativePixel(
                els[0].dominantPixel(msobj))
            grpnames = pixelgroup.pixelGroupNames(msobj, where)
            if self.left in grpnames:
                return AdjacentElements(els[0],None)
        # Default, obviously.
        return AdjacentElements()



    def hasGroup(self,groupname):
        if self.left==groupname:
            return 1
        return 0
    def renameGroup(self,oldname,newname):
        if self.left==oldname:
            self.left=newname
            return 1
        return 0

registeredclass.Registration(
    "Around a Pixel Group",
    InterfaceDef,
    SinglePixelGroupInterface,
    ordering=30,
    params = [
    pixelgroupparam.PixelGroupInterfaceParameter('left',
                                                 tip="Pixels.")
    ],
    tip="Define an interface around elements with a given pixel group.",
    discussion = """<para>

    The object constructed from this class represents an interface between
    the specified pixel group and any other pixel group (or no pixel group).

    </para>"""
    )

#Create a CompoundInterface parent class?
class UnionInterface(InterfaceDef):
    def __init__(self,interfaces):
        self.interfaces=interfaces
        self.namedinterfaces=utils.OrderedDict()
##        for interfacename in interfaces:
##            self.namedinterfaces[interfacename]=interfacemsplugin.namedinterfaces[interfacename]
    def addToMS(self,interfacemsplugin,interfacename):
        for name in self.interfaces:
            self.namedinterfaces[name]=interfacemsplugin.namedinterfaces[name]
        interfacemsplugin.addInterface(interfacename,self)
##    def info(self):
##        return "Union of interfaces\n" + self.namedinterfaces
##    def __eq__(self,other):
##        if self.__class__!=other.__class__:
##            return 0
##        return ((self._interface1==other._interface1 and \
##                 self._interface2==other._interface2) or
##                (self._interface1==other._interface2 and
##                 self._interface2==other._interface1))
    #This function is used by the mesh construction function to test
    #whether a skeleton segment is part of the interface.
    def getAdjacentElements(self,seg,skelctxt):
        # TODO OPT: This loop returns the first element-set where it gets
        # a hit -- this is fine as long as there is only one that will
        # do this.  Is this in fact the case?
        for interfaceobj in self.namedinterfaces.values():
            els = interfaceobj.getAdjacentElements(seg,skelctxt)
            if els:
                return els
        return AdjacentElements()
    def hasBulkMaterial(self,bulkmatname):
        for interfaceobj in self.namedinterfaces.values():
            if interfaceobj.hasBulkMaterial(bulkmatname):
                return 1
        return 0
    def renameBulkMaterial(self,oldname,newname):
        numrenamed=0
        for interfaceobj in self.namedinterfaces.values():
            if interfaceobj.renameBulkMaterial(oldname,newname):
                numrenamed+=1
        return numrenamed
    def hasInterface(self,interfacename):
        for name, obj in self.namedinterfaces.items():
            if obj.hasInterface(interfacename):
                return 1
            if name==interfacename:
                return 1
        return 0
    def renameInterface(self,oldname,newname):
        interfacenames=self.namedinterfaces.keys()[:]
        for name in interfacenames:
            obj=self.namedinterfaces[name]
            obj.renameInterface(oldname,newname)
            if name==oldname:
                del self.namedinterfaces[oldname]
                self.namedinterfaces[newname]=obj

registeredclass.Registration(
    "Union of named interfaces",
    InterfaceDef,
    UnionInterface,
    ordering=100,
    params = [
    interfaceparameters.ListOfInterfacesParameter("interfaces",
                                                  tip="Current list of interfaces defined in this microstructure."),
    ],
    tip="Define an interface from a union of named interfaces.",
    discussion = """<para>

    The object constructed from this class represents an interface consisting of
    the union of a list of interfaces.

    </para>"""
    )

## Define a Microstructure IO PlugIn so that Interfaces
## will be written to Microstructure data files.

#OOF.LoadData.Microstructure.Interface.New is defined in interfacemenu.py
#OOF.LoadData.Material.Interface.Assign is defined in materialmenu.py

def writeInterface(datafile, mscontext):
    #Interface branch
    #TODO 3.1: The bulk materials that define the interfaces must be written,
    #even if the material is not assigned to pixels.
    #Interface materials are not assigned to pixels. They must be
    #explicitly listed here.
    msobj=mscontext.getObject()
    interfacemsplugin=msobj.getPlugIn("Interfaces")
    for interfacename, interfacedef in interfacemsplugin.namedinterfaces.items():
        datafile.startCmd(OOF.LoadData.Microstructure.Interface.New)
        datafile.argument('microstructure',msobj.name())
        datafile.argument('name',interfacename)
        datafile.argument('interface_type',interfacedef)
        datafile.endCmd()

    #Write interface properties and materials.
    #An interface material is saved only if it has been assigned to
    #an interface.
    materialmenu.writeMaterials(datafile,
                                [materialmanager.getMaterial(m)
                                 for m in interfacemsplugin.getInterfaceMaterials()])

    #Assign interface materials to interfaces
    for matname, interfacenames in interfacemsplugin._materialassignments.items():
        if len(interfacenames)==0:
            continue
##        datafile.startCmd(OOF.LoadData.MaterialandType)
##        datafile.argument('name',matname)
##        matobj=materialmanager.getMaterial(matname)
##        datafile.argument('properties', [prop.registration().name()
##                                         for prop in matobj.properties()])
##        datafile.argument('materialtype',matobj.type())
##        datafile.endCmd()
        datafile.startCmd(OOF.LoadData.Material.Interface.Assign)
        datafile.argument('microstructure',msobj.name())
        datafile.argument('material',matname)
        datafile.argument('interfaces',interfacenames)
        datafile.endCmd()

if runtimeflags.surface_mode:
    microstructureIO.registerMicrostructureIOPlugIn_last(writeInterface)
