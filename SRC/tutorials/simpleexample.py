# -*- python -*-
# $RCSfile: simpleexample.py,v $
# $Revision: 1.26.2.13 $
# $Author: langer $
# $Date: 2014/09/23 17:42:35 $

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


TutorialClass(subject="A Simple Example",
              ordering=0.1,
              lessons = [
    TutoringItem(
    subject="Introduction",
    comments=

    """This tutorial is designed to familiarize users with OOF3D by
    guiding them through a simple but complete project.

    We assume that you run this tutorial from a fresh start of OOF3D.
    Whether you run it this way or not doesn't make any significant
    difference but it simplifies things in a few places.

    BOLD(Objective): A simple finite element analysis of a fictitious
    microstructure under uniaxial tension.  The microstructure is
    composed of two fictitious materials named BOLD(yellow) and
    BOLD(cyan) with linear elastic properties given by:

    BOLD(yellow) : E=1.0, nu=0.3

    BOLD(cyan) : E=0.5. nu=0.3
    """
        ),
    
    

    TutoringItem(
    subject="Graphics Window",
    comments=

    """Open a graphics window, if none has been opened yet, with the
    BOLD(Graphics/New) command in the BOLD(Windows) menu in any OOF3D
    window.  Graphical representations of entities such as
    Microstructure, Skeleton, and Mesh, are displayed in the graphics
    window.
    """
    ),

    TutoringItem(
    subject="Get the Image",
    comments=
    """Download and unpack the file BOLD(cyallow.tar.gz) from
    http://www.ctcms.nist.gov/oof/oof3d/examples to create the
    BOLD(cyallow) directory, or locate the directory within the
    share/oof3d/examples directory in your OOF3D installation.
    """),

    TutoringItem(
    subject="Loading a Microstructure and an Image",
    comments=

    """Open the BOLD(Microstructure) page from the BOLD(Task) menu in
    the main OOF3D window.

    Create a new Microstructure from the cyallow image files by
    clicking the BOLD(New from Image Files) button.

    In the file selector, navigate to BOLD(cyallow).  For now,
    leave the BOLD(microstructure_name), BOLD(width) and BOLD(height)
    values set to BOLD(automatic).  Click BOLD(OK).

    You should see an image -- cyan on top of yellow -- displayed on
    the graphics window.  Also, the BOLD(Microstructure) pull down
    menu at the top of the Microstructure page now should contain a
    single entry, "cyallow", which is the automatically generated name
    for the Microstructure that was created by the BOLD(New from Image
    Files) command.
    """,
    
    signal=("new who", "Microstructure")
    ),

    TutoringItem(
    subject="Categorizing Pixels",
    comments=

    """At this point, a microstructure has been created but it
    contains no useful information other than its size.

    We need to let the microstructure know that it has two different
    materials and they are represented by the two different colors in
    the Image.

    Generally, this is a fairly complicated process, but the sample
    microstructure in this tutorial can be automatically categorized
    with a single click of a button, since the base image features
    only two distinct colors.

    Open the BOLD(Image) page in the main OOF3D window.

    Click the BOLD(Group...) button, and click BOLD(OK) in the dialog box.

    Go back to the BOLD(Microstructure) page, and notice that two
    voxel groups have been created.""",
    signal="new pixel group"
    ),

    TutoringItem(
    subject="Renaming Pixel Groups",
    comments=

    """The automatically generated names of the voxel groups are not
    terribly convenient. The groups can be renamed.

    Select the first voxel group, BOLD(#ffff00).

    Once it's been highlighted, click the BOLD(Rename) button in the
    column to the left of the Voxel Groups list (not the Rename button
    below the New buttons, which will rename the Microstructure).

    Delete the old name and type in BOLD(yellow), which is the actual
    color of the group.  (Triple-clicking on the old name in the
    dialog box will select the whole name, making it easier to
    replace.)

    Click BOLD(OK) to finalize the change.
    """,
    signal="renamed pixel group"
    ),

    TutoringItem(
    subject="Renaming Pixel Groups -- continued",
    comments=

    """Select the second voxel group and BOLD(Rename) it to
    BOLD(cyan).

    Now you're ready to create materials for each voxel group.
    """,
    signal="renamed pixel group"
    ),        

    TutoringItem(
    subject="Adding Materials",
    comments=
    """Open the BOLD(Materials) page in the main OOF3D window.

    The page contains two panes.  The left hand BOLD(Property) pane
    allows you to define material properties.  The right hand
    BOLD(Material) pane allows you to combine properties into a
    Material.

    Create a new material by clicking on the BOLD(New) button in the
    BOLD(Material) pane.

    The check box in the BOLD(name) field controls whether OOF3D will
    automatically generate a name for the Material or let you choose
    it.  Click the check box and type BOLD(yellow-material) in the
    text entry field.  (You can use any name you like for the
    material, including names that you've used for other objects.  To
    avoid confusion in this tutorial, though, don't use the name
    "yellow" since it's already been used for the voxel group.)

    Leave "material_type" set to "bulk".
    
    Click BOLD(OK).
    """,
    signal="new_material"
    ),

    TutoringItem(
    subject="Adding Materials -- continued",
    comments=
    """Create a second BOLD(New) material with the name
    BOLD(cyan-material).""",
    signal="new_material"
    ),

    TutoringItem(
    subject="Creating a Property",
    comments=

    """We now need to make our materials meaningful by adding properties
    to them.

    The BOLD(Property) pane on the left side of the Materials page
    hierarchically lists all of the Property types that are installed
    in OOF3D.  Clicking on a triangle pointing RIGHT will expand a level,
    and clicking on a triangle pointing DOWN will collapse a
    level of the hierarchy.

    Start creating a property for BOLD(yellow-material) by selecting
    BOLD(Isotropic) from BOLD(Elasticity) in the BOLD(Mechanical)
    property hierarchy.

    Click BOLD(Copy) and check the box to give it a user-defined name.
    (Use the Copy button in the Property pane, not the one in the
    Material pane!)

    Type in BOLD(yellow_elasticity) and click BOLD(OK).  Note that
    Property names must begin with a letter and can only contain
    letters, numerals, and underscores (they must be legal Python
    variable names). """,
    signal = "new property"
    ),
    
    TutoringItem(
    subject="Parametrizing a Property",
    comments=
    
    """Select BOLD(yellow_elasticity) from the Property hierarchy and
    either double click it or click the BOLD(Parametrize...) button to
    input actual values.

    The elasticity parameters can be entered in a variety of formats.
    The default format is BOLD(Cij).  Change it to BOLD(E and nu) with
    the pull down menu at the top of the Parametrize dialog box.

    Set the Young's modulus (BOLD(young)) to 1.0 and Poisson's ratio
    (BOLD(poisson)) to 0.3.

    Click BOLD(OK) to finish up.
    """,
    signal = "redraw"
    ),

    TutoringItem(
    subject="Adding a Property to a Material",
    comments=

    """ Below the BOLD(New) button in the BOLD(Material) pane is a
    pull-down menu that lists all of the Materials that have been
    defined.  Select the BOLD(yellow-material) that you defined
    earlier.

    Make sure that the BOLD(yellow_elasticity) Property is still
    selected.

    Click BOLD(Add Property to Material) in the BOLD(Property) pane to
    add the Property to the Material.

    The addition should immediately appear in the BOLD(Material) pane,
    in the list of Properties below the Material selector.
    """,
    signal= "prop_added_to_material"
    ),

    TutoringItem(
    subject="Creating Another Property",
    comments=
    """Make another BOLD(Copy) of BOLD(Isotropic) and name it
    BOLD(cyan_elasticity).""",
    signal = "new property"
    ),

    TutoringItem(
    subject="Parametrizing Another Property",
    comments=
    """BOLD(Parametrize) the property BOLD(cyan_elasticity) with these
    values: BOLD(young)=0.5, BOLD(poisson)=0.3.""",
    signal = "redraw"
    ),

    TutoringItem(
    subject="Adding Another Property to a Material",
    comments=

    """Select BOLD(cyan-material) in the Material selector in the
    BOLD(Material) pane, and add the Property BOLD(cyan_elasticity) by
    clicking on the BOLD(Add Property to Material) button.

    Make sure that the Materials contain the correct Properties before
    you move on.  Select a Property in the BOLD(Material) pane and use
    the BOLD(Remove Property from Material) button if you've made a
    mistake.  """,
        
    signal= "prop_added_to_material"
    ),

    TutoringItem(
    subject="Adding Colors to Materials",
    comments=
    """Although it's not necessary mathematically, it's convenient to
    assign colors to Materials so that the Microstructure can have a
    more informative display.

    BOLD(Copy) the BOLD(Color) property in the BOLD(Property) pane,
    giving the copy the name BOLD(yellow).

    BOLD(Parametrize) the BOLD(yellow) Property.  The color of the
    Material doesn't have to be the same as the color in the Image,
    but might be confusing if it's different.  In the Parametrize
    dialog box, switch from BOLD(Gray) to BOLD(RGBColor), and set the
    BOLD(Red), BOLD(Green), and BOLD(Blue) sliders to something
    yellowish, say BOLD(Red)=1, BOLD(Green=0.8), and
    BOLD(Blue)=0. (You can either slide the sliders or type values
    into the boxes on the right.)  Click BOLD(OK).

    Add the BOLD(yellow) Property to the BOLD(yellow-material).

    Similarly create a BOLD(Color) property for BOLD(cyan) and
    parametrize it with BOLD(Red)=0, BOLD(Green)=0.8, and
    BOLD(Blue)=1.  Add it to the BOLD(cyan-material).  """,

    signal="prop_added_to_material"
    ),

    TutoringItem(
    subject="Assigning a Material to Pixels",
    
    comments=

    """Now that we have defined Materials and created voxel groups in
    the Microstructure, we can assign Materials to the microstructure.

    Select the material BOLD(yellow-material) and click on the button labelled
    BOLD(Assign Material to Voxels...) in the BOLD(Material) pane.

    The pop-up window lets you choose the Microstructure to which the
    Material will be assigned (currently we only have one, "cyallow"),
    and the voxels within the Microstructure.  Choose the voxel group
    BOLD(yellow) in the BOLD(pixels) pull-down menu.  (We often use
    the word "pixel" when we mean "voxel".  OOF2 and OOF3D share a lot
    of code.)

    Click BOLD(OK) to finish.
    """,
    signal = "materials changed in microstructure"
    ),

    TutoringItem(
    subject="Displaying a Microstructure",
    comments=

    """The graphics window displays many things automatically, but if
    you want to view a Microstructure you must tell it to do so
    explicitly by adding a new BOLD(Display Layer).

    Dig up the Graphics window that you opened earlier by choosing
    BOLD(Graphics/Graphics 1) in the BOLD(Windows) menu on any OOF3D
    window.

    Make this tutorial window large enough to see all of its text
    before continuing...

    Select BOLD(New) from the BOLD(Layer) menu in the Graphics window.
    A BOLD(New) window for layer creation will appear.

    This window is composed of 3 major blocks. A variety of object
    types (called BOLD(categories) in the menu) can be displayed in a
    layer: Microstructure, Image, Skeleton, etc. Those objects types
    can operate on different data sources, which are identified by the
    BOLD(what) attribute. For example you might have many
    microstructures and will have to point BOLD(what) to the one you
    want to use. Finally the BOLD(how) allows you to define how you
    want to display your object in the Graphics canvas. The filter
    component allows you to select sub-parts of the objects
    (selections, group, etc...) or display the results of simple
    operations (union, intersection, complement, etc...).
    
    Select the BOLD(Microstructure) in the category menu then make
    sure BOLD(what) is pointed at BOLD(cyallow). By default
    BOLD(Material) is selected, meaning you will create a display
    layer showing the Material colors.  Below Material you can specify
    the color to use to display voxels that have no assigned material
    BOLD(no_material) or have a material, but one that does not
    contain a color property BOLD(no_color).

    Since we have only two materials that we want to display and they
    cover the entire microstructure, ignore both parameters for now 
    and click the BOLD(OK) button.
    
    This will create the layer and add it to the layers list.

    """),

    TutoringItem(
    subject="Layer List",
    comments=
    
    """The Microstructure Material Display appears in the Graphics
    window.  Pixels to which you assigned the yellow-material are
    drawn in yellow, or whatever color you gave to that Material.  The
    remaining voxels are black because they have no Material, and the
    default value for BOLD(no_material) is black.

    The Layer List in the Graphics Window now shows two layers: a
    Microstructure layer on top of an Image layer.  You may have to
    scroll the list to see both layers.  Because the Microstructure
    and the Image are the same size, you can only see one of them at a
    time.  The buttons in the column labelled BOLD(Show) in the Layer
    List allow you to choose which layers will actually be displayed.
    
    """),

    TutoringItem(
    subject="Assigning a Material to Pixels -- continued",
    comments=
    
    """Select the BOLD(cyan-material) in the BOLD(Material) pane in
    the main OOF3D window and assign it to the voxel group named
    BOLD(cyan).

    Make the Microstructure display layer visible in the graphics
    window, and note that the black voxels have turned cyan, since
    they now have a Material assigned to them.""",

    signal = "materials changed in microstructure"
    ),


    TutoringItem(
    subject="Creating a Skeleton",
    comments=

    """OOF3D doesn't create a finite element mesh directly from a
    Microstructure.  Instead, it creates a BOLD(Skeleton), which
    specifies the mesh geometry and nothing else.  One Skeleton can be
    used to create many different meshes, with different element types
    and different physical fields.

    Open the BOLD(Skeleton) page in the main OOF3D window.

    Since we have such a simple microstructure, creating a reasonable
    skeleton is going to be short and sweet.

    Click the BOLD(New) button to open up a skeleton initializer.

    To keep things simple, just click BOLD(OK) to create a 4x4x4 grid
    of tetrahedral skeleton elements.  (To be precise, it's a 4x4x4
    grid of rectangular boxes, each subdivided into 5 tetrahedra.)
    """,
    
    signal = ("new who", "Skeleton")
    ),

    TutoringItem(
    subject="Snapping Nodes to Material Boundaries",
    comments=

    """The Skeleton is now displayed on top of the Microstructure in the
    graphics window.  (If you can't see the Skeleton, click on the
    BOLD(Tumble) button above the graphics canvas and use the mouse to
    rotate the image slightly.  The filled 3D volume of the Material
    display sometimes hides the lines of the Skeleton display.)

    The second row of elements (from the bottom) contains both
    BOLD(cyan) and BOLD(yellow), while other elements contain only one
    Material.

    The Skeleton will be a better representation of the Microstructure
    if each element contains only one Material (ie, it is
    BOLD(homogeneous).)  To get there, we will need to make some
    modifications to the Skeleton, specifically, we want to move the
    nodes between the bottom two layers of elements to the material
    boundary.
    
    Back in the main window, notice the BOLD(Skeleton Modification)
    pane, in the right hand half of the BOLD(Skeleton) page. Click on
    the chooser widget for the BOLD(method) parameter in that pane,
    and select BOLD(Snap Nodes).

    Set BOLD(alpha) to 1.0.  Place the mouse over the labels and menu
    items to see an explanation of what the parameters mean.
    
    Click BOLD(OK) to modify the skeleton.

    In OOF2, this operation on this very simple image would have
    reliably created a completely homogeneous skeleton, in which all
    of the elements contained just one Material.  In 3D, the more
    complex element geometry means that OOF3D doesn't always find the
    optimum configuration (it's choosing the order of operations at
    random).  The BOLD(Homogeneity Index) displayed on the left side
    of the BOLD(Skeleton) Page indicates how homogeneous the Skeleton
    is.  If it's less than 1.0, there are some inhomogeneous elements
    (which may be hidden inside the Microstructure).  Making the
    Skeleton completely homogeneous isn't necessary, but try undoing
    your node snap, and then running BOLD(Snap Nodes) once or twice
    and watch the homogeneity index.

    """,

    signal = "Skeleton modified"
    ),

    TutoringItem(
    subject="Viewing the Skeleton",
    comments=
    """ It's not possible to see how well the Skeleton matches the
    Microstructure because you can't see inside it.  In the
    BOLD(Layers) list in the Graphics window, uncheck the BOLD(Show)
    boxes in the lines for the BOLD(Microstructure) and the
    BOLD(Image).  Now it's possible to see the Skeleton edges inside
    the Microstructure, but still difficult to tell what's what.

    Make sure that the BOLD(Tumble) button above the canvas is
    selected, and click and drag the mouse within the canvas to rotate
    the view.  You can go back to a previous view, or restore a
    predefined view with the arrow buttons and pull down menu to the
    right of the buttons above the canvas.  This helps a bit, but not
    enough.

    Double-click on the BOLD(Skeleton) layer in the BOLD(Layers) list.
    In the layer-editing dialog, change BOLD(filter=) from BOLD(All)
    to BOLD(Material) and set the BOLD(material=) parameter to
    BOLD(cyan-material).  Click BOLD(OK).  Now only the cyan elements
    are drawn, and you can see if the interface between cyan and
    yellow is smooth.

    To get an even better view, create a new graphics layer, setting
    category=Skeleton, what=cyallow/skeleton, and how=Material Color,
    with filter=Material and material=cyan-material.
    """),

    TutoringItem(
    subject="Creating a Finite Element Mesh",
    comments=
    """It's time to create an FE mesh based on this skeleton.

    Open the BOLD(FE Mesh) page.

    Click the BOLD(New) button to get a dialog box for creating a new
    Mesh.  The BOLD(mapping order) and BOLD(interpolation order)
    pull-down menus specify what order polynomials will be used for
    positioning the elements (mapping) and for interpolating within
    them.  Leave these set to BOLD(1) to use linear elements.

    The pull-down menus labelled BOLD(Tetrahedron element),
    BOLD(Quadrilateral  element), BOLD(triangle  element) and 
    BOLD(Line  element) list the available element types that are
    consistent with the polynomial orders chosen.  There's only one
    choice for each: BOLD(TET4_4), BOLD(Q4_4), BOLD(T3_3) and 
    BOLD(D2_2). Positioning the mouse over the menus will bring up a
    tooltip describing the element type.

    Click BOLD(OK) to create an FE Mesh.

    If you left the Graphics window displays in the state they were in
    at the end of the previous tutorial page, you'll notice that the
    Mesh is now drawn on top of the Skeleton.  You can see it because
    the BOLD(filter) for the default Mesh display is BOLD(All).  You
    may want to hide or delete the Skeleton display layers at this
    point.

    """,
    signal = ("new who", "Mesh")
    ),

    TutoringItem(
    subject="Defining Fields",
    comments=

    """Proceed to the BOLD(Fields & Equations) page.
        
    Here, we need to tell OOF3D about the (known) unknowns of the
    problem that we're trying to solve.

    Fields are BOLD(defined) if they have been given values on the Mesh.

    Fields are BOLD(active) if the solver will find their values.
    Only defined fields can be active.

    We're solving a uniaxial tension problem, so BOLD(displacement) is
    the only (known) unknown.

    Check both boxes for the BOLD(Displacement) field.
    """
    ),

    TutoringItem(
    subject="Activating Equations",
    comments=
    """Stay in the BOLD(Fields & Equations) page.

    We're solving the BOLD(Force_Balance) equation, so check the
    corresponding box BOLD(active) to activate it.

    """ ),

    TutoringItem(
    subject="Applying Boundary Conditions",
    comments=
    """Now, move to the BOLD(Boundary Conditions) page.

    The boundary conditions we're going to apply are:

    BOLD(1.) u_x = 0 on the BOLD(Xmin) boundary. which is on the left
    in the default view
    
    BOLD(2.) u_y = 0 on the BOLD(Ymin) boundary, which is the bottom
    in the default view.

    BOLD(3.) u_y = 10.0 on the BOLD(Ymax) boundary, which is on the
    top in the default view.

    BOLD(4.) u_z = 0 on the XminYminZmin boundary, which is the point
    at the origin.

    If you've tumbled your view away from the default, you can
    identify the x, y and z axes from the colored arrows."""
    ),

    TutoringItem(
    subject="Applying Boundary Conditions -- continued",
    comments=
    """ When constructing new boundary conditions, all of the action
    happens in the dialog box brought up by the BOLD(New...) button.
    OOF3D boundary conditions all have a field, to which they apply
    the condition, and an associated equation component.  The equation
    component must be specified by the user because OOF3D handles
    general couplings between fields, so the program does not
    generally know in advance which equation should be constrained to
    accommodate the new condition.

    OOF3D boundary conditions also have names, which can be convenient
    for referring to them afterwards.

    You can also specify profiles, which allow you to indicate how you
    want the field values to vary along the boundary in space and
    possibly time.

    For this tutorial case, we will stick to constant profiles, and we
    will only have the Displacement field and Force_Balance equations
    to work with.

    Go to the next slide to really set the boundary conditions.
    """),

    TutoringItem(
    subject="Applying Boundary Conditions -- continued",
    comments=
    """First, expand this tutorial window so that you can see the full
    text.  Once you open the boundary condition building dialog, you
    won't be able to scroll the tutorial.
    
    Click the BOLD(New...) button to bring
    up a boundary condition builder.  The pull-down menu at the top of
    the dialog box allows you to choose the type of boundary
    condition.  Leave it set to BOLD(Dirichlet) boundary conditions, which
    gives Fields fixed values at the boundaries.

    The first B.C. deals with displacement in the BOLD(x)-direction,
    so select BOLD(x) for both BOLD(Displacement) and
    BOLD(Force_Balance).

    The BOLD(profile) is the functional form of the Field along the
    boundary.  The predefined boundaries in OOF3D (Xmax, Xmin, Ymax,
    Zmax, Zmin,) are oriented using their normals around the microstructure.
    Set the BOLD(profile) to BOLD(Constant Profile) with BOLD(value)=0.0.

    Finally, choose the BOLD(boundary) to which this condition should
    be applied (BOLD(Xmin)) and click BOLD(OK).

    BOLD(Important Note) Do not click the BOLD(Apply) button in the
    builder window.  This button enables users to continue building
    boundary conditions without having to close and re-open the
    builder window in a real world practice, but in this tutorial
    setting, it will keep you from advancing to the next slide. If you
    DID click BOLD(Apply), close the builder window and move to the
    next slide.

    """,
    
    signal = "boundary conditions changed"
    ),

    TutoringItem(
    subject="Applying Boundary Conditions -- continued",
    comments=

    """Click BOLD(New...) to add the second boundary condition.

    Select BOLD(y) for both BOLD(Displacement) and
    BOLD(Force_Balance).

    Select BOLD(Constant Profile) and type in BOLD(0).

    This condition's going to be applied to the BOLD(Ymin) of the
    mesh. Select BOLD(Ymin) and click BOLD(OK) to finish.""",

    signal = "boundary conditions changed"
    ),

    TutoringItem(
    subject="Applying Boundary Conditions -- continued again",
    comments=

    """Click BOLD(New...) to add the third boundary condition.

    Select BOLD(y) for both BOLD(Displacement) and
    BOLD(Force_Balance).

    The boundary condition's value is BOLD(10.0), and it's constant
    along the face.  Select BOLD(Constant Profile) and type in
    BOLD(10.0).

    This condition's going to be applied to the BOLD(Ymax) face of
    the mesh. Select BOLD(Ymax) and click BOLD(OK) to finish.

    """,
    signal = "boundary conditions changed"
    ),

    TutoringItem(
    subject="Applying Boundary Conditions -- continued again",
    comments=
    """Finally, set the fourth boundary condition by choosing BOLD(z) for
    the field and equation components, BOLD(0) for the profile value,
    and BOLD(XminYminZmin) for the boundary.
    """,
    signal="boundary conditions changed"
    ),

    
    TutoringItem(
    subject="Solving the Equations",
    comments=
    """We're almost at the end of this tutorial.
    
    Open the BOLD(Solver) page.  For this simple example, you just
    need to specify that you want the BOLD(default) subproblem to be
    solved.  Double-click the item in the list in the top pane,
    labelled BOLD(Solvers), and accept the defaults -- it should be
    the BOLD(Basic) solver mode, with a BOLD(Static) time-stepper with
    some reasonable default matrix method parameters.  Click BOLD(OK)
    to set this solver, and then click BOLD(Solve) on the page.  """
    ),
    
    TutoringItem(
    subject="Displaying a Mesh",
    comments=

    """Bring up the graphics window to examine the deformed mesh.
    """),

    TutoringItem(
    subject="Displaying Contours",
    comments=

    """In the layer list at the bottom of the graphics window, 
    double-click on the Mesh layer to bring up the graphics layer editor
    dialog. Make it bigger, if necessary, so that you can view the
    whole dialog.

    In the BOLD(how=) part of the dialog, change the BOLD(Element
    Edges) method to be BOLD(Filled Contour).  The rest of the
    BOLD(how=) box will present some new parameters.  The defaults are
    pretty good.  What we want to display is the BOLD(y) component of
    the BOLD(Displacement) field.  Make sure the dialog box reflects
    this -- if necessary, select BOLD(Field) in the BOLD(what=) part
    of the box, and ensure that it's referring to the BOLD(Component),
    and that the selected component is BOLD(y).  All of these except
    the BOLD(y) component should be the defaults. 

    The BOLD(where=) sub-category of the BOLD(how=) controls whether
    the contours are drawn at the displaced or undisplaced locations
    of the mesh.  Leave this set to BOLD(Actual), which will draw them
    on the displaced mesh.

    Accept the defaults for the contour bounds and colormap. Click
    BOLD(OK) and go back to the Graphics Window to observe the result.
    The map on the right edge of the window indicates how colors
    correspond to actual values.

    Congratulations!!! You've finished your first OOF3D project.
    """
    )

      
    ])
