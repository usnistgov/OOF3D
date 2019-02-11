# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import unittest, os
import memorycheck
from UTILS import file_utils
file_utils.generate = False
reference_file = file_utils.reference_file


class SkeletonModify(unittest.TestCase):
    def setUp(self):
        global skeletoncontext, microstructure
        from ooflib.engine import skeletoncontext
        from ooflib.common import microstructure

    @memorycheck.check()
    def doModify(self, registration, startfile, compfile, kwargs):
        # Loaded Microstructure:Skeleton must be named "5color:skeleton".
        OOF.File.Load.Data(filename=reference_file("skeleton_data", startfile))
        msname = microstructure.microStructures.actualMembers()[0].name()
        skelname = msname + ":skeleton"
        mod = registration(**kwargs)
        # Make sure tests are reproducible by re-seeding the random
        # number generator before each test.
        OOF.Settings.Random_Seed(seed=17)
        OOF.Skeleton.Modify(skeleton=skelname, modifier=mod)
        skelc = skeletoncontext.skeletonContexts[skelname]
        OOF.Help.Debug.Sanity_Check(skeleton=skelname, quick=False)
        self.assert_(skelc.sane)
        OOF.File.Save.Skeleton(
            filename="skeleton_mod_test",
            mode="w", format="ascii",
            skeleton=skelname)
        errdata = skelc.getObject().checkCategoryVolumes()
        self.assert_(errdata.avgError() < 1.e-10)


        ## Keep this commented-out block, which might be useful if the
        ## homogeneity calculation changes again.  CSkeleton::compare2
        ## is available only when oof3d is compiled in debug mode.
        # # Use CSkeleton::compare2 to check that changes to the element
        # # homogeneity calculation have made only trivial changes to
        # # the skeleton.  If compare2 returns "OK!" but the following
        # # fp_file_compare fails, it's probably safe to replace the
        # # reference file with skeleton_mod_test and carry on.
        # OOF.Microstructure.Rename(microstructure='5color', name='modified')
        # OOF.File.Load.Data(filename=reference_file("skeleton_data", compfile))
        # skelc0 = skeletoncontext.skeletonContexts['modified:skeleton']
        # skelc1 = skeletoncontext.skeletonContexts['5color:skeleton']
        # print "Results from compare2:"
        # print skelc0.getObject().compare2(skelc1.getObject())
        # OOF.Microstructure.Delete(microstructure='modified')
        
        self.assert_(file_utils.fp_file_compare(
                "skeleton_mod_test",
                os.path.join("skeleton_data", compfile),
                1.e-13
                ))
        file_utils.remove("skeleton_mod_test")
        OOF.Microstructure.Delete(microstructure=msname)

    def Modify(self):
        from ooflib.SWIG.engine import cskeletonmodifier
        for r in cskeletonmodifier.CSkeletonModifier.registry:
            try:
                mods = skel_modify_args[r.name()]
            except KeyError:
                print >> sys.stderr, ("No data for skeleton modifier %s." 
                                      % r.name())
            else:
                print >> sys.stderr, "*** Testing skeleton modifier", r.name()
                for (startfile, compfile, kwargs) in mods:
                    self.doModify(r, startfile, compfile, kwargs)
                    

# Data for the skeleton modifier tests.  This is a dictionary indexed by
# skeleton modifier name, and for each modifier, there is a set of
# arguments to supply to the modifier menu item for the test, and the
# name of a file containing correct results for that test.
skel_modify_args = {}
def build_mod_args():
    global skel_modify_args
    skel_modify_args = {
        "Refine" :
        # Pairs of tests with 'True' and 'False' in their
        # names differ only in the refinement criteria.  The
        # 'False' tests have a criterion which is never met,
        # so no refinement is done.
        
        [
            ("base_skel_refine", "refine_1True",
             {"targets" : CheckAllElements(),
              "criterion" : Unconditionally(),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_2True",
             {"targets" : CheckAllElements(),
              "criterion" : MinimumVolume(threshold=10.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_2False",
             {"targets" : CheckAllElements(),
              "criterion" : MinimumVolume(threshold=50.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_3True",
             {"targets" : CheckAllElements(),
              "criterion" : MinimumVolume(threshold=10.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_3False",
             {"targets" : CheckAllElements(),
              "criterion" : MinimumVolume(threshold=50.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_4True",
             {"targets" : CheckAllElements(),
              "criterion" : MinimumVolume(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_4False",
             {"targets" : CheckAllElements(),
              "criterion" : MinimumVolume(threshold=50.0, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_5True",
             { "targets" : CheckHomogeneity(threshold=1.0),
               "criterion" : Unconditionally(),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_5False",
             { "targets" : CheckHomogeneity(threshold=0.4),
               "criterion" : Unconditionally(),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_6True",
             {"targets" : CheckHomogeneity(threshold=1.0),
              "criterion" : MinimumVolume(threshold=10.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_6False",
             {"targets" : CheckHomogeneity(threshold=1.0),
              "criterion" : MinimumVolume(threshold=50.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_7True",
             {"targets" : CheckHomogeneity(threshold=1.0),
              "criterion" : MinimumVolume(threshold=10.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_7False",
             {"targets" : CheckHomogeneity(threshold=1.0),
              "criterion" : MinimumVolume(threshold=50.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_8True",
             {"targets" : CheckHomogeneity(threshold=1.0),
              "criterion" : MinimumVolume(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_8False",
             {"targets" : CheckHomogeneity(threshold=1.0),
              "criterion" : MinimumVolume(threshold=50.0, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine","refine_9True",
             {"targets" : CheckElementsInGroup(group='egroup'),
              "criterion" : Unconditionally(),
              "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_10True",
             {"targets" : CheckElementsInGroup(group='egroup'),
              "criterion" : MinimumVolume(threshold=10.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_10False",
             {"targets" : CheckElementsInGroup(group='egroup'),
              "criterion" : MinimumVolume(threshold=50.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_11True",
             {"targets" : CheckElementsInGroup(group='egroup'),
              "criterion" : MinimumVolume(threshold=10.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_11False",
             {"targets" : CheckElementsInGroup(group='egroup'),
              "criterion" : MinimumVolume(threshold=50.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_12True",
             {"targets" : CheckElementsInGroup(group='egroup'),
              "criterion" : MinimumVolume(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_12False",
             {"targets" : CheckElementsInGroup(group='egroup'),
              "criterion" : MinimumVolume(threshold=50.0, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine","refine_13True",
             {"targets" : CheckAllElements(),
              "criterion" : Unconditionally(),
              "alpha" : 0.5}),

            ("base_skel_refine", "refine_17True",
             { "targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromAllSegments()),
               "criterion" : Unconditionally(),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_17False",
             { "targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromAllSegments()),
               "criterion" : Unconditionally(),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_171True",
             { "targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromAllSegments()),
               "criterion" : MinimumLength(threshold=5.0, unit='Voxel'),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_171False",
             { "targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromAllSegments()),
               "criterion" : MinimumLength(threshold=5.0, unit='Voxel'),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_172True",
             { "targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromAllSegments()),
               "criterion" : MinimumLength(threshold=5.0, unit='Physical'),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_172False",
             { "targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromAllSegments()),
               "criterion" : MinimumLength(threshold=5.0, unit='Physical'),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_173True",
             { "targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromAllSegments()),
               "criterion" : MinimumLength(threshold=0.002, unit='Fractional'),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_173False",
             { "targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromAllSegments()),
               "criterion" : MinimumLength(threshold=0.002, unit='Fractional'),
               "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_18True",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromSelectedSegments()),
              "criterion" : Unconditionally(),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_18False",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromSelectedSegments()),
              "criterion" : Unconditionally(),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_181True",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromSelectedSegments()),
              "criterion" : MinimumLength(threshold=5.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_181False",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromSelectedSegments()),
              "criterion" : MinimumLength(threshold=5.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_182True",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromSelectedSegments()),
              "criterion" : MinimumLength(threshold=5.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_182False",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromSelectedSegments()),
              "criterion" : MinimumLength(threshold=5.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_183True",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromSelectedSegments()),
              "criterion" : MinimumLength(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_183False",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromSelectedSegments()),
              "criterion" : MinimumLength(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_19True",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromSelectedElements()),
              "criterion" : Unconditionally(),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_19False",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromSelectedElements()),
              "criterion" : Unconditionally(),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_191True",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromSelectedElements()),
              "criterion" : MinimumLength(threshold=5.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_191False",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromSelectedElements()),
              "criterion" : MinimumLength(threshold=5.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_192True",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromSelectedElements()),
              "criterion" : MinimumLength(threshold=5.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_192False",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromSelectedElements()),
              "criterion" : MinimumLength(threshold=5.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_193True",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1.0, choose_from=FromSelectedElements()),
              "criterion" : MinimumLength(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_193False",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=0.4, choose_from=FromSelectedElements()),
              "criterion" : MinimumLength(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine","refine_20True",
             {"targets" : CheckSelectedEdges(),
              "criterion" : Unconditionally(),
              "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_21True",
             {"targets" : CheckSelectedEdges(),
              "criterion" : MinimumLength(threshold=5.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_21False",
             {"targets" : CheckSelectedEdges(),
              "criterion" : MinimumLength(threshold=50.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_22True",
             {"targets" : CheckSelectedEdges(),
              "criterion" : MinimumLength(threshold=5.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_22False",
             {"targets" : CheckSelectedEdges(),
              "criterion" : MinimumLength(threshold=50.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_23True",
             {"targets" : CheckSelectedEdges(),
              "criterion" : MinimumLength(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_23False",
             {"targets" : CheckSelectedEdges(),
              "criterion" : MinimumLength(threshold=50.0, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine","refine_24True",
             {"targets" : CheckSegmentsInGroup(group='sgroup'),
              "criterion" : Unconditionally(),
              "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_25True",
             {"targets" : CheckSegmentsInGroup(group='sgroup'),
              "criterion" : MinimumLength(threshold=5.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_25False",
             {"targets" : CheckSegmentsInGroup(group='sgroup'),
              "criterion" : MinimumLength(threshold=50.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_26True",
             {"targets" : CheckSegmentsInGroup(group='sgroup'),
              "criterion" : MinimumLength(threshold=5.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_26False",
             {"targets" : CheckSegmentsInGroup(group='sgroup'),
              "criterion" : MinimumLength(threshold=50.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_27True",
             {"targets" : CheckSegmentsInGroup(group='sgroup'),
              "criterion" : MinimumLength(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_27False",
             {"targets" : CheckSegmentsInGroup(group='sgroup'),
              "criterion" : MinimumLength(threshold=50.0, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_28True",
             { "targets" : CheckSelectedFaces(),
               "criterion" : Unconditionally(),
               "alpha" : 0.5}),

            ("base_skel_refine", "refine_29True",
             {"targets" : CheckSelectedFaces(),
              "criterion" : MinimumArea(threshold=10.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_29False",
             {"targets" : CheckSelectedFaces(),
              "criterion" : MinimumArea(threshold=50.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_30True",
             {"targets" : CheckSelectedFaces(),
              "criterion" : MinimumArea(threshold=10.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_30False",
             {"targets" : CheckSelectedFaces(),
              "criterion" : MinimumArea(threshold=50.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine","refine_31True",
             {"targets" : CheckSelectedFaces(),
              "criterion" : MinimumArea(threshold=0.002, unit='Fractional'),
              "alpha" : 0.5}),
            
            ("base_skel_refine","refine_31False",
             {"targets" : CheckSelectedFaces(),
              "criterion" : MinimumArea(threshold=50.0, unit='Fractional'),
              "alpha" : 0.5}),
            
            ("base_skel_refine", "refine_32True",
             {"targets" : CheckFacesInGroup(group='fgroup'),
              "criterion" : Unconditionally(),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_33True",
             {"targets" : CheckFacesInGroup(group='fgroup'),
              "criterion" : MinimumArea(threshold=10.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_33False",
             {"targets" : CheckFacesInGroup(group='fgroup'),
              "criterion" : MinimumArea(threshold=50.0, unit='Voxel'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_34True",
             {"targets" : CheckFacesInGroup(group='fgroup'),
              "criterion" : MinimumArea(threshold=10.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_34False",
             {"targets" : CheckFacesInGroup(group='fgroup'),
              "criterion" : MinimumArea(threshold=50.0, unit='Physical'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_35True",
             {"targets" : CheckFacesInGroup(group='fgroup'),
              "criterion" : MinimumArea(threshold=0.002, unit='Fractional'),
              "alpha" : 0.3}),
            
            ("base_skel_refine", "refine_35False",
             {"targets" : CheckFacesInGroup(group='fgroup'),
              "criterion" : MinimumArea(threshold=50.0, unit='Fractional'),
              "alpha" : 0.3})
        ],
        # "Relax" :
        #     [
        #     ("modbase", "relax",
        #      { "alpha" : 0.5,
        #        "gamma" : 0.5,
        #        "iterations" : 1
        #        }
        #      )
        #     ],

        "Snap Nodes" :
        [ 
            ("modbase", "snapnodes",
             {"targets" : SnapAll(),
              "criterion" : AverageEnergy(alpha=1.)}
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
            ("modgroups2", "anneal_2",
             {"targets" : NodesInGroup(group='#5959f3'),
              "criterion" : AverageEnergy(alpha=0.7),
              "T" : 0.0,
              "delta" : 1.0,
              "iteration" : FixedIteration(iterations=50)            
              }
             ),
            ("modgroups_bg", "anneal_3",
             {"targets" : FiddleElementsInGroup(group='#a1fc93'),
              "criterion" : AverageEnergy(alpha=0.7),
              "T" : 0.0,
              "delta" : 0.25,
              "iteration" : FixedIteration(iterations=20)            
              }
             ),
            ("modgroups", "anneal_4",
             {"targets" : FiddleHeterogeneousElements(threshold=0.95),
              "criterion" : AverageEnergy(alpha=0.8),
              "T" : 0.0,
              "delta" : 1.0,
              "iteration" : FixedIteration(iterations=10)            
              }
             )
            ],
        "Smooth" :
            [ 
            ("annealed", "smooth0",
             {"targets" : AllNodes(),
                "criterion" : AverageEnergy(alpha=0.0),
                "T" : 0.0,
                "iteration" : FixedIteration(iterations=5)
                }
             ),
            ("annealed", "smooth1",
             {"targets" : AllNodes(),
              "criterion" : AverageEnergy(alpha=0.7),
              "T" : 0.0,
              "iteration" : FixedIteration(iterations=5)
              }
             ),
            ],
        "Surface Smooth" :
            [
            ("modgroups_bg", "surfacesmooth1",
             {"criterion" : AverageEnergy(alpha=1),
              "T" : 0.0,
              "gamma" : 0.1,
              "iteration" : FixedIteration(iterations=20)
              }
             ),
            ("modgroups_bg", "surfacesmooth2",
             {"criterion" : AverageEnergy(alpha=0.6),
              "T" : 0.0,
              "gamma" : 0.1,
              "iteration" : FixedIteration(iterations=20)
              }
             ),
            ],
        "Rationalize" :
        ## TODO 3.1: Add more Rationalization tests that are designed
        ## to trigger specific parts of the rationalization code.
        ## This will be hard to do without commenting out the parts of
        ## the code that you don't want to use.
            [
                ("bad.skel", "rationalize",
                 {"targets" : AllElements(),
                  "criterion" : AverageEnergy(alpha=0.3),
                  "method" : SpecificRationalization(
                      rationalizers=[RemoveBadTetrahedra(acute_angle=15,
                                                         obtuse_angle=150)])
              }
             ),
                ("bad.skel", "rationalize2",
                 {"targets" : AllElements(),
                  "criterion" : AverageEnergy(alpha=0.3),
                  "method" : AutomaticRationalization()
              }
             )
            ],
        "Snap Refine" :
            [
            # Snaprefine a 1x1x1 skeleton on the simple bluegreen image.
            ("bluegreen111", "snaprefine_bg1",
             {"targets" : CheckHomogeneity(threshold=1),
              "criterion" : Unconditionally(),
              "min_distance" : 0.01,
              "alpha" : 0.3
              }
             ),
            # Snaprefine the bluegreen image, but rotated by 90
            # degrees.
            ("bluegreen111_2", "snaprefine_bg2",
             {"targets" : CheckHomogeneity(threshold=1),
              "criterion" : Unconditionally(),
              "min_distance" : 0.01,
              "alpha" : 0.3
              }
             ),
            # Check that the min_distance param is working.  A large
            # value prevents some elements from being refined.  The
            # critical value is min_distance=1, since some nodes are 1
            # pixel away from the blue/green boundary.
            ("bluegreen444", "snaprefine_bg3",
             {"targets" : CheckHomogeneity(threshold=1),
              "criterion" : Unconditionally(),
              "min_distance" : 1.1, # large
              "alpha" : 0.3
              }
             ),
            ("bluegreen444", "snaprefine_bg4",
             {"targets" : CheckHomogeneity(threshold=1),
              "criterion" : Unconditionally(),
              "min_distance" : 0.9, # small
              "alpha" : 0.3
              }
             ),
            # More complicated snaprefines...
            ("modbase", "snaprefine_1",
             { "targets" : CheckHomogeneity(threshold=0.9),
               "criterion" : Unconditionally(),
               "min_distance" : 0.01,
               "alpha" : 0.3
               }
             ),
            ("modgroups","snaprefine_2",
             {"targets" : CheckElementsInGroup(group='elementgroup'),
              "criterion" : Unconditionally(),
              "min_distance" : 0.5,
              "alpha" : 0.3
              }
             ),
            ("modgroups","snaprefine_3",
             {"targets" : CheckAllElements(),
              "criterion" : Unconditionally(),
              "min_distance" : 0.01,
              "alpha" : 0.3
              }
             ),

            ## Uncomment after implementing CheckAspectRatio in 3D
            # ("modgroups","snaprefine_4",
            #  {"targets" : CheckAspectRatio(threshold=1.5),
            #   "criterion" : Unconditionally(),
            #   "min_distance" : 0.01,
            #   }
            #  ),
                
            ("modgroups","snaprefine_5",
             {"targets" : CheckHeterogeneousEdges(
                 threshold=1, choose_from=FromAllSegments()),
              "criterion" : Unconditionally(),
              "min_distance" : 0.1,
              "alpha" : 0.3
              }
             ),
            ]
        # "Swap Edges" :
        #     [ ("modsecond", "swapedges",
        #        {"targets" : AllElements(),
        #         "criterion" : AverageEnergy(alpha=0.3)
        #         }
        #        )
        #       ],
        # "Merge Triangles" :
        #     [ ("modsecond", "mergetriangles",
        #        {"targets" : AllElements(),
        #         "criterion" : AverageEnergy(alpha=0.3)
        #         }
        #        )
        #       ],
        }

    # skel_modify_args = {
    #     "Anneal" :
    #     [
    #         ("modgroups_bg", "anneal_3",
    #          {"targets" : FiddleElementsInGroup(group='#a1fc93'),
    #           "criterion" : AverageEnergy(alpha=0.7),
    #           "T" : 0.0,
    #           "delta" : 0.25,
    #           "iteration" : FixedIteration(iterations=20)            
    #          }
    #         ),
    #     ],
    # }
        
    

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Skeleton_Save(unittest.TestCase):
  def setUp(self):
      global skeletoncontext
      from ooflib.engine import skeletoncontext
      OOF.Settings.Random_Seed(seed=23)
        
  def tearDown(self):
      pass
  
  def skelContext(self, skelname):
      return skeletoncontext.skeletonContexts[skelname]
        
  def selectedElements(self, skelname):
      return self.skelContext(skelname).elementselection.retrieveSize()
  
  def selectedFaces(self, skelname):
      return self.skelContext(skelname).faceselection.retrieveSize()
  
  def selectedSegments(self, skelname):
      return self.skelContext(skelname).segmentselection.retrieveSize()
  
  def selectedNodes(self, skelname):
      return self.skelContext(skelname).nodeselection.retrieveSize()
      
  def elements(self, skelname):
      return [el.getIndex()
              for el in self.skelContext(skelname).elementselection.retrieve()]
  
  def faces(self, skelname):
      return [tuple(n.getIndex() for n in fa.getNodes()) 
              for fa in self.skelContext(skelname).faceselection.retrieve()]
  
  def segments(self, skelname):
      return [tuple(n.getIndex() for n in se.getNodes())
              for se in self.skelContext(skelname).segmentselection.retrieve()]
  
  def nodes(self, skelname):
      return [no.getIndex()
              for no in self.skelContext(skelname).nodeselection.retrieve()]
  
  def elementsGroupSize(self, skelname):
      return self.skelContext(skelname).nodeselection.retrieveSize()
  
  def facesGroupSize(self, skelname):
      return self.skelContext(skelname).faceselection.retrieveSize()
  
  def segmentsGroupSize(self, skelname):
      return self.skelContext(skelname).segmentselection.retrieveSize()
  
  def nodesGroupSize(self, skelname):
      return self.skelContext(skelname).nodeselection.retrieveSize()
   
  def assertSavedEqual2Loaded(self, skelname, loadedeles, loadedfacs,
                              loadedsegs, loadednods):
    beforeeles = [el.getIndex()
	      for el in self.skelContext(skelname).elementselection.retrieve()]
    self.assertEqual(beforeeles, loadedeles)
    beforefacs =  [tuple(n.getIndex() for n in fa.getNodes())
	      for fa in self.skelContext(skelname).faceselection.retrieve()]
    self.assertEqual(beforefacs, loadedfacs)
    beforesegs =  [tuple(n.getIndex() for n in se.getNodes())
	      for se in self.skelContext(skelname).segmentselection.retrieve()]
    self.assertEqual(beforesegs, loadedsegs)
    beforenods = [no.getIndex()
	      for no in self.skelContext(skelname).nodeselection.retrieve()]
    self.assertEqual(beforenods, loadednods)
    
  def selectComponents1(self, skelname):
      # Select components from the unrefined 4x4x4 skeleton
      OOF.ElementSelection.Select(
          skeleton=skelname,
          method=SingleElementSelect(element=215,operator=Select()))
      OOF.FaceSelection.Select(
           skeleton=skelname,
          method=SingleFaceSelect(nodes=[79, 104, 103],operator=Select()))
      OOF.SegmentSelection.Select(
          skeleton=skelname,
          method=SingleSegmentSelect(nodes=[103, 108],operator=Select()))
      OOF.NodeSelection.Select(
          skeleton=skelname,
          method=SingleNodeSelect(point=Coord(5,5,5),operator=Select()))

  def selectComponentsRefined(self, skelname):
      OOF.ElementSelection.Select(
          skeleton=skelname,
          method=SingleElementSelect(element=583,operator=Select()))
      OOF.SegmentSelection.Select(
          skeleton=skelname,
          method=SingleSegmentSelect(nodes=[470, 108],operator=Select()))
      OOF.FaceSelection.Select(
          skeleton=skelname,
          method=SingleFaceSelect(nodes=[79, 632, 307],operator=Select()))
      OOF.NodeSelection.Select(
          skeleton=skelname,
          method=SingleNodeSelect(point=Coord(5,5,5),operator=Select()))
	
  def configureGroups(self, skelname):
    OOF.ElementGroup.New_Group(
            skeleton=skelname,
            name='elgroup')
    OOF.FaceGroup.New_Group(
            skeleton=skelname,
            name='fagroup')
    OOF.SegmentGroup.New_Group(
            skeleton=skelname,
            name='segroup')
    OOF.NodeGroup.New_Group(
            skeleton=skelname,
            name='nogroup')
                   
  def groupComponents(self, skelname):
      self.selectComponents1(skelname)
      OOF.ElementGroup.Add_to_Group(
          skeleton=skelname, group='elgroup')
      OOF.FaceGroup.Add_to_Group(
          skeleton=skelname, group='fagroup')
      OOF.SegmentGroup.Add_to_Group(
          skeleton=skelname, group='segroup')
      OOF.NodeGroup.Add_to_Group(
          skeleton=skelname, group='nogroup')
            
  def groupComponentsRefined(self, skelname):
    OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
	skeleton=skelname,
	points=[Point(5.37437,5.53555,21.2376)],
	view=View(cameraPosition=Coord(5,5,34.2583),
		  focalPoint=Coord(5,5,5),
		  up=Coord(0,1,0), angle=30,
		  clipPlanes=[], invertClip=0, size_x=694, size_y=671),
	shift=0, ctrl=0)
    OOF.ElementGroup.Add_to_Group(
            skeleton=skelname, group='elgroup')
            
    OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton=skelname, 
            points=[Point(-15.6761,18.8259,20.2608)],
            view=View(cameraPosition=Coord(-15.7316,18.862,20.3001),
                      focalPoint=Coord(5,5,5), 
                      up=Coord(0.217668,0.851693,-0.476696), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
    OOF.FaceGroup.Add_to_Group(
            skeleton=skelname, group='fagroup')
            
    OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
	skeleton=skelname,
	points=[Point(0.236924,19.8997,26.4638)],
	view=View(cameraPosition=Coord(-0.0410486,21.1544,28.8678),
		  focalPoint=Coord(5,5,5),
		  up=Coord(-0.00161767,0.827986,-0.560746), angle=30,
		  clipPlanes=[], invertClip=0, size_x=691, size_y=652),
	shift=0, ctrl=0)
    OOF.SegmentGroup.Add_to_Group(
            skeleton=skelname, group='segroup')
    
    OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
	skeleton=skelname,
	points=[Point(2.2182,13.9491,18.2603)],
	view=View(cameraPosition=Coord(-0.0410486,21.1544,28.8678),
		  focalPoint=Coord(5,5,5),
		  up=Coord(-0.00161767,0.827986,-0.560746), angle=30,
		  clipPlanes=[], invertClip=0, size_x=691, size_y=652),
	shift=0, ctrl=0)
    OOF.NodeGroup.Add_to_Group(
            skeleton=skelname, group='nogroup')
        
  def oneSkeletonStep1(self):
    OOF.Microstructure.New(
	name='onemicrostructure', width=10,
	height=10, depth=10, width_in_pixels=10,
	height_in_pixels=10, depth_in_pixels=10)
    OOF.Skeleton.New(
	name='oneskeleton', microstructure='onemicrostructure',
	x_elements=4, y_elements=4, z_elements=4,
	skeleton_geometry=TetraSkeleton(arrangement='moderate'))
  
  def twoSkeletonsStep1(self):
    OOF.Microstructure.New(
	name='twomicrostructure1', width=10,
	height=10, depth=10, width_in_pixels=10,
	height_in_pixels=10, depth_in_pixels=10)
    OOF.Skeleton.New(
	name='twoskeleton1', microstructure='twomicrostructure1',
	x_elements=4, y_elements=4, z_elements=4,
	skeleton_geometry=TetraSkeleton(arrangement='moderate'))
    
    OOF.Microstructure.New(
	name='twomicrostructure2', width=10,
	height=10, depth=10, width_in_pixels=10,
	height_in_pixels=10, depth_in_pixels=10)
    OOF.Skeleton.New(
	name='twoskeleton2', microstructure='twomicrostructure2',
	x_elements=3, y_elements=3, z_elements=3,
	skeleton_geometry=TetraSkeleton(arrangement='moderate'))
    
  @memorycheck.check("onemicrostructure")
  def OneSkeletonSelectRefine(self):
      self.oneSkeletonStep1()
      OOF.Windows.Graphics.New()
      self.selectComponents1('onemicrostructure:oneskeleton')
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      OOF.Skeleton.Modify(
          skeleton='onemicrostructure:oneskeleton',
          modifier=Refine(targets=CheckAllElements(),
                          criterion=Unconditionally(),
                          alpha=0.3))
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 8)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 4)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 2)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      savedElements = self.elements("onemicrostructure:oneskeleton")
      savedFaces = self.faces("onemicrostructure:oneskeleton")
      savedSegments = self.segments("onemicrostructure:oneskeleton")
      savedNodes = self.nodes("onemicrostructure:oneskeleton")
      OOF.File.Save.Skeleton(filename="oneskeleton_save",
          mode="w", format="ascii",
          skeleton="onemicrostructure:oneskeleton")
      self.assert_(file_utils.fp_file_compare(
           "oneskeleton_save",
           os.path.join("skeleton_data", "oneskeleton_selectrefine"), 1.e-9))
      file_utils.remove("oneskeleton_save")
      OOF.Graphics_1.File.Close()
      OOF.Skeleton.Delete(skeleton="onemicrostructure:oneskeleton")
      OOF.Microstructure.Delete(microstructure='onemicrostructure')
      OOF.File.Load.Data(
          filename=reference_file("skeleton_data", "oneskeleton_selectrefine"))
      OOF.Windows.Graphics.New()
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 8)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 4)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 2)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      self.assertSavedEqual2Loaded(
          "onemicrostructure:oneskeleton", savedElements, savedFaces,
          savedSegments, savedNodes)
      OOF.Graphics_1.File.Close()
      
  @memorycheck.check("onemicrostructure")
  def OneSkeletonRefineSelect(self):
      self.oneSkeletonStep1()
      OOF.Windows.Graphics.New()
      OOF.Skeleton.Modify(
          skeleton='onemicrostructure:oneskeleton',
          modifier=Refine(targets=CheckAllElements(),
          criterion=Unconditionally(),alpha=0.3))
      self.selectComponentsRefined('onemicrostructure:oneskeleton')
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      savedElements = self.elements("onemicrostructure:oneskeleton")
      savedFaces = self.faces("onemicrostructure:oneskeleton")
      savedSegments = self.segments("onemicrostructure:oneskeleton")
      savedNodes = self.nodes("onemicrostructure:oneskeleton")
      OOF.File.Save.Skeleton(filename="oneskeleton_save",
          mode="w", format="ascii",
          skeleton="onemicrostructure:oneskeleton")
      self.assert_(file_utils.fp_file_compare(
           "oneskeleton_save",
           os.path.join("skeleton_data", "oneskeleton_refineselect"),
           1.e-9))
      file_utils.remove("oneskeleton_save")
      OOF.Graphics_1.File.Close()
      OOF.Skeleton.Delete(skeleton="onemicrostructure:oneskeleton")
      OOF.Microstructure.Delete(microstructure='onemicrostructure')
      OOF.File.Load.Data(filename=reference_file("skeleton_data", 
                                                 "oneskeleton_refineselect"))
      OOF.Windows.Graphics.New()
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      self.assertSavedEqual2Loaded("onemicrostructure:oneskeleton",
                                   savedElements, savedFaces, savedSegments,
                                   savedNodes)
      OOF.Graphics_1.File.Close()
      
  @memorycheck.check("onemicrostructure")
  def OneSkeletonGroupSelect(self):
      self.oneSkeletonStep1()
      OOF.Windows.Graphics.New()
      self.configureGroups('onemicrostructure:oneskeleton')
      self.groupComponents('onemicrostructure:oneskeleton')
      self.selectComponents1('onemicrostructure:oneskeleton')
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.elementsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.facesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.segmentsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.nodesGroupSize("onemicrostructure:oneskeleton"), 1)
      savedElements = self.elements("onemicrostructure:oneskeleton")
      savedFaces = self.faces("onemicrostructure:oneskeleton")
      savedSegments = self.segments("onemicrostructure:oneskeleton")
      savedNodes = self.nodes("onemicrostructure:oneskeleton")
      OOF.File.Save.Skeleton(filename="oneskeleton_save",
          mode="w", format="ascii",
          skeleton="onemicrostructure:oneskeleton")
      self.assert_(file_utils.fp_file_compare(
           "oneskeleton_save",
           os.path.join("skeleton_data", "oneskeleton_groupselect"),
           1.e-9))
      file_utils.remove("oneskeleton_save")
      OOF.Graphics_1.File.Close()
      OOF.Skeleton.Delete(skeleton="onemicrostructure:oneskeleton")
      OOF.Microstructure.Delete(microstructure='onemicrostructure')
      OOF.File.Load.Data(filename=reference_file("skeleton_data",
                                                 "oneskeleton_groupselect"))
      OOF.Windows.Graphics.New()
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1) 
      self.assertEqual(
          self.elementsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.facesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.segmentsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.nodesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertSavedEqual2Loaded(
          "onemicrostructure:oneskeleton",
          savedElements, savedFaces, savedSegments, savedNodes)
      OOF.Graphics_1.File.Close()

  @memorycheck.check("onemicrostructure")
  def OneSkeletonGroupRefineSelect(self):
      self.oneSkeletonStep1()
      OOF.Windows.Graphics.New()
      self.configureGroups('onemicrostructure:oneskeleton')
      self.groupComponents('onemicrostructure:oneskeleton')
      self.assertEqual(
          self.elementsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.facesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.segmentsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.nodesGroupSize("onemicrostructure:oneskeleton"), 1)
      OOF.Skeleton.Modify(
          skeleton='onemicrostructure:oneskeleton',
          modifier=Refine(targets=CheckAllElements(),
          criterion=Unconditionally(),alpha=0.3))
      self.selectComponentsRefined('onemicrostructure:oneskeleton')
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      savedElements = self.elements("onemicrostructure:oneskeleton")
      savedFaces = self.faces("onemicrostructure:oneskeleton")
      savedSegments = self.segments("onemicrostructure:oneskeleton")
      savedNodes = self.nodes("onemicrostructure:oneskeleton")
      OOF.File.Save.Skeleton(filename="oneskeleton_save",
          mode="w", format="ascii",
          skeleton="onemicrostructure:oneskeleton")
      self.assert_(file_utils.fp_file_compare(
           "oneskeleton_save",
           os.path.join("skeleton_data", "oneskeleton_grouprefineselect"),
           1.e-9))
      file_utils.remove("oneskeleton_save")
      OOF.Graphics_1.File.Close()
      OOF.Skeleton.Delete(skeleton="onemicrostructure:oneskeleton")
      OOF.Microstructure.Delete(microstructure='onemicrostructure')
      OOF.File.Load.Data(filename=reference_file(
          "skeleton_data", "oneskeleton_grouprefineselect"))
      OOF.Windows.Graphics.New()
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.elementsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.facesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.segmentsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(self.nodesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertSavedEqual2Loaded(
          "onemicrostructure:oneskeleton",
          savedElements, savedFaces, savedSegments, savedNodes)
      OOF.Graphics_1.File.Close()
      
  @memorycheck.check("onemicrostructure")
  def OneSkeletonGroupSelectRefine(self):
      self.oneSkeletonStep1()
      OOF.Windows.Graphics.New()
      self.configureGroups('onemicrostructure:oneskeleton')
      self.groupComponents('onemicrostructure:oneskeleton')
      self.assertEqual(
          self.elementsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.facesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.segmentsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.nodesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.selectComponents1('onemicrostructure:oneskeleton')
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      OOF.Skeleton.Modify(
          skeleton='onemicrostructure:oneskeleton',
          modifier=Refine(targets=CheckAllElements(),
          criterion=Unconditionally(),alpha=0.3))
      savedElements = self.elements("onemicrostructure:oneskeleton")
      savedFaces = self.faces("onemicrostructure:oneskeleton")
      savedSegments = self.segments("onemicrostructure:oneskeleton")
      savedNodes = self.nodes("onemicrostructure:oneskeleton")
      OOF.File.Save.Skeleton(filename="oneskeleton_save",
          mode="w", format="ascii",
          skeleton="onemicrostructure:oneskeleton")
      self.assert_(file_utils.fp_file_compare(
           "oneskeleton_save",
           os.path.join("skeleton_data", "oneskeleton_grouprefineselect"),
           1.e-9))
      file_utils.remove("oneskeleton_save")
      OOF.Graphics_1.File.Close()
      OOF.Skeleton.Delete(skeleton="onemicrostructure:oneskeleton")
      OOF.Microstructure.Delete(microstructure='onemicrostructure')
      OOF.File.Load.Data(filename=reference_file(
          "skeleton_data", "oneskeleton_grouprefineselect"))
      OOF.Windows.Graphics.New()
      self.assertEqual(
          self.selectedElements("onemicrostructure:oneskeleton"), 8)
      self.assertEqual(
          self.selectedFaces("onemicrostructure:oneskeleton"), 4)
      self.assertEqual(
          self.selectedSegments("onemicrostructure:oneskeleton"), 2)
      self.assertEqual(
          self.selectedNodes("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.elementsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.facesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.segmentsGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertEqual(
          self.nodesGroupSize("onemicrostructure:oneskeleton"), 1)
      self.assertSavedEqual2Loaded(
          "onemicrostructure:oneskeleton",
          savedElements, savedFaces, savedSegments, savedNodes)
      OOF.Graphics_1.File.Close()
      
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Refine the central tet in a 1x1x1 Skeleton, after selecting various
# edges.  This invokes each refinement rule, although it doesn't test
# all of the cases within each rule.  

# TODO 3.0: Add tests for all of the remaining refinement rules. (Already
# done?  Check!)

# TODO 3.0: Figure out how to test the cases within each rule.

class Refine(unittest.TestCase):
    def setUp(self):
        global skeletoncontext, crefine
        from ooflib.engine import skeletoncontext
        from ooflib.SWIG.engine import crefine
        # Make sure tests are reproducible by re-seeding the random
        # number generator before each test.
        OOF.Settings.Random_Seed(seed=17)
        OOF.Windows.Graphics.New()

    def refine1x1(self, segments, filename):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure',
            x_elements=1, y_elements=1, z_elements=1,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        skelctxt = skeletoncontext.skeletonContexts["microstructure:skeleton"]

        for i,nodeNos in enumerate(segments):
            print "nodeNos=", nodeNos
            OOF.SegmentSelection.Select(
                skeleton='microstructure:skeleton',
                method=SingleSegmentSelect(
                    nodes=nodeNos,
                    operator=(Select() if i==0 else AddSelection())))

            # OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            #     skeleton='microstructure:skeleton',
            #     points=[point],
            #     view=View(cameraPosition=Coord(0.5,0.5,3.42583),
            #               focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0),
            #               angle=30, clipPlanes=[], invertClip=0),
            #     shift=(i!=0), ctrl=False)
        
        # # This ensures that the segments to be refined were actually
        # # selected.  It's a test of the test setup, rather than of the
        # # refinement.
        # segsel = skelctxt.segmentselection
        # self.assertEqual(segsel.retrieveSize(), len(clickpoints))

        OOF.Skeleton.Modify(
            skeleton='microstructure:skeleton', 
            modifier=Refine(targets=CheckSelectedEdges(),
                            criterion=Unconditionally(),alpha=0.3))

        OOF.Help.Debug.Sanity_Check(
            skeleton='microstructure:skeleton',
            quick=False)
        self.assert_(skelctxt.sane)
        crefine.printRuleUsage()
        OOF.File.Save.Skeleton(
            filename='testskel.skel',
            mode='w', format='ascii',
            skeleton='microstructure:skeleton')
        self.assert_(file_utils.fp_file_compare(
                'testskel.skel', reference_file('skeleton_data', filename),
                tolerance=1.e-10))
        file_utils.remove('testskel.skel')

    def tearDown(self):
        OOF.Graphics_1.File.Close()
            
    @memorycheck.check("microstructure")
    def OneEdge(self):
        # Check refinement rule tet1Edge1Div
        self.refine1x1([[7,1]],
                       "oneedge.skel")
    
    @memorycheck.check("microstructure")
    def TwoEdgeAdjacent(self):
        # Check refinement rule tet2Edges1DivAdjacent
        self.refine1x1([[7,4], [7,1]],
                       "twoedgeadj.skel")

    @memorycheck.check("microstructure")
    def TwoEdgeOpposite(self):
        # Check refinement rule tet2EdgesDivOpposite
        self.refine1x1([[7,4], [1,2]],
                       "twoedgeopp.skel")

    @memorycheck.check("microstructure")
    def ThreeEdgeTriangle(self):
        # Check refinement rule tet3Edges1DivTriangle
        self.refine1x1([[1,2], [1,7], [7,2]],
                       "threeedgetri.skel")

    @memorycheck.check("microstructure")
    def ThreeEdgeZigZag(self):
        # Check refinement rule tet3Edges1DivZigZag
        self.refine1x1([[1,7], [7,2], [2,4]],
                       'zigzag.skel')
    @memorycheck.check("microstructure")
    def ThreeEdgeZagZig(self):
        # Check refinement rule tet3Edges1DivZigZag.  The refined
        # segments are the mirror image of the ones used in ZigZag,
        # above.
        self.refine1x1([[1,7], [7,4], [4,2]],
                       'zagzig.skel')
    @memorycheck.check("microstructure")
    def ThreeEdgeNode(self):
        # Check refinement rule tet3Edges1Div1Node
        self.refine1x1([[7,4], [7,2], [7,1]],
                       "threeedgenode.skel")
    @memorycheck.check("microstructure")
    def Tet4Edges1(self):
        # Check refinement rule tet4Edges1Div1
        self.refine1x1([[1,2], [7,1], [7,2], [1,4]],
                       'tet4edges1.skel')
    @memorycheck.check("microstructure")
    def Tet4Edges2(self):
        # Check refinement rule tet4Edges1Div2
        self.refine1x1([[1,4], [2,4], [7,2], [1,7]], 
                       "tet4edges2.skel")
    @memorycheck.check("microstructure")
    def FiveEdge(self):
        # Check refinement rule tet5Edges1Div
        self.refine1x1([[1,2], [7,1], [2,4], [7,4], [7,2]],
                       "fiveedges.skel")
    @memorycheck.check("microstructure")
    def SixEdge(self):
        self.refine1x1([[1,2], [7,1], [2,4], [7,4], [7,2], [1,4]],
                       "sixedges.skel")

    @memorycheck.check("microstructure")
    def AllRules(self):
        # The following sequence has been determined to run through
        # all 45 of the subcases of all of the refinement rules.  
        ## TODO 3.1: If the refinement rules change, define TESTCOVERAGE
        ## in crefine.h, build the debug version, and refine a
        ## Skeleton with --debug turned on.  It probably helps to set
        ## Avoid_Deadlocks to 0, as is done below.  Then run
        ## OOF.Help.Debug.RefinementRule_Coverage.Print() to see which
        ## rules were used.
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure', 
            x_elements=6, y_elements=6, z_elements=6,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Help.Debug.RefinementRule_Coverage.Avoid_Deadlocks(0)
        # iterations, alpha, prob, # of refinement rules tested
        # 5 0.3 0.27027  45
        # 3 0.3 0.27027  40
        # 3 0.7 0.27027  39
        # 4 0.7 0.27017  44
        # 3 0.3 0.5      43
        # 3 0.5 0.5      45
        iters = 3
        alpha = 0.5
        prob = 0.5
        for i in range(iters):
            OOF.SegmentSelection.Select(
                skeleton='microstructure:skeleton',
                method=RandomSegments(probability=prob,
                                      operator=Select()))
            OOF.Skeleton.Modify(
                skeleton='microstructure:skeleton',
                modifier=Refine(targets=CheckSelectedEdges(),
                                criterion=Unconditionally(),
                                alpha=alpha))
        OOF.Help.Debug.RefinementRule_Coverage.Print()
        OOF.Help.Debug.RefinementRule_Coverage.Avoid_Deadlocks(1)
        skelctxt = skeletoncontext.skeletonContexts["microstructure:skeleton"]
        OOF.Help.Debug.Sanity_Check(
            skeleton='microstructure:skeleton',
            quick=False)
        self.assert_(skelctxt.sane)
        OOF.File.Save.Skeleton(
            filename='testskel.skel',
            mode='w', format='ascii',
            skeleton='microstructure:skeleton')
        self.assert_(file_utils.fp_file_compare(
                'testskel.skel', reference_file('skeleton_data',
                                                'allrules.skel'),
                tolerance=1.e-10))
        file_utils.remove('testskel.skel')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Skeleton_Undo(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        # Make sure tests are reproducible by re-seeding the random
        # number generator before each test.
        OOF.Settings.Random_Seed(seed=17)
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data","5color"),
                pattern="slice(0|([1-9][0-9]*))\\.tif",
                sort=NumericalOrder()),
            microstructure_name="skeltest",
            height=20.0, width=20.0, depth=20.0)
        OOF.Image.AutoGroup(image="skeltest:5color", name_template='%c')
        OOF.Windows.Graphics.New()

    def tearDown(self):
        OOF.Graphics_1.File.Close()

    @memorycheck.check("skeltest")
    def Undo(self):
        OOF.Skeleton.New(
            name="undotest", microstructure="skeltest",
            x_elements=2, y_elements=3, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        sk_context = skeletoncontext.skeletonContexts["skeltest:undotest"]
        sk_0 = sk_context.getObject()
        self.assert_(not sk_context.undoable())
        OOF.Skeleton.Modify(
            skeleton="skeltest:undotest",
            modifier=Refine(
                targets=CheckHomogeneity(threshold=0.9),
                criterion=Unconditionally(),
                alpha=0.3)
            )
        sk_1 = sk_context.getObject()
        self.assert_(sk_context.undoable())
        self.assertNotEqual(id(sk_0),id(sk_1))
        OOF.Skeleton.Undo(skeleton="skeltest:undotest")
        sk_2 = sk_context.getObject()
        self.assertEqual(id(sk_0), id(sk_2))

    @memorycheck.check("skeltest")
    def Redo(self):
        OOF.Skeleton.New(
            name="redotest", microstructure="skeltest",
            x_elements=2, y_elements=3, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        sk_context = skeletoncontext.skeletonContexts["skeltest:redotest"]
        sk_0 = sk_context.getObject()
        OOF.Skeleton.Modify(
            skeleton="skeltest:redotest",
            modifier=Refine(
                targets=CheckHomogeneity(threshold=0.9),
                criterion=Unconditionally(),
                alpha=0.3)
            )
        sk_1 = sk_context.getObject()
        OOF.Skeleton.Undo(skeleton="skeltest:redotest")
        sk_2 = sk_context.getObject()
        OOF.Skeleton.Redo(skeleton="skeltest:redotest")
        self.assertEqual(id(sk_1),id(sk_context.getObject()))
        self.assert_(not sk_context.redoable())

    # Do and undo a modification that only moves nodes, and therefore
    # uses a DeputySkeleton.
    @memorycheck.check("skeltest")
    def UndoRedo2(self):
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='skeltest',
            x_elements=4, y_elements=4, z_elements=4, 
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=SnapNodes(targets=SnapAll(),
                               criterion=AverageEnergy(alpha=1)))
        OOF.File.Save.Skeleton(
            filename="skeleton.dat",
            mode="w", format="ascii",
            skeleton="skeltest:skeleton")
        self.assert_(file_utils.fp_file_compare(
                "skeleton.dat",
                os.path.join("skeleton_data", "undo1"),
                1.e-9))
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        # By saving the Skeleton we check that the nodes were actually
        # moved back into the correct positions.  It's not sufficient
        # to check that the object identities are correct as in the
        # previous Undo test.
        OOF.File.Save.Skeleton(
            filename="skeleton.dat",
            mode="w", format="ascii",
            skeleton="skeltest:skeleton")
        self.assert_(file_utils.fp_file_compare(
                "skeleton.dat",
                os.path.join("skeleton_data", "undo2"),
                1.e-9))
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.File.Save.Skeleton(
            filename="skeleton.dat",
            mode="w", format="ascii",
            skeleton="skeltest:skeleton")
        self.assert_(file_utils.fp_file_compare(
                "skeleton.dat",
                os.path.join("skeleton_data", "undo1"),
                1.e-9))
        file_utils.remove("skeleton.dat")

    # Test Undo and redo that run up against the limits of a small
    # undo buffer.  To repeat the same sequence with both regular
    # Skeletons and Deputies, the next two tests each define a
    # function that does the modifications, and pass it to
    # smallBuffer(), which does the testing.
    @memorycheck.check("skeltest")
    def SmallBufferAnneal(self):
        def anneal(*dummy):
            OOF.Skeleton.Modify(
                skeleton='skeltest:skeleton',
                modifier=Anneal(targets=AllNodes(),
                                criterion=AverageEnergy(alpha=1),
                                T=0.0,
                                delta=0.1,
                                iteration=FixedIteration(iterations=1)))
        self.smallBuffer(anneal, reffile="smallbufferA")

    @memorycheck.check("skeltest")
    def SmallBufferRefine(self):
        def refine(element):
            OOF.ElementSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleElementSelect(element=element,operator=Select()))
            OOF.Skeleton.Modify(
                skeleton='skeltest:skeleton',
                modifier=Refine(targets=CheckSelectedElements(),
                                criterion=Unconditionally(),alpha=0.3))
        self.smallBuffer(refine, reffile="smallbufferR")

    def smallBuffer(self, modifierfn, reffile):
        OOF.Settings.UndoBuffer_Size.Skeleton(size=3)
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='skeltest',
            x_elements=4, y_elements=4, z_elements=4, 
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        # The argument to modifierfn is used in SmallBufferRefine but
        # not SmallBufferAnneal.  It's the index of the element that's
        # being refined at each iteration.  modifierfn didn't need an
        # argument in the original version of these tests, because the
        # scripted element selection command used in SmallBufferRefine
        # refined the element at a given point, not with a given
        # index.  Then we changed the arguments of the command and
        # broke the test.  The result is clumsy but not worth fixing.
        modifierfn(195)
        OOF.File.Save.Skeleton(
            filename="skeleton.dat",
            mode="w", format="ascii",
            skeleton="skeltest:skeleton")
        self.assert_(file_utils.fp_file_compare(
            "skeleton.dat",
            os.path.join("skeleton_data", reffile+"1"),
            1.e-9))
        modifierfn(32)
        modifierfn(275)
        modifierfn(112)
        OOF.File.Save.Skeleton(
            filename="skeleton.dat",
            mode="w", format="ascii",
            skeleton="skeltest:skeleton")
        self.assert_(file_utils.fp_file_compare(
            "skeleton.dat",
            os.path.join("skeleton_data", reffile+"2"),
            1.e-9))
        OOF.Skeleton.Undo(skeleton="skeltest:skeleton")
        OOF.Skeleton.Undo(skeleton="skeltest:skeleton")
        OOF.Skeleton.Undo(skeleton="skeltest:skeleton")
        OOF.File.Save.Skeleton(
            filename="skeleton.dat",
            mode="w", format="ascii",
            skeleton="skeltest:skeleton")
        self.assert_(file_utils.fp_file_compare(
            "skeleton.dat",
            os.path.join("skeleton_data", reffile+"3"),
            1.e-9))
        # Try undoing once too often
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Undo,
            skeleton="skeltest:skeleton")
        OOF.Skeleton.Redo(skeleton="skeltest:skeleton")
        OOF.Skeleton.Redo(skeleton="skeltest:skeleton")
        OOF.Skeleton.Redo(skeleton="skeltest:skeleton")
        OOF.File.Save.Skeleton(
            filename="skeleton.dat",
            mode="w", format="ascii",
            skeleton="skeltest:skeleton")
        self.assert_(file_utils.fp_file_compare(
            "skeleton.dat",
            os.path.join("skeleton_data", reffile+"2"),
            1.e-9))
        # Try redoing once too often
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Redo,
            skeleton="skeltest:skeleton")
        file_utils.remove("skeleton.dat")
        OOF.Settings.UndoBuffer_Size.Skeleton(size=50)


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def initialize():
    # Modify arguments make use of classes which are not in the
    # namespace until after oof.run() has been called, so they can't
    # be used at import-time.
    build_mod_args()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    SkeletonModify("Modify"),

    Skeleton_Save("OneSkeletonSelectRefine"),
    Skeleton_Save("OneSkeletonRefineSelect"),
    Skeleton_Save("OneSkeletonGroupSelect"),
    Skeleton_Save("OneSkeletonGroupRefineSelect"),

    Refine("OneEdge"),
    Refine("TwoEdgeAdjacent"),
    Refine("TwoEdgeOpposite"),
    Refine("ThreeEdgeTriangle"),
    Refine("ThreeEdgeZigZag"),
    Refine("ThreeEdgeZagZig"),
    Refine("ThreeEdgeNode"),
    Refine("Tet4Edges1"),
    Refine("Tet4Edges2"),
    Refine("FiveEdge"),
    Refine("SixEdge"),
    Refine("AllRules"),
    Skeleton_Undo("Undo"),
    Skeleton_Undo("Redo"),
    Skeleton_Undo("UndoRedo2"),
    Skeleton_Undo("SmallBufferAnneal"),
    Skeleton_Undo("SmallBufferRefine")
]

# test_set = [
#     Skeleton_Undo("Undo"),
#     Skeleton_Undo("Redo"),
#     Skeleton_Undo("UndoRedo2"),
#     Skeleton_Undo("SmallBufferAnneal"),
#     Skeleton_Undo("SmallBufferRefine")
# ]
