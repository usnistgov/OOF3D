# -*- python -*-
# $RCSfile: activityviewermenu.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2013/01/28 16:58:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import progressbar_delay
from ooflib.common.threadmanager import threadManager

activityviewermenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'ActivityViewer',
    secret=1,
    help='Control the Activity Viewer Window.',
    discussion="""<para>

    In GUI mode, the <link
    linkend='Section-Windows-ActivityViewer'>Activity Viewer</link>
    window displays progress bars for monitoring &oof2; tasks and
    <guilabel>Stop</guilabel> buttons for interrupting them.  In text
    mode, progress bars are drawn with asterisks in a terminal window,
    and typing control-C interrupts tasks.

    </para>"""
    
    ))

# The "File" menu item is visible in the ActivityViewer window in
# GUI mode -- GUI-only menu items are added to it at that time.
# It has to be created here in order to be the first in the sequence on
# the menubar.
filemenu = activityviewermenu.addItem(oofmenu.OOFMenuItem('File', no_doc=1))

settingsmenu = activityviewermenu.addItem(oofmenu.OOFMenuItem(
    'Settings',
    help='Parameters controlling the behavior of the Activity Viewer window.'
    ))

autoDismiss = True
def _autodismiss(menuitem, value):
    global autoDismiss
    autoDismiss = value

settingsmenu.addItem(oofmenu.CheckOOFMenuItem(
    'AutoDismiss',
    value=autoDismiss,
    callback=_autodismiss,
    help="Dismiss progress bars automatically when processes end.",
    threadable = oofmenu.UNTHREADABLE,
    discussion="""<para>

    In GUI mode, when <command>AutoDismiss</command> is on, progress
    bars will be removed from the <link
    linkend='Section-Windows-ActivityViewer'>Activity Viewer</link>
    window when the task that they're monitoring finishes.  If
    <command>AutoDismiss</command> is off, it's necessary to remove
    progress bars explicitly with the <guibutton>Dismiss</guibutton> or
    <guibutton>Dismiss All</guibutton> buttons.

    </para>"""))

settingsmenu.addItem(oofmenu.OOFMenuItem(
    'DelayProgressBarCreation',
    callback=progressbar_delay.set_delay,
    params=[
    parameter.IntParameter('milliseconds', progressbar_delay.delay, tip="Delay time of the progress bar in milliseconds.")],
    help='Create progress bars only for processes that take longer than a specified time.',
    threadable = oofmenu.UNTHREADABLE,
    discussion="""<para>

    Don't create progress bars until a task has been running for the
    given number of <varname>milliseconds</varname>.  This has the
    effect of suppressing progress bars for short-lived tasks, and not
    cluttering up the screen so much.
    
    </para>"""
    ))




