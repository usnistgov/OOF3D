#!/usr/bin/env python
#   mpirun -np 4 latency.py
import sys, time, os
from math import *
##
## Note:
## This script will NOT work for a parallel application if your local
## PYTHONPATH in your .cshrc file is not set to be wherever this code
## and oof.py is.
## Also, do not forget to put a soft link from wherever
## this program lives to the PYTHONPATH.
## For example, in my .cshr file I wrote:
## setenv PYTHONPATH $PYTHONPATH':/Users/edwin/NIST/OOF2/MPIBUILD'
##

## Initialization overhead.
import oofcppc ## import this ALWAYS before any swig-generated modules
from ooflib.SWIG.common import mpitools
mpitools.mpi_initialize(sys.argv)
## no need to use mpi_finalize. The modele  at_exit takes care of that.
numproc = mpitools.size()
rank =    mpitools.rank()
name =    mpitools.get_processor_name()

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
    self.startbutton = gtk.GtkButton("send message")
    self.startbutton.connect("clicked", self.send_message, self.control_box)
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
    print "quitting main"
    sys.stdout.flush()
    sys.exit()

  def send_message(self, control_box, data=None):
    ## message should be sent here.
    msg = "Hello world!"
    mpitools.send_string(msg, 1)



if numproc < 2:
  mpitools.mpi_abort() ## the whole point is to run in parallel!
  
if rank == 0:
  ## start GUI
  import gtk
  localGUI = mpiGUI()
  localGUI.mainloop()
else:
  while 1:
    msg = mpitools.recieve_string(0) ## waiting messages from GUI
    if msg == "quit":
      print "quitting process", rank
      sys.stdout.flush()
      sys.exit()
    print msg, " my rank is ", rank, " my name is ", name
    sys.stdout.flush()

## no need to use mpi_finalize. at_exit takes care of this implicitly.





