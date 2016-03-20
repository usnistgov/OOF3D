from ooflib.engine.skeletoncontext import skeletonContexts
skelctxt = skeletonContexts["skeltest:skeleton"]
eset = skelctxt.segmentselection.retrieve()
indices = [e.uiIdentifier() for e in eset]
print "There are", len(indices), "selected segments"
print indices
