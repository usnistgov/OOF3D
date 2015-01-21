# -*- python -*-
# $RCSfile: parallel_object_manager.py,v $
# $Revision: 1.4.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:54 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug


global_counter = 0

class ParallelObjectManager:
    def __init__(self):
        self.obj_dict = {}
        
    def add(self, obj, id=None):
        global global_counter
        if id is None:
            self.obj_dict[global_counter] = obj
            global_counter +=1
            return global_counter - 1
        else:
           self.obj_dict[id] = obj
           return id
        
    def getObject(self, index):
        return self.obj_dict[index]
    
    def getIndex(self, obj):
        index_val = None
        for index in self.obj_dict.keys():
            if self.obj_dict[index] == obj:
                index_val = index
                break
        return index_val
        
    def delete(self, index):
        del(self.obj_dict[index])
        self.reset_counter()

    def reset_counter(self):
        global global_counter
        while global_counter>0 :
            if self.obj_dict.has_key(global_counter-1) == 1:
                return
            else:
                global_counter -= 1

parallelObjectManager = ParallelObjectManager()
