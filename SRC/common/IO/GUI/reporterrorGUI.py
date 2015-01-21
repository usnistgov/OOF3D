# -*- python -*-
# $RCSfile: reporterrorGUI.py,v $
# $Revision: 1.1.4.9 $
# $Author: langer $
# $Date: 2014/09/26 17:35:25 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common.IO import mainmenu
from ooflib.common.IO import reporter
from ooflib.common.IO import reporterror
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
import gtk
import os
import pango
import time

#TODO: Add tooltips to all parts.

Report_Error=mainmenu.OOF.Help.Report_Error
class ReportErrorGUI(reporterror.ReportError):
    def _init_(self):
	debug.mainthreadTest()
	reporterror.ReportError._init_(self)
        widgetscope.WidgetScope.__init__(self, None)
        
    def update(self):
        if reporterror.traceback != None:
	   self.tracebackButton.show()
	else:
	   self.tracebackButton.hide()
	self.box31.hide()
	self.infilenames= reporterror.getInfiles()
	if len(self.infilenames) > 0:
	    newFile = self.infilenames[-1]
	    already = False
	    for button in self.infilebuttons:
		if button.get_label() == newFile:
		  already = True
		  break
	    if not already:
	      newButton = gtk.CheckButton(newFile)
	      self.infilebuttons.append(newButton)
	      self.box31.pack_start(newButton)
	      newButton.set_active(True)
	      newButton.show()
	self.box31.show()
        
    def okbutton1(self,widget): # window asking if the user wants to save the error report
	
	#saves user comments to the comments parameter of Report_Error
	textbuffer = self.textview.get_buffer()
	comment_text= textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter())
	Report_Error.get_arg('comments').value= comment_text
	
	# sets boolean values for other parameters based on what the user chose
	if(self.pythonLogButton.get_active()):
	    Report_Error.get_arg('pythonlog').value = True
	if(self.pythonplusLogButton.get_active()):
	    Report_Error.get_arg('pythonlogandoutputs').value = True
	if(self.instalLogButton.get_active()):
	    Report_Error.get_arg('installationlog').value = True
	
	
	# makes a list of the files the user wants to include in the report 
	filesIncluded=[]
	for button,filename in zip(self.infilebuttons,self.infilenames):
	    if (button.get_active()):
		filesIncluded.append(filename)
	Report_Error.get_arg('inputfiles').value = filesIncluded
	filesIncluded=[]
	for button,filename in zip(self.outfilebuttons,self.outfilenames):
	    if (button.get_active()):
		filesIncluded.append(filename)
	Report_Error.get_arg('outputfiles').value = filesIncluded
	
	# adds the deleted files if the user chose to do so
	if(self.deletedfilesbutton.get_active()):
	    Report_Error.get_arg('deletedfiles').value = reporterror.getDelfiles()
        # Make a default file name
        Report_Error.get_arg('filename').value = \
               "oof3d_report_" + os.getlogin() + '_' + time.strftime("%Y%m%d")
	    
	if parameterwidgets.getParameters(
                Report_Error.get_arg('filename'),
                title="Save Messages", 
                bottommessage=
                "Save the file then email it to oof_bugs@nist.gov"
                " with the subject \'Error Report\'.  If the report"
                " file is too big for email, please contact us"
                " to arrange an alternate way to send it."):
	    Report_Error.callWithDefaults(reporterGUI=self)
	
    def add_button(self, widget):
        menuitem = reporterror.errorreportermenu.Add_Input_File
	if parameterwidgets.getParameters(
	    title='Select a file and add it to the list of input files',
	    *menuitem.params):
	    menuitem.callWithDefaults(reporter=self)
	   
    def cancelbutton(self,widget,window):
	window.destroy()
    
    def show(self): #the first report error window 
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.window.set_border_width(15)
	self.window.set_title("Report Error")
	
	self.box=gtk.VBox(False,5) #contains all the widgets 
	self.window.add(self.box)
	
	hbox=gtk.HBox()
	self.box.pack_start(hbox)
	label= gtk.Label(
            "Choose what information to include in the error report."
            " The more information you include, the easier it will be"
            " to pinpoint the cause of the error.")
        label.set_line_wrap(True)
	label.modify_font(pango.FontDescription("italic "))
	label.set_alignment(0,0)
	hbox.pack_start(label)
	label.show()
	hbox.show()
	
	# User chooses which logs to include
	label= gtk.Frame('Include:')
	self.box.pack_start(label,False,False,0)
	self.box2 = gtk.VBox(False,2)
	label.add(self.box2)
	self.pythonLogButton=gtk.CheckButton("Python Log")
	self.pythonLogButton.set_active(True)
	self.pythonplusLogButton=gtk.CheckButton("Python Log with Outputs")
	self.pythonplusLogButton.set_active(True)
	self.instalLogButton=gtk.CheckButton("Installation Log")
	self.instalLogButton.set_active(True)
	self.tracebackButton=gtk.CheckButton("Traceback file")
	self.tracebackButton.set_active(True)
	self.box2.pack_start(self.pythonLogButton)
	self.box2.pack_start(self.pythonplusLogButton)
	self.box2.pack_start(self.instalLogButton)
	self.box2.pack_start(self.tracebackButton)
	self.pythonLogButton.show()
	self.pythonplusLogButton.show()
	self.instalLogButton.show()
	self.tracebackButton.hide()
	self.box2.show()
	label.show()
	
	reporterror.parseFiles(reporterror.getPythonLog) # finds all the file calls in pythonlog
	
	#User input files to include
	self.box3= gtk.HBox(False,0)
	label= gtk.Frame('Input Files to Include:')
	self.add_file=gtk.Button(stock=gtk.STOCK_ADD)
	self.add_file.connect("clicked",self.add_button)
	#tooltips.set_tooltip_text(self.add_file, "Allow user to manually add input files.")
	self.box3.pack_start(label,True,True,0)
	self.box3.pack_start(self.add_file, False, False, 0)
	self.add_file.show()
	self.box.pack_start(self.box3, True, True,0)
	self.box31= gtk.VBox(False,2)
	label.add(self.box31)
	self.infilenames= reporterror.getInfiles()
	self.infilebuttons=[]
	for file in self.infilenames:
	    self.infilebuttons.append(gtk.CheckButton(file))   
	for button in self.infilebuttons:
	    self.box31.pack_start(button)
	    button.set_active(True)
	    button.show()	    
	self.box31.show()
	label.show()#show files box
	self.box3.show()
	
	#User output files to include
	label= gtk.Frame('Output Files to Include:')
	self.box.pack_start(label,False,False,0)
	self.box4= gtk.VBox(False,2)
	label.add(self.box4)	
	self.outfilenames= reporterror.getOutfiles()
	self.outfilebuttons=[]
	for file in self.outfilenames:
	    self.outfilebuttons.append(gtk.CheckButton(file))	    
	for button in self.outfilebuttons:
	    self.box4.pack_start(button)
	    button.set_active(True)
	    button.show()	    
	self.box4.show()
	label.show()#show
	
	#Option to include files that have been deleted from the system
	label= gtk.Frame('')
	self.box.pack_start(label)
	self.delfiles = reporterror.getDelfiles()
	files="( "
	i=1
	for file in self.delfiles: #Formatting the files list
	    if (i%2==0):
		file = file+'\n' 
	    files = files+'\''+file+'\' '
	    i+=1
	files= files+')'
	self.deletedfilesbutton = gtk.CheckButton("Include names of input/output files that are no longer in the system:\n"+files)
	self.deletedfilesbutton.set_active(True)
	label.add(self.deletedfilesbutton)
	if(self.delfiles != []):
	    self.deletedfilesbutton.show()
	    label.show()
	
	#Comments Sections
	label=gtk.Frame('Additional Comments:')
	self.box.pack_start(label)
	self.box5= gtk.VBox(False,2)
	hbox= gtk.HBox(False,100)
	label.add(self.box5)
	self.box5.pack_start(hbox)
	text= gtk.Label("What did you do? What went wrong?")
	text.modify_font(pango.FontDescription("italic "))
	text.set_alignment(0,0)
	hbox.pack_start(text,False, False, 0)
	text.show()
	hbox.show()
	scroll = gtk.ScrolledWindow()
	scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	self.textview = fixedwidthtext.FixedWidthTextView()
	scroll.add(self.textview)
	scroll.show()
	self.textview.show()
	self.box5.pack_start(scroll)
	self.box5.show()
	label.show()
	
        self.window.set_default_size(60*gtkutils.widgetCharSize(self.textview), -1)
	
	# OK and CANCEL Buttons
	self.end = gtk.HBox(False,100)
	self.button1=gtk.Button(stock=gtk.STOCK_OK)
	self.button1.connect("clicked",self.okbutton1)
	self.end.pack_start(self.button1, True, True, 0)
	self.button1.show()
	self.button2=gtk.Button(stock=gtk.STOCK_CANCEL)
	self.button2.connect("clicked",self.cancelbutton,self.window)
	self.end.pack_start(self.button2, True, True, 0)
	self.button2.show()
	self.box.pack_start(self.end, True,True,0)
	self.end.show()
	
	self.box.show()
	self.window.show()
        
def newReportError(menuitem):
    reporterror= ReportErrorGUI()
    reporterror.show()
    
# Called from oofGUI "stop" function, which closes all open non-modal
# windows as a precaution.
def destroyReportError():               
    if reporterror.reportError is not None:
        reporterror.reportError.close()

mainmenu.OOF.Help.Report_Error.add_gui_callback(newReportError)
