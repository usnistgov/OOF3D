# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Define a MicrostructurePlugIn to catch "material changed"
## switchboard signals and tell the relevant subproblems of the event.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import material
from ooflib.common import debug
from ooflib.common import microstructure
from ooflib.common import runtimeflags
from ooflib.engine import materialmanager
from ooflib.engine import mesh
from ooflib.engine import subproblemcontext


class MaterialMSPlugIn(microstructure.MicrostructurePlugIn):
    def __init__(self, ms):
        microstructure.MicrostructurePlugIn.__init__(self, ms)
        self.sbcallback = switchboard.requestCallback("material changed",
                                                      self.matChanged)
    def destroy(self):
        switchboard.removeCallback(self.sbcallback)
        microstructure.MicrostructurePlugIn.destroy(self)
    def matChanged(self, materialname):
        # The given material has changed.  Look through the materials
        # in our Microstructure to see if we care.
        matl = materialmanager.getMaterial(materialname)
        #Interface branch
        if config.dimension() == 2 and runtimeflags.surface_mode:
            interfacemsplugin=self.microstructure.getPlugIn("Interfaces")
            interfacemats=interfacemsplugin.getInterfaceMaterials()
#         elif config.dimension() == 3:
        else:
            interfacemats = []

        if matl in material.getMaterials(self.microstructure) or \
               materialname in interfacemats:
            # We *do* care. Really.  Tell all the SubProblems
            # belonging to the microstructure that the material has
            # changed.
            msname = self.microstructure.name()
            subppaths = subproblemcontext.subproblems.keys(base=msname)
            for subppath in subppaths:
                subpctxt = subproblemcontext.subproblems[[msname]+subppath]
                subpctxt.changed("Material properties changed.")
            # Also tell everything that cares whether the mesh data
            # has changed.  This includes PropertyOutputs that may be
            # displayed in a mesh data viewer.
            meshpaths = mesh.meshes.keys(base=msname)
            for meshpath in meshpaths:
                meshctxt = mesh.meshes[[msname]+meshpath]
                switchboard.notify("mesh data changed", meshctxt)
                  

microstructure.registerMicrostructurePlugIn(MaterialMSPlugIn, "Material")
