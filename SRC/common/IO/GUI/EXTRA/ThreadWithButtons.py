import sys
import time
import gtk


from threading import Thread

threadcount=0

class Worker (Thread):
    def __init__ (self,widget, thread_id):
        Thread.__init__(self)
        self.widget = widget
        self.thread_id = thread_id
        
    def run (self):
        for i in range(10):
            ## print "<----", self.widget
            # Acquire and release the lock each time.
            gtk.threads_enter()
            self.widget.set_text("Thread number %d - iteration number %d" % (self.thread_id, i+1))
            gtk.threads_leave()
            time.sleep(1)
        self.widget.set_text("No threads running")

def start_new_thread (button, widget, data=None):
    global threadcount
    threadcount += 1
    a = Worker(widget,threadcount)
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
        
label = gtk.GtkLabel()
control_box.add(label)
label.set_text(" No threads at this time")
label.show()

button = gtk.GtkButton("  Start Thread  ")
button.connect("clicked", start_new_thread, label)
control_box.add(button)
button.show()

window.show_all()
gtk.threads_enter()
gtk.mainloop()
gtk.threads_leave()
