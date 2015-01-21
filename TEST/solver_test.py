# -*- python -*-
# $RCSfile: solver_test.py,v $
# $Revision: 1.23 $
# $Author: langer $
# $Date: 2009/05/19 21:34:30 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

import unittest, os
import memorycheck

class OOF_Solver(unittest.TestCase):
    def setUp(self):
        global mesh, femesh, cskeleton, cmicrostructure
        from ooflib.engine import mesh
        from ooflib.SWIG.engine import femesh
        from ooflib.SWIG.engine import cskeleton
        from ooflib.SWIG.common import cmicrostructure
        OOF.File.Load.Data(filename=os.path.join("mesh_data", "solveable"))

    def tearDown(self):
        OOF.Property.Delete(property='Color:bloo')
        OOF.Property.Delete(property='Color:wred')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:soft')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:stiff')
        
    @memorycheck.check("solve_test")
    def Null(self):             # Establish baseline for memory leak tests
        pass

    @memorycheck.check("solve_test")
    def Solve(self):
        global solution
        make_solution()
        OOF.Subproblem.Set_Solver(
            subproblem='solve_test:skeleton:mesh:default',
            linearity=Linear(),
            solver=StaticDriver(matrixmethod=ConjugateGradient(
            preconditioner=ILUPreconditioner(),tolerance=1e-13,
            max_iterations=1000)))

        OOF.Mesh.Solve(mesh='solve_test:skeleton:mesh',
                       endtime=0.0, stepsize=0)


        # Then look for evidence that it worked.  Direct evidence
        # would be that the solution exists and is right, so poll
        # DOFs.
        from ooflib.engine import mesh
        msh_obj = mesh.meshes["solve_test:skeleton:mesh"].getObject()
        for fn in msh_obj.funcnode_iterator():
            delta = fn.displaced_position(msh_obj)-solution[fn.index()]
            self.assertAlmostEqual(delta**2, 0.0, 6)
        del msh_obj


# The expected solution, to some number of digits...
solution = {}

def make_solution():
    global solution
    from ooflib.common import primitives
    Point = primitives.Point
    solution = {
        0 : Point(0,0),
        1 : Point(15.3456,0),
        2 : Point(29.3792,0),
        3 : Point(44.4774,0),
        4 : Point(53.7066,0),
        5 : Point(79.1839,0),
        6 : Point(91.3082,0),
        7 : Point(103.883,0),
        8 : Point(120.872,0),
        9 : Point(133.066,0),
        10 : Point(150,0),
        11 : Point(1.02728,16.4524),
        12 : Point(15.6609,16.2508),
        13 : Point(30.4716,16.2151),
        14 : Point(43.6244,15.7484),
        15 : Point(60.3963,16.754),
        16 : Point(75.0237,17.5751),
        17 : Point(91.5844,14.1872),
        18 : Point(102.949,15.5236),
        19 : Point(120.474,16.6512),
        20 : Point(132.625,16.241),
        21 : Point(148.972,16.5332),
        22 : Point(1.52051,30.0604),
        23 : Point(16.2071,33.3001),
        24 : Point(30.8991,30.4828),
        25 : Point(45.6079,33.4832),
        26 : Point(60.7761,33.9675),
        27 : Point(74.0779,37.4084),
        28 : Point(83.8242,33.2106),
        29 : Point(104.411,30.1855),
        30 : Point(119.091,29.37),
        31 : Point(134.16,33.7042),
        32 : Point(148.34,30.0331),
        33 : Point(2.19445,50.2799),
        34 : Point(16.7242,50.7027),
        35 : Point(31.2362,51.7433),
        36 : Point(45.8163,51.7643),
        37 : Point(60.2318,51.9829),
        38 : Point(74.457,49.75),
        39 : Point(88.8261,50.7005),
        40 : Point(104.913,50.3512),
        41 : Point(118.196,49.2456),
        42 : Point(132.525,51.4415),
        43 : Point(147.79,53.4387),
        44 : Point(2.05798,67.5431),
        45 : Point(14.8366,67.3739),
        46 : Point(31.2821,65.9517),
        47 : Point(46.1495,65.8259),
        48 : Point(60.7822,69.0642),
        49 : Point(75.7266,66.6852),
        50 : Point(93.3626,65.9692),
        51 : Point(103.441,67.0739),
        52 : Point(118.719,69.3317),
        53 : Point(135.207,65.789),
        54 : Point(147.787,64.6342),
        55 : Point(1.99675,80.9863),
        56 : Point(16.7526,81.8107),
        57 : Point(29.1946,81.378),
        58 : Point(48.1439,82.7936),
        59 : Point(60.4777,82.3962),
        60 : Point(73.5941,82.7034),
        61 : Point(92.2705,81.7089),
        62 : Point(106.38,80.4622),
        63 : Point(119.175,81.4804),
        64 : Point(131.641,82.1859),
        65 : Point(147.781,85.4699),
        66 : Point(1.88776,95.9814),
        67 : Point(17.2527,96.4019),
        68 : Point(30.1717,99.5727),
        69 : Point(49.4866,99.4899),
        70 : Point(59.6651,97.3678),
        71 : Point(74.9832,98.6638),
        72 : Point(88.8785,98.9017),
        73 : Point(103.448,98.0985),
        74 : Point(119.347,96.7856),
        75 : Point(133.161,98.7585),
        76 : Point(147.765,96.1162),
        77 : Point(2.24623,117.006),
        78 : Point(17.6256,113.88),
        79 : Point(30.4922,111.41),
        80 : Point(46.5759,121.402),
        81 : Point(59.963,115.714),
        82 : Point(74.8293,121.31),
        83 : Point(89.4507,116.556),
        84 : Point(104.341,116.026),
        85 : Point(119.383,120.032),
        86 : Point(133.368,115.822),
        87 : Point(147.875,117.23),
        88 : Point(1.75494,134.545),
        89 : Point(16.3664,132.979),
        90 : Point(31.4934,134.875),
        91 : Point(44.9669,133.591),
        92 : Point(59.5566,133.689),
        93 : Point(75.214,132.016),
        94 : Point(90.0049,132.202),
        95 : Point(106.91,133.193),
        96 : Point(120.19,132.849),
        97 : Point(134.102,133.763),
        98 : Point(148.42,132.849),
        99 : Point(1.22331,147.769),
        100 : Point(12.4483,148.211),
        101 : Point(30.0218,148.003),
        102 : Point(43.8137,151.562),
        103 : Point(59.2445,145.003),
        104 : Point(74.5036,144.654),
        105 : Point(89.1165,148.237),
        106 : Point(105.194,148.662),
        107 : Point(121.625,148.048),
        108 : Point(134.024,148.261),
        109 : Point(148.959,148.564),
        110 : Point(0,165),
        111 : Point(10.9222,165),
        112 : Point(29.495,165),
        113 : Point(43.6219,165),
        114 : Point(59.5322,165),
        115 : Point(76.1102,165),
        116 : Point(94.2732,165),
        117 : Point(109.84,165),
        118 : Point(122.217,165),
        119 : Point(134.538,165),
        120 : Point(150,165),
        121 : Point(39.5967,0),
        122 : Point(45.9346,8.15438),
        123 : Point(38.3474,7.99599),
        124 : Point(47.778,0),
        125 : Point(56.8694,8.69266),
        126 : Point(53.3768,15.0907),
        127 : Point(50.1103,7.79032),
        128 : Point(64.762,0),
        129 : Point(75.5827,9.80986),
        130 : Point(70.2517,15.2455),
        131 : Point(67.4264,8.71299),
        132 : Point(81.2923,18.4121),
        133 : Point(83.3039,8.55795),
        134 : Point(112.459,0),
        135 : Point(111.804,15.879),
        136 : Point(142.019,0),
        137 : Point(141.709,16.397),
        138 : Point(15.6663,27.6216),
        139 : Point(10.4221,32.9438),
        140 : Point(10.031,25.5778),
        141 : Point(23.6054,33.6652),
        142 : Point(23.051,25.7457),
        143 : Point(45.0869,25.6473),
        144 : Point(38.5011,33.49),
        145 : Point(38.5876,24.2525),
        146 : Point(64.2572,24.7054),
        147 : Point(53.0029,34.6801),
        148 : Point(55.2326,25.1952),
        149 : Point(75.4335,24.5275),
        150 : Point(66.2885,34.6352),
        151 : Point(69.1308,28.7841),
        152 : Point(89.5627,25.2533),
        153 : Point(79.9291,33.9315),
        154 : Point(81.9201,29.9363),
        155 : Point(95.3881,31.6527),
        156 : Point(97.0168,23.9474),
        157 : Point(110.748,29.7889),
        158 : Point(133.722,24.5659),
        159 : Point(125.218,34.8498),
        160 : Point(127.521,23.6718),
        161 : Point(148.735,23.0719),
        162 : Point(142.579,30.0657),
        163 : Point(141.278,23.7942),
        164 : Point(16.4,40.2806),
        165 : Point(9.72393,49.4974),
        166 : Point(1.96095,39.5143),
        167 : Point(9.15347,39.2943),
        168 : Point(30.9716,41.3014),
        169 : Point(23.9819,51.7764),
        170 : Point(23.9692,40.2717),
        171 : Point(45.5963,41.3319),
        172 : Point(38.5148,51.7425),
        173 : Point(38.279,41.304),
        174 : Point(60.2841,42.568),
        175 : Point(52.87,52.1594),
        176 : Point(52.9197,41.3792),
        177 : Point(76.7987,42.5638),
        178 : Point(67.822,52.8658),
        179 : Point(67.6439,42.5751),
        180 : Point(90.0995,42.2706),
        181 : Point(83.1881,51.03),
        182 : Point(81.6933,42.1624),
        183 : Point(105.548,40.4896),
        184 : Point(96.5672,54.1836),
        185 : Point(99.654,43.1961),
        186 : Point(119.735,37.9323),
        187 : Point(111.327,50.7031),
        188 : Point(111.728,39.7193),
        189 : Point(133.919,44.9828),
        190 : Point(127.381,50.6295),
        191 : Point(126.159,46.2146),
        192 : Point(147.727,40.6607),
        193 : Point(140.023,49.9206),
        194 : Point(141.106,41.8387),
        195 : Point(16.133,57.9615),
        196 : Point(8.89851,57.7089),
        197 : Point(31.2716,57.786),
        198 : Point(24.9079,65.8988),
        199 : Point(23.9937,57.7987),
        200 : Point(45.4739,58.3905),
        201 : Point(38.571,65.9605),
        202 : Point(38.5526,57.785),
        203 : Point(60.2874,58.3558),
        204 : Point(52.4529,65.8977),
        205 : Point(53.0394,58.1728),
        206 : Point(74.5979,57.1723),
        207 : Point(68.5952,66.0119),
        208 : Point(67.1802,59.2531),
        209 : Point(92.8165,58.6084),
        210 : Point(83.8933,66.6782),
        211 : Point(85.3598,57.4013),
        212 : Point(103.588,58.1025),
        213 : Point(97.6893,64.9933),
        214 : Point(97.7566,59.7746),
        215 : Point(118.045,57.0093),
        216 : Point(110.804,66.86),
        217 : Point(112.468,58.1711),
        218 : Point(133.216,56.8574),
        219 : Point(125.867,66.0993),
        220 : Point(125.977,58.0998),
        221 : Point(140.523,57.7308),
        222 : Point(31.8145,73.85),
        223 : Point(23.9717,74.0992),
        224 : Point(45.8775,73.7822),
        225 : Point(39.1212,84.3652),
        226 : Point(38.7251,73.7068),
        227 : Point(52.477,74.6887),
        228 : Point(76.3496,73.6233),
        229 : Point(68.1102,74.5697),
        230 : Point(93.3797,74.2518),
        231 : Point(85.011,81.9347),
        232 : Point(83.4839,73.2173),
        233 : Point(103.685,73.2667),
        234 : Point(97.5085,81.7252),
        235 : Point(97.5307,75.4813),
        236 : Point(111.164,73.3295),
        237 : Point(135.236,73.3525),
        238 : Point(125.789,72.8491),
        239 : Point(147.783,74.674),
        240 : Point(8.20569,98.409),
        241 : Point(1.91709,91.1306),
        242 : Point(8.43269,88.5794),
        243 : Point(38.2234,97.2791),
        244 : Point(74.5727,91.8969),
        245 : Point(68.3574,100.918),
        246 : Point(67.8065,90.6077),
        247 : Point(88.6435,91.1772),
        248 : Point(84.9046,98.9998),
        249 : Point(84.8486,90.7584),
        250 : Point(102.459,90.1602),
        251 : Point(93.4556,99.0457),
        252 : Point(94.3286,90.5665),
        253 : Point(111.065,98.2107),
        254 : Point(111.873,89.9417),
        255 : Point(132.817,92.1574),
        256 : Point(125.989,99.1315),
        257 : Point(126.781,90.8571),
        258 : Point(140.017,98.8549),
        259 : Point(140.539,92.0804),
        260 : Point(15.0287,106.402),
        261 : Point(8.40523,114.296),
        262 : Point(2.3649,109.518),
        263 : Point(9.27901,102.027),
        264 : Point(22.6791,114.327),
        265 : Point(22.6228,107.201),
        266 : Point(39.5459,112.898),
        267 : Point(60.5346,107.478),
        268 : Point(53.3171,117.272),
        269 : Point(54.2262,104.831),
        270 : Point(74.7058,109.246),
        271 : Point(67.186,112.315),
        272 : Point(67.7973,105.509),
        273 : Point(90.9312,106.958),
        274 : Point(81.4102,117.514),
        275 : Point(84.3106,108.032),
        276 : Point(104.198,105.547),
        277 : Point(97.0138,116.075),
        278 : Point(96.2387,105.82),
        279 : Point(118.7,105.428),
        280 : Point(111.666,116.002),
        281 : Point(111.432,105.473),
        282 : Point(133.226,105.6),
        283 : Point(126.794,115.339),
        284 : Point(125.963,105.4),
        285 : Point(147.574,106.727),
        286 : Point(139.841,116.805),
        287 : Point(140.767,105.431),
        288 : Point(17.1803,124.891),
        289 : Point(9.93468,129.004),
        290 : Point(2.11943,123.035),
        291 : Point(10.9028,119.233),
        292 : Point(31.9623,122.805),
        293 : Point(22.589,131.043),
        294 : Point(24.9115,120.131),
        295 : Point(45.7518,126.407),
        296 : Point(36.8902,132.167),
        297 : Point(42.5213,123.989),
        298 : Point(61.1858,127.719),
        299 : Point(52.3798,134.339),
        300 : Point(53.5735,127.795),
        301 : Point(75.2042,126.876),
        302 : Point(66.7429,132.113),
        303 : Point(67.6962,124.291),
        304 : Point(90.0591,124.425),
        305 : Point(82.5053,132.496),
        306 : Point(81.7562,124.702),
        307 : Point(104.291,123.562),
        308 : Point(97.0838,132.372),
        309 : Point(97.6964,124.405),
        310 : Point(111.689,124.269),
        311 : Point(133.779,122.587),
        312 : Point(127.979,124.36),
        313 : Point(140.294,123.345),
        314 : Point(15.286,138.744),
        315 : Point(8.45871,139.741),
        316 : Point(31.9619,141.667),
        317 : Point(22.4461,156.63),
        318 : Point(22.1735,141.951),
        319 : Point(45.2828,140.095),
        320 : Point(38.5952,149.433),
        321 : Point(38.101,142.11),
        322 : Point(60.041,138.682),
        323 : Point(51.1775,152.985),
        324 : Point(52.5351,140.848),
        325 : Point(74.5153,139.482),
        326 : Point(67.2908,147.136),
        327 : Point(67.2998,138.69),
        328 : Point(89.9052,140.603),
        329 : Point(81.3357,146.637),
        330 : Point(82.5132,140.071),
        331 : Point(103.778,142.094),
        332 : Point(95.9196,150.642),
        333 : Point(97.1926,140.285),
        334 : Point(110.383,148.498),
        335 : Point(111.953,140.613),
        336 : Point(13.7456,158.646),
        337 : Point(7.71359,165),
        338 : Point(6.87261,157.146),
        339 : Point(33.9257,156.539),
        340 : Point(17.6892,165),
        341 : Point(22.379,156.692),
        342 : Point(44.8747,157.939),
        343 : Point(37.735,165),
        344 : Point(38.4635,156.332),
        345 : Point(59.9679,156.792),
        346 : Point(52.5661,165),
        347 : Point(52.426,159.325),
        348 : Point(74.7428,151.475),
        349 : Point(66.2683,165),
        350 : Point(67.8035,159.412),
        351 : Point(90.1436,156.794),
        352 : Point(85.7691,165),
        353 : Point(82.7241,154.369),
        354 : Point(104.195,155.532),
        355 : Point(102.857,165),
        356 : Point(97.4033,160.367),
        357 : Point(112.594,156.332)
        }


## OOF_Solver2 is a full blown test of a lot of features.  It creates
## a microstructure by selecting pixels and assigning a Material to
## *some* of them, so the microstructure isn't rectangular.  It then
## solves a simple elasticity problem with Dirichlet, Neumann, and
## Floating BCs all mixed together.

class OOF_Solver2(unittest.TestCase):
    @memorycheck.check("saved", "microstructure")
    def Solve(self):
        OOF.File.Load.Script(filename=os.path.join("mesh_data", "eltest.log"))
        OOF.File.Load.Data(filename=os.path.join("mesh_data", "eltest.mesh"))
        from ooflib.engine import mesh
        from ooflib.SWIG.engine import femesh
        from ooflib.SWIG.engine import cskeleton
        from ooflib.SWIG.common import cmicrostructure
        saved = mesh.meshes["saved:skeleton:mesh"]
        damned = mesh.meshes["microstructure:skeleton:mesh"]
        self.assertEqual(saved.compare(damned, 1.0e-13), 0)

        # Check that re-solving the mesh works. This line isn't in
        # eltest.log because exceptions raised in scripts don't seem
        # to make the tests fail.  TODO: Fix that.
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        self.assertEqual(saved.compare(damned, 1.0e-13), 0)

    def tearDown(self):
        OOF.Material.Delete(name='materialx')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:elastix')

## Similar to OOF_Solver2, but edits some boundary conditions and
## re-solves the system a few more times.
class OOF_Solver3(unittest.TestCase):
    @memorycheck.check("saved2", "microstructure")
    def Solve(self):
        OOF.File.Load.Script(filename=os.path.join("mesh_data", "eltest.log"))
        #Edit neumann and float boundary conditions and solve again (2x)
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<5>', mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(flux=Stress,
                                profile=[ConstantProfile(value=0.0),
                                         ConstantProfile(value=-0.040000000000000001)],
                                boundary='right',normal=True))
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<6>', mesh='microstructure:skeleton:mesh',
            condition=FloatBC(field=Displacement,field_component='x',
                              equation=Force_Balance,eqn_component='x',
                              profile=ContinuumProfile(
            function='-(y-0.16)**2'),boundary='right'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0,
                       stepsize=0)
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<5>', mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(flux=Stress,
                                profile=[ConstantProfile(value=0.0),
                                         ConstantProfile(value=-0.050000000000000001)],
                                boundary='right',normal=True))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0,
                       stepsize=0)
        OOF.File.Load.Data(filename=os.path.join("mesh_data", "eltest2.mesh"))
        from ooflib.engine import mesh
        saved = mesh.meshes["saved2:skeleton:mesh"]
        damned = mesh.meshes["microstructure:skeleton:mesh"]
        self.assertEqual(saved.compare(damned, 1.0e-13), 0)
    def tearDown(self):
        # Delete stuff added by script.
        OOF.Material.Delete(name='materialx')
        OOF.Property.Delete(
            property='Mechanical:Elasticity:Isotropic:elastix')

# OOF_Solver4 tests that an anisotropic property is rotated correctly
# by solving a thermal conductivity problem.  To regenerate the
# reference file for this test, change the first line
# mesh_data/anisotherm.log to "generate=True", load that file into
# oof2, and save the resulting mesh into mesh_data/anisotherm.mesh.

class OOF_Solver4(unittest.TestCase):
    @memorycheck.check("saved", "damned")
    def Solve(self):
        OOF.File.Load.Script(filename=os.path.join("mesh_data",
                                                   "anisotherm.log"))
        OOF.File.Load.Data(filename=os.path.join("mesh_data",
                                                 "anisotherm.mesh"))
        from ooflib.engine import mesh
        saved = mesh.meshes["saved:skeleton:mesh"]
        damned = mesh.meshes["damned:skeleton:mesh"]
        self.assertEqual(saved.compare(damned, 1.0e-13), 0)
    def tearDown(self):
        OOF.Material.Delete(name="materialx")
        OOF.Property.Delete(property='Orientation:unsure')
        OOF.Property.Delete(
            property='Thermal:Conductivity:Anisotropic:Monoclinic:mono')

# Check that solving a static problem after a nonstatic problem on the
# same mesh works correctly.

class OOF_Solver5(unittest.TestCase):
    @memorycheck.check("microstructure")
    def Solve(self):
        OOF.File.Load.Script(filename=os.path.join("mesh_data", "timenotime.log"))
        from ooflib.engine import mesh
        mesh0 = mesh.meshes["microstructure:skeleton:mesh"]
        mesh1 = mesh.meshes["microstructure:skeleton:mesh<2>"]
        self.assertEqual(mesh0.compare(mesh1, 1.0e-13), 0)
    def tearDown(self):
        OOF.Material.Delete(name='material')

# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.

def run_tests():

    from ooflib.SWIG.common import config
    if config.devel():
        print >> sys.stderr,  "Devel mode detected, solver testing skipped."
        return 0
    
    solver_set = [
        OOF_Solver("Null"),
        OOF_Solver("Solve"),
        OOF_Solver2("Solve"),
        OOF_Solver3("Solve"),
        OOF_Solver4("Solve"),
      #  OOF_Solver5("Solve")
        ]
    
    test_set = solver_set

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

    print "******************"
    print "Test OOF_Solver5 in solver_test.py has been skipped!!!"
    print "******************"
