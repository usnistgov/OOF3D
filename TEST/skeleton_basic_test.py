# -*- python -*-
# $RCSfile: skeleton_basic_test.py,v $
# $Revision: 1.31.10.1 $
# $Author: vrc $
# $Date: 2010/12/03 22:18:27 $

# Test suite for the menu commands under OOF.Skeleton.*
# Namely, New, Simple, Delete, Copy, Rename, Modify, Undo,
# Redo, but not including PinNodes or Boundary, which are done in
# other files.  These basic commands, particularly modify, have
# variability in their results as the code evolves, so they've
# been separated out.

# This file assumes that microstructures, images, and pixel group
# menu items have all been tested and work.

import unittest, os
import memorycheck

class OOF_Skeleton(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        global cskeleton
        from ooflib.SWIG.engine import cskeleton
        global cmicrostructure
        from ooflib.SWIG.common import cmicrostructure
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="skeltest",
            height=20.0, width=20.0)
        OOF.Image.AutoGroup(image="skeltest:small.ppm")

    @memorycheck.check("skeltest")
    def New(self):
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)
        from ooflib.common.IO import parameter
        self.assertRaises(
            parameter.ParameterMismatch,
            OOF.Skeleton.New,
            name="mis:punctuated", microstructure="skeltest",
            x_elements=8,y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        OOF.Skeleton.New(
            name="skeleton", microstructure="skeltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:skeleton"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 81)
        self.assertEqual(skel.nelements(), 64)
        self.assert_(skel.sanity_check())
        
    @memorycheck.check("skeltest")
    def NewTri(self):
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)
        OOF.Skeleton.New(
            name="skeleton", microstructure="skeltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=TriSkeleton(arrangement="conservative",
                                          top_bottom_periodicity=False,
                                          left_right_periodicity=False))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:skeleton"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 81)
        self.assertEqual(skel.nelements(), 128)
        self.assert_(skel.sanity_check())

    @memorycheck.check("skeltest")
    def Delete(self):
        OOF.Skeleton.New(
            name="skeleton", microstructure="skeltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        OOF.Skeleton.Delete(skeleton="skeltest:skeleton")
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)

    @memorycheck.check("skeltest")
    def Simple(self):
        OOF.Skeleton.Simple(
            name="simple", microstructure="skeltest",
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:simple"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nelements(), 22500)
        self.assertEqual(skel.nnodes(), 22801)
        # No sanity check here, because it takes too long.  The simple
        # skeleton uses the same code as the regular skeleton, so
        # checking shouldn't be necessary.

    @memorycheck.check("skeltest")
    def SimpleTri(self):
        OOF.Skeleton.Simple(
            name='simple', microstructure='skeltest',
            skeleton_geometry=TriSkeleton(arrangement='moderate',
                                          left_right_periodicity=False,
                                          top_bottom_periodicity=False))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:simple"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nelements(), 45000)
        self.assertEqual(skel.nnodes(), 22801)
        # No sanity check here, because it takes too long.  The simple
        # skeleton uses the same code as the regular skeleton, so
        # checking shouldn't be necessary.

    @memorycheck.check("skeltest")
    def Copy(self):
        OOF.Skeleton.New(
            name="skeleton", microstructure="skeltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        OOF.Skeleton.Copy(skeleton="skeltest:skeleton",
                          name="copy")
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 2)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:copy"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 81)
        self.assertEqual(skel.nelements(), 64)
        self.assert_(skel.sanity_check())
        OOF.Skeleton.Delete(skeleton="skeltest:copy")

    @memorycheck.check("skeltest")
    def Rename(self):
        OOF.Skeleton.New(
            name="skeleton", microstructure="skeltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        OOF.Skeleton.Rename(skeleton="skeltest:skeleton",
                            name="rename")
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:rename"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 81)
        self.assertEqual(skel.nelements(), 64)
        self.assert_(skel.sanity_check())

    @memorycheck.check("skeltest")
    def Save(self):
        import os, filecmp
        OOF.Skeleton.New(
            name="savetest", microstructure="skeltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        OOF.File.Save.Skeleton(filename="skeleton_save",
                               mode="w", format="ascii",
                               skeleton="skeltest:savetest")
        self.assert_(filecmp.cmp(os.path.join("skeleton_data",
                                              "savetest"),
                                 "skeleton_save"))
        os.remove("skeleton_save")

    @memorycheck.check("skeltest")
    def Load(self):
        OOF.File.Load.Data(filename=os.path.join("skeleton_data",
                                                 "savetest"))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        self.assert_( ["skeltest", "savetest"] in
                      skeletoncontext.skeletonContexts.keys())
        skelctxt = skeletoncontext.skeletonContexts["skeltest:savetest"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 81)
        self.assertEqual(skel.nelements(), 64)
        self.assert_(skel.sanity_check())
        
    @memorycheck.check("skeltest")
    def doModify(self, registration, startfile, compfile, kwargs):
        import os, random
        from ooflib.SWIG.common import crandom
        # Loaded skeleton must be named "modtest".
        OOF.File.Load.Data(filename=os.path.join("skeleton_data", startfile))
        mod = registration(**kwargs)
        random.seed(17)
        crandom.rndmseed(17)
        OOF.Skeleton.Modify(skeleton="skeltest:modtest", modifier=mod)
        skelc = skeletoncontext.skeletonContexts["skeltest:modtest"]
        self.assert_(skelc.getObject().sanity_check())
        # Saving and reloading the Skeleton guarantees that node
        # indices match up with the reference skeleton.  Nodes are
        # re-indexed when a skeleton is saved. (Necessary with new scheme?)
        OOF.File.Save.Skeleton(
            filename="skeleton_mod_test",
            mode="w", format="ascii",
            skeleton="skeltest:modtest")
        OOF.Skeleton.Delete(skeleton="skeltest:modtest")
        OOF.File.Load.Data(filename="skeleton_mod_test")
        # Saved skeleton is named "skelcomp:reference".
        OOF.File.Load.Data(
            filename=os.path.join("skeleton_data",
                                  compfile))
        sk1 = skeletoncontext.skeletonContexts[
            "skeltest:modtest"].getObject()
        sk2 = skeletoncontext.skeletonContexts[
            "skelcomp:reference"].getObject()
        # Tolerance is 1.0e-13, 100x double-precision noise.
        self.assertEqual(sk1.compare(sk2, 1.0e-13), 0)
        os.remove("skeleton_mod_test")
        OOF.Skeleton.Delete(skeleton="skeltest:modtest")
        OOF.Skeleton.Delete(skeleton="skelcomp:reference")
        OOF.Microstructure.Delete(microstructure="skelcomp")

    # This is a modify pass which may be considered preliminary -- the
    # only possible target is "AllNodes", because we do not yet know
    # that we can make selections, or pin nodes, or anything.
    def Modify(self):
        from ooflib.engine import skeletonmodifier
        for r in skeletonmodifier.SkeletonModifier.registry:
            try:
                mods = skel_modify_args[r.name()]
            except KeyError:
                print >> sys.stderr,  "No data for skeleton modifier %s." % r.name()
            else:
                for (startfile, compfile, kwargs) in mods:
                    self.doModify(r, startfile, compfile, kwargs)

            
        

    @memorycheck.check("skeltest")
    def Undo(self):
        from ooflib.engine import skeletoncontext
        OOF.Skeleton.New(
            name="undotest", microstructure="skeltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        sk_context = skeletoncontext.skeletonContexts["skeltest:undotest"]
        sk_0 = sk_context.getObject()
        self.assert_(not sk_context.undoable())
        OOF.Skeleton.Modify(skeleton="skeltest:undotest",
                            modifier=Refine(
            targets=CheckHomogeneity(threshold=0.9),
            criterion=Unconditionally(),
            degree=Trisection(rule_set="conservative")))
        sk_1 = sk_context.getObject()
        self.assert_(sk_context.undoable())
        self.assertNotEqual(id(sk_0),id(sk_1))
        OOF.Skeleton.Undo(skeleton="skeltest:undotest")
        sk_2 = sk_context.getObject()
        self.assertEqual(id(sk_0), id(sk_2))


    @memorycheck.check("skeltest")
    def Redo(self):
        from ooflib.engine import skeletoncontext
        OOF.Skeleton.New(
            name="redotest", microstructure="skeltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        sk_context = skeletoncontext.skeletonContexts["skeltest:redotest"]
        sk_0 = sk_context.getObject()
        OOF.Skeleton.Modify(skeleton="skeltest:redotest",
                            modifier=Refine(
            targets=CheckHomogeneity(threshold=0.9),
            criterion=Unconditionally(),
            degree=Trisection(rule_set="conservative")))
        sk_1 = sk_context.getObject()
        OOF.Skeleton.Undo(skeleton="skeltest:redotest")
        sk_2 = sk_context.getObject()
        OOF.Skeleton.Redo(skeleton="skeltest:redotest")
        self.assertEqual(id(sk_1),id(sk_context.getObject()))
        self.assert_(not sk_context.redoable())

    def tearDown(self):
         pass

# Extra tests that can't be in OOF_Skeleton for one reason or another.

class OOF_Skeleton_Special(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        global microstructure
        from ooflib.common import microstructure
        global oofimage
        from ooflib.SWIG.image import oofimage

    def tearDown(self):
        pass

    # Now that skeletons are known to work, we can test if deleting a
    # microstructure which contains a skeleton does the right thing.
    # This test is pretty much redundant with the tests inserted by
    # the memorycheck decorator.

    def MS_Delete(self):
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="deltest",
            height=20.0, width=20.0)
        OOF.Image.AutoGroup(image="deltest:small.ppm")
        OOF.Skeleton.New(
            name="skeleton", microstructure="deltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        OOF.Microstructure.Delete(microstructure="deltest")
        self.assertEqual(microstructure.microStructures.nActual(), 0)
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)
        self.assertEqual(oofimage.imageContexts.nActual(), 0)
        self.assertEqual(cskeleton.get_globalNodeCount(), 0)
        self.assertEqual(cskeleton.get_globalElementCount(), 0)
        self.assertEqual(cmicrostructure.get_globalMicrostructureCount(), 0)

    # Check that round-off error isn't making nodes that should be on
    # a boundary appear to be off the boundary.  This can't be done as
    # part of the other tests, because it requires a special
    # Microstructure size.  (This bug was reported by Tobias Ziegler
    # in version 2.0.1.)
    
    @memorycheck.check("roundoff")
    def RoundOff(self):
        OOF.Microstructure.New(name='roundoff',
                               width=0.0067400000000000003, # magic number
                               height=0.0067400000000000003,
                               width_in_pixels=10, height_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton', microstructure='roundoff',
            x_elements=22, y_elements=22, # magic number
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        skelctxt = skeletoncontext.skeletonContexts['roundoff:skeleton']
        skel = skelctxt.getObject()
        #  Node 512 on the top boundary should be able to move in x only.
        node = skel.getNode(512)
        print >> sys.stderr,  "x:", node.movable_x(), "y:", node.movable_y()
        self.assert_(node.movable_x() and not node.movable_y())
        # Node 367 on the right boundary should be able to move in y only.
        node = skel.getNode(367)
        self.assert_(node.movable_y() and not node.movable_x())
        
# Data for the skeleton modifier tests.  This is a dictionary indexed by
# skeleton modifier name, and for each modifier, there is a set of
# arguments to supply to the modifier menu item for the test, and the
# name of a file containing correct results for that test.
skel_modify_args = {}
def build_mod_args():
    global skel_modify_args
    skel_modify_args = {
        "Refine" :
        [
        ("modbase", "refine_1",
         { "targets" : CheckHomogeneity(threshold=0.9),
           "criterion" : Unconditionally(),
           "degree" : Trisection(rule_set="conservative"),
           "alpha" : 0.5
           }
         ),
        ("modbase", "refine_2",
         { "targets" : CheckHomogeneity(threshold=0.9),
           "criterion" : Unconditionally(),
           "degree" : Bisection(rule_set="conservative"),
           "alpha" : 0.5
           }
         ),
        ("modgroups","refine_3",
         {"targets" : CheckElementsInGroup(group='elementgroup'),
          "criterion" : Unconditionally(),
          "degree" : Bisection(rule_set="conservative"),
          "alpha" : 0.5
          }
         ),
        ("modgroups","refine_4",
         {"targets" : CheckAllElements(),
          "criterion" : Unconditionally(),
          "degree" : Bisection(rule_set="conservative"),
          "alpha" : 0.5
          }
         ),
        ("modgroups","refine_5",
         {"targets" : CheckAspectRatio(threshold=1.5),
          "criterion" : Unconditionally(),
          "degree" : Bisection(rule_set="conservative"),
          "alpha" : 0.5
          }
         ),
        ("modgroups","refine_6",
         {"targets" : CheckHeterogeneousEdges(threshold=1,
                                              choose_from=FromAllSegments()),
          "criterion" : Unconditionally(),
          "degree" : Bisection(rule_set="conservative"),
          "alpha" : 0.5
          }
         )
        ],
        "Relax" :
        [
        ("modbase", "relax",
         { "alpha" : 0.5,
           "gamma" : 0.5,
           "iterations" : 1
           }
         )
        ],
        "Snap Nodes" :
        [ ("modbase", "snapnodes",
           { "targets" : SnapAll(),
             "criterion" : AverageEnergy(alpha=1.)
             }
           )
          ],
        "Split Quads" :
        [ ("modbase", "splitquads",
           { "targets" : AllElements(),
             "criterion" : AverageEnergy(alpha=0.9),
             "split_how" : GeographicQ2T()
             }
           )
          ],
        "Anneal" :
        [
        ("modbase", "anneal",
         {"targets" : AllNodes(),
          "criterion" : AverageEnergy(alpha=0.6),
          "T" : 0.0,
          "delta" : 1.0,
          "iteration" : FixedIteration(iterations=5)            
          }
         ),
        ("modgroups", "anneal_2",
         {"targets" : NodesInGroup(group='nodegroup'),
          "criterion" : AverageEnergy(alpha=0.6),
          "T" : 0.0,
          "delta" : 1.0,
          "iteration" : FixedIteration(iterations=5)            
          }
         ),
        ("modgroups", "anneal_3",
         {"targets" : FiddleElementsInGroup(group='elementgroup'),
          "criterion" : AverageEnergy(alpha=0.6),
          "T" : 0.0,
          "delta" : 1.0,
          "iteration" : FixedIteration(iterations=5)            
          }
         ),
        ("modgroups", "anneal_4",
         {"targets" : FiddleHeterogeneousElements(threshold=0.95),
          "criterion" : AverageEnergy(alpha=0.6),
          "T" : 0.0,
          "delta" : 1.0,
          "iteration" : FixedIteration(iterations=5)            
          }
         )
        ],
        "Smooth" :
        [ ("modsecond", "smooth",
           {"targets" : AllNodes(),
            "criterion" : AverageEnergy(alpha=0.3),
            "T" : 0.0,
            "iteration" : FixedIteration(iterations=5)
            }
           )
          ],
        "Swap Edges" :
        [ ("modsecond", "swapedges",
           {"targets" : AllElements(),
            "criterion" : AverageEnergy(alpha=0.3)
            }
           )
          ],
        "Merge Triangles" :
        [ ("modsecond", "mergetriangles",
           {"targets" : AllElements(),
            "criterion" : AverageEnergy(alpha=0.3)
            }
           )
          ],
        "Rationalize" :
        [ ("modsecond", "rationalize",
           {"targets" : AllElements(),
            "criterion" : AverageEnergy(alpha=0.3),
            "method" : SpecificRationalization(
        rationalizers=[RemoveShortSide(ratio=5.0),
                       QuadSplit(angle=150),
                       RemoveBadTriangle(acute_angle=30,obtuse_angle=130)])
            }
           )
          ],
        #For snaprefine_3 and snaprefine_5, if we used modgroups,
        #then there would be a difference in results between
        #32 and 64 bit machines.
        "Snap Refine" :
        [
        ("modbase", "snaprefine_1",
         { "targets" : CheckHomogeneity(threshold=0.9),
           "criterion" : Unconditionally(),
           "min_distance" : 0.01,
           }
         ),
        ("modgroups","snaprefine_2",
         {"targets" : CheckElementsInGroup(group='elementgroup'),
          "criterion" : Unconditionally(),
          "min_distance" : 1.0,
          }
         ),
        ("modgroups2","snaprefine_3",
         {"targets" : CheckAllElements(),
          "criterion" : Unconditionally(),
          "min_distance" : 1.0,
          }
         ),
        ("modgroups","snaprefine_4",
         {"targets" : CheckAspectRatio(threshold=1.5),
          "criterion" : Unconditionally(),
          "min_distance" : 0.01,
          }
         ),
        ("modgroups2","snaprefine_5",
         {"targets" : CheckHeterogeneousEdges(threshold=1,
                                              choose_from=FromAllSegments()),
          "criterion" : Unconditionally(),
          "min_distance" : 1.0,
          }
         )
        ]
        }

# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.
def run_tests():
    # Modfiy arguments make use of classes which are not in the
    # namespace until after oof.run() has been called, so they can't
    # be used at import-time.
    build_mod_args()

    skel_set = [
        OOF_Skeleton("New"),
        OOF_Skeleton("NewTri"),        
        OOF_Skeleton("Delete"),
        OOF_Skeleton("Simple"),
        OOF_Skeleton("SimpleTri"),
        OOF_Skeleton("Copy"),
        OOF_Skeleton("Rename"),
        OOF_Skeleton("Save"),
        OOF_Skeleton("Load"),
        OOF_Skeleton("Modify"),
        OOF_Skeleton("Undo"),
        OOF_Skeleton("Redo")
        ]

    special_set = [
        OOF_Skeleton_Special("MS_Delete"),
        OOF_Skeleton_Special("RoundOff")
        ]

    test_set = skel_set + special_set
    
    logan = unittest.TextTestRunner()
    for t in test_set:
        print >> sys.stderr,  "\n *** Running test: %s\n" % t.id()
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
        print "OOF is not correctly installed on this system."
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
