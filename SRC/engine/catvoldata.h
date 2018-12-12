// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This is used to transfer data from
// CSkeletonBase::checkCategoryVolumes when measuring how well the
// category volumes code is working.

#ifndef CATVOLDATA_H
#define CATVOLDATA_H

#include <oofconfig.h>
#include <vector>
#include "common/doublevec.h"
#include "engine/cskeleton2.h"

class CategoryVolumesData {
private:
  double avgerr; 		// average per element error in volume
  double rmserr;		// rms deviation of error
  double maxerr; 		// max error overa all elements
  std::vector<int> catCounts;	// no. of voxels in each category
  DoubleVec catVolumes;		// computed volume in each category
  DoubleVec catErrors;		// total error in each category
public:
  int nCategories() const { return catCounts.size(); }
  double avgError() const { return avgerr; }
  double rmsError() const { return rmserr; }
  double maxError() const { return maxerr; }
  int catCount(int i) const { return catCounts[i]; }
  double catVolume(int i) const { return catVolumes[i]; }
  double catError(int i) const { return catErrors[i]; }
  friend class CSkeletonBase;
};

#endif // CATVOLDATA_H
