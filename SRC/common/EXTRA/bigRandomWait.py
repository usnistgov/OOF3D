#!/usr/bin/env python
import sys, time, os, random, math
from math import *
tl = 1.0e-3 ## latency time
tc = 1.0e-6 ## time per-cycle
pn = 2
num_rows = num_cols = pn
numproc = num_rows*num_cols
nds= 10
NumNodes = nds*nds
num_nodes_cols = int(math.sqrt(NumNodes))
SENDWAIT = 0

proc_list = []

## Random Classes

class Node:
  def __init__(self, x, y, rank):
    ## self.pos = (x,y)
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
  dx = dy = 1./math.sqrt(N)
  y=0
  while y<1:
    x=0
    while x<1:
      the_rank = processor_number(x,y)
      nlist.append(Node(x, y, the_rank))
      x += dx
    y +=dy
  return nlist

def print_list(list):
  for nd in list:
    print nd.index


def set_connectivity(nodelist):
  N = len(nodelist)
  global num_nodes_cols
  for i in range(num_nodes_cols): ## row number
    for j in range(num_nodes_cols): ## col number
      I = j+num_nodes_cols*i
      node = nodelist[I]
      ## side neighbors
      
      ## left node
      if j/num_nodes_cols == 0 and (I-1)>0:
        left = nodelist[I-1]
        if left not in node.connected:
          node.add_connected(left)
        if node not in left.connected:
          left.add_connected(node)
      ## right node
      if (I+1) <N and (j+1)/num_nodes_cols == 0:
        right = nodelist[I+1]
        if right not in node.connected:
          node.add_connected(right)
        if node not in right.connected:
          right.add_connected(node)

      ## up-down neighbors
      ## top node
      if I - num_nodes_cols >0 :
        top = nodelist[I-num_nodes_cols]
        if top not in node.connected:
          node.add_connected(top)
        if node not in top.connected:
          top.add_connected(node)
      ## bottom node
      if I + num_nodes_cols<N:
        bottom = nodelist[I+num_nodes_cols]
        if bottom not in node.connected:
          node.add_connected(bottom)
        if node not in bottom.connected:
          bottom.add_connected(node)


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
    self.totalwaits = []



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
            need_other = 1
        else:                           # other.index > node.index
          if self.leastforeignundoneindex is None \
                 or self.leastforeignundoneindex > other.index:
            self.leastforeignundoneindex = other.index
    return need_other ## otherwise we do NOT need another node

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

def _bigSimulation():
  for n in range(2, 5):
     N= (10*n)*(10*n)
     _simulation(N)
  ##for n in range(5, 11):
  ##   N= (10*n)*(10*n)
  ##   _simulation(N)
  ##for n in range(1, 5):
  ##  N= (100*n)*(100*n)
  ##  _simulation(N)
  ##for n in range(5, 11):
  ##  N= (100*n)*(100*n)
  ##  _simulation(N)
     
def _simulation(N):
  global numproc
  global NumNodes
  global proc_list
  global num_nodes_cols
  ## N = NumNodes
  for pNumber in range(2, 15):
    ## N= (100*n)*(100*n)
    nodelist = []
    proc_list = []
    numproc = pNumber*pNumber
    ##print "number of processors", numproc
    ## print N, " nodes"
    num_nodes_cols = int(math.sqrt(N))
    node_list = create_node_list(N)
    set_connectivity(node_list)
    random.shuffle(node_list)
    set_index(node_list)
    proc_list = [Processor(node_list, rnk, SENDWAIT) for rnk in range(numproc)]
    min_index = 0
    counter = 0
    while min_index < N and min_index is not None:
      indexes = []
      for processor in proc_list:
        indexes.append(processor.iter())
        min_index = min(indexes)
      ## end for
      counter += 1
    ## while ends
    max_sends = 0 ## maximum number of sends
    max_shared = 0 ## maximum number of shared nodes
    for prc in proc_list:
      max_sends = max(max_sends,prc.nsends)
      max_shared = max(max_shared, prc.shared())
    average_wait = float(reduce(lambda x,y: x+y,
                                [p.get_total_wait() for p in proc_list]))/float(numproc)
    ## average number of wait cycles per processor
    global FILE
    t_computing = (tl*float(max_sends) + tc*counter)/float(tc*N)
    procratio = float(N)/float(numproc)
    FILE = open("execution_time.txt", 'a')
    FILE2 = open("operations.txt", 'a')
    FILE.write("%f"%procratio+ " %f\n"%t_computing)
    FILE2.write("%i"%N + " %i"%numproc + " %i"%max_sends + " %i "%counter +" %i"%max_shared + " %f\n"%average_wait)
    FILE.close()
    FILE2.close()
    ## clean-up the mess
    del proc_list 
    del nodelist 

_bigSimulation()





