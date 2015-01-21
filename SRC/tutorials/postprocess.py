# -*- python -*-
# $RCSfile: postprocess.py,v $
# $Revision: 1.22.18.7 $
# $Author: langer $
# $Date: 2014/09/26 20:55:22 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.tutorials import tutorial
TutoringItem = tutorial.TutoringItem
TutorialClass = tutorial.TutorialClass

      
TutorialClass(
    subject = "Postprocessing",
    ordering = 4,
    lessons = [
      
    TutoringItem(
    subject="Introduction",
    comments=

    """OOF3D provides various post-processing tools for viewing and
    analyzing a solution.  This tutorial provides a brief discussion
    of these tools."""  ),

    TutoringItem(
    subject="Example Mesh",
    comments=

    """Let's load an example Mesh.  Download and uncompress the file
    BOLD(cyallow.mesh.gz) from
    http://www.ctcms.nist.gov/oof/oof3d/examples, or locate
    BOLD(cyallow.mesh) within the share/oof3d/examples directory in
    your OOF3D installation.  From the BOLD(File) menu, choose
    BOLD(Load/Data), and in the file selector, select
    BOLD(cyallow.mesh).  Click BOLD(OK) to load the mesh.""",
    signal = ("new who" ,"Mesh")
    ),

    TutoringItem(
    subject="Graphics window",
    comments=

    """Open a graphics window to display the mesh.  If you've
    completed the BOLD(Simple Example) tutorial, you should be
    familiar with this mesh.
    
    First, we'll go over standard features such as displaying contour
    (filled or line) plots and element/node queries in the graphics
    window."""

    ),

    TutoringItem(
    subject="New layer",
    comments=

    """We'll start with a filled contour of the displacement in the
    x-direction, which is one of a few non-trivial results - the mesh
    is subjected to an uniaxial tension in the x-direction.
    
    In the graphics window, create a new layer using the BOLD(New)
    entry of the BOLD(Layer) menu on the graphics window menubar.  A
    layer dialog will pop up.  Select BOLD(Mesh) for BOLD(Category).
    If you have other meshes in the system, make sure you choose
    BOLD(cyallow) from the second option menu that represents the
    microstructure of the mesh.
    
    In the BOLD(how) option block, select BOLD(FilledContour), BOLD(Field)
    and  BOLD(Component).  Then, select BOLD(Displacement) and BOLD(x)
    for the field and the component, respectively.
        
    The option BOLD(where) determines whether to plot the contour at
    the displaced or original position.  Select BOLD(Original).
    
    Leave the next six options as they are.  Click BOLD(OK) to display
    the contour plot."""
    ),
        
    TutoringItem(
    subject="More levels for contour",
    comments=
    """Bring up the graphics window to check the contour displayed.  You
    may have to hide the image layer in order to see your
    contours. 

    If you want to put more levels in the contour, you can edit it by
    double clicking in the layer list. (There are two Mesh layers.  Be
    sure to double click the layer that says "FilledContourDisplay" in
    the "How" column of the list.)  Look for the parameter
    BOLD(levels) and type in BOLD(21).  Click BOLD(OK).  The contour
    plot in the graphics window should reflect the change
    accordingly.

    Edit the layer again, and change BOLD(where) to BOLD(Actual).  Now
    the contour display lines up with the displaced Mesh edges,
    instead of the undisplaced Skeleton edges.  You can hide the
    SkeletonEdgeDisplay.
    """
    ),

    # TutoringItem(
    # subject="Values for the level",
    # comments=

    # """A map of all the contour levels is displayed on the right-hand
    # pane of the graphics window, called the BOLD(Contour Map).  The
    # actual value range for a given color on the BOLD(Contour Map) can
    # be queried here, by clicking on the contour map itself.  This will
    # cause the value range for the clicked color-block to be displayed
    # at the bottom of the contour map pane.""" ),
        
    TutoringItem(
    subject="Mesh info toolbox",
    comments=

    """While contour plots are effective in presenting the overall
    trend, if you are interested in result data at specific locations,
    you need to use other tools.  OOF3D provides the BOLD(Mesh Info)
    toolbox for this situation.
    
    Open the BOLD(Mesh Info) toolbox in the graphics window.  The
    toolbox lets you query complete information on elements and
    nodes""" ),
        
    TutoringItem(
    subject="Querying node data",
    comments=

    """The first order of business in using the toolbox is to set
    the mode.  Set the toolbox in the node mode by clicking on the label
    BOLD(Node) or the check box for it.

    Hide the Contour, Skeleton, and Image layers in the graphics window so that
    you can see the Mesh nodes.
    
    Click on any node that you think might be interesting.  The
    queried node is highlighted as a blue dot and its basic
    data, such as index and position, are displayed in the
    information frame."""),
        
    TutoringItem(
    subject="Querying element data",
    comments=

    """Now, switch the toolbox to the element mode.  As soon as you
    switch the mode, you will notice an element is automatically
    selected.  It's the closest element to the last mouse point from
    the previous mode.
    
    By default, basic data, including index, nodes, and 
    material, are displayed. 

    Double clicking on a node in the list of nodes in the toolbox will
    switch it into Node mode for the selected node.
    
    To query BOLD(Displacement) or BOLD(Stress) data, use the
    BOLD(Mesh Data) window.  [Not available in 3.0.0.]  The BOLD(Mesh
    Data) results are calculated at the mouse point, and are updated
    each time the mouse is clicked on the Mesh when the Mesh Info
    toolbox is active.  Note that to query points inside the Mesh, you
    need to set a clipping plane in the BOLD(Viewer) toolbox.
    """),
    
    TutoringItem(
    subject="Clearing up",
    comments=

    """There are three utility buttons at the bottom of the toolbox.  They
    are self-explanatory.  Click on the BOLD(Clear) button, which will
    clear the selection on the canvas, and remove the associated
    selection data from the toolbox.  It does not clear the data in
    the data viewer."""),
        
    TutoringItem(
    subject="Analysis page",
    comments=

    """Move to the BOLD(Analysis) page in the main BOLD(OOF) window.
    These tools do not require that the data be present in the
    graphics windown.  This BOLD(Analysis) page includes statistical
    operations, as well as direct output."""),

    TutoringItem(
    subject="Analysis page - organization",

    comments=

    """There are four panes in this window.  Each pane has automatic
    scroll-bars -- it may be necessary to enlarge the main OOF window,
    or scroll the panes, to see all the controls.  The BOLD(Output)
    pane determines what data will be used for the analysis operation.
    The BOLD(Operation) pane determines how the data will be
    processed.  The BOLD(Domain) pane determines where the data will
    come from, and the BOLD(Sampling) pane determines how data will be
    taken from the domain.

    The selections available in the BOLD(Sampling) pane are sensitive
    to what selections have been made in the BOLD(Domain) and
    BOLD(Operation) panes.

    Go to the next tutorial page for an example."""  ),

    TutoringItem(
    subject="Analysis page - Grid example",
    comments=

    """We will evaluate some data on an evenly-spaced BOLD(Grid) of points.

    Begin with the BOLD(Output) pane.  Select BOLD(Field) and
    BOLD(Derivative).  As soon as you select BOLD(Derivative), another
    menu bar should appear.  Select BOLD(Component).  So far, we've
    decided that we're going to output a derivative of a field
    component.  The next three option menus are for specific choices.
    Select BOLD(Displacement), BOLD(x), and BOLD(x) in order - it's a
    normal strain in the BOLD(x)-direction.

    Select BOLD(Entire Mesh) for the BOLD(Domain), and BOLD(Direct
    Output) for the BOLD(Operation).

    Then select BOLD(Grid Points), and set BOLD(x_points),
    BOLD(y_points), and BOLD(z_points) to BOLD(3), so we get a
    manageable (small) amount of data.  You may also elect to suppress
    certain columns from the data output using the toggle buttons.
    For now, retain all of the data.

    The BOLD(Destination) pane at the bottom of the BOLD(Analysis)
    page governs where the data will go.  You can click BOLD(New) to
    enter a file name, or use the pull-down menu to select previous
    files or the Message window.  Leave it set to BOLD(<Message
    Window>).
    
    Press BOLD(Go).  Check the output in the Message window.

    If you scroll up in the message window you'll see that the output
    is preceded by some comments describing the data.  Comments are
    indicated by '#'.  If you were sending the data to a file, perhaps
    to be read by another program, you might want to use a different
    comment character or use a different way of delimiting columns of
    data.  You can change them in the BOLD(Settings/Output Formatting)
    menu in the main OOF3D window's menu bar.
    """),
    
    TutoringItem(
    subject="Analysis page - Notes",
    comments=

    """Experiment with other BOLD(Operations) in the BOLD(Analysis)
    page.  Select BOLD(Average) or BOLD(Standard Deviation), and hit
    BOLD(Go) again.

    Other available BOLD(Domains) include voxel groups or selections,
    element groups or selections, face and point boundaries, and
    linear or planar mesh cross-sections.

    BOLD(Grid) samples on element or voxel groups or selections are
    computed on a rectangular bounding box of the selection,
    discarding grid points that are outside of the sampling region.
    BOLD(Grid) sampling is not available on face boundaries or planar
    cross sections.

    When using a BOLD(Face Boundary) domain, it's necessary to specify
    which side of the faces to use.  Quantities are evaluated in the
    element on the BOLD(FRONT) or BOLD(BACK) side.  FRONT is the side
    in the direction of the positive surface normal.  If only one side
    has an element, that element will be used, however.

    There is no way to use an edge boundary as a domain, because there
    is no easy way to determine which elements should be used when
    evaluating the data.

    """
    )
    
    ])
