// -*- C++ -*-
// $RCSfile: crandom.swg,v $
// $Revision: 1.2.18.4 $
// $Author: langer $
// $Date: 2014/01/05 03:19:59 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This is the SWIG file for the "random.[Ch]" files. It has a name
// different from random because there's already a Python module
// called "random".
#ifndef CRANDOM_SWG
#define CRANDOM_SWG

%module crandom
%include "common/typemaps.swg"
%{
#include "common/random.h"
%}

void rndmseed(int);
double rndm();
int irndm();

%new IntVec *randomInts(int);

#endif // CRANDOM_SWG
