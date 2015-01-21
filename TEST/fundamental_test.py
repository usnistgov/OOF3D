# -*- python -*-
# $RCSfile: fundamental_test.py,v $
# $Revision: 1.7 $
# $Author: langer $
# $Date: 2008/09/07 02:19:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

import unittest, os

class OOF_Fundamental(unittest.TestCase):
    def setUp(self):
        global allWorkers, allWorkerCores
        from ooflib.common.worker import allWorkers, allWorkerCores
    def OrderedDict(self):
        from ooflib.common.utils import OrderedDict
        od = OrderedDict();
        od['a'] = 'hey'
        od['c'] = 'sea'
        od['b'] = 'bee'
        od['d'] = 'dee'
        vals = []
        for key,val in od.items():
            vals.append(val)
        self.assertEqual(vals, ['hey', 'sea', 'bee', 'dee'])
        od.reorder(['a', 'b', 'c'])
        vals = []
        for key,val in od.items():
            vals.append(val)
        self.assertEqual(vals, ['hey', 'bee', 'sea', 'dee'])
        
    def Ordered_Set(self):
        from ooflib.common.utils import OrderedSet
        os1 = OrderedSet([1,3,2,4])
        self.assertEqual([x for x in os1], [1,3,2,4])
        os1.add(1)
        self.assertEqual([x for x in os1], [1,3,2,4])
        self.assert_(3 in os1)
        self.assert_(5 not in os1)
        os1.discard(3)
        self.assertEqual([x for x in os1], [1,2,4])
        os1.discard(3)
        self.assertEqual([x for x in os1], [1,2,4])
        self.assertRaises(KeyError, os1.remove, 3)
        os2 = OrderedSet([4,2,7,1])
        union1 = os1 | os2
        self.assertEqual([x for x in union1], [1,2,4,7])
        union2 = os2 | os1
        self.assertEqual([x for x in union2], [4,2,7,1])
        inter1 = os1 & os2
        self.assertEqual([x for x in inter1], [1,2,4])
        inter2 = os2 & os1
        self.assertEqual([x for x in inter2], [4,2,1])
        self.assertEqual(os1, OrderedSet([1,2,4]))
        self.assertNotEqual(os1, os2)

    def WorkerCleanup(self):
        # Check that worker is destroyed after successful completion
        # of its task.
        from ooflib.SWIG.common import ooferror
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)
        OOF.Help.Debug.NoOp()
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)

    def WorkerException0(self):
        # Check that a worker is destroyed if its task raises an
        # exception in Python.
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)
        self.assertRaises(RuntimeError, OOF.Help.Debug.Error.PyError)
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)
        
    def WorkerException1(self):
        # Check that a worker is destroyed if its task raises an
        # exception in C++.
        from ooflib.SWIG.common import ooferror
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)
        self.assertRaises(ooferror.ErrProgrammingError,
                          OOF.Help.Debug.Error.CError)
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)

    def WorkerException2(self):
        # Check that a worker is destroyed if its task raises a Python
        # exception by calling a Python function from C++.
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)
        self.assertRaises(AttributeError, OOF.Help.Debug.Error.CPyError)
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)

    def WorkerException3(self):
        # Check that a worker is destroyed if its task calls a C++
        # function that calls a Python function that calls a C++
        # function that throws an exception.
        from ooflib.SWIG.common import ooferror
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)
        self.assertRaises(ooferror.ErrProgrammingError,
                          OOF.Help.Debug.Error.CPyCError)
        self.assertEqual(len(allWorkers), 0)
        self.assertEqual(len(allWorkerCores), 0)

def run_tests():
    test_set = [
        OOF_Fundamental("OrderedDict"),
        OOF_Fundamental("Ordered_Set"),
        OOF_Fundamental("WorkerCleanup"),
        OOF_Fundamental("WorkerException0"),
        OOF_Fundamental("WorkerException1"),
        OOF_Fundamental("WorkerException2"),
        OOF_Fundamental("WorkerException3")
        ]
    logan = unittest.TextTestRunner()
    for t in test_set:
        print >> sys.stderr, "\n *** Running test: %s\n" % t.id()
        res = logan.run(t)
        if not res.wasSuccessful():
            return 0
    return 1

###################################################################
# The code below this line should be common to all testing files. #
###################################################################

if __name__=="__main__":
    # If directly run, then start oof, and run the local tests, then quit.
    import sys
    try:
        import oof2
        sys.path.append(os.path.dirname(oof2.__file__))
        from ooflib.common import oof
    except ImportError:
        print >> sys.stderr, "OOF is not correctly installed on this system."
        sys.exit(4)
    sys.argv.append("--text")
    sys.argv.append("--quiet")
    sys.argv.append("--seed=17")
    oof.run(no_interp=1)

    success = run_tests()

    OOF.File.Quit()
    
    if success:
        print "All tests passed."
    else:
        print "Test failure."
