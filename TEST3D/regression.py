# -*- python -*-
# $RCSfile: regression.py,v $
# $Revision: 1.2.8.35 $
# $Author: langer $
# $Date: 2014/10/03 17:44:57 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.



# Top-level regression test file for the OOF application.  Knows about
# all the test suites in this directory, and what order to run them in
# in order to get a proper regression test.

import sys, imp, os, getopt, copy, unittest

# The startup sequence for regression.py has to imitate the executable
# oof2 script. That one imports the contents of the math module into
# the main oof namespace, so we have to do it here too.  Not importing
# math here will make some tests fail.
from math import *

# The test modules are listed here in the order in which they'll be
# run.  The modules must contain a list called "test_set" that
# contains the unittest.TestCase instances that will be run.  If the
# modules have a function called "initialize" it will be run before
# the tests, but after the oof globals have been inserted into the
# module.

test_module_names = [
    "fundamental_test",
    "microstructure_test",
    "image_test",
    "pixel_test",
    "activearea_test",
    #"microstructure_extra_test", # saving options, etc.  See TODO in test file
    "matrix_test",
    "skeleton_basic_test",
    # Material property test comes before skeleton_select_test so that
    # selection by Material can be tested.
    "material_property_test",
    "skeleton_select_test",
    "skeleton_modification_test",
    "skeleton_select_mod_test",
    "skeleton_pinnodes_test",
    "skeleton_bdy_test",
    ##     "skeleton_periodic_test",
    ##     "skeleton_periodic_bdy_test",

    ## TODO MER: The only things we need from skeleton_extra_test are the
    ## 3D equivalents of SelectSegmentPixels, SelectElementPixels,
    ## etc, which haven't been implemented yet.  There are TODOs in
    ## engine/pixelselect.py.
    ##     "skeleton_extra_test",

    "mesh_test",
    "subproblem_test",
    "output_test",
    "solver_test",
    "boundary_condition_test",
    "aniso_test",
    "scheduled_output_test",
    "nonconstant_property_test",
    "nonlinear_property_test",
    "nonlinear_floatbc_test",
    "nonlinear_linear_test",
    "nonlinear_timedependent_test",
    "subproblem_test_extra",
    "pyproperty_test",
    ]

def stripdotpy(name):
    if name.endswith(".py"):
        return name[:-3]
    return name

testcount = 1

def run_modules(test_module_names, oofglobals, backwards):
    logan = unittest.TextTestRunner()
    if backwards:
        test_module_names.reverse()
    for m in test_module_names:
        try:
            exec "import " + m + " as test_module"
        except ImportError:
            print >> sys.stderr, "Import error."
        else:
            print "Running test module %s." % m
            # Make sure all the goodies in the OOF namespace are available.
            test_module.__dict__.update(oofglobals)
            if hasattr(test_module, "initialize"):
                test_module.initialize()
            for t in test_module.test_set:
                global testcount
                print >> sys.stderr, "\n *** Running test %d: %s ***\n" % \
                    (testcount, t.id())
                testcount += 1
                if not dryrun:
                    res = logan.run(t)
                    if not res.wasSuccessful():
                        return False
    return True

if __name__=="__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:],"f:a:t:o:d",
                                  ["from=", "after=", "to=", "oofargs=",
                                   "forever", "debug", "backwards",
                                   "dryrun"])
    except getopt.GetoptError, err:
        print str(err)
        print "Usage: regression.py [--from <starttest> | --after <starttest>] [--to <endtest>] [--forever] [--oofargs <oofargs>] [--debug] [--backwards] [tests]"
        print "       Don't use --from or --to if tests are listed explicitly."
        sys.exit(2)

    oofargs = []
    
    fromtogiven = False
    startaftergiven = False
    forever = False
    debug = False
    backwards = False

    global dryrun
    dryrun = False

    for o,v in opts:
        if o in ("-f", "--from"):
            if startaftergiven:
                print >> sys.stderr, "You can't use both --from and --after."
                sys.exit(1)
            v = stripdotpy(v)
            test_module_names = test_module_names[test_module_names.index(v):]
            fromtogiven = True
            startaftergiven = True
        if o in ("-a", "--after"):
            if startaftergiven:
                print >> sys.stderr, "You can't use both --from and --after."
                sys.exit(1)
            v = stripdotpy(v)
            test_module_names = \
                test_module_names[test_module_names.index(v)+1:]
            fromtogiven = True
            startaftergiven = True
        elif o in ("-t", "--to"):
            v = stripdotpy(v)
            test_module_names = \
                test_module_names[:test_module_names.index(v)+1]
            fromtogiven = True
        elif o in ("-o","--oofargs"):
            oofargs = v.split()
        elif o == "--forever":
            forever = True
        elif o == "--debug":
            debug = True
        elif o == "--backwards":
            backwards = True
        elif o in ("-d", "--dryrun"):
            dryrun = True

    if fromtogiven:
        if args:
            print "You can't explicitly list the tests *and* use --from, --after, or --to."
            sys.exit(1)
    elif args:
        test_module_names = [stripdotpy(a) for a in args]
        

    # Effectively pass these through.
    sys.argv = [sys.argv[0]] + oofargs

    try:
        import oof3d
        sys.path.append(os.path.dirname(oof3d.__file__))
        from ooflib.common import oof
    except ImportError:
        print "OOF3D is not correctly installed on this system."
        sys.exit(4)

    sys.argv.extend(["--text", "--quiet", "--seed=17"])
    if debug:
        sys.argv.append("--debug")

    oof.run(no_interp=1)

    # Make a temp directory and cd to it, but put the current
    # directory in the path first, so imports will still work.  By
    # cd'ing to a temp directory, we ensure that all files written
    # during the tests won't clobber or be clobbered by files written
    # by another test being run in the same file system.
    import tempfile
    homedir = os.path.realpath(sys.path[0]) # where we are now.
    sys.path[0] = os.path.realpath(sys.path[0])
    tmpdir = tempfile.mkdtemp(prefix='oof3temp_')
    print >> sys.stderr, "Using temp dir", tmpdir
    os.chdir(tmpdir)
    # Tell file_utils where the home directory is, since reference
    # files are named relative to it.
    from UTILS import file_utils
    file_utils.set_reference_dir(homedir)

    # globals() contains OOF namespace objects that we will be making
    # available to each test script.  If test scripts modify globals
    # (eg, by using utils.OOFdefine or the scriptloader), we don't
    # want those modifications to affect later test scripts.
    # Therefore we create a pristine copy of globals now, and use it
    # instead of globals() later.
    oofglobals = copy.copy(globals())
    ok = False
    try:
        if forever:
            count = 0
            ok = False
            while run_modules(test_module_names, oofglobals, backwards):
                count += 1
                print >> sys.stderr, "******* Finished", count, \
                    "iteration%s"%("s"*(count>1)), "*******"
        else:
            ok = run_modules(test_module_names, oofglobals, backwards)
        OOF.File.Quit()
    finally:
        if ok:
            os.rmdir(tmpdir)
            print >> sys.stderr, "All tests completed successfully!"
        else:
            print >> sys.stderr, "Tests failed."
            print >> sys.stderr, "Temp dir", tmpdir, "was not removed."
