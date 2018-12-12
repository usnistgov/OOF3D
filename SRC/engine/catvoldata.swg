// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CATVOLDATA_SWG
#define CATVOLDATA_SWG

%module catvoldata
%include "engine/typemaps.swg"
%{
  #include "engine/catvoldata.h"
%}

class CategoryVolumesData {
public:
  int nCategories();
  double avgError();
  double rmsError();
  double maxError();
  int catCount(int i);
  double catVolume(int i);
  double catError(int i);
};

#endif // CATVOLDATA_SWG
