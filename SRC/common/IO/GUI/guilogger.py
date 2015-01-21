# -*- python -*-
# $RCSfile: guilogger.py,v $
# $Revision: 1.25.2.7 $
# $Author: langer $
# $Date: 2014/07/31 18:32:50 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common import thread_enable
from ooflib.common.IO import filenameparam
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import reporter
from ooflib.common.IO import parameter
from ooflib.common.IO import progressbar_delay
from ooflib.common.IO.GUI import activityViewer
from ooflib.common.IO.GUI import gtklogger
import gobject
import gtk
import os
import sys
import traceback

guidebugmenu = mainmenu.debugmenu.addItem(oofmenu.OOFMenuItem("GUI_Logging",
                                                              ordering=1000,
                                                              no_log=True,
                                                              post_hook=None))


# When running under the OOF context, gtklogger should catch OOF
# errors also.  TODO 3.1 -- after the changeover to SWIG 1.3, OOF
# exceptions will probably be subclasses of Exception, so this will be
# redundant.
gtklogger.allexceptions = (Exception, ooferror.ErrErrorPtr)

###################################

# menucheckpoint is installed as the main menu's post_hook function.
# It's run after every menu command, and inserts a checkpoint in the
# log file.

def menucheckpoint(menuitem, successful):
    # successful==True means that the menuitem's callback didn't raise
    # an exception.
    gtklogger.checkpoint(menuitem.path())

##################################

_recording = False
_replaying = False

def recording():
    return _recording

def replaying():
    return _replaying

def logFinished():                      # called by GUILogPlayer when done
    global _replaying
    _replaying = False
    if not recording():
        mainmenu.OOF.removeOption('post_hook')
    debug.fmsg("Finished replaying gui log file.")

############################
    
def startLog(menuitem, filename, use_gui):#Passing the use_gui parameter to show the loggergui
    gtklogger.reset_checkpoints()
    menuitem.root().setOption('post_hook', menucheckpoint)
    if debug.debug():
        dblevel = 3
    else:
        dblevel = 0
    global _recording
    _recording = True
    #if use_gui:
    #    loggui = os.popen("python -m loggergui " + filename, "w")
    #    gtklogger.start(loggui, debugLevel=dblevel)
    #else:
    #    gtklogger.start(filename, debugLevel=dblevel)
    #debug.fmsg()
    #debug.dumpTrace()
    gtklogger.start(filename, debugLevel=dblevel, logger_comments=use_gui) # Passing the logger_comments parameter to show the loggergui

guidebugmenu.addItem(oofmenu.OOFMenuItem(
    'Record',
    callback=startLog,
    params=[filenameparam.WriteFileNameParameter(
                'filename', ident='guilog', tip="Name of the file."),
            parameter.BooleanParameter(
                'use_gui', True, tip="Use the logger gui to insert comments?")
            ],
    ellipsis=1,
    help="Save GUI events in a Python script",
    ))

############################

def stopLog(menuitem):
    debug.mainthreadTest()
    global _recording
    _recording = False
    menuitem.root().removeOption('post_hook')
    gtklogger.stop()

guidebugmenu.addItem(oofmenu.OOFMenuItem(
    'Stop',
    callback=stopLog,
    no_log=1,
    threadable=oofmenu.UNTHREADABLE,
    help="Stop recording GUI events"))

############################

# loggererror is installed as the gtklogger handler for exceptions
# that occur during playback.  It's not possible to use the standard
# oof2 exception handling mechanism directly, because it doesn't
# handle the gtk thread locks properly in this case (ie, inside an
# idle callback on the main thread, but with
# oof_mainiteration._inside_idle_callback==0).

def loggererror(exc, line):
    from ooflib.common.IO.GUI import reporter_GUI
    type, value, tb = sys.exc_info()
    tblist = traceback.extract_tb(tb)
    reporter_GUI.gui_printTraceBack(type, value, tblist)
    return True

####

def loadLog(menuitem, filename, checkpoints):
    if gtklogger.replaying():
        raise ooferror.ErrUserError(
            "Multiple GUI logs cannot be replayed simultaneously!")
    debug.fmsg("Loading gui script", filename)
    menuitem.root().setOption('post_hook', menucheckpoint)
    dblevel = 0
    if debug.debug():
        dblevel = 3
    #dblevel = 4
    global _replaying
    _replaying = True

    # When replaying, we have to make sure that progress bars *always*
    # appear, so we set the delay time to 0.  If the delay time is
    # non-zero, then a script recorded on a slow machine would insert
    # a checkpoint for opening the activity viewer window, but a
    # faster machine might never open the window, and would wait
    # forever for the checkpoint when replaying the script.
    progressbar_delay.set_delay(None, 0)

    gtklogger.replay(
        filename,
        beginCB=activityViewer.openActivityViewer,
        finishCB=logFinished,
        debugLevel=dblevel,
        threaded=thread_enable.query(),
        exceptHook=loggererror,
        checkpoints=checkpoints)

guidebugmenu.addItem(oofmenu.OOFMenuItem(
    'Replay',
    callback=loadLog,
    params=[filenameparam.ReadFileNameParameter('filename', ident='guilog',
                                                tip="Name of the file."),
            parameter.BooleanParameter('checkpoints', True, 'obey checkpoints?')
            ],
    ellipsis=1,
    help="Load a GUI log file"))

##############################

def rerecordLog(menuitem, filename, checkpoints, use_gui):
    if gtklogger.replaying():
        raise ooferror.ErrUserError(
            "Multiple GUI logs cannot be replayed simultaneously!")
    menuitem.root().setOption('post_hook', menucheckpoint)
    dblevel = 0
    if debug.debug():
        dblevel = 3
    #dblevel = 4
    global _replaying, _recording
    _replaying = True
    _recording = True
    progressbar_delay.set_delay(None, 0)

    # Find a suitable new name for the backup copy of the old log
    # file.  Just append ".bak", but if that file already exists,
    # append ".bakX", where X is an integer.
    if not os.path.exists(filename + '.bak'):
        backupname = filename + '.bak'
    else:
        backupname = None
        count = 2
        while not backupname:
            trialname = "%s.bak%d" % (filename, count)
            if not os.path.exists(trialname):
                backupname = trialname
            count += 1
    os.system('cp '+filename+' '+backupname)
    debug.fmsg("Loading gui script", backupname)

    gtklogger.replay(
        backupname,
        beginCB=activityViewer.openActivityViewer,
        finishCB=logFinished,
        debugLevel=dblevel,
        threaded=thread_enable.query(),
        exceptHook=loggererror,
        rerecord=filename,
        checkpoints=checkpoints,
        logger_comments=use_gui) #Passing the logger_comments parameter to show the loggergui

guidebugmenu.addItem(oofmenu.OOFMenuItem(
    'Rerecord',
    callback=rerecordLog,
    params=[
        filenameparam.FileNameParameter('filename', ident='guilog',
                                        tip='Name of the log file'),
        parameter.BooleanParameter('checkpoints', True, 'obey checkpoints?'),
        parameter.BooleanParameter('use_gui', True,
                                   tip="Use the logger gui to insert comments?")
            ],
    ellipsis=1,
    help="Load and rerecord a GUI log file"))

#####################

def sanity_check(menuitem):
    gtklogger.comprehensive_sanity_check()

guidebugmenu.addItem(oofmenu.OOFMenuItem(
    'Sanity_Check',
    callback=sanity_check,
    no_log=1,
    help="Check that widget names are unique"))


############################

# Selecting 'Pause' from the logger menu when recording will cause the
# program to pause on playback until the Continue button is pressed.
# Clicks on the Continue button are *not* recorded, so the program
# can't continue on its own, but must wait for the user to press the
# button the old fashioned way.

def pauseLog(menuitem):
    pass

def pauseGUI(menuitem):
    dialog = gtk.Dialog()
    dialog.set_title("OOF2 Pause")
    dialog.vbox.pack_start(gtk.Label("Continue?"))
    dialog.add_button(gtk.STOCK_OK, 0)
    dialog.show_all()
    result = dialog.run()
    dialog.destroy()
    menuitem.callWithDefaults()

guidebugmenu.addItem(oofmenu.OOFMenuItem(
        'Pause',
        callback=pauseLog,
        gui_callback=pauseGUI,
        help="Stop replaying until the 'Continue' button is pressed."))

