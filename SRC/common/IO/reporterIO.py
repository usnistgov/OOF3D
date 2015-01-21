# -*- python -*-
# $RCSfile: reporterIO.py,v $
# $Revision: 1.9.10.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Routine for saving the contents of the Message Window.  It has its
# own file to avoid import loops.


from ooflib.common import debug
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import filenameparam
from ooflib.common.IO import reporter

def saveMessages(menuitem, filename, mode, **messagetypes):
    file = open(filename, mode.string())
    for message in reporter.messagemanager.all_messages():
        if messagetypes[message[1]]:
            print >> file, message[0]
    file.close()

mainmenu.OOF.File.Save.addItem(oofmenu.OOFMenuItem(
    "Messages",
    help="Save the message logs from the message windows to a file.",
    callback=saveMessages,
    ordering=20,
    params=[filenameparam.WriteFileNameParameter('filename',
                                                 tip="Name of the file."),
            filenameparam.WriteModeParameter('mode',
                                             tip="'w' to (over)write and 'a' to append")] +
    [parameter.BooleanParameter(name, True,
                                tip="True to include and False to not.")
     for name in reporter.messageclasses],
    discussion="Unlike other <link linkend='MenuItem:OOF.File.Save'>OOF.File.Save</link> menu varieties, messages are saved only in an <emphasis>ascii</emphasis> format for an obvious reason."))
