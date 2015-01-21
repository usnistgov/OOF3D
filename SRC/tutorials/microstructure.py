# -*- python -*-
# $RCSfile: microstructure.py,v $
# $Revision: 1.15.18.10 $
# $Author: langer $
# $Date: 2014/09/25 19:34:16 $

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

TutorialClass(subject="Microstructure",
              ordering=1,

              lessons = [
    TutoringItem(
    subject="Introduction",
    comments=

    """This tutorial covers most of the basic operations related to
    Microstructures in OOF3D by letting users create and manipulate a
    Microstructure based on a typical micrograph.

    A digitized image on a computer is nothing but a three dimensional
    array of colored voxels.  These voxels become meaningful in OOF3D
    only after materials have been assigned to them or they have been
    assembled into voxel groups.

    An OOF3D Microstructure is the data structure that stores this
    information."""  ),

    TutoringItem(
    subject="Graphics Window",
    comments=

    """Open a graphics window with the BOLD(Graphics/New) command in
    the BOLD(Windows) menu.

    Let us get started by creating a microstructure from an image
    file.  """
    ),

    TutoringItem(
    subject="Locate the Data",
    comments=
    """Download and unpack the file BOLD(K1_small.tar.gz) from
    http://www.ctcms.nist.gov/oof/oof3d/examples, or locate the
    BOLD(K1_small) within the share/oof3d/examples directory in your
    OOF3D installation.

    """
    ),
    

    TutoringItem(
    subject="Creating a Microstructure",
    comments=

    """This tutorial page contains a lot of instructions, but you
    won't be able to scroll the page while the microstructure selection 
    dailog box is up. So before you do anything else, enlarge this window
    so that you can see all of the text.
    
    Open the BOLD(Microstructure) page in the main OOF3D window.  Click
    on BOLD(New from Image File).

    In the file selection dialog box, navigate to BOLD(K1_small).

    Look for a parameter named BOLD(microstructure_name).  It's at the
    top of the block of four text entry fields above the OK button..

    If you want to set the name of the microstructure yourself, click
    on the check box next to BOLD(microstructure_name) and type in a
    name.  To use an automatically generated name (which will be the
    same as the image name), leave the box unchecked.

    The parameters BOLD(height), BOLD(width), and BOLD(depth) are the
    physical size of the microstructure in the y, x, and z directions,
    respectively.  Leave these set to BOLD(automatic).  The size will
    be determined by assuming that each voxel is a unit cube.

    Click BOLD(OK) to create the Microstructure.""",

    signal = ("new who", "Microstructure") ),

    TutoringItem(
    subject="A Glance at the Microstructure",
    comments=

    """As shown in the graphics window, the micrograph
    BOLD('K1_small') features two distinct materials, one in
    BOLD(black) and the other in BOLD(white).

    The boundaries between two materials are rather blurry and some
    parts of materials are not as discernable as others.

    At this point, your Microstructure object doesn't contain any
    useful information other than its size and the micrograph itself.

    The ultimate goal of this tutorial session is to establish two
    distinct voxel groups that represent the two materials featured in
    the micrograph.

    For any given voxel, you could decide individually whether it
    belongs to BOLD(black) or BOLD(white).  This process would be
    tedious.  OOF3D contains image manipulation tools to make it
    easier.

    """
    ),
    
    TutoringItem(
    subject="The Image Page",
    comments=

    """
    Open the BOLD(Image) page in the main OOF3D window.

    The two pull-down menus at the top of the page, labelled
    BOLD(Microstructure) and BOLD(Image) comprise the BOLD(Image
    Selector).  They let you choose which BOLD(Image) object the page
    operates on. (Most OOF3D main window pages have some sort of
    Selector at the top.) Since we currently have only one
    Microstructure and it contains only one Image, neither menu in the
    Selector has any other choices in it.

    The left hand pane on the BOLD(Image) page just displays
    information about the chosen Image.

    The right hand BOLD(Image Modification) pane contains a pull-down
    menu labelled BOLD(Method) which lets you select an image
    modification method.
    """
    ),
      
    TutoringItem(
    subject="Normalizing the image",
    comments=

    """Select BOLD(Normalize) from the BOLD(Method) pull-down menu.

    Click BOLD(OK).

    The gray values in the image now span the full range from black to white.
    """,

    signal= "modified image"
    ),

    TutoringItem(
    subject="Increasing Contrast",
    comments=

    """Select BOLD(Contrast) and apply it BOLD(three) times.

    The darker region gets darker and the brighter region gets
    brighter, which make materials more distinguishable than
    before.

    The two materials are now clearly distinguishable except a
    questionable spot in the lower-middle part of the image. For the
    purposes of this tutorial, we will accept that this material is
    dark.  """,
    signal= "modified image"
    ),

    TutoringItem(
    subject="The Voxel Selection Toolbox",
    comments=

    """The image is ready for categorization.

    Unfortunately, one-click do-it-all feature (the BOLD(Group) button
    in the Image page) is not going to work for this micrograph,
    because it contains too many shades of gray. Thus, we will
    categorize the voxels manually using a few BOLD(voxel selection)
    algorithms.

    Go to the graphics window and open the BOLD(Voxel Selection)
    toolbox, using the BOLD(Toolbox) menu at the top of the left hand
    pane. """
        ),

    TutoringItem(
    subject="Point Selector",
    comments=

    """There are a few methods to select desired voxels in the
    toolbox.

    Select BOLD(Point) in the BOLD(Method) pull-down menu.

    Click on a voxel in the Image to select it.  The selected voxel
    will be marked in BOLD(red).
    """,
    signal= "new pixel selection"
    ),

    TutoringItem(
    subject="Selection Modifiers -- shift",
    comments=

    """You can accumulate the selected voxels by holding the
    BOLD(shift) key while clicking the mouse on the image.

    Try selecting multiple voxels by using this feature.
    """,
    signal= "new pixel selection"
    ),

    TutoringItem(
    subject="Undo, Redo, Clear and Invert",
    comments=

    """If you've made a mistake, you can undo the latest few
    selections by clicking on the BOLD(Undo) button in the toolbox.

    If you changed your mind while undoing, you can restore the
    selection status by clicking the BOLD(Redo) button.

    Also available are BOLD(Clear) and BOLD(Invert) buttons, which do
    just what they say.

    """
        ),

    TutoringItem(
    subject="Zooming",
    comments=

    """If you're having a hard time selecting voxels due to their
    small size on the screen, you can select the BOLD(Dolly) mode in
    the graphics window, after which dragging the mouse vertically
    across the canvas will move you closer to or farther from the
    microstructure.  You can also make adjustments to the view in the
    BOLD(Viewer) toolbox, on the left-hand side of the graphics
    window. (This involves selecting away from the BOLD(Voxel
    Selection) toolbox temporarily).  In the BOLD(Zoom) tool, you can
    zoom in, out, or select BOLD(fill) to fill the canvas with the
    microstructure.

    Using the BOLD(Viewer) toolbox will also help you to zoom in on
    particular voxels.

    """
        ),

    TutoringItem(
    subject="Better Selectors",
    comments=

    """Although the BOLD(Point) selector allows individual voxel
    selections for accuracy, BOLD(Burn) and BOLD(Color) selection
    methods are more suited for what we want to accomplish with this
    image.

    Basically, they can select voxels of similar color ranges automatically.

    BOLD(Burn) only selects contiguous voxels, whereas BOLD(Color)
    works on the entire microstructure.

    BOLD(Clear) the current voxel selection, if any, and move on to
    the next slide for some real action.
    """
    ),

    TutoringItem(
    subject="The Color Selector",
    comments=

    """Select BOLD(Color) for the selection method in the BOLD(Voxel
    Selection) toolbox in the Graphics window.

    The BOLD(Color) selector selects all voxels whose color is within
    a specified range of the color of a voxel that you choose with the
    mouse.  Colors in OOF3D are specified in one of three formats:

    BOLD(Gray): a single floating point value between 0 and 1.

    BOLD(RGB): three floating point values between 0 and 1,
    representing red, green, and blue intensities, respectively.

    BOLD(HSV): three floating point values representing hue,
    saturation and value, respectively.  Hue is between 0 and 360.
    Saturation and value are between 0 and 1.

    Since we have a gray-scale image, set the BOLD(range) of the selector
    to BOLD(DeltaGray) with the parameter BOLD(delta_gray) set to 0.4.  

    Now, we need to provide a reference color by clicking on a voxel.
    Click on any BOLD(black) voxel.
    """,
    signal= "new pixel selection"
    ),

    TutoringItem(
    subject="Creating a Voxel Group",
    comments=

    """Invert the selection you've made, using the BOLD(Invert) button
    near the bottom of the BOLD(Voxel Selection) toolbox.  This
    selects all the voxels belonging to the white material -- it's a
    smaller set of voxels than the black original.  Having made this
    selection, it's a good idea to let the microstructure know about
    it.

    Open the BOLD(Microstructure) page on the main OOF window. Create
    a new voxel group by clicking BOLD(New...) in the BOLD(Voxel
    Groups) pane. (Don't create a new microstructure, that's a
    different "New..." button.)

    Check the little box next to the parameter BOLD(name) and type in
    BOLD(white) for its name. (You can use a different name, of
    course, or just use the automatic name, if you're willing to
    forego some of the pedagogic value of this tutorial.)

    Click BOLD(OK) to create a new voxel group.

    The BOLD(Voxel Groups) pane should show the voxel group you just created.
    """,
    signal= "new pixel group"
    ),
    
    TutoringItem(
    subject="Storing Voxels in a Voxel Group",
    comments=

    """ The voxel group you just created doesn't yet contain any
    voxels.  Click BOLD(Add) in the BOLD(Voxel Groups) pane to add the
    currently selected voxels to the group.

    The information for the group will be updated immediately.

    About 79080 voxels should be present in the group, if you did it
    correctly.  You might get a different number if you didn't follow
    the instructions exactly when modifying the image, or if you
    didn't click on the darkest part of the image when you used the
    BOLD(Color) selector two pages ago.
    """,
    signal= "changed pixel group"
    ),

    TutoringItem(
    subject="Playing with Fire",
    comments=

    """As mentioned, BOLD(Burn) works in a similar way to the BOLD(Color)
    selector but with a major difference -- it only selects
    contiguous voxels.

    BOLD(Clear) the selection (it's okay, we saved that group) and
    select BOLD(Burn) in the BOLD(Voxel Selection) toolbox.
    
    Try clicking on any black voxel.

    You'll immediately notice that each selection forms an island and
    does not extend into the white material.

    Thus, if you need to store islands of black voxels to different
    voxel groups, BOLD(Burn) is the way to go.

    Hold the shift key as you click on a black region to select
    multiple islands.
    """,
    signal= "new pixel selection"
    ),

    TutoringItem(
    subject="Copying an Image",
    comments=

    """OOF3D Microstructures can contain multiple versions of an Image,
    or, indeed, multiple unrelated Images, as long as they are all the
    same size.  This can be useful when different microstructural
    features are easier to observe in different images.

    In the BOLD(Image) page, click BOLD(Copy), and click BOLD(OK) in
    the dialog box.

    The BOLD(Image Selector) now shows that the current BOLD(Image) is
    "K1_small<2>" in the BOLD(Microstructure) named "K1_small"
    (unless you gave it a different name when loading the image).  The
    "<2>" is part of the automatically generated name for the copied
    Image."""

    ),


    TutoringItem(
    subject="Displaying the Copied Image",
    comments=

    """In the BOLD(Layer List) at the bottom of the BOLD(Graphics) window,
    you can see the BOLD(Image) layer corresponding to the current
    image display.

    From the BOLD(Layer) menu at the top of the graphics window,
    select BOLD(New...), to bring up the new graphics layer dialog. In
    this dialog, select BOLD(Image) for the category.  Notice that
    there is a source selection, called BOLD(what=), which allows you
    to pick a data source for your new layer. Pick BOLD(K1_small) (or
    whatever name you're using) for the top component (this is the
    microstructure object), and BOLD(K1_small<2>) for the second
    component -- this is your copy of the image.  Accept the defaults
    for the other parameters, and click BOLD(OK). This creates a second image
    layer with the copied image on it.  In principle you could use a
    second image, with different image-processing controls applied, to
    bring out other features of importance in the microstructure."""

    ),

    TutoringItem(
    subject="Revert to the Original Image",
    comments=

    """ Copying an Image isn't very useful if you don't do anything
    different with the copy.  Since we copied the modified Image, we
    can BOLD(undo) the modifications on the original Image.

    Switch the BOLD(Image Selector) in the BOLD(Image) page in the
    main window to the original Image, "K1_small", and click
    BOLD(Undo) four times. """
    
    ),

    TutoringItem(
    subject="Switching Layers",
    comments=
    
    """In the BOLD(Layer List) in the BOLD(Graphics) window, the leftmost
    widget is a checkbox which indicates whether or not a given layer
    should be shown. It's called BOLD(Show) for this reason.  Try
    alternately showing the two image layers to see the effect of our
    undo operations in the graphics window.  When both layers are
    enabled, there's an ambiguity as to which should be shown -- the
    graphics "layer" paradigm is stretched to the breaking point, and
    the actual display depends on implementation details outside of
    user control. You can always selectively show and hide layers to
    get what you want, in this case to either admire the purity of the
    original image, or examine the highly useful normalized and
    contrast-enhanced image."""
    ),
    
    TutoringItem(
    subject="Making Selections with Multiple Images",
    comments=

    """The set of currently selected voxels is a property of a
    BOLD(Microstructure), not of an BOLD(Image).  It's possible to
    select voxels in one Image, switch Images, and then modify the
    selection.

    In the graphics window, switch the BOLD(Voxel Selection Method)
    to BOLD(Color) and set BOLD(range) to BOLD(DeltaGray) with
    BOLD(delta_gray)=0.05.

    Click the mouse in the middle of one of the dark regions in the
    Image.  Note how many voxels have been selected, in the box at the
    bottom of the BOLD(Voxel Selection) toolbox.

    Using the BOLD(Layer List) show controls, switch to the other version of the
    Image.
    Notice that the selection hasn't changed, since you
    haven't changed Microstructures.

    Click on the BOLD(Repeat) button in the toolbox.  This repeats the
    previous mouse click, but this time the selection method will act
    on the other Image.  Notice that a different set of voxels have
    been selected."""
    ),
    

    TutoringItem(
    subject="The Voxel Selection Page",
    comments=

    """Open the BOLD(Voxel Selection) page in the main OOF3D window.
    This page allows you to create and manipulate voxel selections in
    ways that don't require mouse clicks on the graphics window.

    The page has two panes: an information pane on the left and a
    BOLD(Voxel Selection Modification) pane on the right.
    
    Select BOLD(Group) in the BOLD(Method) pull-down menu in
    the Voxel Selection Modification pane.

    Select BOLD(white) for the voxel BOLD(group), BOLD(Select Only)
    for the operator, and click BOLD(OK).  """,
    signal= "new pixel selection"
    ),

    TutoringItem(
    subject="Inverting the Voxel Selection",
    comments=

    """Now that you have selected BOLD(white), to select black voxels
    you only need to invert the current selection.

    Click BOLD(Invert) in the BOLD(Voxel Selection) toolbox in the
    graphics window, or, equivalently, select BOLD(Invert) in the
    BOLD(Method) menu in the BOLD(Voxel Selection) page and click
    BOLD(OK).
    """,
    signal= "new pixel selection"
    ),

    TutoringItem(
    subject="Creating Another Voxel Group",
    comments=
    
    """Open the BOLD(Microstructure) page and create a new voxel group
    named BOLD(black).


    """,

    signal= "new pixel group"
    ),

    TutoringItem(
    subject="Storing Voxels in a Voxel Group -- again",
    comments=

    """ Add the currently selected voxels to the group by clicking the
    BOLD(Add) button.

    The Microstructure now has enough information to go on to the next
    step -- creating a Skeleton.  Although we haven't assigned
    Materials to the voxels, the voxels have been differentiated by
    virtue of being assigned to different voxel groups.  This is
    sufficient for establishing the Skeleton geometry.""",

    signal= "changed pixel group"
    ),

    TutoringItem(
    subject="Saving a Microstructure",
    comments=

    """
    In the main OOF3D window, select BOLD(Save/Microstructure) from the
    BOLD(File) menu.

    (Now click BOLD(Cancel) so that you can finish reading this
    tutorial entry.  Go back to the BOLD(Save/Microstructure) dialog
    when you're ready.)

    The file selector has a pull-down menu labelled
    BOLD(microstructure) which lets you choose which Microstructure to
    save.

    The BOLD(format) menu has three choices:

    BOLD(script): This saves the Microstructure as a Python script.
    It's a text file, so it can be edited in any text editor.  Because
    it's a Python script, it can contain any valid Python commands, so
    you could augment it in interesting and creative ways.  A data
    file saved as a script can be loaded by the BOLD(Load/Script)
    command in the BOLD(File) menu, or by the BOLD(--script) command
    line option at startup time.  If you're paranoid, you don't want
    to load scripts from untrustworthy sources, since they could
    conceivably contain malicious code.

    BOLD(ascii): This saves the Microstructure as a text file that is
    BOLD(not) a valid Python script.  It can be reloaded with the
    BOLD(Load/Data) command in the BOLD(File) menu, or by the
    BOLD(--data) command line option.  Because this file format cannot
    contain arbitrary Python commands, it is more trustworthy than the
    BOLD(script) format (for the paranoid).

    BOLD(binary): This saves the Microstructure as a binary file.
    Binary files are usually smaller and load faster than text files.
    Furthermore, they are not subject to round-off errors from
    converting numbers to text, and cannot contain arbitrary Python
    code.  Their one disadvantage is that they are not easily
    editable.  Binary data files can be loaded into OOF3D with the
    BOLD(Load/Data) command in the BOLD(File) menu.

    Select BOLD(Save/Microstructure) from the BOLD(File) menu again.
    Enter a file name, select a data format and click BOLD(OK).

    """
    ),

    TutoringItem(
    subject="Homework",
    comments=

    """So far, most of the significant operations involving
    BOLD(Microstructure)/BOLD(Voxel Selections) have been addressed.
    Topics not covered in the tutorials are covered in the manual,
    and, of course, in the tooltips.  Some relevant topics are:

    BOLD(Active Areas): This is a way of restricting OOF3D operations
    to a given set of voxels in the Microstructure.

    BOLD(Image Modification Tools): Other techniques for modifying
    Images before selecting voxels.

    BOLD(Voxel Selection Modification Tools): Techniques for modifying
    the set of currently selected voxels, in the BOLD(Voxel Selection)
    page of the main OOF3D window.
    """
    )
    ])
