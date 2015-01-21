# -*- python -*-
# $RCSfile: quit.py,v $
# $Revision: 1.37.2.2 $
# $Author: langer $
# $Date: 2012/03/13 15:01:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import guitop
from ooflib.common import debug
from ooflib.common.IO import mainmenu
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import parameterwidgets
import ooflib.common.quit

# OOFMenu gui callback for the Quit commands.  Installed by
# mainmenuGUI.py and subWindow.py.  This should only be called on the
# main thread.
def queryQuit(*args, **kwargs):
    if _quitQuery():
        ooflib.common.quit.cleanup(shutdown, kwargs.get('exitstatus', 0))
        return True
    return False

def _quitQuery():
    if not ooflib.common.quit.quiet():
        if mainmenu.OOF.logChanged():
            answer = reporter.query("Save log file before quitting?",
                                    "Save", "Don't Save", "Cancel",
                                    default="Don't Save")
            if answer=="Cancel" or answer is None:
                return False        # don't quit
            if answer=="Save":
                menuitem = mainmenu.OOF.File.Save.Python_Log
                if parameterwidgets.getParameters(title="Save Log File", 
                                                  *menuitem.params):
                    menuitem.callWithDefaults()
                    return True    # log was saved, quit
                else:
                    return False # saving was cancelled, don't quit
    return True                  # quit

def shutdown(exitstatus):
    gui = guitop.top()
    if gui:
        gui.stop()
        gui.destroy()
    ooflib.common.quit.shutdown(exitstatus)
