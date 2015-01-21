# -*- python -*-
# $RCSfile: interface_test.py,v $
# $Revision: 1.12 $
# $Author: langer $
# $Date: 2008/10/20 15:28:59 $

# Test mesh with interfaces.
#Assumes the images cyallow.png and serendipity.png in the examples
#directory don't change!

import unittest, os, filecmp, random

class OOF_SimpleInterfaceTest(unittest.TestCase):
    def setUp(self):
        OOF.Microstructure.Create_From_ImageFile(
            filename='../examples/cyallow.png',
            microstructure_name='cyallow.png',
            height=automatic, width=automatic)
        OOF.Image.AutoGroup(image='cyallow.png:cyallow.png', name_template='%c')
        OOF.Property.Copy(property='Mechanical:Elasticity:Isotropic',
                          new_name='simpleelasticity')
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.simpleelasticity(
            cijkl=IsotropicRank4TensorEnu(
                young=0.66666666666666663,
                poisson=0.33333333333333331))
        OOF.Material.New(name='material', material_type='bulk')
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic:simpleelasticity')
        OOF.Material.Assign(material='material', microstructure='cyallow.png',
                            pixels='RGBColor(red=1.00000,green=1.00000,blue=0.00000)')
        OOF.Material.New(name='material<2>', material_type='bulk')
        OOF.Material.Add_property(
            name='material<2>',
            property='Mechanical:Elasticity:Isotropic:simpleelasticity')
        OOF.Material.Assign(
            material='material<2>', microstructure='cyallow.png',
            pixels='RGBColor(red=0.00000,green=1.00000,blue=1.00000)')
        #Here is a simple surface tension property
        OOF.Property.Copy(
            property='Mechanical:Interface:SurfaceTension:Isotropic',
            new_name='simpletension')
        OOF.Property.Parametrize.Mechanical.Interface.SurfaceTension.Isotropic.simpletension(
            gamma_left=0.5,gamma_right=0.5)
        #Assign the surface tension property to an interface material
        OOF.Material.New(name='interfacematerial', material_type='interface')
        OOF.Material.Add_property(
            name='interfacematerial',
            property='Mechanical:Interface:SurfaceTension:Isotropic:simpletension')

        OOF.Skeleton.New(
            name='skeleton', microstructure='cyallow.png',
            x_elements=4, y_elements=4,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))

    # Create an interface between two materials, between two pixel
    # groups, around a single material, and around a single pixel
    # group.  Check the number of nodes and edgements in the
    # mesh. Assign an interface material to the interfaces and set a
    # Generalized Force BC that cancels out the surface tension.
    # Check that the solution is everywhere zero in this setup.
    def InterfaceTension(self):
        from ooflib.engine import mesh
        #Create interface between two materials
        OOF.Microstructure.Interface.New(
            microstructure='cyallow.png',
            name='interface',
            interface_type=MaterialInterface(left='material',
                                             right='material<2>'))
        #Create interface between two pixel groups.
        #The edgements will use the material of the last interface created.
        OOF.Microstructure.Interface.New(
            microstructure='cyallow.png',
            name='interface<2>',
            interface_type=PixelGroupInterface(
                left='RGBColor(red=1.00000,green=1.00000,blue=0.00000)',
                right='RGBColor(red=0.00000,green=1.00000,blue=1.00000)'))

        OOF.Material.Interface.Assign(microstructure='cyallow.png',
                                      material='interfacematerial',
                                      interfaces=['interface'])
        OOF.Material.Interface.Assign(microstructure='cyallow.png',
                                      material='interfacematerial',
                                      interfaces=['interface<2>'])

        OOF.Mesh.New(name='mesh', skeleton='cyallow.png:skeleton',
                     element_types=['D2_2', 'T3_3', 'Q4_4'])
        meshctxt=mesh.meshes["cyallow.png:skeleton:mesh"]

        self.assert_(meshctxt.nnodes()==30)
        self.assert_(meshctxt.nedgements()==20)
        
        OOF.Subproblem.Field.Define(
            subproblem='cyallow.png:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            field=Displacement)
        OOF.Mesh.Field.In_Plane(mesh='cyallow.png:skeleton:mesh',
                                field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            equation=Force_Balance)
        #Pin the top and bottom boundaries
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='top'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,
                                  field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='top'))

        OOF.Windows.Graphics.New()
        #Create a point boundary at the middle of the left boundary
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='cyallow.png:skeleton',
            points=[Point(0.312741,29.3629)], shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton='cyallow.png:skeleton',
            name='midleft',
            constructor=PointFromNodes(group=selection))
        #Create a point boundary at the middle of the right boundary
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='cyallow.png:skeleton',
            points=[Point(60.1969,29.6178)], shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton='cyallow.png:skeleton',
            name='midright',
            constructor=PointFromNodes(group=selection))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<5>', mesh='cyallow.png:skeleton:mesh',
            condition=ForceBC(equation=Force_Balance,eqn_component='x',
                              profile=ContinuumProfile(function='-1'),
                              boundary='midright'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<6>', mesh='cyallow.png:skeleton:mesh',
            condition=ForceBC(equation=Force_Balance,eqn_component='x',
                              profile=ContinuumProfile(function='1'),
                              boundary='midleft'))

        OOF.Mesh.Set_Field_Initializer(
            mesh='cyallow.png:skeleton:mesh',
            field=Displacement,
            initializer=ConstTwoVectorFieldInit(cx=10.0,cy=10.0))


        OOF.Subproblem.Set_Solver(
            subproblem='cyallow.png:skeleton:mesh:default',
            linearity=Linear(),
            solver=StaticDriver(
            matrixmethod=BiConjugateGradient(
            preconditioner=ILUPreconditioner(),
            tolerance=1e-13,max_iterations=1000)))
        
        OOF.Mesh.Solve(mesh='cyallow.png:skeleton:mesh', endtime=0.0,
                       stepsize=0)

        #Cancellation of Generalized Force BCs and surface tension
        #property should be perfect.
        meshobj=meshctxt.getObject()
        for fn in meshobj.funcnode_iterator():
            delta = fn.displaced_position(meshobj) - fn.position()
            self.assertAlmostEqual(delta**2, 0.0, 6)

        #Remove one of the overlapping interfaces and solve again
        OOF.Microstructure.Interface.Delete(microstructure='cyallow.png',
                                            interface='interface<2>')
        
        self.assert_(meshctxt.nnodes()==30)
        self.assert_(meshctxt.nedgements()==20)


        OOF.Mesh.Solve(mesh='cyallow.png:skeleton:mesh', endtime=0.0,
                       stepsize=0)

        meshobj=meshctxt.getObject()
        for fn in meshobj.funcnode_iterator():
            delta = fn.displaced_position() - fn.position()
            self.assertAlmostEqual(delta**2, 0.0, 6)

        #Remove the last interface
        OOF.Microstructure.Interface.Delete(microstructure='cyallow.png',
                                            interface='interface')

        #Create a new pair of interfaces
        OOF.Microstructure.Interface.New(
            microstructure='cyallow.png',
            name='interface',
            interface_type=SingleMaterialInterface(left='material'))
        OOF.Microstructure.Interface.New(
            microstructure='cyallow.png',
            name='interface<2>',
            interface_type=SinglePixelGroupInterface(
                left='RGBColor(red=0.00000,green=1.00000,blue=1.00000)'))

        OOF.Material.Interface.Assign(microstructure='cyallow.png',
                                      material='interfacematerial',
                                      interfaces=['interface'])
        OOF.Material.Interface.Assign(microstructure='cyallow.png',
                                      material='interfacematerial',
                                      interfaces=['interface<2>'])

        #Check again
        self.assert_(meshctxt.nnodes()==30)
        self.assert_(meshctxt.nedgements()==20)

        OOF.Solver.Solve(
            subproblem='cyallow.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))

        meshobj=meshctxt.getObject()
        for fn in meshobj.funcnode_iterator():
            delta = fn.displaced_position() - fn.position()
            self.assertAlmostEqual(delta**2, 0.0, 6)

        #Create a skeleton boundary from an interface definition, and assign
        #it an interface material.
        OOF.Skeleton.Boundary.Construct(
            skeleton='cyallow.png:skeleton',
            name='boundary',
            constructor=EdgeFromInterface(interface='interface',
                                          direction='Clockwise'))
        OOF.Skeleton.Boundary.Construct(
            skeleton='cyallow.png:skeleton',
            name='boundary<2>',
            constructor=EdgeFromInterface(interface='interface<2>',
                                          direction='Clockwise'))

        OOF.Material.Interface.Assign(microstructure='cyallow.png',
                                      material='interfacematerial',
                                      skeleton='skeleton',
                                      interfaces=['boundary'])
        OOF.Material.Interface.Assign(microstructure='cyallow.png',
                                      material='interfacematerial',
                                      skeleton='skeleton',
                                      interfaces=['boundary<2>'])

        #Remove an interface, which triggers a mesh rebuild, which
        #puts the new boundaries into the mesh.
        OOF.Microstructure.Interface.Delete(microstructure='cyallow.png',
                                            interface='interface')

        self.assert_(meshctxt.nnodes()==30)
        self.assert_(meshctxt.nedgements()==20)

        OOF.Solver.Solve(
            subproblem='cyallow.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))

        meshobj=meshctxt.getObject()
        for fn in meshobj.funcnode_iterator():
            delta = fn.displaced_position() - fn.position()
            self.assertAlmostEqual(delta**2, 0.0, 6)

        OOF.Graphics_1.File.Close()

    #Test Field Discontinuity BC across an interface.
    #Cyan region gets separated from the Yellow region by a finite displacement.
    def DetachedMesh(self):
        from ooflib.engine import mesh
        #Create interface between two materials
        OOF.Microstructure.Interface.New(
            microstructure='cyallow.png',
            name='interface',
            interface_type=MaterialInterface(left='material',
                                             right='material<2>'))

        #Use higher order elements
        OOF.Mesh.New(name='mesh', skeleton='cyallow.png:skeleton',
                     element_types=['D3_3', 'T6_6', 'Q8_8'])
        meshctxt=mesh.meshes["cyallow.png:skeleton:mesh"]

        self.assert_(meshctxt.nnodes()==74)
        self.assert_(meshctxt.nedgements()==20)
        
        OOF.Subproblem.Field.Define(
            subproblem='cyallow.png:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            field=Displacement)
        OOF.Mesh.Field.In_Plane(mesh='cyallow.png:skeleton:mesh',
                                field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            equation=Force_Balance)

        #Pin the bottom boundary
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', mesh='cyallow.png:skeleton:mesh',
            condition=JumpBC(field=Displacement,field_component='y',
                             jump_value=10.0,
                             independent=False,
                             boundary='interface'))

        OOF.Solver.Solve(
            subproblem='cyallow.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))

        meshobj=meshctxt.getObject()
        numup=0
        for fn in meshobj.funcnode_iterator():
            #Check that half of the nodes shifted up by 10 units.
            delta = fn.displaced_position() - fn.position()
            self.assertAlmostEqual(delta.x, 0.0, 6)
            if delta.y>0.01:
                numup+=1
                self.assertAlmostEqual(delta.y, 10.0, 6)
            else:
                self.assertAlmostEqual(delta.y, 0.0, 6)
        self.assert_(numup==37)

        #Create a skeleton boundary from an interface definition, and
        #apply the same jump condition across it.
        OOF.Skeleton.Boundary.Construct(
            skeleton='cyallow.png:skeleton',
            name='boundary',
            constructor=EdgeFromInterface(interface='interface',
                                          direction='Right to left'))
        #Remove an interface, which triggers a mesh rebuild, which
        #puts the new boundaries into the mesh. This should also
        #remove the BC assigned to the interface.
        OOF.Microstructure.Interface.Delete(microstructure='cyallow.png',
                                            interface='interface')

        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', mesh='cyallow.png:skeleton:mesh',
            condition=JumpBC(field=Displacement,field_component='y',
                             jump_value=10.0,
                             independent=False,
                             boundary='boundary'))

        OOF.Mesh.Set_Field_Initializer(
            mesh='cyallow.png:skeleton:mesh',
            field=Displacement,
            initializer=ConstTwoVectorFieldInit(cx=0.0,cy=0.0))

        OOF.Solver.Solve(
            subproblem='cyallow.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))

        self.assert_(meshctxt.nnodes()==74)
        self.assert_(meshctxt.nedgements()==20)

        meshobj=meshctxt.getObject()
        numup=0
        for fn in meshobj.funcnode_iterator():
            #Check that half of the nodes shifted up by 10 units.
            delta = fn.displaced_position() - fn.position()
            self.assertAlmostEqual(delta.x, 0.0, 6)
            if delta.y>0.01:
                numup+=1
                self.assertAlmostEqual(delta.y, 10.0, 6)
            else:
                self.assertAlmostEqual(delta.y, 0.0, 6)
        self.assert_(numup==37)

    #Mr. Gorbachev...
    def tearDown(self):
        OOF.Microstructure.Delete(microstructure="cyallow.png")
        OOF.Material.Delete(name='material')
        OOF.Material.Delete(name='material<2>')
        OOF.Material.Delete(name='interfacematerial')
        OOF.Property.Delete(
            property='Mechanical:Interface:SurfaceTension:Isotropic:simpletension')
        OOF.Property.Delete(
            property='Mechanical:Elasticity:Isotropic:simpleelasticity')

class OOF_InterfaceTest2(unittest.TestCase):
    def setUp(self):
        random.seed(17)
        OOF.Microstructure.Create_From_ImageFile(
            filename='../examples/serendipity.png',
            microstructure_name='serendipity.png',
            height=automatic, width=automatic)
        OOF.Image.AutoGroup(image='serendipity.png:serendipity.png',
                            name_template='%c')
        
        OOF.Property.Copy(property='Mechanical:Elasticity:Isotropic',
                          new_name='simpleelasticity')
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.simpleelasticity(
            cijkl=IsotropicRank4TensorEnu(young=0.66666666666666663,
                                          poisson=0.33333333333333331))
        OOF.Material.New(name='material', material_type='bulk')
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic:simpleelasticity')
        OOF.Material.Assign(material='material',
                            microstructure='serendipity.png', pixels=all)
        #Use Auto Skeleton
        OOF.Skeleton.New(
            name='skeleton', microstructure='serendipity.png',
            x_elements=2, y_elements=2,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))
        OOF.Skeleton.Modify(
            skeleton='serendipity.png:skeleton',
            modifier=Refine(
                targets=CheckHomogeneity(threshold=0.90000000000000002),
                criterion=Unconditionally(),
                degree=Bisection(rule_set='liberal'),
                alpha=0.80000000000000004))
        OOF.Skeleton.Modify(
            skeleton='serendipity.png:skeleton',
            modifier=Refine(
                targets=CheckHomogeneity(threshold=0.90000000000000002),
                criterion=Unconditionally(),
                degree=Bisection(rule_set='liberal'),
                alpha=0.80000000000000004))
        OOF.Skeleton.Modify(
            skeleton='serendipity.png:skeleton',
            modifier=Refine(
                targets=CheckHomogeneity(threshold=0.90000000000000002),
                criterion=Unconditionally(),
                degree=Bisection(rule_set='liberal'),
                alpha=0.80000000000000004))
        OOF.Skeleton.Modify(
            skeleton='serendipity.png:skeleton',
            modifier=SnapRefine(
                targets=CheckHomogeneity(threshold=0.90000000000000002),
                criterion=Unconditionally(),min_distance=0.01))
        OOF.Skeleton.Modify(
            skeleton='serendipity.png:skeleton',
            modifier=Rationalize(
                targets=AllElements(),
                criterion=AverageEnergy(alpha=0.80000000000000004),
                method=SpecificRationalization(
                    rationalizers=[RemoveShortSide(ratio=5.0),
                                   QuadSplit(angle=150),
                                   RemoveBadTriangle(acute_angle=15,
                                                     obtuse_angle=150)])))
        OOF.Skeleton.Modify(
            skeleton='serendipity.png:skeleton',
            modifier=Rationalize(
                targets=AllElements(),
                criterion=AverageEnergy(alpha=0.80000000000000004),
                method=SpecificRationalization(
                    rationalizers=[RemoveShortSide(ratio=5.0),
                                   QuadSplit(angle=150),
                                   RemoveBadTriangle(acute_angle=15,
                                                     obtuse_angle=150)])))
        OOF.Skeleton.PinNodes.Pin_Internal_Boundary_Nodes(
            skeleton='serendipity.png:skeleton')
        OOF.Skeleton.Modify(
            skeleton='serendipity.png:skeleton',
            modifier=Smooth(targets=AllNodes(),
                            criterion=AverageEnergy(alpha=0.29999999999999999),
                            T=0.0,iteration=FixedIteration(iterations=5)))
        OOF.Skeleton.PinNodes.Undo(skeleton='serendipity.png:skeleton')

    # Create a non-sequenceable boundary based on an interface
    # definition and apply a jump condition
    def DisconnectedBoundaryJump(self):
        from ooflib.engine import mesh
        OOF.Microstructure.Interface.New(
            microstructure='serendipity.png',
            name='interface',
            interface_type=PixelGroupInterface(
                left='RGBColor(red=1.00000,green=0.00000,blue=0.00000)',
                right='RGBColor(red=0.00000,green=1.00000,blue=1.00000)'))
        OOF.Skeleton.Boundary.Construct(
            skeleton='serendipity.png:skeleton',
            name='boundary',
            constructor=EdgeFromInterface(interface='interface',
                                          direction='Non-sequenceable'))
        OOF.Mesh.New(
            name='mesh', skeleton='serendipity.png:skeleton',
            element_types=['D2_2', 'T3_3', 'Q4_4'])

        meshctxt=mesh.meshes["serendipity.png:skeleton:mesh"]
        self.assert_(meshctxt.nnodes()==219)
        self.assert_(meshctxt.nedgements()==45)

        OOF.Subproblem.Field.Define(
            subproblem='serendipity.png:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='serendipity.png:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='serendipity.png:skeleton:mesh:default',
            equation=Force_Balance)
        OOF.Subproblem.Equation.Activate(
            subproblem='serendipity.png:skeleton:mesh:default',
            equation=Plane_Stress)
        
        #Pin the top boundary
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='serendipity.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='top'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='serendipity.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='top'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>',
            mesh='serendipity.png:skeleton:mesh',
            condition=JumpBC(field=Displacement,field_component='x',
                             jump_value=10.0,
                             independent=False,
                             boundary='boundary'))

        OOF.Solver.Solve(
            subproblem='serendipity.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))
        meshobj=meshctxt.getObject()
        nodelist=[]
        numjumps=0
        for edgement in meshobj.edgement_iterator():
            if edgement.name()!='boundary':
                continue
            ei=edgement.node_iterator()
            while not ei.end():
                realnode1=ei.node()
                realnode2=ei.node2()
                if realnode1 in nodelist:
                    ei.increment()
                    continue
                nodelist.append(realnode1)
                nodelist.append(realnode2)
                if realnode1!=realnode2:
                    #Check that the "partner" nodes in the edgement
                    #have separated by the right amount.
                    delta = (realnode1.displaced_position()
                             - realnode2.displaced_position())
                    self.assertAlmostEqual(delta**2, 100.0, 6)
                    numjumps+=1
                ei.increment()
        self.assert_(numjumps==11)

    def tearDown(self):
        OOF.Microstructure.Delete(microstructure="serendipity.png")
        OOF.Material.Delete(name='material')
        OOF.Property.Delete(
            property='Mechanical:Elasticity:Isotropic:simpleelasticity')

#Test that the continuity of the fields across an interior boundary
#gives the same solution as when the interior boundary is absent.
class OOF_InterfaceTest3(unittest.TestCase):
    def setUp(self):
        #Create two microstructures based on the same image
        OOF.Microstructure.Create_From_ImageFile(
            filename='../examples/cyallow.png',
            microstructure_name='cyallow.png',
            height=automatic, width=automatic)
        OOF.Image.AutoGroup(image='cyallow.png:cyallow.png', name_template='%c')
        #Make a copy of the first one
        OOF.Microstructure.Copy(microstructure='cyallow.png',
                                name='cyallow.png.Copy')

        #Create two elastic properties
        OOF.Property.Copy(property='Mechanical:Elasticity:Isotropic',
                          new_name='simpleelasticity')
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.simpleelasticity(
            cijkl=IsotropicRank4TensorEnu(young=1,poisson=0.3))
        OOF.Property.Copy(property='Mechanical:Elasticity:Isotropic',
                          new_name='simpleelasticity2')
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.simpleelasticity2(
            cijkl=IsotropicRank4TensorEnu(young=4,poisson=0.3))

        #Create two thermal properties
        OOF.Property.Copy(property='Thermal:Conductivity:Isotropic',
                          new_name='simpleconductivity')
        OOF.Property.Parametrize.Thermal.Conductivity.Isotropic.simpleconductivity(
            kappa=1.0)
        OOF.Property.Copy(property='Thermal:Conductivity:Isotropic',
                          new_name='simpleconductivity2')
        OOF.Property.Parametrize.Thermal.Conductivity.Isotropic.simpleconductivity2(
            kappa=2.0)

        #Create two materials
        OOF.Material.New(name='material', material_type='bulk')
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic:simpleelasticity')
        OOF.Material.Add_property(
            name='material',
            property='Thermal:Conductivity:Isotropic:simpleconductivity')
        OOF.Material.Assign(material='material', microstructure='cyallow.png',
                            pixels='RGBColor(red=1.00000,green=1.00000,blue=0.00000)')
        OOF.Material.Assign(
            material='material', microstructure='cyallow.png.Copy',
            pixels='RGBColor(red=1.00000,green=1.00000,blue=0.00000)')
        OOF.Material.New(name='material<2>', material_type='bulk')
        OOF.Material.Add_property(
            name='material<2>',
            property='Mechanical:Elasticity:Isotropic:simpleelasticity2')
        OOF.Material.Add_property(
            name='material<2>',
            property='Thermal:Conductivity:Isotropic:simpleconductivity2')
        OOF.Material.Assign(
            material='material<2>', microstructure='cyallow.png',
            pixels='RGBColor(red=0.00000,green=1.00000,blue=1.00000)')
        OOF.Material.Assign(
            material='material<2>', microstructure='cyallow.png.Copy',
            pixels='RGBColor(red=0.00000,green=1.00000,blue=1.00000)')

        #Create a skeleton for each microstructure
        OOF.Skeleton.New(
            name='skeleton', microstructure='cyallow.png',
            x_elements=4, y_elements=4,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))

        OOF.Skeleton.New(
            name='skeleton', microstructure='cyallow.png.Copy',
            x_elements=4, y_elements=4,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))

    def Stretch(self):
        from ooflib.engine import mesh
        #Create a mesh
        OOF.Mesh.New(name='mesh', skeleton='cyallow.png:skeleton',
                     element_types=['D2_2', 'T3_3', 'Q4_4'])
        meshctxt=mesh.meshes["cyallow.png:skeleton:mesh"]
        self.assert_(meshctxt.nnodes()==25)
        self.assert_(meshctxt.nedgements()==16)

        #For the second microstructure, define an interface
        OOF.Microstructure.Interface.New(
            microstructure='cyallow.png.Copy',
            name='interface',
            interface_type=MaterialInterface(left='material',
                                             right='material<2>'))
        OOF.Mesh.New(name='mesh', skeleton='cyallow.png.Copy:skeleton', 
                     element_types=['D2_2', 'T3_3', 'Q4_4'])
        meshctxt2=mesh.meshes["cyallow.png.Copy:skeleton:mesh"]
        self.assert_(meshctxt2.nnodes()==30)
        self.assert_(meshctxt2.nedgements()==20)

        #Plane strain case
        OOF.Subproblem.Field.Define(
            subproblem='cyallow.png:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            field=Displacement)
        OOF.Mesh.Field.In_Plane(mesh='cyallow.png:skeleton:mesh', 
                                field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            equation=Force_Balance)

        OOF.Subproblem.Field.Define(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            field=Displacement)
        OOF.Mesh.Field.In_Plane(
            mesh='cyallow.png.Copy:skeleton:mesh', field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            equation=Force_Balance)

        #Set BCs
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='top'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,
                                  field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='y'),
                                  boundary='top'))

        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='cyallow.png.Copy:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='top'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='cyallow.png.Copy:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', mesh='cyallow.png.Copy:skeleton:mesh',
            condition=DirichletBC(field=Displacement,
                                  field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>', mesh='cyallow.png.Copy:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='y'),
                                  boundary='top'))
        
        #Solve 'em
        OOF.Solver.Solve(
            subproblem='cyallow.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))
        OOF.Solver.Solve(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))

        #Make a table of the solutions, then compare
        solutiondict={}
        meshobj=meshctxt.getObject()
        for fn in meshobj.funcnode_iterator():
            solutiondict[(fn.position().x,fn.position().y)] = \
                fn.displaced_position()
        meshobj2=meshctxt2.getObject()
        for fn in meshobj2.funcnode_iterator():
            s2=fn.displaced_position()
            s1=solutiondict[(fn.position().x,fn.position().y)]
            self.assertAlmostEqual(s1.x, s2.x, 6)
            self.assertAlmostEqual(s1.y, s2.y, 6)

        #Plane stress case
        OOF.Mesh.Field.Out_of_Plane(mesh='cyallow.png:skeleton:mesh',
                                    field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            equation=Plane_Stress)
        OOF.Mesh.Field.Out_of_Plane(mesh='cyallow.png.Copy:skeleton:mesh',
                                    field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            equation=Plane_Stress)

        #Solve 'em
        OOF.Solver.Solve(
            subproblem='cyallow.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))
        OOF.Solver.Solve(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))

        #Make a table of the solutions, then compare
        solutiondict={}
        meshobj=meshctxt.getObject()
        for fn in meshobj.funcnode_iterator():
            solutiondict[(fn.position().x,fn.position().y)] = \
                fn.displaced_position()
        meshobj2=meshctxt2.getObject()
        for fn in meshobj2.funcnode_iterator():
            s2=fn.displaced_position()
            s1=solutiondict[(fn.position().x,fn.position().y)]
            self.assertAlmostEqual(s1.x, s2.x, 6)
            self.assertAlmostEqual(s1.y, s2.y, 6)

    def Heat(self):
        from ooflib.engine import mesh
        #Create a mesh
        OOF.Mesh.New(name='mesh', skeleton='cyallow.png:skeleton', 
                     element_types=['D2_2', 'T3_3', 'Q4_4'])
        meshctxt=mesh.meshes["cyallow.png:skeleton:mesh"]
        self.assert_(meshctxt.nnodes()==25)
        self.assert_(meshctxt.nedgements()==16)

        #For the second microstructure, define an interface
        OOF.Microstructure.Interface.New(
            microstructure='cyallow.png.Copy',
            name='interface',
            interface_type=MaterialInterface(left='material',
                                             right='material<2>'))
        OOF.Mesh.New(name='mesh', skeleton='cyallow.png.Copy:skeleton', 
                     element_types=['D2_2', 'T3_3', 'Q4_4'])
        meshctxt2=mesh.meshes["cyallow.png.Copy:skeleton:mesh"]
        self.assert_(meshctxt2.nnodes()==30)
        self.assert_(meshctxt2.nedgements()==20)

        #in-plane
        OOF.Subproblem.Field.Define(
            subproblem='cyallow.png:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            field=Temperature)
        OOF.Mesh.Field.In_Plane(mesh='cyallow.png:skeleton:mesh',
                                field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            equation=Heat_Eqn)

        OOF.Subproblem.Field.Define(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            field=Temperature)
        OOF.Mesh.Field.In_Plane(mesh='cyallow.png.Copy:skeleton:mesh',
                                field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            equation=Heat_Eqn)

        #Set BCs
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ContinuumProfile(function='x'),
                                  boundary='top'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='cyallow.png:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))

        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='cyallow.png.Copy:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ContinuumProfile(function='x'),
                                  boundary='top'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='cyallow.png.Copy:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='bottom'))

        #Solve 'em
        OOF.Solver.Solve(
            subproblem='cyallow.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))
        OOF.Solver.Solve(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))

        #Make a table of the solutions, then compare
        solutiondict={}
        meshobj=meshctxt.getObject()
        for fn in meshobj.funcnode_iterator():
            solutiondict[(fn.position().x,fn.position().y)] = \
                Temperature.value(fn,0)
        meshobj2=meshctxt2.getObject()
        for fn in meshobj2.funcnode_iterator():
            s2=Temperature.value(fn,0)
            s1=solutiondict[(fn.position().x,fn.position().y)]
            self.assertAlmostEqual(s1, s2, 6)

        #Plane_Heat_Flux. There seems to be no difference with the
        #in-plane solution.
        OOF.Mesh.Field.Out_of_Plane(mesh='cyallow.png:skeleton:mesh',
                                    field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png:skeleton:mesh:default',
            equation=Plane_Heat_Flux)
        OOF.Mesh.Field.Out_of_Plane(mesh='cyallow.png.Copy:skeleton:mesh', 
                                    field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            equation=Plane_Heat_Flux)

        #Solve 'em
        OOF.Solver.Solve(
            subproblem='cyallow.png:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))
        OOF.Solver.Solve(
            subproblem='cyallow.png.Copy:skeleton:mesh:default',
            solver=LinearDriver(
                method=CGSolver(max_iterations=1000,
                                tolerance=1e-13,
                                preconditioner=ILUPreconditioner())))

        #Make a table of the solutions, then compare
        solutiondict={}
        meshobj=meshctxt.getObject()
        for fn in meshobj.funcnode_iterator():
            solutiondict[(fn.position().x,fn.position().y)] = \
                Temperature.value(fn,0)
        meshobj2=meshctxt2.getObject()
        for fn in meshobj2.funcnode_iterator():
            s2=Temperature.value(fn,0)
            s1=solutiondict[(fn.position().x,fn.position().y)]
            self.assertAlmostEqual(s1, s2, 6)

    def tearDown(self):
        OOF.Microstructure.Delete(microstructure="cyallow.png")
        OOF.Microstructure.Delete(microstructure="cyallow.png.Copy")
        OOF.Material.Delete(name='material')
        OOF.Material.Delete(name='material<2>')
        OOF.Property.Delete(
            property='Mechanical:Elasticity:Isotropic:simpleelasticity')
        OOF.Property.Delete(
            property='Mechanical:Elasticity:Isotropic:simpleelasticity2')
        OOF.Property.Delete(
            property='Thermal:Conductivity:Isotropic:simpleconductivity')
        OOF.Property.Delete(
            property='Thermal:Conductivity:Isotropic:simpleconductivity2')

# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.
def run_tests():

    test_set = [
        OOF_SimpleInterfaceTest("InterfaceTension"),
        OOF_SimpleInterfaceTest("DetachedMesh"),
        OOF_InterfaceTest2("DisconnectedBoundaryJump"),
        OOF_InterfaceTest3("Stretch"),
        OOF_InterfaceTest3("Heat")
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
