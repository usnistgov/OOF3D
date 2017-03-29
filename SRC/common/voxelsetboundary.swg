// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef VOXELSETBOUNDARY_SWG
#define VOXELSETBOUNDARY_SWG

%module voxelsetboundary

%{
#include <oofconfig.h>
#include "common/voxelsetboundary.h"
%}

%include "common/typemaps.swg"
%pragma(python) include="voxelsetboundary.spy"

unsigned char vox000, vox100, vox010, vox110, vox001, vox101, vox011, vox111;

const string &printSig(unsigned char);
void initializeProtoNodes();

#endif // VOXELSETBOUNDARY_SWG
