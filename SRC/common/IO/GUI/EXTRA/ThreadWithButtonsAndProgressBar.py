import sys
import time
import gtk


from threading import Thread

threadcount=0

class ProgressBar:
    ## Esentially an HBox with a bunch of entries
    ## the calback function is esentially thread object that returns
    ## a query_function that is  added to the overall GUI in a stack
    def __init__(self, know_how_far = None):
        ## button defaults
        self.orientation = gtk.PROGRESS_LEFT_TO_RIGHT
        self.style = gtk.PROGRESS_CONTINUOUS
        ## the bar is continuous by default.
        ## It's behaviour is automatically altered if know_how_far < 10 or if know_how_far == None
        self.know_how_far = know_how_far
        if not self.know_how_far:
            self.counter = 0.0
        self.progressbar = None
        self.create_bar()
        

    def progress_discrete(self):
        self.style = gtk.PROGRESS_DISCRETE
        
    
    def create_bar(self):
        ## Here we create the actual bar
        if not self.progressbar :
            self.progressbar = gtk.GtkProgressBar()
            self.progressbar.set_orientation(self.orientation)
            if self.know_how_far:
                if self.know_how_far <= 10 :
                    self.progress_discrete() ## if less than 10 things to do in the thread, make the bar discrete
            else:
                self.back_and_forth_state(gtk.TRUE)
                
            
            self.progressbar.set_bar_style(self.style)
        
        
    def back_and_forth_state(self, val):
        self.progressbar.set_activity_mode(val)
        

    
    def get_bar(self):
        return self.progressbar


    def update(self, value = None):
        if self.know_how_far :
            self.progressbar.update(value)
        else:
            if self.counter< 10.0 :
                self.counter +=1.0
            else:
                self.counter = 0.0
            self.progressbar.update(self.counter/10.0)
            
        
            

    


class Worker (Thread):
    def __init__ (self,widget, bar, thread_id):
        Thread.__init__(self)
        self.widget = widget
        self.bar = bar
        self.thread_id = thread_id
        
    def run (self):
        num_cycles =500.0
        for i in range(num_cycles):
            ## print "<----", self.widget
            # Acquire and release the lock each time.
            gtk.threads_enter()
            self.widget.set_text("Thread number %d - iteration number %d" % (self.thread_id, i+1))
            ## self.bar.update()
            self.bar.update(float(i+1)/num_cycles)
            gtk.threads_leave()
            time.sleep(5./num_cycles)
        self.widget.set_text("No threads running")

def start_new_thread (button, widget, bar, data=None):
    global threadcount
    threadcount += 1
    a = Worker(widget,bar, threadcount)
    a.start()



def destroy(*args):
    window.hide()
    gtk.mainquit()

window = gtk.GtkWindow(gtk.WINDOW_TOPLEVEL)
window.connect("destroy", destroy)
window.set_border_width(10)
window.set_usize(500, 100)

control_box = gtk.GtkVBox(gtk.FALSE,0)
window.add(control_box)                      
control_box.show()

## create label
label = gtk.GtkLabel()
control_box.add(label)
label.set_text("No threads running")
label.show()

## create static bar
a_bar_obj = ProgressBar(100)
a_bar = a_bar_obj.get_bar()
control_box.pack_start(a_bar, gtk.TRUE, gtk.FALSE, 0)
a_bar.show()


## create button
button = gtk.GtkButton("  Start Thread  ")
button.connect("clicked", start_new_thread, label, a_bar_obj)
control_box.add(button)
button.show()



window.show_all()
gtk.threads_enter()
gtk.mainloop()
gtk.threads_leave()
