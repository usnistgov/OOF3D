# -*- python -*-
# $RCSfile: output_test.py,v $
# $Revision: 1.1.2.20 $
# $Author: langer $
# $Date: 2014/09/28 17:31:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import unittest, os, sys, math
import memorycheck

from UTILS import file_utils
fp_file_compare = file_utils.fp_file_compare
reference_file = file_utils.reference_file
# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
file_utils.generate = False

# These tests should be run *before* solver_test so that outputs can
# be used to verify solutions.  That means that these tests should use
# meshes with artificial data.

## TODO 3.1: Add tests for managing linear and planar cross sections.

from ooflib.common import utils
meshTestDict = utils.OrderedDict() # OutputTests keyed by Mesh path
outputTestDict = utils.OrderedDict() # OutputTests keyed by Output path

class OutputTest(object):
    def __init__(self, mesh, operation, output, oparams, domain, sampling,
                 referencefile, time=0.0, tolerance=1.e-8, skip=False,
                 commands=[]):
        self.mesh = mesh        # just the Mesh part of the path
        self.operation = operation
        self.output = output    # path
        self.oparams = oparams  # dict
        self.domain = domain
        self.sampling = sampling
        self.referencefile = referencefile
        self.tolerance = tolerance
        self.time = time
        self.skip = skip        # for cutting down the list while debugging
        self.commands = commands # OOF commands to run before the test
        if not self.skip:
            outputTestDict.setdefault(output, []).append(self)
            meshTestDict.setdefault(mesh, []).append(self)
    def perform(self, test):
        if self.skip:
            return
        print >> sys.stderr, "Running", self.referencefile
        if self.commands:
            from ooflib.common import utils
            for cmd in self.commands:
                utils.OOFexec(cmd)
        menuitem = getattr(OOF.Mesh.Analyze, self.operation)
        menuitem.callWithDefaults(
            mesh='microstructure:skeleton:' + self.mesh,
            data=getOutput(self.output, **self.oparams),
            time=self.time,
            domain=self.domain,
            sampling=self.sampling,
            destination=OutputStream(filename='test.dat', mode='w'))
        ## TODO 3.1: The default params for fp_file_compare include
        ## "comment='#'", so comments in files aren't compared.  This
        ## is useful for log files, since they contain a comment with
        ## the OOF version number, which changes.  However, output
        ## files include meaningful comments that *should* be
        ## compared.  Adding "comment=None" to the args here would
        ## achieve that.  Doing so makes the tests fail because the
        ## output files have "show_x=True" and the reference files
        ## have "show_x=1".  Do the reference files need to be
        ## updated, or do some versions of Python write bools as 1,0
        ## instead of True,False?
        test.assert_(
            fp_file_compare('test.dat',
                            os.path.join('output_data', self.referencefile),
                            self.tolerance))
        file_utils.remove('test.dat')
        

# Test construction has to be done in a function because the OOF
# namespace isn't available when this module is loaded.

def buildTests():
    skip = False        # set to True to reduce test set for debugging
    entiremesh = EntireMesh()

    # OutputTests are stored in meshTestDict when they're built, so we
    # don't have to keep references to them here.  Just create them.

    # Tests are run in the order that they're created, except that all
    # tests for each input file are run together, so that the input
    # files don't have to be reloaded.

    # xtemp.dat is a 5x5x5 mesh on a 10x10x10 microstructure with T=x.
    # The simple form of T ensures that it's fit perfectly by the
    # finite element shape functions, so we know that the answers are
    # correct.  It contains 2 voxel groups (smallx and largex) and two
    # element groups derived from them.  The elements in largex are
    # selected.

    # First, test a bunch of Sampling methods with Direct_Output.
    OutputTest('xtemp', 
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               entiremesh, 
               GridSampleSet(x_points=6, y_points=6, z_points=6,
                             show_x=True, show_y=True, show_z=True),
               'xtemp_direct', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               entiremesh,
               GridSampleSet(x_points=4, y_points=3, z_points=2,
                             show_x=True, show_y=True, show_z=True),
               'xtemp_direct2', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               entiremesh,
               GridSampleSet(x_points=4, y_points=3, z_points=2,
                             show_x=False, show_y=True, show_z=True),
               'xtemp_direct3a', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               entiremesh,
               GridSampleSet(x_points=4, y_points=3, z_points=2,
                             show_x=True, show_y=False, show_z=False),
               'xtemp_direct3b', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               entiremesh,
               GridSampleSet(x_points=4, y_points=3, z_points=2,
                             show_x=True, show_y=True, show_z=False),
               'xtemp_direct3c', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               entiremesh,
               SpacedGridSampleSet(delta_x=3,delta_y=3,delta_z=3,
                                   show_x=True, show_y=True, show_z=True),
               'xtemp_direct_spaced', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               entiremesh,
               PixelSampleSet(show_voxel=True,show_x=False,
                              show_y=False,show_z=False),
               'xtemp_direct_voxel', skip=skip)
    
    # Now vary the Domain, still using Direct_Output.
    gridsample = GridSampleSet(x_points=4, y_points=4, z_points=4,
                               show_x=True, show_y=True, show_z=True)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               SinglePoint(point=Point(3,4,5)),
               PointSampleSet(show_x=True,show_y=True,show_z=True),
               'xtemp_direct_point', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               PixelGroup(group=every),
               gridsample,
               'xtemp_direct_every', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               PixelGroup(group='smallx'),
               gridsample,
               'xtemp_direct_smallx', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               PixelGroup(group='largex'),
               gridsample,
               'xtemp_direct_largex', skip=skip)

    # Voxel selection.  These tests use commands to select voxels
    # because the voxel selection isn't (yet) saved in the
    # microstructure data file.
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               PixelGroup(group=selection),
               gridsample,
               'xtemp_direct_voxsel',
               commands=[
                   "OOF.PixelSelection.Region(microstructure='microstructure', shape=BoxSelectionShape(point0=Point(0,0,0),point1=Point(5,5,5)), units=PhysicalUnits(),operator=Select())"
                   ],
               skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               PixelGroup(group=selection),
               gridsample,
               'xtemp_direct_voxsel2',
               commands=[
                   "OOF.PixelSelection.Region(microstructure='microstructure', shape=BoxSelectionShape(point0=Point(0,0,0),point1=Point(5,5,5)),units=PhysicalUnits(), operator=Select())",
                   "OOF.PixelSelection.Region(microstructure='microstructure', shape=BoxSelectionShape(point0=Point(1,1,1),point1=Point(4,4,4)),units=PhysicalUnits(), operator=Unselect())"
                   ],
               skip=skip)

    # Linear cross sections.
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               LinearCrossSectionDomain(cross_section='xyz'),
               LinearGridSampleSet(npts=11,show_distance=True,
                                   show_fraction=True,
                                   show_x=True,show_y=True,show_z=True),
               'xtemp_direct_linearcs_xyz', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               LinearCrossSectionDomain(cross_section='yz'),
               LinearGridSampleSet(npts=11,show_distance=True,
                                   show_fraction=True,
                                   show_x=True,show_y=True,show_z=True),
               'xtemp_direct_linearcs_yz', skip=skip)

    # There are no tests for FaceBoundary domains here, because direct
    # output isn't supported on them.

    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               SkeletonPointBoundaryDomain(boundary='XminYminZmin'),
               PointSampleSet(show_x=True,show_y=True,show_z=True),
               'xtemp_direct_point_0', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               SkeletonPointBoundaryDomain(boundary='XmaxYmaxZmax'),
               PointSampleSet(show_x=True,show_y=True,show_z=True),
               'xtemp_direct_point_1', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               SkeletonPointBoundaryDomain(boundary='XmaxYminZmax'),
               PointSampleSet(show_x=True,show_y=True,show_z=True),
               'xtemp_direct_point_2', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               ElementGroup(elements='smallx'),
               GridSampleSet(x_points=10,y_points=10,z_points=10,
                             show_x=True,show_y=True,show_z=True),
               'xtemp_direct_elgroup_smallx', skip=skip)
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               ElementGroup(elements='largex'),
               GridSampleSet(x_points=10,y_points=10,z_points=10,
                             show_x=True,show_y=True,show_z=True),
               'xtemp_direct_elgroup_largex', skip=skip)
    # xtemp_direct_elgroup_largex and xtemp_direct_elgroup_selection
    # should differ only in the comment specifying the domain, because
    # the selected elements and the largex group are identical.
    OutputTest('xtemp',
               'Direct_Output',
               'Field:Value', {'field':Temperature},
               ElementGroup(elements=selection),
               GridSampleSet(x_points=10,y_points=10,z_points=10,
                             show_x=True,show_y=True,show_z=True),
               'xtemp_direct_elgroup_selection', skip=skip)

    # Test non-direct output operations, still using xtemp.dat and
    # Field:Value.
    OutputTest('xtemp',
               'Range',
               'Field:Value', {'field':Temperature},
               entiremesh,
               StatGridSampleSet(x_points=10,y_points=10,z_points=10),
               'xtemp_range_grid', skip=skip)
    OutputTest('xtemp',
               'Range',
               'Field:Value', {'field':Temperature},
               ElementGroup(elements='largex'),
               StatGridSampleSet(x_points=10,y_points=10,z_points=10),
               'xtemp_range_largex', skip=skip)
    OutputTest('xtemp',
               'Range',
               'Field:Value', {'field':Temperature},
               ElementGroup(elements='smallx'),
               StatGridSampleSet(x_points=10,y_points=10,z_points=10),
               'xtemp_range_smallx', skip=skip)
    OutputTest('xtemp',
               'Range',
               'Field:Value', {'field':Temperature},
               ElementGroup(elements=selection),
               StatGridSampleSet(x_points=10,y_points=10,z_points=10),
               'xtemp_range_selection', skip=skip)
               
    # A bunch of non-direct-output tests for the Linear Cross Section
    # domain, which has to deal with a lot of special cases when the
    # cross section lies on or passes through nodes, edges, and faces.
    
    # Define a bunch of commands to set different linear cross sections.
    linearCSCommands = [
        # 0 Diagonal through the midplane of a plane of
        # elements. L=14.1421356237
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(5,0,0),end=Point(5,10,10)))"],
        # 1 Diagonal across a face of the microstructure. L=14.1421356237
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(0,0,0),end=Point(0,10,10)))"],
        # 2 Diagonal between two planes of elements. L=14.1421356237
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(6,0,0),end=Point(6,10,10)))"],
        # 3 Diagonal close to a face of the microstruture. L=14.1421356237
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(0.1,0,0),end=Point(0.1,10,10)))"],
        # 4 Not quite on the diagonal on a face. L=14.135066324570252
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(0,0,0),end=Point(0,10,9.99)))"],
        # 5 Not quite a diagonal and not quite on a face. L=14.135066324570252
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(0.1,0,0),end=Point(0.1,10,9.99)))"],
        # 6 Diagonal between a different two planes of elements. L=14.1421356237
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(4,0,0),end=Point(4,10,10)))"],
        # 7 Main diagonal in all three dimensions. L=17.320508075688775
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(0,0,0),end=Point(10,10,10)))"],
        # 8 Main diagonal in all three dimensions. L=17.320508075688775
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(10,0,0),end=Point(0,10,10)))"],
        # 9 Main diagonal in all three dimensions. L=17.320508075688775
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(10,10,0),end=Point(0,0,10)))"],
        # 10 A line that begins and ends within elements. L=9
        ["OOF.Mesh.Cross_Section.Edit(mesh='microstructure:skeleton:xtemp', name='yz', cross_section=StraightCrossSection(start=Point(0.5,0.5,0.5),end=Point(0.5,9.5,0.5)))"],
    ]

    # First, just integrate a constant to check that the full domain
    # is being included.
    for i, cmd in enumerate(linearCSCommands):
        OutputTest(mesh='xtemp',
                   operation='Integral',
                   output='XYZFunction:Scalar', oparams={'f':'1.0'},
                   domain=LinearCrossSectionDomain(cross_section='yz'),
                   sampling=ContinuumSampleSet(order=automatic),
                   commands=cmd,
                   referencefile='xtemp_length_linearcs'+`i`,
                   skip=skip) 

    # Now integrate a linear function (y).  The integral is the
    # average of y times the length of the cross section.
    for i, cmd in enumerate(linearCSCommands):
        OutputTest(mesh='xtemp',
                   operation='Integral',
                   output='XYZFunction:Scalar', oparams={'f':'y'},
                   domain=LinearCrossSectionDomain(cross_section='yz'),
                   sampling=ContinuumSampleSet(order=automatic),
                   commands=cmd,
                   referencefile='xtemp_linearfn_linearcs'+`i`,
                   skip=skip)
    
    ## Test integration over planar cross sections
    planarDomains = [
        # Planes perpendicular to the x axis.  A=100
        # 0
        PlanarCrossSectionDomain(normal=VectorDirection(x=1,y=0,z=0),
                                 offset=0, side='FRONT'),
        # 1
        PlanarCrossSectionDomain(normal=VectorDirection(x=1,y=0,z=0),
                                 offset=4.5, side='FRONT'),
        # 2
        PlanarCrossSectionDomain(normal=VectorDirection(x=1,y=0,z=0),
                                 offset=6, side='FRONT'),
        # 3
        PlanarCrossSectionDomain(normal=VectorDirection(x=1,y=0,z=0),
                                 offset=10, side='BACK'),
        # Planes perpendicular to the y axis.  A=100
        # 4
        PlanarCrossSectionDomain(normal=VectorDirection(x=0,y=1,z=0),
                                 offset=0, side='FRONT'),
        # 5
        PlanarCrossSectionDomain(normal=VectorDirection(x=0,y=1,z=0),
                                 offset=4.5, side='FRONT'),
        # 6
        PlanarCrossSectionDomain(normal=VectorDirection(x=0,y=1,z=0),
                                 offset=6, side='FRONT'),
        # 7
        PlanarCrossSectionDomain(normal=VectorDirection(x=0,y=1,z=0),
                                 offset=10, side='BACK'),

        # Planes at 45 degrees to two axes.
        # offset=5*sqrt(2)=7.0710678118654755 puts the plane through
        # opposite edges since the microstructure is 10x10x10.  Planes
        # with offset less than or equal to that have area
        # A=20*offset.  Planes with offsets greater than that have
        # area 20*(offset-5*sqrt(2)).
        # 8
        PlanarCrossSectionDomain(normal=VectorDirection(x=1,y=1,z=0),
                                 offset=0.1, side='FRONT'),
        # 9
        PlanarCrossSectionDomain(normal=VectorDirection(x=1,y=1,z=0),
                                 offset=5*math.sqrt(2.), side='FRONT'),
        # 10
        PlanarCrossSectionDomain(normal=VectorDirection(x=1,y=0,z=1),
                                 offset=0.1, side='FRONT'),
        # 11
        PlanarCrossSectionDomain(normal=VectorDirection(x=1,y=0,z=1),
                                 offset=5*math.sqrt(2.), side='FRONT'),
        # 12
        PlanarCrossSectionDomain(normal=VectorDirection(x=0,y=1,z=1),
                                 offset=0.1, side='FRONT'),
        # 13
        PlanarCrossSectionDomain(normal=VectorDirection(x=0,y=1,z=1),
                                 offset=5*math.sqrt(2.), side='FRONT'),
    ]

    for i, plane in enumerate(planarDomains):
        OutputTest(mesh='xtemp',
                   operation='Integral',
                   output='XYZFunction:Scalar', oparams={'f':'1.0'},
                   domain=plane,
                   sampling=ContinuumSampleSet(order=automatic),
                   referencefile='xtemp_area_planarcs'+`i`,
                   skip=skip)

    for i, plane in enumerate(planarDomains):
        OutputTest(mesh='xtemp',
                   operation='Average',
                   output='XYZFunction:Vector',
                   oparams={'fx':'1.0', 'fy':'x', 'fz':'x**2'},
                   domain=plane,
                   sampling=ContinuumSampleSet(order=2),
                   referencefile='xtemp_xavgs_planarcs'+`i`,
                   skip=skip)

    # Test Face Boundary domains (which weren't tested above during
    # the Direct_Output tests).
    faceBdyDomainNames = ['Xmax', 'Xmin', 'Ymax', 'Ymin', 'Zmax', 'Zmin']
    for domainname in faceBdyDomainNames:
        OutputTest(mesh='xtemp',
                   operation='Average_and_Deviation',
                   output='Field:Value', oparams={'field':Temperature},
                   domain=FaceBoundaryDomain(boundary=domainname, side='BACK'),
                   sampling=ContinuumSampleSet(order=2),
                   referencefile='xtemp_faceavg_' + domainname,
                   skip=skip)

    # Now test the other output quantities, using direct evaluation on
    # a 4x4x4 linear mesh.  The displacement field is initialized to
    # (x, y*y, z*z*z).  The output values are interpolated on linear
    # elements, so the y and z components are not exactly equal to the
    # nominal field values at intermediate points.

    # At the output points at y=1/3 and y=2/3, y**2 interpolates to
    # 0.125 and 0.4583333 respectively.  At z=1/3 and 2/3, z**3
    # interpolates to 0.0520833333 and 0.3229166666.

    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Value', 
               oparams={'field':Displacement},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_value',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Component', 
               oparams={'field':Displacement, 'component':'x'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_x',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Component', 
               oparams={'field':Displacement, 'component':'y'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_y',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Component', 
               oparams={'field':Displacement, 'component':'z'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_z',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Component',
               oparams={'field':Temperature, 'component':''},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_temp_component',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Derivative:Value',
               oparams={'field':Temperature, 'derivative':'x'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_temp_deriv_x',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Derivative:Value',
               oparams={'field':Temperature, 'derivative':'y'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_temp_deriv_y',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Derivative:Value',
               oparams={'field':Displacement, 'derivative':'y'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_deriv_y',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Derivative:Value',
               oparams={'field':Displacement, 'derivative':'z'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_deriv_z',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Derivative:Component',
               oparams={'field':Displacement, 'component':'x',
                        'derivative':'x'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_comp_x_deriv_x',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Derivative:Component',
               oparams={'field':Displacement, 'component':'x',
                        'derivative':'y'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_comp_x_deriv_y',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Derivative:Invariant',
               oparams={'field':Displacement, 'invariant':Magnitude(),
                        'derivative':'x'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_mag_deriv_x',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Derivative:Invariant',
               oparams={'field':Displacement, 'invariant':Magnitude(),
                        'derivative':'y'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_mag_deriv_y',
               skip=skip)
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Field:Invariant',
               oparams={'field':Displacement, 'invariant':Magnitude()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_disp_mag',
               skip=skip)

    # dispmesh2 initializes Displacement to 0.1*(y, z, x).  The
    # elastic modulus is the default isotropic one, so the diagonal
    # components of the stress are 0 and the offdiagonals are 1/40.
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Value',
               oparams={'flux':Stress},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_stress',
               skip=skip)
    # The thermal conductivity is the unit tensor and T=x, so heat
    # flux is -1 in the x direction.
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Value',
               oparams={'flux':Heat_Flux},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_heatflux',
               skip=skip)
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Component',
               oparams={'flux':Stress, 'component':'xx'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_stress_xx',
               skip=skip)
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Component',
               oparams={'flux':Stress, 'component':'xz'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_stress_xz',
               skip=skip)
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Component',
               oparams={'flux':Heat_Flux, 'component':'x'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_heatflux_x',
               skip=skip)
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Component',
               oparams={'flux':Heat_Flux, 'component':'z'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_heatflux_z',
               skip=skip)
    # Stress magnitude is sqrt(6)/40.
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Invariant',
               oparams={'flux':Stress, 'invariant':Magnitude()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_stress_mag',
               skip=skip)
    # Stress trace is 0.
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Invariant',
               oparams={'flux':Stress, 'invariant':MatrixTrace()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_stress_trace',
               skip=skip)
    # Stress determinant is 2/(40**3).
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Invariant',
               oparams={'flux':Stress, 'invariant':Determinant()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_stress_determinant',
               skip=skip)
    # Stress second invariant is -3/(40**2)
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Invariant',
               oparams={'flux':Stress, 'invariant':SecondInvariant()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_stress_2ndinv',
               skip=False)
    # Stress deviator is the same as the magnitude.
    OutputTest(mesh='dispmesh2',
               operation='Direct_Output',
               output='Flux:Invariant',
               oparams={'flux':Stress, 'invariant':Deviator()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_stress_deviator',
               skip=skip)

    # Flux normal, only evaluated on surfaces.
 
    # The normal component of the stress is (1/40, 1/40) parallel to
    # the surface.
    OutputTest(mesh='dispmesh2',
               operation='Average',
               output='Flux:Normal:Value',
               oparams={'flux':Stress},
               domain=FaceBoundaryDomain(boundary='Xmax', side='BACK'),
               sampling=ContinuumSampleSet(order=automatic),
               referencefile='dispmesh_stress_normal_xmax',
               skip=skip)
    OutputTest(mesh='dispmesh2',
               operation='Average',
               output='Flux:Normal:Value',
               oparams={'flux':Stress},
               domain=FaceBoundaryDomain(boundary='Xmin', side='BACK'),
               sampling=ContinuumSampleSet(order=automatic),
               referencefile='dispmesh_stress_normal_xmin',
               skip=skip)
    OutputTest(mesh='dispmesh2',
               operation='Average',
               output='Flux:Normal:Value',
               oparams={'flux':Heat_Flux},
               domain=FaceBoundaryDomain(boundary='Xmin', side='BACK'),
               sampling=ContinuumSampleSet(order=automatic),
               referencefile='dispmesh_heatflux_normal_xmin',
               skip=skip)
    OutputTest(mesh='dispmesh2',
               operation='Average',
               output='Flux:Normal:Value',
               oparams={'flux':Heat_Flux},
               domain=FaceBoundaryDomain(boundary='Xmax', side='BACK'),
               sampling=ContinuumSampleSet(order=automatic),
               referencefile='dispmesh_heatflux_normal_xmax',
               skip=skip)
    OutputTest(mesh='dispmesh2',
               operation='Average',
               output='Flux:Normal:Value',
               oparams={'flux':Heat_Flux},
               domain=FaceBoundaryDomain(boundary='Ymax', side='BACK'),
               sampling=ContinuumSampleSet(order=automatic),
               referencefile='dispmesh_heatflux_normal_ymax',
               skip=skip)
    # The magnitude of the normal component of the stress is sqrt(2)/40
    OutputTest(mesh='dispmesh2',
               operation='Average',
               output='Flux:Normal:Invariant',
               oparams={'flux':Stress, 'invariant':Magnitude()},
               domain=FaceBoundaryDomain(boundary='Zmax', side='BACK'),
               sampling=ContinuumSampleSet(order=automatic),
               referencefile='dispmesh_stress_normal_mag_zmax',
               skip=skip)

    # Strain tests
    OutputTest(mesh='dispmesh',
               operation='Direct_Output',
               output='Strain:Value',
               oparams={'type':GeometricStrain()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_geometric',
               skip=skip)
    # displacement in dispmesh3 is (0.1*(x+y+z), 0.2*(x+y+z), 0.3*(x+y+z))_
    OutputTest(mesh='dispmesh3',
               operation='Direct_Output',
               output='Strain:Value',
               oparams={'type':GeometricStrain()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_geometric2',
               skip=skip)
    OutputTest(mesh='dispmesh3',
               operation='Direct_Output',
               output='Strain:Component',
               oparams={'type':GeometricStrain(), 'component':'xx'},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_component',
               skip=skip)
    # Thermal strain should be zero.
    OutputTest(mesh='dispmesh3',
               operation='Direct_Output',
               output='Strain:Value',
               oparams={'type':ThermalStrain()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_thermal0',
               skip=skip)
    # dispmesh4 adds thermal expansion with T=x and alpha=0.01.
    # Measure geometric, thermal, and elastic strains.
    OutputTest(mesh='dispmesh4',
               operation='Direct_Output',
               output='Strain:Value',
               oparams={'type':ThermalStrain()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_thermal1',
               skip=skip)
    OutputTest(mesh='dispmesh4',
               operation='Direct_Output',
               output='Strain:Value',
               oparams={'type':GeometricStrain()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_geometric3',
               skip=skip)
    OutputTest(mesh='dispmesh4',
               operation='Direct_Output',
               output='Strain:Value',
               oparams={'type':ElasticStrain()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_elastic0',
               skip=skip)
    # Strain invariants
    OutputTest(mesh="dispmesh3",
               operation="Range",
               output="Strain:Invariant",
               oparams={'invariant':MatrixTrace(), 'type':GeometricStrain()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_trace',
               skip=skip)
    # The determinant for dispmesh3 is 0 but in a non-trivial way.
    OutputTest(mesh="dispmesh3",
               operation="Range",
               output="Strain:Invariant",
               oparams={'invariant':Determinant(), 'type':GeometricStrain()},
               domain=entiremesh,
               sampling=gridsample,
               referencefile='dispmesh_strain_determinant',
               skip=skip)

    # Energy

    # dispmesh5 has isotropic thermal conductivity with alpha=0.01,
    # T=1, and xx,yy, and zz geometric strain of 0.1.  Total energy
    # density is 0.0243
    OutputTest(mesh="dispmesh5",
               operation="Integral",
               output="Energy",
               oparams={'etype':'Total'},
               domain=entiremesh,
               sampling=ContinuumSampleSet(order=automatic),
               referencefile='dispmesh_energy0',
               skip=skip)
    # Set T=0 to check just the elastic energy, which should be 0.03.
    OutputTest(mesh="dispmesh5",
               operation="Integral",
               output="Energy",
               oparams={'etype':'Total'},
               domain=entiremesh,
               sampling=ContinuumSampleSet(order=automatic),
               commands=[
                   "OOF.Mesh.Set_Field_Initializer(mesh='microstructure:skeleton:dispmesh5', field=Temperature, initializer=ConstScalarFieldInit(value=0.0))",
                   "OOF.Mesh.Apply_Field_Initializers(mesh='microstructure:skeleton:dispmesh5')"],
               referencefile='dispmesh_energy1',
               skip=skip)
    # Set T=1 and turn off the geometric strain.  The energy is 0.0003.
    OutputTest(mesh="dispmesh5",
               operation="Integral",
               output="Energy",
               oparams={'etype':'Total'},
               domain=entiremesh,
               sampling=ContinuumSampleSet(order=automatic),
               commands=[
                   "OOF.Mesh.Set_Field_Initializer(mesh='microstructure:skeleton:dispmesh5', field=Temperature, initializer=ConstScalarFieldInit(value=1.0))",
                   "OOF.Mesh.Set_Field_Initializer(mesh='microstructure:skeleton:dispmesh5', field=Displacement, initializer=ConstThreeVectorFieldInit(cx=0.0,cy=0.0,cz=0.0))",
                   "OOF.Mesh.Apply_Field_Initializers(mesh='microstructure:skeleton:dispmesh5')"],
               referencefile='dispmesh_energy2',
               skip=skip)
    
    # Difference.  Just define two XYZ functions.
    OutputTest(mesh="dispmesh5",
               operation="Integral",
               output="Difference",
               oparams={
                   'minuend':getOutput('XYZFunction:Scalar',f='0.125'),
                   'subtrahend':getOutput('XYZFunction:Scalar',f='x*y*z')},
               domain=entiremesh,
               sampling=ContinuumSampleSet(order=automatic),
               referencefile="dispmesh_difference",
               skip=False)
    

class OOF_Output(unittest.TestCase):
    def setUp(self):
        global outputdestination
        from ooflib.engine.IO import outputdestination

    def tearDown(self):
        pass
    
    @memorycheck.check("microstructure")
    def PDFOutput(self):
        from ooflib.common.IO import gfxmanager
        # Load the output mesh, and draw a nice filled contour plot.
        OOF.File.Load.Data(filename=reference_file('output_data',
                                                 'position_mesh'))
        OOF.Windows.Graphics.New()
        OOF.LayerEditor.LayerSet.New(window='Graphics_1')
        OOF.LayerEditor.LayerSet.DisplayedObject(
            category='Mesh', object='microstructure:skeleton:mesh')
        OOF.LayerEditor.LayerSet.Add_Method(
            method=FilledContourDisplay(
            what=getOutput('Field:Component',
                           component='x',
                           field=Displacement),
            where=getOutput('original'),
            min=automatic, max=automatic, levels=11,
            nbins=5, colormap=ThermalMap()))
        OOF.LayerEditor.LayerSet.DisplayedObject(
            category='Microstructure', object='microstructure')
        OOF.LayerEditor.LayerSet.Add_Method(
            method=MicrostructureMaterialDisplay(
                no_material=Gray(value=0.0),
                no_color=RGBColor(red=0.0,green=0.0,blue=1.0)))
        OOF.LayerEditor.LayerSet.Send(window='Graphics_1')
        OOF.Graphics_1.File.Save_Image(filename="test.pdf",overwrite=True)

        # In Python 2.7 and above, the floating point numbers in the
        # comments in the pdf file have short reprs, (eg, 0.6 instead
        # of 0.59999999999999998).  That messes up the character
        # counts later in the file, so we have to use different
        # reference files for different floating point formats.  Check
        # float_repr_style instead of the Python version number
        # because not all platforms support the short reprs.
        try:
            shortform = sys.float_repr_style == 'short'
        except AttributeError:
            shortform = False
        if shortform:
            self.assert_(
                fp_file_compare(
                    'test.pdf', os.path.join('output_data','posmesh-short.pdf'),
                    1.0e-08, comment="%", pdfmode=True) )
        else:
            self.assert_(
                fp_file_compare(
                    'test.pdf', os.path.join('output_data','posmesh.pdf'),
                    1.0e-08, comment="%", pdfmode=True) )
        file_utils.remove('test.pdf')
            
        OOF.Graphics_1.File.Close()
        OOF.Material.Delete(name="material")
        

    def Outputs(self):
        buildTests()
        # Check that a test exists for each Output
        from ooflib.engine.IO import output
        outputTree = output.valueOutputs
        outputPaths = outputTree.leafpaths()
        outputNames = [':'.join(x) for x in outputPaths]
        for name in outputNames:
            if name not in outputTestDict:
                print >> sys.stderr, "*** No tests for", name, "! ***"
        # Run the tests for each mesh together, to avoid rebuilding
        # the meshes.
        for meshname, outputlist in meshTestDict.items():
            self.runTests(meshname, outputlist)

    @memorycheck.check("microstructure")
    def runTests(self, meshname, outputlist):
        # Load the mesh from meshname.dat.  The microstructure and
        # skeleton have to be named 'microstructure' and 'skeleton'
        OOF.File.Load.Data(filename=reference_file('output_data',
                                                   meshname + '.dat'))
        for test in outputlist:
            test.perform(self)
        OOF.Material.Delete_All()
        OOF.Property.Delete_All()
                
                
class OOF_BadMaterial(unittest.TestCase):
    @memorycheck.check("microstructure")
    def Analyze(self):
        from ooflib.SWIG.engine import ooferror2
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material',
            microstructure='microstructure',
            pixels=every)
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Anisotropic:Cubic')
        OOF.Material.Add_property(
            name='material', property='Orientation')
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
        # This shouldn't raise an exception
        OOF.Mesh.Analyze.Average(
            mesh='microstructure:skeleton:mesh', 
            time=latest,
            data=getOutput('Flux:Component',component='xx',flux=Stress),
            domain=EntireMesh(),
            sampling=ContinuumSampleSet(order=automatic),
            destination=MessageWindowStream())
        # Remove the Orientation property, so the Material is no
        # longer self-consistent.
        OOF.Material.Remove_property(
            name='material', 
            property='Orientation')
        self.assertRaises(
            ooferror2.ErrBadMaterial,
            OOF.Mesh.Analyze.Average,
            mesh='microstructure:skeleton:mesh',
            time=latest,
            data=getOutput('Flux:Component', component='xx',flux=Stress),
            domain=EntireMesh(),
            sampling=ContinuumSampleSet(order=automatic),
            destination=MessageWindowStream())
        # Re-add the Orientation.
        OOF.Material.Add_property(
            name='material', property='Orientation')
        OOF.Mesh.Analyze.Average(
            mesh='microstructure:skeleton:mesh', 
            time=latest,
            data=getOutput('Flux:Component',component='xx',flux=Stress),
            domain=EntireMesh(),
            sampling=ContinuumSampleSet(order=automatic),
            destination=MessageWindowStream())
    def tearDown(self):
        OOF.Material.Delete(name='material')


class OOF_NamedAnalysis(unittest.TestCase):
    def setUp(self):
        global namedanalysis
        from ooflib.engine import namedanalysis
        OOF.File.Load.Data(
            filename=reference_file("output_data", "xtemp.dat"))
    @memorycheck.check("microstructure")
    def CreateDelete(self):
        OOF.Named_Analysis.Create(
            name='output1', 
            operation=DirectOutput(),
            data=getOutput('Field:Value',field=Temperature),
            domain=EntireMesh(),
            sampling=GridSampleSet(
                x_points=3,y_points=3,z_points=3,
                show_x=True,show_y=True,show_z=True))
        self.assertEqual(namedanalysis.analysisNames(), ["output1"])
        OOF.Named_Analysis.Create(
            name='output2', 
            operation=AverageOutput(),
            data=getOutput('Field:Value',field=Temperature),
            domain=EntireMesh(),
            sampling=ContinuumSampleSet(order=automatic))
        self.assertEqual(namedanalysis.analysisNames(), ["output1", "output2"])
        OOF.Named_Analysis.Create(
            name='output2', 
            operation=AverageOutput(),
            data=getOutput('Field:Value',field=Temperature),
            domain=EntireMesh(),
            sampling=ContinuumSampleSet(order=automatic))
        self.assertEqual(namedanalysis.analysisNames(),
                         ["output1", "output2", "output2<2>"])
        OOF.Named_Analysis.Delete(
            name="output2<2>")
        self.assertEqual(namedanalysis.analysisNames(), ["output1", "output2"])
        # NamedAnalyses persist after the Microstructure is deleted,
        # so be sure to explicitly delete all NamedAnalyses at the end
        # of each test, to avoid interactions with subsequent tests.
        OOF.Named_Analysis.Delete(
            name="output2")
        OOF.Named_Analysis.Delete(
            name="output1")
        self.assertEqual(namedanalysis.analysisNames(), [])
    @memorycheck.check("microstructure")
    def Save(self):
        OOF.Named_Analysis.Create(
            name='output1', 
            operation=DirectOutput(),
            data=getOutput('Field:Value',field=Temperature),
            domain=EntireMesh(),
            sampling=GridSampleSet(
                x_points=3,y_points=3,z_points=3,
                show_x=True,show_y=True,show_z=True))
        OOF.Named_Analysis.Create(
            name='output2', 
            operation=AverageOutput(),
            data=getOutput('Field:Value',field=Temperature),
            domain=EntireMesh(),
            sampling=ContinuumSampleSet(order=automatic))
        OOF.Named_Analysis.SaveAnalysisDefs(
            filename='test.dat',
            mode='w',
            format='ascii', 
            names=['output1', 'output2'])
        self.assert_(
            fp_file_compare('test.dat',
                            os.path.join('output_data', 'analysisdefs.out'),
                            1.e-10))
        file_utils.remove('test.dat')
        # NamedAnalyses persist after the Microstructure is deleted,
        # so be sure to explicitly delete all NamedAnalyses at the end
        # of each test, to avoid interactions with subsequent tests.
        OOF.Named_Analysis.Delete(
            name="output2")
        OOF.Named_Analysis.Delete(
            name="output1")
    @memorycheck.check("microstructure")
    def Load(self):
        OOF.File.Load.Data(
            filename=reference_file("output_data", "analysisdefs.out"))
        self.assertEqual(namedanalysis.analysisNames(), ["output1", "output2"])
            
test_set = [
    OOF_Output("Outputs"),
    # OOF_Output("PDFOutput"), ## Skip until vtk PDF output is fixed
    OOF_BadMaterial("Analyze"),
    OOF_NamedAnalysis("CreateDelete"),
    OOF_NamedAnalysis("Save"),
    OOF_NamedAnalysis("Load"),
]
