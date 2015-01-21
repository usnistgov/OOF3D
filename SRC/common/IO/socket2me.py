# -*- python -*-
# $RCSfile: socket2me.py,v $
# $Revision: 1.33.18.1 $
# $Author: langer $
# $Date: 2014/05/08 14:38:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

assert False
OBSOLETE

from ooflib.SWIG.common import lock
from ooflib.SWIG.common import mpitools
from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common.IO import menuparser
import errno, os, socket, sys, time, types


# Local buffer and lock for doing socket-like communications between
# threads on process zero.  The buffer lock should be locked
# (acquired) whenever the string is empty, so that attempts to read it
# will block until there is data.
_buffer_lock = lock.SLock()
_buffer = ""
_buffer_lock.acquire()

SSH_TUNNEL = 0  # If boolean-true, then tunnel socket connections over ssh.

# Device for listening to a socket, for use by remote "back end"
# processes.  Implements "getLine" and "getBytes".  Starts an ssh
# process to tunnel the socket from the remote machine to the local
# machine.  When a thread-safe concurrent implementation of MPI2
# exists, it should be used to replace this object.

class SocketInput(menuparser.InputSource):
    # init requires the remote hostname and port.
    connection_attempt_limit = 1000000
    buffer_size = 80
    def __init__(self, host, port, MPIrank):
        local_name = mpitools.Get_processor_name()
        # If the "server" is on the same machine as the SocketInput,
        # then the ssh process can become confused -- hosts don't
        # always know themselves, and there can be name-resolution
        # issues if a host has several interfaces and/or names.  So, in
        # this case, just connect directly.
        if local_name == host:
            self.comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.comm.connect((local_name, port))
        else:
            if SSH_TUNNEL:
                host_name = "127.0.0.1"
                proto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proto.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                proto.bind( (host_name, socket.INADDR_ANY) )
                nearport = proto.getsockname()[1]
                
                # Build and run the appropriate ssh command.
                ssh_cmd = "ssh -L %d:127.0.0.1:%d %s -N" % \
                          (nearport, port, host)
                os.popen2(ssh_cmd)
                proto.close() # Discard the socket.
            else:
                # Non-ssh -- direct connection.
                host_name = host
                nearport = port
                
            c_count = 0
            
            while c_count < SocketInput.connection_attempt_limit:
                try:
                    c_count += 1
                    self.comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.comm.connect( (host_name, nearport) )
                except socket.error, e:
                    if e[0]==errno.ECONNREFUSED: # "Connection refused"
                        self.comm.close()
                        time.sleep(0.1)
                    else:
                        self.comm.close()
                        raise

                else:
                    break
                # If we didn't break out, then we're up to the limit.
            else:
                raise "Connection failure after %d attempts." % c_count
            # At this point, self.comm is the socket, and it's now connected.
            # At all times, self.data is a big string of all the data that
            # has been read but not returned to any caller.
        
        self.comm.send("%05d" % MPIrank)
        self.data = ""

    def __del__(self):
        self.comm.close()

    # Add data to the buffer.
    def _read(self):
        while 1:
            try:
                self.data += self.comm.recv(SocketInput.buffer_size)
            except socket.error, e:
                # If the socket error no. is EINTR (interrupted system call),
                # then just go around again.
                debug.fmsg(e)
                if e[0]!=errno.EINTR:
                    break
            else:
                # If no exceptions of the socket.error instance, then exit.
                break

    # Chops "self.data" at the first "\n" and returns the string,
    # *with* the \n included, modifying self.data in the process.
    # Including the \n emulates the behavior of the file.readline()
    # routine.  Returns None if no \n is found.
    def _cutline(self):
        llist = self.data.split("\n", 1)
        rval = None
        if len(llist)>1:
            rval = llist[0]+"\n" # Restore the carriage return.
            self.data = llist[1]
        return rval
        
    # getLine blocks until it gets a full line.
    def getLine(self):
        # Return a line, if we already have one.
        res = self._cutline()
        if res:
            return res

        # Otherwise, keep reading until it works.
        while 1:
            self._read()
            res = self._cutline()
            if res:
                return res

    # Blocks until it can return all n bytes.  
    def getBytes(self, n):
        if len(self.data)>=n:
            res = self.data[:n]
            self.data = self.data[n:]
            return res
        # Else, as in getLine, keep reading until it works.
        while 1:
            self._read()
            if len(self.data)>=n:
                res = self.data[:n]
                self.data = self.data[n:]
                return res

    def putData(self, data):
        self.comm.send(data)
        

# Object to set up the socketry on the "root" machine.  Startup is a
# two-step process -- you should first instantiate a SocketPort
# object, then query it for its port, and tell all the clients what
# the port is.  Then you can call "connect" on the object, and it will
# create and connect up all the necessary sockets.


class SocketPort:
    buffer_size = 80
    def __init__(self):
        self.comms = {}
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if SSH_TUNNEL: # For ssh-forwards, need to be on the local interface.
            self.listener.bind( ("127.0.0.1", socket.INADDR_ANY) )
        else:
            self.listener.bind( ('', socket.INADDR_ANY) )
        self.port = self.listener.getsockname()[1]
    def getPort(self):
        return self.port
    # Accept exactly n connections.
    def connect(self, n):
        socketlist = []
        self.listener.listen(n)
        count = 0
        while count < n:
            (comm, addr) = self.listener.accept()
            socketlist.append(comm)
            count += 1
        self.listener.close()
        # Get the ranks of all the clients.
        for s in socketlist:
            r_string = s.recv(5)
            rank = int(r_string)
            self.comms[rank]=s
    # Send data to a particular rank recipient, or to all if dest is None.
    def sendBytes(self, bytes, dest=None):
        if dest is not None:
            self.comms[dest].send(bytes)
        else:
            for c in self.comms.values():
                c.send(bytes)

    # Send data, but add a "\n" so recipient's getLine can be used,
    # and will know when to stop.
    def sendLine(self, line, dest=None):
        self.sendBytes(line+"\n", dest)

    # "other" is the rank to get data from, can be zero.  This
    # function will block until there is some data to read, and then
    # return up to buffer_size of it.
    def getData(self, other):
        global _buffer_lock, _buffer
        if other!=0:
            self.comms[other].recv(SocketPort.buffer_size)
        else:
            # For machine 0, that's us, so there's no socket.  Wait
            # for another thread to fill the buffer and clear the lock.
            _buffer_lock.acquire()
            res = _buffer
            # Buffer is empty, so leave lock in acquired state.
            _buffer = ""
            return res

    # __del__ not required, sockets are automatically closed by the
    # Python interpreter at quit time.
            

socketInput = None

def makeSocketInput(host, port, rank):
    global socketInput
    if socketInput is None:
        socketInput = SocketInput(host, port, rank)
    return socketInput

class SocketPipe:
    def __init__(self, scktprt):
        self.socket_port = scktprt
    def close(self):
        pass ## the socket always remains open (bottomless "file")
    def write(self, strng): ## broadcast to all processes the menuitem
        self.socket_port.sendBytes(strng)



def getSocketInput():
    global socketInput
    return socketInput


def socketWrite(data):
    if type(data)==types.StringType:
        global socketInput
        if socketInput is not None:
            # rank != 0, real socket exists, use it.
            socketInput.putData(data)
        else: 
            # rank==0, use the buffer.
            global _buffer_lock, _buffer
            if len(data)>0:
                _buffer += data
                _buffer_lock.release()
                # Buffer is not empty, so leave lock in "released" state.
    else:
        raise ooferror.ErrPyProgrammingError(
            "Non-string data passed to socketWrite.")



def pipeToSocket(menuitem, args, kwargs):
    ## front end encodes a menuitem and its arguments and sends it
    ## to the back end
    global socketPipe
    if mpitools.Rank() == 0:
        binarypipe.startCmd(menuitem) ## grabs the menuitem and encodes it
        for (key, value) in kwargs.items():
            binarypipe.argument(key, value) ## iterate over all the keyword arguments
            ## and encode them
        binarypipe.endCmd() ## Send the encoded data to back end
    else:
        pass




socketPort = None
socketPipe = None
binarypipe = None
if mpitools.Rank() == 0:
    socketPort = SocketPort() ## front end creates a socket input
    socketPipe = SocketPipe(socketPort) ## front end also creates a socket pipe
    ## to send all the menuitems in binary mode
    from ooflib.common.IO.binarydata import BinaryDataFile
    binarypipe = BinaryDataFile(socketPipe)

