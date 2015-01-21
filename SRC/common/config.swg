// -*- C++ -*-
// $RCSfile: config.swg,v $
// $Revision: 1.9.12.2 $
// $Author: langer $
// $Date: 2013/02/01 20:31:05 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CONFIG_SWG
#define CONFIG_SWG

%module config

%{
#include <oofconfig.h>

bool no_gui() {
#ifdef NO_GUI
  return true;
#else
  return false;
#endif
}

bool debug() {
#ifdef DEBUG
   return true;
#else
   return false;
#endif
}

int devel() {
#ifdef DEVEL
  return DEVEL;
#else
  return 0;
#endif
}

int petsc() {
#ifdef HAVE_PETSC
  return HAVE_PETSC;
#else
  return 0;
#endif
}

int enablempi() {
#ifdef HAVE_MPI
  return HAVE_MPI;
#else
  return 0;
#endif
}

bool enable_segmentation() {
#ifdef ENABLE_SEGMENTATION
  return true;
#else
  return false;
#endif
}

int dimension() {
#ifdef DIM
  return DIM;
#else
  return 0;
#endif
}

bool nanoHUB() {
#ifdef NANOHUB
  return true;
#else
  return false;
#endif
}

%}

bool no_gui();
int devel(); 
bool debug();
int petsc();
int enablempi();
bool enable_segmentation();
int dimension();
bool nanoHUB();

#endif // CONFIG_SWG
