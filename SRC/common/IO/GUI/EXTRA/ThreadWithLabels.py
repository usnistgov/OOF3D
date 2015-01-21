from gtk import *
from threading import *
import time

## launches thread correctly, but does not closes appropriately

class Worker(Thread):
    def __init__ (self, widget):
        Thread.__init__(self)
        self.widget = widget
    
    def run (self):
        for i in range(10):
            threads_enter()
            self.widget.set_text ("Count: %d" % i)
            threads_leave()
            time.sleep(1)
            



win = GtkWindow()
label = GtkLabel()
win.add(label)
win.show_all()

threads_enter()
worker = Worker(label)
worker.start()
mainloop()
threas_leave()
