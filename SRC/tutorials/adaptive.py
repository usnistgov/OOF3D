# -*- python -*-
# $RCSfile: adaptive.py,v $
# $Revision: 1.14.2.6 $
# $Author: langer $
# $Date: 2014/09/27 22:34:44 $

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

## TODO 3.1: Rewrite this so that it uses the Refine SkeletonModifier
## instead of the AMR MeshModifier.  Then re-record the GUI test for
## this tutorial.

TutorialClass(
    subject = "Adaptive Mesh Refinement",
    ordering = 6,
    lessons = [
    
    TutoringItem(
    subject="Introduction",
    comments=

    """OOF3D provides a rudimentary adaptive mesh refinement tool via
    BOLD(a Posteriori) error estimation scheme that utilizes
    BOLD(Superconvergent Patch Recovery) of BOLD(Zienkiewicz) and
    BOLD(Zhu) -- more discussion of the subject can be found in the
    OOF3D manual.

    In this tutorial, the adaptive mesh refinement will be briefly
    demonstrated.

    BOLD(NOTE:) In version 3.0 of OOF3D, adaptive mesh refinement
    only works on the default Subproblem of a Mesh.  Fields and
    Equations defined on other Subproblems will not be seen by the
    adaptive mesh machinery.
    
    """),

    TutoringItem(
    subject="Loading a Skeleton",
    comments=
    
    """Open a graphics window, if none has been opened yet, with
    the BOLD(Graphics/New) command in the BOLD(Windows) menu.

    Download the file BOLD(el_shape.mesh) from
    http://www.ctcms.nist.gov/oof/oof3d/examples, or locate it within the
    share/oof3d/examples directory in your OOF3D installation.

    A data file can be loaded from the BOLD(File) menu in the main OOF3D
    window (BOLD(File -> Load -> Data)).
    Select the example file (BOLD(el_shape.mesh)) in the file selector,
    and click BOLD(OK).
    """,
    signal = ("new who", "Skeleton")
    ),
    
    TutoringItem(
    subject="L-shaped Domain",
    comments=

    """If you have finished the tutorial for BOLD(Non-rectangular Domain),
    you should be familiar with this Mesh.
    The Mesh looks rectangular but Material has been assigned only to
    the BOLD(green) part of the Mesh, which simulates an effective
    BOLD(L)-shaped domain.
    
    Move on to the next slide.
    """ ),

    TutoringItem(
    subject="Boundary Conditions",
    comments="""The Mesh is ready to be solved.

    The applied boundary conditions (all BOLD(Dirichlet)) are:

    BOLD(1.) u_x = 0 on the BOLD(Xmin) side
    
    BOLD(2.) u_y = 0 on the BOLD(Xmin) side
    
    BOLD(3.) u_z = 0 on the BOLD(Xmin) side

    BOLD(4.) u_x = 0 on the BOLD(Ymax) side

    BOLD(5.) u_y = 0 on the BOLD(Ymax) side
    
    BOLD(6.) u_z = 0 on the BOLD(Ymax) side

    BOLD(7.) u_y = -2 on the BOLD(Xmax) side
    
    BOLD(8.) u_z = -2 on the BOLD(Xmax) side"""
    ),

    # TODO 3.0: Minor schizophrenia -- since the introduction of
    # subproblems, the "Solve" menu item sends "subproblem changed"
    # and not "mesh changed", but the adaptive mesh refinement routine
    # itself sends "mesh changed".
    TutoringItem(
    subject="Solution",
    comments=
    
    """Open the BOLD(Solver) page and just click BOLD(Solve).
    A deformed Mesh will be displayed in the graphics window.
    Note that dummy elements (BOLD(ivory) part) are BOLD(NOT) displayed
    in the deformed Mesh.

    For the clearer view, let us hide the Skeleton layer.
    Navigate to the bottom of the graphics window and find a layer
    labeled BOLD(Skeleton(skeleton)) and Uncheck the square box to
    hide the layer.

    Due to the shape of the domain, it is obvious that stresses are
    highly concentrated in the region surrounding the corner.
    It is also safe to assume that errors in this region would be higher
    than in other regions.

    Move on to the next slide to start the process for adaptive mesh
    refinement.
    """,
    signal = "subproblem changed"
    ),
    # TODO: *** Mesh Status for el_shape:skeleton:mesh ***
    # Unsolvable: Subproblem 'default' is ill-posed!
    # Equation 'Force_Balance' has no flux contributions


    TutoringItem(
    subject="Adaptive Mesh Refinement",
    comments=
    
    """Go back to the BOLD(FEMesh) page.

    Select BOLD(Adaptive Mesh Refinement).
    As of now, we have only one error estimator, BOLD(Z-Z Estimator).
    Select BOLD(L2 Error Norm) for error estimating BOLD(method).
    Select BOLD(stress), which is the only entity,
    for the BOLD(flux) parameter.
    Set BOLD(threshold) to be BOLD(10).

    For each element, an L2 error norm will be computed
    with stresses computed from the finite element solution and their
    recovered counterparts, which act as exact stresses.
    If the relative error exceeds 10 percent, the element will be refined.

    The next three parameters, BOLD(criterion), BOLD(degree) and, BOLD(alpha)
    take care of actual refinement. Don't bother with these parameters
    for this tutorial (See BOLD(skeleton) tutorial for details).

    Sometimes, refinement could create badly-shaped elements. These elements
    can be removed by turning on the BOLD(rationalize) option.

    By default, field values are transferred to the refined mesh.
    This, however, is just a
    projection of the previous solution onto the refined mesh --
    you need to re-solve the problem for improved solution.

    Leave these options as they are for now and click BOLD(OK).
    """,
    signal = "mesh changed"
    ),

    TutoringItem(
    subject="Refined Mesh",
    comments=
    
    """As expected, elements surrounding the corner have been refined.

    Now, go to the BOLD(Solver) page.
    BOLD(Solve) the problem again with the refined mesh.
    """,
    signal = "subproblem changed"
    ),

    TutoringItem(
    subject="Refine Again",
    comments=
    
    """
    Go back to the BOLD(FEMesh) page and refine the mesh again
    (just click BOLD(OK)).
    
    The corner has been refined more. For a better view, use
    BOLD(ctrl)+BOLD(.) or BOLD(Settings)->BOLD(Zoom)->BOLD(In) from
    the graphics window.

    This process (BOLD(Refine) + BOLD(Solve)) can be repeated, until
    you're satisfied.

    Thanks for trying out the tutorial.
    """,
    signal = "mesh changed"
    )
    
    ])
