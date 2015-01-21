## Wish list:
## -- Front-end with threaded GUI.
## -- Back-end unthreaded
## -- Exceptions should be issued on the main thread, main process.

## --Each parallelized callback may require an architecture like:

def parallel_callback():
    pre_process_All() ## ALL processors
    if (rank == 0):
        pre_process_MP() ## organize lists. MP
        distribute_work() ## MP sends (menuitems), rest listen
        front_end_work() ## in thread; old callback?? MP
        post_process_MP() ## update lists, sort, optimize. MP
    else:
        receive_work()
        back_end_work() ## old callback ??
        post_process_BE() ## update lists, sort, optimize
    post_process_All()
	   
## --functions could just pass
## --parallel_callback can be a member function of some sort of
## *parallel* worker.

##########################################################################
##########################################################################



## If OOF2 runs with --with-mpi flag enabled:

## ## Startup
## --Main Process (MP) creates a GUI and waits for commands from user
## --Process N loads pertinent modules, and wait for commands from MP.
## --Instantiate the adequate PETSc matrices and vectors by using the 
## adequate macro where necessary

## example of implementation in oof.py:
def run():
    if (args ="with-mpi"):
        from SWIG.common import mpitools
        mpitools.startup_MPI(args)
        rank = mpitools.rank()
        if (rank == 0):
            import GUI
            front_end()
        else:
            ## do not import GUI.
            back_end()
    else:
        serial_run()
	       

##########################################################################
##########################################################################



## ## a. Create Skeleton.
## If microstructure lives only in one processor (main process?):
def pre_process():
    if rank ==0:
        microstructure_bits = split_microstructure(mc)## split microstructure. collective operation
    hash_microstructure = HashMicrostructure(microstructure_bits, rank)
    # DistributedMicrostructure?
    ## create *hash* microstructure object so that we know where the 
    ## actual part of the skeleton actually lives
    send(hash_microstructure, rank) ## send hash object and corresponding bits
    return

def parallel_callback():
    ## Each processor creates a section of the skeleton. 
    ## Compatibility should be maintained by querying the boundary  
    ## elements/nodes.
    ## e.g.,
    if (mpitools.rank() != 0):
        ## processor N:
        for i in range(n_local + 1):
            for j in range(m_local +1):
                local_node = mesh.newNode(j*dx, i*dy)
                hash_node = mesh.newHashNode(j*dx, i*dy)
                ## identify global and local boundary nodes
                ## do other local stuff
        post_process_local() 
        ## -- collective send hash list contribution back to MP.
        ## -- also make point-to-point communications with other
        ## processors to fix boundaries
    else:
        ## MP:
        ## processor N:
        for i in range(n_local + 1):
            for j in range(m_local +1):
                local_node = mesh.newNode(j*dx, i*dy)
                hash_node = mesh.newHashNode(j*dx, i*dy)
                ## identify global and local boundary nodes
                ## do other local stuff
        post_process_local() 
        ## collective operations using  hash list
        post_process_optimize() ## sort list if necessary: exchange 
        ## elements between processes to minimize 
        ## communication later on.

## -- skeleton refinement and anneal should mark hash elements in MP
## and send operators to processors that own the actual objects (not hash)
## -- other interactive operations such as point-click refer to the hash 
## table


##########################################################################
##########################################################################


## ## b. Create FEmesh.
## If skeleton lives only in one processor (main process?):
def pre_process():
    if rank == 0:
        skeleton_bits = split_skeleton(skel)## split skeleton. collective operation
     hash_skel= HashSkeleton(microstructure_bits, rank)## create *hash* skeleton object using serialized 
    ## so that we know where the actual part of 
    ## the skeleton actually lives
    return

def parallel_callback(menuitem, name, skeleton, **kwargs):
    ## Each processor creates a section of the mesh. 
    ## Compatibility should be maintained by querying the boundary 
    ## elements.
    ## e.g.,
    if (rank() != 0):
        ## processor N:
        edict = {}                          # dict to pass to the Skeleton
        for ename, var in kwargs.items():
            n = nsidesFromParamName(ename)   # extract geometry from Parameter name
            if n is not None:
                local_edict[n] = masterelement.getMasterElementFromEnum(var)

        hashskelpath = labeltree.makePath(skeleton) ## get hash skeleton
        ## at this point, hash skeleton should exist
        hashskel = skeletoncontext.skeletonContexts[hashskelpath].getObject()
        

        femesh = hashskel.femesh(local_edict)
        ## At the C++ level, hash.skel.femesh() does the job.
        ## Each processor uses its local list of elements
        ## to make its contribution. Its seems atomic enough to not need
        ## any cross-referencing
        mash = engine.mesh.meshes.add(hashskelpath+[name], femesh,
                                      skeleton=hashskel, elementdict=local_edict)
        
        
	post_process_local() 
	## collective synchronization using hash tables, if any.
        ## operations that require communication are deferred (buffered?)
        ## until this here. 
   else:
       ## MP:
       ## processor N:
        edict = {}                          # dict to pass to the Skeleton
        for ename, var in kwargs.items():
            n = nsidesFromParamName(ename)   # extract geometry from Parameter name
            if n is not None:
                local_edict[n] = masterelement.getMasterElementFromEnum(var)

        hashskelpath = labeltree.makePath(skeleton) ## get hash skeleton
        ## at this point, hash skeleton should exist
        hashskel = skeletoncontext.skeletonContexts[hashskelpath].getObject()
        

        femesh = hashskel.femesh(local_edict)
        ## At the C++ level, hash.skel.femesh() does the job.
        ## Each processor uses its local list of elements
        ## to make its contribution. Its seems atomic enough to not need
        ## any cross-referencing
        mash = engine.mesh.meshes.add(hashskelpath+[name], femesh,
                                      skeleton=hashskel, elementdict=local_edict)
        
        
	post_process_local() 
	## collective synchronization using hash tables, if any.
        ## operations that require communication are deferred (buffered?)
        ## until this here. 
        post_process_local() 
        ## collective synchronization using hash tables, if any.
        ## operations that require communication are deferred (buffered?)
        ## until this here
        post_process_optimize() ## sort list if necessary

   return mash
   ## all processes return hash mesh, with its local REAL contribution




## c. Solve mesh.
## If femesh lives only in one processor (main process):
def pre_process():
    if rank == 0:
        element_bits = split_element(mesh)## order list so cross-comunication is minimized ## main process
    send(element_bits[rank],rank)
    ## split data among different processors. ## collective operation
    return

void FEMesh::make_stiffness() {
    if(stiffness) delete stiffness; //all processors
 
    stiffness = new StiffnessMatrix(this, nodaleqn.size(), dof.size());
    /*
      StiffnesMatrix instantiates a wrapped PETSc sparse matrix.
      It uses the global nodaleqn.size() and global dof.size()
    */
    Material::precompute_all(); //all processors
    for(int i=0; i<element.size() && !localbar->query_stop(); i++) {
        element[i]->make_stiffness(this, *stiffness); 
        //all processors iterate over its local list of elements
  }
    //No need to post_process()
    
    
   

void FEMesh::boundary_rhs_init(int n_global) {
  if (boundary_right_side) {
    delete boundary_right_side;
    // *boundary_right_side = 0.0; // Assigns to all of the elements.
  }
  boundary_right_side = new VECTOR_D(n, 0.0);
  // VECTOR_D is a wrapped PETSc Vector
}

def Solve():
    ## --- PETSc knows what to do on each processor...
    ## the  global PETsc sparse matrix already exists
    ## (see make_stiffness())
    return
   
def quit():
    serial_quit()
    ## Tell all processes is time to quit (send a OOF.Quit() command)
    mpitools.MPI_barrier()
    ## Wait at MPI_Barrier for all processes (including MP),
    ## so that the whole
    ## application exits at unison.



OOF.File.addItem('Quit', callback=quit)

def quit(menuitem):
    if mpi:
        mpi_broadcast('OOFMPI.quit')
    else:
        reallyquit()


OOFMPI = OOFMenu('OOFMPI', no_log=1)           # separate from OOF menu
OOFMPI.addItem('quit', callback=localquit)
def localquit(menuitem):
    reallyquit()
    mpitools.MPI_barrier()  # maybe in worker?


# Remote processors should have a communication thread and a work
# thread, so that they can be interrupted.
