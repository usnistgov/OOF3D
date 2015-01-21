# -*- python -*-
# $RCSfile: tutorialsGUI.py,v $
# $Revision: 1.48.2.6 $
# $Author: langer $
# $Date: 2014/09/25 20:04:13 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common.IO import filenameparam
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO.GUI import fileselector
from ooflib.common.IO.GUI import fontselector
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import subWindow
from ooflib.common.IO.GUI import tooltips
from ooflib.tutorials import tutorial

import gtk
import pango
import re
import string
import textwrap
import os


## TODO 3.1: Add a table of contents.

## TODO 3.1: We will preferably keep the IMAGE TAG for later. And find
## a less intrusive way to displayed some images in the tutorial. A
## nice way will be to have them floating out of the screen when the
## addressed section is passed or the user is over it. Note: The image
## TAG is used like the BOLD one except that the link to the image is
## passed in. The base path is the images folder in the tutorials.

## TODO 3.1: Allow the tutorial window to scroll even when a modal
## dialog box is open. Maybe use a separate process?  How will the
## Next button be sensitized then?

## TODO 3.1: Using the Back and Next or Jump buttons can desensitize a
## sensitized Next button.  Fix that.

boldtag = "BOLD("
imagetag = "IMAGE("
lenboldtag = len(boldtag)
lenimagetag = len(imagetag)
delimexpr = re.compile(r'[^\\]\)')      # finds ')' not preceded by '\'
nondelimexpr = re.compile(r'\\\)')      # finds '\)'
parasplit = re.compile(r'\n\s*\n')      # finds lines with only white space
endline = re.compile(r'\s*\n\s*')
imagespath = os.getcwd()+'/SRC/tutorials/images/'


## This is ugly.  It should be rewritten to take advantage of pango markup.

class Comment:
    def __init__(self, comment, font=None):
        self.font = font
        self.commentList = []
        self.fontList = []
        self.pixList = []
        # Split comment into paragraphs at blank lines.
        paragraphs = parasplit.split(comment)

        for para in paragraphs:
            # Replace newlines with spaces within paragraphs, and get
            # rid of excess white space.
            para = endline.sub(' ', para).strip()

            # Separate paragraph into strings so that each string has
            # a single font, by looking for BOLD(...).
            while para:
                index_bold = string.find(para, boldtag)
                index_image = string.find(para, imagetag)
                if index_bold != -1:
		    self.commentList.append(para[:index_bold])
		    self.fontList.append(0)
		    self.pixList.append(0)
		    para = para[index_bold + lenboldtag:]
		    # look for closing ')'
		    endmatch = delimexpr.search(para)
		    if not endmatch:
			raise ooferror.ErrPyProgrammingError(
			    "Missing delimeter for BOLD tag in tutorial!")
		    boldtext = para[:endmatch.start()+1]
		    # replace all occurences of '\)' with ')'
		    self.commentList.append(nondelimexpr.sub(')', boldtext))
		    self.fontList.append('bold')
		    self.pixList.append(0)
		    para = para[endmatch.end():]
                elif index_image != -1:
		    self.commentList.append(para[:index_image])
		    self.pixList.append(0)
		    self.fontList.append(0)
		    para = para[index_image + lenimagetag:]
		    # look for closing ')'
		    endmatch = delimexpr.search(para)
		    if not endmatch:
			raise ooferror.ErrPyProgrammingError(
			    "Missing delimeter for IMAGE tag in tutorial!")
		    imagename = para[:endmatch.start()+1]
		    # replace all occurences of '\)' with ')'
		    self.commentList.append(nondelimexpr.sub(')', imagename))
		    self.pixList.append('image')
		    self.fontList.append(0)
		    para = para[endmatch.end():]
                else:
		    self.commentList.append(para)
		    self.fontList.append(0)
		    self.pixList.append(0)
		    break
            self.commentList.append('\n\n')
            self.fontList.append(0)
            self.pixList.append(0)

    def isBold(self, index):
        return self.fontList[index]
    def isImage(self, index):
	return self.pixList[index]
    def __len__(self):
        return len(self.commentList)
    def __getitem__(self, i):
        return self.commentList[i]


####################################            

tutorialInProgress = None

def start_class(tutor, progress=0):
    debug.mainthreadTest()
    global tutorialInProgress
    if not tutorialInProgress:
        tutorialInProgress = TutorialClassGUI(tutor)
    tutorialInProgress.raise_window()
    mainmenu.OOF.Windows.Tutorial.enable()
    if progress != 0:
        tutorialInProgress.resume(progress)

tutorial.start_tutorial = start_class

# Resume a tutorial from a saved script.
def resume_tutorial(menuitem, subject, progress):
    tutor = tutorial.allTutorials[subject]
    mainthread.runBlock(start_class, (tutor, progress))
    
mainmenu.OOF.Help.Tutorials.addItem(
    oofmenu.OOFMenuItem('Resume',
                        callback=resume_tutorial,
                        secret=1,
                        params=[parameter.StringParameter('subject'),
                                parameter.IntParameter('progress')],
                        help="Resume a tutorial.  This command is only used when tutorials are saved."
                        )
    )

def raise_tutorial(menuitem):
    debug.mainthreadTest()
    tutorialInProgress.raise_window()

mainmenu.OOF.Windows.addItem(oofmenu.OOFMenuItem(
    'Tutorial',
    help="Raise the tutorial window.",
    callback=raise_tutorial,
    threadable=oofmenu.UNTHREADABLE,
    gui_only=1,
    ordering=1000))
mainmenu.OOF.Windows.Tutorial.disable() # there's no window to raise, yet.
                                             
class TutorialClassGUI(subWindow.SubWindow):
    def __init__(self, tutor):
        debug.mainthreadTest()

        for menuitem in mainmenu.OOF.Help.Tutorials.items:
            menuitem.disable()

        subWindow.SubWindow.__init__(self, title=tutor.subject, menu="")

        self.subwindow_menu.File.addItem(oofmenu.OOFMenuItem(
            'Save_Text',
            callback=self.savePrintable,
            params=[filenameparam.WriteFileNameParameter('filename',
                                                         ident="FileMenu"),
                    filenameparam.WriteModeParameter('mode')],
            help="Save the text of this tutorial in a file.",
            no_log=1,
            ordering=-1))

        labelhbox = gtk.HBox()
        self.subject = gtk.Label()
        self.slideIndex = gtk.Label()
        labelhbox.pack_start(self.subject, expand=1, fill=1, padding=2)
        labelhbox.pack_end(self.slideIndex, expand=0, fill=0, padding=2)
        self.mainbox.pack_start(labelhbox, expand=0, fill=0, padding=2)

        self.msgscroll = gtk.ScrolledWindow()
        self.scrollsignals = gtklogger.logScrollBars(self.msgscroll,
                                                     "TutorialScroll")
        self.msgscroll.set_shadow_type(gtk.SHADOW_IN)
        self.msgscroll.set_border_width(2)
        self.msgscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.mainbox.pack_start(self.msgscroll, expand=1, fill=1)
        self.textview = gtk.TextView()
        self.textview.set_cursor_visible(False)
        self.textview.set_editable(False)
        textattrs = self.textview.get_default_attributes()
        self.centerImageTag = self.textview.get_buffer().create_tag ('center-image', justification = gtk.JUSTIFY_CENTER)
        self.boldTag = self.textview.get_buffer().create_tag(
            "bold",
            weight=pango.WEIGHT_BOLD,  # why doesn't this work?
            foreground="blue")
##         self.boldTag = self.textview.get_buffer().create_tag(
##             "bold",
##             weight=pango.WEIGHT_HEAVY,  # why doesn't this work?
##             underline=pango.UNDERLINE_SINGLE)
        self.textview.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.msgscroll.add(self.textview)        

        buttonbox = gtk.HBox(homogeneous=1, spacing=2)
        self.mainbox.pack_end(buttonbox, expand=0, fill=0, padding=2)
        self.backbutton = gtkutils.StockButton(gtk.STOCK_GO_BACK, "Back")
        gtklogger.setWidgetName(self.backbutton, "Back")
        gtklogger.connect(self.backbutton, "clicked", self.backCB)
        tooltips.set_tooltip_text(self.backbutton, 
                                  "Move to the previous slide.")

        self.nextbutton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD, "Next")
        gtklogger.setWidgetName(self.nextbutton, "Next")
        gtklogger.connect(self.nextbutton, "clicked", self.nextCB)
        tooltips.set_tooltip_text(self.nextbutton, "Move to the next slide.")
        
        self.jumpbutton = gtkutils.StockButton(gtk.STOCK_GOTO_LAST, "Jump")
        gtklogger.setWidgetName(self.jumpbutton, "Jump")
        gtklogger.connect(self.jumpbutton, "clicked", self.jumpCB)
        tooltips.set_tooltip_text(self.jumpbutton, "Jump to the leading slide.")

        self.savebutton = gtkutils.StockButton(gtk.STOCK_SAVE, "Save...")
        gtklogger.setWidgetName(self.savebutton, "Save")
        gtklogger.connect(self.savebutton, "clicked", self.saveCB)
        tooltips.set_tooltip_text(self.savebutton, 
                                  "Save your tutorial session.")

        self.closebutton = gtkutils.StockButton(gtk.STOCK_CLOSE, "Close")
        gtklogger.setWidgetName(self.closebutton, "Close")
        gtklogger.connect(self.closebutton, "clicked", self.closeCB)
        tooltips.set_tooltip_text(self.closebutton, "Quit the tutorial.")
        
        buttonbox.pack_start(self.backbutton, expand=1, fill=1, padding=2)
        buttonbox.pack_start(self.nextbutton, expand=1, fill=1, padding=2)
        buttonbox.pack_start(self.jumpbutton, expand=1, fill=1, padding=2)
        buttonbox.pack_start(self.savebutton, expand=1, fill=1, padding=2)
        buttonbox.pack_end(self.closebutton, expand=1, fill=1, padding=2)

        self.gtk.connect('destroy', self.closeCB)
        self.gtk.set_default_size(500, 300)

        self.progress = 0  # How far has the tutorial gone?
                           # It's not affected by "Back" command.
        self.index = 0     # which slide?
        self.signalReceived = 0  # Received a signal, if any.
        self.tutor = tutor
        self.newLesson()
        self.tutor.lessons[0].activate()
        self.saved = None  # if saved or not

        switchboard.requestCallbackMain("task finished", self.signalCB)

    def updateGUI(self):
        debug.mainthreadTest()
        self.lesson = self.tutor.lessons[self.index]  # current lesson
        if self.lesson.subject is not None:
            self.subject.set_text(self.lesson.subject)
        else:
            self.subject.set_text("????")
        self.slideIndex.set_text("%d/%d" %
                                 ((self.index+1), len(self.tutor.lessons)))
        
        bfr = self.textview.get_buffer()
        bfr.set_text("")
        comments = Comment(self.lesson.comments)
        width = 500
        height = 300
        lines = 0
        for i in range(len(comments)):
            comment = comments[i]
            font = comments.isBold(i)
            image = comments.isImage(i)
            if font:
                bfr.insert_with_tags(bfr.get_end_iter(), comment, self.boldTag)
            elif image:
		pixbuf = gtk.gdk.pixbuf_new_from_file(imagespath+comment)
		if pixbuf.get_width() > width:
		   width = pixbuf.get_width()
		   
		if pixbuf.get_height() > height:
		   height = pixbuf.get_height()
		bfr.insert_pixbuf(bfr.get_end_iter(), pixbuf)
            else:
                bfr.insert(bfr.get_end_iter(), comment)
                lines = lines + 1
        #bfr.apply_tag(self.centerImageTag, bfr.get_start_iter(), bfr.get_end_iter())
        
        for s in self.scrollsignals:
            s.block()
        self.msgscroll.get_hadjustment().set_value(0.)
        self.msgscroll.get_vadjustment().set_value(0.)
        
        ##self.gtk.resize(50 + width, height + 2 * lines)
        
        for s in self.scrollsignals:
            s.unblock()
        self.sensitize()
        self.gtk.show_all()

    def newLesson(self):
        self.updateGUI()
        self.signalReceived = 0  # Resetting ...

    def sensitize(self):
        debug.mainthreadTest()
        # Back, Jump, Done
        self.backbutton.set_sensitive(self.index != 0)
        self.jumpbutton.set_sensitive(self.index != self.progress)
        # Next
        self.nextbutton.set_sensitive(1)  # Default
        if self.index == self.progress:
            if self.lesson.signal and not self.signalReceived \
                   and not debug.debug():
                self.nextbutton.set_sensitive(0)
        if self.lesson == self.tutor.lessons[-1]:  # the last one?
            self.nextbutton.set_sensitive(0)

    def signalCB(self):
        debug.mainthreadTest()
        if self.lesson != self.tutor.lessons[-1]:
            self.nextbutton.set_sensitive(1)

    def destroy(self):
        self.closeCB()

    def backCB(self, *args):
        self.index -= 1
        self.updateGUI()

    def nextCB(self, *args):
        if self.index == self.progress:  # move forward
            self.tutor.lessons[self.progress].deactivate()
            self.progress += 1
            self.tutor.lessons[self.progress].activate()
            self.index += 1
            self.newLesson()
        else:
            self.index += 1
            self.updateGUI()

    def jumpCB(self, *args):
        self.index = self.progress
        self.updateGUI()

    def saveCB(self, *args):
        filename = fileselector.getFile(
            ident="FileMenu", title="Save Tutorial Session")
        if filename is not None:
            phile = file(filename, "w")
            mainmenu.OOF.saveLog(phile)
            phile.write("OOF.Help.Tutorials.Resume(subject='%s', progress=%d)\n"
                       % (self.tutor.subject, self.progress))
            phile.close()
        self.saved = self.progress  # saved!

    def closeCB(self, *args):
        debug.mainthreadTest()        
        global tutorialInProgress
        if self.gtk:
            tutorialInProgress = None
            mainmenu.OOF.Windows.Tutorial.disable()
            for menuitem in mainmenu.OOF.Help.Tutorials.items:
                menuitem.enable()
            self.gtk.destroy()
            self.gtk = None

    def resume(self, where):
        self.progress = where
        self.index = self.progress
        self.updateGUI()
        self.tutor.lessons[self.progress].activate()

    def savePrintable(self, menuitem, filename, mode):
        file = open(filename, mode.string())
        pageno = 0
        for lesson in self.tutor.lessons:
            comments = Comment(lesson.comments)
            pageno += 1
            print >> file, pageno, lesson.subject
            print >> file               # blank line

            # comments acts like a list of strings, where each string
            # might be formatted differently when displayed in the
            # GUI.  Here we are discarding formatting, so just join
            # all the strings together.
            fulltext = string.join(comments, "")
            # Now split them up according to paragraphs.
            # Comment.__init__, above, inserted '\n\n' at the ends of
            # paragraphs.
            paragraphs = fulltext.split('\n\n')
            # Now print out each paragraph, wrapping to 70 character lines. 
            for paragraph in paragraphs:
                print >> file, textwrap.fill(paragraph)
                print >> file           # blank line
        file.close()
