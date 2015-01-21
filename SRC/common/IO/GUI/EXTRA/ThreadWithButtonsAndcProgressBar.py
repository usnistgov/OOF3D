

import oofcppc
from ooflib.SWIG.common.IO.stopper import ThreadControl, cProgressBar
from threading import *
import sys
import time
import gtk

threadcount=0 ## Counts the number of launched threads


class ProgressBar:
    def __init__(self, type = "continuous", name_top = " ", name_bottom = " "):
        self.timer = 200 ## in miliseconds
        self.fraction = 0
        self.my_stopper = ThreadControl()
        self.name_top = name_top
        self.name_bottom = name_bottom
        ## button defaults
        self.orientation = gtk.PROGRESS_LEFT_TO_RIGHT
        self.style = gtk.PROGRESS_CONTINUOUS
        ## the bar is continuous by default.
        ## It's behaviour is automatically altered if type =="active" or type =="discrete"
        self.type = type
        if self.type == "active":
            self.counter = 0.0
            
        self.progressbox = None
        self.progressbar = None
        self.label_top = None
        self.label_bottom = None
        
        self.create_bar()
        self.attachGUIcallbacks()

    def progress_discrete(self):
        self.style = gtk.PROGRESS_DISCRETE
        
    
    def create_bar(self):
        ## Here we create the actual bar
        self.destroy_bar = 0
        if not self.progressbox :
            self.progressbox = gtk.GtkVBox(gtk.TRUE, 10)
            
            ## Create the top label, if any
            if self.name_top and not self.label_top:
                self.label_top = gtk.GtkLabel()
                self.label_top.set_text(self.name_top)
                control_box.pack_start(self.label_top, gtk.TRUE, gtk.FALSE, 0)
                self.label_top.show()

            ## Create progress line
            self.progressline = gtk.GtkHBox(gtk.FALSE, 0)
                
            ## Create the progress bar
            self.progressbar = gtk.GtkProgressBar()
            self.progressbar.set_orientation(self.orientation)
            if self.type == "discrete":
                self.progress_discrete() ## if less than 10 things to do in the thread, make the bar discrete
            elif self.type == "active":
                self.back_and_forth_state(gtk.TRUE)
            
                
            
            self.progressbar.set_bar_style(self.style)
            self.progressline.pack_start(self.progressbar, gtk.TRUE, gtk.TRUE, 10)
            self.progressbox.pack_start(self.progressline, gtk.TRUE, gtk.TRUE, 0)
            self.progressbar.show()
            
            ## End of progress bar creation

            
            ## Stop button lives here
            self.stopbutton = gtk.GtkButton("Stop")
            self.stopbutton.connect("clicked", self.stop_it)
            self.progressline.pack_start(self.stopbutton, gtk.TRUE, gtk.TRUE, 20)
            self.stopbutton.show()

            self.progressline.show()
            ## Create the bottom label, if any
            if self.name_bottom and not self.label_bottom:
                self.label_bottom = gtk.GtkLabel()
                ## control_box.add(self.label_bottom)
                self.label_bottom.set_text(self.name_bottom)
                self.progressbox.pack_start(self.label_bottom, gtk.TRUE, gtk.TRUE, 0)
                self.label_bottom.show()

    def stop_it(self, widget):
        self.my_stopper.set_click()
        

    def back_and_forth_state(self, val):
        self.progressbar.set_activity_mode(val)
        
    def schedule_gtk_removal(self):
        self.destroy_bar = 1

    def destroy(self):
        if self.destroy_bar :
            self.progressbar.destroy()
            if self.label_top:
                self.label_top.destroy()
                if self.label_bottom:
                    self.label_bottom.destroy()
            self.progressbox.destroy()
    
    def get_bar(self):
        return self.progressbox

    def get_stopper(self):
        return self.my_stopper

    def update(self, value = None): ## this updates the bar value
        
        if self.type == "continuous" or self.type =="discrete" :
            self.fraction = value
        else:
            if self.counter< 10.0 :
                self.counter +=1.0
            else:
                self.counter = 0.0
            self.fraction = self.counter/10.0
            
    def update_text(self, message_top = " ", message_bottom = " "):
        self.name_top = message_top
        self.name_bottom = message_bottom
        
    def set_text(self, top_text = None, bottom_text = None): ## this updates the text
        if top_text :
            self.label_top.set_text(top_text)
        if bottom_text :
            self.label_bottom.set_text(bottom_text)
        
    def updateBAR(self,value):
        self.progressbar.update(value)

    def updateTEXT(self, message_top, message_bottom):
        self.set_text(message_top, message_bottom)
        
        
    def updateGUI(self):
        self.updateBAR(self.fraction)
        self.updateTEXT(self.name_top, self.name_bottom)
        self.destroy()
        return gtk.TRUE

    def attachGUIcallbacks(self):
        self.bar_tag = gtk.timeout_add(self.timer,self.updateGUI)
        

        

## Be careful to NOT create any gtk objects in the thread.
## The thread is meant only to update the GUI through passed referenced variables.
        
class Worker (Thread):
    def __init__ (self, widget, thread_id):
        Thread.__init__(self)
        self.widget = widget
        self.thread_id = thread_id
        
        
    def run (self):
        num_cycles =250000
        for i in range(num_cycles):
            
            if self.widget.my_stopper.quit():
                self.widget.update_text(" ", "Thread aborted")
                time.sleep(1)
                self.widget.schedule_gtk_removal()
                return
            
            ## Here, the progress bar is updated
            self.widget.update(float(i+1)/float(num_cycles))
            ## Progress bar update section ends here
            
            

        ## Notify that thread has ended
        self.widget.update_text(" ", "Thread finished")
        time.sleep(1)
        ##destruction of label AND bar
        self.widget.schedule_gtk_removal()
        








## Debugging code starts here 
        
def start_new_thread (button, control_box, data=None):
    global threadcount
    
    ## create static bar
    a_bar_obj = ProgressBar("continuous")
    a_bar = a_bar_obj.get_bar()
    control_box.pack_start(a_bar, gtk.FALSE, gtk.FALSE, 0)
    a_bar.show()
    threadcount += 1
    a = Worker(a_bar_obj, threadcount)
    a.start()
    
    print "Number of live threads= ",activeCount() ## this function returns the number of live threads
    


def destroy(*args):
    window.hide()
    gtk.mainquit()


## create gtk window
window = gtk.GtkWindow(gtk.WINDOW_TOPLEVEL)
window.connect("destroy", destroy)
window.set_border_width(10)
window.set_usize(500, 700)

control_box = gtk.GtkVBox(gtk.FALSE,0)
window.add(control_box)                      
control_box.show()


## create startbutton
startbutton = gtk.GtkButton("  Start Thread  ")
startbutton.connect("clicked", start_new_thread, control_box)
control_box.add(startbutton)
startbutton.show()

## create quitbutton
quitbutton = gtk.GtkButton("Quit")
quitbutton.connect("clicked", destroy)
control_box.add(quitbutton)
quitbutton.show()

## show the window
window.show_all()
## gtk.threads_enter()
gtk.mainloop()
## gtk.threads_leave()
