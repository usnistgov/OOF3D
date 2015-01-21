#!/usr/bin/env python
#   mpirun -np 2 latency.py
import sys, time, os
from math import *
##
## ############### DOCUMENTATION ############### ##
##
## 1. Making the program work:
##
## 1.a. set the PYTHONPATH in your environment variables
## file to wherever oof.py lives. (e.g., )
## For example, in my .cshrc file I wrote:
## setenv PYTHONPATH $PYTHONPATH':/Users/edwin/NIST/OOF2/MPIBUILD'
##
## 1.b. create a soft link from wherever this script lives to
## PYTHONPATH.
## For example, latency.py lives in /Users/edwin/NIST/OOF2/SRC/common/EXTRA
## so I set from PYTHONPATH -- ln -s /Users/edwin/NIST/OOF2/SRC/common/EXTRA/latency.py .
##
## 1.c. Change the permissions for the program, e.g.,
## chmod +x latency.py
##
## 2. In order to make this program work across different machines (platforms)
## use the option -p4pg from  mpirun. For example:
##
## mpirun -p4pg mpiprocgroup -np 2 latency.py
##
## where mpiprocgroup is a file containing the python  *executables* with
## their full path. For example:
##
## adamantium.local 0 /Users/edwin/NIST/OOF2/MPIBUILD/latency.py
## jeeves.nist.gov  1 /users/redwing/OOF2/MPIBUILD/latency.py redwing
##
## would in principle run process zero in adamantium.local (GUI)
## and process 1 in jeeves.
##
## Note that latency.py should be set-up in both adamantium.local AND
## jeeves.nist.gov, in the specified PATHS in order for the example to work.
##
##

## Initialization overhead.
sys.path.append("")
os.chdir("/Users/edwin/NIST/OOF2/MPIBUILD")
import oofcppc ## import this ALWAYS before any swig-generated modules
from ooflib.SWIG.common import mpitools
mpitools.mpi_initialize(sys.argv)
## no need to use mpi_finalize. The modele  at_exit takes care of that.
numproc = mpitools.size()
rank =    mpitools.rank()
name =    mpitools.get_processor_name()
msg = ""
## All processes wait each other here.
mpitools.mpi_barrier()


### GTK classes start HERE ###
class mpiGUI:
  def __init__(self):
    ## create gtk window
    self.window = gtk.GtkWindow(gtk.WINDOW_TOPLEVEL)
    self.window.connect("destroy", self.destroy)
    self.window.set_border_width(10)
    self.window.set_usize(140, 100)
    
    self.control_box = gtk.GtkVBox(gtk.FALSE,0)
    self.window.add(self.control_box)                      
    self.control_box.show()
    
  ## create startbutton
    self.startbutton = gtk.GtkButton("test latency")
    self.startbutton.connect("clicked", self.latencyTime, self.control_box)
    self.control_box.add(self.startbutton)
    self.startbutton.show()

    
  ## create quitbutton
    self.quitbutton = gtk.GtkButton("Quit")
    self.quitbutton.connect("clicked", self.destroy)
    self.control_box.add(self.quitbutton)
    self.quitbutton.show()
    
  ## show the window
  def  mainloop(self):
    self.window.show_all()
    gtk.mainloop()
    
  def destroy(self, *args):
    mpitools.send_string("quit", 1)
    self.window.hide()
    gtk.mainquit()
    ## print "quitting main"
    sys.stdout.flush()
    sys.exit()

  def latencyTime(self, control_box, data=None):
    ## message should be sent here.
    global msg
    msg += 50*" "
    startTime = time.time()
    mpitools.send_string(msg, 1)
    msg = mpitools.receive_string(1)
    endTime = time.time()
    print len(msg), endTime -startTime
    sys.stdout.flush()
    
if numproc < 2:
  mpitools.mpi_abort() ## the whole point is to run in parallel!
  
if rank == 0:
  ## start GUI
  import gtk, time
  localGUI = mpiGUI()
  localGUI.mainloop()
else:
  while 1:
    msg = mpitools.receive_string(0) ## waiting messages from GUI
    if msg == "quit":
      ## print "quitting process", rank
      sys.stdout.flush()
      sys.exit()
      ## mpitools.mpi_abort()
    mpitools.send_string(msg,0)
    ## print msg, " my rank is ", rank, " my name is ", name
    

## no need to use mpi_finalize. at_exit takes care of this implicitly.





