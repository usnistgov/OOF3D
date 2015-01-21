#!/usr/bin/env python
#   mpirun -np 2 latency.py
import sys, time, os, random, math
from math import *


##os.chdir("/Users/edwin/NIST/OOF2/MPIBUILD")
##import oofcppc ## import this ALWAYS before any swig-generated modules
##from SWIG.common import mpitools
tl = 1.0e-3 ## latency time
tc = 1.0e-6 ## time per-cycle


pn = 2
num_rows = pn
num_cols = pn
numproc = num_rows*num_cols
nds= 10
NumNodes = nds*nds
num_nodes_cols = int(math.sqrt(NumNodes))
SENDWAIT = 1

proc_list = []

## Random Classes

class Node:
  def __init__(self, x, y, rank):
    self.pos = (x,y)
    self.index = 0
    self.rank = rank
    self.connected = []
    self.sent = 0
    ## sent has two states:
    ## 0: NOT sent
    ## 1: Sent 
  def add_connected(self, node):
    self.connected.append(node)
  def get_rank(self):
    return self.rank
##  def get_index(self):
##    return self.index
  
def processor_number(x, y):
  global num_rows
  global num_cols
  return int(math.floor(num_rows*y) + num_rows*math.floor(num_cols*x))

def random_rank():
  global numproc
  return math.floor(random.uniform(0, numproc))

def random_node(nlist):
  N = len(nlist)
  which = int(math.floor(random.uniform(0,N)))
  return nlist[which]

##def random_int(Nmin, Nmax):
##  return math.floor(random.uniform(Nmin, Nmax+1))

def create_node_list(N):
  nlist = []
##  global num_nodes_rows
##  global num_nodes_cols
  ## for i in range(N):
  ##  nlist.append(Node(i, random_rank()))
##  dx = 1./math.pow(float(N),0.5)
##  dy = 1./math.pow(float(N),0.5)
  dx = dy = 1./math.sqrt(N)
  y=0
  index =0
  while y<1:
    x=0
    while x<1:
      the_rank = processor_number(x,y)
      ## print the_rank
      nlist.append(Node(x, y, the_rank))
      x += dx
      index +=1                         # index isn't used???
    y +=dy
##  print "list size", len(nlist)
  return nlist

def print_list(list):
  for nd in list:
    print nd.index


def set_connectivity(nodelist):
  N = len(nodelist)
##  global num_nodes_rows
  global num_nodes_cols
  ## print num_nodes_cols
  for i in range(num_nodes_cols): ## row number
    for j in range(num_nodes_cols): ## col number
      I = j+num_nodes_cols*i
      node = nodelist[I]
      ## print "setting neighbors of node ", I, " pos=", node.pos
      ## side neighbors
      
      ## left node
      if j/num_nodes_cols == 0 and (I-1)>0:
        left = nodelist[I-1]
        ## print "setting left ", I-1
        if left not in node.connected:
          node.add_connected(left)
        if node not in left.connected:
          left.add_connected(node)
      ## right node
      if (I+1) <N and (j+1)/num_nodes_cols == 0:
        right = nodelist[I+1]
        ## print "setting right ", I+1
        if right not in node.connected:
          node.add_connected(right)
        if node not in right.connected:
          right.add_connected(node)

      ## up-down neighbors
      ## top node
      if I - num_nodes_cols >0 :
        top = nodelist[I-num_nodes_cols]
        ## print "setting top ", I-num_nodes_cols
        if top not in node.connected:
          node.add_connected(top)
        if node not in top.connected:
          top.add_connected(node)
      ## bottom node
      if I + num_nodes_cols<N:
        bottom = nodelist[I+num_nodes_cols]
        ## print "setting bottom ", I+num_nodes_cols
        if bottom not in node.connected:
          node.add_connected(bottom)
        if node not in bottom.connected:
          bottom.add_connected(node)

  ## for i in range(len(nodelist)):
  ##  node = nodelist[i]
  ##  print "node", i, " has # neighbor nodes", len(node.connected)

class Message:
  def __init__(self, node):
    self.node = node                    # subject of the message
    self.procs = []                     # receiving processors
  def interestedProcessor(self, proc):
    self.procs.append(proc)

class Processor:
  def __init__(self, listofnodes, rank, sendwait = 0):
    self.must_send_message = 0
    self.sendwait = sendwait
    self.rank = rank
    self.list = listofnodes
    self.messagebuffer = []             # node moves waiting to be sent out
    self.index = -1
    self.waits = 0

    # leastforeignundoneindex is the smallest index of a node on any
    # remote processor that is waiting to be told the new position of
    # a node on this processor.
    self.leastforeignundoneindex = None

    self.nsends = 0
    self.list_size = len(self.list)
    self.current = self.getnextnode()
    ## print "index at startup=", self.index, "rank=", self.rank
    self.totalwaits = []
##    self.machines = []


  def getnextnode(self):
    self.index += 1
    while self.index < self.list_size : ## if there are still more nodes to process
      candidate = self.list[self.index] ## get next node
      if candidate.get_rank() != self.rank: ## if not the same rank,
        self.index +=1
      else:
        return candidate
    self.flushbuffer(1, exittime=1)

    
  def iter(self):
    if self.current is not None:
      if self.need_other_node(self.current):
        self.waits += 1
        self.flushbuffer(force=1)
      else:
        # process the node...
        self.processnode(self.current)
        self.flushbuffer(force=0)
        self.current = self.getnextnode() # sets self.index
        if self.waits > 0:              # if you have waited to do this node
          self.totalwaits.append(self.waits) # save the wait
          self.waits = 0
    return self.index                 

  def processnode(self, node, exittime=0):
    msg = Message(node)
    for other in node.connected:
      if other.rank != node.rank:
        if other.index > node.index:
          msg.interestedProcessor(proc_list[other.rank])
    if len(msg.procs) > 0:
      self.messagebuffer.append(msg)

  def flushbuffer(self, force, exittime=0):
    if self.messagebuffer:
      if self.sendwait and not force and \
             self.index < self.leastforeignundoneindex \
             and not exittime:
        return
      # The number of messages sent is the number of processors listed
      # in all the Messages, not the number of Messages.
      procdict = {}                     # used to count messages
      for msg in self.messagebuffer:
        msg.node.sent = 1
        for proc in msg.procs:
          procdict[proc] = 1
      if self.waits == 0:
        self.nsends += len(procdict)
      self.messagebuffer = []
      self.leastforeignundoneindex = None
    
  def need_other_node(self, node):
    need_other = 0
    for other in node.connected:
      if other.rank != node.rank:       ## if other node of different rank
        if other.index < node.index:    ## and other node of lower precedence
          if not other.sent:            ## if other node not sent yet
            ## print self.rank, "we need another node", other.index
            need_other = 1
        else:                           # other.index > node.index
          if self.leastforeignundoneindex is None \
                 or self.leastforeignundoneindex > other.index:
            self.leastforeignundoneindex = other.index
    ## print self.rank, "we do not need another node", self.index
    return need_other ## otherwise we do NOT need another node


##  def need_to_wait(self, node):
##    for other in node.connected:
##      if other.rank != node.rank: ## if other node of different rank
##        if other.index > node.index: ## and other node of lower precedence
##          if other.sent != 1: ## if other node not sent yet
##            return 1 ## then we need another node
##    return 0 ## otherwise we do NOT need another node

  def get_waits(self):
    return self.totalwaits ## list of waits

  def get_total_wait(self):
    www = 0
    for thiswait in self.totalwaits:
      www +=thiswait
    return www
  
  def shared(self):
    shrd = {}
    for node in self.list:
      if self.rank == node.rank:
        for con in node.connected:
          if node.rank != con.rank:
            shrd[con] = con
    return len(shrd)

def set_index(nlist):
  index =0
  for node in nlist:
    node.index = index
    index += 1

def _simulation():
  global numproc
  global NumNodes
  global proc_list
  N = NumNodes
  node_list = create_node_list(N)
  set_connectivity(node_list)
  random.shuffle(node_list)
  set_index(node_list)
##  proc_list = []
##  for rnk in range(numproc):
##    proc_list.append(Processor(node_list, rnk, 0))
  proc_list = [Processor(node_list, rnk, SENDWAIT) for rnk in range(numproc)]
  min_index = 0
  counter = 0
  while min_index < N and min_index is not None:
    indexes = []
    for processor in proc_list:
      indexes.append(processor.iter())
      ## print "processor rank ", processor.rank, " index=", processor.index, " wait", processor.waits
      min_index = min(indexes)
    ## print "\n"
    counter += 1
##    print counter, min_index
      ## print indexes
  ## print 'Total # of iterations =', counter
  ## Nsends= float(reduce(lambda x,y: x+y,
  ##               [p.nsends for p in proc_list]))/float(numproc) 
  ## Sumwaits = float(reduce(lambda x,y: x+y,
  ##                        [p.get_total_wait() for p in proc_list]))/float(numproc)
  max_sends = 0
  for prc in proc_list:
    max_sends = max(max_sends,prc.nsends)
  global FILE
##  global FILE2
  t_computing = tl*float(max_sends) + tc*counter
  procratio = float(NumNodes)/float(numproc)
  FILE.write("%f"%procratio+ " %f\n"%t_computing)
##  FILE2.write("%f"%procratio+ " %f\n"%Sumwaits)
  for processor in proc_list:
    print ":::", processor.rank,\
          " wait fraction=", processor.get_total_wait()/float(N),\
          " # of waits", len(processor.totalwaits),\
          " # of sends", processor.nsends, \
          " # of shared nodes", processor.shared()

### GTK classes start HERE ###

class theGUI:
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
    self.startbutton = gtk.GtkButton("test!")
    self.startbutton.connect("clicked", self.test, self.control_box)
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
    self.window.hide()
    gtk.mainquit()
    ## print "quitting main"
    sys.stdout.flush()
    sys.exit()

  def test(self, control_box, data=None):
    _simulation()
    
## main ##  
import gtk, time
FILE = open("execution_time.txt", 'a')
## FILE2 = open("numwaits.txt", "a")
localGUI = theGUI()
localGUI.mainloop()
FILE.close()
## FLIE2.close()
    

## no need to use mpi_finalize. at_exit takes care of this implicitly.


##def send_nodes(nodelist):
##  index_list = []
##  for node in nodelist:
##    index_list.append(node.get_index())
##    index_list.append(node.get_rank())
##  global numproc
##  global rank
##  for dest in numproc:
##    if dest != rank:
##      mpitools.send_vector_of_ints(index_list, dest)
##  connectivity_list = []
##  for node in nodelist:
##    Nnodes = len(node.connected)
##    connectivity_list.append(Nnodes)
##    for nd in node.connected:
##      connectivity_list.append(nd.get_index())
##  for dest in numproc:
##    if dest != rank:
##      mpitools.send_vector_of_ints(connectivity_list, dest)

##def receive_nodes():
##  ## receive global index rank
##  nil = mpitools.receive_vector_of_ints(0)
##  index = 0
##  N = len(nil)
##  node_list = []
  
##  ## create back-end list of nodes
##  while index < N:
##    node_list.append(Node(nil[index], nil[index+1]))
##    index += 2
  
##  ## receive connectivity
##  cnlist = mpitools.receive_vector_of_ints(0)
##  cn_index = 0

##  ## reconstruct connectivity
##  for node in node_list:
##    Nnodes = cnlist[cn_index]
##    cn_index +=1
##    for i in Nnodes:
##      node.add_connected(node_list[ndlist[cn_index]])
##      cn_index += 1    
##  return node_list



