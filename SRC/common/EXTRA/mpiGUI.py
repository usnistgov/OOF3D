import gtk, time, sys, os
from ooflib.SWIG.common import mpitools
import clerk




### GTK classes to test MPI/GUI interactions ###
class MpiGUI:
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
    self.startbutton = gtk.GtkButton("perform test")
    self.startbutton.connect("clicked", self.apply_function, self.control_box)
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

  
  def apply_function(self, control_box, data=None):
    ## message should be sent here.
    startTime = time.time()
    msg = "apply function"
    mpitools.send_string(msg, 1) ## tells other processors to execute the function callback
    self.callback()
    msg = mpitools.recieve_string(1) ## waits for processors to send
    endTime = time.time()
    print "processing time=", endTime -startTime
    sys.stdout.flush()

  def add_function(self,f):
    self.callback = f


class MpiAndThreadsGUI(MpiGUI):
  def __init__(self):
    MpiGUI.__init__(self)
    self.thread = None
  def apply_function(self, control_box, data=None):
      ## message should be sent here.
    ##startTime = time.time()
    msg = "apply function"
    mpitools.send_string(msg, 1)
    ## tells other processors to execute the function callback
    ## create and launch thread
    self.thread = clerk.Clerk(self.callback)
    self.thread.start()
    
    
class MpiBroadcastAndTGUI(MpiGUI):
    def __init__(self):
        MpiGUI.__init__(self)
        self.thread = None
        
    def apply_function(self, control_box, data=None):
        msg = "apply function"
        mpitools.broadcast_string(msg, 0) ## args: command and sender
        ## tells other processors to execute the function callback
        ## next: create and launch thread
        self.thread = clerk.Clerk(self.callback)
        self.thread.start()
        
    def destroy(self, *args):
        mpitools.broadcast_string("quit", 0) ## args: command and sender
        self.window.hide()
        gtk.mainquit()
        print "quitting main"
        sys.stdout.flush()
        mpitools.mpi_barrier()
        sys.exit()
