# -*- python -*-
# $RCSfile: mesh_modify_test.py,v $
# $Revision: 1.20 $
# $Author: langer $
# $Date: 2009/07/07 18:42:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

import unittest, os
import memorycheck
import file_compare

OBSOLETE


class OOF_Mesh_Modify(unittest.TestCase):
    def setUp(self):
        global cskeleton, femesh, cmicrostructure
        from ooflib.SWIG.engine import cskeleton, femesh
        from ooflib.SWIG.common import cmicrostructure

    def tearDown(self):
        pass

    # Since there are only a few modifiers, and they work differently,
    # just do them separately in their own individual tests.  The
    # complicated one is "Adaptive Mesh Refinement", it's saved for
    # last.  The easy ones are "Assign Material", "Remove Material",
    # and "Revert Mesh".

    @memorycheck.check('mesh_mod_test')
    def Assign_Material(self):
        from ooflib.engine import skeletoncontext
        from ooflib.engine import mesh
        
        OOF.File.Load.Data(filename=os.path.join(
            "mesh_data","modifiable_mesh"))

        OOF.Mesh.Modify(mesh="mesh_mod_test:skeleton:mesh",
                        modifier=AssignMaterial(
            material="other", target=MeshElementGroup(group="central")))
        
        skc=skeletoncontext.skeletonContexts["mesh_mod_test:skeleton"]
        egr=skc.elementgroups.get_group("central")
        mesh_indices = [e.meshindex for e in egr]
        mesh_obj=mesh.meshes["mesh_mod_test:skeleton:mesh"].getObject()

        ei = mesh_obj.element_iterator()
        while not ei.end():
            el = ei.element()
            mat = el.getExplicitMaterial()
            if mat:
                self.assert_(el.get_index() in mesh_indices)
            else:
                self.assert_(not el.get_index() in mesh_indices)
            ei.next()

        ## Save mesh and make sure that materials are stored &
        ## reloaded properly.

        OOF.File.Save.Mesh(filename='mod.mesh', mode='w', format='ascii',
                           mesh='mesh_mod_test:skeleton:mesh')
        self.assert_(file_compare.fp_file_compare(
                os.path.join('mesh_data', 'mod.mesh'), 'mod.mesh',
                tolerance=1.e-10))

        OOF.Mesh.Delete(mesh='mesh_mod_test:skeleton:mesh')
        OOF.File.Load.Data(filename='mod.mesh')
        ei = mesh_obj.element_iterator()
        while not ei.end():
            el = ei.element()
            mat = el.getExplicitMaterial()
            if mat:
                self.assert_(el.get_index() in mesh_indices)
            else:
                self.assert_(not el.get_index() in mesh_indices)
            ei.next()        

        ## TODO: Check that explicitly assigned materials are
        ## inherited properly during AMR.

        OOF.Material.Delete(name="soft")
        OOF.Material.Delete(name="firm")
        OOF.Material.Delete(name="other")
        OOF.Property.Delete(property="Color:blue")
        OOF.Property.Delete(property="Color:red")
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:strong')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:weak')
        

    @memorycheck.check('mesh_mod_test')
    def Remove_Material(self):
        from ooflib.engine import mesh
        OOF.File.Load.Data(filename=os.path.join(
            "mesh_data","modifiable_mesh"))

        OOF.Mesh.Modify(
            mesh="mesh_mod_test:skeleton:mesh",
            modifier=AssignMaterial(
                material="other", target=MeshElementGroup(group="central")))
        #
        OOF.Mesh.Modify(
            mesh="mesh_mod_test:skeleton:mesh",
            modifier=RemoveMaterial(
                target=MeshElementGroup(group="central")))

        mesh_obj=mesh.meshes["mesh_mod_test:skeleton:mesh"].getObject()
        ei=mesh_obj.element_iterator()
        while not ei.end():
            el=ei.element()
            mat=el.getExplicitMaterial()
            self.assert_(not mat)
            ei.next()
        
        OOF.Material.Delete(name="soft")
        OOF.Material.Delete(name="firm")
        OOF.Material.Delete(name="other")
        OOF.Property.Delete(property="Color:blue")
        OOF.Property.Delete(property="Color:red")
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:strong')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:weak')


    @memorycheck.check('el_shape.png')
    def Adaptive_Mesh_Refinement(self):
        # This test also runs RevertMesh.
        from ooflib.engine import mesh
        from ooflib.common import primitives
        OOF.File.Load.Data(filename=os.path.join(
            "mesh_data","el_shape.mesh"))
        OOF.Subproblem.Set_Solver(
            subproblem='el_shape.png:skeleton:mesh:default',
            linearity=Linear(),
            solver=StaticDriver(matrixmethod=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13, max_iterations=1000)))
        OOF.Mesh.Solve(mesh='el_shape.png:skeleton:mesh',
                       endtime=0.0, stepsize=0.0)
        OOF.Mesh.Modify(
            mesh='el_shape.png:skeleton:mesh',
            modifier=AdaptiveMeshRefinement(
                subproblem='el_shape.png:skeleton:mesh:default',
                estimator=ZZ_Estimator(norm=L2ErrorNorm(),
                                       flux=Stress,threshold=10),
                criterion=Unconditionally(),
                degree=Trisection(rule_set='conservative'),
                alpha=0.29999999999999999,
                rationalize=False))
        # Check if we get the expected number of elements.  This is
        # the only type of quantitative sanity check performed here.
        meshctxt=mesh.meshes["el_shape.png:skeleton:mesh"]
        self.assert_(meshctxt.nelements()==510)

        # Call RevertMesh
        OOF.Mesh.Modify(
            mesh='el_shape.png:skeleton:mesh',
            modifier=RevertMesh(base_skeleton='Base Skeleton 0',init_field=True)
            )

        # Check if the initial number of elements is recovered.
        meshctxt=mesh.meshes["el_shape.png:skeleton:mesh"]
        self.assert_(meshctxt.nelements()==400)
 
        OOF.Material.Delete(name="green-material")
        OOF.Property.Delete(
            property="Mechanical:Elasticity:Isotropic:green_elasticity")

    @memorycheck.check('el_shape.png')
    def Adaptive_SubProblem_Refinement(self):
        from ooflib.engine import mesh
        from ooflib.common import primitives
        Point = primitives.Point
        OOF.File.Load.Data(filename=os.path.join(
            "mesh_data","el_shape.mesh"))
        OOF.Windows.Graphics.New()
        OOF.Graphics_1.Toolbox.Pixel_Select.Rectangle(
            source='el_shape.png:el_shape.png',
            points=[Point(0.222008,9.73552), Point(2.7278,3.11004)],
            shift=0, ctrl=0)
        OOF.PixelGroup.New(name='upperpixels', microstructure='el_shape.png')
        OOF.PixelGroup.AddSelection(microstructure='el_shape.png',
                                    group='upperpixels')
        OOF.Subproblem.New(name='subproblem', mesh='el_shape.png:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='upperpixels'))
        OOF.Solver.Solve(
            subproblem='el_shape.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000, tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))
        OOF.Subproblem.Copy_Field_State(
            source='el_shape.png:skeleton:mesh:default',
            target='el_shape.png:skeleton:mesh:subproblem')
        OOF.Subproblem.Copy_Equation_State(
            source='el_shape.png:skeleton:mesh:default',
            target='el_shape.png:skeleton:mesh:subproblem')
        OOF.Mesh.Modify(
            mesh='el_shape.png:skeleton:mesh',
            modifier=AdaptiveMeshRefinement(
                subproblem='el_shape.png:skeleton:mesh:subproblem',
                estimator=ZZ_Estimator(norm=L2ErrorNorm(),
                                       flux=Stress,threshold=10),
                criterion=Unconditionally(),
                degree=Trisection(rule_set='conservative'),
                alpha=0.29999999999999999,
                rationalize=False))
        #Check if we get the expected number of elements.
        meshctxt=mesh.meshes["el_shape.png:skeleton:mesh"]
        self.assertEqual(meshctxt.nelements(), 488)

        OOF.Graphics_1.File.Close()
        OOF.Microstructure.Delete(microstructure="el_shape.png")
        OOF.Material.Delete(name="green-material")
        OOF.Property.Delete(
            property="Mechanical:Elasticity:Isotropic:green_elasticity")


# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.

def run_tests():

    from ooflib.SWIG.common import config
    if config.devel():
        print >> sys.stderr,  "Devel mode detected, modify testing skipped."
        return 0
    
    modify_set = [
        OOF_Mesh_Modify("Assign_Material"),
        OOF_Mesh_Modify("Remove_Material"),
        OOF_Mesh_Modify("Adaptive_Mesh_Refinement"),
        OOF_Mesh_Modify("Adaptive_SubProblem_Refinement")
        ]
    
    test_set = modify_set

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
