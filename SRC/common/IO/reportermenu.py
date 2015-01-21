# -*- python -*-
# $RCSfile: reportermenu.py,v $
# $Revision: 1.10.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Menu operations for the message manager -- operations for
# changing what is reported on the command-line, plus an entry
# which can be used in the GUI to bring up a new message window.
# Also, menu logging via the message manager is enabled here.

from ooflib.common.IO import mainmenu
from ooflib.common.IO import reporter
mainmenu.OOF.addLogger(reporter.log)

from ooflib.common.IO import oofmenu

def new_messages(menuitem):
    reporter._new_messages()

winmenu = mainmenu.OOF.Windows

messagemenu = oofmenu.OOFMenuItem('Messages')

messagemenu.addItem(oofmenu.OOFMenuItem(
    'New', callback=new_messages,
    help="Open a new Message window.",
    no_log=1,
    threadable=oofmenu.UNTHREADABLE,
    discussion="<para>Open a new <link linkend='Section:Windows:Messages'>Message</link> window.</para>"))

winmenu.addItem(messagemenu)

