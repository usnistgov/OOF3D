# -*- python -*-
# $RCSfile: skeletonselectiontoolbox.py,v $
# $Revision: 1.19.18.4 $
# $Author: langer $
# $Date: 2013/05/20 17:34:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common.IO import genericselecttoolbox
from ooflib.common import toolbox
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.engine import skeletonselmodebase

## There are four skeleton selection toolboxes, for selecting
## Elements, Nodes, Faces, and Segments.  Each is a subclass of
## SkeletonSelectionToolbox.  The subclasses are created automatically
## by instancing a subclass of SkeletonSelectionMode.


#############################

class SkeletonSelectionToolbox(genericselecttoolbox.GenericSelectToolbox):
    def __init__(self, mode, gfxwindow):
        ## 'mode' is a SkeletonSelectionMode object.  It's stored in
        ## the extrakwargs dict in the GenericSelectToolbox, and is
        ## passed from GenericSelectToolbox.getSelection() to
        ## SkeletonContext.getSelectionContext(), where it's used to
        ## retrieve the appropriate Selection object from the
        ## SkeletonContext.
        self.mode = mode
        genericselecttoolbox.GenericSelectToolbox.__init__(
            self,
            name="Select_"+self.modename(),
            gfxwindow=gfxwindow,
            mode=mode,
            method=mode.methodclass)
    def modename(self):
        return self.mode.name
    def emptyMessage(self):
        return "No Skeleton!"           # you spineless bastard

    def sourceParams(self):
        return [whoville.WhoParameter('skeleton',
                                      whoville.getClass('Skeleton'),
                                      tip=parameter.emptyTipString)]

    def setSourceParams(self, menuitem, source):
        menuitem.get_arg('skeleton').value = source.path()

    def getSourceObject(self, params, gfxwindow):
        ## See comments in common/IO/pixelselectiontoolbox.py.  We're
        ## expecting to find a Skeleton or Mesh, but always return the
        ## Skeleton.
        whopath = labeltree.makePath(params['skeleton'])
        return whoville.getClass('Skeleton')[whopath[:2]]

    def signal(self, method, pointlist, selection):
        # Called by GenericSelectToolbox.selectCB after performing a
        # selection.
        switchboard.notify(self.mode.newselectionsignal, method, pointlist)
        switchboard.notify(self.mode.changedselectionsignal,
                           selection=selection)
        switchboard.notify("redraw")

    # Functions used for xml documentation.
    def objName(self):
        return self.mode.name
    def sourceName(self):
        return "&skel;"
    def sourceParamName(self):
        return 'skeleton'

## Create toolbox subclasses for each SkeletonSelectionMode

tbordering=2.5

def _newSelectionMode(mode):
    class SkelSelectToolbox(SkeletonSelectionToolbox):
        def __init__(self, gfxwindow):
            SkeletonSelectionToolbox.__init__(self,
                                              # mode is extrakwargs.
                                              mode=mode,
                                              gfxwindow=gfxwindow)
        global tbordering
        tbordering += 0.01
        tip="Select " + mode.name + "s in a Skeleton."
        discussion="""<para>
        Commands for selecting %ss in a &skel;, based on mouse input.
        </para>""" % mode.name

    ## The mode keeps a reference to the associated class so that GUI
    ## extensions can be applied to the class.  If the mode didn't
    ## keep a reference, then the only way to find the class would be
    ## to look through the registry in toolbox.py.
    mode.tbclass = SkelSelectToolbox
    toolbox.registerToolboxClass(SkelSelectToolbox, ordering=tbordering)
    
for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
    _newSelectionMode(mode)
    
switchboard.requestCallback(skeletonselmodebase.SkeletonSelectionMode,
                            _newSelectionMode)
