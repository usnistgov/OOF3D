# -*- python -*-
# $RCSfile: timedep.py,v $
# $Revision: 1.10.4.4 $
# $Author: langer $
# $Date: 2014/09/23 02:31:49 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.tutorials import tutorial
TutoringItem = tutorial.TutoringItem

tutorial.TutorialClass(
    subject = "Solving Time Dependent Systems",
    ordering=7,
    lessons=[
        TutoringItem(
            subject="Introduction",
            comments=
"""OOF3D can compute the time evolution of a system if:

(1) The material properties define the coefficients of at least one
time derivative in at least one active equation, and

(2) A non-static time stepping method is selected in the BOLD(Solver)
page.

In addition, it helps if at least one output quantity is selected on
the the BOLD(Scheduled Output) page.

This tutorial demonstrates how to solve a damped elasticity problem.
It assumes that you already know how to create a Microstructure,
define Material Properties, and all the other operations involved in
setting up an OOF3D problem.

"""),

        TutoringItem(
            subject="Create a Microstructure",
            comments="""
We'll first create a simple uniform microstructure.  Go to the
BOLD(Microstructure) page and click BOLD(New) to create a
Microstructure.  Use the default values for the parameters and click
BOLD(OK).
""",
            signal=("new who", "Microstructure")),

        TutoringItem(
            subject="Define a Material",
            comments="""
Go to the BOLD(Materials) page and create a BOLD(New) bulk material.

Add the following Properties to the Material:

BOLD(Mechanical:Elasticity:Isotropic) with bulk modulus 0.5 and shear
modulus 0.25.

BOLD(Mechanical:ForceDensity:ConstantForceDensity) with gx=gz=0 and
gy=-0.03.  This simulates gravity.  Since we haven't specified what
units we're using in this toy problem, we can choose whatever value we
like for g.

BOLD(Mechanical:MassDensity:ConstantMassDensity) with rho=1.0.  This
gives the material inertia and will allow us to solve F=ma.

BOLD(Mechanical:Viscosity:Isotropic) with bulk=0.07 and shear=0.25.
Viscosity has the same form as an elastic modulus, so we parametrize
it the same way.

Assign the new Material to all of the pixels in the Microstructure.
""",
            signal="materials changed in microstructure"),

        TutoringItem(
            subject="Create a Skeleton and a Mesh",
            comments="""
Go to the BOLD(Skeleton) page and create a 4x4x4 nonperiodic Skeleton.

Go to the BOLD(FE Mesh) page and create a Mesh, using the default
parameters.
""",
            signal=("new who", "Mesh")),

        TutoringItem(
            subject="Define Fields and Equations",
            comments="""
Go to the BOLD(Fields & Equations) page.

Define and activate the BOLD(Displacement) field, and activate
the BOLD(Force Balance) equation.
"""),

        TutoringItem(
            subject="Set Boundary Conditions",
            comments="""
Go to the BOLD(Boundary Conditions) page and create three boundary
conditions on the Xmin boundary.  Set the x, y, and z components of the
displacements to be zero with Dirichlet boundary conditions on this
boundary.
""",
            signal="boundary conditions changed"),

        TutoringItem(
            subject="Schedule Outputs",
            comments="""
Go to the BOLD(Scheduled Output) page.  This page controls what output
quantities will be computed while OOF3D is solving a time-dependent
system.  All of the quantities that can be computed by the
BOLD(Analysis) page are available to be computed during a time
evolution.

A Scheduled Output consists of three parts, which are displayed in the
four columns on the page.

BOLD(0.) The leftmost column contains check boxes that allow Scheduled
Outputs to be turned on and off easily. 

BOLD(1.) The next column contains the quantity to be
BOLD(Output). "Quantity" is interpreted loosely here.  It includes
quantities from the Analysis and Boundary Analysis pages, as well as
graphics window updates and mesh data files.

BOLD(2.) The third column contains the BOLD(Schedule), which
determines when the output operation takes place.

BOLD(3.) The fourth column contains the BOLD(Destination), which
determines where the output is written.
"""),

        TutoringItem(
            subject="Schedule Graphics Output",
            comments="""
We'll first add a Scheduled Output that determines how often the
BOLD(Graphics Window) will be updated.

Click the BOLD(New) button.  A dialog window will open allowing you to choose
an Output, a Schedule, and a Destination, and to give it a name for
future reference.

Set the BOLD(output) parameter to BOLD(Update Graphics) and
leave the BOLD(name) parameter set to "automatic".

Set the BOLD(scheduletype). The available types are BOLD(Aboslute)
(operations will be performed at given times), BOLD(Relative)
(operations will be performed at given relative times to the 
start of the evolution), and BOLD(Conditional) (operations take 
place when some other criteria are satsified).  Set it to
BOLD(Aboslute) now.

Set the BOLD(schedule) to be BOLD(Periodic), with a delay of 0.0
and an interval of 0.1.  The graphics window will be updated
whenver the time is 0.0+0.1*k for integer k. 

Because the BOLD(output) is set ot BOLD(Update Graphics), the only
choice for BOLD(destination) is BOLD(Graphics Window), so don't change
it.

Click BOLD(OK).

The new Output is listed in the window.  If we had given a value to
the BOLD(name) parameter in the dialog box, then that name would
appear in the Output column.  Instead, it contains the generic name,
"GraphicsUpdate".
"""),

        TutoringItem(
            subject="Schedule Data Output",
            comments="""
Now we'll define an output operation that stores the average position
of the Xmax boundary in a file. We will be averaging in both
time and space. 

Click the BOLD(New) button in the BOLD(Output) column to define a new
output operation.  This time, in the dialog box set "output" to
"Analysis".  Set the BOLD(data) group to be the value of the
displacement field. For "operation", choose "Average". For the
"domain", select "Face Boundary", set the "boundary" to "Xmax", and
leave the normal direction set to FRONT. Set the "sampling"
to be "Integrate", and use the default (automatic) integration
order.

For the schedule, set it up the same way you did for the graphics
window updates -- Absolute and Periodic, with a delay of 0.0 and an
interval of 0.1.

Now we'll set up an output stream to send this data to a file.
Change the "destination" output to be "Output Stream", and 
type a file name in the input box.

Click BOLD(OK) to create your second output.
"""),

        TutoringItem(
            subject="Schedule Data Output, continued",
            comments="""
Sometimes you'll want to save and re-use an Output definition,
especially ones that have a lot of parameters, such as those listed in
the "Analysis" submenu of the New Output dialog box.  These
outputs are the same as those performed on the BOLD(Analysis) page.
OOF3D lets you give a name to these analysis operations and refer to
them by name in either the BOLD(Analysis) page or the New Output
dialog on the BOLD(Scheduled Output) page.

Go to the BOLD(Analysis Page) and set the BOLD(Output),
BOLD(Operation), BOLD(Domain) and BOLD(Sampling) widgets for the
quantity you want to examine.  For example, to compute y displacement
averaged over the whole mesh, set BOLD(Output) to
"Field/Component/Displacement/y", set BOLD(Operation) to
"Average", set BOLD(Domain) to "Entire Mesh", and BOLD(Sampling) to
"Integrate".

Note that the available options in a given pane on this page can
depend on what has been selected in another pane. For example, if
BOLD(Operation) is set to "Direct Output", BOLD(Sampling) can't be set
to "Integrate".

To give these settings a name, click the BOLD(Create) button in the
BOLD(Named Analysis) box in the lower left corner of the page.  Either
click BOLD(OK) to accept the default name (which is "analysis"), or
click the checkbox next to the name and type a new name.  Click
BOLD(OK) to accept the new name.
""",
            signal="named analyses changed"),

        TutoringItem(
            subject="Schedule Data Output, part 3",
            comments="""
Go back to the BOLD(Scheduled Output) page.  Click on the BOLD(New)
button to create a new Output.  This time, leave "name" set to
"automatic" (uncheck the box if necessary) and set "output" to "Named
Analysis".  The name you used appears in a pull down menu for the
"analysis" parameter. 

Set the schedule to be the same as the previous outputs --
this will be the default.  Set the destination similarly --
you should set it to the same output file that you used
for the previous output.

Click BOLD(OK).  The new Output now appears in the lists.  Its name is
the name that you assigned to the Named Analyis.
""",
            signal="scheduled outputs changed"),
        
        TutoringItem(
            subject="The Solver Page",
            comments="""
Go to the BOLD(Solver) page.

The page consists of three regions.  In the BOLD(Solvers) pane you
can assign a Solver to a Subproblem and choose which Subproblems to
solve and in which order.

The BOLD(Field Initialization) pane allows you to choose how Fields
will be initialized and to apply the initializers.  It also allows an
initial BOLD(time) to be assigned to the Mesh.

At the bottom of the page are boxes for the time, the BOLD(Solve)
button itself, and a BOLD(Status) box.  The "current time" box shows
the Mesh's current time, which is determined by the time evolution.
It can be reset when Fields are initialized.

"end time" is the target time for a time-dependent solution.  You
should set it before clicking BOLD(Solve). 

The BOLD(Status) box briefly describes the state of the solution of
the current Mesh.  Clicking the BOLD(Details) button will sometimes
display a bit more information in the Message window.

"""),

        TutoringItem(
            subject="Choose a Solver",
            comments="""
The BOLD(Solvers) list contains one line, for the "default"
Subproblem that is defined on all Meshes.  If you define other
Subproblems on the BOLD(FE Mesh) page, they will also appear in the
list. 

The checkboxes in the BOLD(Solve?) column indicate whether or not OOF3D
should solve each Subproblem.  Make sure that the checkbox is checked.

(Resize this tutorial window so that you can see all the text before
going on.)

The BOLD(Solver) column shows the solution method that will be used on
each Subproblem.  If it says "<none>" that Subproblem won't be solved,
even if its BOLD(Solve?) checkbox is checked.  Click on the "default"
Subproblem line to select it, and click the BOLD(Set Solver) button
(or double-click the line).  A dialog box opens that lets you choose a
solution method.

The solver can be specified either in BOLD(Basic) mode or
BOLD(Advanced) mode.  In Basic mode, OOF3D makes many decisions for
you.  Set the "solver_mode" parameter to BOLD(Advanced).

The "time_stepper" parameter determines which time-stepping algorithm
to use.  If it's set to "Static" no time stepping will be done,
(although if the end time is greater than the start time, the system
will be solved quasistaticly).  "Uniform" takes time steps with a
fixed size, and "Adaptive" adjusts the time steps to achieve a given
accuracy.  Set "time stepper" to "Adaptive", with tolerance=0.0001,
initialstep=0.1, minstep=1.e-5, errorscaling=Absolute, and
stepper=TwoStep.  Set the TwoStep parameters to singlestep=SS22 with
both theta1 and theta2 equal to 0.5.

Leave the "nonlinear_solver" parameter set to "None".  You'd only use
a different value if you were solving a microstructure that had
nonlinear material properties.

The "symmetric_solver" parameter governs how OOF3D solves the symmetric
matrix equations that arise from discretizing the equations of motion.
Set it to "CG" (conjugate gradient) with preconditioner=ILU,
tolerance=1e-13, and max_iterations=1000.

The "asymmetric_solver" parameter governs how OOF3D solves asymmetric
matrix equations, if they arise.  This example won't create any
asymmetric matrices, so the setting of this parameter is unimportant.

Click BOLD(OK).
""",
            signal="subproblem solver changed"),

        TutoringItem(
            subject="Set Field Initializers",
            comments="""
The BOLD(Field Initialization) pane in the BOLD(Solver) page lists all
of the fields defined on the Mesh.  Displacement appears because it
was defined on the BOLD(Fields & Equations) page.  Its time
derivative, Displacement_t, appears because the Force_Balance equation
is second order in time (the material has a MassDensity property) and
we've chosen a non-static time stepping method.  If we had set
time_stepping=Static in the previous tutorial page, then
Displacement_t would not need to be initialized.

Select the "Displacement" link in the BOLD(Field Initialization) list
and click on the BOLD(Set) button, or double click on the line.  A
dialog box appears for setting the initialization method for the
components of the field.  The components can be initialized to
constant values, to functions of x, y, z, and t, or by copying from
another Mesh.  For this example, choose "XYZTFunction" and set "fx"
and "fz" to 0.0 and "fy" to 0.1*x*y*z.  Click BOLD(OK).

Initialize the time derivative field, Displacement_t, to "Constant"
with all three components set to 0.0.
""",
            signal="field initializer set"),

        TutoringItem(
            subject="Initialize Fields",
            comments="""
Assigning initializers to the fields doesn't actually initialize the
fields.  That has to be done in a separate step.  First, open a
graphics window so that you can see the effect.  The window is
displaying both a Skeleton and a Mesh, but they're exactly coincident.
Click the BOLD(Apply) button in the BOLD(Field Initialization) pane.

Notice that the Mesh nodes have moved because the displacement field
has been initialized.  To make the display easier to read, either hide
the Skeleton layer or change its color.  Light gray works well.
"""),

        TutoringItem(
            subject="Solve",
            comments="""
Type "6" into the BOLD(end time) box at the bottom of the BOLD(Solver)
page. 

Click the BOLD(Solve) button to compute the time evolution.

The progress of the solution can be monitored by observing the
BOLD(current time) field in the BOLD(Solver) page, the progress bar in
the BOLD(Activity Viewer) window, and the updates in the graphics
window.  The progress bar and the current time are updated more
frequently than the graphics window as long as the adaptive stepper is
taking steps that are smaller than the graphics update interval that
was specified on the BOLD(Scheduled Output) page.  The progress bar
also shows the time step (dt) that the adaptive stepper is currently
using.

When the solution is finished, the BOLD(Status) pane in the
BOLD(Solver) page will say "Solved".  Note that the BOLD(end time) is
now 12 and the BOLD(Solve) button has changed to a BOLD(Continue)
button.  If you want to extend the time evolution, you only have to
click BOLD(Continue).
"""),

        TutoringItem(
            subject="Animate the Solution",
            comments="""
Watching the graphics window as the solution was calculated was
possibly not very exciting because the computation was slow.  Or
perhaps you just weren't paying attention and missed it.  In either
case, you'd like to be able to replay it without repeating all of the
calculations.

Go to the graphics window, and choose BOLD(Animate) from the
BOLD(File) menu.  Click BOLD(OK) in the dialog box, and pay better
attention to the graphics window this time.
"""),

        TutoringItem(
            subject="Output Files",
            comments="""
Examine the output file that you created.  It'll be in the directory
that you were using when you started OOF3D unless you specified
another directory when you chose the file name.  Notice that each line
of data in the file is preceded by a bunch of comment lines beginning
with a '#' character.  The comments describe the contents of the data
lines.  If you had directed only one output to the file, the comments
would only appear at the top, and the file would be more readable.
"""),

        TutoringItem(
            subject="Start Over",
            comments="""
The motion of the microstructure wasn't very dramatic. Let's
change the material parameters and try again.

Go to the BOLD(Materials) page.  Select the material's Viscosity
property by clicking on it in the BOLD(Material) pane.  Click
BOLD(Parametrize) in the BOLD(Property) pane and change "shear" to
0.01.  Click BOLD(OK).  Similarly, change the y component of the Force
Density to -0.06.

Go back to the BOLD(Solver) page.  Note that the BOLD(Status) pane
says "Unsolved", because the computed solution is now invalid.  Also
note the the current time is still 6, and that the end time is still
12.  To recompute the time evolution, we need to reinitialize the
fields and the times as well.  To do that, click BOLD(Apply at time)
in the BOLD(Field Initialization) page.  In the dialog box, set "time"
to 0.0 and click BOLD(OK).  Change BOLD(end time) back to 6.

Click BOLD(Solve) again to recompute the time evolution with the new
parameters.  (Note that the solution is completely unphysical because
it's using linear elasticity with large displacements.)
"""),

        TutoringItem(
            subject="Undiscussed Topics",
            comments="""
You've finished the tutorial on time dependent systems.  The tutorial
didn't go into great detail, so please play around with the options to
see what their effects are.  (As a last resort, read the manual! It
may or may not be up to date.)  Here are some comments on a few topics
that weren't covered in the tutorial:

BOLD(Time Steps): Whether the time stepper is Uniform or Adaptive, the
step size is always adjusted so that it hits the output times
exactly. For example, if the start time is 0, the output time interval
is 1 and the uniform step size is 0.75, then the size of the first
step will be 0.75, but the size of the second step will be only 0.25,
to attain the output time of 1.0.  The third step will be 0.75 again.

BOLD(Choosing a Matrix Method): The finite element solution process
always includes the solution of a matrix equation.  OOF3D offers a
number of solution methods.  If the matrix is symmetric, the Conjugate
Gradient method (CG) is almost always the best method.  If the matrix
is not symmetric, use BiCG or GMRES instead.  These methods are all
preconditioned sparse iterative methods, meaning that they approach a
solution gradually and approximately and don't require extra memory to
store the parts of the matrix that are zero.  The preconditioner is a
way of guessing the answer beforehand so as to start the iteration
close to the solution.  The ILU preconditioner seems to work well in
most cases, but you might want to try the others if the solution is
taking a long time.

The Direct matrix method is not iterative or sparse.  It may give
better answers, but may also run out of memory if you're solving a
large problem.  It may or may not be faster than the sparse iterative
methods.

BOLD(Uniform and Adaptive Time Stepping): Uniform steppers take steps
of a constant predetermined size.  Adaptive steppers adjust the step
size to keep an error estimate below a specified tolerance.  They do
more work per step than the uniform steppers, but (a) may take fewer
steps and (b) provide some confidence that the answer is correct.  When
this tutorial was written, there was only one Adaptive time stepper in
OOF3D, TwoStep. This method uses a Uniform Stepper to take one step,
then repeats that step with two smaller steps, and compares the
results.  The choices for the "singlestep" parameter for the TwoStep
stepper are the same as the choices for the "stepper" parameter for
the Uniform stepping method.

BOLD(Error Scaling): The adaptive methods require you to set an
"errorscaling" parameter which determines how errors are compared to
the tolerance.  Relative errors are scaled by the value of the
solution, so if a component of the solution passes through zero, the
relative error will be very large, and the adaptive method will
attempt to take very small time steps (and probably fail).  Absolute
errors aren't scaled, and so will be a better choice for solutions
containing zeros, but may be too restrictive for large
values. Cross-over (XOver) errors are a sort of compromise.  If an
adaptive stepper is failing because the step size is too small, try
changing the error scaling.

BOLD(Choosing a Stepper): Forward Euler is the simplest time stepper
and has very little computational overhead, but tends to be unstable
and require very small time steps.  Its error is proportional to the
square of the time step.  Usually it's better to pick a more
sophisticated method that can take larger time steps.  Backward Euler
has little overhead and is more stable than Forward Euler, but its
error scales the same way. Crank-Nicolson has an error that scales
with the cube of the time step, so it's more accurate and doesn't have
much more overhead than Backward Euler.  Liniger and Galerkin are
variants of Crank-Nicolson.  All of the aforementioned methods are
designed for equations with only first order time derivatives.  If
solving an equation with second order time derivatives, OOF3D can use
these methods if it augments the system of equations with additional
equations for the first derivatives.  This increases the number of
equations and also makes the resulting matrices asymmetric, so CG
can't be used.

SS22 works directly on equations with second order time derivatives
without requiring auxiliary equations, so it can be used with the CG
matrix solver.

BOLD(Solving Multiple Subproblems): If more than one subproblem is
being solved with an adaptive stepper, each will use its own time
step.  If the fields in the two subproblems are changing on different
time scales, putting them in separate subproblems allows the steppers
to work more efficiently.  If the fields in one subproblem
instantaneously reach equilibrium, solve that problem with the Static
time stepping, which will compute the quasistatic solution at each
instant in time.

BOLD(Animation Options): The start time and finish time can be chosen
from any of the times at which output was computed by clicking on the
arrows on either side of the entry boxes in the the Animate dialog.
Times between those times can be entered directly in the boxes, and
interpolated solutions will be computed.  If "style" is set to "Loop"
or "Back and Forth" the animation will continue forever or until you
click the "Stop" button in the Activity Viewer window, whichever comes
first.

BOLD(Mesh Data Cache): The data for all the fields at all the nodes at
all the time steps can take up a lot of memory.  If your computer
doesn't have enough memory, you can tell OOF3D to cache this data in
temporary files on disk instead.  In the main OOF3D window, choose Mesh
Defaults/Data Cache Type in the Settings menu to set the cache to Disk
for all new meshes.  To change the cache type for an existing mesh,
use the Set Data Cache method in the Mesh Operations pane on the FE
Mesh page.
""")
        ]
)
