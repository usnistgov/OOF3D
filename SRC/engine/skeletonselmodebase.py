# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import mainmenu
from ooflib.common.IO import xmlmenudump

# Each category of thing in a Skeleton which can be selected by the
# user (such as Elements, Nodes, and Segments) must have a subclass of
# SkeletonSelectionMode, and a single instance of that subclass must
# be created at startup time.  The SkeletonSelectionMode subclass
# stores meta-data about the selectable objects, and is used by the
# SkeletonSelectionPage and SkeletonSelectionToolbox to automatically
# generate the user interface and switchboard signals required to
# select the objects.

class SkeletonSelectionMode:
    modes = []
    def __init__(self, name, methodclass, modifierclass,
                 changedselectionsignal, modifierappliedsignal,
                 groupmenu,
                 allCourier,
                 materialsallowed=None):
        self.name = name

        # methodclass is the RegisteredClass of routines for creating
        # new selections.  These appear in the
        # SkeletonSelectionToolbox.
        self.methodclass = methodclass

        # modifierclass is the RegisteredClass of routines for
        # modifying existing selections.  These appear in the
        # SkeletonSelectionPage.
        self.modifierclass = modifierclass

        # changedselectionsignal is sent when any change is made in
        # a selection.  It indicates which selection was changed, but
        # not how.
        self.changedselectionsignal = changedselectionsignal
        # modifierappliedsignal is sent when a selection modifier is
        # uses.  The modifier is sent as an argument.
        self.modifierappliedsignal = modifierappliedsignal

        # groupmenu is the menu of commands for manipulating groups of
        # the object.
        self.groupmenu = groupmenu

        # allCourier is a SkeletonSelectionCourier class that can be
        # used to loop over all objects of this category in the
        # Skeleton.
        self.allCourier = allCourier

        # materialsallowed is either None or a MaterialType instance.
        # If not None, it indicates what kinds of material may be
        # explicitly assigned to groups of this type of selectable
        # object.
        self.materialsallowed = materialsallowed

        self.stacksize = 50

        # Create a menuitem for changing the stack size.  The
        # parameter is shared among the menuitems for all
        # SkeletonSelectionModes as well as the menuitem that sets all
        # of the buffer sizes at once.
        self.stacksize_menuitem = bufsizmenu.addItem(oofmenu.OOFMenuItem(
            name,
            callback=self.setUndoBufferSize,
            params=_stacksize_params, # global, see below
            help="Set the history buffer size for Skeleton %s selections"
            % name,
            discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/skelbufsize.xml',
                lambda text,obj: text.replace('CLASS', name))
            ))
        

        SkeletonSelectionMode.modes.append(self)

    def toolboxName(self):
        return "Select_" + self.name + "s"

    def getSelectionContext(self, skeletoncontext):
        raise ooferror.ErrPyProgrammingError(
            "SkeletonSelectionMode.getSelectionContext() needs to be redefined"
            " in class " + self.__class__.__name__)
    def getGroups(self, skeletoncontext):
        raise ooferror.ErrPyProgrammingError(
            "SkeletonSelectionMode.getGroups() needs to be redefined in class "
            + self.__class__.__name__)
    def getSelectionMenu(self):
        raise ooferror.ErrPyProgrammingError(
            "SkeletonSelectionMode.getSelectionMenu() needs to be redefined"
            " in class " + self.__class__.__name__)
    def getGroupMenu(self):
        raise ooferror.ErrPyProgrammingError(
            "SkeletonSelectionMode.getGroupMenu() needs to be redefined"
            " in class " + self.__class__.__name__)

    def setUndoBufferSize(self, menuitem, size):
        self.stacksize = size+1         # affects future Selection objects
        # Change buffer size for all existing Skeletons
        switchboard.notify(('skelselection ringbuffer resize', self.name),
                           size+1)

    def __repr__(self):
        return "SkeletonSelectionMode('%s')" % self.name

def getMode(name):
    for mode in SkeletonSelectionMode.modes:
        if mode.name == name:
            return mode


def firstMode():
    if SkeletonSelectionMode.modes:
        return SkeletonSelectionMode.modes[0]

########################
    
bufsizmenu = mainmenu.OOF.Settings.UndoBuffer_Size.addItem(oofmenu.OOFMenuItem(
    'Skeleton_Selection',
    help="Set the size of history buffers for Skeleton selection operations",
    ordering=1))

_stacksize = 50

def _allBufSizesCB(menuitem, size):
    _stacksize = size
    for mode in SkeletonSelectionMode.modes:
        mode.setUndoBufferSize(menuitem, size)

_stacksize_params = [parameter.IntParameter(
    'size',
    _stacksize,
    tip='number of previous selections to retain')]

_all_stacksize_menuitem = bufsizmenu.addItem(oofmenu.OOFMenuItem(
    'All',
    callback = _allBufSizesCB,
    ordering=-1,
    params=_stacksize_params,
    help="Set the history buffer size for all Skeleton selections",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/skelbufsizes.xml')
    ))
