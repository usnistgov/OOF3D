# -*- python -*-
# $RCSfile: skeletonbdy.py,v $
# $Revision: 1.14.18.9 $
# $Author: langer $
# $Date: 2014/09/26 20:55:22 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.SWIG.common import switchboard
from ooflib.tutorials import tutorial
TutoringItem = tutorial.TutoringItem
TutorialClass = tutorial.TutorialClass


   
def new_boundaries(*args):
    switchboard.notify("new boundaries for tutorial")
switchboard.requestCallback("new boundary created", new_boundaries)

TutorialClass(
    subject = "Skeleton Boundaries",
    ordering=3,
    lessons = [
    TutoringItem(
    subject="Introduction",
    comments=
    
    """This tutorial explains
    how to construct boundaries in skeletons.

    Skeleton boundaries are the places to which boundary conditions
    are applied.  Boundaries created in a skeleton are automatically
    propagated to previous and later BOLD(modifications) of the skeleton,
    and are also created in all of the finite-element BOLD(meshes)
    associated with each of these modifications.

    This tutorial tries to give a flavor of the different ways in
    which you can create boundaries.  In some cases there are
    different ways of doing the same thing, and this tutorial doesn't
    always demonstrate the easiest, in order to give a better feel for
    the total range of possibilities.  As always, you are encouraged
    to explore on your own.
    """  
    ),
      
    TutoringItem(
    subject="Default Boundaries",

    comments=
    """When an initial Skeleton is created, it automatically constructs
    BOLD(26) default boundaries: 6 faces, 12 edges, and 8 corners.
    These boundaries will be properly preserved throughout the
    skeleton modification processes.

    If you need to apply boundary conditions to places other than
    these, you need to create boundaries yourself, which you will
    learn how to do in this tutorial."""  ),

    TutoringItem(
    subject="Point Boundaries and Edge Boundaries",
    comments=

    """OOF3D provides three kinds of boundaries, BOLD(point boundaries),
    BOLD(edge boundaries), and BOLD(face boundaries).  A point
    boundary is merely a collection of one or more nodes. An edge
    boundary is a collection of one or more segments with a specified
    direction. A face boundary is a collection of element faces with a
    specified normal"""  ),

    TutoringItem(
    subject="Sample Skeleton",
    comments= 
    """Let's load a sample skeleton.  Download and uncompress the file
    BOLD(two_circles.skeleton.gz) from
    http://www.ctcms.nist.gov/oof/oof3d/examples, or locate
    BOLD(two_circles.skeleton) within the share/oof3d/examples
    directory in your OOF3D installation.

    Choose BOLD(Load/Data) from the BOLD(File) menu in the main OOF3D
    window.  Open the file BOLD(two_circles.skeleton).

    Open a graphics window, if you haven't yet.  (If you see the image
    but not the Skeleton, BOLD(Tumble) the view slightly.)
    """,
    signal = ("new who", "Skeleton")
    ),

    TutoringItem(
    subject="Three Boundaries to Create",
    comments=

    """We'll create four additional boundaries in this skeleton.

    1. A closed face boundary consisting of all of the faces
    surrounding the BOLD(red) voxels.

    2. An open face boundary consisting of all of the faces of the
    BOLD(red) elements on the BOLD(Zmax) (front) side of the Skeleton.

    3. A closed clockwise edge boundary around the circumference of
    the BOLD(red) circle on the front face BOLD(Zmax).

    4. A point boundary around the circumference of the BOLD(red)
    circle on the front face.

    """

    # If you did not do the unusualmesh tutorial, go ahead and do it.
    # You should get a way to have specific boundaries. for example in this
    # case if you want to go for the cylinders BOLD(red) and BOLD(yellow),
    #  you will have boundary surfaces that are non oriented. You cannot
    #  create boundaries from unoriented surfaces. That's why we will only focus
    #  on the front visible faces of the areas we want.
    ),

    TutoringItem(
    subject="Selecting Elements by Dominant Voxel",
    comments=
    
    """Let us create the first boundary.

    Open the BOLD(Skeleton Selection) toolbox from
    the graphics window.  Make sure that the toolbox is in BOLD(Element)
    mode and select BOLD(ByDominantVoxel) from the pull-down menu
    for the parameter BOLD(Method).

    Click on any BOLD(red) voxel to select all the elements inside
    the red cylinder.

    It's hard to see that anything's been selected because you can't
    see inside the 3D image, and the selected elements are shown in red,
    which doesn't show up on the surface of the red voxels.  Use the
    BOLD(Show) checkbox in the layer list to temporarily hide the
    image, and BOLD(Tumble) the skeleton to see the selected elements.

    The size of the selection, shown at the bottom of the toolbox,
    should be BOLD(454).
    """,
    signal = "changed element selection"
    ),

    TutoringItem(
    subject="Select Elements and Faces",
    comments=
    """
    Open the BOLD(Skeleton Selection) pane on the main OOF window and make
    sure it's in BOLD(Elements) mode.  Create an element group
    BOLD(RedElements), and BOLD(Add) the contents of the current
    element selection to it.

    Switch the pane to BOLD(Faces) mode, and select the exterior faces
    of the currently selected element set.  Do this by setting the
    BOLD(Action) in the BOLD(Face Selection Operations) pane to be
    BOLD(Select from Selected Elements), setting coverage to
    BOLD(Exterior), and clicking BOLD(OK).  The newly selected faces
    will be colored blue in the graphics window, but because they're
    drawn on top of selected red elements, they appear to be purple.
    You can unselect the elements if you like.
    
    Create a new face group, BOLD(RedFaces), and add the selected
    faces to it."""
    ),  

    TutoringItem(
    subject="Create a Closed Face Boundary",
    comments=
    """
    Go to the BOLD(Skeleton Boundaries) page in the main OOF window,
    and click the BOLD(New...) button.

    Give the new boundary a name, like "Red Cylinder"

    In the dialog box, select BOLD(Face boundary from faces), with
    BOLD(group) set to either BOLD(<selection>) or BOLD(RedFaces).
    They're the same, as long as you didn't change the face selection
    after creating the group in the last step.

    If we were using boundary conditions that dependend on the normal
    to the surface, we'd need to define which side of the surface is
    in the positive normal direction.  Because the selected faces form
    a closed surface, the choices for BOLD(direction) are BOLD(Inward)
    or BOLD(Outward).  Choose one.
    
    Click BOLD(OK).

    You've created a new Skeleton Boundary.
    """,
    signal= "new boundary created"
    ),

    TutoringItem(
    subject="Viewing and Editing a Selected Boundary",
    comments="""
    The new boundary is now selected in the BOLD(Boundaries) list on
    the BOLD(Skeleton Boundaries) page, and information about it
    appears in the right hand pane.  In the graphics window, orange
    dots appear on the surface of the blue (or purple) cylinder.  The
    dots are the ends of arrowheads (cones, really) that are drawn
    through each face of the boundary, indicating the direction of the
    positive normal.  The boundary faces themselves are colored orange
    too, but you can't see them because they're also selected, which
    colors them blue.

    Go to the BOLD(Skeleton Selection) page and clear the selected
    faces.  Now you can't see some of the arrows as well because
    they're orange on orange, but you can BOLD(Tumble) the view to
    make them visible.

    Back on the BOLD(Skeleton Boundaries) page, click the BOLD(Modify)
    button.  Set BOLD(modifier) to BOLD(Reverse direction) and click
    BOLD(OK).  All of the arrowheads have flipped.

    Control-click on the selected boundary in the BOLD(Boundaries)
    list to deselect it.  The orange faces and arrows no longer appear
    in the graphics window.
    """),
    
    TutoringItem(
    subject="Select the Front Face of the Red Cylinder",
    comments=

    """
    Go back to the BOLD(Skeleton Selection) page to start working on
    the second new boundary, consisting of the faces of the red
    cylinder that lie on the front face of the Skeleton.

    With BOLD(Selection Mode) set to BOLD(Faces), set BOLD(Action) to
    BOLD(Select Named Boundary) and BOLD(boundary) to BOLD(Zmax), and
    click BOLD(OK). You should see the front plane entirely selected.
    Then set BOLD(Action) to BOLD(Intersect Group) and pick
    BOLD(RedFaces). This means that you are deselecting faces that are
    not in the BOLD(RedFaces) group. Go ahead and click BOLD(OK).

    Save this set of faces as a group named BOLD(Redfront).
    """
    ), 

    TutoringItem(
    subject="Create an Open Face Boundary",
    comments="""
    Open the BOLD(Skeleton Boundaries) page in the main OOF3D window.

    Click the BOLD(New...) button.  Enter a name ("RedFace", say), and
    set the BOLD(constructor) parameter to BOLD(Face boundary from
    faces) again, and set BOLD(group) to either BOLD(<selection>) or
    BOLD(RedFront).

    Notice that the BOLD(direction) options are different this time,
    because the faces don't form a closed surface.  Select BOLD(-Z to
    +Z) and click BOLD(OK).

    You've now created a second new boundary.
    """,
    signal= "new boundary created"),

    TutoringItem(
    subject="Edge Boundary from Faces",
    comments=
    """
    Now we'll create a closed edge boundary around the perimeter of
    the previous boundary.  Click BOLD(New...) in the BOLD(Skeleton
    Boundaries) page again.

    Select BOLD(Edge boundary from faces) and select BOLD(RedFaces)
    for the parameter BOLD(group).  You should see that the
    BOLD(direction) chooser says BOLD(No edge sequence), and the
    BOLD(OK) button isn't clickable.  This is because the RedFaces
    group is a closed surface and doesn't have a perimeter that can
    form an edge boundary.

    Click BOLD(Cancel) so that you can go on to the next tutorial page. """
    ),
    
    TutoringItem(
    subject="Edge Boundary from Selected Front Faces",
    comments=

    """Click BOLD(New...) in the BOLD(Boundaries) pane yet again.

    Check the little box that is next to the parameter BOLD(name) and
    type in BOLD(Red Circle) for the name of the boundary.

    Select BOLD(Edge boundary from faces) and select BOLD(<selection>)
    or BOLD(RedFront) for the BOLD(group).  The direction choices are
    now things like BOLD(Clockwise-x), which means "clockwise when
    viewed from the +X side of the Skeleton.  Since this boundary is
    in the YZ plane, that isn't a sensible way of specifying the
    direction.  Set it to BOLD(Clockwise-z) instead.
    
    Click BOLD(OK) to create the boundary.  The new boundary is drawn
    with orange segments in the graphics window, and each segment has
    an arrow pointing clockwise.  (Restore the BOLD(Front) view using
    the menu at the top right of the grpahics window if necessary.)
    """,
    signal= "new boundary created"),

    TutoringItem(
    subject="Select Points",
    comments=

    """Next let's create a point boundary along the perimeter of the
    same front face of the red cylinder. 

    If you do the same thing you did in the previous step, but select
    BOLD(Point boundary from faces) in the BOLD(New) dialog, you will
    create a boundary consisting of all of the nodes on the selected
    faces, not just the ones on the perimeter.  Try it if you like,
    but that's not what we want to do.
    
    To select just the perimeter nodes, go back to the BOLD(Skeleton
    Selection) page.  Make sure that the BOLD(RedFront) face group is
    still selected by using BOLD(Select Group) in BOLD(Faces) mode.
    Then switch to BOLD(Nodes) mode, and choose BOLD(Select From
    Selected Faces), BOLD(coverage) to BOLD(Exterior), and click
    BOLD(OK).  Switch back to BOLD(Faces) mode to clear the face selection.

    The selected nodes are drawn in the graphics window with small
    blue dots (which might be a bit hard to see)."""
    ),

    TutoringItem(
    subject="Create a Point Boundary",
    comments=

    """Now go back to the BOLD(Skeleton Boundaries) page and click
    BOLD(New).  This time, choose BOLD(Point boundary from nodes) with
    BOLD(group) set to BOLD(<selection>).  There's no BOLD(direction)
    because point boundaries aren't oriented.  Set a name and click
    BOLD(OK).

    The new point boundary is highlighted in the graphics window with
    orange spheres. """,
    signal="new boundary created"
    ),

    TutoringItem(
    subject="Homework Exercises",
    comments=
    """
    1. Create an open face boundary between the cyan region and the
    white region.  It may be convenient to create element groups for
    each region.  Because the data file included voxel groups, you can
    create the element groups in one step with the BOLD(Auto) button
    on the BOLD(Skeleton Selection) page in BOLD(Elements) mode.

    2. Using only the tools in the BOLD(Skeleton Selection) and
    BOLD(Skeleton Boundaries) page, without resorting to clicking on
    individual elements, create a closed face boundary that includes
    the red and yellow cylinders and a narrow isthmus between them.

    3. Select a Mobius strip of contiguous faces and try to create a
    boundary from them.

    """
    )])

    # TutoringItem(
    # subject="One Last Boundary",
    # comments=

    # """Next let's create the face boundary along the surface of the
    # BOLD(cyan) component from elements and then from faces.  This is
    # similar to operations you've just been doing, but here we select
    # BOLD(Face boundary from elements). Pull the BOLD(group) to
    # BOLD(CyanElements) and leave BOLD(direction) to BOLD(Outward). You
    # can try the others later. Click BOLD(OK).  You will see the
    # resulting boundary being displayed. Saely this is working only
    # for this component. Because the BOLD(Red), BOLD(Yellow) and
    # BOLD(White) do not have orientable surfaces so no faces boundaries
    # can be created from them. On the other end, while going for the
    # faces picking all the faces for each components gives the same
    # result as the elements, picking the fron faces for each components
    # will allow you to create some boundaries."""
    # ),

    # TutoringItem(
    # subject="Fin",
    # comments=

    # """So far, we've covered most of important features concerning
    # skeleton boundaries.
    
    # Further details, if needed, may be found in the manual.
    
    # Thanks for trying out the tutorial."""
    # )
    
    # ])
