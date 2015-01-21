// -*- C++ -*-
// $RCSfile: petsc_preconditioner.C,v $
// $Revision: 1.11.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// *****************************************
// PETScII
// *****************************************

extern "C"
{
#include "petscksp.h"
}
#include "petsc_preconditioner.h"

// Everything is in the headers. Some preconditioners need specific options set in order
// for the solvers to be more efficient compared with the defaults
// (and some KSP solvers don't work with certain preconditioners).
// These preconditioner specific calls may be implemented here.
