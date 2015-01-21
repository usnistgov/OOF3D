# -*- python -*-
# $RCSfile: subproblemtype.py,v $
# $Revision: 1.3.2.3 $
# $Author: fyc $
# $Date: 2014/04/18 20:00:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import registeredclass
from ooflib.common.IO import xmlmenudump
import sys

# SubProblemType subclasses describe CSubProblem subclass
# instances. Using SubProblem or CSubProblem instances as parameter
# values in OOF.Subproblem.New is a memory leak, because the parameter
# keeps a copy of its value.  Since SubProblems are large objects, and
# tied to their Meshes, that's a bad idea.  SubProblemType is
# lightweight and not tied to a particular Mesh, so it's ok to have an
# extra one live inside the parameter object.

class SubProblemType(registeredclass.RegisteredClass):
    registry = []
    tip = "Different varieties of Subproblems."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/subproblemtype.xml')
    
    def get_dependencies(self):
        # Return the paths (colon separated strings) to the other
        # subproblems on which this one depends. 
        return []
         
    def update_dependency(self, newobject):
        #Update one dependency object
        pass
    def add_dependent(self, dependent):
        #Add the dependent to the dependents
        pass
      
    def remove_dependent(self, dependent):
        #Remove a dependent
        pass
    def get_dependents(self):
        # Return the paths (colon separated strings) to the other
        # subproblems that depends this one. 
        return []
