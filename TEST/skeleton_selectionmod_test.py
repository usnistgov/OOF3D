# -*- python -*-
# $RCSfile: skeleton_selectionmod_test.py,v $
# $Revision: 1.8 $
# $Author: langer $
# $Date: 2008/09/08 18:30:07 $

# Test suite for skeleton selection and group commands, not including
# boundary commands, which are tested separately.  


# This file assumes that microstructures, images, and pixel group
# menu items have all been tested and work, and that the skeleton_basic
# tests also work.

import unittest, os
import memorycheck

aperiodic = dict(left_right_periodicity=False, top_bottom_periodicity=False)
xperiodic = dict(left_right_periodicity=True, top_bottom_periodicity=False)
yperiodic = dict(left_right_periodicity=False, top_bottom_periodicity=True)
xyperiodic = dict(left_right_periodicity=True, top_bottom_periodicity=True)

class TestBase(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        OOF.Microstructure.New(name='microstructure', width=1.0, height=1.0,
                               width_in_pixels=23, height_in_pixels=23)
        OOF.Material.New(name='material')
    def createSkel(self, periodicities):
        OOF.Skeleton.New(name='skeleton', microstructure='microstructure',
                         x_elements=10, y_elements=10,
                         skeleton_geometry=QuadSkeleton(**periodicities))
        OOF.Windows.Graphics.New()
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='microstructure:skeleton',
            points=[Point(0.0655642,0.647665)], shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='microstructure:skeleton',
            points=[Point(0.125486,0.647665)], shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='microstructure:skeleton',
            points=[Point(0.142607,0.553502)], shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='microstructure:skeleton',
            points=[Point(0.0398833,0.540661)], shift=1, ctrl=0)
        OOF.Skeleton.Modify(
            skeleton='microstructure:skeleton',
            modifier=Refine(targets=CheckSelectedElements(),
                            criterion=Unconditionally(),
                            degree=Bisection(rule_set='liberal'),alpha=0.3))
        OOF.PixelSelection.Select_Element_Pixels(
            microstructure='microstructure', skeleton='microstructure:skeleton')
        OOF.Material.Assign(material='material',
                            microstructure='microstructure', pixels=selection)
        OOF.PixelGroup.New(name='pixelgroup', microstructure='microstructure')
        OOF.PixelGroup.AddSelection(microstructure='microstructure',
                                    group='pixelgroup')
        OOF.PixelGroup.New(name='circle', microstructure='microstructure')

        OOF.LayerEditor.LayerSet.New(window='Graphics_1')
        OOF.LayerEditor.LayerSet.DisplayedObject(category='Microstructure',
                                                 object='microstructure')
        OOF.LayerEditor.LayerSet.Add_Method(
            method=MicrostructureMaterialDisplay(
            no_material=Gray(value=0.0),
            no_color=RGBColor(red=0.0,green=0.0,blue=1.0)))
        OOF.LayerEditor.LayerSet.Send(window='Graphics_1')
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source='microstructure', points=[Point(0.733268,0.258171),
                                             Point(0.857393,0.138327)],
            shift=0, ctrl=0)
        OOF.PixelGroup.AddSelection(microstructure='microstructure',
                                    group='circle')
        OOF.Material.New(name='material<2>')
        OOF.Material.Assign(material='material<2>',
                            microstructure='microstructure', pixels='circle')

        self.sk_context = skeletoncontext.skeletonContexts[
            "microstructure:skeleton"]
        self.e_selection = self.sk_context.elementselection
        self.s_selection = self.sk_context.segmentselection
        self.n_selection = self.sk_context.nodeselection
    def tearDown(self):
        OOF.Graphics_1.File.Close()
#         OOF.Microstructure.Delete(microstructure='microstructure')
        OOF.Material.Delete(name='material')
        OOF.Material.Delete(name='material<2>')

####################
        
class Element_Selection_Test(TestBase):
    @memorycheck.check("microstructure")
    def elementType(self, periodicities, **answers):
	self.createSkel(periodicities)
        OOF.ElementSelection.Clear(skeleton='microstructure:skeleton')
        self.assertEqual(self.e_selection.size(), 0)
        OOF.ElementSelection.Select_by_Element_Type(
            skeleton='microstructure:skeleton', shape='triangle')
        self.assertEqual(self.e_selection.size(), answers['triangle'])
        OOF.ElementSelection.Select_by_Element_Type(
            skeleton='microstructure:skeleton', shape='quad')
        self.assertEqual(self.e_selection.size(), answers['quad'])
    def ElementTypeA(self):
        self.elementType(aperiodic, triangle=18, quad=106)
    def ElementTypeX(self):
        self.elementType(xperiodic, triangle=24, quad=104)
    def ElementTypeY(self):
        self.elementType(yperiodic, triangle=18, quad=106)
    def ElementTypeXY(self):
        self.elementType(xyperiodic, triangle=24, quad=104)

    @memorycheck.check("microstructure")
    def material(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.ElementSelection.Select_by_Material(
            skeleton='microstructure:skeleton', material='<None>')
        self.assertEqual(self.e_selection.size(), answers['none'])
        OOF.ElementSelection.Select_by_Material(
            skeleton='microstructure:skeleton', material='<Any>')
        self.assertEqual(self.e_selection.size(), answers['any'])
        OOF.ElementSelection.Select_by_Material(
            skeleton='microstructure:skeleton', material='material')
        self.assertEqual(self.e_selection.size(), answers['material'])
    def MaterialA(self):
        self.material(aperiodic, none=95, any=29, material=20)
    def MaterialX(self):
        self.material(xperiodic, none=99, any=29, material=20)
    def MaterialY(self):
        self.material(yperiodic, none=95, any=29, material=20)
    def MaterialXY(self):
        self.material(xyperiodic, none=99, any=29, material=20)

    @memorycheck.check("microstructure")
    def homogeneity(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.ElementSelection.Select_by_Homogeneity(
            skeleton='microstructure:skeleton', threshold=0.9)
        self.assertEqual(self.e_selection.size(), answers['thresh09'])
        OOF.ElementSelection.Select_by_Homogeneity(
            skeleton='microstructure:skeleton', threshold=0.8)
        self.assertEqual(self.e_selection.size(), answers['thresh08'])
    def HomogeneityA(self):
        self.homogeneity(aperiodic, thresh09=23, thresh08=15)
    def HomogeneityY(self):
        self.homogeneity(yperiodic, thresh09=23, thresh08=15)
    def HomogeneityX(self):
        self.homogeneity(xperiodic, thresh09=23, thresh08=15)
    def HomogeneityXY(self):
        self.homogeneity(xyperiodic, thresh09=23, thresh08=15)

    @memorycheck.check("microstructure")
    def shapeEnergy(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode(
            origin=Point(0.8,0.2),
            destination=Point(0.78035,0.159728))
        OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode(
            origin=Point(1,0.2),
            destination=Point(0.994358,0.262451))
        OOF.ElementSelection.Select_by_Shape_Energy(
            skeleton='microstructure:skeleton', threshold=0.25)
        self.assertEqual(self.e_selection.size(), answers["thresh25"])
        OOF.ElementSelection.Select_by_Shape_Energy(
            skeleton='microstructure:skeleton', threshold=0.10)
        self.assertEqual(self.e_selection.size(), answers["thresh10"])
    def ShapeEnergyA(self):
        self.shapeEnergy(aperiodic, thresh25=14, thresh10=18)
    def ShapeEnergyY(self):
        self.shapeEnergy(yperiodic, thresh25=14, thresh10=18)        
    def ShapeEnergyX(self):
        self.shapeEnergy(xperiodic, thresh25=19, thresh10=24)
    def ShapeEnergyXY(self):
        self.shapeEnergy(xyperiodic, thresh25=19, thresh10=24)

    @memorycheck.check("microstructure")
    def illegal(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.ElementSelection.Select_Illegal_Elements(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.e_selection.size(), 0)
        OOF.Graphics_1.Toolbox.Move_Nodes.AllowIllegal(allowed=1)
        OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode(
            origin=Point(0,0.2),
            destination=Point(0.00136187,0.0570039))
        OOF.ElementSelection.Select_Illegal_Elements(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.e_selection.size(), answers["nill"])
    def IllegalA(self):
        self.illegal(aperiodic, nill=1)
    def IllegalX(self):
        self.illegal(xperiodic, nill=2)
    def IllegalY(self):
        self.illegal(yperiodic, nill=1)
    def IllegalXY(self):
        self.illegal(xyperiodic, nill=2)

    @memorycheck.check("microstructure")
    def expand(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.ElementSelection.Expand_Element_Selection(
            skeleton='microstructure:skeleton', ignorePBC=False)
        self.assertEqual(self.e_selection.size(), answers["withPBC"])
        OOF.ElementSelection.Undo(skeleton='microstructure:skeleton')
        OOF.ElementSelection.Expand_Element_Selection(
            skeleton='microstructure:skeleton', ignorePBC=True)
        self.assertEqual(self.e_selection.size(), answers["withoutPBC"])
    def ExpandA(self):
        self.expand(aperiodic, withPBC=36, withoutPBC=36)
    def ExpandY(self):
        self.expand(yperiodic, withPBC=36, withoutPBC=36)
    def ExpandX(self):
        self.expand(xperiodic, withPBC=44, withoutPBC=36)
    def ExpandXY(self):
        self.expand(xyperiodic, withPBC=44, withoutPBC=36)

    @memorycheck.check("microstructure")
    def SelectGroup(self):
        self.createSkel(xperiodic)
        # Create some element groups.
        OOF.ElementGroup.New_Group(skeleton='microstructure:skeleton',
                                   name='elementgroup')
        OOF.ElementGroup.Add_to_Group(skeleton='microstructure:skeleton',
                                      group='elementgroup')
        OOF.ElementSelection.Select_by_Material(
            skeleton='microstructure:skeleton', material='material<2>')
        OOF.ElementGroup.New_Group(
            skeleton='microstructure:skeleton', name='matgroup')
        OOF.ElementGroup.Add_to_Group(skeleton='microstructure:skeleton',
                                      group='matgroup')
        OOF.ElementSelection.Clear(skeleton='microstructure:skeleton')
        # Check that selecting a group selects *only* the elements in
        # the group...
        OOF.ElementSelection.Select_Group(skeleton='microstructure:skeleton',
                                          group='elementgroup')
        self.assertEqual(self.e_selection.size(), 16)
        # ... so don't clear the selection before selecting the second group.
        OOF.ElementSelection.Select_Group(skeleton='microstructure:skeleton',
                                          group='matgroup')
        self.assertEqual(self.e_selection.size(), 9)

        # Select all elements before testing Unselect.
        OOF.ElementSelection.Clear(skeleton='microstructure:skeleton')
        OOF.ElementSelection.Invert(skeleton='microstructure:skeleton')
        self.assertEqual(self.e_selection.size(), 128)

        OOF.ElementSelection.Unselect_Group(skeleton='microstructure:skeleton',
                                            group='elementgroup')
        self.assertEqual(self.e_selection.size(), 112)
        OOF.ElementSelection.Unselect_Group(skeleton='microstructure:skeleton',
                                            group='matgroup')
        self.assertEqual(self.e_selection.size(), 103)

        # Check that Add_Group doesn't deselect already selected elements.
        OOF.ElementSelection.Clear(skeleton='microstructure:skeleton')
        OOF.ElementSelection.Add_Group(skeleton='microstructure:skeleton',
                                       group='elementgroup')
        self.assertEqual(self.e_selection.size(), 16)
        OOF.ElementSelection.Add_Group(skeleton='microstructure:skeleton',
                                       group='matgroup')
        self.assertEqual(self.e_selection.size(), 25)

        # Select some other elements to test intersections
        OOF.ElementSelection.Select_by_Homogeneity(
            skeleton='microstructure:skeleton', threshold=0.9)
        self.assertEqual(self.e_selection.size(), 23)
        OOF.ElementSelection.Intersect_Group(skeleton='microstructure:skeleton',
                                             group='elementgroup')
        self.assertEqual(self.e_selection.size(), 0)
        OOF.ElementSelection.Undo(skeleton='microstructure:skeleton')
        OOF.ElementSelection.Intersect_Group(skeleton='microstructure:skeleton',
                                             group='matgroup')
        self.assertEqual(self.e_selection.size(), 3)

        # Test that selecting by pixelgroup doesn't leave previously
        # selected elelments selected.
        OOF.ElementSelection.Select_by_Pixel_Group(
            skeleton='microstructure:skeleton', group='pixelgroup')
        self.assertEqual(self.e_selection.size(), 20)
        OOF.ElementSelection.Select_by_Pixel_Group(
            skeleton='microstructure:skeleton', group='circle')
        self.assertEqual(self.e_selection.size(), 9)

####################

class Node_Selection_Test(TestBase):
    @memorycheck.check("microstructure")
    def internal(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.NodeSelection.Select_Internal_Boundaries(
            skeleton='microstructure:skeleton', ignorePBC=False)
        self.assertEqual(self.n_selection.size(), answers['withPBC'])
        OOF.NodeSelection.Select_Internal_Boundaries(
            skeleton='microstructure:skeleton', ignorePBC=True)
        self.assertEqual(self.n_selection.size(), answers['withoutPBC'])
    def InternalA(self):
        self.internal(aperiodic,withPBC=26, withoutPBC=26)
    def InternalX(self):
        self.internal(xperiodic, withPBC=36, withoutPBC=26)
    def InternalY(self):
        self.internal(yperiodic, withPBC=26, withoutPBC=26)
    def InternalXY(self):
        self.internal(xyperiodic, withPBC=36, withoutPBC=26)

    @memorycheck.check("microstructure")
    def expand(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.Graphics_1.Toolbox.Select_Node.Circle(
            skeleton='microstructure:skeleton',
            points=[Point(0.76751,0.258171), Point(1.07568,0.0655642)],
            shift=0, ctrl=0)
        self.assertEqual(self.n_selection.size(), 37)
        OOF.NodeSelection.Expand_Node_Selection(
            skeleton='microstructure:skeleton',
            criterion=ExpandByElements(), ignorePBC=False)
        self.assertEqual(self.n_selection.size(), answers["e_PBC"])
        OOF.NodeSelection.Undo(skeleton='microstructure:skeleton')
        self.assertEqual(self.n_selection.size(), 37)
        OOF.NodeSelection.Expand_Node_Selection(
            skeleton='microstructure:skeleton',
            criterion=ExpandByElements(), ignorePBC=True)
        self.assertEqual(self.n_selection.size(), answers["e_noPBC"])
        OOF.NodeSelection.Undo(skeleton='microstructure:skeleton')
        OOF.NodeSelection.Expand_Node_Selection(
            skeleton='microstructure:skeleton',
            criterion=ExpandBySegments(), ignorePBC=False)
        self.assertEqual(self.n_selection.size(), answers["s_PBC"])
        OOF.NodeSelection.Undo(skeleton='microstructure:skeleton')
        OOF.NodeSelection.Expand_Node_Selection(
            skeleton='microstructure:skeleton',
            criterion=ExpandBySegments(), ignorePBC=True)
        self.assertEqual(self.n_selection.size(), answers["s_noPBC"])
    def ExpandA(self):
        self.expand(aperiodic, e_PBC=53, e_noPBC=53, s_PBC=49, s_noPBC=49)
    def ExpandX(self):
        self.expand(xperiodic, e_PBC=67, e_noPBC=53, s_PBC=62, s_noPBC=49)
    def ExpandY(self):
        self.expand(yperiodic, e_PBC=65, e_noPBC=53, s_PBC=60, s_noPBC=49)
    def ExpandXY(self):
        self.expand(xyperiodic, e_PBC=83, e_noPBC=53, s_PBC=75, s_noPBC=49)

    @memorycheck.check("microstructure")
    def SelectGroup(self):
        # Create some groups
        self.createSkel(aperiodic)
        OOF.Graphics_1.Toolbox.Select_Node.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(-0.0157588,1.01576), Point(0.557782,0.472179)],
            shift=0, ctrl=0)
        OOF.NodeGroup.New_Group(skeleton='microstructure:skeleton',
                                name='upleft')
        OOF.NodeGroup.Add_to_Group(skeleton='microstructure:skeleton',
                                   group='upleft')
        OOF.Graphics_1.Toolbox.Select_Node.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(0.258171,0.741829), Point(0.660506,0.343774)],
            shift=0, ctrl=0)
        OOF.NodeGroup.New_Group(skeleton='microstructure:skeleton', name='mid')
        OOF.NodeGroup.Add_to_Group(skeleton='microstructure:skeleton',
                                   group='mid')

        OOF.NodeSelection.Clear(skeleton='microstructure:skeleton')
        self.assertEqual(self.n_selection.size(), 0)
        OOF.NodeSelection.Select_Group(skeleton='microstructure:skeleton',
                                       group='upleft')
        self.assertEqual(self.n_selection.size(), 52)
        OOF.NodeSelection.Select_Group(skeleton='microstructure:skeleton',
                                       group='mid')
        self.assertEqual(self.n_selection.size(), 16)
        OOF.NodeSelection.Unselect_Group(skeleton='microstructure:skeleton',
                                         group='upleft')
        self.assertEqual(self.n_selection.size(), 7)
        OOF.NodeSelection.Unselect_Group(skeleton='microstructure:skeleton',
                                         group='mid')
        self.assertEqual(self.n_selection.size(), 0)
        OOF.NodeSelection.Add_Group(skeleton='microstructure:skeleton',
                                    group='upleft')
        self.assertEqual(self.n_selection.size(), 52)
        OOF.NodeSelection.Add_Group(skeleton='microstructure:skeleton',
                                    group='mid')
        self.assertEqual(self.n_selection.size(), 59)

        OOF.NodeSelection.Clear(skeleton='microstructure:skeleton')
        OOF.NodeSelection.Select_Group(skeleton='microstructure:skeleton',
                                       group='upleft')
        OOF.NodeSelection.Intersect_Group(skeleton='microstructure:skeleton',
                                          group='mid')
        self.assertEqual(self.n_selection.size(), 9)

    @memorycheck.check("microstructure")
    def selectBoundary(self, periodicities):
        self.createSkel(periodicities)
        OOF.NodeSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='topleft')
        self.assertEqual(self.n_selection.size(), 1)
        OOF.NodeSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='bottomleft')
        self.assertEqual(self.n_selection.size(), 1)
        OOF.NodeSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='bottomright')
        self.assertEqual(self.n_selection.size(), 1)
        OOF.NodeSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='topright')
        self.assertEqual(self.n_selection.size(), 1)
    def BoundaryA(self):
        self.selectBoundary(aperiodic)
    def BoundaryXY(self):
        self.selectBoundary(xyperiodic)
    def BoundaryX(self):
        self.selectBoundary(xperiodic)
    def BoundaryY(self):
        self.selectBoundary(yperiodic)

    @memorycheck.check("microstructure")
    def periodicPartners(self, periodicities, **answers):
        self.createSkel(periodicities)
        # Select a corner
        OOF.NodeSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='topleft')
        OOF.NodeSelection.Select_Periodic_Partners(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.n_selection.size(), answers["corner"])
        # Select some nodes in the middle
        OOF.Graphics_1.Toolbox.Select_Node.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(0.279572,0.724708), Point(0.664786,0.348054)],
            shift=0, ctrl=0)
        self.assertEqual(self.n_selection.size(), 16)
        OOF.NodeSelection.Select_Periodic_Partners(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.n_selection.size(), 16)
        # Select an edge
        OOF.Graphics_1.Toolbox.Select_Node.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(-0.0457198,1.03288), Point(1.03288,0.960117)],
            shift=0, ctrl=0)
        self.assertEqual(self.n_selection.size(), 11)
        OOF.NodeSelection.Select_Periodic_Partners(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.n_selection.size(), answers["edge"])
    def PeriodicPartnersA(self):
        self.periodicPartners(aperiodic, corner=1, edge=11)
    def PeriodicPartnersX(self):
        self.periodicPartners(xperiodic, corner=2, edge=11)
    def PeriodicPartnersY(self):
        self.periodicPartners(yperiodic, corner=2, edge=22)
    def PeriodicPartnersXY(self):
        self.periodicPartners(xyperiodic, corner=4, edge=22)


class Segment_Selection_Test(TestBase):
    @memorycheck.check("microstructure")
    def internal(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.SegmentSelection.Select_Internal_Boundary_Segments(
            skeleton='microstructure:skeleton', ignorePBC=False)
        self.assertEqual(self.s_selection.size(), answers["withPBC"])
        OOF.SegmentSelection.Select_Internal_Boundary_Segments(
            skeleton='microstructure:skeleton', ignorePBC=True)
        self.assertEqual(self.s_selection.size(), answers["withoutPBC"])
    def InternalA(self):
        self.internal(aperiodic, withPBC=25, withoutPBC=25)
    def InternalX(self):
        self.internal(xperiodic, withPBC=35, withoutPBC=25)
    def InternalY(self):
        self.internal(yperiodic, withPBC=25, withoutPBC=25)
    def InternalXY(self):
        self.internal(xyperiodic, withPBC=35, withoutPBC=25)

    @memorycheck.check("microstructure")
    def homogeneity(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.SegmentSelection.Select_by_Homogeneity(
            skeleton='microstructure:skeleton', threshold=0.9)
        self.assertEqual(self.s_selection.size(), answers["thresh09"])
        OOF.SegmentSelection.Select_by_Homogeneity(
            skeleton='microstructure:skeleton', threshold=0.7)
        self.assertEqual(self.s_selection.size(), answers["thresh07"])
    def HomogeneityA(self):
        self.homogeneity(aperiodic, thresh09=37, thresh07=15)
    def HomogeneityX(self):
        self.homogeneity(xperiodic, thresh09=37, thresh07=15)

    @memorycheck.check("microstructure")
    def SelectGroup(self):
        self.createSkel(xperiodic)
        # Create some groups
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(-0.00719844,1.02004), Point(0.416537,0.587743)],
            shift=0, ctrl=0)
        OOF.SegmentGroup.New_Group(skeleton='microstructure:skeleton',
                                   name='topleft')
        OOF.SegmentGroup.Add_to_Group(skeleton='microstructure:skeleton',
                                      group='topleft')
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(0.172568,0.827432), Point(0.724708,0.283852)],
            shift=0, ctrl=0)
        OOF.SegmentGroup.New_Group(skeleton='microstructure:skeleton',
                                   name='middle')
        OOF.SegmentGroup.Add_to_Group(skeleton='microstructure:skeleton',
                                      group='middle')
        
        OOF.SegmentSelection.Clear(skeleton='microstructure:skeleton')
        self.assertEqual(self.s_selection.size(), 0)
        
        OOF.SegmentSelection.Select_Group(skeleton='microstructure:skeleton',
                                          group='topleft')
        self.assertEqual(self.s_selection.size(), 61)
        OOF.SegmentSelection.Select_Group(skeleton='microstructure:skeleton',
                                          group='middle')
        self.assertEqual(self.s_selection.size(), 66)

        OOF.SegmentSelection.Unselect_Group(skeleton='microstructure:skeleton',
                                            group='topleft')
        self.assertEqual(self.s_selection.size(), 51)
        OOF.SegmentSelection.Unselect_Group(skeleton='microstructure:skeleton',
                                            group='middle')
        self.assertEqual(self.s_selection.size(), 0)

        OOF.SegmentSelection.Add_Group(skeleton='microstructure:skeleton',
                                       group='middle')
        self.assertEqual(self.s_selection.size(), 66)
        OOF.SegmentSelection.Add_Group(skeleton='microstructure:skeleton',
                                       group='topleft')
        self.assertEqual(self.s_selection.size(), 112)
        
        OOF.SegmentSelection.Intersect_Group(skeleton='microstructure:skeleton',
                                             group='topleft')
        self.assertEqual(self.s_selection.size(), 61)
        OOF.SegmentSelection.Intersect_Group(skeleton='microstructure:skeleton',
                                             group='middle')
        self.assertEqual(self.s_selection.size(), 15)

        OOF.SegmentSelection.Invert(skeleton='microstructure:skeleton')
        self.assertEqual(self.s_selection.size(), 251)

    @memorycheck.check("microstructure")
    def boundary(self, periodicities, **answers):
        self.createSkel(periodicities)
        OOF.SegmentSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='top')
        self.assertEqual(self.s_selection.size(), answers['top'])
        OOF.SegmentSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='bottom')
        self.assertEqual(self.s_selection.size(), answers['bottom'])
        OOF.SegmentSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='left')
        self.assertEqual(self.s_selection.size(), answers['left'])
        OOF.SegmentSelection.Select_Named_Boundary(
            skeleton='microstructure:skeleton', boundary='right')
        self.assertEqual(self.s_selection.size(), answers['right'])
    def BoundaryA(self):
        self.boundary(aperiodic, top=10, bottom=10, right=10, left=12)
    def BoundaryX(self):
        self.boundary(xperiodic, top=10, bottom=10, right=12, left=12)
    def BoundaryY(self):
        self.boundary(yperiodic, top=10, bottom=10, right=10, left=12)
    def BoundaryXY(self):
        self.boundary(xyperiodic, top=10, bottom=10, right=12, left=12)

    @memorycheck.check("microstructure")
    def periodicPartners(self, periodicities, **answers):
        self.createSkel(periodicities)
        # Select top edge
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(-0.0371595,1.02004), Point(1.05428,0.951556)],
            shift=0, ctrl=0)
        self.assertEqual(self.s_selection.size(), 10)
        OOF.SegmentSelection.Select_Periodic_Partners(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.s_selection.size(), answers['top'])
        # select a horizontal line through the middle, from edge to edge
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(-0.0285992,0.330934), Point(1.05,0.262451)],
            shift=0, ctrl=0)
        self.assertEqual(self.s_selection.size(), 10)
        OOF.SegmentSelection.Select_Periodic_Partners(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.s_selection.size(), 10)
        # select the whole right edge
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(0.955837,1.0286), Point(1.04144,-0.0243191)],
            shift=0, ctrl=0)
        OOF.SegmentSelection.Select_Periodic_Partners(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.s_selection.size(), answers['right'])

    def PeriodicPartnersA(self):
        self.periodicPartners(aperiodic, top=10, right=10)
    def PeriodicPartnersX(self):
        self.periodicPartners(xperiodic, top=10, right=24)
    def PeriodicPartnersY(self):
        self.periodicPartners(yperiodic, top=20, right=10)
    def PeriodicPartnersXY(self):
        self.periodicPartners(xyperiodic, top=20, right=24)


class Combination_Tests(TestBase):
    def createSkel(self, periodicities):
        TestBase.createSkel(self, periodicities)
        # Make some selections
        OOF.Graphics_1.Toolbox.Select_Element.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(-0.0157588,1.01576), Point(0.532101,0.373735)],
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(-0.0114786,-0.00291829), Point(0.335214,0.523541)],
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton='microstructure:skeleton',
            points=[Point(-0.0243191,1.01576), Point(0.356615,0.159728)],
            shift=0, ctrl=0)

    ## These tests don't actually depend on the Skeleton periodicity,
    ## because the selected elements, nodes, and segments are not in
    ## the part of the Skeleton that is different for the different
    ## periodicities (one of the refinement operations used to create
    ## the Skeleton produces a periodicity-dependent result).  We
    ## should check the selection operations on the periodic variants
    ## anyway.

    @memorycheck.check("microstructure")
    def elementsFromOther(self, periodicities):
        self.createSkel(periodicities)
        OOF.ElementSelection.Select_from_Selected_Nodes(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.e_selection.size(), 31)
        OOF.ElementSelection.Select_from_Selected_Segments(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.e_selection.size(), 59)
    def ElementsFromOtherA(self):
        self.elementsFromOther(aperiodic)
    def ElementsFromOtherX(self):
        self.elementsFromOther(xperiodic)
    def ElementsFromOtherY(self):
        self.elementsFromOther(yperiodic)
    def ElementsFromOtherXY(self):
        self.elementsFromOther(xyperiodic)


    @memorycheck.check("microstructure")
    def nodesFromOther(self, periodicities):
        self.createSkel(periodicities)
        OOF.NodeSelection.Select_from_Selected_Segments(
            skeleton='microstructure:skeleton')
        self.assertEqual(self.n_selection.size(), 52)
        OOF.NodeSelection.Select_from_Selected_Elements(
            skeleton='microstructure:skeleton',
            internal=False, boundary=True)
        self.assertEqual(self.n_selection.size(), 24)
        OOF.NodeSelection.Select_from_Selected_Elements(
            skeleton='microstructure:skeleton',
            internal=True, boundary=True)
        self.assertEqual(self.n_selection.size(), 58)
        OOF.NodeSelection.Select_from_Selected_Elements(
            skeleton='microstructure:skeleton',
            internal=True, boundary=False)
        self.assertEqual(self.n_selection.size(), 34)
        # This case should be prohibited, but it's not...
        OOF.NodeSelection.Select_from_Selected_Elements(
            skeleton='microstructure:skeleton',
            internal=False, boundary=False)
        self.assertEqual(self.n_selection.size(), 0)
    def NodesFromOtherA(self):
        self.nodesFromOther(aperiodic)
    def NodesFromOtherX(self):
        self.nodesFromOther(xperiodic)
    def NodesFromOtherY(self):
        self.nodesFromOther(yperiodic)
    def NodesFromOtherXY(self):
        self.nodesFromOther(xyperiodic)

    @memorycheck.check("microstructure")
    def segmentsFromOther(self, periodicities):
        self.createSkel(periodicities)
        OOF.SegmentSelection.Select_from_Selected_Elements(
            skeleton='microstructure:skeleton',
            internal=False, boundary=True)
        self.assertEqual(self.s_selection.size(), 24)
        OOF.SegmentSelection.Select_from_Selected_Elements(
            skeleton='microstructure:skeleton',
            internal=True, boundary=True)
        self.assertEqual(self.s_selection.size(), 111)
        OOF.SegmentSelection.Select_from_Selected_Elements(
            skeleton='microstructure:skeleton',
            internal=True, boundary=False)
        self.assertEqual(self.s_selection.size(), 87)
        OOF.SegmentSelection.Select_from_Selected_Elements(
            skeleton='microstructure:skeleton',
            internal=False, boundary=False)
        self.assertEqual(self.s_selection.size(), 0)
    def SegmentsFromOtherA(self):
        self.segmentsFromOther(aperiodic)
    def SegmentsFromOtherX(self):
        self.segmentsFromOther(xperiodic)
    def SegmentsFromOtherY(self):
        self.segmentsFromOther(yperiodic)
    def SegmentsFromOtherXY(self):
        self.segmentsFromOther(xyperiodic)
        
        
        
def run_tests():
    element_tests = [
        Element_Selection_Test("ElementTypeA"),
        Element_Selection_Test("ElementTypeX"),
        Element_Selection_Test("ElementTypeY"),
        Element_Selection_Test("ElementTypeXY"),
        Element_Selection_Test("MaterialA"),
        Element_Selection_Test("MaterialX"),
        Element_Selection_Test("MaterialY"),
        Element_Selection_Test("MaterialXY"),
        Element_Selection_Test("HomogeneityA"),
        Element_Selection_Test("HomogeneityX"),
        Element_Selection_Test("HomogeneityY"),
        Element_Selection_Test("HomogeneityXY"),
        Element_Selection_Test("ShapeEnergyA"),
        Element_Selection_Test("ShapeEnergyX"),
        Element_Selection_Test("ShapeEnergyY"),        
        Element_Selection_Test("ShapeEnergyXY"),
        Element_Selection_Test("IllegalA"),
        Element_Selection_Test("IllegalX"),        
        Element_Selection_Test("IllegalY"),
        Element_Selection_Test("IllegalXY"),
        Element_Selection_Test("ExpandA"),
        Element_Selection_Test("ExpandX"),
        Element_Selection_Test("ExpandY"),
        Element_Selection_Test("ExpandXY"),
        Element_Selection_Test("SelectGroup")
        ]

    node_tests = [
        Node_Selection_Test("InternalA"),
        Node_Selection_Test("InternalX"),
        Node_Selection_Test("InternalY"),
        Node_Selection_Test("InternalXY"),
        Node_Selection_Test("ExpandA"),
        Node_Selection_Test("ExpandX"),
        Node_Selection_Test("ExpandY"),
        Node_Selection_Test("ExpandXY"),
        Node_Selection_Test("SelectGroup"),
        Node_Selection_Test("BoundaryA"),
        Node_Selection_Test("BoundaryX"),
        Node_Selection_Test("BoundaryY"),
        Node_Selection_Test("BoundaryXY"),
        Node_Selection_Test("PeriodicPartnersA"),
        Node_Selection_Test("PeriodicPartnersX"),
        Node_Selection_Test("PeriodicPartnersY"),
        Node_Selection_Test("PeriodicPartnersXY"),
        ]
    
    segment_tests = [
        Segment_Selection_Test("InternalA"),
        Segment_Selection_Test("InternalX"),
        Segment_Selection_Test("InternalY"),
        Segment_Selection_Test("InternalXY"),
        Segment_Selection_Test("HomogeneityA"),
        Segment_Selection_Test("HomogeneityX"),
        Segment_Selection_Test("SelectGroup"),
        Segment_Selection_Test("BoundaryA"),
        Segment_Selection_Test("BoundaryX"),
        Segment_Selection_Test("BoundaryY"),
        Segment_Selection_Test("BoundaryXY"),
        Segment_Selection_Test("PeriodicPartnersA"),
        Segment_Selection_Test("PeriodicPartnersX"),
        Segment_Selection_Test("PeriodicPartnersY"),
        Segment_Selection_Test("PeriodicPartnersXY"),
        ]

    combined_tests = [
        Combination_Tests("ElementsFromOtherA"),
        Combination_Tests("ElementsFromOtherX"),
        Combination_Tests("ElementsFromOtherY"),
        Combination_Tests("ElementsFromOtherXY"),
        Combination_Tests("NodesFromOtherA"),
        Combination_Tests("NodesFromOtherX"),
        Combination_Tests("NodesFromOtherY"),
        Combination_Tests("NodesFromOtherXY"),
        Combination_Tests("SegmentsFromOtherA"),
        Combination_Tests("SegmentsFromOtherX"),
        Combination_Tests("SegmentsFromOtherY"),
        Combination_Tests("SegmentsFromOtherXY")
        ]

    test_set = element_tests + node_tests + segment_tests + combined_tests
    test_set = combined_tests

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

