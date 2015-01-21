# -*- python -*-
# $RCSfile: material_property_test.py,v $
# $Revision: 1.27 $
# $Author: langer $
# $Date: 2008/09/08 18:30:06 $

# Test suite for materials and properties.

import unittest, os, filecmp
import memorycheck


# Property menu has Copy, Delete, and Parametrize.  Parametrize is the
# head of a tree of menus replicating the properties known to the
# PropertyManager.  Since properties are stand-alone objects, there's
# no real set-up or tear-down required.
class Property(unittest.TestCase):
    def setUp(self):
        global propertyregistration
        from ooflib.engine import propertyregistration
        self.allprops = propertyregistration.AllProperties
        
    def tearDown(self):
        pass

    # Utility function to get all the nontrivial nonsecret nodes
    # (those with non-None .objects, i.e. property registrations,
    # which themselves are not secret) out of the AllProperties
    # labeltree.  Regs can occur at non-leaf nodes if copying
    # operations have already happened.
    def labeltree2list(self, lt):
        result = []
        if lt.nodes:
            if lt.object and not lt.object.secret():
                result = [lt]
            for c in lt.nodes:
                result.extend(self.labeltree2list(c))
        else:
            if not lt.secret():
                result = [lt]
        return result

    @memorycheck.check()
    def Copy(self):
        proplist = self.labeltree2list(self.allprops.data)
        # p contains the *name* of the property to copy. 
        for p in [x.path() for x in proplist]:
            OOF.Property.Copy(property=p, new_name="copy_test")
            new_p = self.allprops[p + ":copy_test"]
            self.assertEqual(new_p.__class__.__name__,
                             "NamedPropertyRegistration")
        # Check that colons are prohibited in Property names
        from ooflib.common.IO import parameter
        self.assertRaises(parameter.ParameterMismatch, OOF.Property.Copy,
                          property='Color', new_name='abc:def')
            

    # Assumes the "Copy" has been run successfully.
    @memorycheck.check()
    def Delete(self):
        proplist = self.labeltree2list(self.allprops.data)
        for p in proplist:
            if p.object.name().split(':')[-1] == "copy_test":
                OOF.Property.Delete(property=p.path())
        new_proplist = self.labeltree2list(self.allprops.data)
        for p in new_proplist:
            self.assert_(p in proplist)
            self.assertNotEqual(
                p.object.name().split(':')[-1], "copy_test")
            

    # Reparametrizes the "default" properties, not copies, and adds
    # them to a Material.
    @memorycheck.check()
    def Parametrize(self):
        global parametrize_dict
        parammenu = OOF.Property.Parametrize
        proplist = self.labeltree2list(self.allprops.data)
        OOF.Material.New(name="prop_mat")
        try:
            for p in proplist:
                thisparammenu = parammenu
                ppath = p.path()
                for n in ppath.split(':'):
                    thisparammenu = thisparammenu.getItem(n)
                try:
                    argset = parametrize_dict[ppath]
                except KeyError:
                    print >> sys.stderr,  "No parametrization test for property ", p.path()
                    OOF.Material.Add_property(name="prop_mat",
                                              property=p.path())
                    OOF.Material.Remove_property(name="prop_mat",
                                                 property=p.path())
                else:
                    for argdict in argset:
                        # Save the old values of the parameters...
                        old_values = {}
                        for param in p.object.params:
                            old_values[param.name]=param.value

                        thisparammenu.callWithDefaults(**argdict)
                        OOF.Material.Add_property(name="prop_mat",
                                                  property=ppath)

                        # Check that the params in the registration object
                        # match the ones you wanted from the dictionary.
                        # Obviously this is only meaningful if the
                        # dictionary-supplied numbers are nondefault.
                        for param in p.object.params:
                            self.assertEqual(param.value, argdict[param.name])

                        # Restore the old values -- if the first one worked,
                        # this one should also.
                        thisparammenu.callWithDefaults(**old_values)
                        OOF.Material.Remove_property(name="prop_mat",
                                                     property=ppath)
        finally:
            OOF.Material.Delete(name="prop_mat")


class MaterialBasic(unittest.TestCase):
    def setUp(self):
        global materialmanager
        from ooflib.engine import materialmanager
        self.mat_manager = materialmanager.materialmanager
        global material
        from ooflib.SWIG.engine import material
        global microstructure
        from ooflib.common import microstructure
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="mat_test", height=20.0,
            width=20.0)
        OOF.Image.AutoGroup(image="mat_test:small.ppm")

    def ms(self):
        # setUp used to set self.ms to the microstructure.  Making
        # self.ms a function prevents the Unittest object from holding
        # a reference to the microstructure, which would mess up the
        # memorycheck tests.
        return microstructure.getMicrostructure("mat_test")
    
        
    # We can't count on the props having default values, they may have
    # been modified by the property tester, but then again, it may not
    # have been run.
    
    @memorycheck.check("mat_test")
    def New(self):
        OOF.Material.New(name="new_mat");
        self.assertEqual(len(self.mat_manager.materials), 1)
        # self.mat_manager returns MaterialProps objects.
        mat = self.mat_manager["new_mat"]
        self.assertEqual(mat.name, "new_mat")

    # Delete assumes that New has just been run successfully.
    @memorycheck.check("mat_test")
    def Delete(self):
        OOF.Material.Delete(name="new_mat");
        self.assertEqual(len(self.mat_manager.materials), 0)


    # These two tests have to be in here, because the "Ops" tests
    # (below) delete the material in between tests.  For Add_property
    # and Remove_property, we want the property (and thus the
    # material) to persist between tests.

    # Assumes no properties are present.
    @memorycheck.check("mat_test")
    def Add_property(self):
        from ooflib.engine import propertyregistration
        OOF.Material.New(name="new_mat")
        OOF.Material.Add_property(name="new_mat",
                                  property="Mechanical:Elasticity:Isotropic")
        self.assertEqual(len(self.mat_manager.materials),1)
        mat = self.mat_manager["new_mat"]
        self.assertEqual(len(mat.data),1)
        (key, val) = mat.data.items()[0]
        self.assertEqual(key, "Mechanical:Elasticity:Isotropic")
        self.assertEqual(val,
                         propertyregistration.AllProperties[
            "Mechanical:Elasticity:Isotropic"])
        

    # Assumes the previous test has run, and the elasticity property
    # is present.
    @memorycheck.check("mat_test")
    def Remove_property(self):
        OOF.Material.Remove_property(
            name="new_mat",  property="Mechanical:Elasticity:Isotropic")
        self.assertEqual(len(self.mat_manager.materials), 1)
        mat = self.mat_manager["new_mat"]
        self.assertEqual(len(mat.data),0)
        OOF.Material.Delete(name="new_mat")



class MaterialOps(MaterialBasic):
    def setUp(self):
        MaterialBasic.setUp(self)
        OOF.Material.New(name="new_mat")

    def tearDown(self):
        OOF.Material.Delete(name="new_mat")
        MaterialBasic.tearDown(self)

    # Copy is deferred to here so that it can copy nontrivial materials.  
    @memorycheck.check("mat_test")
    def Copy(self):
        OOF.Material.Add_property(
            name="new_mat", property="Mechanical:Elasticity:Isotropic")
        OOF.Material.Copy(name="new_mat", new_name="mat_copy")
        self.assertEqual(len(self.mat_manager.materials), 2)
        mat1 = self.mat_manager["new_mat"]
        mat2 = self.mat_manager["mat_copy"]
        self.assertEqual(mat2.name, "mat_copy")
        self.assertEqual(len(mat2.data), 1)
        self.assertEqual(mat1.data["Mechanical:Elasticity:Isotropic"],
                         mat2.data["Mechanical:Elasticity:Isotropic"])
        OOF.Material.Delete(name="mat_copy")

    @memorycheck.check("mat_test")
    def Rename(self):
        OOF.Material.Add_property(
            name="new_mat", property="Mechanical:Elasticity:Isotropic")
        OOF.Material.Rename(material="new_mat", name="mat_copy")
        self.assertEqual(len(self.mat_manager.materials), 1)
        mat1 = self.mat_manager["mat_copy"]
        self.assertEqual(mat1.name, "mat_copy")
        self.assertEqual(len(mat1.data), 1)
        # Now rename it back, so tear-down can remove it.
        OOF.Material.Rename(material="mat_copy", name="new_mat")
        

    # Utility function -- finds the reddest autogroup, and renames it
    # "red", for convenience later.  Autogroup names can be round-off
    # sensitive.
    def redgroup(self):
        from ooflib.common import color
        def colordiff(c1,c2):
            return (c1.red-c2.red)**2 + \
                   (c1.green-c2.green)**2 + \
                   (c1.blue-c2.blue)**2
        diff = None
        for name in self.ms().groupNames():
            rgb = eval(name)
            red_diff =  colordiff(rgb, color.red)
            if diff==None or red_diff < diff:
                red_name = name
                diff =  red_diff
        OOF.PixelGroup.Rename(microstructure="mat_test",
                              group=red_name, new_name="red")
        
        
    # Assign, likewise, assumes that the material manager has the
    # "new_mat" material in it.
    @memorycheck.check("mat_test")
    def Assign(self):
        self.redgroup()
        OOF.Material.New(name="stuff")
        OOF.Material.Add_property(name="stuff",
                                  property="Mechanical:Elasticity:Isotropic")
        OOF.Material.Assign(material="stuff",
                            microstructure="mat_test",
                            pixels="red")
        mat = self.mat_manager["stuff"].actual
        # Then figure out if it worked.  Check pixels for group
        # membership and material assignment.  This is quite slow.
        redgroup = self.ms().findGroup("red").members()
        for c in self.ms().coords():
            ms_mat = material.getMaterialFromPoint(self.ms(), c)
            if c in redgroup:
                self.assertEqual(ms_mat, mat)
            else:
                self.assertEqual(ms_mat, None)
        OOF.Material.Delete(name="stuff")
                
            

    # Removes material from pixels.  Assumes the previous test has
    # been run, so that the "stuff" material exists.
    @memorycheck.check("mat_test")
    def Remove(self):
        self.redgroup()
        OOF.Material.New(name="stuff")
        OOF.Material.Add_property(name="stuff",
                                  property="Mechanical:Elasticity:Isotropic")
        OOF.Material.Assign(material="stuff",
                            microstructure="mat_test",
                            pixels="red")
        OOF.Material.Remove(microstructure="mat_test",
                            pixels="red")
        for c in self.ms().coords():
            ms_mat = material.getMaterialFromPoint(self.ms(), c)
            self.assertEqual(ms_mat, None)

        OOF.Material.Delete(name="stuff")


    @memorycheck.check("mat_test")
    def Delete2(self):
        # Delete a Material without removing it from pixels, and check
        # to see that it has been removed automatically.
        self.redgroup()
        OOF.Material.New(name="stuff")
        OOF.Material.Assign(material="stuff", microstructure="mat_test",
                            pixels=all)
        OOF.Material.Delete(name="stuff")
        for c in self.ms().coords():
            ms_mat = material.getMaterialFromPoint(self.ms(), c)
            self.assertEqual(ms_mat, None)


class MatPropIO(unittest.TestCase):
    def setUp(self):
        global propertyregistration
        from ooflib.engine import propertyregistration
        self.allprops = propertyregistration.AllProperties
        global materialmanager
        from ooflib.engine import materialmanager
        self.mat_manager = materialmanager.materialmanager
        
        
    @memorycheck.check()
    def PropSave(self):
        OOF.Property.Copy(property="Color", new_name="bloo")
        OOF.Property.Parametrize.Color.bloo(
            color=RGBColor(red=0.1,green=0.1,blue=0.9))
        OOF.File.Save.Property(filename="prop_save_test",
                               mode="w", format="ascii",
                               property="Color:bloo")
        self.assert_(filecmp.cmp(os.path.join("matprop_data","propsave"),
                                 "prop_save_test"))
        os.remove("prop_save_test")
        OOF.Property.Delete(property="Color:bloo")
        

    @memorycheck.check()
    def PropLoad(self):
        OOF.File.Load.Data(filename=os.path.join("matprop_data","propload"))
        new_p = self.allprops["Color:load"]
        self.assertEqual(new_p.name().split(':')[-1], "load")
        OOF.Property.Delete(property="Color:load")
                           
    @memorycheck.check()
    def MatSave(self):
        OOF.Material.New(name="save")
        OOF.Property.Copy(property="Color", new_name="check")
        OOF.Property.Parametrize.Color.check(
            color=RGBColor(red=0.2,green=0.3,blue=0.4))
        OOF.Material.Add_property(name="save",
                                  property="Color:check")
        OOF.File.Save.Materials(filename="mat_save_test",
                                mode="w", format="ascii",
                                materials=["save"])
        self.assert_(filecmp.cmp(os.path.join("matprop_data","matsave"),
                                 "mat_save_test"))
        os.remove("mat_save_test")
        OOF.Material.Delete(name="save")
        OOF.Property.Delete(property="Color:check")

    @memorycheck.check()
    def MatLoad(self):
        OOF.File.Load.Data(filename=os.path.join("matprop_data","matload"))
        mat = self.mat_manager["load"]
        prop = self.allprops["Color:check"]
        self.assertEqual(prop.name().split(':')[-1], "check")
        self.assertEqual(mat.name, "load")
        OOF.Material.Delete(name="load")
        OOF.Property.Delete(property="Color:check")


parametrize_dict = {}

def build_parametrize_dict():
    global parametrize_dict 
    parametrize_dict = {
        'Color' :  [ { "color" : Gray(value=0.5) },
                     { "color" : HSVColor(hue=200.0,
                                          saturation=0.5,
                                          value=0.5) },
                     { "color" : RGBColor(red=0.2, green=0.3, blue=0.4) } ],

        'Mechanical:Elasticity:Isotropic' :
        [ {"cijkl" : IsotropicRank4TensorCij(c11=1.5,c12=0.7) },
          {"cijkl" : IsotropicRank4TensorLame(lmbda=0.7,mu=0.3) },
          {"cijkl" : IsotropicRank4TensorEnu(young=0.7,poisson=0.4) },
          {"cijkl" : IsotropicRank4TensorBulkShear(bulk=0.7,shear=0.3) }
          ],

        'Mechanical:Elasticity:Anisotropic:Cubic' :
        [ {"cijkl" : CubicRank4TensorCij(c11=1.5,c12=0.7,c44=0.2)},
          {"cijkl" : CubicRank4TensorLame(lmbda=0.7,mu=0.3,aniso=0.9)},
          {"cijkl" : CubicRank4TensorEnu(young=0.7,poisson=0.4,aniso=0.9)},
          {"cijkl" : CubicRank4TensorBulkShear(bulk=0.7,shear=0.3,aniso=0.9)}
          ],

        'Mechanical:Elasticity:Anisotropic:Hexagonal' :
        [ {"cijkl" : HexagonalRank4TensorCij(c11=0.9,c12=0.4,c13=0.1,
                                             c33=0.1,c44=0.05) }
          ],

        'Mechanical:Elasticity:Anisotropic:Tetragonal' :
        [ {"cijkl" : TetragonalRank4TensorCij(c11=0.9,c12=0.4,c13=0.1,
                                              c33=1.0,c44=0.9,c66=0.8,
                                              c16=0.1) }
          ],

        'Mechanical:Elasticity:Anisotropic:TrigonalA' :
        [ {"cijkl" : TrigonalARank4TensorCij(c11=0.9,c12=0.4,c13=0.1,
                                             c33=0.9,c44=0.2,c14=0.1,
                                             c15=0.1) }
          ],

        'Mechanical:Elasticity:Anisotropic:TrigonalB' :
        [ {"cijkl" : TrigonalBRank4TensorCij(c11=0.9,c12=0.4,c13=0.45,
                                             c33=0.9, c44=0.2,c14=0.1) }
          ],

        'Mechanical:Elasticity:Anisotropic:Orthorhombic' :
        [ {"cijkl" : OrthorhombicRank4TensorCij(c11=0.9,c12=0.4, c13=0.4,
                                                c22=0.8, c23=0.4,c33=0.95,
                                                c44=0.25,c55=0.24, c66=0.23) }
          ],

        'Mechanical:Elasticity:Anisotropic:Monoclinic' : 
        [ {"cijkl" : MonoclinicRank4TensorCij(c11=0.9,c12=0.4,c13=0.39,
                                              c15=0.01,c22=0.8,c23=0.38,
                                              c25=0.1,c33=0.2,c35=0.19,
                                              c44=0.22,c46=0.05,c55=0.21,
                                              c66=0.20) }
          ],

        'Mechanical:Elasticity:Anisotropic:Triclinic' :
        [ {"cijkl" : TriclinicRank4TensorCij(c11=0.9,c12=0.4,c13=0.39,
                                             c14=0.1,c15=0.11,c16=0.12,
                                             c22=0.84,c23=0.38,c24=0.13,
                                             c25=0.14,c26=0.15,c33=0.82,
                                             c34=0.0,c35=0.1,c36=0.09,
                                             c44=0.24,c45=0.08,c46=0.07,
                                             c55=0.23,c56=0.04,c66=0.21) }
          ],

        'Mechanical:Elasticity:ThermoElasticity' :
        [ {'alpha': 0.2, 'cijkl': IsotropicRank4TensorLame(lmbda=0.9,mu=0.4),
           't0': 0.1},
          {'alpha': 0.0, 'cijkl': IsotropicRank4TensorCij(c11=1.9,c12=1.0),
           't0': 0.08},
          {'alpha': 0.3,
           'cijkl': IsotropicRank4TensorEnu(young=1.3333333333333333,
                                            poisson=0.3),
           't0': 0.06},
          {'alpha': 0.4,
           'cijkl': IsotropicRank4TensorBulkShear(bulk=1.3333333333333333,
                                                  shear=0.6),
           't0': 0.04} ],

        'Mechanical:Elasticity:NonLinearElasticity' :
        [ {'hardening': 0.1,
           'cijkl': IsotropicRank4TensorCij(c11=1.0,
                                            c12=0.27777777777777779)},
          {'hardening': 0.2,
           'cijkl': IsotropicRank4TensorLame(lmbda=0.3,
                                             mu=0.41666666666666669) },
          {'hardening': 0.3,
           'cijkl': IsotropicRank4TensorEnu(young=0.8,
                                            poisson=0.20000000000000001)},
          {'hardening': 0.4,
           'cijkl': IsotropicRank4TensorBulkShear(bulk=0.5,
                                                  shear=0.4)}
          ],
        
        'Mechanical:ForceDensity:ConstantForceDensity' : 
        [ {'gz': 0.0, 'gy': -9.75000000000000007, 'gx': 0.0} ],
        
        'Mechanical:MassDensity:ConstantMassDensity' :
        [ {'rho': 0.1} ],

        'Mechanical:StressFreeStrain:Isotropic' :
        [{'epsilon0' : 1.0}],

        'Mechanical:StressFreeStrain:Anisotropic:Cubic':
        [{'epsilon0': CubicRank2Tensor(xx=1.2)}],

        'Mechanical:StressFreeStrain:Anisotropic:Hexagonal':
        [{'epsilon0': HexagonalRank2Tensor(xx=1.2, zz=0.3)}],

        'Mechanical:StressFreeStrain:Anisotropic:Trigonal':
        [{'epsilon0': TrigonalRank2Tensor(xx=2.4, zz=0.2)}],

        'Mechanical:StressFreeStrain:Anisotropic:Tetragonal':
        [{'epsilon0':TetragonalRank2Tensor(xx=1.4, zz=2.1)}],

        'Mechanical:StressFreeStrain:Anisotropic:Orthorhombic':
        [{'epsilon0': OrthorhombicRank2Tensor(xx=1.0, yy=2.0, zz=3.1415)}],

        'Mechanical:StressFreeStrain:Anisotropic:Monoclinic':
        [{'epsilon0': MonoclinicRank2Tensor(xx=10, yy=20, zz=30, xz=2)}],

        'Mechanical:StressFreeStrain:Anisotropic:Triclinic':
        [{'epsilon0': TriclinicRank2Tensor(xx=5.0,yy=4.0, zz=1.0,
                                           yz=0.21,xz=0.1, xy=0.3)}],
        
        'Mechanical:Plasticity:TestPlasticity' : 
        [ {'yield_stress': 1.1} ],
        
        'Thermal:Conductivity:Isotropic' :
        [ {'kappa': 1.2} ],
        
        'Thermal:Conductivity:Anisotropic:Cubic' :
        [ {'kappa': CubicRank2Tensor(xx=1.100000)} ],
        
        'Thermal:Conductivity:Anisotropic:Hexagonal' :
        [ {'kappa': HexagonalRank2Tensor(xx=1.100000, zz=0.600000)} ],
        
        'Thermal:Conductivity:Anisotropic:Tetragonal' :
        [ {'kappa': TetragonalRank2Tensor(xx=1.200000, zz=0.400000)} ],
        
        'Thermal:Conductivity:Anisotropic:Trigonal' :
        [ {'kappa': TrigonalRank2Tensor(xx=1.300000, zz=0.200000)} ],
        
        'Thermal:Conductivity:Anisotropic:Orthorhombic' :
        [ {'kappa': OrthorhombicRank2Tensor(xx=1.100000, yy=1.000000,
                                            zz=1.000000)} ],
        
        'Thermal:Conductivity:Anisotropic:Monoclinic' : 
        [ {'kappa': MonoclinicRank2Tensor(xx=1.000000, yy=1.100000,
                                          zz=1.000000, xz=0.500000)} ],
        
        'Thermal:Conductivity:Anisotropic:Triclinic' :
        [ {'kappa': TriclinicRank2Tensor(xx=1.000000,yy=1.000000, zz=1.000000,
                                         yz=0.010000,xz=0.000000,
                                         xy=0.000000)} ],
        
        'Thermal:HeatCapacity:ConstantHeatCapacity' :
        [ {'cv': 1.1} ],
        
        'Thermal:HeatSource' :
        [ {'rate': 0.1} ],
        
        'Electric:DielectricPermittivity:Isotropic' : 
        [ {'epsilon': 1.2} ],
        
        'Electric:DielectricPermittivity:Anisotropic:Cubic' :
        [ {'epsilon': CubicRank2Tensor(xx=1.900000)} ],
        
        'Electric:DielectricPermittivity:Anisotropic:Hexagonal' :
        [ {'epsilon': HexagonalRank2Tensor(xx=1.800000, zz=0.500000)} ],

        'Electric:DielectricPermittivity:Anisotropic:Tetragonal' : 
        [ {'epsilon': TetragonalRank2Tensor(xx=1.700000, zz=1.000000)} ],
        
        'Electric:DielectricPermittivity:Anisotropic:Trigonal' :
        [ {'epsilon': TrigonalRank2Tensor(xx=1.600000, zz=0.500000)} ],
        
        'Electric:DielectricPermittivity:Anisotropic:Orthorhombic' :
        [ {'epsilon': OrthorhombicRank2Tensor(xx=1.500000,
                                              yy=1.000000, zz=1.000000)} ],
        
        'Electric:DielectricPermittivity:Anisotropic:Monoclinic' :
        [ {'epsilon': MonoclinicRank2Tensor(xx=1.000000, yy=1.000000,
                                            zz=1.500000, xz=0.500000)} ],

        'Electric:DielectricPermittivity:Anisotropic:Triclinic' :
        [ {'epsilon': TriclinicRank2Tensor(xx=1.000000,yy=1.000000,
                                         zz=1.000000,yz=0.000000,
                                         xz=0.050000,xy=0.000000)} ],
    
        'Electric:SpaceCharge' :
        [ {'charge': 0.2} ],
        
        'Orientation' :
        [ {'angles': Abg(alpha=0.1,beta=0.0,gamma=0.0)},
          {'angles': X(phi=0.2,theta=0.0,psi=0.0)},
          {'angles': XYZ(phi=0.3,theta=0.0,psi=0.0)},
          {'angles': Axis(angle=0.4,x=0.0,y=0.0,z=1.0)},
          {'angles': Quaternion(e0=1.0,e1=0.1,e2=0.0,e3=0.0)},
          {'angles': Rodrigues(r1=0.1,r2=0.0,r3=0.0)},
          {'angles': Bunge(phi1=0.0,theta=0.2,phi2=0.0)} ],

        'Couplings:ThermalExpansion:Isotropic' :
        [ {'alpha': 1.1, 'T0': 0.1} ],
        
        'Couplings:ThermalExpansion:Anisotropic:Cubic' :
        [ {'alpha': CubicRank2Tensor(xx=1.100000), 'T0': 1.0} ],

        'Couplings:ThermalExpansion:Anisotropic:Hexagonal' :
        [ {'alpha': HexagonalRank2Tensor(xx=1.000000, zz=0.400000),
           'T0': 1.1} ],

        'Couplings:ThermalExpansion:Anisotropic:Trigonal' :
        [ {'alpha': TrigonalRank2Tensor(xx=1.200000, zz=0.500000),
           'T0': 0.2} ],
        
        'Couplings:ThermalExpansion:Anisotropic:Tetragonal' :
        [ {'alpha': TetragonalRank2Tensor(xx=1.300000, zz=0.500000),
           'T0': 0.3} ],
        
        'Couplings:ThermalExpansion:Anisotropic:Orthorhombic' :
        [ {'alpha': OrthorhombicRank2Tensor(xx=1.400000, yy=1.000000,
                                            zz=1.000000),
           'T0': 0.4} ],
        
        'Couplings:ThermalExpansion:Anisotropic:Monoclinic' :
        [ {'alpha': MonoclinicRank2Tensor(xx=1.000000, yy=1.000000,
                                          zz=1.400000, xz=0.500000),
           'T0': 0.5} ],
        
        'Couplings:ThermalExpansion:Anisotropic:Triclinic' :
        [ {'alpha': TriclinicRank2Tensor(xx=1.000000,yy=1.000000,
                                         zz=1.400000,yz=0.000000,
                                         xz=0.000000,xy=0.000000),
           'T0': 0.6} ],

        'Couplings:PiezoElectricity:Cubic:Td' :
        [ {'dijk': TdRank3Tensor(d14=1.1)} ],
        
        'Couplings:PiezoElectricity:Hexagonal:D3h' :
        [ {'dijk': D3hRank3Tensor(d22=1.1)} ],
        
        'Couplings:PiezoElectricity:Hexagonal:C6v' :
        [ {'dijk': C6vRank3Tensor(d15=1, d31=1.1, d33=1)} ],
        
        'Couplings:PiezoElectricity:Hexagonal:D6' : 
        [ {'dijk': D6Rank3Tensor(d14=1.2)} ],
        
        'Couplings:PiezoElectricity:Hexagonal:D6i' :
        [ {'dijk': D6iRank3Tensor(d11=1.1, d22=1)} ],
        
        'Couplings:PiezoElectricity:Hexagonal:C6' :
        [ {'dijk': C6Rank3Tensor(d14=1, d15=1.2, d31=1, d33=1)} ],
        
        'Couplings:PiezoElectricity:Trigonal:C3v' :
        [ {'dijk': C3vRank3Tensor(d15=1, d22=1.2, d31=1, d33=1)} ],
        
        'Couplings:PiezoElectricity:Trigonal:D3' :
        [ {'dijk': D3Rank3Tensor(d11=1.3, d14=1)} ],
        
        'Couplings:PiezoElectricity:Trigonal:C3' :
        [ {'dijk': C3Rank3Tensor(d11=1, d14=1, d15=1, d22=1,
                                 d31=1, d33=1.3)} ],
        
        'Couplings:PiezoElectricity:Tetragonal:D2d' :
        [ {'dijk': D2dRank3Tensor(d14=1, d36=1.2)} ],
        
        'Couplings:PiezoElectricity:Tetragonal:C4v' :
        [ {'dijk': C4vRank3Tensor(d15=1.2, d31=1, d33=1)} ],
        
        'Couplings:PiezoElectricity:Tetragonal:D4' :
        [ {'dijk': D4Rank3Tensor(d14=1.1)} ],
        
        'Couplings:PiezoElectricity:Tetragonal:C4i' :
        [ {'dijk': C4iRank3Tensor(d14=1, d15=1.2, d31=1, d36=1)} ],
        
        'Couplings:PiezoElectricity:Tetragonal:C4' :
        [ {'dijk': C4Rank3Tensor(d14=1, d15=1.3, d31=1, d33=1)} ],
        
        'Couplings:PiezoElectricity:Orthorhombic:C2v' :
        [ {'dijk': C2vRank3Tensor(d15=1, d24=1.05, d31=1, d32=1, d33=1)} ],
        
        'Couplings:PiezoElectricity:Orthorhombic:D2' :
        [ {'dijk': D2Rank3Tensor(d14=1, d25=1.1, d36=1)} ],
        
        'Couplings:PiezoElectricity:Monoclinic:Cs' :
        [ {'dijk': CsRank3Tensor(d11 = 1.4, d12 = 1, d13 = 1, d15 = 1,
                                 d24 = 1, d26 = 1, d31 = 1, d32 = 1,
                                 d33 = 1, d35 = 1)} ],
        
        'Couplings:PiezoElectricity:Monoclinic:C2' :
        [ {'dijk': C2Rank3Tensor(d14 = 1.2, d16 = 1, d21 = 1, d22 = 1,
                                 d23 = 1, d25 = 1, d34 = 1, d36 = 1)} ],
        
        'Couplings:PiezoElectricity:Triclinic:C1' :
        [ {'dijk': C1Rank3Tensor(d11 = 1.8, d12 = 1, d13 = 1, d14 = 1,
                                 d15 = 1, d16 = 1, d21 = 1, d22 = 1,
                                 d23 = 1, d24 = 1, d25 = 1, d26 = 1,
                                 d31 = 1, d32 = 1, d33 = 1, d34 = 1,
                                 d35 = 1, d36 = 1)} ],

        'Couplings:PyroElectricity' :
        [ {'px' : 0.1, 'py' : 0.2, 'pz' : 0.3, 'T0' : 0.4,
           'coefficient_type' : 'Constant strain' },
          {'px' : 0.2, 'py' : 0.1, 'pz' : 0.4, 'T0' : 0.5,
           'coefficient_type' : 'Constant stress'}]
        }


def run_tests():
    global parametrize_dict

    prop_set = [
        Property("Copy"),
        Property("Delete")
        ]

    mat_set = [
        MaterialBasic("New"),
        MaterialBasic("Delete"),
        MaterialBasic("Add_property"),
        MaterialBasic("Remove_property"),
        MaterialOps("Copy"),
        MaterialOps("Rename"),
        MaterialOps("Assign"),
        MaterialOps("Remove"),
        MaterialOps("Delete2")
        ]

    extra_set = [
        Property("Parametrize"),
        MatPropIO("PropSave"),
        MatPropIO("PropLoad"),
        MatPropIO("MatSave"),
        MatPropIO("MatLoad")
        ]

    test_set = prop_set + mat_set + extra_set
    #test_set = [MaterialOps('Delete2')]
    
    build_parametrize_dict()
    
    logan = unittest.TextTestRunner()
    for t in test_set:
        print >> sys.stderr,  "\n *** Running test: %s\n" % t.id()
        res = logan.run(t)
        if not res.wasSuccessful():
            return 0

    # Empty the dictionary locally, otherwise you get weird errors at
    # shut-down time.
    parametrize_dict={}
    
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
