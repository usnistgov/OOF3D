# -*- python -*-
# $RCSfile: pixelinfoplugin.py,v $
# $Revision: 1.2.18.6 $
# $Author: fyc $
# $Date: 2013/08/26 15:41:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import subthread
from ooflib.common.IO.GUI import gtklogger
import ooflib.common.microstructure

import gtk

#####################

# PixelInfoPlugIn classes add additional information about
# pixels/voxels to the PixelInfo toolbox.

# PixelInfoPlugIn classes need the following things:
#   * ordering, at the class level
#   * nrows, at the class level
#   * A constructor with arguments (GtkTable, row) which inserts nrows
#     of widgets into the table starting at the given row.
#   * A function update(toolbox, iPoint) that updates the widgets
#   * A function close() that's called when the toolbox is closed.
#   * A function nonsense() that's called when the mouse click isn't sensible.
#   * A function clear() that's called when the clear button is pressed.

# Here's a nearly useless baseclass:
class PixelInfoPlugIn:
    def __init__(self, toolbox):
        self.toolbox = toolbox
    def close(self):
        del self.toolbox
    def update(self, point):
        pass
    def nonsense(self):
        pass
    def clear(self):
        pass
    

plugInClasses = []
cat = []

def pluginsorter(a,b):
    if a.ordering < b.ordering: return -1
    if a.ordering > b.ordering: return 1
    return 0

def registerPlugInClass(plugin):
    plugInClasses.append(plugin)
    plugInClasses.sort(pluginsorter)
    switchboard.notify('new pixelinfo plugin')

####################################

class MicrostructurePlugIn(PixelInfoPlugIn):
    ordering = 2
    nrows = 3
    def __init__(self, toolbox, table, row):
        debug.mainthreadTest()
        PixelInfoPlugIn.__init__(self, toolbox)
        label = gtk.Label('microstructure=')
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, row,row+1, xpadding=5, xoptions=gtk.FILL)
        self.microtext = gtk.Entry()
        gtklogger.setWidgetName(self.microtext,'MSText')
        self.microtext.set_size_request(12*guitop.top().charsize, -1)
        self.microtext.set_editable(0)
        table.attach(self.microtext, 1,2, row,row+1,
                     xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)

        label = gtk.Label('pixel groups=')
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, row+1,row+2, xpadding=5, xoptions=gtk.FILL)
        self.grouplist = gtk.TextView()
        self.grouplist.set_size_request(12*guitop.top().charsize, -1)
        self.grouplist.set_editable(False)
        self.grouplist.set_cursor_visible(False)
        self.grouplist.set_wrap_mode(gtk.WRAP_WORD)
        gtklogger.setWidgetName(self.grouplist, 'Group view')
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "MSScroll")
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(self.grouplist)
        table.attach(scroll, 1,2, row+1,row+2,
                     xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)

        label = gtk.Label('category=')
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, row+2,row+3, xpadding=5, xoptions=gtk.FILL)
        self.categorytext = gtk.Entry()
        gtklogger.setWidgetName(self.categorytext, 'CategoryText')
        self.categorytext.set_size_request(12*guitop.top().charsize, -1)
        self.categorytext.set_editable(0)
        table.attach(self.categorytext, 1,2, row+2, row+3, xpadding=5,
                     xoptions=gtk.EXPAND|gtk.FILL)

        self.sbcallbacks = [
            switchboard.requestCallbackMain('changed pixel group',
                                            self.grpchanged),
            switchboard.requestCallbackMain('changed pixel groups',
                                            self.grpschngd),
            switchboard.requestCallbackMain('destroy pixel group',
                                            self.grpdestroy),
            switchboard.requestCallbackMain('renamed pixel group',
                                            self.grprenamed)
            ]

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        PixelInfoPlugIn.close(self)

    def clear(self):
        debug.mainthreadTest()
        self.microtext.set_text("")
        self.grouplist.get_buffer().set_text("")
        
    def update(self, where):
        subthread.execute(self.update_thread, (where,))
    def update_thread(self, where):
        debug.subthreadTest()
        global cat
        microstructure = self.toolbox.findMicrostructure()
        if microstructure and where is not None:
            mscntxt = ooflib.common.microstructure.getMSContextFromMS(
                microstructure)
            msname = microstructure.name()
            mscntxt.begin_reading()
            cat = microstructure.category(where)
            try:
                names = pixelgroup.pixelGroupNames(microstructure, cat)
            finally:
                mscntxt.end_reading()
            grpnames = '\n'.join(names)
        else:
            msname = '(No microstructure)'
            grpnames = ''
            cat = ''
        mainthread.runBlock(self.reallyupdate, (msname, grpnames, cat))
    def reallyupdate(self, msname, grpnames, cat):
        debug.mainthreadTest()
        self.microtext.set_text(msname)
        self.grouplist.get_buffer().set_text(grpnames)
        self.categorytext.set_text(`cat`)
##        self.grouplist.show_all()

    def nonsense(self):
        debug.mainthreadTest()
        self.grouplist.get_buffer().set_text('')
        self.microtext.set_text('???')
    def grpchanged(self, group, ms_name):
        microstructure = self.toolbox.findMicrostructure()
        if microstructure and microstructure.name() == ms_name:
            if group.name() in microstructure.groupNames():
                self.update(self.toolbox.currentPixel())
    def grpschngd(self, ms_name):
        microstructure = self.toolbox.findMicrostructure()
        if microstructure and microstructure.name() == ms_name:
            self.update(self.toolbox.currentPixel())
    def grpdestroy(self, group, ms_name):
        microstructure = self.toolbox.findMicrostructure()
        if microstructure and microstructure.name() == ms_name:
            self.update(self.toolbox.currentPixel())                
    def grprenamed(self, group, oldname, newname):
        microstructure = self.toolbox.findMicrostructure()
        if microstructure:
            if newname in microstructure.groupNames():
                self.update(self.toolbox.currentPixel())

registerPlugInClass(MicrostructurePlugIn)


