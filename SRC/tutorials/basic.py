# -*- python -*-
# $RCSfile: basic.py,v $
# $Revision: 1.14.18.6 $
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

TutorialClass(subject="Basics",
              ordering=0,
              lessons=[
    TutoringItem(
    subject="Introduction",
    comments=
    """This tutorial is a concise guide to the essential OOF3D components.

    It's a good idea to read through this tutorial before you venture
    into more task-specific ones, just to make yourself familiar with
    various OOF3D parts.

    To go to the next tutorial page, click on the BOLD(Next) button
    below.  Sometimes the BOLD(Next) button will be grayed out -- this
    means that you have to perform the action described in the
    tutorial page before proceeding.

    The BOLD(Back) button below will take you to the previous tutorial
    page.  The BOLD(Jump) button takes you to the highest numbered
    page that you've visited in this session.

    Use the BOLD(Save) button to save a tutorial session in a file so
    that you can resume it later.  To resume a session, load the saved
    file with the BOLD(Load Script) command in the BOLD(File) menu in
    the main OOF3D window."""
    ),

    TutoringItem(
    subject="OOF3D Terminology",
    comments=
    """OOF3D creates and manipulates a variety of data structures
    ("objects", in the lingo), which are described here briefly so
    that they can be referred to later in the tutorials.

    BOLD(Microstructure): A grid of voxels with Materials assigned to
    them. Microstructures have a fixed height, width, and depth in 
    physical units. Microstructures also contain other data structures, 
    defined below.

    BOLD(Image): Just what it sounds like -- a grid of voxels with
    colors assigned to them.  Every Image in OOF3D is assigned to a
    Microstructure. The Image and the Microstructure must have the
    same size.  A Microstructure can have many Images assigned to it.

    BOLD(Material): A collection of Properties which define the
    physical behavior of the material at a point in a Microstructure.

    BOLD(Property): Something that contributes somehow to the
    definition of a material.  Some Properties correspond directly to
    terms in a constitutive equation (eg, elasticity, thermal
    conductivity), and some contribute indirectly (eg, orientation).
    They can also be purely decorative (eg, color).

    BOLD(Skeleton): The geometry of a finite element mesh, specifying
    where the nodes, edges, and elements are, but without any further
    information.  Skeletons are created within Microstructures.  A
    single Microstructure can contain many Skeletons.

    BOLD(Mesh): A full finite element mesh, including information
    about element type, which fields are defined, which equations are
    being solved, boundary conditions, etc.

    BOLD(Subproblem): A part of a finite element mesh.  A mesh can
    contain many subproblems.  Subproblems can differ in the mesh
    elements included in them, in the fields defined on them, or the
    equations solved on them.  When a Mesh is created, a default
    Subproblem that includes all Mesh elements is created
    automatically.     
    """
    ),

    TutoringItem(
    subject="A Note on Units",
    comments=
    """OOF3D has BOLD(no) preferred set of units.  Enter data in any
    set of units that you prefer, and the output will be in those
    units.  Of course, at NIST we prefer that you use SI units
    (kilograms, meters, and seconds, etc), but if you use slugs,
    furlongs, and fortnights instead, OOF3D will not complain."""
    ),

    TutoringItem(
    subject="Launching OOF3D",
    comments=
    """ If you're reading this, you've presumably figured out how to
    launch OOF3D by typing 'oof3d' on the Unix command line.  This
    starts OOF3D in graphics mode.  To launch it without the graphical
    user interface, type

    % oof3d --text

    To list all the available options, type

    % oof3d --help

    (For convenience, you only need to type enough of an option to
    distinguish it from the other options.  "oof3d --he" is equivalent
    to "oof3d --help".)
    """
    ),

    TutoringItem(
    subject="The Main OOF3D window",
    comments=
    """ Upon launching, the main OOF3D window and a message window
    appear.

    The main window contains most of the OOF3D controls. The message
    window displays the output from OOF3D commands, the command
    history, and error messages.

    The main window features two major parts, the menu bar and the
    task page.

    The menu bar contains four menus, BOLD(File), BOLD(Settings),
    BOLD(Windows), and BOLD(Help).

    The BOLD(File) menu deals with loading and saving files and
    quitting OOF3D.

    The BOLD(Settings) menu lets you select fonts, window themes,
    and buffer sizes.

    From the BOLD(Windows) menu, one can open additional OOF3D windows
    and raise existing windows.

    The BOLD(Help) menu contains tools to help you use OOF3D and to
    help us debug it.
    """
    ),

    TutoringItem(
    subject="Task Pages",
    comments=
    """ Most of the real estate of the main OOF3D window is dedicated
    to a task page.

    There are many task pages available in OOF3D. When you first start
    OOF3D, the BOLD(Introduction) page is displayed. To open a specific
    task page, select it from the pull-down menu labelled BOLD(Task).
    The tasks are listed more-or-less in the order in which they must
    be performed when doing an OOF calculation.  The arrow buttons to
    the left and right of the BOLD(Task) menu switch to the previous
    and next tasks in the list.

    A brief description of each page is displayed when the mouse
    cursor is over the page's entry in the task menu.

    Open the BOLD(Microstructure) page by selecting
    BOLD(Microstructure) in the task menu.

    Notice that some buttons in the page are grayed out, that is, they
    are not accessible.  In OOF3D, only the buttons that are meaningful
    at the moment will be clickable. The BOLD(Delete) button, for
    instance, is useless at this point, since there's no
    Microstructure to delete."""
    ),

    TutoringItem(
    subject="Create a Microstructure",
    comments=

    """Now, create a microstructure to see what happens to the
    grayed-out buttons on the page.

    Download and unpack the file BOLD(5color.tar.gz) from
    http://www.ctcms.nist.gov/oof/oof3d/examples/, or locate the
    5color directory within the share/oof3d/examples directory in your
    OOF3D installation.  (Unpack the downloaded file with "tar -xzf
    5color.tar.gz".)  This directory contains a set of 2D image files,
    each one of which is one slice of a 3D image.

    Click the BOLD(New from Image Files) button.

    The box labeled BOLD(filenames=) in the dialog is where you tell
    OOF3D which files to load.  The topmost pull-down menu in the box
    determines how the image files are going to be specified.  We're
    going to use all the files in the directory, so leave it set to
    BOLD(Entire Directory).

    Inside the BOLD(filenames=) box is a box labeled BOLD(directory=).
    These are what you use to navigate to the folder BOLD(5color).
    You can type a name in the BOLD(Directory) field, or use the
    pull-down menu to its right to choose a parent or child directory.
    Double-clicking on a directory in the list descends into that
    directory.  You can also click the list and type the first letters
    of a file or directory name to jump to that entry.  Because you
    selected BOLD(Entire Directory), OOF3D won't let you select a file
    at the moment.

    When you've located and selected the BOLD(5color) directory, click
    the BOLD(OK) button.

    You should see that all of the buttons in the upper part of the
    Microstructure page have been turned on, and that a Microstructure
    called "5color" has been created.

    Also, if you bring up the messages window (select Messages/Message
    1 in the Windows menu, if necessary), you'll notice that it has
    logged the menu command for Microstructure creation.
    """,
        signal=("new who", "Microstructure")
    ),

    TutoringItem(
    subject="The Graphics Window",
    comments=

    """The graphics window displays Microstructures, Skeletons, and
    Meshes and their associated data.  Open a graphics window with the
    BOLD(Graphics/New) command in the BOLD(Windows) menu.

    You should see the Image BOLD(5color) displayed in the window.
    (If the image doesn't appear, try resizing the window slightly.)
    
    The graphics window is composed of five parts: a menu bar, a
    toolbox area, a canvas, and a layer list.  

    The BOLD(menu bar) at the top part of the window contains all the
    necessary menus to operate the graphics window and it works just
    like the one in the main OOF3D window.

    The BOLD(toolbox) area on the left side of the window is the home of
    the many toolboxes of OOF3D.  Toolboxes are somewhat similar to the
    task pages in the main OOF3D window but they are designed to
    perform tasks that are (mostly) driven by mouse clicks in the
    canvas area.

    Any objects that have graphical representations can be drawn on
    the BOLD(canvas) on the right side of the window.  Everything
    drawn on the canvas is part of a BOLD(display layer). These layers
    are enumerated in the BOLD(layer list) at the bottom of the
    window.  (Thin horizontal lines in the layer list correspond to
    predefined default layers -- to see the full definition of these
    layers select BOLD(List All Layers) from the BOLD(Settings) menu.)
    
    The toolbox, canvas, and layer list are separated by dividers
    which can be dragged with the mouse to change the size of the
    various parts of the window.  (The exact appearance of the
    dividers and other user interface components depends on the
    current BOLD(gtk theme), which can be changed with the
    Settings/Theme menu item in the main OOF3D window.

    """
        ),

    TutoringItem(
    subject="Activity Viewer and Progress Bars",
    comments=

    """If you're running OOF3D in threaded mode (which is the default)
    you'll be able to monitor the progress of certain activities and
    furthermore you'll be able to stop these activities at will.

    Demonstrate this feature by categorizing a new Microstructure,
    BOLD(jpeg), by voxel colors, that is, create a BOLD(voxel
    group) for each color of voxel in the Image.

    First create the microstructure by using the BOLD(New from Image
    Files) button again to load the exfiles in the folder
    BOLD(jpeg), in the BOLD(examples) directory.
    
    Open the BOLD(Image) page in the main OOF3D window.  Make sure
    that the BOLD(Microstructure) chooser at the top of the window is
    set to BOLD(jpeg), and click the BOLD(Group) button.  Click the
    BOLD(OK) button in the dialog box.

    The BOLD(Activity Viewer) window will appear.  It features a
    progress bar that lets you graphically monitor the progress of
    voxel categorization.

    While the bar is still moving, you can abort the process by
    clicking on the BOLD(Stop) button.

    Cool, isn't it?
    """
    ),

    TutoringItem(
    subject="Error Handling",
    comments=

    """Once in a while, you will encounter an error when working with
    OOF3D.  Mostly this is your own damn fault, but sometimes (rarely,
    we hope) it's ours.

    In these cases, OOF3D launches a window that explains what went
    wrong.  You must close this window before you can continue using
    any other features of OOF3D.

    From this BOLD(OOF3D Error) window, you can ignore the error by
    clicking BOLD(OK), and OOF3D will try to continue.

    If you're interested in tracking down the source of error, you can
    click the BOLD(View Traceback) button to see what really happened.
    This traceback can be saved to a file by clicking BOLD(Save
    Traceback).

    The BOLD(Report) button compiles all of the relevant information
    about the error into a file which will help us to debug the
    problem, if mailed to BOLD(oof_bugs@nist.gov).
   
    Finally, you can choose to abort the program by clicking on the
    BOLD(Abort) button.  OOF3D will give you a chance to save the
    session log file before aborting."""
    ),

    TutoringItem(
    subject="Error Handling -- continued",
    comments=
    """Generate an error by loading a script that features an
    erroneous line.

    Download the file BOLD(errorgen.log) from
    http://www.ctcms.nist.gov/oof/oof3d/examples, or locate it within the
    share/oof3d/examples directory in your OOF3D installation.
    
    Select the BOLD(Load/Script) command in the BOLD(File) menu in the
    main OOF3D window.

    In the file selector, navigate to BOLD(errorgen.log) and click
    BOLD(OK).

    Upon loading the file, you should have an BOLD(OOF3D Error) window.

    You can explore the options on the window freely, but BOLD(do not)
    click on the BOLD(Abort) button - you'll lose this tutorial session.

    None of the other OOF3D windows (not even this one) will be
    responsive until the error dialog is closed.  """
    ),

    TutoringItem(
    subject="Quitting and Restarting OOF3D",
    comments=
    
    """Almost every OOF3D window has a BOLD(Quit) command in its
    BOLD(File) menu.

    If you've executed any commands without saving them, OOF3D will ask
    if you'd like to save a log file.  
    
    The saved script can be loaded
    later with the BOLD(Load/Script) command in the BOLD(File) menu,
    or with the "--script" command line option, like this:

    % oof3d --script=myoof.log

    where "myoof.log" is the name you assigned to the log file.
    Loading the script will re-execute all the commands that you
    performed, and thus duplicate your OOF3D session.

    To recover an OOF3D session without repeating all the commands, you
    need to save and reload the data (Microstructure, Skeleton, etc.)
    instead of the commands.  This can be done with the BOLD(Save) and
    BOLD(Load/Data) menus in the BOLD(File) menu.

    Thanks for trying out this tutorial!!!""",
    )
    
    ]
              )
