# -*- python -*-
# $RCSfile: output_test.py,v $
# $Revision: 1.34 $
# $Author: langer $
# $Date: 2009/03/20 15:42:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

import unittest, os, string, sys
import memorycheck

import file_compare
fp_file_compare = file_compare.fp_file_compare
# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
file_compare.generate = False

class OOF_Output(unittest.TestCase):
    def setUp(self):
        global femesh, cskeleton
        from ooflib.SWIG.engine import femesh, cskeleton
        global cmicrostructure
        from ooflib.SWIG.common import cmicrostructure
        global allWorkers, allWorkerCores
        from ooflib.common.worker import allWorkers, allWorkerCores
        global outputdestination
        from ooflib.engine.IO import outputdestination

    def tearDown(self):
        pass
    
    @memorycheck.check("microstructure")
    def PDFOutput(self):
        from ooflib.common.IO import gfxmanager
        # Load the output mesh, and draw a nice filled contour plot.
        OOF.File.Load.Data(filename=os.path.join('output_data',
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
        # Hard-coded tolerance for this test.
        self.assert_( fp_file_compare(
            'test.pdf', os.path.join('output_data','posmesh.pdf'),
            1.0e-08, comment="%", pdfmode=True) )
        try:
            os.remove('test.pdf')
        except:
            if file_compare.generate:
                pass
            else:
                raise
            
        OOF.Graphics_1.File.Close()
        OOF.Material.Delete(name="material")
        
        
    @memorycheck.check("microstructure")
    def PositionOutputs(self):
        global position_output_args
        tolerance = 1.0e-08
        from ooflib.common import utils
        from ooflib.engine import mesh
        from ooflib.engine.IO import output
        from ooflib.SWIG.engine import mastercoord
        tree = output.positionOutputs
        outputpaths = tree.leafpaths()
        outputnames = [ string.join(x,':') for x in outputpaths ]
        OOF.File.Load.Data(filename=os.path.join('output_data',
                                                 'position_mesh'))
        meshobj = mesh.meshes['microstructure:skeleton:mesh'].getObject()
        for name in outputnames:
            try:
                (param_args, results) = position_output_args[name]
            except KeyError:
                print >> sys.stderr,  "No test data for PositionOutput %s." % name
            else:
                outputobj = tree[name].object
                paramhier = outputobj.listAllParametersHierarchically(
                    onlySettable=1)
                params = utils.flatten_all(paramhier)
                # Actually set the settable parameters.
                pdict = {}
                for p in params:
                    pdict[p.name]=param_args[p.name]
                #
                outputclone = outputobj.clone(params=pdict)

                # The "Analyze" menu item doesn't do PositionOutputs,
                # so we do these directly.  Evaluate each element at
                # mastercoord (0,0).

                elset = meshobj.element_iterator()
                reslist = []
                while not elset.end():
                    lmnt = elset.element()
                    reslist += outputclone.evaluate(
                        meshobj, [lmnt],
                        [[mastercoord.MasterCoord(0.0,0.0)]])
                    elset.next()
                for (r1,r2) in zip(reslist, results):
                    self.assert_( (r1-r2)**2 < tolerance )
        del meshobj
        OOF.Material.Delete(name='material')
                
                
    @memorycheck.check("thermms", "electroms")
    def outputs(self, treename, tree, args, tolerance):
        from ooflib.common import utils
        from ooflib.engine.IO import analyze

        outputpaths = tree.leafpaths()
        outputnames = [ string.join(x,':') for x in outputpaths ]

        OOF.File.Load.Data(filename=os.path.join('output_data',
                                                 'thermoelastic.mesh'))
        OOF.File.Load.Data(filename=os.path.join('output_data',
                                                 'electroelastic.mesh'))
        for name in outputnames:
            try:
                testlist = args[name]
            except KeyError:
                print >> sys.stderr, "No test data for %s %s." % (treename,
                                                                  name)
            else:
                outputobj = tree[name].object
                paramhier = outputobj.listAllParametersHierarchically(
                    onlySettable=1)
                output_params = utils.flatten_all(paramhier)

                print >> sys.stderr, \
                      "Running test for %s %s." % (treename, name)
                
                for test in testlist:
                    meshname = test[0]
                    test_argdict = test[1]
                    comp_file = test[2]

                    output_param_dict = {}
                    for p in output_params:
                        output_param_dict[p.name]=test_argdict[p.name]

                    outputclone = outputobj.clone(params=output_param_dict)
                    
                    OOF.Mesh.Analyze.Direct_Output(
                        data=outputclone,
                        mesh=meshname,
                        time=latest,
                        domain=EntireMesh(),
                        sampling=GridSampleSet(x_points=10, y_points=10,
                                                 show_x=True, show_y=True),
                        destination=OutputStream(filename='test.dat', mode='w'))

                    outputdestination.forgetTextOutputStreams()

                    # Compare test.dat with the right comparison file.
                    print >> sys.stderr,  "Comparing test.dat to", \
                          os.path.join('output_data', comp_file)
                    self.assert_(
                        fp_file_compare('test.dat',
                                        os.path.join('output_data', comp_file),
                                        tolerance ) )

                    try:
                        # File might not be there in "generate" mode.
                        os.remove('test.dat')
                    except:
                        if file_compare.generate:
                            pass
                        else:
                            raise

        OOF.Material.Delete(name='therm_left')
        OOF.Material.Delete(name='therm_centre')
        OOF.Material.Delete(name='therm_right')
        OOF.Material.Delete(name='electro_left')
        OOF.Material.Delete(name='electro_centre')
        OOF.Material.Delete(name='electro_right')

    def ScalarOutputs(self):
        global scalar_output_args
        tolerance = 1.0e-08
        from ooflib.engine.IO import output
        self.outputs("Scalar Outputs",
                     output.scalarOutputs,
                     scalar_output_args,
                     tolerance)

    def AggregateOutputs(self):
        global aggregate_output_args
        tolerance = 1.0e-08
        from ooflib.engine.IO import output
        self.outputs("Aggregate Outputs",
                     output.aggregateOutputs,
                     aggregate_output_args,
                     tolerance)
        

# Entries in the position_output_args dictionary are: Keys are the
# names of position outputs, and values a tuple consisting of a
# dictionary of parameter values for the output, and then a list of
# the expected results for this output applied to the standard
# 'position_mesh' at MasterCoord(0.0) in each element.

position_output_args = {}
def build_position_output_args():
    from ooflib.common import primitives
    Point = primitives.Point
    global position_output_args
    position_output_args = {
        'original':({},[Point(0.125,0.125),
                        Point(0.375,0.125),
                        Point(0.625,0.125),
                        Point(0.875,0.125),
                        Point(0.125,0.375),
                        Point(0.375,0.375),
                        Point(0.625,0.375),
                        Point(0.875,0.375),
                        Point(0.125,0.625),
                        Point(0.375,0.625),
                        Point(0.625,0.625),
                        Point(0.875,0.625),
                        Point(0.125,0.875),
                        Point(0.375,0.875),
                        Point(0.625,0.875),
                        Point(0.875,0.875)]),
        'actual':({},[Point(0.132547,0.136804),
                      Point(0.377216,0.135438),
                      Point(0.622784,0.135438),
                      Point(0.867453,0.136804),
                      Point(0.142188,0.411169),
                      Point(0.380488,0.408743),
                      Point(0.619512,0.408743),
                      Point(0.857812,0.411169),
                      Point(0.144706,0.686449),
                      Point(0.381683,0.684979),
                      Point(0.618317,0.684979),
                      Point(0.855294,0.686449),
                      Point(0.14515,0.962084), 
                      Point(0.38182,0.961674),
                      Point(0.61818,0.961674), 
                      Point(0.85485,0.962084)]),
        'enhanced':({'factor':2.0},[Point(0.140094,0.148609),
                                    Point(0.379431,0.145877),
                                    Point(0.620569,0.145877),
                                    Point(0.859906,0.148609),
                                    Point(0.159377,0.447338),
                                    Point(0.385976,0.442487),
                                    Point(0.614024,0.442487),
                                    Point(0.840623,0.447338),
                                    Point(0.164412,0.747898),
                                    Point(0.388366,0.744958),
                                    Point(0.611634,0.744958),
                                    Point(0.835588,0.747898),
                                    Point(0.1653,1.04917),
                                    Point(0.388641,1.04835),
                                    Point(0.611359,1.04835),
                                    Point(0.8347,1.04917)])
        }
    

# Values of this dictionary are a list of tuples.  Each tuple
# specifies a filename from which to load a mesh, a dictionary of
# parameters for the output, and a filename against which to compare
# the output.
scalar_output_args = {}
def build_scalar_output_args():
    global scalar_output_args
    scalar_output_args = {
        'Field:Component':[ ('thermms:thermskel:therm',
                             {'field':Displacement,'component':'x'},
                             'fcomp_displacement_x.dat'),

                            ('thermms:thermskel:therm',
                             {'field':Displacement,'component':'y'},
                             'fcomp_displacement_y.dat'),

                            ('thermms:thermskel:therm',
                             {'field':Temperature,'component':''},
                             'fcomp_temperature.dat'),

                            ('electroms:electroskel:electro',
                             {'field':Voltage,'component':''},
                             'fcomp_voltage.dat')
                            ],
        'Field:Invariant':[('thermms:thermskel:therm',
                            {'invariant':Magnitude(),'field':Displacement},
                            'finvar_displacement_mag.dat')],
        'Field:Derivative:Component':[('thermms:thermskel:therm',
                                       {'field':Displacement,
                                        'component':'x',
                                        'derivative':'x'},
                                       'fderivcomp_disp_xx.dat'),
                                      ('thermms:thermskel:therm',
                                       {'field':Displacement,
                                        'component':'x',
                                        'derivative':'y'},
                                       'fderivcomp_disp_xy.dat'),
                                      ('thermms:thermskel:therm',
                                       {'field':Displacement,
                                        'component':'y',
                                        'derivative':'x'},
                                       'fderivcomp_disp_yx.dat'),
                                      ('thermms:thermskel:therm',
                                       {'field':Displacement,
                                        'component':'y',
                                        'derivative':'y'},
                                       'fderivcomp_disp_yy.dat'),
                                      ('thermms:thermskel:therm',
                                       {'field':Temperature,
                                        'component':'',
                                        'derivative':'x'},
                                       'fderivcomp_temp_x.dat'),
                                      ('thermms:thermskel:therm',
                                       {'field':Temperature,
                                        'component':'',
                                        'derivative':'y'},
                                       'fderivcomp_temp_y.dat'),
                                      ('electroms:electroskel:electro',
                                       {'field':Voltage,
                                        'component':'',
                                        'derivative':'x'},
                                       'fderivcomp_voltage_x.dat'),
                                      ('electroms:electroskel:electro',
                                       {'field':Voltage,
                                        'component':'',
                                        'derivative':'y'},
                                       'fderivcomp_voltage_y.dat')
                                      ],
        'Field:Derivative:Invariant':[('thermms:thermskel:therm',
                                       {'field':Displacement,
                                        'derivative':'x',
                                        'invariant':Magnitude()},
                                       'fderiv_invar_x_mag.dat'),
                                      ('thermms:thermskel:therm',
                                       {'field':Displacement,
                                        'derivative':'y',
                                        'invariant':Magnitude()},
                                       'fderiv_invar_y_mag.dat')
                                      ],
        # Just do a few representative stress components -- the full
        # stress will be examined in detail in the aggregate output
        # tests.
        'Flux:Component':[('thermms:thermskel:therm',
                           {'flux':Stress,'component':'xx'},
                           'flux_comp_stress_xx.dat'),
                          ('thermms:thermskel:therm',
                           {'flux':Stress,'component':'xy'},
                           'flux_comp_stress_xy.dat'),
                          ('thermms:thermskel:therm',
                           {'flux':Stress,'component':'yy'},
                           'flux_comp_stress_yy.dat'),
                          ('thermms:thermskel:therm',
                           {'flux':Heat_Flux,'component':'x'},
                           'flux_comp_heat_x.dat'),
                          ('thermms:thermskel:therm',
                           {'flux':Heat_Flux,'component':'y'},
                           'flux_comp_heat_y.dat'),
                          ('thermms:thermskel:therm',
                           {'flux':Heat_Flux,'component':'z'},
                           'flux_comp_heat_z.dat'),
                          ('electroms:electroskel:electro',
                           {'flux':Total_Polarization,'component':'x'},
                           'flux_comp_polarization_x.dat'),
                          ('electroms:electroskel:electro',
                           {'flux':Total_Polarization,'component':'y'},
                           'flux_comp_polarization_y.dat'),
                          ('electroms:electroskel:electro',
                           {'flux':Total_Polarization,'component':'z'},
                           'flux_comp_polarization_z.dat')
                          ],
        'Flux:Invariant':[('thermms:thermskel:therm',
                           {'flux':Stress,
                            'invariant':MatrixTrace()},
                           'flux_invar_stress_trace.dat'),
                          ('thermms:thermskel:therm',
                           {'flux':Stress,
                            'invariant':Determinant()},
                           'flux_invar_stress_det.dat'),
                          ('thermms:thermskel:therm',
                           {'flux':Stress,
                            'invariant':SecondInvariant()},
                           'flux_invar_stress_2nd.dat'),
                          ('thermms:thermskel:therm',
                           {'flux':Heat_Flux,
                            'invariant':Magnitude()},
                           'flux_invar_heat_mag.dat'),
                          ('electroms:electroskel:electro',
                           {'flux':Total_Polarization,
                            'invariant':Magnitude()},
                           'flux_invar_polarization_mag.dat')
                          ],
        'XYFunction':[('thermms:thermskel:therm',
                       {'f':'x*y'},
                       'xyfunction.dat')],
        'Energy':[('thermms:thermskel:therm',
                   {'etype':'Total'},
                   'therm_e_total.dat'),
                  ('thermms:thermskel:therm',
                   {'etype':'Elastic'},
                   'therm_e_elastic.dat'),
                  ('electroms:electroskel:electro',
                   {'etype':'Total'},
                   'electro_e_total.dat'),
                  ('electroms:electroskel:electro',
                   {'etype':'Electric'},
                   'electro_e_electric.dat')
                  ],
        # Again, restricted to the few most relevant components --
        # full set will be covered in the aggregate output tests.
        'Strain:Component':[('thermms:thermskel:therm',
                             {'type':GeometricStrain(),'component':'xx'},
                             'strain_therm_geom_xx.dat'),
                            ('thermms:thermskel:therm',
                             {'type':GeometricStrain(),'component':'xy'},
                             'strain_therm_geom_xy.dat'),
                            ('thermms:thermskel:therm',
                             {'type':GeometricStrain(),'component':'yy'},
                             'strain_therm_geom_yy.dat'),
                            
                            ('thermms:thermskel:therm',
                             {'type':ElasticStrain(),'component':'xx'},
                             'strain_therm_elastic_xx.dat'),
                            ('thermms:thermskel:therm',
                             {'type':ElasticStrain(),'component':'xy'},
                             'strain_therm_elastic_xy.dat'),
                            ('thermms:thermskel:therm',
                             {'type':ElasticStrain(),'component':'yy'},
                             'strain_therm_elastic_yy.dat'),

                            
                            ('thermms:thermskel:therm',
                             {'type':ThermalStrain(),'component':'xx'},
                             'strain_therm_thermal_xx.dat'),
                            ('thermms:thermskel:therm',
                             {'type':ThermalStrain(),'component':'xy'},
                             'strain_therm_thermal_xy.dat'),
                            ('thermms:thermskel:therm',
                             {'type':ThermalStrain(),'component':'yy'},
                             'strain_therm_thermal_yy.dat'),

                            ('electroms:electroskel:electro',
                             {'type':GeometricStrain(),'component':'xx'},
                             'strain_electro_geom_xx.dat'),
                            ('electroms:electroskel:electro',
                             {'type':GeometricStrain(),'component':'xy'},
                             'strain_electro_geom_xy.dat'),
                            ('electroms:electroskel:electro',
                             {'type':GeometricStrain(),'component':'yy'},
                             'strain_electro_geom_yy.dat'),
                            
                            ('electroms:electroskel:electro',
                             {'type':ElasticStrain(),'component':'xx'},
                             'strain_electro_elastic_xx.dat'),
                            ('electroms:electroskel:electro',
                             {'type':ElasticStrain(),'component':'xy'},
                             'strain_electro_elastic_xy.dat'),
                            ('electroms:electroskel:electro',
                             {'type':ElasticStrain(),'component':'yy'},
                             'strain_electro_elastic_yy.dat'),
                            
                            ('electroms:electroskel:electro',
                             {'type':PiezoelectricStrain(),'component':'xx'},
                             'strain_electro_piezo_xx.dat'),
                            ('electroms:electroskel:electro',
                             {'type':PiezoelectricStrain(),'component':'xy'},
                             'strain_electro_piezo_xy.dat'),
                            ('electroms:electroskel:electro',
                             {'type':PiezoelectricStrain(),'component':'yy'},
                             'strain_electro_piezo_yy.dat')
                            ],
        'Strain:Invariant':[('thermms:thermskel:therm',
                             {'type':GeometricStrain(),
                              'invariant':MatrixTrace()},
                             'strain_therm_geom_trace.dat'),
                            
                            ('thermms:thermskel:therm',
                             {'type':GeometricStrain(),
                              'invariant':Determinant()},
                             'strain_therm_geom_det.dat'),

                            ('thermms:thermskel:therm',
                             {'type':GeometricStrain(),
                              'invariant':SecondInvariant()},
                             'strain_therm_geom_2nd.dat'),

                            ('thermms:thermskel:therm',
                             {'type':ElasticStrain(),
                              'invariant':MatrixTrace()},
                             'strain_therm_elastic_trace.dat'),

                            ('thermms:thermskel:therm',
                             {'type':ElasticStrain(),
                              'invariant':Determinant()},
                             'strain_therm_elastic_det.dat'),

                            ('thermms:thermskel:therm',
                             {'type':ElasticStrain(),
                              'invariant':SecondInvariant()},
                             'strain_therm_elastic_2nd.dat'),

                            ('thermms:thermskel:therm',
                             {'type':ThermalStrain(),
                              'invariant':MatrixTrace()},
                             'strain_therm_thermal_trace.dat'),

                            ('thermms:thermskel:therm',
                             {'type':ThermalStrain(),
                              'invariant':Determinant()},
                             'strain_therm_thermal_det.dat'),

                            ('thermms:thermskel:therm',
                             {'type':ThermalStrain(),
                              'invariant':SecondInvariant()},
                             'strain_therm_thermal_2nd.dat'),

                            ('electroms:electroskel:electro',
                             {'type':GeometricStrain(),
                              'invariant':MatrixTrace()},
                             'strain_electro_geom_trace.dat'),
                            
                            ('electroms:electroskel:electro',
                             {'type':GeometricStrain(),
                              'invariant':Determinant()},
                             'strain_electro_geom_det.dat'),

                            ('electroms:electroskel:electro',
                             {'type':GeometricStrain(),
                              'invariant':SecondInvariant()},
                             'strain_electro_geom_2nd.dat'),

                            ('electroms:electroskel:electro',
                             {'type':ElasticStrain(),
                              'invariant':MatrixTrace()},
                             'strain_electro_elastic_trace.dat'),

                            ('electroms:electroskel:electro',
                             {'type':ElasticStrain(),
                              'invariant':Determinant()},
                             'strain_electro_elastic_det.dat'),

                            ('electroms:electroskel:electro',
                             {'type':ElasticStrain(),
                              'invariant':SecondInvariant()},
                             'strain_electro_elastic_2nd.dat'),

                            ('electroms:electroskel:electro',
                             {'type':PiezoelectricStrain(),
                              'invariant':MatrixTrace()},
                             'strain_electro_piezo_trace.dat'),

                            ('electroms:electroskel:electro',
                             {'type':PiezoelectricStrain(),
                              'invariant':Determinant()},
                             'strain_electro_piezo_det.dat'),

                            ('electroms:electroskel:electro',
                             {'type':PiezoelectricStrain(),
                              'invariant':SecondInvariant()},
                             'strain_electro_piezo_2nd.dat')
                            ]
                            
        }


# Dictionary for aggregate output tests -- has the same structure as
# the scalar output dictionary.
aggregate_output_args = {}
def build_aggregate_output_args():
    global aggregate_output_args
    aggregate_output_args = {
        'Field:Value':[('thermms:thermskel:therm',
                        {'field':Displacement},
                        'field_displacement.dat'),
                       ('thermms:thermskel:therm',
                        {'field':Temperature},
                        'field_temp.dat'),
                       ('electroms:electroskel:electro',
                        {'field':Voltage},
                        'field_voltage.dat')
                       ],
        'Field:Derivative':[('thermms:thermskel:therm',
                             {'field':Displacement,
                              'derivative':'x'},
                             'field_displacement_dx.dat'),
                            ('thermms:thermskel:therm',
                             {'field':Displacement,
                              'derivative':'y'},
                             'field_displacement_dy.dat'),
                            ('thermms:thermskel:therm',
                             {'field':Temperature,
                              'derivative':'x'},
                             'field_temperature_dx.dat'),
                            ('thermms:thermskel:therm',
                             {'field':Temperature,
                              'derivative':'y'},
                             'field_temperature_dy.dat'),
                            ('electroms:electroskel:electro',
                             {'field':Voltage,
                              'derivative':'x'},
                             'field_voltage_dx.dat'),
                            ('electroms:electroskel:electro',
                             {'field':Voltage,
                              'derivative':'y'},
                             'field_voltage_dy.dat')
                            ],
        'Field:Invariant':[('thermms:thermskel:therm',
                            {'field':Displacement,
                             'invariant':Magnitude()},
                            'field_displacement_mag.dat'),
#                            ('thermms:thermskel:therm',
#                             {'field':Temperature,
#                              'invariant':None},
#                             'field_temperature_invar.dat'),
#                            ('electroms:electroskel:electro',
#                             {'field':Voltage,
#                              'invariant':Magnitude()},
#                             'field_voltage_invar.dat')
                           ],
        'Flux:Value':[('thermms:thermskel:therm',
                       {'flux':Stress},
                       'flux_therm_stress.dat'),
                      ('thermms:thermskel:therm',
                       {'flux':Heat_Flux},
                       'flux_therm_heatflux.dat'),
                      ('electroms:electroskel:electro',
                       {'flux':Stress},
                       'flux_electro_stress.dat'),
                      ('electroms:electroskel:electro',
                       {'flux':Heat_Flux},
                       'flux_electro_heatflux.dat')
                      ],
        'Energy':[('thermms:thermskel:therm',
                   {'etype':'Total'},
                   'agg_e_therm_total.dat'),
                  ('thermms:thermskel:therm',
                   {'etype':'Elastic'},
                   'agg_e_therm_elastic.dat'),
                  ('electroms:electroskel:electro',
                   {'etype':'Total'},
                   'agg_e_electro_total.dat'),
                  ('electroms:electroskel:electro',
                   {'etype':'Electric'},
                   'agg_e_electro_electric.dat')
                  ],
        'Strain:Value':[('thermms:thermskel:therm',
                         {'type':GeometricStrain()},
                         'agg_strain_therm_geometric.dat'),
                        ('thermms:thermskel:therm',
                         {'type':ElasticStrain()},
                         'agg_strain_therm_elastic.dat'),
                        ('thermms:thermskel:therm',
                         {'type':ThermalStrain()},
                         'agg_strain_therm_thermal.dat'),
                        ('electroms:electroskel:electro',
                         {'type':GeometricStrain()},
                         'agg_strain_electro_geometric.dat'),
                        ('electroms:electroskel:electro',
                         {'type':ElasticStrain()},
                         'agg_strain_electro_elastic.dat'),
                        ('electroms:electroskel:electro',
                         {'type':PiezoelectricStrain()},
                         'agg_strain_electro_piezo.dat')
                        ],
        # Invariant coverage is not complete, because the actual
        # outputs are the same objects as in the Scalar test -- just
        # make sure these outputs exist in the tree, and that
        # invocation as aggregates doesn't crash.
        'Strain:Invariant':[('thermms:thermskel:therm',
                             {'type':ElasticStrain(),
                              'invariant':MatrixTrace()},
                             'agg_strain_therm_elastic_trace.dat'),
                            
                            ('electroms:electroskel:electro',
                             {'type':PiezoelectricStrain(),
                              'invariant':MatrixTrace()},
                             'agg_strain_electro_piezo_trace.dat')
                            ]
        }



class OOF_PlaneFluxRHS(unittest.TestCase):
    def setUp(self):
        OOF.Microstructure.New(name='microstructure', width=1.0, height=1.0,
                               width_in_pixels=10, height_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        OOF.Material.New(name='material')
        OOF.Material.Add_property(name='material',
                                  property='Mechanical:Elasticity:Isotropic')
        OOF.Property.Parametrize.Mechanical.StressFreeStrain.Isotropic(
            epsilon0=0.10000000000000001)
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:StressFreeStrain:Isotropic')
        OOF.Material.Assign(material='material',
                            microstructure='microstructure', pixels=all)
        OOF.Mesh.New(name='mesh',
                     skeleton='microstructure:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Plane_Stress)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,
                                  field_component='x',
                                  equation=Force_Balance,
                                  eqn_component='x',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='bottomleft'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,
                                  field_component='y',
                                  equation=Force_Balance,
                                  eqn_component='y',
                                  profile=ConstantProfile(value=0.0),
            boundary='bottomleft'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,
                                  field_component='y',
                                  equation=Force_Balance,
                                  eqn_component='y',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='bottomright'))

        
    def tearDown(self):
        OOF.Material.Delete(name="material")

    # Solve the system and examine the resulting strain.  Sufficient
    # proof that it worked is if the strain in the system is within
    # roundoff of (0.1,0.1,0.1).
    @memorycheck.check("microstructure")
    def StrainCheck(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            linearity=Linear(),
            solver=StaticDriver(matrixmethod=ConjugateGradient(
            preconditioner=ILUPreconditioner(),tolerance=1e-13,
            max_iterations=1000)))

        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        OOF.Mesh.Analyze.Direct_Output(
            mesh='microstructure:skeleton:mesh',
            time=latest,
            data=getOutput('Strain:Value',
                           type=GeometricStrain()),
            domain=EntireMesh(),
            sampling=GridSampleSet(x_points=3,
                                   y_points=3,
                                   show_x=True,
                                   show_y=True),
            destination=OutputStream(filename='plane_stress_rhs.out', mode='w'))

        outputdestination.forgetTextOutputStreams()

        self.assert_(fp_file_compare(
            'plane_stress_rhs.out',
            os.path.join('output_data','plane_stress_ref.dat'),
            1.0e-08)
                     )
        try:
            os.remove('plane_stress_rhs.out')
        except:
            if file_compare.generate:
                pass
            else:
                raise

        

# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.

def run_tests():

    from ooflib.SWIG.common import config
    if config.devel():
        print >> sys.stderr,  "Devel mode detected, solver testing skipped."
        return 0
    
    output_set = [
        OOF_Output("PDFOutput"),
        OOF_Output("PositionOutputs"),
        OOF_Output("ScalarOutputs"),
        OOF_Output("AggregateOutputs")
        ]

    extra_set = [
        OOF_PlaneFluxRHS("StrainCheck")
        ]
    
    test_set = output_set+extra_set

    build_position_output_args()
    build_scalar_output_args()
    build_aggregate_output_args()

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
        os.remove("test.dat")
    except:
        pass
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
