

import oofcppc
from ooflib.SWIG.common.IO import stopper
from threading import *
import sys
import time
from types import *
import string




class TextProgressBar:
    def __init__(self, type = "continuous", name_top = " "):

        if type == "continuous":
            self.progressbar = stopper.cProgressBar(1, name_top)
        elif type =="active":
            self.progressbar = stopper.cProgressBar(0, name_top)
        elif type =="quiet": ## no display bar
            self.progressbar = stopper.cProgressBar(-1,name_top)
        self.my_stopper = self.progressbar.get_stopper()
        
        
    def stop_it(self, widget):
        self.my_stopper.set_click()
        

    def get_bar(self):
        return self.progressbar

    def get_stopper(self):
        return self.my_stopper
        
    def get_message(self):
        return self.progressbar.get_message()
        
    def update(self,value = None):
        self.progressbar.update(value)

    def set_message(self,text =None):
        if not text:
            text = " "
        self.progressbar.set_message(text);

    def get_fraction(self):
        return self.progressbar.get_fraction()
        
    
    def displaybar(self):
        self.progressbar.print_message()
    
      

        

## Be careful to NOT create any gtk objects in the thread.
## The thread is meant only to update the GUI through passed referenced variables.
        
class Worker (Thread):
    def __init__ (self, widget, thread_id):
        Thread.__init__(self)
        self.widget = widget
        self.thread_id = thread_id
        
        
    def run (self):
        num_cycles =5000
        for i in range(num_cycles):
            if self.widget.my_stopper.quit():
                self.widget.set_message("\nThread aborted\n")
                ## self.widget.displaybar()
                ## time.sleep(0.1)
                return
            time.sleep(0.1)
            ## Here, the progress bar is updated
            self.widget.update(float(i+1)/float(num_cycles))
            ## self.widget.displaybar()
            ## Progress bar update section ends here
            
            

        ## Notify that thread has ended
        ## self.widget.set_message("\nThread finished\n")
        self.widget.displaybar()
        self.widget.my_stopper.set_click()
        time.sleep(0.1)

        


## Debugging code starts here 
        
def start_new_thread ():
    threadcount = activeCount()
    
    ## create text bar
    a_bar_obj = stopper.TextProgressBar("active", "Thread " + str(threadcount))
    the_stopper = a_bar_obj.get_stopper()
    ## create thread
    a = Worker(a_bar_obj, threadcount)
    a.start()
    interrupt = 1
    try:
        while interrupt :
            time.sleep(1)
            a_bar_obj.displaybar()
            if the_stopper.quit():
                interrupt = 0
        a_bar_obj.set_message("\nThread finished\n")
        a_bar_obj.displaybar()
    except KeyboardInterrupt:
        the_stopper.set_click()
        interrupt = 0
        a_bar_obj.set_message("\nThread aborted\n")
        a_bar_obj.displaybar()
        ## print "Just hit ctrl-C! in main"
    

def only_while():
    interrupt = 1
    try:
        while interrupt:
            pass
    except KeyboardInterrupt:
        interrupt = 0
        print "Just hit ctrl-C! in main"
    
## only_while()
start_new_thread()
