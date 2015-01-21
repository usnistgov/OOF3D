# -*- python -*-
# $RCSfile: object_id.py,v $
# $Revision: 1.8.6.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

class ObjectID:
    ## this class stores the information
    ## on what processor owns the writing permissions
    ## of the associated object. This object
    ## also knows the index entry in the list
    ## of the processor that owns it/mantains
    ## it.
    def __init__(self, rank = None, index = None):
        self.rank = rank
        if rank is None:
            rank = -1
        ## self.rank is the processor that owns the
        ## writing permissions
        self.index = index
        if  index is None:
            self.index = -1
        ## self.index corresponds to the index in the list
        ## used in the processor that owns the permissions
        ## to write the SkeletonObject: node, segment, element
    def set_id(self, rnk, index):
        self.rank = rnk
        self.index = index
        if  index is None:
            self.index = -1
    def set_rank(self, rank):
        self.rank = rank
    def set_index(self, index): 
        self.index = index
    def get_id(self):
        return (self.rank, self.index)
    def get_rank(self):
        return self.rank
    def get_index(self):
        return self.index
