Instructions on building SWIG for Windows 95/NT

Special Note : 6/8/99
---------------------
If you are using Swig with Perl, you should upgrade to the latest
release of Perl and Swig possible.   The last time I tested the
distribution it worked with ActiveState Perl (Build 517), Visual C++ 5.0,
and Windows NT 4.0 SP1 (Although I had to hack around with it a bit to
get it to work).  Good luck!

January 3, 1998

Building SWIG
=============

Instructions for Visual C++ 4.x/5.x
------------------------------------

The Visual C++ makefile has been contributed by Kevin Butler. SWIG
should be compiled from the command line using 'nmake'.  Follow these
instructions.

1.  Make sure the C++ compiler environment variables have been set by
    the 'vcvars32' script.   If you didn't enable this when you installed
    visual C++ you may have to type 'vcvars32' at the command prompt first.

2.  Copy the file 'makefile.vc' to 'makefile'.

3.  Take a look at the file 'make_win.in'.   You will need to change values
    as appropriate and decide where you want SWIG to be installed.

4.  Type 'nmake' to build SWIG.

4a. If building the runtime libraries, type 'nmake runtime'.  In order
    for this to work, you will probably need to edit the file 
    'Runtime/makefile.msc' to reflect your local installation.  If you
    don't know what the runtime libraries are or why you would use
    them, skip this step.

5.  Type 'nmake install' to install SWIG and the SWIG library.
    The SWIG installation consists of two basic parts :

           swig.exe          -  The SWIG executable.  You should put
                                this somewhere on your PATH.

           swig_lib          -  The SWIG library.   This contains code
                                that is used by SWIG during its code
                                generation.

    By default, SWIG will install itself as follows :

           c:\swig1.1\swig.exe
           c:\swig1.1\swig_lib\

    To uninstall SWIG, simply delete the swig1.1 directory.

    Note : The location of the SWIG library is hard-wired into SWIG when you
    compile.   If you move the library to a new location, you should recompile
    or set the SWIG_LIB environment variable to point to its new location.

    Note : Due to the broken command shell on Win95, you may need to type 
    'nmake install95' to properly install SWIG.

6.  To clean up, type 'nmake clean'.

7.  Read the section below about building the examples.


Instructions for Borland C++ 5.x
---------------------------------

This Makefile has been provided by Pier Giorgio Esposito.   I have tested
it with Borland C++ 5.2 on my development machine.  Please report problems
to beazley@cs.utah.edu.

1.  Copy the file 'makefile.bc' to 'makefile'

2.  Modify the file 'make_bc.in' to reflect the settings on your machine..

3.  Type 'make' to build SWIG.

4.  Type 'make install' to install SWIG for Windows-NT.

5.  Type 'make install95' to install SWIG on Windows-95.

6.  Type 'make clean' to cleanup.

Building the Examples
=====================

Since SWIG is developed under Unix, most of the examples have been implemented
and tested in that environment.  Windows makefiles are now available for
most of the examples.   However,  some of the examples don't work under
Windows and others may require a little makefile hacking (in other words,
your mileage may vary).

All of the examples are designed to be compiled and run from the MS-DOS
command prompt.  It is also possible to use SWIG from within an environment
such as Developer Studio, but the project files tend to be rather large. Given
the number of examples, I've opted to make them short and easy to build from the
command line instead.

Visual C++ :
------------

1. Edit the file 'Makefile.win.vc' to reflect the settings on your machine
   including the installed locations of SWIG, Tcl, Python, Perl, and so
   forth.

2. Copy the file 'Makefile.win.vc' to 'Makefile.win' in the top level
   directory.

3. Now, go into each example and type 'nmake /f makefile.msc target' where
   target is one of 'tcl', 'perl', or 'python'.  For example :

           nmake /f makefile.msc tcl
           nmake /f makefile.msc perl

Borland C++ 
------------
1.  Edit the file 'Makefile.win.bc' to reflect the settings on your machine
    including the locations of SWIG, Tcl, Python, Perl, Borland C++, and
    so forth.

2.  Copy the file 'Makefile.win.bc' to 'Makefile.win' in the top level

3.  To build each example, type 'make /f makefile.msc target' where
    target is one of 'tcl', 'perl', or 'python'.   For example

           make /f makefile.msc tcl
           make /f makefile.msc perl


Note : Borland support is relatively new and incomplete at this time.  Some
of the examples may not compile or work properly.  Some of the more complicated
examples such as OpenGL and GIFPlot do not contain any Borland C++ makefiles.
The 'Makefile.win.bc' file is still incomplete at this time.

I have only been able to successfully use the Borland compiler with
versions of Tcl and Perl that have also been compiled with Borland.  I
have no idea if extensions can be built to binary releases of Tcl,
Perl, or Python that have been compiled with a different compiler such
as Visual C++. (If this is possible, please send me e-mail!).


General Disclaimer
==================

I am primarily a Unix developer, but will do whatever is necessary to
make SWIG work better on non-Unix platforms.  Technical questions
about using SWIG under Windows should be addressed to the SWIG mailing
list (swig@cs.utah.edu).  Questions or bug reports about SWIG's
compilation and installation under Windows can be sent to
beazley@cs.utah.edu.

Acknowledgments
===============
The Windows port would not be possible without the contributions of SWIG
users.

John Buckman tested some very early versions of SWIG unders Windows-NT.
Kevin Butler provided the Visual C++ makefile.
Pier Giorgio Esposito provided the Borland C++ makefile.
Mark Hammond has provided useful input on all sorts of Windows-related issues.
Bob Techentin Contributed the makefile for the runtime libraries.

Dave Beazley
beazley@cs.utah.edu
January 4, 1998







