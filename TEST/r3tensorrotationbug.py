# -*- python -*-
# $RCSfile: r3tensorrotationbug.py,v $
# $Revision: 1.8 $
# $Author: langer $
# $Date: 2008/10/20 15:28:59 $

# Test for a particular, pernicious bug.

import unittest, os
import memorycheck


class R3TensorRotationBug(unittest.TestCase):
    # Looks complicated, but we just need to set up a well-posed
    # problem that has piezoelectricity in it, so we can run the
    # piezoelectricity's "precompute" routine.
    def setUp(self):
        OOF.Microstructure.New(name='r3bug',
                               width=1.0, height=1.0,
                               width_in_pixels=10, height_in_pixels=10)
        OOF.Material.New(name='material')
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Material.Add_property(
            name='material',
            property='Electric:DielectricPermittivity:Isotropic')
        OOF.Material.Add_property(
            name='material',
            property='Orientation')
        OOF.Material.Add_property(
            name='material',
            property='Couplings:ThermalExpansion:Isotropic')
        OOF.Material.Add_property(
            name='material',
            property='Couplings:PiezoElectricity:Hexagonal:C6v')
        OOF.Skeleton.New(
            name='skeleton', microstructure='r3bug',
            x_elements=4, y_elements=4,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))
        OOF.Mesh.New(
            name='mesh', skeleton='r3bug:skeleton',
            element_types=['T3_3', 'Q4_4'])
        OOF.Subproblem.Field.Define(subproblem='r3bug:skeleton:mesh:default',
                                    field=Temperature)
        OOF.Subproblem.Field.Define(subproblem='r3bug:skeleton:mesh:default',
                                    field=Displacement)
        OOF.Subproblem.Field.Activate(subproblem='r3bug:skeleton:mesh:default',
                                      field=Displacement)
        OOF.Subproblem.Field.Define(subproblem='r3bug:skeleton:mesh:default',
                                    field=Voltage)
        OOF.Subproblem.Field.Activate(subproblem='r3bug:skeleton:mesh:default',
                                      field=Voltage)
        OOF.Mesh.Field.In_Plane(mesh='r3bug:skeleton:mesh', field=Voltage)
        OOF.Mesh.Set_Field_Initializer(
            mesh='r3bug:skeleton:mesh', field=Temperature,
            initializer=ConstScalarFieldInit(value=1.0))
        OOF.Subproblem.Equation.Activate(
            subproblem='r3bug:skeleton:mesh:default', equation=Force_Balance)
        OOF.Subproblem.Equation.Activate(
            subproblem='r3bug:skeleton:mesh:default', equation=Plane_Stress)
        OOF.Subproblem.Equation.Activate(
            subproblem='r3bug:skeleton:mesh:default', equation=Coulomb_Eqn)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='r3bug:skeleton:mesh', 
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.0),
                boundary='bottomleft'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='r3bug:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.0),boundary='bottomleft'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', mesh='r3bug:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.0),boundary='bottomright'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>', mesh='r3bug:skeleton:mesh',
            condition=DirichletBC(
                field=Voltage,field_component='',
                equation=Coulomb_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),boundary='bottomright'))

        OOF.Material.Assign(material='material',
                            microstructure='r3bug', pixels=all)   

        
    def tearDown(self):
        OOF.Material.Delete(name='material')

    @memorycheck.check("r3bug")
    def Identity(self):
        global refdata
        OOF.Subproblem.Set_Solver(
            subproblem='r3bug:skeleton:mesh:default',
            linearity=Linear(),
            solver=StaticDriver(
                matrixmethod=GeneralizedMinResidual(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000,krylov_dimension=100)))
        OOF.Mesh.Solve(mesh='r3bug:skeleton:mesh', endtime=0.0, stepsize=0)
        from ooflib.engine import materialmanager
        m = materialmanager.getMaterial('material')
        p = m.fetchProperty('PiezoElectricity')
        d = p.dijk()
        for i in range(3):
            for j in range(3):
                for k in range(j,3):
                    self.assertAlmostEqual(d[i,j,k],
                                           refdata['identity'][(i,j,k)],
                                           6)
                    

    @memorycheck.check("r3bug")
    def Nontrivial(self):
        OOF.Property.Parametrize.Orientation(
            angles=Abg(alpha=30.0, beta=0.0, gama=0.0))
        OOF.Subproblem.Set_Solver(
            subproblem='r3bug:skeleton:mesh:default',
            linearity=Linear(),
            solver=StaticDriver(
                matrixmethod=GeneralizedMinResidual(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000,krylov_dimension=100)))
        OOF.Mesh.Solve(mesh='r3bug:skeleton:mesh', endtime=0.0, stepsize=0)
        from ooflib.engine import materialmanager
        m = materialmanager.getMaterial('material')
        p = m.fetchProperty('PiezoElectricity')
        d = p.dijk()
        for i in range(3):
            for j in range(3):
                for k in range(j,3):
                    self.assertAlmostEqual(d[i,j,k],
                                           refdata['nontrivial'][(i,j,k)],
                                           6)
        
global refdata

def set_refdata():
    global refdata
    refdata = {}
    refdata['identity']={(0,0,0):0.0, (0,0,1):0.0, (0,0,2):1.0,
                         (0,1,1):0.0, (0,1,2):0.0, (0,2,2):0.0,
                         (1,0,0):0.0, (1,0,1):0.0, (1,0,2):0.0,
                         (1,1,1):0.0, (1,1,2):1.0, (1,2,2):0.0,
                         (2,0,0):1.0, (2,0,1):0.0, (2,0,2):0.0,
                         (2,1,1):1.0, (2,1,2):0.0, (2,2,2):1.0
                         }
    refdata['nontrivial']={
        (0,0,0):-1.250000,
        (0,0,1):0.000000,
        (0,0,2):0.433013,
        (0,1,1):-0.500000,
        (0,1,2):0.000000,
        (0,2,2):0.250000,
        (1,0,0):0.000000,
        (1,0,1):-0.500000,
        (1,0,2):0.000000,
        (1,1,1):0.000000,
        (1,1,2):0.866025,
        (1,2,2):0.000000,
        (2,0,0):0.433013,
        (2,0,1):0.000000,
        (2,0,2):0.250000,
        (2,1,1):0.866025,
        (2,1,2):0.000000,
        (2,2,2):1.299038,
        }
    

def run_tests():
    
    set_refdata()

    test_set = [
        R3TensorRotationBug("Identity"),
        R3TensorRotationBug("Nontrivial")
        ]

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
