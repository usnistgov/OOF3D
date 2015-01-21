# -*- python -*-
# $RCSfile: skeleton_generate.py,v $
# $Revision: 1.8 $
# $Author: langer $
# $Date: 2008/06/23 21:24:07 $

# Special file for regenerating reference files for skeleton
# comparisons, after changes are made to the skeleton code.
# Obviously, such reference data should not be generated until/unless
# the corresponding modifiers are known to function correctly --
# running this file will generate reference data such that the
# regression tests will pass.

# The file writes the reference data in the local directory with the
# prefix "skel_".  Users must manually overwrite the older reference
# data.  Automatically overwriting test reference data is just wrong.

# Note that this file does *not* generate the snap-nodes-with-pinning
# reference data needed by skeleton_extra_test.py.

import filecmp, os, random

def generate():
    from ooflib.SWIG.common import crandom
    from ooflib.engine import skeletonmodifier
    from ooflib.engine import skeletonnode
    from ooflib.engine import skeletonelement
    from ooflib.engine import skeletonsegment
    for r in skeletonmodifier.SkeletonModifier.registry:
        try:
            mods = skel_modify_args[r.name()]
        except KeyError:
            print "No data for skeleton modifier %s." % r.name()
        else:
            # Saved skeleton must be named "modtest".
            for (startfile, destfile, kwargs) in mods:
                OOF.File.Load.Data(
                    filename=os.path.join("skeleton_data", startfile))
                mod = r(**kwargs)
                random.seed(17)
                crandom.rndmseed(17)
                OOF.Skeleton.Modify(skeleton="skeltest:modtest",
                                    modifier=mod)
                OOF.Microstructure.Rename(microstructure="skeltest",
                                          name="skelcomp")
                OOF.Skeleton.Rename(skeleton="skelcomp:modtest",
                                    name="reference")
                OOF.File.Save.Skeleton(filename="skel_"+destfile,
                                       mode="w", format="ascii",
                                       skeleton="skelcomp:reference")
                OOF.Microstructure.Delete(microstructure="skelcomp")




# Data for the skeleton modifier tests.  This is a dictionary indexed by
# skeleton modifier name, and for each modifier, there is a set of
# arguments to supply to the modifier menu item for the test, and the
# name of a file containing correct results for that test.
skel_modify_args = {}
def build_mod_args():
    global skel_modify_args
    skel_modify_args = {
        "Refine" :
        [ ("modbase", "refine_1",
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
        [ ("modbase", "relax",
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
          ]
        }


def run():
    build_mod_args()
    generate()

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
    
    success = run()

    OOF.File.Quit()
    
