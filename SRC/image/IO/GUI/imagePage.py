# -*- python -*-
# $RCSfile: imagePage.py,v $
# $Revision: 1.64.10.3 $
# $Author: langer $
# $Date: 2013/11/15 22:03:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import config
if config.dimension() == 2:
    from ooflib.SWIG.image import oofimage
elif config.dimension() == 3:
    from ooflib.SWIG.image import oofimage3d
    #from ooflib.image import oofimage3d
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import mainthread
from ooflib.common import microstructure
from ooflib.common import ringbuffer
from ooflib.common import subthread
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import historian
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.image import imagemodifier
from ooflib.image import imagecontext
from types import *
import gtk

#font = load_font("-*-fixed-*-*-*-*-*-120-*-*-*-*-iso8859-*")

class ImagePage(oofGUI.MainPage):
    def __init__(self):
        oofGUI.MainPage.__init__(self, name="Image", ordering=50,
                                 tip='Manipulate Images')

        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        label = gtk.Label('Microstructure=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        self.imagewidget = whowidget.WhoWidget(imagecontext.imageContexts)
        centerbox.pack_start(self.imagewidget.gtk[0], expand=0, fill=0)
        label = gtk.Label('Image=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.imagewidget.gtk[1], expand=0, fill=0)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(homogeneous=1, spacing=3)
        align.add(centerbox)

        self.loadbutton = gtk.Button('Load...')
        gtklogger.setWidgetName(self.loadbutton, 'Load')
        centerbox.pack_start(self.loadbutton, expand=1, fill=1)
        gtklogger.connect(self.loadbutton, 'clicked', self.loadCB)
        tooltips.set_tooltip_text(self.loadbutton,
                             'Load a new image into an existing Microstructure')
        
        self.copybutton = gtkutils.StockButton(gtk.STOCK_COPY, 'Copy...')
        gtklogger.setWidgetName(self.copybutton, 'Copy')
        gtklogger.connect(self.copybutton, 'clicked', self.copyCB)
        centerbox.pack_start(self.copybutton, expand=1, fill=1)
        tooltips.set_tooltip_text(self.copybutton,
                             'Copy the current image.  The copy can be in the same or a different Microstructure.')

        self.renamebutton = gtkutils.StockButton(gtk.STOCK_EDIT, 'Rename...')
        gtklogger.setWidgetName(self.renamebutton, 'Rename')
        gtklogger.connect(self.renamebutton, 'clicked', self.renameCB)
        tooltips.set_tooltip_text(self.renamebutton,
                             'Rename the current image.')
        centerbox.pack_start(self.renamebutton, expand=1, fill=1)

        self.deletebutton = gtkutils.StockButton(gtk.STOCK_DELETE, 'Delete')
        gtklogger.setWidgetName(self.deletebutton, 'Delete')
        gtklogger.connect(self.deletebutton, 'clicked', self.deleteCB)
        tooltips.set_tooltip_text(self.deletebutton,
                             'Delete the current image.')
        centerbox.pack_start(self.deletebutton, expand=1, fill=1)

        self.savebutton = gtkutils.StockButton(gtk.STOCK_SAVE, 'Save...')
        gtklogger.setWidgetName(self.savebutton, 'Save')
        gtklogger.connect(self.savebutton, 'clicked', self.saveCB)
        tooltips.set_tooltip_text(self.savebutton,
                             'Save the current image to a file.')
        centerbox.pack_start(self.savebutton, expand=1, fill=1)

        self.autogroupbutton = gtk.Button('Group...')
        gtklogger.setWidgetName(self.autogroupbutton, 'Group')
        gtklogger.connect(self.autogroupbutton, 'clicked', self.autogroupCB)
        centerbox.pack_start(self.autogroupbutton, expand=1, fill=1, padding=2)
        if config.dimension() == 2:
            tooltips.set_tooltip_text(self.autogroupbutton, "Create a pixel group in the current image's microstructure for each color pixel in the image.")
        elif config.dimension() == 3:
            tooltips.set_tooltip_text(self.autogroupbutton, "Create a voxel group in the current image's microstructure for each color voxel in the image.")

        mainpane = gtk.HPaned()
        gtklogger.setWidgetName(mainpane, 'Pane')
        mainbox.pack_start(mainpane, expand=1, fill=1)
        gtklogger.connect_passive(mainpane, 'notify::position')

        frame = gtk.Frame('Image Information')
        frame.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack1(frame, resize=True, shrink=False)
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "StatusScroll")
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        frame.add(scroll)

        self.infoarea = fixedwidthtext.FixedWidthTextView()
        self.infoarea.set_wrap_mode(gtk.WRAP_WORD)
        self.infoarea.set_editable(False)
        self.infoarea.set_cursor_visible(False)
        scroll.add_with_viewport(self.infoarea)

        frame = gtk.Frame('Image Modification')
        frame.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack2(frame, resize=False, shrink=False)
        vbox = gtk.VBox()
        frame.add(vbox)
##        scroll = gtk.ScrolledWindow()    # scroll window for image mod method
##        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
##        vbox.pack_start(scroll, expand=1, fill=1)
        self.imageModFactory = regclassfactory.RegisteredClassFactory(
            imagemodifier.ImageModifier.registry,
            title="Method:", name="Method")
##        scroll.add_with_viewport(self.imageModFactory.gtk)
        vbox.pack_start(self.imageModFactory.gtk, expand=1, fill=1)
        self.historian = historian.Historian(self.imageModFactory.set,
                                             self.sensitizeHistory,
                                             setCBkwargs={'interactive':1})
        self.imageModFactory.set_callback(self.historian.stateChangeCB)

        # Prev, OK, and Next buttons
        hbox = gtk.HBox()
        vbox.pack_start(hbox, expand=0, fill=0, padding=2)
        self.prevmethodbutton = gtkutils.prevButton()
        gtklogger.connect(self.prevmethodbutton, 'clicked',
                          self.historian.prevCB)
        hbox.pack_start(self.prevmethodbutton, expand=0, fill=0, padding=2)
        tooltips.set_tooltip_text(self.prevmethodbutton,
                             'Recall the previous image modification operation.')
        self.okbutton = gtk.Button(stock=gtk.STOCK_OK)
        gtklogger.setWidgetName(self.okbutton, 'OK')
        hbox.pack_start(self.okbutton, expand=1, fill=1, padding=5)
        gtklogger.connect(self.okbutton, 'clicked', self.okbuttonCB)
        tooltips.set_tooltip_text(self.okbutton,
                  'Perform the image modification operation defined above.')
        self.nextmethodbutton = gtkutils.nextButton()
        gtklogger.connect(self.nextmethodbutton, 'clicked',
                          self.historian.nextCB)
        hbox.pack_start(self.nextmethodbutton, expand=0, fill=0, padding=2)
        tooltips.set_tooltip_text(self.nextmethodbutton,
                             "Recall the next image modification operation.")

        # Undo and Redo buttons
        hbox = gtk.HBox()
        vbox.pack_start(hbox, expand=0, fill=0, padding=2)
        self.undobutton = gtk.Button(stock=gtk.STOCK_UNDO)
        gtklogger.setWidgetName(self.undobutton, 'Undo')
        gtklogger.connect(self.undobutton, 'clicked', self.undoCB)
        tooltips.set_tooltip_text(self.undobutton,
                             'Undo the latest image modification.')
        hbox.pack_start(self.undobutton, expand=1, fill=0, padding=10)
        self.redobutton = gtk.Button(stock=gtk.STOCK_REDO)
        gtklogger.setWidgetName(self.redobutton, 'Redo')
        gtklogger.connect(self.redobutton, 'clicked', self.redoCB)
        tooltips.set_tooltip_text(self.redobutton,
                             'Redo the latest undone image modification.')
        hbox.pack_start(self.redobutton, expand=1, fill=0, padding=10)

        self.sensitize()
        self.sensitizeHistory()
        
        self.sbcallbacks = [
            switchboard.requestCallbackMain(('new who', 'Microstructure'),
                                            self.newMicrostructureCB),
            switchboard.requestCallbackMain(('new who', 'Image'),
                                            self.newImageCB),
            switchboard.requestCallbackMain(('remove who', 'Image'),
                                            self.rmWhoCB),
            switchboard.requestCallbackMain('modified image',
                                            self.modifiedImageCB),
            switchboard.requestCallbackMain(imagemodifier.ImageModifier,
                                            self.updateImageModifiers),
            switchboard.requestCallbackMain(self.imagewidget,
                                            self.iWidgetChanged),
            switchboard.requestCallbackMain(('validity',
                                             self.imageModFactory),
                                            self.validityChangeCB),
            switchboard.requestCallbackMain(('WhoDoUndo buffer change',
                                             'Image'),
                                            self.whoBufChangeCB)
            ]

        subthread.execute(self.displayImageInfo)
        
    def sensitize(self):
        debug.mainthreadTest()
        image = self.getCurrentImage()
        selected = image is not None
        self.copybutton.set_sensitive(selected)
        self.renamebutton.set_sensitive(selected)
        self.deletebutton.set_sensitive(selected)
        self.savebutton.set_sensitive(selected)
        self.okbutton.set_sensitive(selected and self.imageModFactory.isValid())
        self.autogroupbutton.set_sensitive(selected)
        self.loadbutton.set_sensitive(self.getCurrentMS() is not None)
        if selected:
            self.undobutton.set_sensitive(image.undoable())
            self.redobutton.set_sensitive(image.redoable())
        else:
            self.undobutton.set_sensitive(0)
            self.redobutton.set_sensitive(0)

    def sensitizeHistory(self):
        debug.mainthreadTest()
        self.nextmethodbutton.set_sensitive(self.historian.nextSensitive())
        self.prevmethodbutton.set_sensitive(self.historian.prevSensitive())

    def validityChangeCB(self, validity):
        self.sensitize()

    def whoBufChangeCB(self):
        self.sensitize()

    def iWidgetChanged(self, interactive):
        self.sensitize()
        subthread.execute(self.displayImageInfo)
        
    def displayImageInfo(self):
        debug.subthreadTest()
        imagecontext = self.getCurrentImage()
        text = ""
        if imagecontext:
            imagecontext.begin_reading()
            try:
                if config.dimension() == 2:
                    image = imagecontext.getObject()
                    size = image.sizeInPixels()
                    text += 'Pixel size: %dx%d\n' % (size.x, size.y)
                    size = image.size()
                    text += 'Physical size: %gx%g\n' % (size.x, size.y)
                    if image.comment():
                        text += '\nComments:\n%s\n' % image.comment()
                elif config.dimension() == 3:
                    image = imagecontext.getObject()
                    size = image.sizeInPixels()
                    text += 'Voxel size: %dx%dx%d\n' % (size.x, size.y, size.z)
                    size = image.size()
                    text += 'Physical size: %gx%gx%g\n' % (size.x, size.y, size.z)                    
            finally:
                imagecontext.end_reading()
        mainthread.runBlock(self.displayImageInfo_thread, (text,))

    def displayImageInfo_thread(self, text):
        debug.mainthreadTest()
        self.infoarea.get_buffer().set_text(text)

    def getCurrentImageName(self):
        path = labeltree.makePath(self.imagewidget.get_value())
        if path:
            return path[-1]

    def getCurrentMSName(self):
        return self.imagewidget.get_value(depth=1)

    def getCurrentMS(self):
        try:
            return microstructure.microStructures[self.getCurrentMSName()]
        except KeyError:
            pass
        
    def getCurrentImage(self):
        try:
            return imagecontext.imageContexts[self.imagewidget.get_value()]
        except KeyError:
            pass

    def updateImageModifiers(self):
        self.imageModFactory.update(imagemodifier.ImageModifier.registry)

    def newImageCB(self, whoname):        # switchboard 'new who', 'Image'
        self.imagewidget.set_value(whoname)
        self.sensitize()

    def rmWhoCB(self, whoname):         # switchboard 'remove who'
        self.sensitize()

    def newMicrostructureCB(self, msname):
        if not self.getCurrentImage():
            self.imagewidget.set_value(msname)

    ############### GUI callbacks ################

    def loadCB(self, button):
        menuitem = mainmenu.OOF.File.Load.Image
        if parameterwidgets.getParameters(title='Load Image',
                                          *menuitem.params):
            menuitem.callWithDefaults()

    def copyCB(self, button):
        menuitem = mainmenu.OOF.Image.Copy
        nameparam = menuitem.get_arg('name')
        msparam = menuitem.get_arg('microstructure')
        if parameterwidgets.getParameters(msparam, nameparam,
                                          title="Copy Image"):
            menuitem.callWithDefaults(image=self.imagewidget.get_value())

    def renameCB(self, button):
        menuitem = mainmenu.OOF.Image.Rename
        namearg = menuitem.get_arg('name')
        namearg.value = labeltree.makePath(self.imagewidget.get_value())[-1]
        if parameterwidgets.getParameters(namearg, title='Rename Image'):
            menuitem.callWithDefaults(image=self.imagewidget.get_value())

    def deleteCB(self, button):
        if reporter.query("Really delete %s?"
                          % self.getCurrentImageName(),
                          "No", default="Yes") == "Yes":
            mainmenu.OOF.Image.Delete(image=self.imagewidget.get_value())
            
    def saveCB(self,button):
        menuitem = mainmenu.OOF.File.Save.Image
        params = filter(lambda x: x.name!="image", menuitem.params)
        if parameterwidgets.getParameters(title='Save Image', *params):
            menuitem.callWithDefaults(image=self.imagewidget.get_value())
                                          
    def okbuttonCB(self, button):
        modmeth = self.imageModFactory.getRegistration()
        if modmeth is not None:
            # buildImageModMenu() in imagemenu.py builds the
            # Image.Modify menu items from the members of the
            # ImageModifier RegisteredClass.  The Parameters in the
            # menu items are identically the Parameters in the
            # Registrations.  So copying new values out of the Factory
            # into the Registrations, and invoking the menu item with
            # callWithDefaults() executes the command with the current
            # arguments.
            self.imageModFactory.set_defaults() # copy from gui to Registration
            menuitem = getattr(mainmenu.OOF.Image.Modify, modmeth.name())
            menuitem.callWithDefaults(image=self.imagewidget.get_value())

    def modifiedImageCB(self, imageModifier, imagename): # sb 'modified image'
        # Called whenever the image is changed, either by applying an
        # ImageModifier or the Undo and Redo buttons, in which case
        # the imageModifier arg is None.
        if imageModifier is not None:
            self.historian.record(imageModifier)
        self.sensitize()
        
    def undoCB(self, button):
        mainmenu.OOF.Image.Undo(image=self.imagewidget.get_value())

    def redoCB(self, button):
        mainmenu.OOF.Image.Redo(image=self.imagewidget.get_value())

    def autogroupCB(self, button):
        menuitem = mainmenu.OOF.Image.AutoGroup
        nameparam = menuitem.get_arg('name_template')
        if parameterwidgets.getParameters(nameparam,
                                          title='AutoGroup'):
            menuitem.callWithDefaults(image=self.imagewidget.get_value())
##        mainmenu.OOF.Image.AutoGroup(image=self.imagewidget.get_value())
        
ImagePage()

