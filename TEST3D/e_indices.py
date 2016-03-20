from ooflib.engine.skeletoncontext import skeletonContexts
from ooflib.common import microstructure
msname = microstructure.microStructures.actualMembers()[0].name()
skelctxt = skeletonContexts[msname + ":skeleton"]
eset = skelctxt.elementselection.retrieve()
indices = [e.uiIdentifier() for e in eset]
print indices
