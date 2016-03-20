from ooflib.engine.skeletoncontext import skeletonContexts
from ooflib.common import microstructure
msname = microstructure.microStructures.actualMembers()[0].name()
skelctxt = skeletonContexts[msname + ":skeleton"]
nset = skelctxt.pinnednodes.retrieve()
indices = [n.uiIdentifier() for n in nset]
print indices
