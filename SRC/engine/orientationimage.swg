// -*- C++ -*-
// $RCSfile: orientationimage.swg,v $
// $Revision: 1.2.18.2 $
// $Author: langer $
// $Date: 2013/11/08 20:44:37 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ORIENTATIONIMAGE_SWG
#define ORIENTATIONIMAGE_SWG

%module orientationimage
%include "engine/typemaps.swg"
%extern "engine/angle2color.swg"

%{
#include "engine/orientationimage.h"
#include "common/ccolor.h"
%}

class CMicrostructure;

class OrientationImage {
public:
  OrientationImage(CMicrostructure*, Angle2Color*, CColor*, CColor*);
};

#endif // ORIENTATIONIMAGE_SWG
