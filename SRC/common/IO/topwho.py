# -*- python -*-
# $RCSfile: topwho.py,v $
# $Revision: 1.15.18.3 $
# $Author: langer $
# $Date: 2014/11/05 16:54:16 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. HoweveHoweverr, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.common import debug
from ooflib.common.IO import whoville

class TopWho(whoville.WhoProxyClass):
    def resolve(self, proxy, gfxwindow):
        if gfxwindow is not None:
            return gfxwindow.topwho(proxy.whoclass.name())
    # def getTimeStamp(self, proxy, gfxwindow):
    #     return gfxwindow.getLayerChangeTimeStamp()

# Create the WhoProxyClass.  It's automatically registered by the
# WhoProxyClass constructor, so we don't need to keep a reference to
# it here.

TopWho('<topmost>')                           


# 
pixel_select_whoset = ('Microstructure', 'Image')

class TopPixelSelection(whoville.WhoProxyClass):
    def resolve(self, proxy, gfxwindow):
        if gfxwindow is not None:
            whoobj = gfxwindow.topwho(*pixel_select_whoset)
            if whoobj is not None:
                microstructure = whoobj.getMicrostructure()
                if microstructure:
                    return microstructure.pixelselection
    # def getTimeStamp(self, proxy, gfxwindow):
    #     return gfxwindow.getLayerChangeTimeStamp()
        
TopPixelSelection('<top microstructure>')

active_area_whoset = ('Microstructure', 'Image', 'Skeleton', 'Mesh')

class TopActiveArea(whoville.WhoProxyClass):
    def resolve(self, proxy, gfxwindow):
        if gfxwindow is not None:
            whoobj = gfxwindow.topwho(*active_area_whoset)
            if whoobj is not None:
                microstructure = whoobj.getMicrostructure()
                if microstructure:
                    return microstructure.activearea
    # def getTimeStamp(self, proxy, gfxwindow):
    #     return gfxwindow.getLayerChangeTimeStamp()


TopActiveArea('<top activearea>')

