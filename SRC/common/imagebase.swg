// -*- C++ -*-
// $RCSfile: imagebase.swg,v $
// $Revision: 1.1.2.4 $
// $Author: langer $
// $Date: 2014/09/27 22:33:51 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef IMAGEBASE_SWG
#define IMAGEBASE_SWG

%module imagebase
%include "common/typemaps.swg"

%{
#include "common/imagebase.h"
#include "common/coord.h"
%}

class ImageBase {
public:
  Coord size();
  ICoord sizeInPixels();
  void setSize(Coord *Point);
  void update();
};

#endif // IMAGEBASE_SWG
