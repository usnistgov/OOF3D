from ooflib.engine.skeletoncontext import skeletonContexts
skelctxt = skeletonContexts["skeltest:skeleton"]
eset = skelctxt.faceselection.retrieve()
indices = [e.uiIdentifier() for e in eset]
print indices
