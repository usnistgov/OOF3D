# -*- python -*-
# $RCSfile: reporterror.py,v $
# $Revision: 1.1.4.9 $
# $Author: langer $
# $Date: 2014/09/26 17:35:24 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# Collect information to send as an error report

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.image import oofimage3d as oofimage
from ooflib.common import debug
from ooflib.common import installationLog
from ooflib.common.IO import filenameparam
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
import os
import os.path
import platform
import shutil
import sys
import tarfile
import tempfile
import time

class ReportError:
    def _init_(self):
        self.menu = menu
        self.currentReportError = display.ReportError(whoville.nobody)
        self.currentWhoClass = whoville.noclass
        self.lock = lock.Lock()
    def destroy(self):
        global reportError
        reportError = None

#goes through the reporter messages and collects the python log messages
def getPythonLog(): 
    pythonLog =''
    for m in reporter.messagemanager.all_messages():
	if m[1]=='Log':
	    pythonLog += (m[0]+'\n')
    return pythonLog

# Parses through python log to find files that were inputted/outputed into/out of OOF 
# and seperates those file names based on if they are input, output or have been deleted 
def parseFiles(pythonLog):
    global dirfiles,infiles,outfiles,delfiles, traceback
    infiles=[]
    outfiles=[]
    delfiles=[]
    traceback = None

    for line in getPythonLog().splitlines():
	if line[:3] == 'OOF': #checks if the command comes from a menuitem
	    startindex = 0
	    
	    while line[startindex] != '(':
		startindex += 1
	    menuitem = eval('mainmenu.'+line[:startindex]) #extracts the menuitem name
	    files=[]
	    for parameter in menuitem.params: #goes through the parameters of the menuitem
		
		if parameter.classRepr() == 'ReadFileNameParameter' or parameter.classRepr() == 'RegisteredParameter(ThreeDImageSpecification)': #finds the input file names
		    file=''
		    if parameter.classRepr() == 'RegisteredParameter(ThreeDImageSpecification)':
		       file = parameter.value.directory
		    else:
		       param = parameter.name
		       endindex= startindex+ len(param)
		       # finds the name of the file from the python log instead of extracting it from the
		       # parameter value because the parameter value may have changed
		       while startindex<len(line) and endindex<len(line):
			     if line[startindex:endindex]==param:
				i = endindex+2
				while line[i]!='\'' and i<len(line):
				    i+=1
				file = line[endindex+2:i]
				break
			     endindex +=1  
			     startindex +=1
		    if(file!='' and (not duplicate(file,files)) ):
			if os.path.isfile(file):
			    infiles.append(file)
			    files.append(file)
			elif os.path.isdir(file):
			   infiles.append(file)
			   files.append(file)
			else:
			    delfiles.append(file) #if the file no longer exists, add it to the deleted files list
			    files.append(file)
		
		elif parameter.classRepr() == 'WriteFileNameParameter': #finds the output file names
		    file=''
		    param = parameter.name
		    endindex = startindex + len(param)
		    # finds the name of the file from the python log instead of extracting it from the
		    # parameter value because the parameter value may have changed
		    while startindex<len(line) and endindex<len(line):
			if line[startindex:endindex]== param:
			    i=endindex+2
			    while line[i]!='\'' and i<len(line):
				i+=1
			    file = line[endindex+2:i]
			    break
			endindex += 1  
			startindex += 1
		    if(file!='' and (not duplicate(file,files)) ):
			if os.path.isfile(file):
			    outfiles.append(file)
			    files.append(file)
			elif os.path.isdir(file):
			   infiles.append(file)
			   files.append(file)
			else:
			    delfiles.append(file) #if the file no longer exists, add it to the deleted files list
			    files.append(file)
	

def duplicate(file, list): #checks that a file name is in a list (true)
    for entry in list:
	if entry==file:
	    return True
    return False
	
def getInfiles():
    return infiles
def getOutfiles():
    return outfiles
def getDelfiles():
    return delfiles
def geTraceback():
    return traceback

# tars a directory with all the error report files
def openReportError(menuitem,reporterGUI,filename,pythonlog,pythonlogandoutputs,installationlog,inputfiles,outputfiles,deletedfiles,comments):
    temp_directory= tempfile.mkdtemp(prefix='reporterror')

    dirname = "OOF3Dreport_" + time.strftime("%Y%m%d")
    report_directory=os.path.join(temp_directory, dirname)
    os.makedirs(report_directory)
    notesfile = open(os.path.join(report_directory, 'notes.txt'),'w') 
    
    # system information added to notesfile
    try:
	linux_distribution= platform.linux_distribution()
    except:
	linux_distribution= "N/A"

    notesfile.write("""System Information:
    Python version: %s
    dist: %s
    linux_distribution: %s
    system: %s
    machine: %s
    platform: %s
    uname: %s
    version: %s
    mac_ver: %s\n\n""" % (
    sys.version.split('\n'),
    str(platform.dist()),
    linux_distribution,
    platform.system(),
    platform.machine(),
    platform.platform(),
    platform.uname(),
    platform.version(),
    platform.mac_ver(),
    ))
    
    if (comments != None):
	# if the user has additional comments, add it to notes file
	notesfile.write('User Comments:\n')
	notesfile.write(comments+'\n')
	notesfile.write('\n')
    
    if (pythonlog):
	# add python log to temporary directory as a file 
	with open(os.path.join(report_directory,'pythonlog.txt'),'w') as pythonlogfile:
	    for line in getPythonLog().splitlines():
		pythonlogfile.write(line+'\n')
	    pythonlogfile.close()
    
    if (pythonlogandoutputs):
	# add python log and other outputs to temporary directory as a file 
	with open(os.path.join(report_directory,'pythonlogANDoutputs.txt'),'w') as pythonlogplusfile:
	    for m in reporter.messagemanager.all_messages():
		pythonlogplusfile.write(m[0]+'\n')
	    pythonlogplusfile.close()
	
    if (installationlog):
	# add installation log to temporary directory as a file
	logfilename = 'installation_log.txt'
	file = open(os.path.join(report_directory , logfilename),'w')
	file.write(installationLog.logdata)
	file.close()
	    
    if traceback != None and reporterGUI.tracebackButton.get_active():
       if os.path.isfile(traceback):
	  shutil.copyfile(traceback, os.path.join(report_directory , traceback))
	  notesfile.write('Error traceback: %s\n' %traceback)
    
    finalnames=[] # final file names used in the report directory
    
    if (inputfiles != None):
	# add user input files to the temporary directory and file
	# name to notes file
	notesfile.write("Input File Names:\n")
	for files in inputfiles:
	    num = 1
	    message = ''
	    name = files 
	    # checks if there is a file with the same name but
	    # different path if so, a number is added to the beginning
	    # of the name of the version saved in the report this
	    # change is recorded in the notes file
	    while (duplicate(os.path.basename(name),finalnames)):
		split = os.path.split(name)
		name = os.path.join(split[0],str(num)+split[1])
		message = '(was changed to \''+os.path.basename(name)+'\')'
		num+=1
	    finalnames.append(os.path.basename(name))
	    dest = os.path.join(report_directory , os.path.basename(name))
	    if os.path.isfile(files):
	       shutil.copyfile(files, dest)
	       notesfile.write('\''+files+'\' '+message+'\n')
	    elif os.path.isdir(files):
	       try:
		  shutil.copytree(files, dest)
		  notesfile.write('\''+files+'\' '+message+'\n')
	       except:
		  pass
	    else:
	      pass
	notesfile.write('\n')
	    
    if (outputfiles != None):
	# add user output files to the temporary directory and file
	# name to notes file
	notesfile.write("Output File Names:\n")
	for files in outputfiles:
	    num = 1
	    message = ''
	    name = files 
	    # checks if there is a file with the same name but
	    # different path if so, a number is added to the beginning
	    # of the name of the version saved in the report this
	    # change is recorded in the notes file
	    while (duplicate(os.path.basename(name),finalnames)):
		split = os.path.split(name)
		name = os.path.join(split[0],str(num)+split[1])
		message = '(was changed to \''+os.path.basename(name)+'\')'
		num+=1
	    finalnames.append(os.path.basename(name))
	    dest = os.path.join(report_directory , os.path.basename(name))
	    if os.path.isfile(files):
	       shutil.copyfile(files, dest)
	       notesfile.write('\''+files+'\' '+message+'\n')
	    elif os.path.isdir(files):
	       try:
	          shutil.copytree(files, dest)
	          notesfile.write('\''+files+'\' '+message+'\n')
	       except:
		  pass
	    else:
	       pass
	notesfile.write('\n')
	    
    if (deletedfiles != None):
	#add names of input/output files that have been deleted from
	#the system to the notes file
	notesfile.write("Deleted File Names:\n")
	for files in deletedfiles:
	    notesfile.write('\''+os.path.basename(files)+'\'\n')
	notesfile.write('\n')
    
    notesfile.close()
    
    
    #tars the temporary directory in the location the user wants it saved
    ## Don't change the file name by adding ".tgz" or ".tar.gz".
    ## That'll just be confusing for the user.
    report_tar = tarfile.open(filename,"w:gz")
    report_tar.add(report_directory,os.path.basename(report_directory))
    report_tar.close()
    shutil.rmtree(temp_directory) #removes the temporary directory
    
    reporterGUI.window.destroy()

# end openReportError
    
def newReportError():
    return ReportError

errorreportermenu = mainmenu.OOF.Help.addItem(oofmenu.OOFMenuItem(
    'Report_Error',
    callback= openReportError,
    params=[
        filenameparam.WriteFileNameParameter(
            'filename',tip="Name of the report file."),
        parameter.BooleanParameter(
            'pythonlog', True), 
        parameter.BooleanParameter(
            'pythonlogandoutputs', True),
        parameter.BooleanParameter(
            'installationlog', True),
        parameter.ListOfStringsParameter(
            'inputfiles', tip="Names of input files"),
        parameter.ListOfStringsParameter(
            'outputfiles', tip="Names of output files"),
        parameter.ListOfStringsParameter(
            'deletedfiles',
            tip="Names of input/output files no longer on the system"),
        parameter.StringParameter('comments')],
    no_log=1,
    help ="Choose information to send as an error report"))   

def addInputFile(menuitem, reporter, filename):
    if filename is not None and filename not in infiles:
       filenamePath = os.path.basename(filename)
       infiles.append(filename)
       reporter.update()
    
errorreportermenu.addItem(oofmenu.OOFMenuItem(
    'Add_Input_File',
    callback=addInputFile,
    params=[filenameparam.FileOrDirectoryParameter(
        'filename', ident="add", tip="Name of the input file or directory.")],
    ellipsis=1,
    no_log=1,
    help="Add an input file."))
